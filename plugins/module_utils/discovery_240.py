#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2022 - 2025,
#   Michael Sekania &
#   Robin Gierse <robin.gierse@checkmk.com> &
#   Max Sickora <max.sickora@checkmk.com> &
#   Lars Getwan <lars.getwan@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
import time

from ansible_collections.checkmk.general.plugins.module_utils.api import CheckmkAPI
from ansible_collections.checkmk.general.plugins.module_utils.discovery import (
    HTTP_CODES,
    HTTP_CODES_BULK,
    HTTP_CODES_BULK_SC,
    HTTP_CODES_SC,
    Discovery,
)
from ansible_collections.checkmk.general.plugins.module_utils.types import (
    generate_result,
)

COMPATIBLE_MODES = [
    "new",
    "remove",
    "fix_all",
    "only_host_labels",
    "only_service_labels",
    "tabula_rasa",
    "refresh",
    "monitor_undecided_services",
]

SUPPORTED_VERSIONS = {
    "min": "2.4.0",
    "max": "2.4.0p99",
}


class ServiceDiscoveryAPI(CheckmkAPI):
    def post(self):
        mode = self.params.get("state")
        if mode not in COMPATIBLE_MODES:
            return generate_result(
                msg="State %s is not supported with this Checkmk version." % mode
            )

        if mode == "monitor_undecided_services":
            return generate_result(
                msg="State %s is only supported in bulk mode." % mode
            )

        data = {
            "host_name": self.params.get("host_name"),
            "mode": mode,
        }

        return self._fetch(
            code_mapping=HTTP_CODES,
            endpoint="domain-types/service_discovery_run/actions/start/invoke",
            data=data,
            method="POST",
            logger=self.logger,
        )


class ServiceBulkDiscoveryAPI(CheckmkAPI):
    def post(self):
        mode = self.params.get("state")
        if mode not in COMPATIBLE_MODES or mode == "refresh":
            return generate_result(
                msg="State %s is not supported with this Checkmk version." % mode
            )

        options = {
            "monitor_undecided_services": False,
            "remove_vanished_services": False,
            "update_service_labels": False,
            "update_host_labels": False,
        }

        if self.params.get("state") in ["new", "fix_all", "monitor_undecided_services"]:
            options["monitor_undecided_services"] = True
        if self.params.get("state") in ["remove", "fix_all"]:
            options["remove_vanished_services"] = True
        if self.params.get("state") in ["only_service_labels"]:
            options["update_service_labels"] = True
        if self.params.get("state") in ["new", "fix_all", "only_host_labels"]:
            options["update_host_labels"] = True

        data = {
            "hostnames": self.params.get("hosts", []),
            "options": options,
            "do_full_scan": self.params.get("do_full_scan", True),
            "bulk_size": self.params.get("bulk_size", 1),
            "ignore_errors": self.params.get("ignore_errors", True),
        }

        return self._fetch(
            code_mapping=HTTP_CODES_BULK,
            endpoint="domain-types/discovery_run/actions/bulk-discovery-start/invoke",
            data=data,
            method="POST",
        )


class ServiceCompletionAPI(CheckmkAPI):
    def get(self):
        data = {}

        return self._fetch(
            code_mapping=HTTP_CODES_SC,
            endpoint=(
                "objects/service_discovery_run/"
                + self.params.get("host_name")
                + "/actions/wait-for-completion/invoke"
            ),
            data=data,
            method="GET",
        )


class ServiceCompletionBulkAPI(CheckmkAPI):
    def get(self, job_id):
        data = {}

        return self._fetch(
            code_mapping=HTTP_CODES_BULK_SC,
            endpoint=("objects/background_job/%s" % job_id),
            data=data,
            method="GET",
        )


class Discovery240(Discovery):
    def __init__(self, module, logger):
        super().__init__(module, logger)

        self.discovery_single = ServiceDiscoveryAPI(self.module, self.logger)
        self.discovery_bulk = ServiceBulkDiscoveryAPI(self.module, self.logger)
        self.completion_single = ServiceCompletionAPI(self.module, self.logger)
        self.completion_bulk = ServiceCompletionBulkAPI(self.module, self.logger)

        self.discovery_api = self._discovery_api()
        self.service_completion_api = self._service_completion_api()

        self.supported_versions = SUPPORTED_VERSIONS

    def _discovery_api(self):
        if self.single_mode:
            return self.discovery_single

        return self.discovery_bulk

    def _service_completion_api(self):
        if self.single_mode:
            return self.completion_single

        return self.completion_bulk

    def _wait_for_completion(self, what, job_id=None):
        now = time.time()
        deadline = now + self.timeout

        if self.bulk_mode and not job_id:
            return generate_result(
                msg=(
                    "Unable to get job_id for bulk service discovery. "
                    "Will not wait for job to finish"
                ),
                failed=False,
                changed=True,
            )

        while True:
            now = time.time()
            if now > deadline:
                return generate_result(
                    msg="Timeout reached while waiting for %s discovery" % what
                )

            if self.single_mode:
                result = self.service_completion_api.get()
                # For single mode, there's a forwarding, but _fetch_url() doesn't support that.
                if result.http_code != 302:
                    break

            else:
                # For bulk mode, the completion api shows the state of the job
                result = self.service_completion_api.get(job_id)
                if not json.loads(result.content).get("extensions").get("active"):
                    break

            time.sleep(3)

        return result

    def start_discovery(self):
        if self.wait_for_previous and self.single_mode:
            # For bulk mode, it's neither possible nor necessary to wait for the previous
            # discovery, as jobs are now allowed to run in parallel
            result = self._wait_for_completion("previous")
            if result.failed:
                return result

        result = self.discovery_api.post()
        if result.failed:
            return result

        if self.wait_for_completion:
            if self.single_mode and result.http_code != 200:
                result = self._wait_for_completion("current")
            elif self.bulk_mode:
                job_id = json.loads(result.content).get("id")
                result = self._wait_for_completion("current", job_id=job_id)

        return result

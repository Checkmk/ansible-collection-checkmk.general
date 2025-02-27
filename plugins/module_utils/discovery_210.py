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
    "refresh",
    "only_host_labels",
]

SUPPORTED_VERSIONS = {
    "min": "2.1.0",
    "max": "2.1.0p99",
}


class ServiceDiscoveryAPI(CheckmkAPI):
    def post(self):
        mode = self.params.get("state")
        if mode not in COMPATIBLE_MODES:
            return generate_result(
                msg="State %s is not supported with this Checkmk version." % mode
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
        if mode not in COMPATIBLE_MODES:
            return generate_result(
                msg="State %s is not supported with this Checkmk version."
            )

        data = {
            "hostnames": self.params.get("hosts", []),
            "mode": self.params.get("state"),
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
            endpoint=("objects/service_discovery_run/" + self.params.get("host_name")),
            data=data,
            method="GET",
        )


class ServiceCompletionBulkAPI(CheckmkAPI):
    def get(self):
        data = {}

        return self._fetch(
            code_mapping=HTTP_CODES_BULK_SC,
            endpoint=("objects/discovery_run/bulk_discovery"),
            data=data,
            method="GET",
        )


class Discovery210(Discovery):
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

    def _wait_for_completion(self, what):
        now = time.time()
        deadline = now + self.timeout
        while True:
            now = time.time()
            if now > deadline:
                return generate_result(
                    msg="Timeout reached while waiting for %s discovery" % what
                )

            result = self.service_completion_api.get()

            # The completion api shows the state of the job
            if not json.loads(result.content).get("extensions").get("active"):
                break

            time.sleep(3)

        return result

    def start_discovery(self):
        if self.wait_for_previous:
            result = self._wait_for_completion("previous")
            if result.failed:
                return result

        result = self.discovery_api.post()
        if result.failed:
            return result

        if self.wait_for_completion:
            result = self._wait_for_completion("current")

        return result

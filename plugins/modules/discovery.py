#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2022, Robin Gierse <robin.gierse@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: discovery

short_description: Discover services in Checkmk.

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "0.0.1"

description:
- Discovery services within Checkmk.

extends_documentation_fragment: [checkmk.general.common]

options:
    host_name:
        description: The host who's services you want to manage. Mutualy exclusive with hosts.
        required: false
        type: str
    hosts:
        description: The list of hosts the services of which you want to manage. Mutualy exclusive with host_name
        required: false
        type: list
        elements: str
    state:
        description: The action to perform during discovery.
        type: str
        default: new
        choices: [new, remove, fix_all, refresh, tabula_rasa, only_host_labels]
    # mode:
    #     description:
    #     type: str
    #     default: single
    #     choices: [single, bulk]
    do_full_scan:
        description: The option whether to perform a full scan or not. (bulk mode only).
        type: bool
        default: True
    bulk_size:
        description: The number of hosts to be handled at once. (bulk mode only).
        type: int
        default: 1
    ignore_errors:
        description: The option whether to ignore errors in single check plugins. (bulk mode only).
        type: bool
        default: True

author:
    - Robin Gierse (@robin-checkmk)
    - Michael Sekania (@msekania)
"""

EXAMPLES = r"""
# Create a single host.
- name: "Add newly discovered services on host."
  checkmk.general.discovery:
    server_url: "http://localhost/"
    site: "my_site"
    automation_user: "automation"
    automation_secret: "$SECRET"
    host_name: "my_host"
    state: "new"
- name: "Add newly discovered services, update labels and remove vanished services on host."
  checkmk.general.discovery:
    server_url: "http://localhost/"
    site: "my_site"
    automation_user: "automation"
    automation_secret: "$SECRET"
    host_name: "my_host"
    state: "fix_all"
- name: "Add newly discovered services on hosts."
  checkmk.general.discovery:
    server_url: "http://localhost/"
    site: "my_site"
    automation_user: "automation"
    automation_secret: "$SECRET"
    host_names: "[my_host_0, my_host_1]"
    state: "new"
    mode: "bulk"
- name: "Add newly discovered services, update labels and remove vanished services on host; 3 at once"
  checkmk.general.discovery:
    server_url: "http://localhost/"
    site: "my_site"
    automation_user: "automation"
    automation_secret: "$SECRET"
    host_names: "[my_host_0, my_host_1, my_host_2, my_host_3, my_host_4, my_host_5]"
    state: "fix_all"
    mode: "bulk"
    bulk_size: 3
"""

RETURN = r"""
http_code:
    description: The HTTP code the Checkmk API returns.
    type: int
    returned: always
    sample: '200'
message:
    description: The output message that the module generates.
    type: str
    returned: always
    sample: 'Host created.'
"""

import time
import json

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.checkmk.general.plugins.module_utils.api import CheckmkAPI
from ansible_collections.checkmk.general.plugins.module_utils.types import RESULT
from ansible_collections.checkmk.general.plugins.module_utils.utils import (
    result_as_dict,
)

HTTP_CODES = {
    # http_code: (changed, failed, "Message")
    200: (True, False, "Discovery successful."),
    302: (
        True,
        False,
        "The service discovery background job has been initialized. Redirecting to the 'Wait for service discovery completion' endpoint.",
    ),
    400: (False, True, "Bad Request."),
    403: (False, True, "Forbidden: Configuration via WATO is disabled."),
    404: (False, True, "Not Found: Host could not be found."),
    406: (False, True, "Not Acceptable."),
    415: (False, True, "Unsupported Media Type."),
    500: (False, True, "General Server Error."),
}

HTTP_CODES_SC = {
    # http_code: (changed, failed, "Message")
    200: (True, False, "The service discovery has been completed."),
    302: (
        True,
        False,
        "The service discovery is still running. Redirecting to the 'Wait for completion' endpoint.",
    ),
    403: (False, True, "Forbidden: Configuration via Setup is disabled."),
    404: (False, True, "Not Found: There is no running service discovery"),
    406: (False, True, "Not Acceptable."),
    500: (False, True, "General Server Error."),
}

HTTP_CODES_BULK = {
    # http_code: (changed, failed, "Message")
    200: (True, False, "Discovery successful."),
    400: (False, True, "Bad Request."),
    403: (False, True, "Forbidden: Configuration via WATO is disabled."),
    406: (False, True, "Not Acceptable."),
    409: (False, True, "Conflict: A bulk discovery job is already active"),
    415: (False, True, "Unsupported Media Type."),
    500: (False, True, "General Server Error."),
}

HTTP_CODES_BULK_SC = {
    # http_code: (changed, failed, "Message")
    200: (True, False, "The service discovery has been completed."),
    403: (False, True, "Forbidden: Configuration via WATO is disabled."),
    404: (False, True, "Not Found: There is no running bulk_discovery job"),
    406: (False, True, "Not Acceptable."),
    500: (False, True, "General Server Error."),
}


class DiscoveryAPI(CheckmkAPI):
    def post(self):
        data = {
            "host_name": self.params.get("host_name"),
            "mode": self.params.get("state"),
        }

        return self._fetch(
            code_mapping=HTTP_CODES,
            endpoint="domain-types/service_discovery_run/actions/start/invoke",
            data=data,
            method="POST",
        )


class oldDiscoveryAPI(CheckmkAPI):
    def post(self):
        data = {
            "mode": self.params.get("state"),
        }

        return self._fetch(
            code_mapping=HTTP_CODES,
            endpoint=(
                "/objects/host/"
                + self.params.get("host_name")
                + "/actions/discover_services/invoke"
            ),
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


class BulkDiscoveryAPI(CheckmkAPI):
    def post(self):
        data = {
            "hostnames": self.params.get("host_names", []),
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


class ServiceCompletionBulkAPI(CheckmkAPI):
    def get(self):
        data = {}

        return self._fetch(
            code_mapping=HTTP_CODES_BULK_SC,
            endpoint=("objects/discovery_run/bulk_discovery"),
            data=data,
            method="GET",
        )


def run_module():
    module_args = dict(
        server_url=dict(type="str", required=True),
        site=dict(type="str", required=True),
        validate_certs=dict(type="bool", required=False, default=True),
        automation_user=dict(type="str", required=True),
        automation_secret=dict(type="str", required=True, no_log=True),
        host_name=dict(type="str", required=False),
        hosts=dict(type="list", elements="str", required=False),
        state=dict(
            type="str",
            default="new",
            choices=[
                "new",
                "remove",
                "fix_all",
                "refresh",
                "tabula_rasa",
                "only_host_labels",
            ],
        ),
        # state=dict(
        #     type="str",
        #     default="single",
        #     choices=[
        #         "single",
        #         "bulk",
        #     ],
        # ),
        do_full_scan=dict(type="bool", default=True),
        bulk_size=dict(type="int", default=1),
        ignore_errors=dict(type="bool", default=True),
    )
    module = AnsibleModule(
        argument_spec=module_args,
        mutually_exclusive=[
            ("host_name", "hosts"),
        ],
        required_one_of=[
            ("host_name", "hosts"),
        ],
        supports_check_mode=False,
    )

    result = RESULT(
        # http_code=http_code,
        msg="Nothing to be done",
        failed=False,
        changed=False,
    )

    # if module.params.get("mode") == "single":
    if "host_name" in module.params:
        discovery = DiscoveryAPI(module)
        checkmkversion = discovery.getversion()
        if checkmkversion[0] == "2" and checkmkversion[1] == "0":
            discovery = oldDiscoveryAPI(module)

        result = discovery.post()

        # If the API returns 302, check the service completion endpoint
        # until the discovery has completed successfully.
        if result.http_code == "302":
            servicecompletion = ServiceCompletionAPI(module)
            while True:
                result = servicecompletion.get()
                if result.http_code == "302":
                    break

                time.sleep(3)
    elif len(module.params.get("groups", [])) > 0:
        if module.params.get("state") == "tabula_rasa"
            result = RESULT(
                # http_code=http_code,
                msg="State 'tabula_rasa' is not supported by Bulk Discovery mode",
                failed=True,
                changed=False,
            )
            module.fail_json(**result_as_dict(result))

        bulk_discovery = BulkDiscoveryAPI(module)
        checkmkversion = bulk_discovery.getversion()
        if checkmkversion[0] == "2" and checkmkversion[1] == "0":
            result = RESULT(
                # http_code=http_code,
                msg="Bulk Discovery mode is unsupported in CMK 2.0.0",
                failed=True,
                changed=False,
            )
            module.fail_json(**result_as_dict(result))

        result = bulk_discovery.post()

        # If the API returns 200, check the service completion endpoint
        # repeat until the bulk_discovery has completed successfully (or failed).
        if result.http_code == "200":
            servicecompletion = ServiceCompletionBulkAPI(module)

            while True:
                result = servicecompletion.get()

                if not (json.loads(result.content).get("extensions").get("active")):
                    break

                time.sleep(3)

    # content of json.loads(result.content).get("extensions").get("logs").get("result") is alos quite interesting
    module.exit_json(**result_as_dict(result))


def main():
    run_module()


if __name__ == "__main__":
    main()

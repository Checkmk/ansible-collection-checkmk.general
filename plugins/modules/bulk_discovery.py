#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2022, Robin Gierse <robin.gierse@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: bulk_discovery

short_description: Bulk discover services in Checkmk.

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "0.0.1"

description:
- Bulk discovery services within Checkmk.

extends_documentation_fragment: [checkmk.general.common]

options:
    host_names:
        description: The list of hosts the services of which you want to manage.
        required: true
        type: list
        elements: str
    state:
        description: The action to perform during discovery.
        type: str
        default: new
        choices: [new, remove, fix_all, refresh, only_host_labels]
    do_full_scan:
        description: The option whether to perform a full scan or not.
        type: bool
        default: True
    bulk_size:
        description: The number of hosts to be handled at once.
        type: int
        default: 1
    ignore_errors:
        description: The option whether to ignore errors in single check plugins.
        type: bool
        default: True

author:
    - Robin Gierse (@robin-checkmk)
    - Michael Sekania (@msekania)
"""

EXAMPLES = r"""
- name: "Add newly discovered services on hosts."
  checkmk.general.bulk_discovery:
    server_url: "http://localhost/"
    site: "my_site"
    automation_user: "automation"
    automation_secret: "$SECRET"
    host_names: "[my_host_0, my_host_1]"
    state: "new"
- name: "Add newly discovered services, update labels and remove vanished services on host; 3 at once"
  checkmk.general.bulk_discovery:
    server_url: "http://localhost/"
    site: "my_site"
    automation_user: "automation"
    automation_secret: "$SECRET"
    host_names: "[my_host_0, my_host_1, my_host_2, my_host_3, my_host_4, my_host_5]"
    state: "fix_all"
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
    sample: '???...'
"""

import json
import time

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.checkmk.general.plugins.module_utils.api import CheckmkAPI
from ansible_collections.checkmk.general.plugins.module_utils.utils import (
    result_as_dict,
)

HTTP_CODES = {
    # http_code: (changed, failed, "Message")
    200: (True, False, "Discovery successful."),
    400: (False, True, "Bad Request."),
    403: (False, True, "Forbidden: Configuration via WATO is disabled."),
    406: (False, True, "Not Acceptable."),
    409: (False, True, "Conflict: A bulk discovery job is already active"),
    415: (False, True, "Unsupported Media Type."),
    500: (False, True, "General Server Error."),
}

HTTP_CODES_SC = {
    # http_code: (changed, failed, "Message")
    200: (True, False, "The service discovery has been completed."),
    403: (False, True, "Forbidden: Configuration via WATO is disabled."),
    404: (False, True, "Not Found: There is no running bulk_discovery job"),
    406: (False, True, "Not Acceptable."),
    500: (False, True, "General Server Error."),
}


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
            code_mapping=HTTP_CODES,
            endpoint="domain-types/discovery_run/actions/bulk-discovery-start/invoke",
            data=data,
            method="POST",
        )


# class oldDiscoveryAPI(CheckmkAPI):
#     def post(self):
#        data = {
#             "mode": self.params.get("state"),
#         }
#
#         return self._fetch(
#             code_mapping=HTTP_CODES,
#             endpoint=(
#                 "/objects/host/"
#                 + self.params.get("host_name")
#                 + "/actions/discover_services/invoke"
#             ),
#             data=data,
#             method="POST",
#         )


class ServiceCompletionAPI(CheckmkAPI):
    def get(self):
        data = {}

        return self._fetch(
            code_mapping=HTTP_CODES_SC,
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
        host_names=dict(type="list", elements="str", required=True),
        state=dict(
            type="str",
            default="new",
            choices=[
                "new",
                "remove",
                "fix_all",
                "refresh",
                "only_host_labels",
            ],
        ),
        do_full_scan=dict(type="bool", default=True),
        bulk_size=dict(type="int", default=1),
        ignore_errors=dict(type="bool", default=True),
    )
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=False)

    bulk_discovery = BulkDiscoveryAPI(module)
    checkmkversion = bulk_discovery.getversion()
    # if checkmkversion[0] == "2" and checkmkversion[1] == "0":
    #     bulk_discovery = oldDiscoveryAPI(module)

    result = bulk_discovery.post()

    # If the API returns 200, check the service completion endpoint
    # repeat until the bulk_discovery has completed successfully (or failed).
    if result.http_code == "200":
        servicecompletion = ServiceCompletionAPI(module)

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

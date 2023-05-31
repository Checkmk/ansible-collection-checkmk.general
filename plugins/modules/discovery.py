#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2022, Robin Gierse <robin.gierse@tribe29.com>
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

extends_documentation_fragment: [tribe29.checkmk.common]

options:
    host_name:
        description: The host who's services you want to manage.
        required: true
        type: str
    state:
        description: The action to perform during discovery.
        type: str
        default: new
        choices: [new, remove, fix_all, refresh, tabula_rasa, only_host_labels]

author:
    - Robin Gierse (@robin-tribe29)
"""

EXAMPLES = r"""
# Create a single host.
- name: "Add newly discovered services on host."
  tribe29.checkmk.discovery:
    server_url: "http://localhost/"
    site: "my_site"
    automation_user: "automation"
    automation_secret: "$SECRET"
    host_name: "my_host"
    state: "new"
- name: "Add newly discovered services, update labels and remove vanished services on host."
  tribe29.checkmk.discovery:
    server_url: "http://localhost/"
    site: "my_site"
    automation_user: "automation"
    automation_secret: "$SECRET"
    host_name: "my_host"
    state: "fix_all"
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

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.tribe29.checkmk.plugins.module_utils.api import CheckmkAPI
from ansible_collections.tribe29.checkmk.plugins.module_utils.utils import (
    result_as_dict,
)

HTTP_CODES = {
    # http_code: (changed, failed, "Message")
    200: (True, False, "Discovery successful."),
    400: (False, True, "Bad Request."),
    403: (False, True, "Forbidden: Configuration via WATO is disabled."),
    404: (False, True, "Not Found: Host could not be found."),
    406: (False, True, "Not Acceptable."),
    415: (False, True, "Unsupported Media Type."),
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


def run_module():
    module_args = dict(
        server_url=dict(type="str", required=True),
        site=dict(type="str", required=True),
        validate_certs=dict(type="bool", required=False, default=True),
        automation_user=dict(type="str", required=True),
        automation_secret=dict(type="str", required=True, no_log=True),
        host_name=dict(type="str", required=True),
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
    )
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=False)

    discovery = DiscoveryAPI(module)
    checkmkversion = discovery.getversion()
    if checkmkversion[0] == '2' and checkmkversion[1] == '0':
        discovery = oldDiscoveryAPI(module)

    result = discovery.post()

    time.sleep(3)

    module.exit_json(**result_as_dict(result))


def main():
    run_module()


if __name__ == "__main__":
    main()

#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2022, Robin Gierse <robin.gierse@tribe29.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: activation

short_description: Activate changes in Checkmk.

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "0.0.1"

description:
- Activate changes within Checkmk.
- This module only needs to be run once and not for every host. Use C(run_once).

extends_documentation_fragment: [tribe29.checkmk.common]

options:
    sites:
        description: The sites that should be activated. Omitting this option activates all sites.
        default: []
        type: raw
    force_foreign_changes:
        description: Wheather to active foreign changes.
        default: false
        type: bool

author:
    - Robin Gierse (@robin-tribe29)
"""

EXAMPLES = r"""
- name: "Activate changes on all sites."
  tribe29.checkmk.activation:
      server_url: "http://localhost/"
      site: "my_site"
      automation_user: "automation"
      automation_secret: "$SECRET"
  run_once: 'true'

- name: "Activate changes on a specific site."
  tribe29.checkmk.activation:
      server_url: "http://localhost/"
      site: "my_site"
      automation_user: "automation"
      automation_secret: "$SECRET"
      sites:
        - "my_site"
  run_once: 'true'

- name: "Activate changes including foreign changes."
  tribe29.checkmk.activation:
      server_url: "http://localhost/"
      site: "my_site"
      automation_user: "automation"
      automation_secret: "$SECRET"
      force_foreign_changes: 'true'
  run_once: 'true'
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
    sample: 'Changes activated.'
"""

import time

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        server_url=dict(type="str", required=True),
        site=dict(type="str", required=True),
        validate_certs=dict(type="bool", required=False, default=True),
        automation_user=dict(type="str", required=True),
        automation_secret=dict(type="str", required=True, no_log=True),
        sites=dict(type="raw", default=[]),
        force_foreign_changes=dict(type="bool", default=False),
    )

    result = dict(changed=False, failed=False, http_code="", msg="")

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=False)

    changed = False
    failed = False
    http_code = ""
    sites = module.params["sites"]
    if sites == {}:
        sites = []

    http_code_mapping = {
        # http_code: (changed, failed, "Message")
        200: (True, False, "Changes activated."),
        204: (True, False, "Changes activated."),
        302: (True, False, "Redirected."),
        422: (False, False, "There are no changes to be activated."),
        400: (False, True, "Bad Request."),
        401: (
            False,
            True,
            "Unauthorized: There are foreign changes, which you may not activate, or you did not use <force_foreign_changes>.",
        ),
        403: (False, True, "Forbidden: Configuration via WATO is disabled."),
        406: (False, True, "Not Acceptable."),
        409: (False, True, "Conflict: Some sites could not be activated."),
        415: (False, True, "Unsupported Media Type."),
        423: (False, True, "Locked: There is already an activation running."),
    }

    # Declare headers including authentication to send to the Checkmk API
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer %s %s"
        % (
            module.params.get("automation_user", ""),
            module.params.get("automation_secret", ""),
        ),
    }

    params = {
        "force_foreign_changes": module.params.get("force_foreign_changes", ""),
        "redirect": False,
        "sites": sites,
    }

    base_url = "%s/%s/check_mk/api/1.0" % (
        module.params.get("server_url", ""),
        module.params.get("site", ""),
    )

    api_endpoint = "/domain-types/activation_run/actions/activate-changes/invoke"
    url = base_url + api_endpoint
    response, info = fetch_url(
        module, url, module.jsonify(params), headers=headers, method="POST"
    )
    http_code = info["status"]

    # Kudos to Lars G.!
    if http_code in http_code_mapping.keys():
        changed, failed, msg = http_code_mapping[http_code]
    else:
        changed, failed, msg = (False, True, "Error calling API")

    result["msg"] = msg
    result["changed"] = changed
    result["failed"] = failed
    result["http_code"] = http_code

    if result["failed"]:
        module.fail_json(**result)

    # Work around a possible race condition in the activation process.
    # The sleep can be removed, once this is stable on Checkmk's and.
    time.sleep(3)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()

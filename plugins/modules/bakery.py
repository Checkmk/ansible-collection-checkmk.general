#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2023, Robin Gierse <robin.gierse@tribe29.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: bakery

short_description: Trigger baking and signing in the agent bakery.

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "0.21.0"

description:
- Trigger baking and signing in the agent bakery.

extends_documentation_fragment: [tribe29.checkmk.common]

options:
    sign_key_id:
        description: The id of the signing key
        required: false
        type: int

    sign_key_passphrase:
        description: The passphrase of the signing key
        required: false
        type: str

    state:
        description: State - Baked, signed or baked and signed
        choices: ["baked", "signed", "baked_signed"]
        default: "baked"
        type: str

author:
    - Max Sickora (@max-checkmk)
"""

EXAMPLES = r"""
# Bake all agents without signing, as example in a fresh installation without a signature key.
- name: "Bake all agents without signing."
  tribe29.checkmk.bakery:
    server_url: "http://localhost/"
    site: "my_site"
    automation_user: "automation"
    automation_secret: "$SECRET"
    state: "baked"
# Sign all agents.
- name: "Sign all agents."
  tribe29.checkmk.bakery:
    server_url: "http://localhost/"
    site: "my_site"
    automation_user: "automation"
    automation_secret: "$SECRET"
    sign_key_id: 1
    sign_key_passphrase: "secretkey"
    state: "signed"
# Sign and bake all agents.
- name: "Sign and Bake all agents."
  tribe29.checkmk.bakery:
    server_url: "http://localhost/"
    site: "my_site"
    automation_user: "automation"
    automation_secret: "$SECRET"
    sign_key_id: 1
    sign_key_passphrase: "secretkey"
    state: "baked_signed"
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
    sample: 'Done.'
"""

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url


def run_module():
    module_args = dict(
        server_url=dict(type="str", required=True),
        site=dict(type="str", required=True),
        validate_certs=dict(type="bool", required=False, default=True),
        automation_user=dict(type="str", required=True),
        automation_secret=dict(type="str", required=True, no_log=True),
        sign_key_id=dict(type="int", required=False),
        sign_key_passphrase=dict(type="str", required=False, no_log=True),
        state=dict(
            type="str",
            default="baked",
            choices=["baked", "signed", "baked_signed"],
            required=False,
        ),
    )

    result = dict(changed=False, failed=False, http_code="", msg="")

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=False)

    changed = False
    failed = False
    http_code = ""

    http_code_mapping = {
        # http_code: (changed, failed, "Message")
        200: (True, False, "The operation was done successfully."),
        400: (False, True, "Bad Request: Parameter or validation failure"),
        403: (False, True, "Forbidden: Configuration via WATO is disabled."),
        406: (
            False,
            True,
            "Not Acceptable: The requests accept headers can not be satisfied",
        ),
        415: (
            False,
            True,
            "Unsupported Media Type: The submitted content-type is not supported",
        ),
        500: (False, True, "General Server Error."),
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

    base_url = "%s/%s/check_mk/api/1.0" % (
        module.params.get("server_url", ""),
        module.params.get("site", ""),
    )

    action = module.params.get("state", "")

    if action == "baked":
        api_endpoint = "/domain-types/agent/actions/bake/invoke"
        params = ()

    elif action == "signed":
        api_endpoint = "/domain-types/agent/actions/sign/invoke"
        params = {
            "key_id": module.params.get("sign_key_id", ""),
            "passphrase": module.params.get("sign_key_passphrase", ""),
        }

    elif action == "baked_signed":
        api_endpoint = "/domain-types/agent/actions/bake_and_sign/invoke"
        params = {
            "key_id": module.params.get("sign_key_id", ""),
            "passphrase": module.params.get("sign_key_passphrase", ""),
        }

    url = base_url + api_endpoint
    response, info = fetch_url(
        module, url, module.jsonify(params), headers=headers, method="POST", timeout=60
    )

    http_code = info["status"]

    # Kudos to Lars G.!
    if http_code in http_code_mapping.keys():
        changed, failed, msg = http_code_mapping[http_code]
    else:
        changed, failed, msg = (
            False,
            True,
            "Error calling API. HTTP Return Code is %d" % http_code,
        )

    if failed:
        details = info.get("body", info.get("msg", "N/A"))
        msg += " Details: %s" % details

    result["msg"] = msg
    result["changed"] = changed
    result["failed"] = failed
    result["http_code"] = http_code

    if result["failed"]:
        module.fail_json(**result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()

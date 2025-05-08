#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2023, Max Sickora <max.sickora@checkmk.com>
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

extends_documentation_fragment: [checkmk.general.common]

options:
    signature_key_id:
        description: The id of the signing key
        required: false
        type: int

    signature_key_passphrase:
        description: The passphrase of the signing key
        required: false
        type: str

    state:
        description: State - Baked, signed or baked and signed
        required: true
        choices: ["baked", "signed", "baked_signed"]
        type: str

author:
    - Max Sickora (@max-checkmk)
"""

EXAMPLES = r"""
# Bake all agents without signing, as example in a fresh installation without a signature key.
- name: "Bake all agents without signing."
  checkmk.general.bakery:
    server_url: "http://myserver/"
    site: "mysite"
    automation_user: "myuser"
    automation_secret: "mysecret"
    state: "baked"
# Sign all agents.
- name: "Sign all agents."
  checkmk.general.bakery:
    server_url: "http://myserver/"
    site: "mysite"
    automation_user: "myuser"
    automation_secret: "mysecret"
    signature_key_id: 1
    signature_key_passphrase: "my_key"
    state: "signed"
# Bake and sign all agents.
- name: "Bake and sign all agents."
  checkmk.general.bakery:
    server_url: "http://myserver/"
    site: "mysite"
    automation_user: "myuser"
    automation_secret: "mysecret"
    signature_key_id: 1
    signature_key_passphrase: "my_key"
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

import time

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.checkmk.general.plugins.module_utils.api import CheckmkAPI
from ansible_collections.checkmk.general.plugins.module_utils.utils import (
    result_as_dict,
    base_argument_spec,
)


class BakeryAPI(CheckmkAPI):
    def post(self):
        if self.params.get("state", "") != "baked":
            data = {
                "key_id": self.params.get("signature_key_id", ""),
                "passphrase": self.params.get("signature_key_passphrase", ""),
            }
        else:
            data = ""

        if self.params.get("state", "") == "baked":
            action = "bake"
        if self.params.get("state", "") == "signed":
            action = "sign"
        if self.params.get("state", "") == "baked_signed":
            action = "bake_and_sign"

        return self._fetch(
            endpoint="/domain-types/agent/actions/%s/invoke" % action,
            data=data,
            method="POST",
        )


def run_module():
    argument_spec = base_argument_spec()
    argument_spec.update(
        signature_key_id=dict(type="int", required=False),
        signature_key_passphrase=dict(type="str", required=False, no_log=True),
        state=dict(
            type="str",
            choices=["baked", "signed", "baked_signed"],
            required=True,
        ),
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    bakery = BakeryAPI(module)
    result = bakery.post()

    time.sleep(3)

    module.exit_json(**result_as_dict(result))


def main():
    run_module()


if __name__ == "__main__":
    main()

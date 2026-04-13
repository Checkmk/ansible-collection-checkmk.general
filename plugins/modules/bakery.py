#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2023, Max Sickora <max.sickora@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: bakery

short_description: Trigger baking and signing in the agent bakery

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "0.21.0"

description:
- Trigger baking and signing in the agent bakery.
- Baking compiles monitoring agents for all configured hosts. Signing applies a
  cryptographic signature so that agents can be verified before installation.
- This module only works with the commercial Checkmk editions.

extends_documentation_fragment: [checkmk.general.common]

options:
    signature_key_id:
        description: The id of the signing key.
        required: false
        type: str

    signature_key_passphrase:
        description: The passphrase of the signing key.
        required: false
        type: str

    state:
        description: State - Baked, signed or baked and signed.
        required: true
        choices: ["baked", "signed", "baked_signed"]
        type: str

notes:
    - The agent bakery is only available in the commercial editions of Checkmk.
      This module will fail on Checkmk Raw (CRE).
    - Signing requires a signing key to be present in the bakery. Provide the key ID and
      passphrase when using C(state=signed) or C(state=baked_signed).

seealso:
    - plugin: checkmk.general.bakery
      plugin_type: lookup

author:
    - Max Sickora (@max-checkmk)
"""

EXAMPLES = r"""
# ---------------------------------------------------------------------------
# Baking and signing agents
# ---------------------------------------------------------------------------

- name: "Bake all agents without signing."
  checkmk.general.bakery:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    state: "baked"

- name: "Sign all agents with an existing signing key."
  checkmk.general.bakery:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    signature_key_id: 12abcd34-e56f-78gh-9101-i11213j14k15
    signature_key_passphrase: "mypassphrase"
    state: "signed"

- name: "Bake and sign all agents in one step."
  checkmk.general.bakery:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    signature_key_id: 12abcd34-e56f-78gh-9101-i11213j14k15
    signature_key_passphrase: "mypassphrase"
    state: "baked_signed"

# ---------------------------------------------------------------------------
# Using environment variables for authentication
# ---------------------------------------------------------------------------
# Connection parameters can be provided via environment variables instead of
# task parameters. The supported variables are:
#   CHECKMK_VAR_SERVER_URL, CHECKMK_VAR_SITE,
#   CHECKMK_VAR_API_USER, CHECKMK_VAR_API_SECRET,
#   CHECKMK_VAR_VALIDATE_CERTS

- name: "Bake all agents using environment variables for authentication."
  checkmk.general.bakery:
    state: "baked"
  environment:
    CHECKMK_VAR_SERVER_URL: "https://myserver/"
    CHECKMK_VAR_SITE: "mysite"
    CHECKMK_VAR_API_USER: "myuser"
    CHECKMK_VAR_API_SECRET: "mysecret"
    CHECKMK_VAR_VALIDATE_CERTS: "true"
"""

RETURN = r"""
http_code:
    description: The HTTP code the Checkmk API returns.
    type: int
    returned: always
    sample: '200'
msg:
    description: The output message that the module generates.
    type: str
    returned: always
    sample: 'Done.'
"""

import time

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.checkmk.general.plugins.module_utils.api import CheckmkAPI
from ansible_collections.checkmk.general.plugins.module_utils.utils import (
    base_argument_spec,
    result_as_dict,
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
        signature_key_id=dict(type="str", required=False),
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

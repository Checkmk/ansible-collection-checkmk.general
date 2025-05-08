#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2022, Robin Gierse <robin.gierse@checkmk.com>
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

extends_documentation_fragment: [checkmk.general.common]

options:
    redirect:
        description:
          - If set to C(true), wait for the activation to complete.
            If set to C(false), start the activation, but do not wait for it to finish.
        default: false
        type: bool
    sites:
        description: The sites that should be activated. Omitting this option activates all sites.
        default: []
        type: raw
    force_foreign_changes:
        description: Whether to active foreign changes.
        default: false
        type: bool

author:
    - Robin Gierse (@robin-checkmk)
"""

EXAMPLES = r"""
- name: "Start activation on all sites."
  checkmk.general.activation:
      server_url: "http://myserver/"
      site: "mysite"
      automation_user: "myuser"
      automation_secret: "mysecret"
  run_once: 'true'

- name: "Start activation on a specific site."
  checkmk.general.activation:
      server_url: "http://myserver/"
      site: "mysite"
      automation_user: "myuser"
      automation_secret: "mysecret"
      sites:
          - "mysite"
  run_once: 'true'

- name: "Start activation including foreign changes."
  checkmk.general.activation:
      server_url: "http://myserver/"
      site: "mysite"
      automation_user: "myuser"
      automation_secret: "mysecret"
      force_foreign_changes: 'true'
  run_once: 'true'

- name: "Activate changes including foreign changes and wait for completion."
  checkmk.general.activation:
      server_url: "http://localhost/"
      site: "mysite"
      automation_user: "automation"
      automation_secret: "$SECRET"
      redirect: 'true'
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
    sample: 'Activation started.'
"""

import time

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.checkmk.general.plugins.module_utils.api import CheckmkAPI
from ansible_collections.checkmk.general.plugins.module_utils.utils import (
    result_as_dict,
    base_argument_spec,
)

HTTP_CODES = {
    # http_code: (changed, failed, "Message")
    200: (True, False, "Activation started."),
    204: (True, False, "Activation has been completed."),
    302: (True, False, "Redirected."),
    422: (False, False, "There are no changes to be activated."),
    401: (
        False,
        True,
        "There are foreign changes, which you do not have permission to activate, or you did not use <force_foreign_changes>.",
    ),
    409: (False, True, "Some sites could not be activated."),
    423: (False, True, "There is already an activation running."),
}


class ActivationAPI(CheckmkAPI):
    def post(self):
        data = {
            "force_foreign_changes": self.params.get("force_foreign_changes"),
            "redirect": self.params.get("redirect"),
            "sites": self.params.get("sites", []),
        }

        return self._fetch(
            code_mapping=HTTP_CODES,
            endpoint="domain-types/activation_run/actions/activate-changes/invoke",
            data=data,
            method="POST",
        )


def run_module():
    argument_spec = base_argument_spec()
    argument_spec.update(
        sites=dict(type="raw", default=[]),
        force_foreign_changes=dict(type="bool", default=False),
        redirect=dict(type="bool", default=False),
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    activation = ActivationAPI(module)
    activation.headers["If-Match"] = "*"
    result = activation.post()

    time.sleep(3)

    module.exit_json(**result_as_dict(result))


def main():
    run_module()


if __name__ == "__main__":
    main()

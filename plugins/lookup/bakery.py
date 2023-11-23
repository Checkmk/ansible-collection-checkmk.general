# Copyright: (c) 2023, Max Sickora <max.sickora@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    name: bakery
    author: Max Sickora (@max-checkmk)
    version_added: "3.5.0"
    short_description: Get the bakery status of a Checkmk server
    description:
      - Returns the bakery status of a Checkmk server as a string, e.g. 'running'
    options:
      _terms:
        description: site url
        required: True
      automation_user:
        description: automation user for the REST API access
        required: True
      automation_secret:
        description: automation secret for the REST API access
        required: True
      validate_certs:
        description: Wether or not to validate TLS certificates
        type: boolean
        required: False
        default: True
    notes:
      - Like all lookups, this runs on the Ansible controller and is unaffected by other keywords such as 'become'.
        If you need to use different permissions, you must change the command or run Ansible as another user.
      - Alternatively, you can use a shell/command task that runs against localhost and registers the result.
      - The directory of the play is used as the current working directory.
"""

EXAMPLES = """
- name: "Show bakery status"
  debug:
    msg: "Bakery status is {{ bakery }}"
  vars:
    bakery: "{{ lookup('checkmk.general.bakery',
                   server_url + '/' + site,
                   validate_certs=False,
                   automation_user=automation_user,
                   automation_secret=automation_secret
               )}}"
"""

RETURN = """
  _list:
    description:
      - server bakery status
    type: list
    elements: str
"""

import json

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
from ansible_collections.checkmk.general.plugins.module_utils.lookup_api import (
    CheckMKLookupAPI,
)


class LookupModule(LookupBase):
    def run(self, terms, variables, **kwargs):
        self.set_options(var_options=variables, direct=kwargs)
        user = self.get_option("automation_user")
        secret = self.get_option("automation_secret")
        validate_certs = self.get_option("validate_certs")

        ret = []

        for term in terms:
            api = CheckMKLookupAPI(
                site_url=term,
                user=user,
                secret=secret,
                validate_certs=validate_certs,
            )

            response = json.loads(
                api.get("/domain-types/agent/actions/baking_status/invoke")
            )

            if "code" in response:
                raise AnsibleError(
                    "Received error for %s - %s: %s"
                    % (
                        response.get("url", ""),
                        response.get("code", ""),
                        response.get("msg", ""),
                    )
                )

            ret.append(response.get("result", {}).get("value").get("state"))
        return ret

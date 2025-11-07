# Copyright: (c) 2023, Max Sickora <max.sickora@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    name: bakery
    author: Max Sickora (@max-checkmk)
    version_added: "4.0.0"

    short_description: Get the bakery status of a Checkmk server

    description:
      - Returns the bakery status of a Checkmk server as a string, e.g. 'running'

    extends_documentation_fragment: [checkmk.general.common_lookup]

    notes:
      - Like all lookups, this runs on the Ansible controller and is unaffected by other keywords such as 'become'.
        If you need to use different permissions, you must change the command or run Ansible as another user.
      - Alternatively, you can use a shell/command task that runs against localhost and registers the result.
      - The directory of the play is used as the current working directory.
      - It is B(NOT) possible to assign other variables to the variables mentioned in the C(vars) section!
        This is a limitation of Ansible itself.
"""

EXAMPLES = """
- name: "Show bakery status"
  ansible.builtin.debug:
    msg: "Bakery status is {{ bakery }}"
  vars:
    bakery: "{{ lookup('checkmk.general.bakery',
                   server_url=http://myserver,
                   site=mysite,
                   validate_certs=False,
                   automation_user=automation_user,
                   automation_secret=automation_secret
               )}}"

- name: "Use variables from inventory."
  ansible.builtin.debug:
    msg: "Bakery status is {{ bakery }}"
  vars:
    checkmk_var_server_url: "http://myserver/"
    checkmk_var_site: "mysite"
    checkmk_var_automation_user: "myuser"
    checkmk_var_automation_secret: "mysecret"
    checkmk_var_validate_certs: false
    bakery: "{{ lookup('checkmk.general.bakery') }}"
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
        server_url = self.get_option("server_url")
        site = self.get_option("site")
        api_auth_type = self.get_option("api_auth_type") or "bearer"
        api_auth_cookie = self.get_option("api_auth_cookie")
        automation_user = self.get_option("automation_user")
        automation_secret = self.get_option("automation_secret")
        validate_certs = self.get_option("validate_certs")

        ret = []

        api = CheckMKLookupAPI(
            site_url=server_url + "/" + site,
            api_auth_type=api_auth_type,
            api_auth_cookie=api_auth_cookie,
            automation_user=automation_user,
            automation_secret=automation_secret,
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

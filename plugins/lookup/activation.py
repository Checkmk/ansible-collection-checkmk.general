# Copyright: (c) 2025, Robin Gierse <robin.gierse@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    name: activation
    author: Robin Gierse (@robin-checkmk)
    version_added: "6.8.0"

    short_description: Get the status of a single activation

    description:
      - Returns the status of a single activation

    options:

      _terms:
        description: activation ID to look up
        required: True

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
- name: "Show activation status"
  ansible.builtin.debug:
    msg: "Activation status is {{ activation }}"
  vars:
    activation: "{{ lookup('checkmk.general.activation',
                   my_activation_id
                   server_url=http://myserver,
                   site=mysite,
                   validate_certs=False,
                   automation_user=automation_user,
                   automation_secret=automation_secret
               )}}"

- name: "Use variables from inventory."
  ansible.builtin.debug:
    msg: "Activation status is {{ activation }}"
  vars:
    checkmk_var_server_url: "http://myserver/"
    checkmk_var_site: "mysite"
    checkmk_var_automation_user: "myuser"
    checkmk_var_automation_secret: "mysecret"
    checkmk_var_validate_certs: false
    activation: "{{ lookup('checkmk.general.activation', my_activation_id) }}"
"""

RETURN = """
  _list:
    description:
      - activation status
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
        regex_params = {}
        self.set_options(var_options=variables, direct=kwargs)
        server_url = self.get_option("server_url")
        site = self.get_option("site")
        api_auth_type = self.get_option("api_auth_type") or "bearer"
        api_auth_cookie = self.get_option("api_auth_cookie")
        automation_user = self.get_option("automation_user")
        automation_secret = self.get_option("automation_secret")
        validate_certs = self.get_option("validate_certs")

        site_url = server_url + "/" + site

        api = CheckMKLookupAPI(
            site_url=site_url,
            api_auth_type=api_auth_type,
            api_auth_cookie=api_auth_cookie,
            automation_user=automation_user,
            automation_secret=automation_secret,
            validate_certs=validate_certs,
        )

        ret = []

        for term in terms:
            # the activation_run API will return a status 404 when the job is no longer active so we better
            # use the background_job API
            response = json.loads(api.get("/objects/activation_run/%s" % term))

            if "code" in response:
                raise AnsibleError(
                    "Received error for %s - %s: %s"
                    % (
                        response.get("url", ""),
                        response.get("code", ""),
                        response.get("msg", ""),
                    )
                )

            ret.append(
                "running"
                if response.get("extensions", {}).get("is_running")
                else "finished"
            )

        return ret

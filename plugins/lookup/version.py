# Copyright: (c) 2023, Lars Getwan <lars.getwan@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    name: version
    author: Lars Getwan (@lgetwan)
    version_added: "3.1.0"

    short_description: Get the version of a Checkmk server

    description:
      - Returns the version of a Checkmk server as a string, e.g. '2.1.0p31.cre'

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
- name: "Show Checkmk version"
  debug:
    msg: "Server version is {{ version }}"
  vars:
    version: "{{ lookup('checkmk.general.version',
                   server_url=my_url,
                   site=mysite,
                   validate_certs=False,
                   api_user=myuser,
                   api_secret=mysecret
               )}}"

- name: "Use variables from inventory."
  ansible.builtin.debug:
    msg: "Server version is {{ version }}"
  vars:
    checkmk_var_server_url: "http://myserver/"
    checkmk_var_site: "mysite"
    checkmk_var_api_user: "myuser"
    checkmk_var_api_secret: "mysecret"
    checkmk_var_validate_certs: false
    attributes: "{{ lookup('checkmk.general.version') }}"
"""

RETURN = """
  _list:
    description:
      - server Checkmk version
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
        api_user = self.get_option("api_user")
        api_secret = self.get_option("api_secret")
        validate_certs = self.get_option("validate_certs")

        site_url = server_url + "/" + site

        api = CheckMKLookupAPI(
            site_url=site_url,
            api_auth_type=api_auth_type,
            api_auth_cookie=api_auth_cookie,
            api_user=api_user,
            api_secret=api_secret,
            validate_certs=validate_certs,
        )

        response = json.loads(api.get("/version"))

        if "code" in response:
            raise AnsibleError(
                "Received error for %s - %s: %s"
                % (
                    response.get("url", ""),
                    response.get("code", ""),
                    response.get("msg", ""),
                )
            )

        return [response.get("versions", {}).get("checkmk")]

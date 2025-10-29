# Copyright: (c) 2023, Lars Getwan <lars.getwan@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    name: hosts
    author: Lars Getwan (@lgetwan)
    version_added: "3.3.0"

    short_description: Get various information about a host

    description:
      - Returns a list of subhosts
      - Returns a list of hosts of the host

    options:

      effective_attributes:
        description: show all effective attributes on hosts
        type: boolean
        required: False
        default: False

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
- name: Get all hosts
  ansible.builtin.debug:
    msg: "Host: {{ item.id }} in folder {{ item.extensions.folder }}, IP: {{ item.extensions.effective_attributes.ipaddress }}"
  loop: "{{
    lookup('checkmk.general.hosts',
        effective_attributes=True,
        server_url=my_server_url,
        site=mysite,
        automation_user=myuser,
        automation_secret=mysecret,
        validate_certs=False
        )
    }}"
  loop_control:
      label: "{{ item.id }}"

- name: "Use variables from inventory."
  ansible.builtin.debug:
    msg: "Host: {{ item.id }} in folder {{ item.extensions.folder }}, IP: {{ item.extensions.effective_attributes.ipaddress }}"
  vars:
    checkmk_var_server_url: "http://myserver/"
    checkmk_var_site: "mysite"
    checkmk_var_automation_user: "myuser"
    checkmk_var_automation_secret: "mysecret"
    checkmk_var_validate_certs: false
  loop: "{{
    lookup('checkmk.general.hosts', effective_attributes=True) }}"
  loop_control:
      label: "{{ item.id }}"
"""

RETURN = """
  _list:
    description:
      - A list of hosts and their attributes
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
        effective_attributes = self.get_option("effective_attributes")
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
        parameters = {
            "effective_attributes": effective_attributes,
        }

        response = json.loads(
            api.get("/domain-types/host_config/collections/all", parameters)
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
        ret.append(response.get("value"))

        return ret

# Copyright: (c) 2023, Lars Getwan <lars.getwan@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    name: folder
    author: Lars Getwan (@lgetwan)
    version_added: "3.3.0"

    short_description: Get folder attributes

    description:
      - Returns the attributes of a folder

    options:

      _terms:
        description: complete folder path using tilde as a delimiter
        required: True

    extends_documentation_fragment: [checkmk.general.common_lookup]

    notes:
      - Like all lookups, this runs on the Ansible controller and is unaffected by other keywords such as 'become'.
        If you need to use different permissions, you must change the command or run Ansible as another user.
      - Alternatively, you can use a shell/command task that runs against localhost and registers the result.
      - The directory of the play is used as the current working directory.
      - It is B(NOT) possible to assign other variables to the variables mentioned in the C(vars) section!
        This is a limitation of Ansible itself.

    seealso:
      - module: checkmk.general.folder
      - plugin: checkmk.general.folders
        plugin_type: lookup
"""

EXAMPLES = """
- name: "Get the attributes of a single folder."
  ansible.builtin.debug:
    msg: "Extended attributes of folder /tests: {{ attributes.extensions }}"
  vars:
    attributes: "{{
      lookup('checkmk.general.folder',
             '~tests',
             server_url='https://myserver/',
             site='mysite',
             api_user='myuser',
             api_secret='mysecret',
             validate_certs=False
             )
    }}"

- name: "Iterate over multiple folders."
  ansible.builtin.debug:
    msg: "Folder {{ item.id }} has attributes: {{ item.extensions }}"
  loop: "{{
           lookup('checkmk.general.folder',
                  '~tests', '~snmp',
                  server_url='https://myserver/',
                  site='mysite',
                  api_user='myuser',
                  api_secret='mysecret',
                  validate_certs=False
                  )
         }}"
  loop_control:
    label: "{{ item.id }}"

# ---------------------------------------------------------------------------
# Using variables from inventory
# ---------------------------------------------------------------------------
# Connection parameters can be provided via inventory variables instead of
# lookup parameters. The supported variables are:
#   checkmk_var_server_url, checkmk_var_site,
#   checkmk_var_api_user, checkmk_var_api_secret,
#   checkmk_var_validate_certs

- name: "Get folder attributes using inventory variables."
  ansible.builtin.debug:
    msg: "Extended attributes of folder /tests: {{ attributes.extensions }}"
  vars:
    checkmk_var_server_url: "https://myserver/"
    checkmk_var_site: "mysite"
    checkmk_var_api_user: "myuser"
    checkmk_var_api_secret: "mysecret"
    checkmk_var_validate_certs: false
    attributes: "{{ lookup('checkmk.general.folder', '~tests') }}"
"""

RETURN = """
  _list:
    description:
      - A dict of attributes of the folder if you query a single folder.
      - A list of dicts of attributes of the folders if you query multiple folders.
    type: list
    elements: dict
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

        ret = []

        for term in terms:
            response = json.loads(
                api.get("/objects/folder_config/" + term.replace("/", "~"))
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
            ret.append(response)

        return ret

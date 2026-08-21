# Copyright: (c) 2025, Lars Getwan <lars.getwan@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# This code was originally authored by Atruvia AG (https://atruvia.de/)
# and subsequently modified by Checkmk.
# Thank you so much for donating this code!

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    name: dcd
    author: Lars Getwan (@lgetwan)
    version_added: "8.4.0"

    short_description: Get DCD connection attributes

    description:
      - Returns the attributes of a Dynamic Host Management (DCD) connection in Checkmk.

    options:

      _terms:
        description:
          - One or more DCD connection IDs, either as separate terms or as a single list.
        required: True
        type: list
        elements: str

    extends_documentation_fragment: [checkmk.general.common_lookup]

    notes:
      - Like all lookups, this runs on the Ansible controller and is unaffected by other keywords such as 'become'.
        If you need to use different permissions, you must change the command or run Ansible as another user.
      - Alternatively, you can use a shell/command task that runs against localhost and registers the result.
      - The directory of the play is used as the current working directory.
      - It is B(NOT) possible to assign other variables to the variables mentioned in the C(vars) section!
        This is a limitation of Ansible itself.

    seealso:
      - module: checkmk.general.dcd
      - name: "Dynamic host management: The official user guide."
        description: "The official user guide on Dynamic Host Management (DCD)."
        link: "https://docs.checkmk.com/latest/en/dcd.html"
"""

EXAMPLES = """
- name: "Get the attributes of a DCD connection."
  ansible.builtin.debug:
    msg: "Attributes of DCD connection: {{ attributes }}"
  vars:
    attributes: "{{
      lookup('checkmk.general.dcd',
        'my_dcd_connection',
        server_url='https://myserver',
        site='mysite',
        api_user='myuser',
        api_secret='mysecret',
        validate_certs=False
      )
    }}"

# ---------------------------------------------------------------------------
# Using variables from inventory
# ---------------------------------------------------------------------------
# Connection parameters can be provided via inventory variables instead of
# lookup parameters. The supported variables are:
#   checkmk_var_server_url, checkmk_var_site,
#   checkmk_var_api_user, checkmk_var_api_secret,
#   checkmk_var_validate_certs

- name: "Get DCD connection attributes using inventory variables."
  ansible.builtin.debug:
    msg: "Attributes of DCD connection: {{ attributes }}"
  vars:
    checkmk_var_server_url: "https://myserver"
    checkmk_var_site: "mysite"
    checkmk_var_api_user: "myuser"
    checkmk_var_api_secret: "mysecret"
    checkmk_var_validate_certs: false
    attributes: "{{ lookup('checkmk.general.dcd', 'my_dcd_connection') }}"
"""

RETURN = """
  _list:
    description:
      - A list of dicts of attributes of the DCD connection(s).
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

        api = CheckMKLookupAPI(
            server_url=server_url,
            site=site,
            api_auth_type=api_auth_type,
            api_auth_cookie=api_auth_cookie,
            api_user=api_user,
            api_secret=api_secret,
            validate_certs=validate_certs,
        )

        ret = []

        for term in self._flatten(terms):
            response = json.loads(api.get("/objects/dcd/" + term))

            if "code" in response:
                raise AnsibleError(
                    "Received error for %s - %s: %s"
                    % (
                        response.get("url", ""),
                        response.get("code", ""),
                        response.get("msg", ""),
                    )
                )

            # 'dcd_id' is the identifier of the domain object itself, not part
            # of its extensions. Carry it over, so the naming matches the
            # 'dcd_config.dcd_id' option of the checkmk.general.dcd module.
            connection = response.get("extensions", {})
            connection["dcd_id"] = response.get("id")

            ret.append(connection)

        return ret

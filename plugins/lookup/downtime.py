# Copyright: (c) 2025, Lars Getwan <lars.getwan@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    name: downtime
    author: Lars Getwan (@lgetwan)
    version_added: "6.7.0"

    short_description: Show a downtime identified by its ID

    description:
      - Returns the downtime(s) with the given ID.

    options:

      _terms:
        description: One or more downtime IDs.
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
      - module: checkmk.general.downtime
      - plugin: checkmk.general.downtimes
        plugin_type: lookup
"""

EXAMPLES = """
- name: "Get the downtime with ID 42."
  ansible.builtin.debug:
    msg: "Downtime: {{ downtime }}"
  vars:
    downtime: "{{
      lookup('checkmk.general.downtime',
        '42',
        server_url='https://myserver/',
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

- name: "Get a downtime by ID using inventory variables."
  ansible.builtin.debug:
    msg: "Downtime: {{ downtime }}"
  vars:
    checkmk_var_server_url: "https://myserver/"
    checkmk_var_site: "mysite"
    checkmk_var_api_user: "myuser"
    checkmk_var_api_secret: "mysecret"
    checkmk_var_validate_certs: false
    downtime: "{{ lookup('checkmk.general.downtime', '42') }}"
"""

RETURN = """
  _list:
    description:
      - The downtime object(s) matching the given ID(s).
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
        api_user = self.get_option("api_user")
        api_secret = self.get_option("api_secret")
        validate_certs = self.get_option("validate_certs")

        api = CheckMKLookupAPI(
            site_url=server_url + "/" + site,
            api_user=api_user,
            api_secret=api_secret,
            validate_certs=validate_certs,
        )

        ret = []
        for term in terms:
            # Query by the 'id' column so no site_id has to be supplied. The
            # object endpoint (/objects/downtime/{id}) would require a site_id.
            query = json.dumps({"op": "=", "left": "id", "right": str(term)})
            response = json.loads(
                api.get(
                    "/domain-types/downtime/collections/all",
                    {"query": query},
                )
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

            ret += response.get("value", [])

        return ret

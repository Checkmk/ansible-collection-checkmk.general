# Copyright: (c) 2025, Lars Getwan <lars.getwan@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    name: bi_packs
    author: Lars Getwan (@lgetwan)
    version_added: "8.6.0"

    short_description: Get all BI packs

    description:
      - Returns the attributes of all BI packs of a Checkmk site.

    extends_documentation_fragment: [checkmk.general.common_lookup]

    notes:
      - Like all lookups, this runs on the Ansible controller and is unaffected by other keywords such as 'become'.
        If you need to use different permissions, you must change the command or run Ansible as another user.
      - Alternatively, you can use a shell/command task that runs against localhost and registers the result.
      - The directory of the play is used as the current working directory.
      - It is B(NOT) possible to assign other variables to the variables mentioned in the C(vars) section!
        This is a limitation of Ansible itself.
      - Checkmk has no endpoint that returns several BI packs at once, so this lookup
        sends one request for the list of packs and one for each pack.
      - C(rules) and C(aggregations) of each pack hold the ids of its rules and
        aggregations. Use the P(checkmk.general.bi_rules#lookup) and
        P(checkmk.general.bi_aggregations#lookup) lookups to get the objects.

    seealso:
      - module: checkmk.general.bi_pack
      - plugin: checkmk.general.bi_pack
        plugin_type: lookup
      - plugin: checkmk.general.bi_rules
        plugin_type: lookup
      - plugin: checkmk.general.bi_aggregations
        plugin_type: lookup
"""

EXAMPLES = """
- name: "Get all BI packs."
  ansible.builtin.debug:
    msg: "BI pack {{ item.id }} has the rules {{ item.rules }}."
  loop: "{{
    lookup('checkmk.general.bi_packs',
      server_url='https://myserver',
      site='mysite',
      api_user='myuser',
      api_secret='mysecret',
      validate_certs=False
    )
  }}"
  loop_control:
    label: "{{ item.id }}"

- name: "Use variables outside the module call."
  ansible.builtin.debug:
    msg: "BI pack {{ item.id }}: {{ item.title }}"
  loop: "{{ lookup('checkmk.general.bi_packs') }}"
  loop_control:
    label: "{{ item.id }}"
  vars:
    checkmk_var_server_url: "https://myserver"
    checkmk_var_site: "mysite"
    checkmk_var_api_user: "myuser"
    checkmk_var_api_secret: "mysecret"
"""

RETURN = """
  _list:
    description:
      - The attributes of all BI packs of the site.
      - C(rules) and C(aggregations) hold the ids of each pack's rules and
        aggregations, not the objects.
    type: list
    elements: dict
"""

import json

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
from ansible_collections.checkmk.general.plugins.module_utils.bi import (
    collection_ids,
    pack_attributes,
)
from ansible_collections.checkmk.general.plugins.module_utils.lookup_api import (
    CheckMKLookupAPI,
)


def _get(api, endpoint):
    response = json.loads(api.get(endpoint))

    if "code" in response:
        raise AnsibleError(
            "Received error for %s - %s: %s"
            % (
                response.get("url", ""),
                response.get("code", ""),
                response.get("msg", ""),
            )
        )

    return response


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

        # The collection reports its packs as links rather than as objects,
        # and there is no bulk endpoint, so fetch them one by one.
        packs = _get(api, "/domain-types/bi_pack/collections/all")

        return [
            [
                pack_attributes(_get(api, "/objects/bi_pack/" + pack_id))
                for pack_id in collection_ids(packs)
            ]
        ]

# Copyright: (c) 2025, Lars Getwan <lars.getwan@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    name: bi_rules
    author: Lars Getwan (@lgetwan)
    version_added: "8.4.0"

    short_description: Get the ids of all BI rules of a BI pack

    description:
      - Returns the ids of all BI rules of a BI pack.
      - Checkmk reports a pack's rules as links rather than as objects, and has no
        bulk endpoint for them, so this plugin returns ids. Pass them to the
        M(checkmk.general.bi_rule) lookup to get the objects themselves.

    options:

      pack_id:
        description: The ID of the BI pack.
        required: True
        type: str

    extends_documentation_fragment: [checkmk.general.common_lookup]

    notes:
      - Like all lookups, this runs on the Ansible controller and is unaffected by other keywords such as 'become'.
        If you need to use different permissions, you must change the command or run Ansible as another user.
      - Alternatively, you can use a shell/command task that runs against localhost and registers the result.
      - The directory of the play is used as the current working directory.
      - It is B(NOT) possible to assign other variables to the variables mentioned in the C(vars) section!
        This is a limitation of Ansible itself.
      - The Checkmk API has no endpoint to list BI rules across all BI packs, so a
        I(pack_id) is required. Use the M(checkmk.general.bi_packs) lookup to discover pack IDs.
      - There is no bulk endpoint for BI rules either, so hydrating every id costs one
        request per object. That is left to the caller rather than done here.

    seealso:
      - module: checkmk.general.bi_rule
      - plugin: checkmk.general.bi_rule
        plugin_type: lookup
      - plugin: checkmk.general.bi_packs
        plugin_type: lookup
"""

EXAMPLES = """
- name: "Get all BI rules of a BI pack."
  ansible.builtin.debug:
    msg: "BI rules: {{ items }}"
  vars:
    items: "{{
      lookup('checkmk.general.bi_rules',
        pack_id='default',
        server_url='https://myserver',
        site='mysite',
        api_user='myuser',
        api_secret='mysecret',
        validate_certs=False
      )
    }}"

- name: "Get the BI rules themselves, by feeding the ids to the singular lookup."
  ansible.builtin.debug:
    msg: "BI rules: {{ items }}"
  vars:
    checkmk_var_server_url: "https://myserver"
    checkmk_var_site: "mysite"
    checkmk_var_api_user: "myuser"
    checkmk_var_api_secret: "mysecret"
    items: "{{ lookup('checkmk.general.bi_rule',
                 lookup('checkmk.general.bi_rules', pack_id='default')) }}"

- name: "Get all BI rules of every BI pack."
  ansible.builtin.debug:
    msg: "BI rules of pack {{ item }}: {{ lookup('checkmk.general.bi_rules', pack_id=item) }}"
  loop: "{{ lookup('checkmk.general.bi_packs') }}"
  vars:
    checkmk_var_server_url: "https://myserver"
    checkmk_var_site: "mysite"
    checkmk_var_api_user: "myuser"
    checkmk_var_api_secret: "mysecret"
"""

RETURN = """
  _list:
    description:
      - The ids of all BI rules of the BI pack.
      - Pass these to the M(checkmk.general.bi_rule) lookup to get the objects.
    type: list
    elements: str
"""

import json

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
from ansible_collections.checkmk.general.plugins.module_utils.bi import member_ids
from ansible_collections.checkmk.general.plugins.module_utils.lookup_api import (
    CheckMKLookupAPI,
)


class LookupModule(LookupBase):
    def run(self, terms, variables, **kwargs):
        self.set_options(var_options=variables, direct=kwargs)
        pack_id = self.get_option("pack_id")
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

        # There is no collection endpoint for BI rules. The pack endpoint
        # reports them, but as links rather than as objects.
        response = json.loads(api.get("/objects/bi_pack/" + pack_id))

        if "code" in response:
            raise AnsibleError(
                "Received error for %s - %s: %s"
                % (
                    response.get("url", ""),
                    response.get("code", ""),
                    response.get("msg", ""),
                )
            )

        return [member_ids(response, "rules")]

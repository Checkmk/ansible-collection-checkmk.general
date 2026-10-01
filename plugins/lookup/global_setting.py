# Copyright: (c) 2026, Lars Getwan <lars.getwan@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    name: global_setting
    author: Lars Getwan (@lgetwan)
    version_added: "8.6.0"
    short_description: Get the value of a global setting
    description:
      - Returns the value of one or more global settings, in the same
        representation the M(checkmk.general.global_setting) module accepts,
        i.e. as shown in the Checkmk GUI.
      - Without I(site_id), the central value is returned. With I(site_id), the
        value that applies to that site connection is returned.
    options:
      _terms:
        description:
          - One or more internal names of global settings, e.g. C(log_levels).
        required: True
        type: list
        elements: str
      site_id:
        description:
          - The ID of a site connection. When set, the site-specific view of the
            setting is returned.
        required: False
        type: str
      full:
        description:
          - When C(true), return a dictionary with the keys C(varname),
            C(site_id), C(title), C(origin) and C(value) instead of only the
            value. C(origin) tells whether the value is the built-in default
            (C(factory)), configured centrally (C(global)) or overridden for the
            site (C(site)).
        required: False
        type: bool
        default: False
    extends_documentation_fragment: [checkmk.general.common_lookup]
    notes:
      - The global settings endpoints belong to the internal REST API of
        Checkmk and are only available in Checkmk versions that ship them.
      - Like all lookups, this runs on the Ansible controller and is unaffected by other keywords such as 'become'.
        If you need to use different permissions, you must change the command or run Ansible as another user.
      - Alternatively, you can use a shell/command task that runs against localhost and registers the result.
      - The directory of the play is used as the current working directory.
      - It is B(NOT) possible to assign other variables to the variables mentioned in the C(vars) section!
        This is a limitation of Ansible itself.
    seealso:
      - module: checkmk.general.global_setting
"""

EXAMPLES = """
- name: "Show the central log levels."
  ansible.builtin.debug:
    msg: "{{ lookup('checkmk.general.global_setting',
               'log_levels',
               server_url='https://myserver',
               site='mysite',
               api_user='myuser',
               api_secret='mysecret') }}"

- name: "Show where the log levels of a remote site come from."
  ansible.builtin.debug:
    msg: "{{ lookup('checkmk.general.global_setting',
               'log_levels',
               site_id='remote1',
               full=true,
               server_url='https://myserver',
               site='mysite',
               api_user='myuser',
               api_secret='mysecret') }}"
"""

RETURN = """
  _list:
    description:
      - The value of each requested setting, or a dictionary with details
        if I(full) is set.
    type: list
    elements: raw
"""

import json

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
from ansible_collections.checkmk.general.plugins.module_utils.global_settings import (
    internal_api_url,
    setting_endpoint,
    ui_from_setting,
)
from ansible_collections.checkmk.general.plugins.module_utils.lookup_api import (
    CheckMKLookupAPI,
)


class LookupModule(LookupBase):
    def run(self, terms, variables, **kwargs):
        self.set_options(var_options=variables, direct=kwargs)
        site_id = self.get_option("site_id")
        full = self.get_option("full")

        api = CheckMKLookupAPI(
            server_url=self.get_option("server_url"),
            site=self.get_option("site"),
            api_auth_type=self.get_option("api_auth_type") or "bearer",
            api_auth_cookie=self.get_option("api_auth_cookie"),
            api_user=self.get_option("api_user"),
            api_secret=self.get_option("api_secret"),
            validate_certs=self.get_option("validate_certs"),
        )
        api.url = internal_api_url(api.url)

        ret = []
        for term in self._flatten(terms):
            response = json.loads(api.get("/" + setting_endpoint(term, site_id)))
            if "code" in response:
                raise AnsibleError(
                    "Received error for %s - %s: %s"
                    % (
                        response.get("url", ""),
                        response.get("code", ""),
                        response.get("msg", ""),
                    )
                )
            setting = ui_from_setting(response)
            ret.append(setting if full else setting["value"])
        return ret

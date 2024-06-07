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

    options:

      server_url:
        description: URL of the Checkmk server
        required: True
        vars:
          - name: ansible_lookup_checkmk_server_url
        env:
          - name: ANSIBLE_LOOKUP_CHECKMK_SERVER_URL
        ini:
          - section: checkmk_lookup
            key: server_url

      site:
        description: Site name.
        required: True
        vars:
          - name: ansible_lookup_checkmk_site
        env:
          - name: ANSIBLE_LOOKUP_CHECKMK_SITE
        ini:
          - section: checkmk_lookup
            key: site

      automation_user:
        description: Automation user for the REST API access.
        required: True
        vars:
          - name: ansible_lookup_checkmk_automation_user
        env:
          - name: ANSIBLE_LOOKUP_CHECKMK_AUTOMATION_USER
        ini:
          - section: checkmk_lookup
            key: automation_user

      automation_secret:
        description: Automation secret for the REST API access.
        required: True
        vars:
          - name: ansible_lookup_checkmk_automation_secret
        env:
          - name: ANSIBLE_LOOKUP_CHECKMK_AUTOMATION_SECRET
        ini:
          - section: checkmk_lookup
            key: automation_secret

      validate_certs:
        description: Whether or not to validate TLS certificates.
        type: boolean
        required: False
        default: True
        vars:
          - name: ansible_lookup_checkmk_validate_certs
        env:
          - name: ANSIBLE_LOOKUP_CHECKMK_VALIDATE_CERTS
        ini:
          - section: checkmk_lookup
            key: validate_certs

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

- name: "Use variables outside the module call."
  ansible.builtin.debug:
    msg: "Bakery status is {{ bakery }}"
  vars:
    ansible_lookup_checkmk_server_url: "http://myserver/"
    ansible_lookup_checkmk_site: "mysite"
    ansible_lookup_checkmk_automation_user: "myuser"
    ansible_lookup_checkmk_automation_secret: "mysecret"
    ansible_lookup_checkmk_validate_certs: false
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
        user = self.get_option("automation_user")
        secret = self.get_option("automation_secret")
        validate_certs = self.get_option("validate_certs")

        ret = []

        api = CheckMKLookupAPI(
            site_url=server_url + "/" + site,
            user=user,
            secret=secret,
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

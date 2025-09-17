# Copyright: (c) 2023, Lars Getwan <lars.getwan@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    name: ldap_connection
    author: Lars Getwan (@lgetwan)
    version_added: "5.3.0"

    short_description: Show the configuration of an ldap connection

    description:
      - Returns the configuration of an ldap connection

    options:

      _terms:
        description: ldap connection ID
        required: True

      server_url:
        description: URL of the Checkmk server.
        required: True
        vars:
          - name: checkmk_var_server_url
          - name: ansible_lookup_checkmk_server_url
        env:
          - name: CHECKMK_VAR_SERVER_URL
          - name: ANSIBLE_LOOKUP_CHECKMK_SERVER_URL
        ini:
          - section: checkmk_lookup
            key: server_url

      site:
        description: Site name.
        required: True
        vars:
          - name: checkmk_var_site
          - name: ansible_lookup_checkmk_site
        env:
          - name: CHECKMK_VAR_SITE
          - name: ANSIBLE_LOOKUP_CHECKMK_SITE
        ini:
          - section: checkmk_lookup
            key: site

      automation_user:
        description: Automation user for the REST API access.
        required: True
        vars:
          - name: checkmk_var_automation_user
          - name: ansible_lookup_checkmk_automation_user
        env:
          - name: CHECKMK_VAR_AUTOMATION_USER
          - name: ANSIBLE_LOOKUP_CHECKMK_AUTOMATION_USER
        ini:
          - section: checkmk_lookup
            key: automation_user

      automation_secret:
        description: Automation secret for the REST API access.
        required: True
        vars:
          - name: checkmk_var_automation_secret
          - name: ansible_lookup_checkmk_automation_secret
        env:
          - name: CHECKMK_VAR_AUTOMATION_SECRET
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
          - name: checkmk_var_validate_certs
          - name: ansible_lookup_checkmk_validate_certs
        env:
          - name: CHECKMK_VAR_VALIDATE_CERTS
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
- name: Get a site with a particular ldap connection id
  ansible.builtin.debug:
    msg: "ldap connection: {{ extensions }}"
  vars:
    extensions: "{{
      lookup('checkmk.general.ldap_connection',
        'my_ldap_connection',
        server_url=server_url,
        site=site,
        automation_user=automation_user,
        automation_secret=automation_secret,
        validate_certs=False
      )
    }}"

- name: "Use variables from inventory."
  ansible.builtin.debug:
    msg: "ldap connection: {{ extensions }}"
  vars:
    checkmk_var_server_url: "http://myserver/"
    checkmk_var_site: "mysite"
    checkmk_var_automation_user: "myuser"
    checkmk_var_automation_secret: "mysecret"
    checkmk_var_validate_certs: false
    attributes: "{{ lookup('checkmk.general.ldap_connection', 'my_ldap_connection') }}"
"""

RETURN = """
  _list:
    description:
      - The details of a particular ldap connection
    type: list
    elements: str
"""

import json

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
from ansible_collections.checkmk.general.plugins.module_utils.ldap import compress_recursive
from ansible_collections.checkmk.general.plugins.module_utils.lookup_api import CheckMKLookupAPI


class LookupModule(LookupBase):
    def run(self, terms, variables, **kwargs):
        self.set_options(var_options=variables, direct=kwargs)
        server_url = self.get_option("server_url")
        site = self.get_option("site")
        user = self.get_option("automation_user")
        secret = self.get_option("automation_secret")
        validate_certs = self.get_option("validate_certs")

        site_url = server_url + "/" + site

        api = CheckMKLookupAPI(
            site_url=site_url,
            user=user,
            secret=secret,
            validate_certs=validate_certs,
        )

        ret = []

        for term in terms:
            response = json.loads(api.get("/objects/ldap_connection/" + term))

            if "code" in response:
                raise AnsibleError(
                    "Received error for %s - %s: %s"
                    % (
                        response.get("url", ""),
                        response.get("code", ""),
                        response.get("msg", ""),
                    )
                )

            ret.append(compress_recursive(response.get("extensions", {})))

        # return log
        return ret

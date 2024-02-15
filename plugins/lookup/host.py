# Copyright: (c) 2023, Lars Getwan <lars.getwan@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    name: host
    author: Lars Getwan (@lgetwan)
    version_added: "3.3.0"

    short_description: Get host attributes

    description:
      - Returns the attributes of a host

    options:

      _terms:
        description: host name
        required: True

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

      effective_attributes:
        description: show all effective attributes on hosts
        type: boolean
        required: False
        default: False

    notes:
      - Like all lookups, this runs on the Ansible controller and is unaffected by other keywords such as 'become'.
        If you need to use different permissions, you must change the command or run Ansible as another user.
      - Alternatively, you can use a shell/command task that runs against localhost and registers the result.
      - The directory of the play is used as the current working directory.
"""

EXAMPLES = """
- name: Get the attributes of host example.com
  ansible.builtin.debug:
    msg: "Attributes of host example: {{ attributes }}"
  vars:
    attributes: "{{
                    lookup('checkmk.general.host',
                        'example.com',
                        effective_attributes=True,
                        server_url=my_server_url,
                        site=my_site,
                        automation_user=my_user,
                        automation_secret=my_secret,
                        validate_certs=False
                        )
                 }}"

- name: "Use variables outside the module call."
  ansible.builtin.debug:
    msg: "Attributes of host example: {{ attributes }}"
  vars:
    ansible_lookup_checkmk_server_url: "{{ checkmk_var_server_url }}"
    ansible_lookup_checkmk_site: "{{ outer_item.site }}"
    ansible_lookup_checkmk_automation_user: "{{ checkmk_var_automation_user }}"
    ansible_lookup_checkmk_automation_secret: "{{ checkmk_var_automation_secret }}"
    ansible_lookup_checkmk_validate_certs: false
    attributes: "{{ lookup('checkmk.general.host', 'example.com', effective_attributes=True) }}"
"""

RETURN = """
  _list:
    description:
      - A list of dicts of attributes of the host(s)
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

        parameters = {
            "effective_attributes": effective_attributes,
        }

        for term in terms:
            api_endpoint = "/objects/host_config/" + term

            response = json.loads(api.get("/objects/host_config/" + term, parameters))

            if "code" in response:
                raise AnsibleError(
                    "Received error for %s - %s: %s"
                    % (
                        response.get("url", ""),
                        response.get("code", ""),
                        response.get("msg", ""),
                    )
                )
            ret.append(response.get("extensions"))

        return ret

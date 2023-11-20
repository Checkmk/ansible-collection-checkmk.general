# Copyright: (c) 2023, Lars Getwan <lars.getwan@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    name: ruleset
    author: Lars Getwan (@lgetwan)
    version_added: "4.0.0"
    short_description: Show ruleset
    description:
      - Returns details of a ruleset
    options:
      _terms:
        description: The ruleset name.
        required: True
      server_url:
        description: URL of the Checkmk server
        required: True
      site:
        description: site name
        required: True
      automation_user:
        description: automation user for the REST API access
        required: True
      automation_secret:
        description: automation secret for the REST API access
        required: True
      validate_certs:
        description: Wether or not to validate TLS cerificates
        type: boolean
        required: False
        default: True
"""

EXAMPLES = """
- name: Get all subfolders of the main folder recursively
  ansible.builtin.debug:
    msg: "Folder tree: {{ item.id }}"
  loop: "{{
    lookup('checkmk.general.folders',
        '~',
        show_hosts=False,
        recursive=True,
        server_url=server_url,
        site=site,
        automation_user=automation_user,
        automation_secret=automation_secret,
        validate_certs=False
        )
    }}"
  loop_control:
      label: "{{ item.id }}"

- name: Get all hosts of the folder /test recursively
  ansible.builtin.debug:
    msg: "Host found in {{ item.0.id }}: {{ item.1.title }}"
  vars:
    looping: "{{
                 lookup('checkmk.general.folders',
                     '~tests',
                     show_hosts=True,
                     recursive=True,
                     server_url=server_url,
                     site=site,
                     automation_user=automation_user,
                     automation_secret=automation_secret,
                     validate_certs=False
                     )
              }}"
  loop: "{{ looping|subelements('members.hosts.value') }}"
  loop_control:
      label: "{{ item.0.id }}"
"""

RETURN = """
  _list:
    description:
      - A list of folders and, optionally, hosts of a folder
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

        site_url = server_url + "/" + site

        api = CheckMKLookupAPI(
            site_url=site_url,
            user=user,
            secret=secret,
            validate_certs=validate_certs,
        )

        ret = []
        for term in terms:
            response = json.loads(api.get("/objects/ruleset/" + term))

            if "code" in response:
                raise AnsibleError(
                    "Received error for %s - %s: %s"
                    % (
                        response.get("url", ""),
                        response.get("code", ""),
                        response.get("msg", ""),
                    )
                )

            ret.append(response.get("extensions", {}))

        return ret

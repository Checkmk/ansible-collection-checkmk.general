# Copyright: (c) 2023, Lars Getwan <lars.getwan@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    name: folders
    author: Lars Getwan (@lgetwan)
    version_added: "3.3.0"
    short_description: Get various information about a folder
    description:
      - Returns a list of subfolders
      - Returns a list of hosts of the folder
    options:
      _terms:
        description: complete folder path using tilde as a delimiter
        required: True
      show_hosts:
        description: Also show the hosts of the folder(s) found
        type: boolean
        required: False
        default: False
      recursive:
        description: Do a recursive query
        type: boolean
        required: False
        default: False
      site_url:
        description: site url
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
        site_url=server_url + '/' + site,
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
                     site_url=server_url + '/' + site,
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

from ansible.plugins.lookup import LookupBase
from ansible_collections.checkmk.general.plugins.module_utils.lookup_api import (
    CheckMKLookupAPI,
)


class LookupModule(LookupBase):
    def run(self, terms, variables, **kwargs):
        self.set_options(var_options=variables, direct=kwargs)
        show_hosts = self.get_option("show_hosts")
        recursive = self.get_option("recursive")
        site_url = self.get_option("site_url")
        user = self.get_option("automation_user")
        secret = self.get_option("automation_secret")
        validate_certs = self.get_option("validate_certs")

        api = CheckMKLookupAPI(
            site_url=site_url,
            user=user,
            secret=secret,
            validate_certs=validate_certs,
        )

        ret = []
        for term in terms:
            parameters = {
                "parent": term.replace("/", "~"),
                "recursive": recursive,
                "show_hosts": show_hosts,
            }

            response = json.loads(
                api.get("/domain-types/folder_config/collections/all", parameters)
            )

            ret.append(response.get("value"))
            #ret.append([{"name": "debug %s" % term, "extensions": { "attributes": { "tag_criticality": "prod" } } }])

        return ret

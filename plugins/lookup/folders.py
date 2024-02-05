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

    notes:
      - Like all lookups, this runs on the Ansible controller and is unaffected by other keywords such as 'become'.
        If you need to use different permissions, you must change the command or run Ansible as another user.
      - Alternatively, you can use a shell/command task that runs against localhost and registers the result.
      - The directory of the play is used as the current working directory.
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
        server_url=my_server_url,
        site=my_site,
        automation_user=my_user,
        automation_secret=my_secret,
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
                     server_url=my_server_url,
                     site=my_site,
                     automation_user=my_user,
                     automation_secret=my_secret,
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
        show_hosts = self.get_option("show_hosts")
        recursive = self.get_option("recursive")
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
            parameters = {
                "parent": term.replace("/", "~"),
                "recursive": recursive,
                "show_hosts": show_hosts,
            }

            response = json.loads(
                api.get("/domain-types/folder_config/collections/all", parameters)
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
            ret.append(response.get("value"))

        return ret

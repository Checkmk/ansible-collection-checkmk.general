# Copyright: (c) 2023, Lars Getwan <lars.getwan@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    name: rulesets
    author: Lars Getwan (@lgetwan)
    version_added: "3.5.0"

    short_description: Search rulesets

    description:
      - Returns a list of Rulesets

    options:

      server_url:
        description: URL of the Checkmk server.
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

      regex:
        description: A regex of the ruleset name.
        required: True

      rulesets_folder:
        description:
          - The folder in which to search for rules.
          - Path delimiters can be either ~ or /.
        required: False
        default: "/"

      rulesets_deprecated:
        description: Only show deprecated rulesets. Defaults to False.
        type: boolean
        required: False
        default: False

      rulesets_used:
        description: Only show used rulesets. Defaults to True.
        type: boolean
        required: False
        default: True

    notes:
      - Like all lookups, this runs on the Ansible controller and is unaffected by other keywords such as 'become'.
        If you need to use different permissions, you must change the command or run Ansible as another user.
      - Alternatively, you can use a shell/command task that runs against localhost and registers the result.
      - The directory of the play is used as the current working directory.
"""

EXAMPLES = """
- name: Get all used rulesets with 'file' in their name
  ansible.builtin.debug:
    msg: "Ruleset: {{ item.extensions.name }} has {{ item.extensions.number_of_rules }} rules."
  loop: "{{
    lookup('checkmk.general.rulesets',
      regex='file',
      rulesets_used=True,
      server_url=server_url,
      site=site,
      automation_user=automation_user,
      automation_secret=automation_secret,
      validate_certs=False
      )
    }}"
  loop_control:
      label: "{{ item.id }}"

- name: Get all used deprecated rulesets
  ansible.builtin.debug:
    msg: "Ruleset {{ item.extension.name }} is deprecated."
  loop: "{{
    lookup('checkmk.general.rulesets',
      regex='',
      rulesets_deprecated=True,
      rulesets_used=True,
      server_url=server_url,
      site=site,
      automation_user=automation_user,
      automation_secret=automation_secret,
      validate_certs=False
      )
    }}"
  loop_control:
      label: "{{ item.0.id }}"
"""

RETURN = """
  _list:
    description:
      - A list of rulesets
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
        regex = self.get_option("regex")
        rulesets_folder = self.get_option("rulesets_folder")
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

        parameters = {
            "name": regex,
            "folder": rulesets_folder.replace("/", "~"),
        }

        if self.get_option("rulesets_deprecated") is not None:
            parameters.update({"deprecated": self.get_option("rulesets_deprecated")})

        if self.get_option("rulesets_used") is not None:
            parameters.update({"used": self.get_option("rulesets_used")})

        response = json.loads(
            api.get("/domain-types/ruleset/collections/all", parameters)
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

        return [response.get("value")]

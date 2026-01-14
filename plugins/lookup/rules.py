# Copyright: (c) 2023, Lars Getwan <lars.getwan@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    name: rules
    author: Lars Getwan (@lgetwan)
    version_added: "3.5.0"

    short_description: Get a list rules

    description:
      - Returns a list of Rules

    options:

      ruleset:
        description: The ruleset name.
        required: True

      description_regex:
        description: A regex to filter for certain descriptions.
        required: False
        default: ""

      comment_regex:
        description: A regex to filter for certain comment strings.
        required: False
        default: ""

      folder_regex:
        description: A regex to filter for certain folders.
        required: False
        default: ""

    extends_documentation_fragment: [checkmk.general.common_lookup]

    notes:
      - Like all lookups, this runs on the Ansible controller and is unaffected by other keywords such as 'become'.
        If you need to use different permissions, you must change the command or run Ansible as another user.
      - Alternatively, you can use a shell/command task that runs against localhost and registers the result.
      - The directory of the play is used as the current working directory.
      - It is B(NOT) possible to assign other variables to the variables mentioned in the C(vars) section!
        This is a limitation of Ansible itself.
"""

EXAMPLES = """
- name: Get all rules of the ruleset host_groups
  ansible.builtin.debug:
    msg: "Rule: {{ item.extensions }}"
  loop: "{{
    lookup('checkmk.general.rules',
        ruleset='host_groups',
        server_url=server_url,
        site=site,
        api_user=api_user,
        api_secret=api_secret,
        validate_certs=False
        )
    }}"
  loop_control:
    label: "{{ item.id }}"

- name: Get all rules of the ruleset host_groups in folder /test
  ansible.builtin.debug:
    msg: "Rule: {{ item.extensions }}"
  loop: "{{
    lookup('checkmk.general.rules',
        ruleset='host_groups',
        folder_regex='^/test$',
        server_url=server_url,
        site=site,
        api_user=api_user,
        api_secret=api_secret,
        validate_certs=False
        )
    }}"
  loop_control:
    label: "{{ item.id }}"

- name: active_checks:http rules that match a certain description AND comment
  ansible.builtin.debug:
    msg: "Rule: {{ item.extensions }}"
  loop: "{{
    lookup('checkmk.general.rules',
        ruleset='active_checks:http',
        description_regex='foo.*bar',
        comment_regex='xmas-edition',
        server_url=server_url,
        site=site,
        api_user=api_user,
        api_secret=api_secret,
        validate_certs=False
        )
    }}"
  loop_control:
    label: "{{ item.id }}"

- name: "Use variables from inventory."
  ansible.builtin.debug:
    msg: "Rule: {{ item.extensions }}"
  vars:
    checkmk_var_server_url: "http://myserver/"
    checkmk_var_site: "mysite"
    checkmk_var_api_user: "myuser"
    checkmk_var_api_secret: "mysecret"
    checkmk_var_validate_certs: false
  loop: "{{
    lookup('checkmk.general.rules', ruleset='host_groups') }}"
  loop_control:
    label: "{{ item.id }}"
"""

RETURN = """
  _list:
    description:
      - A list of all rules of a particular ruleset
    type: list
    elements: str
"""

import json
import re

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
from ansible_collections.checkmk.general.plugins.module_utils.lookup_api import (
    CheckMKLookupAPI,
)


class LookupModule(LookupBase):
    def run(self, terms, variables, **kwargs):
        regex_params = {}
        self.set_options(var_options=variables, direct=kwargs)
        ruleset = self.get_option("ruleset")
        regex_params["description"] = self.get_option("description_regex")
        regex_params["comment"] = self.get_option("comment_regex")
        regex_params["folder"] = self.get_option("folder_regex")
        server_url = self.get_option("server_url")
        site = self.get_option("site")
        api_auth_type = self.get_option("api_auth_type") or "bearer"
        api_auth_cookie = self.get_option("api_auth_cookie")
        api_user = self.get_option("api_user")
        api_secret = self.get_option("api_secret")
        validate_certs = self.get_option("validate_certs")

        site_url = server_url + "/" + site

        api = CheckMKLookupAPI(
            site_url=site_url,
            api_auth_type=api_auth_type,
            api_auth_cookie=api_auth_cookie,
            api_user=api_user,
            api_secret=api_secret,
            validate_certs=validate_certs,
        )

        parameters = {
            "ruleset_name": ruleset,
        }

        response = json.loads(api.get("/domain-types/rule/collections/all", parameters))

        if "code" in response:
            raise AnsibleError(
                "Received error for %s - %s: %s"
                % (
                    response.get("url", ""),
                    response.get("code", ""),
                    response.get("msg", ""),
                )
            )

        rule_list = response.get("value")

        log = []

        log.append("PARAMS: %s" % str(regex_params))
        for what, regex in regex_params.items():
            try:
                if regex:
                    log.append("ITEMS: %s" % str((what, regex)))

                    def _rule_attribute(rule, what, regex):
                        if what == "folder":
                            log.append(
                                "Folder: %s regex: %s"
                                % (rule.get("extensions", {}).get("folder", ""), regex)
                            )
                            return rule.get("extensions", {}).get("folder", "")
                        return (
                            rule.get("extensions", {})
                            .get("properties", {})
                            .get(what, "")
                        )

                    rule_list = [
                        r
                        for r in rule_list
                        if re.search(
                            regex,
                            _rule_attribute(r, what, regex),
                        )
                    ]

            except re.error as e:
                raise AnsibleError(
                    "Invalid regex for %s, pattern: %s, position: %s error: %s"
                    % (what, e.pattern, e.pos, e.msg)
                )

        # return [log]
        return [rule_list]

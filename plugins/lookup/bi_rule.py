# Copyright: (c) 2025, Lars Getwan <lars.getwan@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    name: bi_rule
    author: Lars Getwan (@lgetwan)
    version_added: "6.1.0"

    short_description: Retrieve details of a BI rule.

    description:
      - This lookup returns the details of a specified BI rule.

    options:

      _terms:
        description: The ID of the BI rule to retrieve.
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

      automation_auth_type:
        description: The authentication type to use ('bearer', 'basic', 'cookie').
        required: False
        default: 'bearer'

      automation_user:
        description: The automation user for authentication.
        required: True

      automation_secret:
        description: The automation secret or password for authentication.
        required: True

      automation_auth_cookie:
        description: The authentication cookie value if using cookie-based authentication.
        required: False

      validate_certs:
        description: Whether to validate SSL certificates.
        required: False
        type: bool
        default: True

    notes:
      - Like all lookups, this runs on the Ansible controller and is unaffected by other keywords such as 'become'.
      - The directory of the play is used as the current working directory.
      - It is B(NOT) possible to assign other variables to the variables mentioned in the C(vars) section!
        This is a limitation of Ansible itself.
"""

EXAMPLES = """
- name: Get a BI rule with a particular rule id
  ansible.builtin.debug:
    msg: "BI rule: {{ bi_rule_details }}"
  vars:
    bi_rule_details: "{{
      lookup('checkmk.general.bi_rule',
        'rule123',
        server_url='http://myserver/',
        site='mysite',
        automation_user='myuser',
        automation_secret='mysecret',
        validate_certs=False
      )
    }}"

- name: "Use variables outside the module call."
  ansible.builtin.debug:
    msg: "BI rule: {{ bi_rule_details }}"
  vars:
    ansible_lookup_checkmk_server_url: "http://myserver/"
    ansible_lookup_checkmk_site: "mysite"
    ansible_lookup_checkmk_automation_user: "myuser"
    ansible_lookup_checkmk_automation_secret: "mysecret"
    ansible_lookup_checkmk_validate_certs: false
    bi_rule_details: "{{ lookup('checkmk.general.bi_rule', 'rule123') }}"
"""

RETURN = """
_list:
  description:
    - A list of dicts containing the attributes of the BI rule, including its aggregations and related objects.
  type: list
  elements: dict
"""

import base64
import json

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
from ansible_collections.checkmk.general.plugins.module_utils.lookup_api import (
    CheckMKLookupAPI,
)


class ExtendedCheckmkAPI(CheckMKLookupAPI):
    """
    Extends CheckMKLookupAPI to support 'basic' and 'cookie' authentication methods.
    Ensures that Bearer authentication uses both 'automation_user' and 'automation_secret'.
    """

    def __init__(
        self,
        site_url,
        automation_auth_type="bearer",
        automation_user=None,
        automation_secret=None,
        automation_auth_cookie=None,
        validate_certs=True,
    ):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        cookies = {}

        # Bearer Authentication: "Bearer USERNAME PASSWORD"
        if automation_auth_type == "bearer":
            if not automation_user or not automation_secret:
                raise ValueError(
                    "`automation_user` and `automation_secret` are required for bearer authentication."
                )
            headers["Authorization"] = f"Bearer {automation_user} {automation_secret}"

        # Basic Authentication
        elif automation_auth_type == "basic":
            if not automation_user or not automation_secret:
                raise ValueError(
                    "`automation_user` and `automation_secret` are required for basic authentication."
                )
            auth_str = f"{automation_user}:{automation_secret}"
            auth_b64 = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")
            headers["Authorization"] = f"Basic {auth_b64}"

        # Cookie Authentication
        elif automation_auth_type == "cookie":
            if not automation_auth_cookie:
                raise ValueError(
                    "`automation_auth_cookie` is required for cookie authentication."
                )
            cookies["auth_cmk"] = automation_auth_cookie

        else:
            raise ValueError(
                f"Unsupported `automation_auth_type`: {automation_auth_type}"
            )

        super().__init__(
            site_url=site_url, user="", secret="", validate_certs=validate_certs
        )
        self.headers.update(headers)
        self.cookies = cookies


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        self.set_options(var_options=variables, direct=kwargs)
        rule_id = terms[0]

        try:
            server_url = self.get_option("server_url")
            site = self.get_option("site")
            automation_auth_type = self.get_option("automation_auth_type") or "bearer"
            automation_user = self.get_option("automation_user")
            automation_secret = self.get_option("automation_secret")
            automation_auth_cookie = self.get_option("automation_auth_cookie")
            validate_certs = self.get_option("validate_certs")
        except KeyError as e:
            raise AnsibleError(f"Missing required configuration option: {str(e)}")

        site_url = f"{server_url.rstrip('/')}/{site}"

        # Optional: Debugging prints
        # print(f"automation_auth_type: {automation_auth_type}")
        # print(f"server_url: {server_url}")
        # print(f"rule_id: {rule_id}")

        try:
            api = ExtendedCheckmkAPI(
                site_url=site_url,
                automation_auth_type=automation_auth_type,
                automation_user=automation_user,
                automation_secret=automation_secret,
                automation_auth_cookie=automation_auth_cookie,
                validate_certs=validate_certs,
            )
        except ValueError as e:
            raise AnsibleError(str(e))

        ret = []

        try:
            api_endpoint = f"/objects/bi_rule/{rule_id}"
            response_content = api.get(api_endpoint)
            response = json.loads(response_content)

            if "code" in response:
                raise AnsibleError(
                    "Received error for %s - %s: %s"
                    % (
                        response.get("url", ""),
                        response.get("code", ""),
                        response.get("msg", ""),
                    )
                )

            ret.append(response)

        except Exception as e:
            raise AnsibleError(f"Error fetching BI rule '{rule_id}': {str(e)}")

        return ret

# Copyright: (c) 2025, Lars Getwan <lars.getwan@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    name: bi_pack
    author: Lars Getwan (@lgetwan)
    version_added: "6.1.0"

    short_description: Get BI pack attributes

    description:
      - Returns the attributes of a BI Pack in Checkmk, including its rules and aggregations.

    options:

      _terms:
        description: BI Pack ID
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
        description:
          - Automation user for the REST API access.
        required: True
        vars:
          - name: ansible_lookup_checkmk_automation_user
        env:
          - name: ANSIBLE_LOOKUP_CHECKMK_AUTOMATION_USER
        ini:
          - section: checkmk_lookup
            key: automation_user

      automation_secret:
        description:
          - Automation secret for the REST API access.
        required: True
        vars:
          - name: ansible_lookup_checkmk_automation_secret
        env:
          - name: ANSIBLE_LOOKUP_CHECKMK_AUTOMATION_SECRET
        ini:
          - section: checkmk_lookup
            key: automation_secret

      validate_certs:
        description:
          - Whether or not to validate TLS certificates.
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
      - The directory of the play is used as the current working directory.
"""

EXAMPLES = """
- name: Get the attributes of a BI Pack
  ansible.builtin.debug:
    msg: "Attributes of BI Pack: {{ attributes }}"
  vars:
    attributes: "{{
                    lookup('checkmk.general.bi_pack',
                        'example_pack',
                        server_url=my_server_url,
                        site=mysite,
                        automation_user=myuser,
                        automation_secret=mysecret,
                        validate_certs=False
                        )
                 }}"

- name: "Use variables outside the module call."
  ansible.builtin.debug:
    msg: "Attributes of BI Pack: {{ attributes }}"
  vars:
    ansible_lookup_checkmk_server_url: "http://myserver/"
    ansible_lookup_checkmk_site: "mysite"
    ansible_lookup_checkmk_automation_user: "myuser"
    ansible_lookup_checkmk_automation_secret: "mysecret"
    ansible_lookup_checkmk_validate_certs: false
    attributes: "{{ lookup('checkmk.general.bi_pack', 'example_pack') }}"
"""

RETURN = """
_list:
  description:
    - A list of dicts of attributes of the BI Pack(s), including rules and aggregations.
  type: list
  elements: dict
"""

import json

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
from ansible_collections.checkmk.general.plugins.module_utils.lookup_api import (
    CheckMKLookupAPI,
)


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        self.set_options(var_options=variables, direct=kwargs)

        try:
            server_url = self.get_option("server_url")
            site = self.get_option("site")
            user = self.get_option("automation_user")
            secret = self.get_option("automation_secret")
            validate_certs = self.get_option("validate_certs")
        except KeyError as e:
            raise AnsibleError(f"Missing required configuration option: {str(e)}")

        site_url = f"{server_url.rstrip('/')}/{site}"

        api = CheckMKLookupAPI(
            site_url=site_url,
            user=user,
            secret=secret,
            validate_certs=validate_certs,
        )

        ret = []

        for term in terms:
            try:
                # Fetch the BI Pack details
                api_endpoint = f"/objects/bi_pack/{term}"
                response = json.loads(api.get(api_endpoint))

                if "code" in response:
                    raise AnsibleError(
                        "Received error for %s - %s: %s"
                        % (
                            response.get("url", ""),
                            response.get("code", ""),
                            response.get("msg", ""),
                        )
                    )

                # Fetch the rules associated with the BI Pack
                rules_endpoint = f"/objects/bi_pack/{term}/rules"
                rules_response = json.loads(api.get(rules_endpoint))

                # Fetch the aggregations associated with the BI Pack
                aggregations_endpoint = f"/objects/bi_pack/{term}/aggregations"
                aggregations_response = json.loads(api.get(aggregations_endpoint))

                # Add rules and aggregations to the BI pack response
                response["rules"] = rules_response.get("rules", [])
                response["aggregations"] = aggregations_response.get("aggregations", [])

                ret.append(response)

            except Exception as e:
                raise AnsibleError(f"Error fetching BI Pack '{term}': {str(e)}")

        return ret

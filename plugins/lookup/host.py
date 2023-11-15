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
      effective_attributes:
        description: show all effective attributes on hosts
        type: boolean
        required: False
        default: False
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
- name: Get the attributes of host example.com
  ansible.builtin.debug:
    msg: "Attributes of host example: {{ attributes }}"
  vars:
    attributes: "{{
                    lookup('checkmk.general.host',
                        'example.com',
                        effective_attributes=True,
                        server_url=server_url,
                        site=site,
                        automation_user=automation_user,
                        automation_secret=automation_secret,
                        validate_certs=False
                        )
                 }}"
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

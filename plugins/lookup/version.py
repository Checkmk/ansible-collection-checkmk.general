# Copyright: (c) 2023, Lars Getwan <lars.getwan@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    name: version
    author: Lars Getwan (@lgetwan)
    version_added: "3.1.0"
    short_description: Get the version of a Checkmk server
    description:
      - Returns the version of a Checkmk server as a string, e.g. '2.1.0p31.cre'
    options:
      _terms:
        description: site url
        required: True
      automation_user:
        description: automation user for the REST API access
        required: True
      automation_secret:
        description: automation secret for the REST API access
        required: True
      validate_certs:
        description: Wether or not to validate TLS certificates
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
- name: "Show Checkmk version"
  debug:
    msg: "Server version is {{ version }}"
  vars:
    version: "{{ lookup('checkmk.general.version',
                   server_url + '/' + site,
                   validate_certs=False,
                   automation_user=my_user,
                   automation_secret=my_secret
               )}}"
"""

RETURN = """
  _list:
    description:
      - server Checkmk version
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
        user = self.get_option("automation_user")
        secret = self.get_option("automation_secret")
        validate_certs = self.get_option("validate_certs")

        ret = []

        for term in terms:
            api = CheckMKLookupAPI(
                site_url=term,
                user=user,
                secret=secret,
                validate_certs=validate_certs,
            )

            response = json.loads(api.get("/version"))
            ret.append(response.get("versions", {}).get("checkmk"))
        return ret

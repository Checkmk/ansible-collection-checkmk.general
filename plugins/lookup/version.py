# Copyright: (c) 2023, Lars Getwan <lars.getwan@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
    name: version
    author: Lars Getwan (@lgetwan)
    version_added: "3.1"
    short_description: Get the version of a CMK server
    description:
      - Returns the version of a CMK server as a string, e.g. '2.1.0p31.cre'
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
        description: Wether or not to validate TLS cerificates
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
- name: We could read the file directly, but this shows output from command
  ansible.builtin.debug: 
      msg: "CMK version installed is{{ lookup('checkmk.general.version', 'https://myserver/mysite', automation_user='automation', automation_secret='$SECRET'}}."
"""

RETURN = """
  _list:
    description:
      - server CMK version
    type: list
    elements: str
"""

import json
from ansible.errors import AnsibleError
from ansible.module_utils.common.text.converters import to_text, to_native
from ansible.module_utils.urls import open_url, ConnectionError, SSLValidationError
from ansible.plugins.lookup import LookupBase
from urllib.error import HTTPError, URLError


class LookupModule(LookupBase):

    def run(self, terms, variables, **kwargs):

        self.set_options(var_options=variables, direct=kwargs)
        user = self.get_option("automation_user")
        secret = self.get_option("automation_secret")
        validate_certs = self.get_option("validate_certs")

        ret = []
        for term in terms:
            base_url = term + "/check_mk/api/1.0"
            api_endpoint = "/version"
            url = base_url + api_endpoint

            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": "Bearer %s %s" % (user, secret),
            }

            try:
                response = open_url(url, data=None, headers=headers, method="GET", validate_certs=validate_certs)

            except HTTPError as e:
                raise AnsibleError("Received HTTP error for %s : %s" % (url, to_native(e)))
            except URLError as e:
                raise AnsibleError("Failed lookup url for %s : %s" % (url, to_native(e)))
            except SSLValidationError as e:
                raise AnsibleError("Error validating the server's certificate for %s: %s" % (url, to_native(e)))
            except ConnectionError as e:
                raise AnsibleError("Error connecting to %s: %s" % (url, to_native(e)))

            checkmkinfo = json.loads(to_text(response.read()))
            ret.append(checkmkinfo.get("versions").get("checkmk"))

        return ret

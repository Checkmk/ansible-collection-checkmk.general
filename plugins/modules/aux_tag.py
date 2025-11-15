#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2025, Nicolas Brainez <nicolas@brainez.net>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: aux_tag

short_description: Manage auxiliary tags in Checkmk.

version_added: "6.3.0"

description:
- Manage auxiliary tags in Checkmk.

extends_documentation_fragment: [checkmk.general.common]

options:
    name:
        description: The ID of the auxiliary tag.
        required: true
        type: str
        aliases: ["id"]

    title:
        description: The title of the auxiliary tag.
        required: false
        type: str

    topic:
        description: The topic or category of the auxiliary tag.
        required: false
        type: str

    help:
        description: Help text describing the auxiliary tag.
        required: false
        type: str

    state:
        description: The desired state.
        required: true
        choices: ["present", "absent"]
        type: str

author:
    - Nicolas Brainez (@nicoske)
"""

EXAMPLES = r"""
# Create an auxiliary tag
- name: "Create auxiliary tag for HTTPS"
  checkmk.general.aux_tag:
    server_url: "http://myserver/"
    site: "mysite"
    automation_user: "myuser"
    automation_secret: "mysecret"
    name: https
    title: Web Server HTTPS
    topic: Services
    help: "Host provides HTTPS services"
    state: "present"

# Update an auxiliary tag
- name: "Update auxiliary tag"
  checkmk.general.aux_tag:
    server_url: "http://myserver/"
    site: "mysite"
    automation_user: "myuser"
    automation_secret: "mysecret"
    name: https
    title: Web Server HTTPS/TLS
    topic: Services
    state: "present"

# Delete an auxiliary tag
- name: "Delete auxiliary tag"
  checkmk.general.aux_tag:
    server_url: "http://myserver/"
    site: "mysite"
    automation_user: "myuser"
    automation_secret: "mysecret"
    name: https
    state: "absent"
"""

RETURN = r"""
http_code:
    description: The HTTP code the Checkmk API returns.
    type: int
    returned: always
    sample: '200'
message:
    description: The output message that the module generates.
    type: str
    returned: always
    sample: 'Done.'
"""

import time

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.checkmk.general.plugins.module_utils.api import CheckmkAPI
from ansible_collections.checkmk.general.plugins.module_utils.types import RESULT
from ansible_collections.checkmk.general.plugins.module_utils.utils import (
    base_argument_spec,
    result_as_dict,
)

# We count 404 not as failed, because we want to know if the aux tag exists or not.
HTTP_CODES_GET = {
    # http_code: (changed, failed, "Message")
    404: (False, False, "Not Found: The requested object has not been found."),
}

HTTP_CODES_DELETE = {
    # http_code: (changed, failed, "Message")
    404: (False, False, "Not Found: The requested object has not been found."),
}


class AuxTagCreateAPI(CheckmkAPI):
    def post(self):  # Create aux tag
        data = {
            "aux_tag_id": self.params.get("name", ""),
            "title": self.params.get("title", ""),
            "topic": self.params.get("topic", ""),
            "help": self.params.get("help", ""),
        }

        # Remove all keys without value, as otherwise they would be None.
        data = {key: val for key, val in data.items() if val}

        return self._fetch(
            endpoint="/domain-types/aux_tag/collections/all",
            data=data,
            method="POST",
        )


class AuxTagUpdateAPI(CheckmkAPI):
    def put(self):  # Update aux tag
        data = {
            "title": self.params.get("title", ""),
            "topic": self.params.get("topic", ""),
            "help": self.params.get("help", ""),
        }

        # Remove all keys without value, as they would be emptied.
        data = {key: val for key, val in data.items() if val}

        return self._fetch(
            endpoint="/objects/aux_tag/%s" % self.params.get("name"),
            data=data,
            method="PUT",
        )


class AuxTagDeleteAPI(CheckmkAPI):
    def delete(self):  # Remove aux tag
        return self._fetch(
            code_mapping=HTTP_CODES_DELETE,
            endpoint="/objects/aux_tag/%s" % self.params.get("name"),
            method="DELETE",
        )


class AuxTagGetAPI(CheckmkAPI):
    def get(self):
        return self._fetch(
            code_mapping=HTTP_CODES_GET,
            endpoint="/objects/aux_tag/%s" % self.params.get("name"),
            method="GET",
        )


def run_module():
    argument_spec = base_argument_spec()
    argument_spec.update(
        name=dict(type="str", required=True, aliases=["id"]),
        title=dict(type="str", required=False),
        topic=dict(type="str", required=False),
        help=dict(type="str", required=False),
        state=dict(
            type="str",
            choices=["present", "absent"],
            required=True,
        ),
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    result = RESULT(
        http_code=0,
        msg="Nothing to be done",
        content="",
        etag="",
        failed=False,
        changed=False,
    )

    auxtag = AuxTagAPI(module)

    if module.params.get("state") == "present":
        if auxtag.current.http_code == 200:
            if changes_detected(
                module, json.loads(auxtag.current.content.decode("utf-8"))
            ):
                result = auxtag.put()

        elif auxtag.current.http_code == 404:
            result = auxtag.post()

    if module.params.get("state") == "absent":
        if auxtag.current.http_code == 200:
            result = auxtag.delete()
        elif auxtag.current.http_code == 404:
            result = RESULT(
                http_code=0,
                msg="Aux tag already absent.",
                content="",
                etag="",
                failed=False,
                changed=False,
            )

    module.exit_json(**result_as_dict(result))


def main():
    run_module()


if __name__ == "__main__":
    main()

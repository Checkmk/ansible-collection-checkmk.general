#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2025, Nicolas Brainez <nicolas@brainez.net>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: aux_tag

short_description: Manage auxiliary tags in Checkmk

version_added: "6.5.0"

description:
- Manage auxiliary tags in Checkmk.
- Auxiliary tags can be assigned to tag group values and are used to group hosts
  for rule matching without exposing the underlying tag structure to the user.

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

notes:
    - Only parameters that are explicitly provided are compared and potentially updated.
      Omitting a parameter will not reset or change its current value on the server.

seealso:
    - module: checkmk.general.tag_group

author:
    - Nicolas Brainez (@nicoske)
"""

EXAMPLES = r"""
# ---------------------------------------------------------------------------
# Create and update auxiliary tags
# ---------------------------------------------------------------------------

- name: "Create an auxiliary tag."
  checkmk.general.aux_tag:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    name: "https"
    title: "HTTPS"
    state: "present"

- name: "Create an auxiliary tag with a topic and help text."
  checkmk.general.aux_tag:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    name: "https"
    title: "HTTPS"
    topic: "Web Services"
    help: "Host provides HTTPS services."
    state: "present"

- name: "Update the title of an existing auxiliary tag."
  checkmk.general.aux_tag:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    name: "https"
    title: "HTTPS/TLS"
    state: "present"

# ---------------------------------------------------------------------------
# Delete auxiliary tags
# ---------------------------------------------------------------------------

- name: "Delete an auxiliary tag."
  checkmk.general.aux_tag:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    name: "https"
    state: "absent"

# ---------------------------------------------------------------------------
# Using environment variables for authentication
# ---------------------------------------------------------------------------
# Connection parameters can be provided via environment variables instead of
# task parameters. The supported variables are:
#   CHECKMK_VAR_SERVER_URL, CHECKMK_VAR_SITE,
#   CHECKMK_VAR_API_USER, CHECKMK_VAR_API_SECRET,
#   CHECKMK_VAR_VALIDATE_CERTS

- name: "Create an auxiliary tag using environment variables for authentication."
  checkmk.general.aux_tag:
    name: "https"
    title: "HTTPS"
    state: "present"
  environment:
    CHECKMK_VAR_SERVER_URL: "https://myserver/"
    CHECKMK_VAR_SITE: "mysite"
    CHECKMK_VAR_API_USER: "myuser"
    CHECKMK_VAR_API_SECRET: "mysecret"
    CHECKMK_VAR_VALIDATE_CERTS: "true"
"""

RETURN = r"""
http_code:
    description: The HTTP code the Checkmk API returns.
    type: int
    returned: always
    sample: 200
msg:
    description: The output message that the module generates.
    type: str
    returned: always
    sample: 'Auxiliary tag created.'
"""

import json

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.checkmk.general.plugins.module_utils.api import CheckmkAPI
from ansible_collections.checkmk.general.plugins.module_utils.types import RESULT
from ansible_collections.checkmk.general.plugins.module_utils.utils import (
    base_argument_spec,
    exit_module,
)

# We count 404 not as failed, because we want to know if the aux tag exists or not.
HTTP_CODES_GET = {
    # http_code: (changed, failed, "Message")
    404: (False, False, "Not Found: The requested object has not been found."),
}


class AuxTagAPI(CheckmkAPI):
    def __init__(self, module):
        super().__init__(module)

        # Get current aux tag
        self.current = self._fetch(
            code_mapping=HTTP_CODES_GET,
            endpoint="/objects/aux_tag/%s" % self.params.get("name"),
            method="GET",
        )

    def normalize_data(self):
        data = {
            "title": self.params.get("title", ""),
            "topic": self.params.get("topic", ""),
            "help": self.params.get("help", ""),
        }

        # Remove all keys without value, as they would be emptied.
        data = {key: val for key, val in data.items() if val}

        return data

    def post(self):
        data = self.normalize_data()
        data["aux_tag_id"] = self.params.get("name", "")

        return self._fetch(
            endpoint="/domain-types/aux_tag/collections/all",
            data=data,
            method="POST",
        )

    def put(self):
        self.headers["If-Match"] = self.current.etag
        data = self.normalize_data()

        return self._fetch(
            endpoint="/objects/aux_tag/%s" % self.params.get("name"),
            data=data,
            method="PUT",
        )

    def delete(self):
        self.headers["If-Match"] = self.current.etag

        return self._fetch(
            endpoint="/objects/aux_tag/%s/actions/delete/invoke"
            % self.params.get("name"),
            data={},
            method="POST",
        )


def changes_detected(module, current):
    if module.params.get("title") and module.params.get("title") != current.get(
        "title"
    ):
        return True

    if module.params.get("topic") and module.params.get("topic") != current.get(
        "extensions", {}
    ).get("topic"):
        return True

    if module.params.get("help") and module.params.get("help") != current.get(
        "extensions", {}
    ).get("help"):
        return True

    return False


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

    exit_module(module, result=result)


def main():
    run_module()


if __name__ == "__main__":
    main()

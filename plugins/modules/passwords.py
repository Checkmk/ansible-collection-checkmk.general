#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2023, Robin Gierse <robin.gierse@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: passwords

short_description: Manage passwords in checkmk.

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "2.3.0"

description:
- Manage passwords in checkmk.

extends_documentation_fragment: [checkmk.general.common]

options:
    name:
        description: An unique identifier for the password.
        required: true
        type: str

    title:
        description: A title for the password.
        required: false
        type: str

    comment:
        description: A comment for the password.
        required: false
        type: str

    documentation_url:
        description: An optional URL pointing to documentation or any other page.
        required: false
        type: str

    password:
        description: The password string.
        required: false
        type: str

    owner:
        description: Each password is owned by a group of users which are able to edit, delete and use existing passwords.
        required: false
        type: str

    shared:
        description: The list of members to share the password with.
        required: false
        type: raw

    state:
        description: create/update or delete a password.
        required: true
        choices: ["present", "absent"]
        type: str

author:
    - Max Sickora (@max-checkmk)
"""

EXAMPLES = r"""
# Creating and Updating is the same.
# If passwords are configured, no_log should be set to true.
- name: "Create a new password."
  checkmk.general.passwords:
    server_url: "http://localhost/"
    site: "my_site"
    automation_user: "automation"
    automation_secret: "$SECRET"
    name: "mypassword"
    title: "My Password"
    comment: "Comment on my password"
    documentation_url: "https://url.to.mypassword/"
    password: "topsecret"
    owner: "admin"
    shared: [
        "all"
    ]
    state: "present"
  no_log: true
- name: "Delete a password."
  checkmk.general.passwords:
    server_url: "http://localhost/"
    site: "my_site"
    automation_user: "automation"
    automation_secret: "$SECRET"
    name: "mypassword"
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

import json
import time

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.checkmk.general.plugins.module_utils.api import CheckmkAPI
from ansible_collections.checkmk.general.plugins.module_utils.types import RESULT
from ansible_collections.checkmk.general.plugins.module_utils.utils import (
    result_as_dict,
)

# We count 404 not as failed, because we want to know if the password exists or not.
HTTP_CODES_GET = {
    # http_code: (changed, failed, "Message")
    200: (True, False, "OK: The operation was done successfully."),
    400: (False, True, "Bad Request: Parameter or validation failure."),
    403: (False, True, "Forbidden: Configuration via Setup is disabled."),
    404: (False, False, "Not Found: The requested object has not been found."),
    406: (
        False,
        True,
        "Not Acceptable: The requests accept headers can not be satisfied.",
    ),
    415: (
        False,
        True,
        "Unsupported Media Type: The submitted content-type is not supported.",
    ),
    500: (False, True, "General Server Error."),
}

HTTP_CODES_DELETE = {
    # http_code: (changed, failed, "Message")
    200: (True, False, "OK: The operation was done successfully."),
    400: (False, True, "Bad Request: Parameter or validation failure."),
    403: (False, True, "Forbidden: Configuration via Setup is disabled."),
    404: (False, True, "Not Found: The requested object has not been found."),
    406: (
        False,
        True,
        "Not Acceptable: The requests accept headers can not be satisfied.",
    ),
    415: (
        False,
        True,
        "Unsupported Media Type: The submitted content-type is not supported.",
    ),
    500: (False, True, "General Server Error."),
}

HTTP_CODES_CREATE = {
    # http_code: (changed, failed, "Message")
    200: (True, False, "OK: The operation was done successfully."),
    400: (False, True, "Bad Request: Parameter or validation failure."),
    403: (False, True, "Forbidden: Configuration via Setup is disabled."),
    406: (
        False,
        True,
        "Not Acceptable: The requests accept headers can not be satisfied.",
    ),
    415: (
        False,
        True,
        "Unsupported Media Type: The submitted content-type is not supported.",
    ),
    500: (False, True, "General Server Error."),
}

HTTP_CODES_UPDATE = {
    # http_code: (changed, failed, "Message")
    200: (
        True,
        False,
        "No Content: Operation was done successfully. No further output",
    ),
    403: (False, True, "Forbidden: Configuration via Setup is disabled."),
    404: (False, True, "Not Found: The requested object has not been found."),
    406: (
        False,
        True,
        "Not Acceptable: The requests accept headers can not be satisfied.",
    ),
    412: (
        False,
        True,
        "Precondition Failed: The value of the If-Match header doesn't match the object's ETag.",
    ),
    415: (
        False,
        True,
        "Unsupported Media Type: The submitted content-type is not supported.",
    ),
    428: (
        False,
        True,
        "Precondition Required: The required If-Match header is missing.",
    ),
    500: (False, True, "General Server Error."),
}


class PasswordsCreateAPI(CheckmkAPI):
    def post(self):
        data = {
            "ident": self.params.get("name", ""),
            "title": self.params.get("title", ""),
            "comment": self.params.get("comment", ""),
            "documentation_url": self.params.get("documentation_url", ""),
            "password": self.params.get("password", ""),
            "owner": self.params.get("owner", ""),
            "shared": self.params.get("shared", ""),
        }

        return self._fetch(
            code_mapping=HTTP_CODES_CREATE,
            endpoint="/domain-types/password/collections/all",
            data=data,
            method="POST",
        )


class PasswordsUpdateAPI(CheckmkAPI):
    def put(self):
        data = {
            "title": self.params.get("title", ""),
            "comment": self.params.get("comment", ""),
            "documentation_url": self.params.get("documentation_url", ""),
            "password": self.params.get("password", ""),
            "owner": self.params.get("owner", ""),
            "shared": self.params.get("shared", ""),
        }

        # Remove all keys without value, as they would be emptied.
        data = {key: val for key, val in data.items() if val}

        return self._fetch(
            code_mapping=HTTP_CODES_UPDATE,
            endpoint="/objects/password/%s" % self.params.get("name"),
            data=data,
            method="PUT",
        )


class PasswordsDeleteAPI(CheckmkAPI):
    def delete(self):
        data = {}

        return self._fetch(
            code_mapping=HTTP_CODES_DELETE,
            endpoint="/objects/password/%s" % self.params.get("name"),
            data=data,
            method="DELETE",
        )


class PasswordsGetAPI(CheckmkAPI):
    def get(self):
        data = {}

        return self._fetch(
            code_mapping=HTTP_CODES_GET,
            endpoint="/objects/password/%s" % self.params.get("name"),
            data=data,
            method="GET",
        )


def run_module():
    module_args = dict(
        server_url=dict(type="str", required=True),
        site=dict(type="str", required=True),
        validate_certs=dict(type="bool", required=False, default=True),
        automation_user=dict(type="str", required=True),
        automation_secret=dict(type="str", required=True, no_log=True),
        name=dict(type="str", required=True),
        title=dict(type="str", required=False),
        comment=dict(type="str", required=False),
        documentation_url=dict(type="str", required=False),
        password=dict(type="str", required=False, no_log=True),
        owner=dict(type="str", required=False),
        shared=dict(type="raw", required=False),
        state=dict(
            type="str",
            choices=["present", "absent"],
            required=True,
        ),
    )
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=False)

    result = RESULT(
        http_code=0,
        msg="Nothing to be done",
        content="",
        etag="",
        failed=False,
        changed=False,
    )

    if module.params.get("state") == "present":
        passwordget = PasswordsGetAPI(module)
        result = passwordget.get()

        if result.http_code == 200:
            passwordupdate = PasswordsUpdateAPI(module)
            passwordupdate.headers["If-Match"] = result.etag
            result = passwordupdate.put()

            time.sleep(3)

        elif result.http_code == 404:
            passwordcreate = PasswordsCreateAPI(module)
            result = passwordcreate.post()

            time.sleep(3)

    if module.params.get("state") == "absent":
        passworddelete = PasswordsDeleteAPI(module)
        result = passworddelete.delete()

        time.sleep(3)

    module.exit_json(**result_as_dict(result))


def main():
    run_module()


if __name__ == "__main__":
    main()

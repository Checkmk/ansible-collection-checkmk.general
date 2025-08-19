#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2023, Max Sickora <max.sickora@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: password

short_description: Manage passwords in Checkmk.

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "2.3.0"

description:
- Manage passwords in Checkmk.

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

    customer:
        description: For the Checkmk Managed Edition (CME), you need to specify which customer ID this object belongs to.
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
  checkmk.general.password:
    server_url: "http://myserver/"
    site: "mysite"
    automation_user: "myuser"
    automation_secret: "mysecret"
    name: "mypassword"
    title: "My Password"
    customer: "provider"
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
  checkmk.general.password:
    server_url: "http://myserver/"
    site: "mysite"
    automation_user: "myuser"
    automation_secret: "mysecret"
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

import time

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.checkmk.general.plugins.module_utils.api import CheckmkAPI
from ansible_collections.checkmk.general.plugins.module_utils.types import RESULT
from ansible_collections.checkmk.general.plugins.module_utils.utils import (
    base_argument_spec,
    result_as_dict,
)
from ansible_collections.checkmk.general.plugins.module_utils.version import (
    CheckmkVersion,
)

# We count 404 not as failed, because we want to know if the password exists or not.
HTTP_CODES_GET = {
    # http_code: (changed, failed, "Message")
    404: (False, False, "Not Found: The requested object has not been found."),
}

HTTP_CODES_DELETE = {
    # http_code: (changed, failed, "Message")
    404: (False, False, "Not Found: The requested object has not been found."),
}


class PasswordsCreateAPI(CheckmkAPI):
    def post(self):
        data = {
            "ident": self.params.get("name", ""),
            "title": self.params.get("title", ""),
            "customer": self.params.get("customer", ""),
            "comment": self.params.get("comment", ""),
            "documentation_url": self.params.get("documentation_url", ""),
            "password": self.params.get("password", ""),
            "owner": self.params.get("owner", ""),
            "shared": self.params.get("shared", ""),
        }

        # Remove all keys without value, as otherwise they would be None.
        data = {key: val for key, val in data.items() if val}

        return self._fetch(
            endpoint="/domain-types/password/collections/all",
            data=data,
            method="POST",
        )


class PasswordsUpdateAPI(CheckmkAPI):
    def put(self):
        data = {
            "title": self.params.get("title", ""),
            "customer": self.params.get("customer", ""),
            "comment": self.params.get("comment", ""),
            "documentation_url": self.params.get("documentation_url", ""),
            "password": self.params.get("password", ""),
            "owner": self.params.get("owner", ""),
            "shared": self.params.get("shared", ""),
        }

        # Remove all keys without value, as they would be emptied.
        data = {key: val for key, val in data.items() if val}

        return self._fetch(
            endpoint="/objects/password/%s" % self.params.get("name"),
            data=data,
            method="PUT",
        )


class PasswordsDeleteAPI(CheckmkAPI):
    def delete(self):
        return self._fetch(
            code_mapping=HTTP_CODES_DELETE,
            endpoint="/objects/password/%s" % self.params.get("name"),
            method="DELETE",
        )


class PasswordsGetAPI(CheckmkAPI):
    def get(self):

        return self._fetch(
            code_mapping=HTTP_CODES_GET,
            endpoint="/objects/password/%s" % self.params.get("name"),
            method="GET",
        )


def run_module():
    argument_spec = base_argument_spec()
    argument_spec.update(
        name=dict(type="str", required=True),
        title=dict(type="str", required=False),
        customer=dict(type="str", required=False),
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

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

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

            checkmkversion = CheckmkVersion(str(passwordcreate.getversion()))
            if (
                checkmkversion.edition == "cme"
                and module.params.get("customer") is None
            ):
                result = RESULT(
                    http_code=0,
                    msg="Missing required parameter 'customer' for CME",
                    content="",
                    etag="",
                    failed=True,
                    changed=False,
                )
                module.fail_json(**result_as_dict(result))

            result = passwordcreate.post()

            time.sleep(3)

    if module.params.get("state") == "absent":
        passwordget = PasswordsGetAPI(module)
        result = passwordget.get()

        if result.http_code == 200:
            passworddelete = PasswordsDeleteAPI(module)
            passworddelete.headers["If-Match"] = result.etag
            result = passworddelete.delete()

            time.sleep(3)

    module.exit_json(**result_as_dict(result))


def main():
    run_module()


if __name__ == "__main__":
    main()

#!/usr/bin/python

# Copyright: (c) 2018, Mathias Buresch <mathias.buresch@de.clara.net>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: password

short_description: Manage passwords in Checkmk

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "0.17.0"

description: Manage passwords in the Checkmk password store.

options:
    name:
        description: 
            - Title/name of the password.
        required: true
        type: str
    ident:
        description:
            - The unique identifier for the password.
            - Optional. Will be generated out of name.
    password:
        description:
            - Define the password.
        type: str
    owner:
        description:
            - Group of users which are able to edit, delete and use the password.
        type: str
    state:
        description:
            - Whether the password should exist.
            - When C(absent), removes the password.
        type: str
        choices: [ absent, present ]
        default: present
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
extends_documentation_fragment:
  - tribe29.checkmk.common

author:
    - Mathias Buresch (@elwood218)
'''

EXAMPLES = r"""
# Add a password.
- name: "Add a password."
  tribe29.checkmk.password:
    server_url: "http://localhost/"
    site: "my_site"
    automation_user: "automation"
    automation_secret: "$SECRET"
    name: "my-password"
    owner: "admin"
    state: "present"
# Delete a password.
- name: "Delete a password."
  tribe29.checkmk.host:
    server_url: "http://localhost/"
    site: "my_site"
    automation_user: "automation"
    automation_secret: "$SECRET"
    name: "my-password"
    state: "absent"
"""

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'goodbye'
'''

import json
import re

from ansible.module_utils.urls import fetch_url
from ansible.module_utils.basic import AnsibleModule


def exit_failed(module, msg):
    result = {"msg": msg, "changed": False, "failed": True}
    module.fail_json(**result)


def exit_changed(module, msg):
    result = {"msg": msg, "changed": True, "failed": False}
    module.exit_json(**result)


def exit_ok(module, msg):
    result = {"msg": msg, "changed": False, "failed": False}
    module.exit_json(**result)


def get_password(module, base_url, headers, norm_id):
    current_state = "unknown"
    etag = ""
    current_owner = ""

    api_endpoint = "/objects/password/" + module.params.get("id", norm_id)
    url = base_url + api_endpoint

    response, info = fetch_url(
        module, url, data=None, headers=headers, method="GET")

    if info["status"] == 200:
        body = json.loads(response.read())
        current_state = "present"
        etag = info.get("etag", "")
        extensions = body.get("extensions", {})
        current_owner = "%s" % extensions.get("owned_by")

    elif info["status"] == 404:
        current_state = "absent"

    else:
        exit_failed(
            module,
            "Error calling API. HTTP code %d. Details: %s."
            % (info["status"], info.get("body", "N/A")),
        )

    return current_state, etag, current_owner


def create_password(module, base_url, headers, norm_id):
    api_endpoint = "/domain-types/password/collections/all"
    params = {
        "ident": module.params.get("id", norm_id),
        "title": module.params.get("name"),
        "password": module.params.get("password"),
        "owner": module.params.get("owner")
    }
    url = base_url + api_endpoint

    response, info = fetch_url(
        module, url, module.jsonify(params), headers=headers, method="POST"
    )

    if info["status"] != 200:
        exit_failed(
            module,
            "Error calling API. HTTP code %d. Details: %s, "
            % (info["status"], info["body"]),
        )


def update_password(module, base_url, headers, norm_id):
    api_endpoint = "/objects/password/" + module.params.get("id", norm_id)
    params = {
        "title": module.params.get("name"),
        "password": module.params.get("password"),
        "owner": module.params.get("owner")
    }
    url = base_url + api_endpoint

    response, info = fetch_url(
        module, url, module.jsonify(params), headers=headers, method="PUT"
    )

    if info["status"] != 200:
        exit_failed(
            module,
            "Error calling API. HTTP code %d. Details: %s, "
            % (info["status"], info["body"]),
        )


def delete_password(module, base_url, headers, norm_id):
    api_endpoint = "/objects/password/" + module.params.get("id", norm_id)
    url = base_url + api_endpoint

    response, info = fetch_url(
        module, url, data=None, headers=headers, method="DELETE")

    if info["status"] != 204:
        exit_failed(
            module,
            "Error calling API. HTTP code %d. Details: %s, "
            % (info["status"], info["body"]),
        )


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        server_url=dict(type="str", required=True),
        site=dict(type="str", required=True),
        validate_certs=dict(type="bool", required=False, default=True),
        automation_user=dict(type="str", required=True),
        automation_secret=dict(type="str", required=True, no_log=True),
        ident=dict(type="str", default=""),
        name=dict(type="str", required=True, aliases=["title"]),
        password=dict(type='str', no_log=True),
        owner=dict(type="str", default="admin"),
        state=dict(type="str", default="present",
                   choices=["present", "absent"]),
    )

    module = AnsibleModule(argument_spec=module_args,
                           supports_check_mode=False)

    # Normalize id
    if module.params.get("ident") == "":
        norm_id = re.sub(r' ', '-', module.params.get("name"))
        # norm_id = re.sub(r' ','-',module.get.params("name").lower())
    else:
        norm_id = ""

    # Use the parameters to initialize some common variables
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer %s %s"
        % (
            module.params.get("automation_user", ""),
            module.params.get("automation_secret", ""),
        ),
    }

    base_url = "%s/%s/check_mk/api/1.0" % (
        module.params.get("server_url", ""),
        module.params.get("site", ""),
    )

    # Determine desired state
    state = module.params.get("state", "present")

    # Determine the current state of this particular password
    (
        current_state,
        etag,
        current_owner
    ) = get_password(module, base_url, headers, norm_id)

    # Handle the password accordingly to above findings and desired state
    if state == "present" and current_state == "present":
        headers["If-Match"] = etag
        # msg_tokens = []
        exit_ok(module, "Password already exists.")

        # if module.params.get("owner") != current_owner:
        #    update_password(module, base_url, headers, norm_id)
        #    msg_tokens.append("Ownership changed.")

        # if len(msg_tokens) >= 1:
        #    exit_changed(module, " ".join(msg_tokens))
        # else:
        #    exit_ok(module, "")

    elif state == "present" and current_state == "absent":
        create_password(module, base_url, headers, norm_id)
        exit_changed(module, "Password created.")

    elif state == "absent" and current_state == "absent":
        exit_ok(module, "Password already absent.")

    elif state == "absent" and current_state == "present":
        delete_password(module, base_url, headers, norm_id)
        exit_changed(module, "Password deleted.")

    else:
        exit_failed(module, "Unknown error")


def main():
    run_module()


if __name__ == "__main__":
    main()

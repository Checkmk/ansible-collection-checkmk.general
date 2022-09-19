#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: host_group

short_description: Manage host groups in Checkmk.

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "0.0.1"

description:
- Manage host groups within Checkmk.

extends_documentation_fragment: [tribe29.checkmk.common]

options:
    host_group_name:
        description: The name of the host group to be created/modified/deleted.
        required: true
        type: str
    title:
        description: The title (alias) of your host group. If omitted defaults to the host_group_name.
        type: str
    state:
        description: The state of your host group.
        type: str
        default: present
        choices: [present, absent]
    validate_certs:
        description: Whether to validate the SSL certificate of the Checkmk server.
        default: true
        type: bool

"""

EXAMPLES = r"""
# Create a single host group.
- name: "Create a single host group."
  tribe29.checkmk.host_group:
    server_url: "http://localhost/"
    site: "my_site"
    automation_user: "automation"
    automation_secret: "$SECRET"
    host_group_name: "my_host_group"
    title: "My Host Group"
    state: "present"

"""

RETURN = r"""
message:
    description: The output message that the module generates.
    type: str
    returned: always
    sample: 'Host group created.'
"""

import json

# https://docs.ansible.com/ansible/latest/dev_guide/testing/sanity/import.html
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url


def exit_failed(module, msg):
    result = {"msg": msg, "changed": False, "failed": True}
    module.fail_json(**result)


def exit_changed(module, msg):
    result = {"msg": msg, "changed": True, "failed": False}
    module.exit_json(**result)


def exit_ok(module, msg):
    result = {"msg": msg, "changed": False, "failed": False}
    module.exit_json(**result)


def get_current_host_group_state(module, base_url, headers):
    current_state = "unknown"
    current_title = ""
    etag = ""

    api_endpoint = "/objects/host_group_config/" + module.params["host_group_name"]
    url = base_url + api_endpoint

    response, info = fetch_url(module, url, data=None, headers=headers, method="GET")

    if info["status"] == 200:
        body = json.loads(response.read())
        current_state = "present"
        etag = info.get("etag", "")
        current_title = body.get("title", "")

    elif info["status"] == 404:
        current_state = "absent"

    else:
        exit_failed(
            module,
            "Error calling API. HTTP code %d. Details: %s"
            % (info["status"], info.get("body", "N/A")),
        )

    return current_state, current_title, etag


def move_host_group(module, base_url, headers):
    host_group_name = module.params["host_group_name"]

    api_endpoint = "/objects/host_group_config/" + host_group_name
    params = {
        "alias": module.params.get("title", host_group_name),
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


def create_host_group(module, base_url, headers):
    host_group_name = module.params["host_group_name"]

    api_endpoint = "/domain-types/host_group_config/collections/all"
    params = {
        "name": host_group_name,
        "alias": module.params.get("title", host_group_name),
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


def delete_host_group(module, base_url, headers):
    api_endpoint = "/objects/host_group_config/" + module.params["host_group_name"]
    url = base_url + api_endpoint

    response, info = fetch_url(module, url, data=None, headers=headers, method="DELETE")

    if info["status"] != 204:
        exit_failed(
            module,
            "Error calling API. HTTP code %d. Details: %s, "
            % (info["status"], info["body"]),
        )


def run_module():
    module_args = dict(
        server_url=dict(type="str", required=True),
        site=dict(type="str", required=True),
        validate_certs=dict(type="bool", required=False, default=True),
        automation_user=dict(type="str", required=True),
        automation_secret=dict(type="str", required=True, no_log=True),
        host_group_name=dict(type="str", required=True),
        title=dict(type="str", required=False),
        state=dict(type="str", default="present", choices=["present", "absent"]),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=False)

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

    # Determine the current state of this particular host group
    (
        current_state,
        current_title,
        etag,
    ) = get_current_host_group_state(module, base_url, headers)

    # Handle the host group accordingly to above findings and desired state
    if state == "present" and current_state == "present":
        headers["If-Match"] = etag
        msg_tokens = []

        if current_title != module.params["title"]:
            move_host_group(module, base_url, headers)
            msg_tokens.append("Host group was updated.")

        if len(msg_tokens) >= 1:
            exit_changed(module, " ".join(msg_tokens))
        else:
            exit_ok(
                module, "Host group already present."
            )

    elif state == "present" and current_state == "absent":
        create_host_group(module, base_url, headers)
        exit_changed(module, "Host group created.")

    elif state == "absent" and current_state == "absent":
        exit_ok(module, "Host group already absent.")

    elif state == "absent" and current_state == "present":
        delete_host_group(module, base_url, headers)
        exit_changed(module, "Host group deleted.")

    else:
        exit_failed(module, "Unknown error")


def main():
    run_module()


if __name__ == "__main__":
    main()

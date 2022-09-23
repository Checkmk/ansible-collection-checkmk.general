#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: bulk_host_group

short_description: Manage host groups in Checkmk (bulk version).

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "0.0.1"

description:
- Manage host groups in Checkmk (bulk version).

extends_documentation_fragment: [tribe29.checkmk.common]

options:
    host_groups:
        name:
            description: name of the host group to be created/modified/deleted.
            default: ""
            type: str
        title:
            description: title (alias) of the host group to be created/modified. If omitted defaults to the host group name.
            default: ""
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

author:
    - Michael Sekania (@msekania)
"""

EXAMPLES = r"""
# Create several host groups.
- name: "Create several host groups."
  tribe29.checkmk.bulk_host_group:
    server_url: "http://localhost/"
    site: "my_site"
    automation_user: "automation"
    automation_secret: "$SECRET"
    hostgroups:
      - name: "my_host_group_one"
        title: "My Host Group One"
      - name: "my_host_group_two"
        title: "My Host Group Two"
      - name: "my_host_group_test"
        title: "My Test"
    state: "present"

# Create several host groups.
- name: "Create several host groups."
  tribe29.checkmk.bulk_host_group:
    server_url: "http://localhost/"
    site: "my_site"
    automation_user: "automation"
    automation_secret: "$SECRET"
    hostgroups:
      - name: "my_host_group_one"
        title: "My Host Group One"
      - name: "my_host_group_two"
      - name: "my_host_group_test"
        title: ""
    state: "present"

# delete several host groups.
- name: "Delete several host groups."
  tribe29.checkmk.bulk_host_group:
    server_url: "http://localhost/"
    site: "my_site"
    automation_user: "automation"
    automation_secret: "$SECRET"
    hostgroups:
      - name: "my_host_group_one"
      - name: "my_host_group_two"
    state: "absent"
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


def get_current_host_groups(module, base_url, headers):
    current_groups = []

    api_endpoint = "/domain-types/host_group_config/collections/all"
    url = base_url + api_endpoint

    response, info = fetch_url(module, url, headers=headers, method="GET")

    if info["status"] == 200:
        body = json.loads(response.read())
        tmp = body.get("value", [])
        current_groups = [
            {
                "name": el.get("href").rsplit("/", 1)[-1],
                "title": el.get("title", el.get("name")),
            }
            for el in tmp
        ]
    else:
        exit_failed(
            module,
            "Error calling API in (collections). HTTP code %d. Details: %s"
            % (info["status"], info.get("body", "N/A")),
        )

    return current_groups


def move_host_groups(module, base_url, host_groups, headers):
    api_endpoint = "/domain-types/host_group_config/actions/bulk-update/invoke"
    params = {
        "entries": [
            {
                "name": el.get("name"),
                "attributes": {
                    "alias": el.get("title", el.get("name")),
                },
            }
            for el in host_groups
        ],
    }
    url = base_url + api_endpoint

    response, info = fetch_url(
        module, url, module.jsonify(params), headers=headers, method="PUT"
    )

    if info["status"] != 200:
        exit_failed(
            module,
            "Error calling API (bulk-update). HTTP code %d. Details: %s, "
            % (info["status"], info["body"]),
        )


def create_host_groups(module, base_url, host_groups, headers):
    api_endpoint = "/domain-types/host_group_config/actions/bulk-create/invoke"
    params = {
        "entries": [
            {
                "name": el.get("name"),
                "alias": el.get("title", el.get("name")),
            }
            for el in host_groups
        ],
    }
    url = base_url + api_endpoint

    response, info = fetch_url(
        module, url, module.jsonify(params), headers=headers, method="POST"
    )

    if info["status"] != 200:
        exit_failed(
            module,
            "Error calling API (bulk-create). HTTP code %d. Details: %s, "
            % (info["status"], info["body"]),
        )


def delete_host_groups(module, base_url, host_groups, headers):
    api_endpoint = "/domain-types/host_group_config/actions/bulk-delete/invoke"
    params = {
        "entries": [el["name"] for el in host_groups],
    }
    url = base_url + api_endpoint

    response, info = fetch_url(
        module, url, module.jsonify(params), headers=headers, method="POST"
    )

    if info["status"] != 204:
        exit_failed(
            module,
            "Error calling API (bulk-delete). HTTP code %d. Details: %s, "
            % (info["status"], info["body"]),
        )


def run_module():
    module_args = dict(
        server_url=dict(type="str", required=True),
        site=dict(type="str", required=True),
        validate_certs=dict(type="bool", required=False, default=True),
        automation_user=dict(type="str", required=True),
        automation_secret=dict(type="str", required=True, no_log=True),
        host_groups=dict(type="raw", default=[]),
        state=dict(type="str", default="present", choices=["present", "absent"]),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=False)

    host_groups = module.params.get("host_groups")

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

    # Determine which host groups do already exest
    current_groups = get_current_host_groups(module, base_url, headers)

    # Determine intersection and difference with input, according to 'name' only
    if len(set([el.get("name") for el in host_groups])) != len(host_groups):
        exit_failed(module, "two or more entries with the same name!")

    listofnames = set([el.get("name") for el in current_groups])

    intersection_list = [el for el in host_groups if el.get("name") in listofnames]
    difference_list = [el for el in host_groups if not el.get("name") in listofnames]

    # Handle the host group accordingly to above findings and desired state
    if state == "present":
        # create host groups which do not exist (difference)
        # modify host groups that exist (intersection)

        msg_tokens = []

        if len(difference_list) > 0:
            create_host_groups(module, base_url, difference_list, headers)
            msg_tokens.append(
                "Host groups: "
                + " ".join([el["name"] for el in difference_list])
                + " were created."
            )

        if len(intersection_list) > 0:
            # determines difference between lists according to 'name' and 'title' pair
            current_groups_dict = dict(
                (el["name"], el["title"]) for el in current_groups
            )
            remainings_list = [
                el
                for el in intersection_list
                if el.get("title") != current_groups_dict[el.get("name")]
            ]

            if len(remainings_list) > 0:
                changed = move_host_groups(module, base_url, remainings_list, headers)
                msg_tokens.append(
                    "Host groups: "
                    + " ".join([el["name"] for el in remainings_list])
                    + " were updated."
                )

        if len(msg_tokens) >= 1:
            exit_changed(module, " ".join(msg_tokens))
        else:
            exit_ok(module, "Host groups already present.")

    elif state == "absent":
        # delete host groups that exist (intersection_list)
        if len(intersection_list) > 0:
            # extra check if title-s (alias-es) match.
            delete_host_groups(module, base_url, intersection_list, headers)
            exit_changed(
                module,
                "Host groups: "
                + " ".join([el["name"] for el in intersection_list])
                + " were deleted.",
            )

    else:
        exit_failed(module, "Unknown error")


def main():
    run_module()


if __name__ == "__main__":
    main()

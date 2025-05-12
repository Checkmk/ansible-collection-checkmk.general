#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2022, Michael Sekania &
#                      Robin Gierse <robin.gierse@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: service_group

short_description: Manage service groups in Checkmk (bulk version).

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "0.12.0"

description:
- Manage service groups in Checkmk.

extends_documentation_fragment: [checkmk.general.common]

options:
    name:
        description: The name of the service group to be created/modified/deleted.
        type: str
    title:
        description: The title (alias) of your service group. If omitted defaults to the name.
        type: str
    customer:
        description: For the Checkmk Managed Edition (CME), you need to specify which customer ID this object belongs to.
        required: false
        type: str
    groups:
        description:
            - instead of 'name', 'title' a list of dicts with elements of service group name and title (alias) to be created/modified/deleted.
              If title is omitted in entry, it defaults to the service group name.
        default: []
        type: raw
    state:
        description: The state of your service group.
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
# Create a single service group.
- name: "Create a single service group."
  checkmk.general.service_group:
    server_url: "http://myserver/"
    site: "mysite"
    automation_user: "myuser"
    automation_secret: "mysecret"
    name: "my_service_group"
    title: "My Service Group"
    customer: "provider"
    state: "present"

# Create several service groups.
- name: "Create several service groups."
  checkmk.general.service_group:
    server_url: "http://myserver/"
    site: "mysite"
    automation_user: "myuser"
    automation_secret: "mysecret"
    customer: "provider"
    groups:
      - name: "my_service_group_one"
        title: "My Service Group One"
      - name: "my_service_group_two"
        title: "My Service Group Two"
      - name: "my_service_group_test"
        title: "My Test"
    state: "present"

# Create several service groups.
- name: "Create several service groups."
  checkmk.general.service_group:
    server_url: "http://myserver/"
    site: "mysite"
    automation_user: "myuser"
    automation_secret: "mysecret"
    customer: "provider"
    groups:
      - name: "my_service_group_one"
        title: "My Service Group One"
      - name: "my_service_group_two"
      - name: "my_service_group_test"
    state: "present"

# Delete a single service group.
- name: "Create a single service group."
  checkmk.general.service_group:
    server_url: "http://myserver/"
    site: "mysite"
    automation_user: "myuser"
    automation_secret: "mysecret"
    name: "my_service_group"
    state: "absent"

# Delete several service groups.
- name: "Delete several service groups."
  checkmk.general.service_group:
    server_url: "http://myserver/"
    site: "mysite"
    automation_user: "myuser"
    automation_secret: "mysecret"
    groups:
      - name: "my_service_group_one"
      - name: "my_service_group_two"
    state: "absent"
"""

RETURN = r"""
message:
    description: The output message that the module generates.
    type: str
    returned: always
    sample: 'Service group created.'
"""

import json

# https://docs.ansible.com/ansible/latest/dev_guide/testing/sanity/import.html
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url
from ansible_collections.checkmk.general.plugins.module_utils.utils import (
    base_argument_spec,
)


def exit_failed(module, msg):
    result = {"msg": msg, "changed": False, "failed": True}
    module.fail_json(**result)


def exit_changed(module, msg):
    result = {"msg": msg, "changed": True, "failed": False}
    module.exit_json(**result)


def exit_ok(module, msg):
    result = {"msg": msg, "changed": False, "failed": False}
    module.exit_json(**result)


def get_current_single_service_group(module, base_url, headers):
    current_state = "unknown"
    current_title = ""
    etag = ""
    name = module.params["name"]

    api_endpoint = "/objects/service_group_config/" + name
    url = base_url + api_endpoint

    response, info = fetch_url(module, url, data=None, headers=headers, method="GET")

    if info["status"] == 200:
        body = json.loads(response.read())
        current_state = "present"
        etag = info.get("etag", "")
        current_title = body.get("title", name)

    elif info["status"] == 404:
        current_state = "absent"

    else:
        exit_failed(
            module,
            "Error calling API. HTTP code %d. Details: %s"
            % (info["status"], info.get("body", "N/A")),
        )

    return current_state, current_title, etag


def get_current_service_groups(module, base_url, headers):
    current_groups = []

    api_endpoint = "/domain-types/service_group_config/collections/all"
    url = base_url + api_endpoint

    response, info = fetch_url(module, url, headers=headers, method="GET")

    if info["status"] == 200:
        body = json.loads(response.read())
        tmp = body.get("value", [])
        # Response from 2.2.0 is different. So this should fix it until module is migrated to new CheckMKAPI
        for el in tmp:
            if el.get("domainType") == "service_group_config":  # 2.2.0
                current_groups = [
                    {
                        "name": el.get("id"),
                        "title": el.get("title", el.get("name")),
                    }
                    for el in tmp
                ]
            else:  # 2.0.0 and 2.1.0
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


def update_single_service_group(module, base_url, headers):
    name = module.params["name"]

    api_endpoint = "/objects/service_group_config/" + name
    params = {
        "alias": module.params.get("title", name),
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


def update_service_groups(module, base_url, groups, headers):
    api_endpoint = "/domain-types/service_group_config/actions/bulk-update/invoke"
    params = {
        "entries": [
            {
                "name": el.get("name"),
                "attributes": {
                    "alias": el.get("title", el.get("name")),
                },
            }
            for el in groups
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


def create_single_service_group(module, base_url, headers):
    name = module.params["name"]

    api_endpoint = "/domain-types/service_group_config/collections/all"
    if module.params.get("customer") is not None:
        params = {
            "name": name,
            "alias": module.params.get("title", name),
            "customer": module.params.get("customer", "provider"),
        }
    else:
        params = {
            "name": name,
            "alias": module.params.get("title", name),
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


def create_service_groups(module, base_url, groups, headers):
    api_endpoint = "/domain-types/service_group_config/actions/bulk-create/invoke"

    if module.params.get("customer") is not None:
        params = {
            "entries": [
                {
                    "name": el.get("name"),
                    "alias": el.get("title", el.get("name")),
                    "customer": module.params.get("customer"),
                }
                for el in groups
            ],
        }
    else:
        params = {
            "entries": [
                {
                    "name": el.get("name"),
                    "alias": el.get("title", el.get("name")),
                }
                for el in groups
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


def delete_single_service_group(module, base_url, headers):
    api_endpoint = "/objects/service_group_config/" + module.params["name"]
    url = base_url + api_endpoint

    response, info = fetch_url(module, url, data=None, headers=headers, method="DELETE")

    if info["status"] != 204:
        exit_failed(
            module,
            "Error calling API. HTTP code %d. Details: %s, "
            % (info["status"], info["body"]),
        )


def delete_service_groups(module, base_url, groups, headers):
    api_endpoint = "/domain-types/service_group_config/actions/bulk-delete/invoke"
    params = {
        "entries": [el["name"] for el in groups],
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
    argument_spec = base_argument_spec
    argument_spec.update(
        name=dict(type="str", required=False),
        title=dict(type="str", required=False),
        customer=dict(type="str", required=False),
        groups=dict(type="raw", required=False, default=[]),
        state=dict(type="str", default="present", choices=["present", "absent"]),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=[
            ("groups", "name"),
        ],
        required_one_of=[
            ("groups", "name"),
        ],
        supports_check_mode=False,
    )

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

    if (
        "groups" in module.params
        and module.params.get("groups")
        and len(module.params.get("groups", [])) > 0
    ):
        if "title" in module.params and module.params.get("title", ""):
            exit_failed(
                module,
                "'title' has only effect when 'name' is defined and not 'groups'",
            )

        groups = module.params.get("groups")

        # Determine which service groups do already exest
        current_groups = get_current_service_groups(module, base_url, headers)

        # Determine intersection and difference with input, according to 'name' only
        if len(set([el.get("name") for el in groups])) != len(groups):
            exit_failed(module, "two or more entries with the same name!")

        listofnames = set([el.get("name") for el in current_groups])

        intersection_list = [el for el in groups if el.get("name") in listofnames]
        difference_list = [el for el in groups if not el.get("name") in listofnames]

        # Handle the service group accordingly to above findings and desired state
        if state == "present":
            # create service groups which do not exist (difference)
            # update service groups that exist (intersection)

            msg_tokens = []

            if len(difference_list) > 0:
                create_service_groups(module, base_url, difference_list, headers)
                msg_tokens.append(
                    "Service groups: "
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
                    update_service_groups(module, base_url, remainings_list, headers)
                    msg_tokens.append(
                        "Service groups: "
                        + " ".join([el["name"] for el in remainings_list])
                        + " were updated."
                    )

            if len(msg_tokens) >= 1:
                exit_changed(module, " ".join(msg_tokens))
            else:
                exit_ok(module, "Service groups already present.")

        elif state == "absent":
            # delete service groups that exist (intersection_list)
            if len(intersection_list) > 0:
                # extra check if title-s (alias-es) match.
                delete_service_groups(module, base_url, intersection_list, headers)
                exit_changed(
                    module,
                    "Service groups: "
                    + " ".join([el["name"] for el in intersection_list])
                    + " were deleted.",
                )

        else:
            exit_failed(module, "Unknown error")
    elif "name" in module.params and module.params.get("name", ""):
        # Determine the current state of this particular service group
        (
            current_state,
            current_title,
            etag,
        ) = get_current_single_service_group(module, base_url, headers)

        # Handle the service group accordingly to above findings and desired state
        if state == "present" and current_state == "present":
            headers["If-Match"] = etag
            msg_tokens = []

            if current_title != module.params["title"]:
                update_single_service_group(module, base_url, headers)
                msg_tokens.append("Service group was updated.")

            if len(msg_tokens) >= 1:
                exit_changed(module, " ".join(msg_tokens))
            else:
                exit_ok(module, "Service group already present.")

        elif state == "present" and current_state == "absent":
            create_single_service_group(module, base_url, headers)
            exit_changed(module, "Service group created.")

        elif state == "absent" and current_state == "absent":
            exit_ok(module, "Service group already absent.")

        elif state == "absent" and current_state == "present":
            delete_single_service_group(module, base_url, headers)
            exit_changed(module, "Service group deleted.")

        else:
            exit_failed(module, "Unknown error")
    else:
        exit_failed(module, "One shoudl define either 'groups' or 'name'")


def main():
    run_module()


if __name__ == "__main__":
    main()

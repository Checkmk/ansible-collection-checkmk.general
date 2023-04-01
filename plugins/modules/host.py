#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2022, Robin Gierse <robin.gierse@tribe29.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: host

short_description: Manage hosts in Checkmk.

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "0.0.1"

description:
    - Manage hosts within Checkmk.

extends_documentation_fragment: [tribe29.checkmk.common]

options:
    name:
        description: The host you want to manage.
        required: true
        type: str
        aliases: [host_name]
    folder:
        description: The folder your host is located in.
        type: str
    attributes:
        description:
            - The attributes of your host as described in the API documentation.
              B(Attention! This option OVERWRITES all existing attributes!)
        type: raw
        default: {}
    update_attributes:
        description:
            - The update_attributes of your host as described in the API documentation.
              This will only update the given attributes.
        type: raw
        default: {}
    remove_attributes:
        description:
            - The remove_attributes of your host as described in the API documentation.
              This will only remove the given attributes.
        type: raw
        default: []
    state:
        description: The state of your host.
        type: str
        default: present
        choices: [present, absent]

author:
    - Robin Gierse (@robin-tribe29)
    - Lars Getwan (@lgetwan)
    - Oliver Gaida (@ogaida)
"""

EXAMPLES = r"""
# Create a host.
- name: "Create a host."
  tribe29.checkmk.host:
    server_url: "http://localhost/"
    site: "my_site"
    automation_user: "automation"
    automation_secret: "$SECRET"
    name: "my_host"
    folder: "/"
    state: "present"

# Create a host with IP.
- name: "Create a host with IP address."
  tribe29.checkmk.host:
    server_url: "http://localhost/"
    site: "my_site"
    automation_user: "automation"
    automation_secret: "$SECRET"
    name: "my_host"
    attributes:
      alias: "My Host"
      ipaddress: "127.0.0.1"
    folder: "/"
    state: "present"

# Create a host which is monitored on a distinct site.
- name: "Create a host which is monitored on a distinct site."
  tribe29.checkmk.host:
    server_url: "http://localhost/"
    site: "my_site"
    automation_user: "automation"
    automation_secret: "$SECRET"
    name: "my_host"
    attributes:
      site: "my_remote_site"
    folder: "/"
    state: "present"

# Update only specified attributes
- name: "Create a host which is monitored on a distinct site."
  tribe29.checkmk.host:
    server_url: "http://localhost/"
    site: "my_site"
    automation_user: "automation"
    automation_secret: "$SECRET"
    name: "my_host"
    update_attributes:
      alias: "foo"
    state: "present"

# Remove specified attributes
- name: "Create a host which is monitored on a distinct site."
  tribe29.checkmk.host:
    server_url: "http://localhost/"
    site: "my_site"
    automation_user: "automation"
    automation_secret: "$SECRET"
    name: "my_host"
    remove_attributes:
      - alias
    state: "present"
"""

RETURN = r"""
message:
    description: The output message that the module generates. Contains the API response details in case of an error.
    type: str
    returned: always
    sample: 'Host created.'
"""

import json

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


def get_current_host_state(module, base_url, headers):
    current_state = "unknown"
    current_explicit_attributes = {}
    current_folder = "/"
    etag = ""

    api_endpoint = "/objects/host_config/" + module.params.get("name")
    parameters = "?effective_attributes=true"
    url = base_url + api_endpoint + parameters

    response, info = fetch_url(module, url, data=None, headers=headers, method="GET")

    if info["status"] == 200:
        body = json.loads(response.read())
        current_state = "present"
        etag = info.get("etag", "")
        extensions = body.get("extensions", {})
        current_explicit_attributes = extensions.get("attributes", {})
        current_folder = "%s" % extensions.get("folder", "/")
        if "meta_data" in current_explicit_attributes:
            del current_explicit_attributes["meta_data"]

    elif info["status"] == 404:
        current_state = "absent"

    else:
        exit_failed(
            module,
            "Error calling API. HTTP code %d. Details: %s."
            % (info["status"], info.get("body", "N/A")),
        )

    return current_state, current_explicit_attributes, current_folder, etag


def set_host_attributes(module, attributes, base_url, headers, update_method):
    api_endpoint = "/objects/host_config/" + module.params.get("name")
    params = {
        update_method: attributes,
    }
    url = base_url + api_endpoint

    response, info = fetch_url(
        module, url, module.jsonify(params), headers=headers, method="PUT"
    )

    if info["status"] == 400 and update_method == "remove_attributes":
        return "Host attributes allready removed."
    elif info["status"] != 200:
        exit_failed(
            module,
            "Error calling API. HTTP code %d. Details: %s, "
            % (info["status"], info["body"]),
        )


def move_host(module, base_url, headers):
    api_endpoint = "/objects/host_config/%s/actions/move/invoke" % module.params.get(
        "name"
    )
    params = {
        "target_folder": module.params.get("folder", "/"),
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


def create_host(module, attributes, base_url, headers):
    api_endpoint = "/domain-types/host_config/collections/all"
    params = {
        "folder": module.params.get("folder", "/"),
        "host_name": module.params.get("name"),
        "attributes": attributes,
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


def delete_host(module, base_url, headers):
    api_endpoint = "/objects/host_config/" + module.params.get("name")
    url = base_url + api_endpoint

    response, info = fetch_url(module, url, data=None, headers=headers, method="DELETE")

    if info["status"] != 204:
        exit_failed(
            module,
            "Error calling API. HTTP code %d. Details: %s, "
            % (info["status"], info["body"]),
        )


def normalize_folder(folder):
    if folder in ["", " ", "/", "//"]:
        return "/"

    if not folder.startswith("/"):
        folder = "/%s" % folder

    if folder.endswith("/"):
        folder = folder.rstrip("/")

    return folder


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        server_url=dict(type="str", required=True),
        site=dict(type="str", required=True),
        validate_certs=dict(type="bool", required=False, default=True),
        automation_user=dict(type="str", required=True),
        automation_secret=dict(type="str", required=True, no_log=True),
        name=dict(
            type="str",
            required=True,
            aliases=["host_name"],
            deprecated_aliases=[
                {
                    "name": "host_name",
                    "date": "2024-01-01",
                    "collection_name": "tribe29.checkmk",
                }
            ],
        ),
        attributes=dict(type="raw", default={}),
        remove_attributes=dict(type="raw", default=[]),
        update_attributes=dict(type="raw", default={}),
        folder=dict(type="str", required=False),
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

    # Determine desired state and attributes
    attributes = module.params.get("attributes", {})
    if attributes == []:
        attributes = {}
    remove_attributes = module.params.get("remove_attributes", {})
    if remove_attributes == []:
        remove_attributes = {}
    update_attributes = module.params.get("update_attributes", {})
    if update_attributes == []:
        update_attributes = {}
    state = module.params.get("state", "present")

    if module.params["folder"]:
        module.params["folder"] = normalize_folder(module.params["folder"])

    # Determine the current state of this particular host
    (
        current_state,
        current_explicit_attributes,
        current_folder,
        etag,
    ) = get_current_host_state(module, base_url, headers)

    # Handle the host accordingly to above findings and desired state
    if state == "present" and current_state == "present":
        headers["If-Match"] = etag
        msg_tokens = []

        current_folder = normalize_folder(current_folder)

        if module.params["folder"] and current_folder != module.params["folder"]:
            move_host(module, base_url, headers)
            msg_tokens.append("Host was moved.")

        if attributes != {} and current_explicit_attributes != attributes:
            set_host_attributes(module, attributes, base_url, headers, "attributes")
            msg_tokens.append("Host attributes replaced.")

        if update_attributes != {} and current_explicit_attributes != current_explicit_attributes.update(update_attributes):
            set_host_attributes(module, update_attributes, base_url, headers, "update_attributes")
            msg_tokens.append("Host attributes updated.")

        if remove_attributes != {}:
            msg = set_host_attributes(module, remove_attributes, base_url, headers, "remove_attributes")
            if msg == "Host attributes allready removed.":
                exit_ok(module, msg)
            else:
                msg_tokens.append("Host attributes removed.")

        if len(msg_tokens) >= 1:
            exit_changed(module, " ".join(msg_tokens))
        else:
            exit_ok(module, "Host already present. All explicit attributes as desired.")

    elif state == "present" and current_state == "absent":
        create_host(module, attributes, base_url, headers)
        exit_changed(module, "Host created.")

    elif state == "absent" and current_state == "absent":
        exit_ok(module, "Host already absent.")

    elif state == "absent" and current_state == "present":
        delete_host(module, base_url, headers)
        exit_changed(module, "Host deleted.")

    else:
        exit_failed(module, "Unknown error")


def main():
    run_module()


if __name__ == "__main__":
    main()

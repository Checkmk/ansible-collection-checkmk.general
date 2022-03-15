#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2022, Robin Gierse <robin.gierse@tribe29.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: folder

short_description: Manage folders in Checkmk.

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "0.0.1"

description:
- Manage folders within Checkmk.

extends_documentation_fragment: [tribe29.checkmk.common]

options:
    path:
        description: The full path to the folder you want to manage. Pay attention to the leading C(/) and avoid trailing C(/).
        required: true
        type: str
    title:
        description: The title of your folder. If omitted defaults to the folder name.
        type: str
    attributes:
        description: The attributes of your folder as described in the API documentation.
        type: raw
        default: {}
    state:
        description: The state of your folder.
        type: str
        default: present
        choices: [present, absent]

author:
    - Robin Gierse (@robin-tribe29)
    - Lars Getwan (@lgetwan)
"""

EXAMPLES = r"""
# Create a single folder.
- name: "Create a single folder."
  tribe29.checkmk.folder:
    server_url: "http://localhost/"
    site: "my_site"
    automation_user: "automation"
    automation_secret: "$SECRET"
    path: "/my_folder"
    title: "My Folder"
    state: "present"

# Create a folder who's hosts should be hosted on a remote site.
- name: "Create a single folder."
  tribe29.checkmk.folder:
    server_url: "http://localhost/"
    site: "my_site"
    automation_user: "automation"
    automation_secret: "$SECRET"
    path: "/my_remote_folder"
    title: "My Remote Folder"
    attributes:
      site: "my_remote_site"
    state: "present"
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
    sample: 'Folder created.'
"""

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url
from pathlib import Path
import json


def exit_failed(module, msg):
    result = {"msg": msg, "changed": False, "failed": True}
    module.fail_json(**result)


def exit_changed(module, msg):
    result = {"msg": msg, "changed": True, "failed": False}
    module.exit_json(**result)


def exit_ok(module, msg):
    result = {"msg": msg, "changed": False, "failed": False}
    module.exit_json(**result)


def cleanup_path(path):
    p = Path(path)
    if not p.is_absolute():
        p = Path("/").joinpath(p)
    return str(p.parent).lower(), p.name


def get_current_folder_state(module, base_url, headers):
    current_state = "unknown"
    current_explicit_attributes = {}
    current_folder = "/"
    etag = ""

    path_for_url = module.params["path"].replace("/", "~")

    api_endpoint = "/objects/folder_config/" + path_for_url
    url = base_url + api_endpoint

    response, info = fetch_url(module, url, data=None, headers=headers, method="GET")

    if info["status"] == 200:
        body = json.loads(response.read())
        current_state = "present"
        etag = info.get("etag", "")
        extensions = body.get("extensions", {})
        current_explicit_attributes = extensions.get("attributes", {})
        if "meta_data" in current_explicit_attributes:
            del current_explicit_attributes["meta_data"]

    elif info["status"] == 404:
        current_state = "absent"

    else:
        exit_failed(
            module,
            "Error calling API. HTTP code %d. Details: %s. Body: %s"
            % (info["status"], info["body"], body),
        )

    return current_state, current_explicit_attributes, etag


def set_folder_attributes(module, attributes, base_url, headers):
    parent, foldername = cleanup_path(module.params["path"])
    path_for_url = module.params["path"].replace("/", "~")
    title = module.params.get("title", foldername)

    api_endpoint = "/objects/folder_config/" + path_for_url
    params = {
        "title": title,
        "attributes": attributes,
    }
    url = base_url + api_endpoint

    response, info = fetch_url(module, url, module.jsonify(params), headers=headers, method="PUT")

    if info["status"] != 200:
        exit_failed(
            module,
            "Error calling API. HTTP code %d. Details: %s, " % (info["status"], info["body"]),
        )


def create_folder(module, attributes, base_url, headers):
    parent, foldername = cleanup_path(module.params["path"])
    path_for_url = module.params["path"].replace("/", "~")
    title = module.params.get("title", foldername)

    api_endpoint = "/domain-types/folder_config/collections/all"
    params = {
        "name": foldername,
        "title": title,
        "parent": parent,
        "attributes": attributes,
    }
    url = base_url + api_endpoint

    response, info = fetch_url(module, url, module.jsonify(params), headers=headers, method="POST")

    if info["status"] != 200:
        exit_failed(
            module,
            "Error calling API. HTTP code %d. Details: %s, " % (info["status"], info["body"]),
        )


def delete_folder(module, base_url, headers):
    path_for_url = module.params["path"].replace("/", "~")

    api_endpoint = "/objects/folder_config/" + path_for_url
    url = base_url + api_endpoint

    response, info = fetch_url(module, url, data=None, headers=headers, method="DELETE")

    if info["status"] != 204:
        exit_failed(
            module,
            "Error calling API. HTTP code %d. Details: %s, " % (info["status"], info["body"]),
        )


def run_module():
    module_args = dict(
        server_url=dict(type="str", required=True),
        site=dict(type="str", required=True),
        automation_user=dict(type="str", required=True),
        automation_secret=dict(type="str", required=True, no_log=True),
        path=dict(type="str", required=True),
        title=dict(type="str"),
        attributes=dict(type="raw", default=[]),
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
    state = module.params.get("state", "present")

    # Determine the current state of this particular folder
    (
        current_state,
        current_explicit_attributes,
        etag,
    ) = get_current_folder_state(module, base_url, headers)

    # Handle the folder accordingly to above findings and desired state
    if state == "present" and current_state == "present":
        headers["If-Match"] = etag
        msg_tokens = []

        if attributes != {} and current_explicit_attributes != attributes:
            set_folder_attributes(module, attributes, base_url, headers)
            msg_tokens.append("Folder attributes changed.")

        if len(msg_tokens) >= 1:
            exit_changed(module, " ".join(msg_tokens))
        else:
            exit_ok(module, "Folder already present. All explicit attributes as desired.")

    elif state == "present" and current_state == "absent":
        create_folder(module, attributes, base_url, headers)
        exit_changed(module, "Folder created.")

    elif state == "absent" and current_state == "absent":
        exit_ok(module, "Folder already absent.")

    elif state == "absent" and current_state == "present":
        delete_folder(module, base_url, headers)
        exit_changed(module, "Folder deleted.")

    else:
        exit_failed(module, "Unknown error")


def main():
    run_module()


if __name__ == "__main__":
    main()

#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2022, Robin Gierse <robin.gierse@checkmk.com>
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

extends_documentation_fragment: [checkmk.general.common]

options:
    path:
        description:
            - The full path to the folder you want to manage.
              Pay attention to the leading C(/) and avoid trailing C(/).
              Special characters apart from C(_) are not allowed!
        required: true
        type: str
    name:
        description: The name of your folder. If omitted defaults to the folder name.
        type: str
        aliases: [title]
    attributes:
        description:
            - The attributes of your folder as described in the API documentation.
              B(Attention! This option OVERWRITES all existing attributes!)
              As of Check MK v2.2.0p7 and v2.3.0b1, simultaneous use of I(attributes),
              I(remove_attributes), and I(update_attributes) is no longer supported.
        type: raw
        required: false
    update_attributes:
        description:
            - The update_attributes of your host as described in the API documentation.
              This will only update the given attributes.
              As of Check MK v2.2.0p7 and v2.3.0b1, simultaneous use of I(attributes),
              I(remove_attributes), and I(update_attributes) is no longer supported.
        type: raw
        required: false
    remove_attributes:
        description:
            - The remove_attributes of your host as described in the API documentation.
              This will only remove the given attributes.
              As of Check MK v2.2.0p7 and v2.3.0b1, simultaneous use of I(attributes),
              I(remove_attributes), and I(update_attributes) is no longer supported.
        type: raw
        required: false
    state:
        description: The state of your folder.
        type: str
        default: present
        choices: [present, absent]

author:
    - Robin Gierse (@robin-checkmk)
    - Lars Getwan (@lgetwan)
    - Michael Sekania (@msekania)
"""

EXAMPLES = r"""
# Create a single folder.
- name: "Create a single folder."
  checkmk.general.folder:
    server_url: "http://my_server/"
    site: "my_site"
    automation_user: "my_user"
    automation_secret: "my_secret"
    path: "/my_folder"
    name: "My Folder"
    state: "present"

# Create a folder who's hosts should be hosted on a remote site.
- name: "Create a single folder."
  checkmk.general.folder:
    server_url: "http://my_server/"
    site: "my_site"
    automation_user: "my_user"
    automation_secret: "my_secret"
    path: "/my_remote_folder"
    name: "My Remote Folder"
    attributes:
      site: "my_remote_site"
    state: "present"

# Create a folder with Criticality set to a Test system and Networking Segment WAN (high latency)"
- name: "Create a folder with tag_criticality test and tag_networking wan"
  checkmk.general.folder:
    server_url: "http://my_server/"
    site: "my_site"
    automation_user: "my_user"
    automation_secret: "my_secret"
    path: "/my_remote_folder"
    attributes:
      tag_criticality: "test"
      tag_networking: "wan"
    state: "present"

# Update only specified attributes
- name: "Update only specified attributes"
  checkmk.general.folder:
    server_url: "http://my_server/"
    site: "my_site"
    automation_user: "my_user"
    automation_secret: "my_secret"
    path: "/my_folder"
    update_attributes:
      tag_networking: "dmz"
    state: "present"

# Remove specified attributes
- name: "Remove specified attributes"
  checkmk.general.folder:
    server_url: "http://my_server/"
    site: "my_site"
    automation_user: "my_user"
    automation_secret: "my_secret"
    path: "/my_folder"
    remove_attributes:
      - tag_networking
    state: "present"
"""

RETURN = r"""
message:
    description: The output message that the module generates. Contains the API response details in case of an error.
    type: str
    returned: always
    sample: 'Folder created.'
"""

import json
import sys
import traceback

# https://docs.ansible.com/ansible/latest/dev_guide/testing/sanity/import.html
from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible.module_utils.common.dict_transformations import dict_merge
from ansible_collections.checkmk.general.plugins.module_utils.api import CheckmkAPI
from ansible_collections.checkmk.general.plugins.module_utils.types import RESULT
from ansible_collections.checkmk.general.plugins.module_utils.utils import (
    result_as_dict,
)

from ansible_collections.checkmk.general.plugins.module_utils.version import (
    CheckmkVersion,
)

PYTHON_VERSION = 3
HAS_PATHLIB2_LIBRARY = True
PATHLIB2_LIBRARY_IMPORT_ERROR = None

if sys.version[0] == "3":
    from pathlib import Path
else:
    PYTHON_VERSION = 2
    try:
        from pathlib2 import Path
    except ImportError:
        HAS_PATHLIB2_LIBRARY = False
        PATHLIB2_LIBRARY_IMPORT_ERROR = traceback.format_exc()

FOLDER = (
    "name",
    "fullname",
    "customer",
    "password",
    "enforce_password_change",
    "auth_type",
    "disable_login",
    "email",
    "fallback_contact",
    "pager",
    "idle_timeout_option",
    "idle_timeout_duration",
    "roles",
    "authorized_sites",
    "contactgroups",
    "disable_notifications",
    "disable_notifications_timerange",
    "language",
    "interface_theme",
    "sidebar_position",
    "navigation_bar_icons",
    "mega_menu_icons",
    "show_mode",
    )


class FolderHTTPCodes:
    # http_code: (changed, failed, "Message")
    get = {
        200: (False, False, "Folder found, nothing changed"),
        404: (False, False, "Folder not found"),
    }

    create = {200: (True, False, "Folder created")}
    edit = {200: (True, False, "Folder modified")}
    delete = {204: (True, False, "Folder deleted")}


class FolderEndpoints:
    default = "/objects/folder_config"
    create = "/domain-types/folder_config/collections/all"


class FolderAPI(CheckmkAPI):
    def _build_folder_data(self):
        folder = {}

        folder["disable_notifications"] = {}
        folder["interface_options"] = {}

        # For some keys the API has required sub keys. We can use them as indicator,
        # that the key must be used
        if self.required.get("auth_type"):
            folder["auth_option"] = {}
        if self.required.get("email"):
            folder["contact_options"] = {}
        if self.required.get("idle_timeout_option"):
            folder["idle_timeout"] = {}

        for key, value in self.required.items():
            if key in (
                "username",
                "fullname",
                "customer",
                "disable_login",
                "roles",
                "authorized_sites",
                "contactgroups",
            ):
                folder[key] = value

            if key in "pager":
                key = "pager_address"
                folder[key] = value

            if key in "language":
                if value != "default":
                    folder["language"] = value

            if key in ("auth_type", "password", "enforce_password_change"):
                if key == "password" and self.params.get("auth_type") == "automation":
                    # Unfortunately the API uses different strings for the password
                    # depending on the kind of folder...
                    key = "secret"
                folder["auth_option"][key] = value

            if key in ("email", "fallback_contact"):
                folder["contact_options"][key] = value

            if key == "idle_timeout_option":
                folder["idle_timeout"]["option"] = value
            if key == "idle_timeout_duration":
                folder["idle_timeout"]["duration"] = value

            if key == "disable_notifications":
                folder["disable_notifications"]["disable"] = value
            if key == "disable_notifications_timerange":
                folder["disable_notifications"]["timerange"] = value

            if key in (
                "interface_theme",
                "sidebar_position",
                "navigation_bar_icons",
                "mega_menu_icons",
                "show_mode",
            ):
                folder["interface_options"][key] = value

        return folder

    def _set_current(self, result):
        # A flat hierarchy allows an easy comparison of differences
        content = json.loads(result.content)["extensions"]
        for key in FOLDER:
            if key in content:
                if key != "disable_notifications":
                    self.current[key] = content[key]
            if key in "pager" and "pager_address" in content:
                self.current[key] = content["pager_address"]
            if key in ("email", "fallback_contact") and "contact_options" in content:
                self.current[key] = content["contact_options"][key]
            if key == "idle_timeout_option":
                self.current[key] = content["idle_timeout"]["option"]
            if key == "idle_timeout_duration":
                if "duration" in content["idle_timeout"]:
                    self.current[key] = content["idle_timeout"]["duration"]
            if key == "disable_notifications":
                if "disable" in content["disable_notifications"]:
                    self.current[key] = content["disable_notifications"]["disable"]
                else:
                    self.current[key] = False
            if key == "disable_notifications_timerange":
                if "timerange" in content["disable_notifications"]:
                    self.current[key] = content["disable_notifications"]["timerange"]

            if (
                key
                in (
                    "interface_theme",
                    "sidebar_position",
                    "navigation_bar_icons",
                    "mega_menu_icons",
                    "show_mode",
                )
                and key in content["interface_options"]
            ):
                self.current[key] = content["interface_options"][key]

    def _build_default_endpoint(self):
        return "%s/%s" % (FolderEndpoints.default, self.params.get("name"))

    def build_required(self):
        # A flat hierarchy allows an easy comparison of differences
        for key in FOLDER:
            if key == "username":
                self.required[key] = self.params["name"]
                continue
            if self.params.get(key) is None:
                continue
            self.required[key] = self.params[key]

    def needs_editing(self):
        black_list = ("username", "password", "auth_type", "authorized_sites")
        for key, value in self.required.items():
            if key not in black_list and self.current.get(key) != value:
                return True
        return False

    def get(self):
        result = self._fetch(
            code_mapping=FolderHTTPCodes.get,
            endpoint=self._build_default_endpoint(),
            method="GET",
        )

        if result.http_code == 200:
            self.state = "present"
            self._set_current(result)
        else:
            self.state = "absent"
        return result

    def create(self):
        data = self._build_folder_data()
        # It's allowed in Ansible to skip the fullname, but it's not allowed
        # in the Checkmk API...
        data.setdefault("fullname", data["username"])

        result = self._fetch(
            code_mapping=FolderHTTPCodes.create,
            endpoint=FolderEndpoints.create,
            data=data,
            method="POST",
        )

        return result

    def edit(self, etag):
        data = self._build_folder_data()
        self.headers["if-Match"] = etag

        result = self._fetch(
            code_mapping=FolderHTTPCodes.edit,
            endpoint=self._build_default_endpoint(),
            data=data,
            method="PUT",
        )

        return result

    def delete(self):
        result = self._fetch(
            code_mapping=FolderHTTPCodes.delete,
            endpoint=self._build_default_endpoint(),
            method="DELETE",
        )

        return result

# 
# 
# def exit_failed(module, msg):
#     result = {"msg": msg, "changed": False, "failed": True}
#     module.fail_json(**result)
# 
# 
# def exit_changed(module, msg):
#     result = {"msg": msg, "changed": True, "failed": False}
#     module.exit_json(**result)
# 
# 
# def exit_ok(module, msg):
#     result = {"msg": msg, "changed": False, "failed": False}
#     module.exit_json(**result)
# 
# 
# def cleanup_path(path):
#     p = Path(path)
#     if not p.is_absolute():
#         p = Path("/").joinpath(p)
#     return str(p.parent).lower(), p.name
# 
# 
# def path_for_url(module):
#     return module.params["path"].replace("/", "~")
# 
# 
# def get_version(module, base_url, headers):
#     api_endpoint = "version"
#     url = base_url + api_endpoint
# 
#     response, info = fetch_url(module, url, data=None, headers=headers, method="GET")
# 
#     if info["status"] != 200:
#         exit_failed(
#             module,
#             "Error calling API. HTTP code %d. Details: %s, "
#             % (info["status"], info["body"]),
#         )
# 
#     checkmkinfo = json.loads(json.loads(response.read()))
#     return (checkmkinfo.get("versions").get("checkmk")).split(".")
# 
# 
# def get_current_folder_state(module, base_url, headers):
#     current_state = "unknown"
#     current_explicit_attributes = {}
#     current_title = ""
#     etag = ""
# 
#     api_endpoint = "/objects/folder_config/" + path_for_url(module)
#     parameters = "?show_hosts=false"
#     url = base_url + api_endpoint + parameters
# 
#     response, info = fetch_url(module, url, data=None, headers=headers, method="GET")
# 
#     if info["status"] == 200:
#         body = json.loads(response.read())
#         current_state = "present"
#         etag = info.get("etag", "")
#         extensions = body.get("extensions", {})
#         current_explicit_attributes = extensions.get("attributes", {})
#         current_title = "%s" % body.get("title", "")
#         if "meta_data" in current_explicit_attributes:
#             del current_explicit_attributes["meta_data"]
# 
#     elif info["status"] == 404:
#         current_state = "absent"
# 
#     else:
#         exit_failed(
#             module,
#             "Error calling API. HTTP code %d. Details: %s. URL: %s. Parameters: %s"
#             % (info["status"], info.get("body", "N/A"), url, parameters),
#         )
# 
#     return current_state, current_explicit_attributes, current_title, etag
# 
# 
# def set_folder_attributes(module, base_url, headers, params):
#     api_endpoint = "/objects/folder_config/" + path_for_url(module)
#     url = base_url + api_endpoint
# 
#     response, info = fetch_url(
#         module, url, module.jsonify(params), headers=headers, method="PUT"
#     )
# 
#     if (
#         info["status"] == 400
#         and params.get("remove_attributes")
#         and not params.get("title")
#         and not params.get("attributes")
#         and not params.get("update_attributes")
#     ):
#         # "Folder attributes allready removed."
#         return False
#     elif info["status"] != 200:
#         exit_failed(
#             module,
#             "Error calling API. HTTP code %d. Details: %s, "
#             % (info["status"], info["body"]),
#         )
# 
#     return True
# 
# 
# def create_folder(module, attributes, base_url, headers):
#     parent, foldername = cleanup_path(module.params["path"])
#     name = module.params.get("name", foldername)
# 
#     api_endpoint = "/domain-types/folder_config/collections/all"
#     params = {
#         "name": foldername,
#         "title": name,
#         "parent": parent,
#         "attributes": attributes if attributes else {},
#     }
#     url = base_url + api_endpoint
# 
#     response, info = fetch_url(
#         module, url, module.jsonify(params), headers=headers, method="POST"
#     )
# 
#     if info["status"] != 200:
#         exit_failed(
#             module,
#             "Error calling API. HTTP code %d. Details: %s, URL: %s, Params: %s, "
#             % (info["status"], info["body"], url, str(params)),
#         )
# 
# 
# def delete_folder(module, base_url, headers):
#     api_endpoint = "/objects/folder_config/" + path_for_url(module)
#     url = base_url + api_endpoint
# 
#     response, info = fetch_url(module, url, data=None, headers=headers, method="DELETE")
# 
#     if info["status"] != 204:
#         exit_failed(
#             module,
#             "Error calling API. HTTP code %d. Details: %s, "
#             % (info["status"], info["body"]),
#         )
# 
# 
# def get_version_ge_220p7(module, checkmkversion):
#     if "p" in checkmkversion[2]:
#         patchlevel = checkmkversion[2].split("p")
#         patchtype = "p"
#     elif "a" in checkmkversion[2]:
#         patchlevel = checkmkversion[2].split("a")
#         patchtype = "a"
#     elif "b" in checkmkversion[2]:
#         patchlevel = checkmkversion[2].split("b")
#         patchtype = "b"
#     else:
#         exit_failed(
#             module,
#             "Not supported patch-level schema: %s" % (checkmkversion[2]),
#         )
# 
#     if (
#         int(checkmkversion[0]) > 2
#         or (int(checkmkversion[0]) == 2 and int(checkmkversion[1]) > 2)
#         or (
#             int(checkmkversion[0]) == 2
#             and int(checkmkversion[1]) == 2
#             and int(patchlevel[0]) > 0
#         )
#         or (
#             int(checkmkversion[0]) == 2
#             and int(checkmkversion[1]) == 2
#             and int(patchlevel[0]) == 0
#             and patchtype == "p"
#             and int(patchlevel[1]) >= 7
#         )
#     ):
#         return True
#     else:
#         return False


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        server_url=dict(type="str", required=True),
        site=dict(type="str", required=True),
        validate_certs=dict(type="bool", required=False, default=True),
        automation_user=dict(type="str", required=True),
        automation_secret=dict(type="str", required=True, no_log=True),
        path=dict(type="str", required=True),
        name=dict(
            type="str",
            required=False,
            aliases=["title"],
        ),
        attributes=dict(type="raw", required=False),
        remove_attributes=dict(type="raw", required=False),
        update_attributes=dict(type="raw", required=False),
        state=dict(
            type="str", required=False, default="present", choices=["present", "absent"]
        ),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    # Use the parameters to initialize some common api variables
    folder = FolderAPI(module)

    folder.build_required()
    result = folder.get()
    etag = result.etag

    required_state = folder.params.get("state")
    if folder.state == "present":
        if required_state == "reset_password":
            folder.required.pop("username")
            result = folder.edit(etag)
        elif required_state == "absent":
            result = folder.delete()
        elif folder.needs_editing():
            folder.required.pop("username")
            result = folder.edit(etag)
    elif folder.state == "absent":
        if required_state in ("present", "reset_password"):
            result = folder.create()

    module.exit_json(**result_as_dict(result))

#     # Handle library import error according to the following link:
#     # https://docs.ansible.com/ansible/latest/dev_guide/testing/sanity/import.html
#     if PYTHON_VERSION == 2 and not HAS_PATHLIB2_LIBRARY:
#         # Needs: from ansible.module_utils.basic import missing_required_lib
#         module.fail_json(
#             msg=missing_required_lib("pathlib2"),
#             exception=PATHLIB2_LIBRARY_IMPORT_ERROR,
#         )
# 
#     # Use the parameters to initialize some common variables
#     headers = {
#         "Accept": "application/json",
#         "Content-Type": "application/json",
#         "Authorization": "Bearer %s %s"
#         % (
#             module.params.get("automation_user", ""),
#             module.params.get("automation_secret", ""),
#         ),
#     }
# 
#     base_url = "%s/%s/check_mk/api/1.0" % (
#         module.params.get("server_url", ""),
#         module.params.get("site", ""),
#     )
# 
#     count_options = sum(
#         [
#             1
#             for el in ["attributes", "remove_attributes", "update_attributes"]
#             if module.params.get(el)
#         ]
#     )
# 
#     if count_options > 1:
#         checkmkversion = get_version(module, base_url, headers)
# 
#         version_ge_220p7 = get_version_ge_220p7(module, checkmkversion)
# 
#         if version_ge_220p7:
#             exit_failed(
#                 module,
#                 "As of Check MK v2.2.0p7 and v2.3.0b1, simultaneous use of attributes, remove_attributes, and update_attributes is no longer supported.",
#             )
#         else:
#             module.warn(
#                 "As of Check MK v2.2.0p7 and v2.3.0b1, simultaneous use of attributes, remove_attributes, and update_attributes is no longer supported."
#             )
# 
#     # Determine desired state and attributes
#     attributes = module.params.get("attributes")
#     remove_attributes = module.params.get("remove_attributes")
#     update_attributes = module.params.get("update_attributes")
#     if attributes == []:
#         attributes = {}
# 
#     state = module.params.get("state", "present")
# 
#     # Determine the current state of this particular folder
#     (
#         current_state,
#         current_explicit_attributes,
#         current_title,
#         etag,
#     ) = get_current_folder_state(module, base_url, headers)
# 
#     # Handle the folder accordingly to above findings and desired state
#     if state == "present" and current_state == "present":
#         headers["If-Match"] = etag
#         msg_tokens = []
# 
#         if update_attributes:
#             merged_attributes = dict_merge(
#                 current_explicit_attributes, update_attributes
#             )
# 
#         params = {}
#         changed = False
#         if module.params["name"] and current_title != module.params["name"]:
#             params["title"] = module.params.get("name")
#             changed = True
# 
#         if attributes and current_explicit_attributes != attributes:
#             params["attributes"] = attributes
#             changed = True
# 
#         if update_attributes and current_explicit_attributes != merged_attributes:
#             params["update_attributes"] = merged_attributes
#             changed = True
# 
#         if remove_attributes:
#             for el in remove_attributes:
#                 if current_explicit_attributes.get(el):
#                     changed = True
#                     break
#             params["remove_attributes"] = remove_attributes
# 
#         if params != {}:
#             if not module.check_mode:
#                 changed = set_folder_attributes(module, base_url, headers, params)
# 
#             if changed:
#                 msg_tokens.append("Folder attributes updated.")
# 
#         if len(msg_tokens) >= 1:
#             exit_changed(module, " ".join(msg_tokens))
#         else:
#             exit_ok(
#                 module, "Folder already present. All explicit attributes as desired."
#             )
# 
#     elif state == "present" and current_state == "absent":
#         if (update_attributes and update_attributes != {}) and (
#             not attributes or attributes == {}
#         ):
#             attributes = update_attributes
#         if not module.check_mode:
#             create_folder(module, attributes, base_url, headers)
#         exit_changed(module, "Folder created.")
# 
#     elif state == "absent" and current_state == "absent":
#         exit_ok(module, "Folder already absent.")
# 
#     elif state == "absent" and current_state == "present":
#         if not module.check_mode:
#             delete_folder(module, base_url, headers)
#         exit_changed(module, "Folder deleted.")
# 
#     else:
#         exit_failed(module, "Unknown error")


def main():
    run_module()


if __name__ == "__main__":
    main()

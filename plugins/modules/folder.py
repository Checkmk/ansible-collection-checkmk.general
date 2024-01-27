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
              B(If a list of strings is supplied, the listed attributes are removed.)
              B(If instead a dict is supplied, the attributes {key: value} that exactly match the passed attributes are removed.)
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
from ansible.module_utils.common.dict_transformations import dict_merge, recursive_diff
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
    "customer",
    "attributes",
    "update_attributes",
    "remove_attributes",
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
    def __init__(self, module):
        super().__init__(module)

        self.desired = {}

        (self.desired["parent"], self.desired["name"]) = _normalize_path(
            self.params.get("path")
        )
        self.desired["title"] = self.params.get("title", self.desired["name"])

        for key in FOLDER:
            if self.params.get(key):
                self.desired[key] = self.params.get(key)

        # Get the current folder from the API and set some parameters
        self._get_current()
        self._changed_items = self._detect_changes()

        self._verify_compatibility()

    def _verify_compatibility(self):
        # Check if parameters are compatible with CMK version
        if (
            sum(
                [
                    1
                    for el in ["attributes", "remove_attributes", "update_attributes"]
                    if self.module.params.get(el)
                ]
            )
            > 1
        ):

            ver = self.getversion()
            msg = (
                "As of Check MK v2.2.0p7 and v2.3.0b1, simultaneous use of"
                " attributes, remove_attributes, and update_attributes is no longer supported."
            )

            if ver >= CheckmkVersion("2.2.0p7"):
                result = RESULT(
                    http_code=0,
                    msg=msg,
                    content="",
                    etag="",
                    failed=True,
                    changed=False,
                )
                self.module.exit_json(**result_as_dict(result))
            else:
                self.module.warn(msg)

    @staticmethod
    def _normalize_path(path):
        p = Path(path)
        if not p.is_absolute():
            p = Path("/").joinpath(p)
        return str(p.parent).lower(), p.name

    @staticmethod
    def _urlize_path(path):
        return path.replace("/", "~").replace("~~", "~")

    def _build_default_endpoint(self):
        return "%s/%s" % (
            FolderEndpoints.default,
            _urlize_path("%s/%s" % (self.desired["parent"], self.desired["name"])),
        )

    def _detect_changes(self):
        current_attributes = self.current.get("attributes", {})
        desired_attributes = self.desired.copy()
        changes = []

        if desired_attributes.get("update_attributes"):
            merged_attributes = dict_merge(
                current_attributes, desired_attributes.get("update_attributes")
            )

            if merged_attributes != current_attributes:
                try:
                    (_, m_c) = recursive_diff(current_attributes, merged_attributes)
                    changes.append("update attributes: %" % json.dumps(m_c))
                except Exception as e:
                    changes.append("update attributes")
                desired_attributes["update_attributes"] = merged_attributes

        if desired_attributes.get(
            "attributes"
        ) and current_attributes != desired_attributes.get("attributes"):
            changes.append("attributes")

        if self.current.get("title") != desired_attributes.get("title"):
            changes.append("title")

        if desired_attributes.get("remove_attributes"):
            tmp_remove_attributes = desired_attributes.get("remove_attributes")
            if isinstance(tmp_remove_attributes, list):
                removes_which = [a for a in tmp_remove_attributes if current_attributes.get(a)]
                if len(removes_which) > 0:
                    changes.append("remove attributes: %s" % " ".join(removes_which) )
            elif isinstance(tmp_remove_attributes, dict):
                try:
                    (c_m, _) = recursive_diff(current_attributes, tmp_remove_attributes)
                    (c_c_m, _) = recursive_diff(current_attributes, c_m)
                    if c_c_m:
                        changes.append("remove attributes: %" % json.dumps(c_c_m))
                        self.desired.pop("remove_attributes")
                        self.desired["retained_attributes"] = c_m
                except Exception as e:
                    module.fail_json(
                        msg="ERROR: incompatible parameter: remove_attributes!",
                        exception=e,
                    )
            else:
                module.fail_json(
                    msg="ERROR: The parameter remove_attributes can be a list of strings or a dictionary!",
                    exception=e,
                )

        return changes

    def _get_current(self):
        result = self._fetch(
            code_mapping=FolderHTTPCodes.get,
            endpoint=self._build_default_endpoint(),
            method="GET",
        )

        if result.http_code == 200:
            self.state = "present"

            content = json.loads(result.content)

            self.current["title"] = content["title"]

            extensions = content["extensions"]
            for key, value in extensions.items():
                if key == "attributes":
                    value.pop("meta_data")
                self.current[key] = value

            self.etag = result.etag

        else:
            self.state = "absent"

    def _check_output(self, mode):
        return RESULT(
            http_code=0,
            msg="Running in check mode. Would have done an %s" % mode,
            content="",
            etag="",
            failed=False,
            changed=False,
        )

    def needs_update(self):
        return len(self._changed_items) > 0

    def needs_reduction(self):
        return ("retained_attributes" in self.desired)

    def create(self):
        data = self.desired.copy()
        if not data.get("attributes"):
            data["attributes"] = data.pop("update_attributes", {})

        if data.get("remove_attributes"):
            data.pop("remove_attributes")

        if data.get("retained_attributes"):
            data.pop("retained_attributes")

        if self.module.check_mode:
            return self._check_output("create")

        result = self._fetch(
            code_mapping=FolderHTTPCodes.create,
            endpoint=FolderEndpoints.create,
            data=data,
            method="POST",
        )

        return result

    def edit(self):
        data = self.desired.copy()
        data.pop("name")
        data.pop("parent")
        self.headers["if-Match"] = self.etag

        if data.get("retained_attributes"):
            data.pop("retained_attributes")

        if self.module.check_mode:
            return self._check_output("edit")

        result = self._fetch(
            code_mapping=FolderHTTPCodes.edit,
            endpoint=self._build_default_endpoint(),
            data=data,
            method="PUT",
        )

        return result._replace(
            msg=result.msg + ". Changed: %s" % ", ".join(self._changed_items)
        )

    def reduct(self):
        data = self.desired.copy()

        if data.get("attributes"):
            data.pop("attributes")

        if data.get("update_attributes"):
            data.pop("remove_attributes")

        if data.get("remove_attributes"):
            data.pop("remove_attributes")

        if self.module.check_mode:
            return self._check_output("reduct (remove_attributes supplied by dict object)")

        result = self._fetch(
            code_mapping=FolderHTTPCodes.create,
            endpoint=FolderEndpoints.create,
            data=data,
            method="POST",
        )

        return result._replace(
            msg=result.msg + ". Changed: %s" % ", ".join(self._changed_items)
        )

    def delete(self):
        if self.module.check_mode:
            return self._check_output("delete")

        result = self._fetch(
            code_mapping=FolderHTTPCodes.delete,
            endpoint=self._build_default_endpoint(),
            method="DELETE",
        )

        return result


def _exit_if_missing_pathlib(module):
    # Handle library import error according to the following link:
    # https://docs.ansible.com/ansible/latest/dev_guide/testing/sanity/import.html
    if PYTHON_VERSION == 2 and not HAS_PATHLIB2_LIBRARY:
        # Needs: from ansible.module_utils.basic import missing_required_lib
        module.fail_json(
            msg=missing_required_lib("pathlib2"),
            exception=PATHLIB2_LIBRARY_IMPORT_ERROR,
        )


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

    _exit_if_missing_pathlib(module)

    # Create an API object that contains the current and desired state
    current_folder = FolderAPI(module)

    result = RESULT(
        http_code=0,
        msg="No changes needed.",
        content="",
        etag="",
        failed=False,
        changed=False,
    )

    desired_state = current_folder.params.get("state")
    if current_folder.state == "present":
        result = result._replace(
            msg="Folder already exists with the desired parameters."
        )
        if desired_state == "absent":
            result = current_folder.delete()
        else:
            if current_folder.needs_update():
                result = current_folder.edit()
            if current_folder.needs_reduction()
                result = current_folder.reduct()
    elif current_folder.state == "absent":
        result = result._replace(msg="Folder already absent.")
        if desired_state in ("present"):
            result = current_folder.create()

    module.exit_json(**result_as_dict(result))


def main():
    run_module()


if __name__ == "__main__":
    main()

#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2022, Robin Gierse <robin.gierse@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: folder

short_description: Manage folders in Checkmk

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "0.0.1"

description:
    - Manage folders within Checkmk.
    - Folders are used to organize hosts and can carry attributes that are inherited
      by all hosts within them.

extends_documentation_fragment: [checkmk.general.common]

options:
    path:
        description:
            - The full path to the folder you want to manage.
              Pay attention to the leading C(/) and avoid trailing C(/).
              Special characters apart from C(_) are not allowed!
              Missing parent folders will be created.
        required: true
        type: str
    name:
        description: The name (title) of your folder. If omitted defaults to the string after the last C(/) in I(path).
        required: false
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
              B(If extended_functionality and a dict is supplied, the attributes that exactly match
              the passed attributes are removed.)
              This will only remove the given attributes.
              As of Check MK v2.2.0p7 and v2.3.0b1, simultaneous use of I(attributes),
              I(remove_attributes), and I(update_attributes) is no longer supported.
        type: raw
        required: false
    state:
        description: The state of your folder.
        required: false
        type: str
        default: present
        choices: ["present", "absent"]
    extended_functionality:
        description: Allow extended functionality instead of the expected REST API behavior.
        required: false
        type: bool
        default: true

seealso:
    - plugin: checkmk.general.folder
      plugin_type: lookup
    - plugin: checkmk.general.folders
      plugin_type: lookup
    - module: checkmk.general.host

author:
    - Robin Gierse (@robin-checkmk)
    - Lars Getwan (@lgetwan)
    - Michael Sekania (@msekania)
"""

EXAMPLES = r"""
# ---------------------------------------------------------------------------
# Create and delete folders
# ---------------------------------------------------------------------------

- name: "Create a folder."
  checkmk.general.folder:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    path: "/myfolder"
    name: "My Folder"
    state: "present"

- name: "Create a nested folder."
  checkmk.general.folder:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    path: "/myfolder/mysubfolder"
    name: "My Subfolder"
    state: "present"

- name: "Delete a folder."
  checkmk.general.folder:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    path: "/myfolder"
    state: "absent"

# ---------------------------------------------------------------------------
# Create folders with attributes
# ---------------------------------------------------------------------------
# The 'attributes' option OVERWRITES all existing attributes on the folder.
# Use 'update_attributes' to only change specific attributes.

- name: "Create a folder and pin its hosts to a specific monitoring site."
  checkmk.general.folder:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    path: "/myfolder"
    name: "My Folder"
    attributes:
      site: "myremotesite"
    state: "present"

- name: "Create a folder with host tags set."
  checkmk.general.folder:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    path: "/myfolder"
    name: "My Folder"
    attributes:
      tag_criticality: "test"
      tag_networking: "wan"
    state: "present"

# ---------------------------------------------------------------------------
# Update and remove attributes
# ---------------------------------------------------------------------------

- name: "Update specific attributes on a folder without touching others."
  checkmk.general.folder:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    path: "/myfolder"
    update_attributes:
      tag_networking: "wan"
    state: "present"

- name: "Remove specific attributes from a folder."
  checkmk.general.folder:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    path: "/myfolder"
    remove_attributes:
      - tag_networking
    state: "present"

- name: "Remove multiple attributes from a folder."
  checkmk.general.folder:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    path: "/myfolder"
    remove_attributes:
      - tag_networking
      - tag_criticality
    state: "present"

# ---------------------------------------------------------------------------
# Using environment variables for authentication
# ---------------------------------------------------------------------------
# Connection parameters can be provided via environment variables instead of
# task parameters. The supported variables are:
#   CHECKMK_VAR_SERVER_URL, CHECKMK_VAR_SITE,
#   CHECKMK_VAR_API_USER, CHECKMK_VAR_API_SECRET,
#   CHECKMK_VAR_VALIDATE_CERTS

- name: "Create a folder using environment variables for authentication."
  checkmk.general.folder:
    path: "/myfolder"
    name: "My Folder"
    state: "present"
  environment:
    CHECKMK_VAR_SERVER_URL: "https://myserver/"
    CHECKMK_VAR_SITE: "mysite"
    CHECKMK_VAR_API_USER: "myuser"
    CHECKMK_VAR_API_SECRET: "mysecret"
    CHECKMK_VAR_VALIDATE_CERTS: "true"
"""

RETURN = r"""
msg:
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
from ansible.module_utils.common.validation import check_type_list
from ansible_collections.checkmk.general.plugins.module_utils.api import CheckmkAPI
from ansible_collections.checkmk.general.plugins.module_utils.logger import Logger
from ansible_collections.checkmk.general.plugins.module_utils.types import RESULT
from ansible_collections.checkmk.general.plugins.module_utils.utils import (
    base_argument_spec,
    exit_module,
)
from ansible_collections.checkmk.general.plugins.module_utils.version import (
    CheckmkVersion,
)

logger = Logger()

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

FOLDER_PARENTS_PARSE = (
    "attributes",
    "update_attributes",
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

        self.extended_functionality = self.params.get("extended_functionality", True)

        self.desired = {}

        self.desired["parent"], self.desired["name"] = self._normalize_path(
            self.params.get("path")
        )

        if self.params.get("name"):
            self.desired["title"] = self.params.get("name")
        else:
            self.desired["title"] = self.desired.get("name")

        for key in FOLDER:
            if self.params.get(key):
                self.desired[key] = self.params.get(key)

        for key in FOLDER_PARENTS_PARSE:
            if self.desired.get(key):
                if self.desired.get(key).get("parents"):
                    self.desired[key]["parents"] = check_type_list(
                        self.desired.get(key).get("parents")
                    )

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
                exit_module(self.module, result=result, logger=logger)
            else:
                self.module.warn(msg)

    def _normalize_path(self, path):
        p = Path(path)
        if not p.is_absolute():
            p = Path("/").joinpath(p)
        return str(p.parent), p.name

    def _urlize_path(self, path):
        return path.replace("/", "~").replace("~~", "~")

    def _build_default_endpoint(self, path=None):
        if not path:
            return "%s/%s" % (
                FolderEndpoints.default,
                self._urlize_path(
                    "%s/%s" % (self.desired["parent"], self.desired["name"])
                ),
            )
        else:
            return "%s/%s" % (
                FolderEndpoints.default,
                self._urlize_path(path),
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
                    c_m, m_c = recursive_diff(current_attributes, merged_attributes)
                    changes.append("update attributes: %s" % json.dumps(m_c))
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
                removes_which = [
                    a for a in tmp_remove_attributes if current_attributes.get(a)
                ]
                if len(removes_which) > 0:
                    changes.append("remove attributes: %s" % " ".join(removes_which))
            elif isinstance(tmp_remove_attributes, dict):
                if not self.extended_functionality:
                    self.module.fail_json(
                        msg="ERROR: The parameter remove_attributes of dict type is not supported for the paramter extended_functionality: false!",
                    )

                tmp_remove, tmp_rest = (current_attributes, {})
                if current_attributes != tmp_remove_attributes:
                    try:
                        c_m, m_c = recursive_diff(
                            current_attributes, tmp_remove_attributes
                        )

                        if c_m:
                            # if nothing to remove
                            if current_attributes == c_m:
                                tmp_remove, tmp_rest = ({}, current_attributes)
                            else:
                                c_c_m, c_m_c = recursive_diff(current_attributes, c_m)
                                tmp_remove, tmp_rest = (c_c_m, c_m)
                    except Exception as e:
                        self.module.fail_json(
                            msg="ERROR: incompatible parameter: remove_attributes!",
                            exception=e,
                        )

                desired_attributes.pop("remove_attributes")
                if tmp_remove != {}:
                    changes.append("remove attributes: %s" % json.dumps(tmp_remove))
                    if tmp_rest != {}:
                        desired_attributes["update_attributes"] = tmp_rest
            else:
                self.module.fail_json(
                    msg="ERROR: The parameter remove_attributes can be a list of strings or a dictionary!",
                    exception=e,
                )

        if self.extended_functionality:
            self.desired = desired_attributes.copy()

        # self.module.fail_json(json.dumps(desired_attributes))

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
                    if "network_scan_result" in value:
                        value.pop("network_scan_result")
                self.current[key] = value

            self.etag = result.etag

        else:
            self.state = "absent"
        logger.debug("state: %s" % self.state)

    def _check_output(self, mode):
        return RESULT(
            http_code=0,
            msg="Running in check mode. Would have done an %s" % mode,
            content="",
            etag="",
            failed=False,
            changed=True,
        )

    def needs_update(self):
        return len(self._changed_items) > 0

    def _ensure_parent_exists(self, parent):
        logger.debug("Ensure that path %s exists" % parent)

        result = self._fetch(
            code_mapping=FolderHTTPCodes.get,
            endpoint=self._build_default_endpoint(parent),
            method="GET",
        )

        if result.http_code 200:
            logger.debug("-> exists")
            return result
        else:
            logger.debug("-> missing")
            grandparent, parent = self._normalize_path(parent)
            result = self._ensure_parent_exists(grandparent)
            if result.http_code != 200:
                return result

            logger.debug("Creating parent folder %s" % parent)
            data = {
                "name": parent,
                "title": parent,
                "parent": grandparent,
            }

            if self.module.check_mode:
                return self._check_output("create parent")

            return self._fetch(
                code_mapping=FolderHTTPCodes.create,
                endpoint=FolderEndpoints.create,
                data=data,
                method="POST",
            )

    def create(self):
        logger.debug("Will create the folder")
        data = self.desired.copy()
        result = self._ensure_parent_exists(data.get("parent"))
        if result.http_code != 200:
            exit_module(
                self.module,
                msg="Failed to create parent folder(s).",
                content=result.content,
                failed=True,
                logger=logger,
            )

        if data.get("attributes", {}) == {}:
            data["attributes"] = data.pop("update_attributes", {})

        if data.get("remove_attributes"):
            data.pop("remove_attributes")

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
        logger.debug("Will update the folder")
        logger.debug("diff: %s" % str(self._changed_items))
        data = self.desired.copy()
        data.pop("name")
        data.pop("parent")
        self.headers["if-Match"] = self.etag

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
        exit_module(
            module,
            msg=missing_required_lib("pathlib2") + str(PATHLIB2_LIBRARY_IMPORT_ERROR) + "\n",
            failed=True,
            logger=logger,
        )


def run_module():
    argument_spec = base_argument_spec()
    argument_spec.update(
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
        extended_functionality=dict(type="bool", required=False, default=True),
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    logger.set_loglevel(module._verbosity)
    logger.set_loglevel(2)

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
        elif current_folder.needs_update():
            result = current_folder.edit()
    elif current_folder.state == "absent":
        result = result._replace(msg="Folder already absent.")
        if desired_state in ("present"):
            result = current_folder.create()

    exit_module(module, result=result, logger=logger)


def main():
    run_module()


if __name__ == "__main__":
    main()

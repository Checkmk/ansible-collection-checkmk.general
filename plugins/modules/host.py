#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2022, Robin Gierse <robin.gierse@checkmk.com>
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

extends_documentation_fragment: [checkmk.general.common]

options:
    name:
        description: The host you want to manage.
        required: true
        type: str
    folder:
        description: The folder your host is located in. On create it defaults to C(/).
        type: str
    attributes:
        description:
            - The attributes of your host as described in the API documentation.
              B(Attention! This option OVERWRITES all existing attributes!)
              If you are using custom tags, make sure to prepend the attribute with C(tag_).
        type: raw
        required: false
    update_attributes:
        description:
            - The update_attributes of your host as described in the API documentation.
              This will only update the given attributes.
              If you are using custom tags, make sure to prepend the attribute with C(tag_).
        type: raw
        required: false
    remove_attributes:
        description:
            - The remove_attributes of your host as described in the API documentation.
              B(If a list of strings is supplied, the listed attributes are removed.)
              B(If extended_functionality and a dict is supplied, the attributes that exactly match
              the passed attributes are removed.)
              This will only remove the given attributes.
              If you are using custom tags, make sure to prepend the attribute with C(tag_).
              As of Check MK v2.2.0p7 and v2.3.0b1, simultaneous use of I(attributes),
              I(remove_attributes), and I(update_attributes) is no longer supported.
        type: raw
        required: false
    state:
        description: The state of your host.
        type: str
        default: present
        choices: [present, absent]
    extended_functionality:
        description: Allow extended functionality instead of the expected REST API behavior.
        type: bool
        default: true

author:
    - Robin Gierse (@robin-checkmk)
    - Lars Getwan (@lgetwan)
    - Oliver Gaida (@ogaida)
"""

EXAMPLES = r"""
# Create a host.
- name: "Create a host."
  checkmk.general.host:
    server_url: "http://my_server/"
    site: "my_site"
    automation_user: "my_user"
    automation_secret: "my_secret"
    name: "my_host"
    folder: "/"
    state: "present"

# Create a host with IP.
- name: "Create a host with IP address."
  checkmk.general.host:
    server_url: "http://my_server/"
    site: "my_site"
    automation_user: "my_user"
    automation_secret: "my_secret"
    name: "my_host"
    attributes:
      alias: "My Host"
      ipaddress: "127.0.0.1"
    folder: "/"
    state: "present"

# Create a host which is monitored on a distinct site.
- name: "Create a host which is monitored on a distinct site."
  checkmk.general.host:
    server_url: "http://my_server/"
    site: "my_site"
    automation_user: "my_user"
    automation_secret: "my_secret"
    name: "my_host"
    attributes:
      site: "my_remote_site"
    folder: "/"
    state: "present"

# Create a host with update_attributes.
- name: "Create a host which is monitored on a distinct site."
  checkmk.general.host:
    server_url: "http://my_server/"
    site: "my_site"
    automation_user: "my_user"
    automation_secret: "my_secret"
    name: "my_host"
    update_attributes:
      site: "my_remote_site"
    state: "present"

# Update only specified attributes
- name: "Update only specified attributes"
  checkmk.general.host:
    server_url: "http://my_server/"
    site: "my_site"
    automation_user: "my_user"
    automation_secret: "my_secret"
    name: "my_host"
    update_attributes:
      alias: "foo"
    state: "present"

# Remove specified attributes
- name: "Remove specified attributes"
  checkmk.general.host:
    server_url: "http://my_server/"
    site: "my_site"
    automation_user: "my_user"
    automation_secret: "my_secret"
    name: "my_host"
    remove_attributes:
      - alias
    state: "present"

# Add custom tags to a host (note the leading 'tag_')
- name: "Remove specified attributes"
  checkmk.general.host:
    server_url: "http://my_server/"
    site: "my_site"
    automation_user: "my_user"
    automation_secret: "my_secret"
    name: "my_host"
    update_attributes:
      - tag_my_tag_1: "Bar"
      - tag_my_tag_2: "Foo"
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
from ansible.module_utils.common.dict_transformations import dict_merge, recursive_diff
from ansible.module_utils.common.validation import check_type_list
from ansible_collections.checkmk.general.plugins.module_utils.api import CheckmkAPI
from ansible_collections.checkmk.general.plugins.module_utils.types import RESULT
from ansible_collections.checkmk.general.plugins.module_utils.utils import (
    result_as_dict,
)
from ansible_collections.checkmk.general.plugins.module_utils.version import (
    CheckmkVersion,
)

HOST = (
    "attributes",
    "update_attributes",
    "remove_attributes",
)

HOST_PARENTS_PARSE = (
    "attributes",
    "update_attributes",
)


class HostHTTPCodes:
    # http_code: (changed, failed, "Message")
    get = {
        200: (False, False, "Host found, nothing changed"),
        404: (False, False, "Host not found"),
    }

    create = {200: (True, False, "Host created")}
    edit = {200: (True, False, "Host modified")}
    move = {200: (True, False, "Host moved")}
    delete = {204: (True, False, "Host deleted")}


class HostEndpoints:
    default = "/objects/host_config"
    create = "/domain-types/host_config/collections/all"


class HostAPI(CheckmkAPI):
    def __init__(self, module):
        super().__init__(module)

        self.extended_functionality = self.params.get("extended_functionality", True)

        self.desired = {}

        self.desired["host_name"] = self.params.get("name")

        for key in HOST:
            if self.params.get(key):
                self.desired[key] = self.params.get(key)

        for key in HOST_PARENTS_PARSE:
            if self.desired.get(key):
                if self.desired.get(key).get("parents"):
                    self.desired[key]["parents"] = check_type_list(
                        self.desired.get(key).get("parents")
                    )

        # Get the current host from the API and set some parameters
        self._get_current()
        tmp_folder = self.params.get("folder")
        if not tmp_folder:
            tmp_folder = self.current.get("folder", "/")
        self.desired["folder"] = tmp_folder
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

    def _normalize_folder(self, folder):
        if folder in ["", " ", "/", "//"]:
            return "/"

        if not folder.startswith("/"):
            folder = "/%s" % folder

        if folder.endswith("/"):
            folder = folder.rstrip("/")

        return folder

    def _build_default_endpoint(self):
        return "%s/%s" % (
            HostEndpoints.default,
            self.desired["host_name"],
        )

    def _build_move_endpoint(self):
        return "%s/%s/actions/move/invoke" % (
            HostEndpoints.default,
            self.desired["host_name"],
        )

    ###
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
                    (c_m, m_c) = recursive_diff(current_attributes, merged_attributes)
                    changes.append("update attributes: %s" % json.dumps(m_c))
                except Exception as e:
                    changes.append("update attributes")
                desired_attributes["update_attributes"] = merged_attributes

        if desired_attributes.get(
            "attributes"
        ) and current_attributes != desired_attributes.get("attributes"):
            changes.append("attributes")

        if self.current.get("folder") != desired_attributes.get("folder"):
            changes.append("folder")

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

                (tmp_remove, tmp_rest) = (current_attributes, {})
                if current_attributes != tmp_remove_attributes:
                    try:
                        (c_m, m_c) = recursive_diff(
                            current_attributes, tmp_remove_attributes
                        )

                        if c_m:
                            # if nothing to remove
                            if current_attributes == c_m:
                                (tmp_remove, tmp_rest) = ({}, current_attributes)
                            else:
                                (c_c_m, c_m_c) = recursive_diff(current_attributes, c_m)
                                (tmp_remove, tmp_rest) = (c_c_m, c_m)
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

    ###
    def _get_current(self):
        result = self._fetch(
            code_mapping=HostHTTPCodes.get,
            endpoint=self._build_default_endpoint(),
            method="GET",
        )

        if result.http_code == 200:
            self.state = "present"

            content = json.loads(result.content)

            extensions = content["extensions"]
            self.current["folder"] = extensions.get("folder", "/")
            for key, value in extensions.items():
                if key == "attributes":
                    value.pop("meta_data")
                    if "network_scan_results" in value:
                        value.pop("network_scan_results")
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

    ###
    def needs_update(self):
        return len(self._changed_items) > 0

    ###
    def create(self):
        data = self.desired.copy()
        if data.get("attributes", {}) == {}:
            data["attributes"] = data.pop("update_attributes", {})

        if data.get("remove_attributes"):
            data.pop("remove_attributes")

        if self.module.check_mode:
            return self._check_output("create")

        result = self._fetch(
            code_mapping=HostHTTPCodes.create,
            endpoint=HostEndpoints.create,
            data=data,
            method="POST",
        )

        return result

    def edit(self):
        data = self.desired.copy()
        data.pop("host_name")

        tmp = {}
        tmp["target_folder"] = data.get("folder", "/")
        self.headers["if-Match"] = self.etag

        if self.module.check_mode:
            return self._check_output("edit")

        result = self._fetch(
            code_mapping=HostHTTPCodes.move,
            endpoint=self._build_move_endpoint(),
            data=tmp,
            method="POST",
        )

        result._replace(msg=result.msg + ". Moved to: %s" % tmp.get("target_folder"))

        if self.module.check_mode:
            return self._check_output("edit")

        if data.get("update_attributes") == {}:
            data.pop("update_attributes")

        if data.get("remove_attributes") == []:
            data.pop("remove_attributes")

        if data.get("update_attributes") and data.get("remove_attributes"):
            tmp = data.copy()
            tmp.pop("remove_attributes")
            self.module.fail_json(json.dumps(tmp))
            result = self._fetch(
                code_mapping=HostHTTPCodes.edit,
                endpoint=self._build_default_endpoint(),
                data=tmp,
                method="PUT",
            )

            tmp = data.copy()
            tmp.pop("update_attributes")
            result = self._fetch(
                code_mapping=HostHTTPCodes.edit,
                endpoint=self._build_default_endpoint(),
                data=tmp,
                method="PUT",
            )
        else:
            data["update_method"] = data.pop("update_attributes")

            result = self._fetch(
                code_mapping=HostHTTPCodes.edit,
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
            code_mapping=HostHTTPCodes.delete,
            endpoint=self._build_default_endpoint(),
            method="DELETE",
        )

        return result


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
        ),
        attributes=dict(type="raw", required=False),
        remove_attributes=dict(type="raw", required=False),
        update_attributes=dict(type="raw", required=False),
        folder=dict(type="str", required=False),
        state=dict(type="str", default="present", choices=["present", "absent"]),
        extended_functionality=dict(type="bool", required=False, default=True),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    # Create an API object that contains the current and desired state
    current_host = HostAPI(module)

    result = RESULT(
        http_code=0,
        msg="No changes needed.",
        content="",
        etag="",
        failed=False,
        changed=False,
    )

    desired_state = current_host.params.get("state")
    if current_host.state == "present":
        result = result._replace(msg="Host already exists with the desired parameters.")
        if desired_state == "absent":
            result = current_host.delete()
        elif current_host.needs_update():
            result = current_host.edit()
    elif current_host.state == "absent":
        result = result._replace(msg="Folder already absent.")
        if desired_state in ("present"):
            result = current_host.create()

    module.exit_json(**result_as_dict(result))


def main():
    run_module()


if __name__ == "__main__":
    main()

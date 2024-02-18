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
version_added: "4.4.0"

description:
    - Manage cluster hosts within Checkmk.

extends_documentation_fragment: [checkmk.general.common]

options:
    name:
        description: The cluster host you want to manage.
        required: true
        type: str
    folder:
        description: The folder your host is located in. On create it defaults to C(/).
        type: str
    nodes:
        description: Nodes, members of the cluster-container host provided in name.
        required: true
        type: list
        elements: str
    attributes:
        description:
            - The attributes of your host as described in the API documentation.
              B(Attention! This option OVERWRITES all existing attributes!)
              If you are using custom tags, make sure to prepend the attribute with C(tag_).
        type: raw
        required: false
    state:
        description: The state of your host.
        type: str
        default: present
        choices: [present, absent]

author:
    - Robin Gierse (@robin-checkmk)
    - Lars Getwan (@lgetwan)
    - Michael Sekania (@msekania)
"""

EXAMPLES = r"""
# Create a host.
- name: "Create a cluste host."
  checkmk.general.cluster:
    server_url: "http://my_server/"
    site: "my_site"
    automation_user: "my_user"
    automation_secret: "my_secret"
    name: "my_cluster_host"
    folder: "/"
    nodes: ["cluster_node_1", "cluster_node_2", "cluster_node_3"]
    state: "present"

# Create a cluster host with IP.
- name: "Create a cluster host with IP address."
  checkmk.general.cluster:
    server_url: "http://my_server/"
    site: "my_site"
    automation_user: "my_user"
    automation_secret: "my_secret"
    name: "my_cluster_host"
    attributes:
      alias: "My Cluster Host"
      ipaddress: "127.0.0.1"
    folder: "/"
    state: "present"

# Create a cluster host which is monitored on a distinct site.
- name: "Create a cluster host which is monitored on a distinct site."
  checkmk.general.cluster:
    server_url: "http://my_server/"
    site: "my_site"
    automation_user: "my_user"
    automation_secret: "my_secret"
    name: "my_host"
    nodes: ["cluster_node_1", "cluster_node_2", "cluster_node_3"]
    attributes:
      site: "my_remote_site"
    folder: "/"
    state: "present"

# Create a host with update_attributes.
- name: "Create a host which is monitored on a distinct site."
  checkmk.general.cluster:
    server_url: "http://my_server/"
    site: "my_site"
    automation_user: "my_user"
    automation_secret: "my_secret"
    name: "my_host"
    nodes:
      - "cluster_node_1"
      - "cluster_node_2"
      - "cluster_node_3"
    update_attributes:
      site: "my_remote_site"
    state: "present"

# Update only specified attributes
- name: "Update only specified attributes, Use host module instead!"
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
- name: "Remove specified attributes, Use host module instead!"
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
- name: "Remove specified attributes, Use host module instead!"
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
    sample: 'Cluster host created.'
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

CLUSTER = (
    "attributes",
#    "update_attributes",
#    "remove_attributes",
)

CLUSTER_PARENTS_PARSE = (
    "attributes",
#    "update_attributes",
)


class ClusterHostHTTPCodes:
    # http_code: (changed, failed, "Message")
    get = {
        200: (False, False, "Cluster host found, nothing changed"),
        404: (False, False, "Cluster host not found"),
    }

    create = {200: (True, False, "Cluster host created")}
    edit = {200: (True, False, "Cluster host edited")}
    modify = {200: (True, False, "Cluster host nodes modified")}
    delete = {204: (True, False, "Cluster host deleted")}


class ClusterHostEndpoints:
    default = "/objects/host_config/"
    create = "/domain-types/host_config/collections/clusters"
    modify = "/objects/host_config/%s/properties/nodes"


class ClusterHostAPI(CheckmkAPI):
    def __init__(self, module):
        super().__init__(module)

        if self.params.get("folder"):
            self.params["folder"] = self._normalize_folder(self.params.get("folder"))

        self.desired = {}

        self.desired["host_name"] = self.params.get("name")
        self.desired["nodes"] = self.params.get("nodes")

        for key in CLUSTER:
            if self.params.get(key):
                self.desired[key] = self.params.get(key)

        for key in CLUSTER_PARENTS_PARSE:
            if self.desired.get(key):
                if self.desired.get(key).get("parents"):
                    self.desired[key]["parents"] = check_type_list(
                        self.desired.get(key).get("parents")
                    )

        # Get the current host from the API and set some parameters
        self._get_current()

        if self.state == "present":
            if (
                self.params.get("folder")
                and self.current["folder"] != self.params["folder"]
            ):
                self.desired["folder"] = self.params["folder"]

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
        if folder in ["", " ", "/", "//", "~"]:
            return "/"

        if not folder.startswith("/"):
            folder = "/%s" % folder

        if folder.endswith("/"):
            folder = folder.rstrip("/")

        return folder

    def _build_default_endpoint(self):
        return "%s/%s" % (
            ClusterHostEndpoints.default,
            self.desired["host_name"],
        )

    def _build_modify_endpoint(self):
        return ClusterHostEndpoints.modify % self.desired["host_name"]

    def _detect_changes(self):
        current_attributes = self.current.copy()
        desired_attributes = self.desired.copy()
        changes = []

        if desired_attributes.get(
            "attributes"
        ) and current_attributes.get("attributes", {}) != desired_attributes.get("attributes"):
            changes.append(
                "attributes: %s" % json.dumps(desired_attributes.get("attributes"))
            )

        if (
            desired_attributes.get("folder")
            and current_attributes.get("folder")
            and current_attributes.get("folder") != desired_attributes.get("folder")
        ):
            changes.append("folder")


        if desired_attributes.get("nodes") != current_attributes.get("nodes"):
            changes.append("nodes")

        return changes

    def _get_current(self):
        result = self._fetch(
            code_mapping=ClusterHostHTTPCodes.get,
            endpoint=self._build_default_endpoint() + "?effective_attributes=true",
            method="GET",
        )

        if result.http_code == 200:
            self.state = "present"

            content = json.loads(result.content)

            extensions = content["extensions"]
            for key, value in extensions.items():
                if key == "attributes":
                    value.pop("meta_data")
                    if "network_scan_results" in value:
                        value.pop("network_scan_results")
                self.current[key] = value
            self.current["folder"] = self._normalize_folder(
                self.current.get("folder", "/")
            )

            self.etag = result.etag

        else:
            self.state = "absent"

    def _check_output(self, mode):
        return RESULT(
            http_code=0,
            msg="Running in check mode. Would have done an %s. Changed: %s"
            % (mode, ", ".join(self._changed_items)),
            content="",
            etag="",
            failed=False,
            changed=False,
        )

    def needs_update(self):
        return len(self._changed_items) > 0

    def create(self):
        data = self.desired.copy()
        if data.get("attributes", {}) == {}:
            data["attributes"] = data.pop("update_attributes", {})

        if data.get("remove_attributes"):
            data.pop("remove_attributes")

        if not data.get("folder"):
            data["folder"] = self._normalize_folder("/")

        if self.module.check_mode:
            return self._check_output("create")

        result = self._fetch(
            code_mapping=ClusterHostHTTPCodes.create,
            endpoint=ClusterHostEndpoints.create,
            data=data,
            method="POST",
        )

        return result

    def edit(self):
        data = self.desired.copy()
        data.pop("host_name")

        self.headers["if-Match"] = self.etag

        if self.module.check_mode:
            return self._check_output("edit")

        result_move = {}
        if data.get("folder"):
            tmp = {}
            tmp["target_folder"] = data.pop("folder")

            result_move = self._fetch(
                code_mapping=ClusterHostHTTPCodes.move,
                endpoint=self._build_move_endpoint(),
                data=tmp,
                method="POST",
            )

            result_move = result_move._replace(
                msg=result_move.msg + ". Moved from to: %s" % tmp.get("target_folder")
            )

        result_nodes = {}
        if data.get("folder"):
            tmp = {}
            tmp["host_name"] = data.get("host_name")
            tmp["nodes"] = data.pop("nodes")

            result_nodes = self._fetch(
                code_mapping=ClusterHostHTTPCodes.modify,
                endpoint=self._build_modify_endpoint(),
                data=tmp,
                method="PUT",
            )

            result_nodes = result_nodes._replace(
                msg=result_nodes.msg + ". Nodes modified to: %s" % tmp.get("target_folder")
            )

        result = self._fetch(
            code_mapping=ClusterHostHTTPCodes.edit,
            endpoint=self._build_default_endpoint(),
            data=data,
            method="PUT",
        )

        return result._replace(
            msg=((result_move.msg + ". ") if result_move != {} else "")
            + ((result_nodes.msg + ". ") if result_nodes != {} else "")
            + result.msg
            + ". Changed: %s" % ", ".join(self._changed_items)
        )

    def delete(self):
        if self.module.check_mode:
            return self._check_output("delete")

        result = self._fetch(
            code_mapping=ClusterHostHTTPCodes.delete,
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
        nodes=dict(type=list, required=True, elements="str"),
        attributes=dict(type="raw", required=False),
        folder=dict(type="str", required=False),
        state=dict(type="str", default="present", choices=["present", "absent"]),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    # Create an API object that contains the current and desired state
    current_cluster = ClusterHostAPI(module)

    result = RESULT(
        http_code=0,
        msg="No changes needed.",
        content="",
        etag="",
        failed=False,
        changed=False,
    )

    desired_state = current_cluster.params.get("state")
    if current_cluster.state == "present":
        result = result._replace(msg="Cluster host already exists with the desired parameters.")
        if desired_state == "absent":
            result = current_cluster.delete()
        elif current_cluster.needs_update():
            result = current_cluster.edit()
    elif current_cluster.state == "absent":
        result = result._replace(msg="Cluster host already absent.")
        if desired_state in ("present"):
            result = current_cluster.create()

    module.exit_json(**result_as_dict(result))


def main():
    run_module()


if __name__ == "__main__":
    main()

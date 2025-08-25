#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2025, Robin Gierse <robin.gierse@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: dcd
short_description: Manage Dynamic Host Management.
version_added: "6.1.0"
description:
  - Manage Dynamic Host Management (DCD), including creation, updating, and deletion.
extends_documentation_fragment: [checkmk.general.common]
options:
    dcd_config:
        description: Configuration parameters for the DCD.
        type: dict
        required: true
        suboptions:
            dcd_id:
                description: Identifier for the DCD configuration.
                type: str
                required: true
            title:
                description: Title of the DCD.
                type: str
                required: false
            comment:
                description: Description or comment for the DCD.
                type: str
                default: ""
            site:
                description: Name of the Checkmk site for the DCD configuration.
                type: str
                required: false
            connector:
                description: DCD Connector configuration.
                type: dict
                required: false
                suboptions:
                    connector_type:
                        description: Type of connector (e.g., "piggyback").
                        type: str
                        default: piggyback
                    interval:
                        description: Interval in seconds for DCD polling.
                        type: int
                        default: 60
                    creation_rules:
                        description: Rules for creating hosts.
                        type: list
                        elements: dict
                        suboptions:
                            folder_path:
                                description: Folder path for host creation.
                                type: str
                                required: true
                            delete_hosts:
                                description: Whether to delete hosts that no longer match.
                                type: bool
                                default: false
                            host_attributes:
                                description: Additional host attributes to set on created hosts.
                                type: dict
                    discover_on_creation:
                        description: Discover services on host creation.
                        type: bool
                        default: true
                    restrict_source_hosts:
                        description: List of source hosts to restrict the DCD to.
                        type: list
                        elements: str
                    no_deletion_time_after_init:
                        description: Seconds to prevent host deletion after site startup, e.g. when booting the Checkmk server.
                        type: int
                        default: 600
                    max_cache_age:
                        description: Seconds to keep hosts when piggyback source only sends piggyback data for other hosts.
                        type: int
                        default: 3600
                    validity_period:
                        description: Seconds to continue consider outdated piggyback data as valid.
                        type: int
                        default: 60
    state:
        description: Desired state of the DCD.
        type: str
        choices:
        - present
        - absent
        default: present
author:
  - Lars Getwan (@lgetwan)
"""

EXAMPLES = r"""
- name: Create a DCD configuration
  checkmk.general.dcd:
    server_url: "http://myserver/"
    site: "mysite"
    automation_auth_type: "bearer"
    automation_user: "myuser"
    automation_secret: "mysecret"
    dcd_config:
      dcd_id: "PiggybackCluster1"
      title: "Piggyback Configuration for Cluster1"
      comment: "Piggyback config for Cluster1 host"
      site: "mysite"
      connector_type: "piggyback"
      interval: 5
      creation_rules:
        - folder_path: "/cluster1"
          delete_hosts: false
          host_attributes:
            tag_address_family: "no-ip"
            tag_agent: "special-agents"
            tag_piggyback: "piggyback"
            tag_snmp_ds: "no-snmp"
      discover_on_creation: true
      restrict_source_hosts:
        - "cluster1"
    state: "present"
- name: Delete a DCD configuration
  checkmk.general.dcd:
    server_url: "http://myserver/"
    site: "mysite"
    automation_auth_type: "bearer"
    automation_user: "myuser"
    automation_secret: "mysecret"
    dcd_config:
      dcd_id: "PiggybackCluster1"
      site: "mysite"
    state: "absent"
"""

RETURN = r"""
msg:
  description:
    - The output message that the module generates.
  type: str
  returned: always
http_code:
  description:
    - HTTP code returned by the Checkmk API.
  type: int
  returned: always
content:
  description:
    - Content of the DCD object.
  returned: when state is present and DCD created or updated.
  type: dict
diff:
  description:
    - The diff between the current and desired state.
  type: dict
  returned: when differences are detected or in diff mode
"""

import json

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.checkmk.general.plugins.module_utils.api import (
    CheckmkAPI,
)
from ansible_collections.checkmk.general.plugins.module_utils.differ import ConfigDiffer
from ansible_collections.checkmk.general.plugins.module_utils.logger import Logger
from ansible_collections.checkmk.general.plugins.module_utils.utils import (
    base_argument_spec,
    exit_module,
)

logger = Logger()


class DCDHTTPCodes:
    """
    DCDHTTPCodes defines the HTTP status codes and corresponding messages
    for DCD operations such as GET, CREATE, EDIT, and DELETE.
    """

    get = {
        200: (False, False, "DCD configuration found, nothing changed"),
        404: (False, False, "DCD configuration not found"),
    }
    create = {
        200: (True, False, "DCD configuration created"),
        201: (True, False, "DCD configuration created"),
        204: (True, False, "DCD configuration created"),
        405: (False, True, "Method Not Allowed"),
    }
    edit = {
        200: (True, False, "DCD configuration modified"),
        405: (False, True, "Method Not Allowed"),
    }
    delete = {
        204: (True, False, "DCD configuration deleted"),
        405: (False, True, "Method Not Allowed"),
    }


class DCDAPI(CheckmkAPI):
    """
    Manages DCD operations via the Checkmk API.
    """

    def __init__(self, module):
        """
        Initializes the DCDAPI class, retrieves the current state of the DCD configuration.
        Args:
            module (AnsibleModule): The Ansible module object.
        """
        super().__init__(module)
        dcd_config = self.params.get("dcd_config")
        if not dcd_config or "dcd_id" not in dcd_config:
            exit_module(
                self.module,
                msg="Missing 'dcd_id' in dcd_config dictionary",
                failed=True,
                logger=logger,
            )

        self.dcd_id = dcd_config["dcd_id"]
        self.desired = dcd_config.copy()

        # Ensure 'site' is present in the desired state
        if "site" not in self.desired or self.desired["site"] is None:
            self.desired["site"] = self.params.get("site")
            if self.desired["site"] is None:
                exit_module(
                    self.module,
                    msg="`site` is required in dcd_config.",
                    failed=True,
                    logger=logger,
                )

        # Ensure 'comment' is not null
        if "comment" not in self.desired or self.desired["comment"] is None:
            self.desired["comment"] = ""

        self.state = None

        self._get_current()

        # Initialize the ConfigDiffer with desired and current configurations
        self.differ = ConfigDiffer(self.desired, self.current)

    def _get_current(self):
        """
        Retrieves the current state of the DCD configuration from the Checkmk API.
        """
        endpoint = self._build_endpoint(action="get")
        result = self._fetch(
            code_mapping=DCDHTTPCodes.get,
            endpoint=endpoint,
            logger=logger,
            method="GET",
        )

        if result.http_code == 200:
            self.state = "present"
            try:
                current_raw = json.loads(result.content)
                self.current = current_raw.get("extensions", {})
                self.current["dcd_id"] = current_raw.get("id")

            except json.JSONDecodeError:
                exit_module(
                    self.module,
                    msg="Failed to decode JSON response from API.",
                    content=result.content,
                    failed=True,
                    logger=logger,
                )
        else:
            self.state = "absent"
            self.current = {}

    def _build_endpoint(self, action="get"):
        """
        Builds the API endpoint URL for the DCD configuration.
        Args:
            action (str): The action for which to build the endpoint. Options are 'create', 'get', 'edit', 'delete'.
        Returns:
            str: API endpoint URL.
        """
        if action == "create":
            return "/domain-types/dcd/collections/all"
        elif action in ["get", "edit", "delete"]:
            return "/objects/dcd/%s" % self.dcd_id
        else:
            exit_module(
                self.module,
                msg="Unsupported action '%s' for building endpoint." % action,
                failed=True,
                logger=logger,
            )

    def needs_update(self):
        """
        Determines whether an update to the DCD configuration is needed.
        Returns:
            bool: True if changes are needed, False otherwise.
        """
        return self.differ.needs_update()

    def generate_diff(self, deletion=False):
        """
        Generates a diff between the current and desired state.
        Args:
            deletion (bool): Whether the diff is for a deletion.
        Returns:
            dict: Dictionary containing 'before' and 'after' states.
        """
        return self.differ.generate_diff(deletion)

    def _perform_action(self, action, method, data=None):
        """
        Helper method to perform CRUD actions.
        Args:
            action (str): The action being performed ('create', 'edit', 'delete').
            method (str): The HTTP method.
            data (dict, optional): The data to send with the request.
        Returns:
            dict: The result dictionary.
        """
        endpoint = self._build_endpoint(action=action)

        diff = None
        if self.module._diff:
            deletion_flag = action == "delete"
            diff = self.generate_diff(deletion=deletion_flag)

        if self.module.check_mode:
            action_msgs = {
                "create": "would be created",
                "edit": "would be modified",
                "delete": "would be deleted",
            }
            return dict(
                msg="DCD configuration %s." % action_msgs.get(action, action),
                changed=True,  # Indicate that changes would occur
                diff=diff,
            )

        return self._fetch(
            code_mapping=getattr(DCDHTTPCodes, action),
            endpoint=endpoint,
            data=data,
            logger=logger,
            method=method,
        )

    def create(self):
        """
        Creates a new DCD configuration via the Checkmk API.
        Returns:
            dict: The result of the creation operation.
        """
        filtered_data = {k: v for k, v in self.desired.items() if v is not None}
        return self._perform_action(action="create", method="POST", data=filtered_data)

    def edit(self):
        """
        Updates an existing DCD configuration via the Checkmk API.
        Returns:
            dict: The result of the update operation.
        """
        filtered_data = {k: v for k, v in self.desired.items() if v is not None}
        return self._perform_action(action="edit", method="PUT", data=filtered_data)

    def delete(self):
        """
        Deletes an existing DCD configuration via the Checkmk API.
        Returns:
            dict: The result of the deletion operation.
        """
        return self._perform_action(action="delete", method="DELETE")


def run_module():
    """
    The main logic for the Ansible module.
    This function defines the module parameters, initializes the DCDAPI, and performs
    the appropriate action (create or delete) based on the state of the DCD configuration.
    Note: Update functionality is currently disabled due to the lack of a REST API endpoint for updates.
    Returns:
        None: The result is returned to Ansible via module.exit_json().
    """

    argument_spec = base_argument_spec()
    argument_spec.update(
        server_url=dict(type="str", required=True),
        site=dict(type="str", required=True),
        dcd_config=dict(
            type="dict",
            required=True,
            options={
                "dcd_id": dict(type="str", required=True),
                "title": dict(type="str", required=False),
                "comment": dict(type="str", default=""),
                "site": dict(type="str", required=False),
                "connector": dict(
                    type="dict",
                    options={
                        "connector_type": dict(type="str", default="piggyback"),
                        "interval": dict(type="int", default=60),
                        "creation_rules": dict(
                            type="list",
                            elements="dict",
                            options={
                                "folder_path": dict(type="str", required=True),
                                "delete_hosts": dict(type="bool", default=False),
                                "host_attributes": dict(type="dict", required=False),
                            },
                        ),
                        "discover_on_creation": dict(type="bool", default=True),
                        "restrict_source_hosts": dict(
                            type="list", elements="str", required=False
                        ),
                        "no_deletion_time_after_init": dict(
                            type="int", required=False, default=600
                        ),
                        "max_cache_age": dict(type="int", required=False, default=3600),
                        "validity_period": dict(type="int", required=False, default=60),
                    },
                ),
            },
        ),
        state=dict(type="str", default="present", choices=["present", "absent"]),
    )

    required_if = [
        ("api_auth_type", "bearer", ["automation_user", "automation_secret"]),
        ("api_auth_type", "basic", ["automation_user", "automation_secret"]),
        ("api_auth_type", "cookie", ["api_auth_cookie"]),
    ]

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=required_if,
    )

    logger.set_loglevel(module._verbosity)
    logger.set_loglevel(2)

    desired_state = module.params["state"]
    dcd_api = DCDAPI(module)

    try:
        if desired_state == "present":
            if dcd_api.state == "absent":
                result = dcd_api.create()
            elif dcd_api.needs_update():
                exit_module(
                    module,
                    msg="DCD object cannot be updated. No REST API endpoint available for updates. Diff: %s"
                    % str(dcd_api.generate_diff()),
                    failed=True,
                    logger=logger,
                )

            else:
                exit_module(
                    module,
                    msg="DCD configuration is already in the desired state.",
                    logger=logger,
                )

        elif desired_state == "absent":
            if dcd_api.state == "present":
                result = dcd_api.delete()
            else:
                exit_module(
                    module,
                    msg="DCD configuration is already absent.",
                    logger=logger,
                )

    except Exception as e:
        exit_module(
            module, msg="Error managing the DCD configuration: %s" % e, logger=logger
        )


def main():
    """
    Main entry point for the module.
    This function is invoked when the module is executed directly.
    Returns:
        None: Calls run_module() to handle the logic.
    """
    run_module()


if __name__ == "__main__":
    main()

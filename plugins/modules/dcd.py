#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2025, Robin Gierse <robin.gierse@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: dcd

short_description: Manage Dynamic Configuration Definitions in Checkmk.

version_added: "6.1.0"

description:
  - Manage Dynamic Configuration Definitions (DCD) in Checkmk, including creation, updating, and deletion.

extends_documentation_fragment: [checkmk.general.common]

options:

  dcd_config:
    description:
      - Configuration parameters for the DCD.
    type: dict
    required: true
    options:
      dcd_id:
        description:
          - Identifier for the DCD configuration.
        type: str
        required: true
      title:
        description:
          - Title of the DCD.
        type: str
        required: false
      comment:
        description:
          - Description or comment for the DCD.
        type: str
        default: ""
      site:
        description:
          - Name of the Checkmk site for the DCD configuration.
        type: str
        required: true
      connector_type:
        description:
          - Type of connector (e.g., "piggyback").
        type: str
        default: piggyback
      interval:
        description:
          - Interval in seconds for DCD polling.
        type: int
        default: 60
      creation_rules:
        description:
          - Rules for creating hosts.
        type: list
        elements: dict
        options:
          folder_path:
            description:
              - Folder path for host creation.
            type: str
            required: true
          delete_hosts:
            description:
              - Whether to delete hosts that no longer match.
            type: bool
            default: false
          host_attributes:
            description:
              - Additional host attributes to set on created hosts.
            type: dict
      discover_on_creation:
        description:
          - Discover services on host creation.
        type: bool
        default: true
      restrict_source_hosts:
        description:
          - List of source hosts to restrict the DCD to.
        type: list
        elements: str
  state:
    description:
      - Desired state of the DCD.
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
    auth_type: "bearer"
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
    auth_type: "bearer"
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

import base64
import json

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.checkmk.general.plugins.module_utils.api import CheckmkAPI
from ansible_collections.checkmk.general.plugins.module_utils.differ import ConfigDiffer


class ExtendedCheckmkAPI(CheckmkAPI):
    """
    Extends CheckmkAPI to support bearer, basic, and cookie authentication methods.
    """

    def __init__(self, module):
        super().__init__(module)
        auth_type = self.params.get("auth_type", "bearer")
        automation_user = self.params.get("automation_user")
        automation_secret = self.params.get("automation_secret")
        auth_cookie = self.params.get("auth_cookie")

        if auth_type == "bearer":
            if not automation_user or not automation_secret:
                self.module.fail_json(
                    msg="`automation_user` and `automation_secret` are required for bearer authentication."
                )
            self.headers["Authorization"] = (
                f"Bearer {automation_user} {automation_secret}"
            )

        elif auth_type == "basic":
            if not automation_user or not automation_secret:
                self.module.fail_json(
                    msg="`automation_user` and `automation_secret` are required for basic authentication."
                )
            auth_b64 = base64.b64encode(
                f"{automation_user}:{automation_secret}".encode()
            ).decode()
            self.headers["Authorization"] = f"Basic {auth_b64}"

        elif auth_type == "cookie":
            if not auth_cookie:
                self.module.fail_json(
                    msg="`auth_cookie` is required for cookie authentication."
                )
            self.cookies["auth_cmk"] = auth_cookie

        else:
            self.module.fail_json(msg=f"Unsupported `auth_type`: {auth_type}")


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


class DCDAPI(ExtendedCheckmkAPI):
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
            self.module.fail_json(msg="Missing 'dcd_id' in dcd_config dictionary")

        self.dcd_id = dcd_config["dcd_id"]
        self.desired = dcd_config.copy()

        # Ensure 'site' is present in the desired state
        if "site" not in self.desired or self.desired["site"] is None:
            self.desired["site"] = self.params.get("site")
            if self.desired["site"] is None:
                self.module.fail_json(msg="`site` is required in dcd_config.")

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
            method="GET",
        )

        if result.http_code == 200:
            self.state = "present"
            try:
                current_raw = json.loads(result.content)
                extensions = current_raw.get("extensions", {})
                self.current = {}

                # Mapping fields
                self.current["dcd_id"] = current_raw.get("id")
                self.current["title"] = extensions.get("title")
                self.current["comment"] = extensions.get("comment")
                self.current["documentation_url"] = extensions.get("docu_url")
                self.current["disabled"] = extensions.get("disabled")
                self.current["site"] = extensions.get("site")

                # Connector and its settings
                connector = extensions.get("connector", [])
                if isinstance(connector, list) and len(connector) == 2:
                    self.current["connector_type"] = connector[0]
                    connector_settings = connector[1]

                    # Mapping connector settings
                    self.current["interval"] = connector_settings.get("interval")
                    self.current["discover_on_creation"] = connector_settings.get(
                        "discover_on_creation"
                    )
                    self.current["no_deletion_time_after_init"] = (
                        connector_settings.get("no_deletion_time_after_init")
                    )
                    self.current["max_cache_age"] = connector_settings.get(
                        "max_cache_age"
                    )
                    self.current["validity_period"] = connector_settings.get(
                        "validity_period"
                    )
                    self.current["restrict_source_hosts"] = connector_settings.get(
                        "source_filters", []
                    )
                    self.current["activate_changes_interval"] = connector_settings.get(
                        "activate_changes_interval"
                    )

                    # Mapping 'activation_exclude_times' to 'exclude_time_ranges'
                    activation_exclude_times = connector_settings.get(
                        "activation_exclude_times", []
                    )
                    self.current["exclude_time_ranges"] = []
                    for time_range in activation_exclude_times:
                        start_time = time_range[0]
                        end_time = time_range[1]
                        self.current["exclude_time_ranges"].append(
                            {
                                "start": f"{start_time[0]:02d}:{start_time[1]:02d}",
                                "end": f"{end_time[0]:02d}:{end_time[1]:02d}",
                            }
                        )

                    # Mapping 'creation_rules'
                    self.current["creation_rules"] = []
                    for rule in connector_settings.get("creation_rules", []):
                        # Transform 'create_folder_path' to 'folder_path' and add leading slash
                        folder_path = rule.get("create_folder_path", "")
                        if not folder_path.startswith("/"):
                            folder_path = "/" + folder_path

                        # Transform 'host_attributes' from list of lists to dictionary
                        host_attributes_list = rule.get("host_attributes", [])
                        host_attributes_dict = {}
                        for attr_pair in host_attributes_list:
                            if isinstance(attr_pair, list) and len(attr_pair) == 2:
                                host_attributes_dict[attr_pair[0]] = attr_pair[1]
                            else:
                                self.module.fail_json(
                                    msg="Unexpected structure in 'host_attributes'."
                                )

                        mapped_rule = {
                            "folder_path": folder_path,
                            "delete_hosts": rule.get("delete_hosts"),
                            "host_attributes": host_attributes_dict,
                        }
                        self.current["creation_rules"].append(mapped_rule)
                else:
                    self.module.fail_json(
                        msg="Unexpected structure in 'connector' field."
                    )
            except json.JSONDecodeError:
                self.module.fail_json(
                    msg="Failed to decode JSON response from API.",
                    content=result.content,
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
            return f"/objects/dcd/{self.dcd_id}"
        else:
            self.module.fail_json(
                msg=f"Unsupported action '{action}' for building endpoint."
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
                msg=f"DCD configuration {action_msgs.get(action, action)}.",
                changed=True,  # Indicate that changes would occur
                diff=diff,
            )

        response = self._fetch(
            code_mapping=getattr(DCDHTTPCodes, action),
            endpoint=endpoint,
            data=data,
            method=method,
        )

        if response.failed:
            if response.http_code == 405:
                self.module.fail_json(
                    msg=f"Method Not Allowed: Unable to {action} the DCD configuration.",
                    content=response.content,
                )
            else:
                self.module.fail_json(msg=response.msg, content=response.content)

        result_dict = {
            "changed": response.changed,
            "msg": response.msg,
            "http_code": response.http_code,
            "content": json.loads(response.content) if response.content else {},
        }

        if diff:
            result_dict["diff"] = diff

        return result_dict

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
    module_args = dict(
        server_url=dict(type="str", required=True),
        site=dict(type="str", required=True),
        auth_type=dict(
            type="str", choices=["bearer", "basic", "cookie"], default="bearer"
        ),
        automation_user=dict(type="str"),
        automation_secret=dict(type="str", no_log=True),
        auth_cookie=dict(type="str", no_log=True),
        dcd_config=dict(
            type="dict",
            required=True,
            options={
                "dcd_id": dict(type="str", required=True),
                "title": dict(type="str", required=False),
                "comment": dict(type="str", default=""),
                "site": dict(type="str", required=False),
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
                "exclude_time_ranges": dict(type="list", required=False),
                "discover_on_creation": dict(type="bool", default=True),
                "restrict_source_hosts": dict(type="list", elements="str"),
                "no_deletion_time_after_init": dict(type="int", required=False),
                "max_cache_age": dict(type="int", required=False),
                "validity_period": dict(type="int", required=False),
            },
        ),
        state=dict(type="str", default="present", choices=["present", "absent"]),
        validate_certs=dict(type="bool", default=True),
    )

    required_if = [
        ("auth_type", "bearer", ["automation_user", "automation_secret"]),
        ("auth_type", "basic", ["automation_user", "automation_secret"]),
        ("auth_type", "cookie", ["auth_cookie"]),
    ]

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_if=required_if,
    )

    desired_state = module.params["state"]
    dcd_api = DCDAPI(module)

    try:
        if desired_state == "present":
            if dcd_api.state == "absent":
                result = dcd_api.create()
            elif dcd_api.needs_update():
                result = dict(
                    changed=False,
                    msg="DCD object cannot be updated. No REST API endpoint available for updates.",
                    diff=dcd_api.generate_diff(),
                )
            else:
                result = dict(
                    changed=False,
                    msg="DCD configuration is already in the desired state.",
                )
        elif desired_state == "absent":
            if dcd_api.state == "present":
                result = dcd_api.delete()
            else:
                result = dict(
                    changed=False,
                    msg="DCD configuration is already absent.",
                )
    except Exception as e:
        module.fail_json(msg=f"Error managing the DCD configuration: {e}")

    module.exit_json(**result)


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

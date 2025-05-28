#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2025, Robin Gierse <robin.gierse@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: bi_rule

short_description: Manage BI rules.

version_added: "6.1.0"

description:
  - Manage BI rules, including creation, updating, and deletion.

extends_documentation_fragment: [checkmk.general.common]

options:
    rule:
        type: dict
        required: true
        description: Definition of the BI rule as needed by the Checkmk API.
        suboptions:
            pack_id:
                type: str
                required: true
                description: The identifier of the BI pack.
            id:
                type: str
                required: true
                description: The unique BI rule ID.
            nodes:
                type: list
                elements: dict
                required: true
                description: List of nodes associated with the BI rule.
            properties:
                type: dict
                required: true
                description: Properties of the BI rule.
            aggregation_function:
                type: dict
                required: true
                description: Aggregation function configuration.
            computation_options:
                type: dict
                required: true
                description: Computation options for the BI rule.
            node_visualization:
                type: dict
                required: true
                description: Visualization options for the BI rule nodes.
            params:
                type: dict
                required: false
                description: Additional parameters for the BI rule.
                suboptions:
                    arguments:
                        type: list
                        elements: str
                        required: false
                        description: List of arguments for the BI rule.

    state:
        type: str
        default: "present"
        choices: ["present", "absent"]
        description: State of the BI rule.

author:
  - Lars Getwan (@lgetwan)
"""

EXAMPLES = r"""
- name: Create a BI rule
  checkmk.general.bi_rule:
    server_url: "https://example.com/"
    site: "mysite"
    automation_auth_type: "bearer"
    automation_user: "myuser"
    automation_secret: "mysecret"
    rule:
      pack_id: "cluster_pack"
      id: "testrule1"
      nodes:
        - search:
            type: "empty"
          action:
            type: "call_a_rule"
            rule_id: "test-child-rule1"
            params:
              arguments: []
      properties:
        title: "Test Rule 1"
        comment: ""
        docu_url: ""
        icon: ""
        state_messages: {}
      aggregation_function:
        type: "best"
        count: 1
        restrict_state: 2
      computation_options:
        disabled: false
      node_visualization:
        type: "block"
        style_config: {}
    state: "present"

- name: Delete a BI rule
  checkmk.general.bi_rule:
    server_url: "https://example.com/"
    site: "mysite"
    automation_auth_type: "bearer"
    automation_user: "myuser"
    automation_secret: "mysecret"
    rule:
      pack_id: "cluster_pack"
      id: "testrule1"
    state: "absent"
"""

RETURN = r"""
msg:
  description:
    - The output message that the module generates. Contains the API status details in case of an error.
  type: str
  returned: always
  sample: 'BI rule created.'

http_code:
  description:
    - The HTTP code the Checkmk API returns.
  type: int
  returned: always
  sample: 200

content:
  description:
    - The complete created/changed BI rule.
  returned: when the BI rule is created or updated.
  type: dict
"""

import base64
import json

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.checkmk.general.plugins.module_utils.api import CheckmkAPI
from ansible_collections.checkmk.general.plugins.module_utils.differ import ConfigDiffer
from ansible_collections.checkmk.general.plugins.module_utils.utils import (
    base_argument_spec,
)


class ExtendedCheckmkAPI(CheckmkAPI):
    """
    Extends CheckmkAPI to support 'basic' and 'cookie' authentication methods.
    Ensures that Bearer authentication uses both 'automation_user' and 'automation_secret'.
    """

    def __init__(self, module):
        """Initialize ExtendedCheckmkAPI with authentication handling."""
        super().__init__(module)
        automation_auth_type = self.params.get("automation_auth_type", "bearer")
        automation_user = self.params.get("automation_user")
        automation_secret = self.params.get("automation_secret")
        automation_auth_cookie = self.params.get("automation_auth_cookie")

        if automation_auth_type == "bearer":
            if not automation_user or not automation_secret:
                self.module.fail_json(
                    msg="`automation_user` and `automation_secret` are required for bearer authentication."
                )
            self.headers["Authorization"] = (
                f"Bearer {automation_user} {automation_secret}"
            )
        elif automation_auth_type == "basic":
            if not automation_user or not automation_secret:
                self.module.fail_json(
                    msg="`automation_user` and `automation_secret` are required for basic authentication."
                )
            auth_str = f"{automation_user}:{automation_secret}"
            auth_b64 = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")
            self.headers["Authorization"] = f"Basic {auth_b64}"
        elif automation_auth_type == "cookie":
            if not automation_auth_cookie:
                self.module.fail_json(
                    msg="`automation_auth_cookie` is required for cookie authentication."
                )
            self.cookies["auth_cmk"] = automation_auth_cookie
        else:
            self.module.fail_json(
                msg=f"Unsupported `automation_auth_type`: {automation_auth_type}"
            )


class BIRuleHTTPCodes:
    """
    BIRuleHTTPCodes defines the HTTP status codes and corresponding messages
    for BI rule operations such as GET, CREATE, EDIT, and DELETE.
    """

    get = {
        200: (False, False, "BI rule found, nothing changed"),
        404: (False, False, "BI rule not found"),
    }
    create = {
        200: (True, False, "BI rule created"),
        201: (True, False, "BI rule created"),
        204: (True, False, "BI rule created"),
    }
    edit = {
        200: (True, False, "BI rule modified"),
    }
    delete = {
        204: (True, False, "BI rule deleted"),
    }


class BIRuleAPI(ExtendedCheckmkAPI):
    """
    Manages BI rule operations via the Checkmk API.
    """

    def __init__(self, module):
        """Initialize BIRuleAPI with module parameters.

        Args:
            module (AnsibleModule): The Ansible module object.
        """
        super().__init__(module)
        rule = self.params.get("rule")
        if not rule or "id" not in rule or "pack_id" not in rule:
            self.module.fail_json(msg="Missing 'id' or 'pack_id' in rule dictionary")

        self.rule_id = rule["id"]
        self.pack_id = rule["pack_id"]
        self.desired = rule.copy()

        self.state = None
        self._get_current()

        # Initialize the ConfigDiffer with desired and current configurations
        self.differ = ConfigDiffer(self.desired, self.current)

    def _get_current(self):
        """
        Retrieves the current state of the BI rule from the Checkmk API.
        """
        endpoint = self._build_endpoint(action="get")
        result = self._fetch(
            code_mapping=BIRuleHTTPCodes.get,
            endpoint=endpoint,
            method="GET",
        )

        if result.http_code == 200:
            self.state = "present"
            try:
                self.current = json.loads(result.content)
            except json.JSONDecodeError:
                self.module.fail_json(
                    msg="Failed to decode JSON response from API.",
                    content=result.content,
                )
        else:
            self.state = "absent"
            self.current = {}

    def _build_endpoint(self, action):
        """
        Builds the API endpoint URL for the BI rule.

        Args:
            action (str): The action being performed ('get', 'create', 'edit', 'delete').

        Returns:
            str: API endpoint URL.
        """
        supported_actions = ["get", "create", "edit", "delete"]
        if action in supported_actions:
            return f"/objects/bi_rule/{self.rule_id}"
        else:
            self.module.fail_json(
                msg=f"Unsupported action '{action}' for building endpoint."
            )

    def needs_update(self):
        """
        Determines whether an update to the BI rule is needed.

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
            action_msgs = {"create": "created", "edit": "modified", "delete": "deleted"}
            return dict(
                msg=f"BI rule would be {action_msgs.get(action, action)}.",
                changed=True,
                diff=diff,
            )

        response = self._fetch(
            code_mapping=getattr(BIRuleHTTPCodes, action),
            endpoint=endpoint,
            data=data,
            method=method,
        )

        if response.failed:
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
        Creates a new BI rule via the Checkmk API.

        Returns:
            dict: The result of the creation operation.
        """
        return self._perform_action(action="create", method="POST", data=self.desired)

    def edit(self):
        """
        Updates an existing BI rule via the Checkmk API.

        Returns:
            dict: The result of the update operation.
        """
        return self._perform_action(action="edit", method="PUT", data=self.desired)

    def delete(self):
        """
        Deletes an existing BI rule via the Checkmk API.

        Returns:
            dict: The result of the deletion operation.
        """
        return self._perform_action(action="delete", method="DELETE")


def run_module():
    """
    The main logic for the Ansible module.

    This function defines the module parameters, initializes the BIRuleAPI, and performs
    the appropriate action (create, edit, delete) based on the state of the BI rule.

    Returns:
        None: The result is returned to Ansible via module.exit_json().
    """
    argument_spec = base_argument_spec()
    argument_spec.update(
        rule=dict(
            type="dict",
            required=True,
            options=dict(
                pack_id=dict(
                    type="str",
                    required=True,
                ),
                id=dict(
                    type="str",
                    required=True,
                ),
                nodes=dict(
                    type="list",
                    elements="dict",
                    required=True,
                ),
                properties=dict(
                    type="dict",
                    required=True,
                ),
                aggregation_function=dict(
                    type="dict",
                    required=True,
                ),
                computation_options=dict(
                    type="dict",
                    required=True,
                ),
                node_visualization=dict(
                    type="dict",
                    required=True,
                ),
                params=dict(
                    type="dict",
                    required=False,
                    options=dict(
                        arguments=dict(
                            type="list",
                            elements="str",
                            required=False,
                        ),
                    ),
                ),
            ),
        ),
        state=dict(
            type="str",
            default="present",
            choices=["present", "absent"],
        ),
    )

    required_if = [
        ("automation_auth_type", "bearer", ["automation_user", "automation_secret"]),
        ("automation_auth_type", "basic", ["automation_user", "automation_secret"]),
        ("automation_auth_type", "cookie", ["automation_auth_cookie"]),
    ]

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=required_if,
    )

    desired_state = module.params.get("state")
    rule = module.params.get("rule")

    # Initialize BIRuleAPI
    bi_rule_api = BIRuleAPI(module)

    try:
        if desired_state == "present":
            if bi_rule_api.state == "absent":
                result = bi_rule_api.create()
            elif bi_rule_api.needs_update():
                result = bi_rule_api.edit()
            else:
                result = dict(
                    changed=False,
                    msg="BI rule is already in the desired state.",
                )
        elif desired_state == "absent":
            if bi_rule_api.state == "present":
                result = bi_rule_api.delete()
            else:
                result = dict(
                    changed=False,
                    msg="BI rule is already absent.",
                )
    except Exception as e:
        module.fail_json(msg=f"Error managing the BI rule: {e}")

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

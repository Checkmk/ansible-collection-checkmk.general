#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2025, Robin Gierse <robin.gierse@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: bi_aggregation

short_description: Manage BI aggregations in Checkmk.

version_added: "6.1.0"

description:
    - Manage BI aggregations within Checkmk. This module allows the creation, updating, and deletion of BI aggregations via the Checkmk API.

extends_documentation_fragment: [checkmk.general.common]

options:
    aggregation:
        description:
          - Definition of the BI aggregation as needed by the Checkmk API.
        type: dict
        required: true
        suboptions:
            id:
                description:
                    - The unique aggregation ID.
                type: str
                required: true
            pack_id:
                description:
                    - The identifier of the BI pack.
                type: str
                required: true
            comment:
                description:
                    - An optional comment that may be used to explain the purpose of this aggregation.
                type: str
                required: false
            customer:
                description:
                    - The customer ID for this aggregation (CME Edition only).
                type: str
                required: false
            groups:
                description:
                    - Groups associated with the aggregation.
                type: dict
                required: false
                suboptions:
                    names:
                        description:
                            - List of group names.
                        type: list
                        elements: str
                        required: false
                    paths:
                        description:
                            - List of group paths.
                        type: list
                        elements: list
                        required: false
            node:
                description:
                    - Node generation definition.
                type: dict
                required: true
                suboptions:
                    search:
                        description:
                            - Search criteria.
                        type: dict
                        required: true
                    action:
                        description:
                            - Action on search results.
                        type: dict
                        required: true
            aggregation_visualization:
                description:
                    - Aggregation visualization options.
                type: dict
                required: false
            computation_options:
                description:
                    - Computation options.
                type: dict
                required: false
    state:
        description:
            - State of the BI aggregation.
        choices: [present, absent]
        default: present
        type: str

author:
    - Lars Getwan (@lgetwan)
"""

EXAMPLES = r"""
- name: Create a BI aggregation with state_of_host
  checkmk.general.bi_aggregation:
    server_url: "http://myserver/"
    site: "mysite"
    auth_type: "bearer"
    automation_user: "myuser"
    automation_secret: "mysecret"
    aggregation:
      id: "aggr1"
      pack_id: "pack1"
      comment: "Aggregation comment"
      customer: "customer1"
      groups:
        names: ["groupA", "groupB"]
        paths:
          - ["path", "group", "a"]
          - ["path", "group", "b"]
      node:
        search:
          type: "empty"
        action:
          type: "state_of_host"
          rule_id: "rule123"
          host_regex: ".*"
      aggregation_visualization:
        ignore_rule_styles: false
        layout_id: "builtin_default"
        line_style: "round"
      computation_options:
        disabled: false
        use_hard_states: false
        escalate_downtimes_as_warn: false
        freeze_aggregations: false
    state: "present"

- name: Delete a BI aggregation
  checkmk.general.bi_aggregation:
    server_url: "http://myserver/"
    site: "mysite"
    auth_type: "bearer"
    automation_user: "myuser"
    automation_secret: "mysecret"
    aggregation:
      id: "aggr1"
      pack_id: "pack1"
    state: "absent"
"""

RETURN = r"""
msg:
    description: The output message that the module generates.
    type: str
    returned: always
    sample: 'BI aggregation created.'
http_code:
    description: The HTTP code the Checkmk API returns.
    type: int
    returned: always
    sample: 200
content:
    description: The complete created/changed BI aggregation.
    returned: when the BI aggregation is created or updated.
    type: dict
"""

import base64
import json

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.checkmk.general.plugins.module_utils.api import CheckmkAPI
from ansible_collections.checkmk.general.plugins.module_utils.differ import ConfigDiffer


class ExtendedCheckmkAPI(CheckmkAPI):
    """
    Extends CheckmkAPI to support 'basic' and 'cookie' authentication methods.
    Ensures that Bearer authentication uses both 'automation_user' and 'automation_secret'.
    """

    def __init__(self, module):
        """Initialize ExtendedCheckmkAPI with authentication handling."""
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
            auth_str = f"{automation_user}:{automation_secret}"
            auth_b64 = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")
            self.headers["Authorization"] = f"Basic {auth_b64}"
        elif auth_type == "cookie":
            if not auth_cookie:
                self.module.fail_json(
                    msg="`auth_cookie` is required for cookie authentication."
                )
            self.cookies["auth_cmk"] = auth_cookie
        else:
            self.module.fail_json(msg=f"Unsupported `auth_type`: {auth_type}")


class BIAggregationHTTPCodes:
    """
    Defines HTTP status codes and corresponding actions for BI aggregation operations.
    """

    get = {
        200: (False, False, "BI aggregation found, nothing changed"),
        404: (False, False, "BI aggregation not found"),
    }
    create = {
        200: (True, False, "BI aggregation created"),
        201: (True, False, "BI aggregation created"),
        204: (True, False, "BI aggregation created"),
    }
    edit = {
        200: (True, False, "BI aggregation modified"),
    }
    delete = {
        204: (True, False, "BI aggregation deleted"),
    }


class BIAggregationAPI(ExtendedCheckmkAPI):
    """
    Manages BI aggregation operations via the Checkmk API.
    """

    def __init__(self, module):
        """Initialize BIAggregationAPI with module parameters.

        Args:
            module (AnsibleModule): The Ansible module object.
        """
        super().__init__(module)
        aggregation = self.params.get("aggregation")
        if not aggregation or "id" not in aggregation or "pack_id" not in aggregation:
            self.module.fail_json(
                msg="Missing 'id' or 'pack_id' in aggregation dictionary"
            )

        self.aggregation_id = aggregation["id"]
        self.pack_id = aggregation["pack_id"]
        self.desired = aggregation.copy()

        self.state = None
        self._get_current()

        # Initialize the ConfigDiffer with desired and current configurations
        self.differ = ConfigDiffer(self.desired, self.current)

    def _get_current(self):
        """
        Retrieve the current state of the BI aggregation from the Checkmk API.
        """
        endpoint = self._build_endpoint(action="get")
        result = self._fetch(
            code_mapping=BIAggregationHTTPCodes.get,
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

    def _build_endpoint(self, action="get"):
        """
        Build the API endpoint URL for the BI aggregation.

        Args:
            action (str): The action being performed ('get', 'create', 'edit', 'delete').

        Returns:
            str: API endpoint URL.
        """
        if action in ["get", "create", "edit", "delete"]:
            return f"/objects/bi_aggregation/{self.aggregation_id}"
        else:
            self.module.fail_json(
                msg=f"Unsupported action '{action}' for building endpoint."
            )

    def needs_update(self):
        """
        Determine whether an update to the BI aggregation is needed.

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
                msg=f"BI aggregation would be {action_msgs.get(action, action)}.",
                changed=True,
                diff=diff,
            )

        response = self._fetch(
            code_mapping=getattr(BIAggregationHTTPCodes, action),
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
        Create a new BI aggregation via the Checkmk API.

        Returns:
            dict: The result of the creation operation.
        """
        return self._perform_action(action="create", method="POST", data=self.desired)

    def edit(self):
        """
        Update an existing BI aggregation via the Checkmk API.

        Returns:
            dict: The result of the update operation.
        """
        return self._perform_action(action="edit", method="PUT", data=self.desired)

    def delete(self):
        """
        Delete an existing BI aggregation via the Checkmk API.

        Returns:
            dict: The result of the deletion operation.
        """
        return self._perform_action(action="delete", method="DELETE")


def run_module():
    """
    The main logic for the Ansible module.

    This function defines the module parameters, initializes the BIAggregationAPI, and performs
    the appropriate action (create, edit, delete) based on the state of the BI aggregation.

    Returns:
        None: The result is returned to Ansible via module.exit_json().
    """
    module_args = dict(
        server_url=dict(type="str", required=True),
        site=dict(type="str", required=True),
        auth_type=dict(
            type="str",
            choices=["bearer", "basic", "cookie"],
            default="bearer",
            required=False,
        ),
        automation_user=dict(type="str", required=False),
        automation_secret=dict(type="str", required=False, no_log=True),
        auth_cookie=dict(type="str", required=False, no_log=True),
        aggregation=dict(
            type="dict",
            required=True,
            options=dict(
                id=dict(type="str", required=True),
                pack_id=dict(type="str", required=True),
                comment=dict(type="str", required=False),
                customer=dict(type="str", required=False),
                groups=dict(
                    type="dict",
                    required=False,
                    options=dict(
                        names=dict(type="list", elements="str", required=False),
                        paths=dict(
                            type="list",
                            elements="list",
                            required=False,
                        ),
                    ),
                ),
                node=dict(
                    type="dict",
                    required=False,
                    options=dict(
                        search=dict(type="dict", required=True),
                        action=dict(type="dict", required=True),
                    ),
                ),
                aggregation_visualization=dict(
                    type="dict",
                    required=False,
                ),
                computation_options=dict(
                    type="dict",
                    required=False,
                ),
            ),
        ),
        state=dict(type="str", default="present", choices=["present", "absent"]),
        validate_certs=dict(type="bool", default=True, required=False),
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

    desired_state = module.params.get("state")
    aggregation = module.params.get("aggregation")

    # Initialize BIAggregationAPI
    bi_aggregation_api = BIAggregationAPI(module)

    try:
        if desired_state == "present":
            if bi_aggregation_api.state == "absent":
                result = bi_aggregation_api.create()
            elif bi_aggregation_api.needs_update():
                result = bi_aggregation_api.edit()
            else:
                result = dict(
                    changed=False,
                    msg="BI aggregation is already in the desired state.",
                )
        elif desired_state == "absent":
            if bi_aggregation_api.state == "present":
                result = bi_aggregation_api.delete()
            else:
                result = dict(
                    changed=False,
                    msg="BI aggregation is already absent.",
                )
    except Exception as e:
        module.fail_json(msg=f"Error managing the BI aggregation: {e}")

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

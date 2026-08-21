#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2025, Lars Getwan <lars.getwan@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# This code was originally authored by Atruvia AG (https://atruvia.de/)
# and subsequently modified by Checkmk.
# Thank you so much for donating this code!

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: bi_rule

short_description: Manage BI rules.

version_added: "8.4.0"

description:
  - Manage BI rules, including creation, updating and deletion.

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
                required: false
                description:
                  - List of nodes associated with the BI rule.
                  - Required when I(state=present).
            properties:
                type: dict
                required: false
                description:
                  - Properties of the BI rule.
                  - Required when I(state=present).
            aggregation_function:
                type: dict
                required: false
                description:
                  - Aggregation function configuration.
                  - Required when I(state=present).
            computation_options:
                type: dict
                required: false
                description:
                  - Computation options for the BI rule.
                  - Required when I(state=present).
            node_visualization:
                type: dict
                required: false
                description:
                  - Visualization options for the BI rule nodes.
                  - Required when I(state=present).
            params:
                type: dict
                required: false
                description:
                  - Additional parameters for the BI rule.
                  - The Checkmk API requires this field, so it defaults to an empty argument list.
                default: {"arguments": []}
                suboptions:
                    arguments:
                        type: list
                        elements: str
                        required: false
                        default: []
                        description: List of arguments for the BI rule.

    state:
        type: str
        default: "present"
        choices: ["present", "absent"]
        description: State of the BI rule.

author:
  - Lars Getwan (@lgetwan)

seealso:
    - module: checkmk.general.bi_pack
    - module: checkmk.general.bi_aggregation
    - plugin: checkmk.general.bi_rule
      plugin_type: lookup
    - plugin: checkmk.general.bi_rules
      plugin_type: lookup
    - name: "Business Intelligence: The official user guide."
      description: "The official user guide on Business Intelligence (BI)."
      link: "https://docs.checkmk.com/latest/en/bi.html"
"""

EXAMPLES = r"""
# ---------------------------------------------------------------------------
# Create a BI rule
# ---------------------------------------------------------------------------
- name: "Create a BI rule."
  checkmk.general.bi_rule:
    server_url: "https://myserver"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
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

# ---------------------------------------------------------------------------
# Delete a BI rule
# ---------------------------------------------------------------------------
- name: "Delete a BI rule."
  checkmk.general.bi_rule:
    server_url: "https://myserver"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
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

diff:
  description: The diff between the current and the desired state.
  type: dict
  returned: when differences are detected or in diff mode
"""

import json

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.checkmk.general.plugins.module_utils.api import CheckmkAPI
from ansible_collections.checkmk.general.plugins.module_utils.bi import (
    object_attributes,
    prune_none,
    restrict_to_shape,
)
from ansible_collections.checkmk.general.plugins.module_utils.differ import ConfigDiffer
from ansible_collections.checkmk.general.plugins.module_utils.utils import (
    base_argument_spec,
)

# Suboptions of 'rule' that the Checkmk API requires when creating or updating.
REQUIRED_WHEN_PRESENT = (
    "nodes",
    "properties",
    "aggregation_function",
    "computation_options",
    "node_visualization",
)


class BIRuleHTTPCodes:
    """
    BIRuleHTTPCodes defines the HTTP status codes and corresponding messages
    for BI rule operations such as GET, CREATE, EDIT and DELETE.
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


class BIRuleAPI(CheckmkAPI):
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
        if not rule or not rule.get("id") or not rule.get("pack_id"):
            self.module.fail_json(msg="Missing 'id' or 'pack_id' in rule dictionary.")

        self.rule_id = rule["id"]
        self.pack_id = rule["pack_id"]

        # Only compare and send what the user actually specified. Unset options
        # arrive as None from the argument spec; the API rejects explicit nulls,
        # and they must not take part in the diff either.
        self.desired = prune_none(rule)

        self.state = None
        self._get_current()

        # Checkmk fills in defaults for nested options it was not given, so
        # compare only what the playbook actually specified.
        self.differ = ConfigDiffer(
            self.desired, restrict_to_shape(self.desired, self.current)
        )

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
                current_raw = json.loads(result.content)
            except json.JSONDecodeError:
                self.module.fail_json(
                    msg="Failed to decode JSON response from API.",
                    content=result.content,
                )

            # Some BI endpoints wrap the attributes in 'extensions',
            # others return them flat at the top level.
            self.current = object_attributes(current_raw)

            # The API reports pack_id as an empty string rather than the
            # owning pack, so it cannot be compared. Carry the desired
            # value over when the API does not report one, which keeps
            # the comparison correct if it ever starts to.
            # Consequence: moving to another pack is not detected.
            if not self.current.get("pack_id"):
                self.current["pack_id"] = self.desired.get("pack_id")
        else:
            self.state = "absent"
            self.current = {}

    def _build_endpoint(self, action):
        """
        Builds the API endpoint URL for the BI rule.

        The BI API expects create, read, update and delete on the very same
        object endpoint, so all supported actions share one URL.

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
            deletion (bool): If True, generate a diff for a deletion.

        Returns:
            dict: A dictionary containing the 'before' and 'after' states.
        """
        return self.differ.generate_diff(deletion=deletion)

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

    This function defines the module parameters, initializes the BIRuleAPI and performs
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
                pack_id=dict(type="str", required=True),
                id=dict(type="str", required=True),
                nodes=dict(type="list", elements="dict", required=False),
                properties=dict(type="dict", required=False),
                aggregation_function=dict(type="dict", required=False),
                computation_options=dict(type="dict", required=False),
                node_visualization=dict(type="dict", required=False),
                params=dict(
                    type="dict",
                    required=False,
                    default=dict(arguments=[]),
                    options=dict(
                        arguments=dict(
                            type="list", elements="str", required=False, default=[]
                        ),
                    ),
                ),
            ),
        ),
        state=dict(type="str", default="present", choices=["present", "absent"]),
    )

    required_if = [
        ("api_auth_type", "bearer", ["api_user", "api_secret"]),
        ("api_auth_type", "basic", ["api_user", "api_secret"]),
        ("api_auth_type", "cookie", ["api_auth_cookie"]),
    ]

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=required_if,
    )

    desired_state = module.params.get("state")
    rule = module.params.get("rule")

    # The API needs the full rule definition to create or update it, while a
    # deletion only needs the identifying attributes.
    if desired_state == "present":
        missing = [key for key in REQUIRED_WHEN_PRESENT if rule.get(key) is None]
        if missing:
            module.fail_json(
                msg="The following options are required in 'rule' when state is "
                "'present': %s" % ", ".join(missing)
            )

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
        else:
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

    Returns:
        None: Calls run_module() to handle the logic.
    """
    run_module()


if __name__ == "__main__":
    main()

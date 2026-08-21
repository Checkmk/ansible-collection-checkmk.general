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
module: bi_aggregation

short_description: Manage BI aggregations in Checkmk.

version_added: "8.4.0"

description:
    - Manage BI aggregations within Checkmk. This module allows the creation, updating and deletion of BI aggregations.

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
                    - The customer ID for this aggregation.
                    - Only available in the Checkmk Managed Services Edition.
                type: str
                required: false
            groups:
                description:
                    - Groups associated with the aggregation.
                    - Required when I(state=present). Pass empty lists to assign no groups.
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
                    - Required when I(state=present).
                type: dict
                required: false
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
                    - Required when I(state=present).
                type: dict
                required: false
            computation_options:
                description:
                    - Computation options.
                    - Required when I(state=present).
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

seealso:
    - module: checkmk.general.bi_pack
    - module: checkmk.general.bi_rule
    - plugin: checkmk.general.bi_aggregation
      plugin_type: lookup
    - plugin: checkmk.general.bi_aggregations
      plugin_type: lookup
    - name: "Business Intelligence: The official user guide."
      description: "The official user guide on Business Intelligence (BI)."
      link: "https://docs.checkmk.com/latest/en/bi.html"
"""

EXAMPLES = r"""
# ---------------------------------------------------------------------------
# Create a BI aggregation
# ---------------------------------------------------------------------------
- name: "Create a BI aggregation with state_of_host."
  checkmk.general.bi_aggregation:
    server_url: "https://myserver"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    aggregation:
      id: "aggr1"
      pack_id: "default"
      comment: "Aggregation comment"
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

# ---------------------------------------------------------------------------
# Delete a BI aggregation
# ---------------------------------------------------------------------------
- name: "Delete a BI aggregation."
  checkmk.general.bi_aggregation:
    server_url: "https://myserver"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    aggregation:
      id: "aggr1"
      pack_id: "default"
    state: "absent"
"""

RETURN = r"""
msg:
  description:
    - The output message that the module generates. Contains the API status details in case of an error.
  type: str
  returned: always
  sample: 'BI aggregation created.'

http_code:
  description:
    - The HTTP code the Checkmk API returns.
  type: int
  returned: always
  sample: 200

content:
  description:
    - The complete created/changed BI aggregation.
  returned: when the BI aggregation is created or updated.
  type: dict

diff:
  description: The diff between the current and the desired state.
  type: dict
  returned: when differences are detected or in diff mode
"""

import json

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.checkmk.general.plugins.module_utils.api import CheckmkAPI
from ansible_collections.checkmk.general.plugins.module_utils.bi import prune_none
from ansible_collections.checkmk.general.plugins.module_utils.differ import ConfigDiffer
from ansible_collections.checkmk.general.plugins.module_utils.utils import (
    base_argument_spec,
)

# Suboptions of 'aggregation' that the Checkmk API requires when creating or
# updating. Omitting any of them is answered with a 400, so check up front and
# report which ones are missing instead of passing the API error back.
REQUIRED_WHEN_PRESENT = (
    "groups",
    "node",
    "aggregation_visualization",
    "computation_options",
)


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


class BIAggregationAPI(CheckmkAPI):
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
        if (
            not aggregation
            or not aggregation.get("id")
            or not aggregation.get("pack_id")
        ):
            self.module.fail_json(
                msg="Missing 'id' or 'pack_id' in aggregation dictionary."
            )

        self.aggregation_id = aggregation["id"]
        self.pack_id = aggregation["pack_id"]

        # Only compare and send what the user actually specified. Unset options
        # arrive as None from the argument spec; the API rejects explicit nulls,
        # and they must not take part in the diff either.
        self.desired = prune_none(aggregation)

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
                current_raw = json.loads(result.content)
            except json.JSONDecodeError:
                self.module.fail_json(
                    msg="Failed to decode JSON response from API.",
                    content=result.content,
                )

            # The aggregation attributes live in 'extensions' of the returned
            # domain object. Comparing the whole domain object instead would
            # always report a difference, because of 'links' and friends.
            self.current = current_raw.get("extensions", {})

            # The identifying attributes are part of the domain object itself,
            # so carry them over for the comparison.
            self.current.setdefault("id", current_raw.get("id"))
            self.current.setdefault("pack_id", self.pack_id)
        else:
            self.state = "absent"
            self.current = {}

    def _build_endpoint(self, action="get"):
        """
        Build the API endpoint URL for the BI aggregation.

        The BI API expects create, read, update and delete on the very same
        object endpoint, so all supported actions share one URL.

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
        Determines whether an update to the BI aggregation is needed.

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
        Creates a new BI aggregation via the Checkmk API.

        Returns:
            dict: The result of the creation operation.
        """
        return self._perform_action(action="create", method="POST", data=self.desired)

    def edit(self):
        """
        Updates an existing BI aggregation via the Checkmk API.

        Returns:
            dict: The result of the update operation.
        """
        return self._perform_action(action="edit", method="PUT", data=self.desired)

    def delete(self):
        """
        Deletes an existing BI aggregation via the Checkmk API.

        Returns:
            dict: The result of the deletion operation.
        """
        return self._perform_action(action="delete", method="DELETE")


def run_module():
    """
    The main logic for the Ansible module.

    This function defines the module parameters, initializes the BIAggregationAPI and
    performs the appropriate action (create, edit, delete) based on the state of the
    BI aggregation.

    Returns:
        None: The result is returned to Ansible via module.exit_json().
    """
    argument_spec = base_argument_spec()
    argument_spec.update(
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
    aggregation = module.params.get("aggregation")

    # The API needs the full aggregation definition to create or update it,
    # while a deletion only needs the identifying attributes.
    if desired_state == "present":
        missing = [key for key in REQUIRED_WHEN_PRESENT if aggregation.get(key) is None]
        if missing:
            module.fail_json(
                msg="The following options are required in 'aggregation' when "
                "state is 'present': %s" % ", ".join(missing)
            )

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
        else:
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

    Returns:
        None: Calls run_module() to handle the logic.
    """
    run_module()


if __name__ == "__main__":
    main()

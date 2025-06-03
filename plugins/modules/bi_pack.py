#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2025, Robin Gierse <robin.gierse@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: bi_pack

short_description: Manage BI packs in Checkmk.

version_added: "6.1.0"

description:
  - Manage BI packs within Checkmk. This module allows the creation, updating, and deletion of BI packs via the Checkmk API.

extends_documentation_fragment: [checkmk.general.common]

options:

    pack:
        description: Definition of the BI pack as required by the Checkmk API.
        type: dict
        required: true
        suboptions:
            id:
                description: Unique identifier for the BI pack.
                type: str
                required: true

            title:
                description: Title of the BI pack.
                type: str
                required: false

            contact_groups:
                description: List of contact groups associated with the BI pack.
                type: list
                elements: str
                default: []
                required: false

            public:
                description: Whether the BI pack is public or not.
                type: bool
                default: false
                required: false

    state:
        description:
        - Desired state of the BI pack.
            Use `present` to create or update the BI pack.
            Use `absent` to delete the BI pack.
        type: str
        default: "present"
        choices:
            - present
            - absent

author:
    - Lars Getwan (@lgetwan)
"""

EXAMPLES = r"""
- name: Create a BI pack with Bearer Authentication
  bi_pack:
    server_url: "http://myserver/"
    site: "mysite"
    automation_auth_type: "bearer"
    automation_user: "myuser"
    automation_secret: "mysecret"
    pack:
      id: "cluster_pack"
      title: "Cluster Pack"
      contact_groups:
        - "Admins"
        - "DevOps"
      public: true
    state: "present"

- name: Create a BI pack with Basic Authentication
  bi_pack:
    server_url: "http://myserver/"
    site: "mysite"
    automation_auth_type: "basic"
    automation_user: "basicuser"
    automation_secret: "basicpassword"
    pack:
      id: "network_pack"
      title: "Network Pack"
      contact_groups:
        - "NetworkAdmins"
      public: false
    state: "present"

- name: Create a BI pack with Cookie Authentication
  bi_pack:
    server_url: "http://myserver/"
    site: "mysite"
    automation_auth_type: "cookie"
    automation_auth_cookie: "sessionid=abc123xyz"
    pack:
      id: "storage_pack"
      title: "Storage Pack"
      contact_groups:
        - "StorageAdmins"
      public: true
    state: "present"

- name: Delete a BI pack
  bi_pack:
    server_url: "http://myserver/"
    site: "mysite"
    automation_auth_type: "bearer"
    automation_user: "myuser"
    automation_secret: "mysecret"
    pack:
      id: "cluster_pack"
    state: "absent"
"""

RETURN = r"""
msg:
  description: The output message that the module generates. Contains the API status details in case of an error.
  type: str
  returned: always
  sample: 'BI pack created.'

http_code:
  description: The HTTP code the Checkmk API returns.
  type: int
  returned: always
  sample: 200

content:
  description: The complete created/changed BI pack.
  returned: when the BI pack is created or updated.
  type: dict
"""

import json

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.checkmk.general.plugins.module_utils.api import CheckmkAPI
from ansible_collections.checkmk.general.plugins.module_utils.differ import ConfigDiffer
from ansible_collections.checkmk.general.plugins.module_utils.utils import (
    base_argument_spec,
)


class BIPackHTTPCodes:
    """
    Defines HTTP status codes and corresponding actions for BI pack operations.
    """

    get = {
        200: (False, False, "BI pack found, nothing changed"),
        404: (False, False, "BI pack not found"),
    }
    create = {
        200: (True, False, "BI pack created"),
        201: (True, False, "BI pack created"),
        204: (True, False, "BI pack created"),
    }
    edit = {
        200: (True, False, "BI pack modified"),
    }
    delete = {
        204: (True, False, "BI pack deleted"),
    }


class BIPackAPIHandler(CheckmkAPI):
    """
    Manages BI pack operations via the Checkmk API.
    """

    def __init__(self, module):
        """Initialize BIPackAPIHandler with module parameters."""
        super().__init__(module)
        pack = module.params.get("pack")
        if not pack or "id" not in pack:
            self.module.fail_json(msg="Missing 'id' in pack dictionary")

        self.pack_id = pack["id"]
        self.desired = {
            "title": pack["title"],
            "contact_groups": pack.get("contact_groups"),
            "public": pack.get("public"),
        }

        self.state = None
        self._get_current()

        # Initialize the ConfigDiffer with desired and current configurations
        self.differ = ConfigDiffer(self.desired, self.current)

    def _get_current(self):
        """
        Fetches the current state of the BI pack from the Checkmk API.
        """
        endpoint = self._build_endpoint(action="get")
        response = self._fetch(
            code_mapping=BIPackHTTPCodes.get,
            endpoint=endpoint,
            method="GET",
        )

        if response.http_code == 200:
            self.state = "present"
            try:
                api_response = json.loads(response.content)
            except json.JSONDecodeError:
                self.module.fail_json(
                    msg="Failed to decode JSON response from API.",
                    content=response.content,
                )

            # Extrahiere relevante Felder aus 'extensions'
            extensions = api_response.get("extensions", {})

            self.current = {
                "title": extensions.get("title", api_response.get("title", "")),
                "contact_groups": extensions.get(
                    "contact_groups", api_response.get("contact_groups", [])
                ),
                "public": extensions.get("public", api_response.get("public", False)),
            }
        else:
            self.state = "absent"
            self.current = {}

    def _build_endpoint(self, action):
        """
        Constructs the API endpoint for the BI pack based on the action.

        Args:
            action (str): The action being performed ('get', 'create', 'edit', 'delete').

        Returns:
            str: The full API endpoint URL for the BI pack.

        Raises:
            AnsibleModule.fail_json: If an unsupported action is provided.
        """
        supported_actions = ["get", "create", "edit", "delete"]
        if action in supported_actions:
            return f"/objects/bi_pack/{self.pack_id}"
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
        Generates a diff output to show changes between the current and desired state.

        Args:
            deletion (bool): If True, generate a diff for a deletion.

        Returns:
            dict: A dictionary containing the 'before' and 'after' states of the BI pack.
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
                msg=f"BI pack would be {action_msgs.get(action, action)}.",
                changed=True,
                diff=diff,
            )

        response = self._fetch(
            code_mapping=getattr(BIPackHTTPCodes, action),
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
        Creates a new BI pack via the Checkmk API.

        Returns:
            dict: The result of the creation operation.
        """
        return self._perform_action(action="create", method="POST", data=self.desired)

    def edit(self):
        """
        Updates an existing BI pack via the Checkmk API.

        Returns:
            dict: The result of the update operation.
        """
        return self._perform_action(action="edit", method="PUT", data=self.desired)

    def delete(self):
        """
        Deletes an existing BI pack via the Checkmk API.

        Returns:
            dict: The result of the deletion operation.
        """
        return self._perform_action(action="delete", method="DELETE")


def run_module():
    """
    The main logic for the Ansible module.

    This function defines the module parameters, initializes the BIPackAPIHandler, and performs
    the appropriate action (create, edit, delete) based on the state of the BI pack.

    Returns:
        None: The result is returned to Ansible via module.exit_json().
    """
    argument_spec = base_argument_spec()
    argument_spec.update(
        pack=dict(
            type="dict",
            required=True,
            options=dict(
                id=dict(type="str", required=True),
                title=dict(type="str", required=False),
                contact_groups=dict(
                    type="list", elements="str", default=[], required=False
                ),
                public=dict(type="bool", default=False, required=False),
            ),
        ),
        state=dict(type="str", default="present", choices=["present", "absent"]),
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
    pack = module.params.get("pack")

    # Additional validation: 'title' is required when 'state' is 'present'
    if desired_state == "present":
        if "title" not in pack or not pack["title"]:
            module.fail_json(
                msg="'title' is required in 'pack' when state is 'present'."
            )

    bipack_api = BIPackAPIHandler(module)

    try:
        if desired_state == "present":
            if bipack_api.state == "absent":
                result = bipack_api.create()
            elif bipack_api.needs_update():
                result = bipack_api.edit()
            else:
                result = dict(
                    changed=False,
                    msg="BI pack is already in the desired state.",
                )
        elif desired_state == "absent":
            if bipack_api.state == "present":
                result = bipack_api.delete()
            else:
                result = dict(
                    changed=False,
                    msg="BI pack is already absent.",
                )
    except Exception as e:
        module.fail_json(msg=f"Error managing the BI pack: {e}")

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

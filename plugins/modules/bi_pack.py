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
module: bi_pack

short_description: Manage BI packs in Checkmk.

version_added: "8.4.0"

description:
  - Manage BI packs within Checkmk. This module allows the creation, updating and deletion of BI packs.

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
                description:
                  - Title of the BI pack.
                  - Required when I(state=present).
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
          - Use C(present) to create or update the BI pack.
          - Use C(absent) to delete the BI pack.
        type: str
        default: "present"
        choices:
            - present
            - absent

author:
    - Lars Getwan (@lgetwan)

seealso:
    - module: checkmk.general.bi_rule
    - module: checkmk.general.bi_aggregation
    - plugin: checkmk.general.bi_pack
      plugin_type: lookup
    - plugin: checkmk.general.bi_packs
      plugin_type: lookup
    - name: "Business Intelligence: The official user guide."
      description: "The official user guide on Business Intelligence (BI)."
      link: "https://docs.checkmk.com/latest/en/bi.html"
"""

EXAMPLES = r"""
# ---------------------------------------------------------------------------
# Create a BI pack
# ---------------------------------------------------------------------------
- name: "Create a BI pack."
  checkmk.general.bi_pack:
    server_url: "https://myserver"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    pack:
      id: "cluster_pack"
      title: "Cluster Pack"
      contact_groups:
        - "Admins"
        - "DevOps"
      public: true
    state: "present"

# ---------------------------------------------------------------------------
# Using basic authentication
# ---------------------------------------------------------------------------
- name: "Create a BI pack using basic authentication."
  checkmk.general.bi_pack:
    server_url: "https://myserver"
    site: "mysite"
    api_auth_type: "basic"
    api_user: "basicuser"
    api_secret: "basicpassword"
    pack:
      id: "network_pack"
      title: "Network Pack"
      contact_groups:
        - "NetworkAdmins"
      public: false
    state: "present"

# ---------------------------------------------------------------------------
# Using cookie authentication
# ---------------------------------------------------------------------------
- name: "Create a BI pack using cookie authentication."
  checkmk.general.bi_pack:
    server_url: "https://myserver"
    site: "mysite"
    api_auth_type: "cookie"
    api_auth_cookie: "auth_mysite=abc123xyz"
    pack:
      id: "storage_pack"
      title: "Storage Pack"
      contact_groups:
        - "StorageAdmins"
      public: true
    state: "present"

# ---------------------------------------------------------------------------
# Delete a BI pack
# ---------------------------------------------------------------------------
- name: "Delete a BI pack."
  checkmk.general.bi_pack:
    server_url: "https://myserver"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
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


class BIPackAPI(CheckmkAPI):
    """
    Manages BI pack operations via the Checkmk API.
    """

    def __init__(self, module):
        """Initialize BIPackAPI with module parameters."""
        super().__init__(module)
        pack = self.params.get("pack")
        if not pack or not pack.get("id"):
            self.module.fail_json(msg="Missing 'id' in pack dictionary.")

        self.pack_id = pack["id"]
        # title, contact_groups and public are all required by the API;
        # the latter two always have a default, so only title can be absent.
        self.desired = prune_none(
            {
                "title": pack.get("title"),
                "contact_groups": pack.get("contact_groups"),
                "public": pack.get("public"),
            }
        )

        self.state = None
        self._get_current()

        # Checkmk fills in defaults for options it was not given, so compare
        # only what the playbook actually specified.
        self.differ = ConfigDiffer(
            self.desired, restrict_to_shape(self.desired, self.current)
        )

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

            # Some BI endpoints wrap the attributes in 'extensions', others
            # return them flat at the top level.
            self.current = object_attributes(api_response)
        else:
            self.state = "absent"
            self.current = {}

    def _build_endpoint(self, action):
        """
        Constructs the API endpoint for the BI pack.

        The BI API expects create, read, update and delete on the very same
        object endpoint, so all supported actions share one URL.

        Args:
            action (str): The action being performed ('get', 'create', 'edit', 'delete').

        Returns:
            str: The API endpoint for the BI pack.
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
        Determines whether an update to the BI pack is needed.

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

    This function defines the module parameters, initializes the BIPackAPI and performs
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
    pack = module.params.get("pack")

    # Additional validation: 'title' is required when 'state' is 'present'
    if desired_state == "present" and not pack.get("title"):
        module.fail_json(msg="'title' is required in 'pack' when state is 'present'.")

    bipack_api = BIPackAPI(module)

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
        else:
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

    Returns:
        None: Calls run_module() to handle the logic.
    """
    run_module()


if __name__ == "__main__":
    main()

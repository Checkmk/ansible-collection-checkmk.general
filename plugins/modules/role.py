#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2025, Checkmk GmbH
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: role

short_description: Manage roles in Checkmk.

version_added: "7.5.0"

description:
    - Manage user roles within Checkmk. Custom roles are created by
      cloning an existing built-in role and can then be modified.
    - Built-in roles (C(admin), C(user), C(guest), C(agent_registration))
      cannot be created or deleted, but their permissions can be modified
      using this module with C(state=present).

extends_documentation_fragment:
    - checkmk.general.common

options:
    name:
        description:
            - The internal ID of the role. This is used to uniquely
              identify the role. It cannot be changed after creation.
        required: true
        type: str
    title:
        description:
            - The human-readable title (alias) of the role.
            - Optional when creating a new custom role. If omitted, the
              title of the source role is used.
        type: str
        aliases: ["alias"]
    based_on:
        description:
            - The ID of the built-in role to clone from when creating
              a new custom role. Valid values are C(admin), C(user),
              C(guest), and C(agent_registration).
            - Required when creating a new custom role.
            - This parameter is ignored when updating an existing role.
        type: str
        choices: ["admin", "user", "guest", "agent_registration"]
    permissions:
        description:
            - A dictionary of permissions to set on the role.
            - Keys are permission IDs (e.g., C(general.use), C(wato.edit),
              C(wato.all_folders)).
            - Values must be one of C(yes), C(no), or C(default). Values
              must be quoted strings in YAML; unquoted C(yes) and C(no) are
              interpreted as booleans and will be rejected.
            - The value C(default) reverts a permission to the base role's
              setting. It is only valid for custom roles. For built-in roles
              (C(admin), C(user), C(guest), C(agent_registration)) use
              C(yes) or C(no) explicitly.
            - Permissions not listed here will remain unchanged.
            - You can find the internal permission IDs in the Checkmk
              GUI under I(Setup > Users > Roles & permissions) using
              the inline help (available from Checkmk 2.4.0 onwards
              via Werk #17953).
        type: dict
    state:
        description:
            - The desired state of the role.
            - C(present) ensures the role exists with the specified
              configuration. If the role does not exist, it will be
              created by cloning the role specified in C(based_on).
            - C(absent) ensures the custom role does not exist.
              Built-in roles cannot be deleted.
        type: str
        default: present
        choices: ["present", "absent"]

author:
    - "Checkmk GmbH (@checkmk)"

notes:
    - "Idempotency: This module compares the desired configuration
      against the current state and only makes changes when necessary."
    - "Built-in roles (admin, user, guest, agent_registration) cannot
      be created or deleted, but their permissions can be updated."

seealso:
    - module: checkmk.general.user
    - name: "Checkmk documentation on roles"
      description: "Complete documentation for user roles and permissions."
      link: "https://docs.checkmk.com/latest/en/wato_user.html"
"""

EXAMPLES = r"""
# Create a custom role based on the "user" role.
- name: "Create a custom monitoring role."
  checkmk.general.role:
    server_url: "http://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    name: "limited_user"
    title: "Limited Monitoring User"
    based_on: "user"
    state: "present"

# Create a custom role with specific permissions.
- name: "Create a custom role with tailored permissions."
  checkmk.general.role:
    server_url: "http://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    name: "host_manager"
    title: "Host Manager"
    based_on: "user"
    permissions:
      wato.all_folders: "yes"
      wato.edit: "yes"
      wato.manage_hosts: "yes"
      general.edit_notifications: "no"
    state: "present"

# Update permissions on an existing role.
- name: "Update permissions on an existing custom role."
  checkmk.general.role:
    server_url: "http://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    name: "host_manager"
    permissions:
      wato.all_folders: "yes"
    state: "present"

# Update permissions on a built-in role.
- name: "Modify permissions on the built-in user role."
  checkmk.general.role:
    server_url: "http://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    name: "user"
    permissions:
      general.edit_notifications: "no"
    state: "present"

# Delete a custom role.
- name: "Delete a custom role."
  checkmk.general.role:
    server_url: "http://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    name: "limited_user"
    state: "absent"
"""

RETURN = r"""
msg:
    description: The output message that the module generates. Contains
                 the API response details in case of an error.
    type: str
    returned: always
    sample: 'Role created.'
http_code:
    description: The HTTP code the Checkmk API returns.
    type: int
    returned: always
    sample: 200
"""

import json

# https://docs.ansible.com/ansible/latest/dev_guide/testing/sanity/import.html
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.checkmk.general.plugins.module_utils.api import (
    CheckmkAPI,
)
from ansible_collections.checkmk.general.plugins.module_utils.types import RESULT
from ansible_collections.checkmk.general.plugins.module_utils.utils import (
    base_argument_spec,
    result_as_dict,
)

BUILTIN_ROLES = ("admin", "user", "guest", "agent_registration")
VALID_PERMISSION_VALUES = frozenset(("yes", "no", "default"))

# 404 is not failed for GET — we use it to detect absence.
HTTP_CODES_GET = {
    200: (False, False, "Role found, nothing changed."),
    404: (False, False, "Role not found."),
}

HTTP_CODES_CREATE = {
    200: (True, False, "Role created."),
}

HTTP_CODES_EDIT = {
    200: (True, False, "Role updated."),
}

HTTP_CODES_DELETE = {
    204: (True, False, "Role deleted."),
}


class RoleAPI(CheckmkAPI):
    def __init__(self, module):
        super().__init__(module)

        self.params = self.module.params
        self.state = self.params.get("state")
        self.name = self.params.get("name")
        self.title = self.params.get("title")
        self.based_on = self.params.get("based_on")
        self.permissions = self.params.get("permissions")

        self.current = self._fetch(
            code_mapping=HTTP_CODES_GET,
            endpoint="/objects/user_role/%s" % self.name,
            method="GET",
        )

    def _build_edit_data(self):
        data = {}

        if self.title is not None:
            data["new_alias"] = self.title

        if self.permissions is not None:
            data["new_permissions"] = self.permissions

        return data

    def _get_base_role_permissions(self, based_on):
        if not based_on:
            return set()
        result = self._fetch(
            code_mapping={200: (False, False, "Base role found.")},
            endpoint="/objects/user_role/%s" % based_on,
            method="GET",
        )
        if result.http_code != 200:
            return set()
        content = json.loads(result.content.decode("utf-8"))
        return set(content.get("extensions", {}).get("permissions", []))

    def _needs_update(self):
        if self.current.http_code != 200:
            return False

        current_content = json.loads(self.current.content.decode("utf-8"))
        current_extensions = current_content.get("extensions", {})

        if self.title is not None:
            if current_extensions.get("alias", "") != self.title:
                return True

        if self.permissions is not None:
            current_perms = set(current_extensions.get("permissions", []))
            has_default = any(v == "default" for v in self.permissions.values())
            base_perms = (
                self._get_base_role_permissions(current_extensions.get("basedon", ""))
                if has_default
                else set()
            )

            for perm, value in self.permissions.items():
                if value == "yes" and perm not in current_perms:
                    return True
                elif value == "no" and perm in current_perms:
                    return True
                elif value == "default":
                    if (perm in base_perms) != (perm in current_perms):
                        return True

        return False

    def create(self):
        data = {
            "role_id": self.based_on,
            "new_role_id": self.name,
        }

        if self.title is not None:
            data["new_alias"] = self.title

        # Note: permissions cannot be set on create via the API.
        # They are applied via a follow-up PUT in run_module() if specified.

        return self._fetch(
            code_mapping=HTTP_CODES_CREATE,
            endpoint="/domain-types/user_role/collections/all",
            data=data,
            method="POST",
        )

    def edit(self):
        data = self._build_edit_data()

        if not data:
            return RESULT(
                http_code=200,
                msg="Role already up to date.",
                content={},
                etag="",
                failed=False,
                changed=False,
            )

        if self.current.etag:
            self.headers["If-Match"] = self.current.etag
        return self._fetch(
            code_mapping=HTTP_CODES_EDIT,
            endpoint="/objects/user_role/%s" % self.name,
            data=data,
            method="PUT",
        )

    def delete(self):
        if self.current.etag:
            self.headers["If-Match"] = self.current.etag
        return self._fetch(
            code_mapping=HTTP_CODES_DELETE,
            endpoint="/objects/user_role/%s" % self.name,
            method="DELETE",
        )


def run_module():
    module_args = base_argument_spec()
    module_args.update(
        dict(
            name=dict(type="str", required=True),
            title=dict(type="str", aliases=["alias"]),
            based_on=dict(
                type="str",
                choices=["admin", "user", "guest", "agent_registration"],
            ),
            permissions=dict(type="dict"),
            state=dict(
                type="str",
                default="present",
                choices=["present", "absent"],
            ),
        )
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    name = module.params.get("name")
    permissions = module.params.get("permissions")
    if permissions:
        for perm, value in permissions.items():
            if value not in VALID_PERMISSION_VALUES:
                module.fail_json(
                    msg="Invalid permission value '%s' for '%s'. Must be one of: %s."
                    % (value, perm, ", ".join(sorted(VALID_PERMISSION_VALUES)))
                )
                return
            if name in BUILTIN_ROLES and value == "default":
                module.fail_json(
                    msg="Permission value 'default' is not valid for built-in role '%s'. "
                    "Built-in roles have no base role; use 'yes' or 'no' explicitly."
                    % name
                )
                return

    role = RoleAPI(module)
    result = RESULT(
        http_code=0,
        msg="Nothing to be done.",
        content={},
        etag="",
        failed=False,
        changed=False,
    )

    if role.state == "present":
        if role.current.http_code == 200:
            if role._needs_update():
                if not module.check_mode:
                    result = role.edit()
                else:
                    result = RESULT(
                        http_code=200,
                        msg="Role would be updated.",
                        content={},
                        etag="",
                        failed=False,
                        changed=True,
                    )
            else:
                result = RESULT(
                    http_code=200,
                    msg="Role already exists with desired state.",
                    content={},
                    etag="",
                    failed=False,
                    changed=False,
                )
        elif role.current.http_code == 404:
            if role.based_on is None:
                module.fail_json(
                    msg="'based_on' is required when creating a new custom role."
                )
                return
            if not module.check_mode:
                result = role.create()
                # Permissions cannot be set during create; apply via PUT if needed.
                # Null title so the follow-up edit only sends new_permissions.
                if not result.failed and role.permissions is not None:
                    role.title = None
                    edit_result = role.edit()
                    if edit_result.failed:
                        module.fail_json(msg=edit_result.msg)
                        return
            else:
                result = RESULT(
                    http_code=200,
                    msg="Role would be created.",
                    content={},
                    etag="",
                    failed=False,
                    changed=True,
                )

    elif role.state == "absent":
        if role.current.http_code == 200:
            if role.name in BUILTIN_ROLES:
                module.fail_json(
                    msg="Built-in role '%s' cannot be deleted." % role.name
                )
                return
            if not module.check_mode:
                result = role.delete()
            else:
                result = RESULT(
                    http_code=204,
                    msg="Role would be deleted.",
                    content={},
                    etag="",
                    failed=False,
                    changed=True,
                )
        elif role.current.http_code == 404:
            result = RESULT(
                http_code=0,
                msg="Role already absent.",
                content={},
                etag="",
                failed=False,
                changed=False,
            )

    module.exit_json(**result_as_dict(result))


def main():
    run_module()


if __name__ == "__main__":
    main()

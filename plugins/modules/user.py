#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2023, Lars Getwan <lars.getwan@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: user

short_description: Manage users in Checkmk.

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "0.18.0"

description:
- Create and delete users within Checkmk.

extends_documentation_fragment: [checkmk.general.common]

options:
    name:
        description: The user you want to manage.
        required: true
        type: str
    fullname:
        description: The alias or full name of the user.
        type: str
    customer:
        description: For the Checkmk Managed Edition (CME), you need to specify which customer ID this object belongs to.
        required: false
        type: str
    password:
        description: The password or secret for login.
        type: str
    enforce_password_change:
        description: If set to true, the user will be forced to change his/her password at the next login.
        type: bool
    auth_type:
        description: The authentication type.
        type: str
        choices: [password, automation]
    disable_login:
        description: The user can be blocked from login but will remain part of the site. The disabling does not affect notification and alerts.
        type: bool
    email:
        description: The mail address of the user. Required if the user is a monitoring contact and receives notifications via mail.
        type: str
    fallback_contact:
        description: In case none of your notification rules handles a certain event a notification will be sent to the specified email.
        type: bool
    pager_address:
        description: The pager address.
        type: str
    idle_timeout_duration:
        description: The duration in seconds of the individual idle timeout if individual is selected as idle timeout option.
        type: str
    idle_timeout_option:
        description: Specify if the idle timeout should use the global configuration, be disabled or use an individual duration
        type: str
        choices: [global, disable, individual]
    roles:
        description: The list of assigned roles to the user.
        type: raw
    authorized_sites:
        description: The names of the sites the user is authorized to handle.
        type: raw
    contactgroups:
        description: Assign the user to one or multiple contact groups. If no contact group is specified then no monitoring contact will be created.
        type: raw
    disable_notifications:
        description: Option if all notifications should be temporarily disabled.
        type: raw
    language:
        description: Configure the language to be used by the user in the user interface. Omitting this will configure the default language.
        type: str
        choices: [default, en, de, ro]
    state:
        description: Desired state
        type: str
        default: present
        choices: [present, absent, reset_password]

author:
    - Lars Getwan (@lgetwan)
"""

EXAMPLES = r"""
# Create a user.
- name: "Create a user."
  checkmk.general.user:
    server_url: "http://my_server/"
    site: "local"
    automation_user: "my_user"
    automation_secret: "my_secret"
    name: "krichards"
    fullname: "Keith Richards"
    customer: "provider"
    email: "keith.richards@rollingstones.com"
    password: "Open-G"
    contactgroups:
        - "rolling_stones"
        - "glimmer_twins"
        - "x-pensive_winos"
        - "potc_cast"
    state: "present"

# Create an automation user.
- name: "Create an automation user."
  checkmk.general.user:
    server_url: "http://my_server/"
    site: "local"
    automation_user: "my_user"
    automation_secret: "my_secret"
    name: "registration"
    fullname: "Registration User"
    customer: "provider"
    auth_type: "automation"
    password: "ZGSDHUVDSKJHSDF"
    roles:
        - "registration"
    state: "present"

# Create a detailed user.
- name: "Create a detailed user."
  checkmk.general.user:
    server_url: "http://my_server/"
    site: "local"
    automation_user: "my_user"
    automation_secret: "my_secret"
    name: "horst"
    fullname: "Horst Schlämmer"
    customer: "provider"
    auth_type: "password"
    password: "uschi"
    enforce_password_change: True
    email: "checker@grevenbroich.de"
    fallback_contact: True
    pager_address: 089-123456789
    contactgroups:
      - "sport"
      - "vereinsgeschehen"
      - "lokalpolitik"
    disable_notifications: '{"disable": true, "timerange": { "start_time": "2023-02-23T15:06:48+00:00", "end_time": "2023-02-23T16:06:48+00:00"}}'
    language: "de"
    roles:
      - "user"
    authorized_sites:
      - "{{ my_site }}"
    state: "present"
"""

RETURN = r"""
# These are examples of possible return values, and in general should use other names for return values.
message:
    description: The output message that the module generates. Contains the API response details in case of an error.
    type: str
    returned: always
    sample: 'User created.'
"""


import json

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.tribe29.checkmk.plugins.module_utils.api import CheckmkAPI
from ansible_collections.tribe29.checkmk.plugins.module_utils.utils import (
    result_as_dict,
)

USER = (
    "username",
    "fullname",
    "password",
    "enforce_password_change",
    "auth_type",
    "disable_login",
    "email",
    "fallback_contact",
    "pager_address",
    "idle_timout_option",
    "idle_timeout_duration",
    "roles",
    "authorized_sites",
    "contactgroups",
    "disable_notifications",
    "language",
)


class UserHTTPCodes:
    # http_code: (changed, failed, "Message")
    get = {
        200: (False, False, "User found, nothing changed"),
        404: (False, False, "User not found"),
    }

    create = {200: (True, False, "User created")}
    edit = {200: (True, False, "User modified")}
    delete = {204: (True, False, "User deleted")}


class UserEndpoints:
    default = "/objects/user_config"
    create = "/domain-types/user_config/collections/all"


class UserAPI(CheckmkAPI):
    def _build_user_data(self):
        user = {}

        # For some keys the API has required sub keys. We can use them as indicator,
        # that the key must be used
        if self.required.get("auth_type"):
            user["auth_option"] = {}
        if self.required.get("email"):
            user["contact_options"] = {}
        if self.required.get("idle_timeout_option"):
            user["idle_timeout"] = {}

        for key, value in self.required.items():
            if key in (
                "username",
                "fullname",
                "disable_login",
                "pager_address",
                "roles",
                "authorized_sites",
                "contactgroups",
                "language",
            ):
                user[key] = value

            if key in ("auth_type", "password", "enforce_password_change"):
                if key == "password" and self.params.get("auth_type") == "automation":
                    # Unfortunately the API uses different strings for the password
                    # depending on the kind of user...
                    key = "secret"
                user["auth_option"][key] = value

            if key in ("email", "fallback_contact"):
                user["contact_options"][key] = value

            if key in ("idle_timeout_option", "idle_timeout_duration"):
                user["idle_timeout"] = value

            if key == "disable_notifications":
                user["disable_notifications"]["disable"] = value

        return user

    def _set_current(self, result):
        # A flat hierarchy allows an easy comparison of differences
        if result.http_code == 200:
            content = json.loads(result.content)["extensions"]
            for key in USER:
                if key in content:
                    self.current[key] = content[key]

    def _build_default_endpoint(self):
        return "%s/%s" % (UserEndpoints.default, self.params.get("name"))

    def build_required(self):
        # A flat hierarchy allows an easy comparison of differences
        for key in USER:
            if key == "username":
                self.required[key] = self.params["name"]
                continue
            if self.params.get(key) is None:
                continue
            self.required[key] = self.params[key]

    def needs_editing(self):
        black_list = ("username", "password", "auth_type", "authorized_sites")
        for key, value in self.required.items():
            if key not in black_list and self.current.get(key) != value:
                return True
        return False

    def get(self):
        result = self._fetch(
            code_mapping=UserHTTPCodes.get,
            endpoint=self._build_default_endpoint(),
            method="GET",
        )

        self.state = "present" if result.http_code == 200 else "absent"
        self._set_current(result)

        return result

    def create(self):
        data = self._build_user_data()
        # It's allowed in Ansible to skip the fullname, but it's not allowed
        # in the Checkmk API...
        data.setdefault("fullname", data["username"])

        result = self._fetch(
            code_mapping=UserHTTPCodes.create,
            endpoint=UserEndpoints.create,
            data=data,
            method="POST",
        )

        return result

    def edit(self, etag):
        data = self._build_user_data()
        self.headers["if-Match"] = etag

        result = self._fetch(
            code_mapping=UserHTTPCodes.edit,
            endpoint=self._build_default_endpoint(),
            data=data,
            method="PUT",
        )

        return result

    def delete(self):
        result = self._fetch(
            code_mapping=UserHTTPCodes.delete,
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
        name=dict(required=True, type="str"),
        fullname=dict(type="str"),
        customer=dict(type="str", required=False),
        password=dict(type="str", no_log=True),
        enforce_password_change=dict(type="bool", no_log=False),
        auth_type=dict(type="str", choices=["password", "automation"]),
        disable_login=dict(type="bool"),
        email=dict(type="str"),
        fallback_contact=dict(type="bool"),
        pager_address=dict(type="str"),
        idle_timeout_duration=dict(type="str"),
        idle_timeout_option=dict(
            type="str", choices=["global", "disable", "individual"]
        ),
        roles=dict(type="raw"),
        authorized_sites=dict(type="raw"),
        contactgroups=dict(type="raw"),
        disable_notifications=dict(type="raw"),
        language=dict(type="str", choices=["default", "en", "de", "ro"]),
        state=dict(
            type="str",
            default="present",
            choices=["present", "absent", "reset_password"],
        ),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=False)

    # Use the parameters to initialize some common api variables
    user = UserAPI(module)

    user.build_required()
    result = user.get()
    etag = result.etag

    required_state = user.params.get("state")
    if user.state == "present":
        if required_state == "reset_password":
            user.required.pop("username")
            result = user.edit(etag)
        elif required_state == "absent":
            result = user.delete()
        elif user.needs_editing():
            user.required.pop("username")
            result = user.edit(etag)
    elif user.state == "absent":
        if required_state in ("present", "reset_password"):
            result = user.create()

    module.exit_json(**result_as_dict(result))


def main():
    run_module()


if __name__ == "__main__":
    main()

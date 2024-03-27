#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2023, Lars Getwan <lars.getwan@checkmk.com> &
#                      Marcel Arentz <gdspd_you@open-one.de> &
#                      Max Sickora <max.sickora@checkmk.com>
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
- Manage users in Checkmk.

extends_documentation_fragment: [checkmk.general.common]

options:
    auth_type:
        description:
            - The authentication type.
              Setting this to C(password) will create a normal user, C(automation) will create an automation user.
        type: str
        choices: [password, automation]
    authorized_sites:
        description: The names of the sites the user is authorized to access.
        type: raw
    contactgroups:
        description: A list of contact groups assigned to the user.
        type: raw
    customer:
        description:
            - For the Checkmk Managed Edition (CME), you need to specify which customer ID this object belongs to.
        type: str
    disable_notifications:
        description: Temporarily disable B(all) notifications for this user.
        type: bool
    disable_login:
        description:
            - If set to C(true), the user cannot log in anymore, but will remain part of the site.
              Disabling a user does not affect notifications.
        type: bool
    disable_notifications_timerange:
        description: The duration, for how log notifications should be disabled, if C(disable_notifications) is set to C(true).
        type: dict
    email:
        description:
            - The mail address of the user. Required if the user is a monitoring contact and should receive notifications via mail.
        type: str
    enforce_password_change:
        description: If set to C(true), the user will be forced to change their password on the next login.
        type: bool
    fallback_contact:
        description:
            - This user will receive fallback notifications.
              This means, if no notification rules match a certain event, they are sent to the fallback contacts.
        type: bool
    fullname:
        description: A alias or the full name of the user.
        type: str
    idle_timeout_duration:
        description: The duration in seconds, if C(idle_timeout_option) is set to C(individual).
        type: int
    idle_timeout_option:
        description:
            - Specify, whether the idle timeout should use the global configuration, use an individual duration or be disabled entirely.
        type: str
        choices: [global, disable, individual]
    interface_theme:
        description: The theme of the user interface.
        type: str
        choices: [default, dark, light]
    language:
        description:
            - Configure the language to be used by the user in the user interface.
              Omitting this will configure the default language.
        type: str
        choices: [default, en, de]
    mega_menu_icons:
        description:
          - This option decides if colored icons should be shown for every entry in the mega menus
            or only for the headlines (the 'topics').
        type: str
        choices: [topic, entry]
    name:
        description: The user you want to manage.
        required: true
        type: str
    navigation_bar_icons:
        description: This option decides if icons in the navigation bar should show/hide the respective titles.
        type: str
        choices: [hide, show]
    pager:
        description: A (mobile) phone number, used to receive e.g., SMS.
        type: str
        aliases: ["pager_address"]
    password:
        description:
            - The password or secret for login. Depending on the C(auth_type), this is interpreted as a password or secret.
        type: str
    roles:
        description: A list of roles assigned to the user.
        type: raw
    show_mode:
        description:
          - This option decides what show mode should be used for unvisited menus.
            Alternatively, this option can also be used to enforce show more removing the three dots for all menus.
        type: str
        choices: [default, default_show_less, default_show_more, enforce_show_more]
    sidebar_position:
        description: The position of the sidebar.
        type: str
        choices: [left, right]
    state:
        description: The desired state.
        type: str
        default: present
        choices: [present, absent, reset_password]

author:
    - Lars Getwan (@lgetwan)
    - Marcel Arentz (@godspeed-you)
    - Max Sickora (@max-checkmk)
"""

EXAMPLES = r"""
# Create a user.
- name: "Create a user."
  checkmk.general.user:
    server_url: "http://myserver/"
    site: "local"
    automation_user: "myuser"
    automation_secret: "mysecret"
    name: "krichards"
    fullname: "Keith Richards"
    email: "keith.richards@rollingstones.com"
    password: "Open-G"
    contactgroups:
      - "rolling_stones"
      - "glimmer_twins"
      - "x-pensive_winos"
      - "potc_cast"

# Create an automation user.
- name: "Create an automation user."
  checkmk.general.user:
    server_url: "http://myserver/"
    site: "local"
    automation_user: "myuser"
    automation_secret: "mysecret"
    name: "registration"
    fullname: "Registration User"
    auth_type: "automation"
    password: "ZGSDHUVDSKJHSDF"
    roles:
      - "registration"
    state: "present"

# Create a user with the Checkmk Managed Edition (CME), using the `customer` parameter.
- name: "Create a user."
  checkmk.general.user:
    server_url: "http://myserver/"
    site: "local"
    automation_user: "myuser"
    automation_secret: "mysecret"
    name: "krichards"
    fullname: "Keith Richards"
    email: "keith.richards@rollingstones.com"
    customer: "provider"
    password: "Open-G"
    contactgroups:
      - "rolling_stones"
      - "glimmer_twins"
      - "x-pensive_winos"
      - "potc_cast"

# Create a detailed user.
- name: "Create a more complex user."
  checkmk.general.user:
    server_url: "http://myserver/"
    site: "local"
    automation_user: "myuser"
    automation_secret: "mysecret"
    name: "horst"
    fullname: "Horst Schlämmer"
    customer: "provider"
    auth_type: "password"
    password: "uschi"
    enforce_password_change: true
    email: "checker@grevenbroich.de"
    fallback_contact: True
    pager: 089-123456789
    contactgroups:
      - "sport"
      - "vereinsgeschehen"
      - "lokalpolitik"
    disable_notifications: True
    disable_notifications_timerange: { "start_time": "2023-02-23T15:06:48+00:00", "end_time": "2023-02-23T16:06:48+00:00"}
    language: "de"
    roles:
      - "user"
    authorized_sites:
      - "{{ mysite }}"
    interface_theme: "dark"
    sidebar_position: "right"
    navigation_bar_icons: "show"
    mega_menu_icons: "entry"
    show_mode: "default_show_more"
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
from ansible_collections.checkmk.general.plugins.module_utils.api import CheckmkAPI
from ansible_collections.checkmk.general.plugins.module_utils.types import RESULT
from ansible_collections.checkmk.general.plugins.module_utils.utils import (
    result_as_dict,
)
from ansible_collections.checkmk.general.plugins.module_utils.version import (
    CheckmkVersion,
)

USER = (
    "username",
    "fullname",
    "customer",
    "password",
    "enforce_password_change",
    "auth_type",
    "disable_login",
    "email",
    "fallback_contact",
    "pager",
    "idle_timeout_option",
    "idle_timeout_duration",
    "roles",
    "authorized_sites",
    "contactgroups",
    "disable_notifications",
    "disable_notifications_timerange",
    "language",
    "interface_theme",
    "sidebar_position",
    "navigation_bar_icons",
    "mega_menu_icons",
    "show_mode",
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

        user["disable_notifications"] = {}
        user["interface_options"] = {}

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
                "customer",
                "disable_login",
                "roles",
                "authorized_sites",
                "contactgroups",
            ):
                user[key] = value

            if key in "pager":
                key = "pager_address"
                user[key] = value

            if key in "language":
                if value != "default":
                    user["language"] = value

            if key in ("auth_type", "password", "enforce_password_change"):
                if key == "password" and self.params.get("auth_type") == "automation":
                    # Unfortunately the API uses different strings for the password
                    # depending on the kind of user...
                    key = "secret"
                user["auth_option"][key] = value

            if key in ("email", "fallback_contact"):
                user["contact_options"][key] = value

            if key == "idle_timeout_option":
                user["idle_timeout"]["option"] = value
            if key == "idle_timeout_duration":
                user["idle_timeout"]["duration"] = value

            if key == "disable_notifications":
                user["disable_notifications"]["disable"] = value
            if key == "disable_notifications_timerange":
                user["disable_notifications"]["timerange"] = value

            if key in (
                "interface_theme",
                "sidebar_position",
                "navigation_bar_icons",
                "mega_menu_icons",
                "show_mode",
            ):
                user["interface_options"][key] = value

        return user

    def _set_current(self, result):
        # A flat hierarchy allows an easy comparison of differences
        content = json.loads(result.content)["extensions"]
        for key in USER:
            if key in content:
                if key != "disable_notifications":
                    self.current[key] = content[key]
            if key in "pager" and "pager_address" in content:
                self.current[key] = content["pager_address"]
            if key in ("email", "fallback_contact") and "contact_options" in content:
                self.current[key] = content["contact_options"][key]
            if key == "idle_timeout_option":
                self.current[key] = content["idle_timeout"]["option"]
            if key == "idle_timeout_duration":
                if "duration" in content["idle_timeout"]:
                    self.current[key] = content["idle_timeout"]["duration"]
            if key == "disable_notifications":
                if "disable" in content["disable_notifications"]:
                    self.current[key] = content["disable_notifications"]["disable"]
                else:
                    self.current[key] = False
            if key == "disable_notifications_timerange":
                if "timerange" in content["disable_notifications"]:
                    self.current[key] = content["disable_notifications"]["timerange"]

            if (
                key
                in (
                    "interface_theme",
                    "sidebar_position",
                    "navigation_bar_icons",
                    "mega_menu_icons",
                    "show_mode",
                )
                and key in content["interface_options"]
            ):
                self.current[key] = content["interface_options"][key]

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

    def shortpassword(self, data):
        ver = self.getversion()
        if ver >= CheckmkVersion("2.3.0") and "auth_option" in data:
            if (
                "password" in data["auth_option"]
                and len(data["auth_option"]["password"]) < 12
            ) or (
                "secret" in data["auth_option"]
                and len(data["auth_option"]["secret"]) < 10
            ):
                return True
        return False

    def get(self):
        result = self._fetch(
            code_mapping=UserHTTPCodes.get,
            endpoint=self._build_default_endpoint(),
            method="GET",
        )

        if result.http_code == 200:
            self.state = "present"
            self._set_current(result)
        else:
            self.state = "absent"
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

        if self.shortpassword(data):
            result = RESULT(
                http_code=0,
                msg="Password too short. For 2.3 and higher, please provide at least 12 characters (automation min. 10).",
                content="",
                etag="",
                failed=True,
                changed=False,
            )
        else:
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
        pager=dict(type="str", aliases=["pager_address"]),
        idle_timeout_duration=dict(type="int"),
        idle_timeout_option=dict(
            type="str", choices=["global", "disable", "individual"]
        ),
        roles=dict(type="raw"),
        authorized_sites=dict(type="raw"),
        contactgroups=dict(type="raw"),
        disable_notifications=dict(type="bool"),
        disable_notifications_timerange=dict(type="dict"),
        language=dict(type="str", choices=["default", "en", "de"]),
        interface_theme=dict(type="str", choices=["default", "dark", "light"]),
        sidebar_position=dict(type="str", choices=["left", "right"]),
        navigation_bar_icons=dict(type="str", choices=["hide", "show"]),
        mega_menu_icons=dict(type="str", choices=["topic", "entry"]),
        show_mode=dict(
            type="str",
            choices=[
                "default",
                "default_show_less",
                "default_show_more",
                "enforce_show_more",
            ],
        ),
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
        if required_state in "present":
            result = user.create()
        if required_state in "reset_password":
            result = RESULT(
                http_code=0,
                msg="Can't reset the password for an absent user.",
                content="",
                etag="",
                failed=False,
                changed=False,
            )

    module.exit_json(**result_as_dict(result))


def main():
    run_module()


if __name__ == "__main__":
    main()

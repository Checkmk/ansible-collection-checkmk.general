#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2022, Robin Gierse <robin.gierse@checkmk.com>
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
    server_url: "http://localhost/"
    site: "local"
    automation_user: "automation"
    automation_secret: "$SECRET"
    name: "krichards"
    fullname: "Keith Richards"
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
    server_url: "http://localhost/"
    site: "local"
    automation_user: "automation"
    automation_secret: "$SECRET"
    name: "registration"
    fullname: "Registration User"
    auth_type: "automation"
    password: "ZGSDHUVDSKJHSDF"
    roles:
        - "registration"
    state: "present"

# Create a detailed user.
- name: "Create a detailed user."
  checkmk.general.user:
    server_url: "http://localhost/"
    site: "local"
    automation_user: "automation"
    automation_secret: "$SECRET"
    name: "horst"
    fullname: "Horst Schlämmer"
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
      - "{{ site }}"
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

LOG = []

import copy
import json

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url


def exit_failed(module, msg):
    result = {
        "msg": "%s, log: %s" % (msg, " § ".join(LOG)),
        "changed": False,
        "failed": True,
    }
    module.fail_json(**result)


def exit_changed(module, msg):
    result = {
        "msg": "%s, log: %s" % (msg, " § ".join(LOG)),
        "changed": True,
        "failed": False,
    }
    module.exit_json(**result)


def exit_ok(module, msg):
    result = {
        "msg": "%s, log: %s" % (msg, " § ".join(LOG)),
        "changed": False,
        "failed": False,
    }
    module.exit_json(**result)


def log(msg):
    LOG.append(msg)


class User:

    default_attributes = {
        "disable_login": False,
        "contact_options": {"email": "", "fallback_contact": False},
        "idle_timeout": {"option": "global"},
        "roles": ["user"],
        "contactgroups": [],
        "pager_address": "",
        "disable_notifications": {},
    }

    def __init__(self, username, state="present", attributes=None, etag=None):
        if attributes is None:
            self.attributes = self.default_attributes
        else:
            self.attributes = attributes
        self.state = state
        self.username = username
        self.etag = etag

    def __repr__(self):
        return "User(name: %s, state: %s, attributes: %s, etag: %s)" % (
            self.username,
            self.state,
            str(self.attributes),
            self.etag,
        )

    @classmethod
    def from_api_response(cls, module, api_params):

        # Determine the current state of this particular user
        api_attributes, state, etag = get_current_user_state(module, api_params)

        attributes = copy.deepcopy(api_attributes)

        return cls(module.params["name"], state, attributes, etag)

    @classmethod
    def from_module(cls, params):

        attributes = cls.default_attributes

        attributes["username"] = params["name"]

        def _exists(key):
            return key in params and params[key] is not None

        if _exists("fullname"):
            attributes["fullname"] = params["fullname"]

        if _exists("disable_login"):
            attributes["disable_login"] = params["disable_login"]

        if _exists("pager_address"):
            attributes["pager_address"] = params["pager_address"]

        if _exists("language") and params["language"] != "default":
            attributes["language"] = params["language"]

        if _exists("auth_type"):
            auth_option = {}

            if params.get("auth_type") == "password" and _exists("password"):
                auth_option["password"] = params["password"]
                auth_option["auth_type"] = "password"
                auth_option["enforce_password_change"] = bool(
                    params["enforce_password_change"]
                )
            elif params.get("auth_type") == "automation" and _exists("password"):
                auth_option["secret"] = params["password"]
                auth_option["auth_type"] = "automation"
            else:
                log("Incomplete auth_type/password/secret combination.")
                return
            attributes["auth_option"] = auth_option

        if _exists("idle_timeout_option"):
            idle_timeout = {}
            idle_timeout["idle_timeout_option"] = params["idle_timeout_option"]
            if params["idle_timeout_option"] == "individual":
                if "idle_timeout_duration" in params:
                    idle_timeout["idle_timeout_duration"] = params[
                        "idle_timeout_duration"
                    ]
                else:
                    idle_timeout["idle_timeout_duration"] = 3600
            attributes["idle_timeout"] = idle_timeout

        if _exists("email"):
            contact_options = {}
            contact_options["email"] = params["email"]
            if "fallback_contact" in params:
                contact_options["fallback_contact"] = params["fallback_contact"]
            attributes["contact_options"] = contact_options

        if _exists("disable_notifications"):
            disable_notifications = {}
            try:
                disable_notifications = json.loads(params["disable_notifications"])
            except json.decoder.JSONDecodeError:
                log("json.decoder.JSONDecodeError while parsing disable_notifications.")
                return
            attributes["disable_notifications"] = disable_notifications

        if _exists("roles"):
            attributes["roles"] = params["roles"]

        if _exists("contactgroups"):
            attributes["contactgroups"] = params["contactgroups"]

        if _exists("authorized_sites"):
            attributes["authorized_sites"] = params["authorized_sites"]

        return cls(params["name"], state=params["state"], attributes=attributes)

    def satisfies(self, other_instance):
        for key, value in other_instance.attributes.items():
            if key in ["auth_option", "password"]:
                continue
            if key in self.attributes and value != self.attributes[key]:
                return False

        return True


def get_current_user_state(module, api_params):
    extensions = {}
    etag = ""
    current_state = ""

    api_endpoint = "/objects/user_config/" + module.params.get("name")
    url = api_params["base_url"] + api_endpoint

    response, info = fetch_url(
        module, url, data=None, headers=api_params["headers"], method="GET"
    )

    if info["status"] == 200:
        body = json.loads(response.read())
        current_state = "present"
        etag = info.get("etag", "")
        extensions = body.get("extensions", {})

    elif info["status"] == 404:
        current_state = "absent"

    else:
        exit_failed(
            module,
            "[get_current_user_state] Error calling API. HTTP code %d. Details: %s. Body: %s"
            % (info["status"], info["body"], body),
        )

    return extensions, current_state, etag


def set_user_attributes(module, desired_user, api_params):
    api_endpoint = "/objects/user_config/" + desired_user.username
    url = api_params["base_url"] + api_endpoint
    desired_attributes = desired_user.attributes
    del desired_attributes["username"]  # Not needed as a param, as it's part of the URI

    response, info = fetch_url(
        module,
        url,
        module.jsonify(desired_attributes),
        headers=api_params["headers"],
        method="PUT",
    )

    if info["status"] != 200:
        exit_failed(
            module,
            "[set_user_attributes] Error calling API. HTTP code %d. Details: %s, "
            % (info["status"], info["body"]),
        )


def create_user(module, desired_user, api_params):
    api_endpoint = "/domain-types/user_config/collections/all"
    url = api_params["base_url"] + api_endpoint
    desired_attributes = desired_user.attributes

    if desired_attributes["fullname"] is None or "fullname" not in desired_attributes:
        desired_attributes["fullname"] = desired_attributes["username"]

    response, info = fetch_url(
        module,
        url,
        module.jsonify(desired_attributes),
        headers=api_params["headers"],
        method="POST",
    )

    if info["status"] != 200:
        exit_failed(
            module,
            "[create_user] Error calling API. HTTP code %d. Details: %s, "
            % (info["status"], info["body"]),
        )


def delete_user(module, api_params):
    api_endpoint = "/objects/user_config/" + module.params.get("name")
    url = api_params["base_url"] + api_endpoint

    response, info = fetch_url(
        module, url, data=None, headers=api_params["headers"], method="DELETE"
    )

    if info["status"] != 204:
        exit_failed(
            module,
            "[delete_user] Error calling API. HTTP code %d. Details: %s, "
            % (info["status"], info["body"]),
        )


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
    api_params = {}
    api_params["headers"] = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer %s %s"
        % (
            module.params.pop("automation_user", ""),
            module.params.pop("automation_secret", ""),
        ),
    }

    api_params["base_url"] = "%s/%s/check_mk/api/1.0" % (
        module.params.pop("server_url", ""),
        module.params.pop("site", ""),
    )

    # Determine desired state and attributes
    desired_user = User.from_module(module.params)
    log("desired_user: %s" % str(desired_user))
    desired_state = desired_user.state

    current_user = User.from_api_response(module, api_params)
    current_state = current_user.state
    log("current_user: %s" % str(current_user))

    # Handle the user accordingly to above findings and desired state
    if desired_state in ["present", "reset_password"] and current_state == "present":
        api_params["headers"]["If-Match"] = current_user.etag

        if (
            not current_user.satisfies(desired_user)
            or desired_state == "reset_password"
        ):
            set_user_attributes(module, desired_user, api_params)
            exit_changed(module, "User attributes changed.")
        else:
            exit_ok(module, "User already present. All explicit attributes as desired.")

    elif desired_state == "present" and current_state == "absent":
        create_user(module, desired_user, api_params)
        exit_changed(module, "User created.")

    elif desired_state == "absent" and current_state == "absent":
        exit_ok(module, "User already absent.")

    elif desired_state == "absent" and current_state == "present":
        delete_user(module, api_params)
        exit_changed(module, "User deleted.")

    else:
        exit_failed(module, "[run_module] Unknown error")


def main():
    run_module()


if __name__ == "__main__":
    main()

#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2022, Robin Gierse <robin.gierse@tribe29.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
import copy

__metaclass__ = type

DOCUMENTATION = r"""
---
module: cmk_user

short_description: Manage users in Checkmk.

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "0.0.1"

description:
- Create and delete users within Checkmk.

extends_documentation_fragment: [tribe29.checkmk.common]

options:
    username:
        description: The user you want to manage.
        required: true
        type: str
    fullname:
        description: The alias or full name of the user.
        type: str
    password:
        description: The password or secret for login.
        type: str
        default: /
    enforce_password_change:
        description: If set to true, the user will be forced to change his/her password at the next login.
        type: bool
        default: false
    auth_type:
        description: The authentication type.
        type: str
        default: password
        choices: [password, secret]
    disable_login:
        description: The user can be blocked from login but will remain part of the site. The disabling does not affect notification and alerts.
        type: bool
        default: false
    email:
        description: The mail address of the user. Required if the user is a monitoring contact and receives notifications via mail.
        type: str
    fallback_contact:
        description: In case none of your notification rules handles a certain event a notification will be sent to the specified email.
        type: bool
        default: false
    pager_address:
        description: The pager address.
        type: str
    idle_timeout_duration:
        description: The duration in seconds of the individual idle timeout if individual is selected as idle timeout option.
        type: str
    idle_timeout_option:
        description: Specify if the idle timeout should use the global configuration, be disabled or use an individual duration
        type: str
        default: disable
        choices: [global, disable, individual]
    roles:
        description: The list of assigned roles to the user.
        type: raw
        default: {user}
    authorized_sites:
        description: The names of the sites the user is authorized to handle.
        type: raw
        default: {}
    contactgroups:
        description: Assign the user to one or multiple contact groups. If no contact group is specified then no monitoring contact will be created for the user.
        type: raw
        default: {all}
    disable_notifications:
        description: Option if all notifications should be temporarily disabled.
        type: bool
        default: false
    language:
        description: Configure the language to be used by the user in the user interface. Omitting this will configure the default language.
        type: str
        default: default
        choices: [default, en, de, ro]

author:
    - Robin Gierse (@robin-tribe29)
    - Lars Getwan (@lgetwan)
"""

EXAMPLES = r"""
# Create a user.
- name: "Create a user."
  tribe29.checkmk.user:
    server_url: "http://localhost/"
    site: "local"
    automation_user: "automation"
    automation_secret: "$SECRET"
    user_name: "my_user"
    folder: "/"
    state: "present"

# Create a user with IP.
- name: "Create a user with IP address."
  tribe29.checkmk.user:
    server_url: "http://localhost/"
    site: "local"
    automation_user: "automation"
    automation_secret: "$SECRET"
    user_name: "my_user"
    attributes:
      alias: "My user"
      ip_address: "x.x.x.x"
    folder: "/"
    state: "present"

# Create a user which is monitored on a distinct site.
- name: "Create a user which is monitored on a distinct site."
  tribe29.checkmk.user:
    server_url: "http://localhost/"
    site: "local"
    automation_user: "automation"
    automation_secret: "$SECRET"
    user_name: "my_user"
    attributes:
      site: "NAME_OF_DISTRIBUTED_USER"
    folder: "/"
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

import json
import ast
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url


def exit_failed(module, msg):
    result = {"msg": "%s, log: %s" % (msg, " § ".join(LOG)), "changed": False, "failed": True}
    module.fail_json(**result)


def exit_changed(module, msg):
    result = {"msg": "%s, log: %s" % (msg, " § ".join(LOG)), "changed": True, "failed": False}
    module.exit_json(**result)


def exit_ok(module, msg):
    result = {"msg": msg, "changed": False, "failed": False}
    module.exit_json(**result)


def log(msg):
    LOG.append(msg)


class UserAttributes():

    default_attributes = {
        "disable_login": False,
        "contact_options": {
            "email": "",
            "fallback_contact": False
        },
        "idle_timeout": {
            "option": "global"
        },
        "roles": [
            "user"
        ],
        "contactgroups": [],
        "pager_address": "",
        "disable_notifications": {},
        "enforce_password_change": False,
        ### Only available in >2.1.0:
        # "interface_options": {
        #     "interface_theme": "default",
        #     "sidebar_position": "right",
        #     "navigation_bar_icons": "hide",
        #     "mega_menu_icons": "topic",
        #     "show_mode": "default"
        # }
    }


    def __init__(self, attributes=None):
        if attributes is None:
            self.attributes = self.default_attributes
        else:
            self.attributes = attributes


    @classmethod
    def from_api_response(cls, api_attributes, username):
        attributes = copy.deepcopy(api_attributes)
        attributes["name"] = username

        return cls(attributes)


    @classmethod
    def from_module(cls, params):

        attributes = cls.default_attributes
        attributes["name"] = params["username"]

        if "fullname" in params:
            attributes["fullname"] = params["fullname"]
        if "disable_login" in params:
            attributes["disable_login"] = params["disable_login"] == "True"
        if "pager_address" in params:
            attributes["pager_address"] = params["pager_address"]
        if "language" in params and params["language"] != "default":
            attributes["language"] = params["language"]

        if "authtype" in params or "password" in params or "secret" in params:
            auth_option = {}
            if params["auth_type"] == "password" and "password" in params:
                auth_option["password"] = params["password"]
                auth_option["auth_type"] = "password"
                auth_option["enforce_password_change"] = params["enforce_password_change"] == "True"
            elif params["authtype"] == "secret" and "secret" in params:
                auth_option["secret"] = params["secret"]
                auth_option["auth_type"] = "secret"
            else:
                log("Incomplete auth_type/password/secret combination.")
                return
            attributes["auth_option"] = auth_option

        if "idle_timeout_option" in params:
            idle_timeout = {}
            idle_timeout["idle_timeout_option"] = params["idle_timeout_option"]
            if params["idle_timeout_option"] == "individual":
                if "idle_timeout_duration" in params:
                    idle_timeout["idle_timeout_duration"] = params["idle_timeout_duration"]
                else:
                    idle_timeout["idle_timeout_duration"] = 3600
            attributes["idle_timeout"] = idle_timeout

        if "email" in params:
            contact_options = {}
            contact_options["email"] = params["email"]
            if "fallback_contact" in params:
                contact_options["fallback_contact"] = params["fallback_contact"] == "True"
            attributes["contact_options"] = contact_options

        if "disable_notifications" in params and params["disable_notifications"] is not None:
            disable_notifications = {}
            try:
                disable_notifications = json.loads(params["disable_notifications"])
            except json.decoder.JSONDecodeError:
                log("json.decoder.JSONDecodeError while parsing disable_notifications.")
                return
            attributes["disable_notifications"] = disable_notifications

        if "roles" in params:
            #roles = []
            #try:
            #    roles = params["roles"]
            #except json.decoder.JSONDecodeError:
            #    log("json.decoder.JSONDecodeError while parsing roles.")
            #    return
            attributes["roles"] = params["roles"]

        if "contactgroups" in params:
            #contactgroups = []
            #try:
            #    contactgroups = json.loads(params["contactgroups"])
            #except json.decoder.JSONDecodeError:
            #    log("json.decoder.JSONDecodeError while parsing contactgroups.")
            #    return
            attributes["contactgroups"] = params["contactgroups"]


        if "authorized_sites" in params:
            #authorized_sites = []
            #try:
            #    authorized_sites = json.loads(params["authorized_sites"])
            #except json.decoder.JSONDecodeError:
            #    log("json.decoder.JSONDecodeError while parsing authorized_sites.")
            #    return
            attributes["authorized_sites"] = params["authorized_sites"]

        return cls(attributes)


    def is_equal_with(self, other_instance):
        return self.attributes != other_instance.attributes


def get_current_user_state(module, base_url, headers):
    extensions = {}
    etag = ""

    api_endpoint = "/objects/user_config/" + module.params.get("username")
    url = base_url + api_endpoint

    response, info = fetch_url(module, url, data=None, headers=headers, method="GET")

    if info["status"] == 200:
        body = json.loads(response.read())
        current_state = "present"
        etag = info.get("etag", "")
        extensions = body.get("extensions", {})
        username = body.get("title", "")

    elif info["status"] == 404:
        current_state = "absent"

    else:
        exit_failed(
            module,
            "Error calling API. HTTP code %d. Details: %s. Body: %s"
            % (info["status"], info["body"], body),
        )

    return extensions, username, current_state, etag


def _normalize_attributes(user_attributes):
    # Set the defaults
    default_attributes = {
        "auth_type": "password",
        "password": "",
        "disable_login": "False",
        "email": "",
        "fallback_contact": "False",
        "pager_address": "",
        "idle_timeout_duration": "3600",
        "idle_timeout_option": "global",
        "roles": ["user"],
        "authorized_sites": [],
        "contactgroups": ["all"],
        "disable_notifications": {},
    }

    special_treatment = [
        "idle_timeout_option",
        "idle_timeout_duration",
        "auth_type",
        "password",
        "email",
        "fallback_contact",
    ]

    explicit_attributes = {}
    log(str(user_attributes.items()))
    for k, v in user_attributes.items():
        log("processing %s (%s)" % (k,v))
        if k not in special_treatment:
            if v is None or v == "" or v == "None" or (k == "language" and v == "default"):
                log("To be filled")
                if k in default_attributes:
                    log("Fill with default %s" % default_attributes[k])
                    explicit_attributes[k] = default_attributes[k]
                    log("Filled with default %s" % explicit_attributes[k])
            else:
                log("use what the user provided: %s" % v)
                explicit_attributes[k] = v

    # The API expects "idle_timeout", "auth_option" and "contact options" in a slightly different structure, but we
    # want the Ansible module to be easier to use
    if "idle_timeout_option" in user_attributes or "idle_timeout_duration" in user_attributes:
        log("processing idle_timeout: ")
        idle_timeout = {}
        for key in ["option", "duration"]:
            long_key = "idle_timeout_%s" % key
            if long_key in user_attributes and user_attributes[long_key] is not None and user_attributes[long_key] != "":
                idle_timeout[key] = user_attributes[long_key]
            else:
                idle_timeout[key] = default_attributes[long_key]
        log(str(idle_timeout))
        explicit_attributes["idle_timeout"] = idle_timeout

    if "auth_type" in user_attributes:
        log("processing auth_option: ")
        auth_option = {
            "auth_type": user_attributes.get("auth_type", default_attributes["auth_type"]),
        }
        if user_attributes["auth_type"] == "automation":
            auth_option["secret"] = user_attributes.get("password", default_attributes["password"])
        else:
            auth_option["password"] = user_attributes.get("password", default_attributes["password"])
        log(str(auth_option))
        explicit_attributes["auth_option"] = auth_option

    if "email" in user_attributes or "fallback_contact" in user_attributes:
        log("processing contact_options: ")
        contact_options = {}
        for key in ["email", "fallback_contact"]:
            if key in user_attributes and user_attributes[key] is not None and user_attributes[key] != "":
                contact_options[key] = user_attributes[key]
            else:
                contact_options[key] = default_attributes[key]
        log(str(contact_options))
        explicit_attributes["contact_options"] = contact_options

    log("explicit attributes: ")
    log(str(explicit_attributes))

    return explicit_attributes

def set_user_attributes(module, user_attributes, base_url, headers):
    api_endpoint = "/objects/user_config/" + module.params.get("username")
    url = base_url + api_endpoint

    #explicit_attributes = _normalize_attributes(user_attributes)
    attributes = user_attributes.attributes

    # print("#####################")
    # print(module.jsonify(user_attributes))
    response, info = fetch_url(
        module, url, module.jsonify(attributes), headers=headers, method="PUT"
    )

    if info["status"] != 200:
        exit_failed(
            module,
            "Error calling API. HTTP code %d. Details: %s, "
            % (info["status"], info["body"]),
        )


def create_user(module, user_attributes, base_url, headers):
    api_endpoint = "/domain-types/user_config/collections/all"
    url = base_url + api_endpoint

    if user_attributes["fullname"] is None or "fullname" not in user_attributes:
        user_attributes["fullname"] = user_attributes["username"]

    #explicit_attributes = _normalize_attributes(user_attributes)
    attributes = user_attributes.attributes

    response, info = fetch_url(
        module, url, module.jsonify(attributes), headers=headers, method="POST"
    )

    if info["status"] != 200:
        exit_failed(
            module,
            "Error calling API. HTTP code %d. Details: %s, "
            % (info["status"], info["body"]),
        )


def delete_user(module, base_url, headers):
    api_endpoint = "/objects/user_config/" + module.params.get("username")
    url = base_url + api_endpoint

    response, info = fetch_url(module, url, data=None, headers=headers, method="DELETE")

    if info["status"] != 204:
        exit_failed(
            module,
            "Error calling API. HTTP code %d. Details: %s, "
            % (info["status"], info["body"]),
        )


def run_module():

    # define available arguments/parameters a user can pass to the module
    # TODO: Wenn Parameter nicht gesetzt ist, dann soll
    # - bei einem "create" ein Default verwendet werden
    # - bei einem "change" die gesetzten Werte nicht verändert werden.
    module_args = dict(
        server_url=dict(type="str", required=True),
        site=dict(type="str", required=True),
        automation_user=dict(type="str", required=True),
        automation_secret=dict(type="str", required=True, no_log=True),
        username=dict(required=True, type=str),
        fullname=dict(type="str"),
        password=dict(type="str"),
        enforce_password_change=dict(type="bool"),
        secret=dict(type="str"),
        auth_type=dict(type="str", choices=["password", "secret"]),
        disable_login=dict(type="bool"),
        email=dict(type="str"),
        fallback_contact=dict(type="bool"),
        pager_address=dict(type="str"),
        idle_timeout_duration=dict(type="str"),
        idle_timeout_option=dict(type="str", choices=["global", "disable", "individual"]),
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

    # Use the parameters to initialize some common variables
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer %s %s"
        % (
            module.params.pop("automation_user", ""),
            module.params.pop("automation_secret", ""),
        ),
    }

    base_url = "%s/%s/check_mk/api/1.0" % (
        module.params.pop("server_url", ""),
        module.params.pop("site", ""),
    )

    # Determine desired state and attributes
    state = module.params.pop("state")

    new_attributes = UserAttributes.from_module(module.params)

    ## Clone params and remove keys with empty values
    #user_attributes = module.params.copy()
    #for k, v in module.params.items():
    #    # if v is None or v == "" or (k == "language" and v == "default"):
    #    if k == "language" and v == "default":
    #        del user_attributes[k]

    ## Convert dicts to list wherewver needed
    #if user_attributes["roles"] == {}:
    #    user_attributes["roles"] = []

    #if user_attributes["contactgroups"] == {}:
    #    user_attributes["contactgroups"] = []

    #if user_attributes["authorized_sites"] == {}:
    #    user_attributes["authorized_sites"] = []

    # Determine the current state of this particular user
    _attributes, _username, current_state, etag = get_current_user_state(
        module, base_url, headers
    )

    current_attributes = UserAttributes.from_api_response(_attributes, _username)

    # Handle the user accordingly to above findings and desired state
    if state in ["present", "reset_password"] and current_state == "present":
        headers["If-Match"] = etag

        if not new_attributes.is_equal_with(current_attributes):
            set_user_attributes(module, new_attributes, base_url, headers)
            exit_changed(module, "User attributes changed.")
        else:
            exit_ok(module, "User already present. All explicit attributes as desired.")

        #if state != "reset_password":
        #    del user_attributes["auth_type"]

        #del user_attributes["username"]
        ## TODO: normalize user attributes and then do a deep compare before deciding what to change.
        #if user_attributes != {} and current_user_attributes != user_attributes:
        #    log("current_user_attributes")
        #    log(str(current_user_attributes))
        #    log("user_attributes")
        #    log(str(user_attributes))
        #    set_user_attributes(module, user_attributes, base_url, headers)
        #    log("User attributes changed.")

        #if len(msg_tokens) >= 1:
        #    exit_changed(module, " ".join(msg_tokens))
        #else:
        #    exit_ok(module, "User already present. All explicit attributes as desired.")

    elif state == "present" and current_state == "absent":
        create_user(module, new_attributes, base_url, headers)
        exit_changed(module, "User created.")

    elif state == "absent" and current_state == "absent":
        exit_ok(module, "User already absent.")

    elif state == "absent" and current_state == "present":
        delete_user(module, base_url, headers)
        exit_changed(module, "User deleted.")

    else:
        exit_failed(module, "Unknown error")


def main():
    run_module()



if __name__ == "__main__":
    main()

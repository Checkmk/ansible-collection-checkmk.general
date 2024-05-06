#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2022, diademiemi <emilia@diademiemi.me> & Robin Gierse <robin.gierse@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: rule

short_description: Manage rules in Checkmk.

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "0.10.0"

description:
    - Manage rules within Checkmk. Importing rules from the output of the Checkmk API.
    - Make sure these were exported with Checkmk 2.1.0p10 or above. See https://checkmk.com/werk/14670 for more information.

extends_documentation_fragment: [checkmk.general.common]

options:
    rule:
        description: Definition of the rule as returned by the Checkmk API.
        required: true
        type: dict
        suboptions:
            rule_id:
                description:
                    - If provided, update/delete an existing rule.
                    - If omitted, we try to find an equal rule based on C(properties),
                      C(conditions), C(folder) and C(value_raw).
                    - Please mind the additional notes below.
                type: str
            location:
                description:
                    - Location of the rule within a folder.
                    - By default rules are created at the bottom of the "/" folder.
                type: dict
                suboptions:
                    position:
                        description:
                            - Position of the rule in the folder.
                            - Has no effect when I(state=absent).
                            - For new rule C(any) wil be equivalent to C(bottom)
                        type: str
                        choices:
                            - "top"
                            - "bottom"
                            - "any"
                            - "before"
                            - "after"
                        default: "any"
                    neighbour:
                        description:
                            - Put the rule C(before) or C(after) this rule_id.
                            - Required when I(position) is C(before) or C(after).
                            - Mutually exclusive with I(folder).
                        type: str
                        aliases: [rule_id]
                    folder:
                        description:
                            - Folder of the rule.
                            - Required when I(position) is C(top), C(bottom), or (any).
                            - Required when I(state=absent).
                            - Mutually exclusive with I(neighbour).
                        default: "/"
                        type: str
            conditions:
                description: Conditions of the rule.
                type: dict
            properties:
                description: Properties of the rule.
                type: dict
            value_raw:
                description:
                    - Rule values as exported from the web interface.
                    - Required when I(state) is C(present).
                type: str
    ruleset:
        description: Name of the ruleset to manage.
        required: true
        type: str
    state:
        description: State of the rule.
        choices: [present, absent]
        default: present
        type: str
notes:
    - If rule_id is omitted, due to the internal processing of the C(value_raw), finding the
      matching rule is not reliable, when C(rule_id) is omitted. This sometimes leads to the
      module not being idempotent or to rules being created over and over again.
    - If rule_id is provided, for the same reason, it might happen, that tasks changing a rule
      again and again, even if it already meets the expectations.

author:
    - Lars Getwan (@lgetwan)
    - diademiemi (@diademiemi)
    - Geoffroy Stévenne (@geof77)
    - Michael Sekana (@msekania)
"""

EXAMPLES = r"""
# Create a rule in checkgroup_parameters:memory_percentage_used
# at the top of the main folder.
- name: "Create a rule in checkgroup_parameters:memory_percentage_used."
  checkmk.general.rule:
    server_url: "http://my_server/"
    site: "my_site"
    automation_user: "my_user"
    automation_secret: "my_secret"
    ruleset: "checkgroup_parameters:memory_percentage_used"
    rule:
      conditions: {
        "host_labels": [],
        "host_name": {
          "match_on": [
            "test1.tld"
          ],
          "operator": "one_of"
        },
        "host_tags": [],
        "service_labels": []
      }
      properties: {
        "comment": "Ansible managed",
        "description": "Allow higher memory usage",
        "disabled": false,
        "documentation_url": "https://github.com/Checkmk/ansible-collection-checkmk.general/blob/main/plugins/modules/rule.py"
      }
      value_raw: "{'levels': (80.0, 90.0)}"
      location:
        folder: "/"
        position: "top"
    state: "present"
  register: response

- name: Show the ID of the new rule
  ansible.builtin.debug:
    msg: "RULE ID : {{ response.content.id }}"

# Create another rule with the new label conditions (> 2.3.0)
# in checkgroup_parameters:memory_percentage_used and put it after the rule created above.
- name: "Create a rule in checkgroup_parameters:memory_percentage_used."
  checkmk.general.rule:
    server_url: "http://my_server/"
    site: "my_site"
    automation_user: "my_user"
    automation_secret: "my_secret"
    ruleset: "checkgroup_parameters:memory_percentage_used"
    rule:
      conditions: {
        "host_label_groups": [
            {
                operator: "and",
                label_group: [
                    {
                        operator: "and",
                        label: "cmk/site:beta"
                    },
                    {
                        operator: "or",
                        label: "cmk/os_family:linux"
                    }
                ],
            },
            {
                operator: "or",
                label_group: [
                    {
                        operator: "and",
                        label: "cmk/site:alpha"
                    },
                    {
                        operator: "or",
                        label: "cmk/os_family:windows"
                    }
                ],
            },
        ],
        "host_name": {
          "match_on": [
            "test2.tld"
          ],
          "operator": "one_of"
        },
        "host_tags": [],
        "service_labels": []
      }
      properties: {
        "comment": "Ansible managed",
        "description": "Allow even higher memory usage",
        "disabled": false,
        "documentation_url": "https://github.com/Checkmk/ansible-collection-checkmk.general/blob/main/plugins/modules/rule.py"
      }
      value_raw: "{'levels': (85.0, 99.0)}"
      location:
        position: "after"
        neighbour: "{{ response.content.id }}"
    state: "present"

# Delete the first rule.
- name: "Delete a rule."
  checkmk.general.rule:
    server_url: "http://my_server/"
    site: "my_site"
    automation_user: "my_user"
    automation_secret: "my_secret"
    ruleset: "checkgroup_parameters:memory_percentage_used"
    rule:
      rule_id: "{{ response.content.id }}"
    state: "absent"

# Create a rule rule matching a host label
- name: "Create a rule matching a label."
  checkmk.general.rule:
    server_url: "http://my_server/"
    site: "my_site"
    automation_user: "my_user"
    automation_secret: "my_secret"
    ruleset: "checkgroup_parameters:memory_percentage_used"
    rule:
      conditions: {
        "host_labels": [
          {
            "key": "cmk/check_mk_server",
            "operator": "is",
            "value": "yes"
          }
        ],
        "host_name": {},
        "host_tags": [],
        "service_labels": []
      }
      properties: {
        "comment": "Ansible managed",
        "description": "Allow higher memory usage",
        "disabled": false,
        "documentation_url": "https://github.com/Checkmk/ansible-collection-checkmk.general/blob/main/plugins/modules/rule.py"
      }
      value_raw: "{'levels': (80.0, 90.0)}"
      location:
        folder: "/"
        position: "top"
    state: "present"

# Delete all rules in a ruleset that match a certain comment.
- name: "Delete all rules in a ruleset that match a certain comment."
  checkmk.general.rule:
    server_url: "http://my_server/"
    site: "my_site"
    automation_user: "my_user"
    automation_secret: "my_secret"
    ruleset: "checkgroup_parameters:memory_percentage_used"
    rule:
      rule_id: "{{ item.id }}"
    loop: "{{
             lookup('checkmk.general.rules',
               ruleset=outer_item.ruleset,
               comment_regex='Ansible managed',
               server_url=server_url,
               site=site,
               automation_user=automation_user,
               automation_secret=automation_secret,
               validate_certs=False
               )
           }}"
    loop_control:
      label: "{{ item.id }}"
"""

RETURN = r"""
msg:
    description: The output message that the module generates. Contains the API status details in case of an error.
    type: str
    returned: always
    sample: 'Rule created.'
http_code:
    description: The HTTP code the Checkmk API returns.
    type: int
    returned: always
    sample: '200'
etag:
    description: The etag of the rule.
    type: str
    returned: when the rule is created or when it already exists
    sample: '"ad55730d5488e55e07c58a3da9759fba8cd0b009"'
content:
    description: The complete created/changed rule
    returned: when the rule is created or when it already exists
    type: dict
    contains:
        id:
            description: The ID of the rule.
            type: str
            returned: when the rule is created or when it already exists
            sample: '1f97bc43-52dc-4f1a-ab7b-c2e9553958ab'
        extensions:
            description: The attributes of the rule
            type: dict
            returned: when the rule is created or when it already exists
            contains:
                conditions:
                    description: The contitions of the rule.
                    type: str
                    returned: when the rule is created or when it already exists
                folder:
                    description: The folder of the rule.
                    type: str
                    returned: when the rule is created or when it already exists
                folder_index:
                    description: The index of the rule inside the folder.
                    type: str
                    returned: when the rule is created or when it already exists
                properties:
                    description: The properties of the rule.
                    type: str
                    returned: when the rule is created or when it already exists
                ruleset:
                    description: The ruleset of the rule.
                    type: str
                    returned: when the rule is created or when it already exists
                value_raw:
                    description: The actual value of the rule
                    type: str
                    returned: when the rule is created or when it already exists
"""

import json

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.validation import safe_eval
from ansible_collections.checkmk.general.plugins.module_utils.api import CheckmkAPI
from ansible_collections.checkmk.general.plugins.module_utils.types import RESULT
from ansible_collections.checkmk.general.plugins.module_utils.version import (
    CheckmkVersion,
)

DESIRED_RULE_KEYS = (
    "location",
    "conditions",
    "properties",
    "value_raw",
)

DESIRED_DEFAULTS = {
    "pre_230": {
        "properties": {
            "disabled": False,
        },
        "conditions": {
            "host_tags": [],
            "host_labels": [],
            "service_labels": [],
        },
    },
    "230_or_newer": {
        "properties": {
            "disabled": False,
        },
        "conditions": {
            "host_tags": [],
            "host_label_groups": [],
            "service_label_groups": [],
        },
    },
}

IGNORE_PROPERTIES_DEFAULTS = [
    "description",
    "comment",
]

CURRENT_RULE_KEYS = (
    "folder",
    "ruleset",
    "conditions",
    "properties",
    "value_raw",
)

POSITION_MAPPING = {
    "top": "top_of_folder",
    "bottom": "bottom_of_folder",
    "any": "bottom_of_folder",
    "after": "after_specific_rule",
    "before": "before_specific_rule",
}


class RuleHTTPCodes:
    # http_code: (changed, failed, "Message")
    get = {
        200: (False, False, "Rule found, nothing changed"),
        404: (False, False, "Rule not found"),
    }

    list_rules = {
        200: (False, False, "Ruleset found, nothing changed"),
        404: (False, False, "Ruleset not found"),
    }

    create = {200: (True, False, "Rule created")}
    move = {200: (True, False, "Rule moved")}
    edit = {200: (True, False, "Rule modified")}
    delete = {204: (True, False, "Rule deleted")}


class RuleEndpoints:
    default = "/objects/rule"
    create = "/domain-types/rule/collections/all"


# Get complete ruleset of current rule
class RuleLocation(CheckmkAPI):
    def __init__(self, module, folder, rule_id):
        super().__init__(module)
        self.module = module
        self.params = module.params

        self.folder = folder
        self.rule_id = rule_id

        self.ruleset = self.params.get("ruleset")

        self.rule_dict = self._get_ruleset(self.ruleset)
        self.folder_rule_list = [
            k for k, v in self.rule_dict.items() if v == self.folder
        ]
        self.folder_index = self.folder_rule_list.index(self.rule_id)
        self.folder_size = len(self.folder_rule_list)

    def _build_default_endpoint(self):
        return "%s/%s" % (
            RuleEndpoints.default,
            self.ruleset,
        )

    def _get_ruleset(self, ruleset):
        result = self._fetch(
            code_mapping=RuleHTTPCodes.list_rules,
            endpoint=RuleEndpoints.create + "?ruleset_name=" + self.ruleset,
            method="GET",
        )

        if result.http_code == 200:
            content = json.loads(result.content)
            return {
                r.get("id"): r.get("extensions", {}).get("folder")
                for r in content.get("value")
            }

        return {}

    def is_equal(self, desired_location):
        desired_folder = desired_location.get("folder")
        desired_position = desired_location.get("position")
        desired_neighbour = desired_location.get("neighbour")

        if desired_position in ["bottom", "top", "any"]:
            if desired_folder != self.folder:
                return False
            elif desired_position == "any":
                return True
            elif desired_position == "top" and self.folder_index == 0:
                return True
            elif (
                desired_position == "bottom"
                and self.folder_index == self.folder_size - 1
            ):
                return True
            else:
                return False

        if desired_position in ["before", "after"]:
            if desired_folder != self.folder:
                return False
            elif (
                desired_position == "before"
                and self.folder_index < self.folder_size - 1
                and self.folder_rule_list[self.folder_index + 1] == desired_neighbour
            ):
                return True
            elif (
                desired_position == "after"
                and self.folder_index > 0
                and self.folder_rule_list[self.folder_index - 1] == desired_neighbour
            ):
                return True
            else:
                return False

        # This should never happen ;-)
        return False


class RuleAPI(CheckmkAPI):
    def __init__(self, module):
        super().__init__(module)

        self.module = module
        self.params = self.module.params
        self.rule_id = self.params.get("rule").get("rule_id")
        self.is_new_rule = self.rule_id is None

        self.desired = self._clean_desired(self.params)

        self._changed_items = []
        self.current = None
        self.etag = ""

        self._verify_parameters()

        if not self.rule_id:
            # If no rule_id is provided, we still check if rule exists.
            self.rule_id = self._get_rule_id(self.desired)

        if self.rule_id:
            # Get the current rule from the API and set some parameters
            (self.current, self.state) = self._get_current()
            if self.state == "present":
                self._changed_items = self._detect_changes()

    def _verify_parameters(self):
        self._verify_location()
        self._verify_conditions()

    def _verify_location(self):
        # when neighbour is specified, verify that it exists otherwise give warning
        neighbour_id = self.params.get("rule", {}).get("location", {}).get("neighbour")

        if neighbour_id:
            (neighbour, state) = self._get_rule_by_id(neighbour_id)

            if state == "absent":
                self.module.warn(
                    "Specified neighbour: '%s' does not exist" % neighbour_id
                )
            else:
                self.desired["rule"]["location"]["folder"] = neighbour.get(
                    "rule", {}
                ).get("folder")

    def _verify_conditions(self):
        # The combined host/service labels are only available in > 2.3.0
        conditions = self.params.get("rule", {}).get("conditions")
        if (
            conditions
            and (
                "host_label_groups" in conditions
                or "service_label_groups" in conditions
            )
            and self.getversion() < CheckmkVersion("2.3.0")
        ):
            self.module.fail_json(
                msg="ERROR: label groups are only available from Checkmk 2.3.0 on."
            )

    def rule_id_found(self):
        return self.current is not None

    def _clean_desired(self, params):
        desired = {}
        desired["ruleset"] = params.get("ruleset")
        desired["rule"] = {}
        tmp_params_rule = params.get("rule", {})

        for key in DESIRED_RULE_KEYS:
            if tmp_params_rule.get(key):
                desired["rule"][key] = tmp_params_rule.get(key)

        # Set defaults unless we're editing an existing rule
        if self.getversion() < CheckmkVersion("2.3.0"):
            defaults = DESIRED_DEFAULTS["pre_230"]
        else:
            defaults = DESIRED_DEFAULTS["230_or_newer"]

        for what, def_vals in defaults.items():
            for key, value in def_vals.items():
                if not desired["rule"].get(what):
                    desired["rule"][what] = {}

                if not desired["rule"].get(what).get(key):
                    desired["rule"][what][key] = value

        return desired

    def _raw_value_eval(self, state, data):
        value_raw = data.get("value_raw", "''")

        # This is an ugly hack that translates tuples into lists to have a better hit rate with
        # idempotency.
        # Once the internal handling of value_raw has improved, we will no longer need this.
        value_raw = value_raw.translate(str.maketrans("()", "[]"))

        (safe_value_raw, exc) = safe_eval(value_raw, include_exceptions=True)
        if exc is not None:
            self.module.fail_json(
                msg="ERROR: The %s value_raw has invalid format" % state
            )

        return safe_value_raw

    def _get_rules_in_ruleset(self, ruleset):
        result = self._fetch(
            code_mapping=RuleHTTPCodes.list_rules,
            endpoint=RuleEndpoints.create + "?ruleset_name=" + ruleset,
            method="GET",
        )

        if result.http_code == 200:
            content = json.loads(result.content)
            return content.get("value")

        return []

    def _get_rule_id(self, desired):
        desired_properties = desired["rule"].get("properties")

        if desired_properties.get("description", "") == "":
            desired_properties.pop("description", None)

        if desired_properties.get("comment", "") == "":
            desired_properties.pop("comment", None)

        for r in self._get_rules_in_ruleset(desired.get("ruleset")):
            if (
                r["extensions"]["folder"] == desired["rule"]["location"]["folder"]
                and r["extensions"]["conditions"] == desired["rule"]["conditions"]
                and r["extensions"]["properties"] == desired_properties
                and self._raw_value_eval("search", r["extensions"])
                == self._raw_value_eval("desired", desired["rule"])
            ):
                return r["id"]

        return None

    def _detect_changes(self):
        current = self.current["rule"].copy()
        desired = self.desired.get("rule").copy()
        changes = []

        if current.get("conditions", {}) != desired.get("conditions", {}):
            changes.append("conditions")

        if desired.get("properties"):
            if current.get("properties", {}) != desired.get("properties"):
                for elem in IGNORE_PROPERTIES_DEFAULTS:
                    if (
                        current.get("properties", {}).get(elem, "")
                        == desired.get("properties").get(elem, "")
                        and desired.get("properties").get(elem, "") == ""
                    ):
                        desired["properties"].pop(elem, None)

        if current.get("properties", {}) != desired.get("properties", {}):
            changes.append("properties")

        if self._raw_value_eval("current", current) != self._raw_value_eval(
            "desired", desired
        ):
            changes.append("raw_value")

        desired_location = desired.get("rule", {}).get("location")
        # desired_location = desired.get("location")
        if desired_location:
            current_location = RuleLocation(
                self.module, current.get("folder", "/"), self.rule_id
            )

            if not current_location.is_equal(desired_location):
                changes.append("location")

        return changes

    def _build_default_endpoint(self, rule_id=None):
        return "%s/%s" % (
            RuleEndpoints.default,
            # self.rule_id,
            self.rule_id if not rule_id else rule_id,
        )

    def _get_rule_by_id(self, rule_id):
        current = {}
        state = "absent"

        result = self._fetch(
            code_mapping=RuleHTTPCodes.get,
            endpoint=self._build_default_endpoint(rule_id),
            method="GET",
        )

        if result.http_code == 200:
            current["rule"] = {}
            state = "present"
            current["etag"] = result.etag

            content = json.loads(result.content)
            extensions = content["extensions"]

            current["rule"] = {
                key: value
                for key, value in extensions.items()
                if key in CURRENT_RULE_KEYS
            }

        return (current, state)

    def _get_current(self):
        return self._get_rule_by_id(self.rule_id)

    def _check_output(self, mode):
        return RESULT(
            http_code=0,
            msg="Running in check mode. Would have %s" % mode,
            content="",
            etag="",
            failed=False,
            changed=True,
        )

    def needs_update(self):
        return len(self._changed_items) > 0

    def _moving_needed(self):
        if "location" in self._changed_items:
            return True

        if self.is_new_rule:
            location = self.desired.get("rule").get("location")
            if location and not (
                # folder should be there
                location.get("folder", "/") == "/"
                # position should be there
                and location.get("position", "bottom") == "bottom"
            ):
                return True

        return False

    def _move_if_needed(self):
        if not self._moving_needed():
            return

        location = self.desired.get("rule").get("location")
        data = {"position": POSITION_MAPPING[location.get("position")]}
        #                                    what if fails!? better error message will be better

        # what if location nowhere?
        # position should be there
        pos = location.get("position", "bottom")
        if pos in ["top", "bottom", "any"]:
            # folder should be there
            data["folder"] = location.get("folder", "/")
        elif pos in ["before", "after"]:
            data["rule_id"] = location.get("neighbour")
        # else:
        #     # cannot happen

        if self.module.check_mode:
            return self._check_output("move")

        return self._fetch(
            code_mapping=RuleHTTPCodes.move,
            endpoint=self._build_default_endpoint() + "/actions/move/invoke",
            data=data,
            method="POST",
        )

    def _merge_results(self, results):
        return RESULT(
            http_code=list(results.values())[-1].http_code,
            msg=", ".join(
                [
                    "%s (%d)" % (results[k].msg, results[k].http_code)
                    for k in results.keys()
                ]
            ),
            content=list(results.values())[-1].content,
            etag=list(results.values())[-1].etag,
            failed=any(r.failed for r in list(results.values())),
            changed=any(r.changed for r in list(results.values())),
        )

    def create(self):
        # rule is there always (required true)
        data = self.desired.get("rule").copy()
        location = data.pop("location", {})
        data["ruleset"] = self.desired.get("ruleset")
        data["folder"] = location.get("folder", "/")

        if not data.get("value_raw"):
            self.module.fail_json(
                msg="ERROR: The parameter value_raw is mandatory when 'state is present'."
            )

        if self.module.check_mode:
            return self._check_output("create")

        create_result = self._fetch(
            code_mapping=RuleHTTPCodes.create,
            endpoint=RuleEndpoints.create,
            data=data,
            method="POST",
        )

        if create_result.failed:
            return create_result

        content = json.loads(create_result.content)
        self.rule_id = content.get("id")

        move_result = self._move_if_needed()
        if move_result:
            return self._merge_results({"created": create_result, "moved": move_result})
        else:
            return create_result

    def edit(self):
        # rule is there always (required true)
        data = self.desired.get("rule").copy()
        data.pop("location")
        self.headers["if-Match"] = self.etag

        if not data.get("value_raw"):
            self.module.fail_json(
                msg="ERROR: The parameter value_raw is mandatory when 'state is present'."
            )

        if self.module.check_mode:
            return self._check_output("edit")

        edit_result = self._fetch(
            code_mapping=RuleHTTPCodes.edit,
            endpoint=self._build_default_endpoint(),
            data=data,
            method="PUT",
        )

        edit_result = edit_result._replace(
            msg=edit_result.msg + ". Changed: %s" % ", ".join(self._changed_items)
        )

        if edit_result.failed:
            return edit_result

        move_result = self._move_if_needed()
        if move_result:
            return self._merge_results({"edited": edit_result, "moved": move_result})
        else:
            return edit_result

    def delete(self):
        if self.module.check_mode:
            return self._check_output("delete")

        result = self._fetch(
            code_mapping=RuleHTTPCodes.delete,
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
        ruleset=dict(type="str", required=True),
        rule=dict(
            type="dict",
            required=True,
            options=dict(
                rule_id=dict(type="str", default=None),
                conditions=dict(type="dict"),
                properties=dict(type="dict"),
                value_raw=dict(type="str"),
                location=dict(
                    type="dict",
                    options=dict(
                        position=dict(
                            type="str",
                            choices=["top", "bottom", "any", "before", "after"],
                            default="any",
                        ),
                        folder=dict(
                            type="str",
                            default="/",
                        ),
                        neighbour=dict(type="str", aliases=["rule_id"]),
                    ),
                    required_if=[
                        ("position", "top", ("folder",)),
                        ("position", "bottom", ("folder",)),
                        ("position", "any", ("folder",)),
                        ("position", "before", ("neighbour",)),
                        ("position", "after", ("neighbour",)),
                    ],
                    mutually_exclusive=[("folder", "neighbour")],
                    apply_defaults=True,
                ),
            ),
        ),
        state=dict(type="str", default="present", choices=["present", "absent"]),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    # Create an API object that contains the current and desired state
    current_rule = RuleAPI(module)

    result = RESULT(
        http_code=0,
        msg="",
        content="{}",
        etag="",
        failed=False,
        changed=False,
    )

    desired_state = module.params.get("state")
    rule_id = module.params.get("rule_id")

    if desired_state == "present":
        if current_rule.rule_id_found():
            # Update if needed
            if current_rule.needs_update():
                result = current_rule.edit()
            else:
                result = result._replace(
                    msg="Rule already exists with the desired parameters."
                )
        elif rule_id:
            # There is no rule with the given rule_id
            result = result._replace(
                msg="The provided rule_id was not found.",
                failed=True,
            )
        else:
            # Create new rule
            result = current_rule.create()
    elif desired_state == "absent":
        if current_rule.state == "present":
            # Delete existing rule
            result = current_rule.delete()
        elif current_rule.state == "absent":
            # Rule is already absent
            result = result._replace(msg="Rule already absent.")

    if result.content:
        result = result._replace(content=json.loads(result.content))
    result_as_dict = result._asdict()
    module.exit_json(**result_as_dict)


def main():
    run_module()


if __name__ == "__main__":
    main()

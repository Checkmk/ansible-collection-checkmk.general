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
                    - If provided, update/delete an existing rule
                    - If omitted, create a new rule
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
                        type: str
                        choices:
                            - "top"
                            - "bottom"
                            - "before"
                            - "after"
                        default: "bottom"
                    neighbour:
                        description:
                            - Put the rule C(before) or C(after) this rule_id.
                            - Required when I(position) is C(before) or C(after).
                            - Mutually exclusive with I(folder).
                        aliasses: rule_id
                        type: str
                    folder:
                        description:
                            - Folder of the rule.
                            - Required when I(position) is C(top) or C(bottom).
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
                description: Rule values as exported from the web interface.
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

author:
    - Lars Getwan (@lgetwan)
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
        "comment": "Warning at 80%\nCritical at 90%\n",
        "description": "Allow higher memory usage",
        "disabled": false,
        "documentation_url": "https://github.com/Checkmk/ansible-collection-checkmk.general/blob/main/plugins/modules/rules.py"
      }
      value_raw: "{'levels': (80.0, 90.0)}"
      location:
        folder: "/"
        position: "top"
    state: "present"
  register: response

- name: Show the ID of the new rule
  ansible.builtin.debug:
    msg: "RULE ID : {{ response.id }}"

# Create another rule in checkgroup_parameters:memory_percentage_used
# and put it after the rule created above.
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
            "test2.tld"
          ],
          "operator": "one_of"
        },
        "host_tags": [],
        "service_labels": []
      }
      properties: {
        "comment": "Warning at 85%\nCritical at 99%\n",
        "description": "Allow even higher memory usage",
        "disabled": false,
        "documentation_url": "https://github.com/Checkmk/ansible-collection-checkmk.general/blob/main/plugins/modules/rules.py"
      }
      value_raw: "{'levels': (85.0, 99.0)}"
      location:
        position: "after"
        rule_id: "{{ response.id }}"
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
        "comment": "Warning at 80%\nCritical at 90%\n",
        "description": "Allow higher memory usage",
        "disabled": false,
        "documentation_url": "https://github.com/Checkmk/ansible-collection-checkmk.general/blob/main/plugins/modules/rules.py"
      }
      value_raw: "{'levels': (80.0, 90.0)}"
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
        "comment": "Warning at 80%\nCritical at 90%\n",
        "description": "Allow higher memory usage",
        "disabled": false,
        "documentation_url": "https://github.com/Checkmk/ansible-collection-checkmk.general/blob/main/plugins/modules/rules.py"
      }
      value_raw: "{'levels': (80.0, 90.0)}"
      location:
        folder: "/"
        position: "top"
    state: "present"
"""

RETURN = r"""
msg:
    description: The output message that the module generates. Contains the API status details in case of an error.
    type: str
    returned: always
    sample: 'Rule created.'

id:
    description: The ID of the rule.
    type: str
    returned: when the rule is created or when it already exists
    sample: '1f97bc43-52dc-4f1a-ab7b-c2e9553958ab'
"""

import json

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.validation import safe_eval
from ansible_collections.checkmk.general.plugins.module_utils.api import CheckmkAPI
from ansible_collections.checkmk.general.plugins.module_utils.types import RESULT

DESIRED_RULE_KEYS = (
    "location",
    "conditions",
    "properties",
    "value_raw",
)

DESIRED_DEFAULTS = {
    "properties": {
        "description": "",
        "comment": "",
        "disabled": False,
    },
    "conditions": {
        "host_tags": [],
        "host_labels": [],
        "service_labels": [],
    },
}

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

        self.rule_list = self._get_ruleset(self.module.params.get("ruleset"))
        # self.module.warn("self.rule_list: %s" % str(self.rule_list))
        self.folder_rule_list = [
            k for k, v in self.rule_list.items() if v == self.folder
        ]
        # self.module.fail_json(msg="self.folder_rule_list: %s, self.rule_id: %s" % (str(self.folder_rule_list), self.rule_id))
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
            # self.module.fail_json("content: %s" % str(content))
            return {
                r.get("id"): r.get("extensions", {}).get("folder")
                for r in content.get("value")
            }

        return []

    def is_equal(self, desired_location):
        desired_folder = desired_location.get("folder")
        desired_position = desired_location.get("position")
        desired_neighbour = desired_location.get("neighbour")

        if desired_position in ["bottom", "top"]:
            if desired_folder != self.folder:
                return False
            elif desired_position == "top" and self.folder_index == 0:
                return True
            elif (
                desired_position == "bottom"
                and self.folder_index == self.folder_size - 1
            ):
                return True
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

        # This should never happen
        return False


class RuleAPI(CheckmkAPI):
    def __init__(self, module):
        super().__init__(module)

        self.module = module
        self.params = self.module.params
        self.rule_id = self.params.get("rule", {}).get("rule_id")
        self.is_new_rule = self.rule_id is None

        self.desired = self._clean_desired(self.params)

        self._changed_items = []
        self.current = None
        self.etag = ""

        # self.module.warn("self.rule_id: %s" % str(self.rule_id))
        if self.rule_id:
            # Get the current rule from the API and set some parameters
            self.current = self._get_current()
            self._changed_items = self._detect_changes()
        # self.module.warn("current: %s" % str(self.current))
        # self.module.warn("desired: %s" % str(self.desired))

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

        # Set defaults
        for what, defaults in DESIRED_DEFAULTS.items():
            for key, default in defaults.items():
                if not desired["rule"].get(what):
                    desired["rule"][what] = {}

                tmp_prop = desired["rule"].get(what, {})
                if not desired["rule"].get(what, {}).get(key):
                    desired["rule"][what][key] = default

        return desired

    def _raw_value_eval(self, state, data):
        value_raw = data.get("value_raw", "''")

        # This is an ugly hack that translates tuples into lists to have a better hit rate with
        # idempotency.
        # Once the internal handling of value_raw has improved, we will no loinger need this.
        value_raw = value_raw.translate(str.maketrans("()", "[]"))

        (safe_value_raw, exc) = safe_eval(value_raw, include_exceptions=True)
        if exc is not None:
            self.module.fail_json(
                msg="ERROR: The %s value_raw has invalid format" % state
            )

        return safe_value_raw

    def _detect_changes(self):

        current = self.current["rule"].copy()
        desired = self.desired.get("rule").copy()
        changes = []

        if current.get("conditions", {}) != desired.get("conditions", {}):
            changes.append("conditions")

        if current.get("properties", {}) != desired.get("properties", {}):
            changes.append("properties")

        if self._raw_value_eval("current", current) != self._raw_value_eval(
            "desired", desired
        ):
            changes.append("raw_value")

        desired_location = desired.get("rule", {}).get("location")
        if desired_location:
            current_location = RuleLocation(
                self.module, current.get("folder", "/"), self.rule_id
            )

            if not current_location.is_equal(desired_location):
                changes.append("location")

        return changes

    def _build_default_endpoint(self):
        return "%s/%s" % (
            RuleEndpoints.default,
            self.rule_id,
        )

    def _get_current(self):
        current = {}

        result = self._fetch(
            code_mapping=RuleHTTPCodes.get,
            endpoint=self._build_default_endpoint(),
            method="GET",
        )

        if result.http_code == 200:
            current["rule"] = {}
            self.state = "present"
            current["etag"] = result.etag

            content = json.loads(result.content)
            extensions = content["extensions"]

            for key, value in extensions.items():
                if key in CURRENT_RULE_KEYS:
                    current["rule"][key] = value

        else:
            self.state = "absent"
        return current

    def _check_output(self, mode):
        return RESULT(
            http_code=0,
            msg="Running in check mode. Would have done an %s" % mode,
            content="",
            etag="",
            failed=False,
            changed=False,
        )

    def needs_update(self):
        return len(self._changed_items) > 0

    def _moving_needed(self):
        # self.module.warn("a")
        if "location" in self._changed_items:
            # self.module.warn("b")
            return True

        if self.is_new_rule:
            # self.module.warn("c")
            location = self.desired.get("rule").get("location")
            # self.module.warn("#### %s" % str(location))
            if location and not (
                location.get("folder", "") == "/"
                and location.get("position", "") == "bottom"
            ):
                # self.module.warn("d")
                return True

        return False

    def _move_if_needed(self):
        # self.module.warn("1")
        if not self._moving_needed():
            return

        # self.module.warn("2")
        location = self.desired.get("rule", {}).get("location")
        data = {"position": POSITION_MAPPING[location.get("position")]}

        pos = location.get("position", "")
        # self.module.warn("3")
        if pos in ["top", "bottom"]:
            # self.module.warn("4")
            data["folder"] = location.get("folder", "/")
        elif pos in ["before", "after"]:
            # self.module.warn("5")
            data["rule_id"] = location.get("neighbour")

        if self.module.check_mode:
            return self._check_output("move")

        # self.module.warn("#### %s" % self._build_default_endpoint() + "/actions/move/invoke")
        # self.module.warn("#### %s" % str(data))
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
        data = self.desired.get("rule", {}).copy()
        location = data.pop("location", {})
        data["ruleset"] = self.desired.get("ruleset")
        data["folder"] = location.get("folder", "/")

        if not data.get("value_raw"):
            self.module.fail_json(msg="ERROR: The parameter value_raw is mandatory.")

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

        # self.module.warn("#### create_result.content %s" % str(create_result.content))
        content = json.loads(create_result.content)
        self.rule_id = content.get("id")
        # self.module.warn("#### %s" % self.rule_id)

        move_result = self._move_if_needed()
        if move_result:
            # self.module.warn("#### move_result.content %s" % str(move_result.content))
            m = self._merge_results({"created": create_result, "moved": move_result})
            # self.module.warn("#### m.content %s" % str(m.content))
            return self._merge_results({"created": create_result, "moved": move_result})
        else:
            return create_result

    def edit(self):
        data = self.desired.get("rule", {}).copy()
        data.pop("location")
        self.headers["if-Match"] = self.etag

        if not data.get("value_raw"):
            self.module.fail_json(msg="ERROR: The parameter value_raw is mandatory.")

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
            return self._merge_results({"editd": edit_result, "moved": move_result})
        else:
            return edit_result

    def delete(self):
        # self.module.warn("deleting: %s" % self._build_default_endpoint())
        if self.module.check_mode:
            return self._check_output("delete")

        result = self._fetch(
            code_mapping=RuleHTTPCodes.delete,
            endpoint=self._build_default_endpoint(),
            method="DELETE",
        )

        # self.module.warn("http: %s" % str(result.http_code))
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
                            choices=["top", "bottom", "before", "after"],
                            default="bottom",
                        ),
                        folder=dict(
                            type="str",
                            default="/",
                        ),
                        neighbour=dict(type="str", aliasses=["rule_id"]),
                    ),
                    # required_if=[
                    #    ("position", "top", ("folder",)),
                    #    ("position", "bottom", ("folder",)),
                    #    ("position", "before", ("neighbour",)),
                    #    ("position", "after", ("neighbour",)),
                    # ],
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
        msg="Invalid parameters provided.",
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
                # module.warn("NEEDS UPDATE")
                result = current_rule.edit()
            else:
                # module.warn("ALREADY AS DESIRED")
                result = result._replace(
                    msg="Rule already exists with the desired parameters."
                )
        elif rule_id:
            # rule_id provided but not found. Fail
            result = result._replace(
                msg="The provided rule_id was not found.",
                failed=True,
            )
        else:
            # Create new rule
            result = current_rule.create()
    elif desired_state == "absent":
        # module.warn("desired_state == absent")
        # module.warn("current_state: %s" % str(current_rule.state))
        if current_rule.state == "present":
            result = current_rule.delete()
        elif current_rule.state == "absent":
            result = result._replace(msg="Rule already absent.")

    if result.content:
        result = result._replace(content=json.loads(result.content))
    result_as_dict = result._asdict()
    # module.warn("############ %s" % str(result_as_dict))
    module.exit_json(**result_as_dict)


def main():
    run_module()


if __name__ == "__main__":
    main()

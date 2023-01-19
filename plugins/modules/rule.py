#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2022, diademiemi <emilia@diademiemi.me> & Robin Gierse <robin.gierse@tribe29.com>
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
    - Currently, the idempotency of this module is restricted.
    - To check if an equal rule already exists, only folder, conditions and properties are used. value_raw is currently not being compared.

extends_documentation_fragment: [tribe29.checkmk.common]

options:
    rule:
        description: Definition of the rule as returned by the Checkmk API.
        required: true
        type: dict
        suboptions:
            location:
                description:
                  - Location of the rule within a folder.
                  - By default rules are created at the bottom of the "/" folder.
                  - Mutually exclusive with I(folder).
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
                    rule_id:
                        description:
                            - Put the rule C(before) or C(after) this rule_id.
                            - Required when I(position) is C(before) or C(after).
                            - Mutually exclusive with I(folder).
                        type: str
                    folder:
                        description:
                            - Folder of the rule.
                            - Required when I(position) is C(top) or C(bottom).
                            - Required when I(state=absent).
                            - Mutually exclusive with I(rule_id).
                        default: "/"
                        type: str
            folder:
                description:
                  - Folder of the rule.
                  - Deprecated, use I(location) instead.
                  - Mutually exclusive with I(location).
                type: str
            conditions:
                description: Conditions of the rule.
                type: dict
            properties:
                description: Properties of the rule.
                type: dict
            value_raw:
                description: Rule values as exported from the UI.
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
    - diademiemi (@diademiemi)
    - Geoffroy Stévenne (@geof77)
"""

EXAMPLES = r"""
# Create a rule in checkgroup_parameters:memory_percentage_used
# at the top of the main folder.
- name: "Create a rule in checkgroup_parameters:memory_percentage_used."
  tribe29.checkmk.rule:
    server_url: "http://localhost/"
    site: "my_site"
    automation_user: "automation"
    automation_secret: "$SECRET"
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
            "documentation_url": "https://github.com/tribe29/ansible-collection-tribe29.checkmk/blob/main/plugins/modules/rules.py"
        }
        folder: "/"
        value_raw: "{'levels': (80.0, 90.0)}"
        location:
            folder: "/"
            position: "top"
    state: "present"
    register: response

- name: Show the ID of the new rule
  debug:
    msg: "RULE ID : {{ response.id }}"

# Create another rule in checkgroup_parameters:memory_percentage_used
# and put it after the rule created above.
- name: "Create a rule in checkgroup_parameters:memory_percentage_used."
  tribe29.checkmk.rule:
    server_url: "http://localhost/"
    site: "my_site"
    automation_user: "automation"
    automation_secret: "$SECRET"
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
            "documentation_url": "https://github.com/tribe29/ansible-collection-tribe29.checkmk/blob/main/plugins/modules/rules.py"
        }
        value_raw: "{'levels': (85.0, 99.0)}"
        location:
            position: "after"
            rule_id: "{{ response.id }}"
    state: "present"

# Delete the first rule.
- name: "Delete a rule."
  tribe29.checkmk.rule:
    server_url: "http://localhost/"
    site: "my_site"
    automation_user: "automation"
    automation_secret: "$SECRET"
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
            "documentation_url": "https://github.com/tribe29/ansible-collection-tribe29.checkmk/blob/main/plugins/modules/rules.py"
        }
        value_raw: "{'levels': (80.0, 90.0)}"
    state: "absent"
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
from ansible.module_utils.urls import fetch_url

try:
    from urllib import urlencode
except ImportError:  # For Python 3
    from urllib.parse import urlencode


def exit_failed(module, msg, id=""):
    result = {"msg": msg, "id": id, "changed": False, "failed": True}
    module.fail_json(**result)


def exit_changed(module, msg, id=""):
    result = {"msg": msg, "id": id, "changed": True, "failed": False}
    module.exit_json(**result)


def exit_ok(module, msg, id=""):
    result = {"msg": msg, "id": id, "changed": False, "failed": False}
    module.exit_json(**result)


def get_rules_in_ruleset(module, base_url, headers, ruleset):
    api_endpoint = "/domain-types/rule/collections/all"

    params = {
        "ruleset_name": ruleset,
    }

    url = "%s%s?%s" % (base_url, api_endpoint, urlencode(params))

    response, info = fetch_url(
        module, url, module.jsonify(params), headers=headers, method="GET"
    )

    if info["status"] != 200:
        exit_failed(
            module,
            "Error calling API. HTTP code %d. Details: %s, "
            % (info["status"], info["body"]),
        )
    return json.loads(response.read().decode("utf-8"))


def get_existing_rule(module, base_url, headers, ruleset, rule):
    # Get rules in ruleset
    rules = get_rules_in_ruleset(module, base_url, headers, ruleset)

    if rules is not None:
        # Loop through all rules
        for r in rules.get("value"):
            if (
                r["extensions"]["conditions"] == rule["conditions"]
                and r["extensions"]["properties"] == rule["properties"]
                and r["extensions"]["folder"] == rule["folder"]
                # and r["extensions"]["value_raw"] == rule["value_raw"]
            ):
                # If they are the same, return the ID
                return r["id"]
    return None


def create_rule(module, base_url, headers, ruleset, rule):
    api_endpoint = "/domain-types/rule/collections/all"

    params = {
        "ruleset": ruleset,
        "folder": rule["folder"],
        "properties": rule["properties"],
        "value_raw": rule["value_raw"],
        "conditions": rule["conditions"],
    }

    url = base_url + api_endpoint

    response, info = fetch_url(
        module, url, module.jsonify(params), headers=headers, method="POST"
    )

    if info["status"] != 200:
        exit_failed(
            module,
            "Error calling API. HTTP code %d. Details: %s, "
            % (info["status"], info["body"]),
        )

    r = json.loads(response.read().decode("utf-8"))

    return r["id"]


def get_rule_etag(module, base_url, headers, rule_id):
    api_endpoint = "/objects/rule/" + rule_id

    url = base_url + api_endpoint

    response, info = fetch_url(module, url, headers=headers, method="GET")

    if info["status"] not in [200, 204]:
        exit_failed(
            module,
            "Error calling API. HTTP code %d. Details: %s, "
            % (info["status"], info["body"]),
        )
    return info["etag"]


def move_rule(module, base_url, headers, rule_id, location):
    api_endpoint = "/objects/rule/" + rule_id + "/actions/move/invoke"

    api_keywords = {
        "top": "top_of_folder",
        "bottom": "bottom_of_folder",
        "before": "before_specific_rule",
        "after": "after_specific_rule",
    }

    params = {
        "position": api_keywords[location["position"]],
    }
    if location["position"] in ["after", "before"]:
        params["rule_id"] = location["rule_id"]
    else:
        params["folder"] = location["folder"]

    headers["If-Match"] = get_rule_etag(module, base_url, headers, rule_id)

    url = base_url + api_endpoint

    response, info = fetch_url(
        module, url, module.jsonify(params), headers=headers, method="POST"
    )

    if info["status"] not in [200, 204]:
        exit_failed(
            module,
            "Error calling API. HTTP code %d. Details: %s, "
            % (info["status"], info["body"]),
        )

    r = json.loads(response.read().decode("utf-8"))

    return r["id"]


def delete_rule(module, base_url, headers, rule_id):
    api_endpoint = "/objects/rule/"

    url = "%s%s%s" % (base_url, api_endpoint, rule_id)

    response, info = fetch_url(module, url, headers=headers, method="DELETE")

    if info["status"] != 204:
        exit_failed(
            module,
            "Error calling API. HTTP code %d. Details: %s, "
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
        ruleset=dict(type="str", required=True),
        rule=dict(
            type="dict",
            required=True,
            options=dict(
                folder=dict(type="str"),
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
                        rule_id=dict(type="str"),
                    ),
                    required_if=[
                        ("position", "top", ("folder",)),
                        ("position", "bottom", ("folder",)),
                        ("position", "before", ("rule_id",)),
                        ("position", "after", ("rule_id",)),
                    ],
                    mutually_exclusive=[("folder", "rule_id")],
                    apply_defaults=True,
                    deprecated_aliases=[
                        dict(
                            name="folder",
                            collection_name="tribe29.checkmk",
                            version="1.0.0",
                        ),
                    ],
                ),
            ),
            mutually_exclusive=[("folder", "location")],
        ),
        state=dict(type="str", default="present", choices=["present", "absent"]),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=False)

    # Use the parameters to initialize some common variables
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer %s %s"
        % (
            module.params.get("automation_user", ""),
            module.params.get("automation_secret", ""),
        ),
    }

    base_url = "%s/%s/check_mk/api/1.0" % (
        module.params.get("server_url", ""),
        module.params.get("site", ""),
    )

    # Get the variables
    ruleset = module.params.get("ruleset", "")
    rule = module.params.get("rule", "")
    location = rule.get("location")

    # Check if required params to create a rule are given
    if rule.get("folder") is None or rule.get("folder") == "":
        rule["folder"] = location["folder"]
    if rule.get("properties") is None or rule.get("properties") == "":
        exit_failed(module, "Rule properties are required")
    if rule.get("value_raw") is None or rule.get("value_raw") == "":
        exit_failed(module, "Rule value_raw is required")
    # Default to all hosts if conditions arent given
    if rule.get("conditions") is None or rule.get("conditions") == "":
        rule["conditions"] = {
            "host_tags": [],
            "host_labels": [],
            "service_labels": [],
        }
    if module.params.get("state") == "absent":
        if location.get("rule_id") is not None:
            exit_failed(module, "rule_id in location is invalid with state=absent")

    # Get ID of rule that is the same as the given options
    rule_id = get_existing_rule(module, base_url, headers, ruleset, rule)

    # If rule exists
    if rule_id is not None:
        # If state is absent, delete the rule
        if module.params.get("state") == "absent":
            delete_rule(module, base_url, headers, rule_id)
            exit_changed(module, "Deleted rule")
        # If state is present, do nothing
        else:
            exit_ok(module, "Rule already exists", rule_id)
    # If rule does not exist
    else:
        # If state is present, create the rule
        if module.params.get("state") == "present":
            rule_id = create_rule(module, base_url, headers, ruleset, rule)
            # Move rule to specified location, if it's not default
            if location["position"] != "bottom":
                rule_id = move_rule(module, base_url, headers, rule_id, location)
            exit_changed(module, "Created rule", rule_id)
        # If state is absent, do nothing
        else:
            exit_ok(module, "Rule did not exist")

    # Fallback
    exit_failed(module, "Unknown error")


def main():
    run_module()


if __name__ == "__main__":
    main()

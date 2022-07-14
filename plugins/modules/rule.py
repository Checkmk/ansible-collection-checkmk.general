#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2022, diademiemi <emilia@diademiemi.me> & Robin Gierse <robin.gierse@tribe29.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: host

short_description: Manage hosts in Checkmk.

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "0.6.0"

description:
- Manage rules within Checkmk. Will always return with json of the rule(s).

extends_documentation_fragment: [tribe29.checkmk.common]

options:
    id:
        description: ID of the rule to manage. If not specified, a list of rulesin the ruleset is returned
        required: false
        type: str
    ruleset:
        description: Name of the ruleset.
        type: str
        required: true

author:
    - Robin Gierse (@robin-tribe29)
    - Lars Getwan (@lgetwan)
"""

EXAMPLES = r"""
# Create a rule.
- name: "Create a rule."
  tribe29.checkmk.rule:
    server_url: "http://localhost/"
    site: "my_site"
    automation_user: "automation"
    automation_secret: "$SECRET"
    ruleset: "checkgroup_parameters:cpu_iowait"
    import: |
        {'levels_single': (40.0, 90.0),
        'util': (30.0, 80.0)}
    state: "present"
    enabled: true

# List rules in ruleset.
- name: "List rules in ruleset."
  tribe29.checkmk.rule:
    server_url: "http://localhost/"
    site: "my_site"
    automation_user: "automation"
    automation_secret: "$SECRET"
    ruleset: "checkgroup_parameters:cpu_iowait"
  register: rules

# Export a rule.
- name: "Export a rule."
  tribe29.checkmk.rule:
    server_url: "http://localhost/"
    site: "my_site"
    automation_user: "automation"
    automation_secret: "$SECRET"
    ruleset: "checkgroup_parameters:cpu_iowait"
    id: "123e4567-e89b-12d3-a456-426614174000"
  register: rule_export

# Disable a rule.
- name: "Disable a rule."
  tribe29.checkmk.rule:
    server_url: "http://localhost/"
    site: "my_site"
    automation_user: "automation"
    automation_secret: "$SECRET"
    ruleset: "checkgroup_parameters:cpu_iowait"
    id: "123e4567-e89b-12d3-a456-426614174000"
    enabled: false
"""

RETURN = r"""
msg:
    description: The output message that the module generates. Contains the API response details in case of an error.
    type: str
    returned: always
    sample: 'Rule created.'
results:
    description: API response the module may generate, such as rule exports.
    type: str
    returned: optional
"""

import json

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url

try:
    from urllib import urlencode
except ImportError:  # For Python 3
    from urllib.parse import urlencode

def exit_failed(module, msg):
    result = {"msg": msg, "changed": False, "failed": True}
    module.fail_json(**result)


def exit_changed(module, msg):
    result = {"msg": msg, "changed": True, "failed": False}
    module.exit_json(**result)


def exit_ok(module, msg, response):
    result = {"msg": msg, "changed": False, "failed": False, "response": response}
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

def get_rule_by_id(module, base_url, headers, rule_id):
    api_endpoint = "/objects/rule/"

    url = "%s%s%s" % (base_url, api_endpoint, rule_id)

    response, info = fetch_url(
        module, url, headers=headers, method="GET"
    )

    if info["status"] != 200:
        exit_failed(
            module,
            "Error calling API. HTTP code %d. Details: %s, "
            % (info["status"], info["body"]),
        )
    return json.loads(response.read().decode("utf-8")).get("extensions")

def create_rule(module, base_url, headers, folder, ruleset, rule):
    api_endpoint = "/domain-types/rule/collections/all"

    params = {
        "ruleset": ruleset,
        "folder": folder,
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
    return json.loads(response.read().decode("utf-8"))

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        server_url=dict(type="str", required=True),
        site=dict(type="str", required=True),
        automation_user=dict(type="str", required=True),
        automation_secret=dict(type="str", required=True, no_log=True),
        ruleset=dict(type="str", required=False),
        id=dict(type="str", required=False),
        folder=dict(type="str", required=False, default="~"),
        enabled=dict(type="bool", default=True),
        rule=dict(type="dict", required=False),
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

    rule = module.params.get("rule", "")
    rule_id = module.params.get("id", "")
    ruleset = module.params.get("ruleset", "")
    folder = module.params.get("folder", "")

    if rule_id is None or rule_id == "":
        if ruleset is None or ruleset == "":
            exit_failed(module, "No ruleset specified.")
        else:
            if rule is not None and rule != "":
                response = create_rule(module, base_url, headers, folder, ruleset, rule)
                exit_ok(module, "Created rule in ruleset", response)
            else:
                response = get_rules_in_ruleset(module, base_url, headers, ruleset)
                exit_ok(module, "Got rules in ruleset", response)
    elif rule_id is not None and rule_id != "":
        response = get_rule_by_id(module, base_url, headers, rule_id)
        exit_ok(module, "Got rule by ID", response)
    else:
        exit_failed(module, "Unknown error")


def main():
    run_module()


if __name__ == "__main__":
    main()

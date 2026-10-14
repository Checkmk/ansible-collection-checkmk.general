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
module: bi_rule

short_description: Manage BI rules in Checkmk.

version_added: "8.6.0"

description:
  - Create, update and delete BI rules in Checkmk.
  - The options other than I(name) and I(pack) take the structures of the Checkmk
    REST API as they are. See the C(bi_rule) endpoints in the REST API documentation
    of your Checkmk site for their contents.

extends_documentation_fragment: [checkmk.general.common]

options:
    name:
        description: The ID of the BI rule.
        required: true
        type: str

    pack:
        description:
          - The ID of the BI pack the rule belongs to.
          - Changing it for an existing rule has no effect, see the notes.
        required: true
        type: str

    nodes:
        description:
          - The nodes of the BI rule.
          - Required when I(state=present).
        type: list
        elements: dict

    properties:
        description:
          - The properties of the BI rule, such as C(title) and C(comment).
          - Required when I(state=present).
        type: dict

    aggregation_function:
        description:
          - How the states of the nodes are aggregated.
          - Required when I(state=present).
        type: dict

    computation_options:
        description:
          - The computation options of the BI rule.
          - Required when I(state=present).
        type: dict

    node_visualization:
        description:
          - How the nodes of the BI rule are visualized.
          - Required when I(state=present).
        type: dict

    params:
        description: The parameters of the BI rule.
        type: dict
        default: {"arguments": []}
        suboptions:
            arguments:
                description: The arguments of the BI rule.
                type: list
                elements: str
                default: []

    state:
        description: The desired state of the BI rule.
        type: str
        default: "present"
        choices: ["present", "absent"]

notes:
    - Only the options and nested keys given in the task are compared. Defaults
      that Checkmk fills in for omitted nested keys do not count as a difference.
    - Checkmk does not report which pack a rule belongs to. Moving an existing rule
      to another pack by changing I(pack) is therefore not detected, and the module
      reports no change. Delete the rule and create it in the other pack instead.
    - A rule that calls another rule needs that rule to exist, and Checkmk refuses
      to delete a rule that other rules still call. Create the called rules first
      and delete them last.
    - BI changes have to be activated, for example with M(checkmk.general.activation).

author:
    - Lars Getwan (@lgetwan)

seealso:
    - module: checkmk.general.bi_pack
    - module: checkmk.general.bi_aggregation
    - plugin: checkmk.general.bi_rule
      plugin_type: lookup
    - plugin: checkmk.general.bi_rules
      plugin_type: lookup
    - name: "Business Intelligence: The official user guide."
      description: "The official user guide on Business Intelligence (BI)."
      link: "https://docs.checkmk.com/latest/en/bi.html"
"""

EXAMPLES = r"""
# ---------------------------------------------------------------------------
# Create and update BI rules
# ---------------------------------------------------------------------------
# Create the rules a rule calls before the rule itself.

- name: "Create a BI rule that aggregates the state of a host."
  checkmk.general.bi_rule:
    server_url: "https://myserver"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    name: "host_state"
    pack: "cluster_pack"
    nodes:
      - search:
          type: "empty"
        action:
          type: "state_of_host"
          host_regex: "$HOST$"
    params:
      arguments:
        - "HOST"
    properties:
      title: "Host $HOST$"
      comment: ""
      docu_url: ""
      icon: ""
      state_messages: {}
    aggregation_function:
      type: "worst"
      count: 1
      restrict_state: 2
    computation_options:
      disabled: false
    node_visualization:
      type: "block"
      style_config: {}
    state: "present"

- name: "Create a BI rule that calls the rule above."
  checkmk.general.bi_rule:
    server_url: "https://myserver"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    name: "cluster_state"
    pack: "cluster_pack"
    nodes:
      - search:
          type: "empty"
        action:
          type: "call_a_rule"
          rule_id: "host_state"
          params:
            arguments:
              - "node1"
    properties:
      title: "Cluster"
      comment: ""
      docu_url: ""
      icon: ""
      state_messages: {}
    aggregation_function:
      type: "best"
      count: 1
      restrict_state: 2
    computation_options:
      disabled: false
    node_visualization:
      type: "block"
      style_config: {}
    state: "present"

# ---------------------------------------------------------------------------
# Delete BI rules
# ---------------------------------------------------------------------------
# Delete the aggregations that use a rule first, then the rule, then the rules
# it calls.

- name: "Delete a BI rule."
  checkmk.general.bi_rule:
    server_url: "https://myserver"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    name: "cluster_state"
    pack: "cluster_pack"
    state: "absent"
"""

RETURN = r"""
msg:
    description: The output message that the module generates. Contains the API response details in case of an error.
    type: str
    returned: always
    sample: 'BI rule created.'
http_code:
    description: The HTTP code the Checkmk API returns.
    type: int
    returned: always
    sample: 200
content:
    description:
        - The raw, undecoded response body of the Checkmk API.
        - Empty when the API returned no body, e.g. when nothing had to be done.
    type: str
    returned: always
    sample: '{"id": "cluster_state", "pack_id": "", "nodes": []}'
etag:
    description:
        - The ETag the Checkmk API returned for the object.
        - Empty when the API returned no ETag.
    type: str
    returned: always
    sample: ''
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.checkmk.general.plugins.module_utils.bi import BIObjectAPI
from ansible_collections.checkmk.general.plugins.module_utils.differ import (
    prune_none,
)
from ansible_collections.checkmk.general.plugins.module_utils.utils import (
    base_argument_spec,
    exit_module,
)

# The API requires these on create and update. 'params' has a default.
REQUIRED_WHEN_PRESENT = [
    "nodes",
    "properties",
    "aggregation_function",
    "computation_options",
    "node_visualization",
]


class BIRuleAPI(BIObjectAPI):
    DOMAIN_TYPE = "bi_rule"
    LABEL = "BI rule"


def run_module():
    argument_spec = base_argument_spec()
    argument_spec.update(
        name=dict(type="str", required=True),
        pack=dict(type="str", required=True),
        nodes=dict(type="list", elements="dict"),
        properties=dict(type="dict"),
        aggregation_function=dict(type="dict"),
        computation_options=dict(type="dict"),
        node_visualization=dict(type="dict"),
        params=dict(
            type="dict",
            default=dict(arguments=[]),
            options=dict(
                arguments=dict(type="list", elements="str", default=[]),
            ),
        ),
        state=dict(type="str", default="present", choices=["present", "absent"]),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        required_if=[("state", "present", REQUIRED_WHEN_PRESENT)],
        supports_check_mode=True,
    )

    desired = prune_none(
        {
            "id": module.params.get("name"),
            "pack_id": module.params.get("pack"),
            "nodes": module.params.get("nodes"),
            "properties": module.params.get("properties"),
            "aggregation_function": module.params.get("aggregation_function"),
            "computation_options": module.params.get("computation_options"),
            "node_visualization": module.params.get("node_visualization"),
            "params": module.params.get("params"),
        }
    )

    bi_rule = BIRuleAPI(module, module.params.get("name"), desired)
    exit_module(module, result=bi_rule.ensure(module.params.get("state")))


def main():
    run_module()


if __name__ == "__main__":
    main()

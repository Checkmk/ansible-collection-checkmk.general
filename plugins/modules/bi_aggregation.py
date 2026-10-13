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
module: bi_aggregation

short_description: Manage BI aggregations in Checkmk.

version_added: "8.6.0"

description:
  - Create, update and delete BI aggregations in Checkmk.
  - The options I(node), I(aggregation_visualization) and I(computation_options)
    take the structures of the Checkmk REST API as they are. See the
    C(bi_aggregation) endpoints in the REST API documentation of your Checkmk site
    for their contents.

extends_documentation_fragment: [checkmk.general.common]

options:
    name:
        description: The ID of the BI aggregation.
        required: true
        type: str

    pack:
        description:
          - The ID of the BI pack the aggregation belongs to.
          - Changing it for an existing aggregation has no effect, see the notes.
        required: true
        type: str

    comment:
        description: A comment that explains the purpose of the aggregation.
        type: str

    customer:
        description:
          - For Checkmk Ultimate with multi-tenancy (CME), the customer ID the
            aggregation belongs to.
        type: str

    groups:
        description:
          - The groups the aggregation is shown in.
          - Required when I(state=present). Pass empty lists to show it in no group.
        type: dict
        suboptions:
            names:
                description: The names of the groups.
                type: list
                elements: str
            paths:
                description: The paths of the groups, each a list of path elements.
                type: list
                elements: list

    node:
        description:
          - The node that generates the aggregation, usually a call of a BI rule.
          - Required when I(state=present).
        type: dict
        suboptions:
            search:
                description: The search that selects the objects.
                type: dict
                required: true
            action:
                description: What is done with the search results.
                type: dict
                required: true

    aggregation_visualization:
        description:
          - How the aggregation is visualized.
          - Required when I(state=present).
        type: dict

    computation_options:
        description:
          - The computation options of the aggregation.
          - Required when I(state=present).
        type: dict

    state:
        description: The desired state of the BI aggregation.
        type: str
        default: "present"
        choices: ["present", "absent"]

notes:
    - Only the options and nested keys given in the task are compared. Defaults
      that Checkmk fills in for omitted nested keys do not count as a difference.
    - Checkmk does not report which pack an aggregation belongs to. Moving an
      existing aggregation to another pack by changing I(pack) is therefore not
      detected, and the module reports no change. Delete the aggregation and create
      it in the other pack instead.
    - An aggregation needs the rules it calls to exist. Create the rules first and
      delete the aggregation before them.
    - BI changes have to be activated, for example with M(checkmk.general.activation).

author:
    - Lars Getwan (@lgetwan)

seealso:
    - module: checkmk.general.bi_pack
    - module: checkmk.general.bi_rule
    - plugin: checkmk.general.bi_aggregation
      plugin_type: lookup
    - plugin: checkmk.general.bi_aggregations
      plugin_type: lookup
    - name: "Business Intelligence: The official user guide."
      description: "The official user guide on Business Intelligence (BI)."
      link: "https://docs.checkmk.com/latest/en/bi.html"
"""

EXAMPLES = r"""
# ---------------------------------------------------------------------------
# Create and update BI aggregations
# ---------------------------------------------------------------------------
# Create the rules an aggregation calls before the aggregation.

- name: "Create a BI aggregation that calls a BI rule."
  checkmk.general.bi_aggregation:
    server_url: "https://myserver"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    name: "cluster"
    pack: "cluster_pack"
    comment: "Overall state of the cluster."
    groups:
      names:
        - "Clusters"
      paths: []
    node:
      search:
        type: "empty"
      action:
        type: "call_a_rule"
        rule_id: "cluster_state"
        params:
          arguments: []
    aggregation_visualization:
      ignore_rule_styles: false
      layout_id: "builtin_default"
      line_style: "round"
    computation_options:
      disabled: false
      use_hard_states: false
      escalate_downtimes_as_warn: false
      freeze_aggregations: false
    state: "present"

# ---------------------------------------------------------------------------
# Delete BI aggregations
# ---------------------------------------------------------------------------
# Delete the aggregations before the rules they call.

- name: "Delete a BI aggregation."
  checkmk.general.bi_aggregation:
    server_url: "https://myserver"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    name: "cluster"
    pack: "cluster_pack"
    state: "absent"
"""

RETURN = r"""
msg:
    description: The output message that the module generates. Contains the API response details in case of an error.
    type: str
    returned: always
    sample: 'BI aggregation created.'
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
    sample: '{"id": "cluster", "pack_id": "", "comment": "Overall state of the cluster."}'
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

# The API requires these on create and update.
REQUIRED_WHEN_PRESENT = [
    "groups",
    "node",
    "aggregation_visualization",
    "computation_options",
]


class BIAggregationAPI(BIObjectAPI):
    DOMAIN_TYPE = "bi_aggregation"
    LABEL = "BI aggregation"


def run_module():
    argument_spec = base_argument_spec()
    argument_spec.update(
        name=dict(type="str", required=True),
        pack=dict(type="str", required=True),
        comment=dict(type="str"),
        customer=dict(type="str"),
        groups=dict(
            type="dict",
            options=dict(
                names=dict(type="list", elements="str"),
                paths=dict(type="list", elements="list"),
            ),
        ),
        node=dict(
            type="dict",
            options=dict(
                search=dict(type="dict", required=True),
                action=dict(type="dict", required=True),
            ),
        ),
        aggregation_visualization=dict(type="dict"),
        computation_options=dict(type="dict"),
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
            "comment": module.params.get("comment"),
            "customer": module.params.get("customer"),
            "groups": module.params.get("groups"),
            "node": module.params.get("node"),
            "aggregation_visualization": module.params.get("aggregation_visualization"),
            "computation_options": module.params.get("computation_options"),
        }
    )

    bi_aggregation = BIAggregationAPI(module, module.params.get("name"), desired)
    exit_module(module, result=bi_aggregation.ensure(module.params.get("state")))


def main():
    run_module()


if __name__ == "__main__":
    main()

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
module: bi_pack

short_description: Manage BI packs in Checkmk.

version_added: "8.6.0"

description:
  - Create, update and delete BI packs in Checkmk.
  - A BI pack holds BI rules and BI aggregations, which are managed with the
    M(checkmk.general.bi_rule) and M(checkmk.general.bi_aggregation) modules.

extends_documentation_fragment: [checkmk.general.common]

options:
    name:
        description: The ID of the BI pack.
        required: true
        type: str

    title:
        description:
          - The title of the BI pack.
          - Required when I(state=present).
        type: str

    contact_groups:
        description: The contact groups of the BI pack.
        type: list
        elements: str
        default: []

    public:
        description: Whether the BI pack is visible to all users.
        type: bool
        default: false

    state:
        description:
          - The desired state of the BI pack.
          - C(absent) deletes the BI pack. Checkmk refuses to delete a pack that still
            holds rules, so delete its aggregations and rules first.
        type: str
        default: "present"
        choices: ["present", "absent"]

notes:
    - BI changes have to be activated, for example with M(checkmk.general.activation).

author:
    - Lars Getwan (@lgetwan)

seealso:
    - module: checkmk.general.bi_rule
    - module: checkmk.general.bi_aggregation
    - plugin: checkmk.general.bi_pack
      plugin_type: lookup
    - plugin: checkmk.general.bi_packs
      plugin_type: lookup
    - name: "Business Intelligence: The official user guide."
      description: "The official user guide on Business Intelligence (BI)."
      link: "https://docs.checkmk.com/latest/en/bi.html"
"""

EXAMPLES = r"""
# ---------------------------------------------------------------------------
# Create and update BI packs
# ---------------------------------------------------------------------------

- name: "Create a BI pack."
  checkmk.general.bi_pack:
    server_url: "https://myserver"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    name: "cluster_pack"
    title: "Cluster Pack"
    contact_groups:
      - "admins"
      - "devops"
    public: true
    state: "present"

- name: "Create a BI pack using basic authentication."
  checkmk.general.bi_pack:
    server_url: "https://myserver"
    site: "mysite"
    api_auth_type: "basic"
    api_user: "myuser"
    api_secret: "mypassword"
    name: "network_pack"
    title: "Network Pack"
    state: "present"

# ---------------------------------------------------------------------------
# Delete BI packs
# ---------------------------------------------------------------------------
# Delete the pack's aggregations and rules first, see the examples of the
# checkmk.general.bi_aggregation and checkmk.general.bi_rule modules.

- name: "Delete a BI pack."
  checkmk.general.bi_pack:
    server_url: "https://myserver"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    name: "cluster_pack"
    state: "absent"
"""

RETURN = r"""
msg:
    description: The output message that the module generates. Contains the API response details in case of an error.
    type: str
    returned: always
    sample: 'BI pack created.'
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
    sample: '{"id": "cluster_pack", "title": "Cluster Pack", "contact_groups": [], "public": false}'
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


class BIPackAPI(BIObjectAPI):
    DOMAIN_TYPE = "bi_pack"
    LABEL = "BI pack"


def run_module():
    argument_spec = base_argument_spec()
    argument_spec.update(
        name=dict(type="str", required=True),
        title=dict(type="str"),
        contact_groups=dict(type="list", elements="str", default=[]),
        public=dict(type="bool", default=False),
        state=dict(type="str", default="present", choices=["present", "absent"]),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        required_if=[("state", "present", ["title"])],
        supports_check_mode=True,
    )

    # The API requires all three on create and update.
    desired = prune_none(
        {
            "title": module.params.get("title"),
            "contact_groups": module.params.get("contact_groups"),
            "public": module.params.get("public"),
        }
    )

    bi_pack = BIPackAPI(module, module.params.get("name"), desired)
    exit_module(module, result=bi_pack.ensure(module.params.get("state")))


def main():
    run_module()


if __name__ == "__main__":
    main()

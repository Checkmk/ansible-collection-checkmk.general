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
module: dcd

short_description: Manage Dynamic Host Management

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "6.3.0"

description:
- Manage Dynamic Host Management (DCD), including creation and deletion.

extends_documentation_fragment: [checkmk.general.common]

options:
    dcd_config:
        description: Configuration parameters for the DCD.
        type: dict
        required: true
        suboptions:
            dcd_id:
                description: Identifier for the DCD configuration.
                type: str
                required: true
            title:
                description: Title of the DCD.
                type: str
                required: false
            comment:
                description: Description or comment for the DCD.
                required: false
                type: str
                default: ""
            site:
                description: Name of the Checkmk site for the DCD configuration.
                type: str
                required: false
            connector:
                description: DCD Connector configuration.
                type: dict
                required: false
                suboptions:
                    connector_type:
                        description: Type of connector (e.g., "piggyback").
                        required: false
                        type: str
                        default: piggyback
                    interval:
                        description: Interval in seconds for DCD polling.
                        required: false
                        type: int
                        default: 60
                    creation_rules:
                        description: Rules for creating hosts.
                        required: false
                        type: list
                        elements: dict
                        suboptions:
                            folder_path:
                                description: Folder path for host creation.
                                type: str
                                required: true
                            delete_hosts:
                                description: Whether to delete hosts that no longer exist.
                                required: false
                                type: bool
                                default: false
                            matching_hosts:
                                description: Restrict host creation using regular expressions.
                                required: false
                                type: list
                                elements: str
                                default: []
                            host_attributes:
                                description: Additional host attributes to set on created hosts.
                                required: false
                                type: dict
                    discover_on_creation:
                        description: Discover services on host creation.
                        required: false
                        type: bool
                        default: true
                    restrict_source_hosts:
                        description: List of hosts to consider as piggyback sources for the DCD connection.
                        required: false
                        type: list
                        elements: str
                        default: []
                    no_deletion_time_after_init:
                        description: Seconds to prevent host deletion after site startup.
                        required: false
                        type: int
                        default: 600
                    max_cache_age:
                        description: Seconds to keep hosts when piggyback source only sends piggyback data for other hosts.
                        required: false
                        type: int
                        default: 3600
                    validity_period:
                        description: Seconds before piggyback data is considered outdated.
                        required: false
                        type: int
                        default: 60
    state:
        description: Desired state of the DCD connection.
        required: false
        type: str
        choices:
        - present
        - absent
        default: present

notes:
- Updating an existing DCD connection is currently not supported,
  as there is no REST API endpoint available for updates.
  If a DCD with the same C(dcd_id) already exists but differs from the desired state,
  the module will fail.

author:
- Lars Getwan (@lgetwan)
"""

EXAMPLES = r"""
# ---------------------------------------------------------------------------
# Create a DCD connection
# ---------------------------------------------------------------------------
# Note: Updating an existing DCD connection is currently not supported,
# as there is no REST API endpoint available for updates. If a DCD with the
# same dcd_id exists but differs from the desired state, the module will fail.

- name: "Create a DCD connection with a creation rule."
  checkmk.general.dcd:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    dcd_config:
      dcd_id: "mypiggyback"
      title: "My Piggyback Connection"
      site: "mysite"
      connector:
        connector_type: "piggyback"
        interval: 60
        creation_rules:
          - folder_path: "/"
            delete_hosts: false
        discover_on_creation: true
        restrict_source_hosts:
          - "myhost"
    state: "present"

- name: "Create a DCD connection with host attributes set on created hosts."
  checkmk.general.dcd:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    dcd_config:
      dcd_id: "mypiggyback"
      title: "My Piggyback Connection"
      site: "mysite"
      connector:
        connector_type: "piggyback"
        interval: 60
        creation_rules:
          - folder_path: "/"
            delete_hosts: false
            host_attributes:
              tag_address_family: "no-ip"
              tag_agent: "special-agents"
              tag_piggyback: "piggyback"
              tag_snmp_ds: "no-snmp"
        discover_on_creation: true
        restrict_source_hosts:
          - "myhost"
    state: "present"

- name: "Create a fully configured piggyback DCD with custom timing and host matching."
  checkmk.general.dcd:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    dcd_config:
      dcd_id: "mypiggyback"
      title: "My Piggyback Connection"
      comment: "Full configuration with custom timing and host pattern matching."
      site: "mysite"
      connector:
        connector_type: "piggyback"
        interval: 30
        creation_rules:
          - folder_path: "/myfolder"
            delete_hosts: true
            matching_hosts:
              - "myhost.*"
            host_attributes:
              tag_address_family: "no-ip"
              tag_agent: "special-agents"
              tag_piggyback: "piggyback"
              tag_snmp_ds: "no-snmp"
        discover_on_creation: true
        restrict_source_hosts:
          - "myhost01"
          - "myhost02"
        no_deletion_time_after_init: 300
        max_cache_age: 7200
        validity_period: 120
    state: "present"

# ---------------------------------------------------------------------------
# Delete a DCD connection
# ---------------------------------------------------------------------------

- name: "Delete a DCD connection."
  checkmk.general.dcd:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    dcd_config:
      dcd_id: "mypiggyback"
      site: "mysite"
    state: "absent"

# ---------------------------------------------------------------------------
# Using environment variables for authentication
# ---------------------------------------------------------------------------
# Connection parameters can be provided via environment variables instead of
# task parameters. The supported variables are:
#   CHECKMK_VAR_SERVER_URL, CHECKMK_VAR_SITE,
#   CHECKMK_VAR_API_USER, CHECKMK_VAR_API_SECRET,
#   CHECKMK_VAR_VALIDATE_CERTS

- name: "Create a DCD connection using environment variables for authentication."
  checkmk.general.dcd:
    dcd_config:
      dcd_id: "mypiggyback"
      title: "My Piggyback DCD"
      site: "mysite"
    state: "present"
  environment:
    CHECKMK_VAR_SERVER_URL: "https://myserver/"
    CHECKMK_VAR_SITE: "mysite"
    CHECKMK_VAR_API_USER: "myuser"
    CHECKMK_VAR_API_SECRET: "mysecret"
    CHECKMK_VAR_VALIDATE_CERTS: "true"
"""

RETURN = r"""
msg:
  description:
    - The output message that the module generates.
  type: str
  returned: always
http_code:
  description:
    - HTTP code returned by the Checkmk API.
  type: int
  returned: always
content:
  description:
    - Content of the DCD object.
  returned: when state is present and DCD created or updated.
  type: dict
diff:
  description:
    - The diff between the current and desired state.
  type: dict
  returned: when differences are detected or in diff mode
"""

import json

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.checkmk.general.plugins.module_utils.api import CheckmkAPI
from ansible_collections.checkmk.general.plugins.module_utils.differ import ConfigDiffer
from ansible_collections.checkmk.general.plugins.module_utils.logger import Logger
from ansible_collections.checkmk.general.plugins.module_utils.utils import (
    base_argument_spec,
    exit_module,
)

logger = Logger()

HTTP_CODES_GET = {
    200: (False, False, "DCD configuration found, nothing changed"),
    404: (False, False, "DCD configuration not found"),
}

HTTP_CODES_CREATE = {
    200: (True, False, "DCD configuration created"),
    201: (True, False, "DCD configuration created"),
    204: (True, False, "DCD configuration created"),
    405: (False, True, "Method Not Allowed"),
}

HTTP_CODES_EDIT = {
    200: (True, False, "DCD configuration modified"),
    405: (False, True, "Method Not Allowed"),
}

HTTP_CODES_DELETE = {
    204: (True, False, "DCD configuration deleted"),
    405: (False, True, "Method Not Allowed"),
}


class DCDAPI(CheckmkAPI):
    def __init__(self, module):
        super().__init__(module)
        dcd_config = self.params.get("dcd_config")
        if not dcd_config or "dcd_id" not in dcd_config:
            exit_module(
                self.module,
                msg="Missing 'dcd_id' in dcd_config dictionary",
                failed=True,
                logger=logger,
            )

        self.dcd_id = dcd_config["dcd_id"]
        self.desired = dcd_config.copy()

        if "site" not in self.desired or self.desired["site"] is None:
            self.desired["site"] = self.params.get("site")
            if self.desired["site"] is None:
                exit_module(
                    self.module,
                    msg="`site` is required in dcd_config.",
                    failed=True,
                    logger=logger,
                )

        if "comment" not in self.desired or self.desired["comment"] is None:
            self.desired["comment"] = ""

        if "connector" in self.desired and isinstance(self.desired["connector"], dict):
            for rule in self.desired["connector"].get("creation_rules", []):
                if len(rule.get("matching_hosts", [])) == 0:
                    del rule["matching_hosts"]

            if len(self.desired["connector"].get("restrict_source_hosts", [])) == 0:
                del self.desired["connector"]["restrict_source_hosts"]

        self.state = None
        self._get_current()
        self.differ = ConfigDiffer(self.desired, self.current)

    def _get_current(self):
        result = self._fetch(
            code_mapping=HTTP_CODES_GET,
            endpoint="/objects/dcd/%s" % self.dcd_id,
            logger=logger,
            method="GET",
        )

        if result.http_code == 200:
            self.state = "present"
            try:
                current_raw = json.loads(result.content)
                self.current = current_raw.get("extensions", {})
                self.current["dcd_id"] = current_raw.get("id")
            except (ValueError, TypeError):
                exit_module(
                    self.module,
                    msg="Failed to decode JSON response from API.",
                    content=result.content,
                    failed=True,
                    logger=logger,
                )
        else:
            self.state = "absent"
            self.current = {}

    def needs_update(self):
        return self.differ.needs_update()

    def generate_diff(self, deletion=False):
        return self.differ.generate_diff(deletion)

    def _perform_action(self, action, method, code_mapping, data=None):
        if action == "create":
            endpoint = "/domain-types/dcd/collections/all"
        else:
            endpoint = "/objects/dcd/%s" % self.dcd_id

        diff = None
        if self.module._diff:
            diff = self.generate_diff(deletion=(action == "delete"))

        if self.module.check_mode:
            action_msgs = {
                "create": "would be created",
                "edit": "would be modified",
                "delete": "would be deleted",
            }
            return dict(
                msg="DCD configuration %s." % action_msgs.get(action, action),
                changed=True,
                diff=diff,
            )

        return self._fetch(
            code_mapping=code_mapping,
            endpoint=endpoint,
            data=data,
            logger=logger,
            method=method,
        )

    def create(self):
        filtered_data = {k: v for k, v in self.desired.items() if v is not None}
        return self._perform_action(
            "create", "POST", HTTP_CODES_CREATE, data=filtered_data
        )

    def edit(self):
        filtered_data = {k: v for k, v in self.desired.items() if v is not None}
        return self._perform_action("edit", "PUT", HTTP_CODES_EDIT, data=filtered_data)

    def delete(self):
        return self._perform_action("delete", "DELETE", HTTP_CODES_DELETE)


def run_module():
    argument_spec = base_argument_spec()
    argument_spec.update(
        server_url=dict(type="str", required=True),
        site=dict(type="str", required=True),
        dcd_config=dict(
            type="dict",
            required=True,
            options={
                "dcd_id": dict(type="str", required=True),
                "title": dict(type="str", required=False),
                "comment": dict(type="str", default=""),
                "site": dict(type="str", required=False),
                "connector": dict(
                    type="dict",
                    options={
                        "connector_type": dict(type="str", default="piggyback"),
                        "interval": dict(type="int", default=60),
                        "creation_rules": dict(
                            type="list",
                            elements="dict",
                            options={
                                "folder_path": dict(type="str", required=True),
                                "delete_hosts": dict(type="bool", default=False),
                                "matching_hosts": dict(
                                    type="list",
                                    elements="str",
                                    required=False,
                                    default=[],
                                ),
                                "host_attributes": dict(type="dict", required=False),
                            },
                        ),
                        "discover_on_creation": dict(type="bool", default=True),
                        "restrict_source_hosts": dict(
                            type="list", elements="str", required=False, default=[]
                        ),
                        "no_deletion_time_after_init": dict(
                            type="int", required=False, default=600
                        ),
                        "max_cache_age": dict(type="int", required=False, default=3600),
                        "validity_period": dict(type="int", required=False, default=60),
                    },
                ),
            },
        ),
        state=dict(type="str", default="present", choices=["present", "absent"]),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    logger.set_loglevel(module._verbosity)

    desired_state = module.params["state"]
    dcd_api = DCDAPI(module)

    if desired_state == "present":
        if dcd_api.state == "absent":
            result = dcd_api.create()
            exit_module(module, result=result, logger=logger)
        elif dcd_api.needs_update():
            exit_module(
                module,
                msg="DCD object cannot be updated. No REST API endpoint available for updates. Diff: %s"
                % str(dcd_api.generate_diff()),
                failed=True,
                logger=logger,
            )
        else:
            exit_module(
                module,
                msg="DCD configuration is already in the desired state.",
                logger=logger,
            )

    elif desired_state == "absent":
        if dcd_api.state == "present":
            result = dcd_api.delete()
            exit_module(module, result=result, logger=logger)
        else:
            exit_module(
                module,
                msg="DCD configuration is already absent.",
                logger=logger,
            )


def main():
    run_module()


if __name__ == "__main__":
    main()

#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2025, Robin Gierse <robin.gierse@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: dcd_metricbackend

short_description: Manage Dynamic Host Management connections for the Metric Backend

version_added: "6.4.0"

description:
- Manage Dynamic Configuration Daemon (DCD) connections that use the Metric Backend connector in Checkmk.
- DCD metric backend connections periodically poll the metric backend and create or
  update hosts based on the metrics data found there.
- Available in Checkmk Ultimate, Ultimate with multi-tenancy, and Cloud editions only.

extends_documentation_fragment: [checkmk.general.common]

options:
    dcd_config:
        description: Configuration parameters for the DCD metric backend connection.
        required: true
        type: dict
        suboptions:
            dcd_id:
                description: The unique identifier for the DCD metric backend connection.
                required: true
                type: str
            title:
                description: A human-readable name for this connection.
                required: false
                type: str
            comment:
                description: A comment describing this dynamic host configuration.
                required: false
                type: str
                default: ""
            documentation_url:
                description:
                    - A URL linking to documentation for this connection.
                    - Accepts global URLs (starting with http://), absolute local URLs (starting with /)
                      or relative URLs (relative to check_mk/).
                required: false
                type: str
                default: ""
            disabled:
                description: Set to true to disable this connection while keeping it configured.
                required: false
                type: bool
                default: false
            site:
                description: The site where this connector should run.
                required: false
                type: str
            connector:
                description: The metric backend connector configuration.
                required: false
                type: dict
                suboptions:
                    connector_type:
                        description: The connector type. Currently only C(metric_backend) is supported. API default is C(metric_backend).
                        required: false
                        type: str
                    interval:
                        description: How often (in seconds) the connection checks the metric backend. API default is C(60).
                        required: false
                        type: int
                    host_name_lookup_rules:
                        description:
                            - Rules that derive host names from metric backend attributes.
                            - Each rule carries a host name template and optional attribute filters
                              that scope which series the resulting host collects. A host produced by
                              several rules collects the series matched by every rule that named it.
                            - Multiple rules and free-form host name templates require Checkmk 3.0.0
                              or later. On Checkmk 2.5 the connector supports only a single host name
                              source and one set of attribute filters, so the module applies the first
                              rule only (warning if more are given), lifts its attribute filters to the
                              connector, and maps a C($RESOURCE_ATTR.<key>$) template to that single
                              resource attribute key. A template that is not of that form is ignored
                              with a warning.
                        required: false
                        type: list
                        elements: dict
                        suboptions:
                            host_name_template:
                                description:
                                    - The template used to derive the host name from metric backend attributes.
                                    - Reference resource attributes with C($RESOURCE_ATTR.<key>$), e.g. C($RESOURCE_ATTR.service.name$).
                                    - API default is C($RESOURCE_ATTR.service.name$).
                                type: str
                            resource_attribute_filters:
                                description: Filters applied to resource attributes from the metric backend.
                                required: false
                                type: list
                                elements: dict
                                suboptions:
                                    key:
                                        description: The attribute key to filter on.
                                        type: str
                                    value:
                                        description: The attribute value to filter on.
                                        type: str
                            scope_attribute_filters:
                                description: Filters applied to scope attributes from the metric backend.
                                required: false
                                type: list
                                elements: dict
                                suboptions:
                                    key:
                                        description: The attribute key to filter on.
                                        type: str
                                    value:
                                        description: The attribute value to filter on.
                                        type: str
                            data_point_attribute_filters:
                                description: Filters applied to data point attributes from the metric backend.
                                required: false
                                type: list
                                elements: dict
                                suboptions:
                                    key:
                                        description: The attribute key to filter on.
                                        type: str
                                    value:
                                        description: The attribute value to filter on.
                                        type: str
                    creation_rules:
                        description:
                            - Rules governing how hosts are created from metric backend data.
                            - The first matching rule is used. At least one rule is required.
                        required: false
                        type: list
                        elements: dict
                        suboptions:
                            folder_path:
                                description: The folder in which to create discovered hosts.
                                type: str
                                required: true
                            delete_hosts:
                                description: Delete hosts when their metric backend data is no longer present. API default is C(true).
                                type: bool
                            host_filters:
                                description: Regular expressions to restrict which hosts are created.
                                type: list
                                elements: str
                            host_attributes:
                                description: Additional host attributes to set on newly created hosts.
                                type: dict
                    discover_on_creation:
                        description: Automatically run a service discovery on any newly created host. API default is C(true).
                        required: false
                        type: bool
                    validity_period:
                        description: Seconds to continue considering outdated metric backend data as valid. API default is C(3600).
                        required: false
                        type: int
                    maximum_number_of_hosts:
                        description: Maximum number of hosts this connection may create. API default is C(500).
                        required: false
                        type: int
    state:
        description:
            - Desired state of the DCD metric backend connection.
            - C(absent) will delete the connection if it exists, or succeed without changes if it is already absent.
        required: false
        type: str
        choices: ["present", "absent"]
        default: "present"

notes:
    - This module uses the Checkmk internal API and requires Checkmk 2.5 or later.
    - Updating an existing connection is not supported via the Checkmk API.
      If a connection with the same C(dcd_id) exists but differs from the desired state, the module will fail with a diff.

author:
    - Robin Gierse (@robin-checkmk)
"""

EXAMPLES = r"""
# ---------------------------------------------------------------------------
# Create a DCD metric backend connection
# ---------------------------------------------------------------------------

- name: "Create a minimal DCD metric backend connection."
  checkmk.general.dcd_metricbackend:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    dcd_config:
      dcd_id: "my_metric_backend_dcd"
      title: "My Metric Backend Connection"
      site: "mysite"
      connector:
        connector_type: "metric_backend"
        creation_rules:
          - folder_path: "/"
    state: "present"

- name: "Create a DCD metric backend connection with full configuration."
  checkmk.general.dcd_metricbackend:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    dcd_config:
      dcd_id: "my_metric_backend_dcd"
      title: "My Metric Backend Connection"
      comment: "Syncs hosts from metric backend data."
      documentation_url: "https://example.com/docs/otel"
      site: "mysite"
      connector:
        connector_type: "metric_backend"
        interval: 120
        host_name_lookup_rules:
          - host_name_template: "$RESOURCE_ATTR.service.name$"
            resource_attribute_filters:
              - key: "environment"
                value: "production"
        creation_rules:
          - folder_path: "/otel_hosts"
            delete_hosts: true
            host_filters:
              - ".*\\.example\\.com"
            host_attributes:
              tag_agent: "no-agent"
        discover_on_creation: true
        validity_period: 7200
        maximum_number_of_hosts: 1000
    state: "present"

# ---------------------------------------------------------------------------
# Delete a DCD metric backend connection
# ---------------------------------------------------------------------------

- name: "Delete a DCD metric backend connection."
  checkmk.general.dcd_metricbackend:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    dcd_config:
      dcd_id: "my_metric_backend_dcd"
    state: "absent"

# ---------------------------------------------------------------------------
# Using environment variables for authentication
# ---------------------------------------------------------------------------
# Connection parameters can be provided via environment variables instead of
# task parameters. The supported variables are:
#   CHECKMK_VAR_SERVER_URL, CHECKMK_VAR_SITE,
#   CHECKMK_VAR_API_USER, CHECKMK_VAR_API_SECRET,
#   CHECKMK_VAR_VALIDATE_CERTS

- name: "Create a DCD metric backend connection using environment variables."
  checkmk.general.dcd_metricbackend:
    dcd_config:
      dcd_id: "my_metric_backend_dcd"
      title: "My Metric Backend Connection"
      site: "mysite"
      connector:
        connector_type: "metric_backend"
        creation_rules:
          - folder_path: "/"
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
    description: The output message that the module generates.
    type: str
    returned: always
    sample: 'DCD metric backend connection created.'
http_code:
    description: The HTTP code the Checkmk API returned.
    type: int
    returned: always
    sample: 200
"""

import json
import re

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.checkmk.general.plugins.module_utils.api import CheckmkAPI
from ansible_collections.checkmk.general.plugins.module_utils.differ import (
    ConfigDiffer,
    prune_to_shape,
)
from ansible_collections.checkmk.general.plugins.module_utils.logger import Logger
from ansible_collections.checkmk.general.plugins.module_utils.utils import (
    base_argument_spec,
    exit_module,
)
from ansible_collections.checkmk.general.plugins.module_utils.version import (
    CheckmkVersion,
)

logger = Logger()

# Minimum Checkmk version that supports the host_name_lookup_rules connector
# field. Older versions use a flat connector shape (top-level attribute filters
# plus a single host_name_resource_attribute_key), so the lookup rules are
# translated down to it (see DCDMetricBackendAPI._downconvert_lookup_rules).
HOST_NAME_LOOKUP_RULES_MIN_VERSION = "3.0.0"

# Minimum Checkmk version that provides a dedicated DCD metric backend delete
# endpoint. Older versions must fall back to the generic DCD delete endpoint.
DEDICATED_DELETE_MIN_VERSION = "3.0.0"

# A host name template of the exact form "$RESOURCE_ATTR.<key>$" is equivalent to
# the pre-3.0.0 single-key host naming (host_name_resource_attribute_key). This
# mirrors the server-side backward-compat mapping in the metric backend fetcher.
_RESOURCE_ATTR_TEMPLATE = re.compile(r"^\$RESOURCE_ATTR\.(.+)\$$")


def _strip_none(obj):
    """Recursively remove None values from nested dicts/lists (Ansible suboption defaults)."""
    if isinstance(obj, dict):
        return {k: _strip_none(v) for k, v in obj.items() if v is not None}
    elif isinstance(obj, list):
        return [_strip_none(item) for item in obj]
    return obj


_FILTER_KEYS = (
    "resource_attribute_filters",
    "scope_attribute_filters",
    "data_point_attribute_filters",
)


def _normalize_filter_entries(entries):
    """Rename API read-side filter keys to the write-side names, in place."""
    for entry in entries or []:
        if isinstance(entry, dict):
            if "attribute_key" in entry:
                entry["key"] = entry.pop("attribute_key")
            if "attribute_value" in entry:
                entry["value"] = entry.pop("attribute_value")


def _normalize_current_filters(connector):
    """Rename the API's read-side filter keys to the write-side names, in place.

    The metric backend connector accepts attribute filters as ``{key, value}`` on
    create but returns them as ``{attribute_key, attribute_value}`` on read. Without
    this translation the ConfigDiffer would always see a difference (and, with no
    update endpoint available, report an unfixable diff) whenever filters are set.

    Handles both layouts: the pre-3.0.0 flat connector (top-level filter lists) and
    the 3.0.0+ shape (filters nested in each host_name_lookup_rules entry).
    """
    if not isinstance(connector, dict):
        return
    for filter_key in _FILTER_KEYS:
        _normalize_filter_entries(connector.get(filter_key))
    for rule in connector.get("host_name_lookup_rules", []):
        if isinstance(rule, dict):
            for filter_key in _FILTER_KEYS:
                _normalize_filter_entries(rule.get(filter_key))


HTTP_CODES_GET = {
    200: (False, False, "DCD metric backend connection found."),
    404: (False, False, "DCD metric backend connection not found."),
}

HTTP_CODES_CREATE = {
    200: (True, False, "DCD metric backend connection created."),
    201: (True, False, "DCD metric backend connection created."),
}

HTTP_CODES_DELETE = {
    204: (True, False, "DCD metric backend connection deleted."),
}


class DCDMetricBackendAPI(CheckmkAPI):
    def __init__(self, module):
        super().__init__(module)
        self.url = self.url.replace("/api/1.0", "/api/internal")

        self.version = self.getversion()
        dcd_config = self.params.get("dcd_config") or {}
        self.dcd_id = dcd_config.get("dcd_id")
        self.desired = self._build_desired()
        self.state = None
        self.current = {}

        self._get_current()
        self.differ = ConfigDiffer(
            self.desired, prune_to_shape(self.desired, self.current)
        )

    def _build_desired(self):
        dcd_config = self.params.get("dcd_config") or {}
        desired = {
            "dcd_id": self.dcd_id,
            "title": dcd_config.get("title", ""),
            "comment": dcd_config.get("comment", ""),
            "documentation_url": dcd_config.get("documentation_url", ""),
            "disabled": dcd_config.get("disabled", False),
            "site": dcd_config.get("site"),
        }

        connector = dcd_config.get("connector")
        if connector:
            connector = _strip_none(connector)
            self._gate_connector_fields(connector)
            desired["connector"] = connector

        return {k: v for k, v in desired.items() if v is not None}

    def _gate_connector_fields(self, connector):
        """Adapt the connector payload to the target Checkmk version, in place.

        The module exposes the 3.0.0+ ``host_name_lookup_rules`` shape. On older
        versions, whose API uses a flat connector (top-level attribute filters
        plus a single ``host_name_resource_attribute_key``), the lookup rules are
        translated down so the same playbook works on both. Sending the unknown
        field verbatim would otherwise fail validation on create, or produce an
        unfixable diff on an existing connection (the API has no update endpoint).
        """
        if self.version < CheckmkVersion(HOST_NAME_LOOKUP_RULES_MIN_VERSION):
            self._downconvert_lookup_rules(connector)

    def _downconvert_lookup_rules(self, connector):
        """Translate host_name_lookup_rules into the pre-3.0.0 flat connector shape.

        The legacy connector supports only a single host name source and one set
        of attribute filters, so only the first lookup rule can be represented;
        anything that does not map cleanly is dropped with a warning rather than
        sent (which the older API would reject).
        """
        rules = connector.pop("host_name_lookup_rules", None)
        if not rules:
            return

        if len(rules) > 1:
            self.module.warn(
                "Checkmk %s supports only a single host name lookup rule for the "
                "metric backend connector; the first rule was applied and the "
                "remaining %d were ignored." % (self.version, len(rules) - 1)
            )

        rule = rules[0]

        for filter_key in _FILTER_KEYS:
            if filter_key in rule:
                connector[filter_key] = rule[filter_key]

        template = rule.get("host_name_template")
        if template:
            match = _RESOURCE_ATTR_TEMPLATE.match(template)
            if match:
                connector["host_name_resource_attribute_key"] = match.group(1)
            else:
                self.module.warn(
                    "Checkmk %s derives the host name from a single resource "
                    "attribute key and cannot use the host name template '%s'; "
                    "it was ignored." % (self.version, template)
                )

    def _get_current(self):
        result = self._fetch(
            code_mapping=HTTP_CODES_GET,
            endpoint="/objects/dcd_metric_backend/%s" % self.dcd_id,
            method="GET",
            logger=logger,
        )

        if result.http_code == 200:
            self.state = "present"
            try:
                raw = json.loads(result.content)
                self.current = raw.get("extensions", {})
                self.current["dcd_id"] = raw.get("id")
                _normalize_current_filters(self.current.get("connector"))
            except (ValueError, TypeError):
                exit_module(
                    self.module,
                    msg="Failed to decode JSON response from API.",
                    failed=True,
                    logger=logger,
                )
        else:
            self.state = "absent"
            self.current = {}

    def needs_update(self):
        return self.differ.needs_update()

    def create(self):
        return self._fetch(
            code_mapping=HTTP_CODES_CREATE,
            endpoint="/domain-types/dcd_metric_backend/collections/all",
            data=self.desired,
            method="POST",
            logger=logger,
        )

    def delete(self):
        if self.version < CheckmkVersion(DEDICATED_DELETE_MIN_VERSION):
            # The dedicated delete endpoint does not exist before 3.0.0; fall
            # back to the generic DCD delete, which works for all DCD types.
            endpoint = "/objects/dcd/%s" % self.dcd_id
        else:
            endpoint = "/objects/dcd_metric_backend/%s" % self.dcd_id

        return self._fetch(
            code_mapping=HTTP_CODES_DELETE,
            endpoint=endpoint,
            method="DELETE",
            logger=logger,
        )


def run_module():
    argument_spec = base_argument_spec()
    argument_spec.update(
        dcd_config=dict(
            type="dict",
            required=True,
            options=dict(
                dcd_id=dict(type="str", required=True),
                title=dict(type="str", required=False),
                comment=dict(type="str", required=False, default=""),
                documentation_url=dict(type="str", required=False, default=""),
                disabled=dict(type="bool", required=False, default=False),
                site=dict(type="str", required=False),
                connector=dict(
                    type="dict",
                    required=False,
                    options=dict(
                        connector_type=dict(type="str", required=False),
                        interval=dict(type="int", required=False),
                        host_name_lookup_rules=dict(
                            type="list",
                            elements="dict",
                            required=False,
                            options=dict(
                                host_name_template=dict(type="str", required=False),
                                resource_attribute_filters=dict(
                                    type="list",
                                    elements="dict",
                                    required=False,
                                    options=dict(
                                        key=dict(
                                            type="str", required=False, no_log=False
                                        ),
                                        value=dict(type="str", required=False),
                                    ),
                                ),
                                scope_attribute_filters=dict(
                                    type="list",
                                    elements="dict",
                                    required=False,
                                    options=dict(
                                        key=dict(
                                            type="str", required=False, no_log=False
                                        ),
                                        value=dict(type="str", required=False),
                                    ),
                                ),
                                data_point_attribute_filters=dict(
                                    type="list",
                                    elements="dict",
                                    required=False,
                                    options=dict(
                                        key=dict(
                                            type="str", required=False, no_log=False
                                        ),
                                        value=dict(type="str", required=False),
                                    ),
                                ),
                            ),
                        ),
                        creation_rules=dict(
                            type="list",
                            elements="dict",
                            required=False,
                            options=dict(
                                folder_path=dict(type="str", required=True),
                                delete_hosts=dict(type="bool", required=False),
                                host_filters=dict(
                                    type="list", elements="str", required=False
                                ),
                                host_attributes=dict(type="dict", required=False),
                            ),
                        ),
                        discover_on_creation=dict(type="bool", required=False),
                        validity_period=dict(type="int", required=False),
                        maximum_number_of_hosts=dict(type="int", required=False),
                    ),
                ),
            ),
        ),
        state=dict(type="str", default="present", choices=["present", "absent"]),
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    logger.set_loglevel(module._verbosity)

    api = DCDMetricBackendAPI(module)

    desired_state = module.params["state"]

    if desired_state == "absent":
        if api.state == "absent":
            exit_module(
                module,
                msg="DCD metric backend connection already absent.",
                logger=logger,
            )
        else:
            result = api.delete()
            exit_module(module, result=result, logger=logger)
    elif api.state == "absent":
        result = api.create()
        exit_module(module, result=result, logger=logger)
    elif api.needs_update():
        exit_module(
            module,
            msg="DCD metric backend connection cannot be updated via API. "
            "Diff: %s" % str(api.differ.generate_diff()),
            failed=True,
            logger=logger,
        )
    else:
        exit_module(
            module,
            msg="DCD metric backend connection already in the desired state.",
            logger=logger,
        )


def main():
    run_module()


if __name__ == "__main__":
    main()

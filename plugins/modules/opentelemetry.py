#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2025, Robin Gierse <robin.gierse@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: opentelemetry

short_description: Manage OpenTelemetry collector configuration in Checkmk

version_added: "6.4.0"

description:
- Manage OpenTelemetry collector configurations in Checkmk.
- Three configuration types are supported via the C(config_type) parameter.
- C(activation) enables or disables the OpenTelemetry collector for a site.
  Use C(state=enabled) or C(state=disabled) for this type.
- C(prom_scrape) manages Prometheus scrape target configurations (full CRUD).
  Use C(state=present) or C(state=absent) for this type.
- C(receiver) manages OpenTelemetry receiver endpoint configurations (full CRUD).
  Use C(state=present) or C(state=absent) for this type.
- Available in Checkmk Ultimate and Ultimate with multi-tenancy editions only.

extends_documentation_fragment: [checkmk.general.common]

options:
    config_type:
        description: The type of OpenTelemetry configuration to manage.
        required: true
        type: str
        choices: ["activation", "prom_scrape", "receiver"]
    site_id:
        description:
            - The site ID for which to manage the OpenTelemetry configuration.
            - Required for C(config_type=activation).
        required: false
        type: str
    config_id:
        description:
            - The unique identifier for a prometheus scrape or receiver configuration.
            - Required when C(config_type=prom_scrape) or C(config_type=receiver).
        required: false
        type: str
    config:
        description:
            - Configuration options for C(config_type=prom_scrape) or C(config_type=receiver).
            - Required when C(state=present).
        required: false
        type: dict
        suboptions:
            title:
                description:
                    - A human-readable title for the configuration.
                    - Required when C(state=present).
                required: false
                type: str
            disabled:
                description: Set to true to disable this configuration without deleting it.
                required: false
                type: bool
                default: false
            sites:
                description:
                    - The list of sites for which the configuration applies.
                    - Note that only one configuration per site is allowed.
                    - Required when C(state=present).
                required: false
                type: list
                elements: str
            comment:
                description: An optional comment describing this configuration.
                required: false
                type: str
            docu_url:
                description: An optional URL to related documentation.
                required: false
                type: str
            prometheus_scrape_configs:
                description:
                    - List of Prometheus scrape target configurations.
                    - Only used when C(config_type=prom_scrape).
                required: false
                type: list
                elements: dict
                suboptions:
                    job_name:
                        description: The job name, which is translated to a Checkmk host name.
                        required: true
                        type: str
                    scrape_interval:
                        description: How often (in seconds) to scrape the target.
                        required: true
                        type: int
                    metrics_path:
                        description: The URL path to the metrics endpoint.
                        required: true
                        type: str
                    targets:
                        description: The list of scrape target endpoints.
                        required: true
                        type: list
                        elements: dict
                        suboptions:
                            address:
                                description: The host address of the target.
                                required: true
                                type: str
                            port:
                                description: The port of the target.
                                required: true
                                type: int
                    encryption:
                        description: Whether to use TLS encryption for the scrape connection.
                        required: true
                        type: bool
            receiver_protocol_grpc:
                description:
                    - Configuration for the gRPC receiver protocol.
                    - Only used when C(config_type=receiver).
                    - See the Checkmk API documentation for the full structure.
                required: false
                type: dict
            receiver_protocol_http:
                description:
                    - Configuration for the HTTP receiver protocol.
                    - Only used when C(config_type=receiver).
                    - See the Checkmk API documentation for the full structure.
                required: false
                type: dict
    state:
        description:
            - The desired state of the configuration.
            - Use C(enabled) or C(disabled) when C(config_type=activation).
            - Use C(present) or C(absent) when C(config_type=prom_scrape) or C(config_type=receiver).
        required: false
        type: str
        choices: ["present", "absent", "enabled", "disabled"]
        default: "present"

notes:
    - This module uses the Checkmk internal API and requires Checkmk 2.5 or later.

author:
    - Robin Gierse (@robin-checkmk)
"""

EXAMPLES = r"""
# ---------------------------------------------------------------------------
# Manage collector activation
# ---------------------------------------------------------------------------

- name: "Enable the OpenTelemetry collector for a site."
  checkmk.general.opentelemetry:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    config_type: "activation"
    site_id: "mysite"
    state: "enabled"

- name: "Disable the OpenTelemetry collector for a site."
  checkmk.general.opentelemetry:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    config_type: "activation"
    site_id: "mysite"
    state: "disabled"

# ---------------------------------------------------------------------------
# Manage Prometheus scrape configurations
# ---------------------------------------------------------------------------

- name: "Create a Prometheus scrape configuration."
  checkmk.general.opentelemetry:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    config_type: "prom_scrape"
    config_id: "my_prom_scrape"
    config:
      title: "My Prometheus Scrape"
      disabled: false
      sites:
        - "mysite"
      prometheus_scrape_configs:
        - job_name: "my_service"
          scrape_interval: 60
          metrics_path: "/metrics"
          targets:
            - address: "192.168.1.10"
              port: 9090
          encryption: false
    state: "present"

- name: "Delete a Prometheus scrape configuration."
  checkmk.general.opentelemetry:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    config_type: "prom_scrape"
    config_id: "my_prom_scrape"
    state: "absent"

# ---------------------------------------------------------------------------
# Manage receiver configurations
# ---------------------------------------------------------------------------

- name: "Create an OpenTelemetry receiver configuration using gRPC."
  checkmk.general.opentelemetry:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    config_type: "receiver"
    config_id: "my_receiver"
    config:
      title: "My OTel Receiver"
      disabled: false
      sites:
        - "mysite"
      receiver_protocol_grpc:
        endpoint:
          auth:
            type: "none"
          socket_address:
            type: "default_ipv4"
            port: 4317
          event_console: null
          encryption: false
    state: "present"

- name: "Create an OpenTelemetry receiver configuration using HTTP."
  checkmk.general.opentelemetry:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    config_type: "receiver"
    config_id: "my_receiver"
    config:
      title: "My OTel Receiver"
      disabled: false
      sites:
        - "mysite"
      receiver_protocol_http:
        endpoint:
          auth:
            type: "none"
          socket_address:
            type: "default_ipv4"
            port: 4318
          event_console: null
          encryption: false
    state: "present"

- name: "Create an OpenTelemetry receiver configuration using both gRPC and HTTP."
  checkmk.general.opentelemetry:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    config_type: "receiver"
    config_id: "my_receiver"
    config:
      title: "My OTel Receiver"
      disabled: false
      sites:
        - "mysite"
      receiver_protocol_grpc:
        endpoint:
          auth:
            type: "none"
          socket_address:
            type: "default_ipv4"
          event_console: null
          encryption: false
      receiver_protocol_http:
        endpoint:
          auth:
            type: "none"
          socket_address:
            type: "default_ipv4"
          event_console: null
          encryption: false
    state: "present"

- name: "Delete a receiver configuration."
  checkmk.general.opentelemetry:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    config_type: "receiver"
    config_id: "my_receiver"
    state: "absent"

# ---------------------------------------------------------------------------
# Using environment variables for authentication
# ---------------------------------------------------------------------------
# Connection parameters can be provided via environment variables instead of
# task parameters. The supported variables are:
#   CHECKMK_VAR_SERVER_URL, CHECKMK_VAR_SITE,
#   CHECKMK_VAR_API_USER, CHECKMK_VAR_API_SECRET,
#   CHECKMK_VAR_VALIDATE_CERTS

- name: "Enable the OpenTelemetry collector using environment variables."
  checkmk.general.opentelemetry:
    config_type: "activation"
    site_id: "mysite"
    state: "enabled"
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
    sample: 'OpenTelemetry configuration created.'
http_code:
    description: The HTTP code the Checkmk API returned.
    type: int
    returned: always
    sample: 200
"""

import json

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six.moves.urllib.parse import urlencode
from ansible_collections.checkmk.general.plugins.module_utils.api import CheckmkAPI
from ansible_collections.checkmk.general.plugins.module_utils.differ import (
    ConfigDiffer,
    prune_to_shape,
)
from ansible_collections.checkmk.general.plugins.module_utils.logger import Logger
from ansible_collections.checkmk.general.plugins.module_utils.types import (
    generate_result,
)
from ansible_collections.checkmk.general.plugins.module_utils.utils import (
    base_argument_spec,
    exit_module,
)

logger = Logger()

HTTP_CODES_ACTIVATION = {
    204: (True, False, "OpenTelemetry collector activation updated."),
}

HTTP_CODES_GET = {
    200: (False, False, "OK"),
}

HTTP_CODES_CREATE = {
    200: (True, False, "OpenTelemetry configuration created."),
}

HTTP_CODES_UPDATE = {
    200: (True, False, "OpenTelemetry configuration updated."),
}

HTTP_CODES_DELETE = {
    204: (True, False, "OpenTelemetry configuration deleted."),
}

_PROM_SCRAPE = "prom_scrape"
_RECEIVER = "receiver"

_ENDPOINTS = {
    _PROM_SCRAPE: {
        "collection": "/domain-types/otel_collector_config_prom_scrape/collections/all",
        "object": "/objects/otel_collector_config_prom_scrape",
    },
    _RECEIVER: {
        "collection": "/domain-types/otel_collector_config_receivers/collections/all",
        "object": "/objects/otel_collector_config_receivers",
    },
}

_CONFIG_FIELDS = {
    _PROM_SCRAPE: [
        "title",
        "disabled",
        "sites",
        "comment",
        "docu_url",
        "prometheus_scrape_configs",
    ],
    _RECEIVER: [
        "title",
        "disabled",
        "sites",
        "comment",
        "docu_url",
        "receiver_protocol_grpc",
        "receiver_protocol_http",
    ],
}

_PARAM_TO_API = {
    "sites": "site",
}


class OTelActivationAPI(CheckmkAPI):
    def __init__(self, module):
        super().__init__(module)
        self.url = self.url.replace("/api/1.0", "/api/internal")

    def _get_current_mode(self):
        query = urlencode({"site_id": self.params.get("site_id")})
        result = self._fetch(
            code_mapping=HTTP_CODES_GET,
            endpoint="/domain-types/otel_collector/actions/get/invoke?%s" % query,
            method="GET",
            logger=logger,
        )

        try:
            return json.loads(result.content).get("activation", {}).get("mode")
        except (ValueError, TypeError):
            return None

    def update(self):
        data = {
            "site_id": self.params.get("site_id"),
            "activation": {"mode": self.params.get("state")},
        }

        return self._fetch(
            code_mapping=HTTP_CODES_ACTIVATION,
            endpoint="/domain-types/otel_collector/actions/update/invoke",
            data=data,
            method="PUT",
            logger=logger,
        )

    def run(self):
        if self._get_current_mode() == self.params.get("state"):
            return generate_result(
                msg="OpenTelemetry collector activation already in the desired state.",
                http_code=0,
                failed=False,
            )

        return self.update()


class OTelConfigAPI(CheckmkAPI):
    def __init__(self, module, config_type):
        super().__init__(module)
        self.url = self.url.replace("/api/1.0", "/api/internal")
        self.config_type = config_type
        self.endpoints = _ENDPOINTS[config_type]

    def _get_existing(self, config_id):
        result = self._fetch(
            code_mapping=HTTP_CODES_GET,
            endpoint=self.endpoints["collection"],
            method="GET",
            logger=logger,
        )

        try:
            data = json.loads(result.content)
        except (ValueError, TypeError):
            return None

        for obj in data.get("value", []):
            if obj.get("id") == config_id:
                return obj

        return None

    def _build_data(self, include_id=True):
        data = {}
        if include_id:
            data["id"] = self.params.get("config_id")

        config = self.params.get("config") or {}
        for field in _CONFIG_FIELDS[self.config_type]:
            value = config.get(field)
            if value is not None:
                api_field = _PARAM_TO_API.get(field, field)
                data[api_field] = value

        return data

    def _needs_update(self, existing):
        extensions = existing.get("extensions", {})
        desired = self._build_data(include_id=False)
        pruned = prune_to_shape(desired, extensions)
        return ConfigDiffer(desired, pruned).needs_update()

    def create(self):
        return self._fetch(
            code_mapping=HTTP_CODES_CREATE,
            endpoint=self.endpoints["collection"],
            data=self._build_data(include_id=True),
            method="POST",
            logger=logger,
        )

    def update(self, config_id):
        # The internal API requires an If-Match header for this operation,
        # but never exposes an ETag for these objects, so "*" (match any
        # existing object) is the only value we can send.
        self.headers["If-Match"] = "*"
        return self._fetch(
            code_mapping=HTTP_CODES_UPDATE,
            endpoint="%s/%s" % (self.endpoints["object"], config_id),
            data=self._build_data(include_id=True),
            method="PUT",
            logger=logger,
        )

    def delete(self, config_id):
        self.headers["If-Match"] = "*"
        return self._fetch(
            code_mapping=HTTP_CODES_DELETE,
            endpoint="%s/%s" % (self.endpoints["object"], config_id),
            method="DELETE",
            logger=logger,
        )

    def run(self):
        config_id = self.params.get("config_id")
        state = self.params.get("state", "present")
        existing = self._get_existing(config_id)

        if state == "present":
            if existing is None:
                return self.create()
            elif self._needs_update(existing):
                return self.update(config_id)
            else:
                return generate_result(
                    msg="OpenTelemetry configuration already in the desired state.",
                    http_code=0,
                    failed=False,
                )

        elif state == "absent":
            if existing is not None:
                return self.delete(config_id)
            else:
                return generate_result(
                    msg="OpenTelemetry configuration already absent.",
                    http_code=0,
                    failed=False,
                )


def run_module():
    argument_spec = base_argument_spec()
    argument_spec.update(
        config_type=dict(
            type="str",
            required=True,
            choices=["activation", "prom_scrape", "receiver"],
        ),
        site_id=dict(type="str", required=False),
        config_id=dict(type="str", required=False),
        config=dict(
            type="dict",
            required=False,
            options=dict(
                title=dict(type="str", required=False),
                disabled=dict(type="bool", required=False, default=False),
                sites=dict(type="list", elements="str", required=False),
                comment=dict(type="str", required=False),
                docu_url=dict(type="str", required=False),
                prometheus_scrape_configs=dict(
                    type="list",
                    elements="dict",
                    required=False,
                    options=dict(
                        job_name=dict(type="str", required=True),
                        scrape_interval=dict(type="int", required=True),
                        metrics_path=dict(type="str", required=True),
                        targets=dict(
                            type="list",
                            elements="dict",
                            required=True,
                            options=dict(
                                address=dict(type="str", required=True),
                                port=dict(type="int", required=True),
                            ),
                        ),
                        encryption=dict(type="bool", required=True),
                    ),
                ),
                receiver_protocol_grpc=dict(type="dict", required=False),
                receiver_protocol_http=dict(type="dict", required=False),
            ),
        ),
        state=dict(
            type="str",
            default="present",
            choices=["present", "absent", "enabled", "disabled"],
        ),
    )

    required_if = [
        ("config_type", "activation", ["site_id"]),
        ("config_type", "prom_scrape", ["config_id"]),
        ("config_type", "receiver", ["config_id"]),
    ]

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=False,
        required_if=required_if,
    )

    logger.set_loglevel(module._verbosity)
    config_type = module.params.get("config_type")
    state = module.params.get("state")

    if config_type == "activation" and state not in ("enabled", "disabled"):
        module.fail_json(
            msg="config_type=activation requires state to be 'enabled' or 'disabled', got '%s'."
            % state
        )

    if config_type in (_PROM_SCRAPE, _RECEIVER) and state not in ("present", "absent"):
        module.fail_json(
            msg="config_type=%s requires state to be 'present' or 'absent', got '%s'."
            % (config_type, state)
        )

    if config_type == "activation":
        api = OTelActivationAPI(module)
    else:
        api = OTelConfigAPI(module, config_type)

    exit_module(module, result=api.run(), logger=logger)


def main():
    run_module()


if __name__ == "__main__":
    main()

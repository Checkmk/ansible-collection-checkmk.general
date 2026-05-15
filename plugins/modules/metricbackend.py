#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2025, Robin Gierse <robin.gierse@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: metricbackend

short_description: Manage the Metric Backend configuration in Checkmk

version_added: "6.4.0"

description:
- Configure the Metric Backend for a specific site in Checkmk.
- The Metric Backend can be enabled or disabled, and its ports and memory usage can be configured.
- B(Note:) This module always applies the provided configuration. Since the API does not expose
  a read endpoint, C(changed) will always be reported on every successful run.
- Available in Checkmk Ultimate and Ultimate with multi-tenancy editions only.

extends_documentation_fragment: [checkmk.general.common]

options:
    site_id:
        description: The ID of the site for which to configure the metric backend.
        required: true
        type: str
    config:
        description: The metric backend configuration.
        required: true
        type: dict
        suboptions:
            type:
                description: Whether to enable or disable the metric backend.
                required: true
                type: str
                choices: ["enabled", "disabled"]
            tls_port:
                description:
                    - The port for TLS traffic.
                    - Omit to keep the current value or use the site-specific default on first enable.
                required: false
                type: int
            https_port:
                description:
                    - The port for HTTPS traffic.
                    - Omit to keep the current value or use the site-specific default on first enable.
                required: false
                type: int
            http_port:
                description:
                    - The HTTP port for the metric backend web UI.
                    - Omit to keep the current value or leave unset when previously disabled.
                required: false
                type: int
            relative_memory_limit_percentage:
                description:
                    - Maximum memory the metric backend may use, as a percentage of total available memory.
                    - Valid range is 1.0 to 200.0.
                    - Omit to keep the current value or use the default on first enable.
                required: false
                type: float

notes:
    - This module uses the Checkmk internal API and requires Checkmk 2.5 or later.

author:
    - Robin Gierse (@robin-checkmk)
"""

EXAMPLES = r"""
# ---------------------------------------------------------------------------
# Enable the Metric Backend
# ---------------------------------------------------------------------------

- name: "Enable the Metric Backend for a site."
  checkmk.general.metricbackend:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    site_id: "mysite"
    config:
      type: "enabled"

- name: "Enable the Metric Backend with custom ports and memory limit."
  checkmk.general.metricbackend:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    site_id: "mysite"
    config:
      type: "enabled"
      tls_port: 6790
      https_port: 6791
      http_port: 6792
      relative_memory_limit_percentage: 50.0

# ---------------------------------------------------------------------------
# Disable the Metric Backend
# ---------------------------------------------------------------------------

- name: "Disable the Metric Backend for a site."
  checkmk.general.metricbackend:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    site_id: "mysite"
    config:
      type: "disabled"

# ---------------------------------------------------------------------------
# Using environment variables for authentication
# ---------------------------------------------------------------------------
# Connection parameters can be provided via environment variables instead of
# task parameters. The supported variables are:
#   CHECKMK_VAR_SERVER_URL, CHECKMK_VAR_SITE,
#   CHECKMK_VAR_API_USER, CHECKMK_VAR_API_SECRET,
#   CHECKMK_VAR_VALIDATE_CERTS

- name: "Enable the Metric Backend using environment variables for authentication."
  checkmk.general.metricbackend:
    site_id: "mysite"
    config:
      type: "enabled"
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
    sample: 'Metric backend configuration updated.'
http_code:
    description: The HTTP code the Checkmk API returned.
    type: int
    returned: always
    sample: 204
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.checkmk.general.plugins.module_utils.api import CheckmkAPI
from ansible_collections.checkmk.general.plugins.module_utils.logger import Logger
from ansible_collections.checkmk.general.plugins.module_utils.utils import (
    base_argument_spec,
    exit_module,
)

logger = Logger()

HTTP_CODES_UPDATE = {
    204: (True, False, "Metric backend configuration updated."),
}


class MetricBackendAPI(CheckmkAPI):
    def __init__(self, module):
        super().__init__(module)
        self.url = self.url.replace("/api/1.0", "/api/internal")

    def update(self):
        config = self.params.get("config") or {}
        data = {
            "site_id": self.params.get("site_id"),
            "config": {k: v for k, v in config.items() if v is not None},
        }

        return self._fetch(
            code_mapping=HTTP_CODES_UPDATE,
            endpoint="/domain-types/metric_backend/actions/update/invoke",
            data=data,
            method="PATCH",
            logger=logger,
        )


def run_module():
    argument_spec = base_argument_spec()
    argument_spec.update(
        site_id=dict(type="str", required=True),
        config=dict(
            type="dict",
            required=True,
            options=dict(
                type=dict(type="str", required=True, choices=["enabled", "disabled"]),
                tls_port=dict(type="int", required=False),
                https_port=dict(type="int", required=False),
                http_port=dict(type="int", required=False),
                relative_memory_limit_percentage=dict(type="float", required=False),
            ),
        ),
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    logger.set_loglevel(module._verbosity)

    api = MetricBackendAPI(module)
    result = api.update()
    exit_module(module, result=result, logger=logger)


def main():
    run_module()


if __name__ == "__main__":
    main()

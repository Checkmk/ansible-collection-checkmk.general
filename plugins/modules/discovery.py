#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2022 - 2025,
#   Michael Sekania &
#   Robin Gierse <robin.gierse@checkmk.com> &
#   Max Sickora <max.sickora@checkmk.com> &
#   Lars Getwan <lars.getwan@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: discovery

short_description: Discover services in Checkmk

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "0.0.1"

description:
- Discovery services within Checkmk.

extends_documentation_fragment: [checkmk.general.common]

options:
    host_name:
        description: The host who's services you want to manage. Mutually exclusive with hosts.
        required: false
        type: str
    hosts:
        description:
            - The list of hosts the services of which you want to manage.
              Mutually exclusive with host_name. This enables bulk discovery mode.
        required: false
        type: list
        elements: str
        default: []
    state:
        description:
            - The action to perform during discovery.
            - Not all choices are available with all Checkmk versions.
            - Check the ReDoc documentation in your site for details.
            - In versions 2.4.0 and newer, the modes tabula_rasa and refresh are no longer available,
            - in that case, we perform a add/remove all services and labels, instead.
        required: false
        type: str
        default: new
        choices: [new, remove, fix_all, refresh, tabula_rasa, only_host_labels, only_service_labels, monitor_undecided_services]
    do_full_scan:
        description: The option whether to perform a full scan or not. (Bulk mode only).
        required: false
        type: bool
        default: True
    bulk_size:
        description: The number of hosts to be handled at once. (Bulk mode only).
        required: false
        type: int
        default: 1
    ignore_errors:
        description: The option whether to ignore errors in single check plugins. (Bulk mode only).
        required: false
        type: bool
        default: True
    wait_for_completion:
        description: If true, wait for the discovery to finish.
        required: false
        type: bool
        default: True
    wait_for_previous:
        description: If true, wait for previously running discovery jobs to finish.
        required: false
        type: bool
        default: True
    wait_timeout:
        description:
            - The time in seconds to wait for (previous/current) completion.
            - Default is -1, which means infinite.
        required: false
        type: int
        default: -1


notes:
    - Discovery does not automatically activate changes. Run C(checkmk.general.activation)
      after discovery to apply the discovered services.
    - When using C(hosts) (bulk mode), hosts are processed in batches controlled by C(bulk_size).
      A larger C(bulk_size) is faster but may put more load on the Checkmk server.

seealso:
    - module: checkmk.general.host

author:
    - Robin Gierse (@robin-checkmk)
    - Michael Sekania (@msekania)
    - Max Sickora (@max-checkmk)
    - Lars Getwan (@lgetwan)
"""

EXAMPLES = r"""
# ---------------------------------------------------------------------------
# Single host discovery
# ---------------------------------------------------------------------------

- name: "Add newly discovered services on a host."
  checkmk.general.discovery:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    host_name: "myhost"
    state: "new"

- name: "Add newly discovered services, update labels, and remove vanished services on a host."
  checkmk.general.discovery:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    host_name: "myhost"
    state: "fix_all"

- name: "Remove all vanished services from a host."
  checkmk.general.discovery:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    host_name: "myhost"
    state: "remove"

- name: "Discover only host labels on a host."
  checkmk.general.discovery:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    host_name: "myhost"
    state: "only_host_labels"

- name: "Discover only service labels on a host."
  checkmk.general.discovery:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    host_name: "myhost"
    state: "only_service_labels"

- name: "Move all undecided services to monitored on a host."
  checkmk.general.discovery:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    host_name: "myhost"
    state: "monitor_undecided_services"

# ---------------------------------------------------------------------------
# Bulk discovery
# ---------------------------------------------------------------------------

- name: "Add newly discovered services on multiple hosts."
  checkmk.general.discovery:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    hosts:
      - "myhost01"
      - "myhost02"
    state: "new"

- name: "Add newly discovered services, update labels, and remove vanished services on multiple hosts."
  checkmk.general.discovery:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    hosts:
      - "myhost01"
      - "myhost02"
    state: "fix_all"

- name: "Bulk discovery with a timeout of 30 seconds."
  checkmk.general.discovery:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    hosts:
      - "myhost01"
      - "myhost02"
    state: "new"
    wait_timeout: 30

- name: "Bulk discovery processing 3 hosts at a time."
  checkmk.general.discovery:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    hosts:
      - "myhost01"
      - "myhost02"
      - "myhost03"
      - "myhost04"
      - "myhost05"
      - "myhost06"
    state: "fix_all"
    bulk_size: 3

- name: "Start bulk discovery without waiting for completion."
  checkmk.general.discovery:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    hosts:
      - "myhost01"
      - "myhost02"
    state: "fix_all"
    wait_for_completion: false

# ---------------------------------------------------------------------------
# Using environment variables for authentication
# ---------------------------------------------------------------------------
# Connection parameters can be provided via environment variables instead of
# task parameters. The supported variables are:
#   CHECKMK_VAR_SERVER_URL, CHECKMK_VAR_SITE,
#   CHECKMK_VAR_API_USER, CHECKMK_VAR_API_SECRET,
#   CHECKMK_VAR_VALIDATE_CERTS

- name: "Add newly discovered services using environment variables for authentication."
  checkmk.general.discovery:
    host_name: "myhost"
    state: "new"
  environment:
    CHECKMK_VAR_SERVER_URL: "https://myserver/"
    CHECKMK_VAR_SITE: "mysite"
    CHECKMK_VAR_API_USER: "myuser"
    CHECKMK_VAR_API_SECRET: "mysecret"
    CHECKMK_VAR_VALIDATE_CERTS: "false"
"""

RETURN = r"""
http_code:
    description: The HTTP code the Checkmk API returns.
    type: int
    returned: always
    sample: '200'
msg:
    description: The output message that the module generates.
    type: str
    returned: always
    sample: 'Discovery started.'
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.checkmk.general.plugins.module_utils.api import CheckmkAPI
from ansible_collections.checkmk.general.plugins.module_utils.discovery_210 import (
    Discovery210,
)
from ansible_collections.checkmk.general.plugins.module_utils.discovery_220 import (
    Discovery220,
)
from ansible_collections.checkmk.general.plugins.module_utils.discovery_230 import (
    Discovery230,
)
from ansible_collections.checkmk.general.plugins.module_utils.discovery_240 import (
    Discovery240,
)
from ansible_collections.checkmk.general.plugins.module_utils.discovery_250 import (
    Discovery250,
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

AVAILABLE_API_VERSIONS = [
    # Let's try the newest Version, first.
    Discovery250,
    Discovery240,
    Discovery230,
    Discovery220,
    Discovery210,
]


def run_module():
    argument_spec = base_argument_spec()
    argument_spec.update(
        host_name=dict(type="str", required=False),
        hosts=dict(type="list", elements="str", required=False, default=[]),
        state=dict(
            type="str",
            default="new",
            choices=[
                "new",
                "remove",
                "fix_all",
                "refresh",
                "tabula_rasa",
                "only_host_labels",
                "only_service_labels",
                "monitor_undecided_services",
            ],
        ),
        do_full_scan=dict(type="bool", default=True),
        bulk_size=dict(type="int", default=1),
        ignore_errors=dict(type="bool", default=True),
        wait_for_completion=dict(type="bool", default=True),
        wait_for_previous=dict(type="bool", default=True),
        wait_timeout=dict(type="int", default=-1),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=[
            ("host_name", "hosts"),
        ],
        required_one_of=[
            ("host_name", "hosts"),
        ],
        supports_check_mode=False,
    )

    logger.set_loglevel(module._verbosity)
    result = generate_result(
        http_code=0,
        msg="Nothing to be done",
        failed=False,
    )

    version = CheckmkAPI(module, logger).getversion()
    logger.debug("Version found: %s" % str(version))
    discovery = None

    # Find a submodule compatible to the RESP API's version
    for api in AVAILABLE_API_VERSIONS:
        logger.debug("Checking compatibility with %s" % str(api))
        if api(module, logger).compatible(version):
            discovery = api(module, logger)
            break

    if not discovery:
        exit_module(
            module,
            msg="Version %s is not supported by this module" % version,
            failed=True,
            logger=logger,
        )

    result = discovery.start_discovery()

    exit_module(
        module,
        result=result,
        logger=logger,
    )


def main():
    run_module()


if __name__ == "__main__":
    main()

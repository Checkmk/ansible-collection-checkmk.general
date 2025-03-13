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

short_description: Discover services in Checkmk.

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
        type: str
        default: new
        choices: [new, remove, fix_all, refresh, tabula_rasa, only_host_labels, only_service_labels, monitor_undecided_services]
    do_full_scan:
        description: The option whether to perform a full scan or not. (Bulk mode only).
        type: bool
        default: True
    bulk_size:
        description: The number of hosts to be handled at once. (Bulk mode only).
        type: int
        default: 1
    ignore_errors:
        description: The option whether to ignore errors in single check plugins. (Bulk mode only).
        type: bool
        default: True
    wait_for_completion:
        description: If true, wait for the discovery to finish.
        type: bool
        default: True
    wait_for_previous:
        description: If true, wait for previously running discovery jobs to finish.
        type: bool
        default: True
    wait_timeout:
        description:
            - The time in seconds to wait for (previous/current) completion.
            - Default is -1, which means infinite.
        type: int
        default: -1


author:
    - Robin Gierse (@robin-checkmk)
    - Michael Sekania (@msekania)
    - Max Sickora (@max-checkmk)
    - Lars Getwan (@lgetwan)
"""

EXAMPLES = r"""
# Create a single host.
- name: "Add newly discovered services on host."
  checkmk.general.discovery:
    server_url: "http://myserver/"
    site: "mysite"
    automation_user: "myuser"
    automation_secret: "mysecret"
    host_name: "my_host"
    state: "new"
- name: "Add newly discovered services, update labels and remove vanished services on host."
  checkmk.general.discovery:
    server_url: "http://myserver/"
    site: "mysite"
    automation_user: "myuser"
    automation_secret: "mysecret"
    host_name: "my_host"
    state: "fix_all"
- name: "Add newly discovered services on hosts and wait up to 30s for finishing. (Bulk)"
  checkmk.general.discovery:
    server_url: "http://myserver/"
    site: "mysite"
    automation_user: "myuser"
    automation_secret: "mysecret"
    hosts: ["my_host_0", "my_host_1"]
    wait_timeout: 30
    state: "new"
- name: "Tabula rasa, the bulk way."
  checkmk.general.discovery:
    server_url: "http://myserver/"
    site: "mysite"
    automation_user: "myuser"
    automation_secret: "mysecret"
    hosts: ["my_host_0", "my_host_1"]
    wait_for_completion: false
    state: "tabula_rasa"
- name: "Add newly discovered services, update labels and remove vanished services on host; 3 at once (Bulk)"
  checkmk.general.discovery:
    server_url: "http://myserver/"
    site: "mysite"
    automation_user: "myuser"
    automation_secret: "mysecret"
    hosts: ["my_host_0", "my_host_1", "my_host_2", "my_host_3", "my_host_4", "my_host_5"]
    state: "fix_all"
    bulk_size: 3
"""

RETURN = r"""
http_code:
    description: The HTTP code the Checkmk API returns.
    type: int
    returned: always
    sample: '200'
message:
    description: The output message that the module generates.
    type: str
    returned: always
    sample: 'Host created.'
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
from ansible_collections.checkmk.general.plugins.module_utils.logger import Logger
from ansible_collections.checkmk.general.plugins.module_utils.types import (
    generate_result,
)
from ansible_collections.checkmk.general.plugins.module_utils.utils import exit_module

logger = Logger()

AVAILABLE_API_VERSIONS = [
    # Let's try the newest Version, first.
    Discovery240,
    Discovery230,
    Discovery220,
    Discovery210,
]


def run_module():
    module_args = dict(
        server_url=dict(type="str", required=True),
        site=dict(type="str", required=True),
        validate_certs=dict(type="bool", required=False, default=True),
        automation_user=dict(type="str", required=True),
        automation_secret=dict(type="str", required=True, no_log=True),
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
        argument_spec=module_args,
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

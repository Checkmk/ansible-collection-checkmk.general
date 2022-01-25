#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2022, Robin Gierse <robin.gierse@tribe29.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: activation

short_description: Activate changes in Checkmk.

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "0.0.1"

description:
- Activate changes within Checkmk.

extends_documentation_fragment: [tribe29.checkmk.common]

options:
    sites:
        description: The sites that should be activated.
        required: true
        type: str
    force_foreign_changes:
        description: Wheather to active foreign changes.
        default: false
        type: bool

author:
    - Robin Gierse (@robin-tribe29)
'''

EXAMPLES = r'''
# Pass in a message
- name: "Activate changes."
  tribe29.checkmk.activation:
      server_url: "http://localhost/"
      site: "my_site"
      automation_user: "automation"
      automation_secret: "$SECRET"
      force_foreign_changes: 'true'
      sites: "test"
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
http_code:
    description: The HTTP code the Checkmk API returns.
    type: int
    returned: always
    sample: '200'
message:
    description: The output message that the module generates.
    type: str
    returned: always
    sample: 'Changes activated.'
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        server_url=dict(type='str', required=True),
        site=dict(type='str', required=True),
        automation_user=dict(type='str', required=True),
        automation_secret=dict(type='str', required=True, no_log=True),
        sites=dict(type='str', required=True),
        force_foreign_changes=dict(type='bool', default=False),
    )

    result = dict(changed=False, failed=False, http_code='', msg='')

    module = AnsibleModule(argument_spec=module_args,
                           supports_check_mode=False)

    if module.params['force_foreign_changes'] is None:
        module.params['force_foreign_changes'] = False
    if module.params['sites'] is None:
        module.params['sites'] = {
        }  # ToDo: How to pass empty array of strings?

    changed = False
    failed = False
    http_code = ''
    server_url = module.params['server_url']
    site = module.params['site']
    automation_user = module.params['automation_user']
    automation_secret = module.params['automation_secret']
    sites = module.params['sites']
    force_foreign_changes = module.params['force_foreign_changes']

    http_code_mapping = {
        # http_code: (changed, failed, "Message")
        200: (True, False, "Changes activated."),
        204: (True, False, "Changes activated."),
        302: (True, False, "Redirected."),
        422: (False, False, "There are no changes to be activated."),
        400: (False, True, "Bad Request."),
        401:
        (False, True,
         "Unauthorized: There are foreign changes, which you may not activate, or you did not use <force_foreign_changes>."
         ),
        403: (False, True, "Forbidden: Configuration via WATO is disabled."),
        406: (False, True, "Not Acceptable."),
        409: (False, True, "Conflict: Some sites could not be activated."),
        415: (False, True, "Unsupported Media Type."),
        423: (False, True, "Locked: There is already an activation running."),
    }

    # Declare headers including authentication to send to the Checkmk API
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + automation_user + ' ' + automation_secret
    }

    params = {
        'force_foreign_changes': force_foreign_changes,
        'redirect':
        True,  # ToDo: Do we need this? Does it need to be configurable?
        # ToDo: make sites list iterable
        # 'sites': {
        #     'sitename'
        # }
    }

    api_endpoint = '/domain-types/activation_run/actions/activate-changes/invoke'
    url = server_url + site + "/check_mk/api/1.0" + api_endpoint
    response, info = fetch_url(module,
                               url,
                               module.jsonify(params),
                               headers=headers,
                               method='POST')
    http_code = info['status']

    # Kudos to Lars G.!
    if http_code in http_code_mapping.keys():
        changed, failed, msg = http_code_mapping[http_code]
    else:
        changed, failed, msg = (False, True, 'Error calling API')

    result['msg'] = msg
    result['changed'] = changed
    result['failed'] = failed
    result['http_code'] = http_code

    if result['failed']:
        module.fail_json(**result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()

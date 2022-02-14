#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2022, Robin Gierse <robin.gierse@tribe29.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: host

short_description: Manage hosts in Checkmk.

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "0.0.1"

description:
- Create and delete hosts within Checkmk.

extends_documentation_fragment: [tribe29.checkmk.common]

options:
    host_name:
        description: The host you want to manage.
        required: true
        type: str
    folder:
        description: The folder your host is located in.
        type: str
        default: /
    state:
        description: The state of your host.
        type: str
        default: present
        choices: [present, absent]

author:
    - Robin Gierse (@robin-tribe29)
'''

EXAMPLES = r'''
# Create a single host.
- name: "Create a single host."
  tribe29.checkmk.host:
    server_url: "http://localhost/"
    site: "local"
    automation_user: "automation"
    automation_secret: "$SECRET"
    host_name: "my_host"
    ip_address: "x.x.x.x"
    folder: "/"
    state: "present"
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
    sample: 'Host created.'
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
        host_name=dict(type='str', required=True),
        ip_address=dict(type='str'),
        folder=dict(type='str', required=True),
        state=dict(type='str', choices=['present', 'absent']),
    )

    result = dict(changed=False, failed=False, http_code='', msg='')

    module = AnsibleModule(argument_spec=module_args,
                           supports_check_mode=False)

    if module.params['folder'] is None:
        module.params['folder'] = '/'
    if module.params['state'] is None:
        module.params['state'] = 'present'

    changed = False
    failed = False
    http_code = ''
    server_url = module.params['server_url']
    site = module.params['site']
    automation_user = module.params['automation_user']
    automation_secret = module.params['automation_secret']
    host_name = module.params['host_name']
    folder = module.params['folder']
    state = module.params['state']

    # Declare headers including authentication to send to the Checkmk API
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + automation_user + ' ' + automation_secret
    }

    # Check whether the host exists
    api_endpoint = '/objects/host_config/' + host_name
    url = server_url + site + "/check_mk/api/1.0" + api_endpoint
    response, info = fetch_url(module,
                               url,
                               data=None,
                               headers=headers,
                               method='GET')
    http_code = info['status']
    if http_code == 200:
        host_state = 'present'
    elif http_code == 404:
        host_state = 'absent'
    else:
        msg = 'Error calling API.'
        failed = True

    # Handle the host accordingly to above findings and desired state
    if state == 'present' and host_state == 'present':
        msg = "Host already present."

    elif state == 'present' and host_state == 'absent':
        api_endpoint = '/domain-types/host_config/collections/all'
        params = {
            'folder': folder,
            'host_name': host_name,
            'attributes': {
                'ipaddress': ip_address or '127.0.0.1'
            }
        }
        url = server_url + site + "/check_mk/api/1.0" + api_endpoint

        response, info = fetch_url(module,
                                   url,
                                   module.jsonify(params),
                                   headers=headers,
                                   method='POST')
        http_code = info['status']
        if http_code == 200:
            changed = True
            msg = "Host created."
        else:
            msg = 'Error calling API.'
            failed = True

    elif state == 'absent' and host_state == 'absent':
        msg = "Host already absent."

    elif state == 'absent' and host_state == 'present':
        api_endpoint = '/objects/host_config/' + host_name
        url = server_url + site + "/check_mk/api/1.0" + api_endpoint
        response, info = fetch_url(module,
                                   url,
                                   data=None,
                                   headers=headers,
                                   method='DELETE')
        http_code = info['status']
        if http_code == 204:
            changed = True
            msg = "Host deleted."
        else:
            msg = 'Error calling API.'
            failed = True

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

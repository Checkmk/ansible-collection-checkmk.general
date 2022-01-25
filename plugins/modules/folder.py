#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2022, Robin Gierse <robin.gierse@tribe29.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: folder

short_description: Manage folders in Checkmk.

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "0.0.1"

description:
- Create and delete folders within Checkmk.

extends_documentation_fragment: [tribe29.checkmk.common]

options:
    path:
        description: The full path to the folder you want to manage. Pay attention to the leading C(/) and avoid trailing C(/).
        required: true
        type: str
    title:
        description: The title of your folder. If omitted defaults to the folder name.
        type: str
    state:
        description: The state of your folder.
        type: str
        default: present
        choices: [present, absent]

author:
    - Robin Gierse (@robin-tribe29)
'''

EXAMPLES = r'''
# Create a single folder.
- name: "Create a single folder."
  tribe29.checkmk.folder:
    server_url: "http://localhost/"
    site: "local"
    automation_user: "automation"
    automation_secret: "$SECRET"
    path: "/my_folder"
    title: "My Folder"
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
    sample: 'Folder created.'
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        server_url=dict(type='str', required=True),
        site=dict(type='str', required=True),
        automation_user=dict(type='str', required=True),
        automation_secret=dict(type='str', required=True), no_log=True,
        path=dict(type='str', required=True),
        title=dict(type='str'),
        state=dict(type='str', choices=['present', 'absent']),
    )

    result = dict(changed=False, failed=False, http_code='', msg='')

    module = AnsibleModule(argument_spec=module_args,
                           supports_check_mode=False)

    if module.params['state'] is None:
        module.params['state'] = 'present'

    changed = False
    failed = False
    http_code = ''
    server_url = module.params['server_url']
    site = module.params['site']
    automation_user = module.params['automation_user']
    automation_secret = module.params['automation_secret']

    path = module.params['path'].lower()
    if path[0] != "/":
        path = '/' + path
    if path[-1] == "/":
        path = path.rstrip("/")

    child = path.split("/")[-2:][1]
    parent = path.split("/")[-2:][0]
    if parent == '':
        parent = '/'
    else:
        parent = path.rstrip(child)
        # if parent[0] != "/":
        #     parent = '/' + parent
        if parent[-1] == "/":
            parent = parent.rstrip("/")

    path_for_url = path.replace('/', '~')
    state = module.params['state']
    title = module.params['title']
    if title == '':
        title = child

    # # ToDo: Remove debugging stuff
    # test = dict(
    #     path=path,
    #     parent=parent,
    #     child=child,
    #     path_for_url=path_for_url
    # )
    # module.exit_json(**test)

    # Declare headers including authentication to send to the Checkmk API
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + automation_user + ' ' + automation_secret
    }

    # Check whether the folder exists
    api_endpoint = '/objects/folder_config/' + path_for_url
    url = server_url + site + "/check_mk/api/1.0" + api_endpoint
    params = {
        'parent': parent,  # ToDo: split path to distinguish name and parent
    }
    response, info = fetch_url(module,
                               url,
                               data=None,
                               headers=headers,
                               method='GET')
    http_code = info['status']
    if http_code == 200:
        folder_state = 'present'
    elif http_code == 404:
        folder_state = 'absent'
    else:
        msg = 'Error calling API.'
        failed = True

    # Handle the folder accordingly to above findings and desired state
    if state == 'present' and folder_state == 'present':
        msg = "Folder already present."

    elif state == 'present' and folder_state == 'absent':
        api_endpoint = '/domain-types/folder_config/collections/all'
        params = {
            'name': child,
            'parent': parent,
            'title': title,
            'attributes': {  # ToDo: Enable attribute management
                'tag_criticality': 'prod'
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
            msg = "Folder created."
        else:
            msg = 'Error calling API.'
            failed = True

    elif state == 'absent' and folder_state == 'absent':
        msg = "Folder already absent."

    elif state == 'absent' and folder_state == 'present':
        api_endpoint = '/objects/folder_config/' + path_for_url
        url = server_url + site + "/check_mk/api/1.0" + api_endpoint
        response, info = fetch_url(module,
                                   url,
                                   data=None,
                                   headers=headers,
                                   method='DELETE')
        http_code = info['status']
        if http_code == 204:
            changed = True
            msg = "Folder deleted."
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

#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'version': '0.1'}

DOCUMENTATION = '''
module: checkmk_changes

short_description: Activate configuration changes in checkMK

version_added: "0.1"

description:
    - "With the C(checkmk_changes) module it is possible to activate configuration changes of one or more checkMK sites."
    - "This module provides some more options of the API of checkMK than the C(checkmk_host) module"

author: "Marcel Arentz (@ma@mathias-kettner.de)"

options:
    url:
        description:
            - URL to the Check_MK instance as HTTP or HTTPS
        required: true
    user:
        description:
            - The user to authenticate against the site
        required: true
    password:
        description:
            - The password to authenticate against the site
        required: true
    sites:
        description: Specifies a list of sites to activate changes on. This list may or may not contain the site on which the API call is made on.
        required: false
        default: none
    allow_foreign_changes:
        description: Sometimes other users made changes meanwhile. This option specifies if the changes should be activated if there are configuration changes from other users. 
        required: false
        default: False
        type: bool
    comment:
        description: You can optionally add a comment to this activation. 
        required: false
        default: none
    validate_certs:
        description: Check SSL certificate
        required: false
        default: True
        type: bool
'''

EXAMPLES = '''
- name: Activate changes in a single site of checkMK
  checkmk_changes:
    url: https://monitoring.example.org/mysite
    user: myuser
    password: mypassword
    validate_certs: yes

- name: Activate changes to a set of sites except the call one
  checkmk_changes:
    url: https://monitoring.example.org/mysite
    user: myuser
    password: mypassword
    sites:
        - first_slave_site
        - second_slave_site
    allow_foreign_changes: yes
    comment: Changes made by ansible
'''

RETURN = '''
request:
    - description: The paramters that was passed in
    type: dict
result:
    - description: The result from the Check_MK site
    type: dict
'''


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.checkmk_api import Changes

class CallChanges:
    def __init__(self, session):
        self.session = session

    def activate(self, payload, ansible):
        result = self.session.activate(payload=payload)
        result_output = result['result']

        if 'no changes to activate' in result_output:
            return False, result_output
        elif isinstance(result_output, dict):
            return True, result_output

        ansible.fail_json(msg='Failed to activate changes: %s' % result_output,
                          payload=payload)


def main():
    args = dict(
        # Required
        url=dict(type='str', required=True),
        user=dict(type='str', required=True),
        password=dict(type='str', required=True, no_log=True),
        # Optional
        sites=dict(type='list', default=None),
        allow_foreign_changes=dict(type='bool', default=True),
        comments=dict(type='str', default=None),
        validate_certs=dict(type='bool', default=True),
        )

    ansible = AnsibleModule(
        argument_spec=args,
        supports_check_mode=False
        )

    sites = ansible.params['sites']

    changes = CallChanges(Changes(
        ansible.params['url'],
        ansible.params['user'],
        ansible.params['password'],
        verify=ansible.params['validate_certs'],))

    payload = {
        'allow_foreign_changes': '1' if ansible.params['allow_foreign_changes'] == 'yes' else '0'
        }

    if ansible.params['comments']:
        payload['comment'] = ansible.params['comments']
    if sites:
        payload['sites'] = sites
        payload['mode'] = 'specific'
    else:
        payload['mode'] = 'dirty'

    changed, result = changes.activate(payload, ansible)

    ansible_result = dict(
        sites=sites,
        changed=changed,
        result=result,
        )

    ansible.exit_json(**ansible_result)

if __name__ == '__main__':
    main()

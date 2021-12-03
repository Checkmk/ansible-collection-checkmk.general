#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'version': '0.1'}

DOCUMENTATION = '''
module: checkmk_services

short_description: Managing services in checkMK

version_added: "0.1"

description:
    - "With the C(checkmk_services) module it is possible to discover or rediscover services of a host in checkMK."
    - "This module provides some more options of the API of checkMK than the C(checkmk_host) module"

author: "Marcel Arentz (@ma@mathias-kettner.de)"

options:
    site:
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
    name:
        description: Name of the host
        required: true
    mode:
        description: Controls the behaviour of the service discovery. With C(new) all new services are added to the host while C(remove) just removes vanished services. You can combine these two mode with C(fixall). C(refresh) removes all services and rediscvors them again afterwards.
        required: false
        default: new
        choices:
            - fixall
            - new
            - refresh
            - remove
    validate_certs:
        description: Check SSL certificate
        required: false
        default: True
        type: bool
'''

EXAMPLES = '''
- name: Add new services to a host in checkMK
  checkmk_services:
    url: https://monitoring.example.org/mysite
    user: myuser
    password: mypassword
    name: myhost1

- name: Adds new and removes vanished services
  checkmk_services:
    url: https://monitoring.example.org/mysite
    user: myuser
    password: mypassword
    name: {{ inventory_hostname }}
    mode: fixall
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
from ansible.module_utils.checkmk_api import Services

class CallServices:
    def __init__(self, session):
        self.session = session
        self.hostname = session.hostname


    def discover(self, mode):
        result = self.session.discover(mode=mode)
        result_text = result['result']

        if result_text.startswith('Service discovery successful.'):
            list_as_string = result.text.strip('Service discovery successful.')
            added, removed, kept, new_count = list_as_string.split(',')
            added_count = int(added.split(' ')[1])
            removed_count = int(removed.split(' ')[1])

            if added_count > 0 or removed_count > 0:
                return True, result_text
            return False, result_text

        ansible.fail_json(msg='Failed to discover as %s: %s' % (mode, result_text))

def main():
    args = dict(
        # Required
        url=dict(type='str', required=True),
        user=dict(type='str', required=True),
        password=dict(type='str', required=True, no_log=True),
        name=dict(type='str', required=True),
        # Optional
        mode=dict(type='str', default='new', choices=['']),
        validate_certs=dict(type='bool', default=True),
        )

    ansible = AnsibleModule(
        argument_spec=args,
        supports_check_mode=False
        )

    hostname = ansible.params['name']
    mode = ansible.params['mode']

    host = CallServices(Services(
        ansible.params['url'],
        ansible.params['user'],
        ansible.params['password'],
        verify=ansible.params['validate_certs'],
        hostname=hostname,))

    changed, result = host.discover(mode=mode)    

    ansible_result = dict(
        hostname=hostname,
        changed=changed,
        mode=mode,
        result=result,
        )

    ansible.exit_json(**ansible_result)

if __name__ == '__main__':
    main()

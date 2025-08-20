from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = r"""
    options:
        server_url:
            description: URL of the Checkmk server
            required: True
            vars:
                - name: checkmk_var_server_url
                - name: ansible_lookup_checkmk_server_url
            env:
                - name: CHECKMK_VAR_SERVER_URL
                - name: ANSIBLE_LOOKUP_CHECKMK_SERVER_URL
            ini:
                - section: checkmk_lookup
                  key: server_url
        site:
            description: Site name.
            required: True
            vars:
                - name: checkmk_var_site
                - name: ansible_lookup_checkmk_site
            env:
                - name: CHECKMK_VAR_SITE
                - name: ANSIBLE_LOOKUP_CHECKMK_SITE
            ini:
                - section: checkmk_lookup
                  key: site
        automation_auth_type:
            description:
                - The authentication type to use ('bearer', 'basic', 'cookie').
            required: False
            vars:
                - name: checkmk_var_automation_auth_type
                - name: ansible_lookup_checkmk_automation_auth_type
            env:
                - name: CHECKMK_VAR_AUTOMATION_AUTH_TYPE
                - name: ANSIBLE_LOOKUP_CHECKMK_AUTOMATION_AUTH_TYPE
            ini:
                - section: checkmk_lookup
                  key: automation_auth_type
            default: 'bearer'
        automation_user:
            description: Automation user for the REST API access.
            required: False
            vars:
                - name: checkmk_var_automation_user
                - name: ansible_lookup_checkmk_automation_user
            env:
                - name: CHECKMK_VAR_AUTOMATION_USER
                - name: ANSIBLE_LOOKUP_CHECKMK_AUTOMATION_USER
            ini:
                - section: checkmk_lookup
                  key: automation_user
        automation_secret:
            description: Automation secret for the REST API access.
            required: False
            vars:
                - name: checkmk_var_automation_secret
                - name: ansible_lookup_checkmk_automation_secret
            env:
                - name: CHECKMK_VAR_AUTOMATION_SECRET
                - name: ANSIBLE_LOOKUP_CHECKMK_AUTOMATION_SECRET
            ini:
                - section: checkmk_lookup
                  key: automation_secret
        automation_auth_cookie:
            description:
                - The authentication cookie value if using cookie-based authentication.
            vars:
                - name: checkmk_var_automation_auth_cookie
                - name: ansible_lookup_checkmk_automation_auth_cookie
            env:
                - name: CHECKMK_VAR_AUTOMATION_AUTH_COOKIE
                - name: ANSIBLE_LOOKUP_CHECKMK_AUTOMATION_AUTH_COOKIE
            ini:
                - section: checkmk_lookup
                  key: automation_auth_cookie
            required: False
        validate_certs:
            description:
                - Whether to validate SSL certificates.
            required: False
            vars:
                - name: checkmk_var_validate_certs
                - name: ansible_lookup_checkmk_validate_certs
            env:
                - name: CHECKMK_VAR_VALIDATE_CERTS
                - name: ANSIBLE_LOOKUP_CHECKMK_VALIDATE_CERTS
            ini:
                - section: checkmk_lookup
                  key: validate_certs
            type: bool
            default: True
    """


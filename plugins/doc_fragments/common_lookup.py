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
            env:
                - name: CHECKMK_VAR_SERVER_URL
            ini:
                - section: checkmk_lookup
                  key: server_url
        site:
            description: Site name.
            required: True
            vars:
                - name: checkmk_var_site
            env:
                - name: CHECKMK_VAR_SITE
            ini:
                - section: checkmk_lookup
                  key: site
        api_auth_type:
            description:
                - The authentication type to use ('bearer', 'basic', 'cookie').
            required: False
            vars:
                - name: checkmk_var_api_auth_type
            env:
                - name: CHECKMK_VAR_API_AUTH_TYPE
            ini:
                - section: checkmk_lookup
                  key: api_auth_type
            default: 'bearer'
        api_user:
            description: Automation user for the REST API access.
            required: False
            aliases: [automation_user]
            vars:
                - name: checkmk_var_api_user
            env:
                - name: CHECKMK_VAR_API_USER
            ini:
                - section: checkmk_lookup
                  key: api_user
        api_secret:
            description: Automation secret for the REST API access.
            required: False
            aliases: [automation_secret]
            vars:
                - name: checkmk_var_api_secret
            env:
                - name: CHECKMK_VAR_API_SECRET
            ini:
                - section: checkmk_lookup
                  key: api_secret
        api_auth_cookie:
            description:
                - The authentication cookie value if using cookie-based authentication.
            vars:
                - name: checkmk_var_api_auth_cookie
            env:
                - name: CHECKMK_VAR_API_AUTH_COOKIE
            ini:
                - section: checkmk_lookup
                  key: api_auth_cookie
            required: False
        validate_certs:
            description:
                - Whether to validate SSL certificates.
            required: False
            vars:
                - name: checkmk_var_validate_certs
            env:
                - name: CHECKMK_VAR_VALIDATE_CERTS
            ini:
                - section: checkmk_lookup
                  key: validate_certs
            type: bool
            default: True
    """

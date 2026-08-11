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
        proxy_url:
            description:
                - The URL of your proxy server, e.g. C(http://proxy.example.com:3128).
                - If no scheme is given, C(http://) is assumed.
                - Only the C(http) and C(https) schemes are supported.
                - The same proxy is used for HTTP and HTTPS requests, as the scheme
                  describes how to reach the proxy, not which traffic it forwards.
                - Hosts listed in the C(no_proxy) environment variable are still bypassed.
            required: False
            vars:
                - name: checkmk_var_proxy_url
            env:
                - name: CHECKMK_VAR_PROXY_URL
            ini:
                - section: checkmk_lookup
                  key: proxy_url
            type: str
        proxy_user:
            description:
                - The username to authenticate against your proxy server.
                - Must be provided together with I(proxy_pass).
            required: False
            vars:
                - name: checkmk_var_proxy_user
            env:
                - name: CHECKMK_VAR_PROXY_USER
            ini:
                - section: checkmk_lookup
                  key: proxy_user
            type: str
        proxy_pass:
            description:
                - The password to authenticate against your proxy server.
                - Must be provided together with I(proxy_user).
            required: False
            vars:
                - name: checkmk_var_proxy_pass
            env:
                - name: CHECKMK_VAR_PROXY_PASS
            ini:
                - section: checkmk_lookup
                  key: proxy_pass
            type: str
      notes:
        - Connection parameters are resolved from (in order of precedence) the value
          set directly on the plugin invocation, an Ansible variable of the form
          C(checkmk_var_*), an environment variable of the form C(CHECKMK_VAR_*),
          and the matching key under section C([checkmk_lookup]) in C(ansible.cfg).
    """

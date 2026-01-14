from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = r"""
    options:
        server_url:
            description:
                - The base url of your Checkmk server including the protocol but excluding the site.
                  If not set the module will fall back to the environment variable C(CHECKMK_VAR_SERVER_URL).
            required: true
            type: str
        site:
            description:
                - The site you want to connect to. This will be appended to the server_url as part of the API request url.
                  If not set the module will fall back to the environment variable C(CHECKMK_VAR_SITE).
            required: true
            type: str
        automation_user:
            description:
                - The automation user you want to use. It has to be an 'Automation' user, not a normal one.
                  If not set the module will fall back to the environment variable C(CHECKMK_VAR_AUTOMATION_USER).
            required: true
            type: str
        automation_secret:
            description:
                - The secret to authenticate your automation user.
                  If not set the module will fall back to the environment variable C(CHECKMK_VAR_AUTOMATION_SECRET).
            required: true
            type: str
        api_auth_type:
            description: Type of authentication to use.
            required: false
            type: str
            choices:
                - bearer
                - basic
                - cookie
            default: bearer
        api_auth_cookie:
            description: Authentication cookie for the Checkmk session.
            required: false
            type: str
        client_cert:
            description:
                - Path to the client certificate file for authentication with the web server hosting Checkmk.
                  This is not a Checkmk feature, but one of Ansible and the respective web server.
            required: false
            type: path
        client_key:
            description:
                - Path to the client certificate key file for authentication with the web server hosting Checkmk.
                  This is not a Checkmk feature, but one of Ansible and the respective web server.
            required: false
            type: path
        validate_certs:
            description:
                - Whether to validate the SSL certificate of the Checkmk server.
                  If not set the module will fall back to the environment variable C(CHECKMK_VAR_VALIDATE_CERTS).
            default: true
            type: bool
    """

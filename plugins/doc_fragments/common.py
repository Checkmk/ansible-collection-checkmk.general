from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = r"""
    options:
        server_url:
            description: The base url of your Checkmk server including the protocol but excluding the site directory.
            required: true
            type: str
        site:
            description: The site directory you want to connect to. This will be appended to the server_url as part of the API request url.
            required: true
            type: str
        automation_user:
            description: The automation user you want to use. It has to be an 'Automation' user, not a normal one.
            required: true
            type: str
        automation_secret:
            description: The secret to authenticate your automation user.
            required: true
            type: str
        validate_certs:
            description: Whether to validate the SSL certificate of the Checkmk server.
            default: true
            type: bool
    """

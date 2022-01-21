class ModuleDocFragment(object):
    # Common options for Checkmk modules
    DOCUMENTATION = r'''
    options:
        server_url:
            description: The base url of your Checkmk server.
            required: true
            type: str
        site:
            description: The site you want to connect to.
            required: true
            type: str
        automation_user:
            description: The automation user you want to use.
            required: true
            type: str
        automation_secret:
            description: The secret to authenticate your automation user.
            required: true
            type: str 
    '''
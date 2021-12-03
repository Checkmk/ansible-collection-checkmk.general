# Installation of the check**mk** agent

With this role you are able to rollout the check**mk** agent on your
hosts. 

This role currently covers
* apt based systems like Debian or Ubuntu
* rpm based systems like RedHat Enterprise Linux or CentOS
* Microsoft Windows based systems that support winrm

## Variables that may need manual interaction

Currently you need to specifiy the check**mk** manually to get this role
work correctly. But this may change in the future. You are able to set the
following default variables:

* `cmk_version: "1.5.0p13"`
* `cmk_site_url: "https://myserver.corp.org/mysite"`
* `cmk_host_linux_tmp: "/tmp"`
* `cmk_host_windows_tmp: "C:\\Users\\{{ ansible_user  }}\\AppData\\Local\\Temp"`

## Wishlist of future features that may be added

* Support for agent query via ssh
* Support for automatic firewall configuration
* Support for automatic SELinux configuration
* Support for custom config files on the Windows agent
* Support for new Windows agent
* Support for more operating systems
* ???

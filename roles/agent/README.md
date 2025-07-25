# checkmk.general.agent

This role installs and manages Checkmk agents.

## Requirements

The Checkmk Ansible Collection from which this role originates is needed to
use it, as modules shipped by this collection are used in the role.

It can be installed as easy as running:

    ansible-galaxy collection install checkmk.general

Additionally, this role requires the Python module `netaddr` on the controller.
Please make sure it is installed on your system and available for Ansible.

## Role Variables

### Basic Configuration

    checkmk_agent_version: "2.4.0p8"

The Checkmk version of the site your agents will talk to.

    checkmk_agent_edition: cre

The edition you are using. Valid values are `cre`, `cee`, `cce` and `cme`.

- `cre`: Raw Edition, fully open source.
- `cee`: Enterprise Edition, full enterprise features.
- `cce`: Cloud Edition, for cloud natives. Includes all enterprise features, and a free tier for a limited number of services.
- `cme`: Managed Edition, for service providers.

For details about the editions see: https://checkmk.com/product/editions

    checkmk_agent_server_protocol: http

The protocol used to connect to your Checkmk site.
This is used both for API calls and agent updates.

    checkmk_agent_server: localhost

The FQDN or IP address of your Checkmk server.

    checkmk_agent_server_validate_certs: 'true'

Whether to validate the SSL certificate of the Checkmk server.

    checkmk_agent_server_port: "{% if checkmk_agent_server_protocol == 'https' %}443{% else %}80{% endif %}"

The port of the web interface of your Checkmk server. Defaults to port 80 for http and port 443 for https.

    checkmk_agent_site: 'mysite'

The name of your Checkmk site.

### Authentication

    checkmk_agent_user: 'myuser'

The user used to authenticate against your Checkmk site.

    checkmk_agent_pass: 'mypass'

The password for the normal user used to authenticate against your Checkmk site, both for API calls and agent updates.
This is mutually exclusive with `checkmk_agent_secret`.

    checkmk_agent_secret: 'mysecret'

The secret for the automation user used to authenticate against your Checkmk site, both for API calls and agent updates.
This is mutually exclusive with `checkmk_agent_pass`.

### Registration

    checkmk_agent_registration_server: "{{ checkmk_agent_server }}"

The server you want to use for registration tasks (Agent updates and TLS encryption). Defaults to `{{ checkmk_agent_server }}`.

    checkmk_agent_registration_server_protocol: "{{ checkmk_agent_server_protocol }}"

The protocol used to connect to the registration server. Defaults to `{{ checkmk_agent_server_protocol }}`.

    checkmk_agent_registration_site: "{{ checkmk_agent_site }}"

The site you want to use for registration tasks (Agent updates and TLS encryption). Defaults to `{{ checkmk_agent_site }}`.

    checkmk_agent_auto_activate: 'false'

Enable automatic activation of changes on all sites.
This is disabled by default, as it might be unexpected.

    checkmk_agent_add_host: 'false'

Automatically add the host where the agent was installed on to Checkmk.

    checkmk_agent_host_name: "{{ inventory_hostname }}"

Define the hostname which will be used to add the host to Checkmk.

    checkmk_agent_host_ip: "{{ hostvars[inventory_hostname]['ansible_default_ipv4']['address'] }}"

Define an IP address which will be added to the host in Checkmk. This is optional, as long as the hostname is DNS-resolvable.

    checkmk_agent_host_attributes:
        ipaddress: "{{ checkmk_agent_host_ip | default(omit) }}"
        tag_mytag: value
        labels:
          App: my-app
          
Define attributes with which the host will be added to Checkmk.

    checkmk_agent_folder: '/'

The folder into which the automatically created host will be placed.

    checkmk_agent_discover: 'false'

Automatically discover services on the host where the agent was installed.

    checkmk_agent_discover_max_parallel_tasks: 0

If the value of this parameter is greater than zero, only the defined number of
discovery tasks run at the same time in parallel.

    checkmk_agent_force_foreign_changes: 'false'

Allow forcing foreign changes on activation by handler.

### Agent Configuration

    checkmk_agent_mode: 'pull'

The mode the agent operates in. For most deployments, this will be the `pull` mode.
If you are uncertain, what you are using, this is most likely your mode.
If you are using an alternative way to call the agent, e.g. SSH, you can set the variable to `ssh`, so the agent port check is skipped.
If you are using the Checkmk Cloud Edition (CCE) with an agent in `push` mode, you want to set this to `push` to avoid the agent port check, as well as triggering an initial push of data.

    checkmk_agent_port: '6556'

Configure the port the agent listens on. We recommend to stick to the default.
**This does not change the agent configuration! It merely tells Ansible which port to talk to.**

    checkmk_agent_update: 'false'

Register host for automatic updates. Make sure to have the server side prepared for automatic updates. Otherwise this will fail.
See [this link](https://docs.checkmk.com/latest/en/agent_deployment.html) for more information on the preparations.

    checkmk_agent_tls: 'false'

Register for TLS encryption. Make sure to have the server side prepared for automatic updates. Otherwise this will fail.
See [this link](https://docs.checkmk.com/latest/en/agent_linux.html#registration) for more information on the preparations.

    checkmk_agent_force_install: 'false'

Force the installation of the agent package, no matter the constraints.
This means, downgrades become possible and unverified packages would be installed.

    checkmk_agent_prep_legacy: 'false'

Enable this to automatically install `xinetd` on hosts with systemd prior to version 220.

### Security

    checkmk_agent_no_log: 'true'

Whether to log sensitive information like passwords, Ansible output will be censored for enhanced security by default. Set to `false` for easier troubleshooting. Be careful when changing this value in production, passwords may be leaked in operating system logs.

    checkmk_agent_configure_firewall: 'true'

Automatically configure the firewall to allow access to the Checkmk agent on the `checkmk_agent_port`.
This setting only has effect on systems, which are running `ufw` or `firewalld`.
For elaborate firewall configuration, use your own firewall management!
This setting only enables very basic firewall configuration.

### Delegation

    checkmk_agent_delegate_api_calls: 'localhost'

Configure the host to which Checkmk API calls are delegated to.
Typically this would be your Ansible host, hence the default `localhost`.

    checkmk_agent_delegate_download: "{{ inventory_hostname }}"

Configure the host to which downloads are delegated to. After download the files are transferred to the remote node, when the remote node didn't do the download itself.

    checkmk_agent_delegate_registration: 'false'

Enable this to set up TLS encryption using a third host, which has the Checkmk agent installed already.
`checkmk_agent_delegate_registration_target` defines this third host.
This feature can be used in case a direct connection to the Checkmk site on the agent receiver port (8000+) is not possible from the monitored host.

    checkmk_agent_delegate_registration_target: "{{ inventory_hostname }}"

Configure the target which is used to register the monitored host on the Checkmk server for TLS. The target needs to have a Checkmk agent installed.

### Advanced Options

    checkmk_agent_download_timeout: "{% if ansible_system == 'Win32NT' %}30{% else %}10{% endif %}"

This setting can be used to increase the timeout in seconds for downloading the Checkmk agent from the Checkmk server. Only use this, if you encounter issues with the agent download. There is no role default, the module defaults will be used.

## Tags

Tasks are tagged with the following tags:
| Tag | Purpose |
| ---- | ------- |
| `download-package` | Download agent package. |
| `install-package` | Install agent package with package manager. |
| `install-prerequisites` | Install packages that are required for the role or agent to work. |
| `include-os-family-vars` | Include OS family specific variables. |
| `include-os-family-tasks` | Include OS family specific tasks. |
| `get-package-facts` | Get package facts, used in the role. |
| `enable-xinetd` | Enable xinetd on hosts with systemd prior to version 220. |

You can use Ansible to skip tasks, or only run certain tasks by using these tags. By default, all tasks are run when no tags are specified.

## Dependencies

None.

## Example Playbook

    - hosts: all
      roles:
         - checkmk.general.agent

## Use Cases

This is a brief collection of use cases, that outline how this role can be used.
It should give you an idea of what is possible, but also what things to consider.

### Agent registration against a remote site

See [remote-registration.yml](../../playbooks/usecases/remote-registration.yml).

## Contributing

See [CONTRIBUTING](../../CONTRIBUTING).

## Disclaimer

This role is provided AS IS and we can and will not guarantee that the role works
as intended, nor can we be accountable for any damage or misconfiguration done
by this role. Study the role thoroughly before using it.

## License

See [LICENSE](../../LICENSE).

## Author Information

Robin Gierse (@robin-checkmk)

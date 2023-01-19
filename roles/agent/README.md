# tribe29.checkmk.agent

<!-- A brief description of the role goes here. -->
This role installs Checkmk agents.

## Requirements

<!-- Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required. -->
None.

## Role Variables

<!-- A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well. -->

    checkmk_agent_version: "2.1.0p18"

The Checkmk version of your site.

    checkmk_agent_edition: cre

The edition you are using. Valid values are `cre`, `cfe`, `cee` and `cme`.
- `cre`: Raw Edition, fully open source.
- `cfe`: Free Edition, enterprise features, but limited hosts.
- `cee`: Enterprise Edition, full enterprise features.
- `cme`: Managed Edition, for service providers.

For details about the editions see: https://checkmk.com/product/editions

    checkmk_agent_protocol: http

The protocol used to connect to your Checkmk site.

    checkmk_agent_server: localhost

The FQDN or IP address of your Checkmk server.

    checkmk_agent_server_validate_certs: 'true'

Whether to validate the SSL certificate of the Checkmk server.

    checkmk_agent_port: "{% if checkmk_agent_protocol == 'https' %}443{% else %}80{% endif %}"

The port of the web interface of your Checkmk server. Defaults to port 80 for http and port 443 for https.

    checkmk_agent_site: my_site

The name of your Checkmk site.

    checkmk_agent_registration_server: "{{ checkmk_agent_server }}"

The server you want to use for registration tasks (Agent updates and TLS encryption). Defaults to {{ checkmk_agent_server }}.

    checkmk_agent_registration_site: "{{ checkmk_agent_site }}"

The site you want to use for registration tasks (Agent updates and TLS encryption). Defaults to {{ checkmk_agent_site }}.

    checkmk_agent_user: automation

The user used to authenticate against your Checkmk site.

    checkmk_agent_pass: "{{ automation_secret }}"

The password for the normal user used to authenticate against your Checkmk site.  
This is mutually exclusive with `checkmk_agent_secret`.

    checkmk_agent_secret: "{{ automation_secret }}"

The secret for the automation user used to authenticate against your Checkmk site.  
This is mutually exclusive with `checkmk_agent_pass`.

    checkmk_agent_auto_activate: 'false'

Enable automatic activation of changes on all sites.
This is disabled by default, as it might be unexpected.

    checkmk_agent_add_host: 'false'

Automatically add the host where the agent was installed to Checkmk.

    checkmk_agent_host_name: "{{ inventory_hostname }}"

The hostname to use, when adding the host to Checkmk.

    checkmk_agent_folder: "/"

The folder into which the automatically created host will be places.

    checkmk_agent_discover: 'false'

Automatically discover services on the host where the agent was installed.

    checkmk_agent_update: 'false'

Register host for automatic updates. Make sure to have the server side prepared
for automatic updates. Otherwise this will fail.

    checkmk_agent_tls: 'false'

Register for TLS encryption. Make sure to have the server side prepared
for automatic updates. Otherwise this will fail.

    checkmk_agent_configure_firewall: 'true'

Automatically configure the firewall to allow access to the Checkmk agent.

    checkmk_agent_force_install: 'false'

Force the installation of the agent package, no matter the constraints.
This means, downgrades become possible and unverified packages would be installed.

    checkmk_agent_prep_legacy: 'false'

Enable this to automatically install `xinetd` on hosts with systemd prior to version 220.

    checkmk_agent_delegate_api_calls: localhost

Configure the host to which Checkmk API calls are delegated to.

    checkmk_agent_delegate_download: "{{ inventory_hostname }}"

Configure the host to which Checkmk API downloads are delegated to. After download the files are transfered to the remote node, when the remote node didn't do the download.

    checkmk_agent_host_name: "{{ inventory_hostname }}"

Define the hostname which will be used to add the host to Checkmk.

    checkmk_agent_host_ip: "{{ hostvars[inventory_hostname]['ansible_default_ipv4']['address'] }}"

Define an IP address which will be added to the host in Checkmk. This is optional, as long as the hostname is DNS-resolvable.

    checkmk_agent_host_attributes:
        ipaddress: "{{ checkmk_agent_host_ip | default(omit) }}"
        tag_agent: 'cmk-agent'

Define attributes with which the host will be added to Checkmk.

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

<!-- A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles. -->
None.

## Example Playbook

Including an example of how to use your role (for instance, with variables
passed in as parameters) is always nice for users too:

    - hosts: all
      roles:
         - tribe29.checkmk.agent

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

<!-- An optional section for the role authors to include contact information, or a website (HTML is not allowed). -->
Robin Gierse (@robin-tribe29)

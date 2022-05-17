# tribe29.checkmk.agent

<!-- A brief description of the role goes here. -->
This role installs Checkmk agents.

## Requirements

<!-- Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required. -->
None.

## Role Variables

<!-- A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well. -->

    checkmk_version: "2.0.0p24"

The Checkmk version of your site.

    checkmk_edition: cre

The edition you are using. Valid values are `cre` and `cee`.
Note, that `cee` is not implemented yet.

    checkmk_protocol: http

The protocol used to connect to your Checkmk site.

    checkmk_server: localhost

The FQDN or IP address of your Checkmk server.

    checkmk_site: my_site

The name of your Checkmk site.

## Dependencies

<!-- A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles. -->
None.

## Example Playbook

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: all
      roles:
         - tribe29.checkmk.agent

## Contributing

See [CONTRIBUTING](../../CONTRIBUTING).

## Disclaimer

This role is provided AS IS and we can and will not guarantee that the role works as intended, nor can we be accountable for any damage or misconfiguration done by this role. Study the role thoroughly before using it.

## License

See [LICENSE](../../LICENSE).

## Author Information

<!-- An optional section for the role authors to include contact information, or a website (HTML is not allowed). -->
Robin Gierse (@robin-tribe29)

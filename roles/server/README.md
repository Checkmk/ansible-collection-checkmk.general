# tribe29.checkmk.server

<!-- A brief description of the role goes here. -->
This role installs Checkmk on servers and manages sites.

## Requirements

<!-- Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required. -->
None.

## Role Variables

<!-- A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well. -->

    checkmk_server_version: "2.1.0p1"

The Checkmk version of your site.

    checkmk_server_edition: cre

The edition you want to install. Valid values are

- `cre`
- `cfe`
- `cee`
- `cme`

Note, that you need credentials, to download the `enterprise` and `managed` versions.
See below variables, to set those.

    checkmk_server_download_user: []
    checkmk_server_download_pass: []

Your credentials to the Checkmk customer portal.

    checkmk_server_verify_setup: 'true'

Cryptographically verify the downloaded setup file.

    checkmk_server_configure_firewall: 'true'

Automatically open the necessary ports on the Checkmk server for the
web interface to be accessible.

    checkmk_server_sites:
      - name: test
        version: "{{ checkmk_server_version }}"
        state: started
        admin_pw: test

A dictionary of sites, their version, admin password and state.
If a higher version is specified for an existing site, a config update resolution method must first be given to update it.
Valid choices include `install`, `keepold` and `abort`.

    checkmk_server_sites:
      - name: test
        version: "{{ checkmk_server_version }}"
        update_conflict_resolution: install
        state: started
        admin_pw: test

Directory to backup sites to when updating between versions.
    checkmk_server_backup_dir: /opt/omd/sites

Whether to back up sites when updating between versions. Only disable this if you plan on taking manual backups
    checkmk_server_backup_on_update: 'true'
## Dependencies

<!-- A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles. -->
None.

## Example Playbook

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: all
      roles:
         - tribe29.checkmk.server

## Contributing

See [CONTRIBUTING](../../CONTRIBUTING).

## Disclaimer

This role is provided AS IS and we can and will not guarantee that the role works as intended, nor can we be accountable for any damage or misconfiguration done by this role. Study the role thoroughly before using it.

## License

See [LICENSE](../../LICENSE).

## Author Information

<!-- An optional section for the role authors to include contact information, or a website (HTML is not allowed). -->
Robin Gierse (@robin-tribe29)

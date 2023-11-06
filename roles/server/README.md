# checkmk.general.server

<!-- A brief description of the role goes here. -->
This role installs Checkmk on servers and manages sites.

## Requirements

<!-- Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required. -->
None.

## Distribution Support
This roles includes explicit distribution support.
That means, that even if the role might run on other distributions,
we can only verify, that it works on the ones listed in `defaults/main.yml` in the variable `checkmk_server_server_stable_os`.

To elaborate: We do **not** guarantee, that this role will work on them.
But we do our best to have them stable. On top of that we have
automated tests, that continuously test this role against a set of distributions.

To learn about the distributions used in automated tests, inspect the corresponding `molecule/*/molecule.yml`.

## Role Variables

<!-- A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well. -->

    checkmk_server_version: "2.2.0p12"

The Checkmk version of your site.

    checkmk_server_edition: cre

The edition you want to use. Valid values are `cre`, `cfe`, `cee`, `cce` and `cme`.

- `cre`: Raw Edition, fully open source.
- `cfe`: Free Edition, enterprise features, but limited hosts.
- `cee`: Enterprise Edition, full enterprise features.
- `cce`: Cloud Edition, for cloud natives.
- `cme`: Managed Edition, for service providers.

For details about the editions see: https://checkmk.com/product/editions

Note, that you need credentials, to download all editions apart from `cre` and `cfe`.  
See below variables, to set those.

    checkmk_server_download_user: []
    checkmk_server_download_pass: []

Your credentials to the Checkmk customer portal.

    checkmk_server_verify_setup: 'true'

Cryptographically verify the downloaded Checkmk setup file.

    checkmk_server_epel_gpg_check: 'true'

Cryptographically verify the downloaded epel-release package on RHEL 8.

    checkmk_server_cleanup: 'false'

Uninstall unused Checkmk versions on the server.

    checkmk_server_configure_firewall: 'true'

Automatically open the necessary ports on the Checkmk server for the
web interface to be accessible.

    checkmk_server_allow_downgrades: 'false'

Whether to allow downgrading a sites version. Note this is not a recommended procedure, and will not be supported for enterprise customers.

    checkmk_server_sites:
      - name: mysite
        version: "{{ checkmk_server_version }}"
        update_conflict_resolution: abort
        state: started
        admin_pw: mypw
        omd_auto_restart: 'false'
        omd_config:
          - var: AUTOSTART
            value: on

A dictionary of sites, containing the desired version, admin password and state.
There are also advanced settings, which will be outlined below.
Valid values for `state` are:
- `started`
- `stopped`
- `enabled`
- `disabled`
- `present`
- `absent`

If a higher version is specified for an existing site, a config update resolution method must first be given to update it.
Valid choices include `install`, `keepold` and `abort`.

Site configuration can be passed with the `omd_config` keyword.
The format can be seen above, for a list of variables run `omd show`
on an existing site.  
**Pay special attention to the `omd_auto_restart` variable!** As site configuration needs the site to be stopped, this needs to be handled. By default the variable is set to `false` to avoid unexpected restarting. However, no configuration will be performed if the site is started.

    checkmk_server_backup_on_update: 'true'

Whether to back up sites when updating between versions. Only disable this if you plan on taking manual backups.

    checkmk_server_backup_dir: /tmp

Directory to backup sites to when updating between versions.

    checkmk_agent_no_log: 'true'

Whether to log sensitive information like passwords, Ansible output will be censored for enhanced security by default. Set to `false` for easier troubleshooting. Be careful when changing this value in production, passwords may be leaked in operating system logs.

## Tags
Tasks are tagged with the following tags:
| Tag | Purpose |
| ---- | ------- |
| `download-package` | Download server package. |
| `install-package` | Install server package with package manager. |
| `install-prerequisites` | Install packages that are required for the role or server to work. |
| `download-gpg-key` | Download Checkmk GPG key for verifying the package. |
| `import-gpg-key` | Import the downloaded Checkmk GPG key for verifying the package. |
| `include-os-family-vars` | Include OS family specific variables. |
| `include-rhel-version-vars` | Include RHEL version specific variables. |
| `set-selinux-boolean` | Set necessary SELinux booleans for Checkmk to work on SELinux enabled systems. |
| `enable-repos` | Enable the required external repositories on RHEL based systems. Powertools on RHEL 7 and CentOS 8. CRB and EPEL on RHEL 8. |
| `checkmk_server_epel_gpg_check` | Download and use GPG key verification for EPEL repository. |
| `create-sites` | Create sites on the Checkmk server. |
| `update-sites` | Update sites on the Checkmk server. |
| `start-sites` | Start sites on the Checkmk server. |
| `stop-sites` | Stop sites on the Checkmk server. |
| `destroy-sites` | Destroy sites on the Checkmk server. |
| `set-site-admin-pw` | Set the cmkadmin password of a site. |
| `update-pause` | Pause with a warning when updating a site. |
| `cleanup` | Clean up old Checkmk versions. |

You can use Ansible to skip tasks, or only run certain tasks by using these tags. By default, all tasks are run when no tags are specified.

## Dependencies

<!-- A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles. -->
None.

## Example Playbook

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: all
      roles:
         - checkmk.general.server

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
Robin Gierse (@robin-checkmk)

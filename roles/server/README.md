# checkmk.general.server

This role installs Checkmk on servers and manages sites.

## Requirements

The Checkmk Ansible Collection from which this role originates is needed to
use it, as modules shipped by this collection are used in the role.

It can be installed as easy as running:

    ansible-galaxy collection install checkmk.general

## Distribution Support

This roles includes explicit distribution support.
That means, that even if the role might run on other distributions,
we can only verify, that it works on the ones listed in `defaults/main.yml` in the variable `checkmk_server_server_stable_os`.

To elaborate: We do **not** guarantee, that this role will work on them.
But we do our best to stay as stable as possible on them. On top of that we have
automated tests, that continuously test this role against a subset of distributions.

To learn about the distributions used in automated tests, inspect the corresponding `molecule/*/molecule.yml`.

## Role Variables

### Basic Configuration

    checkmk_server_version: "2.4.0p9"

The global Checkmk version. This is used for installing Checkmk.
To manage sites and their version, see `checkmk_server_sites`.

    checkmk_server_edition: 'cre'

The edition you are using. Valid values are `cre`, `cee`, `cce` and `cme`.

- `cre`: Raw Edition, fully open source.
- `cee`: Enterprise Edition, full enterprise features.
- `cce`: Cloud Edition, for cloud natives. Includes all enterprise features, and a free tier for a limited number of services.
- `cme`: Managed Edition, for service providers.

For details about the editions see: https://checkmk.com/product/editions

Note, that you need credentials, to download the `cee` edition.
See below variables, to set those.

    checkmk_server_download_user: []
    checkmk_server_download_pass: []

Your credentials to the Checkmk customer portal.

    checkmk_server_verify_setup: 'true'

Cryptographically verify the downloaded Checkmk setup file.

    checkmk_server_gpg_download_user: []
    checkmk_server_gpg_download_pass: []

Optional authentication do download the GPG key from a non-default location.

    checkmk_server_epel_gpg_check: 'true'

Cryptographically verify the downloaded epel-release package on RHEL 8.

    checkmk_server_cleanup: 'false'

Uninstall unused Checkmk versions on the server.

### Security

    checkmk_server_no_log: 'true'

Whether to log sensitive information like passwords. Ansible output will be censored for enhanced security by default.
Set to `false` for easier troubleshooting. Be careful when changing this value in production, passwords may be leaked in operating system logs.

    checkmk_server_configure_firewall: 'true'

Automatically open necessary ports on the Checkmk server.
This setting only has effect on systems, which are running `ufw` or `firewalld`.
For elaborate firewall configuration, use your own firewall management!

    checkmk_server_ports:
    - 22
    - 80
    - 443
    - 8000

The TCP ports to open automatically. Adapt this to the specific requirements of your site.

### Site Management

    checkmk_server_sites:
      - name: 'mysite'
        version: "{{ checkmk_server_version }}"
        edition: "{{ checkmk_server_edition }}"
        update_conflict_resolution: 'abort'
        state: 'started'
        admin_pw: 'mypass'
        omd_auto_restart: 'false'
        omd_config:
          - var: AUTOSTART
            value: 'on'
        mkp_packages:
          - name: 'mypackage'
            version: 1.0.0
            src: '/path/to/my.mkp'
            url: 'https://exchange.checkmk.com/packages/mypackage/4711/mypackage-1.0.0.mkp'
            checksum: 'md5:mychecksum'
            installed: true
            enabled: true

A dictionary of sites, containing the desired version, admin password, site configuration options, extension packages and state.
The more advanced settings will be outlined below.

Valid values for `state` are:
- `started`: The site is started and enabled for autostart on system boot.
- `stopped`: The site is stopped and disabled for autostart on system boot.
- `enabled`: The site is stopped, but enabled for autostart on system boot.
- `disabled`: The site is stopped and disabled for autostart on system boot.
- `present`: The site is stopped and disabled for autostart on system boot.
- `absent`: The site is removed from the system entirely.

If a higher version is specified for an existing site, a config update resolution method must first be given to update it.
Valid choices include `install`, `keepold` and `abort`.

Site configuration can be passed with the `omd_config` keyword.
The format can be seen above, for a list of variables run `omd show`
on an existing site.
**Pay special attention to the `omd_auto_restart` variable!** As site configuration needs the site to be stopped, this needs to be handled. By default the variable is set to `false` to avoid unexpected restarting. However, no configuration will be performed if the site is started.

Extension packages can also be listed to be installed on the specific central site. Remote sites will get extension packages replicated upon change activation. A source path can be set on the Ansible controller. Alternatively a URL can be specified to download the mkp package from directly. These options are mutually exclusive.

### Site Updates

    checkmk_server_backup_on_update: 'true'

Whether to back up sites when updating between versions. Only disable this if you plan on taking manual backups.

    checkmk_server_backup_dir: '/tmp'

Directory to backup sites to when updating between versions.
Of course `/tmp/` is not a sane backup location, so change it!

    checkmk_server_backup_opts: '--no-past'

Backup options to use. By default no historic data is backed up, in order to create a small disaster recovery backup.

    checkmk_server_allow_downgrades: 'false'

Whether to allow downgrading a site's version.
Note: this is not a recommended procedure, and will not be supported for enterprise customers.

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

None.

## Example Playbook

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

Robin Gierse (@robin-checkmk)

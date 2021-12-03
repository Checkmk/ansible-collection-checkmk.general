# Installation of the check**mk** agent plugins

With this role you are able to rollout check**mk** agent plugins on your
hosts. Needed plugins (and it's configuration files) will be installed and
obsolete plugins will be removed. This role makes currently only sense, if
you want to ensure some standard plugins on all your hosts. If you have
a generic configuration for a plugin, you may also want them to be rolled
out.

This role will not be useful if you need to have many individual
configurations on your hosts or if you want your plugins only on a group
of hosts. This may change in the future.

This role currently covers the plugin rollout based on
* Processes
* Existing files
* Installed Software

It is additionally possible to enforce plugins. 

## Basic default variables

* `cmk_site_url: "https://myserver.corp.org/mysite"`
* `cmk_agent_lnx_path: "/usr/lib/check_mk_agent"`
* `cmk_agent_win_path: "C:\\Program Files (x86)\\check_mk"`
* `by_process: true`: Turn detection by process on or off
* `by_package: false`: Turn detection by installed software on or off
* `by_files: false`: Turn detection by existing files on or off

## Plugin definition

Only specified plugins will be considered for a rollout. If you don't need
a plugin, simply remove the definition. Otherwise add a plugin definition
and it's conditions, if you need a specific plugin. The name should be the
file name of the plugin. Conditions are all optionally except you will
need to specifiy at least one per plugin. 

Here is an example definition:

    cmk_host_plugins:
      Linux:
        apache_status:
          cmd: apache
          pkg: apache2
          cfg: apache_status.cfg
        mk_cups_queues:
          path: /usr/bin/lpstat
        mk_logwatch:
          cfg: logwatch.cfg
          force: true
        mk_logins:
          force: true
      Windows:
        mk_oracle.ps1:
          cmd: oracle
          cfg: mk_oracle_cfg.ps1

Please consider, that
* Process matches all process that contains that string
* The package definition needs an exact match
* The configuration file needs to be placed into the files folder

## Wishlist of possibly features

* Prevent plugin installation for groups of hosts
* Allow individual configuration files for groups of hosts
* A module to identify needed plugins?
* ???

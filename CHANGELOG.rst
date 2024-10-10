=============================
checkmk.general Release Notes
=============================

.. contents:: Topics

v5.3.0
======

Major Changes
-------------

- Inventory module - Add module for creating a dynamic inventory from Checkmk.
- Site lookup module - Add module to lookup details of a single site.
- Site module - Add module for distributed monitoring. Refer to the module documentation for further details.
- Sites lookup module - Add module to lookup all sites and their details in a distributed monitoring setup.

Minor Changes
-------------

- Rule module - Return 'content' and 'http_code', which includes the 'rule_id'.

Bugfixes
--------

- Folder module - Fix an issue, where the folder module would create an uppercase folder but would not be able to find said folder.

Known Issues
------------

- Site module - To completely enable a site, the livestatus certificate needs to be trusted. This cannot be done with the site module. As of now, there is no automatic way to do this, so you need to log into the site and add the certificate to the trusted certificates manually.

New Plugins
-----------

Lookup
~~~~~~

- checkmk.general.site - Show the configuration of a site
- checkmk.general.sites - Get a list of all sites

New Modules
-----------

- checkmk.general.site - Manage distributed monitoring in Checkmk.

v5.2.1
======

Release Summary
---------------

Bugfix Release.

Bugfixes
--------

- Folder module - Fix bug, where `update_attributes` failed on a folder with the Network Scan enabled.

v5.2.0
======

Release Summary
---------------

Some bug fixing and a module update.

Minor Changes
-------------

- Agent role - Allow registration on mixed protocol environments. This means the central and remote site do not both have to use either HTTP or HTTPS.
- Tag_group module - Enable module for Checkmk 2.4.0 by using `id` instead of `ident` to identify tag groups and their tags. See https://checkmk.com/werk/16364 for background information.
- Tag_group module - Migrate module to new collection API.
- The local development environment was cleaned up. We removed all traces of VirtualBox and now exclusively use KVM/QEMU virtualization. This has no effect on using the collection. It only affects you, if you develop for this collection and used the `Vagrantfile` or `Makefile`.

Bugfixes
--------

- Agent role - Fix registration in cases where a prior registration failed.
- Downtime module - Downtimes are now correctly removed when only specifying a single service.

v5.1.0
======

Release Summary
---------------

Some love for the agent role.

Minor Changes
-------------

- Agent role - All internal variables are now prefixed with a double underscore (`__`). If you hooked into any variable, which is not in `defaults/main.yml` you need to check your inventory. Be advised, that it is bad practice, to use internal variables directly.
- Agent role - Improve idempotency by reading the registration states both for Agent registration and Updater registration and skipping the registration if it is not necessary.
- Server role - All internal variables are now prefixed with a double underscore (`__`). If you hooked into any variable, which is not in `defaults/main.yml` you need to check your inventory. Be advised, that it is bad practice, to use internal variables directly.
- Testing - Testing against Python 3.8 was removed for all modules.

Bugfixes
--------

- Agent role - For Windows hosts the download of correct setup files was broken due to a mixup in the modules used to fetch the files. The role would always fall back to the GENERIC agent, even if a specific agent was available. This is fixed now.

v5.0.0
======

Release Summary
---------------

(Re)writing history with overhauled modules and updated Checkmk, Ansible, Distribution and Python support.

Major Changes
-------------

- Discovery module - The module now fully supports Checkmk 2.3.0. Additionally, two new parameters were introduced, `update_service_labels` and `monitor_undecided_services`. Refer to the module documentation for further details.
- Rule module - The complete module was rewritten to use the new module API. Additionally, a parameter "rule_id" was introduced to modify existing rules. Refer to the module documentation for further details.

Minor Changes
-------------

- Agent role - Add support to open firewall for a list of IPs.
- Agent role - Replace `ansible.builtin.yum` with the succeeding `ansible.builtin.dnf`.
- Server role - Replace `ansible.builtin.yum` with the succeeding `ansible.builtin.dnf`.
- Several modules - Remove unnecessary HTTP codes which get already imported via utils.py.
- Testing - Add Ansible 2.17 to all tests. Be advised, that this Ansible release drops support for Python 2.7 and 3.6.
- Testing - Add Ubuntu 24.04 to the Molecule tests.
- Testing - All tests now cover Checkmk 2.3.0.
- Testing - Remove Ansible 2.14 from all tests, as it is EOL.
- Testing - Remove Checkmk 2.0.0 from all tests, as it is EOL.
- Testing - The Molecule tests now run on Ubuntu 22.04.

Breaking Changes / Porting Guide
--------------------------------

- Agent role - Not really a breaking change, but we removed the internal variable `checkmk_agent_server_ip`. If you set this variable in your inventory, please make sure to update your configuration accordingly!
- Folder lookup module - Return the complete folder information, not only the extensions. To keep the current behavior in your playbooks, you want to use `{{ my_lookup_result.extensions }}` instead of `{{ my_lookup_result }}`.

v4.4.1
======

Release Summary
---------------

Bugfix Release.

Minor Changes
-------------

- Add 'ansible.utils' collection as an explicitely dependency. We already had this dependency, but are now declaring it explicitely.

Bugfixes
--------

- Host module - Fix hosts always being created in the main directory.

v4.4.0
======

Release Summary
---------------

Spring is here! With a rewritten host module including check mode and cluster support.

Major Changes
-------------

- Host module - Add support for cluster hosts.
- Host module - Enable check mode.
- Host module - Update attribute management behavior. Refer to the documentation for details.

Minor Changes
-------------

- Host module - Migrate module to the new collection API.

Bugfixes
--------

- Bakery module - Fix failing integration test due to wrong key passphrase.
- Folder module - Fix issue where the `name` (alias `title`) was entirely ignored.
- Folder module - Fix issues with uppercase and lowercase names.

v4.3.1
======

Release Summary
---------------

Bugfix Release.

Bugfixes
--------

- Rule module - Fix empty rule conditions.

v4.3.0
======

Release Summary
---------------

Reworking the CI, enhancing code quality and improving modules.

Minor Changes
-------------

- Folder module - Extend attribute management. Please refer to the module documentation for more details.
- Lookup modules - Enable usage of ini files, environment and inventory variables to configure basic settings for the lookup plugins, like e.g., the server_url or site alongside the authentication options. Refer to the module documentation for details.
- Rule module - Introduce rule_id to uniquely identify rules. This ID can be retrieved e.g., using the lookup plugin. Refer to the module documentation for further details.

Bugfixes
--------

- Folder module - Fix idempotency when using "attributes" parameter for creating a folder.
- Folder module - Parents will be parsed properly now. This means, that parents given as a string will now be parsed as a list of one.
- Host module - Parents will be parsed properly now. This means, that parents given as a string will now be parsed as a list of one.
- User module - Fix bug, where an absent user was created, if 'reset_password' was used.

Known Issues
------------

- Lookup modules - When using inventory variables to configure e.g., the server_url, it is not possible to assign other variables to these variables. This is a limitation of Ansible itself.

v4.2.0
======

Release Summary
---------------

Happy New Year!

Major Changes
-------------

- Tag_group module - Rewrite module and migrate to new collection API.
- User module - Rewrite module and migrate to new collection API.

Minor Changes
-------------

- Server role - Improve role speed by skipping downloads.
- Tag_group module - Enable `help` and `repair` options.
- User module - Enable several interface options.

Bugfixes
--------

- Agent role - Fix `become` in handler, which could cause errors on delegation.
- Rule module - Fix idempotency for rule location relative to another rule_id, by getting the target folder from neighbour rule.

v4.1.0
======

Release Summary
---------------

Happy holidays, everyone!

Major Changes
-------------

- Rule lookup plugin - Show a particular rule.
- Rules lookup plugin - List the rules of a ruleset.
- Ruleset lookup plugin - Show a particular ruleset.
- Rulesets lookup plugin - Search rulesets.

Minor Changes
-------------

- Password module - Improve error handling.

Bugfixes
--------

- Password module - Fix non-required module options being wrongly required.

v4.0.1
======

v4.0.0
======

Release Summary
---------------

Move fast, break things.

Major Changes
-------------

- Bakery lookup plugin - Get the status of the Checkmk Agent Bakery.

Minor Changes
-------------

- Activation module - Implement proper support for `redirect` parameter. This means, the activation module can now optionally wait for a completed activation or just trigger it and move on.
- Discovery module - Print error message, when using state "tabula_rasa" in bulk discovery mode, because that state is not supported by the API.
- Lookup API - Add improved error handling.

Breaking Changes / Porting Guide
--------------------------------

- Agent role - We restructured the agent. That entails a lot of changes, and we tried to keep everything stable. However, we cannot guarantee stability as we do not know all use-cases out there. Hence this change is also considered breaking.
- Server role - It became necessary to make the way states are handled more consistent. The most siginificant change is, that all sites not in state "started" will be stopped. For all other states please consult the role's README.
- Variable names - We aligned the names of variables throughout the collection. This can impact your existing configuration. Please review the variable names and apapt your configuration accordingly. For more details see `CONTRIBUTING.md`.

New Plugins
-----------

Lookup
~~~~~~

- checkmk.general.bakery - Get the bakery status of a Checkmk server

v3.4.0
======

Release Summary
---------------

Supporting managed service providers, admins and security. All in one release.

Minor Changes
-------------

- Agent role - Avoid logging passwords by default for extra security
- Agent role - Introduce variable to configure agent mode. Refer to the README.
- Contact group module - Add support for the Checkmk Managed Edition (CME).
- Host group module - Add support for the Checkmk Managed Edition (CME).
- Password module - Add support for the Checkmk Managed Edition (CME).
- Server role - Add new states "enabled" and "disabled" for site management.
- Server role - Avoid logging passwords by default for extra security
- Server role - Enable configuration of omd config values. Refer to the README for details.
- Service group module - Add support for the Checkmk Managed Edition (CME).
- User module - Add support for the Checkmk Managed Edition (CME).

Bugfixes
--------

- Agent role - Fix agent port check for agent modes other than "pull".

v3.3.0
======

Release Summary
---------------

This is the librarian release: We added some lookups.

Major Changes
-------------

- Folder lookup plugin - Look up the configuration of a folder.
- Folders lookup plugin - Look up all folders.
- Host lookup plugin - Look up the configuration of a host.
- Hosts lookup plugin - Look up all hosts.
- Timeperiod module - Add timeperiod module.

Minor Changes
-------------

- Agent role - Add support for firewall configuration on Debian derivates.
- Discovery module - Use the version comparison utils.
- Server role - Site management can now be done without specifying 'admin_pw'.
- Utils - Provide a class CheckmkVersion to simplify version comparison.

Bugfixes
--------

- Agent role - Performing the agent registration on a remote would fail, if the host was just created. This release introduces a workaround to enable this.
- Folder module - When creating a new folder with "attributes" parameter, the attributes were ignored. This is now fixed.

Known Issues
------------

- Server role - Not having to provide an admin password introduces a problem though, as users could create sites without knowing the randomly generated password. A task is introduced to mitigate this, but the solution there could be improved.

New Plugins
-----------

Lookup
~~~~~~

- checkmk.general.folder - Get folder attributes
- checkmk.general.folders - Get various information about a folder
- checkmk.general.host - Get host attributes
- checkmk.general.hosts - Get various information about a host

New Modules
-----------

- checkmk.general.timeperiod - Manage time periods in checkmk.

v3.2.0
======

Minor Changes
-------------

- Agent role - Add preflight check for correct Checkmk edition.
- Agent role - Allow the role to download folder-specific agents.
- Server role - Add preflight check for correct Checkmk edition.

Bugfixes
--------

- Agent role - Fix activation handler URL.
- Agent role - Fix agent and update registration on remote sites.

v3.1.0
======

Release Summary
---------------

It is summer and you want to look outside, so we added Windows.

Major Changes
-------------

- Agent role - Add support for Windows.
- Version lookup plugin - Add Version lookup plugin.

Minor Changes
-------------

- Discovery module - Add handling for 409 response.

New Plugins
-----------

Lookup
~~~~~~

- checkmk.general.version - Get the version of a Checkmk server

v3.0.0
======

Release Summary
---------------

Removing deprecated module options and more cleaning.

Minor Changes
-------------

- Agent role - Allow throttling of discovery task to limit load on Checkmk server.
- Folder module - Warn about mutually exclusive attribute options on older Checkmk versions and fail on recent Checkmk versions. See 'Breaking Changes'.

Breaking Changes / Porting Guide
--------------------------------

- Folder module - The module options 'attributes', 'update_attributes' and 'remove_attributes' are now mutually exclusive. Using more than one on a single task will cause a warning or error.
- Host group module - Deprecated options 'host_group_name' and 'host_groups' were removed. Use 'name' and 'groups' instead!
- Host module - Deprecated option 'host_name' was removed. Use 'name' instead!
- Rule module - Deprecated option 'folder' was removed. Use 'location' instead!

v2.4.1
======

Minor Changes
-------------

- Agent role - The activate changes handler was missing the server port. This is fixed now.

v2.4.0
======

Release Summary
---------------

Enabling more operating systems!

Minor Changes
-------------

- Agent role - Ensure fresh data before adding services to host.
- Agent role - Ensure support for Debian 12.
- Discovery module - Improve resilience and stability.
- Server role - Add feature to clean up unused Checkmk versions on the server.
- Server role - Enable explicit support for Oracle Linux 8.
- Server role - Ensure explicit support for Debian 12.

Known Issues
------------

- Discovery module - The module does not work on a controller host with Python 2.

v2.3.0
======

Release Summary
---------------

Features all over the place!

Major Changes
-------------

- Discovery module - Add support for bulk discoveries.
- Password module - Add password module.

Minor Changes
-------------

- Server role - Add support for RHEL and CentOS 9
- Utils - Introduce retries for API calls in case of timeouts.

New Modules
-----------

- checkmk.general.password - Manage passwords in checkmk.

v2.2.0
======

Release Summary
---------------

Extend OS support in roles and fix some minor issues in modules.

Minor Changes
-------------

- Activation module - Properly add If-Match header.
- Agent role - Add support for AlmaLinux and Rocky Linux, both versions 8 and 9.
- Agent role - Bump default Checkmk version to 2.2.0.
- Module utils - Remove workaround from version 2.1.0, where all modules were passed the If-Match header.
- Server role - Add support for AlmaLinux and Rocky Linux, both versions 8 and 9.
- Server role - Bump default Checkmk version to 2.2.0.

Bugfixes
--------

- Downtime module - The comment has a default value now

v2.1.0
======

Major Changes
-------------

- Bakery module - Migrated to use module_utils.
- Discovery module - Migrated to use module_utils.
- contact_group module - The module was not compatible with Checkmk 2.2. This is fixed now.
- host_group module - The module was not compatible with Checkmk 2.2. This is fixed now.
- service_group module - The module was not compatible with Checkmk 2.2. This is fixed now.

Bugfixes
--------

- Discovery module - Properly handle redirects to wait for completion of background jobs.
- Downtime module - The module handles timezones properly now.
- Integration tests - A bug was fixed, where the integration tests did not use the correct Checkmk version.
- Utils - With Checkmk 2.2.0p3 the activation introduces a breaking change, which we need to handle. As a workaround we added the 'If-Match' header to all API requests.

Known Issues
------------

- Utils - All API calls send the 'If-Match' header. This is a workaround and will be fixed in a future release.

v2.0.0
======

Release Summary
---------------

Welcome to the new world!

Breaking Changes / Porting Guide
--------------------------------

- The renaming of the collection has concluded. If you are reading this, you on the right release and repository and should be able to use the collection just as you are used to. Make sure to double check, that you are using the new FQCNs!

v1.0.0
======

Release Summary
---------------

This collection was renamed to checkmk.general. Please use the new name moving forward!

Breaking Changes / Porting Guide
--------------------------------

- This collection was renamed and module redirects have been activated. That means, if you are using this release, you also need the new collection to be installed. Otherwise things will break for you. In any way you should now move to the new collection name: checkmk.general.

v0.23.0
=======

Major Changes
-------------

- folder module - Add support for 'update_attributes' and 'remove_attributes'. Read the documentation for further details.

Minor Changes
-------------

- folder module - Add support for check mode.
- tag_group module - Code cleanup. Should have no effect on functionality, but mentioning it here for transparency.

v0.22.0
=======

Release Summary
---------------

Further centralizing.

Major Changes
-------------

- module_utils - Extend centralization by providing types and further utils.

Minor Changes
-------------

- Playbooks - Reorganize and clean up playbooks. This is a constant work in progress.

v0.21.0
=======

Major Changes
-------------

- Add Bakery module

Minor Changes
-------------

- Server role - Added support for almalinux

Bugfixes
--------

- Agent role - Fix activate changes handler failing with self-signed certificate

New Modules
-----------

- checkmk.general.bakery - Trigger baking and signing in the agent bakery.

v0.20.0
=======

Minor Changes
-------------

- Agent role - Make firewall zone configurable on RedHat derivates.
- Host module - Enable update and removal of attributes in addition to fully managing them. This is analogous to the Checkmk REST API. Additionally the "folder" attribute has no default value anymore except on creation.

Bugfixes
--------

- Rule module - Fix crash, if the Checkmk REST API does not return a value for the "disabled" property.

v0.19.0
=======

Release Summary
---------------

Centralizing functions.

Major Changes
-------------

- We dropped support for Ansible 2.11 and Python 2 entirely. That means you can still use this collection with older versions, we just do not test against them anymore.
- module_utils - Introduce a centralized library to call the Checkmk API.

Minor Changes
-------------

- We added support for Ansible 2.14.

Bugfixes
--------

- User module - Fix creation of automation users.

v0.18.0
=======

Major Changes
-------------

- Add user module.
- Rule module - Enable check mode.

Bugfixes
--------

- Agent role - Fix support for CCE.

Known Issues
------------

- User module - Currently no automation users can be created due to a mismatch of 'auth_type'
- User module - The parameter "interface_options" is not yet usable

New Modules
-----------

- checkmk.general.user - Manage users in Checkmk.

v0.17.1
=======

Minor Changes
-------------

- Agent role - Add cloud edition support.

v0.17.0
=======

Release Summary
---------------

Collected bugfixes.

Minor Changes
-------------

- Agent role - Make forcing of foreign changes on activation by handler configurable.
- Rule module - Improve rule comparison logic. No dummy rule is necessary for comparison anymore.
- contact_group module - Fix Ansible Galaxy linting findings.
- discovery module - Fix Ansible Galaxy linting findings.
- downtime module - Fix Ansible Galaxy linting findings.
- host_group module - Fix Ansible Galaxy linting findings.
- rule module - Fix Ansible Galaxy linting findings.
- service_group module - Fix Ansible Galaxy linting findings.

Bugfixes
--------

- Agent role - Fix delegation of activation in handler.

v0.16.2
=======

Release Summary
---------------

Bugfix Release.

Bugfixes
--------

- Agent role - Add explicit "become: false" to the "Discover services and labels on host." task.
- Downtime module - Fix handling of parameters start_after and end_after.

v0.16.1
=======

Bugfixes
--------

- Agent role - Fix erroneous usage of "checkmk_agent_pass" in activation handler.

v0.16.0
=======

Minor Changes
-------------

- Agent role - Enable automatic activation of changes when needed for this role. Refer to the README for details.
- Agent role - Enable registration for TLS and agent updates on remote sites.
- Agent role - RedHat - Only try to configure firewalld, if the systemd service is present.
- Playbooks - Add use case playbook for registering agents on remote sites.
- Rule module - Now its possible to choose a position when creating a rule. The ID of the created rule is returned in the task's response.

Bugfixes
--------

- Rule module - Now properly comparing the specified rule with the existing ones to achieve idempotency.

Known Issues
------------

- Rule module - comparing the specified rule with the existing ones leads to additional changes in CMK's audit log

v0.15.0
=======

Major Changes
-------------

- The folder module now uses `name` instead of `title`. The latter is retained as an alias until further notice.
- The host module now uses `name` instead of `host_name`. The latter is retained as an alias but will be removed with a future release.

Minor Changes
-------------

- Agent role - Respect the variable `checkmk_agent_host_name` when downloading host specific agents.
- The playbooks shipped with the collection were cleaned up and update. Just for awareness.

Breaking Changes / Porting Guide
--------------------------------

- Agent role - Remove host attribute `tag_agent` from the defaults. Should not be a breaking change, but be aware of it.

v0.14.0
=======

Deprecated Features
-------------------

- host_group module - The module was released with the module options `host_group_name` and `host_groups`. These have ben renamed to `name` and `groups` to align with our standards. The old names will be removed in a future release.

v0.13.0
=======

Major Changes
-------------

- Add service_group module.

Minor Changes
-------------

v0.12.0
=======

Major Changes
-------------

- Add contact_group module.

Minor Changes
-------------

- Agent role - Add option to download agent setup to control node and then upload to target.
- Downtime module - Improve readability of messages in case of API errors.

Bugfixes
--------

- Agent role - Fix timeouts on tasks delegated_to localhost.
- Downtime module - A human-readable error message is now printed if there's an API error.

New Modules
-----------

- checkmk.general.contact_group - Manage contact groups in Checkmk (bulk version).

v0.11.0
=======

Major Changes
-------------

- Add host_group module.
- Add tag_group module.

Minor Changes
-------------

- Agent role - (Actually in v0.10.0) Fix authentication handling, where several tasks would fail, when using a secret.
- Agent role - Add support for CME.

New Modules
-----------

- checkmk.general.host_group - Manage host groups in Checkmk (bulk version).
- checkmk.general.tag_group - Manage tag_group within Checkmk

v0.10.0
=======

Major Changes
-------------

- Add rule module.

Bugfixes
--------

- Host module - Now correctly setting the default folder when getting the current host state.

Known Issues
------------

- Rule exports made with Checkmk API on server versions <2.1.0p10 will not import correctly.

New Modules
-----------

- checkmk.general.rule - Manage rules in Checkmk.

v0.9.0
======

Minor Changes
-------------

- Server role - Improve OS support detection and enhance prerequisites installation.

Bugfixes
--------

- Host module - Do not raise an error, if a host already exists, or on updating a host's attributes while the hosts stays in the same folder.
- Server role - Fix and enhance additional repository handling on RedHat derivatives.

v0.8.0
======

Minor Changes
-------------

- Activation module - Make certificate validation of the Checkmk server configurable.
- Agent role - Add a boolean for whether to validate the SSL certificate of the Checkmk server used to retrieve agent packages.
- Agent role - Enable forced agent installation, skipping all possible constraints, like downgrades.
- Agent role - Make Checkmk server port for API calls configurable. By default the ports 80 and 443 are used according to the configured protocol.
- Discovery module - Make certificate validation of the Checkmk server configurable.
- Downtime module - Make certificate validation of the Checkmk server configurable.
- Folder module - Make certificate validation of the Checkmk server configurable.
- Host module - Make certificate validation of the Checkmk server configurable.
- Server role - Fix setup file verification on Debian derivatives. Using gpg instead of dpkg-sig now.

v0.7.0
======

Release Summary
---------------

Lots of love for the agent role!

Minor Changes
-------------

- Agent role - Check for agent updater and controller binaries. Skip registration if respective binary is missing.
- Agent role - Host attributes can be fully customized now.
- Agent role - Label role. This enables skipping or running tasks exclusively. See the README for a detailed list.
- Server role - Label role. This enables skipping or running tasks exclusively. See the README for a detailed list.

Bugfixes
--------

- Activation module - Fix possible race condition. (#123).
- Activation module - Fix waiting for activation completion (#103).
- Agent role - Support CFE properly.
- Agent role - Support both normal and automation users properly.

v0.6.0
======

Release Summary
---------------

Introducing upgrade management for Checkmk sites!

Major Changes
-------------

- Server role - Add support for automatically updating Checkmk. Read the role's README for important information!

Bugfixes
--------

- Agent role - Fix SELinux handling on RedHat.
- Agent role - Fix firewall handling on RedHat.

v0.5.2
======

Bugfixes
--------

- Fix usage of 'checkmk_agent_host_name'variable. Some tasks had 'inventory_hostname' hardcoded, which is not the desired behavior. This is fixed now.
- Increase HTTP timeout for the discovery module, because the discovery can take some time depending on the discovered device.

v0.5.1
======

Bugfixes
--------

- Fix leakage of admin password in server role.
- Fix usage of 'automation_xxx' and 'checkmk_agent_xxx'. 'automation_xxx' variables can still be used for API authentication, but the behavior is more consistent now.

v0.5.0
======

Minor Changes
-------------

- Add support for RedHat/CentOS 7 and 8 and compatible distributions to server role.
- Enable agent role to automatically add hosts to Checkmk during agent installation.
- Enable firewall management of the host to allow instant access to the agent.
- Enable firewall management of the host to allow instant access to the web interface of the server.
- Introduce ansible linting for roles and fix findings.

Bugfixes
--------

- Handle hosts, where systemd version is below 220. It is now possible to automatically install xinetd in those cases. This has to be enabled explicitely.

v0.4.0
======

Minor Changes
-------------

- Initial release of the Checkmk server role.
- The agent role now supports installing baked agents. It will try to install the host-specific agent and fall back to the GENERIC agent.
- The agent role now supports registering hosts for automatic updates and TLS encryption.

Bugfixes
--------

- Improved the exception handling of the discovery module.

v0.3.3
======

Bugfixes
--------

- The host module can now handle the trailing slash in the folder path returned by the REST API.

v0.3.2
======

Minor Changes
-------------

- Add agent role. Currently supports the vanilla agent.

v0.2.2
======

Minor Changes
-------------

- The discovery module will now be more verbose in case of an API error and print the actual error message from the API.

v0.2.1
======

Minor Changes
-------------

- Add hint, that running the activation module is required only once and not per host.
- Clean up variable assignments in activation module.
- Clean up variable assignments in discovery module.
- Improve construction of headers and base_url variables in activation module.
- Improve construction of headers and base_url variables in discovery module.
- Introduce quick fix for handling of HTTP 500 errors in discovery module.

v0.2.0
======

Major Changes
-------------

- Add downtime module. Kudos to Oliver Gaida (https://github.com/ogaida)!

Minor Changes
-------------

- The way how the API URL is being created is now more consistent. Thus, users can now skip the trailing "/" in the "server_url" for all modules. Thanks to Jan Petto (https://github.com/Edgxxar)!

Known Issues
------------

- Discovery module is not feature complete yet.
- Downtime module is not fully idempotent yet. This affects service downtimes and deletions.
- This release is still in development and a heavy work in progress.
- We might extract the API call handling into a separate Python module.

New Modules
-----------

- checkmk.general.downtime - Manage downtimes in Checkmk.

v0.1.0
======

Major Changes
-------------

- First release to Ansible Galaxy.

Minor Changes
-------------

- Activation is now site aware.

Known Issues
------------

- Discovery is not feature complete yet.
- This release is still in development and a heavy work in progress.

v0.0.2
======

Major Changes
-------------

- Major overhaul of folder module.
- Major overhaul of host module.

Known Issues
------------

- Activation is not site aware yet. All sites will be activated.
- Discovery is not feature complete yet.
- This release is still in development and a heavy work in progress.

v0.0.1
======

Major Changes
-------------

- Add activation module.
- Add discovery module.
- Add folder module.
- Add host module.
- Initial creation of collection structure and layout.

Known Issues
------------

- Activation is not site aware yet. All sites will be activated.
- Discovery is not feature complete yet.
- This release is still in development and a heavy work in progress.

New Modules
-----------

- checkmk.general.activation - Activate changes in Checkmk.
- checkmk.general.discovery - discovery services in Checkmk.
- checkmk.general.folder - Manage folders in Checkmk.
- checkmk.general.host - Manage hosts in Checkmk.

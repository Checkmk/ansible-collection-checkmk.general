=============================
tribe29.checkmk Release Notes
=============================

.. contents:: Topics


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

- tribe29.checkmk.contact_group - Manage contact groups in Checkmk (bulk version).

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

- tribe29.checkmk.host_group - Manage host groups in Checkmk (bulk version).
- tribe29.checkmk.tag_group - Manage tag_group within Checkmk

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

- tribe29.checkmk.rule - Manage rules in Checkmk.

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

- tribe29.checkmk.downtime - Manage downtimes in Checkmk.

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

- tribe29.checkmk.activation - Activate changes in Checkmk.
- tribe29.checkmk.discovery - discovery services in Checkmk.
- tribe29.checkmk.folder - Manage folders in Checkmk.
- tribe29.checkmk.host - Manage hosts in Checkmk.

=============================
tribe29.checkmk Release Notes
=============================

.. contents:: Topics


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

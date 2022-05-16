=============================
tribe29.checkmk Release Notes
=============================

.. contents:: Topics


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

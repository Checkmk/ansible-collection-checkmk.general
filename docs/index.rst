


.. _plugins_in_checkmk.general:

Checkmk.General
===============

Collection version 3.1.0

.. contents::
   :local:
   :depth: 1

Description
-----------

The official Checkmk Ansible collection - brought to you by the Checkmk company.

**Authors:**

* Marcel Arentz (https://github.com/godspeed-you)
* Robin Gierse (https://github.com/robin-checkmk)
* Lars Getwan (https://github.com/lgetwan)

**Supported ansible-core versions:**

* 2.12.0 or newer

.. raw:: html

  <p class="ansible-links">
    <a href="https://github.com/Checkmk/ansible-collection-checkmk.general/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc" aria-role="button" target="_blank" rel="noopener external">Issue Tracker</a>
    <a href="https://github.com/Checkmk/ansible-collection-checkmk.general" aria-role="button" target="_blank" rel="noopener external">Repository (Sources)</a>
  </p>



.. toctree::
    :maxdepth: 1


Plugin Index
------------

These are the plugins in the checkmk.general collection:


Modules
~~~~~~~

* :ansplugin:`activation module <checkmk.general.activation#module>` -- Activate changes in Checkmk.
* :ansplugin:`bakery module <checkmk.general.bakery#module>` -- Trigger baking and signing in the agent bakery.
* :ansplugin:`contact_group module <checkmk.general.contact_group#module>` -- Manage contact groups in Checkmk (bulk version).
* :ansplugin:`discovery module <checkmk.general.discovery#module>` -- Discover services in Checkmk.
* :ansplugin:`downtime module <checkmk.general.downtime#module>` -- Manage downtimes in Checkmk.
* :ansplugin:`folder module <checkmk.general.folder#module>` -- Manage folders in Checkmk.
* :ansplugin:`host module <checkmk.general.host#module>` -- Manage hosts in Checkmk.
* :ansplugin:`host_group module <checkmk.general.host_group#module>` -- Manage host groups in Checkmk (bulk version).
* :ansplugin:`password module <checkmk.general.password#module>` -- Manage passwords in checkmk.
* :ansplugin:`rule module <checkmk.general.rule#module>` -- Manage rules in Checkmk.
* :ansplugin:`service_group module <checkmk.general.service_group#module>` -- Manage service groups in Checkmk (bulk version).
* :ansplugin:`tag_group module <checkmk.general.tag_group#module>` -- Manage tag\_group within Checkmk
* :ansplugin:`user module <checkmk.general.user#module>` -- Manage users in Checkmk.

.. toctree::
    :maxdepth: 1
    :hidden:

    activation_module
    bakery_module
    contact_group_module
    discovery_module
    downtime_module
    folder_module
    host_module
    host_group_module
    password_module
    rule_module
    service_group_module
    tag_group_module
    user_module


Lookup Plugins
~~~~~~~~~~~~~~

* :ansplugin:`version lookup <checkmk.general.version#lookup>` -- Get the version of a Checkmk server

.. toctree::
    :maxdepth: 1
    :hidden:

    version_lookup



.. meta::
  :antsibull-docs: 2.19.1


.. _plugins_in_checkmk.general:

Checkmk.General
===============

Collection version 6.0.1

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
* Max Sickora (https://github.com/Max-checkmk)

**Supported ansible-core versions:**

* 2.15.0 or newer

.. ansible-links::

  - title: "Issue Tracker"
    url: "https://github.com/Checkmk/ansible-collection-checkmk.general/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc"
    external: true
  - title: "Repository (Sources)"
    url: "https://github.com/Checkmk/ansible-collection-checkmk.general"
    external: true




.. toctree::
    :maxdepth: 1

.. _plugin_index_for_checkmk.general:

Plugin Index
------------

These are the plugins in the checkmk.general collection:

.. _module_plugins_in_checkmk.general:

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
* :ansplugin:`password module <checkmk.general.password#module>` -- Manage passwords in Checkmk.
* :ansplugin:`rule module <checkmk.general.rule#module>` -- Manage rules in Checkmk.
* :ansplugin:`service_group module <checkmk.general.service_group#module>` -- Manage service groups in Checkmk (bulk version).
* :ansplugin:`site module <checkmk.general.site#module>` -- Manage distributed monitoring in Checkmk.
* :ansplugin:`tag_group module <checkmk.general.tag_group#module>` -- Manage tag groups in Checkmk.
* :ansplugin:`timeperiod module <checkmk.general.timeperiod#module>` -- Manage time periods in checkmk.
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
    site_module
    tag_group_module
    timeperiod_module
    user_module

.. _inventory_plugins_in_checkmk.general:

Inventory Plugins
~~~~~~~~~~~~~~~~~

* :ansplugin:`checkmk inventory <checkmk.general.checkmk#inventory>` -- Dynamic Inventory Source or Checkmk

.. toctree::
    :maxdepth: 1
    :hidden:

    checkmk_inventory

.. _lookup_plugins_in_checkmk.general:

Lookup Plugins
~~~~~~~~~~~~~~

* :ansplugin:`bakery lookup <checkmk.general.bakery#lookup>` -- Get the bakery status of a Checkmk server
* :ansplugin:`folder lookup <checkmk.general.folder#lookup>` -- Get folder attributes
* :ansplugin:`folders lookup <checkmk.general.folders#lookup>` -- Get various information about a folder
* :ansplugin:`host lookup <checkmk.general.host#lookup>` -- Get host attributes
* :ansplugin:`hosts lookup <checkmk.general.hosts#lookup>` -- Get various information about a host
* :ansplugin:`rule lookup <checkmk.general.rule#lookup>` -- Show a rule
* :ansplugin:`rules lookup <checkmk.general.rules#lookup>` -- Get a list rules
* :ansplugin:`ruleset lookup <checkmk.general.ruleset#lookup>` -- Show a ruleset
* :ansplugin:`rulesets lookup <checkmk.general.rulesets#lookup>` -- Search rulesets
* :ansplugin:`site lookup <checkmk.general.site#lookup>` -- Show the configuration of a site
* :ansplugin:`sites lookup <checkmk.general.sites#lookup>` -- Get a list of all sites
* :ansplugin:`version lookup <checkmk.general.version#lookup>` -- Get the version of a Checkmk server

.. toctree::
    :maxdepth: 1
    :hidden:

    bakery_lookup
    folder_lookup
    folders_lookup
    host_lookup
    hosts_lookup
    rule_lookup
    rules_lookup
    ruleset_lookup
    rulesets_lookup
    site_lookup
    sites_lookup
    version_lookup


.. _role_plugins_in_checkmk.general:

Role Index
----------

These are the roles in the checkmk.general collection:

* :ansplugin:`agent role <checkmk.general.agent#role>` -- Install Checkmk agents
* :ansplugin:`server role <checkmk.general.server#role>` -- Install and manage Checkmk servers

.. toctree::
    :maxdepth: 1
    :hidden:

    agent_role
    server_role

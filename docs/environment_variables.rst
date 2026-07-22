:orphan:

.. meta::
  :antsibull-docs: 2.24.0

.. _list_of_collection_env_vars:

Index of all Collection Environment Variables
=============================================

The following index documents all environment variables declared by plugins in collections.
Environment variables used by the ansible-core configuration are documented in :ref:`ansible_configuration_settings`.

.. envvar:: CHECKMK_VAR_API_AUTH_COOKIE

    The authentication cookie value if using cookie\-based authentication.

    *Used by:*
    :ansplugin:`checkmk.general.activation lookup plugin <checkmk.general.activation#lookup>`,
    :ansplugin:`checkmk.general.activations lookup plugin <checkmk.general.activations#lookup>`,
    :ansplugin:`checkmk.general.bakery lookup plugin <checkmk.general.bakery#lookup>`,
    :ansplugin:`checkmk.general.checkmk inventory plugin <checkmk.general.checkmk#inventory>`,
    :ansplugin:`checkmk.general.folder lookup plugin <checkmk.general.folder#lookup>`,
    :ansplugin:`checkmk.general.folders lookup plugin <checkmk.general.folders#lookup>`,
    :ansplugin:`checkmk.general.host lookup plugin <checkmk.general.host#lookup>`,
    :ansplugin:`checkmk.general.hosts lookup plugin <checkmk.general.hosts#lookup>`,
    :ansplugin:`checkmk.general.ldap\_connection lookup plugin <checkmk.general.ldap_connection#lookup>`,
    :ansplugin:`checkmk.general.ldap\_connections lookup plugin <checkmk.general.ldap_connections#lookup>`,
    :ansplugin:`checkmk.general.role lookup plugin <checkmk.general.role#lookup>`,
    :ansplugin:`checkmk.general.roles lookup plugin <checkmk.general.roles#lookup>`,
    :ansplugin:`checkmk.general.rule lookup plugin <checkmk.general.rule#lookup>`,
    :ansplugin:`checkmk.general.rules lookup plugin <checkmk.general.rules#lookup>`,
    :ansplugin:`checkmk.general.ruleset lookup plugin <checkmk.general.ruleset#lookup>`,
    :ansplugin:`checkmk.general.rulesets lookup plugin <checkmk.general.rulesets#lookup>`,
    :ansplugin:`checkmk.general.site lookup plugin <checkmk.general.site#lookup>`,
    :ansplugin:`checkmk.general.sites lookup plugin <checkmk.general.sites#lookup>`,
    :ansplugin:`checkmk.general.version lookup plugin <checkmk.general.version#lookup>`
.. envvar:: CHECKMK_VAR_API_AUTH_TYPE

    The authentication type to use ('bearer', 'basic', 'cookie').

    *Used by:*
    :ansplugin:`checkmk.general.activation lookup plugin <checkmk.general.activation#lookup>`,
    :ansplugin:`checkmk.general.activations lookup plugin <checkmk.general.activations#lookup>`,
    :ansplugin:`checkmk.general.bakery lookup plugin <checkmk.general.bakery#lookup>`,
    :ansplugin:`checkmk.general.checkmk inventory plugin <checkmk.general.checkmk#inventory>`,
    :ansplugin:`checkmk.general.folder lookup plugin <checkmk.general.folder#lookup>`,
    :ansplugin:`checkmk.general.folders lookup plugin <checkmk.general.folders#lookup>`,
    :ansplugin:`checkmk.general.host lookup plugin <checkmk.general.host#lookup>`,
    :ansplugin:`checkmk.general.hosts lookup plugin <checkmk.general.hosts#lookup>`,
    :ansplugin:`checkmk.general.ldap\_connection lookup plugin <checkmk.general.ldap_connection#lookup>`,
    :ansplugin:`checkmk.general.ldap\_connections lookup plugin <checkmk.general.ldap_connections#lookup>`,
    :ansplugin:`checkmk.general.role lookup plugin <checkmk.general.role#lookup>`,
    :ansplugin:`checkmk.general.roles lookup plugin <checkmk.general.roles#lookup>`,
    :ansplugin:`checkmk.general.rule lookup plugin <checkmk.general.rule#lookup>`,
    :ansplugin:`checkmk.general.rules lookup plugin <checkmk.general.rules#lookup>`,
    :ansplugin:`checkmk.general.ruleset lookup plugin <checkmk.general.ruleset#lookup>`,
    :ansplugin:`checkmk.general.rulesets lookup plugin <checkmk.general.rulesets#lookup>`,
    :ansplugin:`checkmk.general.site lookup plugin <checkmk.general.site#lookup>`,
    :ansplugin:`checkmk.general.sites lookup plugin <checkmk.general.sites#lookup>`,
    :ansplugin:`checkmk.general.version lookup plugin <checkmk.general.version#lookup>`
.. envvar:: CHECKMK_VAR_API_SECRET

    Automation secret for the REST API access.

    *Used by:*
    :ansplugin:`checkmk.general.activation lookup plugin <checkmk.general.activation#lookup>`,
    :ansplugin:`checkmk.general.activations lookup plugin <checkmk.general.activations#lookup>`,
    :ansplugin:`checkmk.general.bakery lookup plugin <checkmk.general.bakery#lookup>`,
    :ansplugin:`checkmk.general.checkmk inventory plugin <checkmk.general.checkmk#inventory>`,
    :ansplugin:`checkmk.general.folder lookup plugin <checkmk.general.folder#lookup>`,
    :ansplugin:`checkmk.general.folders lookup plugin <checkmk.general.folders#lookup>`,
    :ansplugin:`checkmk.general.host lookup plugin <checkmk.general.host#lookup>`,
    :ansplugin:`checkmk.general.hosts lookup plugin <checkmk.general.hosts#lookup>`,
    :ansplugin:`checkmk.general.ldap\_connection lookup plugin <checkmk.general.ldap_connection#lookup>`,
    :ansplugin:`checkmk.general.ldap\_connections lookup plugin <checkmk.general.ldap_connections#lookup>`,
    :ansplugin:`checkmk.general.role lookup plugin <checkmk.general.role#lookup>`,
    :ansplugin:`checkmk.general.roles lookup plugin <checkmk.general.roles#lookup>`,
    :ansplugin:`checkmk.general.rule lookup plugin <checkmk.general.rule#lookup>`,
    :ansplugin:`checkmk.general.rules lookup plugin <checkmk.general.rules#lookup>`,
    :ansplugin:`checkmk.general.ruleset lookup plugin <checkmk.general.ruleset#lookup>`,
    :ansplugin:`checkmk.general.rulesets lookup plugin <checkmk.general.rulesets#lookup>`,
    :ansplugin:`checkmk.general.site lookup plugin <checkmk.general.site#lookup>`,
    :ansplugin:`checkmk.general.sites lookup plugin <checkmk.general.sites#lookup>`,
    :ansplugin:`checkmk.general.version lookup plugin <checkmk.general.version#lookup>`
.. envvar:: CHECKMK_VAR_API_USER

    Automation user for the REST API access.

    *Used by:*
    :ansplugin:`checkmk.general.activation lookup plugin <checkmk.general.activation#lookup>`,
    :ansplugin:`checkmk.general.activations lookup plugin <checkmk.general.activations#lookup>`,
    :ansplugin:`checkmk.general.bakery lookup plugin <checkmk.general.bakery#lookup>`,
    :ansplugin:`checkmk.general.checkmk inventory plugin <checkmk.general.checkmk#inventory>`,
    :ansplugin:`checkmk.general.folder lookup plugin <checkmk.general.folder#lookup>`,
    :ansplugin:`checkmk.general.folders lookup plugin <checkmk.general.folders#lookup>`,
    :ansplugin:`checkmk.general.host lookup plugin <checkmk.general.host#lookup>`,
    :ansplugin:`checkmk.general.hosts lookup plugin <checkmk.general.hosts#lookup>`,
    :ansplugin:`checkmk.general.ldap\_connection lookup plugin <checkmk.general.ldap_connection#lookup>`,
    :ansplugin:`checkmk.general.ldap\_connections lookup plugin <checkmk.general.ldap_connections#lookup>`,
    :ansplugin:`checkmk.general.role lookup plugin <checkmk.general.role#lookup>`,
    :ansplugin:`checkmk.general.roles lookup plugin <checkmk.general.roles#lookup>`,
    :ansplugin:`checkmk.general.rule lookup plugin <checkmk.general.rule#lookup>`,
    :ansplugin:`checkmk.general.rules lookup plugin <checkmk.general.rules#lookup>`,
    :ansplugin:`checkmk.general.ruleset lookup plugin <checkmk.general.ruleset#lookup>`,
    :ansplugin:`checkmk.general.rulesets lookup plugin <checkmk.general.rulesets#lookup>`,
    :ansplugin:`checkmk.general.site lookup plugin <checkmk.general.site#lookup>`,
    :ansplugin:`checkmk.general.sites lookup plugin <checkmk.general.sites#lookup>`,
    :ansplugin:`checkmk.general.version lookup plugin <checkmk.general.version#lookup>`
.. envvar:: CHECKMK_VAR_EXCLUDE_TAGS

    List of host tags to exclude from the inventory.

    Any host that has at least one of the given tags set will be excluded.

    Tags must be given in the full Checkmk format :literal:`tag\_\<group\>\_\<value\>`\ , e.g. :literal:`tag\_criticality\_test` or :literal:`tag\_agent\_cmk\-agent`.

    *Used by:*
    :ansplugin:`checkmk.general.checkmk inventory plugin <checkmk.general.checkmk#inventory>`
.. envvar:: CHECKMK_VAR_FOLDER

    Restrict hosts to a specific folder path in Checkmk.

    Given as a regular path, e.g. :literal:`/linux/production`.

    Unless :literal:`recursive` is enabled, only hosts directly in the given folder are returned.

    All hosts are always fetched from the site and filtered on the client side, so this does not reduce the amount of data retrieved from Checkmk.

    *Used by:*
    :ansplugin:`checkmk.general.checkmk inventory plugin <checkmk.general.checkmk#inventory>`
.. envvar:: CHECKMK_VAR_LOWERCASE_HOSTS

    If set to :literal:`true`\ , all hostnames will be converted to lowercase in the inventory.

    *Used by:*
    :ansplugin:`checkmk.general.checkmk inventory plugin <checkmk.general.checkmk#inventory>`
.. envvar:: CHECKMK_VAR_RECURSIVE

    If set to :literal:`true` and a :literal:`folder` is defined, all subfolders are included recursively.

    Has no effect without :literal:`folder`.

    *Used by:*
    :ansplugin:`checkmk.general.checkmk inventory plugin <checkmk.general.checkmk#inventory>`
.. envvar:: CHECKMK_VAR_SERVER_URL

    URL of the Checkmk server

    *Used by:*
    :ansplugin:`checkmk.general.activation lookup plugin <checkmk.general.activation#lookup>`,
    :ansplugin:`checkmk.general.activations lookup plugin <checkmk.general.activations#lookup>`,
    :ansplugin:`checkmk.general.bakery lookup plugin <checkmk.general.bakery#lookup>`,
    :ansplugin:`checkmk.general.checkmk inventory plugin <checkmk.general.checkmk#inventory>`,
    :ansplugin:`checkmk.general.folder lookup plugin <checkmk.general.folder#lookup>`,
    :ansplugin:`checkmk.general.folders lookup plugin <checkmk.general.folders#lookup>`,
    :ansplugin:`checkmk.general.host lookup plugin <checkmk.general.host#lookup>`,
    :ansplugin:`checkmk.general.hosts lookup plugin <checkmk.general.hosts#lookup>`,
    :ansplugin:`checkmk.general.ldap\_connection lookup plugin <checkmk.general.ldap_connection#lookup>`,
    :ansplugin:`checkmk.general.ldap\_connections lookup plugin <checkmk.general.ldap_connections#lookup>`,
    :ansplugin:`checkmk.general.role lookup plugin <checkmk.general.role#lookup>`,
    :ansplugin:`checkmk.general.roles lookup plugin <checkmk.general.roles#lookup>`,
    :ansplugin:`checkmk.general.rule lookup plugin <checkmk.general.rule#lookup>`,
    :ansplugin:`checkmk.general.rules lookup plugin <checkmk.general.rules#lookup>`,
    :ansplugin:`checkmk.general.ruleset lookup plugin <checkmk.general.ruleset#lookup>`,
    :ansplugin:`checkmk.general.rulesets lookup plugin <checkmk.general.rulesets#lookup>`,
    :ansplugin:`checkmk.general.site lookup plugin <checkmk.general.site#lookup>`,
    :ansplugin:`checkmk.general.sites lookup plugin <checkmk.general.sites#lookup>`,
    :ansplugin:`checkmk.general.version lookup plugin <checkmk.general.version#lookup>`
.. envvar:: CHECKMK_VAR_SITE

    Site name.

    *Used by:*
    :ansplugin:`checkmk.general.activation lookup plugin <checkmk.general.activation#lookup>`,
    :ansplugin:`checkmk.general.activations lookup plugin <checkmk.general.activations#lookup>`,
    :ansplugin:`checkmk.general.bakery lookup plugin <checkmk.general.bakery#lookup>`,
    :ansplugin:`checkmk.general.checkmk inventory plugin <checkmk.general.checkmk#inventory>`,
    :ansplugin:`checkmk.general.folder lookup plugin <checkmk.general.folder#lookup>`,
    :ansplugin:`checkmk.general.folders lookup plugin <checkmk.general.folders#lookup>`,
    :ansplugin:`checkmk.general.host lookup plugin <checkmk.general.host#lookup>`,
    :ansplugin:`checkmk.general.hosts lookup plugin <checkmk.general.hosts#lookup>`,
    :ansplugin:`checkmk.general.ldap\_connection lookup plugin <checkmk.general.ldap_connection#lookup>`,
    :ansplugin:`checkmk.general.ldap\_connections lookup plugin <checkmk.general.ldap_connections#lookup>`,
    :ansplugin:`checkmk.general.role lookup plugin <checkmk.general.role#lookup>`,
    :ansplugin:`checkmk.general.roles lookup plugin <checkmk.general.roles#lookup>`,
    :ansplugin:`checkmk.general.rule lookup plugin <checkmk.general.rule#lookup>`,
    :ansplugin:`checkmk.general.rules lookup plugin <checkmk.general.rules#lookup>`,
    :ansplugin:`checkmk.general.ruleset lookup plugin <checkmk.general.ruleset#lookup>`,
    :ansplugin:`checkmk.general.rulesets lookup plugin <checkmk.general.rulesets#lookup>`,
    :ansplugin:`checkmk.general.site lookup plugin <checkmk.general.site#lookup>`,
    :ansplugin:`checkmk.general.sites lookup plugin <checkmk.general.sites#lookup>`,
    :ansplugin:`checkmk.general.version lookup plugin <checkmk.general.version#lookup>`
.. envvar:: CHECKMK_VAR_VALIDATE_CERTS

    Whether to validate SSL certificates.

    *Used by:*
    :ansplugin:`checkmk.general.activation lookup plugin <checkmk.general.activation#lookup>`,
    :ansplugin:`checkmk.general.activations lookup plugin <checkmk.general.activations#lookup>`,
    :ansplugin:`checkmk.general.bakery lookup plugin <checkmk.general.bakery#lookup>`,
    :ansplugin:`checkmk.general.checkmk inventory plugin <checkmk.general.checkmk#inventory>`,
    :ansplugin:`checkmk.general.folder lookup plugin <checkmk.general.folder#lookup>`,
    :ansplugin:`checkmk.general.folders lookup plugin <checkmk.general.folders#lookup>`,
    :ansplugin:`checkmk.general.host lookup plugin <checkmk.general.host#lookup>`,
    :ansplugin:`checkmk.general.hosts lookup plugin <checkmk.general.hosts#lookup>`,
    :ansplugin:`checkmk.general.ldap\_connection lookup plugin <checkmk.general.ldap_connection#lookup>`,
    :ansplugin:`checkmk.general.ldap\_connections lookup plugin <checkmk.general.ldap_connections#lookup>`,
    :ansplugin:`checkmk.general.role lookup plugin <checkmk.general.role#lookup>`,
    :ansplugin:`checkmk.general.roles lookup plugin <checkmk.general.roles#lookup>`,
    :ansplugin:`checkmk.general.rule lookup plugin <checkmk.general.rule#lookup>`,
    :ansplugin:`checkmk.general.rules lookup plugin <checkmk.general.rules#lookup>`,
    :ansplugin:`checkmk.general.ruleset lookup plugin <checkmk.general.ruleset#lookup>`,
    :ansplugin:`checkmk.general.rulesets lookup plugin <checkmk.general.rulesets#lookup>`,
    :ansplugin:`checkmk.general.site lookup plugin <checkmk.general.site#lookup>`,
    :ansplugin:`checkmk.general.sites lookup plugin <checkmk.general.sites#lookup>`,
    :ansplugin:`checkmk.general.version lookup plugin <checkmk.general.version#lookup>`

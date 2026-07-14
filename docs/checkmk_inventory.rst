.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: 2.24.0

.. Anchors

.. _ansible_collections.checkmk.general.checkmk_inventory:

.. Anchors: short name for ansible.builtin

.. Title

checkmk.general.checkmk inventory -- Dynamic Inventory Source or Checkmk
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This inventory plugin is part of the `checkmk.general collection <https://galaxy.ansible.com/ui/repo/published/checkmk/general/>`_ (version 8.1.0).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible\-galaxy collection install checkmk.general`.

    To use it in a playbook, specify: :code:`checkmk.general.checkmk`.

.. version_added


.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Get hosts from any checkmk site.
- Generate groups based on tag groups or sites in Checkmk.


.. Aliases


.. Requirements






.. Options

Parameters
----------

.. tabularcolumns:: \X{1}{3}\X{2}{3}

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1
  :class: longtable ansible-option-table

  * - Parameter
    - Comments

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-api_auth_cookie"></div>

      .. _ansible_collections.checkmk.general.checkmk_inventory__parameter-api_auth_cookie:

      .. rst-class:: ansible-option-title

      **api_auth_cookie**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-api_auth_cookie" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The authentication cookie value if using cookie\-based authentication.


      .. rst-class:: ansible-option-line

      :ansible-option-configuration:`Configuration:`

      - INI entry:

        .. code-block:: ini

          [checkmk_lookup]
          api_auth_cookie = VALUE


      - Environment variable: :envvar:`CHECKMK\_VAR\_API\_AUTH\_COOKIE`

      - Variable: checkmk\_var\_api\_auth\_cookie


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-api_auth_type"></div>

      .. _ansible_collections.checkmk.general.checkmk_inventory__parameter-api_auth_type:

      .. rst-class:: ansible-option-title

      **api_auth_type**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-api_auth_type" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The authentication type to use ('bearer', 'basic', 'cookie').


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"bearer"`

      .. rst-class:: ansible-option-line

      :ansible-option-configuration:`Configuration:`

      - INI entry:

        .. code-block:: ini

          [checkmk_lookup]
          api_auth_type = bearer


      - Environment variable: :envvar:`CHECKMK\_VAR\_API\_AUTH\_TYPE`

      - Variable: checkmk\_var\_api\_auth\_type


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-api_secret"></div>
        <div class="ansibleOptionAnchor" id="parameter-automation_secret"></div>

      .. _ansible_collections.checkmk.general.checkmk_inventory__parameter-api_secret:
      .. _ansible_collections.checkmk.general.checkmk_inventory__parameter-automation_secret:

      .. rst-class:: ansible-option-title

      **api_secret**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-api_secret" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-aliases:`aliases: automation_secret`

        :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Automation secret for the REST API access.


      .. rst-class:: ansible-option-line

      :ansible-option-configuration:`Configuration:`

      - INI entry:

        .. code-block:: ini

          [checkmk_lookup]
          api_secret = VALUE


      - Environment variable: :envvar:`CHECKMK\_VAR\_API\_SECRET`

      - Variable: checkmk\_var\_api\_secret


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-api_user"></div>
        <div class="ansibleOptionAnchor" id="parameter-automation_user"></div>

      .. _ansible_collections.checkmk.general.checkmk_inventory__parameter-api_user:
      .. _ansible_collections.checkmk.general.checkmk_inventory__parameter-automation_user:

      .. rst-class:: ansible-option-title

      **api_user**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-api_user" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-aliases:`aliases: automation_user`

        :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Automation user for the REST API access.


      .. rst-class:: ansible-option-line

      :ansible-option-configuration:`Configuration:`

      - INI entry:

        .. code-block:: ini

          [checkmk_lookup]
          api_user = VALUE


      - Environment variable: :envvar:`CHECKMK\_VAR\_API\_USER`

      - Variable: checkmk\_var\_api\_user


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-groupsources"></div>

      .. _ansible_collections.checkmk.general.checkmk_inventory__parameter-groupsources:

      .. rst-class:: ansible-option-title

      **groupsources**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-groupsources" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      List of sources for grouping

      Possible sources are :literal:`sites` and :literal:`hosttags`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-plugin"></div>

      .. _ansible_collections.checkmk.general.checkmk_inventory__parameter-plugin:

      .. rst-class:: ansible-option-title

      **plugin**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-plugin" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Name of the plugin. Should always be :literal:`checkmk.general.checkmk`.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"checkmk.general.checkmk"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-server_url"></div>

      .. _ansible_collections.checkmk.general.checkmk_inventory__parameter-server_url:

      .. rst-class:: ansible-option-title

      **server_url**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-server_url" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      URL of the Checkmk server


      .. rst-class:: ansible-option-line

      :ansible-option-configuration:`Configuration:`

      - INI entry:

        .. code-block:: ini

          [checkmk_lookup]
          server_url = VALUE


      - Environment variable: :envvar:`CHECKMK\_VAR\_SERVER\_URL`

      - Variable: checkmk\_var\_server\_url


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site"></div>

      .. _ansible_collections.checkmk.general.checkmk_inventory__parameter-site:

      .. rst-class:: ansible-option-title

      **site**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Site name.


      .. rst-class:: ansible-option-line

      :ansible-option-configuration:`Configuration:`

      - INI entry:

        .. code-block:: ini

          [checkmk_lookup]
          site = VALUE


      - Environment variable: :envvar:`CHECKMK\_VAR\_SITE`

      - Variable: checkmk\_var\_site


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-validate_certs"></div>

      .. _ansible_collections.checkmk.general.checkmk_inventory__parameter-validate_certs:

      .. rst-class:: ansible-option-title

      **validate_certs**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-validate_certs" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Whether to validate SSL certificates.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry-default:`true` :ansible-option-choices-default-mark:`← (default)`


      .. rst-class:: ansible-option-line

      :ansible-option-configuration:`Configuration:`

      - INI entry:

        .. code-block:: ini

          [checkmk_lookup]
          validate_certs = true


      - Environment variable: :envvar:`CHECKMK\_VAR\_VALIDATE\_CERTS`

      - Variable: checkmk\_var\_validate\_certs


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-want_ipv4"></div>

      .. _ansible_collections.checkmk.general.checkmk_inventory__parameter-want_ipv4:

      .. rst-class:: ansible-option-title

      **want_ipv4**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-want_ipv4" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Update ansible\_host variable with ip address from Checkmk


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>


.. note::

    Configuration entries listed above for each entry type (Ansible variable, environment variable, and so on) have a low to high priority order.
    For example, a variable that is lower in the list will override a variable that is higher up.
    The entry types are also ordered by precedence from low to high priority order.
    For example, an ansible.cfg entry (further up in the list) is overwritten by an Ansible variable (further down in the list).

.. Attributes


.. Notes

Notes
-----

.. note::
   - Because inventory plugins run before :literal:`group\_vars/` and :literal:`host\_vars/` are loaded, :literal:`checkmk\_var\_\*` values placed there are :strong:`not` visible to this plugin. Sources that :strong:`do` work are extra\-vars (\ :literal:`\-e`\ ), environment variables (\ :literal:`CHECKMK\_VAR\_\*`\ ) and :literal:`ansible.cfg` :literal:`[checkmk\_lookup]` entries.
   - Connection parameters are resolved from (in order of precedence) the value set directly on the plugin invocation, an Ansible variable of the form :literal:`checkmk\_var\_\*`\ , an environment variable of the form :literal:`CHECKMK\_VAR\_\*`\ , and the matching key under section :literal:`[checkmk\_lookup]` in :literal:`ansible.cfg`.

.. Seealso


.. Examples

Examples
--------

.. code-block:: yaml+jinja

    # To get started, you need to create a file called `checkmk.yml`, which contains
    # one of the example blocks below and use it as your inventory source.
    # E.g., with `ansible-inventory -i checkmk.yml --graph`.

    # Group all hosts based on both tag groups and sites:
    plugin: checkmk.general.checkmk
    server_url: "http://hostname/"
    site: "sitename"
    api_user: "cmkadmin"
    api_secret: "******"
    validate_certs: false
    groupsources: ["hosttags", "sites"]
    want_ipv4: False

    # ---------------------------------------------------------------------------
    # Using environment variables for credentials
    # ---------------------------------------------------------------------------
    # Connection parameters can be provided via environment variables instead of
    # writing them into the inventory file. The supported variables are:
    #   CHECKMK_VAR_SERVER_URL, CHECKMK_VAR_SITE,
    #   CHECKMK_VAR_API_USER, CHECKMK_VAR_API_SECRET,
    #   CHECKMK_VAR_VALIDATE_CERTS, CHECKMK_VAR_API_AUTH_TYPE

    # Minimal inventory file when using environment variables:
    plugin: checkmk.general.checkmk
    groupsources: ["hosttags", "sites"]

    # ---------------------------------------------------------------------------
    # Using Ansible variables for credentials
    # ---------------------------------------------------------------------------
    # Connection parameters can also be provided via Ansible variables, e.g.
    # via extra-vars (`-e`). Note that vars from group_vars/ or host_vars/
    # are NOT visible here, because inventory plugins run before those are loaded.
    # The supported variable names follow the scheme checkmk_var_<parameter>:
    #   checkmk_var_server_url, checkmk_var_site,
    #   checkmk_var_api_user, checkmk_var_api_secret,
    #   checkmk_var_validate_certs, checkmk_var_api_auth_type



.. Facts


.. Return values


..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- Max Sickora (@max-checkmk)


.. Extra links

Collection links
~~~~~~~~~~~~~~~~

.. ansible-links::

  - title: "Issue Tracker"
    url: "https://github.com/Checkmk/ansible-collection-checkmk.general/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc"
    external: true
  - title: "Repository (Sources)"
    url: "https://github.com/Checkmk/ansible-collection-checkmk.general"
    external: true


.. Parsing errors

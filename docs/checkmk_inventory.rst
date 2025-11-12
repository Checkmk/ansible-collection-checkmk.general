.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: 2.22.0

.. Anchors

.. _ansible_collections.checkmk.general.checkmk_inventory:

.. Anchors: short name for ansible.builtin

.. Title

checkmk.general.checkmk inventory -- Dynamic Inventory Source or Checkmk
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This inventory plugin is part of the `checkmk.general collection <https://galaxy.ansible.com/ui/repo/published/checkmk/general/>`_ (version 6.3.0).

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

      Authentication cookie for the Checkmk session.


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

      Type of authentication to use.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`"bearer"` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`"basic"`
      - :ansible-option-choices-entry:`"cookie"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-automation_secret"></div>

      .. _ansible_collections.checkmk.general.checkmk_inventory__parameter-automation_secret:

      .. rst-class:: ansible-option-title

      **automation_secret**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-automation_secret" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The secret to authenticate your automation user. If not set the module will fall back to the environment variable :literal:`CHECKMK\_VAR\_AUTOMATION\_SECRET`.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-automation_user"></div>

      .. _ansible_collections.checkmk.general.checkmk_inventory__parameter-automation_user:

      .. rst-class:: ansible-option-title

      **automation_user**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-automation_user" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The automation user you want to use. It has to be an 'Automation' user, not a normal one. If not set the module will fall back to the environment variable :literal:`CHECKMK\_VAR\_AUTOMATION\_USER`.


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

      The base url of your Checkmk server including the protocol but excluding the site. If not set the module will fall back to the environment variable :literal:`CHECKMK\_VAR\_SERVER\_URL`.


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

      The site you want to connect to. This will be appended to the server\_url as part of the API request url. If not set the module will fall back to the environment variable :literal:`CHECKMK\_VAR\_SITE`.


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

      Whether to validate the SSL certificate of the Checkmk server. If not set the module will fall back to the environment variable :literal:`CHECKMK\_VAR\_VALIDATE\_CERTS`.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry-default:`true` :ansible-option-choices-default-mark:`← (default)`


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


.. Attributes


.. Notes


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
    automation_user: "cmkadmin"
    automation_secret: "******"
    validate_certs: false
    groupsources: ["hosttags", "sites"]
    want_ipv4: False



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

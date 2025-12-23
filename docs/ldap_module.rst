.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: 2.23.0

.. Anchors

.. _ansible_collections.checkmk.general.ldap_module:

.. Anchors: short name for ansible.builtin

.. Title

checkmk.general.ldap module -- Manage LDAP connectors.
++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `checkmk.general collection <https://galaxy.ansible.com/ui/repo/published/checkmk/general/>`_ (version 6.6.0).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible\-galaxy collection install checkmk.general`.

    To use it in a playbook, specify: :code:`checkmk.general.ldap`.

.. version_added

.. rst-class:: ansible-version-added

New in checkmk.general 6.1.0

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Manage LDAP connectors, including creation, updating, and deletion.


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

      .. _ansible_collections.checkmk.general.ldap_module__parameter-api_auth_cookie:

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

      .. _ansible_collections.checkmk.general.ldap_module__parameter-api_auth_type:

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

      .. _ansible_collections.checkmk.general.ldap_module__parameter-automation_secret:

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

      .. _ansible_collections.checkmk.general.ldap_module__parameter-automation_user:

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
        <div class="ansibleOptionAnchor" id="parameter-ldap_config"></div>

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config:

      .. rst-class:: ansible-option-title

      **ldap_config**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Configuration parameters for the LDAP.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/general_properties"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/general_properties:

      .. rst-class:: ansible-option-title

      **general_properties**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/general_properties" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary` / :ansible-option-required:`required`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      General properties of an LDAP connection.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/general_properties/comment"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/general_properties/comment:

      .. rst-class:: ansible-option-title

      **comment**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/general_properties/comment" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      An optional comment to explain the purpose.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/general_properties/description"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/general_properties/description:

      .. rst-class:: ansible-option-title

      **description**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/general_properties/description" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Add a title or describe this rule.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/general_properties/documentation_url"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/general_properties/documentation_url:

      .. rst-class:: ansible-option-title

      **documentation_url**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/general_properties/documentation_url" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Add a documentation URL for this rule.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/general_properties/id"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/general_properties/id:

      .. rst-class:: ansible-option-title

      **id**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/general_properties/id" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      An LDAP connection ID string.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/general_properties/rule_activation"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/general_properties/rule_activation:

      .. rst-class:: ansible-option-title

      **rule_activation**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/general_properties/rule_activation" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Selecting 'deactivated' will disable the rule, but it will

      remain in the configuration.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`"activated"` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`"deactivated"`


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/groups"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/groups:

      .. rst-class:: ansible-option-title

      **groups**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/groups" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The LDAP group configuration.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`{"group\_base\_dn": "", "member\_attribute": "", "search\_filter": "", "search\_scope": "search\_whole\_subtree"}`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/groups/group_base_dn"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/groups/group_base_dn:

      .. rst-class:: ansible-option-title

      **group_base_dn**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/groups/group_base_dn" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Give a base distinguished name here. All group accounts to

      synchronize must be located below this one.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/groups/member_attribute"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/groups/member_attribute:

      .. rst-class:: ansible-option-title

      **member_attribute**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/groups/member_attribute" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Member attribute.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/groups/search_filter"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/groups/search_filter:

      .. rst-class:: ansible-option-title

      **search_filter**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/groups/search_filter" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Define an optional LDAP filter which is used during group related

      LDAP searches. It can be used to only handle a subset of the groups

      below the given group base DN.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/groups/search_scope"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/groups/search_scope:

      .. rst-class:: ansible-option-title

      **search_scope**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/groups/search_scope" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Scope to be used in LDAP searches.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`"search\_whole\_subtree"` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`"search\_only\_base\_dn\_entry"`
      - :ansible-option-choices-entry:`"search\_all\_one\_level\_below\_base\_dn"`


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/ldap_connection"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/ldap_connection:

      .. rst-class:: ansible-option-title

      **ldap_connection**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/ldap_connection" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The LDAP connection configuration.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`{}`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/ldap_connection/bind_credentials"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/ldap_connection/bind_credentials:

      .. rst-class:: ansible-option-title

      **bind_credentials**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/ldap_connection/bind_credentials" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The credentials used to connect to the LDAP server.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/ldap_connection/bind_credentials/bind_dn"></div>

      .. raw:: latex

        \hspace{0.06\textwidth}\begin{minipage}[t]{0.26\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/ldap_connection/bind_credentials/bind_dn:

      .. rst-class:: ansible-option-title

      **bind_dn**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/ldap_connection/bind_credentials/bind_dn" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The distinguished name of the user account which is used to

      bind to the LDAP server. This user account must have read

      access to the LDAP directory.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/ldap_connection/bind_credentials/explicit_password"></div>

      .. raw:: latex

        \hspace{0.06\textwidth}\begin{minipage}[t]{0.26\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/ldap_connection/bind_credentials/explicit_password:

      .. rst-class:: ansible-option-title

      **explicit_password**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/ldap_connection/bind_credentials/explicit_password" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The explicit password.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/ldap_connection/bind_credentials/password_store_id"></div>

      .. raw:: latex

        \hspace{0.06\textwidth}\begin{minipage}[t]{0.26\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/ldap_connection/bind_credentials/password_store_id:

      .. rst-class:: ansible-option-title

      **password_store_id**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/ldap_connection/bind_credentials/password_store_id" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The ID of the password inside the password store.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/ldap_connection/bind_credentials/type"></div>

      .. raw:: latex

        \hspace{0.06\textwidth}\begin{minipage}[t]{0.26\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/ldap_connection/bind_credentials/type:

      .. rst-class:: ansible-option-title

      **type**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/ldap_connection/bind_credentials/type" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Whether to take the password from the password store or to

      provide it explicitly.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`"explicit"` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`"store"`


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/ldap_connection/connect_timeout"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/ldap_connection/connect_timeout:

      .. rst-class:: ansible-option-title

      **connect_timeout**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/ldap_connection/connect_timeout" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`float`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Timeout for the initial connection to the LDAP server in seconds.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/ldap_connection/connection_suffix"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/ldap_connection/connection_suffix:

      .. rst-class:: ansible-option-title

      **connection_suffix**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/ldap_connection/connection_suffix" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The LDAP connection suffix can be used to distinguish equal named

      objects (name conflicts), for example user accounts, from different

      LDAP connections.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/ldap_connection/directory_type"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/ldap_connection/directory_type:

      .. rst-class:: ansible-option-title

      **directory_type**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/ldap_connection/directory_type" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The credentials to be used to connect to the LDAP server. The used

      account must not be allowed to do any changes in the directory the

      whole connection is read only. In some environment an anonymous

      connect/bind is allowed, in this case you don't have to configure

      anything here.It must be possible to list all needed user and group

      objects from the directory.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/ldap_connection/directory_type/domain"></div>

      .. raw:: latex

        \hspace{0.06\textwidth}\begin{minipage}[t]{0.26\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/ldap_connection/directory_type/domain:

      .. rst-class:: ansible-option-title

      **domain**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/ldap_connection/directory_type/domain" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Configure the DNS domain name of your Active directory domain

      here, Checkmk will then query this domain for it's closest

      domain controller to communicate with.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/ldap_connection/directory_type/failover_servers"></div>

      .. raw:: latex

        \hspace{0.06\textwidth}\begin{minipage}[t]{0.26\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/ldap_connection/directory_type/failover_servers:

      .. rst-class:: ansible-option-title

      **failover_servers**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/ldap_connection/directory_type/failover_servers" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      When the connection to the first server fails with connect

      specific errors like timeouts or some other network related

      problems, the connect mechanism will try to use this server

      instead of the server configured above. If you use persistent

      connections (default), the connection is being used until the

      LDAP is not reachable or the local webserver is restarted.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/ldap_connection/directory_type/ldap_server"></div>

      .. raw:: latex

        \hspace{0.06\textwidth}\begin{minipage}[t]{0.26\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/ldap_connection/directory_type/ldap_server:

      .. rst-class:: ansible-option-title

      **ldap_server**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/ldap_connection/directory_type/ldap_server" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Set the host address of the LDAP server. Might be an IP

      address or resolvable host name.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/ldap_connection/directory_type/type"></div>

      .. raw:: latex

        \hspace{0.06\textwidth}\begin{minipage}[t]{0.26\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/ldap_connection/directory_type/type:

      .. rst-class:: ansible-option-title

      **type**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/ldap_connection/directory_type/type" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Select the software the LDAP directory is based on.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`"active\_directory\_manual"` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`"active\_directory\_automatic"`
      - :ansible-option-choices-entry:`"open\_ldap"`
      - :ansible-option-choices-entry:`"389\_directory\_server"`


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/ldap_connection/ldap_version"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/ldap_connection/ldap_version:

      .. rst-class:: ansible-option-title

      **ldap_version**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/ldap_connection/ldap_version" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`integer`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The selected LDAP version the LDAP server is serving. Most modern

      servers use LDAP version 3.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`2`
      - :ansible-option-choices-entry:`3`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/ldap_connection/page_size"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/ldap_connection/page_size:

      .. rst-class:: ansible-option-title

      **page_size**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/ldap_connection/page_size" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`integer`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      LDAP searches can be performed in paginated mode, for example to

      improve the performance. This enables pagination and configures the

      size of the pages.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/ldap_connection/response_timeout"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/ldap_connection/response_timeout:

      .. rst-class:: ansible-option-title

      **response_timeout**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/ldap_connection/response_timeout" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`integer`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Timeout for the reply coming from the LDAP server in seconds.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/ldap_connection/ssl_encryption"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/ldap_connection/ssl_encryption:

      .. rst-class:: ansible-option-title

      **ssl_encryption**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/ldap_connection/ssl_encryption" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Connect to the LDAP server with a SSL encrypted connection. The

      trusted certificates authorities configured in Checkmk will be used

      to validate the certificate provided by the LDAP server.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`"disable\_ssl"` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`"enable\_ssl"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/ldap_connection/tcp_port"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/ldap_connection/tcp_port:

      .. rst-class:: ansible-option-title

      **tcp_port**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/ldap_connection/tcp_port" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`integer`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The TCP port to be used to connect to the LDAP server.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/other"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/other:

      .. rst-class:: ansible-option-title

      **other**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/other" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Other config options for the LDAP connection.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`{}`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/other/sync_interval"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/other/sync_interval:

      .. rst-class:: ansible-option-title

      **sync_interval**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/other/sync_interval" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      This option defines the interval of the LDAP synchronization.

      This setting is only used by sites which have the automatic user

      synchronization enabled.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`{}`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/other/sync_interval/days"></div>

      .. raw:: latex

        \hspace{0.06\textwidth}\begin{minipage}[t]{0.26\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/other/sync_interval/days:

      .. rst-class:: ansible-option-title

      **days**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/other/sync_interval/days" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`integer`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The sync interval in days


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`0`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/other/sync_interval/hours"></div>

      .. raw:: latex

        \hspace{0.06\textwidth}\begin{minipage}[t]{0.26\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/other/sync_interval/hours:

      .. rst-class:: ansible-option-title

      **hours**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/other/sync_interval/hours" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`integer`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The sync interval in hours


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`0`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/other/sync_interval/minutes"></div>

      .. raw:: latex

        \hspace{0.06\textwidth}\begin{minipage}[t]{0.26\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/other/sync_interval/minutes:

      .. rst-class:: ansible-option-title

      **minutes**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/other/sync_interval/minutes" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`integer`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The sync interval in minutes


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`5`

      .. raw:: html

        </div>



  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/sync_plugins"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/sync_plugins:

      .. rst-class:: ansible-option-title

      **sync_plugins**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/sync_plugins" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The LDAP sync plug\-ins configuration.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`{"alias": "", "authentication\_expiration": "", "disable\_notifications": "", "email\_address": "", "mega\_menu\_icons": "", "navigation\_bar\_icons": "", "pager": "", "show\_mode": "", "start\_url": "", "temperature\_unit": "", "ui\_sidebar\_position": "", "ui\_theme": "", "visibility\_of\_hosts\_or\_services": ""}`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/sync_plugins/alias"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/sync_plugins/alias:

      .. rst-class:: ansible-option-title

      **alias**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/sync_plugins/alias" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Enables and populates the alias attribute of the Setup user by

      synchronizing an attribute from the LDAP user account. By default

      the LDAP attribute cn is used.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/sync_plugins/authentication_expiration"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/sync_plugins/authentication_expiration:

      .. rst-class:: ansible-option-title

      **authentication_expiration**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/sync_plugins/authentication_expiration" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      This plug\-in when enabled fetches all information which is needed to

      check whether or not an already authenticated user should be

      deauthenticated, e.g. because the password has changed in LDAP or

      the account has been locked.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/sync_plugins/contact_group_membership"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/sync_plugins/contact_group_membership:

      .. rst-class:: ansible-option-title

      **contact_group_membership**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/sync_plugins/contact_group_membership" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      This plug\-in allows you to synchronize group memberships of the LDAP

      user account into the contact groups of the Checkmk user account.

      This allows you to use the group based permissions of your LDAP

      directory in Checkmk.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/sync_plugins/contact_group_membership/handle_nested"></div>

      .. raw:: latex

        \hspace{0.06\textwidth}\begin{minipage}[t]{0.26\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/sync_plugins/contact_group_membership/handle_nested:

      .. rst-class:: ansible-option-title

      **handle_nested**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/sync_plugins/contact_group_membership/handle_nested" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Once you enable this option, this plug\-in will not only

      handle direct group memberships, instead it will also dig

      into nested groups and treat the members of those groups as

      contact group members as well. Please bear in mind that this

      feature might increase the execution time of your LDAP sync.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`false` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/sync_plugins/contact_group_membership/sync_from_other_connections"></div>

      .. raw:: latex

        \hspace{0.06\textwidth}\begin{minipage}[t]{0.26\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/sync_plugins/contact_group_membership/sync_from_other_connections:

      .. rst-class:: ansible-option-title

      **sync_from_other_connections**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/sync_plugins/contact_group_membership/sync_from_other_connections" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The LDAP attribute whose contents shall be synced into this

      custom attribute.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`[]`

      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/sync_plugins/disable_notifications"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/sync_plugins/disable_notifications:

      .. rst-class:: ansible-option-title

      **disable_notifications**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/sync_plugins/disable_notifications" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      When this option is enabled you will not get any alerts or other

      notifications via email, SMS or similar. This overrides all other

      notification settings and rules, so make sure that you know what

      you do. Moreover you can specify a time range where no notifications

      are generated.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/sync_plugins/email_address"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/sync_plugins/email_address:

      .. rst-class:: ansible-option-title

      **email_address**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/sync_plugins/email_address" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Synchronizes the email of the LDAP user account into Checkmk when

      enabled


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/sync_plugins/groups_to_custom_user_attributes"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/sync_plugins/groups_to_custom_user_attributes:

      .. rst-class:: ansible-option-title

      **groups_to_custom_user_attributes**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/sync_plugins/groups_to_custom_user_attributes" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      This plug\-in allows you to synchronize group memberships of the LDAP

      user account into the custom attributes of the Checkmk user account.

      This allows you to use the group based permissions of your LDAP

      directory in Checkmk.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/sync_plugins/groups_to_custom_user_attributes/groups_to_sync"></div>

      .. raw:: latex

        \hspace{0.06\textwidth}\begin{minipage}[t]{0.26\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/sync_plugins/groups_to_custom_user_attributes/groups_to_sync:

      .. rst-class:: ansible-option-title

      **groups_to_sync**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/sync_plugins/groups_to_custom_user_attributes/groups_to_sync" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The groups to be synchronized.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/sync_plugins/groups_to_custom_user_attributes/groups_to_sync/attribute_to_set"></div>

      .. raw:: latex

        \hspace{0.08\textwidth}\begin{minipage}[t]{0.24\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/sync_plugins/groups_to_custom_user_attributes/groups_to_sync/attribute_to_set:

      .. rst-class:: ansible-option-title

      **attribute_to_set**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/sync_plugins/groups_to_custom_user_attributes/groups_to_sync/attribute_to_set" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The attribute to set


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/sync_plugins/groups_to_custom_user_attributes/groups_to_sync/group_cn"></div>

      .. raw:: latex

        \hspace{0.08\textwidth}\begin{minipage}[t]{0.24\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/sync_plugins/groups_to_custom_user_attributes/groups_to_sync/group_cn:

      .. rst-class:: ansible-option-title

      **group_cn**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/sync_plugins/groups_to_custom_user_attributes/groups_to_sync/group_cn" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The common name of the group.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/sync_plugins/groups_to_custom_user_attributes/groups_to_sync/value"></div>

      .. raw:: latex

        \hspace{0.08\textwidth}\begin{minipage}[t]{0.24\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/sync_plugins/groups_to_custom_user_attributes/groups_to_sync/value:

      .. rst-class:: ansible-option-title

      **value**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/sync_plugins/groups_to_custom_user_attributes/groups_to_sync/value" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The value to set


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/sync_plugins/groups_to_custom_user_attributes/handle_nested"></div>

      .. raw:: latex

        \hspace{0.06\textwidth}\begin{minipage}[t]{0.26\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/sync_plugins/groups_to_custom_user_attributes/handle_nested:

      .. rst-class:: ansible-option-title

      **handle_nested**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/sync_plugins/groups_to_custom_user_attributes/handle_nested" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Once you enable this option, this plug\-in will not only

      handle direct group memberships, instead it will also dig

      into nested groups and treat the members of those groups as

      contact group members as well. Please bear in mind that this

      feature might increase the execution time of your LDAP sync.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`false` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/sync_plugins/groups_to_custom_user_attributes/sync_from_other_connections"></div>

      .. raw:: latex

        \hspace{0.06\textwidth}\begin{minipage}[t]{0.26\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/sync_plugins/groups_to_custom_user_attributes/sync_from_other_connections:

      .. rst-class:: ansible-option-title

      **sync_from_other_connections**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/sync_plugins/groups_to_custom_user_attributes/sync_from_other_connections" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The LDAP attribute whose contents shall be synced into this

      custom attribute.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`[]`

      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/sync_plugins/groups_to_roles"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/sync_plugins/groups_to_roles:

      .. rst-class:: ansible-option-title

      **groups_to_roles**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/sync_plugins/groups_to_roles" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Configures the roles of the user depending on its group memberships

      in LDAP. Please note, additionally the user is assigned to the

      Default Roles. Deactivate them if unwanted.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/sync_plugins/groups_to_roles/handle_nested"></div>

      .. raw:: latex

        \hspace{0.06\textwidth}\begin{minipage}[t]{0.26\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/sync_plugins/groups_to_roles/handle_nested:

      .. rst-class:: ansible-option-title

      **handle_nested**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/sync_plugins/groups_to_roles/handle_nested" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Once you enable this option, this plug\-in will not only

      handle direct group memberships, instead it will also dig

      into nested groups and treat the members of those groups as

      contact group members as well. Please bear in mind that this

      feature might increase the execution time of your LDAP sync.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/sync_plugins/groups_to_roles/roles_to_sync"></div>

      .. raw:: latex

        \hspace{0.06\textwidth}\begin{minipage}[t]{0.26\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/sync_plugins/groups_to_roles/roles_to_sync:

      .. rst-class:: ansible-option-title

      **roles_to_sync**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/sync_plugins/groups_to_roles/roles_to_sync" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The roles to be handled.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/sync_plugins/groups_to_roles/roles_to_sync/groups"></div>

      .. raw:: latex

        \hspace{0.08\textwidth}\begin{minipage}[t]{0.24\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/sync_plugins/groups_to_roles/roles_to_sync/groups:

      .. rst-class:: ansible-option-title

      **groups**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/sync_plugins/groups_to_roles/roles_to_sync/groups" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The LDAP groups that should be considered.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/sync_plugins/groups_to_roles/roles_to_sync/groups/group_dn"></div>

      .. raw:: latex

        \hspace{0.1\textwidth}\begin{minipage}[t]{0.22\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/sync_plugins/groups_to_roles/roles_to_sync/groups/group_dn:

      .. rst-class:: ansible-option-title

      **group_dn**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/sync_plugins/groups_to_roles/roles_to_sync/groups/group_dn" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      This group must be defined within the scope

      of the LDAP Group Settings


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/sync_plugins/groups_to_roles/roles_to_sync/groups/search_in"></div>

      .. raw:: latex

        \hspace{0.1\textwidth}\begin{minipage}[t]{0.22\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/sync_plugins/groups_to_roles/roles_to_sync/groups/search_in:

      .. rst-class:: ansible-option-title

      **search_in**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/sync_plugins/groups_to_roles/roles_to_sync/groups/search_in" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      An existing ldap connection. Use

      this\_connection to select the current

      connection.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"this\_connection"`

      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/sync_plugins/groups_to_roles/roles_to_sync/role"></div>

      .. raw:: latex

        \hspace{0.08\textwidth}\begin{minipage}[t]{0.24\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/sync_plugins/groups_to_roles/roles_to_sync/role:

      .. rst-class:: ansible-option-title

      **role**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/sync_plugins/groups_to_roles/roles_to_sync/role" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The role id as defined in Checkmk.


      .. raw:: html

        </div>



  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/sync_plugins/mega_menu_icons"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/sync_plugins/mega_menu_icons:

      .. rst-class:: ansible-option-title

      **mega_menu_icons**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/sync_plugins/mega_menu_icons" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      When enabled, in the mega menus you can select between two

      options. Have a green icon only for the headlines – the 'topics' –

      for lean design. Or have a colored icon for every entry so that over

      time you can zoom in more quickly to a specific entry.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/sync_plugins/navigation_bar_icons"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/sync_plugins/navigation_bar_icons:

      .. rst-class:: ansible-option-title

      **navigation_bar_icons**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/sync_plugins/navigation_bar_icons" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      With this option enabled you can define if icons in the navigation

      bar should show a title or not. This gives you the possibility to

      save some space in the UI.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/sync_plugins/pager"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/sync_plugins/pager:

      .. rst-class:: ansible-option-title

      **pager**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/sync_plugins/pager" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      When enabled, this plug\-in synchronizes a field of the users LDAP

      account to the pager attribute of the Setup user accounts, which is

      then forwarded to the monitoring core and can be used for

      notifications. By default the LDAP attribute mobile is used.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/sync_plugins/show_mode"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/sync_plugins/show_mode:

      .. rst-class:: ansible-option-title

      **show_mode**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/sync_plugins/show_mode" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      In some places like e.g. the main menu Checkmk divides features,

      filters, input fields etc. in two categories, showing more or less

      entries. With this option you can set a default mode for unvisited

      menus. Alternatively, you can enforce to show more, so that the

      round button with the three dots is not shown at all.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/sync_plugins/start_url"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/sync_plugins/start_url:

      .. rst-class:: ansible-option-title

      **start_url**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/sync_plugins/start_url" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The start URL to display in main frame.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/sync_plugins/temperature_unit"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/sync_plugins/temperature_unit:

      .. rst-class:: ansible-option-title

      **temperature_unit**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/sync_plugins/temperature_unit" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Set the temperature unit used for graphs and perfometers. The default

      unit can be configured here.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/sync_plugins/ui_sidebar_position"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/sync_plugins/ui_sidebar_position:

      .. rst-class:: ansible-option-title

      **ui_sidebar_position**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/sync_plugins/ui_sidebar_position" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The sidebar position


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/sync_plugins/ui_theme"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/sync_plugins/ui_theme:

      .. rst-class:: ansible-option-title

      **ui_theme**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/sync_plugins/ui_theme" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The user interface theme


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/sync_plugins/visibility_of_hosts_or_services"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/sync_plugins/visibility_of_hosts_or_services:

      .. rst-class:: ansible-option-title

      **visibility_of_hosts_or_services**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/sync_plugins/visibility_of_hosts_or_services" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      When this option is checked, the status GUI will only display hosts

      and services that the user is a contact for \- even they have the

      permission for seeing all objects.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/users"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/users:

      .. rst-class:: ansible-option-title

      **users**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/users" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The LDAP user configuration.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`{"create\_users": "on\_sync", "filter\_group": "", "search\_filter": "", "search\_scope": "search\_whole\_subtree", "umlauts\_in\_user\_ids": "keep\_umlauts", "user\_base\_dn": "", "user\_id\_attribute": "", "user\_id\_case": "dont\_convert\_to\_lowercase"}`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/users/create_users"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/users/create_users:

      .. rst-class:: ansible-option-title

      **create_users**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/users/create_users" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Create user accounts during sync or on the first login.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"on\_login"`
      - :ansible-option-choices-entry-default:`"on\_sync"` :ansible-option-choices-default-mark:`← (default)`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/users/filter_group"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/users/filter_group:

      .. rst-class:: ansible-option-title

      **filter_group**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/users/filter_group" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      DN of a group object which is used to filter the users.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/users/search_filter"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/users/search_filter:

      .. rst-class:: ansible-option-title

      **search_filter**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/users/search_filter" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Optional LDAP filter.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/users/search_scope"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/users/search_scope:

      .. rst-class:: ansible-option-title

      **search_scope**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/users/search_scope" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Scope to be used in LDAP searches.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`"search\_whole\_subtree"` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`"search\_only\_base\_dn\_entry"`
      - :ansible-option-choices-entry:`"search\_all\_one\_level\_below\_base\_dn"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/users/umlauts_in_user_ids"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/users/umlauts_in_user_ids:

      .. rst-class:: ansible-option-title

      **umlauts_in_user_ids**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/users/umlauts_in_user_ids" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Checkmk does not support special characters in User\-IDs. However, to

      deal with LDAP users having umlauts in their User\-IDs you previously

      had the choice to replace umlauts with other characters. This option

      is still available for backward compatibility, but you are advised

      to use the 'keep\_umlauts' option for new installations.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`"keep\_umlauts"` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`"replace\_umlauts"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/users/user_base_dn"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/users/user_base_dn:

      .. rst-class:: ansible-option-title

      **user_base_dn**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/users/user_base_dn" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Give a base distinguished name here. All user accounts to

      synchronize must be located below this one.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/users/user_id_attribute"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/users/user_id_attribute:

      .. rst-class:: ansible-option-title

      **user_id_attribute**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/users/user_id_attribute" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      User ID attribute.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldap_config/users/user_id_case"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.ldap_module__parameter-ldap_config/users/user_id_case:

      .. rst-class:: ansible-option-title

      **user_id_case**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldap_config/users/user_id_case" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Convert imported User\-IDs to lower case during synchronization or

      leave as is.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`"dont\_convert\_to\_lowercase"` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`"convert\_to\_lowercase"`


      .. raw:: html

        </div>



  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-server_url"></div>

      .. _ansible_collections.checkmk.general.ldap_module__parameter-server_url:

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

      .. _ansible_collections.checkmk.general.ldap_module__parameter-site:

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
        <div class="ansibleOptionAnchor" id="parameter-state"></div>

      .. _ansible_collections.checkmk.general.ldap_module__parameter-state:

      .. rst-class:: ansible-option-title

      **state**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-state" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Desired state of the LDAP.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`"present"` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`"absent"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-validate_certs"></div>

      .. _ansible_collections.checkmk.general.ldap_module__parameter-validate_certs:

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


.. Attributes


.. Notes


.. Seealso


.. Examples

Examples
--------

.. code-block:: yaml+jinja

    - name: Create a LDAP configuration
      checkmk.general.ldap:
        server_url: "http://myserver/"
        site: "mysite"
        automation_auth_type: "bearer"
        automation_user: "myuser"
        automation_secret: "mysecret"
        ldap_config:
          general_properties:
            id: "test_ldap_defaults"
          ldap_connection:
            directory_type:
              type: "open_ldap"
              ldap_server: "my.ldap.server.tld"
        state: "present"

    - name: Delete a LDAP configuration
      checkmk.general.ldap:
        server_url: "http://myserver/"
        site: "mysite"
        automation_auth_type: "bearer"
        automation_user: "myuser"
        automation_secret: "mysecret"
        ldap_config:
          id: "test_ldap_defaults"
        state: "absent"

    - name: Create a complex LDAP connector
      checkmk.general.ldap:
        server_url: "http://myserver/"
        site: "mysite"
        automation_auth_type: "bearer"
        automation_user: "myuser"
        automation_secret: "mysecret"
        ldap_config:
          general_properties:
            id: "test_ldap_complex"
            rule_activation: activated
            comment: "This is a complex example."
            description: "A complex example"
            documentation_url: "www.example.com"
          ldap_connection:
            directory_type:
              type: "open_ldap"
              ldap_server: "my.ldap.server.tld"
              failover_servers:
                - my2nd.ldap.server.tld
                - my3rd.ldap.server.tld
            bind_credentials:
              bind_dn: "ldap-ro"
              type: store
              password_store_id: "ldap_ro"
            ssl_encryption: enable_ssl
            tcp_port: 663
            connect_timeout: 3
            ldap_version: 3
            page_size: 2000
            response_timeout: 8
          users:
            user_base_dn: "OU=Users,DC=example,DC=com"
            search_scope: search_whole_subtree
            search_filter: "(objectclass=inetOrgPerson)"
            user_id_attribute: uid
            user_id_case: convert_to_lowercase
            create_users: on_login
          groups:
            group_base_dn: "OU=Groups,DC=example,DC=com"
            search_scope: search_only_base_dn_entry
            search_filter: "(objectclass=posixGroup)"
            member_attribute: "uniquemember"
          sync_plugins:
            alias: custom_user_alias
            visibility_of_hosts_or_services: visibility
            contact_group_membership:
              handle_nested: true
            groups_to_custom_user_attributes:
              handle_nested: true
              groups_to_sync:
                - group_cn: CN=megamenu,OU=Groups,DC=example,DC=com
                  attribute_to_set: mega_menu_icons
                  value: per_entry
            groups_to_roles:
              handle_nested: true
              roles_to_sync:
                - role: admin
                  groups:
                    - group_dn: CN=admins,OU=Groups,DC=example,DC=com
                      search_in: this_connection
        state: "present"

    - name: Update all LDAP connectors
      checkmk.general.ldap:
        server_url: "http://myserver/"
        site: "mysite"
        automation_auth_type: "bearer"
        automation_user: "myuser"
        automation_secret: "mysecret"
        ldap_config: "{{ item.extensions | combine(checkmk_var_comment_update, recursive=true) }}"
        state: "present"
      vars:
        checkmk_var_comment_update:
          general_properties:
            comment: New comment
      loop: "{{ lookup('checkmk.general.ldap_connections',
                            server_url='http://myserver/',
                            site='mysite',
                            automation_user='myuser',
                            automation_secret='mysecret',
                            )
                     }}"
      loop_control:
        label: "{{ item.extensions.general_properties.id }}"



.. Facts


.. Return values

Return Values
-------------
Common return values are documented :ref:`here <common_return_values>`, the following are the fields unique to this module:

.. tabularcolumns:: \X{1}{3}\X{2}{3}

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1
  :class: longtable ansible-option-table

  * - Key
    - Description

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-content"></div>

      .. _ansible_collections.checkmk.general.ldap_module__return-content:

      .. rst-class:: ansible-option-title

      **content**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-content" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Content of the LDAP object.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` when state is present and LDAP created or updated.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-diff"></div>

      .. _ansible_collections.checkmk.general.ldap_module__return-diff:

      .. rst-class:: ansible-option-title

      **diff**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-diff" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The diff between the current and desired state.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` when in diff mode


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-http_code"></div>

      .. _ansible_collections.checkmk.general.ldap_module__return-http_code:

      .. rst-class:: ansible-option-title

      **http_code**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-http_code" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`integer`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      HTTP code returned by the Checkmk API.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` always


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-msg"></div>

      .. _ansible_collections.checkmk.general.ldap_module__return-msg:

      .. rst-class:: ansible-option-title

      **msg**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-msg" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The output message that the module generates.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` always


      .. raw:: html

        </div>



..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- Lars Getwan (@lgetwan)


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

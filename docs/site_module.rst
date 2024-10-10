.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: 2.15.0

.. Anchors

.. _ansible_collections.checkmk.general.site_module:

.. Anchors: short name for ansible.builtin

.. Title

checkmk.general.site module -- Manage distributed monitoring in Checkmk.
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `checkmk.general collection <https://galaxy.ansible.com/ui/repo/published/checkmk/general/>`_ (version 5.3.0).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible-galaxy collection install checkmk.general`.

    To use it in a playbook, specify: :code:`checkmk.general.site`.

.. version_added

.. rst-class:: ansible-version-added

New in checkmk.general 5.3.0

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Manage distributed monitoring within Checkmk.


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
        <div class="ansibleOptionAnchor" id="parameter-automation_secret"></div>

      .. _ansible_collections.checkmk.general.site_module__parameter-automation_secret:

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

      The secret to authenticate your automation user.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-automation_user"></div>

      .. _ansible_collections.checkmk.general.site_module__parameter-automation_user:

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

      The automation user you want to use. It has to be an 'Automation' user, not a normal one.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-server_url"></div>

      .. _ansible_collections.checkmk.general.site_module__parameter-server_url:

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

      The base url of your Checkmk server including the protocol.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site"></div>

      .. _ansible_collections.checkmk.general.site_module__parameter-site:

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

      The site you want to connect to.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection"></div>

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection:

      .. rst-class:: ansible-option-title

      **site_connection**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The settings of the site.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/authentication"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/authentication:

      .. rst-class:: ansible-option-title

      **authentication**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/authentication" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The authentication data for a configuration connection.

      Only required when the :ansopt:`checkmk.general.site#module:state` is :ansval:`login`.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/authentication/password"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/authentication/password:

      .. rst-class:: ansible-option-title

      **password**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/authentication/password" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The password for the username provided.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/authentication/username"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/authentication/username:

      .. rst-class:: ansible-option-title

      **username**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/authentication/username" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      A user with administrative permissions.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/site_config"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/site_config:

      .. rst-class:: ansible-option-title

      **site_config**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/site_config" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      A site's connection.

      Only required when that :ansopt:`checkmk.general.site#module:state` is :ansval:`present`.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/site_config/basic_settings"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/site_config/basic_settings:

      .. rst-class:: ansible-option-title

      **basic_settings**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/site_config/basic_settings" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      A site's basic settings.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/site_config/basic_settings/alias"></div>

      .. raw:: latex

        \hspace{0.06\textwidth}\begin{minipage}[t]{0.26\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/site_config/basic_settings/alias:

      .. rst-class:: ansible-option-title

      **alias**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/site_config/basic_settings/alias" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The alias of the site.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/site_config/basic_settings/customer"></div>

      .. raw:: latex

        \hspace{0.06\textwidth}\begin{minipage}[t]{0.26\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/site_config/basic_settings/customer:

      .. rst-class:: ansible-option-title

      **customer**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/site_config/basic_settings/customer" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The customer of the site (Managed Edition - CME only).


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/site_config/basic_settings/site_id"></div>

      .. raw:: latex

        \hspace{0.06\textwidth}\begin{minipage}[t]{0.26\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/site_config/basic_settings/site_id:

      .. rst-class:: ansible-option-title

      **site_id**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/site_config/basic_settings/site_id" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The site ID.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/site_config/configuration_connection"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/site_config/configuration_connection:

      .. rst-class:: ansible-option-title

      **configuration_connection**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/site_config/configuration_connection" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      A site's configuration connection.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/site_config/configuration_connection/direct_login_to_web_gui_allowed"></div>

      .. raw:: latex

        \hspace{0.06\textwidth}\begin{minipage}[t]{0.26\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/site_config/configuration_connection/direct_login_to_web_gui_allowed:

      .. rst-class:: ansible-option-title

      **direct_login_to_web_gui_allowed**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/site_config/configuration_connection/direct_login_to_web_gui_allowed" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      When enabled, this site is marked for synchronization every

      time a web GUI related option is changed and users are

      allowed to login to the web GUI of this site.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry-default:`true` :ansible-option-choices-default-mark:`← (default)`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/site_config/configuration_connection/disable_remote_configuration"></div>

      .. raw:: latex

        \hspace{0.06\textwidth}\begin{minipage}[t]{0.26\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/site_config/configuration_connection/disable_remote_configuration:

      .. rst-class:: ansible-option-title

      **disable_remote_configuration**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/site_config/configuration_connection/disable_remote_configuration" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      It is a good idea to disable access to Setup completely on

      the remote site. Otherwise a user who does not now about

      the replication could make local changes that are overridden

      at the next configuration activation.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry-default:`true` :ansible-option-choices-default-mark:`← (default)`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/site_config/configuration_connection/enable_replication"></div>

      .. raw:: latex

        \hspace{0.06\textwidth}\begin{minipage}[t]{0.26\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/site_config/configuration_connection/enable_replication:

      .. rst-class:: ansible-option-title

      **enable_replication**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/site_config/configuration_connection/enable_replication" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Replication allows you to manage several monitoring sites

      with a logically centralized setup.

      Remote sites receive their configuration

      from the central sites.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`false` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/site_config/configuration_connection/ignore_tls_errors"></div>

      .. raw:: latex

        \hspace{0.06\textwidth}\begin{minipage}[t]{0.26\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/site_config/configuration_connection/ignore_tls_errors:

      .. rst-class:: ansible-option-title

      **ignore_tls_errors**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/site_config/configuration_connection/ignore_tls_errors" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      This might be needed to make the synchronization accept

      problems with SSL certificates when using an SSL secured

      connection. We encourage you to always understand TLS issues

      and fix them, though!


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`false` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/site_config/configuration_connection/replicate_event_console"></div>

      .. raw:: latex

        \hspace{0.06\textwidth}\begin{minipage}[t]{0.26\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/site_config/configuration_connection/replicate_event_console:

      .. rst-class:: ansible-option-title

      **replicate_event_console**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/site_config/configuration_connection/replicate_event_console" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      This option enables the distribution of global settings and

      rules of the Event Console to the remote site. Any change in

      the local Event Console settings will mark the site as needing

      to sync. A synchronization will automatically reload

      the Event Console of the remote site.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry-default:`true` :ansible-option-choices-default-mark:`← (default)`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/site_config/configuration_connection/replicate_extensions"></div>

      .. raw:: latex

        \hspace{0.06\textwidth}\begin{minipage}[t]{0.26\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/site_config/configuration_connection/replicate_extensions:

      .. rst-class:: ansible-option-title

      **replicate_extensions**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/site_config/configuration_connection/replicate_extensions" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      If you enable the replication of MKPs then during each

      activation of changes MKPs that are installed on your central site

      and all other files below the :literal:`$OMD\_ROOT/local/` directory will be

      transferred to the remote site. All other MKPs and

      files below :literal:`$OMD\_ROOT/local/` on the remote site will be removed.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry-default:`true` :ansible-option-choices-default-mark:`← (default)`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/site_config/configuration_connection/url_of_remote_site"></div>

      .. raw:: latex

        \hspace{0.06\textwidth}\begin{minipage}[t]{0.26\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/site_config/configuration_connection/url_of_remote_site:

      .. rst-class:: ansible-option-title

      **url_of_remote_site**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/site_config/configuration_connection/url_of_remote_site" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      URL of the remote site including :literal:`/check\_mk/`.

      This URL can be the same as the URL prefix of the status

      connection, but with :literal:`/check\_mk/` appended.

      Here it must always be an absolute URL, though.

      Unfortunately, this field is required by the REST API,

      even if there is no configuration connection enabled.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"http://localhost/nonexistant/check\_mk/"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/site_config/configuration_connection/user_sync"></div>

      .. raw:: latex

        \hspace{0.06\textwidth}\begin{minipage}[t]{0.26\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/site_config/configuration_connection/user_sync:

      .. rst-class:: ansible-option-title

      **user_sync**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/site_config/configuration_connection/user_sync" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      By default the users are synchronized automatically in

      the interval configured in the connection. For example

      the LDAP connector synchronizes the users every five minutes

      by default. The interval can be changed for each connection

      individually in the connection settings. Please note that

      the synchronization is only performed on the master site

      in distributed setups by default.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/site_config/configuration_connection/user_sync/ldap_connections"></div>

      .. raw:: latex

        \hspace{0.08\textwidth}\begin{minipage}[t]{0.24\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/site_config/configuration_connection/user_sync/ldap_connections:

      .. rst-class:: ansible-option-title

      **ldap_connections**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/site_config/configuration_connection/user_sync/ldap_connections" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      A list of ldap connections to synchronize.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/site_config/configuration_connection/user_sync/sync_with_ldap_connections"></div>

      .. raw:: latex

        \hspace{0.08\textwidth}\begin{minipage}[t]{0.24\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/site_config/configuration_connection/user_sync/sync_with_ldap_connections:

      .. rst-class:: ansible-option-title

      **sync_with_ldap_connections**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/site_config/configuration_connection/user_sync/sync_with_ldap_connections" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Sync with ldap connections.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"ldap"`
      - :ansible-option-choices-entry-default:`"all"` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`"disabled"`


      .. raw:: html

        </div>



  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/site_config/status_connection"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/site_config/status_connection:

      .. rst-class:: ansible-option-title

      **status_connection**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/site_config/status_connection" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      A site's status connection.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/site_config/status_connection/connect_timeout"></div>

      .. raw:: latex

        \hspace{0.06\textwidth}\begin{minipage}[t]{0.26\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/site_config/status_connection/connect_timeout:

      .. rst-class:: ansible-option-title

      **connect_timeout**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/site_config/status_connection/connect_timeout" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`integer`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The time that the GUI waits for a connection to the site

      to be established before the site is considered to be

      unreachable.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`2`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/site_config/status_connection/connection"></div>

      .. raw:: latex

        \hspace{0.06\textwidth}\begin{minipage}[t]{0.26\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/site_config/status_connection/connection:

      .. rst-class:: ansible-option-title

      **connection**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/site_config/status_connection/connection" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      When connecting to sites on remote servers, please

      make sure that Livestatus over TCP is activated there.

      You can use UNIX sockets to connect to foreign sites on

      localhost.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/site_config/status_connection/connection/encrypted"></div>

      .. raw:: latex

        \hspace{0.08\textwidth}\begin{minipage}[t]{0.24\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/site_config/status_connection/connection/encrypted:

      .. rst-class:: ansible-option-title

      **encrypted**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/site_config/status_connection/connection/encrypted" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Enable encryption for the connection.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/site_config/status_connection/connection/host"></div>

      .. raw:: latex

        \hspace{0.08\textwidth}\begin{minipage}[t]{0.24\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/site_config/status_connection/connection/host:

      .. rst-class:: ansible-option-title

      **host**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/site_config/status_connection/connection/host" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The IP or domain name of the host

      running the remote site.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/site_config/status_connection/connection/path"></div>

      .. raw:: latex

        \hspace{0.08\textwidth}\begin{minipage}[t]{0.24\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/site_config/status_connection/connection/path:

      .. rst-class:: ansible-option-title

      **path**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/site_config/status_connection/connection/path" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      When the connection name is unix,

      this is the path to the unix socket.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/site_config/status_connection/connection/port"></div>

      .. raw:: latex

        \hspace{0.08\textwidth}\begin{minipage}[t]{0.24\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/site_config/status_connection/connection/port:

      .. rst-class:: ansible-option-title

      **port**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/site_config/status_connection/connection/port" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`integer`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The Livestatus TCP port to connect to.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/site_config/status_connection/connection/socket_type"></div>

      .. raw:: latex

        \hspace{0.08\textwidth}\begin{minipage}[t]{0.24\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/site_config/status_connection/connection/socket_type:

      .. rst-class:: ansible-option-title

      **socket_type**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/site_config/status_connection/connection/socket_type" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The connection type.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"tcp"`
      - :ansible-option-choices-entry:`"tcp6"`
      - :ansible-option-choices-entry:`"unix"`
      - :ansible-option-choices-entry:`"local"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/site_config/status_connection/connection/verify"></div>

      .. raw:: latex

        \hspace{0.08\textwidth}\begin{minipage}[t]{0.24\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/site_config/status_connection/connection/verify:

      .. rst-class:: ansible-option-title

      **verify**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/site_config/status_connection/connection/verify" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Verify remote site's certificate.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/site_config/status_connection/disable_in_status_gui"></div>

      .. raw:: latex

        \hspace{0.06\textwidth}\begin{minipage}[t]{0.26\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/site_config/status_connection/disable_in_status_gui:

      .. rst-class:: ansible-option-title

      **disable_in_status_gui**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/site_config/status_connection/disable_in_status_gui" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      If you disable a connection, then no data of this site will

      be shown in the status GUI. The replication is not affected

      by this, however.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`false` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/site_config/status_connection/persistent_connection"></div>

      .. raw:: latex

        \hspace{0.06\textwidth}\begin{minipage}[t]{0.26\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/site_config/status_connection/persistent_connection:

      .. rst-class:: ansible-option-title

      **persistent_connection**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/site_config/status_connection/persistent_connection" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      If you enable persistent connections then Multisite

      will try to keep open a number of connections

      to the remote sites.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`false` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/site_config/status_connection/proxy"></div>

      .. raw:: latex

        \hspace{0.06\textwidth}\begin{minipage}[t]{0.26\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/site_config/status_connection/proxy:

      .. rst-class:: ansible-option-title

      **proxy**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/site_config/status_connection/proxy" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The Livestatus Proxy Daemon configuration attributes.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/site_config/status_connection/proxy/global_settings"></div>

      .. raw:: latex

        \hspace{0.08\textwidth}\begin{minipage}[t]{0.24\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/site_config/status_connection/proxy/global_settings:

      .. rst-class:: ansible-option-title

      **global_settings**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/site_config/status_connection/proxy/global_settings" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      When :ansopt:`checkmk.general.site#module:site\_connection.site\_config.status\_connection.proxy.use\_livestatus\_daemon`

      is set to :ansval:`with\_proxy`\ ,

      you can set this to :ansval:`true` to use global setting or

      :ansval:`false` to use custom parameters.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/site_config/status_connection/proxy/params"></div>

      .. raw:: latex

        \hspace{0.08\textwidth}\begin{minipage}[t]{0.24\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/site_config/status_connection/proxy/params:

      .. rst-class:: ansible-option-title

      **params**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/site_config/status_connection/proxy/params" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The Livestatus Proxy Daemon parameters.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/site_config/status_connection/proxy/params/cache"></div>

      .. raw:: latex

        \hspace{0.1\textwidth}\begin{minipage}[t]{0.22\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/site_config/status_connection/proxy/params/cache:

      .. rst-class:: ansible-option-title

      **cache**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/site_config/status_connection/proxy/params/cache" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Enable caching of several non-status queries.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry-default:`true` :ansible-option-choices-default-mark:`← (default)`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/site_config/status_connection/proxy/params/channel_timeout"></div>

      .. raw:: latex

        \hspace{0.1\textwidth}\begin{minipage}[t]{0.22\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/site_config/status_connection/proxy/params/channel_timeout:

      .. rst-class:: ansible-option-title

      **channel_timeout**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/site_config/status_connection/proxy/params/channel_timeout" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`integer`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The timeout waiting for a free channel.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`3`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/site_config/status_connection/proxy/params/channels"></div>

      .. raw:: latex

        \hspace{0.1\textwidth}\begin{minipage}[t]{0.22\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/site_config/status_connection/proxy/params/channels:

      .. rst-class:: ansible-option-title

      **channels**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/site_config/status_connection/proxy/params/channels" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`integer`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The number of channels to keep open.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`5`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/site_config/status_connection/proxy/params/connect_retry"></div>

      .. raw:: latex

        \hspace{0.1\textwidth}\begin{minipage}[t]{0.22\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/site_config/status_connection/proxy/params/connect_retry:

      .. rst-class:: ansible-option-title

      **connect_retry**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/site_config/status_connection/proxy/params/connect_retry" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`integer`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The cooling period after failed

      connect or heartbeat.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`4`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/site_config/status_connection/proxy/params/heartbeat"></div>

      .. raw:: latex

        \hspace{0.1\textwidth}\begin{minipage}[t]{0.22\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/site_config/status_connection/proxy/params/heartbeat:

      .. rst-class:: ansible-option-title

      **heartbeat**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/site_config/status_connection/proxy/params/heartbeat" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The heartbeat interval and timeout

      configuration.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/site_config/status_connection/proxy/params/heartbeat/interval"></div>

      .. raw:: latex

        \hspace{0.12\textwidth}\begin{minipage}[t]{0.2\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/site_config/status_connection/proxy/params/heartbeat/interval:

      .. rst-class:: ansible-option-title

      **interval**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/site_config/status_connection/proxy/params/heartbeat/interval" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`integer`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The heartbeat interval

      for the TCP connection.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`5`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/site_config/status_connection/proxy/params/heartbeat/timeout"></div>

      .. raw:: latex

        \hspace{0.12\textwidth}\begin{minipage}[t]{0.2\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/site_config/status_connection/proxy/params/heartbeat/timeout:

      .. rst-class:: ansible-option-title

      **timeout**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/site_config/status_connection/proxy/params/heartbeat/timeout" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`integer`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The heartbeat timeout

      for the TCP connection.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`2`

      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/site_config/status_connection/proxy/params/query_timeout"></div>

      .. raw:: latex

        \hspace{0.1\textwidth}\begin{minipage}[t]{0.22\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/site_config/status_connection/proxy/params/query_timeout:

      .. rst-class:: ansible-option-title

      **query_timeout**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/site_config/status_connection/proxy/params/query_timeout" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`integer`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The total query timeout.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`120`

      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/site_config/status_connection/proxy/tcp"></div>

      .. raw:: latex

        \hspace{0.08\textwidth}\begin{minipage}[t]{0.24\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/site_config/status_connection/proxy/tcp:

      .. rst-class:: ansible-option-title

      **tcp**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/site_config/status_connection/proxy/tcp" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Allow access to Livestatus via TCP.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/site_config/status_connection/proxy/tcp/only_from"></div>

      .. raw:: latex

        \hspace{0.1\textwidth}\begin{minipage}[t]{0.22\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/site_config/status_connection/proxy/tcp/only_from:

      .. rst-class:: ansible-option-title

      **only_from**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/site_config/status_connection/proxy/tcp/only_from" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Restrict access to these IP addresses.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/site_config/status_connection/proxy/tcp/port"></div>

      .. raw:: latex

        \hspace{0.1\textwidth}\begin{minipage}[t]{0.22\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/site_config/status_connection/proxy/tcp/port:

      .. rst-class:: ansible-option-title

      **port**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/site_config/status_connection/proxy/tcp/port" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`integer`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The TCP port to open.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/site_config/status_connection/proxy/tcp/tls"></div>

      .. raw:: latex

        \hspace{0.1\textwidth}\begin{minipage}[t]{0.22\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/site_config/status_connection/proxy/tcp/tls:

      .. rst-class:: ansible-option-title

      **tls**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/site_config/status_connection/proxy/tcp/tls" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Encrypt TCP Livestatus connections.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`false` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/site_config/status_connection/proxy/use_livestatus_daemon"></div>

      .. raw:: latex

        \hspace{0.08\textwidth}\begin{minipage}[t]{0.24\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/site_config/status_connection/proxy/use_livestatus_daemon:

      .. rst-class:: ansible-option-title

      **use_livestatus_daemon**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/site_config/status_connection/proxy/use_livestatus_daemon" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Use Livestatus daemon with direct connection

      or with Livestatus proxy.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"with\_proxy"`
      - :ansible-option-choices-entry:`"direct"`


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/site_config/status_connection/status_host"></div>

      .. raw:: latex

        \hspace{0.06\textwidth}\begin{minipage}[t]{0.26\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/site_config/status_connection/status_host:

      .. rst-class:: ansible-option-title

      **status_host**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/site_config/status_connection/status_host" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      By specifying a status host for each non-local connection

      you prevent Multisite from running into timeouts when

      remote sites do not respond.

      :emphasis:`This setting can be omitted, when`

      :ansopt:`checkmk.general.site#module:site\_connection.site\_config.status\_connection.proxy.use\_livestatus\_daemon`

      :emphasis:`is set to` :ansval:`with\_proxy`\ !


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/site_config/status_connection/status_host/host"></div>

      .. raw:: latex

        \hspace{0.08\textwidth}\begin{minipage}[t]{0.24\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/site_config/status_connection/status_host/host:

      .. rst-class:: ansible-option-title

      **host**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/site_config/status_connection/status_host/host" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The host name of the status host.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/site_config/status_connection/status_host/site"></div>

      .. raw:: latex

        \hspace{0.08\textwidth}\begin{minipage}[t]{0.24\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/site_config/status_connection/status_host/site:

      .. rst-class:: ansible-option-title

      **site**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/site_config/status_connection/status_host/site" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The site ID of the status host.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/site_config/status_connection/status_host/status_host_set"></div>

      .. raw:: latex

        \hspace{0.08\textwidth}\begin{minipage}[t]{0.24\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/site_config/status_connection/status_host/status_host_set:

      .. rst-class:: ansible-option-title

      **status_host_set**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/site_config/status_connection/status_host/status_host_set" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      enabled for 'use the following status host' and

      disabled for 'no status host'


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"enabled"`
      - :ansible-option-choices-entry-default:`"disabled"` :ansible-option-choices-default-mark:`← (default)`


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_connection/site_config/status_connection/url_prefix"></div>

      .. raw:: latex

        \hspace{0.06\textwidth}\begin{minipage}[t]{0.26\textwidth}

      .. _ansible_collections.checkmk.general.site_module__parameter-site_connection/site_config/status_connection/url_prefix:

      .. rst-class:: ansible-option-title

      **url_prefix**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_connection/site_config/status_connection/url_prefix" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The URL prefix will be prepended to links of addons like

      NagVis when a link to such applications points to a host

      or service on that site.


      .. raw:: html

        </div>




  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site_id"></div>

      .. _ansible_collections.checkmk.general.site_module__parameter-site_id:

      .. rst-class:: ansible-option-title

      **site_id**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_id" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The site ID to manage.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-state"></div>

      .. _ansible_collections.checkmk.general.site_module__parameter-state:

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

      The desired state of this site connection.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`"present"` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`"absent"`
      - :ansible-option-choices-entry:`"login"`
      - :ansible-option-choices-entry:`"logout"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-validate_certs"></div>

      .. _ansible_collections.checkmk.general.site_module__parameter-validate_certs:

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

      Whether to validate the SSL certificate of the Checkmk server.


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

    - name: "Add a remote site with configuration replication."
      checkmk.general.site:
        server_url: "http://myserver/"
        site: "mysite"
        automation_user: "myuser"
        automation_secret: "mysecret"
        site_id: "myremotesite"
        site_connection:
          site_config:
            status_connection:
              connection:
                socket_type: tcp
                port: 6557
                encrypted: true
                host: localhost
                verify: true
              proxy:
                use_livestatus_daemon: "direct"
              connect_timeout: 2
              status_host:
                status_host_set: "disabled"
              url_prefix: "/myremotesite/"
            configuration_connection:
              enable_replication: true
              url_of_remote_site: "http://localhost/myremotesite/check_mk/"
            basic_settings:
              site_id: "myremotesite"
              customer: "provider"
              alias: "My Remote Site"
        state: "present"

    - name: "Log into a remote site."
      checkmk.general.site:
        server_url: "http://myserver/"
        site: "mysite"
        automation_user: "myuser"
        automation_secret: "mysecret"
        site_id: "myremotesite"
        site_connection:
          authentication:
            username: "myremote_admin"
            password: "highly_secret"
        state: "login"

    - name: "Log out from a remote site."
      checkmk.general.site:
        server_url: "http://myserver/"
        site: "mysite"
        automation_user: "myuser"
        automation_secret: "mysecret"
        site_id: "myremotesite"
        state: "logout"

    - name: "Delete a remote site."
      checkmk.general.site:
        server_url: "http://myserver/"
        site: "mysite"
        automation_user: "myuser"
        automation_secret: "mysecret"
        site_id: "myremotesite"
        state: "absent"



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
        <div class="ansibleOptionAnchor" id="return-message"></div>

      .. _ansible_collections.checkmk.general.site_module__return-message:

      .. rst-class:: ansible-option-title

      **message**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-message" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The output message that the module generates. Contains the API response details in case of an error.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` always

      .. rst-class:: ansible-option-line
      .. rst-class:: ansible-option-sample

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`"Site connection created."`


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

.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: 2.24.0

.. Anchors

.. _ansible_collections.checkmk.general.notification_module:

.. Anchors: short name for ansible.builtin

.. Title

checkmk.general.notification module -- Manage notification rules in Checkmk.
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `checkmk.general collection <https://galaxy.ansible.com/ui/repo/published/checkmk/general/>`_ (version 7.4.0).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible\-galaxy collection install checkmk.general`.

    To use it in a playbook, specify: :code:`checkmk.general.notification`.

.. version_added

.. rst-class:: ansible-version-added

New in checkmk.general 7.3.0

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Manage notification rules in Checkmk.
- Create, update, and delete notification rules for various notification methods.


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

      .. _ansible_collections.checkmk.general.notification_module__parameter-api_auth_cookie:

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

      .. _ansible_collections.checkmk.general.notification_module__parameter-api_auth_type:

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
        <div class="ansibleOptionAnchor" id="parameter-api_secret"></div>
        <div class="ansibleOptionAnchor" id="parameter-automation_secret"></div>

      .. _ansible_collections.checkmk.general.notification_module__parameter-api_secret:
      .. _ansible_collections.checkmk.general.notification_module__parameter-automation_secret:

      .. rst-class:: ansible-option-title

      **api_secret**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-api_secret" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-aliases:`aliases: automation_secret`

        :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The secret to authenticate your automation user. If not set the module will fall back to the environment variable :literal:`CHECKMK\_VAR\_API\_SECRET`.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-api_user"></div>
        <div class="ansibleOptionAnchor" id="parameter-automation_user"></div>

      .. _ansible_collections.checkmk.general.notification_module__parameter-api_user:
      .. _ansible_collections.checkmk.general.notification_module__parameter-automation_user:

      .. rst-class:: ansible-option-title

      **api_user**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-api_user" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-aliases:`aliases: automation_user`

        :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The automation user you want to use. It has to be an 'Automation' user, not a normal one. If not set the module will fall back to the environment variable :literal:`CHECKMK\_VAR\_API\_USER`.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-client_cert"></div>

      .. _ansible_collections.checkmk.general.notification_module__parameter-client_cert:

      .. rst-class:: ansible-option-title

      **client_cert**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-client_cert" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`path`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Path to the client certificate file for authentication with the web server hosting Checkmk. This is not a Checkmk feature, but one of Ansible and the respective web server.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-client_key"></div>

      .. _ansible_collections.checkmk.general.notification_module__parameter-client_key:

      .. rst-class:: ansible-option-title

      **client_key**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-client_key" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`path`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Path to the client certificate key file for authentication with the web server hosting Checkmk. This is not a Checkmk feature, but one of Ansible and the respective web server.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule_config"></div>

      .. _ansible_collections.checkmk.general.notification_module__parameter-rule_config:

      .. rst-class:: ansible-option-title

      **rule_config**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule_config" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The notification rule configuration.

      Required when :emphasis:`state=present`.

      Only the fields you want to configure need to be specified.

      On creation, the Checkmk API fills in defaults for unspecified fields.

      On update, only the specified fields are compared and updated. Unspecified fields in the existing rule are left unchanged.

      This should match the structure expected by the Checkmk API.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule_config/conditions"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.checkmk.general.notification_module__parameter-rule_config/conditions:

      .. rst-class:: ansible-option-title

      **conditions**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule_config/conditions" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Conditions for when the rule applies.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule_config/conditions/event_console_alerts"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.notification_module__parameter-rule_config/conditions/event_console_alerts:

      .. rst-class:: ansible-option-title

      **event_console_alerts**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule_config/conditions/event_console_alerts" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Event console alerts.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule_config/conditions/match_check_types"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.notification_module__parameter-rule_config/conditions/match_check_types:

      .. rst-class:: ansible-option-title

      **match_check_types**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule_config/conditions/match_check_types" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Match check types.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule_config/conditions/match_contact_groups"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.notification_module__parameter-rule_config/conditions/match_contact_groups:

      .. rst-class:: ansible-option-title

      **match_contact_groups**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule_config/conditions/match_contact_groups" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Match contact groups.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule_config/conditions/match_exclude_hosts"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.notification_module__parameter-rule_config/conditions/match_exclude_hosts:

      .. rst-class:: ansible-option-title

      **match_exclude_hosts**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule_config/conditions/match_exclude_hosts" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Exclude specific hosts.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule_config/conditions/match_exclude_service_groups"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.notification_module__parameter-rule_config/conditions/match_exclude_service_groups:

      .. rst-class:: ansible-option-title

      **match_exclude_service_groups**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule_config/conditions/match_exclude_service_groups" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Exclude service groups.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule_config/conditions/match_exclude_service_groups_regex"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.notification_module__parameter-rule_config/conditions/match_exclude_service_groups_regex:

      .. rst-class:: ansible-option-title

      **match_exclude_service_groups_regex**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule_config/conditions/match_exclude_service_groups_regex" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Exclude service groups by regex.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule_config/conditions/match_exclude_services"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.notification_module__parameter-rule_config/conditions/match_exclude_services:

      .. rst-class:: ansible-option-title

      **match_exclude_services**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule_config/conditions/match_exclude_services" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Exclude specific services.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule_config/conditions/match_folder"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.notification_module__parameter-rule_config/conditions/match_folder:

      .. rst-class:: ansible-option-title

      **match_folder**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule_config/conditions/match_folder" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Match specific folder.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule_config/conditions/match_host_event_type"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.notification_module__parameter-rule_config/conditions/match_host_event_type:

      .. rst-class:: ansible-option-title

      **match_host_event_type**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule_config/conditions/match_host_event_type" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Match host event types.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule_config/conditions/match_host_groups"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.notification_module__parameter-rule_config/conditions/match_host_groups:

      .. rst-class:: ansible-option-title

      **match_host_groups**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule_config/conditions/match_host_groups" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Match host groups.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule_config/conditions/match_host_labels"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.notification_module__parameter-rule_config/conditions/match_host_labels:

      .. rst-class:: ansible-option-title

      **match_host_labels**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule_config/conditions/match_host_labels" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Match host labels.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule_config/conditions/match_host_tags"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.notification_module__parameter-rule_config/conditions/match_host_tags:

      .. rst-class:: ansible-option-title

      **match_host_tags**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule_config/conditions/match_host_tags" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Match host tags.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule_config/conditions/match_hosts"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.notification_module__parameter-rule_config/conditions/match_hosts:

      .. rst-class:: ansible-option-title

      **match_hosts**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule_config/conditions/match_hosts" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Match specific hosts.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule_config/conditions/match_notification_comment"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.notification_module__parameter-rule_config/conditions/match_notification_comment:

      .. rst-class:: ansible-option-title

      **match_notification_comment**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule_config/conditions/match_notification_comment" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Match notification comment.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule_config/conditions/match_only_during_time_period"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.notification_module__parameter-rule_config/conditions/match_only_during_time_period:

      .. rst-class:: ansible-option-title

      **match_only_during_time_period**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule_config/conditions/match_only_during_time_period" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Match only during time period.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule_config/conditions/match_plugin_output"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.notification_module__parameter-rule_config/conditions/match_plugin_output:

      .. rst-class:: ansible-option-title

      **match_plugin_output**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule_config/conditions/match_plugin_output" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Match plugin output.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule_config/conditions/match_service_event_type"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.notification_module__parameter-rule_config/conditions/match_service_event_type:

      .. rst-class:: ansible-option-title

      **match_service_event_type**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule_config/conditions/match_service_event_type" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Match service event types.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule_config/conditions/match_service_groups"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.notification_module__parameter-rule_config/conditions/match_service_groups:

      .. rst-class:: ansible-option-title

      **match_service_groups**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule_config/conditions/match_service_groups" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Match service groups.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule_config/conditions/match_service_groups_regex"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.notification_module__parameter-rule_config/conditions/match_service_groups_regex:

      .. rst-class:: ansible-option-title

      **match_service_groups_regex**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule_config/conditions/match_service_groups_regex" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Match service groups by regex.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule_config/conditions/match_service_labels"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.notification_module__parameter-rule_config/conditions/match_service_labels:

      .. rst-class:: ansible-option-title

      **match_service_labels**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule_config/conditions/match_service_labels" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Match service labels.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule_config/conditions/match_service_levels"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.notification_module__parameter-rule_config/conditions/match_service_levels:

      .. rst-class:: ansible-option-title

      **match_service_levels**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule_config/conditions/match_service_levels" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Match service levels.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule_config/conditions/match_services"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.notification_module__parameter-rule_config/conditions/match_services:

      .. rst-class:: ansible-option-title

      **match_services**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule_config/conditions/match_services" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Match specific services by regex.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule_config/conditions/match_sites"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.notification_module__parameter-rule_config/conditions/match_sites:

      .. rst-class:: ansible-option-title

      **match_sites**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule_config/conditions/match_sites" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Match specific sites.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule_config/conditions/restrict_to_notification_numbers"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.notification_module__parameter-rule_config/conditions/restrict_to_notification_numbers:

      .. rst-class:: ansible-option-title

      **restrict_to_notification_numbers**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule_config/conditions/restrict_to_notification_numbers" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Restrict to notification numbers.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule_config/conditions/throttle_periodic_notifications"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.notification_module__parameter-rule_config/conditions/throttle_periodic_notifications:

      .. rst-class:: ansible-option-title

      **throttle_periodic_notifications**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule_config/conditions/throttle_periodic_notifications" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Throttle periodic notifications.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule_config/contact_selection"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.checkmk.general.notification_module__parameter-rule_config/contact_selection:

      .. rst-class:: ansible-option-title

      **contact_selection**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule_config/contact_selection" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Selection of contacts to notify.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule_config/contact_selection/all_contacts_of_the_notified_object"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.notification_module__parameter-rule_config/contact_selection/all_contacts_of_the_notified_object:

      .. rst-class:: ansible-option-title

      **all_contacts_of_the_notified_object**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule_config/contact_selection/all_contacts_of_the_notified_object" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Notify all contacts of the object.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule_config/contact_selection/all_users"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.notification_module__parameter-rule_config/contact_selection/all_users:

      .. rst-class:: ansible-option-title

      **all_users**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule_config/contact_selection/all_users" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Notify all users.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule_config/contact_selection/all_users_with_an_email_address"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.notification_module__parameter-rule_config/contact_selection/all_users_with_an_email_address:

      .. rst-class:: ansible-option-title

      **all_users_with_an_email_address**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule_config/contact_selection/all_users_with_an_email_address" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Notify all users with an email address.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule_config/contact_selection/explicit_email_addresses"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.notification_module__parameter-rule_config/contact_selection/explicit_email_addresses:

      .. rst-class:: ansible-option-title

      **explicit_email_addresses**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule_config/contact_selection/explicit_email_addresses" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Notify explicit email addresses.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule_config/contact_selection/members_of_contact_groups"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.notification_module__parameter-rule_config/contact_selection/members_of_contact_groups:

      .. rst-class:: ansible-option-title

      **members_of_contact_groups**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule_config/contact_selection/members_of_contact_groups" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Notify members of contact groups.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule_config/contact_selection/restrict_by_contact_groups"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.notification_module__parameter-rule_config/contact_selection/restrict_by_contact_groups:

      .. rst-class:: ansible-option-title

      **restrict_by_contact_groups**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule_config/contact_selection/restrict_by_contact_groups" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Restrict by contact groups.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule_config/contact_selection/restrict_by_custom_macros"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.notification_module__parameter-rule_config/contact_selection/restrict_by_custom_macros:

      .. rst-class:: ansible-option-title

      **restrict_by_custom_macros**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule_config/contact_selection/restrict_by_custom_macros" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Restrict by custom macros.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule_config/contact_selection/the_following_users"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.notification_module__parameter-rule_config/contact_selection/the_following_users:

      .. rst-class:: ansible-option-title

      **the_following_users**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule_config/contact_selection/the_following_users" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Notify specific users.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule_config/notification_method"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.checkmk.general.notification_module__parameter-rule_config/notification_method:

      .. rst-class:: ansible-option-title

      **notification_method**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule_config/notification_method" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The notification method configuration including plugin and bulking settings.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule_config/rule_properties"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.checkmk.general.notification_module__parameter-rule_config/rule_properties:

      .. rst-class:: ansible-option-title

      **rule_properties**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule_config/rule_properties" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Properties of the notification rule.

      The :literal:`description` field is used to identify the rule when :emphasis:`rule\_id` is not provided.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule_id"></div>

      .. _ansible_collections.checkmk.general.notification_module__parameter-rule_id:

      .. rst-class:: ansible-option-title

      **rule_id**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule_id" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The unique identifier of the notification rule.

      If not provided, the module will try to find an existing rule by matching the :literal:`description` field in :literal:`rule\_properties`.

      If multiple rules match the same description, the module will fail and ask for a unique :literal:`rule\_id`.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-server_url"></div>

      .. _ansible_collections.checkmk.general.notification_module__parameter-server_url:

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

      .. _ansible_collections.checkmk.general.notification_module__parameter-site:

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

      .. _ansible_collections.checkmk.general.notification_module__parameter-state:

      .. rst-class:: ansible-option-title

      **state**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-state" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The desired state of the notification rule.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"present"`
      - :ansible-option-choices-entry:`"absent"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-validate_certs"></div>

      .. _ansible_collections.checkmk.general.notification_module__parameter-validate_certs:

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

Notes
-----

.. note::
   - When :emphasis:`rule\_id` is not provided, the module will try to find an existing rule by matching the :emphasis:`description` field in :emphasis:`rule\_properties`. If multiple rules match the same description, the module will fail and ask for a unique :literal:`rule\_id`.
   - Requires Checkmk \>= 2.4.0p22 to enable minimal configuration input. Older version will need all options set, not only relevant ones.
   - When a key is not explicitly provided, it will not be managed. That means if you set a certain key at some point and later remove it from your Ansible configuration, it will not be removed in the rule.

.. Seealso

See Also
--------

.. seealso::

   :ref:`checkmk.general.contact\_group <ansible_collections.checkmk.general.contact_group_module>`
       Manage contact groups in Checkmk.
   :ref:`checkmk.general.timeperiod <ansible_collections.checkmk.general.timeperiod_module>`
       Manage time periods in Checkmk.
   :ref:`checkmk.general.user <ansible_collections.checkmk.general.user_module>`
       Manage users in Checkmk.

.. Examples

Examples
--------

.. code-block:: yaml+jinja

    # ---
    # Create

    - name: "Create an email notification rule"
      checkmk.general.notification:
        server_url: "https://myserver/"
        site: "mysite"
        api_user: "myuser"
        api_secret: "mysecret"
        rule_config:
          rule_properties:
            description: "Notify all contacts on critical issues"
            comment: "Managed by Ansible"
          notification_method:
            notify_plugin:
              option: "create_notification_with_the_following_parameters"
              plugin_params:
                plugin_name: "mail"
          contact_selection:
            all_contacts_of_the_notified_object:
              state: "enabled"
        state: "present"
      register: notification_result

    - name: "Show the ID of the new notification rule"
      ansible.builtin.debug:
        msg: "Rule ID: {{ notification_result.content.id }}"

    - name: "Create a Slack notification rule"
      checkmk.general.notification:
        server_url: "https://myserver/"
        site: "mysite"
        api_user: "myuser"
        api_secret: "mysecret"
        rule_config:
          rule_properties:
            description: "Slack notifications for critical alerts"
            comment: "Managed by Ansible"
          notification_method:
            notify_plugin:
              option: "create_notification_with_the_following_parameters"
              plugin_params:
                plugin_name: "slack"
                webhook_url:
                  option: "explicit"
                  url: "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
          contact_selection:
            all_contacts_of_the_notified_object:
              state: "enabled"
        state: "present"

    - name: "Create a Microsoft Teams notification rule"
      checkmk.general.notification:
        server_url: "https://myserver/"
        site: "mysite"
        api_user: "myuser"
        api_secret: "mysecret"
        rule_config:
          rule_properties:
            description: "Microsoft Teams notifications for critical alerts"
            comment: "Managed by Ansible"
          notification_method:
            notify_plugin:
              option: "create_notification_with_the_following_parameters"
              plugin_params:
                plugin_name: "msteams"
                webhook_url:
                  option: "explicit"
                  url: "https://outlook.office.com/webhook/YOUR/WEBHOOK/URL"
          contact_selection:
            all_contacts_of_the_notified_object:
              state: "enabled"
        state: "present"

    # ---
    # Update

    # Note: Only keys explicitly provided are compared and updated.
    #       Keys absent from rule_config will not be modified in the existing rule.
    - name: "Update a notification rule"
      checkmk.general.notification:
        server_url: "https://myserver/"
        site: "mysite"
        api_user: "myuser"
        api_secret: "mysecret"
        rule_id: "e83e6ed6-a4cc-47ed-900b-65d7ae1dbb3d"
        rule_config:
          rule_properties:
            description: "Notify all contacts on critical issues"
          notification_method:
            notify_plugin:
              option: "create_notification_with_the_following_parameters"
              plugin_params:
                plugin_name: "mail"
        state: "present"

    # ---
    # Delete

    - name: "Delete a notification rule by rule_id"
      checkmk.general.notification:
        server_url: "https://myserver/"
        site: "mysite"
        api_user: "myuser"
        api_secret: "mysecret"
        rule_id: "e83e6ed6-a4cc-47ed-900b-65d7ae1dbb3d"
        state: "absent"

    # Note: If multiple rules share the same description, deletion by description will fail.
    #       Use rule_id for unambiguous deletion.
    - name: "Delete a notification rule by description"
      checkmk.general.notification:
        server_url: "https://myserver/"
        site: "mysite"
        api_user: "myuser"
        api_secret: "mysecret"
        rule_config:
          rule_properties:
            description: "Notify all contacts on critical issues"
        state: "absent"

    # ---------------------------------------------------------------------------
    # Using environment variables for authentication
    # ---------------------------------------------------------------------------
    # Connection parameters can be provided via environment variables instead of
    # task parameters. The supported variables are:
    #   CHECKMK_VAR_SERVER_URL, CHECKMK_VAR_SITE,
    #   CHECKMK_VAR_API_USER, CHECKMK_VAR_API_SECRET,
    #   CHECKMK_VAR_VALIDATE_CERTS

    - name: "Create a notification rule using environment variables for authentication."
      checkmk.general.notification:
        rule_config:
          rule_properties:
            description: "Notify all contacts on critical issues"
            comment: "Managed by Ansible"
          notification_method:
            notify_plugin:
              option: "create_notification_with_the_following_parameters"
              plugin_params:
                plugin_name: "mail"
          contact_selection:
            all_contacts_of_the_notified_object:
              state: "enabled"
        state: "present"
      environment:
        CHECKMK_VAR_SERVER_URL: "https://myserver/"
        CHECKMK_VAR_SITE: "mysite"
        CHECKMK_VAR_API_USER: "myuser"
        CHECKMK_VAR_API_SECRET: "mysecret"



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

      .. _ansible_collections.checkmk.general.notification_module__return-content:

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

      The complete notification rule object.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` when rule is created or updated


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-content/extensions"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.checkmk.general.notification_module__return-content/extensions:

      .. rst-class:: ansible-option-title

      **extensions**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-content/extensions" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The rule configuration details.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` when rule is created or updated


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-content/id"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.checkmk.general.notification_module__return-content/id:

      .. rst-class:: ansible-option-title

      **id**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-content/id" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The ID of the notification rule.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` when rule is created or updated

      .. rst-class:: ansible-option-line
      .. rst-class:: ansible-option-sample

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`"e83e6ed6\-a4cc\-47ed\-900b\-65d7ae1dbb3d"`


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-content/title"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.checkmk.general.notification_module__return-content/title:

      .. rst-class:: ansible-option-title

      **title**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-content/title" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The title/description of the rule.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` when rule is created or updated


      .. raw:: html

        </div>



  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-msg"></div>

      .. _ansible_collections.checkmk.general.notification_module__return-msg:

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

      .. rst-class:: ansible-option-line
      .. rst-class:: ansible-option-sample

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`"Notification rule created."`


      .. raw:: html

        </div>



..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- Nicolas Brainez (@nicoske)


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

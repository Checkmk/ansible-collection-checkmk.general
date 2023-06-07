
.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. role:: ansible-attribute-support-label
.. role:: ansible-attribute-support-property
.. role:: ansible-attribute-support-full
.. role:: ansible-attribute-support-partial
.. role:: ansible-attribute-support-none
.. role:: ansible-attribute-support-na
.. role:: ansible-option-type
.. role:: ansible-option-elements
.. role:: ansible-option-required
.. role:: ansible-option-versionadded
.. role:: ansible-option-aliases
.. role:: ansible-option-choices
.. role:: ansible-option-choices-default-mark
.. role:: ansible-option-default-bold
.. role:: ansible-option-configuration
.. role:: ansible-option-returned-bold
.. role:: ansible-option-sample-bold

.. Anchors

.. _ansible_collections.tribe29.checkmk.user_module:

.. Anchors: short name for ansible.builtin

.. Anchors: aliases



.. Title

tribe29.checkmk.user module -- Manage users in Checkmk.
+++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `tribe29.checkmk collection <https://galaxy.ansible.com/tribe29/checkmk>`_ (version 0.23.0).

    To install it, use: :code:`ansible-galaxy collection install tribe29.checkmk`.

    To use it in a playbook, specify: :code:`tribe29.checkmk.user`.

.. version_added

.. rst-class:: ansible-version-added

New in tribe29.checkmk 0.18.0

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Create and delete users within Checkmk.


.. Aliases


.. Requirements






.. Options

Parameters
----------

.. rst-class:: ansible-option-table

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1

  * - Parameter
    - Comments

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-auth_type"></div>

      .. _ansible_collections.tribe29.checkmk.user_module__parameter-auth_type:

      .. rst-class:: ansible-option-title

      **auth_type**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-auth_type" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The authentication type.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"password"`
      - :ansible-option-choices-entry:`"automation"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-authorized_sites"></div>

      .. _ansible_collections.tribe29.checkmk.user_module__parameter-authorized_sites:

      .. rst-class:: ansible-option-title

      **authorized_sites**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-authorized_sites" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`any`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The names of the sites the user is authorized to handle.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-automation_secret"></div>

      .. _ansible_collections.tribe29.checkmk.user_module__parameter-automation_secret:

      .. rst-class:: ansible-option-title

      **automation_secret**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-automation_secret" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

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

      .. _ansible_collections.tribe29.checkmk.user_module__parameter-automation_user:

      .. rst-class:: ansible-option-title

      **automation_user**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-automation_user" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

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
        <div class="ansibleOptionAnchor" id="parameter-contactgroups"></div>

      .. _ansible_collections.tribe29.checkmk.user_module__parameter-contactgroups:

      .. rst-class:: ansible-option-title

      **contactgroups**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-contactgroups" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`any`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Assign the user to one or multiple contact groups. If no contact group is specified then no monitoring contact will be created.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-disable_login"></div>

      .. _ansible_collections.tribe29.checkmk.user_module__parameter-disable_login:

      .. rst-class:: ansible-option-title

      **disable_login**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-disable_login" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The user can be blocked from login but will remain part of the site. The disabling does not affect notification and alerts.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-disable_notifications"></div>

      .. _ansible_collections.tribe29.checkmk.user_module__parameter-disable_notifications:

      .. rst-class:: ansible-option-title

      **disable_notifications**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-disable_notifications" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`any`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Option if all notifications should be temporarily disabled.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-email"></div>

      .. _ansible_collections.tribe29.checkmk.user_module__parameter-email:

      .. rst-class:: ansible-option-title

      **email**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-email" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The mail address of the user. Required if the user is a monitoring contact and receives notifications via mail.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-enforce_password_change"></div>

      .. _ansible_collections.tribe29.checkmk.user_module__parameter-enforce_password_change:

      .. rst-class:: ansible-option-title

      **enforce_password_change**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-enforce_password_change" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      If set to true, the user will be forced to change his/her password at the next login.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-fallback_contact"></div>

      .. _ansible_collections.tribe29.checkmk.user_module__parameter-fallback_contact:

      .. rst-class:: ansible-option-title

      **fallback_contact**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-fallback_contact" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      In case none of your notification rules handles a certain event a notification will be sent to the specified email.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-fullname"></div>

      .. _ansible_collections.tribe29.checkmk.user_module__parameter-fullname:

      .. rst-class:: ansible-option-title

      **fullname**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-fullname" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The alias or full name of the user.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-idle_timeout_duration"></div>

      .. _ansible_collections.tribe29.checkmk.user_module__parameter-idle_timeout_duration:

      .. rst-class:: ansible-option-title

      **idle_timeout_duration**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-idle_timeout_duration" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The duration in seconds of the individual idle timeout if individual is selected as idle timeout option.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-idle_timeout_option"></div>

      .. _ansible_collections.tribe29.checkmk.user_module__parameter-idle_timeout_option:

      .. rst-class:: ansible-option-title

      **idle_timeout_option**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-idle_timeout_option" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Specify if the idle timeout should use the global configuration, be disabled or use an individual duration


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"global"`
      - :ansible-option-choices-entry:`"disable"`
      - :ansible-option-choices-entry:`"individual"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-language"></div>

      .. _ansible_collections.tribe29.checkmk.user_module__parameter-language:

      .. rst-class:: ansible-option-title

      **language**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-language" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Configure the language to be used by the user in the user interface. Omitting this will configure the default language.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"default"`
      - :ansible-option-choices-entry:`"en"`
      - :ansible-option-choices-entry:`"de"`
      - :ansible-option-choices-entry:`"ro"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-name"></div>

      .. _ansible_collections.tribe29.checkmk.user_module__parameter-name:

      .. rst-class:: ansible-option-title

      **name**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-name" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The user you want to manage.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-pager_address"></div>

      .. _ansible_collections.tribe29.checkmk.user_module__parameter-pager_address:

      .. rst-class:: ansible-option-title

      **pager_address**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-pager_address" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The pager address.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-password"></div>

      .. _ansible_collections.tribe29.checkmk.user_module__parameter-password:

      .. rst-class:: ansible-option-title

      **password**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-password" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The password or secret for login.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-roles"></div>

      .. _ansible_collections.tribe29.checkmk.user_module__parameter-roles:

      .. rst-class:: ansible-option-title

      **roles**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-roles" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`any`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The list of assigned roles to the user.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-server_url"></div>

      .. _ansible_collections.tribe29.checkmk.user_module__parameter-server_url:

      .. rst-class:: ansible-option-title

      **server_url**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-server_url" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The base url of your Checkmk server.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site"></div>

      .. _ansible_collections.tribe29.checkmk.user_module__parameter-site:

      .. rst-class:: ansible-option-title

      **site**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

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
        <div class="ansibleOptionAnchor" id="parameter-state"></div>

      .. _ansible_collections.tribe29.checkmk.user_module__parameter-state:

      .. rst-class:: ansible-option-title

      **state**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-state" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Desired state


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`"present"` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`"absent"`
      - :ansible-option-choices-entry:`"reset\_password"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-validate_certs"></div>

      .. _ansible_collections.tribe29.checkmk.user_module__parameter-validate_certs:

      .. rst-class:: ansible-option-title

      **validate_certs**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-validate_certs" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

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

    
    # Create a user.
    - name: "Create a user."
      tribe29.checkmk.user:
        server_url: "http://localhost/"
        site: "local"
        automation_user: "automation"
        automation_secret: "$SECRET"
        name: "krichards"
        fullname: "Keith Richards"
        email: "keith.richards@rollingstones.com"
        password: "Open-G"
        contactgroups:
            - "rolling_stones"
            - "glimmer_twins"
            - "x-pensive_winos"
            - "potc_cast"
        state: "present"

    # Create an automation user.
    - name: "Create an automation user."
      tribe29.checkmk.user:
        server_url: "http://localhost/"
        site: "local"
        automation_user: "automation"
        automation_secret: "$SECRET"
        name: "registration"
        fullname: "Registration User"
        auth_type: "automation"
        password: "ZGSDHUVDSKJHSDF"
        roles:
            - "registration"
        state: "present"

    # Create a detailed user.
    - name: "Create a detailed user."
      tribe29.checkmk.user:
        server_url: "http://localhost/"
        site: "local"
        automation_user: "automation"
        automation_secret: "$SECRET"
        name: "horst"
        fullname: "Horst Schlämmer"
        auth_type: "password"
        password: "uschi"
        enforce_password_change: True
        email: "checker@grevenbroich.de"
        fallback_contact: True
        pager_address: 089-123456789
        contactgroups:
          - "sport"
          - "vereinsgeschehen"
          - "lokalpolitik"
        disable_notifications: '{"disable": true, "timerange": { "start_time": "2023-02-23T15:06:48+00:00", "end_time": "2023-02-23T16:06:48+00:00"}}'
        language: "de"
        roles:
          - "user"
        authorized_sites:
          - "{{ site }}"
        state: "present"




.. Facts


.. Return values

Return Values
-------------
Common return values are documented :ref:`here <common_return_values>`, the following are the fields unique to this module:

.. rst-class:: ansible-option-table

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1

  * - Key
    - Description

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-message"></div>

      .. _ansible_collections.tribe29.checkmk.user_module__return-message:

      .. rst-class:: ansible-option-title

      **message**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-message" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

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

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`"User created."`


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

.. raw:: html

  <p class="ansible-links">
    <a href="https://github.com/Checkmk/ansible-collection-tribe29.checkmk/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc" aria-role="button" target="_blank" rel="noopener external">Issue Tracker</a>
    <a href="https://github.com/Checkmk/ansible-collection-tribe29.checkmk" aria-role="button" target="_blank" rel="noopener external">Repository (Sources)</a>
  </p>

.. Parsing errors


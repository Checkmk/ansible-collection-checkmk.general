
.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: 2.11.0

.. Anchors

.. _ansible_collections.checkmk.general.user_module:

.. Anchors: short name for ansible.builtin

.. Title

checkmk.general.user module -- Manage users in Checkmk.
+++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `checkmk.general collection <https://galaxy.ansible.com/ui/repo/published/checkmk/general/>`_ (version 5.0.0).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible-galaxy collection install checkmk.general`.

    To use it in a playbook, specify: :code:`checkmk.general.user`.

.. version_added

.. rst-class:: ansible-version-added

New in checkmk.general 0.18.0

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Manage users in Checkmk.


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
        <div class="ansibleOptionAnchor" id="parameter-auth_type"></div>

      .. _ansible_collections.checkmk.general.user_module__parameter-auth_type:

      .. rst-class:: ansible-option-title

      **auth_type**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-auth_type" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The authentication type. Setting this to \ :literal:`password`\  will create a normal user, \ :literal:`automation`\  will create an automation user.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"password"`
      - :ansible-option-choices-entry:`"automation"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-authorized_sites"></div>

      .. _ansible_collections.checkmk.general.user_module__parameter-authorized_sites:

      .. rst-class:: ansible-option-title

      **authorized_sites**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-authorized_sites" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`any`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The names of the sites the user is authorized to access.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-automation_secret"></div>

      .. _ansible_collections.checkmk.general.user_module__parameter-automation_secret:

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

      .. _ansible_collections.checkmk.general.user_module__parameter-automation_user:

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
        <div class="ansibleOptionAnchor" id="parameter-contactgroups"></div>

      .. _ansible_collections.checkmk.general.user_module__parameter-contactgroups:

      .. rst-class:: ansible-option-title

      **contactgroups**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-contactgroups" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`any`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      A list of contact groups assigned to the user.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-customer"></div>

      .. _ansible_collections.checkmk.general.user_module__parameter-customer:

      .. rst-class:: ansible-option-title

      **customer**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-customer" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      For the Checkmk Managed Edition (CME), you need to specify which customer ID this object belongs to.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-disable_login"></div>

      .. _ansible_collections.checkmk.general.user_module__parameter-disable_login:

      .. rst-class:: ansible-option-title

      **disable_login**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-disable_login" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      If set to \ :literal:`true`\ , the user cannot log in anymore, but will remain part of the site. Disabling a user does not affect notifications.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-disable_notifications"></div>

      .. _ansible_collections.checkmk.general.user_module__parameter-disable_notifications:

      .. rst-class:: ansible-option-title

      **disable_notifications**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-disable_notifications" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Temporarily disable \ :strong:`all`\  notifications for this user.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-disable_notifications_timerange"></div>

      .. _ansible_collections.checkmk.general.user_module__parameter-disable_notifications_timerange:

      .. rst-class:: ansible-option-title

      **disable_notifications_timerange**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-disable_notifications_timerange" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The duration, for how log notifications should be disabled, if \ :literal:`disable\_notifications`\  is set to \ :literal:`true`\ .


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-email"></div>

      .. _ansible_collections.checkmk.general.user_module__parameter-email:

      .. rst-class:: ansible-option-title

      **email**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-email" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The mail address of the user. Required if the user is a monitoring contact and should receive notifications via mail.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-enforce_password_change"></div>

      .. _ansible_collections.checkmk.general.user_module__parameter-enforce_password_change:

      .. rst-class:: ansible-option-title

      **enforce_password_change**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-enforce_password_change" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      If set to \ :literal:`true`\ , the user will be forced to change their password on the next login.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-fallback_contact"></div>

      .. _ansible_collections.checkmk.general.user_module__parameter-fallback_contact:

      .. rst-class:: ansible-option-title

      **fallback_contact**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-fallback_contact" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      This user will receive fallback notifications. This means, if no notification rules match a certain event, they are sent to the fallback contacts.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-fullname"></div>

      .. _ansible_collections.checkmk.general.user_module__parameter-fullname:

      .. rst-class:: ansible-option-title

      **fullname**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-fullname" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      A alias or the full name of the user.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-idle_timeout_duration"></div>

      .. _ansible_collections.checkmk.general.user_module__parameter-idle_timeout_duration:

      .. rst-class:: ansible-option-title

      **idle_timeout_duration**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-idle_timeout_duration" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`integer`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The duration in seconds, if \ :literal:`idle\_timeout\_option`\  is set to \ :literal:`individual`\ .


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-idle_timeout_option"></div>

      .. _ansible_collections.checkmk.general.user_module__parameter-idle_timeout_option:

      .. rst-class:: ansible-option-title

      **idle_timeout_option**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-idle_timeout_option" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Specify, whether the idle timeout should use the global configuration, use an individual duration or be disabled entirely.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"global"`
      - :ansible-option-choices-entry:`"disable"`
      - :ansible-option-choices-entry:`"individual"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-interface_theme"></div>

      .. _ansible_collections.checkmk.general.user_module__parameter-interface_theme:

      .. rst-class:: ansible-option-title

      **interface_theme**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-interface_theme" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The theme of the user interface.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"default"`
      - :ansible-option-choices-entry:`"dark"`
      - :ansible-option-choices-entry:`"light"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-language"></div>

      .. _ansible_collections.checkmk.general.user_module__parameter-language:

      .. rst-class:: ansible-option-title

      **language**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-language" title="Permalink to this option"></a>

      .. ansible-option-type-line::

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


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-mega_menu_icons"></div>

      .. _ansible_collections.checkmk.general.user_module__parameter-mega_menu_icons:

      .. rst-class:: ansible-option-title

      **mega_menu_icons**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-mega_menu_icons" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      This option decides if colored icons should be shown for every entry in the mega menus or only for the headlines (the 'topics').


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"topic"`
      - :ansible-option-choices-entry:`"entry"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-name"></div>

      .. _ansible_collections.checkmk.general.user_module__parameter-name:

      .. rst-class:: ansible-option-title

      **name**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-name" title="Permalink to this option"></a>

      .. ansible-option-type-line::

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
        <div class="ansibleOptionAnchor" id="parameter-navigation_bar_icons"></div>

      .. _ansible_collections.checkmk.general.user_module__parameter-navigation_bar_icons:

      .. rst-class:: ansible-option-title

      **navigation_bar_icons**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-navigation_bar_icons" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      This option decides if icons in the navigation bar should show/hide the respective titles.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"hide"`
      - :ansible-option-choices-entry:`"show"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-pager"></div>
        <div class="ansibleOptionAnchor" id="parameter-pager_address"></div>

      .. _ansible_collections.checkmk.general.user_module__parameter-pager:
      .. _ansible_collections.checkmk.general.user_module__parameter-pager_address:

      .. rst-class:: ansible-option-title

      **pager**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-pager" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-aliases:`aliases: pager_address`

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      A (mobile) phone number, used to receive e.g., SMS.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-password"></div>

      .. _ansible_collections.checkmk.general.user_module__parameter-password:

      .. rst-class:: ansible-option-title

      **password**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-password" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The password or secret for login. Depending on the \ :literal:`auth\_type`\ , this is interpreted as a password or secret.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-roles"></div>

      .. _ansible_collections.checkmk.general.user_module__parameter-roles:

      .. rst-class:: ansible-option-title

      **roles**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-roles" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`any`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      A list of roles assigned to the user.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-server_url"></div>

      .. _ansible_collections.checkmk.general.user_module__parameter-server_url:

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
        <div class="ansibleOptionAnchor" id="parameter-show_mode"></div>

      .. _ansible_collections.checkmk.general.user_module__parameter-show_mode:

      .. rst-class:: ansible-option-title

      **show_mode**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-show_mode" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      This option decides what show mode should be used for unvisited menus. Alternatively, this option can also be used to enforce show more removing the three dots for all menus.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"default"`
      - :ansible-option-choices-entry:`"default\_show\_less"`
      - :ansible-option-choices-entry:`"default\_show\_more"`
      - :ansible-option-choices-entry:`"enforce\_show\_more"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-sidebar_position"></div>

      .. _ansible_collections.checkmk.general.user_module__parameter-sidebar_position:

      .. rst-class:: ansible-option-title

      **sidebar_position**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-sidebar_position" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The position of the sidebar.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"left"`
      - :ansible-option-choices-entry:`"right"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site"></div>

      .. _ansible_collections.checkmk.general.user_module__parameter-site:

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
        <div class="ansibleOptionAnchor" id="parameter-state"></div>

      .. _ansible_collections.checkmk.general.user_module__parameter-state:

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

      The desired state.


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

      .. _ansible_collections.checkmk.general.user_module__parameter-validate_certs:

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

    
    # Create a user.
    - name: "Create a user."
      checkmk.general.user:
        server_url: "http://myserver/"
        site: "local"
        automation_user: "myuser"
        automation_secret: "mysecret"
        name: "krichards"
        fullname: "Keith Richards"
        email: "keith.richards@rollingstones.com"
        password: "Open-G"
        contactgroups:
          - "rolling_stones"
          - "glimmer_twins"
          - "x-pensive_winos"
          - "potc_cast"

    # Create an automation user.
    - name: "Create an automation user."
      checkmk.general.user:
        server_url: "http://myserver/"
        site: "local"
        automation_user: "myuser"
        automation_secret: "mysecret"
        name: "registration"
        fullname: "Registration User"
        auth_type: "automation"
        password: "ZGSDHUVDSKJHSDF"
        roles:
          - "registration"
        state: "present"

    # Create a user with the Checkmk Managed Edition (CME), using the `customer` parameter.
    - name: "Create a user."
      checkmk.general.user:
        server_url: "http://myserver/"
        site: "local"
        automation_user: "myuser"
        automation_secret: "mysecret"
        name: "krichards"
        fullname: "Keith Richards"
        email: "keith.richards@rollingstones.com"
        customer: "provider"
        password: "Open-G"
        contactgroups:
          - "rolling_stones"
          - "glimmer_twins"
          - "x-pensive_winos"
          - "potc_cast"

    # Create a detailed user.
    - name: "Create a more complex user."
      checkmk.general.user:
        server_url: "http://myserver/"
        site: "local"
        automation_user: "myuser"
        automation_secret: "mysecret"
        name: "horst"
        fullname: "Horst Schlämmer"
        customer: "provider"
        auth_type: "password"
        password: "uschi"
        enforce_password_change: true
        email: "checker@grevenbroich.de"
        fallback_contact: True
        pager: 089-123456789
        contactgroups:
          - "sport"
          - "vereinsgeschehen"
          - "lokalpolitik"
        disable_notifications: True
        disable_notifications_timerange: { "start_time": "2023-02-23T15:06:48+00:00", "end_time": "2023-02-23T16:06:48+00:00"}
        language: "de"
        roles:
          - "user"
        authorized_sites:
          - "{{ mysite }}"
        interface_theme: "dark"
        sidebar_position: "right"
        navigation_bar_icons: "show"
        mega_menu_icons: "entry"
        show_mode: "default_show_more"
        state: "present"




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

      .. _ansible_collections.checkmk.general.user_module__return-message:

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

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`"User created."`


      .. raw:: html

        </div>



..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- Lars Getwan (@lgetwan)
- Marcel Arentz (@godspeed-you)
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


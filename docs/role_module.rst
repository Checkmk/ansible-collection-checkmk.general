.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: 2.24.0

.. Anchors

.. _ansible_collections.checkmk.general.role_module:

.. Anchors: short name for ansible.builtin

.. Title

checkmk.general.role module -- Manage roles in Checkmk
++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `checkmk.general collection <https://galaxy.ansible.com/ui/repo/published/checkmk/general/>`_ (version 8.2.0).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible\-galaxy collection install checkmk.general`.

    To use it in a playbook, specify: :code:`checkmk.general.role`.

.. version_added

.. rst-class:: ansible-version-added

New in checkmk.general 7.7.0

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Manage roles within Checkmk. Custom roles are created by cloning an existing built\-in role.


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

      .. _ansible_collections.checkmk.general.role_module__parameter-api_auth_cookie:

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

      .. _ansible_collections.checkmk.general.role_module__parameter-api_auth_type:

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

      .. _ansible_collections.checkmk.general.role_module__parameter-api_secret:
      .. _ansible_collections.checkmk.general.role_module__parameter-automation_secret:

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

      The secret to authenticate your automation user. If not set the module will fall back to the environment variable :literal:`CHECKMK\_VAR\_API\_SECRET`.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-api_user"></div>
        <div class="ansibleOptionAnchor" id="parameter-automation_user"></div>

      .. _ansible_collections.checkmk.general.role_module__parameter-api_user:
      .. _ansible_collections.checkmk.general.role_module__parameter-automation_user:

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

      The automation user you want to use. It has to be an 'Automation' user, not a normal one. If not set the module will fall back to the environment variable :literal:`CHECKMK\_VAR\_API\_USER`.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-based_on"></div>

      .. _ansible_collections.checkmk.general.role_module__parameter-based_on:

      .. rst-class:: ansible-option-title

      **based_on**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-based_on" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The ID of the built\-in role to clone from when creating a new custom role.

      This parameter is ignored when updating an existing role.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"admin"`
      - :ansible-option-choices-entry:`"user"`
      - :ansible-option-choices-entry:`"guest"`
      - :ansible-option-choices-entry:`"agent\_registration"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-client_cert"></div>

      .. _ansible_collections.checkmk.general.role_module__parameter-client_cert:

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

      .. _ansible_collections.checkmk.general.role_module__parameter-client_key:

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
        <div class="ansibleOptionAnchor" id="parameter-name"></div>

      .. _ansible_collections.checkmk.general.role_module__parameter-name:

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

      The internal ID of the role. This is used to uniquely identify the role. It cannot be changed after creation.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-permissions"></div>

      .. _ansible_collections.checkmk.general.role_module__parameter-permissions:

      .. rst-class:: ansible-option-title

      **permissions**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-permissions" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      A dictionary of permissions to set on the role.

      Keys are permission IDs (e.g., :literal:`general.use`\ , :literal:`wato.edit`\ , :literal:`wato.all\_folders`\ ).

      Values must be one of :literal:`yes`\ , :literal:`no`\ , or :literal:`default`. Values must be quoted strings in YAML; unquoted :literal:`yes` and :literal:`no` are interpreted as booleans and will be rejected.

      The value :literal:`default` reverts a permission to the base role's setting. It is only valid for custom roles. For built\-in roles (\ :literal:`admin`\ , :literal:`user`\ , :literal:`guest`\ , :literal:`agent\_registration`\ ) use :literal:`yes` or :literal:`no` explicitly.

      Permissions not listed here will remain unchanged.

      You can find the internal permission IDs in the Checkmk GUI under :emphasis:`Setup \> Users \> Roles & permissions` using the inline help (available from Checkmk 2.4.0 onwards via Werk


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-server_url"></div>

      .. _ansible_collections.checkmk.general.role_module__parameter-server_url:

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

      .. _ansible_collections.checkmk.general.role_module__parameter-site:

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

      .. _ansible_collections.checkmk.general.role_module__parameter-state:

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

      The desired state of the role.

      :literal:`present` ensures the role exists with the specified configuration. If the role does not exist, it will be created by cloning the role specified in :literal:`based\_on`.

      :literal:`absent` ensures the custom role does not exist. Built\-in roles cannot be deleted.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`"present"` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`"absent"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-title"></div>
        <div class="ansibleOptionAnchor" id="parameter-alias"></div>

      .. _ansible_collections.checkmk.general.role_module__parameter-alias:
      .. _ansible_collections.checkmk.general.role_module__parameter-title:

      .. rst-class:: ansible-option-title

      **title**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-title" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-aliases:`aliases: alias`

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The human\-readable title (alias) of the role.

      Optional when creating a new custom role. If omitted, the title of the source role is used.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-validate_certs"></div>

      .. _ansible_collections.checkmk.general.role_module__parameter-validate_certs:

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
   - Built\-in roles cannot be created or deleted, but their permissions can be updated.
   - Creating a role with :emphasis:`permissions` requires two API calls. The role is first cloned from :emphasis:`based\_on`\ , then the permissions are applied in a second call. If the second call fails (e.g., due to an invalid permission ID), the role still exists on the server with the permissions inherited from the base role. The module then fails with :literal:`changed=true` and a message describing this state. To recover, resolve the error and re\-run the task, which updates the permissions of the now existing role. Alternatively, remove the role with :literal:`state=absent`.

.. Seealso

See Also
--------

.. seealso::

   :ref:`checkmk.general.user <ansible_collections.checkmk.general.user_module>`
       Manage users in Checkmk.
   :ref:`checkmk.general.contact\_group <ansible_collections.checkmk.general.contact_group_module>`
       Manage contact groups in Checkmk.
   `Checkmk documentation on roles <https://docs.checkmk.com/latest/en/wato_user.html>`_
       Complete documentation for user roles and permissions.

.. Examples

Examples
--------

.. code-block:: yaml+jinja

    # ---------------------------------------------------------------------------
    # Create and delete roles
    # ---------------------------------------------------------------------------

    - name: "Create a custom monitoring role."
      checkmk.general.role:
        server_url: "https://myserver/"
        site: "mysite"
        api_user: "myuser"
        api_secret: "mysecret"
        name: "limited_user"
        title: "Limited Monitoring User"
        based_on: "user"
        state: "present"

    - name: "Create a custom role with tailored permissions."
      checkmk.general.role:
        server_url: "https://myserver/"
        site: "mysite"
        api_user: "myuser"
        api_secret: "mysecret"
        name: "host_manager"
        title: "Host Manager"
        based_on: "user"
        permissions:
          wato.all_folders: "yes"
          wato.edit: "yes"
          wato.manage_hosts: "yes"
          general.edit_notifications: "no"
        state: "present"

    - name: "Delete a custom role."
      checkmk.general.role:
        server_url: "https://myserver/"
        site: "mysite"
        api_user: "myuser"
        api_secret: "mysecret"
        name: "limited_user"
        state: "absent"

    # ---------------------------------------------------------------------------
    # Update permissions on existing roles
    # ---------------------------------------------------------------------------

    - name: "Update permissions on an existing custom role."
      checkmk.general.role:
        server_url: "https://myserver/"
        site: "mysite"
        api_user: "myuser"
        api_secret: "mysecret"
        name: "host_manager"
        permissions:
          wato.all_folders: "yes"
        state: "present"

    - name: "Modify permissions on the built-in user role."
      checkmk.general.role:
        server_url: "https://myserver/"
        site: "mysite"
        api_user: "myuser"
        api_secret: "mysecret"
        name: "user"
        permissions:
          general.edit_notifications: "no"
        state: "present"

    # ---------------------------------------------------------------------------
    # Using environment variables for authentication
    # ---------------------------------------------------------------------------
    # Connection parameters can be provided via environment variables instead of
    # task parameters. The supported variables are:
    #   CHECKMK_VAR_SERVER_URL, CHECKMK_VAR_SITE,
    #   CHECKMK_VAR_API_USER, CHECKMK_VAR_API_SECRET,
    #   CHECKMK_VAR_VALIDATE_CERTS

    - name: "Create a custom role using environment variables for authentication."
      checkmk.general.role:
        name: "limited_user"
        title: "Limited Monitoring User"
        based_on: "user"
        state: "present"
      environment:
        CHECKMK_VAR_SERVER_URL: "https://myserver/"
        CHECKMK_VAR_SITE: "mysite"
        CHECKMK_VAR_API_USER: "myuser"
        CHECKMK_VAR_API_SECRET: "mysecret"
        CHECKMK_VAR_VALIDATE_CERTS: "true"



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
        <div class="ansibleOptionAnchor" id="return-http_code"></div>

      .. _ansible_collections.checkmk.general.role_module__return-http_code:

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

      The HTTP code the Checkmk API returns.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` always

      .. rst-class:: ansible-option-line
      .. rst-class:: ansible-option-sample

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`200`


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-msg"></div>

      .. _ansible_collections.checkmk.general.role_module__return-msg:

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

      The output message that the module generates. Contains the API response details in case of an error.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` always

      .. rst-class:: ansible-option-line
      .. rst-class:: ansible-option-sample

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`"Role created."`


      .. raw:: html

        </div>



..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- Robin Gierse (@robin-checkmk)


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

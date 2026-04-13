.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: 2.24.0

.. Anchors

.. _ansible_collections.checkmk.general.downtime_module:

.. Anchors: short name for ansible.builtin

.. Title

checkmk.general.downtime module -- Manage downtimes in Checkmk
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `checkmk.general collection <https://galaxy.ansible.com/ui/repo/published/checkmk/general/>`_ (version 7.3.1).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible\-galaxy collection install checkmk.general`.

    To use it in a playbook, specify: :code:`checkmk.general.downtime`.

.. version_added

.. rst-class:: ansible-version-added

New in checkmk.general 0.2.0

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Manage downtimes within Checkmk.


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

      .. _ansible_collections.checkmk.general.downtime_module__parameter-api_auth_cookie:

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

      .. _ansible_collections.checkmk.general.downtime_module__parameter-api_auth_type:

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

      .. _ansible_collections.checkmk.general.downtime_module__parameter-api_secret:
      .. _ansible_collections.checkmk.general.downtime_module__parameter-automation_secret:

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

      .. _ansible_collections.checkmk.general.downtime_module__parameter-api_user:
      .. _ansible_collections.checkmk.general.downtime_module__parameter-automation_user:

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

      .. _ansible_collections.checkmk.general.downtime_module__parameter-client_cert:

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

      .. _ansible_collections.checkmk.general.downtime_module__parameter-client_key:

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
        <div class="ansibleOptionAnchor" id="parameter-comment"></div>

      .. _ansible_collections.checkmk.general.downtime_module__parameter-comment:

      .. rst-class:: ansible-option-title

      **comment**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-comment" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Remarks for the downtime. If omitted in combination with state = present, the default 'Set by Ansible' will be used, in combination with state = absent, ALL downtimes of a host or host/service will be removed.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"Managed by Ansible"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-duration"></div>

      .. _ansible_collections.checkmk.general.downtime_module__parameter-duration:

      .. rst-class:: ansible-option-title

      **duration**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-duration" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`integer`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Duration in minutes. When set, the downtime does not begin automatically at a nominated time, but when a non\-OK status actually appears for the host. Consequently, the start\_time and end\_time is only the time window in which the scheduled downtime can occur.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`0`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-end_after"></div>

      .. _ansible_collections.checkmk.general.downtime_module__parameter-end_after:

      .. rst-class:: ansible-option-title

      **end_after**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-end_after" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The timedelta between :emphasis:`start\_time` and :emphasis:`end\_time`. If you want to use :emphasis:`end\_after` you have to omit :emphasis:`end\_time`. For keys and values see \ `https://docs.python.org/3/library/datetime.html#datetime.timedelta <https://docs.python.org/3/library/datetime.html#datetime.timedelta>`__


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`{}`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-end_time"></div>

      .. _ansible_collections.checkmk.general.downtime_module__parameter-end_time:

      .. rst-class:: ansible-option-title

      **end_time**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-end_time" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The end datetime of the downtime. The format has to conform to the ISO 8601 profile :emphasis:`e.g. 2017\-07\-21T17:32:28Z`. The built\-in default is 30 minutes after now.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-force"></div>

      .. _ansible_collections.checkmk.general.downtime_module__parameter-force:

      .. rst-class:: ansible-option-title

      **force**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-force" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Force the creation of a downtime in case a hostname and comment combination already exists as a downtime.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`false` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-host_name"></div>

      .. _ansible_collections.checkmk.general.downtime_module__parameter-host_name:

      .. rst-class:: ansible-option-title

      **host_name**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-host_name" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The host to schedule the downtime on.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-server_url"></div>

      .. _ansible_collections.checkmk.general.downtime_module__parameter-server_url:

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
        <div class="ansibleOptionAnchor" id="parameter-service_descriptions"></div>

      .. _ansible_collections.checkmk.general.downtime_module__parameter-service_descriptions:

      .. rst-class:: ansible-option-title

      **service_descriptions**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-service_descriptions" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Array of service descriptions. If set only service\-downtimes will be set. If omitted a host downtime will be set.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`[]`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site"></div>

      .. _ansible_collections.checkmk.general.downtime_module__parameter-site:

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
        <div class="ansibleOptionAnchor" id="parameter-start_after"></div>

      .. _ansible_collections.checkmk.general.downtime_module__parameter-start_after:

      .. rst-class:: ansible-option-title

      **start_after**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-start_after" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The timedelta between now and :emphasis:`start\_time`. If you want to use :emphasis:`start\_after` you have to omit :emphasis:`start\_time`. For keys and values see \ `https://docs.python.org/3/library/datetime.html#datetime.timedelta <https://docs.python.org/3/library/datetime.html#datetime.timedelta>`__


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`{}`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-start_time"></div>

      .. _ansible_collections.checkmk.general.downtime_module__parameter-start_time:

      .. rst-class:: ansible-option-title

      **start_time**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-start_time" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The start datetime of the downtime. The format has to conform to the ISO 8601 profile :emphasis:`e.g. 2017\-07\-21T17:32:28Z`. The built\-in default is now.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-state"></div>

      .. _ansible_collections.checkmk.general.downtime_module__parameter-state:

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

      The state of this downtime. If absent, all matching host/service\-downtimes of the given host will be deleted.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`"present"` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`"absent"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-validate_certs"></div>

      .. _ansible_collections.checkmk.general.downtime_module__parameter-validate_certs:

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
   - Idempotency for creation was made for host downtimes by only using the hostname and comment attributes. If this combination already exists as a downtime, the new downtime will not be created except using the :strong:`force` argument. The creation of service downtimes works accordingly, with hostname, service description and comment.

.. Seealso


.. Examples

Examples
--------

.. code-block:: yaml+jinja

    # ---------------------------------------------------------------------------
    # Host downtimes - scheduling
    # ---------------------------------------------------------------------------

    - name: "Schedule a host downtime starting now, ending in 2 hours."
      checkmk.general.downtime:
        server_url: "https://myserver/"
        site: "mysite"
        api_user: "myuser"
        api_secret: "mysecret"
        host_name: "myhost"
        end_after:
          hours: 2

    - name: "Schedule a host downtime with a comment, starting now, ending in 2 hours."
      checkmk.general.downtime:
        server_url: "https://myserver/"
        site: "mysite"
        api_user: "myuser"
        api_secret: "mysecret"
        host_name: "myhost"
        comment: "Managed by Ansible"
        end_after:
          hours: 2

    - name: "Schedule a host downtime using absolute start and end times."
      checkmk.general.downtime:
        server_url: "https://myserver/"
        site: "mysite"
        api_user: "myuser"
        api_secret: "mysecret"
        host_name: "myhost"
        comment: "Managed by Ansible"
        start_time: "2024-03-25T22:00:00Z"
        end_time: "2024-03-26T02:00:00Z"

    - name: "Schedule a host downtime starting in 30 minutes and lasting 4 hours."
      checkmk.general.downtime:
        server_url: "https://myserver/"
        site: "mysite"
        api_user: "myuser"
        api_secret: "mysecret"
        host_name: "myhost"
        comment: "Managed by Ansible"
        start_after:
          minutes: 30
        end_after:
          hours: 4

    # ---------------------------------------------------------------------------
    # Host downtimes - removal
    # ---------------------------------------------------------------------------

    - name: "Remove all downtimes from a host."
      checkmk.general.downtime:
        server_url: "https://myserver/"
        site: "mysite"
        api_user: "myuser"
        api_secret: "mysecret"
        host_name: "myhost"
        state: "absent"

    - name: "Remove only host downtimes matching a specific comment."
      checkmk.general.downtime:
        server_url: "https://myserver/"
        site: "mysite"
        api_user: "myuser"
        api_secret: "mysecret"
        host_name: "myhost"
        comment: "Managed by Ansible"
        state: "absent"

    # ---------------------------------------------------------------------------
    # Service downtimes - scheduling
    # ---------------------------------------------------------------------------

    - name: "Schedule a downtime for a single service on a host."
      checkmk.general.downtime:
        server_url: "https://myserver/"
        site: "mysite"
        api_user: "myuser"
        api_secret: "mysecret"
        host_name: "myhost"
        comment: "Managed by Ansible"
        service_descriptions:
          - "Filesystem /"
        end_after:
          hours: 1

    - name: "Schedule downtimes for multiple services on a host using absolute times."
      checkmk.general.downtime:
        server_url: "https://myserver/"
        site: "mysite"
        api_user: "myuser"
        api_secret: "mysecret"
        host_name: "myhost"
        comment: "Managed by Ansible"
        start_time: "2024-03-25T22:00:00Z"
        end_time: "2024-03-26T02:00:00Z"
        service_descriptions:
          - "CPU utilization"
          - "Memory"

    # ---------------------------------------------------------------------------
    # Service downtimes - removal
    # ---------------------------------------------------------------------------

    - name: "Remove all downtimes for specific services on a host."
      checkmk.general.downtime:
        server_url: "https://myserver/"
        site: "mysite"
        api_user: "myuser"
        api_secret: "mysecret"
        host_name: "myhost"
        service_descriptions:
          - "CPU utilization"
          - "Memory"
        state: "absent"

    - name: "Remove service downtimes matching a specific comment."
      checkmk.general.downtime:
        server_url: "https://myserver/"
        site: "mysite"
        api_user: "myuser"
        api_secret: "mysecret"
        host_name: "myhost"
        comment: "Managed by Ansible"
        service_descriptions:
          - "CPU utilization"
          - "Memory"
        state: "absent"

    # ---------------------------------------------------------------------------
    # Looping over multiple hosts
    # ---------------------------------------------------------------------------

    - name: "Schedule a host downtime for multiple hosts."
      checkmk.general.downtime:
        server_url: "https://myserver/"
        site: "mysite"
        api_user: "myuser"
        api_secret: "mysecret"
        host_name: "{{ item }}"
        comment: "Managed by Ansible"
        start_time: "2024-03-25T22:00:00Z"
        end_time: "2024-03-26T02:00:00Z"
      loop:
        - "myhost01"
        - "myhost02"
        - "myhost03"

    - name: "Remove host downtimes for multiple hosts."
      checkmk.general.downtime:
        server_url: "https://myserver/"
        site: "mysite"
        api_user: "myuser"
        api_secret: "mysecret"
        host_name: "{{ item }}"
        comment: "Managed by Ansible"
        state: "absent"
      loop:
        - "myhost01"
        - "myhost02"
        - "myhost03"

    # ---------------------------------------------------------------------------
    # Flexible (triggered) downtime
    # ---------------------------------------------------------------------------
    # A flexible downtime does not start at a fixed time. Instead, it starts when
    # a non-OK state appears for the host or service within the configured time
    # window. The 'duration' parameter controls how long the downtime lasts once
    # triggered. 'start_time' and 'end_time' define the window during which the
    # trigger is active.
    # Refer to the official user guide for more details on the feature:
    # https://docs.checkmk.com/latest/en/basics_downtimes.html#advanced_options

    - name: "Schedule a flexible host downtime triggered by a non-OK state."
      checkmk.general.downtime:
        server_url: "https://myserver/"
        site: "mysite"
        api_user: "myuser"
        api_secret: "mysecret"
        host_name: "myhost"
        comment: "Flexible downtime during maintenance window"
        start_time: "2024-03-25T22:00:00Z"
        end_time: "2024-03-26T02:00:00Z"
        duration: 30

    # ---------------------------------------------------------------------------
    # Forcing a duplicate downtime
    # ---------------------------------------------------------------------------
    # By default, creating a downtime with the same host_name and comment combination
    # as an existing downtime is skipped for idempotency. Use 'force: true' to create a
    # duplicate downtime regardless.

    - name: "Force a new host downtime even if one with the same comment already exists."
      checkmk.general.downtime:
        server_url: "https://myserver/"
        site: "mysite"
        api_user: "myuser"
        api_secret: "mysecret"
        host_name: "myhost"
        comment: "Repeated patching run"
        end_after:
          hours: 2
        force: true

    # ---------------------------------------------------------------------------
    # Using environment variables for authentication
    # ---------------------------------------------------------------------------
    # Connection parameters can be provided via environment variables instead of
    # task parameters. The supported variables are:
    #   CHECKMK_VAR_SERVER_URL, CHECKMK_VAR_SITE,
    #   CHECKMK_VAR_API_USER, CHECKMK_VAR_API_SECRET,
    #   CHECKMK_VAR_VALIDATE_CERTS

    - name: "Schedule a host downtime using environment variables for authentication."
      checkmk.general.downtime:
        host_name: "myhost"
        comment: "Maintenance via env-based auth"
        end_after:
          hours: 2
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
        <div class="ansibleOptionAnchor" id="return-msg"></div>

      .. _ansible_collections.checkmk.general.downtime_module__return-msg:

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

      The output message that the module generates. Contains the API response details in case of an error. No output in case of success.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` always

      .. rst-class:: ansible-option-line
      .. rst-class:: ansible-option-sample

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`""`


      .. raw:: html

        </div>



..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- Oliver Gaida (@ogaida)
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

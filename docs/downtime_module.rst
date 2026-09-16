.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: 2.27.0

.. Anchors

.. _ansible_collections.checkmk.general.downtime_module:

.. Anchors: short name for ansible.builtin

.. Title

checkmk.general.downtime module -- Manage downtimes in Checkmk
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `checkmk.general collection <https://galaxy.ansible.com/ui/repo/published/checkmk/general/>`_ (version 8.5.0).

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

- Create, update and delete host and service downtimes in Checkmk.
- An existing downtime can be updated (e.g. to shorten or extend its end time) without deleting and recreating it. The downtime to act on can be identified by its ID, by host name (and optionally service descriptions), or by a Livestatus query.
- On the :emphasis:`host\_name` path the :emphasis:`comment` (which defaults to :literal:`Managed by Ansible`\ ) is part of a downtime's identity. A matching downtime is updated in place, while a different comment identifies a different downtime and creates a new one. This keeps the module idempotent and stops it from touching downtimes it did not create. To change a comment, match the downtime by :emphasis:`downtime\_id` or :emphasis:`query` instead.


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

      .. _ansible_collections.checkmk.general.downtime_module__parameter-api_user:
      .. _ansible_collections.checkmk.general.downtime_module__parameter-automation_user:

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

      The comment of the downtime.

      When creating or matching a downtime by :emphasis:`host\_name`\ , the comment is part of the identity of the downtime. If omitted, :literal:`Managed by Ansible` is used.

      When updating a downtime by :emphasis:`downtime\_id` or :emphasis:`query`\ , the comment is only changed if it is explicitly set here.

      When deleting by :emphasis:`host\_name`\ , the deletion is limited to downtimes with this comment if it is set, otherwise all matching downtimes are removed.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-downtime_id"></div>

      .. _ansible_collections.checkmk.general.downtime_module__parameter-downtime_id:

      .. rst-class:: ansible-option-title

      **downtime_id**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-downtime_id" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The numeric ID of a single downtime to update or delete.

      Requires :emphasis:`site\_id` to be set as well.

      Mutually exclusive with :emphasis:`host\_name` and :emphasis:`query`.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-downtime_type"></div>

      .. _ansible_collections.checkmk.general.downtime_module__parameter-downtime_type:

      .. rst-class:: ansible-option-title

      **downtime_type**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-downtime_type" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Selects whether a query operates on host downtimes (\ :literal:`host`\ ) or service downtimes (\ :literal:`service`\ ).

      Required for query\-based :strong:`create` to choose the object type. For :strong:`update`\ /\ :strong:`delete` it optionally narrows the matched downtimes to that type.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"host"`
      - :ansible-option-choices-entry:`"service"`


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

      Duration in minutes. When set, the downtime does not begin automatically at a nominated time, but when a non\-OK status actually appears for the host (flexible downtime).

      Only relevant when creating a downtime.


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

      The timedelta between the start time and the end time. Use this instead of :emphasis:`end\_time`. For keys and values see \ `https://docs.python.org/3/library/datetime.html#datetime.timedelta <https://docs.python.org/3/library/datetime.html#datetime.timedelta>`__.

      When updating an existing downtime, the delta is applied relative to the (defaulted) start time, i.e. now.


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

      The end datetime of the downtime, conforming to the ISO 8601 profile, e.g. :literal:`2017\-07\-21T17:32:28Z`.

      Used both when creating and when updating a downtime.


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

      When creating a downtime by :emphasis:`host\_name`\ , a new downtime is normally only created if no downtime with the same host, service and comment exists yet. Set this to :literal:`true` to always create a new downtime.


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

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The host to schedule, update or delete a downtime for.

      Mutually exclusive with :emphasis:`downtime\_id` and :emphasis:`query`.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-query"></div>

      .. _ansible_collections.checkmk.general.downtime_module__parameter-query:

      .. rst-class:: ansible-option-title

      **query**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-query" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`jsonarg`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      A Livestatus query, written in terms of the Livestatus :literal:`downtimes` table (e.g. :literal:`host\_name`\ , :literal:`service\_description`\ , :literal:`comment`\ ). See the Checkmk REST API documentation for the query syntax.

      Can be given either as a JSON string or as a native YAML/JSON mapping. Note that a variable holding a JSON string may be converted to a mapping by Ansible's templating, so both forms have to be accepted here.

      As the column names are different, depending on the Livestatus table, Please use the column names as defined in the downtimes table, e.g. :literal:`service\_description` instead of :literal:`description` and :literal:`host\_name` instead of :literal:`name`.

      Mutually exclusive with :emphasis:`downtime\_id` and :emphasis:`host\_name`.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-recurring"></div>
        <div class="ansibleOptionAnchor" id="parameter-recur"></div>

      .. _ansible_collections.checkmk.general.downtime_module__parameter-recur:
      .. _ansible_collections.checkmk.general.downtime_module__parameter-recurring:

      .. rst-class:: ansible-option-title

      **recurring**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-recurring" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-aliases:`aliases: recur`

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The recurring mode of a new downtime.

      Only relevant when creating a downtime.

      Only available when using the CMC. On the Nagios core the option is ignored and the downtime is created non\-recurring.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`"fixed"` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`"hour"`
      - :ansible-option-choices-entry:`"day"`
      - :ansible-option-choices-entry:`"week"`
      - :ansible-option-choices-entry:`"second\_week"`
      - :ansible-option-choices-entry:`"fourth\_week"`
      - :ansible-option-choices-entry:`"weekday\_start"`
      - :ansible-option-choices-entry:`"weekday\_end"`
      - :ansible-option-choices-entry:`"day\_of\_month"`


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

      A list of service descriptions.

      Together with :emphasis:`host\_name`\ , the module acts on service downtimes for these services on that particular host. If omitted, it acts on host downtimes.

      If you want to set a downtime on a particular service for :emphasis:`all` hosts, you have to use the :emphasis:`query` parameter.


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
        <div class="ansibleOptionAnchor" id="parameter-site_id"></div>

      .. _ansible_collections.checkmk.general.downtime_module__parameter-site_id:

      .. rst-class:: ansible-option-title

      **site_id**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site_id" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The site the downtime lives on. Required when using :emphasis:`downtime\_id`.


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

      The timedelta between now and the start time. Use this instead of :emphasis:`start\_time`. For keys and values see \ `https://docs.python.org/3/library/datetime.html#datetime.timedelta <https://docs.python.org/3/library/datetime.html#datetime.timedelta>`__.

      Only relevant when creating a downtime.


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

      The start datetime of a new downtime, conforming to the ISO 8601 profile, e.g. :literal:`2017\-07\-21T17:32:28Z`. Defaults to now.

      Only relevant when creating a downtime.


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

      The desired state of the downtime.


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
   - Creating a downtime is possible via :emphasis:`host\_name` or via :emphasis:`query` (using :emphasis:`downtime\_type` to choose host or service). Updating and deleting can be done via :emphasis:`downtime\_id`\ , :emphasis:`host\_name` or :emphasis:`query`.
   - Idempotency is based on the current end time and comment of the matching downtimes. Absolute times (\ :emphasis:`end\_time`\ ) are fully idempotent. Relative times (\ :emphasis:`end\_after`\ ) are recomputed on every run and will therefore usually trigger an update.
   - On the Community edition the Nagios core cannot modify a downtime in place. When an existing downtime needs its end time or comment changed on that edition, the module deletes and re\-creates it. The resulting downtime is identical except that it receives a new downtime ID. On CMC\-based editions the downtime is modified in place and keeps its ID.

.. Seealso

See Also
--------

.. seealso::

   :ref:`checkmk.general.downtime <ansible_collections.checkmk.general.downtime_lookup>` lookup plugin
       Show a downtime identified by its ID.
   :ref:`checkmk.general.downtimes <ansible_collections.checkmk.general.downtimes_lookup>` lookup plugin
       Get a list of downtimes.
   :ref:`checkmk.general.activation <ansible_collections.checkmk.general.activation_module>`
       Activate changes in Checkmk.
   :ref:`checkmk.general.host <ansible_collections.checkmk.general.host_module>`
       Manage hosts in Checkmk.
   :ref:`checkmk.general.rule <ansible_collections.checkmk.general.rule_module>`
       Manage rules in Checkmk.
   :ref:`checkmk.general.timeperiod <ansible_collections.checkmk.general.timeperiod_module>`
       Manage time periods in Checkmk.
   `Scheduling downtimes in Checkmk: The official user guide. <https://docs.checkmk.com/latest/en/basics_downtimes.html>`_
       The official user guide on scheduling downtimes.

.. Examples

Examples
--------

.. code-block:: yaml+jinja

    # ---------------------------------------------------------------------------
    # Creating downtimes
    # ---------------------------------------------------------------------------

    - name: "Schedule a host downtime starting now, ending in 2 hours."
      checkmk.general.downtime:
        server_url: "https://myserver"
        site: "mysite"
        api_user: "myuser"
        api_secret: "mysecret"
        host_name: "myhost"
        end_after:
          hours: 2

    - name: "Schedule a host downtime with a comment, starting now, ending in 2 hours."
      checkmk.general.downtime:
        server_url: "https://myserver"
        site: "mysite"
        api_user: "myuser"
        api_secret: "mysecret"
        host_name: "myhost"
        comment: "Managed by Ansible"
        end_after:
          hours: 2

    - name: "Schedule a host downtime using absolute start and end times."
      checkmk.general.downtime:
        server_url: "https://myserver"
        site: "mysite"
        api_user: "myuser"
        api_secret: "mysecret"
        host_name: "myhost"
        comment: "Managed by Ansible"
        start_time: "2024-03-25T22:00:00Z"
        end_time: "2024-03-26T02:00:00Z"

    - name: "Schedule downtimes for multiple services on a host."
      checkmk.general.downtime:
        server_url: "https://myserver"
        site: "mysite"
        api_user: "myuser"
        api_secret: "mysecret"
        host_name: "myhost"
        comment: "Managed by Ansible"
        service_descriptions:
          - "CPU utilization"
          - "Memory"
        end_after:
          hours: 1

    - name: "Schedule host downtimes for all hosts matching a query."
      checkmk.general.downtime:
        server_url: "https://myserver"
        site: "mysite"
        api_user: "myuser"
        api_secret: "mysecret"
        query: '{"op": "~", "left": "host_name", "right": "^web"}'
        downtime_type: "host"
        comment: "Rolling web tier maintenance"
        end_after:
          hours: 2

    - name: "Schedule host downtimes for a host group using a query."
      checkmk.general.downtime:
        server_url: "https://myserver"
        site: "mysite"
        api_user: "myuser"
        api_secret: "mysecret"
        query: '{"op": ">=", "left": "host_groups", "right": "my_hostgroup"}'
        downtime_type: "host"
        comment: "Maintenance for my_hostgroup"
        end_after:
          hours: 4

    - name: "Schedule service downtimes for all services matching a query."
      checkmk.general.downtime:
        server_url: "https://myserver"
        site: "mysite"
        api_user: "myuser"
        api_secret: "mysecret"
        query: '{"op": "=", "left": "service_description", "right": "Filesystem /"}'
        downtime_type: "service"
        comment: "Storage migration"
        end_after:
          hours: 1

    # ---------------------------------------------------------------------------
    # Updating an existing downtime
    # ---------------------------------------------------------------------------
    # Re-running the same host_name + comment with a different end time shortens or
    # extends the existing downtime instead of doing nothing.

    - name: "Shorten the previously created downtime."
      checkmk.general.downtime:
        server_url: "https://myserver"
        site: "mysite"
        api_user: "myuser"
        api_secret: "mysecret"
        host_name: "myhost"
        comment: "Managed by Ansible"
        end_after:
          minutes: 1

    - name: "Update a specific downtime by its ID."
      checkmk.general.downtime:
        server_url: "https://myserver"
        site: "mysite"
        api_user: "myuser"
        api_secret: "mysecret"
        downtime_id: "42"
        site_id: "mysite"
        end_time: "2024-03-26T00:00:00Z"
        comment: "Window reduced"

    - name: "Update all downtimes matching a query."
      checkmk.general.downtime:
        server_url: "https://myserver"
        site: "mysite"
        api_user: "myuser"
        api_secret: "mysecret"
        query: '{"op": "=", "left": "host_name", "right": "myhost"}'
        end_after:
          minutes: 30

    # On the host_name path the comment is part of the downtime's identity, so a
    # different comment is treated as a different downtime and a new one is created.
    # To change the comment of an existing downtime, select it by a query (e.g. by
    # its host and current comment) and set the new comment; the query matches the
    # downtime independently of the comment you are about to write.
    - name: "Change the comment of an existing downtime."
      checkmk.general.downtime:
        server_url: "https://myserver"
        site: "mysite"
        api_user: "myuser"
        api_secret: "mysecret"
        query: '{"op": "and", "expr": [{"op": "=", "left": "host_name", "right": "myhost"}, {"op": "=", "left": "comment", "right": "Managed by Ansible"}]}'
        comment: "Managed by Peter Grant"

    # ---------------------------------------------------------------------------
    # Deleting downtimes
    # ---------------------------------------------------------------------------

    - name: "Remove all downtimes from a host."
      checkmk.general.downtime:
        server_url: "https://myserver"
        site: "mysite"
        api_user: "myuser"
        api_secret: "mysecret"
        host_name: "myhost"
        state: "absent"

    - name: "Remove only host downtimes with a specific comment."
      checkmk.general.downtime:
        server_url: "https://myserver"
        site: "mysite"
        api_user: "myuser"
        api_secret: "mysecret"
        host_name: "myhost"
        comment: "Managed by Ansible"
        state: "absent"

    - name: "Delete a specific downtime by its ID."
      checkmk.general.downtime:
        server_url: "https://myserver"
        site: "mysite"
        api_user: "myuser"
        api_secret: "mysecret"
        downtime_id: "42"
        site_id: "mysite"
        state: "absent"

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
        CHECKMK_VAR_SERVER_URL: "https://myserver"
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

      .. _ansible_collections.checkmk.general.downtime_module__return-http_code:

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

      The HTTP code returned by the Checkmk API.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` always


      .. raw:: html

        </div>


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

      The output message that the module generates.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` always


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

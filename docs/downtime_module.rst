.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: 2.15.0

.. Anchors

.. _ansible_collections.checkmk.general.downtime_module:

.. Anchors: short name for ansible.builtin

.. Title

checkmk.general.downtime module -- Manage downtimes in Checkmk.
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `checkmk.general collection <https://galaxy.ansible.com/ui/repo/published/checkmk/general/>`_ (version 5.3.0).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible-galaxy collection install checkmk.general`.

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
        <div class="ansibleOptionAnchor" id="parameter-automation_secret"></div>

      .. _ansible_collections.checkmk.general.downtime_module__parameter-automation_secret:

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

      .. _ansible_collections.checkmk.general.downtime_module__parameter-automation_user:

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

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"Created by Ansible"`

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

      Duration in seconds. When set, the downtime does not begin automatically at a nominated time, but when a non-OK status actually appears for the host. Consequently, the start\_time and end\_time is only the time window in which the scheduled downtime can occur.


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

      The end datetime of the downtime. The format has to conform to the ISO 8601 profile :emphasis:`e.g. 2017-07-21T17:32:28Z`. The built-in default is 30 minutes after now.


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

      The base url of your Checkmk server including the protocol.


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

      Array of service descriptions. If set only service-downtimes will be set. If omitted a host downtime will be set.


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

      The site you want to connect to.


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

      The start datetime of the downtime. The format has to conform to the ISO 8601 profile :emphasis:`e.g. 2017-07-21T17:32:28Z`. The built-in default is now.


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

      The state of this downtime. If absent, all matching host/service-downtimes of the given host will be deleted.


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

      Whether to validate the SSL certificate of the Checkmk server.


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

    - name: "Schedule host downtime."
      checkmk.general.downtime:
        server_url: "{{ checkmk_var_server_url }}"
        site: "{{ mysite }}"
        automation_user: "{{ checkmk_var_automation_user }}"
        automation_secret: "{{ checkmk_var_automation_secret }}"
        host_name: my_host
        start_after:
          minutes: 5
        end_after:
          days: 7
          hours: 5

    - name: "Schedule service downtimes for two given services."
      checkmk.general.downtime:
        server_url: "{{ checkmk_var_server_url }}"
        site: "{{ mysite }}"
        automation_user: "{{ checkmk_var_automation_user }}"
        automation_secret: "{{ checkmk_var_automation_secret }}"
        host_name: my_host
        start_time: 2022-03-24T20:39:28Z
        end_time: 2022-03-24T20:40:28Z
        state: "present"
        duration: 0
        service_descriptions:
          - "CPU utilization"
          - "Memory"

    - name: "Delete all service downtimes for two given services."
      checkmk.general.downtime:
        server_url: "{{ checkmk_var_server_url }}"
        site: "{{ mysite }}"
        automation_user: "{{ checkmk_var_automation_user }}"
        automation_secret: "{{ checkmk_var_automation_secret }}"
        host_name: my_host
        service_descriptions:
          - "CPU utilization"
          - "Memory"
        state: absent



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

      .. _ansible_collections.checkmk.general.downtime_module__return-message:

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

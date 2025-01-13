.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: 2.16.1

.. Anchors

.. _ansible_collections.checkmk.general.agent_role:

.. Title

checkmk.general.agent role -- Install Checkmk agents
++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This role is part of the `checkmk.general collection <https://galaxy.ansible.com/ui/repo/published/checkmk/general/>`_ (version 5.3.2).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it use: :code:`ansible-galaxy collection install checkmk.general`.

    To use it in a playbook, specify: :code:`checkmk.general.agent`.

.. contents::
   :local:
   :depth: 2


.. Entry point title

Entry point ``main`` -- Install Checkmk agents
----------------------------------------------

.. version_added


.. Deprecated


Synopsis
^^^^^^^^

.. Description

- This role installs Checkmk agents.

.. Requirements


.. Options

Parameters
^^^^^^^^^^

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
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_agent_add_host"></div>

      .. _ansible_collections.checkmk.general.agent_role__parameter-main__checkmk_agent_add_host:

      .. rst-class:: ansible-option-title

      **checkmk_agent_add_host**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_agent_add_host" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Refer to the README for details.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`false` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_agent_auto_activate"></div>

      .. _ansible_collections.checkmk.general.agent_role__parameter-main__checkmk_agent_auto_activate:

      .. rst-class:: ansible-option-title

      **checkmk_agent_auto_activate**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_agent_auto_activate" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Refer to the README for details.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`false` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_agent_configure_firewall"></div>

      .. _ansible_collections.checkmk.general.agent_role__parameter-main__checkmk_agent_configure_firewall:

      .. rst-class:: ansible-option-title

      **checkmk_agent_configure_firewall**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_agent_configure_firewall" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Refer to the README for details.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry-default:`true` :ansible-option-choices-default-mark:`← (default)`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_agent_configure_firewall_zone"></div>

      .. _ansible_collections.checkmk.general.agent_role__parameter-main__checkmk_agent_configure_firewall_zone:

      .. rst-class:: ansible-option-title

      **checkmk_agent_configure_firewall_zone**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_agent_configure_firewall_zone" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Refer to the README for details.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"public"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_agent_delegate_api_calls"></div>

      .. _ansible_collections.checkmk.general.agent_role__parameter-main__checkmk_agent_delegate_api_calls:

      .. rst-class:: ansible-option-title

      **checkmk_agent_delegate_api_calls**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_agent_delegate_api_calls" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Refer to the README for details.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"localhost"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_agent_delegate_download"></div>

      .. _ansible_collections.checkmk.general.agent_role__parameter-main__checkmk_agent_delegate_download:

      .. rst-class:: ansible-option-title

      **checkmk_agent_delegate_download**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_agent_delegate_download" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Refer to the README for details.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"{{ inventory\_hostname }}"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_agent_discover"></div>

      .. _ansible_collections.checkmk.general.agent_role__parameter-main__checkmk_agent_discover:

      .. rst-class:: ansible-option-title

      **checkmk_agent_discover**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_agent_discover" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Refer to the README for details.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`false` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_agent_discover_max_parallel_tasks"></div>

      .. _ansible_collections.checkmk.general.agent_role__parameter-main__checkmk_agent_discover_max_parallel_tasks:

      .. rst-class:: ansible-option-title

      **checkmk_agent_discover_max_parallel_tasks**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_agent_discover_max_parallel_tasks" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`integer`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Refer to the README for details.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`0`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_agent_edition"></div>

      .. _ansible_collections.checkmk.general.agent_role__parameter-main__checkmk_agent_edition:

      .. rst-class:: ansible-option-title

      **checkmk_agent_edition**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_agent_edition" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Refer to the README for details.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"cre"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_agent_folder"></div>

      .. _ansible_collections.checkmk.general.agent_role__parameter-main__checkmk_agent_folder:

      .. rst-class:: ansible-option-title

      **checkmk_agent_folder**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_agent_folder" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Refer to the README for details.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"{{ checkmk\_var\_folder\_path | default('/') }}"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_agent_force_foreign_changes"></div>

      .. _ansible_collections.checkmk.general.agent_role__parameter-main__checkmk_agent_force_foreign_changes:

      .. rst-class:: ansible-option-title

      **checkmk_agent_force_foreign_changes**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_agent_force_foreign_changes" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Refer to the README for details.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`false` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_agent_force_install"></div>

      .. _ansible_collections.checkmk.general.agent_role__parameter-main__checkmk_agent_force_install:

      .. rst-class:: ansible-option-title

      **checkmk_agent_force_install**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_agent_force_install" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Refer to the README for details.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`false` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_agent_host_attributes"></div>

      .. _ansible_collections.checkmk.general.agent_role__parameter-main__checkmk_agent_host_attributes:

      .. rst-class:: ansible-option-title

      **checkmk_agent_host_attributes**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_agent_host_attributes" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Refer to the README for details.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`{"ipaddress": "{{ checkmk\_agent\_host\_ip | default(omit) }}"}`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_agent_host_name"></div>

      .. _ansible_collections.checkmk.general.agent_role__parameter-main__checkmk_agent_host_name:

      .. rst-class:: ansible-option-title

      **checkmk_agent_host_name**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_agent_host_name" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Refer to the README for details.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"{{ inventory\_hostname }}"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_agent_mode"></div>

      .. _ansible_collections.checkmk.general.agent_role__parameter-main__checkmk_agent_mode:

      .. rst-class:: ansible-option-title

      **checkmk_agent_mode**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_agent_mode" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Refer to the README for details.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"pull"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_agent_no_log"></div>

      .. _ansible_collections.checkmk.general.agent_role__parameter-main__checkmk_agent_no_log:

      .. rst-class:: ansible-option-title

      **checkmk_agent_no_log**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_agent_no_log" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Refer to the README for details.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry-default:`true` :ansible-option-choices-default-mark:`← (default)`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_agent_pass"></div>

      .. _ansible_collections.checkmk.general.agent_role__parameter-main__checkmk_agent_pass:

      .. rst-class:: ansible-option-title

      **checkmk_agent_pass**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_agent_pass" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Refer to the README for details.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"{{ checkmk\_var\_automation\_secret }}"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_agent_port"></div>

      .. _ansible_collections.checkmk.general.agent_role__parameter-main__checkmk_agent_port:

      .. rst-class:: ansible-option-title

      **checkmk_agent_port**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_agent_port" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`integer`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Refer to the README for details.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`6556`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_agent_prep_legacy"></div>

      .. _ansible_collections.checkmk.general.agent_role__parameter-main__checkmk_agent_prep_legacy:

      .. rst-class:: ansible-option-title

      **checkmk_agent_prep_legacy**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_agent_prep_legacy" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Refer to the README for details.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`false` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_agent_registration_server"></div>

      .. _ansible_collections.checkmk.general.agent_role__parameter-main__checkmk_agent_registration_server:

      .. rst-class:: ansible-option-title

      **checkmk_agent_registration_server**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_agent_registration_server" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Refer to the README for details.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"{{ checkmk\_agent\_server }}"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_agent_registration_server_protocol"></div>

      .. _ansible_collections.checkmk.general.agent_role__parameter-main__checkmk_agent_registration_server_protocol:

      .. rst-class:: ansible-option-title

      **checkmk_agent_registration_server_protocol**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_agent_registration_server_protocol" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Refer to the README for details.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"{{ checkmk\_agent\_server\_protocol }}"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_agent_registration_site"></div>

      .. _ansible_collections.checkmk.general.agent_role__parameter-main__checkmk_agent_registration_site:

      .. rst-class:: ansible-option-title

      **checkmk_agent_registration_site**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_agent_registration_site" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Refer to the README for details.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"{{ checkmk\_agent\_site }}"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_agent_secret"></div>

      .. _ansible_collections.checkmk.general.agent_role__parameter-main__checkmk_agent_secret:

      .. rst-class:: ansible-option-title

      **checkmk_agent_secret**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_agent_secret" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Refer to the README for details.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"{{ checkmk\_var\_automation\_secret }}"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_agent_server"></div>

      .. _ansible_collections.checkmk.general.agent_role__parameter-main__checkmk_agent_server:

      .. rst-class:: ansible-option-title

      **checkmk_agent_server**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_agent_server" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Refer to the README for details.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_agent_server_ips"></div>

      .. _ansible_collections.checkmk.general.agent_role__parameter-main__checkmk_agent_server_ips:

      .. rst-class:: ansible-option-title

      **checkmk_agent_server_ips**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_agent_server_ips" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Refer to the README for details.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_agent_server_port"></div>

      .. _ansible_collections.checkmk.general.agent_role__parameter-main__checkmk_agent_server_port:

      .. rst-class:: ansible-option-title

      **checkmk_agent_server_port**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_agent_server_port" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Refer to the README for details.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"{% if checkmk\_agent\_server\_protocol == 'https' %}443{% else %}80{% endif %}"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_agent_server_protocol"></div>

      .. _ansible_collections.checkmk.general.agent_role__parameter-main__checkmk_agent_server_protocol:

      .. rst-class:: ansible-option-title

      **checkmk_agent_server_protocol**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_agent_server_protocol" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Refer to the README for details.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"http"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_agent_server_validate_certs"></div>

      .. _ansible_collections.checkmk.general.agent_role__parameter-main__checkmk_agent_server_validate_certs:

      .. rst-class:: ansible-option-title

      **checkmk_agent_server_validate_certs**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_agent_server_validate_certs" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Refer to the README for details.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry-default:`true` :ansible-option-choices-default-mark:`← (default)`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_agent_site"></div>

      .. _ansible_collections.checkmk.general.agent_role__parameter-main__checkmk_agent_site:

      .. rst-class:: ansible-option-title

      **checkmk_agent_site**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_agent_site" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Refer to the README for details.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_agent_tls"></div>

      .. _ansible_collections.checkmk.general.agent_role__parameter-main__checkmk_agent_tls:

      .. rst-class:: ansible-option-title

      **checkmk_agent_tls**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_agent_tls" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Refer to the README for details.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`false` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_agent_update"></div>

      .. _ansible_collections.checkmk.general.agent_role__parameter-main__checkmk_agent_update:

      .. rst-class:: ansible-option-title

      **checkmk_agent_update**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_agent_update" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Refer to the README for details.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`false` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_agent_user"></div>

      .. _ansible_collections.checkmk.general.agent_role__parameter-main__checkmk_agent_user:

      .. rst-class:: ansible-option-title

      **checkmk_agent_user**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_agent_user" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Refer to the README for details.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"{{ automation\_user | default('automation') }}"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_agent_version"></div>

      .. _ansible_collections.checkmk.general.agent_role__parameter-main__checkmk_agent_version:

      .. rst-class:: ansible-option-title

      **checkmk_agent_version**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_agent_version" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Refer to the README for details.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"2.3.0p19"`

      .. raw:: html

        </div>


.. Attributes


.. Notes


.. Seealso



Authors
^^^^^^^

- Robin Gierse



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

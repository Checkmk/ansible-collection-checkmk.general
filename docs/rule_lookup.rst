
.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: 2.12.0

.. Anchors

.. _ansible_collections.checkmk.general.rule_lookup:

.. Anchors: short name for ansible.builtin

.. Title

checkmk.general.rule lookup -- Show a rule
++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This lookup plugin is part of the `checkmk.general collection <https://galaxy.ansible.com/ui/repo/published/checkmk/general/>`_ (version 5.2.1).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible-galaxy collection install checkmk.general`.

    To use it in a playbook, specify: :code:`checkmk.general.rule`.

.. version_added

.. rst-class:: ansible-version-added

New in checkmk.general 3.5.0

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Returns details of a rule


.. Aliases


.. Requirements






.. Options

Keyword parameters
------------------

This describes keyword parameters of the lookup. These are the values ``key1=value1``, ``key2=value2`` and so on in the following
examples: ``lookup('checkmk.general.rule', key1=value1, key2=value2, ...)`` and ``query('checkmk.general.rule', key1=value1, key2=value2, ...)``

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

      .. _ansible_collections.checkmk.general.rule_lookup__parameter-automation_secret:

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

      Automation secret for the REST API access.


      .. rst-class:: ansible-option-line

      :ansible-option-configuration:`Configuration:`

      - INI entry:

        .. code-block::

          [checkmk_lookup]
          automation_secret = VALUE


      - Environment variable: :envvar:`ANSIBLE\_LOOKUP\_CHECKMK\_AUTOMATION\_SECRET`

      - Variable: ansible\_lookup\_checkmk\_automation\_secret


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-automation_user"></div>

      .. _ansible_collections.checkmk.general.rule_lookup__parameter-automation_user:

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

      Automation user for the REST API access.


      .. rst-class:: ansible-option-line

      :ansible-option-configuration:`Configuration:`

      - INI entry:

        .. code-block::

          [checkmk_lookup]
          automation_user = VALUE


      - Environment variable: :envvar:`ANSIBLE\_LOOKUP\_CHECKMK\_AUTOMATION\_USER`

      - Variable: ansible\_lookup\_checkmk\_automation\_user


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule_id"></div>

      .. _ansible_collections.checkmk.general.rule_lookup__parameter-rule_id:

      .. rst-class:: ansible-option-title

      **rule_id**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule_id" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The rule id.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-server_url"></div>

      .. _ansible_collections.checkmk.general.rule_lookup__parameter-server_url:

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

      URL of the Checkmk server.


      .. rst-class:: ansible-option-line

      :ansible-option-configuration:`Configuration:`

      - INI entry:

        .. code-block::

          [checkmk_lookup]
          server_url = VALUE


      - Environment variable: :envvar:`ANSIBLE\_LOOKUP\_CHECKMK\_SERVER\_URL`

      - Variable: ansible\_lookup\_checkmk\_server\_url


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site"></div>

      .. _ansible_collections.checkmk.general.rule_lookup__parameter-site:

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

      Site name.


      .. rst-class:: ansible-option-line

      :ansible-option-configuration:`Configuration:`

      - INI entry:

        .. code-block::

          [checkmk_lookup]
          site = VALUE


      - Environment variable: :envvar:`ANSIBLE\_LOOKUP\_CHECKMK\_SITE`

      - Variable: ansible\_lookup\_checkmk\_site


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-validate_certs"></div>

      .. _ansible_collections.checkmk.general.rule_lookup__parameter-validate_certs:

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

      Whether or not to validate TLS certificates.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry-default:`true` :ansible-option-choices-default-mark:`← (default)`


      .. rst-class:: ansible-option-line

      :ansible-option-configuration:`Configuration:`

      - INI entry:

        .. code-block::

          [checkmk_lookup]
          validate_certs = true


      - Environment variable: :envvar:`ANSIBLE\_LOOKUP\_CHECKMK\_VALIDATE\_CERTS`

      - Variable: ansible\_lookup\_checkmk\_validate\_certs


      .. raw:: html

        </div>


.. Attributes


.. Notes

Notes
-----

.. note::
   - Like all lookups, this runs on the Ansible controller and is unaffected by other keywords such as 'become'. If you need to use different permissions, you must change the command or run Ansible as another user.
   - Alternatively, you can use a shell/command task that runs against localhost and registers the result.
   - The directory of the play is used as the current working directory.
   - It is \ :strong:`NOT`\  possible to assign other variables to the variables mentioned in the \ :literal:`vars`\  section! This is a limitation of Ansible itself.

.. Seealso


.. Examples

Examples
--------

.. code-block:: yaml+jinja

    
    - name: Get a rule with a particular rule id
      ansible.builtin.debug:
        msg: "Rule: {{ extensions }}"
      vars:
        extensions: "{{
          lookup('checkmk.general.rule',
            rule_id='a9285bc1-dcaf-45e0-a3ba-ad398ef06a49',
            server_url=server_url,
            site=site,
            automation_user=automation_user,
            automation_secret=automation_secret,
            validate_certs=False
          )
        }}"

    - name: "Use variables outside the module call."
      ansible.builtin.debug:
        msg: "Rule: {{ extensions }}"
      vars:
        ansible_lookup_checkmk_server_url: "http://myserver/"
        ansible_lookup_checkmk_site: "mysite"
        ansible_lookup_checkmk_automation_user: "myuser"
        ansible_lookup_checkmk_automation_secret: "mysecret"
        ansible_lookup_checkmk_validate_certs: false
        attributes: "{{ lookup('checkmk.general.rule', rule_id='a9285bc1-dcaf-45e0-a3ba-ad398ef06a49') }}"




.. Facts


.. Return values

Return Value
------------

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
        <div class="ansibleOptionAnchor" id="return-_list"></div>

      .. _ansible_collections.checkmk.general.rule_lookup__return-_list:

      .. rst-class:: ansible-option-title

      **Return value**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-_list" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The details of a particular rule


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` success


      .. raw:: html

        </div>



..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- Lars Getwan (@lgetwan)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.

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


.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: 2.19.1

.. Anchors

.. _ansible_collections.checkmk.general.folder_lookup:

.. Anchors: short name for ansible.builtin

.. Title

checkmk.general.folder lookup -- Get folder attributes
++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This lookup plugin is part of the `checkmk.general collection <https://galaxy.ansible.com/ui/repo/published/checkmk/general/>`_ (version 6.0.1).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible-galaxy collection install checkmk.general`.

    To use it in a playbook, specify: :code:`checkmk.general.folder`.

.. version_added

.. rst-class:: ansible-version-added

New in checkmk.general 3.3.0

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Returns the attributes of a folder


.. Aliases


.. Requirements




.. Terms

Terms
-----

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
        <div class="ansibleOptionAnchor" id="parameter-_terms"></div>

      .. _ansible_collections.checkmk.general.folder_lookup__parameter-_terms:

      .. rst-class:: ansible-option-title

      **Terms**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-_terms" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      complete folder path using tilde as a delimiter


      .. raw:: html

        </div>





.. Options

Keyword parameters
------------------

This describes keyword parameters of the lookup. These are the values ``key1=value1``, ``key2=value2`` and so on in the following
examples: ``lookup('checkmk.general.folder', key1=value1, key2=value2, ...)`` and ``query('checkmk.general.folder', key1=value1, key2=value2, ...)``

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

      .. _ansible_collections.checkmk.general.folder_lookup__parameter-automation_secret:

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

        .. code-block:: ini

          [checkmk_lookup]
          automation_secret = VALUE


      - Environment variable: :envvar:`CHECKMK\_VAR\_AUTOMATION\_SECRET`

      - Environment variable: :envvar:`ANSIBLE\_LOOKUP\_CHECKMK\_AUTOMATION\_SECRET`

      - Variable: checkmk\_var\_automation\_secret

      - Variable: ansible\_lookup\_checkmk\_automation\_secret


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-automation_user"></div>

      .. _ansible_collections.checkmk.general.folder_lookup__parameter-automation_user:

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

        .. code-block:: ini

          [checkmk_lookup]
          automation_user = VALUE


      - Environment variable: :envvar:`CHECKMK\_VAR\_AUTOMATION\_USER`

      - Environment variable: :envvar:`ANSIBLE\_LOOKUP\_CHECKMK\_AUTOMATION\_USER`

      - Variable: checkmk\_var\_automation\_user

      - Variable: ansible\_lookup\_checkmk\_automation\_user


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-server_url"></div>

      .. _ansible_collections.checkmk.general.folder_lookup__parameter-server_url:

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

        .. code-block:: ini

          [checkmk_lookup]
          server_url = VALUE


      - Environment variable: :envvar:`CHECKMK\_VAR\_SERVER\_URL`

      - Environment variable: :envvar:`ANSIBLE\_LOOKUP\_CHECKMK\_SERVER\_URL`

      - Variable: checkmk\_var\_server\_url

      - Variable: ansible\_lookup\_checkmk\_server\_url


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site"></div>

      .. _ansible_collections.checkmk.general.folder_lookup__parameter-site:

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

        .. code-block:: ini

          [checkmk_lookup]
          site = VALUE


      - Environment variable: :envvar:`CHECKMK\_VAR\_SITE`

      - Environment variable: :envvar:`ANSIBLE\_LOOKUP\_CHECKMK\_SITE`

      - Variable: checkmk\_var\_site

      - Variable: ansible\_lookup\_checkmk\_site


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-validate_certs"></div>

      .. _ansible_collections.checkmk.general.folder_lookup__parameter-validate_certs:

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

        .. code-block:: ini

          [checkmk_lookup]
          validate_certs = true


      - Environment variable: :envvar:`CHECKMK\_VAR\_VALIDATE\_CERTS`

      - Environment variable: :envvar:`ANSIBLE\_LOOKUP\_CHECKMK\_VALIDATE\_CERTS`

      - Variable: checkmk\_var\_validate\_certs

      - Variable: ansible\_lookup\_checkmk\_validate\_certs


      .. raw:: html

        </div>


.. note::

    Configuration entries listed above for each entry type (Ansible variable, environment variable, and so on) have a low to high priority order.
    For example, a variable that is lower in the list will override a variable that is higher up.
    The entry types are also ordered by precedence from low to high priority order.
    For example, an ansible.cfg entry (further up in the list) is overwritten by an Ansible variable (further down in the list).

.. Attributes


.. Notes

Notes
-----

.. note::
   - When keyword and positional parameters are used together, positional parameters must be listed before keyword parameters:
     ``lookup('checkmk.general.folder', term1, term2, key1=value1, key2=value2)`` and ``query('checkmk.general.folder', term1, term2, key1=value1, key2=value2)``
   - Like all lookups, this runs on the Ansible controller and is unaffected by other keywords such as 'become'. If you need to use different permissions, you must change the command or run Ansible as another user.
   - Alternatively, you can use a shell/command task that runs against localhost and registers the result.
   - The directory of the play is used as the current working directory.
   - It is :strong:`NOT` possible to assign other variables to the variables mentioned in the :literal:`vars` section! This is a limitation of Ansible itself.

.. Seealso


.. Examples

Examples
--------

.. code-block:: yaml+jinja

    - name: Get the attributes of folders /tests and /snmp
      ansible.builtin.debug:
        msg: "Extended attributes of folder /network: {{ attributes.extensions }}"
      loop: "{{
               lookup('checkmk.general.folder',
                      '~tests', '~snmp',
                      server_url=my_server_url,
                      site=mysite,
                      automation_user=myuser,
                      automation_secret=mysecret,
                      validate_certs=False
                      )
             }}"

    - name: "Use variables from inventory."
      ansible.builtin.debug:
        msg: "Extended attributes of folder /network: {{ attributes.extensions }}"
      vars:
        checkmk_var_server_url: "http://myserver/"
        checkmk_var_site: "mysite"
        checkmk_var_automation_user: "myuser"
        checkmk_var_automation_secret: "mysecret"
        checkmk_var_validate_certs: false
        attributes: "{{ lookup('checkmk.general.folder', '~tests') }}"



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

      .. _ansible_collections.checkmk.general.folder_lookup__return-_list:

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

      A dict of attributes of the folder if you query a single folder

      A list of dicts of attributes of the folders if you query multiple folders


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` success


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

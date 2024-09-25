
.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: 2.12.0

.. Anchors

.. _ansible_collections.checkmk.general.folder_module:

.. Anchors: short name for ansible.builtin

.. Title

checkmk.general.folder module -- Manage folders in Checkmk.
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `checkmk.general collection <https://galaxy.ansible.com/ui/repo/published/checkmk/general/>`_ (version 5.2.1).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible-galaxy collection install checkmk.general`.

    To use it in a playbook, specify: :code:`checkmk.general.folder`.

.. version_added

.. rst-class:: ansible-version-added

New in checkmk.general 0.0.1

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Manage folders within Checkmk.


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
        <div class="ansibleOptionAnchor" id="parameter-attributes"></div>

      .. _ansible_collections.checkmk.general.folder_module__parameter-attributes:

      .. rst-class:: ansible-option-title

      **attributes**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-attributes" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`any`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The attributes of your folder as described in the API documentation. \ :strong:`Attention! This option OVERWRITES all existing attributes!`\  As of Check MK v2.2.0p7 and v2.3.0b1, simultaneous use of \ :emphasis:`attributes`\ , \ :emphasis:`remove\_attributes`\ , and \ :emphasis:`update\_attributes`\  is no longer supported.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-automation_secret"></div>

      .. _ansible_collections.checkmk.general.folder_module__parameter-automation_secret:

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

      .. _ansible_collections.checkmk.general.folder_module__parameter-automation_user:

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
        <div class="ansibleOptionAnchor" id="parameter-extended_functionality"></div>

      .. _ansible_collections.checkmk.general.folder_module__parameter-extended_functionality:

      .. rst-class:: ansible-option-title

      **extended_functionality**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-extended_functionality" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Allow extended functionality instead of the expected REST API behavior.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry-default:`true` :ansible-option-choices-default-mark:`← (default)`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-name"></div>
        <div class="ansibleOptionAnchor" id="parameter-title"></div>

      .. _ansible_collections.checkmk.general.folder_module__parameter-name:
      .. _ansible_collections.checkmk.general.folder_module__parameter-title:

      .. rst-class:: ansible-option-title

      **name**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-name" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-aliases:`aliases: title`

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The name (title) of your folder. If omitted defaults to the string after the last \ :literal:`/`\  in \ :emphasis:`path`\ .


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-path"></div>

      .. _ansible_collections.checkmk.general.folder_module__parameter-path:

      .. rst-class:: ansible-option-title

      **path**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-path" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The full path to the folder you want to manage. Pay attention to the leading \ :literal:`/`\  and avoid trailing \ :literal:`/`\ . Special characters apart from \ :literal:`\_`\  are not allowed!


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-remove_attributes"></div>

      .. _ansible_collections.checkmk.general.folder_module__parameter-remove_attributes:

      .. rst-class:: ansible-option-title

      **remove_attributes**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-remove_attributes" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`any`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The remove\_attributes of your host as described in the API documentation. \ :strong:`If a list of strings is supplied, the listed attributes are removed.`\  \ :strong:`If extended\_functionality and a dict is supplied, the attributes that exactly match the passed attributes are removed.`\  This will only remove the given attributes. As of Check MK v2.2.0p7 and v2.3.0b1, simultaneous use of \ :emphasis:`attributes`\ , \ :emphasis:`remove\_attributes`\ , and \ :emphasis:`update\_attributes`\  is no longer supported.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-server_url"></div>

      .. _ansible_collections.checkmk.general.folder_module__parameter-server_url:

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
        <div class="ansibleOptionAnchor" id="parameter-site"></div>

      .. _ansible_collections.checkmk.general.folder_module__parameter-site:

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

      .. _ansible_collections.checkmk.general.folder_module__parameter-state:

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

      The state of your folder.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`"present"` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`"absent"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-update_attributes"></div>

      .. _ansible_collections.checkmk.general.folder_module__parameter-update_attributes:

      .. rst-class:: ansible-option-title

      **update_attributes**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-update_attributes" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`any`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The update\_attributes of your host as described in the API documentation. This will only update the given attributes. As of Check MK v2.2.0p7 and v2.3.0b1, simultaneous use of \ :emphasis:`attributes`\ , \ :emphasis:`remove\_attributes`\ , and \ :emphasis:`update\_attributes`\  is no longer supported.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-validate_certs"></div>

      .. _ansible_collections.checkmk.general.folder_module__parameter-validate_certs:

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

    
    # Create a single folder.
    - name: "Create a single folder."
      checkmk.general.folder:
        server_url: "http://myserver/"
        site: "mysite"
        automation_user: "myuser"
        automation_secret: "mysecret"
        path: "/my_folder"
        name: "My Folder"
        state: "present"

    # Create a folder who's hosts should be hosted on a remote site.
    - name: "Create a single folder."
      checkmk.general.folder:
        server_url: "http://myserver/"
        site: "mysite"
        automation_user: "myuser"
        automation_secret: "mysecret"
        path: "/my_remote_folder"
        name: "My Remote Folder"
        attributes:
          site: "my_remote_site"
        state: "present"

    # Create a folder with Criticality set to a Test system and Networking Segment WAN (high latency)"
    - name: "Create a folder with tag_criticality test and tag_networking wan"
      checkmk.general.folder:
        server_url: "http://myserver/"
        site: "mysite"
        automation_user: "myuser"
        automation_secret: "mysecret"
        path: "/my_remote_folder"
        attributes:
          tag_criticality: "test"
          tag_networking: "wan"
        state: "present"

    # Update only specified attributes
    - name: "Update only specified attributes"
      checkmk.general.folder:
        server_url: "http://myserver/"
        site: "mysite"
        automation_user: "myuser"
        automation_secret: "mysecret"
        path: "/my_folder"
        update_attributes:
          tag_networking: "dmz"
        state: "present"

    # Remove specified attributes
    - name: "Remove specified attributes"
      checkmk.general.folder:
        server_url: "http://myserver/"
        site: "mysite"
        automation_user: "myuser"
        automation_secret: "mysecret"
        path: "/my_folder"
        remove_attributes:
          - tag_networking
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

      .. _ansible_collections.checkmk.general.folder_module__return-message:

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

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`"Folder created."`


      .. raw:: html

        </div>



..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- Robin Gierse (@robin-checkmk)
- Lars Getwan (@lgetwan)
- Michael Sekania (@msekania)



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


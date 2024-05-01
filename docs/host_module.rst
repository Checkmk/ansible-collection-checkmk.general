
.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: 2.10.0

.. Anchors

.. _ansible_collections.checkmk.general.host_module:

.. Anchors: short name for ansible.builtin

.. Title

checkmk.general.host module -- Manage hosts in Checkmk.
+++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `checkmk.general collection <https://galaxy.ansible.com/ui/repo/published/checkmk/general/>`_ (version 4.4.1).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible-galaxy collection install checkmk.general`.

    To use it in a playbook, specify: :code:`checkmk.general.host`.

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

- Manage hosts within Checkmk.


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
        <div class="ansibleOptionAnchor" id="parameter-add_nodes"></div>

      .. _ansible_collections.checkmk.general.host_module__parameter-add_nodes:

      .. rst-class:: ansible-option-title

      **add_nodes**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-add_nodes" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      List of nodes to be added as members of the cluster-container host provided in name. Works only if the existing host was already a cluster host, or entirely new is created. \ :strong:`Mutualy exclusive with I(nodes`\  and \ :emphasis:`remove\_nodes`\ .)


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-attributes"></div>

      .. _ansible_collections.checkmk.general.host_module__parameter-attributes:

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

      The attributes of your host as described in the API documentation. \ :strong:`Attention! This option OVERWRITES all existing attributes!`\  \ :strong:`Attention! I(folder`\  should match the folder where host is residing) If you are using custom tags, make sure to prepend the attribute with \ :literal:`tag\_`\ .


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-automation_secret"></div>

      .. _ansible_collections.checkmk.general.host_module__parameter-automation_secret:

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

      .. _ansible_collections.checkmk.general.host_module__parameter-automation_user:

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

      .. _ansible_collections.checkmk.general.host_module__parameter-extended_functionality:

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
        <div class="ansibleOptionAnchor" id="parameter-folder"></div>

      .. _ansible_collections.checkmk.general.host_module__parameter-folder:

      .. rst-class:: ansible-option-title

      **folder**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-folder" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The folder your host is located in. On create it defaults to \ :literal:`/`\ . \ :strong:`For existing host, host is moved to the specified folder if different and this procedue is mutualy exclusive with specified I(attributes`\ , \ :emphasis:`update\_attributes`\ , and \ :emphasis:`remove\_attributes`\ ).


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-name"></div>

      .. _ansible_collections.checkmk.general.host_module__parameter-name:

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

      The host you want to manage.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-nodes"></div>

      .. _ansible_collections.checkmk.general.host_module__parameter-nodes:

      .. rst-class:: ansible-option-title

      **nodes**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-nodes" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Nodes, members of the cluster-container host provided in name. \ :strong:`Mutualy exclusive with I(add\_nodes`\  and \ :emphasis:`remove\_nodes`\ .)


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-remove_attributes"></div>

      .. _ansible_collections.checkmk.general.host_module__parameter-remove_attributes:

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

      The remove\_attributes of your host as described in the API documentation. \ :strong:`Attention! I(folder`\  should match the folder where host is residing) \ :strong:`If a list of strings is supplied, the listed attributes are removed.`\  \ :strong:`If`\  \ :emphasis:`extended\_functionality`\  \ :strong:`and a dict is supplied, the attributes that exactly match the passed attributes are removed.`\  This will only remove the given attributes. If you are using custom tags, make sure to prepend the attribute with \ :literal:`tag\_`\ . As of Checkmk 2.2.0p7 and 2.3.0b1, simultaneous use of \ :emphasis:`attributes`\ , \ :emphasis:`remove\_attributes`\ , and \ :emphasis:`update\_attributes`\  is no longer supported.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-remove_nodes"></div>

      .. _ansible_collections.checkmk.general.host_module__parameter-remove_nodes:

      .. rst-class:: ansible-option-title

      **remove_nodes**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-remove_nodes" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      List of nodes to be removes from the cluster-container host provided in name. \ :strong:`Mutualy exclusive with I(nodes`\  and \ :emphasis:`add\_nodes`\ .)


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-server_url"></div>

      .. _ansible_collections.checkmk.general.host_module__parameter-server_url:

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

      .. _ansible_collections.checkmk.general.host_module__parameter-site:

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

      .. _ansible_collections.checkmk.general.host_module__parameter-state:

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

      The state of your host.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`"present"` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`"absent"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-update_attributes"></div>

      .. _ansible_collections.checkmk.general.host_module__parameter-update_attributes:

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

      The update\_attributes of your host as described in the API documentation. \ :strong:`Attention! I(folder`\  should match the folder where host is residing) This will only update the given attributes. If you are using custom tags, make sure to prepend the attribute with \ :literal:`tag\_`\ .


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-validate_certs"></div>

      .. _ansible_collections.checkmk.general.host_module__parameter-validate_certs:

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

    
    # Create a host.
    - name: "Create a host."
      checkmk.general.host:
        server_url: "http://my_server/"
        site: "my_site"
        automation_user: "my_user"
        automation_secret: "my_secret"
        name: "my_host"
        folder: "/"
        state: "present"

    # Create a host with IP.
    - name: "Create a host with IP address."
      checkmk.general.host:
        server_url: "http://my_server/"
        site: "my_site"
        automation_user: "my_user"
        automation_secret: "my_secret"
        name: "my_host"
        attributes:
          alias: "My Host"
          ipaddress: "127.0.0.1"
        folder: "/"
        state: "present"

    # Create a host which is monitored on a distinct site.
    - name: "Create a host which is monitored on a distinct site."
      checkmk.general.host:
        server_url: "http://my_server/"
        site: "my_site"
        automation_user: "my_user"
        automation_secret: "my_secret"
        name: "my_host"
        attributes:
          site: "my_remote_site"
        folder: "/"
        state: "present"

    # Create a cluster host.
    - name: "Create a cluster host."
      checkmk.general.cluster:
        server_url: "http://my_server/"
        site: "my_site"
        automation_user: "my_user"
        automation_secret: "my_secret"
        name: "my_cluster_host"
        folder: "/"
        nodes: ["cluster_node_1", "cluster_node_2", "cluster_node_3"]
        state: "present"

    # Create a cluster host with IP.
    - name: "Create a cluster host with IP address."
      checkmk.general.cluster:
        server_url: "http://my_server/"
        site: "my_site"
        automation_user: "my_user"
        automation_secret: "my_secret"
        name: "my_cluster_host"
        nodes:
          - "cluster_node_1"
          - "cluster_node_2"
          - "cluster_node_3"
        attributes:
          alias: "My Cluster Host"
          ipaddress: "127.0.0.1"
        folder: "/"
        state: "present"

    # Create a host with update_attributes.
    - name: "Create a host which is monitored on a distinct site."
      checkmk.general.host:
        server_url: "http://my_server/"
        site: "my_site"
        automation_user: "my_user"
        automation_secret: "my_secret"
        name: "my_host"
        update_attributes:
          site: "my_remote_site"
        state: "present"

    # Update only specified attributes
    - name: "Update only specified attributes"
      checkmk.general.host:
        server_url: "http://my_server/"
        site: "my_site"
        automation_user: "my_user"
        automation_secret: "my_secret"
        name: "my_host"
        update_attributes:
          alias: "foo"
        state: "present"

    # Remove specified attributes
    - name: "Remove specified attributes"
      checkmk.general.host:
        server_url: "http://my_server/"
        site: "my_site"
        automation_user: "my_user"
        automation_secret: "my_secret"
        name: "my_host"
        remove_attributes:
          - alias
        state: "present"

    # Add custom tags to a host (note the leading 'tag_')
    - name: "Remove specified attributes"
      checkmk.general.host:
        server_url: "http://my_server/"
        site: "my_site"
        automation_user: "my_user"
        automation_secret: "my_secret"
        name: "my_host"
        update_attributes:
          - tag_my_tag_1: "Bar"
          - tag_my_tag_2: "Foo"
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

      .. _ansible_collections.checkmk.general.host_module__return-message:

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

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`"Host created."`


      .. raw:: html

        </div>



..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- Robin Gierse (@robin-checkmk)
- Lars Getwan (@lgetwan)
- Oliver Gaida (@ogaida)
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



.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: 2.11.0

.. Anchors

.. _ansible_collections.checkmk.general.rule_module:

.. Anchors: short name for ansible.builtin

.. Title

checkmk.general.rule module -- Manage rules in Checkmk.
+++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `checkmk.general collection <https://galaxy.ansible.com/ui/repo/published/checkmk/general/>`_ (version 5.0.0).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible-galaxy collection install checkmk.general`.

    To use it in a playbook, specify: :code:`checkmk.general.rule`.

.. version_added

.. rst-class:: ansible-version-added

New in checkmk.general 0.10.0

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Manage rules within Checkmk. Importing rules from the output of the Checkmk API.
- Make sure these were exported with Checkmk 2.1.0p10 or above. See https://checkmk.com/werk/14670 for more information.


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

      .. _ansible_collections.checkmk.general.rule_module__parameter-automation_secret:

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

      .. _ansible_collections.checkmk.general.rule_module__parameter-automation_user:

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
        <div class="ansibleOptionAnchor" id="parameter-rule"></div>

      .. _ansible_collections.checkmk.general.rule_module__parameter-rule:

      .. rst-class:: ansible-option-title

      **rule**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Definition of the rule as returned by the Checkmk API.


      .. raw:: html

        </div>
    
  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule/conditions"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.checkmk.general.rule_module__parameter-rule/conditions:

      .. rst-class:: ansible-option-title

      **conditions**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule/conditions" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Conditions of the rule.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule/location"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.checkmk.general.rule_module__parameter-rule/location:

      .. rst-class:: ansible-option-title

      **location**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule/location" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Location of the rule within a folder.

      By default rules are created at the bottom of the "/" folder.


      .. raw:: html

        </div>
    
  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule/location/folder"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.rule_module__parameter-rule/location/folder:

      .. rst-class:: ansible-option-title

      **folder**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule/location/folder" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Folder of the rule.

      Required when \ :emphasis:`position`\  is \ :literal:`top`\ , \ :literal:`bottom`\ , or (any).

      Required when \ :emphasis:`state=absent`\ .

      Mutually exclusive with \ :emphasis:`neighbour`\ .


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"/"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule/location/neighbour"></div>
        <div class="ansibleOptionAnchor" id="parameter-rule/location/rule_id"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.rule_module__parameter-rule/location/neighbour:
      .. _ansible_collections.checkmk.general.rule_module__parameter-rule/location/rule_id:

      .. rst-class:: ansible-option-title

      **neighbour**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule/location/neighbour" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-aliases:`aliases: rule_id`

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Put the rule \ :literal:`before`\  or \ :literal:`after`\  this rule\_id.

      Required when \ :emphasis:`position`\  is \ :literal:`before`\  or \ :literal:`after`\ .

      Mutually exclusive with \ :emphasis:`folder`\ .


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule/location/position"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.rule_module__parameter-rule/location/position:

      .. rst-class:: ansible-option-title

      **position**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule/location/position" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Position of the rule in the folder.

      Has no effect when \ :emphasis:`state=absent`\ .

      For new rule \ :literal:`any`\  wil be equivalent to \ :literal:`bottom`\ 


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"top"`
      - :ansible-option-choices-entry:`"bottom"`
      - :ansible-option-choices-entry-default:`"any"` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`"before"`
      - :ansible-option-choices-entry:`"after"`


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule/properties"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.checkmk.general.rule_module__parameter-rule/properties:

      .. rst-class:: ansible-option-title

      **properties**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule/properties" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Properties of the rule.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule/rule_id"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.checkmk.general.rule_module__parameter-rule/rule_id:

      .. rst-class:: ansible-option-title

      **rule_id**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule/rule_id" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      If provided, update/delete an existing rule.

      If omitted, we try to find an equal rule based on \ :literal:`properties`\ , \ :literal:`conditions`\ , \ :literal:`folder`\  and \ :literal:`value\_raw`\ .

      Please mind the additional notes below.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule/value_raw"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.checkmk.general.rule_module__parameter-rule/value_raw:

      .. rst-class:: ansible-option-title

      **value_raw**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule/value_raw" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Rule values as exported from the web interface.

      Required when \ :emphasis:`state`\  is \ :literal:`present`\ .


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ruleset"></div>

      .. _ansible_collections.checkmk.general.rule_module__parameter-ruleset:

      .. rst-class:: ansible-option-title

      **ruleset**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ruleset" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Name of the ruleset to manage.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-server_url"></div>

      .. _ansible_collections.checkmk.general.rule_module__parameter-server_url:

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

      .. _ansible_collections.checkmk.general.rule_module__parameter-site:

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

      .. _ansible_collections.checkmk.general.rule_module__parameter-state:

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

      State of the rule.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`"present"` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`"absent"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-validate_certs"></div>

      .. _ansible_collections.checkmk.general.rule_module__parameter-validate_certs:

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
   - If rule\_id is omitted, due to the internal processing of the \ :literal:`value\_raw`\ , finding the matching rule is not reliable, when \ :literal:`rule\_id`\  is omitted. This sometimes leads to the module not being idempotent or to rules being created over and over again.
   - If rule\_id is provided, for the same reason, it might happen, that tasks changing a rule again and again, even if it already meets the expectations.

.. Seealso


.. Examples

Examples
--------

.. code-block:: yaml+jinja

    
    # Create a rule in checkgroup_parameters:memory_percentage_used
    # at the top of the main folder.
    - name: "Create a rule in checkgroup_parameters:memory_percentage_used."
      checkmk.general.rule:
        server_url: "http://myserver/"
        site: "mysite"
        automation_user: "myuser"
        automation_secret: "mysecret"
        ruleset: "checkgroup_parameters:memory_percentage_used"
        rule:
          conditions: {
            "host_labels": [],
            "host_name": {
              "match_on": [
                "test1.tld"
              ],
              "operator": "one_of"
            },
            "host_tags": [],
            "service_labels": []
          }
          properties: {
            "comment": "Ansible managed",
            "description": "Allow higher memory usage",
            "disabled": false,
            "documentation_url": "https://github.com/Checkmk/ansible-collection-checkmk.general/blob/main/plugins/modules/rule.py"
          }
          value_raw: "{'levels': (80.0, 90.0)}"
          location:
            folder: "/"
            position: "top"
        state: "present"
      register: response

    - name: Show the ID of the new rule
      ansible.builtin.debug:
        msg: "RULE ID : {{ response.content.id }}"

    # Create another rule with the new label conditions (> 2.3.0)
    # in checkgroup_parameters:memory_percentage_used and put it after the rule created above.
    - name: "Create a rule in checkgroup_parameters:memory_percentage_used."
      checkmk.general.rule:
        server_url: "http://myserver/"
        site: "mysite"
        automation_user: "myuser"
        automation_secret: "mysecret"
        ruleset: "checkgroup_parameters:memory_percentage_used"
        rule:
          conditions: {
            "host_label_groups": [
                {
                    operator: "and",
                    label_group: [
                        {
                            operator: "and",
                            label: "cmk/site:beta"
                        },
                        {
                            operator: "or",
                            label: "cmk/os_family:linux"
                        }
                    ],
                },
                {
                    operator: "or",
                    label_group: [
                        {
                            operator: "and",
                            label: "cmk/site:alpha"
                        },
                        {
                            operator: "or",
                            label: "cmk/os_family:windows"
                        }
                    ],
                },
            ],
            "host_name": {
              "match_on": [
                "test2.tld"
              ],
              "operator": "one_of"
            },
            "host_tags": [],
            "service_labels": []
          }
          properties: {
            "comment": "Ansible managed",
            "description": "Allow even higher memory usage",
            "disabled": false,
            "documentation_url": "https://github.com/Checkmk/ansible-collection-checkmk.general/blob/main/plugins/modules/rule.py"
          }
          value_raw: "{'levels': (85.0, 99.0)}"
          location:
            position: "after"
            neighbour: "{{ response.content.id }}"
        state: "present"

    # Delete the first rule.
    - name: "Delete a rule."
      checkmk.general.rule:
        server_url: "http://myserver/"
        site: "mysite"
        automation_user: "myuser"
        automation_secret: "mysecret"
        ruleset: "checkgroup_parameters:memory_percentage_used"
        rule:
          rule_id: "{{ response.content.id }}"
        state: "absent"

    # Create a rule rule matching a host label
    - name: "Create a rule matching a label."
      checkmk.general.rule:
        server_url: "http://myserver/"
        site: "mysite"
        automation_user: "myuser"
        automation_secret: "mysecret"
        ruleset: "checkgroup_parameters:memory_percentage_used"
        rule:
          conditions: {
            "host_labels": [
              {
                "key": "cmk/check_mk_server",
                "operator": "is",
                "value": "yes"
              }
            ],
          }
          properties: {
            "comment": "Ansible managed",
            "description": "Allow higher memory usage",
            "disabled": false,
            "documentation_url": "https://github.com/Checkmk/ansible-collection-checkmk.general/blob/main/plugins/modules/rule.py"
          }
          value_raw: "{'levels': (80.0, 90.0)}"
          location:
            folder: "/"
            position: "top"
        state: "present"

    # Delete all rules in a ruleset that match a certain comment.
    - name: "Delete all rules in a ruleset that match a certain comment."
      checkmk.general.rule:
        server_url: "http://myserver/"
        site: "mysite"
        automation_user: "myuser"
        automation_secret: "mysecret"
        ruleset: "checkgroup_parameters:memory_percentage_used"
        rule:
          rule_id: "{{ item.id }}"
        state: "absent"
      loop: "{{
               lookup('checkmk.general.rules',
                 ruleset='checkgroup_parameters:memory_percentage_used',
                 comment_regex='Ansible managed',
                 server_url=server_url,
                 site=site,
                 automation_user=automation_user,
                 automation_secret=automation_secret,
                 validate_certs=False
                 )
             }}"
      loop_control:
        label: "{{ item.id }}"




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
        <div class="ansibleOptionAnchor" id="return-content"></div>

      .. _ansible_collections.checkmk.general.rule_module__return-content:

      .. rst-class:: ansible-option-title

      **content**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-content" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The complete created/changed rule


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` when the rule is created or when it already exists


      .. raw:: html

        </div>

    
  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-content/extensions"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.checkmk.general.rule_module__return-content/extensions:

      .. rst-class:: ansible-option-title

      **extensions**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-content/extensions" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The attributes of the rule


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` when the rule is created or when it already exists


      .. raw:: html

        </div>

    
  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-content/extensions/conditions"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.rule_module__return-content/extensions/conditions:

      .. rst-class:: ansible-option-title

      **conditions**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-content/extensions/conditions" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The contitions of the rule.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` when the rule is created or when it already exists


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-content/extensions/folder"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.rule_module__return-content/extensions/folder:

      .. rst-class:: ansible-option-title

      **folder**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-content/extensions/folder" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The folder of the rule.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` when the rule is created or when it already exists


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-content/extensions/folder_index"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.rule_module__return-content/extensions/folder_index:

      .. rst-class:: ansible-option-title

      **folder_index**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-content/extensions/folder_index" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The index of the rule inside the folder.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` when the rule is created or when it already exists


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-content/extensions/properties"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.rule_module__return-content/extensions/properties:

      .. rst-class:: ansible-option-title

      **properties**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-content/extensions/properties" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The properties of the rule.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` when the rule is created or when it already exists


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-content/extensions/ruleset"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.rule_module__return-content/extensions/ruleset:

      .. rst-class:: ansible-option-title

      **ruleset**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-content/extensions/ruleset" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The ruleset of the rule.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` when the rule is created or when it already exists


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-content/extensions/value_raw"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.rule_module__return-content/extensions/value_raw:

      .. rst-class:: ansible-option-title

      **value_raw**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-content/extensions/value_raw" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The actual value of the rule


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` when the rule is created or when it already exists


      .. raw:: html

        </div>



  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-content/id"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.checkmk.general.rule_module__return-content/id:

      .. rst-class:: ansible-option-title

      **id**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-content/id" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The ID of the rule.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` when the rule is created or when it already exists

      .. rst-class:: ansible-option-line
      .. rst-class:: ansible-option-sample

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`"1f97bc43-52dc-4f1a-ab7b-c2e9553958ab"`


      .. raw:: html

        </div>



  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-etag"></div>

      .. _ansible_collections.checkmk.general.rule_module__return-etag:

      .. rst-class:: ansible-option-title

      **etag**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-etag" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The etag of the rule.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` when the rule is created or when it already exists

      .. rst-class:: ansible-option-line
      .. rst-class:: ansible-option-sample

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`"\\"ad55730d5488e55e07c58a3da9759fba8cd0b009\\""`


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-http_code"></div>

      .. _ansible_collections.checkmk.general.rule_module__return-http_code:

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

      .. _ansible_collections.checkmk.general.rule_module__return-msg:

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

      The output message that the module generates. Contains the API status details in case of an error.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` always

      .. rst-class:: ansible-option-line
      .. rst-class:: ansible-option-sample

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`"Rule created."`


      .. raw:: html

        </div>



..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- Lars Getwan (@lgetwan)
- diademiemi (@diademiemi)
- Geoffroy Stévenne (@geof77)
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


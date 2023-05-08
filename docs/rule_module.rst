
.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. role:: ansible-attribute-support-label
.. role:: ansible-attribute-support-property
.. role:: ansible-attribute-support-full
.. role:: ansible-attribute-support-partial
.. role:: ansible-attribute-support-none
.. role:: ansible-attribute-support-na
.. role:: ansible-option-type
.. role:: ansible-option-elements
.. role:: ansible-option-required
.. role:: ansible-option-versionadded
.. role:: ansible-option-aliases
.. role:: ansible-option-choices
.. role:: ansible-option-choices-default-mark
.. role:: ansible-option-default-bold
.. role:: ansible-option-configuration
.. role:: ansible-option-returned-bold
.. role:: ansible-option-sample-bold

.. Anchors

.. _ansible_collections.tribe29.checkmk.rule_module:

.. Anchors: short name for ansible.builtin

.. Anchors: aliases



.. Title

tribe29.checkmk.rule module -- Manage rules in Checkmk.
+++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `tribe29.checkmk collection <https://galaxy.ansible.com/tribe29/checkmk>`_ (version 0.21.0).

    To install it, use: :code:`ansible-galaxy collection install tribe29.checkmk`.

    To use it in a playbook, specify: :code:`tribe29.checkmk.rule`.

.. version_added

.. rst-class:: ansible-version-added

New in tribe29.checkmk 0.10.0

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

.. rst-class:: ansible-option-table

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1

  * - Parameter
    - Comments

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-automation_secret"></div>

      .. _ansible_collections.tribe29.checkmk.rule_module__parameter-automation_secret:

      .. rst-class:: ansible-option-title

      **automation_secret**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-automation_secret" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

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

      .. _ansible_collections.tribe29.checkmk.rule_module__parameter-automation_user:

      .. rst-class:: ansible-option-title

      **automation_user**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-automation_user" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

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

      .. _ansible_collections.tribe29.checkmk.rule_module__parameter-rule:

      .. rst-class:: ansible-option-title

      **rule**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

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

      .. _ansible_collections.tribe29.checkmk.rule_module__parameter-rule/conditions:

      .. rst-class:: ansible-option-title

      **conditions**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule/conditions" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Conditions of the rule.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule/folder"></div>

      .. _ansible_collections.tribe29.checkmk.rule_module__parameter-rule/folder:

      .. rst-class:: ansible-option-title

      **folder**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule/folder" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Folder of the rule.

      Deprecated, use \ :emphasis:`location`\  instead.

      Mutually exclusive with \ :emphasis:`location`\ .


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule/location"></div>

      .. _ansible_collections.tribe29.checkmk.rule_module__parameter-rule/location:

      .. rst-class:: ansible-option-title

      **location**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule/location" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Location of the rule within a folder.

      By default rules are created at the bottom of the "/" folder.

      Mutually exclusive with \ :emphasis:`folder`\ .


      .. raw:: html

        </div>
    
  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule/location/folder"></div>

      .. _ansible_collections.tribe29.checkmk.rule_module__parameter-rule/location/folder:

      .. rst-class:: ansible-option-title

      **folder**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule/location/folder" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Folder of the rule.

      Required when \ :emphasis:`position`\  is \ :literal:`top`\  or \ :literal:`bottom`\ .

      Required when \ :emphasis:`state=absent`\ .

      Mutually exclusive with \ :emphasis:`rule\_id`\ .


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"/"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule/location/position"></div>

      .. _ansible_collections.tribe29.checkmk.rule_module__parameter-rule/location/position:

      .. rst-class:: ansible-option-title

      **position**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule/location/position" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Position of the rule in the folder.

      Has no effect when \ :emphasis:`state=absent`\ .


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"top"`
      - :ansible-option-choices-entry-default:`"bottom"` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`"before"`
      - :ansible-option-choices-entry:`"after"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule/location/rule_id"></div>

      .. _ansible_collections.tribe29.checkmk.rule_module__parameter-rule/location/rule_id:

      .. rst-class:: ansible-option-title

      **rule_id**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule/location/rule_id" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Put the rule \ :literal:`before`\  or \ :literal:`after`\  this rule\_id.

      Required when \ :emphasis:`position`\  is \ :literal:`before`\  or \ :literal:`after`\ .

      Mutually exclusive with \ :emphasis:`folder`\ .


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule/properties"></div>

      .. _ansible_collections.tribe29.checkmk.rule_module__parameter-rule/properties:

      .. rst-class:: ansible-option-title

      **properties**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule/properties" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Properties of the rule.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rule/value_raw"></div>

      .. _ansible_collections.tribe29.checkmk.rule_module__parameter-rule/value_raw:

      .. rst-class:: ansible-option-title

      **value_raw**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rule/value_raw" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Rule values as exported from the web interface.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ruleset"></div>

      .. _ansible_collections.tribe29.checkmk.rule_module__parameter-ruleset:

      .. rst-class:: ansible-option-title

      **ruleset**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ruleset" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

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

      .. _ansible_collections.tribe29.checkmk.rule_module__parameter-server_url:

      .. rst-class:: ansible-option-title

      **server_url**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-server_url" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The base url of your Checkmk server.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site"></div>

      .. _ansible_collections.tribe29.checkmk.rule_module__parameter-site:

      .. rst-class:: ansible-option-title

      **site**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

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

      .. _ansible_collections.tribe29.checkmk.rule_module__parameter-state:

      .. rst-class:: ansible-option-title

      **state**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-state" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

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

      .. _ansible_collections.tribe29.checkmk.rule_module__parameter-validate_certs:

      .. rst-class:: ansible-option-title

      **validate_certs**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-validate_certs" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

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
   - To achieve idempotency, this module is comparing the specified rule with the already existing rules based on conditions, folder, value\_raw and enabled/disabled.

.. Seealso


.. Examples

Examples
--------

.. code-block:: yaml+jinja

    
    # Create a rule in checkgroup_parameters:memory_percentage_used
    # at the top of the main folder.
    - name: "Create a rule in checkgroup_parameters:memory_percentage_used."
      tribe29.checkmk.rule:
        server_url: "http://localhost/"
        site: "my_site"
        automation_user: "automation"
        automation_secret: "$SECRET"
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
                "comment": "Warning at 80%\nCritical at 90%\n",
                "description": "Allow higher memory usage",
                "disabled": false,
                "documentation_url": "https://github.com/Checkmk/ansible-collection-tribe29.checkmk/blob/main/plugins/modules/rules.py"
            }
            folder: "/"
            value_raw: "{'levels': (80.0, 90.0)}"
            location:
                folder: "/"
                position: "top"
        state: "present"
        register: response

    - name: Show the ID of the new rule
      debug:
        msg: "RULE ID : {{ response.id }}"

    # Create another rule in checkgroup_parameters:memory_percentage_used
    # and put it after the rule created above.
    - name: "Create a rule in checkgroup_parameters:memory_percentage_used."
      tribe29.checkmk.rule:
        server_url: "http://localhost/"
        site: "my_site"
        automation_user: "automation"
        automation_secret: "$SECRET"
        ruleset: "checkgroup_parameters:memory_percentage_used"
        rule:
            conditions: {
                "host_labels": [],
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
                "comment": "Warning at 85%\nCritical at 99%\n",
                "description": "Allow even higher memory usage",
                "disabled": false,
                "documentation_url": "https://github.com/Checkmk/ansible-collection-tribe29.checkmk/blob/main/plugins/modules/rules.py"
            }
            value_raw: "{'levels': (85.0, 99.0)}"
            location:
                position: "after"
                rule_id: "{{ response.id }}"
        state: "present"

    # Delete the first rule.
    - name: "Delete a rule."
      tribe29.checkmk.rule:
        server_url: "http://localhost/"
        site: "my_site"
        automation_user: "automation"
        automation_secret: "$SECRET"
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
                "comment": "Warning at 80%\nCritical at 90%\n",
                "description": "Allow higher memory usage",
                "disabled": false,
                "documentation_url": "https://github.com/Checkmk/ansible-collection-tribe29.checkmk/blob/main/plugins/modules/rules.py"
            }
            value_raw: "{'levels': (80.0, 90.0)}"
        state: "absent"




.. Facts


.. Return values

Return Values
-------------
Common return values are documented :ref:`here <common_return_values>`, the following are the fields unique to this module:

.. rst-class:: ansible-option-table

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1

  * - Key
    - Description

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-id"></div>

      .. _ansible_collections.tribe29.checkmk.rule_module__return-id:

      .. rst-class:: ansible-option-title

      **id**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-id" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

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
        <div class="ansibleOptionAnchor" id="return-msg"></div>

      .. _ansible_collections.tribe29.checkmk.rule_module__return-msg:

      .. rst-class:: ansible-option-title

      **msg**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-msg" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

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

- diademiemi (@diademiemi)
- Geoffroy Stévenne (@geof77)



.. Extra links

Collection links
~~~~~~~~~~~~~~~~

.. raw:: html

  <p class="ansible-links">
    <a href="https://github.com/Checkmk/ansible-collection-tribe29.checkmk/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc" aria-role="button" target="_blank" rel="noopener external">Issue Tracker</a>
    <a href="https://github.com/Checkmk/ansible-collection-tribe29.checkmk" aria-role="button" target="_blank" rel="noopener external">Repository (Sources)</a>
  </p>

.. Parsing errors


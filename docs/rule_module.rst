.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: 2.27.0

.. Anchors

.. _ansible_collections.checkmk.general.rule_module:

.. Anchors: short name for ansible.builtin

.. Title

checkmk.general.rule module -- Manage rules in Checkmk
++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `checkmk.general collection <https://galaxy.ansible.com/ui/repo/published/checkmk/general/>`_ (version 8.5.0).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible\-galaxy collection install checkmk.general`.

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
        <div class="ansibleOptionAnchor" id="parameter-api_auth_cookie"></div>

      .. _ansible_collections.checkmk.general.rule_module__parameter-api_auth_cookie:

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

      .. _ansible_collections.checkmk.general.rule_module__parameter-api_auth_type:

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

      .. _ansible_collections.checkmk.general.rule_module__parameter-api_secret:
      .. _ansible_collections.checkmk.general.rule_module__parameter-automation_secret:

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

      .. _ansible_collections.checkmk.general.rule_module__parameter-api_user:
      .. _ansible_collections.checkmk.general.rule_module__parameter-automation_user:

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

      .. _ansible_collections.checkmk.general.rule_module__parameter-client_cert:

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

      .. _ansible_collections.checkmk.general.rule_module__parameter-client_key:

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

      Required when :emphasis:`position` is :literal:`top`\ , :literal:`bottom`\ , or (any).

      Required when :emphasis:`state=absent`.

      Mutually exclusive with :emphasis:`neighbour`.


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

      Put the rule :literal:`before` or :literal:`after` this rule\_id.

      Required when :emphasis:`position` is :literal:`before` or :literal:`after`.

      Mutually exclusive with :emphasis:`folder`.


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

      Has no effect when :emphasis:`state=absent`.

      For a new rule :literal:`any` will be equivalent to :literal:`bottom`.


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

      If omitted, we try to find an equal rule based on :literal:`properties`\ , :literal:`conditions`\ , :literal:`folder` and :literal:`value\_raw`.

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

      Required when :emphasis:`state` is :literal:`present`.


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

      The base url of your Checkmk server including the protocol but excluding the site. If not set the module will fall back to the environment variable :literal:`CHECKMK\_VAR\_SERVER\_URL`.


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

      The site you want to connect to. This will be appended to the server\_url as part of the API request url. If not set the module will fall back to the environment variable :literal:`CHECKMK\_VAR\_SITE`.


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
   - Provide :literal:`value\_raw` in the canonical format of the target Checkmk version, for example by copying it from the GUI (Export rule for API) or from the output of an existing rule. Value formats can change between Checkmk versions, so playbooks may need updating after a Checkmk upgrade.
   - The Checkmk API masks secrets in its responses. Rules that contain an explicit password in :literal:`value\_raw` can therefore never be compared with the desired state. They report a change on every run when :literal:`rule\_id` is provided, and create another rule on every run when it is omitted. Reference an entry of the Checkmk password store instead, which can be managed with the :ref:`checkmk.general.password <ansible_collections.checkmk.general.password_module>` module. This is the only supported way to manage rules containing secrets with this module.
   - Write the password store reference exactly as the target Checkmk site returns it, because its representation depends on the Checkmk version and on the ruleset. Rulesets using the modern rule specs return for example :literal:`('cmk\_postprocessed', 'stored\_password', ('my\_password', ''`\ )) on Checkmk 2.3 and 2.4, and :literal:`('cmk\_postprocessed', 'stored\_password', ('my\_password', '\*\*\*\*\*\*'`\ )) on Checkmk 2.5, while rulesets still using the legacy valuespecs return :literal:`('store', 'my\_password'`\ ). The last element of such a reference is not evaluated for password store entries, so the masked value can be used as it is returned.
   - The positions :literal:`top`\ , :literal:`bottom`\ , :literal:`before` and :literal:`after` describe the rule order at the time the task runs. Rules created later, including by subsequent tasks or in the GUI, can displace such rules, so the next run detects a location change and moves the rule back.
   - :literal:`position=any` accepts any position within the folder and is thus the only position that is idempotent on its own. Do not use it for rulesets that are evaluated in first match order, because the rule which takes effect would then depend on an arbitrary position. Order the rules of such a ruleset explicitly, as shown in the examples, anchoring the first rule and chaining the following ones behind their predecessor with :literal:`position=after` and :literal:`neighbour`. Once established, such a chain is idempotent, and it restores the intended order if rules are inserted in between.

.. Seealso

See Also
--------

.. seealso::

   :ref:`checkmk.general.rule <ansible_collections.checkmk.general.rule_lookup>` lookup plugin
       Show a rule.
   :ref:`checkmk.general.rules <ansible_collections.checkmk.general.rules_lookup>` lookup plugin
       Get a list rules.
   :ref:`checkmk.general.ruleset <ansible_collections.checkmk.general.ruleset_lookup>` lookup plugin
       Show a ruleset.
   :ref:`checkmk.general.rulesets <ansible_collections.checkmk.general.rulesets_lookup>` lookup plugin
       Search rulesets.

.. Examples

Examples
--------

.. code-block:: yaml+jinja

    # ---------------------------------------------------------------------------
    # Create and delete rules
    # ---------------------------------------------------------------------------

    - name: "Create a rule at the top of the main folder."
      checkmk.general.rule:
        server_url: "https://myserver"
        site: "mysite"
        api_user: "myuser"
        api_secret: "mysecret"
        ruleset: "checkgroup_parameters:filesystem"
        rule:
          conditions:
            host_name:
              match_on:
                - "myhost01"
              operator: "one_of"
            host_tags: []
            host_labels: []
            service_labels: []
          properties:
            description: "Allow higher filesystem usage on myhost01"
            comment: "Managed by Ansible"
            disabled: false
          value_raw: "{'levels': (80.0, 90.0)}"
          location:
            folder: "/"
            position: "top"
        state: "present"
      register: rule_result

    - name: "Show the ID of the new rule."
      ansible.builtin.debug:
        msg: "Rule ID: {{ rule_result.content.id }}"

    - name: "Delete a rule by ID."
      checkmk.general.rule:
        server_url: "https://myserver"
        site: "mysite"
        api_user: "myuser"
        api_secret: "mysecret"
        ruleset: "checkgroup_parameters:filesystem"
        rule:
          rule_id: "{{ rule_result.content.id }}"
        state: "absent"

    # ---------------------------------------------------------------------------
    # Rule placement
    # ---------------------------------------------------------------------------

    - name: "Create a rule and place it after an existing rule."
      checkmk.general.rule:
        server_url: "https://myserver"
        site: "mysite"
        api_user: "myuser"
        api_secret: "mysecret"
        ruleset: "checkgroup_parameters:filesystem"
        rule:
          conditions:
            host_name:
              match_on:
                - "myhost02"
              operator: "one_of"
            host_tags: []
            host_labels: []
            service_labels: []
          properties:
            description: "Allow even higher filesystem usage on myhost02"
            comment: "Managed by Ansible"
            disabled: false
          value_raw: "{'levels': (85.0, 99.0)}"
          location:
            position: "after"
            neighbour: "{{ rule_result.content.id }}"
        state: "present"

    # ---------------------------------------------------------------------------
    # Rules with label conditions (Checkmk >= 2.3.0)
    # ---------------------------------------------------------------------------

    - name: "Create a rule matching a host label."
      checkmk.general.rule:
        server_url: "https://myserver"
        site: "mysite"
        api_user: "myuser"
        api_secret: "mysecret"
        ruleset: "checkgroup_parameters:filesystem"
        rule:
          conditions:
            host_labels:
              - key: "cmk/check_mk_server"
                operator: "is"
                value: "yes"
          properties:
            description: "Allow higher filesystem usage on Checkmk servers"
            comment: "Managed by Ansible"
            disabled: false
          value_raw: "{'levels': (80.0, 90.0)}"
          location:
            folder: "/"
            position: "top"
        state: "present"

    - name: "Create a rule with combined label group conditions (Checkmk >= 2.3.0)."
      checkmk.general.rule:
        server_url: "https://myserver"
        site: "mysite"
        api_user: "myuser"
        api_secret: "mysecret"
        ruleset: "checkgroup_parameters:filesystem"
        rule:
          conditions:
            host_label_groups:
              - operator: "and"
                label_group:
                  - operator: "and"
                    label: "cmk/site:mysite"
                  - operator: "or"
                    label: "cmk/os_family:linux"
            host_tags: []
            service_label_groups: []
          properties:
            description: "Allow higher filesystem usage on Linux hosts in mysite"
            comment: "Managed by Ansible"
            disabled: false
          value_raw: "{'levels': (80.0, 90.0)}"
          location:
            folder: "/"
            position: "bottom"
        state: "present"

    # ---------------------------------------------------------------------------
    # Ordered rules in a ruleset that is evaluated in first match order
    # ---------------------------------------------------------------------------
    # Anchor the first rule of the chain, then chain every following rule behind
    # its predecessor. The relative order of the rules is then guaranteed and
    # idempotent, regardless of other rules in the same folder.

    - name: "Create the more specific rule first."
      checkmk.general.rule:
        server_url: "https://myserver"
        site: "mysite"
        api_user: "myuser"
        api_secret: "mysecret"
        ruleset: "checkgroup_parameters:filesystem"
        rule:
          conditions:
            host_labels:
              - key: "role"
                operator: "is"
                value: "database"
          properties:
            description: "Filesystem levels for database servers"
            comment: "Managed by Ansible"
          value_raw: "{'levels': (95.0, 98.0)}"
          location:
            folder: "/"
            position: "any"
        state: "present"
      register: database_rule

    - name: "Create the general rule directly after the specific one."
      checkmk.general.rule:
        server_url: "https://myserver"
        site: "mysite"
        api_user: "myuser"
        api_secret: "mysecret"
        ruleset: "checkgroup_parameters:filesystem"
        rule:
          properties:
            description: "Filesystem levels for all other hosts"
            comment: "Managed by Ansible"
          value_raw: "{'levels': (80.0, 90.0)}"
          location:
            position: "after"
            neighbour: "{{ database_rule.content.id }}"
        state: "present"

    # ---------------------------------------------------------------------------
    # Bulk delete rules using a lookup
    # ---------------------------------------------------------------------------

    - name: "Delete all rules in a ruleset that match a certain comment."
      checkmk.general.rule:
        server_url: "https://myserver"
        site: "mysite"
        api_user: "myuser"
        api_secret: "mysecret"
        ruleset: "checkgroup_parameters:filesystem"
        rule:
          rule_id: "{{ item.id }}"
        state: "absent"
      loop: "{{
               lookup('checkmk.general.rules',
                 ruleset='checkgroup_parameters:filesystem',
                 comment_regex='Managed by Ansible',
                 server_url='https://myserver',
                 site='mysite',
                 api_user='myuser',
                 api_secret='mysecret',
                 )
             }}"
      loop_control:
        label: "{{ item.id }}"

    # ---------------------------------------------------------------------------
    # Using environment variables for authentication
    # ---------------------------------------------------------------------------
    # Connection parameters can be provided via environment variables instead of
    # task parameters. The supported variables are:
    #   CHECKMK_VAR_SERVER_URL, CHECKMK_VAR_SITE,
    #   CHECKMK_VAR_API_USER, CHECKMK_VAR_API_SECRET,
    #   CHECKMK_VAR_VALIDATE_CERTS

    - name: "Create a rule using environment variables for authentication."
      checkmk.general.rule:
        ruleset: "checkgroup_parameters:filesystem"
        rule:
          properties:
            description: "Allow higher filesystem usage"
            comment: "Managed by Ansible"
            disabled: false
          value_raw: "{'levels': (80.0, 90.0)}"
          location:
            folder: "/"
            position: "bottom"
        state: "present"
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

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`"1f97bc43\-52dc\-4f1a\-ab7b\-c2e9553958ab"`


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

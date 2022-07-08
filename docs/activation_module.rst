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
.. role:: ansible-option-choices-entry
.. role:: ansible-option-default
.. role:: ansible-option-default-bold
.. role:: ansible-option-configuration
.. role:: ansible-option-returned-bold
.. role:: ansible-option-sample-bold

.. Anchors

.. _ansible_collections.tribe29.checkmk.activation_module:

.. Anchors: short name for ansible.builtin

.. Anchors: aliases



.. Title

tribe29.checkmk.activation module -- Activate changes in Checkmk.
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `tribe29.checkmk collection <https://galaxy.ansible.com/tribe29/checkmk>`_ (version 0.5.0).

    You might already have this collection installed if you are using the ``ansible`` package.
    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible-galaxy collection install tribe29.checkmk`.

    To use it in a playbook, specify: :code:`tribe29.checkmk.activation`.

.. version_added

.. versionadded:: 0.0.1 of tribe29.checkmk

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Activate changes within Checkmk.
- This module only needs to be run once and not for every host. Use \ :literal:`run\_once`\ .


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

      .. _ansible_collections.tribe29.checkmk.activation_module__parameter-automation_secret:

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

      .. _ansible_collections.tribe29.checkmk.activation_module__parameter-automation_user:

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
        <div class="ansibleOptionAnchor" id="parameter-force_foreign_changes"></div>

      .. _ansible_collections.tribe29.checkmk.activation_module__parameter-force_foreign_changes:

      .. rst-class:: ansible-option-title

      **force_foreign_changes**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-force_foreign_changes" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Wheather to active foreign changes.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-default-bold:`no` :ansible-option-default:`← (default)`
      - :ansible-option-choices-entry:`yes`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-server_url"></div>

      .. _ansible_collections.tribe29.checkmk.activation_module__parameter-server_url:

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

      .. _ansible_collections.tribe29.checkmk.activation_module__parameter-site:

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
        <div class="ansibleOptionAnchor" id="parameter-sites"></div>

      .. _ansible_collections.tribe29.checkmk.activation_module__parameter-sites:

      .. rst-class:: ansible-option-title

      **sites**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-sites" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`any`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The sites that should be activated. Omitting this option activates all sites.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`[]`

      .. raw:: html

        </div>


.. Attributes


.. Notes


.. Seealso


.. Examples

Examples
--------

.. code-block:: yaml+jinja

    
    - name: "Activate changes on all sites."
      tribe29.checkmk.activation:
          server_url: "http://localhost/"
          site: "my_site"
          automation_user: "automation"
          automation_secret: "$SECRET"
      run_once: 'true'

    - name: "Activate changes on a specific site."
      tribe29.checkmk.activation:
          server_url: "http://localhost/"
          site: "my_site"
          automation_user: "automation"
          automation_secret: "$SECRET"
          sites:
            - "my_site"
      run_once: 'true'

    - name: "Activate changes including foreign changes."
      tribe29.checkmk.activation:
          server_url: "http://localhost/"
          site: "my_site"
          automation_user: "automation"
          automation_secret: "$SECRET"
          force_foreign_changes: 'true'
      run_once: 'true'




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
        <div class="ansibleOptionAnchor" id="return-http_code"></div>

      .. _ansible_collections.tribe29.checkmk.activation_module__return-http_code:

      .. rst-class:: ansible-option-title

      **http_code**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-http_code" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

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

      :ansible-option-sample-bold:`Sample:` "200"


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-message"></div>

      .. _ansible_collections.tribe29.checkmk.activation_module__return-message:

      .. rst-class:: ansible-option-title

      **message**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-message" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The output message that the module generates.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` always

      .. rst-class:: ansible-option-line
      .. rst-class:: ansible-option-sample

      :ansible-option-sample-bold:`Sample:` "Changes activated."


      .. raw:: html

        </div>



..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- Robin Gierse (@robin-tribe29)



.. Extra links

Collection links
~~~~~~~~~~~~~~~~

.. raw:: html

  <p class="ansible-links">
    <a href="https://github.com/tribe29/ansible-collection-tribe29.checkmk/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc" aria-role="button" target="_blank" rel="noopener external">Issue Tracker</a>
    <a href="https://github.com/tribe29/ansible-collection-tribe29.checkmk" aria-role="button" target="_blank" rel="noopener external">Repository (Sources)</a>
  </p>

.. Parsing errors


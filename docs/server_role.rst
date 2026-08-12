.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: 2.24.0

.. Anchors

.. _ansible_collections.checkmk.general.server_role:

.. Title

checkmk.general.server role -- Install and manage Checkmk servers
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This role is part of the `checkmk.general collection <https://galaxy.ansible.com/ui/repo/published/checkmk/general/>`_ (version 8.3.0).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it use: :code:`ansible\-galaxy collection install checkmk.general`.

    To use it in a playbook, specify: :code:`checkmk.general.server`.

.. contents::
   :local:
   :depth: 2

.. _ansible_collections.checkmk.general.server_role__entrypoint-main:

.. Entry point title

Entry point ``main`` -- Install and manage Checkmk servers
----------------------------------------------------------

.. version_added


.. Deprecated


Synopsis
^^^^^^^^

.. Description

- This role installs Checkmk on servers and manages sites.

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
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_server_allow_downgrades"></div>

      .. _ansible_collections.checkmk.general.server_role__parameter-main__checkmk_server_allow_downgrades:

      .. rst-class:: ansible-option-title

      **checkmk_server_allow_downgrades**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_server_allow_downgrades" title="Permalink to this option"></a>

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
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_server_backup_dir"></div>

      .. _ansible_collections.checkmk.general.server_role__parameter-main__checkmk_server_backup_dir:

      .. rst-class:: ansible-option-title

      **checkmk_server_backup_dir**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_server_backup_dir" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Refer to the README for details.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"/tmp"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_server_backup_on_update"></div>

      .. _ansible_collections.checkmk.general.server_role__parameter-main__checkmk_server_backup_on_update:

      .. rst-class:: ansible-option-title

      **checkmk_server_backup_on_update**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_server_backup_on_update" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Refer to the README for details. Not recommended to disable this option!


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry-default:`true` :ansible-option-choices-default-mark:`← (default)`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_server_backup_opts"></div>

      .. _ansible_collections.checkmk.general.server_role__parameter-main__checkmk_server_backup_opts:

      .. rst-class:: ansible-option-title

      **checkmk_server_backup_opts**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_server_backup_opts" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Refer to the README for details.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"\-\-no\-past"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_server_cleanup"></div>

      .. _ansible_collections.checkmk.general.server_role__parameter-main__checkmk_server_cleanup:

      .. rst-class:: ansible-option-title

      **checkmk_server_cleanup**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_server_cleanup" title="Permalink to this option"></a>

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
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_server_configure_firewall"></div>

      .. _ansible_collections.checkmk.general.server_role__parameter-main__checkmk_server_configure_firewall:

      .. rst-class:: ansible-option-title

      **checkmk_server_configure_firewall**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_server_configure_firewall" title="Permalink to this option"></a>

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
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_server_delegate_download"></div>

      .. _ansible_collections.checkmk.general.server_role__parameter-main__checkmk_server_delegate_download:

      .. rst-class:: ansible-option-title

      **checkmk_server_delegate_download**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_server_delegate_download" title="Permalink to this option"></a>

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
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_server_download_pass"></div>

      .. _ansible_collections.checkmk.general.server_role__parameter-main__checkmk_server_download_pass:

      .. rst-class:: ansible-option-title

      **checkmk_server_download_pass**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_server_download_pass" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Refer to the README for details.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_server_download_proxy"></div>

      .. _ansible_collections.checkmk.general.server_role__parameter-main__checkmk_server_download_proxy:

      .. rst-class:: ansible-option-title

      **checkmk_server_download_proxy**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_server_download_proxy" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Refer to the README for details.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_server_download_user"></div>

      .. _ansible_collections.checkmk.general.server_role__parameter-main__checkmk_server_download_user:

      .. rst-class:: ansible-option-title

      **checkmk_server_download_user**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_server_download_user" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Refer to the README for details.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_server_edition"></div>

      .. _ansible_collections.checkmk.general.server_role__parameter-main__checkmk_server_edition:

      .. rst-class:: ansible-option-title

      **checkmk_server_edition**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_server_edition" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Refer to the README for details.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"community"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_server_epel_gpg_check"></div>

      .. _ansible_collections.checkmk.general.server_role__parameter-main__checkmk_server_epel_gpg_check:

      .. rst-class:: ansible-option-title

      **checkmk_server_epel_gpg_check**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_server_epel_gpg_check" title="Permalink to this option"></a>

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
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_server_gpg_delegate_download"></div>

      .. _ansible_collections.checkmk.general.server_role__parameter-main__checkmk_server_gpg_delegate_download:

      .. rst-class:: ansible-option-title

      **checkmk_server_gpg_delegate_download**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_server_gpg_delegate_download" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Refer to the README for details.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"{{ checkmk\_server\_delegate\_download }}"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_server_gpg_download_pass"></div>

      .. _ansible_collections.checkmk.general.server_role__parameter-main__checkmk_server_gpg_download_pass:

      .. rst-class:: ansible-option-title

      **checkmk_server_gpg_download_pass**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_server_gpg_download_pass" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Refer to the README for details.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_server_gpg_download_proxy"></div>

      .. _ansible_collections.checkmk.general.server_role__parameter-main__checkmk_server_gpg_download_proxy:

      .. rst-class:: ansible-option-title

      **checkmk_server_gpg_download_proxy**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_server_gpg_download_proxy" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Refer to the README for details.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"{{ checkmk\_server\_download\_proxy }}"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_server_gpg_download_user"></div>

      .. _ansible_collections.checkmk.general.server_role__parameter-main__checkmk_server_gpg_download_user:

      .. rst-class:: ansible-option-title

      **checkmk_server_gpg_download_user**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_server_gpg_download_user" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Refer to the README for details.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_server_no_log"></div>

      .. _ansible_collections.checkmk.general.server_role__parameter-main__checkmk_server_no_log:

      .. rst-class:: ansible-option-title

      **checkmk_server_no_log**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_server_no_log" title="Permalink to this option"></a>

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
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_server_ports"></div>

      .. _ansible_collections.checkmk.general.server_role__parameter-main__checkmk_server_ports:

      .. rst-class:: ansible-option-title

      **checkmk_server_ports**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_server_ports" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=integer`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Refer to the README for details.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`[22, 80, 443, 8000]`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_server_sites"></div>

      .. _ansible_collections.checkmk.general.server_role__parameter-main__checkmk_server_sites:

      .. rst-class:: ansible-option-title

      **checkmk_server_sites**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_server_sites" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=dictionary`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Refer to the README for details.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_server_sites/admin_pw"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.checkmk.general.server_role__parameter-main__checkmk_server_sites/admin_pw:

      .. rst-class:: ansible-option-title

      **admin_pw**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_server_sites/admin_pw" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The initial password for the cmkadmin user.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_server_sites/edition"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.checkmk.general.server_role__parameter-main__checkmk_server_sites/edition:

      .. rst-class:: ansible-option-title

      **edition**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_server_sites/edition" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The edition of the site.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_server_sites/gid"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.checkmk.general.server_role__parameter-main__checkmk_server_sites/gid:

      .. rst-class:: ansible-option-title

      **gid**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_server_sites/gid" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`integer`




      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The GID of the OMD site group


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_server_sites/mkp_packages"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.checkmk.general.server_role__parameter-main__checkmk_server_sites/mkp_packages:

      .. rst-class:: ansible-option-title

      **mkp_packages**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_server_sites/mkp_packages" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=dictionary`




      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_server_sites/mkp_packages/checksum"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.server_role__parameter-main__checkmk_server_sites/mkp_packages/checksum:

      .. rst-class:: ansible-option-title

      **checksum**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_server_sites/mkp_packages/checksum" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The checksum of the extension package.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_server_sites/mkp_packages/enabled"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.server_role__parameter-main__checkmk_server_sites/mkp_packages/enabled:

      .. rst-class:: ansible-option-title

      **enabled**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_server_sites/mkp_packages/enabled" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`




      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Enable the extension package.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_server_sites/mkp_packages/installed"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.server_role__parameter-main__checkmk_server_sites/mkp_packages/installed:

      .. rst-class:: ansible-option-title

      **installed**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_server_sites/mkp_packages/installed" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`




      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Install the extension package.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_server_sites/mkp_packages/name"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.server_role__parameter-main__checkmk_server_sites/mkp_packages/name:

      .. rst-class:: ansible-option-title

      **name**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_server_sites/mkp_packages/name" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`




      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The name of the extension package.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_server_sites/mkp_packages/src"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.server_role__parameter-main__checkmk_server_sites/mkp_packages/src:

      .. rst-class:: ansible-option-title

      **src**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_server_sites/mkp_packages/src" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The path to the the extension package.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_server_sites/mkp_packages/url"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.server_role__parameter-main__checkmk_server_sites/mkp_packages/url:

      .. rst-class:: ansible-option-title

      **url**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_server_sites/mkp_packages/url" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The URL to download the extension package from.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_server_sites/mkp_packages/version"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.server_role__parameter-main__checkmk_server_sites/mkp_packages/version:

      .. rst-class:: ansible-option-title

      **version**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_server_sites/mkp_packages/version" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The version of the extension package.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_server_sites/name"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.checkmk.general.server_role__parameter-main__checkmk_server_sites/name:

      .. rst-class:: ansible-option-title

      **name**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_server_sites/name" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`




      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The name of the site.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_server_sites/omd_auto_restart"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.checkmk.general.server_role__parameter-main__checkmk_server_sites/omd_auto_restart:

      .. rst-class:: ansible-option-title

      **omd_auto_restart**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_server_sites/omd_auto_restart" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`




      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Whether to automatically restart a site for configuration.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_server_sites/omd_config"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.checkmk.general.server_role__parameter-main__checkmk_server_sites/omd_config:

      .. rst-class:: ansible-option-title

      **omd_config**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_server_sites/omd_config" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=dictionary`




      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_server_sites/omd_config/value"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.server_role__parameter-main__checkmk_server_sites/omd_config/value:

      .. rst-class:: ansible-option-title

      **value**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_server_sites/omd_config/value" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The value of the variable.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_server_sites/omd_config/var"></div>

      .. raw:: latex

        \hspace{0.04\textwidth}\begin{minipage}[t]{0.28\textwidth}

      .. _ansible_collections.checkmk.general.server_role__parameter-main__checkmk_server_sites/omd_config/var:

      .. rst-class:: ansible-option-title

      **var**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_server_sites/omd_config/var" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The name of the OMD configuration variable.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_server_sites/state"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.checkmk.general.server_role__parameter-main__checkmk_server_sites/state:

      .. rst-class:: ansible-option-title

      **state**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_server_sites/state" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`




      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The desired target state for the site.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_server_sites/uid"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.checkmk.general.server_role__parameter-main__checkmk_server_sites/uid:

      .. rst-class:: ansible-option-title

      **uid**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_server_sites/uid" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`integer`




      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The UID of the OMD site user


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_server_sites/update_conflict_resolution"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.checkmk.general.server_role__parameter-main__checkmk_server_sites/update_conflict_resolution:

      .. rst-class:: ansible-option-title

      **update_conflict_resolution**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_server_sites/update_conflict_resolution" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      How to handle file conflicts during updates.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_server_sites/version"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.checkmk.general.server_role__parameter-main__checkmk_server_sites/version:

      .. rst-class:: ansible-option-title

      **version**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_server_sites/version" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`




      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The version of the site.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_server_verify_setup"></div>

      .. _ansible_collections.checkmk.general.server_role__parameter-main__checkmk_server_verify_setup:

      .. rst-class:: ansible-option-title

      **checkmk_server_verify_setup**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_server_verify_setup" title="Permalink to this option"></a>

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
        <div class="ansibleOptionAnchor" id="parameter-main--checkmk_server_version"></div>

      .. _ansible_collections.checkmk.general.server_role__parameter-main__checkmk_server_version:

      .. rst-class:: ansible-option-title

      **checkmk_server_version**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--checkmk_server_version" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Refer to the README for details.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"2.5.0p10"`

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

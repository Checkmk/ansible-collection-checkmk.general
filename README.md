# <img src="https://checkmk.com/favicon.ico" alt="drawing" height="25"/> Checkmk Ansible Collection

Checkmk already provides the needed APIs to automate and configure your monitoring.
With this project we want to augment the experience and provide easy to use
modules and roles for Ansible to both simplify your first steps with automating
Checkmk and keep your daily operations smooth and efficient.

## :dragon_face: Here be dragons!

This collection is provided AS IS and there is **no commercial support whatsoever.**

This is an open source endeavour, on which we collaborate with the community. All fixes and support are provided by individuals in their spare time. Please keep that in mind, when using the collection and interacting with this repository.

## :wrench: Installing this collection

Please refer to [INSTALL.md](INSTALL.md) for detailed installation instructions.

## :construction_worker: Using this collection

We encourage you - in accordance with Ansible Best Practices -
to always use FQCNs (Fully Qualified Collection Names) as seen below.
This ensures, that you always know, which module is at play.

Please keep in mind the parameters `server_url` and `site` are concatenated to form the base URL of the Checkmk site.

```yaml
---
- hosts: all

  tasks:
    - name: "Run activation."
      checkmk.general.activation:
        server_url: "http://myserver/"
        site: "mysite"
        automation_user: "myuser"
        automation_secret: "mysecret"
        force_foreign_changes: 'true'
        sites:
          - "mysite"
```

## :electric_plug: Dependencies

 - [ansible.posix](https://github.com/ansible-collections/ansible.posix)
 - [ansible.utils](https://github.com/ansible-collections/ansible.utils)
 - [ansible.windows](https://github.com/ansible-collections/ansible.windows)
 - [community.general](https://github.com/ansible-collections/community.general)

Although the Ansible project notes, that collections should have no or very little dependencies, we want to make sure the  collection works for you out-of-the-box. Currently we only depend on very basic collections, which are most likely already installed in your environment. For version constraints, see [galaxy.yml](galaxy.yml).

## :bulb: Getting help

For documentation on the [included modules](#modules), head over to [the Galaxy](https://galaxy.ansible.com/ui/repo/published/checkmk/general/docs/),
or run the following command substituting the `$MODULE_NAME`:

    ansible-doc checkmk.general.$MODULE_NAME

For any form of support queries or requests refer to [SUPPORT.md](SUPPORT.md).

## :toolbox: Included content

You can find playbooks, demonstrating the content of this collection in the folder [playbooks/demo/](playbooks/demo/).

[![Ansible Sanity Tests](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ansible-sanity-tests.yaml/badge.svg)](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ansible-sanity-tests.yaml)

### :inbox_tray: Inventory plugins

Name | Description | Tests
--- | --- | ---
[checkmk.general.checkmk](https://github.com/Checkmk/ansible-collection-checkmk.general/blob/main/plugins/inventory/checkmk.py)|Dynamic Inventory Source for Checkmk. | [![Ansible Unit Test for Inventory Module.](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-unit-test-inventory.yaml/badge.svg)](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-unit-test-inventory.yaml)

### :mag: Lookup plugins
Click on the lookup plugin name below, to get detailed documentation about it.
For more in-depth documentation, see [this README](https://github.com/Checkmk/ansible-collection-checkmk.general/blob/main/plugins/lookup/README.md).

Name | Description | Tests
--- | --- | ---
[checkmk.general.bakery](https://github.com/Checkmk/ansible-collection-checkmk.general/blob/main/plugins/lookup/bakery.py)|Look up the status of the agent bakery.|[![Integration Tests for bakery Lookup Module](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-lkp-bakery.yaml/badge.svg)](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-lkp-bakery.yaml)
[checkmk.general.folder](https://github.com/Checkmk/ansible-collection-checkmk.general/blob/main/plugins/lookup/folder.py)|Look up folder attributes.|[![Integration Tests for Folder Lookup Module](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-lkp-folder.yaml/badge.svg)](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-lkp-folder.yaml)
[checkmk.general.folders](https://github.com/Checkmk/ansible-collection-checkmk.general/blob/main/plugins/lookup/folders.py)|Look up all folders.|[![Integration Tests for Folders Lookup Module](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-lkp-folders.yaml/badge.svg)](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-lkp-folders.yaml)
[checkmk.general.host](https://github.com/Checkmk/ansible-collection-checkmk.general/blob/main/plugins/lookup/host.py)|Look up host attributes.|[![Integration Tests for Host Lookup Module](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-lkp-host.yaml/badge.svg)](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-lkp-host.yaml)
[checkmk.general.hosts](https://github.com/Checkmk/ansible-collection-checkmk.general/blob/main/plugins/lookup/hosts.py)|Look up all hosts.|[![Integration Tests for Hosts Lookup Module](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-lkp-hosts.yaml/badge.svg)](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-lkp-hosts.yaml)
[checkmk.general.rule](https://github.com/Checkmk/ansible-collection-checkmk.general/blob/main/plugins/lookup/rule.py)|Look up rule attributes.|[![Integration Tests for Rule Lookup Module](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-lkp-rules.yaml/badge.svg)](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-lkp-rules.yaml)
[checkmk.general.rules](https://github.com/Checkmk/ansible-collection-checkmk.general/blob/main/plugins/lookup/rules.py)|Look up all rules.|[![Integration Tests for Rules Lookup Module](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-lkp-rules.yaml/badge.svg)](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-lkp-rules.yaml)
[checkmk.general.ruleset](https://github.com/Checkmk/ansible-collection-checkmk.general/blob/main/plugins/lookup/ruleset.py)|Look up ruleset attributes.|[![Integration Tests for Ruleset Lookup Module](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-lkp-rulesets.yaml/badge.svg)](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-lkp-rulesets.yaml)
[checkmk.general.rulesets](https://github.com/Checkmk/ansible-collection-checkmk.general/blob/main/plugins/lookup/rulesets.py)|Look up all rulesets.|[![Integration Tests for Rulesets Lookup Module](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-lkp-rulesets.yaml/badge.svg)](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-lkp-rulesets.yaml)
[checkmk.general.site](https://github.com/Checkmk/ansible-collection-checkmk.general/blob/main/plugins/lookup/site.py)|Look up site attributes.|[![Integration Tests for Site Lookup Module](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-lkp-site.yaml/badge.svg)](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-lkp-site.yaml)
[checkmk.general.sites](https://github.com/Checkmk/ansible-collection-checkmk.general/blob/main/plugins/lookup/sites.py)|Look up all sites.|[![Integration Tests for Sites Lookup Module](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-lkp-sites.yaml/badge.svg)](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-lkp-sites.yaml)
[checkmk.general.version](https://github.com/Checkmk/ansible-collection-checkmk.general/blob/main/plugins/lookup/version.py)|Look up version and edition information.|[![Integration Tests for Version Lookup Module](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-lkp-version.yaml/badge.svg)](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-lkp-version.yaml)

### :battery: Modules
Click on the module name below, to get detailed documentation about it.

Name | Description | Tests
--- | --- | ---
[checkmk.general.activation](https://github.com/Checkmk/ansible-collection-checkmk.general/blob/main/plugins/modules/activation.py)|Activate changes.|[![Integration Tests for Activation Module](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-activation.yaml/badge.svg)](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-activation.yaml)
[checkmk.general.bakery](https://github.com/Checkmk/ansible-collection-checkmk.general/blob/main/plugins/modules/bakery.py)|Bake and sign agents.|[![Integration Tests for Bakery Module](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-bakery.yaml/badge.svg)](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-bakery.yaml)
[checkmk.general.contact_group](https://github.com/Checkmk/ansible-collection-checkmk.general/blob/main/plugins/modules/contact_group.py)|Manage contact groups.|[![Integration Tests for Contact Group Module](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-contact_group.yaml/badge.svg)](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-contact_group.yaml)
[checkmk.general.discovery](https://github.com/Checkmk/ansible-collection-checkmk.general/blob/main/plugins/modules/discovery.py)|Discover services on hosts.|[![Integration Tests for Discovery Module](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-discovery.yaml/badge.svg)](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-discovery.yaml)
[checkmk.general.downtime](https://github.com/Checkmk/ansible-collection-checkmk.general/blob/main/plugins/modules/downtime.py)|Manage downtimes.|[![Integration Tests for Downtime Module](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-downtime.yaml/badge.svg)](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-downtime.yaml)
[checkmk.general.folder](https://github.com/Checkmk/ansible-collection-checkmk.general/blob/main/plugins/modules/folder.py)|Manage folders.|[![Integration Tests for Folder Module](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-folder.yaml/badge.svg)](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-folder.yaml)
[checkmk.general.host_group](https://github.com/Checkmk/ansible-collection-checkmk.general/blob/main/plugins/modules/host_group.py)|Manage host groups.|[![Integration Tests for Host Group Module](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-host_group.yaml/badge.svg)](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-host_group.yaml)
[checkmk.general.host](https://github.com/Checkmk/ansible-collection-checkmk.general/blob/main/plugins/modules/host.py)|Manage hosts.|[![Integration Tests for Host Module](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-host.yaml/badge.svg)](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-host.yaml)
[checkmk.general.rule](https://github.com/Checkmk/ansible-collection-checkmk.general/blob/main/plugins/modules/rule.py)|Manage rules.|[![Integration Tests for Rule Module](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-rule.yaml/badge.svg)](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-rule.yaml)
[checkmk.general.service_group](https://github.com/Checkmk/ansible-collection-checkmk.general/blob/main/plugins/modules/service_group.py)|Manage service groups.|[![Integration Tests for Service Group Module](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-service_group.yaml/badge.svg)](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-service_group.yaml)
[checkmk.general.site](https://github.com/Checkmk/ansible-collection-checkmk.general/blob/main/plugins/modules/site.py)|Manage sites.|[![Integration Tests for Site Module](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-site.yaml/badge.svg)](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-site.yaml)
[checkmk.general.tag_group](https://github.com/Checkmk/ansible-collection-checkmk.general/blob/main/plugins/modules/tag_group.py)|Manage tag groups.|[![Integration Tests for Tag Group Module](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-tag_group.yaml/badge.svg)](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-tag_group.yaml)
[checkmk.general.timeperiod](https://github.com/Checkmk/ansible-collection-checkmk.general/blob/main/plugins/modules/timeperiod.py)|Manage time periods.|[![Integration Tests for Tag Group Module](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-timeperiod.yaml/badge.svg)](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-timeperiod.yaml)
[checkmk.general.user](https://github.com/Checkmk/ansible-collection-checkmk.general/blob/main/plugins/modules/user.py)|Manage users.|[![Intime periodsests for User Module](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-user.yaml/badge.svg)](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/ans-int-test-user.yaml)

### :computer: Roles
Click on the role name below, to get documentation about the role.

Name | Description | Tests
--- | --- | ---
[checkmk.general.agent](https://github.com/Checkmk/ansible-collection-checkmk.general/blob/main/roles/agent/README.md)|Installs Checkmk agents.| [![Molecule Tests for Agent Role](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/molecule-role-agent.yaml/badge.svg)](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/molecule-role-agent.yaml)
[checkmk.general.server](https://github.com/Checkmk/ansible-collection-checkmk.general/blob/main/roles/server/README.md)|Installs Checkmk servers and manages Checkmk sites.|[![Molecule Tests for Server Role](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/molecule-role-server.yaml/badge.svg)](https://github.com/Checkmk/ansible-collection-checkmk.general/actions/workflows/molecule-role-server.yaml)

## :heavy_plus_sign: Additional content

We love to see the community build things on top of this collection.
Check out [COMMUNITY.md](COMMUNITY.md) for a listing of interesting projects that build upon this collection in some way.

## :green_heart: Getting Involved

See [CONTRIBUTING](CONTRIBUTING.md).

## :mega: Release notes

See [CHANGELOG.rst](CHANGELOG.rst).

## :books: Versioning

This collection uses [Semantic Versioning](https://semver.org/) for releases. From the official homepage:

    Given a version number MAJOR.MINOR.PATCH, increment the:

      MAJOR version when you make incompatible API changes
      MINOR version when you add functionality in a backward compatible manner
      PATCH version when you make backward compatible bug fixes

## :truck: Roadmap
This is merely a collection of possible additions to the collection.
Please do **not** consider it a concrete planning document!

- Modules
  - Monitoring
    - Acknowledgement
    - Business Intelligence
    - Event Console
  - Setup
    - Agents
    - Business Intelligence
    - Dynamic host management (DCD)
    - Event Console
    - Notification Rules
- OMD Module

## :information_source: More information about Ansible

- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)

## :information_source: More information about Checkmk

* [Checkmk Website](https://checkmk.com)
* [Checkmk Documentation](https://docs.checkmk.com/)
* [Checkmk Community](https://forum.checkmk.com/)

## :scroll: Licensing

See [LICENSE](LICENSE).

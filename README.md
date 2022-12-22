# tribe29 Checkmk Collection

Checkmk already provides the needed APIs to automate and 
configure your monitoring. With this project we want to create
and share modules and roles for Ansible to both simplify your first steps
with automating Checkmk and keep your daily operations smooth and efficient.

---

## Here be dragons!

This repository is provided as is and we cannot guarantee stability at this point.
Additionally, there is no commercial support whatsoever!
This is an open source endeavour, which we want to share and progress with the community.

[![Ansible Sanity Tests](https://github.com/tribe29/ansible-collection-tribe29.checkmk/actions/workflows/ansible-sanity-tests.yaml/badge.svg)](https://github.com/tribe29/ansible-collection-tribe29.checkmk/actions/workflows/ansible-sanity-tests.yaml)
[![Ansible Integration Tests for all Modules](https://github.com/tribe29/ansible-collection-tribe29.checkmk/actions/workflows/ans-int-tests-full.yaml/badge.svg)](https://github.com/tribe29/ansible-collection-tribe29.checkmk/actions/workflows/ans-int-tests-full.yaml)
<!-- [![Ansible Unit Tests](https://github.com/tribe29/ansible-collection-tribe29.checkmk/actions/workflows/ansible-unit-tests.yaml/badge.svg)](https://github.com/tribe29/ansible-collection-tribe29.checkmk/actions/workflows/ansible-unit-tests.yaml) -->

---

This repository is a successor to [ansible-checkmk](https://github.com/tribe29/ansible-checkmk)
in a way, that we take the idea of the initial repository and translate it into
todays format. We will try to keep you posted as best as we can.
Also, keep an eye on [this Checkmk forum post](https://forum.checkmk.com/t/checkmk-goes-ansible/25428) for updates.

## Dependencies
 - [ansible.posix](https://github.com/ansible-collections/ansible.posix)
 - [community.general](https://github.com/ansible-collections/community.general)

Although the Ansible project notes, that collections should have no or very little dependencies, we want to make sure the  collection works for you out-of-the-box. Currently we only depend on very basic collections, which are most likely already installed in your environment. For version constraints, see [galaxy.yml](galaxy.yml).

## Getting help

For documentation on the [included modules](#modules), run the following
command substituting the $MODULE_NAME:

    ansible-doc tribe29.checkmk.$MODULE_NAME

For any form of support queries or requests refer to [SUPPORT.md](SUPPORT.md).

## Repository Structure

For information about the structure and organization of this repository
have a look at [STRUCTURE.md](docs/STRUCTURE.md).

## Included content

<!--start collection content-->
<!-- ### Inventory plugins
Name | Description
--- | ---
[tribe29.checkmk.ec2](https://github.com/tribe29/ansible-collection-tribe29.checkmk/tree/main/docs/tribe29.checkmk.ec2_inventory.rst)|EC2 inventory source

### Lookup plugins
Name | Description
--- | ---
[tribe29.checkmk.account_attribute](https://github.com/tribe29/ansible-collection-tribe29.checkmk/tree/main/docs/tribe29.checkmk.account_attribute_lookup.rst)|Look up Checkmk account attributes.
-->

### Modules
Name | Description | Tests
--- | --- | ---
[tribe29.checkmk.activation](https://github.com/tribe29/ansible-collection-tribe29.checkmk/blob/main/plugins/modules/activation.py)|Activate changes.|[![Integration Tests for Activation Module](https://github.com/tribe29/ansible-collection-tribe29.checkmk/actions/workflows/ans-int-test-activation.yaml/badge.svg)](https://github.com/tribe29/ansible-collection-tribe29.checkmk/actions/workflows/ans-int-test-activation.yaml)
[tribe29.checkmk.contact_group](https://github.com/tribe29/ansible-collection-tribe29.checkmk/blob/main/plugins/modules/contact_group.py)|Manage contact groups.|[![Integration Tests for Contact Group Module](https://github.com/tribe29/ansible-collection-tribe29.checkmk/actions/workflows/ans-int-test-contact_group.yaml/badge.svg)](https://github.com/tribe29/ansible-collection-tribe29.checkmk/actions/workflows/ans-int-test-contact_group.yaml)
[tribe29.checkmk.discovery](https://github.com/tribe29/ansible-collection-tribe29.checkmk/blob/main/plugins/modules/discovery.py)|Discover services on hosts.|[![Integration Tests for Discovery Module](https://github.com/tribe29/ansible-collection-tribe29.checkmk/actions/workflows/ans-int-test-discovery.yaml/badge.svg)](https://github.com/tribe29/ansible-collection-tribe29.checkmk/actions/workflows/ans-int-test-discovery.yaml)
[tribe29.checkmk.downtime](https://github.com/tribe29/ansible-collection-tribe29.checkmk/blob/main/plugins/modules/downtime.py)|Schedule downtimes on hosts and services.|[![Integration Tests for Downtime Module](https://github.com/tribe29/ansible-collection-tribe29.checkmk/actions/workflows/ans-int-test-downtime.yaml/badge.svg)](https://github.com/tribe29/ansible-collection-tribe29.checkmk/actions/workflows/ans-int-test-downtime.yaml)
[tribe29.checkmk.folder](https://github.com/tribe29/ansible-collection-tribe29.checkmk/blob/main/plugins/modules/folder.py)|Manage folders.|[![Integration Tests for Folder Module](https://github.com/tribe29/ansible-collection-tribe29.checkmk/actions/workflows/ans-int-test-folder.yaml/badge.svg)](https://github.com/tribe29/ansible-collection-tribe29.checkmk/actions/workflows/ans-int-test-folder.yaml)
[tribe29.checkmk.host_group](https://github.com/tribe29/ansible-collection-tribe29.checkmk/blob/main/plugins/modules/host_group.py)|Manage host groups.|[![Integration Tests for Host Group Module](https://github.com/tribe29/ansible-collection-tribe29.checkmk/actions/workflows/ans-int-test-host_group.yaml/badge.svg)](https://github.com/tribe29/ansible-collection-tribe29.checkmk/actions/workflows/ans-int-test-host_group.yaml)
[tribe29.checkmk.host](https://github.com/tribe29/ansible-collection-tribe29.checkmk/blob/main/plugins/modules/host.py)|Manage hosts.|[![Integration Tests for Host Module](https://github.com/tribe29/ansible-collection-tribe29.checkmk/actions/workflows/ans-int-test-host.yaml/badge.svg)](https://github.com/tribe29/ansible-collection-tribe29.checkmk/actions/workflows/ans-int-test-host.yaml)
[tribe29.checkmk.rule](https://github.com/tribe29/ansible-collection-tribe29.checkmk/blob/main/plugins/modules/rule.py)|Manage rules.|[![Integration Tests for Rule Module](https://github.com/tribe29/ansible-collection-tribe29.checkmk/actions/workflows/ans-int-test-rule.yaml/badge.svg)](https://github.com/tribe29/ansible-collection-tribe29.checkmk/actions/workflows/ans-int-test-rule.yaml)
[tribe29.checkmk.service_group](https://github.com/tribe29/ansible-collection-tribe29.checkmk/blob/main/plugins/modules/service_group.py)|Manage service groups.|[![Integration Tests for Service Group Module](https://github.com/tribe29/ansible-collection-tribe29.checkmk/actions/workflows/ans-int-test-service_group.yaml/badge.svg)](https://github.com/tribe29/ansible-collection-tribe29.checkmk/actions/workflows/ans-int-test-service_group.yaml)
[tribe29.checkmk.tag_group](https://github.com/tribe29/ansible-collection-tribe29.checkmk/blob/main/plugins/modules/tag_group.py)|Manage tag groups.|[![Integration Tests for Tag Group Module](https://github.com/tribe29/ansible-collection-tribe29.checkmk/actions/workflows/ans-int-test-tag_group.yaml/badge.svg)](https://github.com/tribe29/ansible-collection-tribe29.checkmk/actions/workflows/ans-int-test-tag_group.yaml)

### Roles
Name | Description | Tests
--- | --- | ---
[tribe29.checkmk.agent](https://github.com/tribe29/ansible-collection-tribe29.checkmk/blob/main/roles/agent/README.md)|Installs Checkmk agents.| Tests currently unavailable. <!-- [![Molecule Tests for Agent Role](https://github.com/tribe29/ansible-collection-tribe29.checkmk/actions/workflows/molecule-role-agent.yaml/badge.svg)](https://github.com/tribe29/ansible-collection-tribe29.checkmk/actions/workflows/molecule-role-agent.yaml)-->
[tribe29.checkmk.server](https://github.com/tribe29/ansible-collection-tribe29.checkmk/blob/main/roles/server/README.md)|Installs Checkmk servers.|[![Molecule Tests for Server Role](https://github.com/tribe29/ansible-collection-tribe29.checkmk/actions/workflows/molecule-role-server.yaml/badge.svg)](https://github.com/tribe29/ansible-collection-tribe29.checkmk/actions/workflows/molecule-role-server.yaml)
<!--end collection content-->

## Installing this collection

### Locally

You can install the Checkmk collection locally, if you acquired a tarball from the [releases page](https://github.com/tribe29/ansible-collection-tribe29.checkmk/releases) as follows:

    ansible-galaxy collection install /path/to/tribe29-checkmk-X.Y.Z.tar.gz

You can also include it in a `requirements.yml` file and install it with
`ansible-galaxy collection install -r requirements.yml`, using the format:
```yaml
---
collections:
  - source: /path/to/tribe29-checkmk-X.Y.Z.tar.gz
    type: file
```

### From the Galaxy

You can install the Checkmk collection with the Ansible Galaxy CLI:

    ansible-galaxy collection install tribe29.checkmk

You can also include it in a `requirements.yml` file and install it with
`ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: tribe29.checkmk
    version: X.Y.Z
```

## Using this collection

You can either call modules by their Fully Qualified Collection Namespace (FQCN),
such as `tribe29.checkmk.activation`, or you can call modules by their short name
if you list the `tribe29.checkmk` collection in the playbook's [`collections`](https://docs.ansible.com/ansible/devel/user_guide/collections_using.html#using-collections-in-playbooks) keyword:

```yaml
---
- hosts: all

  collections:
    - tribe29.checkmk

  tasks:
    - name: "Run activation."
      activation:
        server_url: "http://localhost/"
        site: "my_site"
        automation_user: "automation"
        automation_secret: "$SECRET"
        force_foreign_changes: 'true'
        sites:
          - "my_site"
```
### More information about Checkmk

* [Checkmk Website](https://checkmk.com)
* [Checkmk Documentation](https://docs.checkmk.com/)
* [Checkmk Community](https://forum.checkmk.com/)
* [tribe29 - the checkmk company](https://tribe29.com)

## Contributing to this collection

See [CONTRIBUTING](CONTRIBUTING.md).

## Release notes
<!--Add a link to a changelog.rst file or an external docsite to cover this information. -->
See [CHANGELOG.rst](CHANGELOG.rst).

## Roadmap
<!-- Optional. Include the roadmap for this collection, and the proposed release/versioning strategy so users can anticipate the upgrade/update cycle. -->
This is merely a collection of possible additions to the role.
Please do **not** consider a concrete planning document!

- Modules
  - Monitoring
    - Acknowledgement
  - Setup
    - Agents
    - BI
    - Passwords
    - Time Periods
- Lookup Plugins
  - Version

## More information about Ansible

- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)

## Licensing
See [LICENSE](LICENSE).

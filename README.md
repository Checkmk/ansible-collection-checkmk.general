# tribe29 Checkmk Collection

Checkmk already provides the needed APIs to automate and 
configure your monitoring. With this project we want to create
and share modules and roles for Ansible to both simplify your first steps
with automating Checkmk and keep your daily operations smooth and efficient.

---

## Here be dragons!

Everything within this repository is subject to possibly heavy change
and we cannot guarantee stability at this point. You have been warned!

[![Ansible Sanity Tests](https://github.com/tribe29/ansible-collection-tribe29.checkmk/actions/workflows/ansible-sanity-tests.yaml/badge.svg)](https://github.com/tribe29/ansible-collection-tribe29.checkmk/actions/workflows/ansible-sanity-tests.yaml)
[![Ansible Integration Tests](https://github.com/tribe29/ansible-collection-tribe29.checkmk/actions/workflows/ansible-integration-tests.yaml/badge.svg)](https://github.com/tribe29/ansible-collection-tribe29.checkmk/actions/workflows/ansible-integration-tests.yaml)
<!-- [![Ansible Unit Tests](https://github.com/tribe29/ansible-collection-tribe29.checkmk/actions/workflows/ansible-unit-tests.yaml/badge.svg)](https://github.com/tribe29/ansible-collection-tribe29.checkmk/actions/workflows/ansible-unit-tests.yaml) -->

---

This repository is a successor to [ansible-checkmk](https://github.com/tribe29/ansible-checkmk)
in a way, that we take the idea of the initial repository and translate it into
todays format. We will try to keep you posted as best as we can.
Also, keep an eye on [this Checkmk forum post](https://forum.checkmk.com/t/checkmk-goes-ansible/25428) for updates.

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
Name | Description
--- | ---
[tribe29.checkmk.activation](https://github.com/tribe29/ansible-collection-tribe29.checkmk/blob/main/plugins/modules/activation.py)|Activate changes.
[tribe29.checkmk.discovery](https://github.com/tribe29/ansible-collection-tribe29.checkmk/blob/main/plugins/modules/discovery.py)|Discover services on hosts.
[tribe29.checkmk.downtime](https://github.com/tribe29/ansible-collection-tribe29.checkmk/blob/main/plugins/modules/downtime.py)|Schedule downtimes on hosts and services.
[tribe29.checkmk.folder](https://github.com/tribe29/ansible-collection-tribe29.checkmk/blob/main/plugins/modules/folder.py)|Manage folders.
[tribe29.checkmk.host](https://github.com/tribe29/ansible-collection-tribe29.checkmk/blob/main/plugins/modules/host.py)|Manage hosts.
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

We welcome and appreciate community contributions to this collection.
If you find problems, please open an issue or create a pull request against [this repository](https://github.com/tribe29/ansible-collection-tribe29.checkmk).
See [Contributing to Ansible-maintained collections](https://docs.ansible.com/ansible/devel/community/contributing_maintained_collections.html#contributing-maintained-collections) for more details on how to contribute.

You can also join our [Checkmk Community](https://forum.checkmk.com/)
and have a look at the [dedicated post regarding Ansible](https://forum.checkmk.com/t/checkmk-goes-ansible/25428)
and [the 'ansible' tag](https://forum.checkmk.com/tag/ansible) in general.

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
    - Contact Groups
    - Host Groups
    - Host Tag Groups
    - Passwords
    - Service Groups
    - Time Periods
    - Users
- Lookup Plugins
  - Version
- Roles
  - Checkmk server installation
  - Checkmk agent installation

## More information about Ansible

- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)

## Licensing
See [LICENSE](LICENSE).

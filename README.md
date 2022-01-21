# tribe29 Checkmk Collection

## This is a work in progress!
## Do not use until you know what you are doing!

---

We are completely reorganizing this repository. In the process we might even
need to create new repositories or rename this one. Most of this work will
happen in a dedicated branch until it is ready to be mainlined. Keep an eye on
the progress here and feel free to contribute in any way. We will try to keep
you posted as best as we can.
Keep an eye on [this Checkmk forum post](https://forum.checkmk.com/t/checkmk-goes-ansible/25428) for updates.

## Notes

See [NOTES.md](NOTES.md)

## Repository Structure

For information about the structure and organization of this repository
have a look at [STRUCTURE.md](docs/STRUCTURE.md).

---

Checkmk already provides the needed APIs to automate the 
configuration of your monitoring. With this project we want to create
and share roles and modules for Ansible to simplify your first steps
with automating Checkmk through Ansible.

## Included content

<!--start collection content-->
<!-- ### Inventory plugins
Name | Description
--- | ---
[tribe29.checkmk.ec2](https://github.com/tribe29/ansible-checkmk/tree/main/docs/tribe29.checkmk.ec2_inventory.rst)|EC2 inventory source
[tribe29.checkmk.rds](https://github.com/tribe29/ansible-checkmk/tree/main/docs/tribe29.checkmk.rds_inventory.rst)|rds instance source

### Lookup plugins
Name | Description
--- | ---
[tribe29.checkmk.account_attribute](https://github.com/tribe29/ansible-checkmk/tree/main/docs/tribe29.checkmk.account_attribute_lookup.rst)|Look up Checkmk account attributes.
[tribe29.checkmk.secret](https://github.com/tribe29/ansible-checkmk/tree/main/docs/tribe29.checkmk.secret_lookup.rst)|Look up secrets stored in Checkmk Secrets Manager. -->

### Modules
Name | Description
--- | ---
[tribe29.checkmk.activation](https://github.com/tribe29/ansible-checkmk/tree/main/docs/tribe29.checkmk.activation.md)|Activate changes in Checkmk.
[tribe29.checkmk.discovery](https://github.com/tribe29/ansible-checkmk/tree/main/docs/tribe29.checkmk.discovery.md)|Discover services in Checkmk.
[tribe29.checkmk.folder](https://github.com/tribe29/ansible-checkmk/tree/main/docs/tribe29.checkmk.folder.md)|Manage folders in Checkmk.
[tribe29.checkmk.host](https://github.com/tribe29/ansible-checkmk/tree/main/docs/tribe29.checkmk.host.md)|Manage hosts in Checkmk.
<!--end collection content-->

## Installing this collection

### Locally

You can install the Checkmk collection locally, if you aquired a tarball for
offline installation as follows:

    ansible-galaxy collection install /path/to/tribe29-checkmk-X.Y.Z.tar.gz

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - source: /path/to/tribe29-checkmk-X.Y.Z.tar.gz
    type: file
```

### From the Galaxy

You can install the Checkmk collection with the Ansible Galaxy CLI:

    ansible-galaxy collection install tribe29.checkmk

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: tribe29.checkmk
```

## Using this collection

You can either call modules by their Fully Qualified Collection Namespace (FQCN),
such as `tribe29.checkmk.activation`, or you can call modules by their short name
if you list the `tribe29.checkmk` collection in the playbook's `collections` keyword:

```yaml
---
    <Example Playbook>
```
### See Also:

* [Checkmk Documemtation](https://docs.checkmk.com/)
* [Checkmk Website](https://checkmk.com)
* [tribe29 - the checkmk company](https://tribe29.com)

## Contributing to this collection

We welcome community contributions to this collection. If you find problems, please open an issue or create a PR against the [tribe29 Checkmk collection repository](https://github.com/tribe29/ansible-checkmk/). See [Contributing to Ansible-maintained collections](https://docs.ansible.com/ansible/devel/community/contributing_maintained_collections.html#contributing-maintained-collections) for more details.

You can also join our [Checkmk Community](https://docs.checkmk.com/).

## Release notes
<!--Add a link to a changelog.rst file or an external docsite to cover this information. -->

## Roadmap
<!-- Optional. Include the roadmap for this collection, and the proposed release/versioning strategy so users can anticipate the upgrade/update cycle. -->
This is merely a collection of possible additions to the role. Please do not consider a concrete planning document for the near future!

- Modules
  - Monitoring
    - Acknowledgement
    - Downtime
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

## More information

- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)

## Licensing

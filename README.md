# tribe29 Checkmk Collection

## This is a work in progress!
## Do not use until you know what you are doing!

---

We are completely reorganizing this repository. In the process we might even need to create new repositories or rename this one. Most of this work will happen in a dedicated branch until it is ready to be mainlined. Keep an eye on the progress here and feel free to contribute in any way. We will try to keep you posted as best as we can. Keep an eye on [this Checkmk forum post](https://forum.checkmk.com/t/checkmk-goes-ansible/25428) for updates.

## Notes

- https://docs.ansible.com/ansible/latest/dev_guide/developing_collections_structure.html
- https://docs.ansible.com/ansible/latest/user_guide/collections_using.html

---

Checkmk already provides the needed APIs to automate the 
configuration of your monitoring. With this project we want to create
and share roles and modules for ansible to simplify your first steps with automating Checkmk through Ansible.

## Installing this collection

You can install the Checkmk collection with the Ansible Galaxy CLI:

    ansible-galaxy collection install tribe29.checkmk

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: tribe29.checkmk
```

## Using this collection


You can either call modules by their Fully Qualified Collection Namespace (FQCN), such as `tribe29.checkmk.api`, or you can call modules by their short name if you list the `tribe29.checkmk` collection in the playbook's `collections` keyword:

```yaml
---
    <Example Playbook>
```
### See Also:

* [Checkmk Documemtation](https://docs.checkmk.com/)
* [Checkmk Website](https://checkmk.com)
* [tribe29 - the checkmk company](https://tribe29.com)

## Release notes

TBD

## Roadmap

TBD

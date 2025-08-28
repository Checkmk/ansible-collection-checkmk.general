# Installation Guide

This guide provides instructions on how to install and manage the `checkmk.general` Ansible collection. For more detailed information, you can always refer to the [official Ansible documentation on installing collections](https://docs.ansible.com/ansible/latest/collections_guide/collections_installing.html).

## Standard Installation

The recommended way to install the collection is from Ansible Galaxy. This command will download and install the latest published version.

```bash
ansible-galaxy collection install checkmk.general
```

## Updating the Collection

The `install` command does not automatically update an existing collection. To upgrade to the latest version, use the `--force` flag.

```bash
ansible-galaxy collection install checkmk.general --force
```

To install a specific version, you can specify it with a version number:

```bash
ansible-galaxy collection install checkmk.general:==2.0.0
```

## Troubleshooting 💡

If you run a playbook and receive an error like `module or collection not found`, it usually means Ansible cannot find the collection in its configured search paths.

### 1. Verify the Installation

First, confirm that the collection is installed and see where Ansible has placed it.

```bash
ansible-galaxy collection list
```

This command will list all installed collections and their locations.

### 2. Check Ansible Configuration

Next, check which paths your Ansible installation is configured to search.

```bash
ansible --version
```

Look for the `ansible collection location` in the output. If the path where the collection was installed is not listed here, Ansible will not be able to find it.

### 3. Configure the Collections Path (If Needed)

If the collection path is missing from your configuration, you can add it by creating or editing a [`ansible.cfg`](https://docs.ansible.com/ansible/latest/reference_appendices/config.html) file. Add the following content to it:

```ini
[defaults]
collections_path = ~/.ansible/collections
```

This tells Ansible to always look for collections in the standard user-level installation directory, ensuring your playbooks can find and use the `checkmk.general` modules.
# Demo Playbooks

## About These Demos

This directory contains a set of Ansible playbooks designed to demonstrate the functionality of each module in the `checkmk.general` collection.

Each playbook is named after the module it demonstrates. For a comprehensive example, the `full.yml` playbook will run all other playbooks in this directory in a logical sequence.

-----

## Getting Started

Follow these steps to run the demo playbooks against a Checkmk site.

### 1. Configure Connection

Before you start, you need to provide connection details for a Checkmk site.

1.  Open the authentication file: `../vars/auth.yml`.
2.  Update the file with the URL, site name, and automation user credentials for your Checkmk instance.

> **Warning**
> Please use a dedicated **non-production** Checkmk site for this demo. These playbooks will make changes to your Checkmk configuration.

### 2. Run the Playbook

Once your `auth.yml` file is configured, you can run the full demo playbook. The command must be run from the **root directory** of this repository.

```bash
# Ensure you are in the root directory of the ansible-collection-checkmk.general repository
ansible-playbook -i playbooks/hosts playbooks/demo/full.yml
```

This command uses the predefined inventory file at `playbooks/hosts` to execute the `full.yml` playbook, which will demonstrate the collection's capabilities on your configured Checkmk site.

## A Note on Module Naming

You'll notice that modules in this demo are called by their short names (e.g., `server`) instead of their Fully Qualified Collection Name (FQCN) (`e.g., checkmk.general.server`).

This is intentional. Using short names ensures that Ansible runs the module code directly from this Git repository. This prevents the demo from accidentally using a different, pre-installed version of the collection, guaranteeing you are testing the code in this local checkout.

# Demo Playbooks

## About
These playbooks demonstrate the different modules contained in this collection.
The naming should be rather obvious. The only *special* playbook is [full.yml](./full.yml).
As the name suggests, it runs all the playbooks contained in this folder.

## Getting started
To get started, inspect [../vars/auth.yml](../vars/auth.yml).
You need to set up a local site, just as described, or provide the details to an existing site. Do **not** use a productive site here!

Once the prerequisites are met, you can run the playbook with the inventory
provided at [../hosts](../hosts):

    # You need to be in the project root for this to work!
    cd ../../
    ansible-playbook -i playbooks/hosts playbooks/demo/full.yml

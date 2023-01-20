# Playbooks

## Getting started
To get started using these playbooks, you need to create your own [`config.yml`](./vars/config.yml)
in [`./vars/`](./vars/) from the shipped [`config.yml.example`](./vars/config.yml.example). Add the details of your
Checkmk site and call a playbook. Please refer to the following tables, which
playbooks are available and what they do.

## Folders
Name | Description
--- | ---
[vars](./vars/)|Contains variable files. We ship a `config.yml.example` for you to copy.
[usecases](./usecases/)|Contains playbooks for specific use cases.

## Playbooks
Name | Description
--- | ---
[demo.yml](./demo.yml)|Demonstrate the power of this collection against an **empty** demo site. Use this from within this repository.
[roles.yml](./roles.yml)|Run the roles contained in this collection. Use the tags `agent` and `server` to limit the run to one role.

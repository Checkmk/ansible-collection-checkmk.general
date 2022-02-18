# Playbooks

## Getting started
To get started using these playbooks, you need to create your own [`config.yml`](./vars/config.yml)
in [`./vars/`](./vars/) from the shipped [`config.yml.example`](./vars/config.yml.example). Add the details of your
Checkmk site and call a playbook. Please refer to the following table, which
playbooks are available and what they do.

## Playbooks
Name | Description
--- | ---
[demo.yml](./demo.yml)|Demonstrate the power of this collection against an **empty** demo site. Use this from within this repository.
[test-full.yml](./test-full.yml)|Current testing playbook. Handle with care!

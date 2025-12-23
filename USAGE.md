# Usage guide

This document provides a comprehensive guide for new users on how to effectively use this collection.

## Using this collection

We encourage you - in accordance with Ansible Best Practices - to always use **FQCNs (Fully Qualified Collection Names)** as seen below. This ensures that you always know which module is at play.

*Keep in mind the parameters `server_url` and `site` are concatenated to form the base URL of the Checkmk site.*

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
        force_foreign_changes: true
        sites:
          - "mysite"
```

-----

## Specifying common parameters

When using multiple modules from this collection, you'll often need to provide the same parameters (like `server_url`, `site`, `automation_user`, and `automation_secret`) repeatedly. The following sections show several ways Ansible offers to avoid repetition and keep your playbooks clean.

### `module_defaults`

You can set default values for module parameters at the play level. These defaults will be applied to all tasks within that play, unless a task explicitly overrides them.

```yaml
---
- hosts: all
  module_defaults:
    group/checkmk.general.checkmk:
      server_url: "http://myserver/"
      site: "mysite"
      automation_user: "myuser"
      automation_secret: "mysecret"

  tasks:
    - name: "Run activation."
      checkmk.general.activation:
        force_foreign_changes: true
        sites:
          - "mysite"
```

### Environment variables

You can also define these parameters as environment variables. Ansible will automatically pick them up. This is particularly useful for sensitive information like secrets.

```bash
export CHECKMK_SERVER_URL="http://myserver/"
export CHECKMK_SITE="mysite"
export CHECKMK_AUTOMATION_USER="myuser"
export CHECKMK_AUTOMATION_SECRET="mysecret"
```

### INI-style variables

Ansible can read variables from an INI file (e.g., `ansible.cfg` or a custom file). This allows you to centralize your configuration.

```ini
[checkmk]
server_url = http://myserver/
site = mysite
automation_user = myuser
automation_secret = mysecret
```

-----

## Invoking roles

This collection provides roles for common tasks. Here's how to use them:

### Example: Installing the Checkmk agent

To install the Checkmk agent on your hosts, you can use the `checkmk.general.agent` role.

It's important to know that this role comes with predefined default values located in the role's `defaults/main.yml` file. You should review these defaults and override them as needed to match your environment. For example, you can override variables by defining them under `vars` in your playbook.

```yaml
---
- hosts: all
  vars:
    # Example of overriding a default variable
    checkmk_agent_edition: 'cce'
  roles:
    - role: checkmk.general.agent
```

-----

## Invoking modules

Modules are used for executing specific tasks within a playbook.

### Example: Managing a host

This example demonstrates how to create or update a host in Checkmk:

```yaml
---
- hosts: all
  tasks:
    - name: "Create or update a host."
      checkmk.general.host:
        server_url: "http://myserver/"
        site: "mysite"
        automation_user: "myuser"
        automation_secret: "mysecret"
        host_name: "myhost"
        folder: "/"
        attributes:
          ipaddress: "127.0.0.1"
```

-----

## Lookup modules

Lookup modules allow you to fetch data from external sources within your playbooks. This collection for example includes a `version` lookup to retrieve the running version of a Checkmk site.

### Example: Using the `checkmk.general.version` Lookup

This example shows how to query the Checkmk site version and display it. This can be useful for conditional tasks or for simply reporting on your environment.

```yaml
---
- hosts: localhost
  gather_facts: false
  tasks:
    - name: "Get Checkmk version."
      ansible.builtin.set_fact:
        version: "{{ lookup('checkmk.general.version',
                server_url=my_url,
                site=mysite,
                validate_certs=False,
                automation_user=myuser,
                automation_secret=mysecret
            )}}"

    - name: "Print Checkmk version."
      ansible.builtin.debug:
        msg: "The Checkmk version is {{ version }}."
```

-----

## Inventory plugin

An inventory plugin allows Ansible to dynamically fetch its inventory from an external source. This collection includes an inventory plugin to use your Checkmk site as a dynamic source of hosts. This eliminates the need for a static `hosts` file if your Checkmk site is your source of truth.

### Example: Using the Checkmk inventory plugin

To use the plugin, create a YAML file (e.g., `checkmk.yml`) with the following content. This file will define the connection to your Checkmk site and instruct Ansible to use the `checkmk.general.checkmk` inventory plugin.

```yaml
plugin: checkmk.general.checkmk
server_url: "http://myserver/"
site: "mysite"
automation_user: "myuser"
automation_secret: "mysecret"
# Group the hosts based on the following elements
groupsources: ["hosttags", "sites"]
```

You can then run your playbook by pointing to this inventory file with the `-i` flag:

```bash
ansible-playbook -i checkmk.yml my_playbook.yml
```

Ansible will now dynamically execute the playbook against the hosts monitored by your Checkmk site.

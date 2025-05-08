# Lookup Plugins

## Using variables for Lookup plugins
It is possible to set variables for authentication globally for lookup plugins.
This way, they do not need to be provided at task level.

### Method 1: Environment variables
```bash
export CHECKMK_VAR_SERVER_URL="https://myserver"
export CHECKMK_VAR_SITE=mysite
export CHECKMK_VAR_AUTOMATION_USER=automation
export CHECKMK_VAR_AUTOMATION_SECRET=mysecret
export CHECKMK_VAR_VALIDATE_CERTS=False
```

### Method 2: In `ansible.cfg`
```ini
[checkmk_lookup]
server_url = https://myserver
site = mysite
automation_user = automation
automation_secret = mysecret
validate_certs = False

```

### Method 3: In playbooks or the inventory
```yaml
- name: My Task
  hosts: localhost
  gather_facts: false
  vars:
    checkmk_var_server_url: "https://myserver"
    checkmk_var_site: "mysite"
    checkmk_var_automation_user: "myuser"
    checkmk_var_automation_secret: "mysecret"
    checkmk_var_validate_certs: false

  tasks:
    - name: Get the attributes of myhost
      ansible.builtin.debug:
        msg: "Attributes of myhost: {{ attributes }}"
      vars:
        attributes: "{{ lookup('checkmk.general.host', 'myhost', effective_attributes=True) }}"
```

### Example
The following task will work, if one of the above methods has been applied.
```yaml
- name: My Task
  tasks:
    - name: Get the attributes of myhost
      ansible.builtin.debug:
        msg: "Attributes of myhost: {{ attributes }}"
      vars:
        attributes: "{{ lookup('checkmk.general.host', 'myhost', effective_attributes=True) }}"
```

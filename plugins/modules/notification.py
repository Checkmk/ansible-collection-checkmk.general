#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2025, Nicolas Brainez <nicolas@brainez.net>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: notification

short_description: Manage notification rules in Checkmk.

version_added: "7.3.0"

description:
- Manage notification rules in Checkmk.
- Create, update, and delete notification rules for various notification methods.

extends_documentation_fragment:
    - checkmk.general.common
    - checkmk.general.notification_options

notes:
- When I(rule_id) is not provided, the module will try to find an existing rule
  by matching the I(description) field in I(rule_properties).
  If multiple rules match the same description, the module will fail and ask for a unique C(rule_id).
- Requires Checkmk >= 2.3.0p42 or >= 2.4.0p22 for minimal configuration support.
- When a key is not explicitly provided, it will not be managed. That means if you set a certain key
  at some point and later remove it from your Ansible configuration, it will not be removed in the rule.

author:
    - Nicolas Brainez (@nicoske)
"""

EXAMPLES = r"""
# ---
# Create

- name: "Create an email notification rule"
  checkmk.general.notification:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    rule_config:
      rule_properties:
        description: "Notify all contacts on critical issues"
        comment: "Managed by Ansible"
      notification_method:
        notify_plugin:
          option: "create_notification_with_the_following_parameters"
          plugin_params:
            plugin_name: "mail"
      contact_selection:
        all_contacts_of_the_notified_object:
          state: "enabled"
    state: "present"
  register: notification_result

- name: "Show the ID of the new notification rule"
  ansible.builtin.debug:
    msg: "Rule ID: {{ notification_result.content.id }}"

- name: "Create a Slack notification rule"
  checkmk.general.notification:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    rule_config:
      rule_properties:
        description: "Slack notifications for critical alerts"
        comment: "Managed by Ansible"
      notification_method:
        notify_plugin:
          option: "create_notification_with_the_following_parameters"
          plugin_params:
            plugin_name: "slack"
            webhook_url:
              option: "explicit"
              url: "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
      contact_selection:
        all_contacts_of_the_notified_object:
          state: "enabled"
    state: "present"

- name: "Create a Microsoft Teams notification rule"
  checkmk.general.notification:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    rule_config:
      rule_properties:
        description: "Microsoft Teams notifications for critical alerts"
        comment: "Managed by Ansible"
      notification_method:
        notify_plugin:
          option: "create_notification_with_the_following_parameters"
          plugin_params:
            plugin_name: "msteams"
            webhook_url:
              option: "explicit"
              url: "https://outlook.office.com/webhook/YOUR/WEBHOOK/URL"
      contact_selection:
        all_contacts_of_the_notified_object:
          state: "enabled"
    state: "present"

# ---
# Update

# Note: Only keys explicitly provided are compared and updated.
#       Keys absent from rule_config will not be modified in the existing rule.
- name: "Update a notification rule"
  checkmk.general.notification:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    rule_id: "e83e6ed6-a4cc-47ed-900b-65d7ae1dbb3d"
    rule_config:
      rule_properties:
        description: "Notify all contacts on critical issues"
      notification_method:
        notify_plugin:
          option: "create_notification_with_the_following_parameters"
          plugin_params:
            plugin_name: "mail"
    state: "present"

# ---
# Delete

- name: "Delete a notification rule by rule_id"
  checkmk.general.notification:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    rule_id: "e83e6ed6-a4cc-47ed-900b-65d7ae1dbb3d"
    state: "absent"

# Note: If multiple rules share the same description, deletion by description will fail.
#       Use rule_id for unambiguous deletion.
- name: "Delete a notification rule by description"
  checkmk.general.notification:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    rule_config:
      rule_properties:
        description: "Notify all contacts on critical issues"
    state: "absent"

# ---
# Authentication with environment variables

- name: "Create a notification rule using environment variables for authentication"
  checkmk.general.notification:
    server_url: "{{ lookup('ansible.builtin.env', 'CHECKMK_VAR_SERVER_URL') }}"
    site: "{{ lookup('ansible.builtin.env', 'CHECKMK_VAR_SITE') }}"
    api_user: "{{ lookup('ansible.builtin.env', 'CHECKMK_VAR_API_USER') }}"
    api_secret: "{{ lookup('ansible.builtin.env', 'CHECKMK_VAR_API_SECRET') }}"
    validate_certs: "{{ lookup('ansible.builtin.env', 'CHECKMK_VAR_VALIDATE_CERTS') }}"
    rule_config:
      rule_properties:
        description: "Notify all contacts on critical issues"
        comment: "Managed by Ansible"
      notification_method:
        notify_plugin:
          option: "create_notification_with_the_following_parameters"
          plugin_params:
            plugin_name: "mail"
      contact_selection:
        all_contacts_of_the_notified_object:
          state: "enabled"
    state: "present"
"""

RETURN = r"""
msg:
    description: The output message that the module generates.
    type: str
    returned: always
    sample: 'Notification rule created.'
content:
    description: The complete notification rule object.
    type: dict
    returned: when rule is created or updated
    contains:
        id:
            description: The ID of the notification rule.
            type: str
            returned: when rule is created or updated
            sample: 'e83e6ed6-a4cc-47ed-900b-65d7ae1dbb3d'
        title:
            description: The title/description of the rule.
            type: str
            returned: when rule is created or updated
        extensions:
            description: The rule configuration details.
            type: dict
            returned: when rule is created or updated
"""

import json

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.checkmk.general.plugins.module_utils.api import CheckmkAPI
from ansible_collections.checkmk.general.plugins.module_utils.types import RESULT
from ansible_collections.checkmk.general.plugins.module_utils.utils import (
    base_argument_spec,
    result_as_dict,
)

HTTP_CODES_GET = {
    # http_code: (changed, failed, "Message")
    200: (False, False, "Rule found, nothing changed"),
    404: (False, False, "Not Found: The requested object has not been found."),
}

HTTP_CODES_POST = {
    200: (True, False, "OK: The operation was done successfully"),
}

HTTP_CODES_PUT = {
    200: (True, False, "OK: The operation was done successfully"),
}

HTTP_CODES_DELETE = {
    204: (True, False, "Operation done successfully. No further output."),
}


class NotificationRuleAPI(CheckmkAPI):
    def __init__(self, module):
        super().__init__(module)
        self.rule_id = self.params.get("rule_id")
        self.description = None

        rule_config = self.params.get("rule_config")
        if rule_config:
            rule_properties = rule_config.get("rule_properties")
            if rule_properties:
                self.description = rule_properties.get("description")

        # Verify parameters
        error = self._verify_parameters()
        if error:
            self.module.fail_json(msg=error)

        # Resolve rule_id from description if not provided
        if not self.rule_id and self.description:
            self.rule_id = self._find_rule_by_description(self.description)

        # Fetch current state
        if self.rule_id:
            self.current = self._fetch(
                code_mapping=HTTP_CODES_GET,
                endpoint="/objects/notification_rule/%s" % self.rule_id,
                method="GET",
            )
        else:
            self.current = RESULT(
                http_code=404,
                msg="No rule found.",
                content="",
                etag="",
                failed=False,
                changed=False,
            )

    def _verify_parameters(self):
        """Verify that mandatory parameters are present."""
        if (
            self.module.params.get("state") == "absent"
            and not self.rule_id
            and not self.description
        ):
            return (
                "Missing parameter 'rule_id' or "
                "'rule_config.rule_properties.description' "
                "to identify the notification rule to delete."
            )

    def _find_rule_by_description(self, description):
        """Find a notification rule by its description.
        Returns the rule_id if exactly one match is found."""
        result = self._fetch(
            code_mapping=HTTP_CODES_GET,
            endpoint="/domain-types/notification_rule/collections/all",
            method="GET",
        )

        if result.http_code != 200 or not result.content:
            return None

        content = result.content
        if isinstance(content, bytes):
            content = content.decode("utf-8")

        try:
            data = json.loads(content)
        except (json.JSONDecodeError, AttributeError):
            return None

        matches = [
            rule for rule in data.get("value", []) if rule.get("title") == description
        ]

        if len(matches) == 1:
            return matches[0]["id"]

        if len(matches) > 1:
            self.module.fail_json(
                msg=(
                    "Found %d notification rules with description '%s'. "
                    "Please provide a unique rule_id."
                )
                % (len(matches), description),
            )

        return None

    def post(self):
        data = {"rule_config": self.params.get("rule_config")}

        return self._fetch(
            code_mapping=HTTP_CODES_POST,
            endpoint="/domain-types/notification_rule/collections/all",
            data=data,
            method="POST",
        )

    def put(self):
        self.headers["If-Match"] = self.current.etag
        data = {"rule_config": self.params.get("rule_config")}

        return self._fetch(
            code_mapping=HTTP_CODES_PUT,
            endpoint="/objects/notification_rule/%s" % self.rule_id,
            data=data,
            method="PUT",
        )

    def delete(self):
        self.headers["If-Match"] = self.current.etag

        return self._fetch(
            code_mapping=HTTP_CODES_DELETE,
            endpoint="/objects/notification_rule/%s/actions/delete/invoke"
            % self.rule_id,
            data={},
            method="POST",
        )


def _desired_subset_matches(desired, current):
    """Recursively check if all keys in desired match in current.
    Only compares keys that the user actually provided."""
    if not isinstance(desired, dict) or not isinstance(current, dict):
        return desired == current

    for key, desired_value in desired.items():
        current_value = current.get(key)
        if isinstance(desired_value, dict) and isinstance(current_value, dict):
            if not _desired_subset_matches(desired_value, current_value):
                return False
        elif desired_value != current_value:
            return False

    return True


def changes_detected(module, current):
    """Compare desired rule_config against current state.
    Only compares fields that the user provided."""
    desired_config = module.params.get("rule_config")
    if not desired_config:
        return False

    current_config = current.get("extensions", {}).get("rule_config", {})

    return not _desired_subset_matches(desired_config, current_config)


def run_module():
    argument_spec = base_argument_spec()
    argument_spec.update(
        rule_id=dict(type="str", required=False),
        rule_config=dict(type="dict", required=False),
        state=dict(
            type="str",
            choices=["present", "absent"],
            required=True,
        ),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=False,
        required_if=[
            ("state", "present", ("rule_config",)),
            ("state", "absent", ("rule_id", "rule_config"), True),
        ],
    )

    result = RESULT(
        http_code=0,
        msg="Nothing to be done",
        content="",
        etag="",
        failed=False,
        changed=False,
    )

    notification_rule = NotificationRuleAPI(module)

    if module.params.get("state") == "present":
        if notification_rule.rule_id and notification_rule.current.http_code == 200:
            # Rule exists, check if update is needed
            content = notification_rule.current.content
            if isinstance(content, bytes):
                content = content.decode("utf-8")
            if changes_detected(module, json.loads(content)):
                result = notification_rule.put()
            else:
                result = notification_rule.current._replace(
                    msg="Notification rule already exists with the desired parameters.",
                    changed=False,
                )
        elif notification_rule.rule_id and notification_rule.current.http_code == 404:
            # rule_id provided but rule doesn't exist
            result = RESULT(
                http_code=404,
                msg="The provided rule_id was not found.",
                content="",
                etag="",
                failed=True,
                changed=False,
            )
        else:
            # No rule found, create new
            result = notification_rule.post()

    if module.params.get("state") == "absent":
        if notification_rule.current.http_code == 200:
            result = notification_rule.delete()
        elif notification_rule.current.http_code == 404:
            result = RESULT(
                http_code=0,
                msg="Notification rule already absent.",
                content="",
                etag="",
                failed=False,
                changed=False,
            )

    result_dict = result_as_dict(result)
    if result.content:
        try:
            content = result.content
            if isinstance(content, bytes):
                content = content.decode("utf-8")
            result_dict["content"] = json.loads(content)
        except (json.JSONDecodeError, AttributeError):
            pass

    module.exit_json(**result_dict)


def main():
    run_module()


if __name__ == "__main__":
    main()

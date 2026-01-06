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

version_added: "7.2.0"

description:
- Manage notification rules in Checkmk.
- Create, update, and delete notification rules for various notification methods.
- When I(rule_id) is not provided, the module will try to find an existing rule
  by matching the I(description) field in I(rule_properties).
- Requires Checkmk >= 2.3.0p42 or >= 2.4.0p22 for minimal configuration support.

extends_documentation_fragment:
    - checkmk.general.common
    - checkmk.general.notification_options

author:
    - Nicolas Brainez (@nicoske)
"""

EXAMPLES = r"""
# Create an HTML email notification rule with minimal configuration
- name: "Create email notification rule"
  checkmk.general.notification:
    server_url: "http://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    rule_config:
      rule_properties:
        description: "Notify admins on critical issues"
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

- name: Show the ID of the new notification rule
  ansible.builtin.debug:
    msg: "RULE ID: {{ notification_result.content.id }}"

# Create a Slack notification rule
- name: "Create Slack notification rule"
  checkmk.general.notification:
    server_url: "http://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    rule_config:
      rule_properties:
        description: "Slack notifications for critical alerts"
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

# Create a Microsoft Teams notification rule
- name: "Create Microsoft Teams notification rule"
  checkmk.general.notification:
    server_url: "http://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    rule_config:
      rule_properties:
        description: "Teams notifications for critical alerts"
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

# Update an existing notification rule by rule_id
- name: "Update notification rule"
  checkmk.general.notification:
    server_url: "http://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    rule_id: "{{ notification_result.content.id }}"
    rule_config:
      rule_properties:
        description: "Updated notification rule description"
      notification_method:
        notify_plugin:
          option: "create_notification_with_the_following_parameters"
          plugin_params:
            plugin_name: "mail"
    state: "present"

# Delete a notification rule by rule_id
- name: "Delete notification rule"
  checkmk.general.notification:
    server_url: "http://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    rule_id: "{{ notification_result.content.id }}"
    state: "absent"

# Delete a notification rule by description (no rule_id needed)
- name: "Delete notification rule by description"
  checkmk.general.notification:
    server_url: "http://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    rule_config:
      rule_properties:
        description: "Notify admins on critical issues"
    state: "absent"
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
    404: (False, False, "Not Found: The requested object has not been found."),
}

DISABLED = {"state": "disabled"}

DEFAULT_MAIL_PLUGIN_PARAMS = {
    "from_details": DISABLED,
    "reply_to": DISABLED,
    "subject_for_host_notifications": DISABLED,
    "subject_for_service_notifications": DISABLED,
    "send_separate_notification_to_every_recipient": DISABLED,
    "sort_order_for_bulk_notifications": DISABLED,
    "info_to_be_displayed_in_the_email_body": DISABLED,
    "insert_html_section_between_body_and_table": DISABLED,
    "url_prefix_for_links_to_checkmk": DISABLED,
    "display_graphs_among_each_other": DISABLED,
    "enable_sync_smtp": DISABLED,
    "graphs_per_notification": DISABLED,
    "bulk_notifications_with_graphs": DISABLED,
}

DEFAULT_SLACK_PLUGIN_PARAMS = {
    "url_prefix_for_links_to_checkmk": DISABLED,
    "disable_ssl_cert_verification": DISABLED,
    "http_proxy": DISABLED,
}

DEFAULT_MSTEAMS_PLUGIN_PARAMS = {
    "host_title": DISABLED,
    "service_title": DISABLED,
    "host_summary": DISABLED,
    "service_summary": DISABLED,
    "host_details": DISABLED,
    "service_details": DISABLED,
    "affected_host_groups": DISABLED,
    "url_prefix_for_links_to_checkmk": DISABLED,
    "http_proxy": DISABLED,
}

PLUGIN_DEFAULTS = {
    "mail": DEFAULT_MAIL_PLUGIN_PARAMS,
    "slack": DEFAULT_SLACK_PLUGIN_PARAMS,
    "msteams": DEFAULT_MSTEAMS_PLUGIN_PARAMS,
}

DEFAULT_CONTACT_SELECTION = {
    "all_contacts_of_the_notified_object": DISABLED,
    "all_users": DISABLED,
    "all_users_with_an_email_address": DISABLED,
    "the_following_users": DISABLED,
    "members_of_contact_groups": DISABLED,
    "explicit_email_addresses": DISABLED,
    "restrict_by_custom_macros": DISABLED,
    "restrict_by_contact_groups": DISABLED,
}

DEFAULT_CONDITIONS = {
    "match_sites": DISABLED,
    "match_folder": DISABLED,
    "match_host_tags": DISABLED,
    "match_host_labels": DISABLED,
    "match_host_groups": DISABLED,
    "match_hosts": DISABLED,
    "match_exclude_hosts": DISABLED,
    "match_service_labels": DISABLED,
    "match_service_groups": DISABLED,
    "match_exclude_service_groups": DISABLED,
    "match_service_groups_regex": DISABLED,
    "match_exclude_service_groups_regex": DISABLED,
    "match_services": DISABLED,
    "match_exclude_services": DISABLED,
    "match_check_types": DISABLED,
    "match_plugin_output": DISABLED,
    "match_contact_groups": DISABLED,
    "match_service_levels": DISABLED,
    "match_only_during_time_period": DISABLED,
    "match_host_event_type": DISABLED,
    "match_service_event_type": DISABLED,
    "restrict_to_notification_numbers": DISABLED,
    "throttle_periodic_notifications": DISABLED,
    "match_notification_comment": DISABLED,
    "event_console_alerts": DISABLED,
}


def merge_with_defaults(rule_config):
    """Merge user-provided rule_config with defaults for missing fields."""
    if not rule_config:
        return rule_config

    result = dict(rule_config)

    # Merge contact_selection with defaults
    if result.get("contact_selection"):
        merged_contacts = dict(DEFAULT_CONTACT_SELECTION)
        merged_contacts.update(result["contact_selection"])
        result["contact_selection"] = merged_contacts
    else:
        result["contact_selection"] = dict(DEFAULT_CONTACT_SELECTION)

    # Merge conditions with defaults
    if result.get("conditions"):
        merged_conditions = dict(DEFAULT_CONDITIONS)
        merged_conditions.update(result["conditions"])
        result["conditions"] = merged_conditions
    else:
        result["conditions"] = dict(DEFAULT_CONDITIONS)

    # Merge plugin_params with defaults based on plugin_name
    notification_method = result.get("notification_method")
    if notification_method:
        notify_plugin = notification_method.get("notify_plugin")
        if notify_plugin:
            plugin_params = notify_plugin.get("plugin_params")
            if plugin_params:
                plugin_name = plugin_params.get("plugin_name")
                if plugin_name in PLUGIN_DEFAULTS:
                    merged_params = dict(PLUGIN_DEFAULTS[plugin_name])
                    merged_params.update(plugin_params)
                    result["notification_method"] = dict(notification_method)
                    result["notification_method"]["notify_plugin"] = dict(notify_plugin)
                    result["notification_method"]["notify_plugin"][
                        "plugin_params"
                    ] = merged_params

    return result


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
        rule_config = merge_with_defaults(self.params.get("rule_config"))
        data = {"rule_config": rule_config}

        return self._fetch(
            endpoint="/domain-types/notification_rule/collections/all",
            data=data,
            method="POST",
        )

    def put(self):
        self.headers["If-Match"] = self.current.etag
        rule_config = merge_with_defaults(self.params.get("rule_config"))
        data = {"rule_config": rule_config}

        return self._fetch(
            endpoint="/objects/notification_rule/%s" % self.rule_id,
            data=data,
            method="PUT",
        )

    def delete(self):
        self.headers["If-Match"] = self.current.etag

        return self._fetch(
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
            if changes_detected(
                module, json.loads(notification_rule.current.content.decode("utf-8"))
            ):
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

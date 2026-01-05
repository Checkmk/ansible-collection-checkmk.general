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

version_added: "6.5.0"

description:
- Manage notification rules in Checkmk.
- Create, update, and delete notification rules for various notification methods.

extends_documentation_fragment: [checkmk.general.common]

options:
    rule_id:
        description:
            - The unique identifier of the notification rule.
            - Required when updating or deleting an existing rule.
            - If not provided when state is present, a new rule will be created.
        required: false
        type: str

    rule_config:
        description:
            - The complete notification rule configuration.
            - Required when state is present.
            - This should match the structure returned by the Checkmk API.
        required: false
        type: dict
        suboptions:
            rule_properties:
                description: Properties of the notification rule.
                type: dict
            notification_method:
                description: The notification method configuration including plugin and bulking settings.
                type: dict
            contact_selection:
                description: Selection of contacts to notify.
                type: dict
                suboptions:
                    all_contacts_of_the_notified_object:
                        description: Notify all contacts of the object.
                        type: dict
                    all_users:
                        description: Notify all users.
                        type: dict
                    all_users_with_an_email_address:
                        description: Notify all users with an email address.
                        type: dict
                    the_following_users:
                        description: Notify specific users.
                        type: dict
                    members_of_contact_groups:
                        description: Notify members of contact groups.
                        type: dict
                    explicit_email_addresses:
                        description: Notify explicit email addresses.
                        type: dict
                    restrict_by_custom_macros:
                        description: Restrict by custom macros.
                        type: dict
                    restrict_by_contact_groups:
                        description: Restrict by contact groups.
                        type: dict
            conditions:
                description: Conditions for when the rule applies.
                type: dict
                suboptions:
                    match_sites:
                        description: Match specific sites.
                        type: dict
                    match_folder:
                        description: Match specific folder.
                        type: dict
                    match_host_tags:
                        description: Match host tags.
                        type: dict
                    match_host_labels:
                        description: Match host labels.
                        type: dict
                    match_host_groups:
                        description: Match host groups.
                        type: dict
                    match_hosts:
                        description: Match specific hosts.
                        type: dict
                    match_exclude_hosts:
                        description: Exclude specific hosts.
                        type: dict
                    match_service_labels:
                        description: Match service labels.
                        type: dict
                    match_service_groups:
                        description: Match service groups.
                        type: dict
                    match_exclude_service_groups:
                        description: Exclude service groups.
                        type: dict
                    match_service_groups_regex:
                        description: Match service groups by regex.
                        type: dict
                    match_exclude_service_groups_regex:
                        description: Exclude service groups by regex.
                        type: dict
                    match_services:
                        description: Match specific services by regex.
                        type: dict
                    match_exclude_services:
                        description: Exclude specific services.
                        type: dict
                    match_check_types:
                        description: Match check types.
                        type: dict
                    match_plugin_output:
                        description: Match plugin output.
                        type: dict
                    match_contact_groups:
                        description: Match contact groups.
                        type: dict
                    match_service_levels:
                        description: Match service levels.
                        type: dict
                    match_only_during_time_period:
                        description: Match only during time period.
                        type: dict
                    match_host_event_type:
                        description: Match host event types.
                        type: dict
                    match_service_event_type:
                        description: Match service event types.
                        type: dict
                    restrict_to_notification_numbers:
                        description: Restrict to notification numbers.
                        type: dict
                    throttle_periodic_notifications:
                        description: Throttle periodic notifications.
                        type: dict
                    match_notification_comment:
                        description: Match notification comment.
                        type: dict
                    event_console_alerts:
                        description: Event console alerts.
                        type: dict

    state:
        description: The desired state of the notification rule.
        required: true
        choices: ["present", "absent"]
        type: str

author:
    - Nicolas Brainez (@nicoske)
"""

EXAMPLES = r"""
# Create an HTML email notification rule
- name: "Create email notification rule"
  checkmk.general.notification:
    server_url: "http://myserver/"
    site: "mysite"
    automation_user: "myuser"
    automation_secret: "mysecret"
    rule_config:
      rule_properties:
        description: "Notify admins on critical issues"
        comment: "Managed by Ansible"
        documentation_url: ""
        do_not_apply_this_rule:
          state: "disabled"
        allow_users_to_deactivate:
          state: "enabled"
      notification_method:
        notify_plugin:
          option: "create_notification_with_the_following_parameters"
          plugin_params:
            plugin_name: "mail"
            from_details:
              state: "disabled"
            reply_to:
              state: "disabled"
            subject_for_host_notifications:
              state: "disabled"
            subject_for_service_notifications:
              state: "disabled"
            sort_order_for_bulk_notifications:
              state: "disabled"
            send_separate_notification_to_every_recipient:
              state: "disabled"
            info_to_be_displayed_in_the_email_body:
              state: "disabled"
            insert_html_section_between_body_and_table:
              state: "disabled"
            url_prefix_for_links_to_checkmk:
              state: "disabled"
            enable_sync_smtp:
              state: "disabled"
            display_graphs_among_each_other:
              state: "disabled"
            graphs_per_notification:
              state: "disabled"
            bulk_notifications_with_graphs:
              state: "disabled"
        notification_bulking:
          state: "disabled"
      contact_selection:
        all_contacts_of_the_notified_object:
          state: "enabled"
        all_users:
          state: "disabled"
        all_users_with_an_email_address:
          state: "disabled"
        the_following_users:
          state: "disabled"
        members_of_contact_groups:
          state: "disabled"
        explicit_email_addresses:
          state: "disabled"
        restrict_by_custom_macros:
          state: "disabled"
        restrict_by_contact_groups:
          state: "disabled"
      conditions:
        match_sites:
          state: "disabled"
        match_folder:
          state: "disabled"
        match_host_tags:
          state: "disabled"
        match_host_labels:
          state: "disabled"
        match_host_groups:
          state: "disabled"
        match_hosts:
          state: "disabled"
        match_exclude_hosts:
          state: "disabled"
        match_service_labels:
          state: "disabled"
        match_service_groups:
          state: "disabled"
        match_exclude_service_groups:
          state: "disabled"
        match_service_groups_regex:
          state: "disabled"
        match_exclude_service_groups_regex:
          state: "disabled"
        match_services:
          state: "disabled"
        match_exclude_services:
          state: "disabled"
        match_check_types:
          state: "disabled"
        match_plugin_output:
          state: "disabled"
        match_contact_groups:
          state: "disabled"
        match_service_levels:
          state: "disabled"
        match_only_during_time_period:
          state: "disabled"
        match_host_event_type:
          state: "disabled"
        match_service_event_type:
          state: "disabled"
        restrict_to_notification_numbers:
          state: "disabled"
        throttle_periodic_notifications:
          state: "disabled"
        match_notification_comment:
          state: "disabled"
        event_console_alerts:
          state: "disabled"
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
    automation_user: "myuser"
    automation_secret: "mysecret"
    rule_config:
      rule_properties:
        description: "Slack notifications for critical alerts"
        comment: "Managed by Ansible"
        documentation_url: ""
        do_not_apply_this_rule:
          state: "disabled"
        allow_users_to_deactivate:
          state: "enabled"
      notification_method:
        notify_plugin:
          option: "create_notification_with_the_following_parameters"
          plugin_params:
            plugin_name: "slack"
            webhook_url:
              option: "explicit"
              url: "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
            url_prefix_for_links_to_checkmk:
              state: "disabled"
            disable_ssl_cert_verification:
              state: "disabled"
            http_proxy:
              state: "disabled"
        notification_bulking:
          state: "disabled"
      contact_selection:
        all_contacts_of_the_notified_object:
          state: "enabled"
        all_users:
          state: "disabled"
        all_users_with_an_email_address:
          state: "disabled"
        the_following_users:
          state: "disabled"
        members_of_contact_groups:
          state: "disabled"
        explicit_email_addresses:
          state: "disabled"
        restrict_by_custom_macros:
          state: "disabled"
        restrict_by_contact_groups:
          state: "disabled"
      conditions:
        match_sites:
          state: "disabled"
        match_folder:
          state: "disabled"
        match_host_tags:
          state: "disabled"
        match_host_labels:
          state: "disabled"
        match_host_groups:
          state: "disabled"
        match_hosts:
          state: "disabled"
        match_exclude_hosts:
          state: "disabled"
        match_service_labels:
          state: "disabled"
        match_service_groups:
          state: "disabled"
        match_exclude_service_groups:
          state: "disabled"
        match_service_groups_regex:
          state: "disabled"
        match_exclude_service_groups_regex:
          state: "disabled"
        match_services:
          state: "disabled"
        match_exclude_services:
          state: "disabled"
        match_check_types:
          state: "disabled"
        match_plugin_output:
          state: "disabled"
        match_contact_groups:
          state: "disabled"
        match_service_levels:
          state: "disabled"
        match_only_during_time_period:
          state: "disabled"
        match_host_event_type:
          state: "disabled"
        match_service_event_type:
          state: "disabled"
        restrict_to_notification_numbers:
          state: "disabled"
        throttle_periodic_notifications:
          state: "disabled"
        match_notification_comment:
          state: "disabled"
        event_console_alerts:
          state: "disabled"
    state: "present"

# Create a Microsoft Teams notification rule
- name: "Create Microsoft Teams notification rule"
  checkmk.general.notification:
    server_url: "http://myserver/"
    site: "mysite"
    automation_user: "myuser"
    automation_secret: "mysecret"
    rule_config:
      rule_properties:
        description: "Teams notifications for critical alerts"
        comment: "Managed by Ansible"
        documentation_url: ""
        do_not_apply_this_rule:
          state: "disabled"
        allow_users_to_deactivate:
          state: "enabled"
      notification_method:
        notify_plugin:
          option: "create_notification_with_the_following_parameters"
          plugin_params:
            plugin_name: "msteams"
            webhook_url:
              option: "explicit"
              url: "https://outlook.office.com/webhook/YOUR/WEBHOOK/URL"
            host_title:
              state: "disabled"
            service_title:
              state: "disabled"
            host_summary:
              state: "disabled"
            service_summary:
              state: "disabled"
            host_details:
              state: "disabled"
            service_details:
              state: "disabled"
            affected_host_groups:
              state: "disabled"
            url_prefix_for_links_to_checkmk:
              state: "disabled"
            http_proxy:
              state: "disabled"
        notification_bulking:
          state: "disabled"
      contact_selection:
        all_contacts_of_the_notified_object:
          state: "enabled"
        all_users:
          state: "disabled"
        all_users_with_an_email_address:
          state: "disabled"
        the_following_users:
          state: "disabled"
        members_of_contact_groups:
          state: "disabled"
        explicit_email_addresses:
          state: "disabled"
        restrict_by_custom_macros:
          state: "disabled"
        restrict_by_contact_groups:
          state: "disabled"
      conditions:
        match_sites:
          state: "disabled"
        match_folder:
          state: "disabled"
        match_host_tags:
          state: "disabled"
        match_host_labels:
          state: "disabled"
        match_host_groups:
          state: "disabled"
        match_hosts:
          state: "disabled"
        match_exclude_hosts:
          state: "disabled"
        match_service_labels:
          state: "disabled"
        match_service_groups:
          state: "disabled"
        match_exclude_service_groups:
          state: "disabled"
        match_service_groups_regex:
          state: "disabled"
        match_exclude_service_groups_regex:
          state: "disabled"
        match_services:
          state: "disabled"
        match_exclude_services:
          state: "disabled"
        match_check_types:
          state: "disabled"
        match_plugin_output:
          state: "disabled"
        match_contact_groups:
          state: "disabled"
        match_service_levels:
          state: "disabled"
        match_only_during_time_period:
          state: "disabled"
        match_host_event_type:
          state: "disabled"
        match_service_event_type:
          state: "disabled"
        restrict_to_notification_numbers:
          state: "disabled"
        throttle_periodic_notifications:
          state: "disabled"
        match_notification_comment:
          state: "disabled"
        event_console_alerts:
          state: "disabled"
    state: "present"

# Update an existing notification rule
- name: "Update notification rule"
  checkmk.general.notification:
    server_url: "http://myserver/"
    site: "mysite"
    automation_user: "myuser"
    automation_secret: "mysecret"
    rule_id: "{{ notification_result.content.id }}"
    rule_config:
      rule_properties:
        description: "Updated notification rule description"
        comment: "Updated by Ansible"
        documentation_url: ""
        do_not_apply_this_rule:
          state: "disabled"
        allow_users_to_deactivate:
          state: "enabled"
      # ... rest of the configuration
    state: "present"

# Delete a notification rule
- name: "Delete notification rule"
  checkmk.general.notification:
    server_url: "http://myserver/"
    site: "mysite"
    automation_user: "myuser"
    automation_secret: "mysecret"
    rule_id: "{{ notification_result.content.id }}"
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
    if "contact_selection" in result:
        merged_contacts = dict(DEFAULT_CONTACT_SELECTION)
        merged_contacts.update(result["contact_selection"])
        result["contact_selection"] = merged_contacts
    else:
        result["contact_selection"] = dict(DEFAULT_CONTACT_SELECTION)

    # Merge conditions with defaults
    if "conditions" in result:
        merged_conditions = dict(DEFAULT_CONDITIONS)
        merged_conditions.update(result["conditions"])
        result["conditions"] = merged_conditions
    else:
        result["conditions"] = dict(DEFAULT_CONDITIONS)

    return result


class NotificationRuleAPI(CheckmkAPI):
    def __init__(self, module):
        super().__init__(module)
        self.rule_id = self.params.get("rule_id")

        # Get current notification rule if rule_id is provided
        if self.rule_id:
            self.current = self._fetch(
                code_mapping=HTTP_CODES_GET,
                endpoint="/objects/notification_rule/%s" % self.rule_id,
                method="GET",
            )
        else:
            self.current = RESULT(
                http_code=404,
                msg="No rule_id provided",
                content="",
                etag="",
                failed=False,
                changed=False,
            )

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


def changes_detected(module, current):
    desired_config = merge_with_defaults(module.params.get("rule_config"))
    if not desired_config:
        return False

    current_config = current.get("extensions", {}).get("rule_config", {})

    # Compare rule_properties
    desired_props = desired_config.get("rule_properties", {})
    current_props = current_config.get("rule_properties", {})
    if desired_props.get("description") != current_props.get("description"):
        return True
    if desired_props.get("comment") != current_props.get("comment"):
        return True

    # Compare notification_method
    desired_method = desired_config.get("notification_method", {})
    current_method = current_config.get("notification_method", {})
    if desired_method != current_method:
        return True

    # Compare contact_selection
    desired_contacts = desired_config.get("contact_selection", {})
    current_contacts = current_config.get("contact_selection", {})
    if desired_contacts != current_contacts:
        return True

    # Compare conditions
    desired_conditions = desired_config.get("conditions", {})
    current_conditions = current_config.get("conditions", {})
    if desired_conditions != current_conditions:
        return True

    return False


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
            ("state", "absent", ("rule_id",)),
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
            # No rule_id provided, create new rule
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

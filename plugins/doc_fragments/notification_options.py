from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = r"""
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
    """

#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2025, Robin Gierse <robin.gierse@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ldap
short_description: Manage LDAP connectors.
version_added: "6.1.0"
description:
  - Manage LDAP connectors, including creation, updating, and deletion.
extends_documentation_fragment: [checkmk.general.common]
options:
    ldap_config:
        description: Configuration parameters for the LDAP.
        type: dict
        required: true
        suboptions:
            general_properties:
                description: General properties of an LDAP connection.
                type: dict
                required: true
                suboptions:
                    id:
                        description: An LDAP connection ID string.
                        type: str
                        required: true
                    description:
                        description: Add a title or describe this rule.
                        default: ""
                        type: str
                    comment:
                        description: An optional comment to explain the purpose.
                        default: ""
                        type: str
                    documentation_url:
                        description: Add a documentation URL for this rule.
                        default: ""
                        type: str
                    rule_activation:
                        description:
                            - Selecting 'deactivated' will disable the rule, but it will
                            - remain in the configuration.
                        type: str
                        choices:
                            - activated
                            - deactivated
            ldap_connection:
                description: The LDAP connection configuration.
                type: dict
                required: true
                default: {}
                suboptions:
                    directory_type:
                        description:
                            - The credentials to be used to connect to the LDAP server. The used
                            - account must not be allowed to do any changes in the directory the
                            - whole connection is read only. In some environment an anonymous
                            - connect/bind is allowed, in this case you don't have to configure
                            - anything here.It must be possible to list all needed user and group
                            - objects from the directory.
                        type: dict
                        suboptions:
                            type:
                                description: Select the software the LDAP directory is based on.
                                type: str
                                choices:
                                    - "active_directory_manual"
                                    - "active_directory_automatic"
                                    - "open_ldap"
                                    - "389_directory_server"
                                default: "active_directory_manual"
                            ldap_server:
                                description:
                                    - Set the host address of the LDAP server. Might be an IP
                                    - address or resolvable host name.
                                type: str
                            failover_servers:
                                description:
                                    - When the connection to the first server fails with connect
                                    - specific errors like timeouts or some other network related
                                    - problems, the connect mechanism will try to use this server
                                    - instead of the server configured above. If you use persistent
                                    - connections (default), the connection is being used until the
                                    - LDAP is not reachable or the local webserver is restarted.
                                type: list
                                elements: str
                            domain:
                                description:
                                    - Configure the DNS domain name of your Active directory domain
                                    - here, Checkmk will then query this domain for it's closest
                                    - domain controller to communicate with.
                                type: str
                    bind_credentials:
                        description: The credentials used to connect to the LDAP server.
                        type: dict
                        suboptions:
                            type:
                                description:
                                    - Whether to take the password from the password store or to
                                    - provide it explicitly.
                                type: str
                                choices:
                                    - "explicit"
                                    - "store"
                                default: "explicit"
                            bind_dn:
                                description:
                                    - The distinguished name of the user account which is used to
                                    - bind to the LDAP server. This user account must have read
                                    - access to the LDAP directory.
                                type: str
                            password_store_id:
                                description: The ID of the password inside the password store.
                                type: str
                            explicit_password:
                                description: The explicit password.
                                type: str
                    ssl_encryption:
                        description:
                            - Connect to the LDAP server with a SSL encrypted connection. The
                            - trusted certificates authorities configured in Checkmk will be used
                            - to validate the certificate provided by the LDAP server.
                        type: str
                        choices:
                            - "disable_ssl"
                            - "enable_ssl"
                        default: "disable_ssl"
                    tcp_port:
                        description: The TCP port to be used to connect to the LDAP server.
                        type: int
                    connect_timeout:
                        description:
                            - Timeout for the initial connection to the LDAP server in seconds.
                        type: int
                    ldap_version:
                        description:
                            - The selected LDAP version the LDAP server is serving. Most modern
                            - servers use LDAP version 3.
                        type: int
                        choices:
                            - 2
                            - 3
                    page_size:
                        description:
                            - LDAP searches can be performed in paginated mode, for example to
                            - improve the performance. This enables pagination and configures the
                            - size of the pages.
                        type: int
                    response_timeout:
                        description: Timeout for the reply coming from the LDAP server in seconds.
                        type: int
                    connection_suffix:
                        description:
                            - The LDAP connection suffix can be used to distinguish equal named
                            - objects (name conflicts), for example user accounts, from different
                            - LDAP connections.
                        type: str
            users:
                description: The LDAP user configuration.
                type: dict
                suboptions:
                    user_base_dn:
                        description:
                            - Give a base distinguished name here. All user accounts to
                            - synchronize must be located below this one.
                        type: str
                    search_scope:
                        description: Scope to be used in LDAP searches.
                        type: str
                        choices:
                            - "search_whole_subtree"
                            - "search_only_base_dn_entry"
                            - "search_all_one_level_below_base_dn"
                        default: "search_whole_subtree"
                    search_filter:
                        description: Optional LDAP filter.
                        type: str
                        default: ""
                    filter_group:
                        description: DN of a group object which is used to filter the users.
                        type: str
                        default: ""
                    user_id_attribute:
                        description: User ID attribute.
                        type: str
                        default: ""
                    user_id_case:
                        description:
                            - Convert imported User-IDs to lower case during synchronization or
                            - leave as is.
                        type: str
                        choices:
                            - "dont_convert_to_lowercase"
                            - "convert_to_lowercase"
                        default: "dont_convert_to_lowercase"
                    umlauts_in_user_ids:
                        description: 
                            - Checkmk does not support special characters in User-IDs. However, to
                            - deal with LDAP users having umlauts in their User-IDs you previously
                            - had the choice to replace umlauts with other characters. This option
                            - is still available for backward compatibility, but you are advised
                            - to use the 'keep_umlauts' option for new installations.
                        type: str
                        choices:
                            - "keep_umlauts"
                            - "replace_umlauts"
                        default: "keep_umlauts"
                    create_users:
                        description: Create user accounts during sync or on the first login.
                        type: str
                        choices:
                            - "on_login"
                            - "on_sync"
                        default: "on_login"
            groups:
                description: The LDAP group configuration.
                type: dict
                suboptions:
                    group_base_dn:
                        description:
                            - Give a base distinguished name here. All group accounts to
                            - synchronize must be located below this one.
                        type: str
                    search_scope:
                        description: Scope to be used in LDAP searches.
                        type: str
                        choices:
                            - "search_whole_subtree"
                            - "search_only_base_dn_entry"
                            - "search_all_one_level_below_base_dn"
                        default: "search_whole_subtree"
                    search_filter:
                        description:
                            - Define an optional LDAP filter which is used during group related
                            - LDAP searches. It can be used to only handle a subset of the groups
                            - below the given group base DN.
                        type: str
                        default: ""
                    member_attribute:
                        description: Member attribute.
                        type: str
                        default: ""
            sync_plugins:
                description: The LDAP sync plug-ins configuration.
                type: dict
                suboptions:
                    alias:
                        description:
                            - Enables and populates the alias attribute of the Setup user by
                            - synchronizing an attribute from the LDAP user account. By default
                            - the LDAP attribute cn is used.
                        type: str
                        default: ""
                    authentication_expiration:
                        description:
                            - This plug-in when enabled fetches all information which is needed to
                            - check whether or not an already authenticated user should be
                            - deauthenticated, e.g. because the password has changed in LDAP or
                            - the account has been locked.
                        type: str
                        default: ""
                    disable_notifications:
                        description:
                            - When this option is enabled you will not get any alerts or other
                            - notifications via email, SMS or similar. This overrides all other
                            - notification settings and rules, so make sure that you know what
                            - you do. Moreover you can specify a time range where no notifications
                            - are generated.
                        type: str
                        default: ""
                    email_address:
                        description:
                            - Synchronizes the email of the LDAP user account into Checkmk when
                            - enabled
                        type: str
                        default: ""
                    mega_menu_icons:
                        description:
                            - When enabled, in the mega menus you can select between two
                            - options: Have a green icon only for the headlines – the 'topics' –
                            - for lean design. Or have a colored icon for every entry so that over
                            - time you can zoom in more quickly to a specific entry.
                        type: str
                        default: ""
                    navigation_bar_icons:
                        description:
                            - With this option enabled you can define if icons in the navigation
                            - bar should show a title or not. This gives you the possibility to
                            - save some space in the UI.
                        type: str
                        default: ""
                    pager:
                        description:
                            - When enabled, this plug-in synchronizes a field of the users LDAP
                            - account to the pager attribute of the Setup user accounts, which is
                            - then forwarded to the monitoring core and can be used for
                            - notifications. By default the LDAP attribute mobile is used.
                        type: str
                        default: ""
                    show_mode:
                        description:
                            - In some places like e.g. the main menu Checkmk divides features,
                            - filters, input fields etc. in two categories, showing more or less
                            - entries. With this option you can set a default mode for unvisited
                            - menus. Alternatively, you can enforce to show more, so that the
                            - round button with the three dots is not shown at all.
                        type: str
                        default: ""
                    ui_sidebar_position:
                        description: The sidebar position 
                        type: str
                        default: ""
                    start_url:
                        description: The start URL to display in main frame.
                        type: str
                        default: ""
                    temperature_unit:
                        description:
                            - Set the temperature unit used for graphs and perfometers. The default
                            - unit can be configured here.
                        type: str
                        default: ""
                    ui_theme:
                        description: The user interface theme
                        type: str
                        default: ""
                    visibility_of_hosts_or_services:
                        description:
                            - When this option is checked, the status GUI will only display hosts
                            - and services that the user is a contact for - even they have the
                            - permission for seeing all objects.
                        type: str
                        default: ""
                    contact_group_membership:
                        description:
                            - This plug-in allows you to synchronize group memberships of the LDAP
                            - user account into the contact groups of the Checkmk user account.
                            - This allows you to use the group based permissions of your LDAP
                            - directory in Checkmk.
                        type: dict
                        suboptions:
                            handle_nested:
                                description:
                                    - Once you enable this option, this plug-in will not only
                                    - handle direct group memberships, instead it will also dig
                                    - into nested groups and treat the members of those groups as
                                    - contact group members as well. Please bear in mind that this
                                    - feature might increase the execution time of your LDAP sync.
                                type: bool
                                default: false
                            sync_from_other_connections:
                                description:
                                    - The LDAP attribute whose contents shall be synced into this
                                    - custom attribute.
                                type: list
                                elements: str
                                default: []
                    groups_to_custom_user_attributes:
                        description:
                            - This plug-in allows you to synchronize group memberships of the LDAP
                            - user account into the custom attributes of the Checkmk user account.
                            - This allows you to use the group based permissions of your LDAP
                            - directory in Checkmk.
                        type: dict
                        suboptions:
                            handle_nested:
                                description:
                                    - Once you enable this option, this plug-in will not only
                                    - handle direct group memberships, instead it will also dig
                                    - into nested groups and treat the members of those groups as
                                    - contact group members as well. Please bear in mind that this
                                    - feature might increase the execution time of your LDAP sync.
                                type: bool
                                default: false
                            sync_from_other_connections:
                                description:
                                    - The LDAP attribute whose contents shall be synced into this
                                    - custom attribute.
                                type: list
                                elements: str
                                default: []
                            groups_to_sync:
                                type: dict
                                suboptions:
                                    group_cn:
                                        description: The common name of the group.
                                        type: str
                                    attribute_to_set:
                                        description: The attribute to set
                                        type: str
                                    value:
                                        description: The value to set
                                        type: str
                    groups_to_roles:
                        description:
                            - Configures the roles of the user depending on its group memberships
                            - in LDAP. Please note: Additionally the user is assigned to the
                            - Default Roles. Deactivate them if unwanted.
                        type: dict
                        suboptions:
                            handle_nested:
                                description:
                                    - Once you enable this option, this plug-in will not only
                                    - handle direct group memberships, instead it will also dig
                                    - into nested groups and treat the members of those groups as
                                    - contact group members as well. Please bear in mind that this
                                    - feature might increase the execution time of your LDAP sync.
                                type: bool
                                default: false
                            roles_to_sync:
                                type: list
                                elements: dict
                                options:
                                    role:
                                        description: The role id as defined in Checkmk.
                                        type: str
                                    groups:
                                        type: list
                                        elements: dict
                                        options:
                                            group_dn:
                                                description:
                                                    - This group must be defined within the scope
                                                    - of the LDAP Group Settings
                                                type: str
                                            search_in:
                                                description:
                                                    - An existing ldap connection. Use
                                                    - 'this_connection' to select the current
                                                    - connection
                                                type: str
                                                default: "this_connection"
            other:
                description: Other config options for the LDAP connection.
                type: dict
                suboptions:
                    sync_interval:
                        type: dict
                        suboptions:
                            days:
                                description: The sync interval in days
                                type: int
                                default: 0
                            hours:
                                description: The sync interval in hours
                                type: int
                                default: 0
                            minutes:
                                description: The sync interval in minutes
                                type: int
                                default: 5
    state:
        description: Desired state of the LDAP.
        type: str
        choices:
        - present
        - absent
        default: present
author:
  - Lars Getwan (@lgetwan)
"""

EXAMPLES = r"""
- name: Create a LDAP configuration
  checkmk.general.ldap:
    server_url: "http://myserver/"
    site: "mysite"
    automation_auth_type: "bearer"
    automation_user: "myuser"
    automation_secret: "mysecret"
    ldap_config:
      general_properties:
        id: "test_ldap_defaults"
      ldap_connection:
        directory_type:
          type: "open_ldap"
          ldap_server: "my.ldap.server.tld"
    state: "present"
- name: Delete a LDAP configuration
  checkmk.general.ldap:
    server_url: "http://myserver/"
    site: "mysite"
    automation_auth_type: "bearer"
    automation_user: "myuser"
    automation_secret: "mysecret"
    ldap_config:
      id: "test_ldap_defaults"
    state: "absent"
- name: Create a complex LDAP connector
  checkmk.general.ldap:
    server_url: "http://myserver/"
    site: "mysite"
    automation_auth_type: "bearer"
    automation_user: "myuser"
    automation_secret: "mysecret"
    ldap_config:
      general_properties:
        id: "test_ldap_complex"
        rule_activation: activated
        comment: "complex"
        description: "really complex""
        documentation_url: "www.example.com"
      ldap_connection:
        directory_type:
          type: "open_ldap"
          ldap_server: "my.ldap.server.tld"
          failover_servers:
            - my2nd.ldap.server.tld
            - my3rd.ldap.server.tld
        bind_credentials:
          bind_dn: "ldapadmin"
          type: store
          password_store_id: "ldapadmin""
        ssl_encryption: enable_ssl
        tcp_port: 1234
        connect_timeout: 3
        ldap_version: 2
        page_size: 2000
        response_timeout: 8
      users:
        user_base_dn: "OU=Users,DC=example,DC=com"
        search_scope: search_whole_subtree
        search_filter: "(objectclass=inetOrgPerson)"
        user_id_attribute: uid
        user_id_case: convert_to_lowercase
        umlauts_in_user_ids: replace_umlauts
        create_users: on_sync
      groups:
        group_base_dn: "OU=Groups,DC=example,DC=com"
        search_scope: search_only_base_dn_entry
        search_filter: "(objectclass=posixGroup)"
        member_attribute: "uniquemember"
      sync_plugins:
        alias: blubb
        visibility_of_hosts_or_services: blobb
        contact_group_membership:
          handle_nested: true
          sync_from_other_connections: test_ldap_defaults
        groups_to_custom_user_attributes:
          handle_nested: true
          groups_to_sync:
            - group_cn: CN=megamenu,OU=Groups,DC=example,DC=com
              attribute_to_set: mega_menu_icons
              value: per_entry
        groups_to_roles:
          handle_nested: true
          roles_to_sync:
            - role: admin
              groups:
                - group_dn: CN=admins,OU=Groups,DC=example,DC=com
                  search_in: this_connection
    state: "present"
"""

RETURN = r"""
msg:
  description:
    - The output message that the module generates.
  type: str
  returned: always
http_code:
  description:
    - HTTP code returned by the Checkmk API.
  type: int
  returned: always
content:
  description:
    - Content of the LDAP object.
  returned: when state is present and LDAP created or updated.
  type: dict
diff:
  description:
    - The diff between the current and desired state.
  type: dict
  returned: when differences are detected or in diff mode
"""

import json

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.checkmk.general.plugins.module_utils.api import (
    CheckmkAPI,
)
from ansible_collections.checkmk.general.plugins.module_utils.differ import ConfigDiffer
from ansible_collections.checkmk.general.plugins.module_utils.logger import Logger
from ansible_collections.checkmk.general.plugins.module_utils.utils import (
    base_argument_spec,
    exit_module,
)

EXTEND_STATE = {
    "connection_suffix": "suffix",
    "connect_timeout": "seconds",
    "response_timeout": "seconds",
    "ldap_version": "version",
    "page_size": "size",
    "tcp_port": "port",
    "search_filter": "filter",
    "member_attribute": "attribute",
    "authentication_expiration": "attribute_to_sync",
    "disable_notifications": "attribute_to_sync",
    "mega_menu_icons": "attribute_to_sync",
    "navigation_bar_icons": "attribute_to_sync",
    "pager": "attribute_to_sync",
    "show_mode": "attribute_to_sync",
    "start_url": "attribute_to_sync",
    "temperature_unit": "attribute_to_sync",
    "ui_sidebar_position": "attribute_to_sync",
    "ui_theme": "attribute_to_sync",
    "visibility_of_hosts_or_services": "attribute_to_sync",
    "filter_group": "filter",
    "user_id_attribute": "attribute",
    "alias": "attribute_to_sync",
    "email_address": "attribute_to_sync",
    "bind_credentials": None,
    "contact_group_membership": None,
    "groups_to_custom_user_attributes": None,
    "groups_to_roles": None,
}

logger = Logger()


class LDAPHTTPCodes:
    """
    LDAPHTTPCodes defines the HTTP status codes and corresponding messages
    for LDAP operations such as GET, CREATE, EDIT, and DELETE.
    """

    get = {
        200: (False, False, "LDAP connection found, nothing changed"),
        404: (False, False, "LDAP connection not found"),
    }
    create = {
        200: (True, False, "LDAP connection created"),
        201: (True, False, "LDAP connection created"),
        204: (True, False, "LDAP connection created"),
        405: (False, True, "Method Not Allowed"),
    }
    edit = {
        200: (True, False, "LDAP connection modified"),
        405: (False, True, "Method Not Allowed"),
    }
    delete = {
        204: (True, False, "LDAP connection deleted"),
        405: (False, True, "Method Not Allowed"),
    }


class LDAPAPI(CheckmkAPI):
    """
    Manages LDAP operations via the Checkmk API.
    """

    def __init__(self, module):
        """
        Initializes the LDAPAPI class, retrieves the current state of the LDAP configuration.
        Args:
            module (AnsibleModule): The Ansible module object.
        """
        super().__init__(module)

        self.desired_state = self.params.get("state")

        error = self._verify_parameters()
        if error:
            exit_module(
                self.module,
                msg=error,
                failed=True,
                logger=logger,
            )

        if self.desired_state == "present":
            self.desired = self.ldap_config.copy()
            self.desired = self._set_defaults(self.desired)
            self.desired = self._extend_state_parameters(self.desired)

            #logger.debug("DESIRED: %s" % str(self.desired))

            ## Ensure 'comment' is not null
            #if (
            #    "comment" not in self.desired["general_properties"]
            #    or self.desired["general_properties"]["comment"] is None
            #):
            #    self.desired["general_properties"]["comment"] = ""

        self.state = None

        #logger.debug("headers1: %s" % str(self.headers))
        self._get_current()
        #logger.debug("headers2: %s" % str(self.headers))

        # Initialize the ConfigDiffer with desired and current configurations
        if self.desired_state == "present":
            self.differ = ConfigDiffer(self.desired, self.current)

    def _set_defaults(self, ldap_config):
        """
        Set some default values
        """
        ldap_connection = ldap_config.get("ldap_connection")

        # Directory type
        directory_type = ldap_connection.get("directory_type")
        d_type = directory_type.get("type", "active_directory_manual")
        if d_type == "active_directory_automatic":
            ldap_config["ldap_connection"]["directory_type"] = {
                "type": "active_directory_automatic",
                "domain": directory_type.get("domain"),
            }
        else:
            ldap_config["ldap_connection"]["directory_type"] = {
                "type": d_type,
                "ldap_server": directory_type.get("ldap_server"),
                "failover_servers": (
                    []
                    if not directory_type.get("failover_servers")
                    else directory_type.get("failover_servers")
                ),
            }

        return ldap_config

    def _extend_state_parameters(self, ldap_config):
        """
        Some Ansible parameters were simplified for a better Ansible experience.
        When sending them to the REST API, they have to be extended.
        Example:
            connect_timeout: 2
            =>
            connect_timeout: { "state": "enabled", "seconds": 2 }
        """

        def _extend_recursive(d):
            if type(d) == dict:
                to_be_deleted = []
                for k, v in d.items():
                    if type(v) == dict:
                        v = _extend_recursive(d[k])
                    if k in EXTEND_STATE:
                        if not v:
                            d[k] = {"state": "disabled"}
                            # to_be_deleted.append(k)
                        elif EXTEND_STATE[k]:
                            d[k] = {"state": "enabled", EXTEND_STATE[k]: v}
                        else:
                            d[k] = {"state": "enabled"}

                            if k == "bind_credentials":
                                d[k].update(v)
                                if v.get("type") == "store":
                                    del d[k]["explicit_password"]
                                else:
                                    del d[k]["password_store_id"]
                            elif k == "contact_group_membership":
                                d[k]["handle_nested"] = v.get("handle_nested", False)
                                d[k]["sync_from_other_connections"] = v.get(
                                    "sync_from_other_connections", []
                                )
                            elif k == "groups_to_custom_user_attributes":
                                d[k]["handle_nested"] = v.get("handle_nested", False)
                                d[k]["sync_from_other_connections"] = v.get(
                                    "sync_from_other_connections", []
                                )
                                d[k]["groups_to_sync"] = v.get("groups_to_sync", [])
                            elif k == "groups_to_roles":
                                #logger.debug("##### groups_to_roles: %s" % str(v))
                                d[k]["handle_nested"] = v.get("handle_nested", False)
                                # for role in v.get("roles_to_sync", []):
                                #    d[k][role.get("role")] = role.get("groups", [])
                for key in to_be_deleted:
                    del d[key]

            return d

        return _extend_recursive(ldap_config)

    def _verify_parameters(self):
        """
        Checks if all mandatory parameters are there and making sense.
        """
        ldap_config = self.params.get("ldap_config")
        if not ldap_config:
            return "Missing parameter 'ldap_config'."

        general_properties = ldap_config.get("general_properties")
        if not general_properties:
            return "Missing parameter 'general_properties' in ldap_config dictionary."

        self.id = general_properties.get("id")
        if not self.id:
            return "Missing parameter 'id' in general_properties dictionary."

        if self.desired_state == "present":
            ldap_connection = ldap_config.get("ldap_connection")
            if not ldap_connection:
                return "Missing parameter 'ldap_connection' in ldap_config dictionary."

            directory_type = ldap_connection.get("directory_type")
            if not directory_type:
                return "Missing parameter 'directory_type' in directory_type dictionary."

            if directory_type in [
                "active_directory_manual",
                "open_ldap",
                "389_directory_server",
            ] and not directory_type.get("type"):
                return "Directory type '%s' requires a parameter 'type'." % directory_type

            if directory_type == "active_directory_automatic" and not directory_type.get(
                "domain"
            ):
                return "Directory type 'active_directory_automatic' requires a parameter 'domain'."

        self.ldap_config = ldap_config

    def _get_current(self):
        """
        Retrieves the current state of the LDAP connection from the Checkmk API.
        """
        endpoint = self._build_endpoint(action="get")
        result = self._fetch(
            code_mapping=LDAPHTTPCodes.get,
            endpoint=endpoint,
            logger=logger,
            method="GET",
        )

        if result.http_code == 200:
            self.state = "present"
            self.headers['If-Match'] = result.etag.replace("\"", "")
            try:
                current_raw = json.loads(result.content)
                self.current = current_raw.get("extensions", {})
                self.current["id"] = current_raw.get("id")

            except json.JSONDecodeError:
                exit_module(
                    self.module,
                    msg="Failed to decode JSON response from API.",
                    content=result.content,
                    failed=True,
                    logger=logger,
                )
        else:
            self.state = "absent"
            self.current = {}

    def _build_endpoint(self, action="get"):
        """
        Builds the API endpoint URL for the LDAP configuration.
        Args:
            action (str): The action for which to build the endpoint. Options are 'create', 'get', 'edit', 'delete'.
        Returns:
            str: API endpoint URL.
        """
        if action == "create":
            return "/domain-types/ldap_connection/collections/all"
        elif action in ["get", "edit", "delete"]:
            return "/objects/ldap_connection/%s" % self.id
        else:
            exit_module(
                self.module,
                msg="Unsupported action '%s' for building endpoint." % action,
                failed=True,
                logger=logger,
            )

    def needs_update(self):
        """
        Determines whether an update to the LDAP configuration is needed.
        Returns:
            bool: True if changes are needed, False otherwise.
        """
        return self.differ.needs_update()

    def generate_diff(self, deletion=False):
        """
        Generates a diff between the current and desired state.
        Args:
            deletion (bool): Whether the diff is for a deletion.
        Returns:
            dict: Dictionary containing 'before' and 'after' states.
        """
        return self.differ.generate_diff(deletion)

    def _perform_action(self, action, method, data=None):
        """
        Helper method to perform CRUD actions.
        Args:
            action (str): The action being performed ('create', 'edit', 'delete').
            method (str): The HTTP method.
            data (dict, optional): The data to send with the request.
        Returns:
            dict: The result dictionary.
        """
        endpoint = self._build_endpoint(action=action)

        diff = None
        if self.module._diff:
            deletion_flag = action == "delete"
            diff = self.generate_diff(deletion=deletion_flag)

        if self.module.check_mode:
            action_msgs = {
                "create": "would be created",
                "edit": "would be modified",
                "delete": "would be deleted",
            }
            return dict(
                msg="LDAP configuration %s." % action_msgs.get(action, action),
                changed=True,  # Indicate that changes would occur
                diff=diff,
            )

        return self._fetch(
            code_mapping=getattr(LDAPHTTPCodes, action),
            endpoint=endpoint,
            data=data,
            logger=logger,
            method=method,
        )

    def create(self):
        """
        Creates a new LDAP configuration via the Checkmk API.
        Returns:
            dict: The result of the creation operation.
        """
        filtered_data = {k: v for k, v in self.desired.items() if v is not None}
        return self._perform_action(action="create", method="POST", data=filtered_data)

    def edit(self):
        """
        Updates an existing LDAP configuration via the Checkmk API.
        Returns:
            dict: The result of the update operation.
        """
        filtered_data = {k: v for k, v in self.desired.items() if v is not None}
        return self._perform_action(action="edit", method="PUT", data=filtered_data)

    def delete(self):
        """
        Deletes an existing LDAP configuration via the Checkmk API.
        Returns:
            dict: The result of the deletion operation.
        """
        return self._perform_action(action="delete", method="DELETE")


def run_module():
    """
    The main logic for the Ansible module.
    This function defines the module parameters, initializes the LDAPAPI, and performs
    the appropriate action (create or delete) based on the state of the LDAP configuration.
    Note: Update functionality is currently disabled due to the lack of a REST API endpoint for updates.
    Returns:
        None: The result is returned to Ansible via module.exit_json().
    """

    argument_spec = base_argument_spec()
    argument_spec.update(
        server_url=dict(type="str", required=True),
        site=dict(type="str", required=True),
        ldap_config=dict(
            type="dict",
            required=True,
            options={
                "general_properties": dict(
                    type="dict",
                    required=True,
                    options={
                        "rule_activation": dict(type="str", choices=[
                            "activated",
                            "deactivated" ], default="activated"),
                        "comment": dict(type="str", default=""),
                        "description": dict(type="str", default=""),
                        "documentation_url": dict(type="str", default=""),
                        "id": dict(type="str", required=True),
                    },
                ),
                "ldap_connection": dict(
                    type="dict",
                    default={},
                    options={
                        "directory_type": dict(
                            type="dict",
                            options={
                                "type": dict(
                                    type="str",
                                    default="active_directory_manual",
                                    choices=[
                                        "active_directory_manual",
                                        "active_directory_automatic",
                                        "open_ldap",
                                        "389_directory_server",
                                    ],
                                ),
                                "ldap_server": dict(type="str"),
                                "failover_servers": dict(type="list", elements="str"),
                                "domain": dict(type="str"),
                            },
                        ),
                        "bind_credentials": dict(
                            type="dict",
                            options={
                                "type": dict(
                                    type="str",
                                    default="explicit",
                                    choices=["explicit", "store"],
                                ),
                                "bind_dn": dict(type="str"),
                                "password_store_id": dict(type="str"),
                                "explicit_password": dict(type="str"),
                            },
                        ),
                        "ssl_encryption": dict(
                            type="str",
                            default="disable_ssl",
                            choices=["disable_ssl", "enable_ssl"],
                        ),
                        "tcp_port": dict(type="int"),
                        "connect_timeout": dict(type="int"),
                        "ldap_version": dict(type="int", choices=[2, 3]),
                        "page_size": dict(type="int"),
                        "response_timeout": dict(type="int"),
                        "connection_suffix": dict(type="str"),
                    },
                ),
                "users": dict(
                    type="dict",
                    default={
                        "user_base_dn": "",
                        "search_scope": "search_whole_subtree",
                        "search_filter": "",
                        "filter_group": "",
                        "user_id_attribute": "",
                        "user_id_case": "dont_convert_to_lowercase",
                        "umlauts_in_user_ids": "keep_umlauts",
                        "create_users": "on_login",
                    },
                    options={
                        "user_base_dn": dict(type="str", default=""),
                        "search_scope": dict(
                            type="str",
                            default="search_whole_subtree",
                            choices=[
                                "search_whole_subtree",
                                "search_only_base_dn_entry",
                                "search_all_one_level_below_base_dn",
                            ],
                        ),
                        "search_filter": dict(type="str", default=""),
                        "filter_group": dict(type="str", default=""),
                        "user_id_attribute": dict(type="str", default=""),
                        "user_id_case": dict(
                            type="str",
                            default="dont_convert_to_lowercase",
                            choices=[
                                "dont_convert_to_lowercase",
                                "convert_to_lowercase",
                            ],
                        ),
                        "umlauts_in_user_ids": dict(
                            type="str",
                            default="keep_umlauts",
                            choices=["keep_umlauts", "replace_umlauts"],
                        ),
                        "create_users": dict(
                            type="str",
                            choices=["on_login", "on_sync"],
                        ),
                    },
                ),
                "groups": dict(
                    type="dict",
                    default={
                        "group_base_dn": "",
                        "search_scope": "search_whole_subtree",
                        "search_filter": "",
                        "member_attribute": "",
                    },
                    options={
                        "group_base_dn": dict(type="str", default=""),
                        "search_scope": dict(
                            type="str",
                            default="search_whole_subtree",
                            choices=[
                                "search_whole_subtree",
                                "search_only_base_dn_entry",
                                "search_all_one_level_below_base_dn",
                            ],
                        ),
                        "search_filter": dict(type="str", default=""),
                        "member_attribute": dict(type="str"),
                    },
                ),
                "sync_plugins": dict(
                    type="dict",
                    default={
                        "alias": "",
                        "authentication_expiration": "",
                        "disable_notifications": "",
                        "email_address": "",
                        "mega_menu_icons": "",
                        "navigation_bar_icons": "",
                        "pager": "",
                        "show_mode": "",
                        "ui_sidebar_position": "",
                        "start_url": "",
                        "temperature_unit": "",
                        "ui_theme": "",
                        "visibility_of_hosts_or_services": "",
                        # "contact_group_membership": {},
                        # "groups_to_custom_user_attributes": {},
                        # "groups_to_roles": {},
                    },
                    options={
                        "alias": dict(type="str", default=""),
                        "authentication_expiration": dict(type="str", default=""),
                        "disable_notifications": dict(type="str", default=""),
                        "email_address": dict(type="str", default=""),
                        "mega_menu_icons": dict(type="str", default=""),
                        "navigation_bar_icons": dict(type="str", default=""),
                        "pager": dict(type="str", default=""),
                        "show_mode": dict(type="str", default=""),
                        "ui_sidebar_position": dict(type="str", default=""),
                        "start_url": dict(type="str", default=""),
                        "temperature_unit": dict(type="str", default=""),
                        "ui_theme": dict(type="str", default=""),
                        "visibility_of_hosts_or_services": dict(type="str", default=""),
                        "contact_group_membership": dict(
                            type="dict",
                            options={
                                "handle_nested": dict(type="bool", default=False),
                                "sync_from_other_connections": dict(
                                    type="list", elements="str", default=[]
                                ),
                            },
                        ),
                        "groups_to_custom_user_attributes": dict(
                            type="dict",
                            options={
                                "handle_nested": dict(type="bool", default=False),
                                "sync_from_other_connections": dict(
                                    type="list", elements="str", default=[]
                                ),
                                "groups_to_sync": dict(
                                    type="list",
                                    elements="dict",
                                    options={
                                        "group_cn": dict(type="str"),
                                        "attribute_to_set": dict(
                                            type="str",
                                        ),
                                        "value": dict(type="str"),
                                    },
                                ),
                            },
                        ),
                        "groups_to_roles": dict(
                            type="dict",
                            options={
                                "handle_nested": dict(type="bool"),
                                "roles_to_sync": dict(
                                    type="list",
                                    elements="dict",
                                    options={
                                        "role": dict(type="str"),
                                        "groups": dict(
                                            type="list",
                                            elements="dict",
                                            options={
                                                "group_dn": dict(type="str"),
                                                "search_in": dict(
                                                    type="str",
                                                    default="this_connection",
                                                ),
                                            },
                                        ),
                                    },
                                ),
                            },
                        ),
                    },
                ),
                "other": dict(
                    type="dict",
                    default={},
                    options={
                        "sync_interval": dict(
                            type="dict",
                            default={},
                            options={
                                "days": dict(type="int", default=0),
                                "hours": dict(type="int", default=0),
                                "minutes": dict(type="int", default=5),
                            },
                        ),
                    },
                ),
            },
        ),
        state=dict(type="str", default="present", choices=["present", "absent"]),
    )

    required_if = [
        ("api_auth_type", "bearer", ["automation_user", "automation_secret"]),
        ("api_auth_type", "basic", ["automation_user", "automation_secret"]),
        ("api_auth_type", "cookie", ["api_auth_cookie"]),
    ]

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=required_if,
    )

    logger.set_loglevel(module._verbosity)
    logger.set_loglevel(2)

    #logger.debug("Starting...")
    desired_state = module.params["state"]
    #logger.debug("Desired_state: %s" % str(desired_state))
    #logger.debug("Desired_parameters: %s" % str(module.params))
    ldap_api = LDAPAPI(module)
    #logger.debug("LDAPAPI instance created.")

    try:
        if desired_state == "present":
            if ldap_api.state == "absent":
                result = ldap_api.create()
                exit_module(module, result=result, logger=logger)
            elif ldap_api.needs_update():
                result = ldap_api.edit()
                exit_module(module, result=result, logger=logger)

            else:
                exit_module(
                    module,
                    msg="LDAP configuration is already in the desired state.",
                    logger=logger,
                )

        elif desired_state == "absent":
            if ldap_api.state == "present":
                result = ldap_api.delete()
                exit_module(module, result=result, logger=logger)
            else:
                exit_module(
                    module,
                    msg="LDAP configuration is already absent.",
                    logger=logger,
                )

    except Exception as e:
        exit_module(
            module, msg="Error managing the LDAP configuration: %s" % e, logger=logger
        )


def main():
    """
    Main entry point for the module.
    This function is invoked when the module is executed directly.
    Returns:
        None: Calls run_module() to handle the logic.
    """
    run_module()


if __name__ == "__main__":
    main()

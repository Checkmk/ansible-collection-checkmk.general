#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2022, Robin Gierse <robin.gierse@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: site_management

short_description: Manage sites in Checkmk.

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "5.3.0"

description:
    - Manage sites within Checkmk.

extends_documentation_fragment: [checkmk.general.common]

options:
    state:
        description:
            - The desired state of this site connection.
        type: str
        choices: ['present', 'absent', 'login', 'logout']
        default: present
    site_id:
        description:
            - The site ID.
        required: true
        type: str
    site_connection:
        description:
            - The settings of the site.
        type: dict
        suboptions:
            login_data:
                description:
                    - The authentication data for a configuration connection.
                    - Only required when the state is "login".
                type: dict
                suboptions:
                    remote_username:
                        description:
                            - An administrative user's username.
                        type: str
                    remote_password:
                        description:
                            - The password for the username given.
                        type: str
            site_config:
                description:
                    - A site's connection.
                    - Only required when that state is "present".
                type: dict
                suboptions:
                    status_connection:
                        description:
                            - A site's status connection.
                        type: dict
                        suboptions:
                            connection:
                                description:
                                    - When connecting to remote site please make sure that
                                    - Livestatus over TCP is activated there.
                                    - You can use UNIX sockets to connect to foreign sites on
                                    - localhost.
                                type: dict
                                suboptions:
                                    socket_type:
                                        description:
                                            - The connection name. This can be
                                            - tcp, tcp6, unix or local.
                                        type: str
                                        choices: ['tcp', 'tcp6', 'unix', 'local']
                                    port:
                                        description:
                                            - The TCP port to connect to.
                                        type: int
                                    encrypted:
                                        description:
                                            - To enable an encrypted connection.
                                        type: bool
                                    verify:
                                        description:
                                            - Verify server certificate.
                                        type: bool
                                    host:
                                        description:
                                            - The IP or domain name of the host.
                                        type: str
                                    path:
                                        description:
                                            - When the connection name is unix,
                                            - this is the path to the unix socket.
                                        type: str
                            proxy:
                                description:
                                    - The Livestatus proxy daemon configuration attributes.
                                type: dict
                                suboptions:
                                    use_livestatus_daemon:
                                        description:
                                            - Use livestatus daemon with direct connection
                                            - or with livestatus proxy.
                                        type: str
                                        choices: [with_proxy, direct]
                                    global_settings:
                                        description:
                                            - When use_livestatus_daemon is set to 'with_proxy',
                                            - you can set this to True to use global setting or
                                            - False to use custom parameters.
                                        type: bool
                                    tcp:
                                        description:
                                            - Allow access via TCP configuration.
                                        type: dict
                                        suboptions:
                                            port:
                                                description:
                                                    - The TCP port to connect to.
                                                type: int
                                            only_from:
                                                description:
                                                    - Restrict access to these IP addresses.
                                                type: list
                                                elements: str
                                            tls:
                                                description:
                                                    - Encrypt TCP Livestatus connections.
                                                type: bool
                                                default: false
                                    params:
                                        description:
                                            - The live status proxy daemon parameters.
                                        type: dict
                                        suboptions:
                                            channels:
                                                description:
                                                    - The number of channels to keep open.
                                                type: int
                                                default: 5
                                            heartbeat:
                                                description:
                                                    - The heartbeat interval and timeout
                                                    - configuration.
                                                type: dict
                                                suboptions:
                                                    interval:
                                                        description:
                                                            - The heartbeat interval
                                                            - for the TCP connection.
                                                        type: int
                                                        default: 5
                                                    timeout:
                                                        description:
                                                            - The heartbeat timeout
                                                            - for the TCP connection.
                                                        type: int
                                                        default: 2
                                            channel_timeout:
                                                description:
                                                    - The timeout waiting for a free channel.
                                                type: int
                                                default: 3
                                            query_timeout:
                                                description:
                                                    - The total query timeout.
                                                type: int
                                                default: 120
                                            connect_retry:
                                                description:
                                                    - The cooling period after failed
                                                    - connect/heartbeat.
                                                type: int
                                                default: 4
                                            cache:
                                                description:
                                                    - Enable caching.
                                                type: bool
                                                default: true
                            connect_timeout:
                                description:
                                    - The time that the GUI waits for a connection to the site
                                    - to be established before the site is considered to be
                                    - unreachable.
                                type: int
                                default: 2
                            persistent_connection:
                                description:
                                    - If you enable persistent connections then Multisite
                                    - will try to keep open the connection to the remote sites.
                                type: bool
                                default: false
                            url_prefix:
                                description:
                                    - The URL prefix will be prepended to links of addons like
                                    - NagVis when a link to such applications points to a host
                                    - or service on that site.
                                type: str
                            status_host:
                                description:
                                    - By specifying a status host for each non-local connection
                                    - you prevent Multisite from running into timeouts when
                                    - remote sites do not respond.
                                type: dict
                                suboptions:
                                    status_host_set:
                                        description:
                                            - enabled for 'use the following status host' and
                                            - disabled for 'no status host'
                                        type: str
                                        choices: [enabled, disabled]
                                        default: disabled
                                    site:
                                        description:
                                            - The site ID of the status host.
                                        type: str
                                    host:
                                        description:
                                            - The host name of the status host.
                                        type: str
                            disable_in_status_gui:
                                description:
                                    - If you disable a connection, then no data of this site will
                                    - be shown in the status GUI. The replication is not affected
                                    - by this, however.
                                type: bool
                                default: false
                    configuration_connection:
                        description:
                            - A site's configurationstatus connection.
                        type: dict
                        suboptions:
                            enable_replication:
                                description:
                                    - Replication allows you to manage several monitoring sites
                                    - with a logically centralized setup.
                                    - Remote sites receive their configuration
                                    - from the central sites.
                                type: bool
                                default: false
                            url_of_remote_site:
                                description:
                                    - URL of the remote Checkmk including /check_mk/.
                                    - This URL is in many cases the same as the URL-Prefix
                                    - but with check_mk/ appended, but it must always be
                                    - an absolute URL.
                                    - Unfortunately, this field is required by the REST API,
                                    - even if there is no configuration connection enabled.
                                type: str
                                default: http://localhost/nonexistant/check_mk/
                            disable_remote_configuration:
                                description:
                                    - It is a good idea to disable access to Setup completely on
                                    - the remote site. Otherwise a user who does not now about
                                    - the replication could make local changes that are overridden
                                    - at the next configuration activation.
                                type: bool
                                default: true
                            ignore_tls_errors:
                                description:
                                    - This might be needed to make the synchronization accept
                                    - problems with SSL certificates when using an SSL secured
                                    - connection.
                                type: bool
                                default: false
                            direct_login_to_web_gui_allowed:
                                description:
                                    - When enabled, this site is marked for synchronisation every
                                    - time a web GUI related option is changed and users are
                                    - allowed to login to the web GUI of this site.
                                type: bool
                                default: true
                            user_sync:
                                description:
                                    - By default the users are synchronized automatically in
                                    - the interval configured in the connection. For example
                                    - the LDAP connector synchronizes the users every five minutes
                                    - by default. The interval can be changed for each connection
                                    - individually in the connection settings. Please note that
                                    - the synchronization is only performed on the master site
                                    - in distributed setups by default.
                                type: dict
                                suboptions:
                                    sync_with_ldap_connections:
                                        description:
                                            - Sync with ldap connections. The options are
                                            - ldap, all, disabled.
                                        type: str
                                        choices: ['ldap', 'all', 'disabled']
                                        default: all
                                    ldap_connections:
                                        description:
                                            - A list of ldap connections.
                                        type: list
                                        elements: str
                            replicate_event_console:
                                description:
                                    - This option enables the distribution of global settings and
                                    - rules of the Event Console to the remote site. Any change in
                                    - the local Event Console settings will mark the site as need
                                    - sync. A synchronization will automatically reload
                                    - the Event Console of the remote site.
                                type: bool
                                default: true
                            replicate_extensions:
                                description:
                                    - If you enable the replication of MKPs then during each
                                    - Activate Changes MKPs that are installed on your central site
                                    - and all other files below the ~/local/ directory will be also
                                    - transferred to the remote site. All other MKPs and
                                    - files below ~/local/ on the remote site will be removed.
                                type: bool
                                default: true
                    secret:
                        description:
                            - The shared secret used by the central site to authenticate with the
                            - remote site for configuring Checkmk.
                        type: str
                        default:
                    basic_settings:
                        description:
                            - A site's basic settings.
                        type: dict
                        suboptions:
                            alias:
                                description:
                                    - The alias of the site.
                                type: str
                            customer:
                                description:
                                    - The customer of the site (Checkmk Managed Edition - CME only).
                                type: str
                            site_id:
                                description:
                                    - The site ID.
                                type: str

author:
    - Lars Getwan (@lgetwan)
"""

EXAMPLES = r"""
- name: "Add a remotesite with config replication."
  checkmk.general.site_management:
    server_url: "http://myserver/"
    site: "mysite"
    automation_user: "myuser"
    automation_secret: "mysecret"
    site_id: "myremotesite"
    site_connection:
        site_config:
            status_connection:
                connection:
                   socket_type: tcp
                   port: 6559
                   encrypted: True
                   host: localhost
                   verify: True
                proxy:
                   use_livestatus_daemon: "direct"
                connect_timeout: 2
                status_host:
                    status_host_set: "disabled"
                url_prefix: "/myremotesite/"
            configuration_connection:
                enable_replication: True
                url_of_remote_site: "http://localhost/myremotesite/check_mk/"
            basic_settings:
                site_id: "myremotesite"
                customer: "provider"
                alias: "My Remote Site"
    state: "present"

- name: "Log in to a remotesite."
  checkmk.general.site_management:
    server_url: "http://myserver/"
    site: "mysite"
    automation_user: "myuser"
    automation_secret: "mysecret"
    site_id: "myremotesite"
    site_connection:
      login_data:
        remote_username: "myremote_admin"
        aremote_password: "highly#secret"
    state: "login"

- name: "Log out from a remotesite."
  checkmk.general.site_management:
    server_url: "http://myserver/"
    site: "mysite"
    automation_user: "myuser"
    automation_secret: "mysecret"
    site_id: "myremotesite"
    state: "logout"

- name: "Delete a remotesite."
  checkmk.general.site_management:
    server_url: "http://myserver/"
    site: "mysite"
    automation_user: "myuser"
    automation_secret: "mysecret"
    site_id: "myremotesite"
    state: "absent"
"""

RETURN = r"""
message:
    description: The output message that the module generates. Contains the API response details in case of an error.
    type: str
    returned: always
    sample: 'Site connection created.'
"""

import json

# https://docs.ansible.com/ansible/latest/dev_guide/testing/sanity/import.html
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.checkmk.general.plugins.module_utils.api import CheckmkAPI
from ansible_collections.checkmk.general.plugins.module_utils.types import RESULT
from ansible_collections.checkmk.general.plugins.module_utils.version import (
    CheckmkVersion,
)

TARGET_API_GET = "get"
TARGET_API_CREATE = "create"
TARGET_API_LOGIN = "login"
TARGET_API_LOGOUT = "logout"
TARGET_API_UPDATE = "update"
TARGET_API_DELETE = "delete"


def exit_module(
    module,
    result=None,
    http_code=0,
    msg="",
    content="{}",
    etag="",
    failed=False,
    changed=False,
):
    if not result:
        result = RESULT(
            http_code=http_code,
            msg=msg,
            content=content,
            etag=etag,
            failed=failed,
            changed=changed,
        )

    result_as_dict = result._asdict()
    result_as_dict["debug"] = logger.get_log()
    module.exit_json(**result_as_dict)


def merge_results(results):
    return RESULT(
        http_code=list(results.values())[-1].http_code,
        msg=", ".join(
            ["%s (%d)" % (results[k].msg, results[k].http_code) for k in results.keys()]
        ),
        content=list(results.values())[-1].content,
        etag=list(results.values())[-1].etag,
        failed=any(r.failed for r in list(results.values())),
        changed=any(r.changed for r in list(results.values())),
    )


def remove_null_value_keys(params):
    for k in list(params.keys()):
        if isinstance(params[k], dict):
            remove_null_value_keys(params[k])
        elif params[k] is None:
            del params[k]


class Logger:
    def __init__(self):
        self.output: list[str] = []
        self.loglevel = 0

    def set_loglevel(self, loglevel):
        self.loglevel = loglevel

    def warn(self, msg):
        self.output.append("WARN: %s" % msg)

    def info(self, msg):
        if self.loglevel >= 1:
            self.output.append("INFO: %s" % msg)

    def debug(self, msg):
        if self.loglevel >= 2:
            self.output.append("DEBUG: %s" % msg)

    def trace(self, msg):
        if self.loglevel >= 3:
            self.output.append("TRACE: %s" % msg)

    def get_log(self):
        return "\n".join(self.output)


class SiteManagementHTTPCodes:
    # http_code: (changed, failed, "Message")
    get = {
        200: (False, False, "Site connection found, nothing changed"),
        404: (False, False, "Site connection not found"),
    }

    create = {200: (True, False, "Site connection created")}
    update = {200: (True, False, "Site connection modified")}
    delete = {204: (True, False, "Site connection deleted")}
    login = {204: (True, False, "Logged in to site")}
    logout = {204: (True, False, "Logged out from site")}


class SiteManagementEndpoints:
    default = "/objects/site_connection"
    create = "/domain-types/site_connection/collections/all"


class SiteConnection:
    """Represents a particular site connection"""

    def __init__(
        self,
        login_data=None,
        # site_config: SiteConfig | None = None,
        site_config=None,
        state="absent",
        site_id=None,
    ):
        self.site_id = site_id
        self.state = state
        self.site_config = site_config
        self.login_data = login_data

    @classmethod
    def from_module_params(cls, params):
        site_connection = params.get("site_connection")
        state = params.get("state")
        site_id = params.get("site_id")
        if site_connection:
            login_data = site_connection.get("login_data")
            site_config = site_connection.get("site_config")
        else:
            login_data = None
            site_config = None

        return cls(
            site_config=site_config,
            login_data=login_data,
            state=state,
            site_id=site_id,
        )

    @classmethod
    def from_api(cls, api_data):

        if not api_data:
            return None

        return cls(
            site_config=api_data.content.get("extensions"),
            site_id=api_data.content.get("id"),
            state="present",
        )

    def equals(self, site_connection) -> bool:
        return self.site_config == site_connection.site_config

    def _diff(self, d, u):
        differences = []
        for k, v in u.items():
            if isinstance(v, dict):
                differences += self._diff(d.get(k, {}), v)
            else:
                if d.get(k) != v:
                    differences += [k]
        return differences

    def diff(self, site_connection) -> bool:
        return self._diff(self.site_config, site_connection.site_config)

    def logged_in(self) -> bool:
        if self.site_config and self.site_config.get("secret"):
            return True

    def _update(self, d, u):
        for k, v in u.items():
            if isinstance(v, dict):
                d[k] = self._update(d.get(k, {}), v)
            else:
                d[k] = v
        return d

    def merge_with(self, site_connection):
        self._update(self.site_config, site_connection.site_config)

    def get_api_data(self, target_api):

        if target_api in [TARGET_API_CREATE, TARGET_API_UPDATE]:
            logger.trace("get_api_data (%s): %s" % (target_api, str(self.site_config)))
            return {"site_config": self.site_config}

        if target_api in [TARGET_API_LOGIN]:
            if not self.login_data:
                return

            logger.trace(
                "get_api_data (%s): %s"
                % (
                    target_api,
                    str(
                        {
                            "username": self.login_data.get("remote_username"),
                            "password": "********",
                        }
                    ),
                )
            )

            return {
                "username": self.login_data.get("remote_username"),
                "password": self.login_data.get("remote_password"),
            }


class SiteManagementAPI(CheckmkAPI):
    def __init__(self, module):
        super().__init__(module)

        self._verify_compatibility()

        self.module = module
        self.params = self.module.params
        self.state = self.params.get("state")

    def _get_endpoint(self, target_api, site_id: str = ""):
        if target_api == TARGET_API_CREATE:
            return SiteManagementEndpoints.create

        if target_api in [TARGET_API_GET, TARGET_API_UPDATE]:
            return "%s/%s" % (SiteManagementEndpoints.default, site_id)

        if target_api in [TARGET_API_LOGIN]:
            return "%s/%s/actions/login/invoke" % (
                SiteManagementEndpoints.default,
                site_id,
            )

        if target_api in [TARGET_API_LOGOUT]:
            return "%s/%s/actions/logout/invoke" % (
                SiteManagementEndpoints.default,
                site_id,
            )

        if target_api in [TARGET_API_DELETE]:
            return "%s/%s/actions/delete/invoke" % (
                SiteManagementEndpoints.default,
                site_id,
            )

    def get(self, site_id) -> RESULT:
        logger.debug(
            "get endpoint: %s" % self._get_endpoint(TARGET_API_GET, site_id=site_id)
        )
        result = self._fetch(
            code_mapping=SiteManagementHTTPCodes.get,
            endpoint=self._get_endpoint(TARGET_API_GET, site_id=site_id),
        )

        logger.debug("get data: %s" % str(result))

        if result.http_code == 404:
            return None

        result = result._replace(content=json.loads(result.content))
        return result

    def create(self, site_connection) -> RESULT:
        logger.debug("create endpoint: %s" % self._get_endpoint(TARGET_API_CREATE))
        logger.debug(
            "create data: %s" % site_connection.get_api_data(TARGET_API_CREATE)
        )
        return self._fetch(
            code_mapping=SiteManagementHTTPCodes.create,
            endpoint=self._get_endpoint(TARGET_API_CREATE),
            data=site_connection.get_api_data(TARGET_API_CREATE),
            method="POST",
        )

    def update(self, site_connection, desired_site_connection) -> RESULT:
        vorher = site_connection.site_config
        site_connection.merge_with(desired_site_connection)
        nachher = site_connection.site_config
        logger.debug("update endpoint: %s" % self._get_endpoint(TARGET_API_UPDATE))
        logger.debug(
            "update data: %s" % site_connection.get_api_data(TARGET_API_UPDATE)
        )
        return self._fetch(
            code_mapping=SiteManagementHTTPCodes.update,
            endpoint=self._get_endpoint(
                TARGET_API_UPDATE, site_id=site_connection.site_id
            ),
            data=site_connection.get_api_data(TARGET_API_UPDATE),
            method="PUT",
        )

    def login(self, site_connection) -> RESULT:
        logger.debug(
            "login endpoint: %s"
            % self._get_endpoint(TARGET_API_LOGIN, site_id=site_connection.site_id)
        )
        logger.debug("login data: %s" % site_connection.get_api_data(TARGET_API_LOGIN))
        return self._fetch(
            code_mapping=SiteManagementHTTPCodes.login,
            endpoint=self._get_endpoint(
                TARGET_API_LOGIN, site_id=site_connection.site_id
            ),
            data=site_connection.get_api_data(TARGET_API_LOGIN),
            method="POST",
        )

    def logout(self, site_connection) -> RESULT:
        logger.debug(
            "logout endpoint: %s"
            % self._get_endpoint(TARGET_API_LOGOUT, site_id=site_connection.site_id)
        )
        logger.debug(
            "logout data: %s" % site_connection.get_api_data(TARGET_API_LOGOUT)
        )
        return self._fetch(
            code_mapping=SiteManagementHTTPCodes.logout,
            endpoint=self._get_endpoint(
                TARGET_API_LOGOUT, site_id=site_connection.site_id
            ),
            method="POST",
        )

    def delete(self, site_connection) -> RESULT:
        logger.debug(
            "delete endpoint: %s"
            % self._get_endpoint(TARGET_API_DELETE, site_id=site_connection.site_id)
        )
        logger.debug(
            "delete data: %s" % site_connection.get_api_data(TARGET_API_DELETE)
        )
        return self._fetch(
            code_mapping=SiteManagementHTTPCodes.delete,
            endpoint=self._get_endpoint(
                TARGET_API_DELETE, site_id=site_connection.site_id
            ),
            method="POST",
        )

    def _verify_compatibility(self):
        if self.getversion() <= CheckmkVersion("2.2.0"):
            exit_module(
                msg="Site management is only available for Checkmk versions starting with 2.2.0.",
                failed=True,
            )


logger = Logger()


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        server_url=dict(type="str", required=True),
        site=dict(type="str", required=True),
        validate_certs=dict(type="bool", required=False, default=True),
        automation_user=dict(type="str", required=True),
        automation_secret=dict(type="str", required=True, no_log=True),
        state=dict(
            type="str",
            default="present",
            choices=["present", "absent", "login", "logout"],
        ),
        site_id=dict(type="str", required=True),
        site_connection=dict(
            type="dict",
            mutually_exclusive=[
                ("login_data", "site_config"),
            ],
            # required_if=[
            #     ("state", "present", ("site_config",)),
            #     ("state", "login", ("login_data",)),
            # ],
            options=dict(
                login_data=dict(
                    type="dict",
                    options=dict(
                        remote_username=dict(type="str"),
                        remote_password=dict(type="str", no_log=True),
                    ),
                ),
                site_config=dict(
                    type="dict",
                    options=dict(
                        status_connection=dict(
                            type="dict",
                            apply_defaults=True,
                            options=dict(
                                connection=dict(
                                    type="dict",
                                    apply_defaults=False,
                                    options=dict(
                                        socket_type=dict(
                                            type="str",
                                            choices=["tcp", "tcp6", "unix", "local"],
                                        ),
                                        port=dict(
                                            type="int",
                                        ),
                                        encrypted=dict(
                                            type="bool",
                                        ),
                                        verify=dict(
                                            type="bool",
                                        ),
                                        host=dict(
                                            type="str",
                                        ),
                                        path=dict(
                                            type="str",
                                        ),
                                    ),
                                    required_if=[
                                        (
                                            "socket_type",
                                            "tcp",
                                            ("port", "encrypted", "host"),
                                        ),
                                        (
                                            "socket_type",
                                            "tcp6",
                                            (
                                                "port",
                                                "encrypted",
                                                "host",
                                            ),
                                        ),
                                        ("socket_type", "unix", ("path",)),
                                    ],
                                    mutually_exclusive=[
                                        ("host", "path"),
                                        ("port", "path"),
                                        ("encrypted", "path"),
                                        ("verify", "path"),
                                    ],
                                ),
                                proxy=dict(
                                    type="dict",
                                    apply_defaults=False,
                                    options=dict(
                                        use_livestatus_daemon=dict(
                                            type="str",
                                            choices=["with_proxy", "direct"],
                                        ),
                                        global_settings=dict(
                                            type="bool",
                                        ),
                                        tcp=dict(
                                            type="dict",
                                            options=dict(
                                                port=dict(
                                                    type="int",
                                                ),
                                                only_from=dict(
                                                    type="list",
                                                    elements="str",
                                                ),
                                                tls=dict(
                                                    type="bool",
                                                    default=False,
                                                ),
                                            ),
                                        ),
                                        params=dict(
                                            type="dict",
                                            apply_defaults=False,
                                            options=dict(
                                                channels=dict(
                                                    type="int",
                                                    default=5,
                                                ),
                                                heartbeat=dict(
                                                    type="dict",
                                                    options=dict(
                                                        interval=dict(
                                                            type="int",
                                                            default=5,
                                                        ),
                                                        timeout=dict(
                                                            type="int",
                                                            default=2,
                                                        ),
                                                    ),
                                                ),
                                                channel_timeout=dict(
                                                    type="int",
                                                    default=3,
                                                ),
                                                query_timeout=dict(
                                                    type="int",
                                                    default=120,
                                                ),
                                                connect_retry=dict(
                                                    type="int",
                                                    default=4,
                                                ),
                                                cache=dict(
                                                    type="bool",
                                                    default=True,
                                                ),
                                            ),
                                        ),
                                    ),
                                ),
                                connect_timeout=dict(
                                    type="int",
                                    default=2,
                                ),
                                persistent_connection=dict(
                                    type="bool",
                                    default=False,
                                ),
                                url_prefix=dict(
                                    type="str",
                                ),
                                status_host=dict(
                                    type="dict",
                                    apply_defaults=True,
                                    options=dict(
                                        status_host_set=dict(
                                            type="str",
                                            default="disabled",
                                            choices=["enabled", "disabled"],
                                        ),
                                        site=dict(
                                            type="str",
                                        ),
                                        host=dict(
                                            type="str",
                                        ),
                                    ),
                                ),
                                disable_in_status_gui=dict(
                                    type="bool",
                                    default="False",
                                ),
                            ),
                        ),
                        configuration_connection=dict(
                            type="dict",
                            apply_defaults=True,
                            options=dict(
                                enable_replication=dict(
                                    type="bool",
                                    default=False,
                                ),
                                url_of_remote_site=dict(
                                    type="str",
                                    default="http://localhost/nonexistant/check_mk/",
                                ),
                                disable_remote_configuration=dict(
                                    type="bool",
                                    default=True,
                                ),
                                ignore_tls_errors=dict(
                                    type="bool",
                                    default=False,
                                ),
                                direct_login_to_web_gui_allowed=dict(
                                    type="bool",
                                    default=True,
                                ),
                                user_sync=dict(
                                    type="dict",
                                    apply_defaults=True,
                                    required_if=[
                                        (
                                            "sync_with_ldap_connections",
                                            "ldap",
                                            ("ldap_connections",),
                                        )
                                    ],
                                    options=dict(
                                        sync_with_ldap_connections=dict(
                                            type="str",
                                            choices=["ldap", "all", "disabled"],
                                            default="all",
                                        ),
                                        ldap_connections=dict(
                                            type="list",
                                            elements="str",
                                        ),
                                    ),
                                ),
                                replicate_event_console=dict(
                                    type="bool",
                                    default=True,
                                ),
                                replicate_extensions=dict(
                                    default=True,
                                    type="bool",
                                ),
                            ),
                        ),
                        secret=dict(
                            type="str",
                            no_log=True,
                        ),
                        basic_settings=dict(
                            type="dict",
                            options=dict(
                                alias=dict(
                                    type="str",
                                ),
                                customer=dict(
                                    type="str",
                                ),
                                site_id=dict(
                                    type="str",
                                ),
                            ),
                        ),
                    ),
                ),
            ),
        ),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    logger.set_loglevel(module._verbosity)
    remove_null_value_keys(module.params)
    site_id = module.params.get("site_id")

    site_management_api = SiteManagementAPI(module)
    desired_site_connection = SiteConnection.from_module_params(module.params)
    existing_site_connection = SiteConnection.from_api(site_management_api.get(site_id))

    if desired_site_connection.state == "present":
        if existing_site_connection and existing_site_connection.state == "present":
            differences = existing_site_connection.diff(desired_site_connection)
            if differences:
                result = site_management_api.update(
                    existing_site_connection, desired_site_connection
                )

                result = result._replace(
                    msg="%s\nUpdated: %s" % (result.msg, ", ".join(differences))
                )
            else:
                result = RESULT(
                    http_code=0,
                    msg="Site connection already exists with the desired parameters.",
                    content="",
                    etag="",
                    failed=False,
                    changed=False,
                )

        else:
            result = site_management_api.create(desired_site_connection)

        exit_module(module, result=result)

    elif desired_site_connection.state == "absent":
        if existing_site_connection and existing_site_connection.state == "present":
            result = site_management_api.delete(existing_site_connection)
            exit_module(module, result=result)
        else:
            exit_module(module, msg="Site connection already absent.")

    elif desired_site_connection.state == "login":
        if not existing_site_connection:
            exit_module(module, msg="Site does not exist", failed=True)

        if not existing_site_connection.logged_in():
            result = site_management_api.login(desired_site_connection)
            exit_module(module, result=result)
        else:
            exit_module(module, msg="Already logged in to site.")

    elif desired_site_connection.state == "logout":
        if not existing_site_connection:
            exit_module(module, msg="Site does not exist", failed=True)

        if existing_site_connection.logged_in():
            result = site_management_api.logout(desired_site_connection)
            exit_module(module, result=result)
        else:
            exit_module(module, msg="Already logged out from site.")

    else:
        exit_module(
            module,
            msg="Unexpected target state %s" % desired_site_connection.state,
            failed=True,
        )


def main():
    run_module()


if __name__ == "__main__":
    main()

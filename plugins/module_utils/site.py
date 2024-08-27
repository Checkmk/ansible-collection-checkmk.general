#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2024, Lars Getwan <lars.getwan@checkmk.com>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type


class TargetAPI:
    GET = "get"
    CREATE = "create"
    LOGIN = "login"
    LOGOUT = "logout"
    UPDATE = "update"
    DELETE = "delete"


class SiteHTTPCodes:
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


class SiteEndpoints:
    default = "/objects/site_connection"
    create = "/domain-types/site_connection/collections/all"


class SiteConnection:
    """Represents a particular site connection"""

    def __init__(
        self,
        authentication=None,
        site_config=None,
        state="absent",
        site_id=None,
    ):
        self.site_id = site_id
        self.state = state
        self.site_config = site_config
        self.authentication = authentication

    @classmethod
    def from_module_params(cls, params):
        site_connection = params.get("site_connection")
        state = params.get("state")
        site_id = params.get("site_id")
        if site_connection:
            authentication = site_connection.get("authentication")
            site_config = site_connection.get("site_config")
        else:
            authentication = None
            site_config = None

        return cls(
            site_config=site_config,
            authentication=authentication,
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

    def equals(self, site_connection):
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

    def diff(self, site_connection):
        return self._diff(self.site_config, site_connection.site_config)

    def logged_in(self):
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

        t = TargetAPI()
        if target_api in [t.CREATE, t.UPDATE]:
            return {"site_config": self.site_config}

        if target_api in [t.LOGIN]:
            return self.authentication


# Define available arguments/parameters a user can pass to the module
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
            ("authentication", "site_config"),
        ],
        options=dict(
            authentication=dict(
                type="dict",
                options=dict(
                    username=dict(type="str"),
                    password=dict(type="str", no_log=True),
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

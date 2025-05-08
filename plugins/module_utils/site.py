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

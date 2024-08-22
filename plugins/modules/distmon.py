#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2024, Lars Getwan <lars.getwan@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: distmon

short_description: Manage distributed monitoring in Checkmk.

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "5.3.0"

description:
    - Manage distributed monitoring within Checkmk.

extends_documentation_fragment:
    - checkmk.general.common
    - checkmk.general.distmon_options

author:
    - Lars Getwan (@lgetwan)
"""

EXAMPLES = r"""
- name: "Add a remote site with configuration replication."
  checkmk.general.distmon:
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
            port: 6557
            encrypted: true
            host: localhost
            verify: true
          proxy:
            use_livestatus_daemon: "direct"
          connect_timeout: 2
          status_host:
            status_host_set: "disabled"
          url_prefix: "/myremotesite/"
        configuration_connection:
          enable_replication: true
          url_of_remote_site: "http://localhost/myremotesite/check_mk/"
        basic_settings:
          site_id: "myremotesite"
          customer: "provider"
          alias: "My Remote Site"
    state: "present"

- name: "Log into a remote site."
  checkmk.general.distmon:
    server_url: "http://myserver/"
    site: "mysite"
    automation_user: "myuser"
    automation_secret: "mysecret"
    site_id: "myremotesite"
    site_connection:
      login_data:
        remote_username: "myremote_admin"
        remote_password: "highly_secret"
    state: "login"

- name: "Log out from a remote site."
  checkmk.general.distmon:
    server_url: "http://myserver/"
    site: "mysite"
    automation_user: "myuser"
    automation_secret: "mysecret"
    site_id: "myremotesite"
    state: "logout"

- name: "Delete a remote site."
  checkmk.general.distmon:
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
from ansible_collections.checkmk.general.plugins.module_utils.distmon import (
    DistMonEndpoints,
    DistMonHTTPCodes,
    SiteConnection,
    TargetAPI,
    module_args,
)
from ansible_collections.checkmk.general.plugins.module_utils.logger import Logger
from ansible_collections.checkmk.general.plugins.module_utils.types import RESULT
from ansible_collections.checkmk.general.plugins.module_utils.utils import (
    exit_module,
    remove_null_value_keys,
)
from ansible_collections.checkmk.general.plugins.module_utils.version import (
    CheckmkVersion,
)


class DistMonAPI(CheckmkAPI):
    def __init__(self, module):
        super().__init__(module)

        self._verify_compatibility()

        self.module = module
        self.params = self.module.params
        self.state = self.params.get("state")

    def _get_endpoint(self, target_api, site_id=""):
        if target_api == TargetAPI.CREATE:
            return DistMonEndpoints.create

        if target_api in [TargetAPI.GET, TargetAPI.UPDATE]:
            return "%s/%s" % (DistMonEndpoints.default, site_id)

        if target_api in [TargetAPI.LOGIN]:
            return "%s/%s/actions/login/invoke" % (
                DistMonEndpoints.default,
                site_id,
            )

        if target_api in [TargetAPI.LOGOUT]:
            return "%s/%s/actions/logout/invoke" % (
                DistMonEndpoints.default,
                site_id,
            )

        if target_api in [TargetAPI.DELETE]:
            return "%s/%s/actions/delete/invoke" % (
                DistMonEndpoints.default,
                site_id,
            )

    def get(self, site_id):
        logger.debug(
            "get endpoint: %s" % self._get_endpoint(TargetAPI.GET, site_id=site_id)
        )
        result = self._fetch(
            code_mapping=DistMonHTTPCodes.get,
            endpoint=self._get_endpoint(TargetAPI.GET, site_id=site_id),
        )

        logger.debug("get data: %s" % str(result))

        if result.http_code == 404:
            return None

        result = result._replace(content=json.loads(result.content))
        return result

    def create(self, site_connection):
        logger.debug("create endpoint: %s" % self._get_endpoint(TargetAPI.CREATE))
        logger.debug("create data: %s" % site_connection.get_api_data(TargetAPI.CREATE))
        return self._fetch(
            code_mapping=DistMonHTTPCodes.create,
            endpoint=self._get_endpoint(TargetAPI.CREATE),
            data=site_connection.get_api_data(TargetAPI.CREATE),
            method="POST",
        )

    def update(self, site_connection, desired_site_connection):
        vorher = site_connection.site_config
        site_connection.merge_with(desired_site_connection)
        nachher = site_connection.site_config
        logger.debug("update endpoint: %s" % self._get_endpoint(TargetAPI.UPDATE))
        logger.debug("update data: %s" % site_connection.get_api_data(TargetAPI.UPDATE))
        return self._fetch(
            code_mapping=DistMonHTTPCodes.update,
            endpoint=self._get_endpoint(
                TargetAPI.UPDATE, site_id=site_connection.site_id
            ),
            data=site_connection.get_api_data(TargetAPI.UPDATE),
            method="PUT",
        )

    def login(self, site_connection):
        logger.debug(
            "login endpoint: %s"
            % self._get_endpoint(TargetAPI.LOGIN, site_id=site_connection.site_id)
        )
        logger.debug("login data: %s" % site_connection.get_api_data(TargetAPI.LOGIN))
        return self._fetch(
            code_mapping=DistMonHTTPCodes.login,
            endpoint=self._get_endpoint(
                TargetAPI.LOGIN, site_id=site_connection.site_id
            ),
            data=site_connection.get_api_data(TargetAPI.LOGIN),
            method="POST",
        )

    def logout(self, site_connection):
        logger.debug(
            "logout endpoint: %s"
            % self._get_endpoint(TargetAPI.LOGOUT, site_id=site_connection.site_id)
        )
        logger.debug("logout data: %s" % site_connection.get_api_data(TargetAPI.LOGOUT))
        return self._fetch(
            code_mapping=DistMonHTTPCodes.logout,
            endpoint=self._get_endpoint(
                TargetAPI.LOGOUT, site_id=site_connection.site_id
            ),
            method="POST",
        )

    def delete(self, site_connection):
        logger.debug(
            "delete endpoint: %s"
            % self._get_endpoint(TargetAPI.DELETE, site_id=site_connection.site_id)
        )
        logger.debug("delete data: %s" % site_connection.get_api_data(TargetAPI.DELETE))
        return self._fetch(
            code_mapping=DistMonHTTPCodes.delete,
            endpoint=self._get_endpoint(
                TargetAPI.DELETE, site_id=site_connection.site_id
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

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    logger.set_loglevel(module._verbosity)
    remove_null_value_keys(module.params)
    site_id = module.params.get("site_id")

    distmon_api = DistMonAPI(module)
    desired_site_connection = SiteConnection.from_module_params(module.params)
    existing_site_connection = SiteConnection.from_api(distmon_api.get(site_id))

    if desired_site_connection.state == "present":
        if existing_site_connection and existing_site_connection.state == "present":
            differences = existing_site_connection.diff(desired_site_connection)
            if differences:
                result = distmon_api.update(
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
            result = distmon_api.create(desired_site_connection)

        exit_module(module, result=result)

    elif desired_site_connection.state == "absent":
        if existing_site_connection and existing_site_connection.state == "present":
            result = distmon_api.delete(existing_site_connection)
            exit_module(module, result=result)
        else:
            exit_module(module, msg="Site connection already absent.")

    elif desired_site_connection.state == "login":
        if not existing_site_connection:
            exit_module(module, msg="Site does not exist", failed=True)

        if not existing_site_connection.logged_in():
            result = distmon_api.login(desired_site_connection)
            exit_module(module, result=result)
        else:
            exit_module(module, msg="Already logged in to site.")

    elif desired_site_connection.state == "logout":
        if not existing_site_connection:
            exit_module(module, msg="Site does not exist", failed=True)

        if existing_site_connection.logged_in():
            result = distmon_api.logout(desired_site_connection)
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

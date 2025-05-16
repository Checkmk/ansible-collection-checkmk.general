#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2024, Lars Getwan <lars.getwan@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: site

short_description: Manage distributed monitoring in Checkmk.

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "5.3.0"

description:
    - Manage distributed monitoring within Checkmk.

extends_documentation_fragment:
    - checkmk.general.common
    - checkmk.general.site_options

author:
    - Lars Getwan (@lgetwan)
"""

EXAMPLES = r"""
- name: "Add a remote site with configuration replication."
  checkmk.general.site:
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
  checkmk.general.site:
    server_url: "http://myserver/"
    site: "mysite"
    automation_user: "myuser"
    automation_secret: "mysecret"
    site_id: "myremotesite"
    site_connection:
      authentication:
        username: "myremote_admin"
        password: "highly_secret"
    state: "login"

- name: "Log out from a remote site."
  checkmk.general.site:
    server_url: "http://myserver/"
    site: "mysite"
    automation_user: "myuser"
    automation_secret: "mysecret"
    site_id: "myremotesite"
    state: "logout"

- name: "Delete a remote site."
  checkmk.general.site:
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
from ansible_collections.checkmk.general.plugins.module_utils.logger import Logger
from ansible_collections.checkmk.general.plugins.module_utils.site import (
    site_argument_spec,
    SiteConnection,
    SiteEndpoints,
    SiteHTTPCodes,
    TargetAPI,
)
from ansible_collections.checkmk.general.plugins.module_utils.types import RESULT
from ansible_collections.checkmk.general.plugins.module_utils.utils import (
    base_argument_spec,
    exit_module,
    remove_null_value_keys,
)
from ansible_collections.checkmk.general.plugins.module_utils.version import (
    CheckmkVersion,
)


class SiteAPI(CheckmkAPI):
    def __init__(self, module):
        super().__init__(module)

        self.module = module
        self.params = self.module.params
        self.state = self.params.get("state")

        self._verify_compatibility()

    def _get_endpoint(self, target_api, site_id=""):
        if target_api == TargetAPI.CREATE:
            return SiteEndpoints.create

        if target_api in [TargetAPI.GET, TargetAPI.UPDATE]:
            return "%s/%s" % (SiteEndpoints.default, site_id)

        if target_api in [TargetAPI.LOGIN]:
            return "%s/%s/actions/login/invoke" % (
                SiteEndpoints.default,
                site_id,
            )

        if target_api in [TargetAPI.LOGOUT]:
            return "%s/%s/actions/logout/invoke" % (
                SiteEndpoints.default,
                site_id,
            )

        if target_api in [TargetAPI.DELETE]:
            return "%s/%s/actions/delete/invoke" % (
                SiteEndpoints.default,
                site_id,
            )

    def get(self, site_id):
        logger.debug(
            "get endpoint: %s" % self._get_endpoint(TargetAPI.GET, site_id=site_id)
        )
        result = self._fetch(
            code_mapping=SiteHTTPCodes.get,
            endpoint=self._get_endpoint(TargetAPI.GET, site_id=site_id),
            logger=logger,
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
            code_mapping=SiteHTTPCodes.create,
            endpoint=self._get_endpoint(TargetAPI.CREATE),
            data=site_connection.get_api_data(TargetAPI.CREATE),
            method="POST",
            logger=logger,
        )

    def update(self, site_connection, desired_site_connection):
        site_connection.merge_with(desired_site_connection)
        logger.debug("update endpoint: %s" % self._get_endpoint(TargetAPI.UPDATE))
        logger.debug("update data: %s" % site_connection.get_api_data(TargetAPI.UPDATE))
        return self._fetch(
            code_mapping=SiteHTTPCodes.update,
            endpoint=self._get_endpoint(
                TargetAPI.UPDATE, site_id=site_connection.site_id
            ),
            data=site_connection.get_api_data(TargetAPI.UPDATE),
            method="PUT",
            logger=logger,
        )

    def login(self, site_connection):
        logger.debug(
            "login endpoint: %s"
            % self._get_endpoint(TargetAPI.LOGIN, site_id=site_connection.site_id)
        )
        logger.debug("login data: %s" % site_connection.get_api_data(TargetAPI.LOGIN))
        return self._fetch(
            code_mapping=SiteHTTPCodes.login,
            endpoint=self._get_endpoint(
                TargetAPI.LOGIN, site_id=site_connection.site_id
            ),
            data=site_connection.get_api_data(TargetAPI.LOGIN),
            method="POST",
            logger=logger,
        )

    def logout(self, site_connection):
        logger.debug(
            "logout endpoint: %s"
            % self._get_endpoint(TargetAPI.LOGOUT, site_id=site_connection.site_id)
        )
        logger.debug("logout data: %s" % site_connection.get_api_data(TargetAPI.LOGOUT))
        return self._fetch(
            code_mapping=SiteHTTPCodes.logout,
            endpoint=self._get_endpoint(
                TargetAPI.LOGOUT, site_id=site_connection.site_id
            ),
            method="POST",
            logger=logger,
        )

    def delete(self, site_connection):
        logger.debug(
            "delete endpoint: %s"
            % self._get_endpoint(TargetAPI.DELETE, site_id=site_connection.site_id)
        )
        logger.debug("delete data: %s" % site_connection.get_api_data(TargetAPI.DELETE))
        return self._fetch(
            code_mapping=SiteHTTPCodes.delete,
            endpoint=self._get_endpoint(
                TargetAPI.DELETE, site_id=site_connection.site_id
            ),
            method="POST",
            logger=logger,
        )

    def _verify_compatibility(self):
        if self.getversion() <= CheckmkVersion("2.2.0"):
            exit_module(
                self.module,
                msg="Site management is only available for Checkmk versions starting with 2.2.0. Version found: %s"
                % self.getversion(),
                failed=True,
                logger=logger,
            )

        message_broker_port = (
            self.params.get("site_connection", {})
            .get("site_config", {})
            .get("configuration_connection", {})
            .get("message_broker_port")
        )

        if self.getversion() < CheckmkVersion("2.4.0i1") and message_broker_port:
            exit_module(
                self.module,
                msg="The parameter message_broker_port is only available for Checkmk versions starting with 2.4.0. Version found: %s"
                % self.getversion(),
                failed=True,
                logger=logger,
            )


def werk16722(site_config):
    # Remove previously mandatory fields. See https://checkmk.com/werk/16722
    configuration_connection = site_config.get("configuration_connection", {})
    logger.debug("Werk 16722 found. Replication is disabled.")

    for key in [
        "url_of_remote_site",
        "user_sync",
        "disable_remote_configuration",
        "ignore_tls_errors",
        "direct_login_to_web_gui_allowed",
        "replicate_event_console",
        "replicate_extensions",
        "message_broker_port",
    ]:
        try:
            logger.debug("Removing key %s" % key)
            del configuration_connection[key]
        except KeyError:
            pass


logger = Logger()


def run_module():
    argument_spec = base_argument_spec()
    argument_spec.update(site_argument_spec)

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    logger.set_loglevel(module._verbosity)
    remove_null_value_keys(module.params)
    site_id = module.params.get("site_id")

    site_api = SiteAPI(module)
    replication_enabled = (
        module.params.get("site_connection", {})
        .get("site_config", {})
        .get("configuration_connection", {})
        .get("enable_replication", False)
    )

    # Can be removed, once we no longer support Checkmk versions older than 2.3.0p25
    if site_api.getversion() > CheckmkVersion("2.3.0p25") and not replication_enabled:
        # Remove unneeded parameters from the module's parameters
        logger.debug("Cleaning up module parameters")
        werk16722(module.params.get("site_connection", {}).get("site_config", {}))

    desired_site_connection = SiteConnection.from_module_params(module.params)
    existing_site_connection = SiteConnection.from_api(site_api.get(site_id))

    # Can be removed, once we no longer support Checkmk versions older than 2.3.0p25
    if site_api.getversion() > CheckmkVersion("2.3.0p25") and not replication_enabled:
        # Remove unneeded parameters from the existing site connection's config
        logger.debug("Cleaning parameters of existing connection")
        werk16722(existing_site_connection.site_config)

    if desired_site_connection.state == "present":
        if existing_site_connection and existing_site_connection.state == "present":
            differences = existing_site_connection.diff(desired_site_connection)
            if differences:
                result = site_api.update(
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
            result = site_api.create(desired_site_connection)

        exit_module(module, result=result, logger=logger)

    elif desired_site_connection.state == "absent":
        if existing_site_connection and existing_site_connection.state == "present":
            result = site_api.delete(existing_site_connection)
            exit_module(module, result=result, logger=logger)
        else:
            exit_module(module, msg="Site connection already absent.", logger=logger)

    elif desired_site_connection.state == "login":
        if not existing_site_connection:
            exit_module(module, msg="Site does not exist", failed=True, logger=logger)

        if not existing_site_connection.logged_in():
            result = site_api.login(desired_site_connection)
            exit_module(module, result=result, logger=logger)
        else:
            exit_module(module, msg="Already logged in to site.", logger=logger)

    elif desired_site_connection.state == "logout":
        if not existing_site_connection:
            exit_module(module, msg="Site does not exist", failed=True, logger=logger)

        if existing_site_connection.logged_in():
            result = site_api.logout(desired_site_connection)
            exit_module(module, result=result, logger=logger)
        else:
            exit_module(module, msg="Already logged out from site.", logger=logger)

    else:
        exit_module(
            module,
            msg="Unexpected target state %s" % desired_site_connection.state,
            failed=True,
            logger=logger,
        )


def main():
    run_module()


if __name__ == "__main__":
    main()

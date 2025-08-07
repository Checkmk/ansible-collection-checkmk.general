#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2023, Marcel Arentz <gdspd_you@open-one.de>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# Ensure compatibility to Python2
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json

from ansible.module_utils.urls import fetch_url
from ansible_collections.checkmk.general.plugins.module_utils.types import RESULT
from ansible_collections.checkmk.general.plugins.module_utils.utils import (  # result_as_dict,
    GENERIC_HTTP_CODES,
    exit_module,
)
from ansible_collections.checkmk.general.plugins.module_utils.version import (
    CheckmkVersion,
)


class CheckmkAPI:
    """Base class to contact a Checkmk server"""

    def __init__(self, module, logger=None):
        self.module = module
        self.logger = logger
        self.params = self.module.params
        server = self.params.get("server_url")
        site = self.params.get("site")
        user = self.params.get("automation_user")
        secret = self.params.get("automation_secret")
        self.url = "%s/%s/check_mk/api/1.0" % (server, site)
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer %s %s" % (user, secret),
        }
        self.current = {}
        self.required = {}
        # may be "present", "absent" or an individual one
        self.state = ""

    def _fetch(
        self, code_mapping="", endpoint="", data=None, method="GET", logger=None
    ):
        if not logger:
            logger = self.logger

        if logger:
            logger.debug(
                "_fetch(): endpoint: %s, data: %s, method: %s"
                % (
                    endpoint,
                    str(data),
                    method,
                )
            )
        http_mapping = GENERIC_HTTP_CODES.copy()
        http_mapping.update(code_mapping)

        # retry if timed out and each time double the timeout value
        #
        # The below values where changed from 3 retries with an
        # initial timeout of 10 seconds to 1 retry with a timeout
        # of 60 seconds.
        # The reasoning is this: The REST API will continue computing
        # a request, even if the client cancels it. So while the
        # initially implemented back-off mechanism makes sense, in
        # our case it can actually make things worse. Hence the change.
        # TODO: If the REST API at some point actually cancels requests
        # properly, we can go back to the initial back-off mechanism.

        num_of_retries = 1
        timeout = 60
        for i in range(num_of_retries):
            response, info = fetch_url(
                module=self.module,
                url="%s/%s" % (self.url, endpoint),
                data=self.module.jsonify(data),
                headers=self.headers,
                method=method,
                use_proxy=None,
                timeout=timeout,
            )

            http_code = info["status"]

            if http_code != -1:
                break

            timeout *= 2

        (
            changed,
            failed,
            http_readable,
        ) = http_mapping.get(http_code, (False, True, "Error calling API"))
        # Better translate to json later and keep the original response here.
        content = response.read() if response else ""
        msg = "%s - %s" % (str(http_code), http_readable)
        if failed:
            details = info.get("body", info.get("msg", "N/A"))
            msg += " Details: %s" % details

        result = RESULT(
            http_code=http_code,
            msg=msg,
            content=content,
            etag=info.get("etag", ""),
            failed=failed,
            changed=changed,
        )

        if failed:
            exit_module(
                self.module,
                result=result,
                failed=True,
                logger=logger,
            )
            # self.module.fail_json(**result_as_dict(result))
        if logger:
            logger.debug("_fetch(): result: %s" % str(result))
        return result

    def getversion(self):
        data = {}

        result = self._fetch(
            code_mapping={
                200: (True, False, "Discovery successful."),
                406: (False, True, "Not Acceptable."),
            },
            endpoint="version",
            data=data,
            method="GET",
        )

        content = result.content
        checkmkinfo = json.loads(content)
        return CheckmkVersion(checkmkinfo.get("versions").get("checkmk"))

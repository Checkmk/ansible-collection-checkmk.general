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
from ansible_collections.tribe29.checkmk.plugins.module_utils.types import RESULT
from ansible_collections.tribe29.checkmk.plugins.module_utils.utils import (
    GENERIC_HTTP_CODES,
    result_as_dict,
)


class CheckmkAPI:
    """Base class to contact a Checkmk server"""

    def __init__(self, module):
        self.module = module
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
        # may be "present", "abesent" or an individual one
        self.state = ""

    def _fetch(self, code_mapping, endpoint="", data=None, method="GET"):
        http_mapping = GENERIC_HTTP_CODES.copy()
        http_mapping.update(code_mapping)

        response, info = fetch_url(
            module=self.module,
            url="%s/%s" % (self.url, endpoint),
            data=self.module.jsonify(data),
            headers=self.headers,
            method=method,
            use_proxy=None,
            timeout=10,
        )

        http_code = info["status"]
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
            self.module.fail_json(**result_as_dict(result))
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
        return (checkmkinfo.get("versions").get("checkmk")).split(".")

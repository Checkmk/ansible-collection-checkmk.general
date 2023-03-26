#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2023, Marcel Arentz <gdspd_you@open-one.de>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# Ensure compatibility to Python2
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
from collections import namedtuple

from ansible.module_utils.urls import fetch_url

RESULT = namedtuple(
    "Result", ["http_code", "msg", "content", "etag", "changed", "failed"]
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

    def _fetch(self, code_mapping, endpoint="", data=None, method="GET"):
        response, info = fetch_url(
            self.module, "%s/%s" % (self.url, endpoint), self.module.jsonify(data), self.headers, method
        )
        http_code = info["status"]
        (
            changed,
            failed,
            http_readable,
        ) = code_mapping.get(http_code, (False, True, "Error calling API"))
        content = json.loads(response.read()) if response else {}
        msg = "%s - %s" % (str(http_code), http_readable)
        if failed:
            msg = "%s - %s" % (msg, content)
        return RESULT(
            http_code=http_code,
            msg=msg,
            content=content,
            etag=info.get("etag", ""),
            failed=failed,
            changed=changed,
        )

#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2023, Lars Getwan <lars.getwan@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import base64
import json

from ansible.module_utils.common.text.converters import to_text
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.six.moves.urllib.parse import urlencode
from ansible.module_utils.urls import open_url

HTTP_ERROR_CODES = {
    400: "Bad Request: Parameter or validation failure.",
    403: "Forbidden: Configuration via Setup is disabled.",
    404: "Not Found: The requested object has not been found.",
    406: "Not Acceptable: The requests accept headers can not be satisfied.",
}


class CheckMKLookupAPI:
    """Base class to contact a Checkmk server for ~Lookup calls"""

    def __init__(
        self,
        site_url,
        api_auth_type="bearer",
        api_auth_cookie=None,
        automation_user=None,
        automation_secret=None,
        validate_certs=True,
    ):
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        self.site_url = site_url
        self.url = "%s/check_mk/api/1.0" % site_url
        self.validate_certs = validate_certs
        # Bearer Authentication: "Bearer USERNAME PASSWORD"
        if api_auth_type == "bearer":
            if not automation_user or not automation_secret:
                raise ValueError(
                    "`automation_user` and `automation_secret` are required for bearer authentication."
                )
            self.headers["Authorization"] = "Bearer %s %s" % (
                automation_user,
                automation_secret,
            )

        # Basic Authentication
        elif api_auth_type == "basic":
            if not automation_user or not automation_secret:
                raise ValueError(
                    "`automation_user` and `automation_secret` are required for basic authentication."
                )
            auth_str = "%s:%s" % (automation_user, automation_secret)
            auth_b64 = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")
            self.headers["Authorization"] = "Basic %s" % auth_b64

        # Cookie Authentication
        elif api_auth_type == "cookie":
            if not api_auth_cookie:
                raise ValueError(
                    "`api_auth_cookie` is required for cookie authentication."
                )
            self.headers["Cookie"] = api_auth_cookie

        else:
            raise ValueError("Unsupported `api_auth_type`: %s" % api_auth_type)

    def get(self, endpoint="", parameters=None):
        url = self.url + endpoint

        try:
            if parameters:
                url = "%s?%s" % (url, urlencode(parameters))

            raw_response = open_url(
                url, headers=self.headers, validate_certs=self.validate_certs
            )
            return to_text(raw_response.read())
        except HTTPError as e:
            if e.code in HTTP_ERROR_CODES:
                return json.dumps(
                    {"code": e.code, "msg": HTTP_ERROR_CODES[e.code], "url": url}
                )
            else:
                return json.dumps({"code": e.code, "msg": e.reason, "url": url})
        except URLError as e:
            return json.dumps({"code": 0, "msg": str(e), "url": url})
        except Exception as e:
            return json.dumps({"code": 0, "msg": str(e), "url": url})

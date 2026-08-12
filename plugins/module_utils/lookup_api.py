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
        server_url,
        site,
        api_auth_type="bearer",
        api_auth_cookie=None,
        api_user=None,
        api_secret=None,
        validate_certs=True,
    ):
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        self.cookies = {}

        # Joining here rather than in every caller keeps the trailing-slash
        # handling in one place. rstrip() and not urljoin(): urljoin treats the
        # last path segment as a document, so a server_url with a path prefix
        # and no trailing slash would lose that prefix.
        self.site_url = "%s/%s" % (server_url.rstrip("/"), site)
        self.url = "%s/check_mk/api/1.0" % self.site_url
        self.validate_certs = validate_certs
        # Bearer Authentication: "Bearer USERNAME PASSWORD"
        if api_auth_type == "bearer":
            if not api_user or not api_secret:
                raise ValueError(
                    "`api_user` and `api_secret` are required for bearer authentication."
                )
            self.headers["Authorization"] = "Bearer %s %s" % (
                api_user,
                api_secret,
            )

        # Basic Authentication
        elif api_auth_type == "basic":
            if not api_user or not api_secret:
                raise ValueError(
                    "`api_user` and `api_secret` are required for basic authentication."
                )
            auth_str = "%s:%s" % (api_user, api_secret)
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
            msg = HTTP_ERROR_CODES.get(e.code, e.reason)
            detail = self._error_detail(e)
            if detail:
                msg = "%s %s" % (msg, detail)
            return json.dumps({"code": e.code, "msg": msg, "url": url})
        except URLError as e:
            return json.dumps({"code": 0, "msg": str(e), "url": url})
        except Exception as e:
            return json.dumps({"code": 0, "msg": str(e), "url": url})

    @staticmethod
    def _error_detail(error):
        """Extract the human readable part of a Checkmk REST API error body.

        The canned messages in HTTP_ERROR_CODES say what went wrong but not
        which parameter caused it, which matters for endpoints that validate
        a payload.
        """
        try:
            body = json.loads(to_text(error.read()))
        except Exception:
            return ""

        if not isinstance(body, dict):
            return ""

        parts = [body[key] for key in ("detail", "fields") if body.get(key)]

        return " ".join(
            part if isinstance(part, str) else json.dumps(part) for part in parts
        )

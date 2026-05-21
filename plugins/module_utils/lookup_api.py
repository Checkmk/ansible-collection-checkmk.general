#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2023, Lars Getwan <lars.getwan@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import base64
import json
import os
from urllib.parse import urlparse

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
        api_user=None,
        api_secret=None,
        validate_certs=True,
        proxy_url=None,
        proxy_user=None,
        proxy_pass=None,
    ):
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        self.cookies = {}

        self.site_url = site_url
        self.url = "%s/check_mk/api/1.0" % site_url
        self.validate_certs = validate_certs

        if proxy_url:
            proxy_uri = urlparse(proxy_url)
            if proxy_user and proxy_pass:
                proxy_uri = proxy_uri._replace(
                    netloc="%s:%s@%s" % (proxy_user, proxy_pass, proxy_uri.netloc)
                )
            self._proxy_https = proxy_uri.geturl()
            self._proxy_http = proxy_uri._replace(scheme="http").geturl()
        else:
            self._proxy_https = None
            self._proxy_http = None
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

        if parameters:
            url = "%s?%s" % (url, urlencode(parameters))

        _proxy_env_keys = ("http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY")
        _saved_env = {}
        if self._proxy_https:
            _saved_env = {k: os.environ.get(k) for k in _proxy_env_keys}
            os.environ["http_proxy"] = self._proxy_http
            os.environ["https_proxy"] = self._proxy_https
            os.environ["HTTP_PROXY"] = self._proxy_http
            os.environ["HTTPS_PROXY"] = self._proxy_https

        try:
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
        finally:
            for k, v in _saved_env.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v

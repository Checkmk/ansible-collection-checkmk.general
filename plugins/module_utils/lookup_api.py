#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2023, Lars Getwan <lars.getwan@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

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

    def __init__(self, site_url, user, secret, validate_certs=True):
        self.site_url = site_url
        self.user = user
        self.secret = secret
        self.validate_certs = validate_certs
        self.url = "%s/check_mk/api/1.0" % site_url
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer %s %s" % (user, secret),
        }

    def get(self, endpoint="", parameters=None):
        url = self.url + endpoint

        try:
            p_msg = ""
            if parameters:
                p_msg = str(parameters)
                url = "%s?%s" % (url, urlencode(parameters))

            raw_response = open_url(
                url, headers=self.headers, validate_certs=self.validate_certs
            )
            return to_text(raw_response.read())
        except HTTPError as e:
            if e.code in HTTP_ERROR_CODES:
                return json.dumps(
                    {"code": e.code, "msg": HTTP_ERROR_CODES[e.code], "url": url, "parameters": p_msg}
                )
            else:
                return json.dumps({"code": e.code, "msg": e.reason, "url": url, "parameters": p_msg})
        except URLError as e:
            return json.dumps({"code": 0, "msg": str(e), "url": url, "parameters": p_msg})
        except Exception as e:
            return json.dumps({"code": 0, "msg": str(e), "url": url, "parameters": p_msg})

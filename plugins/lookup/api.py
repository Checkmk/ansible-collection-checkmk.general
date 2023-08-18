#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2023, Lars Getwan <lars.getwan@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from urllib.error import HTTPError, URLError
from urllib.parse import urlencode

from ansible.errors import AnsibleError
from ansible.module_utils.common.text.converters import to_native, to_text
from ansible.module_utils.urls import ConnectionError, SSLValidationError, open_url


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

    def get(self, endpoint="", parameters={}):
        url = self.url + endpoint

        if parameters:
            url = "%s?%s" % (url, urlencode(parameters))

        response = ""
        try:
            raw_response = open_url(
                url, headers=self.headers, validate_certs=self.validate_certs
            )
            response = to_text(raw_response.read())

        except HTTPError as e:
            raise AnsibleError("Received HTTP error for %s : %s" % (url, to_native(e)))
        except URLError as e:
            raise AnsibleError("Failed lookup url for %s : %s" % (url, to_native(e)))
        except SSLValidationError as e:
            raise AnsibleError(
                "Error validating the server's certificate for %s: %s"
                % (url, to_native(e))
            )
        except ConnectionError as e:
            raise AnsibleError("Error connecting to %s: %s" % (url, to_native(e)))

        return response

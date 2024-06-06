#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2023, Marcel Arentz <gdspd_you@open-one.de>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# Ensure compatibility to Python2
from __future__ import absolute_import, division, print_function

__metaclass__ = type


def result_as_dict(result):
    return {
        "changed": result.changed,
        "failed": result.failed,
        "msg": result.msg,
    }


GENERIC_HTTP_CODES = {
    200: (True, False, "OK: The operation was done successfully"),
    204: (True, False, "Operation done successfully. No further output."),
    400: (False, True, "Bad request: Parameter or validation failure"),
    401: (False, True, "The user is not authorized to do this request"),
    403: (False, True, "Forbidden: Configuration via Setup is disabled"),
    404: (False, True, "Not Found: The requested object has not been found"),
    405: (
        False,
        True,
        "This request is only allowed with other HTTP methods",
    ),
    406: (False, True, "The requests accept headers can not be satisfied"),
    412: (False, True, "If-Match header doesn't match the object's ETag"),
    415: (False, True, "The submitted content-type is not supported"),
    428: (False, True, "The required If-Match header is missing"),
    500: (False, True, "General Server Error"),
}

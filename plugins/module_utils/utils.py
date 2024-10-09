#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2023, Marcel Arentz <gdspd_you@open-one.de>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# Ensure compatibility to Python2
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.checkmk.general.plugins.module_utils.types import RESULT


def result_as_dict(result):
    return {
        "changed": result.changed,
        "failed": result.failed,
        "msg": result.msg,
    }


def merge_results(results):
    """Merges two or more results. Call like this:
    over_all_result = merge_results({"created": create_result, "moved": move_result})"""

    return RESULT(
        http_code=list(results.values())[-1].http_code,
        msg=", ".join(
            ["%s (%d)" % (results[k].msg, results[k].http_code) for k in results.keys()]
        ),
        content=list(results.values())[-1].content,
        etag=list(results.values())[-1].etag,
        failed=any(r.failed for r in list(results.values())),
        changed=any(r.changed for r in list(results.values())),
    )


def remove_null_value_keys(params):
    """Takes the module.params and removes all parameters that are set to 'null'.
    This unsually removes all parameters that are neither explicitly set
    nor provided in the ansible task"""

    for k in list(params.keys()):
        if isinstance(params[k], dict):
            remove_null_value_keys(params[k])
        elif params[k] is None:
            del params[k]


def exit_module(
    module,
    result=None,
    http_code=0,
    msg="",
    content="{}",
    etag="",
    failed=False,
    changed=False,
    logger=None,
):
    if not result:
        result = RESULT(
            http_code=http_code,
            msg=msg,
            content=content,
            etag=etag,
            failed=failed,
            changed=changed,
        )

    result_as_dict = result._asdict()
    if logger:
        result_as_dict["debug"] = logger.get_log()
    module.exit_json(**result_as_dict)


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

#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2023, Marcel Arentz <gdspd_you@open-one.de>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# Ensure compatibility to Python2
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from collections import namedtuple

RESULT = namedtuple("Result", "http_code msg content etag changed failed")

RESULT_DEFAULTS = {
    "msg": "",
    "http_code": -1,
    "failed": True,
    "changed": False,
    "content": "",
    "etag": "",
}


def generate_result(
    msg=RESULT_DEFAULTS["msg"],
    http_code=RESULT_DEFAULTS["http_code"],
    failed=RESULT_DEFAULTS["failed"],
    changed=RESULT_DEFAULTS["changed"],
    content=RESULT_DEFAULTS["content"],
    etag=RESULT_DEFAULTS["etag"],
):
    return RESULT(
        msg=msg,
        http_code=http_code,
        failed=failed,
        changed=changed,
        content=content,
        etag=etag,
    )

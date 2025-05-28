#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2025, Robin Gierse <robin.gierse@checkmk.com>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# Ensure compatibility to Python2
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import base64

from ansible_collections.checkmk.general.plugins.module_utils.api import CheckmkAPI


class ExtendedCheckmkAPI(CheckmkAPI):
    """
    ExtendedCheckmkAPI adds support for multiple authentication methods: bearer, basic, and cookie.
    """

    def __init__(self, module):
        super().__init__(module)
        auth_type = self.params.get("auth_type", "bearer")
        automation_user = self.params.get("automation_user")
        automation_secret = self.params.get("automation_secret")
        auth_cookie = self.params.get("auth_cookie")

        # Bearer Authentication
        if auth_type == "bearer":
            if not automation_user or not automation_secret:
                self.module.fail_json(
                    msg="`automation_user` and `automation_secret` are required for bearer authentication."
                )
            self.headers["Authorization"] = (
                f"Bearer {automation_user} {automation_secret}"
            )

        # Basic Authentication
        elif auth_type == "basic":
            if not automation_user or not automation_secret:
                self.module.fail_json(
                    msg="`automation_user` and `automation_secret` are required for basic authentication."
                )
            auth_str = f"{automation_user}:{automation_secret}"
            auth_b64 = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")
            self.headers["Authorization"] = f"Basic {auth_b64}"

        # Cookie Authentication
        elif auth_type == "cookie":
            if not auth_cookie:
                self.module.fail_json(
                    msg="`auth_cookie` is required for cookie authentication."
                )
            self.cookies["auth_cmk"] = auth_cookie

        else:
            self.module.fail_json(msg=f"Unsupported `auth_type`: {auth_type}")

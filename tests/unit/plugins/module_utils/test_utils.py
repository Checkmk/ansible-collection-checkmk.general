#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2026, Checkmk GmbH
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""`base_api_url()` is the single place the module-side REST base URL is built.

Before it existed, five call sites assembled the URL by hand and had drifted
apart: `api.py` and `downtime.py` guarded a `None` `server_url`, while the
three group modules did not and raised `AttributeError` on it. Covering the
helper once therefore covers `CheckmkAPI` and all four modules that build the
URL without it.

`test_api.py` asserts the same behaviour through `CheckmkAPI`; that is now a
delegation check, and these are the tests of the logic itself.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from ansible_collections.checkmk.general.plugins.module_utils.utils import base_api_url


@pytest.mark.parametrize(
    "server_url",
    [
        "http://myserver",
        "http://myserver/",
        "http://myserver//",
    ],
)
def test_trailing_slash_is_normalized(server_url):
    """A trailing slash must not produce a doubled slash before the site.

    The collection documented the trailing-slash form for years, so both
    have to build the same URL.
    """
    params = {"server_url": server_url, "site": "mysite"}

    assert base_api_url(params) == "http://myserver/mysite/check_mk/api/1.0"


def test_path_prefix_is_preserved():
    """Only trailing slashes are stripped, not a path the user configured."""
    params = {"server_url": "https://myserver/checkmk/", "site": "mysite"}

    assert base_api_url(params) == "https://myserver/checkmk/mysite/check_mk/api/1.0"


def test_missing_server_url_does_not_raise():
    """server_url is required by the argument spec, but building the URL must
    not blow up with a TypeError or AttributeError before Ansible reports that.

    An unset option reaches a module as `None`, not as a missing key, which is
    what `params.get("server_url", "")` got wrong in the group modules.
    """
    assert base_api_url({"server_url": None, "site": "mysite"}) == (
        "/mysite/check_mk/api/1.0"
    )


def test_absent_server_url_key_does_not_raise():
    assert base_api_url({"site": "mysite"}) == "/mysite/check_mk/api/1.0"

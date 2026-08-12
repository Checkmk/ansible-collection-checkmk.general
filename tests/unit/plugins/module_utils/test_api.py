#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2026, Checkmk GmbH
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from unittest.mock import MagicMock

import pytest
from ansible_collections.checkmk.general.plugins.module_utils.api import CheckmkAPI


def _api(server_url, site="mysite"):
    module = MagicMock()
    module.params = {
        "server_url": server_url,
        "site": site,
        "api_auth_type": "bearer",
        "api_user": "myuser",
        "api_secret": "mysecret",
    }
    return CheckmkAPI(module)


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
    assert _api(server_url).url == "http://myserver/mysite/check_mk/api/1.0"


def test_path_prefix_is_preserved():
    """Only trailing slashes are stripped, not a path the user configured."""
    assert (
        _api("https://myserver/checkmk/").url
        == "https://myserver/checkmk/mysite/check_mk/api/1.0"
    )


def test_missing_server_url_does_not_raise():
    """server_url is required by the argument spec, but __init__ must not
    blow up with a TypeError before Ansible reports that."""
    assert _api(None).url == "/mysite/check_mk/api/1.0"

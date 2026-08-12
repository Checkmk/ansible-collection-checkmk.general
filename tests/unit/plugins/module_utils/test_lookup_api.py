#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2026, Checkmk GmbH
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from ansible_collections.checkmk.general.plugins.module_utils.lookup_api import (
    CheckMKLookupAPI,
)


def _api(server_url, site="mysite"):
    return CheckMKLookupAPI(
        server_url=server_url,
        site=site,
        api_user="myuser",
        api_secret="mysecret",
    )


@pytest.mark.parametrize(
    "server_url",
    [
        "http://myserver",
        "http://myserver/",
        "http://myserver//",
    ],
)
def test_trailing_slash_is_normalized(server_url):
    """The collection documented the trailing-slash form for years, so both
    have to build the same URL."""
    assert _api(server_url).url == "http://myserver/mysite/check_mk/api/1.0"


def test_path_prefix_is_preserved():
    """Only trailing slashes are stripped, never a configured path prefix.

    This is why the join is rstrip() and not urljoin(): urljoin treats the last
    path segment as a document, so "https://myserver/checkmk" would lose the
    prefix and resolve to "https://myserver/mysite".
    """
    assert (
        _api("https://myserver/checkmk").url
        == "https://myserver/checkmk/mysite/check_mk/api/1.0"
    )


def test_site_url_is_exposed_without_the_api_path():
    assert _api("http://myserver/").site_url == "http://myserver/mysite"

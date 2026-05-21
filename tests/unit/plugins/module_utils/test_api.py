#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2025, Robin Gierse <robin.gierse@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
from unittest.mock import MagicMock, patch

from ansible_collections.checkmk.general.plugins.module_utils.api import CheckmkAPI


def make_module(overrides=None):
    module = MagicMock()
    module.params = {
        "server_url": "https://checkmk.example.com",
        "site": "mysite",
        "validate_certs": True,
        "proxy_url": None,
        "proxy_user": None,
        "proxy_pass": None,
        "api_auth_type": "bearer",
        "api_user": "automation",
        "api_secret": "secret123",
        "api_auth_cookie": None,
    }
    if overrides:
        module.params.update(overrides)
    module.jsonify = str
    return module


def make_fetch_response(status=200):
    response = MagicMock()
    response.read.return_value = b"{}"
    info = {"status": status, "etag": ""}
    return response, info


class TestProxyURLConstruction:
    def test_no_proxy(self):
        api = CheckmkAPI(make_module())
        assert api._proxy_https is None
        assert api._proxy_http is None

    def test_proxy_url_without_auth(self):
        api = CheckmkAPI(make_module({"proxy_url": "https://proxy.example.com:3128"}))
        assert api._proxy_https == "https://proxy.example.com:3128"
        assert api._proxy_http == "http://proxy.example.com:3128"

    def test_proxy_url_with_auth(self):
        api = CheckmkAPI(
            make_module(
                {
                    "proxy_url": "https://proxy.example.com:3128",
                    "proxy_user": "alice",
                    "proxy_pass": "s3cr3t",
                }
            )
        )
        assert api._proxy_https == "https://alice:s3cr3t@proxy.example.com:3128"
        assert api._proxy_http == "http://alice:s3cr3t@proxy.example.com:3128"

    def test_proxy_url_http_scheme_unchanged(self):
        api = CheckmkAPI(make_module({"proxy_url": "http://proxy.example.com:3128"}))
        assert api._proxy_https == "http://proxy.example.com:3128"
        assert api._proxy_http == "http://proxy.example.com:3128"

    def test_proxy_user_without_pass_not_embedded(self):
        api = CheckmkAPI(
            make_module(
                {
                    "proxy_url": "https://proxy.example.com:3128",
                    "proxy_user": "alice",
                    "proxy_pass": None,
                }
            )
        )
        assert "alice" not in api._proxy_https

    def test_proxy_pass_without_user_not_embedded(self):
        api = CheckmkAPI(
            make_module(
                {
                    "proxy_url": "https://proxy.example.com:3128",
                    "proxy_user": None,
                    "proxy_pass": "s3cr3t",
                }
            )
        )
        assert "s3cr3t" not in api._proxy_https


class TestProxyEnvVars:
    def _run_fetch(self, api, captured_env):
        def fake_fetch_url(module, url, **kwargs):
            captured_env["http_proxy"] = os.environ.get("http_proxy")
            captured_env["https_proxy"] = os.environ.get("https_proxy")
            captured_env["HTTP_PROXY"] = os.environ.get("HTTP_PROXY")
            captured_env["HTTPS_PROXY"] = os.environ.get("HTTPS_PROXY")
            return make_fetch_response(200)

        with patch(
            "ansible_collections.checkmk.general.plugins.module_utils.api.fetch_url",
            fake_fetch_url,
        ):
            for k in ("http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY"):
                os.environ.pop(k, None)
            api._fetch(endpoint="version")

    def test_no_proxy_does_not_set_env_vars(self):
        api = CheckmkAPI(make_module())
        captured = {}
        self._run_fetch(api, captured)
        assert captured["http_proxy"] is None
        assert captured["https_proxy"] is None

    def test_proxy_sets_env_vars_during_fetch(self):
        api = CheckmkAPI(
            make_module(
                {
                    "proxy_url": "https://proxy.example.com:3128",
                    "proxy_user": "alice",
                    "proxy_pass": "s3cr3t",
                }
            )
        )
        captured = {}
        self._run_fetch(api, captured)
        assert captured["https_proxy"] == "https://alice:s3cr3t@proxy.example.com:3128"
        assert captured["http_proxy"] == "http://alice:s3cr3t@proxy.example.com:3128"
        assert captured["HTTPS_PROXY"] == "https://alice:s3cr3t@proxy.example.com:3128"
        assert captured["HTTP_PROXY"] == "http://alice:s3cr3t@proxy.example.com:3128"

    def test_proxy_env_vars_restored_after_fetch(self):
        api = CheckmkAPI(make_module({"proxy_url": "https://proxy.example.com:3128"}))

        def fake_fetch_url(module, url, **kwargs):
            return make_fetch_response(200)

        with patch(
            "ansible_collections.checkmk.general.plugins.module_utils.api.fetch_url",
            fake_fetch_url,
        ):
            for k in ("http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY"):
                os.environ.pop(k, None)
            api._fetch(endpoint="version")

        assert os.environ.get("http_proxy") is None
        assert os.environ.get("https_proxy") is None
        assert os.environ.get("HTTP_PROXY") is None
        assert os.environ.get("HTTPS_PROXY") is None

    def test_proxy_env_vars_restores_previous_values(self):
        api = CheckmkAPI(make_module({"proxy_url": "https://proxy.example.com:3128"}))

        def fake_fetch_url(module, url, **kwargs):
            return make_fetch_response(200)

        with patch(
            "ansible_collections.checkmk.general.plugins.module_utils.api.fetch_url",
            fake_fetch_url,
        ):
            os.environ["https_proxy"] = "https://original.proxy.com"
            os.environ["http_proxy"] = "http://original.proxy.com"
            try:
                api._fetch(endpoint="version")
                assert os.environ.get("https_proxy") == "https://original.proxy.com"
                assert os.environ.get("http_proxy") == "http://original.proxy.com"
            finally:
                os.environ.pop("https_proxy", None)
                os.environ.pop("http_proxy", None)

#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2026, Robin Gierse <robin.gierse@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
from urllib.parse import unquote, urlparse

import pytest
from ansible_collections.checkmk.general.plugins.module_utils.proxy import (
    PROXY_ENV_KEYS,
    build_proxy_url,
    build_proxy_url_from_params,
    proxy_environment,
)


class TestBuildProxyURL:
    def test_no_proxy_url_returns_none(self):
        assert build_proxy_url(None) is None
        assert build_proxy_url("") is None

    def test_plain_url_is_kept_as_is(self):
        assert (
            build_proxy_url("http://proxy.example.com:3128")
            == "http://proxy.example.com:3128"
        )

    def test_https_scheme_is_not_downgraded(self):
        # The scheme describes how to reach the proxy, so it must survive.
        assert (
            build_proxy_url("https://proxy.example.com:3128")
            == "https://proxy.example.com:3128"
        )

    def test_credentials_are_embedded(self):
        assert (
            build_proxy_url("http://proxy.example.com:3128", "alice", "s3cr3t")
            == "http://alice:s3cr3t@proxy.example.com:3128"
        )

    def test_surrounding_whitespace_is_ignored(self):
        assert (
            build_proxy_url("  http://proxy.example.com:3128  ")
            == "http://proxy.example.com:3128"
        )


class TestMissingScheme:
    """'proxy.example.com:3128' must not be parsed as scheme + path."""

    def test_missing_scheme_defaults_to_http(self):
        assert (
            build_proxy_url("proxy.example.com:3128") == "http://proxy.example.com:3128"
        )

    def test_missing_scheme_keeps_host_and_port(self):
        parsed = urlparse(build_proxy_url("proxy.example.com:3128"))
        assert parsed.hostname == "proxy.example.com"
        assert parsed.port == 3128

    def test_missing_scheme_with_credentials(self):
        parsed = urlparse(build_proxy_url("proxy.example.com:3128", "alice", "s3cr3t"))
        assert parsed.hostname == "proxy.example.com"
        assert parsed.username == "alice"
        assert parsed.password == "s3cr3t"


class TestCredentialEncoding:
    """Special characters must be percent encoded, or they corrupt the URL.

    urllib unquotes the credentials again before building the Proxy-Authorization
    header, so the encoded form has to survive a quote/unquote round trip.
    """

    @pytest.mark.parametrize(
        "password",
        ["p@ss", "a/b:c", "with space", "sla/sh", "co:lon", "at@sign", "hash#tag"],
    )
    def test_password_survives_a_round_trip(self, password):
        parsed = urlparse(
            build_proxy_url("http://proxy.example.com:3128", "alice", password)
        )
        assert parsed.hostname == "proxy.example.com"
        assert parsed.port == 3128
        assert unquote(parsed.username) == "alice"
        assert unquote(parsed.password) == password

    @pytest.mark.parametrize("user", ["do/main\\alice", "alice@corp", "a:b"])
    def test_username_survives_a_round_trip(self, user):
        parsed = urlparse(
            build_proxy_url("http://proxy.example.com:3128", user, "s3cr3t")
        )
        assert parsed.hostname == "proxy.example.com"
        assert unquote(parsed.username) == user
        assert unquote(parsed.password) == "s3cr3t"

    def test_explicit_credentials_replace_embedded_ones(self):
        parsed = urlparse(
            build_proxy_url(
                "http://old:creds@proxy.example.com:3128", "alice", "s3cr3t"
            )
        )
        assert parsed.hostname == "proxy.example.com"
        assert parsed.username == "alice"
        assert parsed.password == "s3cr3t"

    def test_embedded_credentials_are_kept_without_explicit_ones(self):
        parsed = urlparse(build_proxy_url("http://bob:hunter2@proxy.example.com:3128"))
        assert parsed.username == "bob"
        assert parsed.password == "hunter2"


class TestValidation:
    def test_user_without_pass_is_rejected(self):
        with pytest.raises(ValueError, match="must be provided together"):
            build_proxy_url("http://proxy.example.com:3128", "alice", None)

    def test_pass_without_user_is_rejected(self):
        with pytest.raises(ValueError, match="must be provided together"):
            build_proxy_url("http://proxy.example.com:3128", None, "s3cr3t")

    def test_credentials_without_proxy_url_are_rejected(self):
        with pytest.raises(ValueError, match="require `proxy_url`"):
            build_proxy_url(None, "alice", "s3cr3t")

    @pytest.mark.parametrize("url", ["socks5://proxy:1080", "ftp://proxy:21"])
    def test_unsupported_scheme_is_rejected(self, url):
        with pytest.raises(ValueError, match="Unsupported scheme"):
            build_proxy_url(url)

    def test_url_without_host_is_rejected(self):
        with pytest.raises(ValueError, match="No host found"):
            build_proxy_url("http://")


class TestBuildFromParams:
    def test_reads_the_module_parameters(self):
        params = {
            "proxy_url": "http://proxy.example.com:3128",
            "proxy_user": "alice",
            "proxy_pass": "s3cr3t",
        }
        assert (
            build_proxy_url_from_params(params)
            == "http://alice:s3cr3t@proxy.example.com:3128"
        )

    def test_tolerates_missing_keys(self):
        assert build_proxy_url_from_params({}) is None


class TestProxyEnvironment:
    def setup_method(self):
        self._saved = {key: os.environ.get(key) for key in PROXY_ENV_KEYS}
        for key in PROXY_ENV_KEYS:
            os.environ.pop(key, None)

    def teardown_method(self):
        for key, value in self._saved.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value

    def test_sets_all_four_variables(self):
        with proxy_environment("http://proxy.example.com:3128"):
            for key in PROXY_ENV_KEYS:
                assert os.environ[key] == "http://proxy.example.com:3128"

    def test_restores_absence(self):
        with proxy_environment("http://proxy.example.com:3128"):
            pass
        for key in PROXY_ENV_KEYS:
            assert key not in os.environ

    def test_restores_previous_values(self):
        os.environ["http_proxy"] = "http://original:3128"
        with proxy_environment("http://proxy.example.com:3128"):
            assert os.environ["http_proxy"] == "http://proxy.example.com:3128"
        assert os.environ["http_proxy"] == "http://original:3128"

    def test_restores_on_exception(self):
        os.environ["https_proxy"] = "http://original:3128"
        with pytest.raises(RuntimeError):
            with proxy_environment("http://proxy.example.com:3128"):
                raise RuntimeError("boom")
        assert os.environ["https_proxy"] == "http://original:3128"

    def test_none_is_a_no_op(self):
        os.environ["http_proxy"] = "http://ambient:3128"
        with proxy_environment(None):
            assert os.environ["http_proxy"] == "http://ambient:3128"
        assert os.environ["http_proxy"] == "http://ambient:3128"

    def test_no_proxy_is_left_alone(self):
        os.environ["no_proxy"] = "localhost,.internal"
        try:
            with proxy_environment("http://proxy.example.com:3128"):
                assert os.environ["no_proxy"] == "localhost,.internal"
        finally:
            os.environ.pop("no_proxy", None)

#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2026, Robin Gierse <robin.gierse@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
from contextlib import contextmanager
from urllib.parse import quote, urlparse, urlunparse

from ansible.module_utils.urls import fetch_url

# Both the lowercase and uppercase spellings are honoured by urllib, so we have
# to set and restore all four of them.
PROXY_ENV_KEYS = ("http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY")

# urllib can only speak to HTTP(S) proxies. Anything else (socks5, ...) would be
# silently ignored, so reject it instead of pretending it works.
SUPPORTED_PROXY_SCHEMES = ("http", "https")

DEFAULT_PROXY_SCHEME = "http"


def build_proxy_url(proxy_url, proxy_user=None, proxy_pass=None):
    """Build a proxy URL suitable for the http_proxy / https_proxy variables.

    Returns None when no proxy is configured. Raises ValueError on invalid input,
    so that callers can turn it into a proper module failure or Ansible error.
    """

    if not proxy_url:
        if proxy_user or proxy_pass:
            raise ValueError(
                "`proxy_user` and `proxy_pass` require `proxy_url` to be set."
            )
        return None

    if bool(proxy_user) != bool(proxy_pass):
        raise ValueError("`proxy_user` and `proxy_pass` must be provided together.")

    proxy_url = proxy_url.strip()

    # Users commonly write 'proxy.example.com:3128'. Without a scheme urlparse()
    # would read 'proxy.example.com' as the scheme and 3128 as the path, so add
    # the default scheme explicitly.
    if "://" not in proxy_url:
        proxy_url = "%s://%s" % (DEFAULT_PROXY_SCHEME, proxy_url)

    parsed = urlparse(proxy_url)

    if parsed.scheme not in SUPPORTED_PROXY_SCHEMES:
        raise ValueError(
            "Unsupported scheme '%s' in `proxy_url`. Supported schemes are: %s."
            % (parsed.scheme, ", ".join(SUPPORTED_PROXY_SCHEMES))
        )

    if not parsed.hostname:
        raise ValueError("No host found in `proxy_url`: %s" % proxy_url)

    netloc = parsed.netloc
    if proxy_user and proxy_pass:
        # Drop credentials already embedded in the URL, an explicit
        # proxy_user / proxy_pass pair wins over them.
        if "@" in netloc:
            netloc = netloc.rsplit("@", 1)[1]
        # The credentials have to be percent encoded. Otherwise characters like
        # '/', ':' or '@' corrupt the URL and the host is parsed incorrectly.
        netloc = "%s:%s@%s" % (
            quote(proxy_user, safe=""),
            quote(proxy_pass, safe=""),
            netloc,
        )

    return urlunparse(parsed._replace(netloc=netloc))


def build_proxy_url_from_params(params):
    """Build the proxy URL from a module's parameters."""

    return build_proxy_url(
        params.get("proxy_url"),
        params.get("proxy_user"),
        params.get("proxy_pass"),
    )


@contextmanager
def proxy_environment(proxy_url):
    """Temporarily export proxy_url through the standard proxy variables.

    The same URL is used for both HTTP and HTTPS traffic: the scheme of a proxy
    URL describes how to reach the proxy, not which traffic it forwards.

    `no_proxy` is deliberately left untouched, so existing bypass lists keep
    working.
    """

    if not proxy_url:
        yield
        return

    saved = {key: os.environ.get(key) for key in PROXY_ENV_KEYS}
    for key in PROXY_ENV_KEYS:
        os.environ[key] = proxy_url

    try:
        yield
    finally:
        for key, value in saved.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def fetch_url_via_proxy(module, *args, **kwargs):
    """Drop-in replacement for ansible.module_utils.urls.fetch_url.

    It applies the module's proxy_url / proxy_user / proxy_pass parameters for
    the duration of the request. Modules that do not go through
    plugins/module_utils/api.py import this under the name `fetch_url`, so that
    all of their existing call sites are covered without further changes.
    """

    try:
        proxy_url = build_proxy_url_from_params(module.params)
    except ValueError as e:
        module.fail_json(msg="Invalid proxy configuration: %s" % e)

    with proxy_environment(proxy_url):
        return fetch_url(module, *args, **kwargs)

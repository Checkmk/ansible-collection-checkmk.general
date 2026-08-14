#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2026, Checkmk GmbH
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Terms passed as a single list must behave like separate terms.

`lookup('checkmk.general.host', my_host_list)` hands run() a single term that
is itself a list. Before self._flatten(), the plugins that concatenate the term
into a path raised `can only concatenate str (not "_AnsibleLazyTemplateList")`,
and the ones that interpolate it with %s silently requested a URL containing
the repr of the list.

A Jinja expression produces an `_AnsibleLazyTemplateList`, not a plain list;
these tests use a plain list because that is what `_flatten()` keys off — the
lazy container subclasses `list`, so the isinstance check treats them alike.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import importlib
import json
from unittest.mock import patch

import pytest

# Every lookup that consumes `terms`. The others (rule, ruleset, bakery,
# version) take their identifier from a named option instead, so they have
# nothing to flatten.
TERM_LOOKUPS = [
    "activation",
    "folder",
    "folders",
    "host",
    "ldap_connection",
    "role",
    "site",
]

OPTIONS = {
    "server_url": "http://myserver",
    "site": "mysite",
    "api_user": "myuser",
    "api_secret": "mysecret",
}

# Satisfies every consumer: `folder` returns the whole response, `folders`
# reads "value", the rest read "extensions".
API_RESPONSE = json.dumps({"extensions": {}, "value": []})


def _run(name, terms):
    """Run a lookup with its API layer stubbed; return (results, api calls).

    Options are stubbed rather than resolved through lookup_loader, which needs
    the collection finder that only ansible-test installs — the same reason
    tests/unit/plugins/inventory/test_checkmk.py stubs get_option(). run() and
    LookupBase._flatten() are the real thing, which is what is under test.

    Calls are returned as strings combining endpoint and query parameters, so
    one assertion can cover both the plugins that put the term in the path and
    `folders`, which puts it in the `parent` parameter.
    """
    module = importlib.import_module(
        "ansible_collections.checkmk.general.plugins.lookup.%s" % name
    )
    lookup = module.LookupModule()
    lookup.set_options = lambda **kwargs: None
    lookup.get_option = OPTIONS.get  # unset options resolve to None

    with patch.object(module, "CheckMKLookupAPI") as api_class:
        api_class.return_value.get.return_value = API_RESPONSE
        results = lookup.run(terms, variables={})

        calls = [
            call.args[0]
            + (
                ""
                if len(call.args) < 2
                else " " + json.dumps(call.args[1], sort_keys=True)
            )
            for call in api_class.return_value.get.call_args_list
        ]

    return results, calls


@pytest.mark.parametrize("name", TERM_LOOKUPS)
def test_a_single_list_term_is_expanded(name):
    """This is the call shape that used to raise TypeError."""
    results, calls = _run(name, [["alpha", "beta"]])

    assert len(calls) == 2
    assert len(results) == 2
    assert any("alpha" in call for call in calls)
    assert any("beta" in call for call in calls)


@pytest.mark.parametrize("name", TERM_LOOKUPS)
def test_separate_terms_still_work(name):
    """Flattening must not regress the documented call shape."""
    results, calls = _run(name, ["alpha", "beta"])

    assert len(calls) == 2
    assert len(results) == 2


@pytest.mark.parametrize("name", TERM_LOOKUPS)
def test_a_single_string_term_still_works(name):
    results, calls = _run(name, ["alpha"])

    assert len(calls) == 1
    assert len(results) == 1
    assert "alpha" in calls[0]


@pytest.mark.parametrize("name", TERM_LOOKUPS)
def test_no_request_contains_a_stringified_list(name):
    """The activation lookup used to build /objects/activation_run/['a', 'b'].

    It interpolates the term with %s, so a list term produced a syntactically
    valid but nonsensical URL and reported a 404 rather than failing loudly.
    """
    _, calls = _run(name, [["alpha", "beta"]])

    for call in calls:
        assert "[" not in call, call

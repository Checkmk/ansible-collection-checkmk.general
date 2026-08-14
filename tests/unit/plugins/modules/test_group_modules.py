#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2026, Checkmk GmbH
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""`title` is optional; when it is omitted the group name is used as the alias.

`get("title", name)` did not deliver that on either of the two paths, for two
different reasons:

* Single group (`name:`): Ansible puts every declared option in params, so the
  key is always present and the dict default never applied.
* Group list (`groups:`): the option is `type="raw"`, so an omitted key really
  is absent and the default did apply — but a bare `title:` in YAML parses to
  None, which the default does not catch.

Either way the alias went out as null, which the API rejected on create and
which made every subsequent run report a change.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import importlib
import json
from unittest.mock import MagicMock, patch

import pytest

# (module name, REST API domain type)
GROUP_MODULES = [
    ("host_group", "host_group_config"),
    ("contact_group", "contact_group_config"),
    ("service_group", "service_group_config"),
]

BASE_URL = "http://myserver/mysite/check_mk/api/1.0"
HEADERS = {"Accept": "application/json"}


# AnsibleModule puts every declared option in params, filling the ones the
# user did not set with None. Reproducing that is the whole point of these
# tests: "title omitted" reaches the module as `title: None`, never as a
# missing key, which is why `params.get("title", name)` never fell back.
DECLARED_OPTIONS = {"name": None, "title": None, "customer": None}


def _module(**params):
    """A stand-in for AnsibleModule with real params and real jsonify."""
    module = MagicMock()
    module.params = dict(DECLARED_OPTIONS, **params)
    module.jsonify = json.dumps
    return module


def _call(plugin, function, **params):
    """Invoke one of the single-group helpers; return the payload it sent.

    `plugin` rather than `name` because `name` is one of the module params
    these tests pass through.
    """
    module_under_test = importlib.import_module(
        "ansible_collections.checkmk.general.plugins.modules.%s" % plugin
    )
    module = _module(**params)

    with patch.object(module_under_test, "fetch_url") as fetch_url:
        fetch_url.return_value = (None, {"status": 200})
        getattr(module_under_test, function % plugin)(module, BASE_URL, HEADERS)

    module.fail_json.assert_not_called()
    request = fetch_url.call_args
    return json.loads(request.args[2]), request.args[1], request.kwargs["method"]


def _call_bulk(plugin, function, groups, **params):
    """Invoke one of the bulk helpers; return the entries it sent.

    `groups` entries are raw dicts straight from the playbook — Ansible does
    not fill in their missing keys, unlike the top-level options.
    """
    module_under_test = importlib.import_module(
        "ansible_collections.checkmk.general.plugins.modules.%s" % plugin
    )
    module = _module(**params)

    with patch.object(module_under_test, "fetch_url") as fetch_url:
        fetch_url.return_value = (None, {"status": 200})
        getattr(module_under_test, function % plugin)(module, BASE_URL, groups, HEADERS)

    module.fail_json.assert_not_called()
    return json.loads(fetch_url.call_args.args[2])["entries"]


# ---------------------------------------------------------------------------
# Create
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("name, domain_type", GROUP_MODULES)
def test_create_without_title_uses_the_name_as_alias(name, domain_type):
    payload, url, method = _call(name, "create_single_%s", name="mygroup")

    assert payload == {"name": "mygroup", "alias": "mygroup"}
    assert url == "%s/domain-types/%s/collections/all" % (BASE_URL, domain_type)
    assert method == "POST"


@pytest.mark.parametrize("name, _domain_type", GROUP_MODULES)
def test_create_with_a_title_uses_the_title(name, _domain_type):
    payload, _url, _method = _call(
        name, "create_single_%s", name="mygroup", title="My Group"
    )

    assert payload == {"name": "mygroup", "alias": "My Group"}


@pytest.mark.parametrize("name, _domain_type", GROUP_MODULES)
def test_create_with_a_customer_keeps_the_alias_fallback(name, _domain_type):
    """The customer branch builds its own payload, so it needs its own check."""
    payload, _url, _method = _call(
        name, "create_single_%s", name="mygroup", customer="provider"
    )

    assert payload == {
        "name": "mygroup",
        "alias": "mygroup",
        "customer": "provider",
    }


# ---------------------------------------------------------------------------
# Update
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("name, domain_type", GROUP_MODULES)
def test_update_without_title_uses_the_name_as_alias(name, domain_type):
    payload, url, method = _call(name, "update_single_%s", name="mygroup")

    assert payload == {"alias": "mygroup"}
    assert url == "%s/objects/%s/mygroup" % (BASE_URL, domain_type)
    assert method == "PUT"


@pytest.mark.parametrize("name, _domain_type", GROUP_MODULES)
def test_update_with_a_title_uses_the_title(name, _domain_type):
    payload, _url, _method = _call(
        name, "update_single_%s", name="mygroup", title="My Group"
    )

    assert payload == {"alias": "My Group"}


# ---------------------------------------------------------------------------
# Bulk create / update (the `groups:` option)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("name, _domain_type", GROUP_MODULES)
def test_bulk_create_falls_back_per_entry(name, _domain_type):
    """Each entry resolves its own alias; a title on one must not affect another."""
    entries = _call_bulk(
        name,
        "create_%ss",
        [{"name": "nogroup"}, {"name": "titled", "title": "Titled"}],
    )

    assert entries == [
        {"name": "nogroup", "alias": "nogroup"},
        {"name": "titled", "alias": "Titled"},
    ]


@pytest.mark.parametrize("name, _domain_type", GROUP_MODULES)
def test_bulk_create_with_an_explicit_null_title_uses_the_name(name, _domain_type):
    """A bare `title:` under a groups entry parses to None, not to a missing key."""
    entries = _call_bulk(name, "create_%ss", [{"name": "mygroup", "title": None}])

    assert entries == [{"name": "mygroup", "alias": "mygroup"}]


@pytest.mark.parametrize("name, _domain_type", GROUP_MODULES)
def test_bulk_create_with_a_customer_keeps_the_alias_fallback(name, _domain_type):
    entries = _call_bulk(
        name,
        "create_%ss",
        [{"name": "mygroup", "title": None}],
        customer="provider",
    )

    assert entries == [{"name": "mygroup", "alias": "mygroup", "customer": "provider"}]


@pytest.mark.parametrize("name, _domain_type", GROUP_MODULES)
def test_bulk_update_falls_back_per_entry(name, _domain_type):
    entries = _call_bulk(
        name,
        "update_%ss",
        [{"name": "nogroup"}, {"name": "titled", "title": "Titled"}],
    )

    assert entries == [
        {"name": "nogroup", "attributes": {"alias": "nogroup"}},
        {"name": "titled", "attributes": {"alias": "Titled"}},
    ]


@pytest.mark.parametrize("name, _domain_type", GROUP_MODULES)
def test_bulk_update_with_an_explicit_null_title_uses_the_name(name, _domain_type):
    entries = _call_bulk(name, "update_%ss", [{"name": "mygroup", "title": None}])

    assert entries == [{"name": "mygroup", "attributes": {"alias": "mygroup"}}]

#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2026, Checkmk GmbH
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Host labels in the inventory plugin.

Labels come from two places and neither alone is enough. The host
configuration knows only the labels somebody typed into Setup, while the
labels that actually apply -- the ones from label rules and from discovery --
are only known to the monitoring core. The plugin therefore reads both and
merges the core's view on top.

Three things about that are easy to get wrong and are pinned here:

* the merge is keyed by the Checkmk host name, which is not necessarily the
  inventory hostname, because ``domain_map`` and ``lowercase_hosts`` rewrite it,
* the host name in the monitoring response is the object id and the ``name``
  column, never a top-level ``name`` key,
* and the core is queried with POST, because the GET variant of that endpoint is
  deprecated and Checkmk 3.0 no longer serves it.

A failure to reach the core is not fatal: an inventory that lists every host
with the configured labels is far more useful than no inventory at all.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json

import pytest
from ansible_collections.checkmk.general.plugins.inventory.checkmk import (
    InventoryModule,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

HOST_COLLECTION_ENDPOINT = "/domain-types/host/collections/all"


class FakeAPI:
    """Records the calls and answers the monitoring query from a canned body."""

    def __init__(self, monitoring_response=None, monitoring_exception=None):
        self.monitoring_response = monitoring_response
        self.monitoring_exception = monitoring_exception
        self.calls = []

    def get(self, endpoint, parameters=None):
        self.calls.append(("GET", endpoint, parameters))
        raise AssertionError("the monitoring core must not be queried with GET")

    def post(self, endpoint, data=None):
        self.calls.append(("POST", endpoint, data))
        if self.monitoring_exception:
            raise self.monitoring_exception
        return json.dumps(self.monitoring_response)


def _raw_host(host_id, labels, tag="prod"):
    """A host as the host_config collection returns it."""
    return {
        "id": host_id,
        "extensions": {
            "title": host_id,
            "folder": "/",
            "attributes": {"ipaddress": "127.0.0.1"},
            "effective_attributes": {
                "site": "mysite",
                "labels": labels,
                "tag_criticality": tag,
            },
        },
    }


def _monitored_host(host_id, labels, with_name_column=True):
    """A host as the monitoring collection returns it.

    The requested livestatus columns land in ``extensions``; ``id`` and
    ``title`` carry the host name.
    """
    extensions = {"labels": labels}
    if with_name_column:
        extensions["name"] = host_id
    return {"id": host_id, "title": host_id, "extensions": extensions}


class FakeInventory:
    def __init__(self):
        self.groups = []
        self.children = []
        self.variables = {}

    def add_group(self, group):
        self.groups.append(group)

    def add_host(self, host):
        pass

    def add_child(self, group, host):
        self.children.append((group, host))

    def set_variable(self, host, key, value):
        self.variables.setdefault(host, {})[key] = value


@pytest.fixture
def plugin():
    module = InventoryModule()
    module.inventory = FakeInventory()
    module.tags = ["tag_criticality"]
    module.groupsources = []
    module.want_ipv4 = False
    return module


# ---------------------------------------------------------------------------
# Reading the effective labels from the monitoring core
# ---------------------------------------------------------------------------


def test_the_core_is_queried_with_post_for_name_and_labels(plugin):
    """GET on this endpoint is deprecated and gone in Checkmk 3.0, and the two
    columns have to be separate list entries, or livestatus sees one column
    called "name,labels" and rejects the query."""
    api = FakeAPI({"value": [_monitored_host("myhost", {"cmk/os_family": "linux"})]})

    labels = plugin._get_livestatus_labels(api)

    assert api.calls == [
        ("POST", HOST_COLLECTION_ENDPOINT, {"columns": ["name", "labels"]})
    ]
    assert labels == {"myhost": {"cmk/os_family": "linux"}}


def test_labels_are_keyed_by_the_host_name_not_a_top_level_field(plugin):
    """There is no top-level ``name`` in the response. Reading one yields None
    for every host, which silently turns the whole merge into a no-op."""
    api = FakeAPI(
        {
            "value": [
                _monitored_host("with-column", {"a": "1"}),
                _monitored_host("without-column", {"b": "2"}, with_name_column=False),
            ]
        }
    )

    assert plugin._get_livestatus_labels(api) == {
        "with-column": {"a": "1"},
        "without-column": {"b": "2"},
    }


def test_a_host_without_labels_is_kept_as_an_empty_mapping(plugin):
    api = FakeAPI({"value": [_monitored_host("myhost", None)]})

    assert plugin._get_livestatus_labels(api) == {"myhost": {}}


@pytest.mark.parametrize(
    "api",
    [
        # The lookup API reports HTTP errors as a body, it does not raise.
        FakeAPI({"code": 403, "msg": "Forbidden", "url": "http://myserver"}),
        FakeAPI(monitoring_exception=ValueError("no JSON at all")),
    ],
    ids=["api_error_body", "unparseable_response"],
)
def test_an_unreachable_core_is_not_fatal(plugin, api):
    """Losing the rule and discovery labels is worth a warning, not a failed
    inventory: the configured labels are still there."""
    assert plugin._get_livestatus_labels(api) == {}


# ---------------------------------------------------------------------------
# Merging them into the hosts
# ---------------------------------------------------------------------------


def test_the_core_wins_and_configured_labels_survive(plugin):
    raw = [_raw_host("myhost", {"cmk/os_family": "windows", "configured": "yes"})]

    hosts = plugin._parse_hosts(raw, {"myhost": {"cmk/os_family": "linux"}})

    assert hosts[0]["labels"] == {
        "cmk/os_family": "linux",
        "configured": "yes",
    }


def test_the_api_response_is_not_mutated(plugin):
    """The parsed hosts must not alias the response, or a second pass over the
    same payload would see labels that were merged in during the first."""
    raw = [_raw_host("myhost", {"configured": "yes"})]

    plugin._parse_hosts(raw, {"myhost": {"from_the_core": "yes"}})

    assert raw[0]["extensions"]["effective_attributes"]["labels"] == {
        "configured": "yes"
    }


def test_hosts_without_labels_get_an_empty_mapping(plugin):
    """``labels`` can be absent entirely or present as null."""
    raw = [_raw_host("no-key", {}), _raw_host("null-value", None)]
    del raw[0]["extensions"]["effective_attributes"]["labels"]

    hosts = plugin._parse_hosts(raw, {})

    assert [host["labels"] for host in hosts] == [{}, {}]


def test_labels_are_merged_before_the_hostname_is_rewritten(plugin):
    """The core knows the Checkmk host name. ``domain_map`` and
    ``lowercase_hosts`` rename hosts, so merging after the rename would look up
    a name the core never reported."""
    plugin.lowercase_hosts = True
    plugin.domain_map = {"tag_criticality_prod": ".example.com"}
    raw = [_raw_host("MYHOST", {"configured": "yes"})]

    hosts = plugin._parse_hosts(raw, {"MYHOST": {"from_the_core": "yes"}})

    assert hosts[0]["id"] == "myhost.example.com"
    assert hosts[0]["labels"] == {"configured": "yes", "from_the_core": "yes"}


# ---------------------------------------------------------------------------
# Exposing them as variables and groups
# ---------------------------------------------------------------------------


def test_labels_are_exposed_even_without_grouping(plugin):
    """``checkmk_labels`` is the reason the labels are always fetched; it does
    not depend on `labels` being a groupsource."""
    plugin.hosts = [
        {
            "id": "myhost",
            "ipaddress": "127.0.0.1",
            "folder": "/",
            "site": "mysite",
            "tags": {},
            "labels": {"cmk/os_family": "linux"},
        }
    ]

    plugin._populate()

    assert plugin.inventory.variables["myhost"]["checkmk_labels"] == {
        "cmk/os_family": "linux"
    }
    assert plugin.inventory.groups == []


def test_a_group_is_created_per_label(plugin):
    """Label groups cannot be pre-created in _generate_groups(), because the
    labels are only known once the hosts have been read."""
    plugin.groupsources = ["labels"]
    plugin.hosts = [
        {
            "id": "linux-host",
            "ipaddress": "127.0.0.1",
            "folder": "/",
            "site": "mysite",
            "tags": {},
            "labels": {"cmk/os_family": "linux", "team": "ops team"},
        },
        {
            "id": "unlabelled-host",
            "ipaddress": "127.0.0.2",
            "folder": "/",
            "site": "mysite",
            "tags": {},
            "labels": {},
        },
    ]

    plugin._populate()

    # Slashes and spaces are not valid in group names.
    assert sorted(plugin.inventory.groups) == [
        "label_cmk_os_family_linux",
        "label_team_opsteam",
    ]
    assert sorted(plugin.inventory.children) == [
        ("label_cmk_os_family_linux", "linux-host"),
        ("label_team_opsteam", "linux-host"),
    ]
    assert plugin.inventory.variables["unlabelled-host"]["checkmk_labels"] == {}

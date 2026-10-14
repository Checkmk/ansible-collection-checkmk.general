#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2026, Checkmk GmbH
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""`prune_none()` and `prune_to_shape()` make `ConfigDiffer` usable on nested data.

`ConfigDiffer` restricts a comparison to the desired keys only at the top
level. Checkmk fills in defaults for nested options it was not given, and an
unset Ansible option arrives as None, which never equals the default the API
reports. Either one made the DCD module report a difference on every run of an
unchanged task, and since DCD connections cannot be updated, the second run
failed (audit findings C-04 and C-13).
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from ansible_collections.checkmk.general.plugins.module_utils.differ import (
    ConfigDiffer,
    prune_none,
    prune_to_shape,
)


@pytest.mark.parametrize(
    "value, expected",
    [
        ({"a": 1, "b": None}, {"a": 1}),
        ({"a": {"b": None, "c": 2}}, {"a": {"c": 2}}),
        ([{"a": None, "b": 1}, {"c": None}], [{"b": 1}, {}]),
        (
            {"a": [], "b": {}, "c": False, "d": 0, "e": ""},
            {"a": [], "b": {}, "c": False, "d": 0, "e": ""},
        ),
        ([None, 1], [None, 1]),
        ("scalar", "scalar"),
        (None, None),
    ],
)
def test_prune_none(value, expected):
    """Only None-valued dict keys go; falsy values and list items stay."""
    assert prune_none(value) == expected


def test_prune_none_does_not_mutate_input():
    value = {"a": {"b": None}}
    prune_none(value)
    assert value == {"a": {"b": None}}


@pytest.mark.parametrize(
    "desired, current, expected",
    [
        # Server-injected keys are dropped at every level.
        ({"a": 1}, {"a": 1, "b": 2}, {"a": 1}),
        ({"a": {"b": 1}}, {"a": {"b": 1, "c": 2}}, {"a": {"b": 1}}),
        (
            {"r": [{"x": 1}, {"x": 2}]},
            {"r": [{"x": 1, "d": 0}, {"x": 2, "d": 0}]},
            {"r": [{"x": 1}, {"x": 2}]},
        ),
        # Keys missing on the server stay missing, so the difference shows.
        ({"a": 1, "b": 2}, {"a": 1}, {"a": 1}),
        # Lists of different length are left alone, so the difference shows.
        (
            {"r": [{"x": 1}]},
            {"r": [{"x": 1, "d": 0}, {"x": 2}]},
            {"r": [{"x": 1, "d": 0}, {"x": 2}]},
        ),
        # Type mismatches return current unchanged.
        ({"a": {"b": 1}}, {"a": "text"}, {"a": "text"}),
        ({"a": [1]}, {"a": {"b": 1}}, {"a": {"b": 1}}),
        ("x", "y", "y"),
    ],
)
def test_prune_to_shape(desired, current, expected):
    assert prune_to_shape(desired, current) == expected


def test_prune_to_shape_does_not_mutate_input():
    current = {"a": {"b": 1, "c": 2}}
    prune_to_shape({"a": {"b": 1}}, current)
    assert current == {"a": {"b": 1, "c": 2}}


# The C-04/C-13 scenario: a DCD connection created from the module's first
# documented example, read back with the defaults Checkmk injects.
DCD_PARAMS = {
    "dcd_id": "PiggybackCluster",
    "title": "Piggyback Configuration for Clusters",
    "comment": "",
    "site": "mysite",
    "connector": {
        "connector_type": "piggyback",
        "interval": 60,
        "creation_rules": [
            {
                "folder_path": "/cluster",
                "delete_hosts": False,
                "host_attributes": None,
            }
        ],
        "discover_on_creation": True,
        "no_deletion_time_after_init": 600,
        "max_cache_age": 3600,
        "validity_period": 60,
    },
}

DCD_CURRENT = {
    "dcd_id": "PiggybackCluster",
    "title": "Piggyback Configuration for Clusters",
    "comment": "",
    "disabled": False,
    "site": "mysite",
    "connector": {
        "connector_type": "piggyback",
        "interval": 60,
        "creation_rules": [
            {
                "folder_path": "/cluster",
                "delete_hosts": False,
                "host_attributes": {"tag_address_family": "no-ip"},
                "matching_hosts": [],
            }
        ],
        "discover_on_creation": True,
        "restrict_source_hosts": [],
        "no_deletion_time_after_init": 600,
        "max_cache_age": 3600,
        "validity_period": 60,
    },
}


def test_unchanged_dcd_needs_no_update():
    desired = prune_none(DCD_PARAMS)
    differ = ConfigDiffer(desired, prune_to_shape(desired, DCD_CURRENT))
    assert not differ.needs_update()


def test_unpruned_dcd_needs_update():
    """Guards the test above: without the helpers the defaults do differ."""
    assert ConfigDiffer(DCD_PARAMS, DCD_CURRENT).needs_update()


def test_changed_nested_dcd_value_needs_update():
    desired = prune_none(DCD_PARAMS)
    desired["connector"]["creation_rules"][0]["folder_path"] = "/other"
    differ = ConfigDiffer(desired, prune_to_shape(desired, DCD_CURRENT))
    assert differ.needs_update()

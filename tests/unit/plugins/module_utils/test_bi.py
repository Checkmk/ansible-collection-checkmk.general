#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2026, Checkmk GmbH
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""The BI helpers turn the BI REST API's responses into objects and ids.

The BI endpoints do not return what the OpenAPI spec says. Responses are flat
rather than wrapped in 'extensions', and a pack lists its rules and
aggregations, like the pack collection lists its packs, as link stubs that
carry the object id only inside the href. These tests pin the shapes that
were observed on real sites.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
from unittest.mock import MagicMock

import pytest
from ansible_collections.checkmk.general.plugins.module_utils.bi import (
    BIObjectAPI,
    _id_from_href,
    collection_ids,
    member_ids,
    object_attributes,
    pack_attributes,
)
from ansible_collections.checkmk.general.plugins.module_utils.types import RESULT

API = "https://myserver/mysite/check_mk/api/1.0"


def _stub(href, collection="items", title=None):
    """A link stub as Checkmk builds it for a collection member."""
    stub = {
        "domainType": "link",
        "method": "GET",
        "type": "application/json",
        "rel": 'urn:org.restfulobjects:rels/value;collection="%s"' % collection,
        "href": href,
    }
    if title:
        stub["title"] = title
    return stub


@pytest.mark.parametrize(
    "href, expected",
    [
        (API + "/objects/bi_rule/my_rule", "my_rule"),
        (API + "/objects/bi_rule/my_rule/", "my_rule"),
        (API + "/objects/bi_rule/my%20rule", "my rule"),
        (API + "/objects/bi_rule/my_rule?x=1#y", "my_rule"),
        ("my_rule", None),
        ("", None),
        (None, None),
        (42, None),
    ],
)
def test_id_from_href(href, expected):
    assert _id_from_href(href) == expected


def test_flat_response_is_returned_without_the_envelope():
    response = {
        "id": "my_rule",
        "pack_id": "",
        "properties": {"title": "My rule"},
        "links": [],
        "domainType": "bi_rule",
    }
    assert object_attributes(response) == {
        "id": "my_rule",
        "pack_id": "",
        "properties": {"title": "My rule"},
    }


def test_wrapped_response_keeps_the_envelope_id():
    response = {"id": "my_pack", "extensions": {"title": "My pack"}, "links": []}
    assert object_attributes(response) == {"id": "my_pack", "title": "My pack"}


def test_pack_members_are_link_stubs():
    """GET /objects/bi_pack/{id} reports rules and aggregations as links."""
    response = {
        "id": "my_pack",
        "title": "My pack",
        "members": {
            "rules": {
                "value": [
                    _stub(API + "/objects/bi_rule/rule_one"),
                    _stub(API + "/objects/bi_rule/rule_two"),
                ]
            },
            "aggregations": {"value": [_stub(API + "/objects/bi_aggregation/aggr")]},
        },
    }
    assert member_ids(response, "rules") == ["rule_one", "rule_two"]
    assert member_ids(response, "aggregations") == ["aggr"]
    assert pack_attributes(response) == {
        "id": "my_pack",
        "title": "My pack",
        "rules": ["rule_one", "rule_two"],
        "aggregations": ["aggr"],
    }


@pytest.mark.parametrize(
    "rules",
    [
        # Objects that carry their own id.
        [{"id": "rule_one"}, {"id": "rule_two"}],
        # A mapping of id to object.
        {"rule_one": {"title": "One"}, "rule_two": {"title": "Two"}},
    ],
)
def test_other_member_shapes_yield_the_same_ids(rules):
    assert member_ids({"rules": rules}, "rules") == ["rule_one", "rule_two"]


def test_missing_or_broken_members_yield_no_ids():
    assert member_ids({}, "rules") == []
    assert member_ids({"rules": None}, "rules") == []
    assert member_ids({"rules": ["not a dict", {"href": ""}]}, "rules") == []


def test_pack_collection_ids_come_from_the_hrefs():
    """The pack collection's stubs have a title, but no id of their own."""
    response = {
        "value": [
            _stub(API + "/objects/bi_pack/default", "all", "Default Pack"),
            _stub(API + "/objects/bi_pack/my_pack", "all", "My pack"),
        ]
    }
    assert collection_ids(response) == ["default", "my_pack"]


class _RuleAPI(BIObjectAPI):
    DOMAIN_TYPE = "bi_rule"
    LABEL = "BI rule"


def _rule_api(monkeypatch, current, desired, check_mode=False):
    """A BIObjectAPI whose GET returns `current`, or 404 if it is None."""
    module = MagicMock()
    module.check_mode = check_mode
    module.params = {
        "server_url": "https://myserver",
        "site": "mysite",
        "api_auth_type": "bearer",
        "api_user": "myuser",
        "api_secret": "mysecret",
    }

    calls = []

    def fetch(code_mapping, endpoint, method="GET", data=None, **kwargs):
        calls.append((method, endpoint, data))
        if method == "GET":
            if current is None:
                return RESULT(404, "", b"", "", False, False)
            return RESULT(200, "", json.dumps(current).encode(), "", False, False)
        code = 204 if method == "DELETE" else 200
        changed, failed, msg = code_mapping[code]
        return RESULT(code, msg, b"", "", changed, failed)

    monkeypatch.setattr(BIObjectAPI, "_fetch", lambda self, **kwargs: fetch(**kwargs))
    return _RuleAPI(module, "my_rule", desired), calls


RULE = {
    "id": "my_rule",
    "pack_id": "my_pack",
    "properties": {"title": "My rule"},
    "computation_options": {"disabled": False},
}


def test_absent_object_is_created(monkeypatch):
    api, calls = _rule_api(monkeypatch, None, RULE)
    result = api.ensure("present")
    assert result.changed and result.msg == "BI rule created."
    assert calls[-1] == ("POST", "/objects/bi_rule/my_rule", RULE)


def test_unchanged_object_is_left_alone(monkeypatch):
    """Checkmk reports pack_id as "" and adds nested defaults; neither differs."""
    current = dict(
        RULE,
        pack_id="",
        computation_options={
            "disabled": False,
            "downtime_only_on_full_problem_coverage": False,
        },
    )
    api, calls = _rule_api(monkeypatch, current, RULE)
    result = api.ensure("present")
    assert not result.changed
    assert [c[0] for c in calls] == ["GET"]


def test_changed_object_is_updated(monkeypatch):
    current = dict(RULE, properties={"title": "Old title"})
    api, calls = _rule_api(monkeypatch, current, RULE)
    result = api.ensure("present")
    assert result.changed and result.msg == "BI rule updated."
    assert calls[-1] == ("PUT", "/objects/bi_rule/my_rule", RULE)


def test_existing_object_is_deleted(monkeypatch):
    api, calls = _rule_api(monkeypatch, RULE, RULE)
    result = api.ensure("absent")
    assert result.changed and result.msg == "BI rule deleted."
    assert calls[-1] == ("DELETE", "/objects/bi_rule/my_rule", None)


def test_absent_object_stays_absent(monkeypatch):
    api, calls = _rule_api(monkeypatch, None, RULE)
    result = api.ensure("absent")
    assert not result.changed
    assert [c[0] for c in calls] == ["GET"]


def test_check_mode_writes_nothing(monkeypatch):
    api, calls = _rule_api(monkeypatch, None, RULE, check_mode=True)
    result = api.ensure("present")
    assert result.changed
    assert result.msg == "Running in check mode. Would have created the BI rule."
    assert [c[0] for c in calls] == ["GET"]

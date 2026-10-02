#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2026, Lars Getwan <lars.getwan@checkmk.com>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
from unittest.mock import patch

import pytest
from ansible.module_utils.testing import patch_module_args
from ansible_collections.checkmk.general.plugins.module_utils.api import CheckmkAPI
from ansible_collections.checkmk.general.plugins.module_utils.types import RESULT
from ansible_collections.checkmk.general.plugins.modules import global_setting

COMMON_PARAMS = {
    "server_url": "https://localhost/",
    "site": "mysite",
    "api_user": "cmkadmin",
    "api_secret": "mysecret",
}

SPEC = {
    "type": "dictionary",
    "title": "Logging",
    "elements": [
        {
            "name": "cmk.web",
            "required": True,
            "default_value": "h30",
            "parameter_form": {
                "type": "single_choice",
                "title": "Web",
                "elements": [
                    {"name": "h30", "title": "Warning"},
                    {"name": "h10", "title": "Debug"},
                ],
            },
        }
    ],
}


def _setting(value, origin, site_id=None):
    body = {"varname": "log_levels", "value": value, "spec": SPEC, "origin": origin}
    if site_id:
        body["site_id"] = site_id
    return body


def _result(code, body=None, etag='"abc"'):
    return RESULT(
        http_code=code,
        msg="",
        content=json.dumps(body or {}).encode("utf-8"),
        etag=etag,
        failed=False,
        changed=code != 200 or body is None,
    )


class Exit(SystemExit):
    """Like the real exit_json, which raises SystemExit."""


def _run(params, responses, check_mode=False, diff=False):
    """Run the module against a queue of fake API responses.

    Returns the exit_json kwargs and the list of (method, endpoint, data) calls.
    """
    calls = []
    queue = list(responses)

    def fake_fetch(self, code_mapping="", endpoint="", data=None, method="GET", **kw):
        calls.append((method, endpoint, data, dict(self.headers)))
        return queue.pop(0)

    captured = {}

    def fake_exit(self, **kwargs):
        captured.update(kwargs)
        raise Exit()

    args = dict(COMMON_PARAMS, **params)
    if check_mode:
        args["_ansible_check_mode"] = True
    if diff:
        args["_ansible_diff"] = True

    with (
        patch_module_args(args),
        patch.object(CheckmkAPI, "_fetch", fake_fetch),
        patch("ansible.module_utils.basic.AnsibleModule.exit_json", fake_exit),
        patch("ansible.module_utils.basic.AnsibleModule.fail_json", fake_exit),
    ):
        with pytest.raises(Exit):
            global_setting.run_module()
    return captured, calls


def test_uses_internal_api_and_site_path():
    out, calls = _run(
        {"name": "log_levels", "site_id": "remote1", "value": {"Web": "Debug"}},
        [_result(200, _setting({"cmk.web": "h10"}, "site", "remote1"))],
    )
    assert calls[0][1] == "objects/site_connection/remote1/global_setting/log_levels"
    assert out["changed"] is False


def test_idempotent_when_equal_and_configured():
    out, calls = _run(
        {"name": "log_levels", "value": {"Web": "Warning"}},
        [_result(200, _setting({"cmk.web": "h30"}, "global"))],
    )
    assert out["changed"] is False
    assert out["value"] == {"Web": "Warning"}
    assert len(calls) == 1


def test_inherited_equal_value_is_pinned():
    out, calls = _run(
        {"name": "log_levels", "value": {"Web": "Warning"}},
        [
            _result(200, _setting({"cmk.web": "h30"}, "factory")),
            _result(200, _setting({"cmk.web": "h30"}, "global")),
        ],
    )
    assert out["changed"] is True
    assert calls[1][0] == "PUT"


def test_update_sends_frontend_value_and_etag():
    out, calls = _run(
        {"name": "log_levels", "value": {"Web": "Debug"}},
        [
            _result(200, _setting({"cmk.web": "h30"}, "global")),
            _result(200, _setting({"cmk.web": "h10"}, "global")),
        ],
        diff=True,
    )
    method, _endpoint, data, headers = calls[1]
    assert method == "PUT"
    assert data == {"value": {"cmk.web": "h10"}}
    assert headers["If-Match"] == '"abc"'
    assert out["changed"] is True
    assert out["value"] == {"Web": "Debug"}
    assert out["diff"]["before"]["value"] == {"Web": "Warning"}


def test_check_mode_does_not_write():
    out, calls = _run(
        {"name": "log_levels", "value": {"Web": "Debug"}},
        [_result(200, _setting({"cmk.web": "h30"}, "global"))],
        check_mode=True,
    )
    assert out["changed"] is True
    assert out["value"] == {"Web": "Debug"}
    assert [c[0] for c in calls] == ["GET"]


def test_invalid_value_fails_without_write():
    out, calls = _run(
        {"name": "log_levels", "value": {"Web": "Loud"}},
        [_result(200, _setting({"cmk.web": "h30"}, "global"))],
    )
    assert out["failed"] is True
    assert "Loud" in out["msg"]
    assert len(calls) == 1


def test_absent_noop_when_at_default():
    out, calls = _run(
        {"name": "log_levels", "state": "absent"},
        [_result(200, _setting({"cmk.web": "h30"}, "factory"))],
    )
    assert out["changed"] is False
    assert len(calls) == 1


def test_absent_site_noop_when_inherited():
    out, calls = _run(
        {"name": "log_levels", "site_id": "remote1", "state": "absent"},
        [_result(200, _setting({"cmk.web": "h30"}, "global", "remote1"))],
    )
    assert out["changed"] is False


def test_absent_deletes_and_rereads():
    out, calls = _run(
        {"name": "log_levels", "site_id": "remote1", "state": "absent"},
        [
            _result(200, _setting({"cmk.web": "h10"}, "site", "remote1")),
            RESULT(204, "", b"", "", True, False),
            _result(200, _setting({"cmk.web": "h30"}, "global", "remote1")),
        ],
    )
    assert [c[0] for c in calls] == ["GET", "DELETE", "GET"]
    assert out["changed"] is True
    assert out["origin"] == "global"


def test_absent_check_mode():
    out, calls = _run(
        {"name": "log_levels", "state": "absent"},
        [_result(200, _setting({"cmk.web": "h10"}, "global"))],
        check_mode=True,
    )
    assert out["changed"] is True
    assert [c[0] for c in calls] == ["GET"]

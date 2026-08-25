#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2026, Checkmk GmbH
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""`exit_module()` is the single exit point of every module that speaks REST.

Before it was used everywhere, modules assembled their own return dict. The
common variant kept only `changed`, `failed` and `msg`, which silently dropped
`http_code`, `content` and `etag` from the task result even where the RETURN
block documented them -- so playbooks could not retry on `http_code` at all.

These tests pin the shape of what reaches Ansible, so that a future
"simplification" back to a hand-built dict fails here instead of in a
playbook. `test_return_contract.py` covers the other half: that the modules
actually route through this helper and document what it emits.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from unittest.mock import MagicMock

from ansible_collections.checkmk.general.plugins.module_utils.types import RESULT
from ansible_collections.checkmk.general.plugins.module_utils.utils import exit_module

A_RESULT = RESULT(
    http_code=200,
    msg="Object created.",
    content='{"id": "my_object"}',
    etag='"deadbeef"',
    failed=False,
    changed=True,
)


def _exited_with(module):
    """Return the kwargs the module was exited with."""
    module.exit_json.assert_called_once()
    return module.exit_json.call_args.kwargs


def test_every_result_field_reaches_ansible():
    """The whole RESULT is returned, not a hand-picked subset of it."""
    module = MagicMock()

    exit_module(module, result=A_RESULT)

    assert _exited_with(module) == {
        "http_code": 200,
        "msg": "Object created.",
        "content": '{"id": "my_object"}',
        "etag": '"deadbeef"',
        "failed": False,
        "changed": True,
    }


def test_keyword_form_fills_in_the_defaults():
    """Callers that have no RESULT yet may pass the fields directly."""
    module = MagicMock()

    exit_module(module, msg="Nothing to be done.")

    assert _exited_with(module) == {
        "http_code": 0,
        "msg": "Nothing to be done.",
        "content": "{}",
        "etag": "",
        "failed": False,
        "changed": False,
    }


def test_result_takes_precedence_over_keywords():
    """A RESULT is never merged with keywords -- it is returned as it is.

    `api.py` passes `failed=True` alongside a result whose `failed` is already
    True. That is redundant rather than wrong, but only because the result
    wins: a caller cannot flip a field of a result by also passing a keyword.
    """
    module = MagicMock()

    exit_module(module, result=A_RESULT, failed=True, msg="ignored")

    exited = _exited_with(module)
    assert exited["failed"] is False
    assert exited["msg"] == "Object created."


def test_failure_is_reported_through_exit_json():
    """A failed result exits via exit_json, not fail_json.

    Ansible fails the task on the `failed` key, so this still surfaces as
    FAILED, and it keeps the full result on a failure as well. The helper has
    no fail_json path at all, which is what makes the return shape uniform.
    """
    module = MagicMock()
    failed = A_RESULT._replace(failed=True, msg="404 - Not Found", http_code=404)

    exit_module(module, result=failed)

    exited = _exited_with(module)
    assert exited["failed"] is True
    assert exited["http_code"] == 404
    module.fail_json.assert_not_called()


def test_logger_output_is_attached_as_debug():
    """With a logger, the collected log is returned as an extra `debug` key."""
    module = MagicMock()
    logger = MagicMock()
    logger.get_log.return_value = "some debug output"

    exit_module(module, result=A_RESULT, logger=logger)

    assert _exited_with(module)["debug"] == "some debug output"


def test_no_debug_key_without_a_logger():
    """Modules that pass no logger must not grow a `debug` key."""
    module = MagicMock()

    exit_module(module, result=A_RESULT)

    assert "debug" not in _exited_with(module)

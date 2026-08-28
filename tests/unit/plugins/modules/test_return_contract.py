#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2026, Checkmk GmbH
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Every REST module returns the same set of keys, and documents them.

The modules that talk to the REST API used to disagree on what a task result
looks like: some returned the full RESULT, some only `changed`/`failed`/`msg`,
and the RETURN blocks did not match either way. A playbook could therefore not
rely on `http_code` being there -- `until: result.http_code != -1` worked on
one module and raised "object of type 'dict' has no attribute 'http_code'" on
the next.

The contract now is: a module that speaks REST exits through `exit_module()`,
which returns every field of the RESULT, and its RETURN block documents exactly
those fields. These tests hold both halves together by reading the sources, so
that a new module cannot quietly opt out.

The four modules that still drive `fetch_url` by hand have no RESULT to return
and legitimately document `msg` only; they are asserted separately rather than
exempted silently.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import glob
import json
import os
import re
from unittest.mock import MagicMock, patch

import pytest
import yaml
from ansible_collections.checkmk.general.plugins.module_utils.types import RESULT

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

MODULES_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "..",
    "..",
    "..",
    "plugins",
    "modules",
)

# The fields exit_module() emits for every module that returns a RESULT.
RESULT_FIELDS = frozenset(RESULT._fields)

# Modules that build their requests with fetch_url() instead of CheckmkAPI.
# They never construct a RESULT, so `msg` is all they can report.
FETCH_URL_MODULES = frozenset(
    {"contact_group", "downtime", "host_group", "service_group"}
)

# `diff` is documented by these two modules but never returned: RESULT has no
# such field and exit_module() only emits the RESULT. Pinned here so the
# mismatch stays visible instead of spreading to further modules.
UNDELIVERED_KEYS = {"dcd": {"diff"}, "ldap": {"diff"}}


def _module_names():
    names = []
    for path in sorted(glob.glob(os.path.join(MODULES_DIR, "*.py"))):
        name = os.path.basename(path)[:-3]
        if name != "__init__":
            names.append(name)
    return names


def _source(name):
    with open(os.path.join(MODULES_DIR, "%s.py" % name)) as source:
        return source.read()


def _documented_keys(name):
    block = re.search(r'^RETURN = r?"""(.*?)^"""', _source(name), re.S | re.M)
    assert block, "%s has no RETURN block" % name
    documented = yaml.safe_load(block.group(1))
    assert isinstance(documented, dict), "%s: RETURN is not a mapping" % name
    return set(documented)


ALL_MODULES = _module_names()
RESULT_MODULES = [name for name in ALL_MODULES if name not in FETCH_URL_MODULES]


# ---------------------------------------------------------------------------
# The sources agree on one way to exit
# ---------------------------------------------------------------------------


def test_the_dropping_helper_is_gone():
    """`result_as_dict()` returned a subset of the RESULT and is what caused
    the divergence. Nothing may reintroduce it."""
    for name in ALL_MODULES:
        assert "result_as_dict" not in _source(name), (
            "%s must exit through exit_module(), not rebuild the result" % name
        )


@pytest.mark.parametrize("name", RESULT_MODULES)
def test_result_modules_exit_through_the_helper(name):
    assert "exit_module(" in _source(name)


@pytest.mark.parametrize("name", RESULT_MODULES)
def test_result_modules_do_not_hand_build_their_result(name):
    """A bare exit_json()/fail_json() splat is how fields got lost before."""
    source = _source(name)
    for call in re.findall(r"\.(?:exit|fail)_json\(\*\*[^)]*\)", source):
        pytest.fail("%s bypasses exit_module(): %s" % (name, call))


# ---------------------------------------------------------------------------
# The documentation agrees with what is returned
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("name", RESULT_MODULES)
def test_result_modules_document_every_returned_field(name):
    """`failed` and `changed` are Ansible's own keys and are never documented;
    the other four are the module's own output and must be."""
    expected = RESULT_FIELDS - {"failed", "changed"}
    missing = expected - _documented_keys(name)

    assert not missing, "%s does not document %s" % (name, sorted(missing))


@pytest.mark.parametrize("name", RESULT_MODULES)
def test_result_modules_document_nothing_extra(name):
    """A documented key that is never returned is as misleading as a missing
    one -- playbooks condition on it and fail."""
    extra = _documented_keys(name) - RESULT_FIELDS - UNDELIVERED_KEYS.get(name, set())

    assert not extra, "%s documents %s, which it cannot return" % (name, sorted(extra))


@pytest.mark.parametrize("name", sorted(FETCH_URL_MODULES))
def test_fetch_url_modules_document_only_msg(name):
    """These have no RESULT, so anything beyond `msg` would be a promise they
    cannot keep. If one of them is ported to CheckmkAPI, drop it from
    FETCH_URL_MODULES and the tests above start applying."""
    assert _documented_keys(name) == {"msg"}
    assert "CheckmkAPI" not in _source(name)


# ---------------------------------------------------------------------------
# ... and the modules really do return it
# ---------------------------------------------------------------------------

API_RESULT = RESULT(
    http_code=200,
    msg="Object created.",
    content=json.dumps({"id": "my_object", "extensions": {}}).encode("utf-8"),
    etag='"ad55730d5488e55e07c58a3da9759fba8cd0b009"',
    failed=False,
    changed=True,
)


def _run_module_with_stubbed_api(module_name, api_name, params, configure_api):
    """Run a module's run_module() against a stubbed API object.

    Returns the kwargs the module exited with, i.e. exactly what a playbook
    would see in its registered variable.
    """
    module_path = "ansible_collections.checkmk.general.plugins.modules.%s" % module_name
    plugin = __import__(module_path, fromlist=["run_module"])

    ansible_module = MagicMock()
    ansible_module.params = params
    ansible_module.check_mode = False

    api = MagicMock()
    api.params = params
    configure_api(api)

    with patch.object(plugin, "AnsibleModule", return_value=ansible_module):
        with patch.object(plugin, api_name, return_value=api):
            plugin.run_module()

    ansible_module.exit_json.assert_called_once()
    return ansible_module.exit_json.call_args.kwargs


def _configure_host(api):
    api.state = "absent"
    api.create.return_value = API_RESULT


def _configure_rule(api):
    api.rule_id_found.return_value = False
    api.create.return_value = API_RESULT


def _configure_notification(api):
    api.rule_id = None
    api.post.return_value = API_RESULT


@pytest.mark.parametrize(
    "module_name,api_name,params,configure_api",
    [
        ("host", "HostAPI", {"state": "present"}, _configure_host),
        (
            "rule",
            "RuleAPI",
            {"state": "present", "rule_id": None},
            _configure_rule,
        ),
        (
            "notification",
            "NotificationRuleAPI",
            {"state": "present"},
            _configure_notification,
        ),
    ],
)
def test_api_result_reaches_the_playbook(module_name, api_name, params, configure_api):
    """The keys a playbook retries on have to survive the exit.

    These three modules assembled their own return dict, so `http_code` and
    `etag` never left the module.
    """
    exited = _run_module_with_stubbed_api(module_name, api_name, params, configure_api)

    assert exited["http_code"] == 200
    assert exited["etag"] == '"ad55730d5488e55e07c58a3da9759fba8cd0b009"'
    assert exited["changed"] is True
    assert exited["failed"] is False


@pytest.mark.parametrize(
    "module_name,api_name,params,configure_api",
    [
        (
            "rule",
            "RuleAPI",
            {"state": "present", "rule_id": None},
            _configure_rule,
        ),
        (
            "notification",
            "NotificationRuleAPI",
            {"state": "present"},
            _configure_notification,
        ),
    ],
)
def test_decoded_content_is_returned_as_a_mapping(
    module_name, api_name, params, configure_api
):
    """These two decode the response body before exiting, which is why they
    document `content` as a dict while the others document the raw string."""
    exited = _run_module_with_stubbed_api(module_name, api_name, params, configure_api)

    assert exited["content"] == {"id": "my_object", "extensions": {}}

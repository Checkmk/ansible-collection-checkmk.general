#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2026, Checkmk GmbH
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Every module documents exactly the keys it returns.

Modules that talk to the REST API exit through `exit_module()`, which returns
all six fields of the RESULT. Their RETURN block has to list the four that are
the module's own output -- `changed` and `failed` are Ansible's own keys and
are never documented.

The four modules in FETCH_URL_MODULES build their requests by hand, have no
RESULT, and so may only document `msg`.

If you add a module and this test fails, copy the RETURN block from an
existing module such as `plugins/modules/host.py` and adjust the descriptions.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import glob
import os
import re

import pytest
import yaml
from ansible_collections.checkmk.general.plugins.module_utils.types import RESULT

MODULES_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "..",
    "..",
    "..",
    "plugins",
    "modules",
)

# What a REST module has to document: the RESULT fields minus Ansible's own.
EXPECTED_KEYS = set(RESULT._fields) - {"failed", "changed"}

# These use fetch_url() instead of CheckmkAPI and can only report `msg`.
# Port one of them to CheckmkAPI and remove it here, and it gets checked
# like all the others.
FETCH_URL_MODULES = {"contact_group", "downtime", "host_group", "service_group"}

# `dcd` and `ldap` document a `diff` key that exit_module() cannot return.
# Listed here so the mismatch stays visible instead of spreading.
KNOWN_EXTRA_KEYS = {"dcd": {"diff"}, "ldap": {"diff"}}


def _documented_keys(module_name):
    """The top-level keys of a module's RETURN block."""
    path = os.path.join(MODULES_DIR, "%s.py" % module_name)
    with open(path) as source:
        block = re.search(r'^RETURN = r?"""(.*?)^"""', source.read(), re.S | re.M)

    assert block, "%s has no RETURN block" % module_name
    return set(yaml.safe_load(block.group(1)))


def _module_names():
    paths = sorted(glob.glob(os.path.join(MODULES_DIR, "*.py")))
    names = [os.path.basename(path)[:-3] for path in paths]
    return [name for name in names if name != "__init__"]


REST_MODULES = [name for name in _module_names() if name not in FETCH_URL_MODULES]


@pytest.mark.parametrize("module_name", REST_MODULES)
def test_rest_modules_document_the_result_keys(module_name):
    documented = _documented_keys(module_name)
    allowed = EXPECTED_KEYS | KNOWN_EXTRA_KEYS.get(module_name, set())

    assert not EXPECTED_KEYS - documented, "%s does not document %s" % (
        module_name,
        sorted(EXPECTED_KEYS - documented),
    )
    assert not documented - allowed, "%s documents %s, which it cannot return" % (
        module_name,
        sorted(documented - allowed),
    )


@pytest.mark.parametrize("module_name", sorted(FETCH_URL_MODULES))
def test_fetch_url_modules_document_only_msg(module_name):
    assert _documented_keys(module_name) == {"msg"}

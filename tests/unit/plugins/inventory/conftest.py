#!/usr/bin/env python

import sys
import importlib

fake_lookupapi = importlib.import_module(
    "ansible_collections.checkmk.general.tests.unit.plugins.module_utils.lookup_api"
)
sys.modules[
    "ansible_collections.checkmk.general.plugins.module_utils.lookup_api"
] = fake_lookupapi

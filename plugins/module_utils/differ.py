#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2025, Lars Getwan <lars.getwan@checkmk.com>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# This code was originally authored by Atruvia AG (https://atruvia.de/)
# and subsequently modified by Checkmk.
# Thank you so much for donating this code!

# Ensure compatibility to Python2
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json


def prune_none(value):
    """Recursively drop dictionary keys whose value is None.

    Unset Ansible options arrive as None all the way down a nested argument
    spec. The Checkmk API rejects explicit nulls with "Field may not be null"
    rather than treating them as absent, and an unset option must not take
    part in a comparison either: None never equals the default the API
    reports for that field.

    Args:
        value: An arbitrarily nested structure of dicts, lists and scalars.

    Returns:
        The same structure with all None-valued dictionary keys removed.
    """
    if isinstance(value, dict):
        return {k: prune_none(v) for k, v in value.items() if v is not None}
    if isinstance(value, list):
        return [prune_none(v) for v in value]
    return value


def prune_to_shape(desired, current):
    """Reduce current to the keys desired actually specifies, recursively.

    Checkmk fills in defaults for nested options it was not given, so a
    playbook that specifies a subset of a nested dict would otherwise differ
    from the server on every run. ConfigDiffer only restricts the comparison
    at the top level, so nested structures need this before being handed to
    it.

    Lists are only descended into when both sides have the same length, so a
    genuine difference in list length is still reported.

    Args:
        desired: The configuration the user asked for.
        current: The configuration the server reports.

    Returns:
        The current configuration, pruned to the shape of the desired one.
    """
    if isinstance(desired, dict) and isinstance(current, dict):
        return {
            k: prune_to_shape(desired[k], current[k]) for k in desired if k in current
        }
    if isinstance(desired, list) and isinstance(current, list):
        if len(desired) == len(current):
            return [prune_to_shape(d, c) for d, c in zip(desired, current)]
    return current


class ConfigDiffer:
    """
    Handles the normalization and comparison of configuration dictionaries.
    """

    def __init__(self, desired, current):
        self.desired = desired
        self.current = current
        self.reference_keys = list(desired.keys())
        self.desired_cleaned = {}
        self.current_cleaned = {}

    def normalize(self):
        """
        Normalizes the desired and current configurations.
        """
        self.desired_cleaned = self.clean_for_diff(self.desired.copy())
        self.current_cleaned = self.clean_for_diff(self.current.copy())

    def needs_update(self):
        """
        Determines whether an update is needed.
        """
        self.normalize()
        return self.desired_cleaned != self.current_cleaned

    def clean_for_diff(self, data):
        """
        Cleans data dictionaries by keeping only keys present in reference_keys and normalizing the values.
        """
        cleaned = {}
        for key in self.reference_keys:
            if key in data:
                value = data[key]
                if isinstance(value, dict):
                    cleaned[key] = self._normalize_dict(value)
                elif isinstance(value, list):
                    cleaned[key] = self._normalize_list(value)
                else:
                    cleaned[key] = self._normalize_value(value)
        return cleaned

    def _normalize_value(self, value):
        if isinstance(value, (bool, int)):
            return value
        elif isinstance(value, str):
            return value.strip()
        else:
            return value

    def _normalize_list(self, value):
        normalized_list = []
        for item in value:
            if isinstance(item, dict):
                normalized_list.append(self._normalize_dict(item))
            elif isinstance(item, list):
                normalized_list.append(self._normalize_list(item))
            else:
                normalized_list.append(self._normalize_value(item))
        return sorted(normalized_list, key=lambda x: json.dumps(x, sort_keys=True))

    def _normalize_dict(self, data):
        normalized_dict = {}
        for k, v in data.items():
            if isinstance(v, dict):
                normalized_dict[k] = self._normalize_dict(v)
            elif isinstance(v, list):
                normalized_dict[k] = self._normalize_list(v)
            else:
                normalized_dict[k] = self._normalize_value(v)
        return normalized_dict

    def generate_diff(self, deletion=False):
        """
        Generates a diff between the current and desired state.
        """
        self.normalize()

        if deletion:
            before = json.dumps(self.current_cleaned, indent=2, sort_keys=True) + "\n"
            after = "{}" + "\n"
        else:
            before = json.dumps(self.current_cleaned, indent=2, sort_keys=True) + "\n"
            after = json.dumps(self.desired_cleaned, indent=2, sort_keys=True) + "\n"

        return dict(before=before, after=after)

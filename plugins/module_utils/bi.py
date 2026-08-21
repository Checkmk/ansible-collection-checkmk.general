#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2025, Lars Getwan <lars.getwan@checkmk.com>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# Ensure compatibility to Python2
from __future__ import absolute_import, division, print_function

__metaclass__ = type


def member_values(response, name):
    """Return the objects of a named member collection of a domain object.

    'GET /objects/bi_pack/{pack_id}' returns the pack together with its rules
    and aggregations. Those are nested in the 'members' container of the domain
    object, and Checkmk has used more than one shape for it over time. Rather
    than guessing, accept every shape we have seen and always return a list.

    Args:
        response (dict): The decoded domain object returned by the REST API.
        name (str): Name of the member collection, e.g. 'rules'.

    Returns:
        list: The objects of that member collection, empty if there are none.
    """
    members = response.get("members") or {}
    member = members.get(name)

    # A member collection, i.e. {"members": {"rules": {"value": [...]}}}
    if isinstance(member, dict):
        value = member.get("value")
        if isinstance(value, list):
            return value
        if isinstance(value, dict):
            return list(value.values())
        return []

    # An already flattened list, i.e. {"members": {"rules": [...]}}
    if isinstance(member, list):
        return member

    # Older responses put the collections next to 'extensions' instead.
    fallback = response.get(name)
    if isinstance(fallback, list):
        return fallback
    if isinstance(fallback, dict):
        return list(fallback.values())

    return []


def prune_none(value):
    """Recursively drop keys whose value is None.

    Unset Ansible options arrive as None all the way down a nested argument
    spec, and the Checkmk API rejects explicit nulls with
    "Field may not be null" rather than treating them as absent.

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

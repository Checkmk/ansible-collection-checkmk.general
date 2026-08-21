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


# Keys that belong to the REST API's domain object envelope rather than to the
# object itself. 'id' is deliberately absent: for a flat BI response it is a
# real attribute of the object.
ENVELOPE_KEYS = ("links", "domainType", "members", "extensions")


def object_attributes(response):
    """Return an object's own attributes from a REST API response.

    The BI endpoints are not consistent about wrapping. Some responses are
    domain objects carrying the attributes in 'extensions', others return the
    attributes flat at the top level. Reading only 'extensions' yields an empty
    dict for the flat form, which makes every comparison report a difference.

    Args:
        response (dict): The decoded API response.

    Returns:
        dict: The object's attributes, whichever form the response took.
    """
    extensions = response.get("extensions")
    if isinstance(extensions, dict) and extensions:
        attributes = dict(extensions)
        # For the wrapped form the identifier lives on the envelope.
        attributes.setdefault("id", response.get("id"))
        return attributes

    return {k: v for k, v in response.items() if k not in ENVELOPE_KEYS}


def restrict_to_shape(desired, current):
    """Reduce current to the keys desired actually specifies, recursively.

    Checkmk fills in defaults for nested options it was not given, so a
    playbook that specifies a subset of a nested dict would otherwise differ
    from the server on every run. ConfigDiffer only restricts the comparison at
    the top level, so nested dicts need this treatment before being handed to
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
            k: restrict_to_shape(desired[k], current[k])
            for k in desired
            if k in current
        }
    if isinstance(desired, list) and isinstance(current, list):
        if len(desired) == len(current):
            return [restrict_to_shape(d, c) for d, c in zip(desired, current)]
    return current

#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2025, Lars Getwan <lars.getwan@checkmk.com>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# Ensure compatibility to Python2
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.six.moves.urllib.parse import unquote


def _with_id(key, value):
    """Restore an object's id when a collection was keyed by it.

    Checkmk returns some collections as a mapping of object id to object, and
    the object itself then carries no 'id' of its own. Flattening such a
    mapping to a list would throw the identifier away.

    Args:
        key: The mapping key the object was stored under.
        value: The object.

    Returns:
        The object, with 'id' set from the key if it had none.
    """
    if isinstance(value, dict) and not value.get("id"):
        return dict(value, id=key)
    return value


def _as_list(collection):
    """Return a member collection as a list, whether it was a list or a mapping."""
    if isinstance(collection, list):
        return collection
    if isinstance(collection, dict):
        return [_with_id(k, v) for k, v in collection.items()]
    return []


def member_values(response, name):
    """Return the objects of a named collection of a BI pack response.

    'GET /objects/bi_pack/{pack_id}' returns the pack together with its rules
    and aggregations. Checkmk has used more than one shape for that over time:
    nested in the 'members' container of a domain object, or alongside the
    pack's own attributes in a flat response, and as either a list or a mapping
    of id to object. Rather than guessing, accept all of them and always return
    a list of objects that carry their 'id'.

    Args:
        response (dict): The decoded API response.
        name (str): Name of the collection, e.g. 'rules'.

    Returns:
        list: The objects of that collection, empty if there are none.
    """
    collection = (response.get("members") or {}).get(name)

    if collection is None:
        # Flat responses carry the collections next to the pack's attributes.
        collection = response.get(name)

    # A member collection wrapper, i.e. {"value": [...]}
    if isinstance(collection, dict) and "value" in collection:
        collection = collection.get("value")

    return _as_list(collection)


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


def _id_from_href(href):
    """Return the object id from the tail of a REST API object URL.

    Args:
        href (str): A link such as '.../api/1.0/objects/bi_rule/my_rule'.

    Returns:
        str: The last path segment, percent-decoded, or None if there is none.
    """
    if not href or not isinstance(href, str):
        return None

    path = href.split("?")[0].split("#")[0].rstrip("/")
    if "/" not in path:
        return None

    return unquote(path.rsplit("/", 1)[-1]) or None


def member_ids(response, name):
    """Return the ids of the objects in a named collection of a BI pack.

    'GET /objects/bi_pack/{pack_id}' reports a pack's rules and aggregations as
    HATEOAS link stubs rather than as objects:

        {"domainType": "link", "method": "GET", "type": "application/json",
         "rel": "urn:org.restfulobjects:rels/value;collection=\"items\"",
         "href": ".../api/1.0/objects/bi_rule/my_rule"}

    Checkmk has no bulk endpoint for BI rules or aggregations, so the objects
    can only be fetched one at a time. The plural lookups therefore return ids
    and leave hydration to the singular lookups, which accept a list of ids.

    Args:
        response (dict): The decoded API response.
        name (str): Name of the collection, e.g. 'rules'.

    Returns:
        list: The ids of the objects in that collection, in the order reported.
    """
    ids = []
    for entry in member_values(response, name):
        if not isinstance(entry, dict):
            continue

        # An object carries its own id; a link stub only has the URL.
        object_id = entry.get("id") or _id_from_href(entry.get("href"))
        if object_id:
            ids.append(object_id)

    return ids

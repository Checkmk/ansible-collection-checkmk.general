#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2025, Lars Getwan <lars.getwan@checkmk.com>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# Ensure compatibility to Python2
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json

from ansible.module_utils.six.moves.urllib.parse import unquote
from ansible_collections.checkmk.general.plugins.module_utils.api import CheckmkAPI
from ansible_collections.checkmk.general.plugins.module_utils.differ import (
    ConfigDiffer,
    prune_to_shape,
)
from ansible_collections.checkmk.general.plugins.module_utils.types import RESULT


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
    can only be fetched one at a time, by these ids.

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


def collection_ids(response):
    """Return the ids of the objects in a domain-type collection response.

    'GET /domain-types/bi_pack/collections/all' reports its packs the same way a
    pack reports its rules: as link stubs under 'value', built by
    constructors.collection_item(), which carries the identifier only inside the
    href. So the ids are extracted rather than read off the objects.

    Args:
        response (dict): The decoded API response.

    Returns:
        list: The ids of the objects in the collection.
    """
    return member_ids(response, "value")


def pack_attributes(response):
    """Return a BI pack from its REST API response, with member ids.

    The pack endpoint reports the pack's rules and aggregations as links
    rather than as objects, so they are exposed as lists of ids.

    Args:
        response (dict): The decoded response of 'GET /objects/bi_pack/{id}'.

    Returns:
        dict: The pack's attributes, plus 'rules' and 'aggregations' ids.
    """
    pack = object_attributes(response)
    pack["rules"] = member_ids(response, "rules")
    pack["aggregations"] = member_ids(response, "aggregations")
    return pack


class BIObjectAPI(CheckmkAPI):
    """Create, update and delete a single BI pack, rule or aggregation.

    All three live on one object endpoint each, '/objects/<domain type>/<id>',
    which takes GET, POST (create), PUT (update) and DELETE. None of them
    uses ETags.

    Subclasses set DOMAIN_TYPE and LABEL and pass the desired state, already
    stripped of unset options with prune_none().
    """

    DOMAIN_TYPE = ""
    LABEL = ""

    def __init__(self, module, object_id, desired):
        super().__init__(module)
        self.endpoint = "/objects/%s/%s" % (self.DOMAIN_TYPE, object_id)
        self.desired = desired

        result = self._fetch(
            code_mapping={404: (False, False, "%s not found." % self.LABEL)},
            endpoint=self.endpoint,
            method="GET",
        )
        self.exists = result.http_code == 200
        self.current = (
            object_attributes(json.loads(result.content)) if self.exists else {}
        )

        # Rules and aggregations report pack_id as "" rather than the pack
        # they belong to, so it cannot be compared. Use the desired value
        # while the API reports none. Moving an object to another pack is
        # therefore not detected.
        if self.exists and "pack_id" in desired and not self.current.get("pack_id"):
            self.current["pack_id"] = desired["pack_id"]

    def needs_update(self):
        # Checkmk fills in defaults for options it was not given, so compare
        # only what the playbook actually specified.
        return ConfigDiffer(
            self.desired, prune_to_shape(self.desired, self.current)
        ).needs_update()

    def _write(self, method, done, data=None):
        if self.module.check_mode:
            return RESULT(
                http_code=0,
                msg="Running in check mode. Would have %s the %s." % (done, self.LABEL),
                content="",
                etag="",
                failed=False,
                changed=True,
            )

        message = "%s %s." % (self.LABEL, done)
        return self._fetch(
            code_mapping={
                200: (True, False, message),
                201: (True, False, message),
                204: (True, False, message),
            },
            endpoint=self.endpoint,
            data=data,
            method=method,
        )

    def ensure(self, state):
        """Bring the object into the given state and return the RESULT."""
        if state == "present":
            if not self.exists:
                return self._write("POST", "created", self.desired)
            if self.needs_update():
                return self._write("PUT", "updated", self.desired)
            msg = "%s is already in the desired state." % self.LABEL
        elif self.exists:
            return self._write("DELETE", "deleted")
        else:
            msg = "%s is already absent." % self.LABEL

        return RESULT(
            http_code=0,
            msg=msg,
            content="",
            etag="",
            failed=False,
            changed=False,
        )

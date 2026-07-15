#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2025, Lars Getwan <lars.getwan@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: downtime

short_description: Manage downtimes in Checkmk

version_added: "6.7.0"

description:
    - Create, update and delete host and service downtimes in Checkmk.
    - An existing downtime can be updated (e.g. to shorten or extend its end time)
      without deleting and recreating it. The downtime to act on can be identified
      by its ID, by host name (and optionally service descriptions), or by a
      Livestatus query.
    - This module is idempotent. It only changes downtimes when the desired end
      time or comment differs from the current state.

extends_documentation_fragment: [checkmk.general.common]

options:
    downtime_id:
        description:
            - The numeric ID of a single downtime to update or delete.
            - Requires I(site_id) to be set as well.
            - Mutually exclusive with I(host_name) and I(query).
        required: false
        type: str
    site_id:
        description:
            - The site the downtime lives on. Required when using I(downtime_id).
        required: false
        type: str
    host_name:
        description:
            - The host to schedule, update or delete a downtime for.
            - Mutually exclusive with I(downtime_id) and I(query).
        required: false
        type: str
    service_descriptions:
        description:
            - A list of service descriptions.
            - If set together with I(host_name), the module acts on service
              downtimes for these services. If omitted, it acts on host downtimes.
        required: false
        type: list
        elements: str
        default: []
    query:
        description:
            - A Livestatus query as a JSON string, written in terms of the
              Livestatus C(downtimes) table (e.g. C(host_name),
              C(service_description), C(comment)). See the Checkmk REST API
              documentation for the query syntax.
            - The same query columns are used for B(create), B(update) and
              B(delete). For query-based B(create) the module automatically
              translates the columns to the queried object's table (C(host_name)
              becomes C(name) for hosts, C(service_description) becomes
              C(description) for services), so one query works for all operations.
            - Mutually exclusive with I(downtime_id) and I(host_name).
        required: false
        type: str
    downtime_type:
        description:
            - Selects whether a query operates on host downtimes (C(host)) or
              service downtimes (C(service)).
            - Required for query-based B(create) to choose the object type. For
              B(update)/B(delete) it optionally narrows the matched downtimes to
              that type.
        required: false
        type: str
        choices: ["host", "service"]
    comment:
        description:
            - The comment of the downtime.
            - When creating or matching a downtime by I(host_name), the comment is
              part of the identity of the downtime. If omitted, C(Managed by Ansible)
              is used.
            - When updating a downtime by I(downtime_id) or I(query), the comment is
              only changed if it is explicitly set here.
            - When deleting by I(host_name), the deletion is limited to downtimes
              with this comment if it is set, otherwise all matching downtimes are
              removed.
        required: false
        type: str
    start_time:
        description:
            - The start datetime of a new downtime, conforming to the ISO 8601
              profile, e.g. C(2017-07-21T17:32:28Z). Defaults to now.
            - Only relevant when creating a downtime.
        required: false
        type: str
    start_after:
        description:
            - The timedelta between now and the start time. Use this instead of
              I(start_time). For keys and values see
              U(https://docs.python.org/3/library/datetime.html#datetime.timedelta).
            - Only relevant when creating a downtime.
        required: false
        type: dict
        default: {}
    end_time:
        description:
            - The end datetime of the downtime, conforming to the ISO 8601 profile,
              e.g. C(2017-07-21T17:32:28Z).
            - Used both when creating and when updating a downtime.
        required: false
        type: str
    end_after:
        description:
            - The timedelta between the start time and the end time. Use this
              instead of I(end_time). For keys and values see
              U(https://docs.python.org/3/library/datetime.html#datetime.timedelta).
            - When updating an existing downtime, the delta is applied relative to
              the (defaulted) start time, i.e. now.
        required: false
        type: dict
        default: {}
    duration:
        description:
            - Duration in minutes. When set, the downtime does not begin
              automatically at a nominated time, but when a non-OK status actually
              appears for the host (flexible downtime).
            - Only relevant when creating a downtime.
        required: false
        type: int
        default: 0
    recur:
        description:
            - The recurring mode of a new downtime.
            - Only relevant when creating a downtime.
        required: false
        type: str
        default: fixed
        choices:
            - fixed
            - hour
            - day
            - week
            - second_week
            - fourth_week
            - weekday_start
            - weekday_end
            - day_of_month
    force:
        description:
            - When creating a downtime by I(host_name), a new downtime is normally
              only created if no downtime with the same host, service and comment
              exists yet. Set this to C(true) to always create a new downtime.
        required: false
        type: bool
        default: false
    state:
        description:
            - The desired state of the downtime.
        required: false
        type: str
        default: present
        choices: ["present", "absent"]

notes:
    - Creating a downtime is possible via I(host_name) or via I(query) (using
      I(downtime_type) to choose host or service). Updating and deleting can be
      done via I(downtime_id), I(host_name) or I(query).
    - Idempotency is based on the current end time and comment of the matching
      downtimes. Absolute times (I(end_time)) are fully idempotent. Relative times
      (I(end_after)) are recomputed on every run and will therefore usually trigger
      an update.
    - On the Checkmk Raw edition (renamed I(Community) in 2.5) the Nagios core
      cannot modify a downtime in place. When an existing downtime needs its end
      time or comment changed on that edition, the module deletes and re-creates
      it. The resulting downtime is identical except that it receives a new
      downtime ID. On CMC-based editions the downtime is modified in place and
      keeps its ID.

seealso:
    - plugin: checkmk.general.downtime
      plugin_type: lookup
    - plugin: checkmk.general.downtimes
      plugin_type: lookup

author:
    - Oliver Gaida (@ogaida) -- Original implementation
    - Lars Getwan (@lgetwan), with the help of Claude -- Modified version
"""

EXAMPLES = r"""
# ---------------------------------------------------------------------------
# Creating downtimes
# ---------------------------------------------------------------------------

- name: "Schedule a host downtime starting now, ending in 2 hours."
  checkmk.general.downtime:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    host_name: "myhost"
    end_after:
      hours: 2

- name: "Schedule a host downtime using absolute start and end times."
  checkmk.general.downtime:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    host_name: "myhost"
    comment: "Patch window"
    start_time: "2024-03-25T22:00:00Z"
    end_time: "2024-03-26T02:00:00Z"

- name: "Schedule downtimes for multiple services on a host."
  checkmk.general.downtime:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    host_name: "myhost"
    comment: "Patch window"
    service_descriptions:
      - "CPU utilization"
      - "Memory"
    end_after:
      hours: 1

- name: "Schedule host downtimes for all hosts matching a query."
  checkmk.general.downtime:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    query: '{"op": "~", "left": "host_name", "right": "^web"}'
    downtime_type: "host"
    comment: "Rolling web tier maintenance"
    end_after:
      hours: 2

- name: "Schedule service downtimes for all services matching a query."
  checkmk.general.downtime:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    query: '{"op": "=", "left": "service_description", "right": "Filesystem /"}'
    downtime_type: "service"
    comment: "Storage migration"
    end_after:
      hours: 1

# ---------------------------------------------------------------------------
# Updating an existing downtime (solves issue #672)
# ---------------------------------------------------------------------------
# Re-running the same host_name + comment with a different end time shortens or
# extends the existing downtime instead of doing nothing.

- name: "Shorten the previously created downtime."
  checkmk.general.downtime:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    host_name: "myhost"
    comment: "Patch window"
    end_after:
      minutes: 1

- name: "Update a specific downtime by its ID."
  checkmk.general.downtime:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    downtime_id: "42"
    site_id: "mysite"
    end_time: "2024-03-26T00:00:00Z"
    comment: "Window reduced"

- name: "Update all downtimes matching a query."
  checkmk.general.downtime:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    query: '{"op": "=", "left": "host_name", "right": "myhost"}'
    end_after:
      minutes: 30

# On the host_name path the comment is part of the downtime's identity, so a
# different comment is treated as a different downtime and a new one is created.
# To change the comment of an existing downtime, select it by a query (e.g. by
# its host and current comment) and set the new comment; the query matches the
# downtime independently of the comment you are about to write.
- name: "Change the comment of an existing downtime."
  checkmk.general.downtime:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    query: '{"op": "and", "expr": [{"op": "=", "left": "host_name", "right": "myhost"}, {"op": "=", "left": "comment", "right": "Patch window"}]}'
    comment: "Pitch window"

# ---------------------------------------------------------------------------
# Deleting downtimes
# ---------------------------------------------------------------------------

- name: "Remove all downtimes from a host."
  checkmk.general.downtime:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    host_name: "myhost"
    state: "absent"

- name: "Remove only host downtimes with a specific comment."
  checkmk.general.downtime:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    host_name: "myhost"
    comment: "Patch window"
    state: "absent"

- name: "Delete a specific downtime by its ID."
  checkmk.general.downtime:
    server_url: "https://myserver/"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    downtime_id: "42"
    site_id: "mysite"
    state: "absent"

# ---------------------------------------------------------------------------
# Using environment variables for authentication
# ---------------------------------------------------------------------------
# Connection parameters can be provided via environment variables instead of
# task parameters. The supported variables are:
#   CHECKMK_VAR_SERVER_URL, CHECKMK_VAR_SITE,
#   CHECKMK_VAR_API_USER, CHECKMK_VAR_API_SECRET,
#   CHECKMK_VAR_VALIDATE_CERTS

- name: "Schedule a host downtime using environment variables for authentication."
  checkmk.general.downtime:
    host_name: "myhost"
    comment: "Maintenance via env-based auth"
    end_after:
      hours: 2
  environment:
    CHECKMK_VAR_SERVER_URL: "https://myserver/"
    CHECKMK_VAR_SITE: "mysite"
    CHECKMK_VAR_API_USER: "myuser"
    CHECKMK_VAR_API_SECRET: "mysecret"
    CHECKMK_VAR_VALIDATE_CERTS: "true"
"""

RETURN = r"""
msg:
    description:
        - The output message that the module generates.
    type: str
    returned: always
http_code:
    description:
        - The HTTP code returned by the Checkmk API.
    type: int
    returned: always
"""

import json
from datetime import datetime, timedelta

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.checkmk.general.plugins.module_utils.api import CheckmkAPI
from ansible_collections.checkmk.general.plugins.module_utils.logger import Logger
from ansible_collections.checkmk.general.plugins.module_utils.utils import (
    base_argument_spec,
    exit_module,
)

try:
    from urllib import urlencode
except ImportError:  # For Python 3
    from urllib.parse import urlencode

logger = Logger()

DEFAULT_COMMENT = "Managed by Ansible"
TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

# Editions that run the Nagios core (Checkmk Raw, renamed "Community" in 2.5).
# Their core accepts the MODIFY_*_DOWNTIME commands but silently ignores them,
# so in-place downtime modification is not possible and is emulated by
# delete + re-create. Every other edition runs the CMC, which modifies in place.
# The edition is taken from the version string suffix ("cre"/"raw" up to 2.4,
# "community" from 2.5 on).
RAW_EDITIONS = frozenset({"cre", "raw", "community"})


# ---------------------------------------------------------------------------
# Query column translation
# ---------------------------------------------------------------------------
# Queries are always written in terms of the Livestatus "downtimes" table (the
# same columns used to update or delete downtimes), e.g. C(host_name) and
# C(service_description). That is also what the update/delete lookups match on.
#
# For query-based *creation* the query is instead evaluated against the "hosts"
# or "services" table, which name the very same attributes differently: the hosts
# table calls it C(name) (not C(host_name)), and the services table calls it
# C(description) (not C(service_description)). The downtimes table only exposes
# them as joined columns under a "host_"/"service_" prefix.
#
# So for creation we translate the query columns from the downtimes table back to
# the queried object's table. The rule, verified against the 2.5.0 Livestatus
# schema (identical in 2.3.0/2.4.0), is:
#   * host query:    strip a leading "host_"   (host_name -> name, host_state -> state)
#   * service query: strip a leading "service_" (service_description -> description),
#                    but keep "host_" columns as-is (the services table joins them in).
def _object_query_column(column, kind):
    """Translate a downtimes-table query column to the hosts/services table."""
    if kind == "host":
        return column[len("host_") :] if column.startswith("host_") else column
    if column.startswith("service_"):
        return column[len("service_") :]
    return column  # host_* join columns (and bare service columns) stay as-is


def _object_query(query, kind):
    """Rewrite every column reference in a Livestatus query JSON string.

    Translates from the downtimes table to the queried object's table (C(kind) is
    C(host) or C(service)). The tree may nest logical operators (C(and)/C(or)/
    C(not)) whose operands live under C(expr); leaf conditions carry the column
    under C(left). Returns the original string if it cannot be parsed.
    """
    try:
        tree = json.loads(query)
    except (TypeError, ValueError):
        return query

    def walk(node):
        if isinstance(node, dict):
            if isinstance(node.get("left"), str):
                node["left"] = _object_query_column(node["left"], kind)
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(tree)
    return json.dumps(tree)


class DowntimeHTTPCodes:
    """HTTP status codes and their meaning, as (changed, failed, message)."""

    get = {
        200: (False, False, "Downtime(s) found"),
        204: (False, False, "No downtimes found"),
        404: (False, False, "Downtime not found"),
    }
    create = {
        200: (True, False, "Downtime created"),
        204: (True, False, "Downtime created"),
    }
    modify = {
        200: (True, False, "Downtime modified"),
        204: (True, False, "Downtime modified"),
    }
    delete = {
        200: (True, False, "Downtime deleted"),
        204: (True, False, "Downtime deleted"),
    }


class DowntimeAPI(CheckmkAPI):
    """Manages downtime operations via the Checkmk REST API.

    The strategy is uniform for all identification methods: fetch the downtimes
    that currently match, then act on each of them by its ID. Creating is the
    only exception, as it is not tied to an existing object.
    """

    def __init__(self, module):
        super().__init__(module)

        self.desired_state = self.params.get("state")

        # The Checkmk version is fetched so the module can adapt to version
        # specific behaviour. The create/update/delete endpoints used here behave
        # identically from 2.3.0 up to 2.5.0, so no branching is needed yet. This
        # is the natural place to add adjustments for 3.0.0 and later.
        self.version = self.getversion()

        # The Nagios core (Raw/Community edition) does not honour the
        # MODIFY_*_DOWNTIME commands, so modifications are emulated there by
        # deleting and re-creating the downtime. See modify().
        edition = getattr(self.version, "edition", None)
        self.on_nagios_core = str(edition or "").lower() in RAW_EDITIONS

        # Identification.
        self.downtime_id = self.params.get("downtime_id")
        self.dt_site_id = self.params.get("site_id")
        self.host_name = self.params.get("host_name")
        self.service_descriptions = self.params.get("service_descriptions") or []
        self.query = self.params.get("query")
        self.downtime_type = self.params.get("downtime_type")
        self.is_service = bool(self.service_descriptions)

        # Attributes.
        self.comment = self.params.get("comment")
        self.duration = self.params.get("duration")
        self.recur = self.params.get("recur")
        self.force = self.params.get("force")

        error = self._verify_parameters()
        if error:
            exit_module(self.module, msg=error, failed=True, logger=logger)

        self.current = self._get_current()

    def _verify_parameters(self):
        """Ensure a valid, unambiguous identification was given."""
        given = [
            name
            for name, value in (
                ("downtime_id", self.downtime_id),
                ("host_name", self.host_name),
                ("query", self.query),
            )
            if value
        ]
        if not given:
            return "One of 'downtime_id', 'host_name' or 'query' is required."
        # 'mutually_exclusive' in the argument spec already guards multiples.
        if self.downtime_id and not self.dt_site_id:
            return "The parameter 'site_id' is required when using 'downtime_id'."
        return None

    # -- Time helpers --------------------------------------------------------

    def _start_time(self):
        """Return the start time (ISO 8601) for a new downtime."""
        start_time = self.params.get("start_time")
        start_after = {k: int(v) for k, v in self.params.get("start_after").items()}
        if start_time:
            return start_time
        if start_after:
            return (datetime.utcnow() + timedelta(**start_after)).strftime(TIME_FORMAT)
        return datetime.utcnow().strftime(TIME_FORMAT)

    def _desired_end_time(self, default=None):
        """Return the desired end time (ISO 8601) or C(default) if none given."""
        end_time = self.params.get("end_time")
        end_after = {k: int(v) for k, v in self.params.get("end_after").items()}
        if end_time:
            return end_time
        if end_after:
            base = datetime.strptime(self._start_time(), TIME_FORMAT)
            return (base + timedelta(**end_after)).strftime(TIME_FORMAT)
        return default

    @staticmethod
    def _to_epoch(iso_time):
        """Normalize an ISO 8601 timestamp to epoch seconds for comparison."""
        if iso_time is None:
            return None
        try:
            return int(
                datetime.fromisoformat(iso_time.replace("Z", "+00:00")).timestamp()
            )
        except ValueError:
            return None

    # -- Fetching ------------------------------------------------------------

    def _get_current(self):
        """Fetch the downtimes matching the identification as a flat list."""
        if self.downtime_id:
            endpoint = "/objects/downtime/%s?%s" % (
                self.downtime_id,
                urlencode({"site_id": self.dt_site_id}),
            )
            result = self._fetch(
                code_mapping=DowntimeHTTPCodes.get,
                endpoint=endpoint,
                method="GET",
                logger=logger,
                fail_on_error=False,
            )
            if result.http_code != 200:
                return []
            return [self._flatten(json.loads(result.content))]

        params = {}
        if self.query:
            # Queries are written against the downtimes table, so they can be used
            # verbatim to look up existing downtimes. downtime_type narrows the
            # result to host or service downtimes when given.
            params["query"] = self.query
            if self.downtime_type:
                params["downtime_type"] = self.downtime_type
        else:
            params["host_name"] = self.host_name
            params["downtime_type"] = "service" if self.is_service else "host"

        endpoint = "/domain-types/downtime/collections/all?%s" % urlencode(params)
        result = self._fetch(
            code_mapping=DowntimeHTTPCodes.get,
            endpoint=endpoint,
            method="GET",
            logger=logger,
        )
        downtimes = [
            self._flatten(dt) for dt in json.loads(result.content).get("value", [])
        ]

        # The collection endpoint cannot filter a list of services for us.
        if self.is_service:
            downtimes = [
                dt
                for dt in downtimes
                if dt["service_description"] in self.service_descriptions
            ]
        return downtimes

    @staticmethod
    def _flatten(raw):
        """Turn a REST downtime object into a flat dict."""
        ext = raw.get("extensions", {})
        # is_service is a bool from 2.4.0 on, but a "yes"/"no" string in 2.3.0.
        raw_is_service = ext.get("is_service", False)
        if isinstance(raw_is_service, bool):
            is_service = raw_is_service
        else:
            is_service = str(raw_is_service).strip().lower() in ("yes", "true", "1")
        return {
            "id": raw.get("id"),
            "site_id": ext.get("site_id"),
            "host_name": ext.get("host_name"),
            "service_description": ext.get("service_description"),
            "is_service": is_service,
            "start_time": ext.get("start_time"),
            "end_time": ext.get("end_time"),
            "comment": ext.get("comment"),
        }

    def needs_update(self, downtime, desired_end, desired_comment):
        """Return True if a downtime differs from the desired end time/comment."""
        if desired_end is not None and self._to_epoch(
            downtime["end_time"]
        ) != self._to_epoch(desired_end):
            return True
        if desired_comment is not None and downtime["comment"] != desired_comment:
            return True
        return False

    # -- API actions ---------------------------------------------------------

    def _run(self, action, method, endpoint, data=None):
        """Perform a single change (skipped in check mode)."""
        if self.module.check_mode:
            return None
        return self._fetch(
            code_mapping=getattr(DowntimeHTTPCodes, action),
            endpoint=endpoint,
            data=data,
            method=method,
            logger=logger,
        )

    def create(self, service_descriptions=None):
        """Create a host downtime, or service downtimes for the given services."""
        end_time = self._desired_end_time(
            default=(datetime.utcnow() + timedelta(minutes=30)).strftime(TIME_FORMAT)
        )
        data = {
            "start_time": self._start_time(),
            "end_time": end_time,
            "recur": self.recur,
            "duration": self.duration,
            "comment": self.comment or DEFAULT_COMMENT,
            "host_name": self.host_name,
        }
        if service_descriptions:
            data["downtime_type"] = "service"
            data["service_descriptions"] = service_descriptions
            endpoint = "/domain-types/downtime/collections/service"
        else:
            data["downtime_type"] = "host"
            endpoint = "/domain-types/downtime/collections/host"
        return self._run("create", "POST", endpoint, data=data)

    def create_by_query(self):
        """Create host or service downtimes for all objects matching the query."""
        end_time = self._desired_end_time(
            default=(datetime.utcnow() + timedelta(minutes=30)).strftime(TIME_FORMAT)
        )
        data = {
            "start_time": self._start_time(),
            "end_time": end_time,
            "recur": self.recur,
            "duration": self.duration,
            "comment": self.comment or DEFAULT_COMMENT,
            "query": _object_query(self.query, self.downtime_type or "host"),
        }
        if self.downtime_type == "service":
            data["downtime_type"] = "service_by_query"
            endpoint = "/domain-types/downtime/collections/service"
        else:
            data["downtime_type"] = "host_by_query"
            endpoint = "/domain-types/downtime/collections/host"
        return self._run("create", "POST", endpoint, data=data)

    def modify(self, downtimes, desired_end, desired_comment):
        """Modify the end time and/or comment of the given downtimes.

        On the CMC this issues MODIFY_*_DOWNTIME, changing each downtime in
        place (its ID is preserved). The Nagios core used by the Raw/Community
        edition accepts those commands but silently ignores them, so there the
        change is applied by deleting and re-creating each downtime. That
        assigns a new downtime ID but leaves the resulting state identical.
        """
        if self.on_nagios_core:
            result = None
            for downtime in downtimes:
                result = self._recreate(downtime, desired_end, desired_comment)
            return result

        endpoint = "/domain-types/downtime/actions/modify/invoke"
        result = None
        for downtime in downtimes:
            data = {
                "modify_type": "by_id",
                "downtime_id": str(downtime["id"]),
                "site_id": downtime["site_id"],
            }
            if desired_end is not None:
                data["end_time"] = {"modify_type": "absolute", "value": desired_end}
            if desired_comment is not None:
                data["comment"] = desired_comment
            result = self._run("modify", "PUT", endpoint, data=data)
        return result

    def _recreate(self, downtime, desired_end, desired_comment):
        """Delete a downtime and re-create it with the new end time/comment.

        Used on the Nagios core, which cannot modify a downtime in place. The
        original start time and any unchanged attributes are preserved; the
        recurrence/duration come from the module parameters, matching create().
        """
        self.delete([downtime])
        data = {
            "start_time": downtime["start_time"],
            "end_time": (
                desired_end if desired_end is not None else downtime["end_time"]
            ),
            "recur": self.recur,
            "duration": self.duration,
            "comment": (
                desired_comment if desired_comment is not None else downtime["comment"]
            ),
            "host_name": downtime["host_name"],
        }
        if downtime["is_service"]:
            data["downtime_type"] = "service"
            data["service_descriptions"] = [downtime["service_description"]]
            endpoint = "/domain-types/downtime/collections/service"
        else:
            data["downtime_type"] = "host"
            endpoint = "/domain-types/downtime/collections/host"
        return self._run("create", "POST", endpoint, data=data)

    def delete(self, downtimes):
        """Delete the given downtimes, by ID."""
        endpoint = "/domain-types/downtime/actions/delete/invoke"
        result = None
        for downtime in downtimes:
            data = {
                "delete_type": "by_id",
                "downtime_id": str(downtime["id"]),
                "site_id": downtime["site_id"],
            }
            result = self._run("delete", "POST", endpoint, data=data)
        return result


def _diff_text(before, after):
    """A compact, human readable diff embedded into the check-mode message."""

    def summarize(downtimes):
        return [
            {
                "id": dt["id"],
                "host_name": dt["host_name"],
                "service_description": dt["service_description"],
                "end_time": dt["end_time"],
                "comment": dt["comment"],
            }
            for dt in downtimes
        ]

    return " diff=%s" % json.dumps(
        {"before": summarize(before), "after": after}, sort_keys=True
    )


def _update_matching(module, api, matching):
    """Update the end time and/or comment of already-matched downtimes."""
    desired_end = api._desired_end_time()
    desired_comment = api.comment  # None => leave the comment unchanged
    if desired_end is None and desired_comment is None:
        exit_module(
            module,
            msg="Downtime(s) already present, nothing to update"
            " (set 'end_time'/'end_after' and/or 'comment' to change them).",
            logger=logger,
        )
    to_change = [
        dt for dt in matching if api.needs_update(dt, desired_end, desired_comment)
    ]
    if not to_change:
        exit_module(
            module, msg="Downtime(s) already in the desired state.", logger=logger
        )
    if module.check_mode:
        exit_module(
            module,
            msg="Downtime(s) would be modified."
            + _diff_text(
                to_change, {"end_time": desired_end, "comment": desired_comment}
            ),
            changed=True,
            logger=logger,
        )
    result = api.modify(to_change, desired_end, desired_comment)
    exit_module(module, result=result, logger=logger)


def _present(module, api):
    """Handle state=present: create and/or update as needed."""

    # --- Update-only path: identification by downtime_id ------------------
    # A downtime cannot be created from an ID, so a missing match is an error.
    if api.downtime_id:
        if not api.current:
            exit_module(
                module,
                msg="No downtime found to update for the given ID.",
                failed=True,
                logger=logger,
            )
        _update_matching(module, api, api.current)

    # --- Query path: update matching downtimes, or create if none exist ---
    if api.query:
        if api.current:
            _update_matching(module, api, api.current)
        # Nothing matches yet: schedule downtimes for the selected objects.
        if module.check_mode:
            exit_module(
                module,
                msg="Downtime(s) would be created for all objects matching the query.",
                changed=True,
                logger=logger,
            )
        result = api.create_by_query()
        exit_module(module, result=result, logger=logger)

    # --- Create/update path: identification by host_name ------------------
    # For host based identification the comment is part of the downtime's
    # identity, so we only look at downtimes carrying the effective comment.
    effective_comment = api.comment or DEFAULT_COMMENT
    existing = [dt for dt in api.current if dt["comment"] == effective_comment]
    desired_end = api._desired_end_time()

    if api.is_service:
        have = {dt["service_description"] for dt in existing}
        create_services = [
            s for s in api.service_descriptions if api.force or s not in have
        ]
        create_needed = bool(create_services)
        update_targets = (
            []
            if api.force
            else [
                dt
                for dt in existing
                if dt["service_description"] in api.service_descriptions
                and api.needs_update(dt, desired_end, None)
            ]
        )
    else:
        create_services = None
        create_needed = api.force or not existing
        update_targets = (
            []
            if create_needed
            else [dt for dt in existing if api.needs_update(dt, desired_end, None)]
        )

    if not create_needed and not update_targets:
        exit_module(
            module, msg="Downtime(s) already in the desired state.", logger=logger
        )

    if module.check_mode:
        exit_module(
            module,
            msg="Downtime(s) would be created/modified."
            + _diff_text(update_targets, {"end_time": desired_end}),
            changed=True,
            logger=logger,
        )

    results = []
    if create_needed:
        results.append(api.create(service_descriptions=create_services))
    if update_targets:
        results.append(api.modify(update_targets, desired_end, None))

    result = next((r for r in reversed(results) if r is not None), None)
    if result is not None:
        exit_module(module, result=result, logger=logger)
    exit_module(
        module, msg="Downtime(s) created/modified.", changed=True, logger=logger
    )


def _absent(module, api):
    """Handle state=absent: delete matching downtimes."""
    # For host based identification, a comment (if given) narrows the deletion.
    if api.host_name and api.comment:
        matching = [dt for dt in api.current if dt["comment"] == api.comment]
    else:
        matching = api.current

    if not matching:
        exit_module(
            module, msg="No matching downtimes, nothing to delete.", logger=logger
        )

    if module.check_mode:
        exit_module(
            module,
            msg="Downtime(s) would be deleted." + _diff_text(matching, []),
            changed=True,
            logger=logger,
        )
    result = api.delete(matching)
    exit_module(module, result=result, logger=logger)


def run_module():
    argument_spec = base_argument_spec()
    argument_spec.update(
        downtime_id=dict(type="str"),
        site_id=dict(type="str"),
        host_name=dict(type="str"),
        service_descriptions=dict(type="list", elements="str", default=[]),
        query=dict(type="str"),
        downtime_type=dict(type="str", choices=["host", "service"]),
        comment=dict(type="str"),
        start_time=dict(type="str"),
        start_after=dict(type="dict", default={}),
        end_time=dict(type="str"),
        end_after=dict(type="dict", default={}),
        duration=dict(type="int", default=0),
        recur=dict(
            type="str",
            default="fixed",
            choices=[
                "fixed",
                "hour",
                "day",
                "week",
                "second_week",
                "fourth_week",
                "weekday_start",
                "weekday_end",
                "day_of_month",
            ],
        ),
        force=dict(type="bool", default=False),
        state=dict(type="str", default="present", choices=["present", "absent"]),
    )

    required_if = [
        ("api_auth_type", "bearer", ["api_user", "api_secret"]),
        ("api_auth_type", "basic", ["api_user", "api_secret"]),
        ("api_auth_type", "cookie", ["api_auth_cookie"]),
    ]

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        mutually_exclusive=[("downtime_id", "host_name", "query")],
        required_by={"downtime_id": ("site_id",)},
        required_if=required_if,
    )

    logger.set_loglevel(module._verbosity)

    api = DowntimeAPI(module)

    try:
        if module.params["state"] == "present":
            _present(module, api)
        else:
            _absent(module, api)
    except Exception as e:
        exit_module(module, msg="Error managing the downtime: %s" % e, logger=logger)


def main():
    run_module()


if __name__ == "__main__":
    main()

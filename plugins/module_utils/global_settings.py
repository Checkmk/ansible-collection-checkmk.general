#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2026, Lars Getwan <lars.getwan@checkmk.com>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Shared helpers for the global settings module and lookup plugin.

The Checkmk global settings endpoints exchange a value in the representation
the GUI's Vue form components use, together with the rendered form spec
(``spec``) that describes it. That representation is not meant for humans:
single choices are addressed by a SHA-256 hash of their internal value,
multiple choices by ``{"name": ..., "title": ...}`` objects, data sizes as
``["10", "MiB"]``, passwords as encrypted tuples, and so on.

This module walks the spec to translate between that representation and the
values a user sees in the GUI (choice titles, dictionary element titles,
"1h 30min", "10 MiB", ...), in both directions, and provides a canonical form
of a frontend value that makes two values comparable for idempotency.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import re

try:
    from urllib.parse import quote
except ImportError:  # Python 2
    from urllib import quote

HIDDEN_SECRET = "(hidden)"

API_VERSION_PATH = "internal"

# Frontend types whose values are already plain data that a user can read and
# write as-is. They are passed through unchanged.
_PASSTHROUGH_TYPES = frozenset(
    {
        "string",
        "multiline_text",
        "comment_text_area",
        "regex",
        "metric",
        "labels",
        "list_of_strings",
        "ca_certificate",
        "date_picker",
        "time_picker",
        "static_text",
        "file_upload",
        "condition_choices",
        "binary_condition_choices",
        "time_specific",
        "oauth2_connection_setup",
        "telemetry_metrics_custom_query",
        "dcd_telemetry_metrics_filter",
    }
)

_TIME_UNITS = (
    ("d", 86400.0),
    ("h", 3600.0),
    ("min", 60.0),
    ("s", 1.0),
    ("ms", 0.001),
)
_TIME_UNIT_ALIASES = {
    "d": 86400.0,
    "day": 86400.0,
    "days": 86400.0,
    "h": 3600.0,
    "hour": 3600.0,
    "hours": 3600.0,
    "m": 60.0,
    "min": 60.0,
    "mins": 60.0,
    "minute": 60.0,
    "minutes": 60.0,
    "s": 1.0,
    "sec": 1.0,
    "secs": 1.0,
    "second": 1.0,
    "seconds": 1.0,
    "ms": 0.001,
    "millisecond": 0.001,
    "milliseconds": 0.001,
}
_TIME_SPAN_RE = re.compile(r"(-?\d+(?:\.\d+)?)\s*([a-zA-Z]+)")

_DATA_SIZE_UNITS = {
    "B": 1,
    "KB": 1000,
    "MB": 1000**2,
    "GB": 1000**3,
    "TB": 1000**4,
    "PB": 1000**5,
    "EB": 1000**6,
    "ZB": 1000**7,
    "YB": 1000**8,
    "KiB": 1024,
    "MiB": 1024**2,
    "GiB": 1024**3,
    "TiB": 1024**4,
    "PiB": 1024**5,
    "EiB": 1024**6,
    "ZiB": 1024**7,
    "YiB": 1024**8,
}
_DATA_SIZE_RE = re.compile(r"^\s*(-?\d+(?:\.\d+)?)\s*([a-zA-Z]*)\s*$")


class GlobalSettingValueError(ValueError):
    """Raised when a user supplied value does not fit the setting's spec."""


def setting_endpoint(varname, site_id=None):
    """Return the REST API endpoint of a (site specific) global setting."""
    varname = quote(varname, safe="")
    if site_id:
        return "objects/site_connection/%s/global_setting/%s" % (
            quote(site_id, safe=""),
            varname,
        )
    return "objects/global_setting/%s" % varname


def internal_api_url(url):
    """Rewrite a C(.../check_mk/api/1.0) base URL to the internal API version.

    The global settings endpoints are only registered for the internal API
    version, which inherits all endpoints of the lower versions.
    """
    url = url.rstrip("/")
    for suffix in ("/api/1.0", "/api/v1"):
        if url.endswith(suffix):
            return url[: -len(suffix)] + "/api/" + API_VERSION_PATH
    return url


# ---------------------------------------------------------------------------
# Generic spec helpers
# ---------------------------------------------------------------------------


def _path_str(path):
    return "/".join(str(p) for p in path) or "<value>"


def _title(spec):
    return (spec or {}).get("title") or ""


def _norm(text):
    return re.sub(r"\s+", " ", str(text)).strip().casefold()


def _match_choice(elements, wanted, path, get_name, get_title):
    """Find a choice element by its title (preferred) or internal name.

    Matching order: exact title, exact name, case/whitespace-insensitive title.
    """
    for element in elements:
        if get_title(element) == wanted:
            return element
    for element in elements:
        if get_name(element) == wanted:
            return element
    wanted_norm = _norm(wanted)
    candidates = [e for e in elements if _norm(get_title(e)) == wanted_norm]
    if len(candidates) == 1:
        return candidates[0]
    raise GlobalSettingValueError(
        "%s: %r is not a valid choice. Valid choices are: %s"
        % (
            _path_str(path),
            wanted,
            ", ".join(repr(get_title(e) or get_name(e)) for e in elements) or "none",
        )
    )


def _element_keys(elements, get_name, get_spec):
    """Map each element name to the key shown to the user.

    The element's title is used, as that is what the GUI shows. The internal
    name is used instead when the title is empty or not unique.
    """
    titles = [_title(get_spec(e)) for e in elements]
    keys = {}
    for element, title in zip(elements, titles):
        if title and titles.count(title) == 1:
            keys[get_name(element)] = title
        else:
            keys[get_name(element)] = get_name(element)
    return keys


def _resolve_key(elements, key, path, get_name, get_spec):
    """Find an element by user key (title or internal name)."""
    return _match_choice(
        elements,
        key,
        path,
        get_name=get_name,
        get_title=lambda e: _title(get_spec(e)),
    )


# ---------------------------------------------------------------------------
# Scalar conversions
# ---------------------------------------------------------------------------


def _fmt_number(number):
    if float(number).is_integer():
        return str(int(number))
    return ("%.3f" % number).rstrip("0").rstrip(".")


def render_time_span(seconds):
    """Render seconds like the GUI does, e.g. C(1d 2h 30min)."""
    if seconds is None:
        return None
    seconds = float(seconds)
    if seconds == 0:
        return "0s"
    sign = "-" if seconds < 0 else ""
    rest = abs(seconds)
    parts = []
    for unit, factor in _TIME_UNITS:
        if unit == "ms":
            amount = round(rest / factor, 3)
        else:
            amount = int((rest + 1e-9) // factor)
        if amount:
            parts.append("%s%s" % (_fmt_number(amount), unit))
            rest -= amount * factor
    return sign + " ".join(parts)


def parse_time_span(value, path=()):
    """Parse seconds (a number) or a string like C(1h 30min) into seconds."""
    if isinstance(value, bool):
        raise GlobalSettingValueError("%s: expected a time span" % _path_str(path))
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip()
    try:
        return float(text)
    except ValueError:
        pass
    matches = list(_TIME_SPAN_RE.finditer(text))
    if not matches or _TIME_SPAN_RE.sub("", text).strip():
        raise GlobalSettingValueError(
            "%s: %r is not a valid time span. Use seconds or e.g. '1d 2h 30min 10s'."
            % (_path_str(path), value)
        )
    total = 0.0
    for match in matches:
        unit = match.group(2).lower()
        if unit not in _TIME_UNIT_ALIASES:
            raise GlobalSettingValueError(
                "%s: unknown time unit %r in %r" % (_path_str(path), unit, value)
            )
        total += float(match.group(1)) * _TIME_UNIT_ALIASES[unit]
    return total


def _data_size_bytes(number, unit, path):
    if unit not in _DATA_SIZE_UNITS:
        raise GlobalSettingValueError(
            "%s: unknown data size unit %r. Valid units are: %s"
            % (_path_str(path), unit, ", ".join(sorted(_DATA_SIZE_UNITS)))
        )
    return int(round(float(number) * _DATA_SIZE_UNITS[unit]))


def _data_size_to_frontend(spec, value, path):
    magnitudes = [m for m in spec.get("displayed_magnitudes") or [] if m] or ["B"]
    if isinstance(value, bool):
        raise GlobalSettingValueError("%s: expected a data size" % _path_str(path))
    if isinstance(value, (list, tuple)) and len(value) == 2:
        number, unit = value
    elif isinstance(value, (int, float)):
        number, unit = value, "B"
    else:
        match = _DATA_SIZE_RE.match(str(value))
        if not match:
            raise GlobalSettingValueError(
                "%s: %r is not a valid data size, use e.g. '10 MiB'."
                % (_path_str(path), value)
            )
        number, unit = match.group(1), match.group(2) or "B"
    # Match the unit case-insensitively ("mib" -> "MiB").
    unit_lookup = {u.lower(): u for u in _DATA_SIZE_UNITS}
    unit = unit_lookup.get(str(unit).lower(), unit)
    size = _data_size_bytes(number, unit, path)

    if unit in magnitudes:
        return [_fmt_number(float(number)), unit]
    # Express the size in the largest displayed unit it divides evenly into.
    for magnitude in sorted(
        magnitudes, key=lambda m: _DATA_SIZE_UNITS.get(m, 1), reverse=True
    ):
        factor = _DATA_SIZE_UNITS.get(magnitude)
        if factor and size % factor == 0:
            return [str(size // factor), magnitude]
    smallest = min(magnitudes, key=lambda m: _DATA_SIZE_UNITS.get(m, 1))
    return [_fmt_number(size / float(_DATA_SIZE_UNITS[smallest])), smallest]


def _to_bool(value, path):
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    if text in ("true", "yes", "on", "1", "y"):
        return True
    if text in ("false", "no", "off", "0", "n"):
        return False
    raise GlobalSettingValueError("%s: %r is not a boolean" % (_path_str(path), value))


def _to_number(value, kind, path):
    if isinstance(value, bool):
        raise GlobalSettingValueError("%s: expected a number" % _path_str(path))
    try:
        if kind == "integer":
            if isinstance(value, float) and not value.is_integer():
                raise ValueError
            return int(float(value)) if isinstance(value, str) else int(value)
        return float(value)
    except (TypeError, ValueError):
        raise GlobalSettingValueError(
            "%s: %r is not a valid %s" % (_path_str(path), value, kind)
        )


# ---------------------------------------------------------------------------
# Frontend value -> UI value
# ---------------------------------------------------------------------------


def to_ui(spec, value, path=()):
    """Translate a frontend value into the representation shown in the GUI."""
    kind = (spec or {}).get("type")

    if kind in _PASSTHROUGH_TYPES or kind is None:
        return value

    if kind in ("integer", "float", "boolean_choice"):
        return value

    if kind == "legacy_valuespec":
        # Only the rendered HTML is available, the value itself is not.
        return None

    if kind == "fixed_value":
        return spec.get("label") or spec.get("value")

    if kind in ("single_choice", "single_choice_editable"):
        if value is None:
            return None
        for element in spec.get("elements") or []:
            if element.get("name") == value:
                return element.get("title") or value
        return value

    if kind == "cascading_single_choice":
        if not isinstance(value, (list, tuple)) or len(value) != 2:
            return value
        name, sub_value = value
        for element in spec.get("elements") or []:
            if element.get("name") == name:
                title = element.get("title") or name
                sub_spec = element.get("parameter_form") or {}
                if sub_spec.get("type") == "fixed_value":
                    return title
                return {title: to_ui(sub_spec, sub_value, path + (title,))}
        return value

    if kind in ("dictionary", "two_column_dictionary"):
        if not isinstance(value, dict):
            return value
        elements = spec.get("elements") or []
        keys = _element_keys(
            elements, lambda e: e["name"], lambda e: e.get("parameter_form")
        )
        result = {}
        for element in elements:
            name = element["name"]
            if name in value:
                key = keys[name]
                result[key] = to_ui(
                    element.get("parameter_form"), value[name], path + (key,)
                )
        return result

    if kind == "catalog":
        if not isinstance(value, dict):
            return value
        result = {}
        for topic in spec.get("elements") or []:
            topic_name = topic.get("name")
            topic_key = topic.get("title") or topic_name
            topic_value = value.get(topic_name) or {}
            elements = _topic_elements(topic)
            keys = _element_keys(
                elements, lambda e: e["name"], lambda e: e.get("parameter_form")
            )
            result[topic_key] = {
                keys[e["name"]]: to_ui(
                    e.get("parameter_form"),
                    topic_value[e["name"]],
                    path + (topic_key, keys[e["name"]]),
                )
                for e in elements
                if e["name"] in topic_value
            }
        return result

    if kind in ("list", "list_unique_selection"):
        if not isinstance(value, list):
            return value
        template = spec.get("element_template")
        return [to_ui(template, v, path + (i,)) for i, v in enumerate(value)]

    if kind == "tuple":
        if not isinstance(value, (list, tuple)):
            return value
        return [
            to_ui(s, v, path + (i,))
            for i, (s, v) in enumerate(zip(spec.get("elements") or [], value))
        ]

    if kind == "optional_choice":
        if value is None:
            return None
        return to_ui(spec.get("parameter_form"), value, path)

    if kind in ("checkbox_list_choice", "dual_list_choice"):
        if not isinstance(value, list):
            return value
        return [
            (v.get("title") or v.get("name")) if isinstance(v, dict) else v
            for v in value
        ]

    if kind == "time_span":
        return render_time_span(value)

    if kind == "data_size":
        if isinstance(value, (list, tuple)) and len(value) == 2 and value[0] != "":
            return "%s %s" % (value[0], value[1])
        return None

    if kind == "simple_password":
        if isinstance(value, (list, tuple)) and value and value[0]:
            return HIDDEN_SECRET
        return None

    if kind == "password":
        if not isinstance(value, (list, tuple)) or len(value) != 4:
            return value
        password_type, password_id = value[0], value[1]
        if password_type == "stored_password":
            for choice in spec.get("password_store_choices") or []:
                if choice.get("password_id") == password_id:
                    return {"password_store": choice.get("name") or password_id}
            return {"password_store": password_id}
        return HIDDEN_SECRET if value[2] else None

    return value


def _topic_elements(topic):
    """Flatten a catalog topic's elements (which may be grouped)."""
    flat = []
    for element in topic.get("elements") or []:
        if element.get("type") == "topic_group":
            flat.extend(element.get("elements") or [])
        else:
            flat.append(element)
    return flat


# ---------------------------------------------------------------------------
# UI value -> frontend value
# ---------------------------------------------------------------------------


def _current_by_name(current, name):
    if isinstance(current, dict):
        return current.get(name)
    return None


def from_ui(spec, value, current=None, update_secrets=False, path=()):
    """Translate a GUI style value into the frontend representation.

    C(current) is the current frontend value at the same position (or None).
    It is used to keep secrets unchanged unless C(update_secrets) is set, and
    to keep the identity of explicit passwords.
    """
    kind = (spec or {}).get("type")

    if kind == "legacy_valuespec":
        raise GlobalSettingValueError(
            "%s: this part of the setting is still implemented as a legacy "
            "ValueSpec in Checkmk and cannot be configured through the REST API."
            % _path_str(path)
        )

    if kind in _PASSTHROUGH_TYPES or kind is None:
        return value

    if kind == "boolean_choice":
        return _to_bool(value, path)

    if kind in ("integer", "float"):
        return _to_number(value, kind, path)

    if kind == "fixed_value":
        return spec.get("value")

    if kind in ("single_choice", "single_choice_editable"):
        if value is None:
            return None
        element = _match_choice(
            spec.get("elements") or [],
            value,
            path,
            get_name=lambda e: e.get("name"),
            get_title=lambda e: e.get("title") or "",
        )
        return element.get("name")

    if kind == "cascading_single_choice":
        return _cascading_from_ui(spec, value, current, update_secrets, path)

    if kind in ("dictionary", "two_column_dictionary"):
        if not isinstance(value, dict):
            raise GlobalSettingValueError("%s: expected a dictionary" % _path_str(path))
        return _elements_from_ui(
            spec.get("elements") or [], value, current, update_secrets, path
        )

    if kind == "catalog":
        if not isinstance(value, dict):
            raise GlobalSettingValueError(
                "%s: expected a dictionary of topics" % _path_str(path)
            )
        topics = spec.get("elements") or []
        given = {}
        for key, topic_value in value.items():
            topic = _match_choice(
                topics,
                key,
                path,
                get_name=lambda t: t.get("name"),
                get_title=lambda t: t.get("title") or "",
            )
            given[topic["name"]] = (topic.get("title") or topic["name"], topic_value)
        result = {}
        for topic in topics:
            name = topic["name"]
            topic_key, topic_value = given.get(name, (name, {}))
            if not isinstance(topic_value, dict):
                raise GlobalSettingValueError(
                    "%s: expected a dictionary" % _path_str(path + (topic_key,))
                )
            result[name] = _elements_from_ui(
                _topic_elements(topic),
                topic_value,
                _current_by_name(current, name),
                update_secrets,
                path + (topic_key,),
            )
        return result

    if kind in ("list", "list_unique_selection"):
        if not isinstance(value, list):
            raise GlobalSettingValueError("%s: expected a list" % _path_str(path))
        template = spec.get("element_template")
        current_list = current if isinstance(current, list) else []
        return [
            from_ui(
                template,
                v,
                current_list[i] if i < len(current_list) else None,
                update_secrets,
                path + (i,),
            )
            for i, v in enumerate(value)
        ]

    if kind == "tuple":
        elements = spec.get("elements") or []
        if not isinstance(value, (list, tuple)) or len(value) != len(elements):
            raise GlobalSettingValueError(
                "%s: expected a list of %d elements" % (_path_str(path), len(elements))
            )
        current_list = current if isinstance(current, (list, tuple)) else []
        return [
            from_ui(
                s,
                v,
                current_list[i] if i < len(current_list) else None,
                update_secrets,
                path + (i,),
            )
            for i, (s, v) in enumerate(zip(elements, value))
        ]

    if kind == "optional_choice":
        if value is None:
            return None
        return from_ui(spec.get("parameter_form"), value, current, update_secrets, path)

    if kind in ("checkbox_list_choice", "dual_list_choice"):
        if not isinstance(value, list):
            raise GlobalSettingValueError("%s: expected a list" % _path_str(path))
        elements = spec.get("elements") or []
        result = []
        for item in value:
            if not elements:
                # Autocompleted choices: the choices are not part of the spec.
                result.append({"name": item, "title": item})
                continue
            element = _match_choice(
                elements,
                item,
                path,
                get_name=lambda e: e.get("name"),
                get_title=lambda e: e.get("title") or "",
            )
            result.append({"name": element["name"], "title": element.get("title")})
        return result

    if kind == "time_span":
        if value is None:
            return None
        return parse_time_span(value, path)

    if kind == "data_size":
        return _data_size_to_frontend(spec, value, path)

    if kind == "simple_password":
        return _simple_password_from_ui(value, current, update_secrets, path)

    if kind == "password":
        return _password_from_ui(spec, value, current, update_secrets, path)

    return value


def _cascading_from_ui(spec, value, current, update_secrets, path):
    elements = spec.get("elements") or []
    if isinstance(value, dict):
        if len(value) != 1:
            raise GlobalSettingValueError(
                "%s: expected exactly one choice, e.g. {'<choice title>': <value>}"
                % _path_str(path)
            )
        choice, sub_value = list(value.items())[0]
        has_sub_value = True
    elif isinstance(value, (list, tuple)) and len(value) == 2:
        choice, sub_value = value
        has_sub_value = True
    else:
        choice, sub_value, has_sub_value = value, None, False

    element = _match_choice(
        elements,
        choice,
        path,
        get_name=lambda e: e.get("name"),
        get_title=lambda e: e.get("title") or "",
    )
    sub_spec = element.get("parameter_form") or {}
    sub_path = path + (element.get("title") or element["name"],)

    current_sub = None
    if (
        isinstance(current, (list, tuple))
        and len(current) == 2
        and current[0] == element["name"]
    ):
        current_sub = current[1]

    if not has_sub_value:
        if sub_spec.get("type") != "fixed_value":
            raise GlobalSettingValueError(
                "%s: this choice needs a value, use {'%s': <value>}"
                % (_path_str(path), element.get("title") or element["name"])
            )
        return [element["name"], sub_spec.get("value")]

    return [
        element["name"],
        from_ui(sub_spec, sub_value, current_sub, update_secrets, sub_path),
    ]


def _elements_from_ui(elements, value, current, update_secrets, path):
    """Translate dictionary (or catalog topic) elements.

    Elements not given by the user are left out (i.e. unchecked in the GUI),
    unless they are required, in which case the spec's default is used.
    """
    result = {}
    for key, element_value in value.items():
        element = _resolve_key(
            elements,
            key,
            path,
            get_name=lambda e: e["name"],
            get_spec=lambda e: e.get("parameter_form"),
        )
        result[element["name"]] = from_ui(
            element.get("parameter_form"),
            element_value,
            _current_by_name(current, element["name"]),
            update_secrets,
            path + (key,),
        )
    for element in elements:
        if element.get("required") and element["name"] not in result:
            current_value = _current_by_name(current, element["name"])
            result[element["name"]] = (
                current_value
                if current_value is not None
                else element.get("default_value")
            )
    return result


def _simple_password_from_ui(value, current, update_secrets, path):
    if value is None or value == "":
        raise GlobalSettingValueError("%s: a password is required" % _path_str(path))
    has_current = isinstance(current, (list, tuple)) and current and current[0]
    if value == HIDDEN_SECRET:
        if not has_current:
            raise GlobalSettingValueError(
                "%s: no password is set yet, provide the actual password"
                % _path_str(path)
            )
        return list(current)
    if has_current and not update_secrets:
        return list(current)
    return [str(value), False]


def _password_from_ui(spec, value, current, update_secrets, path):
    current_ok = isinstance(current, (list, tuple)) and len(current) == 4

    if isinstance(value, dict):
        if list(value.keys()) != ["password_store"]:
            raise GlobalSettingValueError(
                "%s: use either a password string or {'password_store': <name>}"
                % _path_str(path)
            )
        wanted = value["password_store"]
        choices = spec.get("password_store_choices") or []
        choice = _match_choice(
            choices,
            wanted,
            path,
            get_name=lambda c: c.get("password_id"),
            get_title=lambda c: c.get("name") or "",
        )
        return ["stored_password", choice["password_id"], "", False]

    if value is None or value == "":
        raise GlobalSettingValueError("%s: a password is required" % _path_str(path))

    current_is_explicit = (
        current_ok and current[0] == "explicit_password" and bool(current[2])
    )
    if value == HIDDEN_SECRET:
        if not current_is_explicit:
            raise GlobalSettingValueError(
                "%s: no explicit password is set yet, provide the actual password"
                % _path_str(path)
            )
        return list(current)
    if current_is_explicit and not update_secrets:
        return list(current)
    password_id = current[1] if current_is_explicit else ""
    return ["explicit_password", password_id, str(value), False]


# ---------------------------------------------------------------------------
# Canonical form for comparison
# ---------------------------------------------------------------------------


def canonical(spec, value):
    """Return a representation of a frontend value that is stable to compare.

    Equal settings produce equal canonical forms, regardless of e.g. the unit
    a data size is expressed in or the order of multiple choice selections.
    Secrets that are about to be (re)written in plain text never compare equal
    to stored, encrypted ones.
    """
    kind = (spec or {}).get("type")

    if kind in ("dictionary", "two_column_dictionary"):
        if not isinstance(value, dict):
            return value
        specs = {e["name"]: e.get("parameter_form") for e in spec.get("elements") or []}
        return {k: canonical(specs.get(k), v) for k, v in value.items()}

    if kind == "catalog":
        if not isinstance(value, dict):
            return value
        result = {}
        for topic in spec.get("elements") or []:
            specs = {e["name"]: e.get("parameter_form") for e in _topic_elements(topic)}
            topic_value = value.get(topic["name"]) or {}
            result[topic["name"]] = {
                k: canonical(specs.get(k), v) for k, v in topic_value.items()
            }
        return result

    if kind == "cascading_single_choice":
        if not isinstance(value, (list, tuple)) or len(value) != 2:
            return value
        for element in spec.get("elements") or []:
            if element.get("name") == value[0]:
                return [value[0], canonical(element.get("parameter_form"), value[1])]
        return list(value)

    if kind in ("list", "list_unique_selection"):
        if not isinstance(value, list):
            return value
        return [canonical(spec.get("element_template"), v) for v in value]

    if kind == "tuple":
        if not isinstance(value, (list, tuple)):
            return value
        return [canonical(s, v) for s, v in zip(spec.get("elements") or [], value)]

    if kind == "optional_choice":
        if value is None:
            return None
        return canonical(spec.get("parameter_form"), value)

    if kind in ("checkbox_list_choice", "dual_list_choice"):
        if not isinstance(value, list):
            return value
        return sorted(v.get("name") if isinstance(v, dict) else v for v in value)

    if kind == "data_size":
        if isinstance(value, (list, tuple)) and len(value) == 2 and value[0] != "":
            try:
                return _data_size_bytes(value[0], value[1], ())
            except (GlobalSettingValueError, ValueError):
                return list(value)
        return None

    if kind == "time_span":
        return None if value is None else round(float(value), 3)

    if kind == "float":
        return None if value is None else float(value)

    if kind in ("simple_password", "password"):
        return list(value) if isinstance(value, (list, tuple)) else value

    if isinstance(value, tuple):
        return list(value)
    return value


def ui_from_setting(setting):
    """Build the user facing representation of a REST API setting object."""
    spec = setting.get("spec") or {}
    return {
        "varname": setting.get("varname"),
        "site_id": setting.get("site_id"),
        "origin": setting.get("origin"),
        "title": _title(spec),
        "value": to_ui(spec, setting.get("value")),
    }

#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2026, Lars Getwan <lars.getwan@checkmk.com>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from ansible_collections.checkmk.general.plugins.module_utils.global_settings import (
    HIDDEN_SECRET,
    GlobalSettingValueError,
    canonical,
    from_ui,
    internal_api_url,
    parse_time_span,
    render_time_span,
    setting_endpoint,
    to_ui,
)

# The specs below mimic what the Checkmk form spec visitors emit (to_vue()).
# Single choice names are SHA-256 hashes of the internal value in reality;
# shortened stand-ins are used here.
LEVEL_CHOICE = {
    "type": "single_choice",
    "title": "",
    "elements": [
        {"name": "h50", "title": "Critical"},
        {"name": "h40", "title": "Error"},
        {"name": "h30", "title": "Warning"},
        {"name": "h20", "title": "Informational"},
        {"name": "h10", "title": "Debug"},
    ],
}

LOG_LEVELS_SPEC = {
    "type": "dictionary",
    "title": "Logging",
    "elements": [
        {
            "name": "cmk.web",
            "required": True,
            "default_value": "h30",
            "parameter_form": dict(LEVEL_CHOICE, title="Web"),
        },
        {
            "name": "cmk.core",
            "required": True,
            "default_value": "h30",
            "parameter_form": dict(LEVEL_CHOICE, title="Core"),
        },
        {
            "name": "cmk.optional",
            "required": False,
            "default_value": "",
            "parameter_form": {"type": "string", "title": "Optional"},
        },
    ],
}

CASCADING_SPEC = {
    "type": "cascading_single_choice",
    "title": "Mode",
    "elements": [
        {
            "name": "disabled",
            "title": "Disabled",
            "default_value": None,
            "parameter_form": {"type": "fixed_value", "value": None, "label": None},
        },
        {
            "name": "enabled",
            "title": "Enabled",
            "default_value": {},
            "parameter_form": {
                "type": "dictionary",
                "title": "",
                "elements": [
                    {
                        "name": "timeout",
                        "required": True,
                        "default_value": 60.0,
                        "parameter_form": {
                            "type": "time_span",
                            "title": "Timeout",
                            "displayed_magnitudes": ["hour", "minute", "second"],
                        },
                    },
                    {
                        "name": "limit",
                        "required": False,
                        "default_value": ["", "MiB"],
                        "parameter_form": {
                            "type": "data_size",
                            "title": "Limit",
                            "displayed_magnitudes": ["KiB", "MiB", "GiB"],
                        },
                    },
                ],
            },
        },
    ],
}

MULTI_SPEC = {
    "type": "checkbox_list_choice",
    "title": "Features",
    "elements": [
        {"name": "a", "title": "Alpha"},
        {"name": "b", "title": "Beta"},
        {"name": "c", "title": "Gamma"},
    ],
}

PASSWORD_SPEC = {
    "type": "password",
    "title": "Secret",
    "password_store_choices": [{"password_id": "pw_1", "name": "My stored pw"}],
}


class TestEndpoints:
    def test_central_endpoint(self):
        assert setting_endpoint("log_levels") == "objects/global_setting/log_levels"

    def test_site_endpoint(self):
        assert (
            setting_endpoint("log_levels", "remote1")
            == "objects/site_connection/remote1/global_setting/log_levels"
        )

    def test_internal_url(self):
        assert (
            internal_api_url("https://srv/mysite/check_mk/api/1.0")
            == "https://srv/mysite/check_mk/api/internal"
        )


class TestTimeSpan:
    @pytest.mark.parametrize(
        "text, seconds",
        [
            ("90", 90.0),
            (90, 90.0),
            ("1h 30min", 5400.0),
            ("1d2h", 93600.0),
            ("2 minutes 5 s", 125.0),
            ("250ms", 0.25),
        ],
    )
    def test_parse(self, text, seconds):
        assert parse_time_span(text) == seconds

    def test_parse_invalid(self):
        with pytest.raises(GlobalSettingValueError):
            parse_time_span("soon")

    @pytest.mark.parametrize(
        "seconds, text",
        [(5400.0, "1h 30min"), (0, "0s"), (93661.5, "1d 2h 1min 1s 500ms")],
    )
    def test_render(self, seconds, text):
        assert render_time_span(seconds) == text

    def test_roundtrip(self):
        assert parse_time_span(render_time_span(93661.5)) == 93661.5


class TestDictionaryOfChoices:
    CURRENT = {"cmk.web": "h30", "cmk.core": "h20"}

    def test_to_ui(self):
        assert to_ui(LOG_LEVELS_SPEC, self.CURRENT) == {
            "Web": "Warning",
            "Core": "Informational",
        }

    def test_from_ui_by_title(self):
        assert from_ui(
            LOG_LEVELS_SPEC, {"Web": "Debug", "Core": "Error"}, self.CURRENT
        ) == {"cmk.web": "h10", "cmk.core": "h40"}

    def test_from_ui_accepts_internal_names_and_loose_titles(self):
        assert from_ui(
            LOG_LEVELS_SPEC, {"cmk.web": "debug", "core": " informational "}
        ) == {"cmk.web": "h10", "cmk.core": "h20"}

    def test_required_elements_keep_current_value(self):
        assert from_ui(LOG_LEVELS_SPEC, {"Web": "Debug"}, self.CURRENT) == {
            "cmk.web": "h10",
            "cmk.core": "h20",
        }

    def test_required_elements_fall_back_to_default(self):
        assert from_ui(LOG_LEVELS_SPEC, {"Web": "Debug"}, None) == {
            "cmk.web": "h10",
            "cmk.core": "h30",
        }

    def test_invalid_choice_lists_titles(self):
        with pytest.raises(GlobalSettingValueError) as e:
            from_ui(LOG_LEVELS_SPEC, {"Web": "Verbose"})
        assert "Web" in str(e.value) and "'Debug'" in str(e.value)

    def test_unknown_key(self):
        with pytest.raises(GlobalSettingValueError):
            from_ui(LOG_LEVELS_SPEC, {"Nope": "Debug"})

    def test_roundtrip(self):
        ui = to_ui(LOG_LEVELS_SPEC, self.CURRENT)
        assert from_ui(LOG_LEVELS_SPEC, ui, self.CURRENT) == self.CURRENT


class TestCascading:
    def test_plain_title_for_choice_without_parameters(self):
        assert from_ui(CASCADING_SPEC, "Disabled") == ["disabled", None]
        assert to_ui(CASCADING_SPEC, ["disabled", None]) == "Disabled"

    def test_nested(self):
        frontend = from_ui(
            CASCADING_SPEC, {"Enabled": {"Timeout": "2min", "Limit": "512 MiB"}}
        )
        assert frontend == ["enabled", {"timeout": 120.0, "limit": ["512", "MiB"]}]
        assert to_ui(CASCADING_SPEC, frontend) == {
            "Enabled": {"Timeout": "2min", "Limit": "512 MiB"}
        }

    def test_choice_needing_value(self):
        with pytest.raises(GlobalSettingValueError):
            from_ui(CASCADING_SPEC, "Enabled")

    def test_data_size_in_bytes_uses_displayed_unit(self):
        frontend = from_ui(CASCADING_SPEC, {"Enabled": {"Limit": 2 * 1024**3}})
        assert frontend[1]["limit"] == ["2", "GiB"]

    def test_canonical_data_size_ignores_unit(self):
        a = ["enabled", {"timeout": 60.0, "limit": ["1", "GiB"]}]
        b = ["enabled", {"timeout": 60, "limit": ["1024", "MiB"]}]
        assert canonical(CASCADING_SPEC, a) == canonical(CASCADING_SPEC, b)


class TestMultipleChoice:
    def test_roundtrip_and_order(self):
        current = [{"name": "a", "title": "Alpha"}, {"name": "c", "title": "Gamma"}]
        assert to_ui(MULTI_SPEC, current) == ["Alpha", "Gamma"]
        desired = from_ui(MULTI_SPEC, ["Gamma", "alpha"])
        assert canonical(MULTI_SPEC, desired) == canonical(MULTI_SPEC, current)


class TestPasswords:
    CURRENT = ["explicit_password", "uuid-1", "ENCRYPTED", True]

    def test_hidden_in_ui(self):
        assert to_ui(PASSWORD_SPEC, self.CURRENT) == HIDDEN_SECRET

    def test_kept_by_default(self):
        assert from_ui(PASSWORD_SPEC, "new", self.CURRENT) == self.CURRENT

    def test_updated_when_requested(self):
        assert from_ui(PASSWORD_SPEC, "new", self.CURRENT, update_secrets=True) == [
            "explicit_password",
            "uuid-1",
            "new",
            False,
        ]

    def test_new_password(self):
        assert from_ui(PASSWORD_SPEC, "new", None) == [
            "explicit_password",
            "",
            "new",
            False,
        ]

    def test_password_store_by_name(self):
        frontend = from_ui(PASSWORD_SPEC, {"password_store": "My stored pw"})
        assert frontend == ["stored_password", "pw_1", "", False]
        assert to_ui(PASSWORD_SPEC, frontend) == {"password_store": "My stored pw"}


class TestMisc:
    def test_legacy_valuespec_is_rejected(self):
        with pytest.raises(GlobalSettingValueError):
            from_ui({"type": "legacy_valuespec"}, {"x": 1})

    def test_boolean_from_string(self):
        assert from_ui({"type": "boolean_choice"}, "yes") is True

    def test_integer_from_string(self):
        assert from_ui({"type": "integer"}, "100") == 100

    def test_optional_choice(self):
        spec = {"type": "optional_choice", "parameter_form": {"type": "time_span"}}
        assert from_ui(spec, None) is None
        assert from_ui(spec, "1min") == 60.0
        assert to_ui(spec, 60.0) == "1min"


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------


class _Log:
    def __init__(self):
        self.lines = []

    def debug(self, msg):
        self.lines.append(msg)


class TestLogging:
    def test_logger_is_threaded_through_nested_specs(self):
        log = _Log()
        frontend = from_ui(CASCADING_SPEC, {"Enabled": {"Timeout": "2min"}}, logger=log)
        assert to_ui(CASCADING_SPEC, frontend, logger=log) == {
            "Enabled": {"Timeout": "2min"}
        }
        assert any("path=Enabled/Timeout" in line for line in log.lines)
        assert any("matched by title" in line for line in log.lines)

    def test_required_default_is_logged(self):
        log = _Log()
        from_ui(LOG_LEVELS_SPEC, {"Web": "Debug"}, logger=log)
        assert any("required element 'cmk.core'" in line for line in log.lines)

    def test_secrets_are_not_logged(self):
        log = _Log()
        spec = {
            "type": "dictionary",
            "elements": [
                {"name": "pw", "required": True, "parameter_form": PASSWORD_SPEC}
            ],
        }
        from_ui(spec, {"Secret": "s3cr3t-value"}, update_secrets=True, logger=log)
        assert log.lines
        assert not any("s3cr3t-value" in line for line in log.lines)

    def test_real_log_levels_spec(self):
        """The spec as delivered by the REST API (shortened to two loggers)."""
        levels = [
            ("1a65", "Critical"),
            ("d59e", "Error"),
            ("624b", "Warning"),
            ("f5ca", "Informational"),
            ("e629", "Verbose"),
            ("4a44", "Debug"),
        ]

        def element(name, title):
            return {
                "name": name,
                "required": True,
                "default_value": "624b",
                "parameter_form": {
                    "title": title,
                    "type": "single_choice",
                    "elements": [{"name": n, "title": t} for n, t in levels],
                },
            }

        spec = {
            "type": "dictionary",
            "title": "Logging",
            "elements": [
                element("cmk.web", "Web"),
                element("cmk.web.auth", "Authentication"),
            ],
        }
        current = {"cmk.web": "624b", "cmk.web.auth": "624b"}
        log = _Log()
        desired = from_ui(
            spec,
            {"Web": "Informational", "Authentication": "Debug"},
            current=current,
            logger=log,
        )
        assert desired == {"cmk.web": "f5ca", "cmk.web.auth": "4a44"}
        assert to_ui(spec, current, logger=log) == {
            "Web": "Warning",
            "Authentication": "Warning",
        }


class TestDiffPaths:
    def test_paths(self):
        from ansible_collections.checkmk.general.plugins.module_utils.global_settings import (
            diff_paths,
        )

        assert diff_paths({"a": 1, "b": [1, 2]}, {"a": 1, "b": [1, 3]}) == ["b/1"]
        assert diff_paths({"a": 1}, {"a": 1}) == []
        assert diff_paths({"a": 1}, {}) == ["a"]

#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2026, Checkmk GmbH
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from unittest.mock import MagicMock, patch

import pytest
from ansible_collections.checkmk.general.plugins.module_utils.site import (
    SiteConnection,
    TargetAPI,
)
from ansible_collections.checkmk.general.plugins.module_utils.version import (
    CheckmkVersion,
)
from ansible_collections.checkmk.general.plugins.modules import site as site_module
from ansible_collections.checkmk.general.plugins.modules.site import (
    SiteAPI,
    strips_unreplicated_fields,
    werk16722,
)

# ---------------------------------------------------------------------------
# strips_unreplicated_fields
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "version",
    [
        "2.3.0p26",
        "2.3.0p48",
        "2.4.0",
        "2.4.0p31",
        "2.4.0-2026.01.01",  # daily, suffix dropped
    ],
)
def test_fields_are_stripped_between_werk_and_2_5(version):
    """Werk 16722 made the fields optional, and 2.4 has a dedicated schema for
    connections without replication that requires only enable_replication."""
    assert strips_unreplicated_fields(CheckmkVersion(version)) is True


@pytest.mark.parametrize(
    "version",
    [
        "2.2.0p1",
        "2.3.0p24",
        "2.3.0p25",  # the werk landed *in* p25, so the gate is exclusive
    ],
)
def test_fields_are_not_stripped_before_the_werk(version):
    assert strips_unreplicated_fields(CheckmkVersion(version)) is False


@pytest.mark.parametrize(
    "version",
    [
        "2.5.0b3",  # betas sort above the base release
        "2.5.0",
        "2.5.0p9",
        "2.5.0p10",
        "2.5.0-2026.07.24",
        "3.0.0",
        "3.0.0-2026.07.30",
    ],
)
def test_fields_are_not_stripped_from_2_5_on(version):
    """2.5 collapsed the two schemas into one ConnectionModel that requires all
    nine fields regardless of replication, and 3.0 behaves the same way.

    Stripping here produced a bare {"enable_replication": false} and a 400
    listing eight missing required fields, so no status-only connection could
    be created at all.
    """
    assert strips_unreplicated_fields(CheckmkVersion(version)) is False


# ---------------------------------------------------------------------------
# werk16722
# ---------------------------------------------------------------------------


def test_werk16722_removes_the_optional_fields():
    site_config = {
        "configuration_connection": {
            "enable_replication": False,
            "url_of_remote_site": "http://remote/remote/check_mk/",
            "user_sync": {"sync_with_ldap_connections": "all"},
            "disable_remote_configuration": True,
            "ignore_tls_errors": False,
            "direct_login_to_web_gui_allowed": True,
            "replicate_event_console": True,
            "replicate_extensions": True,
            "message_broker_port": 5672,
            "is_trusted": True,
        }
    }

    werk16722(site_config)

    assert site_config["configuration_connection"] == {"enable_replication": False}


def test_werk16722_tolerates_absent_keys():
    site_config = {"configuration_connection": {"enable_replication": False}}

    werk16722(site_config)

    assert site_config["configuration_connection"] == {"enable_replication": False}


# ---------------------------------------------------------------------------
# verify_message_broker_port
# ---------------------------------------------------------------------------


def _api_without_init(version, params):
    """A SiteAPI that skips __init__, so no HTTP call is needed."""
    with patch.object(SiteAPI, "__init__", lambda self, mod: None):
        api = SiteAPI(None)

    api.module = MagicMock()
    api.params = params
    api.state = "present"
    api.getversion = lambda: CheckmkVersion(version)
    return api


def _params(port=None):
    configuration_connection = {"enable_replication": False}
    if port is not None:
        configuration_connection["message_broker_port"] = port

    return {
        "site_connection": {
            "site_config": {"configuration_connection": configuration_connection}
        }
    }


@pytest.mark.parametrize("version", ["2.5.0", "2.5.0p11", "3.0.0"])
def test_creating_without_the_port_fails_from_2_5_on(version):
    api = _api_without_init(version, _params())

    with patch(
        "ansible_collections.checkmk.general.plugins.modules.site.exit_module"
    ) as exit_mock:
        api.verify_message_broker_port()

    assert exit_mock.call_count == 1
    assert exit_mock.call_args.kwargs["failed"] is True
    assert "message_broker_port" in exit_mock.call_args.kwargs["msg"]
    assert "RABBITMQ_PORT" in exit_mock.call_args.kwargs["msg"]


@pytest.mark.parametrize("version", ["2.5.0", "3.0.0"])
def test_creating_with_the_port_passes_from_2_5_on(version):
    api = _api_without_init(version, _params(port=5672))

    with patch(
        "ansible_collections.checkmk.general.plugins.modules.site.exit_module"
    ) as exit_mock:
        api.verify_message_broker_port()

    assert exit_mock.call_count == 0


@pytest.mark.parametrize("version", ["2.3.0p25", "2.4.0", "2.4.0p31"])
def test_creating_without_the_port_is_fine_before_2_5(version):
    api = _api_without_init(version, _params())

    with patch(
        "ansible_collections.checkmk.general.plugins.modules.site.exit_module"
    ) as exit_mock:
        api.verify_message_broker_port()

    assert exit_mock.call_count == 0


def test_the_port_is_not_required_when_constructing_the_api():
    """The guard must not sit in _verify_compatibility.

    It used to, which made every 'state: present' call on 2.5 fail without the
    parameter, including partial updates of an existing connection that
    legitimately omit it.
    """
    api = _api_without_init("2.5.0p11", _params())

    with patch(
        "ansible_collections.checkmk.general.plugins.modules.site.exit_module"
    ) as exit_mock:
        api._verify_compatibility()

    assert exit_mock.call_count == 0


def _run_module(exit_mock):
    """Run the module with a faithful exit_module.

    The real one ends the process via AnsibleModule.exit_json / fail_json, and
    run_module relies on that: its branches call exit_module and then fall
    through. A mock that merely records the call would let execution continue
    into code the module never reaches in production.
    """
    exit_mock.side_effect = SystemExit

    with pytest.raises(SystemExit):
        site_module.run_module()


class TestRunModule:
    """The port is demanded on the create path only."""

    @staticmethod
    def _module(port=None, state="present"):
        mock_module = MagicMock()
        mock_module.params = dict(_params(port=port), site_id="remote", state=state)
        mock_module._verbosity = 0
        return mock_module

    @staticmethod
    def _api():
        mock_api = MagicMock()
        mock_api.getversion.return_value = CheckmkVersion("2.5.0p11")
        return mock_api

    @patch("ansible_collections.checkmk.general.plugins.modules.site.exit_module")
    @patch("ansible_collections.checkmk.general.plugins.modules.site.SiteConnection")
    @patch("ansible_collections.checkmk.general.plugins.modules.site.SiteAPI")
    @patch("ansible_collections.checkmk.general.plugins.modules.site.AnsibleModule")
    def test_update_does_not_demand_the_port(
        self, module_cls, api_cls, connection_cls, exit_mock
    ):
        module_cls.return_value = self._module()
        api = self._api()
        api_cls.return_value = api

        desired = MagicMock(state="present")
        existing = MagicMock(state="present")
        existing.diff.return_value = ["alias"]
        connection_cls.from_module_params.return_value = desired
        connection_cls.from_api.return_value = existing

        _run_module(exit_mock)

        api.update.assert_called_once()
        api.verify_message_broker_port.assert_not_called()

    @patch("ansible_collections.checkmk.general.plugins.modules.site.exit_module")
    @patch("ansible_collections.checkmk.general.plugins.modules.site.SiteConnection")
    @patch("ansible_collections.checkmk.general.plugins.modules.site.SiteAPI")
    @patch("ansible_collections.checkmk.general.plugins.modules.site.AnsibleModule")
    def test_create_demands_the_port(
        self, module_cls, api_cls, connection_cls, exit_mock
    ):
        module_cls.return_value = self._module()
        api = self._api()
        api_cls.return_value = api

        connection_cls.from_module_params.return_value = MagicMock(state="present")
        connection_cls.from_api.return_value = None

        _run_module(exit_mock)

        api.create.assert_called_once()
        api.verify_message_broker_port.assert_called_once()

    @patch("ansible_collections.checkmk.general.plugins.modules.site.exit_module")
    @patch("ansible_collections.checkmk.general.plugins.modules.site.SiteConnection")
    @patch("ansible_collections.checkmk.general.plugins.modules.site.SiteAPI")
    @patch("ansible_collections.checkmk.general.plugins.modules.site.AnsibleModule")
    def test_an_unchanged_connection_is_not_written(
        self, module_cls, api_cls, connection_cls, exit_mock
    ):
        module_cls.return_value = self._module()
        api = self._api()
        api_cls.return_value = api

        existing = MagicMock(state="present")
        existing.diff.return_value = []
        connection_cls.from_module_params.return_value = MagicMock(state="present")
        connection_cls.from_api.return_value = existing

        _run_module(exit_mock)

        api.update.assert_not_called()
        api.create.assert_not_called()
        assert exit_mock.call_args.kwargs["result"].changed is False

    @patch("ansible_collections.checkmk.general.plugins.modules.site.exit_module")
    @patch("ansible_collections.checkmk.general.plugins.modules.site.SiteConnection")
    @patch("ansible_collections.checkmk.general.plugins.modules.site.SiteAPI")
    @patch("ansible_collections.checkmk.general.plugins.modules.site.AnsibleModule")
    def test_absent_deletes_an_existing_connection(
        self, module_cls, api_cls, connection_cls, exit_mock
    ):
        module_cls.return_value = self._module(state="absent")
        api = self._api()
        api_cls.return_value = api

        connection_cls.from_module_params.return_value = MagicMock(state="absent")
        connection_cls.from_api.return_value = MagicMock(state="present")

        _run_module(exit_mock)

        api.delete.assert_called_once()

    @patch("ansible_collections.checkmk.general.plugins.modules.site.exit_module")
    @patch("ansible_collections.checkmk.general.plugins.modules.site.SiteConnection")
    @patch("ansible_collections.checkmk.general.plugins.modules.site.SiteAPI")
    @patch("ansible_collections.checkmk.general.plugins.modules.site.AnsibleModule")
    def test_absent_is_a_no_op_when_the_connection_is_gone(
        self, module_cls, api_cls, connection_cls, exit_mock
    ):
        module_cls.return_value = self._module(state="absent")
        api = self._api()
        api_cls.return_value = api

        connection_cls.from_module_params.return_value = MagicMock(state="absent")
        connection_cls.from_api.return_value = None

        _run_module(exit_mock)

        api.delete.assert_not_called()
        assert "already absent" in exit_mock.call_args.kwargs["msg"]

    @pytest.mark.parametrize("state", ["login", "logout"])
    @patch("ansible_collections.checkmk.general.plugins.modules.site.exit_module")
    @patch("ansible_collections.checkmk.general.plugins.modules.site.SiteConnection")
    @patch("ansible_collections.checkmk.general.plugins.modules.site.SiteAPI")
    @patch("ansible_collections.checkmk.general.plugins.modules.site.AnsibleModule")
    def test_login_and_logout_need_an_existing_connection(
        self, module_cls, api_cls, connection_cls, exit_mock, state
    ):
        module_cls.return_value = self._module(state=state)
        api = self._api()
        api_cls.return_value = api

        connection_cls.from_module_params.return_value = MagicMock(state=state)
        connection_cls.from_api.return_value = None

        _run_module(exit_mock)

        api.login.assert_not_called()
        api.logout.assert_not_called()
        assert exit_mock.call_args.kwargs["failed"] is True

    @patch("ansible_collections.checkmk.general.plugins.modules.site.exit_module")
    @patch("ansible_collections.checkmk.general.plugins.modules.site.SiteConnection")
    @patch("ansible_collections.checkmk.general.plugins.modules.site.SiteAPI")
    @patch("ansible_collections.checkmk.general.plugins.modules.site.AnsibleModule")
    def test_login_is_skipped_when_already_logged_in(
        self, module_cls, api_cls, connection_cls, exit_mock
    ):
        module_cls.return_value = self._module(state="login")
        api = self._api()
        api_cls.return_value = api

        existing = MagicMock(state="present")
        existing.logged_in.return_value = True
        connection_cls.from_module_params.return_value = MagicMock(state="login")
        connection_cls.from_api.return_value = existing

        _run_module(exit_mock)

        api.login.assert_not_called()
        assert "Already logged in" in exit_mock.call_args.kwargs["msg"]

    @patch("ansible_collections.checkmk.general.plugins.modules.site.exit_module")
    @patch("ansible_collections.checkmk.general.plugins.modules.site.SiteConnection")
    @patch("ansible_collections.checkmk.general.plugins.modules.site.SiteAPI")
    @patch("ansible_collections.checkmk.general.plugins.modules.site.AnsibleModule")
    def test_logout_is_skipped_when_not_logged_in(
        self, module_cls, api_cls, connection_cls, exit_mock
    ):
        module_cls.return_value = self._module(state="logout")
        api = self._api()
        api_cls.return_value = api

        existing = MagicMock(state="present")
        existing.logged_in.return_value = False
        connection_cls.from_module_params.return_value = MagicMock(state="logout")
        connection_cls.from_api.return_value = existing

        _run_module(exit_mock)

        api.logout.assert_not_called()
        assert "Already logged out" in exit_mock.call_args.kwargs["msg"]


# ---------------------------------------------------------------------------
# SiteConnection.diff
# ---------------------------------------------------------------------------


def _connection(site_config, state="present"):
    return SiteConnection(site_config=site_config, site_id="remote", state=state)


def test_diff_only_looks_at_the_keys_the_playbook_sent():
    """Keys the server holds but the task omits are not differences.

    This is what makes a partial update idempotent: the API returns every field
    of a connection, and a task that sets one of them must not be reported as
    changing the rest.
    """
    existing = _connection(
        {
            "basic_settings": {"alias": "old", "site_id": "remote"},
            "configuration_connection": {
                "enable_replication": True,
                "message_broker_port": 5672,
            },
        }
    )
    desired = _connection({"basic_settings": {"alias": "new"}})

    assert existing.diff(desired) == ["alias"]


def test_diff_recurses_into_nested_dicts():
    existing = _connection(
        {"status_connection": {"connection": {"port": 6557, "host": "old"}}}
    )
    desired = _connection(
        {"status_connection": {"connection": {"port": 1234, "host": "old"}}}
    )

    assert existing.diff(desired) == ["port"]


def test_diff_is_empty_when_everything_matches():
    site_config = {
        "basic_settings": {"alias": "same"},
        "configuration_connection": {"enable_replication": False},
    }

    assert _connection(dict(site_config)).diff(_connection(dict(site_config))) == []


def test_diff_ignores_the_logged_in_key():
    """'logged_in' is server state, not configuration.

    Comparing it would make every run after a login report a change.
    """
    existing = _connection({"basic_settings": {"alias": "same"}, "logged_in": True})
    desired = _connection({"basic_settings": {"alias": "same"}, "logged_in": False})

    assert existing.diff(desired) == []


# ---------------------------------------------------------------------------
# SiteConnection.merge_with
# ---------------------------------------------------------------------------


def test_merge_with_keeps_fields_the_update_did_not_restate():
    """An update PUTs the existing connection with the desired values merged in.

    This is why creating demands message_broker_port but updating does not: the
    stored value is carried over untouched.
    """
    existing = _connection(
        {
            "basic_settings": {"alias": "old", "site_id": "remote"},
            "configuration_connection": {
                "enable_replication": True,
                "message_broker_port": 5672,
            },
        }
    )
    existing.merge_with(_connection({"basic_settings": {"alias": "new"}}))

    assert existing.site_config == {
        "basic_settings": {"alias": "new", "site_id": "remote"},
        "configuration_connection": {
            "enable_replication": True,
            "message_broker_port": 5672,
        },
    }


def test_merge_with_does_not_carry_logged_in_over():
    """Logging in is done with state 'login', never as a side effect of a merge."""
    existing = _connection({"basic_settings": {"alias": "old"}})
    existing.merge_with(
        _connection({"basic_settings": {"alias": "new"}, "logged_in": True})
    )

    assert "logged_in" not in existing.site_config


# ---------------------------------------------------------------------------
# SiteConnection.logged_in and get_api_data
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "site_config",
    [
        {"secret": "abc"},  # before werk 18286
        {"logged_in": True},  # after werk 18907
    ],
)
def test_logged_in_accepts_both_api_shapes(site_config):
    assert _connection(site_config).logged_in() is True


@pytest.mark.parametrize("site_config", [{}, {"logged_in": False}, None])
def test_logged_in_is_falsy_otherwise(site_config):
    assert not _connection(site_config).logged_in()


@pytest.mark.parametrize("target", [TargetAPI.CREATE, TargetAPI.UPDATE])
def test_get_api_data_drops_logged_in_from_writes(target):
    """'logged_in' is read-only; sending it back would be rejected."""
    connection = _connection(
        {"basic_settings": {"alias": "some site"}, "logged_in": True}
    )

    assert connection.get_api_data(target) == {
        "site_config": {"basic_settings": {"alias": "some site"}}
    }


def test_get_api_data_sends_only_the_credentials_on_login():
    connection = SiteConnection(
        authentication={"username": "automation", "password": "secret"},
        site_config={"basic_settings": {"alias": "some site"}},
        site_id="remote",
        state="login",
    )

    assert connection.get_api_data(TargetAPI.LOGIN) == {
        "username": "automation",
        "password": "secret",
    }


# ---------------------------------------------------------------------------
# _verify_compatibility
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("version", ["2.1.0p1", "2.2.0"])
def test_site_management_is_refused_before_2_2(version):
    api = _api_without_init(version, _params())

    with patch(
        "ansible_collections.checkmk.general.plugins.modules.site.exit_module"
    ) as exit_mock:
        api._verify_compatibility()

    assert exit_mock.call_args.kwargs["failed"] is True
    assert "2.2.0" in exit_mock.call_args.kwargs["msg"]


@pytest.mark.parametrize("version", ["2.2.0p1", "2.3.0p25"])
def test_the_port_is_refused_before_2_4(version):
    """message_broker_port did not exist before 2.4, so passing it is an error
    rather than something to silently drop."""
    api = _api_without_init(version, _params(port=5672))

    with patch(
        "ansible_collections.checkmk.general.plugins.modules.site.exit_module"
    ) as exit_mock:
        api._verify_compatibility()

    assert exit_mock.call_args.kwargs["failed"] is True
    assert "message_broker_port" in exit_mock.call_args.kwargs["msg"]


@pytest.mark.parametrize("version", ["2.4.0i1", "2.4.0b1", "2.4.0p1", "2.5.0p11"])
def test_the_port_is_accepted_from_2_4_on(version):
    api = _api_without_init(version, _params(port=5672))

    with patch(
        "ansible_collections.checkmk.general.plugins.modules.site.exit_module"
    ) as exit_mock:
        api._verify_compatibility()

    assert exit_mock.call_count == 0

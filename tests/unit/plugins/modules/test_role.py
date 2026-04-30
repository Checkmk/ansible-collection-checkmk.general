#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2025, Checkmk GmbH
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
from unittest.mock import MagicMock, patch


from ansible_collections.checkmk.general.plugins.module_utils.types import RESULT
from ansible_collections.checkmk.general.plugins.modules.role import (
    BUILTIN_ROLES,
    VALID_PERMISSION_VALUES,
    RoleAPI,
    run_module,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

COMMON_PARAMS = {
    "server_url": "http://localhost/",
    "site": "mysite",
    "api_user": "cmkadmin",
    "api_secret": "mysecret",
    "validate_certs": True,
}

ROLE_GET_RESPONSE_200 = RESULT(
    http_code=200,
    msg="Role found, nothing changed.",
    content=json.dumps(
        {
            "id": "test_role",
            "extensions": {
                "alias": "Test Role",
                "permissions": ["general.use"],
                "builtin": False,
                "basedon": "user",
            },
        }
    ).encode("utf-8"),
    etag="",
    failed=False,
    changed=False,
)

ROLE_GET_RESPONSE_404 = RESULT(
    http_code=404,
    msg="Role not found.",
    content={},
    etag="",
    failed=False,
    changed=False,
)

ROLE_CREATE_RESPONSE = RESULT(
    http_code=200,
    msg="Role created.",
    content={},
    etag="",
    failed=False,
    changed=True,
)

ROLE_EDIT_RESPONSE = RESULT(
    http_code=200,
    msg="Role updated.",
    content={},
    etag="",
    failed=False,
    changed=True,
)

ROLE_DELETE_RESPONSE = RESULT(
    http_code=204,
    msg="Role deleted.",
    content={},
    etag="",
    failed=False,
    changed=True,
)


def _make_module_params(**overrides):
    params = dict(COMMON_PARAMS)
    params.update(
        {
            "name": "test_role",
            "title": None,
            "based_on": None,
            "permissions": None,
            "state": "present",
        }
    )
    params.update(overrides)
    return params


def _mock_role_api(module_params, current_result):
    mock_module = MagicMock()
    mock_module.params = module_params
    mock_module.check_mode = False

    with patch.object(RoleAPI, "__init__", lambda self, mod: None):
        api = RoleAPI.__new__(RoleAPI)
        api.module = mock_module
        api.params = module_params
        api.state = module_params["state"]
        api.name = module_params["name"]
        api.title = module_params.get("title")
        api.based_on = module_params.get("based_on")
        api.permissions = module_params.get("permissions")
        api.current = current_result
        api.headers = {}

    return api


# ---------------------------------------------------------------------------
# Tests for constants
# ---------------------------------------------------------------------------


class TestConstants:
    def test_builtin_roles_contains_expected(self):
        assert "admin" in BUILTIN_ROLES
        assert "user" in BUILTIN_ROLES
        assert "guest" in BUILTIN_ROLES
        assert "agent_registration" in BUILTIN_ROLES

    def test_builtin_roles_length(self):
        assert len(BUILTIN_ROLES) == 4

    def test_valid_permission_values(self):
        assert VALID_PERMISSION_VALUES == frozenset({"yes", "no", "default"})


# ---------------------------------------------------------------------------
# Tests for RoleAPI._needs_update
# ---------------------------------------------------------------------------


class TestNeedsUpdate:
    def test_no_update_when_role_not_found(self):
        params = _make_module_params(title="New Title")
        api = _mock_role_api(params, ROLE_GET_RESPONSE_404)
        assert api._needs_update() is False

    def test_no_update_when_nothing_specified(self):
        params = _make_module_params()
        api = _mock_role_api(params, ROLE_GET_RESPONSE_200)
        assert api._needs_update() is False

    def test_update_needed_when_title_differs(self):
        params = _make_module_params(title="Different Title")
        api = _mock_role_api(params, ROLE_GET_RESPONSE_200)
        assert api._needs_update() is True

    def test_no_update_when_title_matches(self):
        params = _make_module_params(title="Test Role")
        api = _mock_role_api(params, ROLE_GET_RESPONSE_200)
        assert api._needs_update() is False

    def test_update_needed_when_permission_value_differs(self):
        params = _make_module_params(
            permissions={
                "wato.edit": "yes"
            }  # wato.edit absent from enabled list → needs enabling
        )
        api = _mock_role_api(params, ROLE_GET_RESPONSE_200)
        assert api._needs_update() is True

    def test_no_update_when_permission_matches(self):
        params = _make_module_params(
            permissions={
                "wato.edit": "no"
            }  # wato.edit absent from enabled list → already disabled
        )
        api = _mock_role_api(params, ROLE_GET_RESPONSE_200)
        assert api._needs_update() is False

    def test_update_needed_when_new_permission_added(self):
        params = _make_module_params(
            permissions={"wato.all_folders": "yes"}  # not in current
        )
        api = _mock_role_api(params, ROLE_GET_RESPONSE_200)
        assert api._needs_update() is True

    def test_no_update_when_default_matches_base(self):
        # general.use is in both base and current perms -> "default" = no change
        params = _make_module_params(permissions={"general.use": "default"})
        api = _mock_role_api(params, ROLE_GET_RESPONSE_200)
        with patch.object(
            api, "_get_base_role_permissions", return_value={"general.use"}
        ) as mock_get_base:
            assert api._needs_update() is False
        mock_get_base.assert_called_once_with("user")

    def test_update_needed_when_default_differs_from_base(self):
        # wato.edit in base but NOT in current -> "default" should restore it -> update needed
        params = _make_module_params(permissions={"wato.edit": "default"})
        api = _mock_role_api(params, ROLE_GET_RESPONSE_200)
        with patch.object(
            api, "_get_base_role_permissions", return_value={"wato.edit"}
        ) as mock_get_base:
            assert api._needs_update() is True
        mock_get_base.assert_called_once_with("user")

    def test_update_needed_when_both_title_and_permissions_differ(self):
        params = _make_module_params(
            title="Changed Title",
            permissions={"wato.edit": "yes"},
        )
        api = _mock_role_api(params, ROLE_GET_RESPONSE_200)
        assert api._needs_update() is True

    def test_no_update_when_title_and_permissions_match(self):
        params = _make_module_params(
            title="Test Role",
            permissions={
                "general.use": "yes",
                "wato.edit": "no",
            },
        )
        api = _mock_role_api(params, ROLE_GET_RESPONSE_200)
        assert api._needs_update() is False


# ---------------------------------------------------------------------------
# Tests for RoleAPI._build_edit_data
# ---------------------------------------------------------------------------


class TestBuildEditData:
    def test_empty_when_nothing_set(self):
        params = _make_module_params()
        api = _mock_role_api(params, ROLE_GET_RESPONSE_200)
        assert api._build_edit_data() == {}

    def test_includes_alias_when_title_set(self):
        params = _make_module_params(title="New Title")
        api = _mock_role_api(params, ROLE_GET_RESPONSE_200)
        data = api._build_edit_data()
        assert data == {"new_alias": "New Title"}

    def test_includes_permissions_when_set(self):
        perms = {"wato.edit": "yes", "wato.all_folders": "no"}
        params = _make_module_params(permissions=perms)
        api = _mock_role_api(params, ROLE_GET_RESPONSE_200)
        data = api._build_edit_data()
        assert data == {"new_permissions": perms}

    def test_includes_both_when_both_set(self):
        perms = {"wato.edit": "yes"}
        params = _make_module_params(title="My Title", permissions=perms)
        api = _mock_role_api(params, ROLE_GET_RESPONSE_200)
        data = api._build_edit_data()
        assert data == {"new_alias": "My Title", "new_permissions": perms}


# ---------------------------------------------------------------------------
# Tests for RoleAPI.create
# ---------------------------------------------------------------------------


class TestCreate:
    def test_create_sends_correct_data(self):
        params = _make_module_params(
            name="new_role",
            title="New Role",
            based_on="user",
        )
        api = _mock_role_api(params, ROLE_GET_RESPONSE_404)
        api._fetch = MagicMock(return_value=ROLE_CREATE_RESPONSE)

        result = api.create()

        api._fetch.assert_called_once()
        call_kwargs = api._fetch.call_args
        data = call_kwargs.kwargs.get("data") or call_kwargs[1].get("data")
        assert data["role_id"] == "user"
        assert data["new_role_id"] == "new_role"
        assert data["new_alias"] == "New Role"
        assert "permissions" not in data
        assert result.changed is True

    def test_create_without_optional_fields(self):
        params = _make_module_params(
            name="minimal_role",
            based_on="guest",
        )
        api = _mock_role_api(params, ROLE_GET_RESPONSE_404)
        api._fetch = MagicMock(return_value=ROLE_CREATE_RESPONSE)

        api.create()

        call_kwargs = api._fetch.call_args
        data = call_kwargs.kwargs.get("data") or call_kwargs[1].get("data")
        assert data["role_id"] == "guest"
        assert data["new_role_id"] == "minimal_role"
        assert "new_alias" not in data
        assert "permissions" not in data


# ---------------------------------------------------------------------------
# Tests for RoleAPI.edit
# ---------------------------------------------------------------------------


class TestEdit:
    def test_edit_returns_no_change_when_no_data(self):
        params = _make_module_params()
        api = _mock_role_api(params, ROLE_GET_RESPONSE_200)

        result = api.edit()

        assert result.changed is False
        assert result.msg == "Role already up to date."

    def test_edit_sends_correct_data(self):
        params = _make_module_params(
            title="Updated Title",
            permissions={"wato.all_folders": "yes"},
        )
        api = _mock_role_api(params, ROLE_GET_RESPONSE_200)
        api._fetch = MagicMock(return_value=ROLE_EDIT_RESPONSE)

        result = api.edit()

        api._fetch.assert_called_once()
        call_kwargs = api._fetch.call_args
        data = call_kwargs.kwargs.get("data") or call_kwargs[1].get("data")
        assert data["new_alias"] == "Updated Title"
        assert data["new_permissions"] == {"wato.all_folders": "yes"}
        assert result.changed is True


# ---------------------------------------------------------------------------
# Tests for RoleAPI.delete
# ---------------------------------------------------------------------------


class TestDelete:
    def test_delete_calls_correct_endpoint(self):
        params = _make_module_params(name="test_role", state="absent")
        api = _mock_role_api(params, ROLE_GET_RESPONSE_200)
        api._fetch = MagicMock(return_value=ROLE_DELETE_RESPONSE)

        result = api.delete()

        api._fetch.assert_called_once()
        call_kwargs = api._fetch.call_args
        endpoint = call_kwargs.kwargs.get("endpoint") or call_kwargs[1].get("endpoint")
        assert "test_role" in endpoint
        method = call_kwargs.kwargs.get("method") or call_kwargs[1].get("method")
        assert method == "DELETE"
        assert result.changed is True


# ---------------------------------------------------------------------------
# Tests for run_module (integration of the logic)
# ---------------------------------------------------------------------------


class TestRunModule:
    @patch("ansible_collections.checkmk.general.plugins.modules.role.RoleAPI")
    @patch("ansible_collections.checkmk.general.plugins.modules.role.AnsibleModule")
    def test_present_creates_new_role(self, mock_ansible_module_cls, mock_role_api_cls):
        mock_module = MagicMock()
        mock_module.params = _make_module_params(
            name="new_role", title="New", based_on="user"
        )
        mock_module.check_mode = False
        mock_ansible_module_cls.return_value = mock_module

        mock_api = MagicMock()
        mock_api.state = "present"
        mock_api.name = "new_role"
        mock_api.current = ROLE_GET_RESPONSE_404
        mock_api.based_on = "user"
        mock_api.permissions = None
        mock_api.create.return_value = ROLE_CREATE_RESPONSE
        mock_role_api_cls.return_value = mock_api

        run_module()

        mock_api.create.assert_called_once()
        mock_api.edit.assert_not_called()
        mock_module.exit_json.assert_called_once()

    @patch("ansible_collections.checkmk.general.plugins.modules.role.RoleAPI")
    @patch("ansible_collections.checkmk.general.plugins.modules.role.AnsibleModule")
    def test_present_creates_role_with_permissions(
        self, mock_ansible_module_cls, mock_role_api_cls
    ):
        mock_module = MagicMock()
        mock_module.params = _make_module_params(
            name="new_role",
            title="New",
            based_on="user",
            permissions={"wato.all_folders": "yes"},
        )
        mock_module.check_mode = False
        mock_ansible_module_cls.return_value = mock_module

        mock_api = MagicMock()
        mock_api.state = "present"
        mock_api.name = "new_role"
        mock_api.current = ROLE_GET_RESPONSE_404
        mock_api.based_on = "user"
        mock_api.permissions = {"wato.all_folders": "yes"}
        mock_api.create.return_value = ROLE_CREATE_RESPONSE
        mock_api.edit.return_value = ROLE_EDIT_RESPONSE
        mock_role_api_cls.return_value = mock_api

        run_module()

        mock_api.create.assert_called_once()
        mock_api.edit.assert_called_once()
        mock_module.exit_json.assert_called_once()
        call_kwargs = mock_module.exit_json.call_args[1]
        assert call_kwargs["changed"] is True
        assert call_kwargs["msg"] == "Role created."

    @patch("ansible_collections.checkmk.general.plugins.modules.role.RoleAPI")
    @patch("ansible_collections.checkmk.general.plugins.modules.role.AnsibleModule")
    def test_title_nulled_before_postcreate_edit(
        self, mock_ansible_module_cls, mock_role_api_cls
    ):
        mock_module = MagicMock()
        mock_module.params = _make_module_params(
            name="new_role",
            title="New",
            based_on="user",
            permissions={"wato.all_folders": "yes"},
        )
        mock_module.check_mode = False
        mock_ansible_module_cls.return_value = mock_module

        mock_api = MagicMock()
        mock_api.state = "present"
        mock_api.name = "new_role"
        mock_api.current = ROLE_GET_RESPONSE_404
        mock_api.based_on = "user"
        mock_api.permissions = {"wato.all_folders": "yes"}
        mock_api.title = "New"
        mock_api.create.return_value = ROLE_CREATE_RESPONSE

        captured_title = []

        def capture_title():
            captured_title.append(mock_api.title)
            return ROLE_EDIT_RESPONSE

        mock_api.edit.side_effect = capture_title
        mock_role_api_cls.return_value = mock_api

        run_module()

        mock_api.edit.assert_called_once()
        assert captured_title[0] is None

    @patch("ansible_collections.checkmk.general.plugins.modules.role.RoleAPI")
    @patch("ansible_collections.checkmk.general.plugins.modules.role.AnsibleModule")
    def test_postcreate_edit_failure_calls_fail_json(
        self, mock_ansible_module_cls, mock_role_api_cls
    ):
        mock_module = MagicMock()
        mock_module.params = _make_module_params(
            name="new_role",
            based_on="user",
            permissions={"wato.all_folders": "yes"},
        )
        mock_module.check_mode = False
        mock_ansible_module_cls.return_value = mock_module

        failed_edit = RESULT(
            http_code=400,
            msg="Bad request.",
            content={},
            etag="",
            failed=True,
            changed=False,
        )
        mock_api = MagicMock()
        mock_api.state = "present"
        mock_api.name = "new_role"
        mock_api.current = ROLE_GET_RESPONSE_404
        mock_api.based_on = "user"
        mock_api.permissions = {"wato.all_folders": "yes"}
        mock_api.title = None
        mock_api.create.return_value = ROLE_CREATE_RESPONSE
        mock_api.edit.return_value = failed_edit
        mock_role_api_cls.return_value = mock_api

        run_module()

        mock_module.fail_json.assert_called_once()
        fail_kwargs = mock_module.fail_json.call_args[1]
        assert fail_kwargs["msg"] == "Bad request."
        mock_module.exit_json.assert_not_called()

    @patch("ansible_collections.checkmk.general.plugins.modules.role.RoleAPI")
    @patch("ansible_collections.checkmk.general.plugins.modules.role.AnsibleModule")
    def test_present_updates_existing_role(
        self, mock_ansible_module_cls, mock_role_api_cls
    ):
        mock_module = MagicMock()
        mock_module.params = _make_module_params(name="test_role", title="Changed")
        mock_module.check_mode = False
        mock_ansible_module_cls.return_value = mock_module

        mock_api = MagicMock()
        mock_api.state = "present"
        mock_api.name = "test_role"
        mock_api.current = ROLE_GET_RESPONSE_200
        mock_api._needs_update.return_value = True
        mock_api.edit.return_value = ROLE_EDIT_RESPONSE
        mock_role_api_cls.return_value = mock_api

        run_module()

        mock_api.edit.assert_called_once()
        mock_module.exit_json.assert_called_once()

    @patch("ansible_collections.checkmk.general.plugins.modules.role.RoleAPI")
    @patch("ansible_collections.checkmk.general.plugins.modules.role.AnsibleModule")
    def test_present_no_change_when_up_to_date(
        self, mock_ansible_module_cls, mock_role_api_cls
    ):
        mock_module = MagicMock()
        mock_module.params = _make_module_params(name="test_role", title="Test Role")
        mock_module.check_mode = False
        mock_ansible_module_cls.return_value = mock_module

        mock_api = MagicMock()
        mock_api.state = "present"
        mock_api.name = "test_role"
        mock_api.current = ROLE_GET_RESPONSE_200
        mock_api._needs_update.return_value = False
        mock_role_api_cls.return_value = mock_api

        run_module()

        mock_api.create.assert_not_called()
        mock_api.edit.assert_not_called()
        mock_module.exit_json.assert_called_once()
        call_kwargs = mock_module.exit_json.call_args[1]
        assert call_kwargs["changed"] is False

    @patch("ansible_collections.checkmk.general.plugins.modules.role.RoleAPI")
    @patch("ansible_collections.checkmk.general.plugins.modules.role.AnsibleModule")
    def test_present_fails_without_based_on(
        self, mock_ansible_module_cls, mock_role_api_cls
    ):
        mock_module = MagicMock()
        mock_module.params = _make_module_params(
            name="new_role", title="New", based_on=None
        )
        mock_module.check_mode = False
        mock_ansible_module_cls.return_value = mock_module

        mock_api = MagicMock()
        mock_api.state = "present"
        mock_api.name = "new_role"
        mock_api.based_on = None
        mock_api.current = ROLE_GET_RESPONSE_404
        mock_role_api_cls.return_value = mock_api

        run_module()

        mock_module.fail_json.assert_called_once()
        fail_kwargs = mock_module.fail_json.call_args[1]
        assert "based_on" in fail_kwargs["msg"]
        mock_api.create.assert_not_called()

    @patch("ansible_collections.checkmk.general.plugins.modules.role.RoleAPI")
    @patch("ansible_collections.checkmk.general.plugins.modules.role.AnsibleModule")
    def test_absent_deletes_custom_role(
        self, mock_ansible_module_cls, mock_role_api_cls
    ):
        mock_module = MagicMock()
        mock_module.params = _make_module_params(name="test_role", state="absent")
        mock_module.check_mode = False
        mock_ansible_module_cls.return_value = mock_module

        mock_api = MagicMock()
        mock_api.state = "absent"
        mock_api.name = "test_role"
        mock_api.current = ROLE_GET_RESPONSE_200
        mock_api.delete.return_value = ROLE_DELETE_RESPONSE
        mock_role_api_cls.return_value = mock_api

        run_module()

        mock_api.delete.assert_called_once()
        mock_module.exit_json.assert_called_once()

    @patch("ansible_collections.checkmk.general.plugins.modules.role.RoleAPI")
    @patch("ansible_collections.checkmk.general.plugins.modules.role.AnsibleModule")
    def test_absent_fails_for_builtin_role(
        self, mock_ansible_module_cls, mock_role_api_cls
    ):
        mock_module = MagicMock()
        mock_module.params = _make_module_params(name="admin", state="absent")
        mock_module.check_mode = False
        mock_ansible_module_cls.return_value = mock_module

        mock_api = MagicMock()
        mock_api.state = "absent"
        mock_api.name = "admin"
        mock_api.current = ROLE_GET_RESPONSE_200
        mock_role_api_cls.return_value = mock_api

        run_module()

        mock_module.fail_json.assert_called_once()
        fail_kwargs = mock_module.fail_json.call_args[1]
        assert "cannot be deleted" in fail_kwargs["msg"]
        mock_api.delete.assert_not_called()

    @patch("ansible_collections.checkmk.general.plugins.modules.role.RoleAPI")
    @patch("ansible_collections.checkmk.general.plugins.modules.role.AnsibleModule")
    def test_absent_no_change_when_already_absent(
        self, mock_ansible_module_cls, mock_role_api_cls
    ):
        mock_module = MagicMock()
        mock_module.params = _make_module_params(name="gone_role", state="absent")
        mock_module.check_mode = False
        mock_ansible_module_cls.return_value = mock_module

        mock_api = MagicMock()
        mock_api.state = "absent"
        mock_api.name = "gone_role"
        mock_api.current = ROLE_GET_RESPONSE_404
        mock_role_api_cls.return_value = mock_api

        run_module()

        mock_api.delete.assert_not_called()
        mock_module.exit_json.assert_called_once()
        call_kwargs = mock_module.exit_json.call_args[1]
        assert call_kwargs["changed"] is False

    @patch("ansible_collections.checkmk.general.plugins.modules.role.RoleAPI")
    @patch("ansible_collections.checkmk.general.plugins.modules.role.AnsibleModule")
    def test_check_mode_create(self, mock_ansible_module_cls, mock_role_api_cls):
        mock_module = MagicMock()
        mock_module.params = _make_module_params(
            name="new_role", title="New", based_on="user"
        )
        mock_module.check_mode = True
        mock_ansible_module_cls.return_value = mock_module

        mock_api = MagicMock()
        mock_api.state = "present"
        mock_api.name = "new_role"
        mock_api.based_on = "user"
        mock_api.current = ROLE_GET_RESPONSE_404
        mock_role_api_cls.return_value = mock_api

        run_module()

        mock_api.create.assert_not_called()
        mock_module.exit_json.assert_called_once()
        call_kwargs = mock_module.exit_json.call_args[1]
        assert call_kwargs["changed"] is True
        assert call_kwargs["msg"] == "Role would be created."

    @patch("ansible_collections.checkmk.general.plugins.modules.role.RoleAPI")
    @patch("ansible_collections.checkmk.general.plugins.modules.role.AnsibleModule")
    def test_check_mode_update(self, mock_ansible_module_cls, mock_role_api_cls):
        mock_module = MagicMock()
        mock_module.params = _make_module_params(name="test_role", title="Changed")
        mock_module.check_mode = True
        mock_ansible_module_cls.return_value = mock_module

        mock_api = MagicMock()
        mock_api.state = "present"
        mock_api.name = "test_role"
        mock_api.current = ROLE_GET_RESPONSE_200
        mock_api._needs_update.return_value = True
        mock_role_api_cls.return_value = mock_api

        run_module()

        mock_api.edit.assert_not_called()
        mock_module.exit_json.assert_called_once()
        call_kwargs = mock_module.exit_json.call_args[1]
        assert call_kwargs["changed"] is True
        assert call_kwargs["msg"] == "Role would be updated."

    @patch("ansible_collections.checkmk.general.plugins.modules.role.RoleAPI")
    @patch("ansible_collections.checkmk.general.plugins.modules.role.AnsibleModule")
    def test_invalid_permission_value_fails(
        self, mock_ansible_module_cls, mock_role_api_cls
    ):
        mock_module = MagicMock()
        mock_module.params = _make_module_params(permissions={"wato.edit": "maybe"})
        mock_module.check_mode = False
        mock_ansible_module_cls.return_value = mock_module

        run_module()

        mock_module.fail_json.assert_called_once()
        fail_kwargs = mock_module.fail_json.call_args[1]
        assert "maybe" in fail_kwargs["msg"]
        assert "wato.edit" in fail_kwargs["msg"]

    @patch("ansible_collections.checkmk.general.plugins.modules.role.RoleAPI")
    @patch("ansible_collections.checkmk.general.plugins.modules.role.AnsibleModule")
    def test_default_permission_on_builtin_role_fails(
        self, mock_ansible_module_cls, mock_role_api_cls
    ):
        mock_module = MagicMock()
        mock_module.params = _make_module_params(
            name="guest",
            permissions={"general.csv_export": "default"},
        )
        mock_module.check_mode = False
        mock_ansible_module_cls.return_value = mock_module

        run_module()

        mock_module.fail_json.assert_called_once()
        fail_kwargs = mock_module.fail_json.call_args[1]
        assert "default" in fail_kwargs["msg"]
        assert "guest" in fail_kwargs["msg"]

    @patch("ansible_collections.checkmk.general.plugins.modules.role.RoleAPI")
    @patch("ansible_collections.checkmk.general.plugins.modules.role.AnsibleModule")
    def test_check_mode_delete(self, mock_ansible_module_cls, mock_role_api_cls):
        mock_module = MagicMock()
        mock_module.params = _make_module_params(name="test_role", state="absent")
        mock_module.check_mode = True
        mock_ansible_module_cls.return_value = mock_module

        mock_api = MagicMock()
        mock_api.state = "absent"
        mock_api.name = "test_role"
        mock_api.current = ROLE_GET_RESPONSE_200
        mock_role_api_cls.return_value = mock_api

        run_module()

        mock_api.delete.assert_not_called()
        mock_module.exit_json.assert_called_once()
        call_kwargs = mock_module.exit_json.call_args[1]
        assert call_kwargs["changed"] is True
        assert call_kwargs["msg"] == "Role would be deleted."

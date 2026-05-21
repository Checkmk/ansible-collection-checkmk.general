# Copyright: (c) 2026, Robin Gierse <robin.gierse@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from ansible.inventory.data import InventoryData
from ansible.plugins.loader import inventory_loader

# Minimal required options that are not under test in a given case.
_REQUIRED = {
    "plugin": "checkmk.general.checkmk",
    "server_url": "http://dummy/",
    "site": "dummy",
}


@pytest.fixture
def plugin():
    """Return a properly initialized InventoryModule instance.

    Using inventory_loader.get() (not direct class instantiation) is required so
    that Ansible's _load_config_defs() is called on the class.  Without it,
    set_options() has no option definitions and env: / vars: entries are ignored.
    """
    plugin_cls = inventory_loader.get("checkmk.general.checkmk", class_only=True)
    p = plugin_cls()
    p.inventory = InventoryData()
    return p


# ---------------------------------------------------------------------------
# Environment variable resolution  (CHECKMK_VAR_*)
# ---------------------------------------------------------------------------


class TestEnvVarResolution:
    """CHECKMK_VAR_* environment variables must be picked up by get_option()."""

    def test_server_url(self, plugin, monkeypatch):
        monkeypatch.setenv("CHECKMK_VAR_SERVER_URL", "http://envserver/")
        monkeypatch.setenv("CHECKMK_VAR_SITE", "envsite")  # also required
        plugin.set_options(direct={"plugin": "checkmk.general.checkmk"})
        assert plugin.get_option("server_url") == "http://envserver/"

    def test_site(self, plugin, monkeypatch):
        monkeypatch.setenv(
            "CHECKMK_VAR_SERVER_URL", "http://envserver/"
        )  # also required
        monkeypatch.setenv("CHECKMK_VAR_SITE", "envsite")
        plugin.set_options(direct={"plugin": "checkmk.general.checkmk"})
        assert plugin.get_option("site") == "envsite"

    def test_api_user(self, plugin, monkeypatch):
        monkeypatch.setenv("CHECKMK_VAR_API_USER", "envuser")
        plugin.set_options(direct=dict(_REQUIRED))
        assert plugin.get_option("api_user") == "envuser"

    def test_api_secret(self, plugin, monkeypatch):
        monkeypatch.setenv("CHECKMK_VAR_API_SECRET", "envsecret")
        plugin.set_options(direct=dict(_REQUIRED))
        assert plugin.get_option("api_secret") == "envsecret"

    def test_validate_certs_false(self, plugin, monkeypatch):
        monkeypatch.setenv("CHECKMK_VAR_VALIDATE_CERTS", "false")
        plugin.set_options(direct=dict(_REQUIRED))
        assert plugin.get_option("validate_certs") is False

    def test_api_auth_type(self, plugin, monkeypatch):
        monkeypatch.setenv("CHECKMK_VAR_API_AUTH_TYPE", "basic")
        plugin.set_options(direct=dict(_REQUIRED))
        assert plugin.get_option("api_auth_type") == "basic"

    def test_direct_overrides_env(self, plugin, monkeypatch):
        """A value given directly in the inventory file beats an env var."""
        monkeypatch.setenv("CHECKMK_VAR_API_USER", "envuser")
        plugin.set_options(direct=dict(_REQUIRED, api_user="directuser"))
        assert plugin.get_option("api_user") == "directuser"


# ---------------------------------------------------------------------------
# Ansible variable resolution  (checkmk_var_*)
# ---------------------------------------------------------------------------


class TestAnsibleVarResolution:
    """checkmk_var_* Ansible variables must be picked up by get_option().

    This covers credential injection where credentials arrive as host/group vars
    at runtime rather than being written into the inventory file.
    """

    def test_server_url(self, plugin):
        plugin.set_options(
            var_options={
                "checkmk_var_server_url": "http://varserver/",
                "checkmk_var_site": "varsite",
            },
            direct={"plugin": "checkmk.general.checkmk"},
        )
        assert plugin.get_option("server_url") == "http://varserver/"

    def test_site(self, plugin):
        plugin.set_options(
            var_options={
                "checkmk_var_server_url": "http://varserver/",
                "checkmk_var_site": "varsite",
            },
            direct={"plugin": "checkmk.general.checkmk"},
        )
        assert plugin.get_option("site") == "varsite"

    def test_api_user(self, plugin):
        plugin.set_options(
            var_options={"checkmk_var_api_user": "varuser"},
            direct=dict(_REQUIRED),
        )
        assert plugin.get_option("api_user") == "varuser"

    def test_api_secret(self, plugin):
        plugin.set_options(
            var_options={"checkmk_var_api_secret": "varsecret"},
            direct=dict(_REQUIRED),
        )
        assert plugin.get_option("api_secret") == "varsecret"

    def test_direct_overrides_vars(self, plugin):
        """A value given directly in the inventory file beats an Ansible variable."""
        plugin.set_options(
            var_options={"checkmk_var_api_user": "varuser"},
            direct=dict(_REQUIRED, api_user="directuser"),
        )
        assert plugin.get_option("api_user") == "directuser"

    def test_vars_override_env(self, plugin, monkeypatch):
        """Ansible variables take precedence over environment variables.

        Resolution order: direct > vars > env > ini > default.
        """
        monkeypatch.setenv("CHECKMK_VAR_API_USER", "envuser")
        plugin.set_options(
            var_options={"checkmk_var_api_user": "varuser"},
            direct=dict(_REQUIRED),
        )
        assert plugin.get_option("api_user") == "varuser"


# ---------------------------------------------------------------------------
# ansible.cfg resolution  ([checkmk_lookup] section)
# ---------------------------------------------------------------------------


class TestIniResolution:
    """Keys under [checkmk_lookup] in ansible.cfg must be picked up by get_option()."""

    def test_api_user_from_ini(self, tmp_path, monkeypatch):
        cfg = tmp_path / "ansible.cfg"
        cfg.write_text("[checkmk_lookup]\napi_user = iniuser\n")
        monkeypatch.setenv("ANSIBLE_CONFIG", str(cfg))

        # Force Ansible to re-read its config so ANSIBLE_CONFIG takes effect.
        from ansible.config.manager import ConfigManager
        import ansible.constants as C

        monkeypatch.setattr(C, "config", ConfigManager())

        # Build the plugin AFTER swapping the config manager so its option
        # definitions resolve against the new manager.
        plugin_cls = inventory_loader.get("checkmk.general.checkmk", class_only=True)
        p = plugin_cls()
        p.inventory = InventoryData()
        p.set_options(direct=dict(_REQUIRED))
        assert p.get_option("api_user") == "iniuser"

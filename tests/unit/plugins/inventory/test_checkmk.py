# Copyright: (c) 2024, Max Sickora <max.sickora@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json

import pytest
from ansible.errors import AnsibleError
from ansible.inventory.data import InventoryData
from ansible_collections.checkmk.general.plugins.inventory.checkmk import (
    InventoryModule,
)
from ansible_collections.checkmk.general.plugins.module_utils.lookup_api import (
    CheckMKLookupAPI,
)


@pytest.fixture(scope="module")
def inventory():
    r = InventoryModule()
    r.inventory = InventoryData()
    return r


def test_verify_file(tmp_path, inventory):
    file = tmp_path / "checkmk.yml"
    file.touch()
    assert inventory.verify_file(str(file)) is True


def test_verify_file_bad_config(inventory):
    assert inventory.verify_file("wrongname.yml") is False


def get_option(opts):
    def fn(option):
        default = opts.get("default", False)
        return opts.get(option, default)

    return fn


def test_populate_allgroups(inventory, mocker):
    inventory.plugin = "checkmk.general.checkmk"
    inventory.server_url = "http://127.0.0.1/"
    inventory.site = "stable"
    inventory.user = "cmkadmin"
    inventory.secret = "cmk"
    inventory.validate_certs = False
    inventory.groupsources = ["hosttags", "sites"]

    opts = {
        "server_url": inventory.server_url,
        "site": inventory.site,
        "api_user": inventory.user,
        "api_secret": inventory.secret,
        "validate_certs": inventory.validate_certs,
    }

    inventory.get_option = mocker.MagicMock(side_effect=get_option(opts))

    api = CheckMKLookupAPI(
        site_url=inventory.get_option("server_url")
        + "/"
        + inventory.get_option("site"),
        api_user=inventory.get_option("api_user"),
        api_secret=inventory.get_option("api_secret"),
        validate_certs=inventory.get_option("validate_certs"),
    )

    inventory.hosttaggroups = inventory._get_taggroups(api)
    inventory.tags = [("tag_" + tag.get("id")) for tag in inventory.hosttaggroups]
    inventory.sites = inventory._get_sites(api)
    inventory.hosts = inventory._get_hosts(api)

    inventory._generate_groups()
    inventory._populate()

    # Test if testhost2 exists
    assert inventory.inventory.get_host("testhost2")

    # Test of sites exist as groups
    for site in ["site_maintestsite", "site_remotetestsite"]:
        assert site in inventory.inventory.groups

    # Test of some tags exist as groups
    for site in [
        "tag_criticality_offline",
        "tag_networking_lan",
        "tag_piggyback_auto_piggyback",
        "tag_snmp_ds_snmp_v2",
        "tag_agent_cmk_agent",
    ]:
        assert site in inventory.inventory.groups

    # Test if testhost1,4,5 are in group tag_criticality_test
    tag_criticality_test_group = inventory.inventory.groups["tag_criticality_test"]
    host_testhost1 = inventory.inventory.get_host("testhost1")
    host_testhost4 = inventory.inventory.get_host("testhost4")
    host_testhost5 = inventory.inventory.get_host("testhost5")
    assert tag_criticality_test_group.hosts == [
        host_testhost1,
        host_testhost4,
        host_testhost5,
    ]

    # Test if testhost3 is in group tag_testtaggroup_None (id = NoneType)
    tag_testtaggroup_none_group = inventory.inventory.groups["tag_testtaggroup_None"]
    host_testhost3 = inventory.inventory.get_host("testhost3")
    assert tag_testtaggroup_none_group.hosts == [host_testhost3]

    # Test if testhost1 is in folder /main
    assert host_testhost1.get_vars()["folder"] == "/main"

    # Test if testhost4 and 5 are not in group site_maintestsite, tag_lonelytag_lonelytag or ungrouped
    for node in ["testhost4", "testhost5"]:
        assert node not in inventory.inventory.get_groups_dict()["site_maintestsite"]
        assert node not in inventory.inventory.get_groups_dict()["ungrouped"]
        assert (
            node not in inventory.inventory.get_groups_dict()["tag_lonelytag_lonelytag"]
        )

    # Test if testhost6 is in group tag_lonelytag_lonelytag
    tag_lonelytag_lonelytag_group = inventory.inventory.groups[
        "tag_lonelytag_lonelytag"
    ]
    host_testhost6 = inventory.inventory.get_host("testhost6")
    assert tag_lonelytag_lonelytag_group.hosts == [host_testhost6]


def test_populate_nogroups(inventory, mocker):
    inventory.plugin = "checkmk.general.checkmk"
    inventory.server_url = "http://127.0.0.1/"
    inventory.site = "stable"
    inventory.user = "cmkadmin"
    inventory.secret = "cmk"
    inventory.validate_certs = False
    inventory.groupsources = []

    opts = {
        "server_url": inventory.server_url,
        "site": inventory.site,
        "api_user": inventory.user,
        "api_secret": inventory.secret,
        "validate_certs": inventory.validate_certs,
    }

    inventory.get_option = mocker.MagicMock(side_effect=get_option(opts))

    api = CheckMKLookupAPI(
        site_url=inventory.get_option("server_url")
        + "/"
        + inventory.get_option("site"),
        api_user=inventory.get_option("api_user"),
        api_secret=inventory.get_option("api_secret"),
        validate_certs=inventory.get_option("validate_certs"),
    )

    inventory.hosttaggroups = inventory._get_taggroups(api)
    inventory.tags = [("tag_" + tag.get("id")) for tag in inventory.hosttaggroups]
    inventory.sites = inventory._get_sites(api)
    inventory.hosts = inventory._get_hosts(api)

    inventory._generate_groups()
    inventory._populate()

    # Test if testhost1 exists
    assert inventory.inventory.get_host("testhost1")

    # Test if sites don't exist as groups
    for site in ["site_maintestsite", "site_remotetestsite"]:
        assert site not in inventory.inventory.groups

    # Test of some tags don't exist as groups
    for tag in [
        "tag_criticality_offline",
        "tag_networking_lan",
        "tag_piggyback_auto_piggyback",
        "tag_snmp_ds_snmp_v2",
        "tag_agent_cmk_agent",
    ]:
        assert tag not in inventory.inventory.groups


@pytest.fixture()
def fresh_inventory():
    r = InventoryModule()
    r.inventory = InventoryData()
    return r


@pytest.fixture()
def api():
    return CheckMKLookupAPI(
        site_url="http://127.0.0.1/stable",
        api_user="cmkadmin",
        api_secret="cmk",
        validate_certs=False,
    )


def _prepare_tags_and_sites(inventory, api):
    inventory.hosttaggroups = inventory._get_taggroups(api)
    inventory.tags = [("tag_" + tag.get("id")) for tag in inventory.hosttaggroups]
    inventory.sites = inventory._get_sites(api)


def _raw_host(host_id, tags=None, folder="/main"):
    effective_attributes = {"site": "maintestsite"}
    effective_attributes.update(tags or {})
    return {
        "id": host_id,
        "extensions": {
            "title": host_id,
            "attributes": {"ipaddress": "192.168.1.1"},
            "folder": folder,
            "effective_attributes": effective_attributes,
        },
    }


def test_is_excluded(fresh_inventory):
    fresh_inventory.exclude_tags = ["tag_criticality_test"]
    assert (
        fresh_inventory._is_excluded({"id": "h1", "tags": {"tag_criticality": "test"}})
        is True
    )
    assert (
        fresh_inventory._is_excluded({"id": "h2", "tags": {"tag_criticality": "prod"}})
        is False
    )
    assert (
        fresh_inventory._is_excluded({"id": "h3", "tags": {"tag_criticality": None}})
        is False
    )


def test_exclude_tags(fresh_inventory, api):
    _prepare_tags_and_sites(fresh_inventory, api)
    fresh_inventory.exclude_tags = ["tag_criticality_test"]

    host_ids = [host["id"] for host in fresh_inventory._get_hosts(api)]

    # testhost1, testhost4 and testhost5 have tag_criticality test
    for excluded in ["testhost1", "testhost4", "testhost5"]:
        assert excluded not in host_ids
    for included in ["testhost2", "testhost3", "testhost6"]:
        assert included in host_ids


def test_domain_map(fresh_inventory, api):
    _prepare_tags_and_sites(fresh_inventory, api)
    fresh_inventory.domain_map = {"tag_criticality_prod": ".example.com"}

    host_ids = [host["id"] for host in fresh_inventory._get_hosts(api)]

    # testhost2 has tag_criticality prod and gets the suffix appended
    assert "testhost2.example.com" in host_ids
    assert "testhost2" not in host_ids
    # testhost3 has tag_criticality critical and keeps its name
    assert "testhost3" in host_ids


def test_domain_map_first_match_wins(fresh_inventory):
    fresh_inventory.domain_map = {
        "tag_criticality_prod": ".example.com",
        "tag_networking_lan": ".lan.example.com",
    }
    host_tags = {"tag_networking": "lan", "tag_criticality": "prod"}
    assert fresh_inventory._get_domain_suffix(host_tags) == ".example.com"


def test_lowercase_hosts(fresh_inventory):
    fresh_inventory.tags = ["tag_criticality"]
    fresh_inventory.lowercase_hosts = True

    hosts = fresh_inventory._parse_hosts([_raw_host("TestHost1")])

    assert hosts[0]["id"] == "testhost1"


def test_folder_matches(fresh_inventory):
    fresh_inventory.folder = "/main"
    assert fresh_inventory._folder_matches("/main") is True
    assert fresh_inventory._folder_matches("/main/sub") is False
    assert fresh_inventory._folder_matches("/other") is False

    # Trailing slashes and the leading slash are normalized away
    fresh_inventory.folder = "main/"
    assert fresh_inventory._folder_matches("/main") is True

    fresh_inventory.recursive = True
    fresh_inventory.folder = "/main"
    assert fresh_inventory._folder_matches("/main") is True
    assert fresh_inventory._folder_matches("/main/sub") is True
    assert fresh_inventory._folder_matches("/mainother") is False

    # The root folder matches everything when recursive
    fresh_inventory.folder = "/"
    assert fresh_inventory._folder_matches("/") is True
    assert fresh_inventory._folder_matches("/main/sub") is True


def test_get_hosts_folder(fresh_inventory, mocker):
    fresh_inventory.tags = []
    fresh_inventory.folder = "/main"

    api = mocker.MagicMock()
    api.get.return_value = json.dumps(
        {
            "value": [
                _raw_host("host_a", folder="/main"),
                _raw_host("host_b", folder="/main/sub"),
                _raw_host("host_c", folder="/other"),
            ]
        }
    )

    host_ids = [host["id"] for host in fresh_inventory._get_hosts(api)]

    # Only hosts directly in the folder are returned
    assert host_ids == ["host_a"]
    api.get.assert_called_once_with(
        "/domain-types/host_config/collections/all",
        {"effective_attributes": True},
    )


def test_get_hosts_folder_recursive(fresh_inventory, mocker):
    fresh_inventory.tags = []
    fresh_inventory.folder = "/main"
    fresh_inventory.recursive = True

    api = mocker.MagicMock()
    api.get.return_value = json.dumps(
        {
            "value": [
                _raw_host("host_a", folder="/main"),
                _raw_host("host_b", folder="/main/sub"),
                _raw_host("host_c", folder="/other"),
            ]
        }
    )

    host_ids = [host["id"] for host in fresh_inventory._get_hosts(api)]

    # Hosts in the folder and its subfolders are returned
    assert host_ids == ["host_a", "host_b"]


def test_domain_map_with_lowercase_hosts(fresh_inventory):
    fresh_inventory.tags = ["tag_criticality"]
    fresh_inventory.domain_map = {"tag_criticality_prod": ".Example.COM"}
    fresh_inventory.lowercase_hosts = True

    hosts = fresh_inventory._parse_hosts(
        [_raw_host("TestHost1", {"tag_criticality": "prod"})]
    )

    # The suffix is appended first, then the whole hostname is lowercased
    assert hosts[0]["id"] == "testhost1.example.com"


def test_exclude_tags_with_domain_map(fresh_inventory):
    fresh_inventory.tags = ["tag_criticality"]
    fresh_inventory.exclude_tags = ["tag_criticality_test"]
    fresh_inventory.domain_map = {
        "tag_criticality_test": ".test.example.com",
        "tag_criticality_prod": ".example.com",
    }

    hosts = fresh_inventory._parse_hosts(
        [
            _raw_host("host_a", {"tag_criticality": "test"}),
            _raw_host("host_b", {"tag_criticality": "prod"}),
        ]
    )

    # host_a is excluded before any renaming, host_b is renamed
    assert [host["id"] for host in hosts] == ["host_b.example.com"]


def test_recursive_without_folder(fresh_inventory, mocker):
    fresh_inventory.tags = []
    fresh_inventory.recursive = True

    api = mocker.MagicMock()
    api.get.return_value = json.dumps({"value": [_raw_host("host_a")]})

    host_ids = [host["id"] for host in fresh_inventory._get_hosts(api)]

    # Without a folder, recursive has no effect and all hosts are fetched
    assert host_ids == ["host_a"]
    api.get.assert_called_once_with(
        "/domain-types/host_config/collections/all",
        {"effective_attributes": True},
    )


def test_get_hosts_error(fresh_inventory, mocker):
    fresh_inventory.tags = []

    api = mocker.MagicMock()
    api.get.return_value = json.dumps(
        {"code": 404, "msg": "Not Found", "url": "http://localhost"}
    )

    with pytest.raises(AnsibleError, match="404"):
        fresh_inventory._get_hosts(api)


def test_populate_with_renamed_hosts(fresh_inventory, api):
    _prepare_tags_and_sites(fresh_inventory, api)
    fresh_inventory.groupsources = ["hosttags", "sites"]
    fresh_inventory.domain_map = {"tag_criticality_test": ".test.example.com"}

    fresh_inventory.hosts = fresh_inventory._get_hosts(api)
    fresh_inventory._generate_groups()
    fresh_inventory._populate()

    # Renamed hosts exist under their new name only
    renamed = fresh_inventory.inventory.get_host("testhost1.test.example.com")
    assert renamed
    assert fresh_inventory.inventory.get_host("testhost1") is None

    # Renamed hosts still end up in their tag and site groups
    groups_dict = fresh_inventory.inventory.get_groups_dict()
    assert "testhost1.test.example.com" in groups_dict["tag_criticality_test"]
    assert "testhost1.test.example.com" in groups_dict["site_maintestsite"]

    # Hosts without a matching tag keep their name and groups
    assert "testhost2" in groups_dict["tag_criticality_prod"]

# Copyright: (c) 2024, Max Sickora <max.sickora@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest

from ansible_collections.checkmk.general.plugins.inventory.checkmk import (
    InventoryModule,
)
from ansible_collections.checkmk.general.plugins.module_utils.lookup_api import (
    CheckMKLookupAPI,
)
from ansible.inventory.data import InventoryData


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
        "automation_user": inventory.user,
        "automation_secret": inventory.secret,
        "validate_certs": inventory.validate_certs,
    }

    inventory.get_option = mocker.MagicMock(side_effect=get_option(opts))

    api = CheckMKLookupAPI(
        site_url=inventory.get_option("server_url")
        + "/"
        + inventory.get_option("site"),
        user=inventory.get_option("automation_user"),
        secret=inventory.get_option("automation_secret"),
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

    # Test if testhost1 is in folder /main
    assert host_testhost1.get_vars()["folder"] == "/main"

    # Test if testhost4 and 5 are not in group site_maintestsite or ungrouped
    for node in ["testhost4", "testhost5"]:
        assert node not in inventory.inventory.get_groups_dict()["site_maintestsite"]
        assert node not in inventory.inventory.get_groups_dict()["ungrouped"]


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
        "automation_user": inventory.user,
        "automation_secret": inventory.secret,
        "validate_certs": inventory.validate_certs,
    }

    inventory.get_option = mocker.MagicMock(side_effect=get_option(opts))

    api = CheckMKLookupAPI(
        site_url=inventory.get_option("server_url")
        + "/"
        + inventory.get_option("site"),
        user=inventory.get_option("automation_user"),
        secret=inventory.get_option("automation_secret"),
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

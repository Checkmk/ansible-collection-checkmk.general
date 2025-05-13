# Copyright: (c) 2024, Max Sickora <max.sickora@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
    name: checkmk
    author: Max Sickora (@max-checkmk)
    short_description: Dynamic Inventory Source or Checkmk
    description:
        - Get hosts from any checkmk site.
        - Generate groups based on tag groups or sites in Checkmk.

    extends_documentation_fragment: [checkmk.general.common]

    options:
        plugin:
            description: Name of the plugin. Should always be C(checkmk.general.checkmk).
            type: string
            required: true
            choices: ['checkmk.general.checkmk']
        groupsources:
            description:
              - List of sources for grouping
              - Possible sources are C(sites) and C(hosttags)
            type: list
            elements: str
            required: false
        want_ipv4:
            description: Update ansible_host variable with ip address from Checkmk
            type: boolean
            required: false
"""

EXAMPLES = """
# To get started, you need to create a file called `checkmk.yml`, which contains
# one of the example blocks below and use it as your inventory source.
# E.g., with `ansible-inventory -i checkmk.yml --graph`.

# Group all hosts based on both tag groups and sites:
plugin: checkmk.general.checkmk
server_url: "http://hostname/"
site: "sitename"
automation_user: "cmkadmin"
automation_secret: "******"
validate_certs: False
groupsources: ["hosttags", "sites"]
want_ipv4: False
"""

import json
import re

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.inventory import BaseInventoryPlugin
from ansible.utils.display import Display
from ansible_collections.checkmk.general.plugins.module_utils.lookup_api import (
    CheckMKLookupAPI,
)

display = Display()


class InventoryModule(BaseInventoryPlugin):
    """Host inventory parser for ansible using Checkmk as source."""

    NAME = "checkmk.general.checkmk"

    def __init__(self):
        super(InventoryModule, self).__init__()

        self.plugin = None
        self.server_url = None
        self.site = None
        self.user = None
        self.secret = None
        self.validate_certs = None
        self.want_ipv4 = None
        self.groupsources = []
        self.hosttaggroups = []
        self.tags = []
        self.groups = []
        self.hosts = []
        self.sites = []

    def convertname(self, name):
        """Removes empty space and changes bad chars to _"""
        regex = r"[^A-Za-z0-9\_]"
        return re.sub(regex, "_", name.replace(" ", ""))

    def verify_file(self, path):
        """return true/false if this is possibly a valid file for this plugin to consume"""
        valid = False
        if super(InventoryModule, self).verify_file(path):
            # base class verifies that file exists and is readable by current user
            if path.endswith(("checkmk.yaml", "checkmk.yml")):
                self.display.vvv("Inventory source file verified")
                valid = True
            else:
                self.display.vvv(
                    "Inventory source file doesn't end with 'checkmk.yaml' or 'checkmk.yml'"
                )
        return valid

    def _generate_groups(self):
        if self.groupsources:
            if "hosttags" in self.groupsources:
                hosttags = []
                for hosttaggroups in self.hosttaggroups:
                    if len(hosttaggroups.get("tags")) > 1:
                        hosttags += [
                            (
                                "tag_" + hosttaggroups.get("id") + "_" + tag.get("id")
                                if tag.get("id")
                                else "tag_" + hosttaggroups.get("id") + "_None"
                            )
                            for tag in (hosttaggroups.get("tags"))
                        ]
                    else:
                        # If the tag group has only one choice, we have to generate TWO groups,
                        # one for hosts that have this tag set and one for hosts that have it unset
                        hosttags.append("tag_" + hosttaggroups.get("id") + "_None")
                        hosttags.append(
                            "tag_"
                            + hosttaggroups.get("id")
                            + "_"
                            + hosttaggroups.get("tags")[0].get("id")
                        )
                self.groups.extend(hosttags)

            if "sites" in self.groupsources:
                sites = ["site_" + site.get("id") for site in self.sites]
                self.groups.extend(sites)

    def parse(self, inventory, loader, path, cache=False):
        super(InventoryModule, self).parse(inventory, loader, path, cache)

        config = self._read_config_data(path)

        try:
            self.plugin = self.get_option("plugin")
            self.server_url = self.get_option("server_url")
            self.site = self.get_option("site")
            self.user = self.get_option("automation_user")
            self.secret = self.get_option("automation_secret")
            self.validate_certs = self.get_option("validate_certs")
            self.want_ipv4 = self.get_option("want_ipv4")
            self.groupsources = self.get_option("groupsources")
        except Exception as e:
            raise AnsibleParserError("All correct options required: {}".format(e))

        api = CheckMKLookupAPI(
            site_url=self.get_option("server_url") + "/" + self.get_option("site"),
            user=self.get_option("automation_user"),
            secret=self.get_option("automation_secret"),
            validate_certs=self.get_option("validate_certs"),
        )

        self.hosttaggroups = self._get_taggroups(api)
        self.tags = [("tag_" + tag.get("id")) for tag in self.hosttaggroups]
        self.sites = self._get_sites(api)

        self.hosts = self._get_hosts(api)

        self._generate_groups()

        self._populate()

    def _populate(self):
        """Return the hosts and groups"""

        for group in self.groups:
            self.inventory.add_group(self.convertname(group))

        for host in self.hosts:
            self.inventory.add_host(host["id"])
            self.inventory.set_variable(host["id"], "ipaddress", host["ipaddress"])
            self.inventory.set_variable(host["id"], "folder", host["folder"])
            if self.want_ipv4:
                self.inventory.set_variable(host["id"], "ansible_host", host["ipaddress"])

        if self.groupsources:
            if "hosttags" in self.groupsources:
                for host in self.hosts:
                    for tag in self.tags:
                        if host.get("tags").get(tag):
                            self.inventory.add_child(
                                tag + "_" + self.convertname(host.get("tags").get(tag)),
                                host.get("id"),
                            )
                        else:
                            self.inventory.add_child(tag + "_None", host.get("id"))
            if "sites" in self.groupsources:
                for host in self.hosts:
                    self.inventory.add_child(
                        "site_" + self.convertname(host.get("site")), host.get("id")
                    )

    def _get_hosts(self, api):
        response = json.loads(
            api.get(
                "/domain-types/host_config/collections/all",
                {"effective_attributes": True},
            )
        )
        if "code" in response:
            raise AnsibleError(
                "Received error for %s - %s: %s"
                % (
                    response.get("url", ""),
                    response.get("code", ""),
                    response.get("msg", ""),
                )
            )

        hosts = [
            {
                "id": host.get("id"),
                "title": host.get("extensions").get("title"),
                "ipaddress": host.get("extensions").get("attributes").get("ipaddress"),
                "folder": host.get("extensions").get("folder"),
                "site": host.get("extensions").get("effective_attributes").get("site"),
                "tags": {
                    taggroup: tag
                    for taggroup, tag in host.get("extensions")
                    .get("effective_attributes")
                    .items()
                    if taggroup in self.tags
                },
            }
            for host in (response.get("value"))
        ]

        return hosts

    def _get_taggroups(self, api):
        response = json.loads(api.get("/domain-types/host_tag_group/collections/all"))
        if "code" in response:
            raise AnsibleError(
                "Received error for %s - %s: %s"
                % (
                    response.get("url", ""),
                    response.get("code", ""),
                    response.get("msg", ""),
                )
            )

        hosttaggroups = [
            {
                "id": hosttaggroup.get("id"),
                "tags": hosttaggroup.get("extensions").get("tags"),
            }
            for hosttaggroup in (response.get("value"))
        ]

        return hosttaggroups

    def _get_sites(self, api):
        response = json.loads(api.get("/domain-types/site_connection/collections/all"))
        if "code" in response:
            raise AnsibleError(
                "Received error for %s - %s: %s"
                % (
                    response.get("url", ""),
                    response.get("code", ""),
                    response.get("msg", ""),
                )
            )

        sites = [
            {"id": site.get("id"), "customer": site.get("extensions").get("customer")}
            for site in (response.get("value"))
        ]

        return sites

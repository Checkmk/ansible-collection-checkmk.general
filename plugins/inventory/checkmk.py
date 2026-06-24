# Copyright: (c) 2024, Max Sickora <max.sickora@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
    name: checkmk
    short_description: Dynamic Inventory Source for Checkmk
    description:
        - Get hosts from any Checkmk site.
        - Generate groups based on tag groups or sites in Checkmk.

    extends_documentation_fragment: [checkmk.general.common_lookup]

    options:
        plugin:
            description: Name of the plugin. Should always be C(checkmk.general.checkmk).
            type: str
            required: true
            choices: ['checkmk.general.checkmk']
        groupsources:
            description:
              - List of sources for grouping.
              - Possible sources are C(sites) and C(hosttags).
            type: list
            elements: str
            required: false
        want_ipv4:
            description: Update ansible_host variable with ip address from Checkmk.
            type: bool
            required: false
        folder:
            description:
              - Restrict hosts to a specific folder path in Checkmk.
              - Given as a regular path, e.g. C(/linux/production).
              - Unless C(recursive) is enabled, only hosts directly in the given folder are returned.
              - All hosts are always fetched from the site and filtered on the client
                side, so this does not reduce the amount of data retrieved from Checkmk.
            required: false
            type: str
            env:
              - name: CHECKMK_VAR_FOLDER
        recursive:
            description:
              - If set to C(true) and a C(folder) is defined, all subfolders are included recursively.
              - Has no effect without C(folder).
            required: false
            default: false
            type: bool
            env:
              - name: CHECKMK_VAR_RECURSIVE
        exclude_tags:
            description:
              - List of host tags to exclude from the inventory.
              - Any host that has at least one of the given tags set will be excluded.
              - Tags must be given in the full Checkmk format C(tag_<group>_<value>),
                e.g. C(tag_criticality_test) or C(tag_agent_cmk-agent).
            required: false
            type: list
            elements: str
            env:
              - name: CHECKMK_VAR_EXCLUDE_TAGS
        lowercase_hosts:
            description:
              - If set to C(true), all hostnames will be converted to lowercase in the inventory.
            required: false
            default: false
            type: bool
            env:
              - name: CHECKMK_VAR_LOWERCASE_HOSTS
        domain_map:
            description:
              - A mapping of full Checkmk tag strings to domain suffixes.
              - For each host, the keys of this map are checked in order against the host's tags.
              - The suffix of the first matching entry is appended to the hostname.
              - If no tag matches, the hostname is used as-is.
              - Keys must be in the full Checkmk format C(tag_<group>_<value>),
                e.g. C(tag_criticality_prod).
              - Values are the domain suffixes to append, e.g. C(.example.com).
              - Unlike the other filtering options, this cannot be set via an
                environment variable.
            required: false
            type: dict

    notes:
        - Because inventory plugins run before C(group_vars/) and C(host_vars/) are
          loaded, C(checkmk_var_*) values placed there are B(not) visible to this
          plugin. Sources that B(do) work are extra-vars (C(-e)), environment
          variables (C(CHECKMK_VAR_*)) and C(ansible.cfg) C([checkmk_lookup]) entries.
        - The C(lowercase_hosts) and C(domain_map) options change hostnames. If a
          transformation maps two different Checkmk hosts to the same name, they are
          merged into a single inventory host, so make sure transformed names stay unique.

    author:
        - Max Sickora (@max-checkmk)
        - JDog1895 (@JDog1895)
        - Robin Gierse (@robin-checkmk)
"""

EXAMPLES = """
# To get started, you need to create a file called `checkmk.yml`, which contains
# one of the example blocks below and use it as your inventory source.
# E.g., with `ansible-inventory -i checkmk.yml --graph`.

# Group all hosts based on both tag groups and sites
# and update ansible_host with the ip address from Checkmk:
plugin: checkmk.general.checkmk
server_url: "http://myserver/"
site: "mysite"
api_user: "myuser"
api_secret: "mysecret"
groupsources: ["hosttags", "sites"]
want_ipv4: true

# The connection options are omitted in the following examples for brevity.
# They can be set as shown above or via environment variables (see below).

# Exclude test and offline systems from the inventory:
plugin: checkmk.general.checkmk
exclude_tags:
  - tag_criticality_test
  - tag_criticality_offline

# Only hosts in a specific folder and its subfolders:
plugin: checkmk.general.checkmk
folder: "/linux"
recursive: true

# Build lowercase FQDNs by appending a domain suffix based on host tags:
plugin: checkmk.general.checkmk
lowercase_hosts: true
domain_map:
  tag_criticality_prod: ".example.com"
  tag_criticality_test: ".test.example.com"

# ---------------------------------------------------------------------------
# Using environment variables
# ---------------------------------------------------------------------------
# Connection parameters and the filtering options can be provided via
# environment variables instead of writing them into the inventory file.
# The supported variables are:
#   CHECKMK_VAR_SERVER_URL, CHECKMK_VAR_SITE,
#   CHECKMK_VAR_API_USER, CHECKMK_VAR_API_SECRET,
#   CHECKMK_VAR_VALIDATE_CERTS, CHECKMK_VAR_API_AUTH_TYPE,
#   CHECKMK_VAR_FOLDER, CHECKMK_VAR_RECURSIVE,
#   CHECKMK_VAR_EXCLUDE_TAGS (comma-separated), CHECKMK_VAR_LOWERCASE_HOSTS

# Minimal inventory file when using environment variables:
plugin: checkmk.general.checkmk
groupsources: ["hosttags", "sites"]

# ---------------------------------------------------------------------------
# Using Ansible variables for credentials
# ---------------------------------------------------------------------------
# Connection parameters can also be provided via Ansible variables, e.g.
# via extra-vars (`-e`). Note that vars from group_vars/ or host_vars/
# are NOT visible here, because inventory plugins run before those are loaded.
# The supported variable names follow the scheme checkmk_var_<parameter>:
#   checkmk_var_server_url, checkmk_var_site,
#   checkmk_var_api_user, checkmk_var_api_secret,
#   checkmk_var_validate_certs, checkmk_var_api_auth_type
"""

import json
import re

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.inventory import BaseInventoryPlugin
from ansible.utils.display import Display
from ansible_collections.checkmk.general.plugins.module_utils.lookup_api import (
    CheckMKLookupAPI,
)
from ansible_collections.checkmk.general.plugins.module_utils.utils import (
    normalize_folder,
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
        self.api_auth_type = None
        self.api_auth_cookie = None
        self.validate_certs = None
        self.want_ipv4 = None
        self.folder = None
        self.recursive = False
        self.exclude_tags = []
        self.lowercase_hosts = False
        self.domain_map = {}
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

    def _is_excluded(self, host):
        """Return True if the host has any of the excluded tags set."""
        if not self.exclude_tags:
            return False
        host_tags = host.get("tags", {})
        # host_tags has the form {"tag_criticality": "test", "tag_agent": "cmk-agent", ...}
        # We reconstruct the full tag string "tag_<group>_<value>" and check against exclude_tags
        for group, value in host_tags.items():
            if value:
                full_tag = group + "_" + value
                if full_tag in self.exclude_tags:
                    display.vvv(
                        "Excluding host '%s' due to tag '%s'"
                        % (host.get("id"), full_tag)
                    )
                    return True
        return False

    def parse(self, inventory, loader, path, cache=False):
        super(InventoryModule, self).parse(inventory, loader, path, cache)

        config = self._read_config_data(path)

        try:
            self.plugin = self.get_option("plugin")
            self.server_url = self.get_option("server_url")
            self.site = self.get_option("site")
            self.user = self.get_option("api_user")
            self.secret = self.get_option("api_secret")
            self.api_auth_type = self.get_option("api_auth_type")
            self.api_auth_cookie = self.get_option("api_auth_cookie")
            self.validate_certs = self.get_option("validate_certs")
            self.want_ipv4 = self.get_option("want_ipv4")
            self.groupsources = self.get_option("groupsources")
            self.folder = self.get_option("folder")
            self.recursive = self.get_option("recursive")
            self.exclude_tags = self.get_option("exclude_tags") or []
            self.lowercase_hosts = self.get_option("lowercase_hosts")
            self.domain_map = self.get_option("domain_map") or {}
        except Exception as e:
            raise AnsibleParserError("All correct options required: {}".format(e))

        if self.exclude_tags:
            display.vvv("Excluding hosts with tags: %s" % self.exclude_tags)

        api = CheckMKLookupAPI(
            site_url=self.get_option("server_url") + "/" + self.get_option("site"),
            api_auth_type=self.api_auth_type,
            api_auth_cookie=self.api_auth_cookie,
            api_user=self.get_option("api_user"),
            api_secret=self.get_option("api_secret"),
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
                self.inventory.set_variable(
                    host["id"], "ansible_host", host["ipaddress"]
                )

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

    def _get_domain_suffix(self, host_tags):
        """Return the suffix of the first domain_map entry matching a host tag, or empty string."""
        host_full_tags = {
            group + "_" + value for group, value in host_tags.items() if value
        }
        for tag, suffix in self.domain_map.items():
            if tag in host_full_tags:
                return suffix
        return ""

    def _folder_matches(self, host_folder, target=None):
        """Return True if the host's folder matches the folder option.

        ``target`` is the pre-normalized folder option. It is computed once per
        run in ``_parse_hosts`` and passed in to avoid re-normalizing it for
        every host; when omitted it is derived from ``self.folder``.
        """
        if not self.folder:
            return True
        if target is None:
            target = normalize_folder(self.folder)
        host_folder = normalize_folder(host_folder)
        if host_folder == target:
            return True
        if self.recursive:
            prefix = "/" if target == "/" else target + "/"
            return host_folder.startswith(prefix)
        return False

    def _parse_hosts(self, raw_hosts):
        """Convert raw API host list to internal format, apply folder, exclude_tags and domain_map."""
        folder_target = normalize_folder(self.folder) if self.folder else None
        hosts = []
        for host in raw_hosts:
            host_id = host.get("id")
            host_tags = {
                taggroup: tag
                for taggroup, tag in host.get("extensions")
                .get("effective_attributes")
                .items()
                if taggroup in self.tags
            }
            parsed = {
                "id": host_id,
                "title": host.get("extensions").get("title"),
                "ipaddress": host.get("extensions").get("attributes").get("ipaddress"),
                "folder": host.get("extensions").get("folder"),
                "site": host.get("extensions").get("effective_attributes").get("site"),
                "tags": host_tags,
            }

            if not self._folder_matches(parsed["folder"], folder_target):
                continue

            if self._is_excluded(parsed):
                continue

            if self.domain_map:
                suffix = self._get_domain_suffix(host_tags)
                if suffix:
                    parsed["id"] = host_id + suffix
                    display.vvv(
                        "Host '%s' gets suffix '%s' -> '%s'"
                        % (host_id, suffix, parsed["id"])
                    )

            if self.lowercase_hosts:
                parsed["id"] = parsed["id"].lower()

            hosts.append(parsed)
        return hosts

    def _get_hosts(self, api):
        # The folder option is filtered on the client side in _parse_hosts,
        # because fetching hosts per folder via the REST API does not support
        # effective_attributes on all supported Checkmk versions.
        if self.folder:
            display.vvv(
                "Restricting hosts to folder '%s'%s"
                % (self.folder, " (recursive)" if self.recursive else "")
            )

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

        return self._parse_hosts(response.get("value", []))

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

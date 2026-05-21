# Copyright: (c) 2024, Max Sickora <max.sickora@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
    name: checkmk
    author: Max Sickora (@max-checkmk)
    short_description: Dynamic Inventory Source for Checkmk
    description:
        - Get hosts from any Checkmk site.
        - Generate groups based on tag groups or sites in Checkmk.

    extends_documentation_fragment: [checkmk.general.common_lookup]

    options:
        plugin:
            description: Name of the plugin. Should always be C(checkmk.general.checkmk).
            type: string
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
            type: boolean
            required: false
        server_url:
            description: URL of the Checkmk server.
            required: false
            type: str
            env:
              - name: CHECKMK_VAR_SERVER_URL
        site:
            description: The Checkmk site name.
            required: false
            type: str
            env:
              - name: CHECKMK_VAR_SITE
        api_user:
            description: The api user for the REST API.
            required: false
            type: str
            env:
              - name: CHECKMK_VAR_API_USER
        api_secret:
            description: The secret for the api user.
            required: false
            type: str
            env:
              - name: CHECKMK_VAR_API_SECRET
        validate_certs:
            description: Whether to validate SSL certificates.
            default: true
            type: bool
            env:
              - name: CHECKMK_VAR_VALIDATE_CERTS
        folder:
            description:
              - Restrict hosts to a specific folder path in Checkmk.
              - Uses the Checkmk tilde-format, e.g. C(~linux~production) instead of C(/linux/production).
              - If not set, all hosts from the entire site are returned.
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
              - Can also be set via environment variable as a comma-separated string,
                e.g. C(tag_criticality_test,tag_agent_cmk-agent).
            required: false
            type: list
            elements: str
            env:
              - name: CHECKMK_VAR_EXCLUDE_TAGS
        lowercase_hosts:
            description:
              - If set to C(true), all hostnames will be converted to lowercase in the inventory.
              - Default is C(false), hostnames are used exactly as defined in Checkmk.
            required: false
            default: false
            type: bool
            env:
              - name: CHECKMK_VAR_LOWERCASE_HOSTS
        domain_map:
            description:
              - A mapping of full Checkmk tag strings to domain suffixes.
              - For each host, the tags are checked against the keys of this map in order.
              - The suffix of the first matching tag is appended to the hostname.
              - If no tag matches, the hostname is used as-is.
              - Keys must be in the full Checkmk format C(tag_<group>_<value>),
                e.g. C(tag_criticality_prod).
              - Values are the domain suffixes to append, e.g. C(.example.com).
            required: false
            type: dict
    notes:
        - Because inventory plugins run before C(group_vars/) and C(host_vars/) are
          loaded, C(checkmk_var_*) values placed there are B(not) visible to this
          plugin. Sources that B(do) work are extra-vars (C(-e)), environment
          variables (C(CHECKMK_VAR_*)) and C(ansible.cfg) C([checkmk_lookup]) entries.
"""

EXAMPLES = """
# Group all hosts based on both tag groups and sites, exclude test systems:
plugin: checkmk.general.checkmk
server_url: "http://hostname/"
site: "sitename"
api_user: "cmkadmin"
api_secret: "******"
validate_certs: false
groupsources: ["hosttags", "sites"]
want_ipv4: false
exclude_tags:
  - tag_criticality_test

# Only hosts in a specific folder and its subfolders, excluding test and offline:
plugin: checkmk.general.checkmk
validate_certs: false
folder: "~linux~production"
recursive: true
exclude_tags:
  - tag_criticality_test
  - tag_criticality_offline

# ---------------------------------------------------------------------------
# Using environment variables for credentials
# ---------------------------------------------------------------------------
# Connection parameters can be provided via environment variables instead of
# writing them into the inventory file. The supported variables are:
#   CHECKMK_VAR_SERVER_URL, CHECKMK_VAR_SITE,
#   CHECKMK_VAR_API_USER, CHECKMK_VAR_API_SECRET,
#   CHECKMK_VAR_VALIDATE_CERTS, CHECKMK_VAR_API_AUTH_TYPE

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
import os
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

            self.folder = self.get_option("folder") or os.environ.get(
                "CHECKMK_VAR_FOLDER"
            )

            _recursive_yaml = self.get_option("recursive")
            _recursive_env = os.environ.get("CHECKMK_VAR_RECURSIVE")
            if _recursive_yaml is not None:
                self.recursive = _recursive_yaml
            elif _recursive_env is not None:
                self.recursive = _recursive_env.lower() not in ("false", "0", "no")
            else:
                self.recursive = False

            # exclude_tags: YAML liefert eine Liste, Env-Var kommt als komma-separierter String
            _exclude_tags_yaml = self.get_option("exclude_tags")
            _exclude_tags_env = os.environ.get("CHECKMK_VAR_EXCLUDE_TAGS")
            if _exclude_tags_yaml:
                self.exclude_tags = _exclude_tags_yaml
            elif _exclude_tags_env:
                self.exclude_tags = [
                    t.strip() for t in _exclude_tags_env.split(",") if t.strip()
                ]
            else:
                self.exclude_tags = []

            if self.exclude_tags:
                display.vvv("Excluding hosts with tags: %s" % self.exclude_tags)

            _lowercase_yaml = self.get_option("lowercase_hosts")
            _lowercase_env = os.environ.get("CHECKMK_VAR_LOWERCASE_HOSTS")
            if _lowercase_yaml is not None:
                self.lowercase_hosts = _lowercase_yaml
            elif _lowercase_env is not None:
                self.lowercase_hosts = _lowercase_env.lower() not in (
                    "false",
                    "0",
                    "no",
                )
            else:
                self.lowercase_hosts = False

            self.domain_map = self.get_option("domain_map") or {}

        except Exception as e:
            raise AnsibleParserError("All correct options required: {}".format(e))

        for attr, name in [
            (self.server_url, "server_url"),
            (self.site, "site"),
            (self.user, "api_user"),
            (self.secret, "api_secret"),
        ]:
            if not attr:
                raise AnsibleParserError(
                    "Option '%s' is required but not set in inventory file or environment variables "
                    "(CHECKMK_VAR_%s)" % (name, name.upper())
                )

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
        """Return the first matching domain suffix from domain_map, or empty string."""
        for group, value in host_tags.items():
            if value:
                full_tag = group + "_" + value
                if full_tag in self.domain_map:
                    return self.domain_map[full_tag]
        return ""

    def _parse_hosts(self, raw_hosts):
        """Convert raw API host list to internal format, apply exclude_tags and domain_map."""
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

            if self._is_excluded(parsed):
                continue

            # add Domain-Suffix
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

    def _get_hosts_in_folder(self, api, folder):
        """Fetch raw hosts directly in a specific folder."""
        response = json.loads(
            api.get(
                "/objects/folder_config/%s/collections/hosts" % folder,
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
        return response.get("value", [])

    def _get_subfolders(self, api, folder):
        """Fetch all subfolder IDs recursively for a given folder."""
        response = json.loads(
            api.get(
                "/domain-types/folder_config/collections/all",
                {"parent": folder, "recursive": True},
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
        return [f.get("id") for f in response.get("value", [])]

    def _get_hosts(self, api):
        if self.folder:
            if self.recursive:
                folders = [self.folder] + self._get_subfolders(api, self.folder)
                display.vvv("Recursive folder search in: %s" % folders)
            else:
                folders = [self.folder]

            raw_hosts = []
            seen_ids = set()
            for f in folders:
                for host in self._get_hosts_in_folder(api, f):
                    host_id = host.get("id")
                    if host_id not in seen_ids:
                        seen_ids.add(host_id)
                        raw_hosts.append(host)
        else:
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
            raw_hosts = response.get("value", [])

        return self._parse_hosts(raw_hosts)

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

#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2023, Lars Getwan <lars.getwan@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

# This is a fake lookup_api to create static response for unit testing modules of the checkmk collection


class CheckMKLookupAPI:
    """Base class to contact a Checkmk server for ~Lookup calls"""

    def __init__(self, site_url, user, secret, validate_certs=True):
        self.site_url = site_url
        self.user = user
        self.secret = secret
        self.validate_certs = validate_certs
        self.url = "%s/check_mk/api/1.0" % site_url
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer %s %s" % (user, secret),
        }

    def get(self, endpoint="", parameters=None):
        if endpoint == "/domain-types/host_tag_group/collections/all":
            # Example response from the endpoint "Show all host tag groups"
            host_tag_group = """{
                "domainType": "host_tag_group",
                "id": "host_tag",
                "links": [
                    {
                        "domainType": "link",
                        "href": "http://192.168.11.11/maintestsite/check_mk/api/1.0/domain-types/host_tag_group/collections/all",
                        "method": "GET",
                        "rel": "self",
                        "type": "application/json"
                    }
                ],
                "value": [
                    {
                        "domainType": "host_tag_group",
                        "extensions": {
                            "tags": [
                                {
                                    "aux_tags": [],
                                    "id": "prod",
                                    "title": "Productive system"
                                },
                                {
                                    "aux_tags": [],
                                    "id": "critical",
                                    "title": "Business critical"
                                },
                                {
                                    "aux_tags": [],
                                    "id": "test",
                                    "title": "Test system"
                                },
                                {
                                    "aux_tags": [],
                                    "id": "offline",
                                    "title": "Do not monitor this host"
                                }
                            ],
                            "topic": "Tags"
                        },
                        "id": "criticality",
                        "links": [
                            {
                                "domainType": "link",
                                "href": "http://192.168.11.11/maintestsite/check_mk/api/1.0/objects/host_tag_group/criticality",
                                "method": "GET",
                                "rel": "self",
                                "type": "application/json"
                            },
                            {
                                "domainType": "link",
                                "href": "http://192.168.11.11/maintestsite/check_mk/api/1.0/objects/host_tag_group/criticality",
                                "method": "PUT",
                                "rel": "urn:org.restfulobjects:rels/update",
                                "type": "application/json"
                            },
                            {
                                "domainType": "link",
                                "href": "http://192.168.11.11/maintestsite/check_mk/api/1.0/objects/host_tag_group/criticality",
                                "method": "DELETE",
                                "rel": "urn:org.restfulobjects:rels/delete",
                                "type": "application/json"
                            }
                        ],
                        "members": {
                            "title": {
                                "format": "string",
                                "id": "title",
                                "links": [
                                    {
                                        "domainType": "link",
                                        "href": "http://192.168.11.11/maintestsite/check_mk/api/1.0/objects/host_tag_group/criticality/properties/title",
                                        "method": "GET",
                                        "rel": "self",
                                        "type": "application/json"
                                    }
                                ],
                                "memberType": "property",
                                "title": null,
                                "value": "Criticality"
                            }
                        },
                        "title": "Criticality"
                    },
                    {
                        "domainType": "host_tag_group",
                        "extensions": {
                            "tags": [
                                {
                                    "aux_tags": [],
                                    "id": "lan",
                                    "title": "Local network (low latency)"
                                },
                                {
                                    "aux_tags": [],
                                    "id": "wan",
                                    "title": "WAN (high latency)"
                                },
                                {
                                    "aux_tags": [],
                                    "id": "dmz",
                                    "title": "DMZ (low latency, secure access)"
                                }
                            ],
                            "topic": "Tags"
                        },
                        "id": "networking",
                        "links": [
                            {
                                "domainType": "link",
                                "href": "http://192.168.11.11/maintestsite/check_mk/api/1.0/objects/host_tag_group/networking",
                                "method": "GET",
                                "rel": "self",
                                "type": "application/json"
                            },
                            {
                                "domainType": "link",
                                "href": "http://192.168.11.11/maintestsite/check_mk/api/1.0/objects/host_tag_group/networking",
                                "method": "PUT",
                                "rel": "urn:org.restfulobjects:rels/update",
                                "type": "application/json"
                            },
                            {
                                "domainType": "link",
                                "href": "http://192.168.11.11/maintestsite/check_mk/api/1.0/objects/host_tag_group/networking",
                                "method": "DELETE",
                                "rel": "urn:org.restfulobjects:rels/delete",
                                "type": "application/json"
                            }
                        ],
                        "members": {
                            "title": {
                                "format": "string",
                                "id": "title",
                                "links": [
                                    {
                                        "domainType": "link",
                                        "href": "http://192.168.11.11/maintestsite/check_mk/api/1.0/objects/host_tag_group/networking/properties/title",
                                        "method": "GET",
                                        "rel": "self",
                                        "type": "application/json"
                                    }
                                ],
                                "memberType": "property",
                                "title": null,
                                "value": "Networking Segment"
                            }
                        },
                        "title": "Networking Segment"
                    },
                    {
                        "domainType": "host_tag_group",
                        "extensions": {
                            "tags": [
                                {
                                    "aux_tags": [],
                                    "id": "None",
                                    "title": "WannabeNone"
                                },
                                {
                                    "aux_tags": [],
                                    "id": null,
                                    "title": "TherealNone"
                                },
                                {
                                    "aux_tags": [],
                                    "id": "None2",
                                    "title": "Justanothertag"
                                }
                            ],
                            "topic": "Tags"
                        },
                        "id": "testtaggroup",
                        "links": [
                            {
                                "domainType": "link",
                                "href": "http://192.168.11.11/maintestsite/check_mk/api/1.0/objects/host_tag_group/testtaggroup",
                                "method": "GET",
                                "rel": "self",
                                "type": "application/json"
                            },
                            {
                                "domainType": "link",
                                "href": "http://192.168.11.11/maintestsite/check_mk/api/1.0/objects/host_tag_group/testtaggroup",
                                "method": "PUT",
                                "rel": "urn:org.restfulobjects:rels/update",
                                "type": "application/json"
                            },
                            {
                                "domainType": "link",
                                "href": "http://192.168.11.11/maintestsite/check_mk/api/1.0/objects/host_tag_group/testtaggroup",
                                "method": "DELETE",
                                "rel": "urn:org.restfulobjects:rels/delete",
                                "type": "application/json"
                            }
                        ],
                        "members": {
                            "title": {
                                "format": "string",
                                "id": "title",
                                "links": [
                                    {
                                        "domainType": "link",
                                        "href": "http://192.168.11.11/maintestsite/check_mk/api/1.0/objects/host_tag_group/testtaggroup/properties/title",
                                        "method": "GET",
                                        "rel": "self",
                                        "type": "application/json"
                                    }
                                ],
                                "memberType": "property",
                                "title": null,
                                "value": "testtaggroup"
                            }
                        },
                        "title": "testtaggroup"
                    },
                    {
                        "domainType": "host_tag_group",
                        "extensions": {
                            "tags": [
                                {
                                    "aux_tags": [
                                        "tcp",
                                        "checkmk-agent"
                                    ],
                                    "id": "cmk-agent",
                                    "title": "API integrations if configured, else Checkmk agent"
                                },
                                {
                                    "aux_tags": [
                                        "tcp",
                                        "checkmk-agent"
                                    ],
                                    "id": "all-agents",
                                    "title": "Configured API integrations and Checkmk agent"
                                },
                                {
                                    "aux_tags": [
                                        "tcp"
                                    ],
                                    "id": "special-agents",
                                    "title": "Configured API integrations, no Checkmk agent"
                                },
                                {
                                    "aux_tags": [],
                                    "id": "no-agent",
                                    "title": "No API integrations, no Checkmk agent"
                                }
                            ],
                            "topic": "Monitoring agents"
                        },
                        "id": "agent",
                        "links": [
                            {
                                "domainType": "link",
                                "href": "http://192.168.11.11/maintestsite/check_mk/api/1.0/objects/host_tag_group/agent",
                                "method": "GET",
                                "rel": "self",
                                "type": "application/json"
                            },
                            {
                                "domainType": "link",
                                "href": "http://192.168.11.11/maintestsite/check_mk/api/1.0/objects/host_tag_group/agent",
                                "method": "PUT",
                                "rel": "urn:org.restfulobjects:rels/update",
                                "type": "application/json"
                            },
                            {
                                "domainType": "link",
                                "href": "http://192.168.11.11/maintestsite/check_mk/api/1.0/objects/host_tag_group/agent",
                                "method": "DELETE",
                                "rel": "urn:org.restfulobjects:rels/delete",
                                "type": "application/json"
                            }
                        ],
                        "members": {
                            "title": {
                                "format": "string",
                                "id": "title",
                                "links": [
                                    {
                                        "domainType": "link",
                                        "href": "http://192.168.11.11/maintestsite/check_mk/api/1.0/objects/host_tag_group/agent/properties/title",
                                        "method": "GET",
                                        "rel": "self",
                                        "type": "application/json"
                                    }
                                ],
                                "memberType": "property",
                                "title": null,
                                "value": "Checkmk agent / API integrations"
                            }
                        },
                        "title": "Checkmk agent / API integrations"
                    },
                    {
                        "domainType": "host_tag_group",
                        "extensions": {
                            "help": "By default, each host has a piggyback data source. ...",
                            "tags": [
                                {
                                    "aux_tags": [],
                                    "id": "auto-piggyback",
                                    "title": "Use piggyback data from other hosts if present"
                                },
                                {
                                    "aux_tags": [],
                                    "id": "piggyback",
                                    "title": "Always use and expect piggyback data"
                                },
                                {
                                    "aux_tags": [],
                                    "id": "no-piggyback",
                                    "title": "Never use piggyback data"
                                }
                            ],
                            "topic": "Monitoring agents"
                        },
                        "id": "piggyback",
                        "links": [
                            {
                                "domainType": "link",
                                "href": "http://192.168.11.11/maintestsite/check_mk/api/1.0/objects/host_tag_group/piggyback",
                                "method": "GET",
                                "rel": "self",
                                "type": "application/json"
                            },
                            {
                                "domainType": "link",
                                "href": "http://192.168.11.11/maintestsite/check_mk/api/1.0/objects/host_tag_group/piggyback",
                                "method": "PUT",
                                "rel": "urn:org.restfulobjects:rels/update",
                                "type": "application/json"
                            },
                            {
                                "domainType": "link",
                                "href": "http://192.168.11.11/maintestsite/check_mk/api/1.0/objects/host_tag_group/piggyback",
                                "method": "DELETE",
                                "rel": "urn:org.restfulobjects:rels/delete",
                                "type": "application/json"
                            }
                        ],
                        "members": {
                            "title": {
                                "format": "string",
                                "id": "title",
                                "links": [
                                    {
                                        "domainType": "link",
                                        "href": "http://192.168.11.11/maintestsite/check_mk/api/1.0/objects/host_tag_group/piggyback/properties/title",
                                        "method": "GET",
                                        "rel": "self",
                                        "type": "application/json"
                                    }
                                ],
                                "memberType": "property",
                                "title": null,
                                "value": "Piggyback"
                            }
                        },
                        "title": "Piggyback"
                    },
                    {
                        "domainType": "host_tag_group",
                        "extensions": {
                            "tags": [
                                {
                                    "aux_tags": [],
                                    "id": "no-snmp",
                                    "title": "No SNMP"
                                },
                                {
                                    "aux_tags": [
                                        "snmp"
                                    ],
                                    "id": "snmp-v2",
                                    "title": "SNMP v2 or v3"
                                },
                                {
                                    "aux_tags": [
                                        "snmp"
                                    ],
                                    "id": "snmp-v1",
                                    "title": "SNMP v1"
                                }
                            ],
                            "topic": "Monitoring agents"
                        },
                        "id": "snmp_ds",
                        "links": [
                            {
                                "domainType": "link",
                                "href": "http://192.168.11.11/maintestsite/check_mk/api/1.0/objects/host_tag_group/snmp_ds",
                                "method": "GET",
                                "rel": "self",
                                "type": "application/json"
                            },
                            {
                                "domainType": "link",
                                "href": "http://192.168.11.11/maintestsite/check_mk/api/1.0/objects/host_tag_group/snmp_ds",
                                "method": "PUT",
                                "rel": "urn:org.restfulobjects:rels/update",
                                "type": "application/json"
                            },
                            {
                                "domainType": "link",
                                "href": "http://192.168.11.11/maintestsite/check_mk/api/1.0/objects/host_tag_group/snmp_ds",
                                "method": "DELETE",
                                "rel": "urn:org.restfulobjects:rels/delete",
                                "type": "application/json"
                            }
                        ],
                        "members": {
                            "title": {
                                "format": "string",
                                "id": "title",
                                "links": [
                                    {
                                        "domainType": "link",
                                        "href": "http://192.168.11.11/maintestsite/check_mk/api/1.0/objects/host_tag_group/snmp_ds/properties/title",
                                        "method": "GET",
                                        "rel": "self",
                                        "type": "application/json"
                                    }
                                ],
                                "memberType": "property",
                                "title": null,
                                "value": "SNMP"
                            }
                        },
                        "title": "SNMP"
                    },
                    {
                        "domainType": "host_tag_group",
                        "extensions": {
                            "tags": [
                                {
                                    "aux_tags": [
                                        "ip-v4"
                                    ],
                                    "id": "ip-v4-only",
                                    "title": "IPv4 only"
                                },
                                {
                                    "aux_tags": [
                                        "ip-v6"
                                    ],
                                    "id": "ip-v6-only",
                                    "title": "IPv6 only"
                                },
                                {
                                    "aux_tags": [
                                        "ip-v4",
                                        "ip-v6"
                                    ],
                                    "id": "ip-v4v6",
                                    "title": "IPv4/IPv6 dual-stack"
                                },
                                {
                                    "aux_tags": [],
                                    "id": "no-ip",
                                    "title": "No IP"
                                }
                            ],
                            "topic": "Address"
                        },
                        "id": "address_family",
                        "links": [
                            {
                                "domainType": "link",
                                "href": "http://192.168.11.11/maintestsite/check_mk/api/1.0/objects/host_tag_group/address_family",
                                "method": "GET",
                                "rel": "self",
                                "type": "application/json"
                            },
                            {
                                "domainType": "link",
                                "href": "http://192.168.11.11/maintestsite/check_mk/api/1.0/objects/host_tag_group/address_family",
                                "method": "PUT",
                                "rel": "urn:org.restfulobjects:rels/update",
                                "type": "application/json"
                            },
                            {
                                "domainType": "link",
                                "href": "http://192.168.11.11/maintestsite/check_mk/api/1.0/objects/host_tag_group/address_family",
                                "method": "DELETE",
                                "rel": "urn:org.restfulobjects:rels/delete",
                                "type": "application/json"
                            }
                        ],
                        "members": {
                            "title": {
                                "format": "string",
                                "id": "title",
                                "links": [
                                    {
                                        "domainType": "link",
                                        "href": "http://192.168.11.11/maintestsite/check_mk/api/1.0/objects/host_tag_group/address_family/properties/title",
                                        "method": "GET",
                                        "rel": "self",
                                        "type": "application/json"
                                    }
                                ],
                                "memberType": "property",
                                "title": null,
                                "value": "IP address family"
                            }
                        },
                        "title": "IP address family"
                    }
                ]
            }"""
            return host_tag_group

        # Example response from the endpoint "Show all site connections"
        if endpoint == "/domain-types/site_connection/collections/all":
            site_connection = """{
                "domainType": "site_connection",
                "extensions": {},
                "id": "site_connection",
                "links": [
                    {
                        "domainType": "link",
                        "href": "http://192.168.11.11/maintestsite/check_mk/api/1.0/domain-types/site_connection/collections/all",
                        "method": "GET",
                        "rel": "self",
                        "type": "application/json"
                    }
                ],
                "value": [
                    {
                        "domainType": "site_connection",
                        "extensions": {
                            "basic_settings": {
                                "alias": "Local site maintestsite",
                                "customer": "provider",
                                "site_id": "maintestsite"
                            },
                            "configuration_connection": {
                                "direct_login_to_web_gui_allowed": true,
                                "disable_remote_configuration": true,
                                "enable_replication": false,
                                "ignore_tls_errors": false,
                                "replicate_event_console": false,
                                "replicate_extensions": false,
                                "url_of_remote_site": "",
                                "user_sync": {
                                    "sync_with_ldap_connections": "all"
                                }
                            },
                            "status_connection": {
                                "connect_timeout": 5,
                                "connection": {
                                    "socket_type": "local"
                                },
                                "disable_in_status_gui": false,
                                "persistent_connection": false,
                                "proxy": {
                                    "use_livestatus_daemon": "direct"
                                },
                                "status_host": {
                                    "status_host_set": "disabled"
                                },
                                "url_prefix": "/maintestsite/"
                            }
                        },
                        "id": "maintestsite",
                        "links": [
                            {
                                "domainType": "link",
                                "href": "http://192.168.11.11/maintestsite/check_mk/api/1.0/objects/site_connection/maintestsite",
                                "method": "GET",
                                "rel": "self",
                                "type": "application/json"
                            },
                            {
                                "domainType": "link",
                                "href": "http://192.168.11.11/maintestsite/check_mk/api/1.0/objects/site_connection/maintestsite",
                                "method": "PUT",
                                "rel": "urn:org.restfulobjects:rels/update",
                                "type": "application/json"
                            },
                            {
                                "domainType": "link",
                                "href": "http://192.168.11.11/maintestsite/check_mk/api/1.0/objects/site_connection/maintestsite",
                                "method": "DELETE",
                                "rel": "urn:org.restfulobjects:rels/delete",
                                "type": "application/json"
                            }
                        ],
                        "members": {},
                        "title": "Local site maintestsite"
                    },
                    {
                        "domainType": "site_connection",
                        "extensions": {
                            "basic_settings": {
                                "alias": "remotetestsite",
                                "customer": "provider",
                                "site_id": "remotetestsite"
                            },
                            "configuration_connection": {
                                "direct_login_to_web_gui_allowed": true,
                                "disable_remote_configuration": true,
                                "enable_replication": true,
                                "ignore_tls_errors": false,
                                "replicate_event_console": true,
                                "replicate_extensions": true,
                                "url_of_remote_site": "http://192.168.11.12/remotetestsite/check_mk/",
                                "user_sync": {
                                    "sync_with_ldap_connections": "all"
                                }
                            },
                            "status_connection": {
                                "connect_timeout": 2,
                                "connection": {
                                    "encrypted": true,
                                    "host": "192.168.11.12",
                                    "port": 6557,
                                    "socket_type": "tcp",
                                    "verify": true
                                },
                                "disable_in_status_gui": false,
                                "persistent_connection": false,
                                "proxy": {
                                    "global_settings": true,
                                    "use_livestatus_daemon": "with_proxy"
                                },
                                "status_host": {
                                    "status_host_set": "disabled"
                                },
                                "url_prefix": ""
                            }
                        },
                        "id": "remotetestsite",
                        "links": [
                            {
                                "domainType": "link",
                                "href": "http://192.168.11.11/maintestsite/check_mk/api/1.0/objects/site_connection/remotetestsite",
                                "method": "GET",
                                "rel": "self",
                                "type": "application/json"
                            },
                            {
                                "domainType": "link",
                                "href": "http://192.168.11.11/maintestsite/check_mk/api/1.0/objects/site_connection/remotetestsite",
                                "method": "PUT",
                                "rel": "urn:org.restfulobjects:rels/update",
                                "type": "application/json"
                            },
                            {
                                "domainType": "link",
                                "href": "http://192.168.11.11/maintestsite/check_mk/api/1.0/objects/site_connection/remotetestsite",
                                "method": "DELETE",
                                "rel": "urn:org.restfulobjects:rels/delete",
                                "type": "application/json"
                            }
                        ],
                        "members": {},
                        "title": "remotetestsite"
                    }
                ]
            }"""
            return site_connection

        # Example response from the endpoint "Show all hosts"
        if endpoint == "/domain-types/host_config/collections/all":
            host_config = """{
                "domainType": "host_config",
                "id": "host",
                "links": [
                    {
                        "domainType": "link",
                        "href": "http://192.168.11.11/maintestsite/check_mk/api/1.0/domain-types/host_config/collections/all",
                        "method": "GET",
                        "rel": "self",
                        "type": "application/json"
                    }
                ],
                "value": [
                    {
                        "domainType": "host_config",
                        "extensions": {
                            "attributes": {
                                "ipaddress": "192.168.11.11",
                                "meta_data": {
                                    "created_at": "2024-08-28T07:32:19.415298+00:00",
                                    "created_by": "cmkadmin",
                                    "updated_at": "2024-09-05T07:25:47.164888+00:00"
                                },
                                "site": "maintestsite",
                                "tag_agent": "cmk-agent"
                            },
                            "cluster_nodes": null,
                            "effective_attributes": {
                                "additional_ipv4addresses": [],
                                "additional_ipv6addresses": [],
                                "alias": "",
                                "bake_agent_package": true,
                                "cmk_agent_connection": "pull-agent",
                                "contactgroups": {
                                    "groups": [],
                                    "recurse_perms": false,
                                    "recurse_use": false,
                                    "use": false,
                                    "use_for_services": false
                                },
                                "inventory_failed": false,
                                "ipaddress": "192.168.11.11",
                                "ipv6address": "",
                                "labels": {},
                                "locked_attributes": [],
                                "locked_by": {
                                    "instance_id": "",
                                    "program_id": "",
                                    "site_id": "maintestsite"
                                },
                                "management_address": "",
                                "management_ipmi_credentials": null,
                                "management_protocol": "none",
                                "management_snmp_community": null,
                                "meta_data": {
                                    "created_at": "2024-08-28T07:32:19.415298+00:00",
                                    "created_by": "cmkadmin",
                                    "updated_at": "2024-09-05T07:25:47.164888+00:00"
                                },
                                "network_scan": {
                                    "addresses": [],
                                    "exclude_addresses": [],
                                    "run_as": "cmkadmin",
                                    "scan_interval": 86400,
                                    "set_ip_address": true,
                                    "tag_criticality": "offline",
                                    "time_allowed": [
                                        {
                                            "end": "23:59:59",
                                            "start": "00:00:00"
                                        }
                                    ]
                                },
                                "network_scan_result": {
                                    "end": null,
                                    "output": "",
                                    "start": null,
                                    "state": "running"
                                },
                                "parents": [],
                                "site": "maintestsite",
                                "snmp_community": null,
                                "tag_address_family": "ip-v4-only",
                                "tag_agent": "cmk-agent",
                                "tag_criticality": "prod",
                                "tag_networking": "lan",
                                "tag_piggyback": "auto-piggyback",
                                "tag_snmp_ds": "no-snmp",
                                "tag_testtaggroup": "None"
                            },
                            "folder": "/main",
                            "is_cluster": false,
                            "is_offline": false
                        },
                        "id": "checkmk-server-main",
                        "links": [],
                        "members": {},
                        "title": "checkmk-server-main"
                    },
                    {
                        "domainType": "host_config",
                        "extensions": {
                            "attributes": {
                                "ipaddress": "192.168.111.111",
                                "meta_data": {
                                    "created_at": "2024-09-05T07:24:25.593371+00:00",
                                    "created_by": "cmkadmin",
                                    "updated_at": "2024-09-05T07:25:47.164953+00:00"
                                },
                                "tag_criticality": "test"
                            },
                            "cluster_nodes": null,
                            "effective_attributes": {
                                "additional_ipv4addresses": [],
                                "additional_ipv6addresses": [],
                                "alias": "",
                                "bake_agent_package": true,
                                "cmk_agent_connection": "pull-agent",
                                "contactgroups": {
                                    "groups": [],
                                    "recurse_perms": false,
                                    "recurse_use": false,
                                    "use": false,
                                    "use_for_services": false
                                },
                                "inventory_failed": false,
                                "ipaddress": "192.168.111.111",
                                "ipv6address": "",
                                "labels": {},
                                "locked_attributes": [],
                                "locked_by": {
                                    "instance_id": "",
                                    "program_id": "",
                                    "site_id": "maintestsite"
                                },
                                "management_address": "",
                                "management_ipmi_credentials": null,
                                "management_protocol": "none",
                                "management_snmp_community": null,
                                "meta_data": {
                                    "created_at": "2024-09-05T07:24:25.593371+00:00",
                                    "created_by": "cmkadmin",
                                    "updated_at": "2024-09-05T07:25:47.164953+00:00"
                                },
                                "network_scan": {
                                    "addresses": [],
                                    "exclude_addresses": [],
                                    "run_as": "cmkadmin",
                                    "scan_interval": 86400,
                                    "set_ip_address": true,
                                    "tag_criticality": "offline",
                                    "time_allowed": [
                                        {
                                            "end": "23:59:59",
                                            "start": "00:00:00"
                                        }
                                    ]
                                },
                                "network_scan_result": {
                                    "end": null,
                                    "output": "",
                                    "start": null,
                                    "state": "running"
                                },
                                "parents": [],
                                "site": "maintestsite",
                                "snmp_community": null,
                                "tag_address_family": "ip-v4-only",
                                "tag_agent": "cmk-agent",
                                "tag_criticality": "test",
                                "tag_networking": "lan",
                                "tag_piggyback": "auto-piggyback",
                                "tag_snmp_ds": "no-snmp",
                                "tag_testtaggroup": "None"
                            },
                            "folder": "/main",
                            "is_cluster": false,
                            "is_offline": false
                        },
                        "id": "testhost1",
                        "links": [],
                        "members": {},
                        "title": "testhost1"
                    },
                    {
                        "domainType": "host_config",
                        "extensions": {
                            "attributes": {
                                "ipaddress": "192.168.111.222",
                                "meta_data": {
                                    "created_at": "2024-09-05T07:24:40+00:00",
                                    "created_by": "cmkadmin",
                                    "updated_at": "2024-09-05T07:25:47.164986+00:00"
                                },
                                "tag_agent": "cmk-agent",
                                "tag_snmp_ds": "snmp-v2"
                            },
                            "cluster_nodes": null,
                            "effective_attributes": {
                                "additional_ipv4addresses": [],
                                "additional_ipv6addresses": [],
                                "alias": "",
                                "bake_agent_package": true,
                                "cmk_agent_connection": "pull-agent",
                                "contactgroups": {
                                    "groups": [],
                                    "recurse_perms": false,
                                    "recurse_use": false,
                                    "use": false,
                                    "use_for_services": false
                                },
                                "inventory_failed": false,
                                "ipaddress": "192.168.111.222",
                                "ipv6address": "",
                                "labels": {},
                                "locked_attributes": [],
                                "locked_by": {
                                    "instance_id": "",
                                    "program_id": "",
                                    "site_id": "maintestsite"
                                },
                                "management_address": "",
                                "management_ipmi_credentials": null,
                                "management_protocol": "none",
                                "management_snmp_community": null,
                                "meta_data": {
                                    "created_at": "2024-09-05T07:24:40+00:00",
                                    "created_by": "cmkadmin",
                                    "updated_at": "2024-09-05T07:25:47.164986+00:00"
                                },
                                "network_scan": {
                                    "addresses": [],
                                    "exclude_addresses": [],
                                    "run_as": "cmkadmin",
                                    "scan_interval": 86400,
                                    "set_ip_address": true,
                                    "tag_criticality": "offline",
                                    "time_allowed": [
                                        {
                                            "end": "23:59:59",
                                            "start": "00:00:00"
                                        }
                                    ]
                                },
                                "network_scan_result": {
                                    "end": null,
                                    "output": "",
                                    "start": null,
                                    "state": "running"
                                },
                                "parents": [],
                                "site": "maintestsite",
                                "snmp_community": null,
                                "tag_address_family": "ip-v4-only",
                                "tag_agent": "cmk-agent",
                                "tag_criticality": "prod",
                                "tag_networking": "lan",
                                "tag_piggyback": "auto-piggyback",
                                "tag_snmp_ds": "snmp-v2",
                                "tag_testtaggroup": "None"
                            },
                            "folder": "/main",
                            "is_cluster": false,
                            "is_offline": false
                        },
                        "id": "testhost2",
                        "links": [],
                        "members": {},
                        "title": "testhost2"
                    },
                    {
                        "domainType": "host_config",
                        "extensions": {
                            "attributes": {
                                "meta_data": {
                                    "created_at": "2024-09-05T07:25:47.154584+00:00",
                                    "created_by": "cmkadmin",
                                    "updated_at": "2024-09-05T07:25:47.165017+00:00"
                                },
                                "tag_agent": "special-agents",
                                "tag_criticality": "critical"
                            },
                            "cluster_nodes": null,
                            "effective_attributes": {
                                "additional_ipv4addresses": [],
                                "additional_ipv6addresses": [],
                                "alias": "",
                                "bake_agent_package": true,
                                "cmk_agent_connection": "pull-agent",
                                "contactgroups": {
                                    "groups": [],
                                    "recurse_perms": false,
                                    "recurse_use": false,
                                    "use": false,
                                    "use_for_services": false
                                },
                                "inventory_failed": false,
                                "ipaddress": "",
                                "ipv6address": "",
                                "labels": {},
                                "locked_attributes": [],
                                "locked_by": {
                                    "instance_id": "",
                                    "program_id": "",
                                    "site_id": "maintestsite"
                                },
                                "management_address": "",
                                "management_ipmi_credentials": null,
                                "management_protocol": "none",
                                "management_snmp_community": null,
                                "meta_data": {
                                    "created_at": "2024-09-05T07:25:47.154584+00:00",
                                    "created_by": "cmkadmin",
                                    "updated_at": "2024-09-05T07:25:47.165017+00:00"
                                },
                                "network_scan": {
                                    "addresses": [],
                                    "exclude_addresses": [],
                                    "run_as": "cmkadmin",
                                    "scan_interval": 86400,
                                    "set_ip_address": true,
                                    "tag_criticality": "offline",
                                    "time_allowed": [
                                        {
                                            "end": "23:59:59",
                                            "start": "00:00:00"
                                        }
                                    ]
                                },
                                "network_scan_result": {
                                    "end": null,
                                    "output": "",
                                    "start": null,
                                    "state": "running"
                                },
                                "parents": [],
                                "site": "maintestsite",
                                "snmp_community": null,
                                "tag_address_family": "ip-v4-only",
                                "tag_agent": "special-agents",
                                "tag_criticality": "critical",
                                "tag_networking": "lan",
                                "tag_piggyback": "auto-piggyback",
                                "tag_snmp_ds": "no-snmp",
                                "tag_testtaggroup": null
                            },
                            "folder": "/main",
                            "is_cluster": false,
                            "is_offline": false
                        },
                        "id": "testhost3",
                        "links": [],
                        "members": {},
                        "title": "testhost3"
                    },
                    {
                        "domainType": "host_config",
                        "extensions": {
                            "attributes": {
                                "ipaddress": "192.168.11.15",
                                "meta_data": {
                                    "created_at": "2024-08-28T07:36:30.805379+00:00",
                                    "created_by": "cmkadmin",
                                    "updated_at": "2024-09-05T07:27:18.569235+00:00"
                                },
                                "site": "remotetestsite",
                                "tag_agent": "cmk-agent"
                            },
                            "cluster_nodes": null,
                            "effective_attributes": {
                                "additional_ipv4addresses": [],
                                "additional_ipv6addresses": [],
                                "alias": "",
                                "bake_agent_package": true,
                                "cmk_agent_connection": "pull-agent",
                                "contactgroups": {
                                    "groups": [],
                                    "recurse_perms": false,
                                    "recurse_use": false,
                                    "use": false,
                                    "use_for_services": false
                                },
                                "inventory_failed": false,
                                "ipaddress": "192.168.11.15",
                                "ipv6address": "",
                                "labels": {},
                                "locked_attributes": [],
                                "locked_by": {
                                    "instance_id": "",
                                    "program_id": "",
                                    "site_id": "maintestsite"
                                },
                                "management_address": "",
                                "management_ipmi_credentials": null,
                                "management_protocol": "none",
                                "management_snmp_community": null,
                                "meta_data": {
                                    "created_at": "2024-08-28T07:36:30.805379+00:00",
                                    "created_by": "cmkadmin",
                                    "updated_at": "2024-09-05T07:27:18.569235+00:00"
                                },
                                "network_scan": {
                                    "addresses": [],
                                    "exclude_addresses": [],
                                    "run_as": "cmkadmin",
                                    "scan_interval": 86400,
                                    "set_ip_address": true,
                                    "tag_criticality": "offline",
                                    "time_allowed": [
                                        {
                                            "end": "23:59:59",
                                            "start": "00:00:00"
                                        }
                                    ]
                                },
                                "network_scan_result": {
                                    "end": null,
                                    "output": "",
                                    "start": null,
                                    "state": "running"
                                },
                                "parents": [],
                                "site": "remotetestsite",
                                "snmp_community": null,
                                "tag_address_family": "ip-v4-only",
                                "tag_agent": "cmk-agent",
                                "tag_criticality": "prod",
                                "tag_networking": "lan",
                                "tag_piggyback": "auto-piggyback",
                                "tag_snmp_ds": "no-snmp",
                                "tag_testtaggroup": "None"
                            },
                            "folder": "/remote",
                            "is_cluster": false,
                            "is_offline": false
                        },
                        "id": "checkmk-server-remote",
                        "links": [],
                        "members": {},
                        "title": "checkmk-server-remote"
                    },
                    {
                        "domainType": "host_config",
                        "extensions": {
                            "attributes": {
                                "ipaddress": "192.168.222.11",
                                "meta_data": {
                                    "created_at": "2024-09-05T07:26:23.703024+00:00",
                                    "created_by": "cmkadmin",
                                    "updated_at": "2024-09-05T07:27:18.569319+00:00"
                                },
                                "site": "remotetestsite",
                                "tag_criticality": "test"
                            },
                            "cluster_nodes": null,
                            "effective_attributes": {
                                "additional_ipv4addresses": [],
                                "additional_ipv6addresses": [],
                                "alias": "",
                                "bake_agent_package": true,
                                "cmk_agent_connection": "pull-agent",
                                "contactgroups": {
                                    "groups": [],
                                    "recurse_perms": false,
                                    "recurse_use": false,
                                    "use": false,
                                    "use_for_services": false
                                },
                                "inventory_failed": false,
                                "ipaddress": "192.168.222.11",
                                "ipv6address": "",
                                "labels": {},
                                "locked_attributes": [],
                                "locked_by": {
                                    "instance_id": "",
                                    "program_id": "",
                                    "site_id": "maintestsite"
                                },
                                "management_address": "",
                                "management_ipmi_credentials": null,
                                "management_protocol": "none",
                                "management_snmp_community": null,
                                "meta_data": {
                                    "created_at": "2024-09-05T07:26:23.703024+00:00",
                                    "created_by": "cmkadmin",
                                    "updated_at": "2024-09-05T07:27:18.569319+00:00"
                                },
                                "network_scan": {
                                    "addresses": [],
                                    "exclude_addresses": [],
                                    "run_as": "cmkadmin",
                                    "scan_interval": 86400,
                                    "set_ip_address": true,
                                    "tag_criticality": "offline",
                                    "time_allowed": [
                                        {
                                            "end": "23:59:59",
                                            "start": "00:00:00"
                                        }
                                    ]
                                },
                                "network_scan_result": {
                                    "end": null,
                                    "output": "",
                                    "start": null,
                                    "state": "running"
                                },
                                "parents": [],
                                "site": "remotetestsite",
                                "snmp_community": null,
                                "tag_address_family": "ip-v4-only",
                                "tag_agent": "cmk-agent",
                                "tag_criticality": "test",
                                "tag_networking": "lan",
                                "tag_piggyback": "auto-piggyback",
                                "tag_snmp_ds": "no-snmp",
                                "tag_testtaggroup": "None"
                            },
                            "folder": "/remote",
                            "is_cluster": false,
                            "is_offline": false
                        },
                        "id": "testhost4",
                        "links": [],
                        "members": {},
                        "title": "testhost4"
                    },
                    {
                        "domainType": "host_config",
                        "extensions": {
                            "attributes": {
                                "meta_data": {
                                    "created_at": "2024-09-05T07:26:49+00:00",
                                    "created_by": "cmkadmin",
                                    "updated_at": "2024-09-05T07:27:18.569355+00:00"
                                },
                                "parents": [
                                    "testhost4"
                                ],
                                "site": "remotetestsite",
                                "tag_criticality": "test"
                            },
                            "cluster_nodes": null,
                            "effective_attributes": {
                                "additional_ipv4addresses": [],
                                "additional_ipv6addresses": [],
                                "alias": "",
                                "bake_agent_package": true,
                                "cmk_agent_connection": "pull-agent",
                                "contactgroups": {
                                    "groups": [],
                                    "recurse_perms": false,
                                    "recurse_use": false,
                                    "use": false,
                                    "use_for_services": false
                                },
                                "inventory_failed": false,
                                "ipaddress": "",
                                "ipv6address": "",
                                "labels": {},
                                "locked_attributes": [],
                                "locked_by": {
                                    "instance_id": "",
                                    "program_id": "",
                                    "site_id": "maintestsite"
                                },
                                "management_address": "",
                                "management_ipmi_credentials": null,
                                "management_protocol": "none",
                                "management_snmp_community": null,
                                "meta_data": {
                                    "created_at": "2024-09-05T07:26:49+00:00",
                                    "created_by": "cmkadmin",
                                    "updated_at": "2024-09-05T07:27:18.569355+00:00"
                                },
                                "network_scan": {
                                    "addresses": [],
                                    "exclude_addresses": [],
                                    "run_as": "cmkadmin",
                                    "scan_interval": 86400,
                                    "set_ip_address": true,
                                    "tag_criticality": "offline",
                                    "time_allowed": [
                                        {
                                            "end": "23:59:59",
                                            "start": "00:00:00"
                                        }
                                    ]
                                },
                                "network_scan_result": {
                                    "end": null,
                                    "output": "",
                                    "start": null,
                                    "state": "running"
                                },
                                "parents": [
                                    "testhost4"
                                ],
                                "site": "remotetestsite",
                                "snmp_community": null,
                                "tag_address_family": "ip-v4-only",
                                "tag_agent": "cmk-agent",
                                "tag_criticality": "test",
                                "tag_networking": "lan",
                                "tag_piggyback": "auto-piggyback",
                                "tag_snmp_ds": "no-snmp",
                                "tag_testtaggroup": "None"
                            },
                            "folder": "/remote",
                            "is_cluster": false,
                            "is_offline": false
                        },
                        "id": "testhost5",
                        "links": [],
                        "members": {},
                        "title": "testhost5"
                    },
                    {
                        "domainType": "host_config",
                        "extensions": {
                            "attributes": {
                                "meta_data": {
                                    "created_at": "2024-09-05T07:27:18.560244+00:00",
                                    "created_by": "cmkadmin",
                                    "updated_at": "2024-09-05T07:27:18.569386+00:00"
                                },
                                "site": "remotetestsite",
                                "tag_criticality": "critical"
                            },
                            "cluster_nodes": null,
                            "effective_attributes": {
                                "additional_ipv4addresses": [],
                                "additional_ipv6addresses": [],
                                "alias": "",
                                "bake_agent_package": true,
                                "cmk_agent_connection": "pull-agent",
                                "contactgroups": {
                                    "groups": [],
                                    "recurse_perms": false,
                                    "recurse_use": false,
                                    "use": false,
                                    "use_for_services": false
                                },
                                "inventory_failed": false,
                                "ipaddress": "",
                                "ipv6address": "",
                                "labels": {},
                                "locked_attributes": [],
                                "locked_by": {
                                    "instance_id": "",
                                    "program_id": "",
                                    "site_id": "maintestsite"
                                },
                                "management_address": "",
                                "management_ipmi_credentials": null,
                                "management_protocol": "none",
                                "management_snmp_community": null,
                                "meta_data": {
                                    "created_at": "2024-09-05T07:27:18.560244+00:00",
                                    "created_by": "cmkadmin",
                                    "updated_at": "2024-09-05T07:27:18.569386+00:00"
                                },
                                "network_scan": {
                                    "addresses": [],
                                    "exclude_addresses": [],
                                    "run_as": "cmkadmin",
                                    "scan_interval": 86400,
                                    "set_ip_address": true,
                                    "tag_criticality": "offline",
                                    "time_allowed": [
                                        {
                                            "end": "23:59:59",
                                            "start": "00:00:00"
                                        }
                                    ]
                                },
                                "network_scan_result": {
                                    "end": null,
                                    "output": "",
                                    "start": null,
                                    "state": "running"
                                },
                                "parents": [],
                                "site": "remotetestsite",
                                "snmp_community": null,
                                "tag_address_family": "ip-v4-only",
                                "tag_agent": "cmk-agent",
                                "tag_criticality": "critical",
                                "tag_networking": "lan",
                                "tag_piggyback": "auto-piggyback",
                                "tag_snmp_ds": "no-snmp",
                                "tag_testtaggroup": "None"
                            },
                            "folder": "/remote",
                            "is_cluster": false,
                            "is_offline": false
                        },
                        "id": "testhost6",
                        "links": [],
                        "members": {},
                        "title": "testhost6"
                    }
                ]
            }"""
            return host_config

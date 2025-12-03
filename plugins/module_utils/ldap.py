# Copyright: (c) 2023, Lars Getwan <lars.getwan@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

EXTEND_STATE = {
    "connection_suffix": "suffix",
    "connect_timeout": "seconds",
    "response_timeout": "seconds",
    "ldap_version": "version",
    "page_size": "size",
    "tcp_port": "port",
    "search_filter": "filter",
    "member_attribute": "attribute",
    "authentication_expiration": "attribute_to_sync",
    "disable_notifications": "attribute_to_sync",
    "main_menu_icons": "attribute_to_sync",
    "mega_menu_icons": "attribute_to_sync",
    "navigation_bar_icons": "attribute_to_sync",
    "pager": "attribute_to_sync",
    "show_mode": "attribute_to_sync",
    "start_url": "attribute_to_sync",
    "temperature_unit": "attribute_to_sync",
    "ui_sidebar_position": "attribute_to_sync",
    "ui_theme": "attribute_to_sync",
    "visibility_of_hosts_or_services": "attribute_to_sync",
    "filter_group": "filter",
    "user_id_attribute": "attribute",
    "alias": "attribute_to_sync",
    "email_address": "attribute_to_sync",
    "bind_credentials": None,
    "contact_group_membership": None,
    "groups_to_custom_user_attributes": None,
    "groups_to_roles": None,
}


def compress_recursive(d):
    if isinstance(d, dict):
        del_state_from = []
        del_key = []
        gtr = None

        for k, v in d.items():
            if isinstance(v, dict):
                if "state" in v:
                    if v.get("state") == "enabled":
                        if EXTEND_STATE[k]:
                            d[k] = v[EXTEND_STATE[k]]
                        else:
                            if k == "groups_to_roles":
                                # Handle this later not to mix up our dict now
                                gtr = v.copy()
                            else:
                                del_state_from.append(k)
                    else:
                        del_key.append(k)
                else:
                    v = compress_recursive(v)

        if gtr:
            old_gtr = d["groups_to_roles"].copy()
            del old_gtr["state"]

            if "handle_nested" in old_gtr:
                del old_gtr["handle_nested"]

            del gtr["state"]
            gtr["roles_to_sync"] = []
            to_be_deleted = []

            for role, groups in old_gtr.items():
                to_be_deleted.append(role)
                gtr["roles_to_sync"].append(
                    {
                        "role": role,
                        "groups": groups,
                    }
                )

            for role in to_be_deleted:
                del gtr[role]

            d["groups_to_roles"] = gtr

        for k in del_state_from:
            try:
                del d[k]["state"]
            except KeyError:
                pass

        for k in del_key:
            del d[k]

    return d


def extend_recursive(d):
    if isinstance(d, dict):
        to_be_deleted = []
        for k, v in d.items():
            if isinstance(v, dict):
                v = extend_recursive(d[k])
            if k in EXTEND_STATE:
                if not v:
                    d[k] = {"state": "disabled"}
                elif EXTEND_STATE[k]:
                    d[k] = {"state": "enabled", EXTEND_STATE[k]: v}
                else:
                    d[k] = {"state": "enabled"}

                    if k == "bind_credentials":
                        d[k].update(v)
                        if v.get("type") == "store":
                            del d[k]["explicit_password"]
                        else:
                            del d[k]["password_store_id"]
                    elif k == "contact_group_membership":
                        if "handle_nested" in v:
                            d[k]["handle_nested"] = v.get("handle_nested")
                        d[k]["sync_from_other_connections"] = v.get(
                            "sync_from_other_connections", []
                        )
                    elif k == "groups_to_custom_user_attributes":
                        if "handle_nested" in v:
                            d[k]["handle_nested"] = v.get("handle_nested")
                        d[k]["sync_from_other_connections"] = v.get(
                            "sync_from_other_connections", []
                        )
                        d[k]["groups_to_sync"] = v.get("groups_to_sync", [])
                    elif k == "groups_to_roles":
                        if "handle_nested" in v:
                            d[k]["handle_nested"] = v.get("handle_nested")
                        for role in v.get("roles_to_sync", []):
                            d[k][role["role"]] = role["groups"]
        for key in to_be_deleted:
            del d[key]

    return d

#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2022, Stefan Mühling <muehling.stefan@googlemail.com> & Robin Gierse <robin.gierse@tribe29.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: host_tag_group

short_description: Manage host_tag_group within Checkmk

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "0.0.1"

description:
- Manage host_tag_group within Checkmk.

extends_documentation_fragment: [tribe29.checkmk.common]

options:
    host_tag_group:
        description: The host_tag_group to be created/modified/deleted as returned by the Checkmk API.
        type: raw
    state:
        description: State of the host_tag_group.
        choices: [present, absent]
        default: present
        type: str

author:
    - Stefan Mühling (@muehlings)
"""

EXAMPLES = r"""
- name: "Create host_tag_group"
  tribe29.checkmk.host_tag_group:
    server_url: "https://localhost/"
    site: "my_site"
    automation_user: "automation"
    automation_secret: "$SECRET"
    host_tag_group:
      ident: Virtualization
      tags:
        - ident: No_Virtualization
          title: No Virtualization
        - ident: ESXi
          title: ESXi
        - ident: vCenter
          title: vCenter
        - ident: HyperV
          title: HyperV
        - ident: KVM
          title: KVM
      title: Virtualization
      topic: My_Tags
  state: present
"""

RETURN = r"""
http_code:
    description: The HTTP code the Checkmk API returns.
    type: int
    returned: always
    sample: '200'
message:
    description: The output message that the module generates.
    type: str
    returned: always
    sample: 'OK'
"""

import json

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url


def read_host_tag_group(module, base_url, headers):
    result = dict(
        changed=False,
        failed=False,
        http_code="",
        msg="",
        current_host_tag_group={},
        etag="",
    )

    current_state = "unknown"
    current_host_tag_group = dict(title="", topic="", tags=[], ident="")
    etag = ""

    api_endpoint = (
        "/objects/host_tag_group/" + module.params.get("host_tag_group")["ident"]
    )
    url = base_url + api_endpoint

    response, info = fetch_url(module, url, data=None, headers=headers, method="GET")

    response_content = ""

    http_code = info["status"]
    try:
        response_content = response.read()
        detail = str(json.loads(info["body"])["detail"]), str(
            json.loads(info["body"])["fields"]
        )
    except Exception:
        detail = response_content
    msg = info["msg"]
    # failed = ?

    if info["status"] == 200:
        current_state = "present"
        etag = info.get("etag", "")

        extensions = json.loads(response_content).get("extensions", {})
        current_host_tag_group["tags"] = extensions["tags"]
        current_host_tag_group["topic"] = extensions["topic"]
        current_host_tag_group["title"] = json.loads(response_content).get("title", "")
        current_host_tag_group["ident"] = json.loads(response_content).get("id", "")

        for d in current_host_tag_group["tags"]:
            d["ident"] = d.pop("id")
            d.pop("aux_tags")

    elif info["status"] == 404:
        current_state = "absent"

    else:
        failed = True

    result["current_host_tag_group"] = current_host_tag_group
    result["msg"] = str(http_code) + " - " + msg
    result["http_code"] = http_code
    result["state"] = current_state
    result["etag"] = etag

    return result


def create_host_tag_group(module, base_url, headers):
    result = dict(changed=False, failed=False, http_code="", msg="")

    changed = False
    failed = False
    http_code = ""

    host_tag_group = module.params.get("host_tag_group", {})

    api_endpoint = "/domain-types/host_tag_group/collections/all"
    url = base_url + api_endpoint
    response, info = fetch_url(
        module, url, module.jsonify(host_tag_group), headers=headers, method="POST"
    )

    http_code = info["status"]
    try:
        detail = str(json.loads(info["body"])["detail"]), str(
            json.loads(info["body"])["fields"]
        )
    except Exception:
        detail = ""
    msg = info["msg"]
    # failed = ?

    result["msg"] = str(http_code) + " - " + msg
    result["changed"] = changed
    result["failed"] = failed
    result["http_code"] = http_code
    result["info"] = info

    return result


def update_host_tag_group(module, base_url, headers, etag):
    result = dict(changed=False, failed=False, http_code="", msg="")

    changed = False
    failed = False
    http_code = ""

    host_tag_group = module.params.get("host_tag_group", {})
    host_tag_group["repair"] = True
    ident = host_tag_group.pop("ident")

    api_endpoint = "/objects/host_tag_group/" + ident
    url = base_url + api_endpoint
    headers["If-Match"] = etag
    response, info = fetch_url(
        module, url, module.jsonify(host_tag_group), headers=headers, method="PUT"
    )
    http_code = info["status"]
    try:
        detail = str(json.loads(info["body"])["detail"]), str(
            json.loads(info["body"])["fields"]
        )
    except Exception:
        detail = ""
    msg = info["msg"]
    # failed = ?

    result["msg"] = str(http_code) + " - " + msg
    result["changed"] = changed
    result["failed"] = failed
    result["http_code"] = http_code
    result["info"] = info

    return result


def delete_host_tag_group(module, base_url, headers, etag):
    result = dict(changed=False, failed=False, http_code="", msg="")

    changed = False
    failed = False
    http_code = ""

    host_tag_group = module.params.get("host_tag_group", {})
    host_tag_group["repair"] = True
    ident = host_tag_group.pop("ident")

    api_endpoint = "/objects/host_tag_group/" + ident
    url = base_url + api_endpoint
    headers["If-Match"] = etag
    response, info = fetch_url(
        module, url, module.jsonify(host_tag_group), headers=headers, method="DELETE"
    )

    http_code = info["status"]
    try:
        detail = str(json.loads(info["body"])["detail"]), str(
            json.loads(info["body"])["fields"]
        )
    except Exception:
        detail = ""
    msg = info["msg"]
    # failed = ?

    result["msg"] = str(http_code) + " - " + msg
    result["changed"] = changed
    result["failed"] = failed
    result["http_code"] = http_code
    result["info"] = info

    return result


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        server_url=dict(type="str", required=True),
        site=dict(type="str", required=True),
        automation_user=dict(type="str", required=True),
        automation_secret=dict(type="str", required=True, no_log=True),
        host_tag_group=dict(type="raw", default=[]),
        state=dict(type="str", default="present", choices=["present", "absent"]),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=False)

    # Declare headers including authentication to send to the Checkmk API
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer %s %s"
        % (
            module.params.get("automation_user", ""),
            module.params.get("automation_secret", ""),
        ),
    }

    state = module.params.get("state", "present")

    base_url = "%s/%s/check_mk/api/1.0" % (
        module.params.get("server_url", ""),
        module.params.get("site", ""),
    )

    # read current state (GET)
    result = read_host_tag_group(module, base_url, headers)

    if result["etag"] != "":
        # host_tag_group is "present"
        if (
            module.params.get("state") == "absent"
        ):  # host_tag_group needs to be deleted (DELETE)
            result = delete_host_tag_group(module, base_url, headers, result["etag"])
            result["changed"] = True
        elif (
            module.params.get("state") == "present"
        ):  # host_tag_group needs to be updated (PUT)
            pairs = zip(
                module.params.get("host_tag_group")["tags"],
                result["current_host_tag_group"]["tags"],
            )
            current_len = len(result["current_host_tag_group"]["tags"])
            current_etag = result["etag"]
            current_title = result["current_host_tag_group"]["title"]
            current_topic = result["current_host_tag_group"]["topic"]
            changed_len = False
            changed_content = False
            changed_title = False
            changed_topic = False
            if any(x != y for x, y in pairs):
                changed_content = True
            if len(module.params.get("host_tag_group")["tags"]) != current_len:
                changed_len = True
            if module.params.get("host_tag_group")["title"] != current_title:
                changed_title = True
            if module.params.get("host_tag_group")["topic"] != current_topic:
                changed_topic = True
            if changed_len or changed_content or changed_title or changed_topic:
                result = update_host_tag_group(module, base_url, headers, current_etag)
                result["changed"] = True  # different length

    else:
        # host_tag_group is "absent"
        if module.params.get("state") == "absent":
            # nothing to do
            result["changed"] = False
        elif module.params.get("state") == "present":
            # host_tag_group needs to be created (POST)
            result = create_host_tag_group(module, base_url, headers)
            result["changed"] = True

    if result["failed"]:
        module.fail_json(**result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()

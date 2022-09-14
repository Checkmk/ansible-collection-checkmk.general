#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2022, Stefan Mühling <muehling.stefan@googlemail.com> &
#                      Robin Gierse <robin.gierse@tribe29.com>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

import json

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url

__metaclass__ = type

DOCUMENTATION = r"""
---
module: tag_group

short_description: Manage tag_group within Checkmk

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "0.11.0"

description:
- Manage tag_group within Checkmk.

extends_documentation_fragment: [tribe29.checkmk.common]

options:
    id:
        description: The id of the tag_group to be created/
                     modified/deleted.
        default: ""
        type: string
    title:
        description: The title of the tag_group
        default: ""
        type: string
    topic:
        description: The topic of the tag_group
        default: ""
        type: string
    choices:
        description: The list of the tags for the tag_group as dicts.
        default: []
        type: list(dicts)

author:
    - Stefan Mühling (@muehlings)
"""

EXAMPLES = r"""
- name: "Create tag_group"
  tribe29.checkmk.tag_group:
    server_url: "https://localhost/"
    site: "my_site"
    automation_user: "automation"
    automation_secret: "$SECRET"
    id: Virtualization
    title: Virtualization
    topic: My_Tags
    choices:
        - id: No_Virtualization
          title: No Virtualization
        - id: ESXi
          title: ESXi
        - id: vCenter
          title: vCenter
        - id: HyperV
          title: HyperV
        - id: KVM
          title: KVM
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


def read_tag_group(module, base_url, headers):
    result = dict(
        changed=False, failed=False, http_code="", msg="", current_tag_group={}, etag=""
    )

    current_state = "unknown"
    current_tag_group = dict(title="", topic="", tags=[], ident="")
    etag = ""

    ident = module.params.get("id", "")

    api_endpoint = "/objects/host_tag_group/" + ident
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

    if info["status"] == 200:
        current_state = "present"
        etag = info.get("etag", "")

        extensions = json.loads(response_content).get("extensions", {})
        current_tag_group["tags"] = extensions["tags"]
        current_tag_group["topic"] = extensions["topic"]
        current_tag_group["title"] = json.loads(response_content).get("title", "")
        current_tag_group["ident"] = json.loads(response_content).get("id", "")

        for d in current_tag_group["tags"]:
            d["ident"] = d.pop("id")
            d.pop("aux_tags")

    elif info["status"] == 404:
        current_state = "absent"

    else:
        failed = True

    result["current_tag_group"] = current_tag_group
    result["msg"] = str(http_code) + " - " + msg
    result["http_code"] = http_code
    result["state"] = current_state
    result["etag"] = etag

    return result


def create_tag_group(module, base_url, headers):
    result = dict(changed=False, failed=False, http_code="", msg="")

    changed = False
    failed = False
    http_code = ""

    ident = module.params.get("id", "")
    tag_group = {}
    tag_group["ident"] = ident
    tag_group["title"] = module.params.get("title", "")
    tag_group["topic"] = module.params.get("topic", "")
    tag_group["tags"] = module.params.get("choices", "")
    for d in tag_group["tags"]:
        d["ident"] = d.pop("id")

    api_endpoint = "/domain-types/host_tag_group/collections/all"
    url = base_url + api_endpoint
    response, info = fetch_url(
        module, url, module.jsonify(tag_group), headers=headers, method="POST"
    )

    http_code = info["status"]
    try:
        response_content = response.read()
        detail = str(json.loads(info["body"])["detail"]), str(
            json.loads(info["body"])["fields"]
        )
    except Exception:
        detail = ""
    msg = info["msg"]

    if info["status"] != 200:
        failed = True

    result["msg"] = str(http_code) + " - " + msg
    result["changed"] = changed
    result["failed"] = failed
    result["http_code"] = http_code
    result["info"] = info

    return result


def update_tag_group(module, base_url, headers, etag):
    result = dict(changed=False, failed=False, http_code="", msg="")

    changed = False
    failed = False
    http_code = ""

    ident = module.params.get("id", "")
    tag_group = {}
    tag_group["repair"] = True
    tag_group["title"] = module.params.get("title", "")
    tag_group["topic"] = module.params.get("topic", "")
    tag_group["tags"] = module.params.get("choices", "")
    for d in tag_group["tags"]:
        d["ident"] = d.pop("id")

    api_endpoint = "/objects/host_tag_group/" + ident
    url = base_url + api_endpoint
    headers["If-Match"] = etag
    response, info = fetch_url(
        module, url, module.jsonify(tag_group), headers=headers, method="PUT"
    )

    http_code = info["status"]
    try:
        response_content = response.read()
        detail = str(json.loads(info["body"])["detail"]), str(
            json.loads(info["body"])["fields"]
        )
    except Exception:
        detail = ""
    msg = info["msg"]

    if info["status"] != 200:
        failed = True

    result["msg"] = str(http_code) + " - " + msg
    result["changed"] = changed
    result["failed"] = failed
    result["http_code"] = http_code
    result["info"] = info

    return result


def delete_tag_group(module, base_url, headers, etag):
    result = dict(changed=False, failed=False, http_code="", msg="")

    changed = False
    failed = False
    http_code = ""

    ident = module.params.get("id")
    tag_group = {}
    tag_group["repair"] = True
    tag_group["title"] = module.params.get("title", "")
    tag_group["topic"] = module.params.get("topic", "")
    tag_group["tags"] = module.params.get("choices", "")
    for d in tag_group["tags"]:
        d["ident"] = d.pop("id")

    api_endpoint = "/objects/host_tag_group/" + ident
    url = base_url + api_endpoint
    headers["If-Match"] = etag
    response, info = fetch_url(
        module, url, module.jsonify(tag_group), headers=headers, method="DELETE"
    )

    http_code = info["status"]
    try:
        response_content = response.read()
        detail = str(json.loads(info["body"])["detail"]), str(
            json.loads(info["body"])["fields"]
        )
    except Exception:
        detail = ""
    msg = info["msg"]

    if info["status"] != 204:
        failed = True

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
        title=dict(type="str", default=""),
        id=dict(type="str", default=""),
        topic=dict(type="str", default=""),
        choices=dict(type="list", default=[]),
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
    result = read_tag_group(module, base_url, headers)
    msg_tokens = []

    # tag_group is "present"
    if result["etag"] != "":
        # tag_group needs to be deleted (DELETE)
        if module.params.get("state") == "absent":
            result = delete_tag_group(module, base_url, headers, result["etag"])
            msg_tokens.append("Tag group deleted.")
            result["changed"] = True
        # tag_group needs to be updated (PUT)
        elif module.params.get("state") == "present":
            choices = module.params.get("choices")
            current_choices = result["current_tag_group"]["tags"]
            for d in current_choices:
                d["id"] = d.pop("ident")
            pairs = zip(choices, current_choices)
            current_len = len(current_choices)
            current_etag = result["etag"]
            current_title = result["current_tag_group"]["title"]
            current_topic = result["current_tag_group"]["topic"]
            changed_len = False
            changed_content = False
            changed_title = False
            changed_topic = False
            if not all([a == b for a, b in pairs]):
                changed_content = True
                msg_tokens.append("Content of choices changed.")
            if len(module.params.get("choices")) != current_len:
                changed_len = True
                msg_tokens.append("Number of choices changed.")
            if module.params.get("title") != current_title:
                changed_title = True
                msg_tokens.append("Title changed.")
            if module.params.get("topic") != current_topic:
                changed_topic = True
                msg_tokens.append("Topic changed.")
            if (
                changed_content is True
                or changed_len is True
                or changed_title is True
                or changed_topic is True
            ):
                result = update_tag_group(module, base_url, headers, current_etag)
                result["changed"] = True
            else:
                msg_tokens.append("Tag group as desired. Nothing to do.")

    else:
        # tag_group is "absent"
        if module.params.get("state") == "absent":
            # nothing to do
            msg_tokens.append("Nothing to do.")
            result["changed"] = False
        elif module.params.get("state") == "present":
            # tag_group needs to be created (POST)
            result = create_tag_group(module, base_url, headers)
            msg_tokens.append("Tag group created.")
            result["changed"] = True

    if len(msg_tokens) > 0:
        result["msg"] = " ".join(msg_tokens)

    if result["failed"]:
        module.fail_json(**result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()

#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2023, Max Sickora <max.sickora@checkmk.com> &
#                      Stefan Mühling <muehling.stefan@googlemail.com>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: tag_group

short_description: Manage tag groups in Checkmk.

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "0.11.0"

description:
- Manage tag groups in Checkmk.

extends_documentation_fragment: [checkmk.general.common]

options:
    help:
        description: The help text for the tag group.
        default: ""
        type: str
    name:
        description: The name of the tag group to manage.
        required: true
        type: str
        aliases: ["id"]
    repair:
        description:
            - Give permission to update or remove the tag on hosts using it automatically.
              B(Use with caution!)
        default: False
        type: bool
    state:
        description: The desired state.
        default: "present"
        choices: ["present", "absent"]
        type: str
    tags:
        description: A list of the tag groups to be created.
        default: []
        type: list
        elements: dict
        aliases: ["choices"]
        suboptions:
            id:
                description: The id of the tag
                required: true
                type: str
            title:
                description: The title of the tag
                required: true
                type: str
    title:
        description: The title of the tag group.
        default: ""
        type: str
    topic:
        description: The topic of the tag group.
        default: ""
        type: str

author:
    - Max Sickora (@Max-checkmk)
    - Stefan Mühling (@muehlings)
"""

EXAMPLES = r"""
# Create a tag group
- name: "Create tag group"
  checkmk.general.tag_group:
    server_url: "https://myserver/"
    site: "mysite"
    automation_user: "myuser"
    automation_secret: "mysecret"
    name: datacenter
    title: Datacenter
    topic: Tags
    help: "The datacenter this host resides in."
    tags:
      - id: datacenter_none
        title: No Datacenter
      - id: datacenter_1
        title: Datacenter 2
      - id: datacenter_2
        title: Datacenter 2
      - id: datacenter_3
        title: Datacenter 3
    state: present

# Delete a tag group
- name: "Delete tag group."
  checkmk.general.tag_group:
    server_url: "https://myserver/"
    site: "mysite"
    automation_user: "myuser"
    automation_secret: "mysecret"
    name: datacenter
    state: "absent"
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
import time

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.checkmk.general.plugins.module_utils.api import CheckmkAPI
from ansible_collections.checkmk.general.plugins.module_utils.types import RESULT
from ansible_collections.checkmk.general.plugins.module_utils.utils import (
    result_as_dict,
)
from ansible_collections.checkmk.general.plugins.module_utils.version import (
    CheckmkVersion,
)

# We count 404 not as failed, because we want to know if the taggroup exists or not.
HTTP_CODES_GET = {
    # http_code: (changed, failed, "Message")
    404: (False, False, "Not Found: The requested object has not been found."),
}


def normalize_data(raw_data, ver):
    data = {
        "title": raw_data.get("title", ""),
        "topic": raw_data.get("topic", ""),
        "help": raw_data.get("help", ""),
        "tags": raw_data.get("tags", ""),
        "repair": raw_data.get("repair"),
    }

    # Remove all keys without value, as they would be emptied.
    data = {key: val for key, val in data.items() if val}

    # The API uses "ident" instead of "id" for the put & post endpoints
    if "tags" in data:
        for d in data["tags"]:
            if "id" in d and ver < CheckmkVersion("2.4.0"):
                d["ident"] = d.pop("id")

    return data


class TaggroupAPI(CheckmkAPI):
    def __init__(self, module):
        super().__init__(module)

        data = {}
        # Get current taggroup
        self.current = self._fetch(
            code_mapping=HTTP_CODES_GET,
            endpoint="/objects/host_tag_group/%s" % self.params.get("name"),
            data=data,
            method="GET",
        )

        # Get Checkmk-version
        self.ver = self.getversion()

    def post(self):  # Create taggroup
        if not self.params.get("title") or not self.params.get("tags"):
            result = RESULT(
                http_code=0,
                msg="Need parameter title and tags to create hosttag",
                content="",
                etag="",
                failed=True,
                changed=False,
            )
            return result

        else:
            data = normalize_data(self.params, self.ver)
            if self.ver < CheckmkVersion("2.4.0"):
                data["ident"] = self.params.get("name")
            else:
                data["id"] = self.params.get("name")

            return self._fetch(
                endpoint="/domain-types/host_tag_group/collections/all",
                data=data,
                method="POST",
            )

    def put(self):  # Update taggroup
        data = normalize_data(self.params, self.ver)

        return self._fetch(
            endpoint="/objects/host_tag_group/%s" % self.params.get("name"),
            data=data,
            method="PUT",
        )

    def delete(self):  # Remove taggroup
        data = {}

        return self._fetch(
            endpoint="/objects/host_tag_group/%s?repair=%s"
            % (self.params.get("name"), self.params.get("repair")),
            # data=data,
            method="DELETE",
        )


def changes_detected(module, current):
    if module.params.get("title") != current.get("title"):
        # The title has changed
        return True

    if module.params.get("topic") != current.get("extensions", {}).get("topic"):
        # The topic has changed
        return True

    desired_tags = module.params.get("tags")
    current_tags = current.get("extensions", {}).get("tags", [])

    if len(desired_tags) != len(current_tags):
        # The number of tags has changed
        return True

    for d in current_tags:
        d.pop("aux_tags")

    pairs = zip(desired_tags, current_tags)

    if not all(a == b for a, b in pairs):
        # At least one of the tags or the order has changed
        return True

    return False


def run_module():
    module_args = dict(
        server_url=dict(type="str", required=True),
        site=dict(type="str", required=True),
        validate_certs=dict(type="bool", required=False, default=True),
        automation_user=dict(type="str", required=True),
        automation_secret=dict(type="str", required=True, no_log=True),
        title=dict(type="str", default=""),
        name=dict(type="str", required=True, aliases=["id"]),
        topic=dict(type="str", default=""),
        help=dict(type="str", default=""),
        tags=dict(
            type="list",
            elements="dict",
            default=[],
            aliases=["choices"],
            options=dict(
                id=dict(type="str", required=True),
                title=dict(type="str", required=True),
            ),
        ),
        repair=dict(type="bool", default=False),
        state=dict(type="str", default="present", choices=["present", "absent"]),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=False)

    result = RESULT(
        http_code=0,
        msg="Nothing to be done",
        content="",
        etag="",
        failed=False,
        changed=False,
    )

    taggroup = TaggroupAPI(module)

    if module.params.get("state") == "present":
        if taggroup.current.http_code == 200:
            # If tag group has changed then update it.
            if changes_detected(
                module, json.loads(taggroup.current.content.decode("utf-8"))
            ):
                taggroup.headers["If-Match"] = taggroup.current.etag
                result = taggroup.put()

                time.sleep(3)

        elif taggroup.current.http_code == 404:
            # Tag group is not there. Create it.

            result = taggroup.post()

            time.sleep(3)

    if module.params.get("state") == "absent":
        # Only delete if the Taggroup exists
        if taggroup.current.http_code == 200:
            result = taggroup.delete()

            time.sleep(3)
        elif taggroup.current.http_code == 404:
            result = RESULT(
                http_code=0,
                msg="Taggroup doesn't exist.",
                content="",
                etag="",
                failed=False,
                changed=False,
            )

    module.exit_json(**result_as_dict(result))


def main():
    run_module()


if __name__ == "__main__":
    main()

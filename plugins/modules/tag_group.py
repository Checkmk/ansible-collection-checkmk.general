#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2023, Max Sickora <max.sickora@checkmk.com> &
#                      Stefan Mühling <muehling.stefan@googlemail.com> &
#                      Robin Gierse <robin.gierse@checkmk.com>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

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

extends_documentation_fragment: [checkmk.general.common]

options:
    name:
        description: The name of the tag_group to be created/
                     modified/deleted.
        default: ""
        type: str
        aliases: ["id"]
    title:
        description: The title of the tag_group
        default: ""
        type: str
    topic:
        description: The topic of the tag_group
        default: ""
        type: str
    help:
        description: The help of the tag_group
        default: ""
        type: str
    tags:
        description: The list of the tags for the tag_group as dicts.
        default: []
        type: list
        elements: dict
        aliases: ["choices"]
    repair:
        description: Give permission to update or remove the tag automatically on hosts using it.
        default: "False"
        type: bool
    state:
        description: The desired state
        default: "present"
        choices: ["present", "absent"]
        type: str

author:
    - Max Sickora (@Max-checkmk)
"""

EXAMPLES = r"""
# Create a tag group
- name: "Create tag_group"
  checkmk.general.tag_group:
    server_url: "https://localhost/"
    site: "my_site"
    automation_user: "my_user"
    automation_secret: "my_secret"
    name: Datacenter
    title: Datacenter
    topic: Tags
    help: "something useful"
    tags:
      - ident: No_Datacenter
        title: No Datacenter
      - ident: Datacenter 1
        title: Datacenter 2
      - ident: Datacenter 2
        title: Datacenter 2
      - ident: Datacenter US
        title: Datacenter US
      - ident: Datacenter ASIA
        title: Datacenter ASIA
    state: present

# Delete a tag group
- name: "Delete tag_group."
  checkmk.general.tag_group:
    server_url: "https://localhost/"
    site: "my_site"
    automation_user: "my_user"
    automation_secret: "my_secret"
    name: Datacenter
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

# from ansible_collections.checkmk.general.plugins.module_utils.version import (
#     CheckmkVersion,
# )

# We count 404 not as failed, because we want to know if the taggroup exists or not.
HTTP_CODES_GET = {
    # http_code: (changed, failed, "Message")
    200: (True, False, "OK: The operation was done successfully."),
    404: (False, False, "Not Found: The requested object has not been found."),
    500: (False, True, "General Server Error."),
}

HTTP_CODES_DELETE = {
    # http_code: (changed, failed, "Message")
    405: (
        False,
        True,
        "Method Not Allowed: This request is only allowed with other HTTP methods",
    ),
    500: (False, True, "General Server Error."),
}

HTTP_CODES_CREATE = {
    # http_code: (changed, failed, "Message")
    200: (True, False, "OK: The operation was done successfully."),
    500: (False, True, "General Server Error."),
}

HTTP_CODES_UPDATE = {
    # http_code: (changed, failed, "Message")
    200: (True, False, "OK: The operation was done successfully."),
    401: (False, True, "Unauthorized: The user is not authorized to do this request"),
    405: (
        False,
        True,
        "Method Not Allowed: This request is only allowed with other HTTP methods",
    ),
    500: (False, True, "General Server Error."),
}


class TaggroupCreateAPI(CheckmkAPI):
    def post(self):
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
            data = {
                "ident": self.params.get("name", ""),
                "title": self.params.get("title", ""),
                "topic": self.params.get("topic", ""),
                "help": self.params.get("help", ""),
                "tags": self.params.get("tags", ""),
            }

            # Remove all keys without value, as otherwise they would be None.
            data = {key: val for key, val in data.items() if val}

            return self._fetch(
                code_mapping=HTTP_CODES_CREATE,
                endpoint="/domain-types/host_tag_group/collections/all",
                data=data,
                method="POST",
            )


class TaggroupUpdateAPI(CheckmkAPI):
    def put(self):
        data = {
            "title": self.params.get("title", ""),
            "topic": self.params.get("topic", ""),
            "help": self.params.get("help", ""),
            "tags": self.params.get("tags", ""),
            "repair": self.params.get("repair"),
        }

        # Remove all keys without value, as they would be emptied.
        data = {key: val for key, val in data.items() if val}

        return self._fetch(
            code_mapping=HTTP_CODES_UPDATE,
            endpoint="/objects/host_tag_group/%s" % self.params.get("name"),
            data=data,
            method="PUT",
        )


class TaggroupDeleteAPI(CheckmkAPI):
    def delete(self):
        data = {
            "repair": self.params.get("repair"),
        }

        return self._fetch(
            code_mapping=HTTP_CODES_DELETE,
            endpoint="/objects/host_tag_group/%s" % self.params.get("name"),
            data=data,
            method="DELETE",
        )


class TaggroupGetAPI(CheckmkAPI):
    def get(self):
        data = {}

        return self._fetch(
            code_mapping=HTTP_CODES_GET,
            endpoint="/objects/host_tag_group/%s" % self.params.get("name"),
            data=data,
            method="GET",
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
        d["ident"] = d.pop("id")
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
        name=dict(type="str", default="", aliases=["id"]),
        topic=dict(type="str", default=""),
        help=dict(type="str", default=""),
        tags=dict(type="list", elements="dict", default=[], aliases=["choices"]),
        repair=dict(type="bool", default="False"),
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

    if module.params.get("state") == "present":
        taggroupget = TaggroupGetAPI(module)
        current = taggroupget.get()

        if current.http_code == 200:
            # If tag group has changed then update it.
            if changes_detected(module, json.loads(current.content.decode("utf-8"))):
                taggroupupdate = TaggroupUpdateAPI(module)
                taggroupupdate.headers["If-Match"] = current.etag
                result = taggroupupdate.put()

                time.sleep(3)

        elif current.http_code == 404:
            # Tag group is not there. Create it.
            taggroupcreate = TaggroupCreateAPI(module)

            result = taggroupcreate.post()

            time.sleep(3)

    if module.params.get("state") == "absent":
        taggroupdelete = TaggroupDeleteAPI(module)
        result = taggroupdelete.delete()

        time.sleep(3)

    module.exit_json(**result_as_dict(result))


def main():
    run_module()


if __name__ == "__main__":
    main()

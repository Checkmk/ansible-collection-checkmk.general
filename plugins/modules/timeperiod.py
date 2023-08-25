#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2023, Max Sickora <max.sickora@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: timeperiod

short_description: Manage time periods in checkmk.

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "3.3.0"

description:
- Manage time periods in checkmk.

extends_documentation_fragment: [checkmk.general.common]

options:
    name:
        description: An unique identifier for the time period.
        required: true
        type: str

    alias:
        description: An alias for the time period.
        required: false
        type: str

    active_time_ranges:
        description: The list of active time ranges.
        required: false
        type: raw

    exceptions:
        description: A list of additional time ranges to be added.
        required: false
        type: raw

    exclude:
        description: A list of time period aliases whose periods are excluded.
        required: false
        type: raw

    state:
        description: create/update or delete a time period.
        required: true
        choices: ["present", "absent"]
        type: str

author:
    - Max Sickora (@max-checkmk)
"""

EXAMPLES = r"""
# Creating and Updating is the same.
- name: "Create a new time period."
  checkmk.general.timeperiod:
    server_url: "http://localhost/"
    site: "my_site"
    automation_user: "automation"
    automation_secret: "$SECRET"
    name: "worktime"
    title: "Work time"
    active_time_ranges: [
    exceptions: [

    ]
    ]
    exclude: [
        "lunch"
    ]
    state: "present"

- name: "Delete a time period."
  checkmk.general.timeperiod:
    server_url: "http://localhost/"
    site: "my_site"
    automation_user: "automation"
    automation_secret: "$SECRET"
    name: "worktime"
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
    sample: 'Done.'
"""

import time
import json

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.checkmk.general.plugins.module_utils.api import CheckmkAPI
from ansible_collections.checkmk.general.plugins.module_utils.types import RESULT
from ansible_collections.checkmk.general.plugins.module_utils.utils import (
    result_as_dict,
)

# We count 404 not as failed, because we want to know if the time period exists or not.
HTTP_CODES_GET = {
    # http_code: (changed, failed, "Message")
    200: (True, False, "OK: The operation was done successfully."),
    400: (False, True, "Bad Request: Parameter or validation failure."),
    403: (False, True, "Forbidden: Configuration via Setup is disabled."),
    404: (False, False, "Not Found: The requested object has not been found."),
    406: (
        False,
        True,
        "Not Acceptable: The requests accept headers can not be satisfied.",
    ),
    415: (
        False,
        True,
        "Unsupported Media Type: The submitted content-type is not supported.",
    ),
    500: (False, True, "General Server Error."),
}

HTTP_CODES_DELETE = {
    # http_code: (changed, failed, "Message")
    204: (True, False, "No Content: Operation done successfully. No further output."),
    400: (False, True, "Bad Request: Parameter or validation failure."),
    403: (False, True, "Forbidden: Configuration via Setup is disabled."),
    404: (False, True, "Not Found: The requested object has not been found."),
    405: (
        False,
        True,
        "Method Not Allowed: This request is only allowed with other HTTP methods",
    ),
    406: (
        False,
        True,
        "Not Acceptable: The requests accept headers can not be satisfied.",
    ),
    412: (
        False,
        True,
        "Precondition Failed: The value of the If-Match header doesn't match the object's ETag.",
    ),
    415: (
        False,
        True,
        "Unsupported Media Type: The submitted content-type is not supported.",
    ),
    428: (
        False,
        True,
        "Precondition Required: The required If-Match header is missing",
    ),
    500: (False, True, "General Server Error."),
}

HTTP_CODES_CREATE = {
    # http_code: (changed, failed, "Message")
    200: (True, False, "OK: The operation was done successfully."),
    400: (False, True, "Bad Request: Parameter or validation failure."),
    403: (False, True, "Forbidden: Configuration via Setup is disabled."),
    406: (
        False,
        True,
        "Not Acceptable: The requests accept headers can not be satisfied.",
    ),
    415: (
        False,
        True,
        "Unsupported Media Type: The submitted content-type is not supported.",
    ),
    500: (False, True, "General Server Error."),
}

HTTP_CODES_UPDATE = {
    # http_code: (changed, failed, "Message")
    200: (
        True,
        False,
        "No Content: Operation was done successfully. No further output",
    ),
    403: (False, True, "Forbidden: Configuration via Setup is disabled."),
    404: (False, True, "Not Found: The requested object has not been found."),
    405: (
        False,
        True,
        "Method Not Allowed: This request is only allowed with other HTTP methods",
    ),
    406: (
        False,
        True,
        "Not Acceptable: The requests accept headers can not be satisfied.",
    ),
    412: (
        False,
        True,
        "Precondition Failed: The value of the If-Match header doesn't match the object's ETag.",
    ),
    415: (
        False,
        True,
        "Unsupported Media Type: The submitted content-type is not supported.",
    ),
    428: (
        False,
        True,
        "Precondition Required: The required If-Match header is missing",
    ),
    500: (False, True, "General Server Error."),
}


class TimeperiodCreateAPI(CheckmkAPI):
    def post(self):
        data = {
            "name": self.params.get("name", ""),
            "alias": self.params.get("alias", ""),
            "active_time_ranges": self.params.get("active_time_ranges", ""),
        }

        if self.params.get("exceptions") is not None:
            data["exceptions"] = self.params.get("exceptions")

        if self.params.get("exclude") is not None:
            data["exclude"] = self.params.get("exclude")

        return self._fetch(
            code_mapping=HTTP_CODES_CREATE,
            endpoint="/domain-types/time_period/collections/all",
            data=data,
            method="POST",
        )


class TimeperiodUpdateAPI(CheckmkAPI):
    def put(self, existingalias):
        data = {}
        if (
            self.params.get("alias") is not None
            and self.params.get("alias") is not existingalias
        ):
            data["alias"] = self.params.get("alias")

        if self.params.get("active_time_ranges") is not None:
            data["active_time_ranges"] = self.params.get("active_time_ranges")

        if self.params.get("exceptions") is not None:
            data["exceptions"] = self.params.get("exceptions")

        if self.params.get("exclude") is not None:
            data["exclude"] = self.params.get("exclude")

        return self._fetch(
            code_mapping=HTTP_CODES_UPDATE,
            endpoint="/objects/time_period/%s" % self.params.get("name"),
            data=data,
            method="PUT",
        )


class TimeperiodDeleteAPI(CheckmkAPI):
    def delete(self):
        data = {}

        return self._fetch(
            code_mapping=HTTP_CODES_DELETE,
            endpoint="/objects/time_period/%s" % self.params.get("name"),
            data=data,
            method="DELETE",
        )


class TimeperiodGetAPI(CheckmkAPI):
    def get(self):
        data = {}

        return self._fetch(
            code_mapping=HTTP_CODES_GET,
            endpoint="/objects/time_period/%s" % self.params.get("name"),
            data=data,
            method="GET",
        )


def patched_version(checkmkversion):
    if (
        checkmkversion[0] == "2"
        and checkmkversion[1] == "2"
        and int(checkmkversion[2]) >= 9
    ):
        return True
    if (
        checkmkversion[0] == "2"
        and checkmkversion[1] == "1"
        and int(checkmkversion[2]) >= 33
    ):
        return True
    return False


def run_module():
    module_args = dict(
        server_url=dict(type="str", required=True),
        site=dict(type="str", required=True),
        validate_certs=dict(type="bool", required=False, default=True),
        automation_user=dict(type="str", required=True),
        automation_secret=dict(type="str", required=True, no_log=True),
        name=dict(type="str", required=True),
        alias=dict(type="str", required=False),
        active_time_ranges=dict(type="raw", required=False),
        exceptions=dict(type="raw", required=False),
        exclude=dict(type="raw", required=False),
        state=dict(
            type="str",
            choices=["present", "absent"],
            required=True,
        ),
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
        timeperiodget = TimeperiodGetAPI(module)
        result = timeperiodget.get()

        # Time period exists already - Do an update.
        if result.http_code == 200:
            checkmkversion = timeperiodget.getversion()

            if module.params.get("exclude") and not patched_version(checkmkversion):
                result = RESULT(
                    http_code=0,
                    msg="Can't update exclude value in Checkmk 2.2.0p8 or 2.1.0p32 and before. See Werk #16052",
                    content="",
                    etag="",
                    failed=True,
                    changed=False,
                )
                module.fail_json(**result_as_dict(result))

            timeperiodupdate = TimeperiodUpdateAPI(module)
            timeperiodupdate.headers["If-Match"] = result.etag
            # Different output of "Show a time period" in Version 2.0
            if checkmkversion[0] == "2" and checkmkversion[1] == "0":
                existingalias = json.loads(result.content).get("alias")
            else:
                existingalias = (
                    json.loads(result.content).get("extensions").get("alias")
                )
            result = timeperiodupdate.put(existingalias)

            time.sleep(3)

        # Time period doesn't exist - Create new one.
        elif result.http_code == 404:
            timeperiodcreate = TimeperiodCreateAPI(module)
            result = timeperiodcreate.post()

            time.sleep(3)

    if module.params.get("state") == "absent":
        timeperiodget = TimeperiodGetAPI(module)
        result = timeperiodget.get()

        if result.http_code == 200:
            timeperioddelete = TimeperiodDeleteAPI(module)
            timeperioddelete.headers["If-Match"] = result.etag
            result = timeperioddelete.delete()

            time.sleep(3)

        elif result.http_code == 404:
            result = RESULT(
                http_code=404,
                msg="Time period doesn't exist.",
                content="",
                etag="",
                failed=True,
                changed=False,
            )

            time.sleep(3)

    module.exit_json(**result_as_dict(result))


def main():
    run_module()


if __name__ == "__main__":
    main()

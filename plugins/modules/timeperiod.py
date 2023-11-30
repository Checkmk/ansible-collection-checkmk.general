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
- name: "Create a new time period. (Attributes in one line)"
  checkmk.general.timeperiod:
    server_url: "http://my_server/"
    site: "my_site"
    automation_user: "my_user"
    automation_secret: "my_secret"
    name: "worktime"
    title: "Worktime"
    active_time_ranges: '[{"day": "all", "time_ranges": [{"start": "09:00:00", "end": "17:00:00"}]}]'
    exceptions: '[{"date": "2023-12-24", "time_ranges": [{"start": "10:00:00", "end": "12:00:00"}]}]'
    exclude: '[ "Lunchtime" ]'
    state: "present"

- name: "Create a new time period. (Attributes in multiple lines)"
  checkmk.general.timeperiod:
    server_url: "http://my_server/"
    site: "my_site"
    automation_user: "my_user"
    automation_secret: "my_secret"
    name: "worktime"
    title: "Worktime"
    active_time_ranges: [
              {
                  "day": "all",
                  "time_ranges": [
                      {
                          "start": "8:00",
                          "end": "17:00"
                      }
                  ]
              },
          ]
    exceptions: [
              {
                  "date": "2023-12-24",
                  "time_ranges": [
                      {
                          "start": "8:00",
                          "end": "12:00"
                      }
                  ]
              },
          ]
    exclude: [
         "Lunchtime"
          ]
    state: "present"

- name: "Delete a time period."
  checkmk.general.timeperiod:
    server_url: "http://my_server/"
    site: "my_site"
    automation_user: "my_user"
    automation_secret: "my_secret"
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

import json
import time
from datetime import datetime

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.checkmk.general.plugins.module_utils.api import CheckmkAPI
from ansible_collections.checkmk.general.plugins.module_utils.types import RESULT
from ansible_collections.checkmk.general.plugins.module_utils.utils import (
    result_as_dict,
)
from ansible_collections.checkmk.general.plugins.module_utils.version import (
    CheckmkVersion,
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

updatevalues = ("alias", "active_time_ranges", "exceptions", "exclude")


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
        # In case of "alias" the API will respond with an error,
        # if the existing alias is the same as the new one.
        # So at this point we check if new and old are equal
        # and skip the value if that's the case.
        if self.params.get("alias") and self.params.get("alias") != existingalias:
            data["alias"] = self.params.get("alias")

        if self.params.get("active_time_ranges"):
            data["active_time_ranges"] = self.params.get("active_time_ranges")

        if self.params.get("exceptions"):
            data["exceptions"] = self.params.get("exceptions")

        if self.params.get("exclude"):
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


def patched_version(ver):
    if ver > CheckmkVersion("2.1.0p32") and ver < CheckmkVersion("2.2.0"):
        return True
    if ver > CheckmkVersion("2.2.0p8"):
        return True
    return False


# Correct every timerange (all to single days and summarize every day)
def correct_timerange(active_time_ranges):
    all_days = [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    ]
    new_timeranges = []
    for day in all_days:
        timeranges = []
        for time_range in active_time_ranges:
            if time_range["day"] == "all" or time_range["day"] == day:
                timeranges.extend(time_range["time_ranges"])
        if timeranges:
            new_timeranges.append({"day": day, "time_ranges": timeranges})
    return new_timeranges


# Sort new and existing timeranges (exceptions get sorted by date also)
def sort_timerange(time_ranges):
    time_ranges["time_ranges"] = sorted(
        time_ranges["time_ranges"], key=lambda d: d["start"]
    )
    return time_ranges


# Correct timeformat 08:00:00 / 8:00 -> 08:00
def correct_timeformat(time_ranges):
    for time_range in time_ranges["time_ranges"]:
        try:  # Try with seconds
            time_range["start"] = (
                datetime.strptime(time_range["start"], "%H:%M:%S")
            ).strftime("%H:%M")
            time_range["end"] = (
                datetime.strptime(time_range["end"], "%H:%M:%S")
            ).strftime("%H:%M")
        except ValueError:  # In Case of ValueError without seconds
            time_range["start"] = (
                datetime.strptime(time_range["start"], "%H:%M")
            ).strftime("%H:%M")
            time_range["end"] = (
                datetime.strptime(time_range["end"], "%H:%M")
            ).strftime("%H:%M")
    return time_ranges


def existingnew_equalcheck(existing, new):
    # Here we want to check if the existing values are equal to the given ones.
    # For this we have to make them comparable with converting and sorting.

    if new["active_time_ranges"]:
        time_ranges = [
            correct_timeformat(time_ranges) for time_ranges in new["active_time_ranges"]
        ]
        time_ranges = [
            correct_timeformat(time_ranges)
            for time_ranges in existing["active_time_ranges"]
        ]
        new["active_time_ranges"] = correct_timerange(new["active_time_ranges"])
        time_ranges = [
            sort_timerange(time_ranges) for time_ranges in new["active_time_ranges"]
        ]
        time_ranges = [
            sort_timerange(time_ranges)
            for time_ranges in existing["active_time_ranges"]
        ]

    if new["exceptions"]:
        time_ranges = [
            correct_timeformat(time_ranges) for time_ranges in new["exceptions"]
        ]
        time_ranges = [
            correct_timeformat(time_ranges) for time_ranges in existing["exceptions"]
        ]
        time_ranges = [sort_timerange(time_ranges) for time_ranges in new["exceptions"]]
        new["exceptions"] = sorted(new["exceptions"], key=lambda d: d["date"])
        existing["exceptions"] = sorted(existing["exceptions"], key=lambda d: d["date"])
        time_ranges = [
            sort_timerange(time_ranges) for time_ranges in existing["exceptions"]
        ]

    if new["exclude"]:
        new["exclude"] = sorted(new["exclude"])
        existing["exclude"] = sorted(existing["exclude"])
    equal = True
    for key, value in new.items():
        if value is not None and value != existing.get(key):
            equal = False
            break
    return equal


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
            ver = timeperiodget.getversion()

            # Check for value "exclude" as this wasn't possible to update before Werk #16052.
            if module.params.get("exclude") and not patched_version(ver):
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

            # Get the existing values of the time period.
            # Beware of different output of "Show a time period" in Version 2.0.
            existing = {}
            if ver == CheckmkVersion("2.0.0"):
                for value in updatevalues:
                    existing[value] = json.loads(result.content).get(value)
            else:
                for value in updatevalues:
                    existing[value] = (
                        json.loads(result.content).get("extensions").get(value)
                    )

            # Get the new values of the time period.
            new = {}
            for value in updatevalues:
                new[value] = module.params.get(value)

            if existingnew_equalcheck(existing, new):
                # Time period is equal. Skip the update.
                result = RESULT(
                    http_code=0,
                    msg="Existing time period is equal with new one. No need to update.",
                    content="",
                    etag="",
                    failed=False,
                    changed=False,
                )
            else:
                result = timeperiodupdate.put(existing["alias"])

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

    module.exit_json(**result_as_dict(result))


def main():
    run_module()


if __name__ == "__main__":
    main()

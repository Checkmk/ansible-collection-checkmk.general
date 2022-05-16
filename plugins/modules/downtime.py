#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2022, Oliver Gaida <ogaida@t-online.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: downtime

short_description: Manage downtimes in Checkmk.

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "0.2.0"

description:
- Manage downtimes within Checkmk.

notes:
- Idempotency for creation was made for hostdowntimes by only using the hostname and comment attributes.
  If this combination already exists as a downtime, the new downtime will not be created except using force.
  The creation of servicedowntimes works accordingly, with hostname, service description and
  comment.

todo:
- Implement idempotency for deletion
- Fine tune deletion, so only delete dt by host and comment

extends_documentation_fragment: [tribe29.checkmk.common]

options:
    comment:
        description:
        - Remarks for the downtime. If omitted in combination with state = present, the
          default 'Set by Ansible' will be used, in combination with state = absent, ALL downtimes of
          a host or host/service will be removed.
        type: str
    duration:
        description:
        - Duration in seconds. When set, the downtime does not begin automatically at a nominated time,
          but when a non-OK status actually appears for the host.
          Consequently, the start_time and end_time is only the time window in which the scheduled downtime can occur.
        type: int
        default: 0
    end_after:
        description:
        - The timedelta between I(start_time) and I(end_time). If you want to use I(end_after) you have to omit I(end_time).
          For keys and values see U(https://docs.python.org/3/library/datetime.html#datetime.timedelta)
        type: dict
        default: {}
    end_time:
        description:
        - The end datetime of the downtime. The format has to conform to the ISO 8601 profile I(e.g. 2017-07-21T17:32:28Z).
          The built-in default is 30 minutes after now.
        type: str
        default: ''
    force:
        description: Force the creation of a downtime in case a hostname and comment combination already exists as a downtime.
        type: bool
        default: false
    start_after:
        description:
        - The timedelta between now and I(start_time). If you want to use I(start_after) you have to omit I(start_time).
          For keys and values see U(https://docs.python.org/3/library/datetime.html#datetime.timedelta)
        type: dict
        default: {}
    start_time:
        description:
        - The start datetime of the downtime. The format has to conform to the ISO 8601 profile I(e.g. 2017-07-21T17:32:28Z).
          The built-in default is now.
        type: str
        default: ''
    host_name:
        description: The host to schedule the downtime on.
        required: true
        type: str
    service_descriptions:
        description: Array of service descriptions. If set only service-downtimes will be set. If omitted a host downtime will be set.
        type: list
        elements: str
        default: []
    state:
        description: The state of this downtime. If absent, all matching host/service-downtimes of the given host will be deleted.
        type: str
        default: present
        choices: [present, absent]

author:
    - Oliver Gaida (@ogaida)
    - Lars Getwan (@lgetwan)
"""

EXAMPLES = r"""
- name: "Schedule host downtime."
  downtime:
    server_url: "{{ server_url }}"
    site: "{{ site }}"
    automation_user: "{{ automation_user }}"
    automation_secret: "{{ automation_secret }}"
    host_name: my_host
    start_after:
      minutes: 5
    end_after:
      days: 7
      hours: 5

- name: "Schedule service downtimes for two given services."
  downtime:
    server_url: "{{ server_url }}"
    site: "{{ site }}"
    automation_user: "{{ automation_user }}"
    automation_secret: "{{ automation_secret }}"
    host_name: my_host
    start_time: 2022-03-24T20:39:28Z
    end_time: 2022-03-24T20:40:28Z
    state: "present"
    duration: 0
    service_descriptions:
      - "CPU utilization"
      - "Memory"

- name: "Delete all service downtimes for two given services."
  tribe29.checkmk.downtime:
    server_url: "{{ server_url }}"
    site: "{{ site }}"
    automation_user: "{{ automation_user }}"
    automation_secret: "{{ automation_secret }}"
    host_name: my_host
    service_descriptions:
      - "CPU utilization"
      - "Memory"
    state: absent
"""

RETURN = r"""
message:
    description: The output message that the module generates. Contains the API response details in case of an error. No output in case of success.
    type: str
    returned: always
    sample: ''
"""

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url
import json
import re
from datetime import datetime, timedelta

try:
    from urllib import urlencode
except ImportError:  # For Python 3
    from urllib.parse import urlencode


def bail_out(module, state, msg):
    if state == "ok":
        result = {"msg": msg, "changed": False, "failed": False}
        module.exit_json(**result)
    elif state == "changed":
        result = {"msg": msg, "changed": True, "failed": False}
        module.exit_json(**result)
    else:
        result = {"msg": msg, "changed": False, "failed": True}
        module.fail_json(**result)


def _set_timestamps(module):
    default_start_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    default_end_time = (datetime.utcnow() + timedelta(minutes=30)).strftime("%Y-%m-%dT%H:%M:%SZ")
    start_time = module.params.get("start_time")
    end_time = module.params.get("end_time")
    end_after = module.params.get("end_after")
    start_after = module.params.get("start_after")
    if start_time == "":
        if start_after == {}:
            start_time = default_start_time
        else:
            start_time = (datetime.utcnow() + timedelta(**start_after)).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            )
    if end_time == "":
        if end_after == {}:
            end_time = default_end_time
        else:
            start_time = re.sub(r"\+\d\d:\d\d$", "Z", start_time)
            dt_start = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%SZ")
            end_time = (dt_start + timedelta(**end_after)).strftime("%Y-%m-%dT%H:%M:%SZ")
    return [start_time, end_time]


def _get_current_downtimes(module, base_url, headers):
    service_descriptions = module.params.get("service_descriptions")
    host_name = module.params.get("host_name")
    comment = module.params.get("comment")
    filters = []
    is_service = len(service_descriptions) != 0

    if is_service:
        # Handle list of service descriptions
        service_descriptions = module.params.get("service_descriptions")
        if len(service_descriptions) > 1:
            filters = [
                '{"op": "or", "expr": [%s]}'
                % ", ".join(
                    [
                        '{"op": "~", "left": "service_description", "right": "%s"}' % s
                        for s in service_descriptions
                    ]
                )
            ]
        else:
            filters = ['{"op": "~", "left": "service_description", "right": "%s"}']
        filters.append('{"op": "=", "left": "is_service", "right": "1"}')
    else:
        filters.append('{"op": "=", "left": "is_service", "right": "0"}')

    api_endpoint = "/domain-types/downtime/collections/all"
    filters.append('{"op": "~", "left": "host_name", "right": "%s"}' % host_name)
    if comment:
        filters.append('{"op": "~", "left": "comment", "right": "%s"}' % comment)

    params = {"query": '{"op": "and", "expr": [%s]}' % ", ".join(filters)}

    url = "%s%s?%s" % (base_url, api_endpoint, urlencode(params))
    response, info = fetch_url(module, url, headers=headers, method="GET")

    if info["status"] != 200:
        bail_out(
            module,
            "failed",
            "Error calling API while getting downtimes for %s. HTTP code %d. Details: %s, "
            % (host_name, info["status"], info["body"]),
        )

    body = json.loads(response.read().decode('utf-8'))

    if is_service:
        service_descriptions = []
        for dt in body["value"]:
            service_descriptions.append(dt["title"].split(":")[1].strip())
        return service_descriptions

    else:
        if len(body["value"]) > 0:
            return ["HOST"]

    return []


def set_downtime(module, base_url, headers, service_description=None):
    params = {}
    comment = module.params.get("comment", "Set by Ansible")
    host_name = module.params.get("host_name")
    service_descriptions = module.params.get("service_descriptions")
    is_host = len(service_descriptions) == 0
    current_downtimes = _get_current_downtimes(module, base_url, headers)

    if is_host:
        item = host_name
        params = {
            "downtime_type": "host",
        }
        api_endpoint = "/domain-types/downtime/collections/host"
        if len(current_downtimes) != 0 and not module.params.get("force"):
            return (
                "ok",
                "Downtime already exists for '%s' with comment '%s', you may use force attribute to create a new downtime with the same comment ."
                % (item, comment),
            )
    else:
        if not module.params.get("force"):
            # Only consider services that do not have downtimes with that comment, yet
            service_descriptions = [s for s in service_descriptions if s not in current_downtimes]

        item = "%s/[%s]" % (host_name, ", ".join(service_descriptions))
        params = {
            "service_descriptions": service_descriptions,
            "downtime_type": "service",
        }
        api_endpoint = "/domain-types/downtime/collections/service"

    if is_host or len(service_descriptions) > 0:

        start_time, end_time = _set_timestamps(module)
        params.update(
            {
                "start_time": start_time,
                "end_time": end_time,
                "duration": module.params.get("duration"),
                "recur": "fixed",
                "comment": comment,
                "host_name": host_name,
            }
        )

        url = base_url + api_endpoint

        response, info = fetch_url(
            module, url, module.jsonify(params), headers=headers, method="POST"
        )

        if info["status"] != 204:
            return (
                "failed",
                "Error calling API while adding downtime for '%s' with comment '%s'. HTTP code %d.  Details: %s, "
                % (item, comment, info["status"], info["body"]),
            )

        return "changed", "Downtime added for '%s' with comment '%s'." % (item, comment)

    return (
        "ok",
        "Downtime already exists for '%s' with comment '%s', you may use force attribute to create a new downtime with the same comment ."
        % (item, comment),
    )


def remove_downtime(module, base_url, headers):
    host_name = module.params.get("host_name")
    service_descriptions = module.params.get("service_descriptions")
    comment = module.params.get("comment")
    current_downtimes = _get_current_downtimes(module, base_url, headers)
    is_host = len(service_descriptions) == 0
    query_filters = []

    if is_host:
        item = host_name

    else:
        item = "%s/[%s]" % (host_name, ", ".join(service_descriptions))
        if len(service_descriptions) > 1:
            query_filters.append(
                '{"op": "or", "expr": [%s]}'
                % ", ".join(
                    [
                        '{"op": "~", "left": "service_description", "right": "%s"}' % s
                        for s in service_descriptions
                    ]
                )
            )

        else:
            query_filters.append('{"op": "~", "left": "service_description", "right": "%s"}')

    if len(current_downtimes) == 0:  # and comment is not None:
        return "ok", "'%s' has no downtimes with comment '%s'." % (item, comment)

    else:
        api_endpoint = "/domain-types/downtime/actions/delete/invoke"
        url = base_url + api_endpoint

        # Create the query
        query_filters.append('{"op": "~", "left": "host_name", "right": "%s"}' % host_name)

        if comment is not None:
            # If there's a comment, only delete downtimes that match that comment
            query_filters.append('{"op": "~", "left": "comment", "right": "%s"}' % comment)

        params = {
            "delete_type": "query",
            "query": '{"op": "and", "expr": [%s]}' % ", ".join(query_filters),
        }

        response, info = fetch_url(
            module, url, module.jsonify(params), headers=headers, method="POST"
        )

        if info["status"] != 204:
            return (
                "failed",
                "Error calling API while removing downtime from '%s' with comment '%s'. HTTP code %d. Details: %s, "
                % (
                    item,
                    comment,
                    info["status"],
                    info["body"],
                ),
            )
        else:
            return "changed", "Downtime removed from '%s' with comment '%s'." % (item, comment)


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        server_url=dict(type="str", required=True),
        site=dict(type="str", required=True),
        automation_user=dict(type="str", required=True),
        automation_secret=dict(type="str", required=True, no_log=True),
        host_name=dict(type="str", required=True),
        comment=dict(type="str"),
        duration=dict(type="int", default=0),
        start_after=dict(type="dict", default={}),
        start_time=dict(type="str", default=""),
        end_after=dict(type="dict", default={}),
        end_time=dict(type="str", default=""),
        force=dict(type="bool", default=False),
        service_descriptions=dict(type="list", elements="str", default=[]),
        state=dict(type="str", default="present", choices=["present", "absent"]),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=False)

    # Use the parameters to initialize some common variables
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer %s %s"
        % (
            module.params.get("automation_user"),
            module.params.get("automation_secret"),
        ),
    }

    base_url = "%s/%s/check_mk/api/1.0" % (
        module.params.get("server_url"),
        module.params.get("site"),
    )

    # Decide if host- or service-downtime depending on elements of service_descriptions
    service_descriptions = module.params.get("service_descriptions")
    if service_descriptions == []:
        hostdowntime = True
    else:
        hostdowntime = False

    # here, we need only the state param
    state = module.params.get("state", "present")

    # Handle the host accordingly to above findings and desired state
    if state == "present":
        state, msg = set_downtime(module, base_url, headers)
        bail_out(module, state, msg)

    elif state == "absent":
        state, msg = remove_downtime(module, base_url, headers)
        bail_out(module, state, msg)

    else:
        bail_out(module, "error", "Unknown error")


def main():
    run_module()


if __name__ == "__main__":
    main()

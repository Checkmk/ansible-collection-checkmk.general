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
version_added: "0.2"

description:
- Manage downtimes within Checkmk.
- idempotency for creation was made for hostdowntimes by only using the hostname and comment attributes. If this combination already exists as a downtime, the new downtime will not be created except using force. The creation of servicedowntimes is not idempotent at all. 

todos:
- implement idempotency for deletion
- fine tune deletion, so only delete dt by host and comment

extends_documentation_fragment: [tribe29.checkmk.common]

options:
    comment:
        description: remarks for the downtime.
        type: str
    #downtime_type:
    #    description: The type of downtime to create
    #  for simplicity, this is fixed to host
    duration:
        description: Duration in seconds. When set, the downtime does not begin automatically at a nominated time, but when a real problem status appears for the host. Consequencely, the start_time/end_time is only the time window in which the scheduled downtime can begin.
        type: int
        default: 0
    end_after:
        description: the timedelta between start_time and end_time. if you want to use end_after you have to ommit end_time. for keys and values see https://docs.python.org/3/library/datetime.html#datetime.timedelta
        type: dictionary
        default: {}
    end_time:
        description: The end datetime of the new downtime. The format has to conform to the ISO 8601 profile (like: 2017-07-21T17:32:28Z)
        type: str
        default: 30 minutes after now
    force:
        description: Force the creation of a downtime in case a hostname / comment combination already exists as a downtime.
        type: bool
        default: false
    service_descriptions:
        description: Array of service-descriptions. If set only service-downtimes will be set. If omitted a host-downtime will be set.
        type: array
        default: []
    start_after:
        description: the timedelta between now and start_time. if you want to use start_after you have to ommit start_time. for keys and values see https://docs.python.org/3/library/datetime.html#datetime.timedelta
        type: dictionary
        default: {}
    start_time:
        description: The start datetime of the new downtime. The format has to conform to the ISO 8601 profile.
        type: str
        default: now
    host_name:
        description: the affected host.
        required: true
        type: str
    # recur: for simplicity always fixed
    state:
        description: The state of this downtime. If absent, all matching host/service-downtimes of the given host will be deleted.
        type: str
        default: present
        choices: [present, absent]

author:
    - Oliver Gaida
"""

EXAMPLES = r"""
- name: set host-downtime
  downtime:
    server_url: "{{ server_url }}"
    site: "{{ site }}"
    automation_user: "{{ automation_user }}"
    automation_secret: "{{ automation_secret }}"
    host_name: pi4
    start_after:
      minutes: 5
    end_after:
      days: 7
      hours: 5

- name: set service-downtimes
  downtime:
    server_url: "{{ server_url }}"
    site: "{{ site }}"
    automation_user: "{{ automation_user }}"
    automation_secret: "{{ automation_secret }}"
    host_name: pi4
    start_time: 2022-03-24T20:39:28Z
    end_time: 2022-03-24T20:40:28Z
    state: "present"
    duration: 0
    service_descriptions:
      - "CPU utilization"
      - Memory

- name: delete service-downtimes
  tribe29.checkmk.downtime:
    server_url: "{{ server_url }}"
    site: "{{ site }}"
    automation_user: "{{ automation_user }}"
    automation_secret: "{{ automation_secret }}"
    host_name: pi4
    service_descriptions:
      - "CPU utilization"
      - Memory
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
import json, re
from datetime import datetime, timedelta

def exit_failed(module, msg):
    result = {"msg": msg, "changed": False, "failed": True}
    module.fail_json(**result)

def exit_changed(module, msg):
    result = {"msg": msg, "changed": True, "failed": False}
    module.exit_json(**result)

def exit_ok(module, msg):
    result = {"msg": msg, "changed": False, "failed": False}
    module.exit_json(**result)

def set_timestamps(module):
    default_start_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    default_end_time = (datetime.utcnow()+timedelta(minutes=30)).strftime("%Y-%m-%dT%H:%M:%SZ")
    start_time = module.params.get("start_time")
    end_time= module.params.get("end_time")
    end_after= module.params.get("end_after")
    start_after= module.params.get("start_after")
    if start_time == '':
        if start_after == {}:
            start_time = default_start_time
        else:
            start_time = (datetime.utcnow()+timedelta(**start_after)).strftime("%Y-%m-%dT%H:%M:%SZ")
    if end_time == '':
        if end_after == {}:
            end_time = default_end_time
        else:
            start_time = re.sub('\+\d\d:\d\d$','Z', start_time)
            dt_start = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%SZ')
            end_time = (dt_start+timedelta(**end_after)).strftime("%Y-%m-%dT%H:%M:%SZ")
    return [start_time, end_time]

def get_hostdowntimes(module, base_url, headers):
    # this function gets the list of downtime comments which exists for the given host, it returns an array of comments
    api_endpoint = "/domain-types/downtime/collections/all?host_name=%s" % module.params.get("host_name")
    url = base_url + api_endpoint
    response, info = fetch_url(
        module, url, data=None, headers=headers, method="GET"
    )

    if info["status"] != 200:
        exit_failed(
            module,
            "Error calling API. HTTP code %d. Details: %s, "
            % (info["status"], info["body"]),
        )
    
    body = json.loads(response.read())
    comments = []
    for dt in body["value"]:
        comments.append(dt["extensions"]["comment"])
    return comments

def set_hostdowntime(module, base_url, headers):
    comments = get_hostdowntimes(module, base_url, headers)
    comment = module.params.get("comment")
    if module.params.get("force") or not comment in comments:
        api_endpoint = "/domain-types/downtime/collections/host"
        start_time, end_time = set_timestamps(module)
        params = {
            "start_time": start_time,
            "end_time": end_time,
            "duration": module.params.get("duration"),
            "recur": "fixed",
            "comment": comment,
            "downtime_type": "host",
            "host_name": module.params.get("host_name"),
        }

        url = base_url + api_endpoint

        response, info = fetch_url(
            module, url, module.jsonify(params), headers=headers, method="POST"
        )
    else:
        msg = "downtime already exists for comment '%s' on the host '%s', you may use force attribute to create a new downtime with the same comment " % (comment, module.params.get("host_name"))
        exit_ok(module, msg)


    if info["status"] != 204:
        exit_failed(
            module,
            "Error calling API. HTTP code %d. Details: %s, "
            % (info["status"], info["body"]),
        )

def set_servicedowntime(module, base_url, headers):
    api_endpoint = "/domain-types/downtime/collections/service"
    get_hostdowntimes(module, base_url, headers)
    start_time, end_time = set_timestamps(module)
    params = {
        "start_time": start_time,
        "end_time": end_time,
        "duration": module.params.get("duration"),
        "recur": "fixed",
        "comment": module.params.get("comment"),
        "downtime_type": "service",
        "host_name": module.params.get("host_name"),
        "service_descriptions": module.params.get("service_descriptions")
    }
    url = base_url + api_endpoint

    response, info = fetch_url(
        module, url, module.jsonify(params), headers=headers, method="POST"
    )

    if info["status"] != 204:
        exit_failed(
            module,
            "Error calling API. HTTP code %d. Details: %s, "
            % (info["status"], info["body"]),
        )

def remove_hostdowntime(module, base_url, headers):
    api_endpoint = "/domain-types/downtime/actions/delete/invoke"
    params = {
        "delete_type": "params",
        "host_name": module.params.get("host_name")
    }
    url = base_url + api_endpoint
    response, info = fetch_url(
        module, url, module.jsonify(params), headers=headers, method="POST"
    )

    if info["status"] != 204:
        exit_failed(
            module,
            "Error calling API. HTTP code %d. Details: %s, "
            % (info["status"], info["body"]),
        )

def remove_servicedowntime(module, base_url, headers):
    api_endpoint = "/domain-types/downtime/actions/delete/invoke"
    params = {
        "delete_type": "params",
        "host_name": module.params.get("host_name"),
        "service_descriptions": module.params.get("service_descriptions")
    }
    url = base_url + api_endpoint
    response, info = fetch_url(
        module, url, module.jsonify(params), headers=headers, method="POST"
    )

    if info["status"] != 204:
        exit_failed(
            module,
            "Error calling API. HTTP code %d. Details: %s, "
            % (info["status"], info["body"]),
        )

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        server_url=dict(type="str", required=True),
        site=dict(type="str", required=True),
        automation_user=dict(type="str", required=True),
        automation_secret=dict(type="str", required=True, no_log=True),
        host_name=dict(type="str", required=True),
        comment=dict(type="str", default='dt set by ansible'),
        duration=dict(type="int", default=0),
        start_after=dict(type="dict", default={}),
        start_time=dict(type="str", default=''),
        end_after=dict(type="dict", default={}),
        end_time=dict(type="str", default=''),
        force=dict(type="bool", default=False),
        service_descriptions=dict(type='list', elements='str',default = []),
        state=dict(type="str", default='present', choices=["present", "absent"]),
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

        if hostdowntime:
            set_hostdowntime(module, base_url, headers)
            exit_changed(module, "Hostdowntime has been created.")
        else:
            set_servicedowntime(module, base_url, headers)
            exit_changed(module, "Servicedowntime has been created.")

    elif state == "absent":

        if hostdowntime:
            remove_hostdowntime(module, base_url, headers)
            exit_changed(module, "Hostdowntime has been deleted.")
        else:
            remove_servicedowntime(module, base_url, headers)
            exit_changed(module, "Servicedowntime has been deleted.")

    else:
        exit_failed(module, "Unknown error")


def main():
    run_module()


if __name__ == "__main__":
    main()

#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2024, Stefan Mühling <muehling.stefan@googlemail.com>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: notification_rule

short_description: Manage notification_rule in Checkmk.

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "4.3.0"

description:
- Manage notification_rule in Checkmk.

extends_documentation_fragment: [checkmk.general.common]

options:
    [...]

author:
    - Stefan Mühling (@muehlings)
"""

EXAMPLES = r"""
    [...]
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

class Notification_ruleHTTPCodes:
# [Response matrix needs adjustment:
#    delete = {
#        204: (True, False, 'No Content: Operation done successfully. No further output.'),
#    }
#    get = {
#        404: (False, False, 'Not Found: The requested object has not been found.'),
#        200: (False, False, 'OK: The operation was done successfully.'),
#    }
#    post = {
#        204: (True, False, 'No Content: Operation done successfully. No further output.'),
#        200: (True, False, 'OK: The operation was done successfully.'),
#    }
# ]

    # http_code: (changed, failed, "Message")

    post = { 
        406: (False, True, 'Not Acceptable: The requests accept headers can not be satisfied.'), 
        403: (False, True, 'Forbidden: Configuration via Setup is disabled.'), 
        415: (False, True, 'Unsupported Media Type: The submitted content-type is not supported.'), 
        400: (False, True, 'Bad Request: Parameter or validation failure.'), 
        200: (True, False, 'OK: Created.'),
    }

    get = { 
        406: (False, True, 'Not Acceptable: The requests accept headers can not be satisfied.'), 
        403: (False, True, 'Forbidden: Configuration via Setup is disabled.'), 
        #2
        404: (False, False, 'Not Found: The requested object has not been found.'), 
        200: (False, False, 'OK: The operation was done successfully.'),
    }

    put = { 
        406: (False, True, 'Not Acceptable: The requests accept headers can not be satisfied.'), 
        403: (False, True, 'Forbidden: Configuration via Setup is disabled.'), 
        404: (False, True, 'Not Found: The requested object has not been found.'), 
        415: (False, True, 'Unsupported Media Type: The submitted content-type is not supported.'), 
        400: (False, True, 'Bad Request: Parameter or validation failure.'), 
        200: (True, False, 'OK: Updated.'),
    }

class Notification_ruleEndpoints:
    default = "/objects/notification_rule"
    create = "/domain-types/notification_rule/collections/all"

def _build_default_endpoint(module):
    #1
#    ["None" is not always the identifier field, e.g. "new_role_id" for user_role]
    return "%s/%s" % (Notification_ruleEndpoints.default, module.params.get("id"))

def _build_delete_endpoint(module):
#    [delete is a POST endpoint here]
    return "%s/%s/actions/delete/invoke" % (Notification_ruleEndpoints.default, module.params.get("id"))

class Notification_ruleCreateAPI(CheckmkAPI):
    def post(self, data):
        if not self.params.get("rule_config"):
            result = RESULT(
                http_code=0,
                msg="Need parameter 'rule_config' to create notification_rule",
                content="",
                etag="",
                failed=True,
                changed=False,
            )
            return result

        else:
            return self._fetch(
                code_mapping=Notification_ruleHTTPCodes.post,
                endpoint=Notification_ruleEndpoints.create,
                data=data,
                method="POST",
            )

class Notification_ruleUpdateAPI(CheckmkAPI):
    def put(self, data):
        return self._fetch(
            code_mapping=Notification_ruleHTTPCodes.put,
            endpoint=_build_default_endpoint(self),
            data=data,
            method="PUT",
        )

class Notification_ruleDeleteAPI(CheckmkAPI):
    def delete(self):
        data = {}

        return self._fetch(
            code_mapping=Notification_ruleHTTPCodes.delete,
            endpoint=_build_default_endpoint(self),
            method="DELETE",
#            endpoint=_build_delete_endpoint(self),
#            method="POST",
        )

class Notification_ruleGetAPI(CheckmkAPI):
    def get(self):
        data = {}

        return self._fetch(
            code_mapping=Notification_ruleHTTPCodes.get,
            endpoint=_build_default_endpoint(self),
            data=data,
            method="GET",
        )

class Notification_rule():
    rule_config = None
    id = None
    def from_module(self, module):
        self.rule_config = module.get('rule_config')
        self.id = module.get('id')

    def from_current(self, current):
        #4
        self.rule_config = current.get('extensions').get('rule_config')
        self.id = current.get('id')
# [Example]
#        self.aux_tag_id = current.get('id')
#        self.title = current.get('title')
#        self.topic = current.get('extensions').get('topic')
#        self.help = current.get('extensions').get('help')

    # There is no named "id" for notification_rule. The rule gets created everytime it is called
    def post(self):
        data = self.__dict__
        data.pop('id')
        data = {key: val for key, val in data.items() if val}
        return data

    def put(self):
        data = self.__dict__
        data.pop('id')
        data = {key: val for key, val in data.items() if val}
        return data

    def changes_detected(self, other):
        if type(self) != dict:
            _current = self.__dict__
        else:
            _current = self
        if type(other) != dict:
            _module = other.__dict__
        else:
            _module = other
        for k in _current:
            if k in _module:
                if type(_current[k]) is dict:
                    self.changes_detected(_module[k])
                if _current[k] != _module[k]:
                    return True
            else:
                return True
        return False

def run_module():
    module_args = dict(
        server_url=dict(type="str", required=True),
        site=dict(type="str", required=True),
        automation_user=dict(type="str", required=True),
        automation_secret=dict(type="str", required=True, no_log=True),
        validate_certs=dict(type="bool", required=False, default=True),

#        [Probably needs some adjustments, parameter fields can vary in type]
        #3
        rule_config=dict(type="dict", required=True),
        id=dict(type="str", required=True),
#        [...]

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

    notification_ruleget = Notification_ruleGetAPI(module)
    current = notification_ruleget.get()

    current_notification_rule = Notification_rule()
    module_notification_rule = Notification_rule()
    module_notification_rule.from_module(module.params)

    if module.params.get("state") == "present":
        if current.http_code == 200:
            current_notification_rule.from_current(json.loads(current.content.decode("utf-8")))
            #raise Exception(current_notification_rule.put(), module_notification_rule.put())

            # If 'notification_rule' has changed then update it.
            current_notification_rule.from_current(json.loads(current.content.decode("utf-8")))
            if current_notification_rule.changes_detected(module_notification_rule):
                notification_ruleupdate = Notification_ruleUpdateAPI(module)
                notification_ruleupdate.headers["If-Match"] = current.etag
                result = notification_ruleupdate.put(module_notification_rule.put())
                time.sleep(3)

        elif current.http_code == 404:
            # 'notification_rule' is not there. Create it.
            notification_rulecreate = Notification_ruleCreateAPI(module)
            result = notification_rulecreate.post(module_notification_rule.post())

    if module.params.get("state") == "absent":
        # Only delete if the 'notification_rule' exists
        if current.http_code == 200:
            notification_ruledelete = Notification_ruleDeleteAPI(module)
            result = notification_ruledelete.delete()
            time.sleep(3)

        elif current.http_code == 404:
            result = RESULT(
                http_code=0,
                msg="notification_rule doesn't exist.",
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

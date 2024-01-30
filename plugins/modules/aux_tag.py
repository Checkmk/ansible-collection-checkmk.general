#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2024, Stefan Mühling <muehling.stefan@googlemail.com>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: aux_tag

short_description: Manage aux_tag in Checkmk.

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "4.3.0"

description:
- Manage aux_tag in Checkmk.

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

class Aux_tagHTTPCodes:
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

    delete = {
        204: (True, False, 'No Content: Operation done successfully. No further output.'),
    }

    post = { 
        406: (False, True, 'Not Acceptable: The requests accept headers can not be satisfied.'), 
        403: (False, True, 'Forbidden: Configuration via Setup is disabled.'), 
        404: (False, True, 'Not Found: The requested object has not been found.'), 
        409: (False, True, 'Conflict: The request is in conflict with the stored resource.'), 
        415: (False, True, 'Unsupported Media Type: The submitted content-type is not supported.'), 
        400: (False, True, 'Bad Request: Parameter or validation failure.'), 
        204: (True, False, 'No Content: Operation done successfully. No further output.'),
        200: (True, False, 'OK: The operation was done successfully.'),
    }

    get = { 
        406: (False, True, 'Not Acceptable: The requests accept headers can not be satisfied.'), 
        403: (False, True, 'Forbidden: Configuration via Setup is disabled.'), 
        404: (False, False, 'Not Found: The requested object has not been found.'), 
        200: (False, False, 'OK: The operation was done successfully.'),
    }

    put = { 
        406: (False, True, 'Not Acceptable: The requests accept headers can not be satisfied.'), 
        403: (False, True, 'Forbidden: Configuration via Setup is disabled.'), 
        404: (False, True, 'Not Found: The requested object has not been found.'), 
        415: (False, True, 'Unsupported Media Type: The submitted content-type is not supported.'), 
        400: (False, True, 'Bad Request: Parameter or validation failure.'), 
        200: (True, False, 'OK: The operation was done successfully.'),
    }

class Aux_tagEndpoints:
    default = "/objects/aux_tag"
    create = "/domain-types/aux_tag/collections/all"

def _build_default_endpoint(module):
#    ["name" is not always the identifier field, e.g. "new_role_id" for user_role]
    return "%s/%s" % (Aux_tagEndpoints.default, module.params.get("aux_tag_id"))

def _build_delete_endpoint(module):
#    [delete is a POST endpoint here]
    return "%s/%s/actions/delete/invoke" % (Aux_tagEndpoints.default, module.params.get("aux_tag_id"))

class Aux_tagCreateAPI(CheckmkAPI):
    def post(self, data):
        if not self.params.get("aux_tag_id"):
            result = RESULT(
                http_code=0,
                msg="Need parameter 'aux_tag_id' to create aux_tag",
                content="",
                etag="",
                failed=True,
                changed=False,
            )
            return result
        if not self.params.get("title"):
            result = RESULT(
                http_code=0,
                msg="Need parameter 'title' to create aux_tag",
                content="",
                etag="",
                failed=True,
                changed=False,
            )
            return result
        if not self.params.get("topic"):
            result = RESULT(
                http_code=0,
                msg="Need parameter 'topic' to create aux_tag",
                content="",
                etag="",
                failed=True,
                changed=False,
            )
            return result

        else:
            return self._fetch(
                code_mapping=Aux_tagHTTPCodes.post,
                endpoint=Aux_tagEndpoints.create,
                data=data,
                method="POST",
            )

class Aux_tagUpdateAPI(CheckmkAPI):
    def put(self, data):
        return self._fetch(
            code_mapping=Aux_tagHTTPCodes.put,
            endpoint=_build_default_endpoint(self),
            data=data,
            method="PUT",
        )

class Aux_tagDeleteAPI(CheckmkAPI):
    def delete(self):
        data = {}

        return self._fetch(
            code_mapping=Aux_tagHTTPCodes.delete,
#            endpoint=_build_default_endpoint(self),
#            method="DELETE",
            endpoint=_build_delete_endpoint(self),
            method="POST",
        )

class Aux_tagGetAPI(CheckmkAPI):
    def get(self):
        data = {}

        return self._fetch(
            code_mapping=Aux_tagHTTPCodes.get,
            endpoint=_build_default_endpoint(self),
            data=data,
            method="GET",
        )

class Aux_tag():
    aux_tag_id = None
    topic = None
    title = None
    help = None
    def from_module(self, module):
        self.aux_tag_id = module.get('aux_tag_id')
        self.topic = module.get('topic')
        self.title = module.get('title')
        self.help = module.get('help')

    def from_current(self, current):
#        self.aux_tag_id = current.get('aux_tag_id')
#        self.topic = current.get('topic')
#        self.title = current.get('title')
#        self.help = current.get('help')
# [Example]
        self.aux_tag_id = current.get('id')
        self.title = current.get('title')
        self.topic = current.get('extensions').get('topic')
        self.help = current.get('extensions').get('help')

    def post(self):
        data = self.__dict__
        data = {key: val for key, val in data.items() if val}
        return data

    def put(self):
        data = self.__dict__
        data.pop('aux_tag_id')
        data = {key: val for key, val in data.items() if val}
        return data

    def changes_detected(self, other):
        _current = self.__dict__
        _module = other.__dict__
        for k in _current:
            if k in _module:
                if type(_current[k]) is dict:
                    self.changes_detected(_current[k],_module[k])
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
        aux_tag_id=dict(type="str", required=True),
        title=dict(type="str", required=True),
        topic=dict(type="str", required=True),
        help=dict(type="str", default=""),
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

    aux_tagget = Aux_tagGetAPI(module)
    current = aux_tagget.get()

    current_aux_tag = Aux_tag()
    module_aux_tag = Aux_tag()
    module_aux_tag.from_module(module.params)

    if module.params.get("state") == "present":
        if current.http_code == 200:
            # If 'aux_tag' has changed then update it.
            current_aux_tag.from_current(json.loads(current.content.decode("utf-8")))
            if current_aux_tag.changes_detected(module_aux_tag):
                aux_tagupdate = Aux_tagUpdateAPI(module)
                aux_tagupdate.headers["If-Match"] = current.etag
                result = aux_tagupdate.put(module_aux_tag.put())
                time.sleep(3)

        elif current.http_code == 404:
            # 'aux_tag' is not there. Create it.
            aux_tagcreate = Aux_tagCreateAPI(module)
            result = aux_tagcreate.post(module_aux_tag.post())

    if module.params.get("state") == "absent":
        # Only delete if the 'aux_tag' exists
        if current.http_code == 200:
            aux_tagdelete = Aux_tagDeleteAPI(module)
            result = aux_tagdelete.delete()
            time.sleep(3)

        elif current.http_code == 404:
            result = RESULT(
                http_code=0,
                msg="aux_tag doesn't exist.",
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

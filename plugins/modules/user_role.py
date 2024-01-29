#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2024, Stefan Mühling <muehling.stefan@googlemail.com>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: user_role

short_description: Manage user_role in Checkmk.

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "0.11.0"

description:
- Manage user_role in Checkmk.

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

class User_roleHTTPCodes:
#    [Response matrix needs adjustment]
    # http_code: (changed, failed, "Message")

    post = { 
        406: (False, True, 'Not Acceptable: The requests accept headers can not be satisfied.'), 
        403: (False, True, 'Forbidden: Configuration via Setup is disabled.'), 
        415: (False, True, 'Unsupported Media Type: The submitted content-type is not supported.'), 
        400: (False, True, 'Bad Request: Parameter or validation failure.'), 
        200: (True, False, 'OK: The operation was done successfully.'),
    }

    get = { 
        406: (False, True, 'Not Acceptable: The requests accept headers can not be satisfied.'), 
        403: (False, True, 'Forbidden: Configuration via Setup is disabled.'), 
        404: (False, False, 'Not Found: The requested object has not been found.'), 
        200: (False, False, 'OK: The operation was done successfully.'),
    }

    delete = { 
        406: (False, True, 'Not Acceptable: The requests accept headers can not be satisfied.'), 
        403: (False, True, 'Forbidden: Configuration via Setup is disabled.'), 
        404: (False, False, 'Not Found: The requested object has not been found.'), 
        204: (True, False, 'No Content: Operation done successfully. No further output.'),
    }

    put = { 
        406: (False, True, 'Not Acceptable: The requests accept headers can not be satisfied.'), 
        403: (False, True, 'Forbidden: Configuration via Setup is disabled.'), 
        404: (False, True, 'Not Found: The requested object has not been found.'), 
        415: (False, True, 'Unsupported Media Type: The submitted content-type is not supported.'), 
        400: (False, True, 'Bad Request: Parameter or validation failure.'), 
        200: (True, False, 'OK: The operation was done successfully.'),
    }

class User_roleEndpoints:
    default = "/objects/user_role"
    create = "/domain-types/user_role/collections/all"

def _build_default_endpoint(module):
#    ["name" is not always the identifier field, e.g. "new_role_id" for user_role]
    return "%s/%s" % (User_roleEndpoints.default, module.params.get("new_role_id"))

class User_roleCreateAPI(CheckmkAPI):
    def post(self, data):
        if not self.params.get("role_id"):
            result = RESULT(
                http_code=0,
                msg="Need parameter 'role_id' to create user_role",
                content="",
                etag="",
                failed=True,
                changed=False,
            )
            return result

        else:
            return self._fetch(
                code_mapping=User_roleHTTPCodes.post,
                endpoint=User_roleEndpoints.create,
                data=data,
                method="POST",
            )

class User_roleUpdateAPI(CheckmkAPI):
    def put(self, data):
        return self._fetch(
            code_mapping=User_roleHTTPCodes.put,
            endpoint=_build_default_endpoint(self),
            data=data,
            method="PUT",
        )

class User_roleDeleteAPI(CheckmkAPI):
    def delete(self):
        data = {}

        return self._fetch(
            code_mapping=User_roleHTTPCodes.delete,
            endpoint=_build_default_endpoint(self),
            method="DELETE",
        )

class User_roleGetAPI(CheckmkAPI):
    def get(self):
        data = {}

        return self._fetch(
            code_mapping=User_roleHTTPCodes.get,
            endpoint=_build_default_endpoint(self),
            data=data,
            method="GET",
        )

def changes_detected(module, current): # PUT
    new = module.params
    old = current.get('extensions')
    old['role_id'] = current.get('id')

    mapping = []
    for old_key in old.keys():
        for new_key in new.keys():
            if old_key in new_key and old_key != new_key:
                mapping.append((new_key, old_key))
    for new_mapping, old_mapping in mapping:
        if new.get(new_mapping) != old.get(old_mapping):
            yield new_mapping

def normalize_data(raw_data): # POST
#    [Probably needs some adjustments, wrong named input/output fields are possible]
    data = {
        "role_id": raw_data.get("role_id", ""),
        "new_role_id": raw_data.get("new_role_id", ""),
        "new_alias": raw_data.get("new_alias", ""),
    }
#    [e.g.  "role_id": raw_data.get("new_basedon", ""), # "new_basedon" is named "role_id" in POST schema

    # Remove all keys without value, as they would be emptied.
    data = {key: val for key, val in data.items() if val}
    return data

def run_module():
    module_args = dict(
        server_url=dict(type="str", required=True),
        site=dict(type="str", required=True),
        automation_user=dict(type="str", required=True),
        automation_secret=dict(type="str", required=True, no_log=True),
        validate_certs=dict(type="bool", required=False, default=True),

#        [Probably needs some adjustments, parameter fields can vary in type]
        new_basedon=dict(type="str", default=""),
        new_role_id=dict(type="str", default=""),
        role_id=dict(type="str", default=""),
        new_alias=dict(type="str", default=""),
        new_permissions=dict(type="list", default=[]),
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

    user_roleget = User_roleGetAPI(module)
    current = user_roleget.get()

    if module.params.get("state") == "present":
        if current.http_code == 200:
            # If user_role has changed then update it.
            current_content = json.loads(current.content.decode("utf-8"))
            changes = list(changes_detected(module, current_content))
            if len(changes) > 0: 
                data = { change: module.params[change] for change in changes }
#                 [Some fields are not allowed during update or create or need special treatment like re-building a dict of permissions because the GET endpoint only delivers a list of names]
                if data.get('new_permissions') != None:
                    data["new_permissions"] = { key: "yes" for key in data["new_permissions"] }
                user_roleupdate = User_roleUpdateAPI(module)
                user_roleupdate.headers["If-Match"] = current.etag
                result = user_roleupdate.put(data)
                time.sleep(3)

        elif current.http_code == 404:
            # user_role is not there. Create it.
            user_rolecreate = User_roleCreateAPI(module)
            data = normalize_data(module.params) # remove unnessecary parameters
            result = user_rolecreate.post()

    if module.params.get("state") == "absent":
        # Only delete if the user_role exists
        if current.http_code == 200:
            user_roledelete = User_roleDeleteAPI(module)
            result = user_roledelete.delete()
            time.sleep(3)

        elif current.http_code == 404:
            result = RESULT(
                http_code=0,
                msg="user_role doesn't exist.",
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

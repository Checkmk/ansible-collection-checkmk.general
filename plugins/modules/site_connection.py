#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2024, Stefan Mühling <muehling.stefan@googlemail.com>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: site_connection

short_description: Manage site_connection in Checkmk.

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "4.3.0"

description:
- Manage site_connection in Checkmk.

extends_documentation_fragment: [checkmk.general.common]

options:
    [...]

author:
    - Stefan Mühling (@muehlings)
"""

EXAMPLES = r"""
# GET
  "extensions": {
        "basic_settings": {
          "site_id": "smue",
          "alias": "Local site smue",
          "customer": "provider"
        },
        "status_connection": {
          "connection": {
            "socket_type": "local"
          },
          "proxy": {
            "use_livestatus_daemon": "direct"
          },
          "connect_timeout": 5,
          "persistent_connection": false,
          "url_prefix": "/smue/",
          "status_host": {
            "status_host_set": "disabled"
          },
          "disable_in_status_gui": false
        },
        "configuration_connection": {
          "enable_replication": false,
          "url_of_remote_site": "",
          "disable_remote_configuration": true,
          "ignore_tls_errors": false,
          "direct_login_to_web_gui_allowed": true,
          "user_sync": {
            "sync_with_ldap_connections": "all"
          },
          "replicate_event_console": false,
          "replicate_extensions": false
        }
      }

# PUT
  "site_config": {
    "basic_settings": {
      "alias": "Die remote site 1",
      "site_id": "site_id_1",
      "customer": "provider"
    },
    "status_connection": {
      "connection": {
        "socket_type": "tcp",
        "host": "123.124.1.3",
        "port": 1253,
        "encrypted": true,
        "verify": false
      },
      "proxy": {
        "use_livestatus_daemon": "with_proxy",
        "global_settings": false,
        "params": {
          "channels": 15,
          "heartbeat": {
            "interval": 12,
            "timeout": 3
          },
          "channel_timeout": 3.5,
          "query_timeout": 120.2,
          "connect_retry": 4.6,
          "cache": true
        },
        "tcp": {
          "port": 6560,
          "only_from": [
            "192.168.1.1"
          ],
          "tls": false
        }
      },
      "connect_timeout": 2,
      "persistent_connection": false,
      "url_prefix": "/heute_remote_1/",
      "status_host": {
        "status_host_set": "disabled"
      },
      "disable_in_status_gui": false
    },
    "configuration_connection": {
      "enable_replication": true,
      "url_of_remote_site": "http://localhost/heute_remote_site_id_1/check_mk/",
      "disable_remote_configuration": true,
      "ignore_tls_errors": false,
      "direct_login_to_web_gui_allowed": true,
      "user_sync": {
        "sync_with_ldap_connections": "all"
      },
      "replicate_event_console": true,
      "replicate_extensions": true
    }
  }

# POST
  "site_config": {
    "basic_settings": {
      "alias": "Die remote site 1",
      "site_id": "site_id_1",
      "customer": "provider"
    },
    "status_connection": {
      "connection": {
        "socket_type": "tcp",
        "host": "123.124.1.3",
        "port": 1253,
        "encrypted": true,
        "verify": false
      },
      "proxy": {
        "use_livestatus_daemon": "with_proxy",
        "global_settings": false,
        "params": {
          "channels": 15,
          "heartbeat": {
            "interval": 12,
            "timeout": 3
          },
          "channel_timeout": 3.5,
          "query_timeout": 120.2,
          "connect_retry": 4.6,
          "cache": true
        },
        "tcp": {
          "port": 6560,
          "only_from": [
            "192.168.1.1"
          ],
          "tls": false
        }
      },
      "connect_timeout": 2,
      "persistent_connection": false,
      "url_prefix": "/heute_remote_1/",
      "status_host": {
        "status_host_set": "disabled"
      },
      "disable_in_status_gui": false
    },
    "configuration_connection": {
      "enable_replication": true,
      "url_of_remote_site": "http://localhost/heute_remote_site_id_1/check_mk/",
      "disable_remote_configuration": true,
      "ignore_tls_errors": false,
      "direct_login_to_web_gui_allowed": true,
      "user_sync": {
        "sync_with_ldap_connections": "all"
      },
      "replicate_event_console": true,
      "replicate_extensions": true
    }
  }


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

class Site_connectionHTTPCodes:
#    [Response matrix needs adjustment]
    # http_code: (changed, failed, "Message")

    delete = {
        406: (False, True, 'Not Acceptable: The requests accept headers can not be satisfied.'),
        403: (False, True, 'Forbidden: Configuration via Setup is disabled.'),
        404: (False, True, 'Not Found: The requested object has not been found.'),
        415: (False, True, 'Unsupported Media Type: The submitted content-type is not supported.'),
        204: (True, False, 'No Content: Operation done successfully. No further output.'),
    }

    post = {
        406: (False, True, 'Not Acceptable: The requests accept headers can not be satisfied.'), 
        403: (False, True, 'Forbidden: Configuration via Setup is disabled.'), 
        404: (False, True, 'Not Found: The requested object has not been found.'), 
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

class Site_connectionEndpoints:
    default = "/objects/site_connection"
    create = "/domain-types/site_connection/collections/all"

def _build_default_endpoint(module):
#    ["name" is not always the identifier field, e.g. "new_role_id" for user_role]
    return "%s/%s" % (Site_connectionEndpoints.default, module.params.get("site_config")['basic_settings']['site_id'])

def _build_delete_endpoint(module):
#    [delete is a POST endpoint here]
    return "%s/%s/actions/delete/invoke" % (Site_connectionEndpoints.default, module.params.get("site_config")["basic_settings"]["site_id"])

class Site_connectionCreateAPI(CheckmkAPI):
    def post(self, data):
        if not self.params.get("site_config"):
            result = RESULT(
                http_code=0,
                msg="Need parameter 'site_config' to create site_connection",
                content="",
                etag="",
                failed=True,
                changed=False,
            )
            return result

        else:
            return self._fetch(
                code_mapping=Site_connectionHTTPCodes.post,
                endpoint=Site_connectionEndpoints.create,
                data=data,
                method="POST",
            )

class Site_connectionUpdateAPI(CheckmkAPI):
    def put(self, data):
        return self._fetch(
            code_mapping=Site_connectionHTTPCodes.put,
            endpoint=_build_default_endpoint(self),
            data=data,
            method="PUT",
        )

class Site_connectionDeleteAPI(CheckmkAPI):
    def delete(self):
        data = {}

        return self._fetch(
            code_mapping=Site_connectionHTTPCodes.delete,
            endpoint=_build_delete_endpoint(self),
            method="POST",
        )

class Site_connectionGetAPI(CheckmkAPI):
    def get(self):
        data = {}

        return self._fetch(
            code_mapping=Site_connectionHTTPCodes.get,
            endpoint=_build_default_endpoint(self),
            data=data,
            method="GET",
        )

def changes_detected(_current, _module): # PUT
#    raise Exception(_current, _module)
    for k in _current:
        if k in _module:
            if type(_current[k]) is dict:
                changes_detected(_current[k],_module[k])
            if _current[k] != _module[k]:
                #changes[k] = [_current[k], _module[k]]
                return True
        else:
            return True
    return False

def normalize_data(raw_data): # POST
#    [Probably needs some adjustments, wrong named input/output fields are possible]
    data = {
        "site_config": raw_data.get("site_config", ""),
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
        site_config=dict(type="dict", required=True),
        secret=dict(type="str", no_log=True),
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

    site_connectionget = Site_connectionGetAPI(module)
    current = site_connectionget.get()

    if module.params.get("state") == "present":
        if current.http_code == 200:
            # If site_connection has changed then update it.
            current_content = json.loads(current.content.decode("utf-8"))

            changes = changes_detected(current_content['extensions'], module.params['site_config'])
            if changes:
                data = {'site_config': module.params['site_config'] }
#                if module.params.get('secret'): how to handle change of secret?
#                    data['secret'] = module.params.get('secret')
#                 [Some fields are not allowed during update or create or need special treatment like re-building a dict of permissions because the GET endpoint only delivers a list of names]
                site_connectionupdate = Site_connectionUpdateAPI(module)
                site_connectionupdate.headers["If-Match"] = current.etag
                result = site_connectionupdate.put(data)
                time.sleep(3)

        elif current.http_code == 404:
            # site_connection is not there. Create it.
            site_connectioncreate = Site_connectionCreateAPI(module)
            data = normalize_data(module.params) # remove unnessecary parameters
            result = site_connectioncreate.post(data)

    if module.params.get("state") == "absent":
        # Only delete if the site_connection exists
        if current.http_code == 200:
            site_connectiondelete = Site_connectionDeleteAPI(module)
            result = site_connectiondelete.delete()
            time.sleep(3)

        elif current.http_code == 404:
            result = RESULT(
                http_code=0,
                msg="site_connection doesn't exist.",
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

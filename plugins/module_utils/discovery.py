#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2022, Michael Sekania &
#                      Robin Gierse <robin.gierse@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.checkmk.general.plugins.module_utils.version import CheckmkVersion
#from .version import CheckmkVersion

HTTP_CODES = {
    # http_code: (changed, failed, "Message")
    200: (True, False, "Discovery successful."),
    302: (
        True,
        False,
        (
            "The service discovery background job has been initialized. "
            "Redirecting to the 'Wait for service discovery completion' endpoint."
        ),
    ),
    404: (False, True, "Not Found: Host could not be found."),
    409: (False, False, "Conflict: A discovery background job is already running"),
}

HTTP_CODES_SC = {
    # http_code: (changed, failed, "Message")
    200: (True, False, "The service discovery has been completed."),
    302: (
        True,
        False,
        (
            "The service discovery is still running. "
            "Redirecting to the 'Wait for completion' endpoint."
        ),
    ),
    404: (False, False, "Not Found: There is no running service discovery"),
}

HTTP_CODES_BULK = {
    # http_code: (changed, failed, "Message")
    200: (True, False, "Discovery successful."),
    409: (False, False, "Conflict: A bulk discovery job is already active"),
}

HTTP_CODES_BULK_SC = {
    # http_code: (changed, failed, "Message")
    200: (True, False, "The service discovery has been completed."),
    404: (False, False, "Not Found: There is no running bulk_discovery job"),
}

SUPPORTED_VERSIONS = {
    "min": "2.1.0",
    "max": "2.5.0",
}

class Discovery():
    def __init__(self, module, logger):
        self.module = module
        self.logger = logger
        self.timeout = module.params.get("wait_timeout", 15)
        self.wait_for_previous = module.params.get("wait_for_previous", True)
        self.wait_for_completion = module.params.get("wait_for_completion", True)
        self.single_mode = self._single_mode()
        self.bulk_mode = not self.single_mode
        self.supported_versions = SUPPORTED_VERSIONS

    def _single_mode(self):
        return not (
            "hosts" in self.module.params
            and self.module.params.get("hosts")
            and len(self.module.params.get("hosts", [])) > 0
        )

    def _min_version(self):
        return CheckmkVersion(self.supported_versions["min"])

    def _max_version(self):
        return CheckmkVersion(self.supported_versions["max"])

    def compatible(self, version):
        #self.logger.debug(
        #    "min: %s, found: %s, max: %s" % (
        #        self._min_version()._value(),
        #        version._value(),
        #        self._max_version()._value(),
        #    )
        #)
        return self._min_version() <= version <= self._max_version()

    def start_discovery(self):
        raise NotImplementedError

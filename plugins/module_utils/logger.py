#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2024, Lars Getwan <lars.getwan@checkmk.com>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type


class Logger:
    def __init__(self):
        self.output = []
        self.loglevel = 0

    def set_loglevel(self, loglevel):
        self.loglevel = loglevel

    def warn(self, msg):
        self.output.append("WARN: %s" % msg)

    def info(self, msg):
        if self.loglevel >= 1:
            self.output.append("INFO: %s" % msg)

    def debug(self, msg):
        if self.loglevel >= 2:
            self.output.append("DEBUG: %s" % msg)

    def trace(self, msg):
        if self.loglevel >= 3:
            self.output.append("TRACE: %s" % msg)

    def get_log(self):
        return "\n".join(self.output)

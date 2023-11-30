#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2023, Checkmk GmbH
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# Ensure compatibility to Python2
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import re


class CheckmkVersion:
    """Helps to compare Checkmk versions"""

    def __init__(self, version_raw):
        def _parse(version_raw):
            _pattern = "([0-9])\\.([0-9])\\.([0-9])([abp])*([0-9]+)*\\.?([a-zA-Z]{3})*"
            r = re.match(_pattern, version_raw)
            return r

        self.version_raw = version_raw
        p = _parse(version_raw)
        if p:
            self.valid = True
            self._matchgroups = p.groups()
            self.majorversion = "%s.%s.%s" % (p.group(1), p.group(2), p.group(3))
            self.patchtype = p.group(4)
            self.patchlevel = p.group(5)
            self.edition = p.group(6)
        else:
            self.valid = False

    def _value(self):

        patchtype2num = {
            "p": 3,
            "b": 2,
            "a": 1,
            "i": 0,
        }

        g = self._matchgroups
        value = (10000 * int(g[0])) + (1000 * int(g[1])) + (100 * int(g[2]))

        if g[3]:
            value += 10 * patchtype2num[g[3]]
            value += int(g[4])

        return value

    def isvalid(self):
        return self.valid

    def __repr__(self):
        return self.version_raw

    def __gt__(self, other):
        return self._value() > other._value()

    def __lt__(self, other):
        return self._value() < other._value()

    def __ge__(self, other):
        return self._value() >= other._value()

    def __le__(self, other):
        return self._value() <= other._value()

    def __eq__(self, other):
        return self._value() == other._value()

    def __ne__(self, other):
        return self._value() != other._value()

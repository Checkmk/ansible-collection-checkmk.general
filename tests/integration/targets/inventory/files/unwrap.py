"""Unwrap {"__ansible_unsafe": "<value>"} markers from ansible-inventory JSON.

On ansible-core >= 2.19 `ansible-inventory --list` serializes untrusted
string variables as {"__ansible_unsafe": "<value>"} objects, which the
`from_json` filter refuses to deserialize again. Replace those objects
with their plain value so the test can parse the output. On older cores
this is a no-op.
"""

import json
import sys


def unwrap(obj):
    if isinstance(obj, dict):
        if set(obj) == {"__ansible_unsafe"}:
            return unwrap(obj["__ansible_unsafe"])
        return {key: unwrap(value) for key, value in obj.items()}
    if isinstance(obj, list):
        return [unwrap(item) for item in obj]
    return obj


json.dump(unwrap(json.load(sys.stdin)), sys.stdout)

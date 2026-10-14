#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2026, Lars Getwan <lars.getwan@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: global_setting

short_description: Manage global settings in Checkmk

version_added: "8.6.0"

description:
    - Set and reset global settings in Checkmk, either centrally or as a
      site-specific override of a single site connection.
    - Values are given the way the Checkmk GUI shows them. Choices are selected
      by their title, dictionary elements are addressed by their title, time
      spans and data sizes are written like C(1h 30min) or C(10 MiB). The
      module translates them to the representation the REST API expects, based
      on the specification the REST API delivers for each setting. You do not
      need to know that specification.
    - Without I(site_id), the central value is managed, which applies to every
      site that does not override it. With I(site_id), the site-specific value
      of that site connection is managed.

extends_documentation_fragment: [checkmk.general.common]

options:
    name:
        description:
            - The internal name of the global setting, e.g. C(log_levels) or
              C(wato_max_snapshots).
            - Event Console settings are addressed the same way, e.g.
              C(log_level).
            - The internal name is shown in the GUI when hovering over the title
              of a setting on the I(Global settings) page, or in the URL after
              clicking it (C(varname=...)).
        required: true
        type: str
        aliases: ["varname"]
    site_id:
        description:
            - The ID of a site connection. When set, the site-specific value of
              this site is managed instead of the central value.
            - On a non-distributed setup, site-specific settings are not
              available.
        required: false
        type: str
    value:
        description:
            - The desired value, as shown in the GUI. Required for
              I(state=present).
            - Single choices are selected by their title (e.g. C(Informational)),
              falling back to a case-insensitive match. Multiple choices are a
              list of titles.
            - Dictionaries use the titles of their elements as keys (e.g.
              C(Web)). If a title is empty or ambiguous, the internal element
              name is used instead, which is also always accepted as input.
              Elements that are left out are unchecked, just like in the GUI.
              Required elements that are left out keep their current value.
            - Cascading choices are written as a mapping with a single key,
              the choice title, whose value holds the parameters of that
              choice. Choices without further parameters can be given as the
              plain title.
            - Time spans are given in seconds or as a string like
              C(1d 2h 30min 10s). Data sizes are given in bytes or as a string
              like C(10 MiB).
            - Passwords are given in plain text or, where the setting supports
              the password store, as a mapping with the single key
              C(password_store) holding the name or ID of a stored password.
              See I(update_secrets).
            - Use the module's return value C(value) (e.g. with C(--check)) to
              see the expected structure of a setting.
        required: false
        type: raw
    update_secrets:
        description:
            - Passwords are stored encrypted by Checkmk, so the module cannot
              tell whether a given password matches the stored one.
            - With C(false), an already configured password is left unchanged,
              which keeps the module idempotent. With C(true), passwords are
              always written, which will report a change on every run.
        required: false
        type: bool
        default: false
    state:
        description:
            - C(present) makes sure the setting is explicitly configured with
              I(value) on the selected level. This also turns a setting that
              currently only inherits the same value (from the built-in default
              or, for I(site_id), from the central value) into an explicitly
              configured one.
            - C(absent) resets the setting. Without I(site_id), the central value
              is reset to the built-in default. With I(site_id), the
              site-specific override is removed, so the site inherits the
              central value again.
        required: false
        type: str
        default: present
        choices: ["present", "absent"]

notes:
    - The global settings endpoints belong to the internal REST API of Checkmk
      (C(/check_mk/api/internal)). They are only available in Checkmk versions
      that ship them, and their interface may still change.
    - Changes create pending changes. Use M(checkmk.general.activation) to
      activate them.
    - Idempotency compares the canonical form of the desired and the current
      value, together with the level the value is configured on (see I(state)).
    - Parts of a setting that are still implemented as legacy ValueSpecs in
      Checkmk cannot be configured by this module.
    - The module supports check mode and diff mode.
    - I(value) cannot be marked as secret as a whole. Set C(no_log) on the
      task when the value contains passwords.

seealso:
    - plugin: checkmk.general.global_setting
      plugin_type: lookup
    - module: checkmk.general.activation
    - module: checkmk.general.site
    - name: "Global settings: The official user guide."
      description: "The official user guide on the global settings."
      link: "https://docs.checkmk.com/latest/en/wato_configfiles.html"

author:
    - Lars Getwan (@lgetwan)
"""

EXAMPLES = r"""
# ---------------------------------------------------------------------------
# Central global settings
# ---------------------------------------------------------------------------

- name: "Keep more configuration snapshots."
  checkmk.general.global_setting:
    server_url: "https://myserver"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    name: "wato_max_snapshots"
    value: 100

- name: "Increase the log levels of some Checkmk components."
  checkmk.general.global_setting:
    server_url: "https://myserver"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    name: "log_levels"
    value:
      Web: "Informational"
      Authentication: "Debug"

- name: "Select a single choice by its title, as shown in the GUI."
  checkmk.general.global_setting:
    server_url: "https://myserver"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    name: "profile"
    value: "Enable profiling by request"

- name: "Enable the GUI debug mode."
  checkmk.general.global_setting:
    server_url: "https://myserver"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    name: "debug"
    value: true

- name: "Reset a setting to its built-in default."
  checkmk.general.global_setting:
    server_url: "https://myserver"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    name: "wato_max_snapshots"
    state: "absent"

# ---------------------------------------------------------------------------
# Site-specific global settings
# ---------------------------------------------------------------------------

- name: "Override a setting for the remote site 'remote1'."
  checkmk.general.global_setting:
    server_url: "https://myserver"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    site_id: "remote1"
    name: "log_levels"
    value:
      Web: "Debug"

- name: "Remove the override, so the site inherits the central value again."
  checkmk.general.global_setting:
    server_url: "https://myserver"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    site_id: "remote1"
    name: "log_levels"
    state: "absent"

# ---------------------------------------------------------------------------
# Discovering the structure of a setting
# ---------------------------------------------------------------------------
# The lookup plugin returns the current value in exactly the representation
# the module accepts, which is the easiest way to find out how to write it.

- name: "Show the current value of a setting."
  ansible.builtin.debug:
    msg: "{{ lookup('checkmk.general.global_setting', 'log_levels',
             server_url='https://myserver', site='mysite',
             api_user='myuser', api_secret='mysecret') }}"

# ---------------------------------------------------------------------------
# Secrets
# ---------------------------------------------------------------------------

- name: "Set a setting containing a password without logging it."
  checkmk.general.global_setting:
    server_url: "https://myserver"
    site: "mysite"
    api_user: "myuser"
    api_secret: "mysecret"
    name: "some_setting_with_a_password"
    value:
      Password: "{{ vault_password }}"
  no_log: true

# ---------------------------------------------------------------------------
# Using environment variables for authentication
# ---------------------------------------------------------------------------

- name: "Set a global setting using environment variables for authentication."
  checkmk.general.global_setting:
    name: "wato_max_snapshots"
    value: 100
  environment:
    CHECKMK_VAR_SERVER_URL: "https://myserver"
    CHECKMK_VAR_SITE: "mysite"
    CHECKMK_VAR_API_USER: "myuser"
    CHECKMK_VAR_API_SECRET: "mysecret"
"""

RETURN = r"""
msg:
    description:
        - The output message that the module generates.
    type: str
    returned: always
http_code:
    description:
        - The HTTP code returned by the Checkmk API.
    type: int
    returned: always
value:
    description:
        - The value of the setting after the module ran (in check mode, the
          value it would have), in the same representation as I(value).
        - Passwords are shown as C((hidden)). Passing C((hidden)) back as a
          password keeps the stored password.
    type: raw
    returned: when the setting could be read
    sample: {"Web": "Informational", "Authentication": "Warning"}
origin:
    description:
        - The level the value comes from after the module ran. C(factory) for
          the built-in default, C(global) for a centrally configured value and
          C(site) for a site-specific override.
    type: str
    returned: when the setting could be read
    sample: "global"
title:
    description:
        - The title of the setting as shown in the GUI.
    type: str
    returned: when the setting could be read
    sample: "Logging"
"""

import json

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.checkmk.general.plugins.module_utils.api import CheckmkAPI
from ansible_collections.checkmk.general.plugins.module_utils.global_settings import (
    GlobalSettingValueError,
    canonical,
    diff_paths,
    from_ui,
    internal_api_url,
    setting_endpoint,
    to_ui,
)
from ansible_collections.checkmk.general.plugins.module_utils.logger import Logger
from ansible_collections.checkmk.general.plugins.module_utils.utils import (
    base_argument_spec,
    exit_module,
)

logger = Logger()


class GlobalSettingHTTPCodes:
    """HTTP status codes and their meaning, as (changed, failed, message)."""

    get = {
        200: (False, False, "Global setting found"),
        400: (False, True, "Unknown or unavailable global setting"),
        404: (False, True, "Global setting or site not found"),
    }
    update = {
        200: (True, False, "Global setting updated"),
        422: (False, True, "The value does not match the schema of this setting"),
    }
    delete = {
        200: (True, False, "Global setting reset"),
        204: (True, False, "Global setting reset"),
    }


class GlobalSettingAPI(CheckmkAPI):
    """Manages a single (site-specific) global setting via the REST API.

    The current setting is fetched once. It carries the value, the rendered
    form spec that describes it, and the origin of the value. The spec is used
    to translate the user's GUI style value into the frontend representation
    the API expects, and to compare the two for idempotency.
    """

    def __init__(self, module):
        super().__init__(module)
        # The endpoints are only registered for the internal API version.
        self.url = internal_api_url(self.url)

        self.varname = self.params.get("name")
        self.gs_site_id = self.params.get("site_id")
        self.endpoint = setting_endpoint(self.varname, self.gs_site_id)
        # The level this module configures, as reported in 'origin'.
        self.own_origin = "site" if self.gs_site_id else "global"
        logger.debug(
            "GlobalSettingAPI: url=%s, endpoint=%s, own origin=%s"
            % (self.url, self.endpoint, self.own_origin)
        )

        self.etag = ""
        self.current = self._get_current()

    def _get_current(self):
        result = self._fetch(
            code_mapping=GlobalSettingHTTPCodes.get,
            endpoint=self.endpoint,
            method="GET",
            logger=logger,
        )
        self.etag = result.etag
        setting = json.loads(result.content)
        spec = setting.get("spec") or {}
        logger.debug(
            "Current setting: varname=%s, site_id=%s, origin=%s, spec type=%s, "
            "spec title=%r, top-level elements=%d, etag=%s"
            % (
                setting.get("varname"),
                setting.get("site_id"),
                setting.get("origin"),
                spec.get("type"),
                spec.get("title"),
                len(spec.get("elements") or []),
                self.etag,
            )
        )
        return setting

    @property
    def spec(self):
        return self.current.get("spec") or {}

    def _run(self, action, method, data=None):
        """Perform a single change, guarded by the ETag of the fetched state."""
        self.headers["If-Match"] = self.etag or "*"
        return self._fetch(
            code_mapping=getattr(GlobalSettingHTTPCodes, action),
            endpoint=self.endpoint,
            data=data,
            method=method,
            logger=logger,
        )

    def update(self, frontend_value):
        return self._run("update", "PUT", data={"value": frontend_value})

    def delete(self):
        return self._run("delete", "DELETE")


def _exit(module, api, result=None, msg="", changed=False, setting=None, diff=None):
    """Exit with the common result fields plus the setting's UI value."""
    if result is not None:
        output = result._asdict()
        output["changed"] = changed or result.changed
        if msg:
            output["msg"] = msg
    else:
        output = {
            "http_code": 200,
            "msg": msg,
            "content": "{}",
            "etag": api.etag,
            "failed": False,
            "changed": changed,
        }

    if setting is not None:
        output["value"] = setting["value"]
        output["origin"] = setting["origin"]
        output["title"] = setting["title"]
    if diff is not None and module._diff:
        output["diff"] = diff
    output["debug"] = logger.get_log()
    module.exit_json(**output)


def _ui_setting(spec, frontend_value, origin):
    ui_setting = {
        "value": to_ui(spec, frontend_value, logger=logger),
        "origin": origin,
        "title": spec.get("title") or "",
    }
    logger.debug(
        "UI setting: origin=%s, title=%r" % (ui_setting["origin"], ui_setting["title"])
    )
    return ui_setting


def _diff(before, after):
    return {
        "before": {"value": before["value"], "origin": before["origin"]},
        "after": {"value": after["value"], "origin": after["origin"]},
    }


def _present(module, api):
    spec = api.spec
    current_value = api.current.get("value")
    current_origin = api.current.get("origin")
    before = _ui_setting(spec, current_value, current_origin)

    try:
        desired_value = from_ui(
            spec,
            module.params.get("value"),
            current=current_value,
            update_secrets=module.params.get("update_secrets"),
            path=(),
            logger=logger,
        )
    except GlobalSettingValueError as e:
        exit_module(
            module,
            msg="Invalid value for global setting '%s': %s" % (api.varname, e),
            failed=True,
            logger=logger,
        )

    # Only the paths that differ are logged, not the values themselves: the
    # desired value may hold a password in plain text (update_secrets).
    differences = diff_paths(
        canonical(spec, current_value), canonical(spec, desired_value)
    )
    logger.debug(
        "Comparison: current origin=%s, own origin=%s, differing paths=%s"
        % (current_origin, api.own_origin, differences or "none")
    )

    if current_origin == api.own_origin and not differences:
        _exit(
            module,
            api,
            msg="Global setting already in the desired state.",
            setting=before,
            diff=_diff(before, before),
        )

    if not differences:
        logger.debug(
            "Value unchanged, but inherited (origin=%s): writing it to configure "
            "it explicitly on level '%s'." % (current_origin, api.own_origin)
        )

    # For display purposes, a password that is about to be written is hidden.
    after = _ui_setting(spec, desired_value, api.own_origin)
    if module.check_mode:
        _exit(
            module,
            api,
            msg="Global setting would be updated.",
            changed=True,
            setting=after,
            diff=_diff(before, after),
        )

    result = api.update(desired_value)
    try:
        response = json.loads(result.content)
        after = _ui_setting(
            response.get("spec") or spec,
            response.get("value"),
            response.get("origin", api.own_origin),
        )
    except (TypeError, ValueError):
        logger.debug(
            "Update response could not be parsed, reporting the desired value."
        )
    _exit(
        module,
        api,
        result=result,
        changed=True,
        setting=after,
        diff=_diff(before, after),
    )


def _absent(module, api):
    spec = api.spec
    current_origin = api.current.get("origin")
    before = _ui_setting(spec, api.current.get("value"), current_origin)
    logger.debug(
        "Reset requested: current origin=%s, own origin=%s"
        % (current_origin, api.own_origin)
    )

    if current_origin != api.own_origin:
        _exit(
            module,
            api,
            msg=(
                "No site-specific value configured, nothing to remove."
                if api.gs_site_id
                else "Global setting already at its default."
            ),
            setting=before,
            diff=_diff(before, before),
        )

    if module.check_mode:
        # The resulting value is not known without asking the server, so
        # only the level is reported.
        after = dict(
            before, value=None, origin="global" if api.gs_site_id else "factory"
        )
        _exit(
            module,
            api,
            msg="Global setting would be reset.",
            changed=True,
            setting=after,
            diff=_diff(before, after),
        )

    result = api.delete()
    # Re-read the setting to report the value that now applies.
    api.current = api._get_current()
    after = _ui_setting(api.spec, api.current.get("value"), api.current.get("origin"))
    _exit(
        module,
        api,
        result=result,
        changed=True,
        setting=after,
        diff=_diff(before, after),
    )


def run_module():
    argument_spec = base_argument_spec()
    argument_spec.update(
        name=dict(type="str", required=True, aliases=["varname"]),
        site_id=dict(type="str"),
        value=dict(type="raw"),
        update_secrets=dict(type="bool", default=False, no_log=False),
        state=dict(type="str", default="present", choices=["present", "absent"]),
    )

    required_if = [
        ("api_auth_type", "bearer", ["api_user", "api_secret"]),
        ("api_auth_type", "basic", ["api_user", "api_secret"]),
        ("api_auth_type", "cookie", ["api_auth_cookie"]),
        ("state", "present", ["value"]),
    ]

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=required_if,
    )

    logger.set_loglevel(module._verbosity)

    api = GlobalSettingAPI(module)

    try:
        if module.params["state"] == "present":
            _present(module, api)
        else:
            _absent(module, api)
    except Exception as e:
        exit_module(
            module,
            msg="Error managing the global setting: %s" % e,
            failed=True,
            logger=logger,
        )


def main():
    run_module()


if __name__ == "__main__":
    main()

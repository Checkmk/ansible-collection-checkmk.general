#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2026, Checkmk GmbH
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import email.message
import io
import json
from unittest.mock import MagicMock, patch

import pytest
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible_collections.checkmk.general.plugins.module_utils.lookup_api import (
    CheckMKLookupAPI,
)

BASE_URL = "http://myserver/mysite/check_mk/api/1.0"


def _api(server_url, site="mysite"):
    return CheckMKLookupAPI(
        server_url=server_url,
        site=site,
        api_user="myuser",
        api_secret="mysecret",
    )


def _http_error(code, body, reason="Server Error"):
    """Build an HTTPError whose read() returns `body`, like a real API failure."""
    fp = io.BytesIO(body.encode("utf-8") if isinstance(body, str) else body)
    return HTTPError("%s/fail" % BASE_URL, code, reason, email.message.Message(), fp)


@pytest.fixture
def open_url():
    """Patch open_url in the module under test and hand back the mock.

    Defaults to a successful, empty JSON response so tests only have to
    configure the behaviour they actually care about.
    """
    with patch(
        "ansible_collections.checkmk.general.plugins.module_utils.lookup_api.open_url"
    ) as mock:
        mock.return_value = MagicMock(read=MagicMock(return_value=b"{}"))
        yield mock


@pytest.mark.parametrize(
    "server_url",
    [
        "http://myserver",
        "http://myserver/",
        "http://myserver//",
    ],
)
def test_trailing_slash_is_normalized(server_url):
    """The collection documented the trailing-slash form for years, so both
    have to build the same URL."""
    assert _api(server_url).url == "http://myserver/mysite/check_mk/api/1.0"


def test_path_prefix_is_preserved():
    """Only trailing slashes are stripped, never a configured path prefix.

    This is why the join is rstrip() and not urljoin(): urljoin treats the last
    path segment as a document, so "https://myserver/checkmk" would lose the
    prefix and resolve to "https://myserver/mysite".
    """
    assert (
        _api("https://myserver/checkmk").url
        == "https://myserver/checkmk/mysite/check_mk/api/1.0"
    )


def test_site_url_is_exposed_without_the_api_path():
    assert _api("http://myserver/").site_url == "http://myserver/mysite"


# ---------------------------------------------------------------------------
# Query parameter encoding
# ---------------------------------------------------------------------------


def test_list_parameters_become_repeated_keys(open_url):
    """Array query parameters must be `columns=a&columns=b`.

    Without doseq the list is str()'d into a single `columns=%5B%27a%27...`
    value, which the REST API rejects.
    """
    _api("http://myserver").get(
        "/domain-types/host/collections/all", {"columns": ["name", "state"]}
    )

    url = open_url.call_args.args[0]
    assert url == (
        "%s/domain-types/host/collections/all?columns=name&columns=state" % BASE_URL
    )


def test_scalar_parameters_are_unaffected_by_doseq(open_url):
    _api("http://myserver").get(
        "/objects/host_config/myhost", {"effective_attributes": True}
    )

    assert open_url.call_args.args[0] == (
        "%s/objects/host_config/myhost?effective_attributes=True" % BASE_URL
    )


def test_no_parameters_means_no_query_string(open_url):
    _api("http://myserver").get("/version")

    assert open_url.call_args.args[0] == "%s/version" % BASE_URL


def test_empty_parameters_means_no_query_string(open_url):
    """An empty dict must not leave a dangling '?' on the URL."""
    _api("http://myserver").get("/version", {})

    assert open_url.call_args.args[0] == "%s/version" % BASE_URL


# ---------------------------------------------------------------------------
# POST
# ---------------------------------------------------------------------------


def test_get_uses_the_get_method(open_url):
    _api("http://myserver").get("/version")

    assert open_url.call_args.kwargs["method"] == "GET"
    assert open_url.call_args.kwargs["data"] is None


def test_post_sends_a_json_body(open_url):
    """Checkmk 3.0 drops the GET variants of the monitoring collections."""
    _api("http://myserver").post(
        "/domain-types/host/collections/all", {"query": {"op": "=", "left": "name"}}
    )

    assert (
        open_url.call_args.args[0] == "%s/domain-types/host/collections/all" % BASE_URL
    )
    assert open_url.call_args.kwargs["method"] == "POST"
    assert json.loads(open_url.call_args.kwargs["data"].decode("utf-8")) == {
        "query": {"op": "=", "left": "name"}
    }


def test_post_without_data_sends_an_empty_object(open_url):
    """Not `null` and not an empty body — the API expects a JSON object."""
    _api("http://myserver").post("/domain-types/activation_run/actions/activate/invoke")

    assert open_url.call_args.kwargs["data"] == b"{}"


def test_post_sends_the_json_content_type(open_url):
    _api("http://myserver").post("/domain-types/host/collections/all", {})

    headers = open_url.call_args.kwargs["headers"]
    assert headers["Content-Type"] == "application/json"
    assert headers["Authorization"] == "Bearer myuser mysecret"


def test_post_returns_the_response_body(open_url):
    open_url.return_value = MagicMock(read=MagicMock(return_value=b'{"value": []}'))

    assert _api("http://myserver").post("/domain-types/host/collections/all") == (
        '{"value": []}'
    )


# ---------------------------------------------------------------------------
# Error reporting
# ---------------------------------------------------------------------------


def test_error_detail_is_appended_to_the_canned_message(open_url):
    """The canned message says what failed, not which parameter failed."""
    open_url.side_effect = _http_error(
        400, json.dumps({"detail": "Invalid Livestatus query expression."})
    )

    response = json.loads(
        _api("http://myserver").get("/domain-types/host/collections/all")
    )

    assert response["code"] == 400
    assert response["msg"] == (
        "Bad Request: Parameter or validation failure. "
        "Invalid Livestatus query expression."
    )


def test_error_fields_are_appended_as_json(open_url):
    open_url.side_effect = _http_error(
        400, json.dumps({"fields": {"query": ["Unknown column 'nope'."]}})
    )

    msg = json.loads(_api("http://myserver").get("/x"))["msg"]

    assert msg.startswith("Bad Request: Parameter or validation failure. ")
    assert json.loads(msg.split(". ", 2)[-1]) == {"query": ["Unknown column 'nope'."]}


def test_error_detail_and_fields_are_both_reported(open_url):
    open_url.side_effect = _http_error(
        400, json.dumps({"detail": "Bad query.", "fields": {"query": ["nope"]}})
    )

    msg = json.loads(_api("http://myserver").get("/x"))["msg"]

    assert "Bad query." in msg
    assert "nope" in msg


def test_unparseable_error_body_falls_back_to_the_canned_message(open_url):
    """An HTML error page from a reverse proxy must not break the lookup."""
    open_url.side_effect = _http_error(404, "<html>404 not found</html>")

    response = json.loads(_api("http://myserver").get("/x"))

    assert response["msg"] == "Not Found: The requested object has not been found."


def test_non_dict_error_body_falls_back_to_the_canned_message(open_url):
    open_url.side_effect = _http_error(403, json.dumps(["nope"]))

    response = json.loads(_api("http://myserver").get("/x"))

    assert response["msg"] == "Forbidden: Configuration via Setup is disabled."


def test_unknown_status_code_uses_the_reason(open_url):
    """HTTP_ERROR_CODES only covers the codes the API documents."""
    open_url.side_effect = _http_error(
        500, json.dumps({"detail": "Internal error."}), reason="Internal Server Error"
    )

    response = json.loads(_api("http://myserver").get("/x"))

    assert response["code"] == 500
    assert response["msg"] == "Internal Server Error Internal error."


def test_post_errors_are_reported_like_get_errors(open_url):
    """Both verbs share _request, so both must surface the detail."""
    open_url.side_effect = _http_error(400, json.dumps({"detail": "Bad query."}))

    response = json.loads(_api("http://myserver").post("/x", {}))

    assert response["code"] == 400
    assert "Bad query." in response["msg"]


def test_url_error_is_reported_as_code_zero(open_url):
    open_url.side_effect = URLError("connection refused")

    response = json.loads(_api("http://myserver").get("/x"))

    assert response["code"] == 0
    assert "connection refused" in response["msg"]

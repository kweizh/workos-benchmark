import base64
import json
import os

import pytest

PROJECT_DIR = "/home/user/myproject"
TOKEN_FILE = os.path.join(PROJECT_DIR, "widget_token.txt")


def _read_token():
    assert os.path.isfile(TOKEN_FILE), (
        f"Expected widget token file at {TOKEN_FILE}, but it does not exist."
    )
    with open(TOKEN_FILE, "r") as f:
        return f.read().strip()


def _b64url_decode(segment: str) -> bytes:
    padding = "=" * (-len(segment) % 4)
    return base64.urlsafe_b64decode(segment + padding)


def test_widget_token_file_exists_and_non_empty():
    token = _read_token()
    assert token, f"{TOKEN_FILE} is empty; expected a non-empty JWT widget token."


def test_widget_token_has_jwt_structure():
    token = _read_token()
    parts = token.split(".")
    assert len(parts) == 3, (
        f"Expected JWT with three '.'-separated segments, got {len(parts)} segments. "
        f"Token contents: {token!r}"
    )
    for idx, segment in enumerate(parts):
        assert segment, f"JWT segment #{idx} is empty in {TOKEN_FILE}."


def test_widget_token_payload_iss_is_workos_api():
    token = _read_token()
    parts = token.split(".")
    assert len(parts) == 3, "Token is not a well-formed JWT."
    try:
        payload_bytes = _b64url_decode(parts[1])
    except Exception as exc:  # pragma: no cover - defensive
        pytest.fail(f"Failed to base64url-decode JWT payload: {exc}")
    try:
        payload = json.loads(payload_bytes.decode("utf-8"))
    except Exception as exc:
        pytest.fail(f"JWT payload is not valid JSON: {exc}")
    assert isinstance(payload, dict), "JWT payload is not a JSON object."
    iss = payload.get("iss")
    assert iss == "https://api.workos.com", (
        f"Expected JWT 'iss' claim to equal 'https://api.workos.com', got {iss!r}. "
        f"Full payload: {payload}"
    )


def test_widget_token_payload_contains_organization_and_user():
    token = _read_token()
    parts = token.split(".")
    payload = json.loads(_b64url_decode(parts[1]).decode("utf-8"))

    expected_org = os.environ.get("WORKOS_ORGANIZATION_ID")
    expected_user = os.environ.get("WORKOS_USER_ID")
    assert expected_org, (
        "WORKOS_ORGANIZATION_ID must be set in the verifier environment to validate the token."
    )
    assert expected_user, (
        "WORKOS_USER_ID must be set in the verifier environment to validate the token."
    )

    payload_str = json.dumps(payload)
    assert expected_org in payload_str, (
        f"Expected organization id {expected_org!r} to appear in JWT payload, got: {payload}"
    )
    assert expected_user in payload_str, (
        f"Expected user id {expected_user!r} to appear in JWT payload, got: {payload}"
    )

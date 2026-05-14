import base64
import json
import os
import time

import pytest

PROJECT_DIR = "/home/user/myproject"
INDEX_PATH = os.path.join(PROJECT_DIR, "index.js")
SESSION_PATH = os.path.join(PROJECT_DIR, "session.json")

EXPECTED_ISSUER = "https://api.workos.com/"


def _b64url_decode(segment: str) -> bytes:
    # JWT segments are base64url-encoded without padding.
    padding = "=" * (-len(segment) % 4)
    return base64.urlsafe_b64decode(segment + padding)


def _load_session():
    assert os.path.isfile(SESSION_PATH), (
        f"Expected session file at {SESSION_PATH}, but it was not found."
    )
    with open(SESSION_PATH, "r", encoding="utf-8") as f:
        raw = f.read()
    assert raw.strip(), f"Session file {SESSION_PATH} is empty."
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        pytest.fail(f"Session file {SESSION_PATH} is not valid JSON: {exc}")
    assert isinstance(data, dict), (
        f"Session file {SESSION_PATH} must contain a JSON object at the top level."
    )
    return data


def _decode_jwt_payload(token: str) -> dict:
    parts = token.split(".")
    assert len(parts) == 3, (
        f"Access token is not a well-formed JWT (expected 3 segments, got {len(parts)})."
    )
    payload_bytes = _b64url_decode(parts[1])
    try:
        payload = json.loads(payload_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        pytest.fail(f"JWT payload is not valid UTF-8 JSON: {exc}")
    assert isinstance(payload, dict), (
        "Decoded JWT payload must be a JSON object."
    )
    return payload


def test_index_js_exists():
    assert os.path.isfile(INDEX_PATH), (
        f"Expected the agent's Node.js script at {INDEX_PATH}, but it was not found."
    )


def test_session_file_has_required_keys():
    data = _load_session()
    assert "accessToken" in data, (
        f"Session file {SESSION_PATH} is missing the 'accessToken' key."
    )
    assert "refreshToken" in data, (
        f"Session file {SESSION_PATH} is missing the 'refreshToken' key."
    )
    assert isinstance(data["accessToken"], str) and data["accessToken"], (
        "Session file's 'accessToken' must be a non-empty string."
    )
    assert isinstance(data["refreshToken"], str) and data["refreshToken"], (
        "Session file's 'refreshToken' must be a non-empty string."
    )


def test_access_token_is_jwt_issued_by_workos():
    data = _load_session()
    access_token = data.get("accessToken", "")
    payload = _decode_jwt_payload(access_token)
    iss = payload.get("iss")
    assert iss == EXPECTED_ISSUER, (
        f"Expected access token issuer 'iss' to be {EXPECTED_ISSUER!r}, got {iss!r}. "
        "This indicates the token was not issued by WorkOS AuthKit."
    )


def test_access_token_has_not_expired():
    data = _load_session()
    access_token = data.get("accessToken", "")
    payload = _decode_jwt_payload(access_token)
    exp = payload.get("exp")
    assert isinstance(exp, int), (
        f"Expected access token 'exp' claim to be an integer Unix timestamp, got {exp!r}."
    )
    now = int(time.time())
    assert exp > now, (
        f"Access token has already expired: exp={exp}, now={now} (diff={exp - now}s)."
    )


def test_access_token_subject_is_workos_user():
    data = _load_session()
    access_token = data.get("accessToken", "")
    payload = _decode_jwt_payload(access_token)
    sub = payload.get("sub", "")
    assert isinstance(sub, str) and sub.startswith("user_"), (
        f"Expected access token 'sub' claim to start with 'user_' (WorkOS user id), got {sub!r}."
    )

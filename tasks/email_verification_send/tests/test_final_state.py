import json
import os
import urllib.error
import urllib.request

import pytest

PROJECT_DIR = "/home/user/myproject"
SCRIPT_PATH = os.path.join(PROJECT_DIR, "send_verification.js")
OUT_PATH = os.path.join(PROJECT_DIR, "verification.json")

WORKOS_API_KEY = os.environ.get("WORKOS_API_KEY")
WORKOS_USER_ID = os.environ.get("WORKOS_USER_ID")


def test_env():
    assert WORKOS_API_KEY and WORKOS_USER_ID


def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH)


def test_local_response():
    with open(OUT_PATH) as f:
        data = json.load(f)
    user = data.get("user") or {}
    assert user.get("id") == WORKOS_USER_ID, (
        f"Expected verification.json.user.id == {WORKOS_USER_ID!r}, got {user.get('id')!r}"
    )


def test_live_user_reachable():
    req = urllib.request.Request(
        f"https://api.workos.com/user_management/users/{WORKOS_USER_ID}",
        headers={
            "Authorization": f"Bearer {WORKOS_API_KEY}",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        pytest.fail(f"WorkOS API failed: HTTP {e.code} {e.read().decode('utf-8', errors='replace')}")
    assert body.get("id") == WORKOS_USER_ID

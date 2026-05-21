import json
import os
import re
import urllib.error
import urllib.request

import pytest

PROJECT_DIR = "/home/user/myproject"
SCRIPT_PATH = os.path.join(PROJECT_DIR, "create_user.js")
OUT_PATH = os.path.join(PROJECT_DIR, "user.json")

WORKOS_API_KEY = os.environ.get("WORKOS_API_KEY")
ZEALT_RUN_ID = (os.environ.get("ZEALT_RUN_ID") or "default").lower()
EFFECTIVE_EMAIL = f"pochi-user-{ZEALT_RUN_ID}@pochi-benchmark.example"


def test_env():
    assert WORKOS_API_KEY


def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH)


def test_local_user_json():
    with open(OUT_PATH) as f:
        data = json.load(f)
    uid = data.get("id")
    assert isinstance(uid, str) and re.match(r"^user_", uid)
    assert (data.get("email") or "").lower() == EFFECTIVE_EMAIL, (
        f"Expected email {EFFECTIVE_EMAIL!r}, got {data.get('email')!r}"
    )


def test_live_user():
    with open(OUT_PATH) as f:
        data = json.load(f)
    uid = data["id"]
    req = urllib.request.Request(
        f"https://api.workos.com/user_management/users/{uid}",
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
    assert body.get("id") == uid
    assert (body.get("email") or "").lower() == EFFECTIVE_EMAIL

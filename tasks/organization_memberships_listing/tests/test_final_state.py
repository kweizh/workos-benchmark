import json
import os
import urllib.error
import urllib.parse
import urllib.request

import pytest

PROJECT_DIR = "/home/user/myproject"
SCRIPT_PATH = os.path.join(PROJECT_DIR, "list_memberships.js")
OUT_PATH = os.path.join(PROJECT_DIR, "memberships.json")

WORKOS_API_KEY = os.environ.get("WORKOS_API_KEY")
WORKOS_ORGANIZATION_ID = os.environ.get("WORKOS_ORGANIZATION_ID")

REQUIRED = {"id", "user_id", "organization_id", "status"}


def _fetch_all_ids():
    ids = []
    after = None
    while True:
        params = {"organization_id": WORKOS_ORGANIZATION_ID, "limit": 100}
        if after:
            params["after"] = after
        url = f"https://api.workos.com/user_management/organization_memberships?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(url, headers={
            "Authorization": f"Bearer {WORKOS_API_KEY}",
            "Accept": "application/json",
        })
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                body = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            pytest.fail(f"WorkOS API failed: HTTP {e.code} {e.read().decode('utf-8', errors='replace')}")
        for m in body.get("data") or []:
            ids.append(m["id"])
        after = (body.get("list_metadata") or {}).get("after")
        if not after:
            break
    return ids


def test_env():
    assert WORKOS_API_KEY and WORKOS_ORGANIZATION_ID


def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH)


def test_local_shape():
    with open(OUT_PATH) as f:
        data = json.load(f)
    assert isinstance(data, list)
    for entry in data:
        assert set(entry.keys()) == REQUIRED
        assert entry["organization_id"] == WORKOS_ORGANIZATION_ID


def test_ids_match_live():
    with open(OUT_PATH) as f:
        data = json.load(f)
    local_ids = sorted(e["id"] for e in data)
    live_ids = sorted(_fetch_all_ids())
    assert local_ids == live_ids

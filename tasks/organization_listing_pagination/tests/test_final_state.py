import json
import os
import urllib.error
import urllib.parse
import urllib.request

import pytest

PROJECT_DIR = "/home/user/myproject"
SCRIPT_PATH = os.path.join(PROJECT_DIR, "list_orgs.js")
OUT_PATH = os.path.join(PROJECT_DIR, "organizations.json")

WORKOS_API_KEY = os.environ.get("WORKOS_API_KEY")


def _fetch_all_orgs():
    ids = []
    after = None
    while True:
        params = {"limit": 100}
        if after:
            params["after"] = after
        url = f"https://api.workos.com/organizations?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(
            url,
            headers={
                "Authorization": f"Bearer {WORKOS_API_KEY}",
                "Accept": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                body = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            pytest.fail(f"WorkOS API call failed: HTTP {e.code} {e.read().decode('utf-8', errors='replace')}")
        for org in body.get("data", []):
            ids.append(org["id"])
        after = (body.get("list_metadata") or {}).get("after")
        if not after:
            break
    return ids


def test_env():
    assert WORKOS_API_KEY, "WORKOS_API_KEY must be set."


def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Missing {SCRIPT_PATH}"


def test_local_json_shape():
    assert os.path.isfile(OUT_PATH)
    with open(OUT_PATH) as f:
        data = json.load(f)
    assert isinstance(data, list), f"Expected JSON array in {OUT_PATH}"
    for entry in data:
        assert isinstance(entry, dict)
        assert set(entry.keys()) == {"id", "name"}, (
            f"Each entry must have only keys id,name. Got: {sorted(entry.keys())}"
        )
        assert isinstance(entry["id"], str)
        assert isinstance(entry["name"], str)


def test_ids_match_live_api():
    with open(OUT_PATH) as f:
        data = json.load(f)
    local_ids = sorted(e["id"] for e in data)
    live_ids = sorted(_fetch_all_orgs())
    assert local_ids == live_ids, (
        f"Local org ids do not match live API:\n local={local_ids}\n live ={live_ids}"
    )

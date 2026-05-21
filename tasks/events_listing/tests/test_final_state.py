import json
import os
import urllib.error
import urllib.parse
import urllib.request

import pytest

PROJECT_DIR = "/home/user/myproject"
SCRIPT_PATH = os.path.join(PROJECT_DIR, "list_events.js")
OUT_PATH = os.path.join(PROJECT_DIR, "events.json")

WORKOS_API_KEY = os.environ.get("WORKOS_API_KEY")
REQUIRED = {"id", "event", "created_at"}


def _fetch_live_ids():
    qs = urllib.parse.urlencode({"events": "organization.created", "limit": 50})
    req = urllib.request.Request(
        f"https://api.workos.com/events?{qs}",
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
    return {ev["id"] for ev in body.get("data") or []}


def test_env():
    assert WORKOS_API_KEY


def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH)


def test_local_shape():
    with open(OUT_PATH) as f:
        data = json.load(f)
    assert isinstance(data, list)
    for entry in data:
        assert set(entry.keys()) == REQUIRED, (
            f"Expected keys {REQUIRED}, got {set(entry.keys())}"
        )
        assert entry["event"] == "organization.created"


def test_ids_subset_of_live():
    with open(OUT_PATH) as f:
        data = json.load(f)
    local_ids = {e["id"] for e in data}
    live_ids = _fetch_live_ids()
    if local_ids:
        assert local_ids.issubset(live_ids), (
            f"Local event ids not subset of live API: extra={local_ids - live_ids}"
        )

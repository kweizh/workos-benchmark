import json
import os
import urllib.error
import urllib.request

import pytest

PROJECT_DIR = "/home/user/myproject"
SCRIPT_PATH = os.path.join(PROJECT_DIR, "update_metadata.js")
ORG_JSON = os.path.join(PROJECT_DIR, "org.json")

WORKOS_API_KEY = os.environ.get("WORKOS_API_KEY")
WORKOS_ORGANIZATION_ID = os.environ.get("WORKOS_ORGANIZATION_ID")
ZEALT_RUN_ID = os.environ.get("ZEALT_RUN_ID") or "default"

METADATA_KEY = "pochi_benchmark_marker"
EFFECTIVE = f"pochi-mv-{ZEALT_RUN_ID}"


def test_env():
    assert WORKOS_API_KEY and WORKOS_ORGANIZATION_ID


def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH)


def test_org_json_local():
    with open(ORG_JSON) as f:
        data = json.load(f)
    assert data.get("id") == WORKOS_ORGANIZATION_ID
    md = data.get("metadata") or {}
    assert md.get(METADATA_KEY) == EFFECTIVE, (
        f"Expected metadata[{METADATA_KEY!r}] == {EFFECTIVE!r}, got {md.get(METADATA_KEY)!r}"
    )


def test_workos_api_metadata():
    url = f"https://api.workos.com/organizations/{WORKOS_ORGANIZATION_ID}"
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {WORKOS_API_KEY}",
        "Accept": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        pytest.fail(f"WorkOS API failed HTTP {e.code}: {e.read().decode('utf-8', errors='replace')}")
    md = body.get("metadata") or {}
    assert md.get(METADATA_KEY) == EFFECTIVE, (
        f"Live API metadata[{METADATA_KEY!r}] = {md.get(METADATA_KEY)!r}, expected {EFFECTIVE!r}"
    )

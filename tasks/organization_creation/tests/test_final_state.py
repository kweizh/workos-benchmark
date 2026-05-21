import json
import os
import re
import urllib.error
import urllib.request

import pytest

PROJECT_DIR = "/home/user/myproject"
SCRIPT_PATH = os.path.join(PROJECT_DIR, "create_org.js")
ORG_JSON = os.path.join(PROJECT_DIR, "org.json")

WORKOS_API_KEY = os.environ.get("WORKOS_API_KEY")
ZEALT_RUN_ID = os.environ.get("ZEALT_RUN_ID") or "default"

EXPECTED_NAME = f"pochi-benchmark-org-{ZEALT_RUN_ID}"


def test_required_env_vars_present():
    assert WORKOS_API_KEY, "WORKOS_API_KEY must be set for verification."


def test_create_org_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Expected {SCRIPT_PATH} to exist."


def test_org_json_exists_and_valid():
    assert os.path.isfile(ORG_JSON), f"Expected {ORG_JSON} to exist."
    with open(ORG_JSON) as f:
        data = json.load(f)
    assert isinstance(data, dict), f"Expected a JSON object in {ORG_JSON}, got {type(data)}"
    assert isinstance(data.get("id"), str) and re.match(r"^org_", data["id"]), (
        f"Expected id matching ^org_ in {ORG_JSON}, got {data.get('id')!r}"
    )
    assert data.get("name") == EXPECTED_NAME, (
        f"Expected name {EXPECTED_NAME!r} in {ORG_JSON}, got {data.get('name')!r}"
    )


def test_workos_api_reflects_created_org():
    with open(ORG_JSON) as f:
        data = json.load(f)
    org_id = data["id"]
    req = urllib.request.Request(
        f"https://api.workos.com/organizations/{org_id}",
        headers={
            "Authorization": f"Bearer {WORKOS_API_KEY}",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            assert resp.getcode() == 200
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        pytest.fail(
            f"WorkOS API request failed with HTTP {e.code}: {e.read().decode('utf-8', errors='replace')}"
        )
    assert body.get("id") == org_id
    assert body.get("name") == EXPECTED_NAME, (
        f"Expected WorkOS API to report name {EXPECTED_NAME!r}, got {body.get('name')!r}"
    )

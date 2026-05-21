import json
import os
import urllib.error
import urllib.request

import pytest

PROJECT_DIR = "/home/user/myproject"
SCRIPT_PATH = os.path.join(PROJECT_DIR, "revoke_invitation.js")
OUT_PATH = os.path.join(PROJECT_DIR, "invitation.json")

WORKOS_API_KEY = os.environ.get("WORKOS_API_KEY")
WORKOS_ORGANIZATION_ID = os.environ.get("WORKOS_ORGANIZATION_ID")
ZEALT_RUN_ID = (os.environ.get("ZEALT_RUN_ID") or "default").lower()
EFFECTIVE_EMAIL = f"pochi-invite-{ZEALT_RUN_ID}@pochi-benchmark.example"


def test_env():
    assert WORKOS_API_KEY and WORKOS_ORGANIZATION_ID


def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH)


def test_local_invitation_revoked():
    with open(OUT_PATH) as f:
        data = json.load(f)
    assert data.get("state") == "revoked", f"Expected state revoked, got {data.get('state')!r}"
    assert (data.get("email") or "").lower() == EFFECTIVE_EMAIL
    org_id = data.get("organization_id") or data.get("organizationId")
    assert org_id == WORKOS_ORGANIZATION_ID


def test_live_invitation_revoked():
    with open(OUT_PATH) as f:
        data = json.load(f)
    inv_id = data["id"]
    req = urllib.request.Request(
        f"https://api.workos.com/user_management/invitations/{inv_id}",
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
    assert body.get("state") == "revoked"

import json
import os
import urllib.error
import urllib.request

import pytest

PROJECT_DIR = "/home/user/myproject"
SCRIPT_PATH = os.path.join(PROJECT_DIR, "portal_dsync_link.js")
OUT_PATH = os.path.join(PROJECT_DIR, "portal_link.json")

WORKOS_API_KEY = os.environ.get("WORKOS_API_KEY")
WORKOS_ORGANIZATION_ID = os.environ.get("WORKOS_ORGANIZATION_ID")


def _generate_link_via_api():
    body = json.dumps({"organization": WORKOS_ORGANIZATION_ID, "intent": "dsync"}).encode("utf-8")
    req = urllib.request.Request(
        "https://api.workos.com/portal/generate_link",
        data=body,
        headers={
            "Authorization": f"Bearer {WORKOS_API_KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            assert resp.getcode() in (200, 201)
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        pytest.fail(f"WorkOS API failed: HTTP {e.code} {e.read().decode('utf-8', errors='replace')}")


def test_env():
    assert WORKOS_API_KEY and WORKOS_ORGANIZATION_ID


def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH)


def test_local_link():
    with open(OUT_PATH) as f:
        data = json.load(f)
    link = data.get("link")
    assert isinstance(link, str) and link.startswith("https://"), (
        f"Expected https link in {OUT_PATH}, got {link!r}"
    )


def test_live_generate_link_works():
    body = _generate_link_via_api()
    assert isinstance(body.get("link"), str) and body["link"].startswith("https://"), (
        f"Live API did not return https link: {body}"
    )

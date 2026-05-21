import json
import os
import urllib.error
import urllib.request

import pytest

PROJECT_DIR = "/home/user/myproject"
DEACTIVATE_JS = os.path.join(PROJECT_DIR, "deactivate_membership.js")
MEMBERSHIP_JSON = os.path.join(PROJECT_DIR, "membership.json")

WORKOS_API_KEY = os.environ.get("WORKOS_API_KEY")
WORKOS_ORG_MEMBERSHIP_ID = os.environ.get("WORKOS_ORG_MEMBERSHIP_ID")


def test_required_env_vars_present():
    assert WORKOS_API_KEY, "WORKOS_API_KEY must be set for verification."
    assert WORKOS_ORG_MEMBERSHIP_ID, "WORKOS_ORG_MEMBERSHIP_ID must be set for verification."


def test_deactivate_script_exists():
    assert os.path.isfile(DEACTIVATE_JS), (
        f"Expected the implementation script at {DEACTIVATE_JS}."
    )


def test_membership_json_exists_and_is_valid_json():
    assert os.path.isfile(MEMBERSHIP_JSON), (
        f"Expected {MEMBERSHIP_JSON} to exist after running deactivate_membership.js."
    )
    with open(MEMBERSHIP_JSON) as f:
        data = json.load(f)
    assert isinstance(data, dict), (
        f"{MEMBERSHIP_JSON} should contain a JSON object, got: {type(data)}"
    )


def test_membership_json_has_inactive_status():
    with open(MEMBERSHIP_JSON) as f:
        data = json.load(f)

    membership_id = data.get("id")
    assert membership_id == WORKOS_ORG_MEMBERSHIP_ID, (
        f"Expected membership.json id == {WORKOS_ORG_MEMBERSHIP_ID}, got: {membership_id!r}"
    )

    status = data.get("status")
    assert status == "inactive", (
        f"Expected membership.json status == 'inactive', got: {status!r}"
    )


def test_workos_api_reflects_inactive_status():
    """Independently fetch the organization membership from WorkOS to confirm the side effect is real."""
    url = (
        f"https://api.workos.com/user_management/organization_memberships/"
        f"{WORKOS_ORG_MEMBERSHIP_ID}"
    )
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {WORKOS_API_KEY}",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            status = resp.getcode()
            body = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        pytest.fail(
            f"WorkOS API request to {url} failed with HTTP {e.code}: "
            f"{e.read().decode('utf-8', errors='replace')}"
        )
    except urllib.error.URLError as e:
        pytest.fail(f"WorkOS API request to {url} failed: {e}")

    assert status == 200, f"Expected HTTP 200 from WorkOS API, got {status}: {body}"

    payload = json.loads(body)
    assert payload.get("id") == WORKOS_ORG_MEMBERSHIP_ID, (
        f"Expected API response id == {WORKOS_ORG_MEMBERSHIP_ID}, "
        f"got: {payload.get('id')!r}"
    )

    api_status = payload.get("status")
    assert api_status == "inactive", (
        f"Expected the WorkOS organization membership {WORKOS_ORG_MEMBERSHIP_ID} "
        f"to have status 'inactive', got: {api_status!r}"
    )

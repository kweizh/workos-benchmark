import json
import os
import subprocess

import pytest

PROJECT_DIR = "/home/user/myproject"
INDEX_JS = os.path.join(PROJECT_DIR, "index.js")
RESULT_JSON = os.path.join(PROJECT_DIR, "result.json")
WORKOS_API = "https://api.workos.com"


def _load_result():
    assert os.path.isfile(RESULT_JSON), f"Expected {RESULT_JSON} to exist after running the script."
    with open(RESULT_JSON, "r", encoding="utf-8") as f:
        text = f.read()
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        pytest.fail(f"{RESULT_JSON} is not valid JSON: {exc}\nContent: {text[:500]}")


def test_index_js_created():
    assert os.path.isfile(INDEX_JS), f"Expected {INDEX_JS} to be created by the agent."


def test_index_js_uses_update_with_admin_role():
    with open(INDEX_JS, "r", encoding="utf-8") as f:
        source = f.read()
    assert "updateOrganizationMembership" in source, (
        "index.js must call workos.userManagement.updateOrganizationMembership."
    )
    assert "admin" in source, "index.js must reference the 'admin' role slug."
    assert "roleSlug" in source or "role_slug" in source, (
        "index.js must pass a roleSlug parameter to updateOrganizationMembership."
    )


def test_result_json_exists_and_is_valid_json():
    data = _load_result()
    assert isinstance(data, dict), "result.json must contain a JSON object."


def test_result_json_membership_id_matches_env():
    expected_id = os.environ.get("WORKOS_ORG_MEMBERSHIP_ID")
    assert expected_id, "WORKOS_ORG_MEMBERSHIP_ID must be set in the verifier environment."
    data = _load_result()
    actual_id = data.get("id") or data.get("organization_membership", {}).get("id")
    assert actual_id == expected_id, (
        f"Expected result.json id == {expected_id!r}, got {actual_id!r}."
    )


def test_result_json_role_slug_is_admin():
    data = _load_result()
    role = data.get("role") or data.get("organization_membership", {}).get("role")
    assert isinstance(role, dict), (
        f"result.json must contain a 'role' object, got: {role!r}."
    )
    assert role.get("slug") == "admin", (
        f"Expected result.json role.slug == 'admin', got {role.get('slug')!r}."
    )


def test_live_membership_role_is_admin_on_workos():
    """Independently fetch the membership from the WorkOS API to confirm the role was
    actually persisted server-side (no mocking)."""
    api_key = os.environ.get("WORKOS_API_KEY")
    membership_id = os.environ.get("WORKOS_ORG_MEMBERSHIP_ID")
    assert api_key, "WORKOS_API_KEY must be set in the verifier environment."
    assert membership_id, "WORKOS_ORG_MEMBERSHIP_ID must be set in the verifier environment."

    url = f"{WORKOS_API}/user_management/organization_memberships/{membership_id}"
    result = subprocess.run(
        [
            "curl",
            "-sS",
            "-f",
            "-H",
            f"Authorization: Bearer {api_key}",
            "-H",
            "Accept: application/json",
            url,
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, (
        f"Failed to fetch membership from WorkOS: returncode={result.returncode}, "
        f"stderr={result.stderr}, stdout={result.stdout[:500]}"
    )
    try:
        live = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        pytest.fail(f"WorkOS API response was not valid JSON: {exc}\nBody: {result.stdout[:500]}")

    assert live.get("id") == membership_id, (
        f"WorkOS returned membership id {live.get('id')!r}, expected {membership_id!r}."
    )
    role = live.get("role")
    assert isinstance(role, dict), (
        f"WorkOS response must contain a 'role' object, got: {role!r}."
    )
    assert role.get("slug") == "admin", (
        f"Expected live WorkOS role.slug == 'admin', got {role.get('slug')!r}."
    )

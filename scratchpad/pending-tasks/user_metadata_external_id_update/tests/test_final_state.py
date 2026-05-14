import json
import os
import subprocess

PROJECT_DIR = "/home/user/myproject"
SCRIPT_PATH = os.path.join(PROJECT_DIR, "update_user.js")
OUTPUT_PATH = os.path.join(PROJECT_DIR, "user.json")


def _read_user_json():
    with open(OUTPUT_PATH) as f:
        return json.load(f)


def _fetch_user_via_workos_api():
    """Independently call the WorkOS API via @workos-inc/node to fetch the
    authoritative current state of the user. The verifier MUST NOT mock the
    SDK -- it talks to the real WorkOS API.
    """
    api_key = os.environ.get("WORKOS_API_KEY")
    user_id = os.environ.get("WORKOS_USER_ID")
    assert api_key, "WORKOS_API_KEY must be set in the verifier environment."
    assert user_id, "WORKOS_USER_ID must be set in the verifier environment."

    js = r"""
const { WorkOS } = require('@workos-inc/node');

(async () => {
  const workos = new WorkOS(process.env.WORKOS_API_KEY);
  const user = await workos.userManagement.getUser(process.env.WORKOS_USER_ID);
  process.stdout.write(JSON.stringify(user));
})().catch((err) => {
  console.error(err && err.stack ? err.stack : String(err));
  process.exit(1);
});
"""
    result = subprocess.run(
        ["node", "-e", js],
        capture_output=True,
        text=True,
        cwd=PROJECT_DIR,
        env=os.environ.copy(),
    )
    assert result.returncode == 0, (
        "Independent WorkOS API call failed in verifier: "
        f"stdout={result.stdout!r} stderr={result.stderr!r}"
    )
    return json.loads(result.stdout)


def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), (
        f"Expected script not found at {SCRIPT_PATH}."
    )


def test_output_file_exists():
    assert os.path.isfile(OUTPUT_PATH), (
        f"Expected output file not found at {OUTPUT_PATH}."
    )


def test_script_uses_real_workos_sdk():
    """The script must use the real @workos-inc/node SDK and read credentials from env."""
    with open(SCRIPT_PATH) as f:
        source = f.read()
    assert "@workos-inc/node" in source, (
        "update_user.js must import the @workos-inc/node SDK (no mocks/stubs)."
    )
    assert "updateUser" in source, (
        "update_user.js must call workos.userManagement.updateUser."
    )
    assert "WORKOS_API_KEY" in source, (
        "update_user.js must read WORKOS_API_KEY from environment variables."
    )
    assert "WORKOS_USER_ID" in source, (
        "update_user.js must read WORKOS_USER_ID from environment variables."
    )
    assert "WORKOS_NEW_EXTERNAL_ID" in source, (
        "update_user.js must read WORKOS_NEW_EXTERNAL_ID from environment variables."
    )


def test_user_json_contents_match_expected_values():
    """The saved user.json must reflect the requested updates."""
    user_id = os.environ.get("WORKOS_USER_ID")
    new_external_id = os.environ.get("WORKOS_NEW_EXTERNAL_ID")
    assert user_id, "WORKOS_USER_ID must be set in the verifier environment."
    assert new_external_id, (
        "WORKOS_NEW_EXTERNAL_ID must be set in the verifier environment."
    )

    user = _read_user_json()
    assert isinstance(user, dict), "user.json must contain a JSON object."

    assert user.get("id") == user_id, (
        f"user.json id mismatch: got {user.get('id')!r}, expected {user_id!r}."
    )
    assert user.get("externalId") == new_external_id, (
        "user.json externalId does not match WORKOS_NEW_EXTERNAL_ID: "
        f"got {user.get('externalId')!r}, expected {new_external_id!r}."
    )
    metadata = user.get("metadata")
    assert isinstance(metadata, dict), (
        f"user.json metadata must be an object, got {type(metadata).__name__}."
    )
    assert metadata.get("tier") == "premium", (
        "user.json metadata.tier must be the string 'premium', "
        f"got {metadata.get('tier')!r}."
    )


def test_workos_api_reflects_updates():
    """Priority 1: independently call the WorkOS API and assert the user state."""
    new_external_id = os.environ.get("WORKOS_NEW_EXTERNAL_ID")
    assert new_external_id, (
        "WORKOS_NEW_EXTERNAL_ID must be set in the verifier environment."
    )

    api_user = _fetch_user_via_workos_api()
    assert isinstance(api_user, dict), (
        "WorkOS getUser must return an object."
    )

    assert api_user.get("externalId") == new_external_id, (
        "WorkOS API reports a different externalId than expected: "
        f"got {api_user.get('externalId')!r}, expected {new_external_id!r}."
    )
    api_metadata = api_user.get("metadata")
    assert isinstance(api_metadata, dict), (
        "WorkOS API user.metadata must be an object, "
        f"got {type(api_metadata).__name__}."
    )
    assert api_metadata.get("tier") == "premium", (
        "WorkOS API user.metadata.tier must be 'premium', "
        f"got {api_metadata.get('tier')!r}."
    )

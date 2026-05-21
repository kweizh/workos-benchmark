import json
import os
import subprocess

PROJECT_DIR = "/home/user/myproject"
SCRIPT_PATH = os.path.join(PROJECT_DIR, "send_invitation.js")
OUTPUT_PATH = os.path.join(PROJECT_DIR, "invitation.json")


def _read_invitation_file():
    with open(OUTPUT_PATH) as f:
        return json.load(f)


def _fetch_invitation_via_workos_api(invitation_id):
    """Independently call the WorkOS API via @workos-inc/node to fetch the authoritative
    invitation record. The verifier MUST NOT mock the SDK — it talks to the real WorkOS API.
    """
    api_key = os.environ.get("WORKOS_API_KEY")
    assert api_key, "WORKOS_API_KEY must be set in the verifier environment."

    js = r"""
const { WorkOS } = require('@workos-inc/node');

(async () => {
  const workos = new WorkOS(process.env.WORKOS_API_KEY);
  const id = process.env.__VERIFY_INVITATION_ID;
  const invitation = await workos.userManagement.getInvitation(id);
  // Normalize into a plain JSON object that exposes id / state / email / organizationId.
  const out = {
    id: invitation.id,
    state: invitation.state,
    email: invitation.email,
    organizationId: invitation.organizationId,
  };
  process.stdout.write(JSON.stringify(out));
})().catch((err) => {
  console.error(err && err.stack ? err.stack : String(err));
  process.exit(1);
});
"""
    env = os.environ.copy()
    env["__VERIFY_INVITATION_ID"] = invitation_id
    result = subprocess.run(
        ["node", "-e", js],
        capture_output=True,
        text=True,
        cwd=PROJECT_DIR,
        env=env,
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
        "send_invitation.js must import the @workos-inc/node SDK (no mocks/stubs)."
    )
    assert "sendInvitation" in source, (
        "send_invitation.js must call workos.userManagement.sendInvitation."
    )
    assert "WORKOS_API_KEY" in source, (
        "send_invitation.js must read WORKOS_API_KEY from environment variables."
    )
    assert "WORKOS_ORGANIZATION_ID" in source, (
        "send_invitation.js must read WORKOS_ORGANIZATION_ID from environment variables."
    )
    assert "ZEALT_RUN_ID" in source, (
        "send_invitation.js must read ZEALT_RUN_ID from environment variables."
    )


def test_invitation_json_shape():
    """invitation.json must contain non-empty string `id` and `token` fields."""
    data = _read_invitation_file()
    assert isinstance(data, dict), (
        f"invitation.json must contain a JSON object, got: {type(data).__name__}"
    )
    assert "id" in data and isinstance(data["id"], str) and data["id"], (
        "invitation.json must contain a non-empty string `id`."
    )
    assert "token" in data and isinstance(data["token"], str) and data["token"], (
        "invitation.json must contain a non-empty string `token`."
    )
    assert data["id"].startswith("invitation_"), (
        f"Expected `id` to start with 'invitation_', got: {data['id']!r}"
    )


def test_invitation_matches_workos_api():
    """Priority 1: independently call the WorkOS API and confirm the invitation is pending
    and addressed to the expected email / organization."""
    run_id = os.environ.get("ZEALT_RUN_ID")
    expected_email = f"test-{run_id}@example.com" if run_id else os.environ.get("WORKOS_INVITE_EMAIL")
    expected_org = os.environ.get("WORKOS_ORGANIZATION_ID")
    assert expected_email, (
        "ZEALT_RUN_ID or WORKOS_INVITE_EMAIL must be set in the verifier environment."
    )
    assert expected_org, (
        "WORKOS_ORGANIZATION_ID must be set in the verifier environment."
    )

    data = _read_invitation_file()
    api_invitation = _fetch_invitation_via_workos_api(data["id"])

    assert api_invitation.get("state") == "pending", (
        "Invitation fetched from WorkOS must have state == 'pending', "
        f"got: {api_invitation.get('state')!r}"
    )
    assert (
        (api_invitation.get("email") or "").lower() == expected_email.lower()
    ), (
        "Invitation email returned by WorkOS does not match expected email.\n"
        f"  WorkOS: {api_invitation.get('email')!r}\n"
        f"  expected: {expected_email!r}"
    )
    assert api_invitation.get("organizationId") == expected_org, (
        "Invitation organizationId returned by WorkOS does not match WORKOS_ORGANIZATION_ID.\n"
        f"  WorkOS: {api_invitation.get('organizationId')!r}\n"
        f"  expected: {expected_org!r}"
    )

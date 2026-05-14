import json
import os
import subprocess

PROJECT_DIR = "/home/user/myproject"
FACTOR_JSON = os.path.join(PROJECT_DIR, "factor.json")


def _load_factor_json():
    assert os.path.isfile(FACTOR_JSON), (
        f"Expected {FACTOR_JSON} to exist after task completion."
    )
    with open(FACTOR_JSON) as f:
        text = f.read()
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise AssertionError(
            f"{FACTOR_JSON} is not valid JSON. Error: {e}. Content: {text!r}"
        )


def test_factor_json_exists_and_has_required_fields():
    data = _load_factor_json()
    assert isinstance(data, dict), (
        f"factor.json must be a JSON object, got: {type(data).__name__}"
    )
    factor_id = data.get("id")
    assert isinstance(factor_id, str) and factor_id.startswith("auth_factor_"), (
        f"Expected 'id' to be a string starting with 'auth_factor_' in factor.json, got: {factor_id!r}"
    )
    assert data.get("type") == "totp", (
        f"Expected 'type' to be 'totp' in factor.json, got: {data.get('type')!r}"
    )
    qr_code = data.get("qr_code")
    assert isinstance(qr_code, str) and len(qr_code) > 0, (
        f"Expected non-empty 'qr_code' string in factor.json, got: {qr_code!r}"
    )


def test_factor_retrievable_via_workos_api():
    """Priority 1: call the real WorkOS API via the SDK to confirm the
    enrolled TOTP factor actually exists in the WorkOS account."""
    data = _load_factor_json()
    factor_id = data["id"]

    api_key = os.environ.get("WORKOS_API_KEY")
    assert api_key, "WORKOS_API_KEY must be set in the verifier environment."

    verifier_script = f"""
const {{ WorkOS }} = require('@workos-inc/node');
const apiKey = process.env.WORKOS_API_KEY;
if (!apiKey) {{
  console.error('WORKOS_API_KEY not set');
  process.exit(2);
}}
const workos = new WorkOS(apiKey);
(async () => {{
  try {{
    const factor = await workos.mfa.getFactor({json.dumps(factor_id)});
    process.stdout.write(JSON.stringify({{
      id: factor.id,
      type: factor.type,
    }}));
  }} catch (e) {{
    console.error('getFactor failed:', e && e.message ? e.message : String(e));
    process.exit(3);
  }}
}})();
"""

    result = subprocess.run(
        ["node", "-e", verifier_script],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        env={**os.environ},
        timeout=60,
    )

    assert result.returncode == 0, (
        f"workos.mfa.getFactor call failed (rc={result.returncode}). "
        f"stdout={result.stdout!r} stderr={result.stderr!r}"
    )

    try:
        api_data = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        raise AssertionError(
            f"Could not parse JSON from getFactor output: {e}. stdout={result.stdout!r}"
        )

    assert api_data.get("id") == factor_id, (
        f"WorkOS returned factor id {api_data.get('id')!r}, expected {factor_id!r}."
    )
    assert api_data.get("type") == "totp", (
        f"WorkOS returned factor type {api_data.get('type')!r}, expected 'totp'."
    )

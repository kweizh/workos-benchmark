import json
import os
import subprocess

import pytest

PROJECT_DIR = "/home/user/myproject"
INDEX_JS = os.path.join(PROJECT_DIR, "index.js")
WARRANTS_JSON = os.path.join(PROJECT_DIR, "warrants.json")
TRIAL_ID_PATH = "/logs/artifacts/trial_id"
VERIFY_JS = os.path.join(PROJECT_DIR, "verify.js")


def _read_trial_id() -> str:
    assert os.path.isfile(TRIAL_ID_PATH), (
        f"Trial id file {TRIAL_ID_PATH} not found; cannot derive expected identifiers."
    )
    with open(TRIAL_ID_PATH) as f:
        trial_id = f.read().strip()
    assert trial_id, f"Trial id at {TRIAL_ID_PATH} is empty."
    return trial_id


def test_index_js_exists():
    assert os.path.isfile(INDEX_JS), f"{INDEX_JS} was not created by the agent."


def test_index_js_uses_batch_write_warrants():
    with open(INDEX_JS) as f:
        content = f.read()
    assert "batchWriteWarrants" in content, (
        f"{INDEX_JS} must call workos.fga.batchWriteWarrants(...); not found in the file."
    )


def test_warrants_json_exists_and_has_token():
    assert os.path.isfile(WARRANTS_JSON), f"{WARRANTS_JSON} was not created by the agent."
    with open(WARRANTS_JSON) as f:
        data = json.load(f)
    token = data.get("warrantToken") if isinstance(data, dict) else None
    assert isinstance(token, str) and token, (
        f"{WARRANTS_JSON} must contain a non-empty string `warrantToken` field returned by "
        f"workos.fga.batchWriteWarrants(...). Got: {data!r}"
    )


@pytest.fixture(scope="module")
def write_verify_script():
    """Write a Node.js verifier script that calls workos.fga.check for each user."""
    script = r"""
const fs = require('fs');
const { WorkOS } = require('@workos-inc/node');

async function main() {
  const trialId = fs.readFileSync('/logs/artifacts/trial_id', 'utf8').trim();
  const documentId = `doc-batch-${trialId}`;
  const userIds = [
    `user-batch-1-${trialId}`,
    `user-batch-2-${trialId}`,
    `user-batch-3-${trialId}`,
  ];

  const warrantsPath = '/home/user/myproject/warrants.json';
  const warrantData = JSON.parse(fs.readFileSync(warrantsPath, 'utf8'));
  const warrantToken = warrantData.warrantToken;
  if (!warrantToken || typeof warrantToken !== 'string') {
    console.error(JSON.stringify({ error: 'warrants.json missing warrantToken', warrantData }));
    process.exit(2);
  }

  const apiKey = process.env.WORKOS_API_KEY;
  if (!apiKey) {
    console.error(JSON.stringify({ error: 'WORKOS_API_KEY env var is not set in verifier' }));
    process.exit(3);
  }

  const workos = new WorkOS(apiKey);
  const results = {};
  for (const userId of userIds) {
    const checkResult = await workos.fga.check(
      {
        checks: [
          {
            resource: { resourceType: 'document', resourceId: documentId },
            relation: 'viewer',
            subject: { resourceType: 'user', resourceId: userId },
          },
        ],
      },
      { warrantToken },
    );
    results[userId] = checkResult.isAuthorized();
  }

  console.log(JSON.stringify({ documentId, results }));
}

main().catch((err) => {
  console.error(JSON.stringify({ error: String(err && err.message || err) }));
  process.exit(1);
});
"""
    with open(VERIFY_JS, "w") as f:
        f.write(script)
    yield VERIFY_JS


def test_workos_check_returns_authorized_for_each_user(write_verify_script):
    trial_id = _read_trial_id()
    expected_doc = f"doc-batch-{trial_id}"
    expected_users = [
        f"user-batch-1-{trial_id}",
        f"user-batch-2-{trial_id}",
        f"user-batch-3-{trial_id}",
    ]

    api_key = os.environ.get("WORKOS_API_KEY")
    assert api_key, "WORKOS_API_KEY env var must be set in the verifier environment."

    env = os.environ.copy()
    env["WORKOS_API_KEY"] = api_key

    result = subprocess.run(
        ["node", VERIFY_JS],
        capture_output=True,
        text=True,
        cwd=PROJECT_DIR,
        env=env,
        timeout=120,
    )
    assert result.returncode == 0, (
        f"Verifier script `node verify.js` failed with exit code {result.returncode}.\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )

    # The last non-empty stdout line should be the JSON payload from verify.js.
    stdout_lines = [line for line in result.stdout.strip().splitlines() if line.strip()]
    assert stdout_lines, f"Verifier produced no stdout. stderr: {result.stderr}"
    try:
        payload = json.loads(stdout_lines[-1])
    except json.JSONDecodeError as exc:
        pytest.fail(
            f"Could not parse verifier JSON output: {exc}\nstdout: {result.stdout}"
        )

    assert payload.get("documentId") == expected_doc, (
        f"Expected documentId={expected_doc} in verifier output, got: {payload!r}"
    )
    results = payload.get("results") or {}
    for user_id in expected_users:
        assert user_id in results, (
            f"Expected user id {user_id} in verifier results, got: {results!r}"
        )
        assert results[user_id] is True, (
            f"workos.fga.check returned isAuthorized={results[user_id]!r} for {user_id}; "
            f"expected True. Full results: {results!r}"
        )

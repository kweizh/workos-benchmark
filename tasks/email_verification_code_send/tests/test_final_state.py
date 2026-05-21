import json
import os
import re
import subprocess

import pytest

PROJECT_DIR = "/home/user/myproject"
INDEX_JS = os.path.join(PROJECT_DIR, "index.js")
PACKAGE_JSON = os.path.join(PROJECT_DIR, "package.json")
SDK_PACKAGE_JSON = os.path.join(
    PROJECT_DIR, "node_modules", "@workos-inc", "node", "package.json"
)
LOG_FILE = os.path.join(PROJECT_DIR, "output.log")

SUCCESS_LINE_RE = re.compile(
    r"^SUCCESS\s+user_id=user_\S+\s+email=\S+@\S+\s*$"
)


def _read(path):
    with open(path, "r") as f:
        return f.read()


def test_package_json_lists_workos_sdk():
    assert os.path.isfile(PACKAGE_JSON), f"{PACKAGE_JSON} is missing."
    data = json.loads(_read(PACKAGE_JSON))
    deps = {}
    for key in ("dependencies", "devDependencies"):
        if isinstance(data.get(key), dict):
            deps.update(data[key])
    assert (
        "@workos-inc/node" in deps
    ), f"`@workos-inc/node` must be listed under dependencies in {PACKAGE_JSON}. Got: {deps}"


def test_workos_sdk_installed_in_node_modules():
    assert os.path.isfile(SDK_PACKAGE_JSON), (
        "The @workos-inc/node SDK must be installed in node_modules "
        f"(missing {SDK_PACKAGE_JSON})."
    )
    sdk_meta = json.loads(_read(SDK_PACKAGE_JSON))
    assert (
        sdk_meta.get("name") == "@workos-inc/node"
    ), f"Unexpected package metadata in {SDK_PACKAGE_JSON}: {sdk_meta.get('name')}"


def test_index_js_exists():
    assert os.path.isfile(INDEX_JS), f"{INDEX_JS} must exist."


def test_index_js_uses_real_workos_sdk():
    src = _read(INDEX_JS)
    uses_require = (
        "require('@workos-inc/node')" in src
        or 'require("@workos-inc/node")' in src
    )
    uses_import = (
        "from '@workos-inc/node'" in src or 'from "@workos-inc/node"' in src
    )
    assert uses_require or uses_import, (
        "index.js must import the real @workos-inc/node SDK "
        "(via require or ES import)."
    )


def test_index_js_reads_env_vars():
    src = _read(INDEX_JS)
    assert (
        "process.env.WORKOS_API_KEY" in src
    ), "index.js must read WORKOS_API_KEY from process.env."
    assert (
        "process.env.WORKOS_USER_ID" in src
    ), "index.js must read WORKOS_USER_ID from process.env."


def test_index_js_calls_send_verification_email():
    src = _read(INDEX_JS)
    assert (
        "sendVerificationEmail" in src
    ), "index.js must call userManagement.sendVerificationEmail (the real email verification method)."
    assert (
        "userManagement" in src
    ), "index.js must use the workos.userManagement namespace."


def test_index_js_does_not_mock_workos_api():
    src = _read(INDEX_JS)
    forbidden = [
        "jest.mock",
        "sinon.stub",
        "sinon.replace",
        "nock(",
        "MockAdapter",
        "axios-mock-adapter",
        "class WorkOS",
        "function WorkOS",
    ]
    for pattern in forbidden:
        assert (
            pattern not in src
        ), f"index.js must not mock the WorkOS API, but found forbidden pattern: {pattern!r}"


def test_output_log_contains_success_entry():
    assert os.path.isfile(LOG_FILE), f"{LOG_FILE} must exist after the task is performed."
    content = _read(LOG_FILE).strip()
    assert content, f"{LOG_FILE} must not be empty."
    matched = any(SUCCESS_LINE_RE.match(line) for line in content.splitlines())
    assert matched, (
        "output.log must contain a line like "
        "'SUCCESS user_id=user_<id> email=<addr>'. "
        f"Got:\n{content}"
    )


def test_workos_user_resolvable_via_live_get_user():
    """Use the live WorkOS API via the installed SDK to confirm WORKOS_USER_ID is valid.

    Calls `workos.userManagement.getUser(userId)` and asserts the returned user's
    id matches WORKOS_USER_ID. This proves the user targeted by sendVerificationEmail
    is a real WorkOS user accessible with the configured API key.
    """
    api_key = os.environ.get("WORKOS_API_KEY")
    user_id = os.environ.get("WORKOS_USER_ID")
    if not api_key or not user_id:
        pytest.skip(
            "Verifier missing WORKOS_API_KEY / WORKOS_USER_ID; skipping live API check."
        )

    probe = r"""
const { WorkOS } = require('@workos-inc/node');
(async () => {
  try {
    const workos = new WorkOS(process.env.WORKOS_API_KEY);
    const user = await workos.userManagement.getUser(process.env.WORKOS_USER_ID);
    process.stdout.write(JSON.stringify({ ok: true, id: user.id, email: user.email }));
  } catch (err) {
    process.stdout.write(JSON.stringify({ ok: false, error: err.message }));
    process.exit(1);
  }
})();
"""

    env = os.environ.copy()
    env["WORKOS_API_KEY"] = api_key
    env["WORKOS_USER_ID"] = user_id

    result = subprocess.run(
        ["node", "-e", probe],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        env=env,
        timeout=60,
    )

    assert result.returncode == 0, (
        "Live `workos.userManagement.getUser(WORKOS_USER_ID)` call failed.\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )

    try:
        payload = json.loads(result.stdout.strip())
    except json.JSONDecodeError as e:
        pytest.fail(
            f"Could not parse JSON from getUser probe stdout: {result.stdout!r} ({e})"
        )

    assert payload.get("ok") is True, (
        f"getUser probe reported failure: {payload}"
    )
    assert (
        payload.get("id") == user_id
    ), f"Expected getUser to return id={user_id}, got {payload.get('id')}"
    assert payload.get("email"), (
        f"Expected getUser response to include a non-empty email field, got: {payload}"
    )

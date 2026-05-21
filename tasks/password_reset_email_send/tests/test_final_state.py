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


def _read(path):
    with open(path, "r") as f:
        return f.read()


def _success_line_re():
    email = os.environ.get("WORKOS_TEST_EMAIL", "")
    assert email, "WORKOS_TEST_EMAIL must be set in the verifier environment."
    return re.compile(
        r"^SUCCESS\s+password_reset_id=password_reset_\S+\s+email="
        + re.escape(email)
        + r"\s*$"
    )


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
        "process.env.WORKOS_TEST_EMAIL" in src
    ), "index.js must read WORKOS_TEST_EMAIL from process.env."


def test_index_js_calls_create_password_reset():
    src = _read(INDEX_JS)
    assert (
        "createPasswordReset" in src
    ), "index.js must call userManagement.createPasswordReset (the real Password Reset method)."
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
    matched = any(_success_line_re().match(line) for line in content.splitlines())
    assert matched, (
        "output.log must contain a line like "
        "'SUCCESS password_reset_id=password_reset_<id> email=<WORKOS_TEST_EMAIL>'. "
        f"Got:\n{content}"
    )


def test_output_log_contains_password_reset_object():
    content = _read(LOG_FILE)
    object_lines = [
        line for line in content.splitlines() if line.startswith("OBJECT ")
    ]
    assert object_lines, (
        "output.log must contain at least one line starting with 'OBJECT ' followed by "
        f"the serialized password-reset JSON. Got:\n{content}"
    )
    payload = object_lines[0][len("OBJECT "):].strip()
    try:
        obj = json.loads(payload)
    except json.JSONDecodeError as e:
        pytest.fail(f"OBJECT payload is not valid JSON: {payload!r} ({e})")
    assert obj.get("object") == "password_reset", (
        f"OBJECT payload must have object='password_reset', got: {obj.get('object')!r}"
    )
    pr_id = obj.get("id", "")
    assert pr_id.startswith("password_reset_"), (
        f"OBJECT payload id must start with 'password_reset_', got: {pr_id!r}"
    )


def test_script_can_call_live_workos_api():
    """Re-run the script against the live WorkOS API and confirm a new SUCCESS line."""
    api_key = os.environ.get("WORKOS_API_KEY")
    test_email = os.environ.get("WORKOS_TEST_EMAIL")
    assert api_key and test_email, (
        "Verifier requires WORKOS_API_KEY and WORKOS_TEST_EMAIL to be set."
    )

    before = ""
    if os.path.isfile(LOG_FILE):
        before = _read(LOG_FILE)

    env = os.environ.copy()
    env["WORKOS_API_KEY"] = api_key
    env["WORKOS_TEST_EMAIL"] = test_email

    result = subprocess.run(
        ["node", "index.js"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        env=env,
        timeout=60,
    )
    assert result.returncode == 0, (
        f"Re-running `node index.js` against the live WorkOS API failed.\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )

    after = _read(LOG_FILE)
    new_content = after[len(before):]
    matched = any(_success_line_re().match(line) for line in new_content.splitlines())
    assert matched, (
        "After re-running the script against the live WorkOS API, "
        "a new 'SUCCESS password_reset_id=password_reset_...' line should have been "
        f"appended to {LOG_FILE}. New content was:\n{new_content!r}"
    )


def test_workos_test_email_resolves_to_real_user():
    """Use the live WorkOS API via the installed SDK to confirm the test email is a real user."""
    api_key = os.environ.get("WORKOS_API_KEY")
    test_email = os.environ.get("WORKOS_TEST_EMAIL")
    assert api_key and test_email, (
        "Verifier requires WORKOS_API_KEY and WORKOS_TEST_EMAIL to be set."
    )

    verifier_script = (
        "const { WorkOS } = require('@workos-inc/node');\n"
        "(async () => {\n"
        "  const workos = new WorkOS(process.env.WORKOS_API_KEY);\n"
        "  const result = await workos.userManagement.listUsers({ email: process.env.WORKOS_TEST_EMAIL });\n"
        "  const users = (result && result.data) ? result.data : (Array.isArray(result) ? result : []);\n"
        "  const out = users.map(u => ({ id: u.id, email: u.email }));\n"
        "  process.stdout.write(JSON.stringify(out));\n"
        "})().catch(err => { console.error(err && err.message ? err.message : String(err)); process.exit(2); });\n"
    )

    env = os.environ.copy()
    env["WORKOS_API_KEY"] = api_key
    env["WORKOS_TEST_EMAIL"] = test_email

    result = subprocess.run(
        ["node", "-e", verifier_script],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        env=env,
        timeout=60,
    )
    assert result.returncode == 0, (
        "Calling workos.userManagement.listUsers against the live WorkOS API failed.\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )
    try:
        users = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        pytest.fail(
            f"listUsers verifier did not produce JSON output: {result.stdout!r} ({e})"
        )
    assert isinstance(users, list) and users, (
        "listUsers must return at least one user for WORKOS_TEST_EMAIL "
        f"({test_email}); got: {users!r}"
    )
    emails = [u.get("email", "").lower() for u in users]
    assert test_email.lower() in emails, (
        f"WORKOS_TEST_EMAIL ({test_email}) must be a real WorkOS user. "
        f"listUsers returned: {users!r}"
    )

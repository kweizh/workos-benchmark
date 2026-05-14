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
    r"^SUCCESS\s+magic_auth_id=magic_auth_\S+\s+email=passwordless-otp-test@example\.com\s*$"
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
    uses_require = "require('@workos-inc/node')" in src or 'require("@workos-inc/node")' in src
    uses_import = "from '@workos-inc/node'" in src or 'from "@workos-inc/node"' in src
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
        "process.env.WORKOS_CLIENT_ID" in src
    ), "index.js must read WORKOS_CLIENT_ID from process.env."


def test_index_js_calls_create_magic_auth():
    src = _read(INDEX_JS)
    assert (
        "createMagicAuth" in src
    ), "index.js must call userManagement.createMagicAuth (the real Magic Auth/OTP method)."
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
        "'SUCCESS magic_auth_id=magic_auth_<id> email=passwordless-otp-test@example.com'. "
        f"Got:\n{content}"
    )


def test_script_can_call_live_workos_api():
    """Run the script again against the live WorkOS API and confirm a new SUCCESS line."""
    api_key = os.environ.get("WORKOS_API_KEY")
    client_id = os.environ.get("WORKOS_CLIENT_ID")
    if not api_key or not client_id:
        pytest.skip("Verifier missing WORKOS_API_KEY / WORKOS_CLIENT_ID; skipping live API check.")

    before = ""
    if os.path.isfile(LOG_FILE):
        before = _read(LOG_FILE)

    env = os.environ.copy()
    env["WORKOS_API_KEY"] = api_key
    env["WORKOS_CLIENT_ID"] = client_id

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
    matched = any(SUCCESS_LINE_RE.match(line) for line in new_content.splitlines())
    assert matched, (
        "After re-running the script against the live WorkOS API, "
        "a new 'SUCCESS magic_auth_id=magic_auth_...' line should have been appended "
        f"to {LOG_FILE}. New content was:\n{new_content!r}"
    )

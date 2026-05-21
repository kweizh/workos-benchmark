import json
import os
import shutil
import subprocess

import pytest

PROJECT_DIR = "/home/user/myproject"


def test_node_binary_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."


def test_npm_binary_available():
    assert shutil.which("npm") is not None, "npm binary not found in PATH."


def test_node_major_version_is_24():
    result = subprocess.run(
        ["node", "--version"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, f"'node --version' failed: {result.stderr}"
    version = result.stdout.strip()
    assert version.startswith("v24."), f"Expected Node.js v24.x, got {version!r}."


def test_workos_api_key_env_set():
    value = os.environ.get("WORKOS_API_KEY")
    assert value, "Environment variable WORKOS_API_KEY must be set in the task environment."


def test_workos_org_membership_id_env_set():
    value = os.environ.get("WORKOS_ORG_MEMBERSHIP_ID")
    assert value, "Environment variable WORKOS_ORG_MEMBERSHIP_ID must be set in the task environment."


def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."


def test_project_package_json_exists():
    package_json = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(package_json), f"{package_json} does not exist."


def test_workos_sdk_installed():
    sdk_pkg = os.path.join(PROJECT_DIR, "node_modules", "@workos-inc", "node", "package.json")
    assert os.path.isfile(sdk_pkg), (
        f"@workos-inc/node SDK is not installed at {sdk_pkg}."
    )
    with open(sdk_pkg, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data.get("name") == "@workos-inc/node", (
        f"Unexpected SDK package name: {data.get('name')!r}."
    )


def test_result_json_not_yet_created():
    # The agent is expected to create result.json; it must not exist beforehand.
    result_path = os.path.join(PROJECT_DIR, "result.json")
    assert not os.path.exists(result_path), (
        f"{result_path} must not exist before the task is performed."
    )


def test_index_js_not_yet_created():
    # The agent is expected to author index.js.
    index_path = os.path.join(PROJECT_DIR, "index.js")
    assert not os.path.exists(index_path), (
        f"{index_path} must not exist before the task is performed."
    )

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
        ["node", "--version"], capture_output=True, text=True, check=False
    )
    assert result.returncode == 0, f"`node --version` failed: {result.stderr}"
    version = result.stdout.strip().lstrip("v")
    major = version.split(".")[0]
    assert major == "24", f"Expected Node.js major version 24, got: {result.stdout!r}"


def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."


def test_package_json_exists():
    package_json = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(package_json), f"{package_json} does not exist."


def test_workos_sdk_installed():
    sdk_dir = os.path.join(PROJECT_DIR, "node_modules", "@workos-inc", "node")
    assert os.path.isdir(sdk_dir), (
        f"@workos-inc/node SDK is not installed at {sdk_dir}. "
        "Pre-task setup should have installed it via `npm install @workos-inc/node`."
    )


def test_workos_sdk_package_json_declares_name():
    sdk_package_json = os.path.join(
        PROJECT_DIR, "node_modules", "@workos-inc", "node", "package.json"
    )
    assert os.path.isfile(sdk_package_json), (
        f"@workos-inc/node package.json not found at {sdk_package_json}."
    )
    with open(sdk_package_json) as f:
        data = json.load(f)
    assert data.get("name") == "@workos-inc/node", (
        f"Expected name '@workos-inc/node' in {sdk_package_json}, got: {data.get('name')!r}"
    )


def test_index_js_not_created_yet():
    index_js = os.path.join(PROJECT_DIR, "index.js")
    assert not os.path.exists(index_js), (
        f"{index_js} should not exist in the initial state; the agent will create it."
    )


def test_export_json_not_created_yet():
    export_json = os.path.join(PROJECT_DIR, "export.json")
    assert not os.path.exists(export_json), (
        f"{export_json} should not exist in the initial state; the agent will create it."
    )


def test_audit_csv_not_created_yet():
    audit_csv = os.path.join(PROJECT_DIR, "audit.csv")
    assert not os.path.exists(audit_csv), (
        f"{audit_csv} should not exist in the initial state; the agent will create it."
    )


def test_workos_api_key_env_var_is_set():
    api_key = os.environ.get("WORKOS_API_KEY")
    assert api_key, "WORKOS_API_KEY environment variable must be set in the task environment."


def test_workos_organization_id_env_var_is_set():
    organization_id = os.environ.get("WORKOS_ORGANIZATION_ID")
    assert organization_id, (
        "WORKOS_ORGANIZATION_ID environment variable must be set in the task environment."
    )

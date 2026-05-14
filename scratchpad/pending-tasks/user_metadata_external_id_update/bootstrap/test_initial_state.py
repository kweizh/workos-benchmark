import json
import os
import shutil

PROJECT_DIR = "/home/user/myproject"


def test_node_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."


def test_npm_available():
    assert shutil.which("npm") is not None, "npm binary not found in PATH."


def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), (
        f"Project directory {PROJECT_DIR} does not exist."
    )


def test_package_json_exists():
    package_json = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(package_json), (
        f"package.json not found at {package_json}."
    )


def test_workos_sdk_installed():
    sdk_dir = os.path.join(PROJECT_DIR, "node_modules", "@workos-inc", "node")
    assert os.path.isdir(sdk_dir), (
        f"@workos-inc/node SDK is not installed at {sdk_dir}."
    )


def test_workos_sdk_listed_as_dependency():
    package_json = os.path.join(PROJECT_DIR, "package.json")
    with open(package_json) as f:
        data = json.load(f)
    deps = data.get("dependencies", {})
    assert "@workos-inc/node" in deps, (
        "@workos-inc/node should be declared in package.json dependencies."
    )


def test_workos_api_key_env():
    assert os.environ.get("WORKOS_API_KEY"), (
        "WORKOS_API_KEY environment variable must be set in the task environment."
    )


def test_workos_user_id_env():
    assert os.environ.get("WORKOS_USER_ID"), (
        "WORKOS_USER_ID environment variable must be set in the task environment."
    )


def test_workos_new_external_id_env():
    assert os.environ.get("WORKOS_NEW_EXTERNAL_ID"), (
        "WORKOS_NEW_EXTERNAL_ID environment variable must be set in the task environment."
    )

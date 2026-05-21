import os
import shutil
import subprocess

PROJECT_DIR = "/home/user/myproject"


def test_node_binary_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."


def test_npm_binary_available():
    assert shutil.which("npm") is not None, "npm binary not found in PATH."


def test_node_major_version_is_24():
    result = subprocess.run(
        ["node", "--version"], capture_output=True, text=True
    )
    assert result.returncode == 0, f"`node --version` failed: {result.stderr}"
    version = result.stdout.strip()
    assert version.startswith("v24."), (
        f"Expected Node.js v24.x in the environment, got: {version}"
    )


def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), (
        f"Expected project directory {PROJECT_DIR} to exist in the initial environment."
    )


def test_widget_token_not_yet_created():
    token_path = os.path.join(PROJECT_DIR, "widget_token.txt")
    assert not os.path.exists(token_path), (
        f"Expected {token_path} to be absent before the task starts."
    )


def test_workos_api_key_env_var_present():
    assert os.environ.get("WORKOS_API_KEY"), (
        "WORKOS_API_KEY must be set in the environment for the task to run against the real WorkOS API."
    )


def test_workos_organization_id_env_var_present():
    assert os.environ.get("WORKOS_ORGANIZATION_ID"), (
        "WORKOS_ORGANIZATION_ID must be set in the environment for the task."
    )


def test_workos_user_id_env_var_present():
    assert os.environ.get("WORKOS_USER_ID"), (
        "WORKOS_USER_ID must be set in the environment for the task."
    )

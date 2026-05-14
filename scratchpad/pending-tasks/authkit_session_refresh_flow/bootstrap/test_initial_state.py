import os
import shutil
import subprocess

PROJECT_DIR = "/home/user/myproject"
SESSION_PATH = os.path.join(PROJECT_DIR, "session.json")
INDEX_PATH = os.path.join(PROJECT_DIR, "index.js")


def test_node_binary_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."


def test_npm_binary_available():
    assert shutil.which("npm") is not None, "npm binary not found in PATH."


def test_node_major_version_is_24():
    result = subprocess.run(
        ["node", "--version"], capture_output=True, text=True
    )
    assert result.returncode == 0, (
        f"`node --version` failed: stdout={result.stdout!r} stderr={result.stderr!r}"
    )
    version = result.stdout.strip()
    assert version.startswith("v24."), (
        f"Expected Node.js v24.x to be installed, got: {version!r}"
    )


def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), (
        f"Expected project directory {PROJECT_DIR} to exist before the task starts."
    )


def test_index_js_not_yet_created():
    assert not os.path.exists(INDEX_PATH), (
        f"{INDEX_PATH} must not exist before the task starts; the agent is expected to create it."
    )


def test_session_json_not_yet_created():
    assert not os.path.exists(SESSION_PATH), (
        f"{SESSION_PATH} must not exist before the task starts; it is created by running the agent's script."
    )


def test_workos_api_key_is_set():
    api_key = os.environ.get("WORKOS_API_KEY", "")
    assert api_key, (
        "WORKOS_API_KEY environment variable must be set in the task environment."
    )


def test_workos_client_id_is_set():
    client_id = os.environ.get("WORKOS_CLIENT_ID", "")
    assert client_id, (
        "WORKOS_CLIENT_ID environment variable must be set in the task environment."
    )


def test_workos_refresh_token_is_set():
    refresh_token = os.environ.get("WORKOS_REFRESH_TOKEN", "")
    assert refresh_token, (
        "WORKOS_REFRESH_TOKEN environment variable must be set in the task environment."
    )

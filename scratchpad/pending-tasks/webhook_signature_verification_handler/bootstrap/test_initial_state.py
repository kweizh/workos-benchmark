import os
import shutil
import subprocess

PROJECT_DIR = "/home/user/myproject"
SERVER_PATH = os.path.join(PROJECT_DIR, "server.js")
LOG_PATH = os.path.join(PROJECT_DIR, "events.log")


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


def test_server_js_not_yet_created():
    assert not os.path.exists(SERVER_PATH), (
        f"{SERVER_PATH} must not exist before the task starts; the agent is expected to create it."
    )


def test_events_log_not_yet_created():
    assert not os.path.exists(LOG_PATH), (
        f"{LOG_PATH} must not exist before the task starts; it is created by the agent's server when events are verified."
    )


def test_workos_api_key_is_set():
    api_key = os.environ.get("WORKOS_API_KEY", "")
    assert api_key, (
        "WORKOS_API_KEY environment variable must be set in the task environment."
    )


def test_workos_webhook_secret_is_set():
    secret = os.environ.get("WORKOS_WEBHOOK_SECRET", "")
    assert secret, (
        "WORKOS_WEBHOOK_SECRET environment variable must be set in the task environment."
    )

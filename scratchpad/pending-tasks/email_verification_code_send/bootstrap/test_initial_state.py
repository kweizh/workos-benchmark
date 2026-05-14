import json
import os
import shutil
import subprocess

PROJECT_DIR = "/home/user/myproject"
PACKAGE_JSON = os.path.join(PROJECT_DIR, "package.json")
LOG_FILE = os.path.join(PROJECT_DIR, "output.log")
INDEX_JS = os.path.join(PROJECT_DIR, "index.js")


def test_node_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."


def test_npm_available():
    assert shutil.which("npm") is not None, "npm binary not found in PATH."


def test_node_major_version_is_24():
    result = subprocess.run(
        ["node", "--version"], capture_output=True, text=True, check=False
    )
    assert result.returncode == 0, f"`node --version` failed: {result.stderr}"
    version = result.stdout.strip().lstrip("v")
    major = version.split(".", 1)[0]
    assert major == "24", f"Expected Node.js v24, got {result.stdout.strip()}"


def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."


def test_package_json_exists():
    assert os.path.isfile(
        PACKAGE_JSON
    ), f"Initial package.json must already be present at {PACKAGE_JSON}."


def test_package_json_is_valid_json():
    with open(PACKAGE_JSON) as f:
        data = json.load(f)
    assert isinstance(data, dict), f"{PACKAGE_JSON} must contain a JSON object."


def test_workos_sdk_not_yet_installed():
    sdk_pkg = os.path.join(
        PROJECT_DIR, "node_modules", "@workos-inc", "node", "package.json"
    )
    assert not os.path.exists(
        sdk_pkg
    ), "The @workos-inc/node SDK must not be installed in the initial state — the agent is expected to install it."


def test_index_js_absent_initially():
    assert not os.path.exists(
        INDEX_JS
    ), f"{INDEX_JS} must not exist before the task is performed."


def test_output_log_absent_initially():
    assert not os.path.exists(
        LOG_FILE
    ), f"{LOG_FILE} must not exist before the task is performed."


def test_workos_api_key_env_present():
    assert os.environ.get(
        "WORKOS_API_KEY"
    ), "WORKOS_API_KEY environment variable must be set in the task environment."


def test_workos_user_id_env_present():
    assert os.environ.get(
        "WORKOS_USER_ID"
    ), "WORKOS_USER_ID environment variable must be set in the task environment."

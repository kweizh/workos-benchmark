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
        ["node", "--version"], capture_output=True, text=True
    )
    assert result.returncode == 0, f"`node --version` failed: {result.stderr}"
    version = result.stdout.strip()
    assert version.startswith("v24."), (
        f"Expected Node.js major version 24, got '{version}'."
    )


def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), (
        f"Project directory {PROJECT_DIR} does not exist."
    )


def test_project_dir_is_empty_or_has_no_link_file():
    # The agent is expected to CREATE portal_link.txt; it must not pre-exist.
    link_file = os.path.join(PROJECT_DIR, "portal_link.txt")
    assert not os.path.exists(link_file), (
        f"{link_file} must not exist before the task is performed."
    )


def test_workos_api_key_env_present():
    # The task execution environment must inject the real WorkOS API key.
    assert os.environ.get("WORKOS_API_KEY"), (
        "WORKOS_API_KEY environment variable is required but not set."
    )


def test_workos_organization_id_env_present():
    assert os.environ.get("WORKOS_ORGANIZATION_ID"), (
        "WORKOS_ORGANIZATION_ID environment variable is required but not set."
    )

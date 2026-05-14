import os
import shutil
import subprocess
import json

PROJECT_DIR = "/home/user/myproject"


def test_node_binary_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."


def test_npm_binary_available():
    assert shutil.which("npm") is not None, "npm binary not found in PATH."


def test_node_major_version_is_24():
    result = subprocess.run(
        ["node", "--version"], capture_output=True, text=True
    )
    assert result.returncode == 0, (
        f"'node --version' failed: stdout={result.stdout!r} stderr={result.stderr!r}"
    )
    version = result.stdout.strip().lstrip("v")
    major = version.split(".")[0]
    assert major == "24", (
        f"Expected Node.js major version 24, got '{result.stdout.strip()}'."
    )


def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), (
        f"Project directory {PROJECT_DIR} does not exist."
    )


def test_project_package_json_exists():
    pkg_path = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(pkg_path), (
        f"Expected package.json at {pkg_path} but it does not exist."
    )
    with open(pkg_path) as f:
        pkg = json.load(f)
    deps = pkg.get("dependencies", {})
    assert "@workos-inc/node" in deps, (
        f"Expected '@workos-inc/node' in package.json dependencies, got {deps}."
    )


def test_workos_sdk_installed():
    sdk_pkg = os.path.join(
        PROJECT_DIR, "node_modules", "@workos-inc", "node", "package.json"
    )
    assert os.path.isfile(sdk_pkg), (
        f"Expected @workos-inc/node SDK installed at {sdk_pkg} but it is missing."
    )


def test_workos_api_key_env_present():
    api_key = os.environ.get("WORKOS_API_KEY")
    assert api_key, (
        "Expected WORKOS_API_KEY to be set in the task environment."
    )

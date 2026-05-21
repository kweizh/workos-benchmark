import json
import os
import shutil
import subprocess

PROJECT_DIR = "/home/user/myproject"


def test_node_binary_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."


def test_npm_binary_available():
    assert shutil.which("npm") is not None, "npm binary not found in PATH."


def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."


def test_package_json_exists():
    package_json = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(package_json), f"package.json not found at {package_json}."


def test_workos_sdk_installed():
    package_json = os.path.join(PROJECT_DIR, "package.json")
    with open(package_json) as f:
        data = json.load(f)
    deps = data.get("dependencies", {})
    assert "@workos-inc/node" in deps, (
        "Expected @workos-inc/node to be listed in dependencies of package.json."
    )

    workos_pkg = os.path.join(
        PROJECT_DIR, "node_modules", "@workos-inc", "node", "package.json"
    )
    assert os.path.isfile(workos_pkg), (
        f"@workos-inc/node SDK does not appear to be installed at {workos_pkg}."
    )


def test_workos_sdk_loads():
    result = subprocess.run(
        [
            "node",
            "-e",
            "const { WorkOS } = require('@workos-inc/node'); if (!WorkOS) process.exit(1);",
        ],
        capture_output=True,
        text=True,
        cwd=PROJECT_DIR,
    )
    assert result.returncode == 0, (
        f"Failed to require('@workos-inc/node') from project: {result.stderr}"
    )


def test_update_script_not_yet_created():
    p = "/home/user/myproject/update_external_id.js"
    assert not os.path.exists(p), (
        f"{p} should not exist before the task is executed."
    )


def test_org_json_not_yet_created():
    p = "/home/user/myproject/org.json"
    assert not os.path.exists(p), (
        f"{p} should not exist before the task is executed."
    )


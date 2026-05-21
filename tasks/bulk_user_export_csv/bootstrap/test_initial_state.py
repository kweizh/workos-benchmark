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
    pkg_path = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(pkg_path), f"package.json not found at {pkg_path}."


def test_workos_sdk_preinstalled():
    pkg_path = os.path.join(PROJECT_DIR, "node_modules", "@workos-inc", "node", "package.json")
    assert os.path.isfile(pkg_path), (
        "Expected @workos-inc/node SDK to be pre-installed under "
        f"{PROJECT_DIR}/node_modules/@workos-inc/node."
    )
    with open(pkg_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    assert manifest.get("name") == "@workos-inc/node", (
        f"Unexpected package name in pre-installed SDK manifest: {manifest.get('name')!r}."
    )


def test_workos_sdk_loadable():
    result = subprocess.run(
        ["node", "-e", "require('@workos-inc/node');console.log('ok');"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"Failed to require('@workos-inc/node') from {PROJECT_DIR}: {result.stderr.strip()}"
    )
    assert "ok" in result.stdout, (
        f"Expected to load @workos-inc/node successfully, got stdout: {result.stdout!r}"
    )


def test_users_csv_absent_initially():
    out_path = os.path.join(PROJECT_DIR, "users.csv")
    assert not os.path.exists(out_path), (
        f"users.csv should not exist before the task is performed, but found {out_path}."
    )


def test_index_js_absent_initially():
    idx_path = os.path.join(PROJECT_DIR, "index.js")
    assert not os.path.exists(idx_path), (
        f"index.js should not exist before the task is performed, but found {idx_path}."
    )

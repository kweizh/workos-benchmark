import os
import shutil
import pytest

PROJECT_DIR = "/home/user"

def test_node_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_package_json_exists():
    package_json_path = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(package_json_path), f"package.json not found at {package_json_path}"

def test_workos_sdk_installed():
    node_modules_path = os.path.join(PROJECT_DIR, "node_modules", "@workos-inc", "node")
    assert os.path.isdir(node_modules_path), f"WorkOS SDK not found at {node_modules_path}"

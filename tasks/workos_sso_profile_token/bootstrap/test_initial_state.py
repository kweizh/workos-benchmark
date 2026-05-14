import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/app"

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_workos_installed():
    package_json = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(package_json), f"{package_json} not found."
    
    with open(package_json) as f:
        content = f.read()
    assert "@workos-inc/node" in content, "Expected @workos-inc/node to be installed in package.json."

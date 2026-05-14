import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"
USER_ID_FILE = os.path.join(PROJECT_DIR, "user_id.txt")

def test_node_installed():
    assert shutil.which("node") is not None, "Node.js is not installed."
    assert shutil.which("npm") is not None, "npm is not installed."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_user_id_file_exists():
    assert os.path.isfile(USER_ID_FILE), f"User ID file {USER_ID_FILE} does not exist."
    with open(USER_ID_FILE, "r") as f:
        content = f.read().strip()
    assert content != "", "User ID file is empty."

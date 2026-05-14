import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/app"

def test_node_installed():
    assert shutil.which("node") is not None, "Node.js is not installed."

def test_npm_installed():
    assert shutil.which("npm") is not None, "npm is not installed."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

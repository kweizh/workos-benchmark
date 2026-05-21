import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/app"

def test_node_installed():
    assert shutil.which("node") is not None, "Node.js binary not found in PATH."
    assert shutil.which("npm") is not None, "npm binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_postgres_available():
    assert shutil.which("psql") is not None, "psql binary not found in PATH."

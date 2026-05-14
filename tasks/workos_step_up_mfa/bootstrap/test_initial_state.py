import os
import shutil
import pytest

PROJECT_DIR = "/home/user/app"

def test_node_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."

def test_npm_available():
    assert shutil.which("npm") is not None, "npm binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_server_file_exists():
    server_path = os.path.join(PROJECT_DIR, "server.js")
    assert os.path.isfile(server_path), f"Server file {server_path} does not exist."

import os
import shutil
import pytest

PROJECT_DIR = "/home/user/workos_sso_org_mapping"

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_workos_keys_present():
    assert "WORKOS_API_KEY" in os.environ, "WORKOS_API_KEY environment variable is not set."
    assert "WORKOS_CLIENT_ID" in os.environ, "WORKOS_CLIENT_ID environment variable is not set."

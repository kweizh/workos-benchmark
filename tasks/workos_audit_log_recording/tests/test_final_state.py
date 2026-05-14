import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/workos-task"
SCRIPT_PATH = os.path.join(PROJECT_DIR, "record_audit_log.js")

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"

def test_script_execution():
    # Execute the script
    result = subprocess.run(
        ["node", "record_audit_log.js"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Script execution failed: {result.stderr}"

def test_amika_validation():
    # Use amika CLI to validate
    result = subprocess.run(
        ["amika", "validate", "workos_audit_log_recording"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"amika validation failed: {result.stderr}"

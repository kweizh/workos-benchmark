import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/project"
SCRIPT_PATH = os.path.join(PROJECT_DIR, "generate_portal_link.js")

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"

def test_amika_validation():
    """Priority 1: Use amika CLI to verify the final state."""
    result = subprocess.run(
        ["amika", "validate", SCRIPT_PATH],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"amika validation failed: {result.stderr}\nStdout: {result.stdout}"

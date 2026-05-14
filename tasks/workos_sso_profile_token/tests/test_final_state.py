import os
import subprocess
import pytest

APP_FILE = "/home/user/app/index.js"

def test_app_file_exists():
    """Priority 3 fallback: basic file existence check."""
    assert os.path.isfile(APP_FILE), \
        f"index.js not found at {APP_FILE}"

def test_amika_validation():
    """Priority 1: Use amika CLI to verify the final state."""
    result = subprocess.run(
        ["amika", "validate", APP_FILE],
        capture_output=True, text=True, cwd="/home/user/app"
    )
    assert result.returncode == 0, \
        f"'amika validate' failed: {result.stderr}\nStdout: {result.stdout}"

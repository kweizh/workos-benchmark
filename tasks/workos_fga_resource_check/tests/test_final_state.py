import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/project/check.js"

def test_script_exists():
    """Priority 3 fallback: basic file existence check."""
    assert os.path.isfile(SCRIPT_PATH), f"check.js not found at {SCRIPT_PATH}"

def test_amika_validation():
    """Priority 1: Use amika CLI to verify the implementation."""
    result = subprocess.run(
        ["amika", "validate", SCRIPT_PATH],
        capture_output=True,
        text=True,
        cwd="/home/user/project"
    )
    assert result.returncode == 0, f"amika validation failed: {result.stderr}\n{result.stdout}"

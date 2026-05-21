import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/app"

def test_amika_validation():
    """Priority 1: Use amika CLI to verify the final state."""
    result = subprocess.run(
        ["amika", "validate", "generate_portal_link.js"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert result.returncode == 0, f"amika validation failed: {result.stderr}"

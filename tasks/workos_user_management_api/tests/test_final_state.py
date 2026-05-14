import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/project"
OUTPUT_FILE = os.path.join(PROJECT_DIR, "output.txt")

def test_output_file_exists_and_contains_user_id():
    """Priority 3 fallback: check if output.txt exists and contains a user ID."""
    assert os.path.isfile(OUTPUT_FILE), f"Output file not found at {OUTPUT_FILE}"
    
    with open(OUTPUT_FILE, "r") as f:
        content = f.read().strip()
        
    assert content.startswith("user_"), f"Expected output.txt to contain a WorkOS User ID starting with 'user_', got: {content}"

def test_amika_validation():
    """Priority 1: Use amika CLI to verify the final state."""
    result = subprocess.run(
        ["amika", "validate", "workos_user_management_api"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"'amika validate' failed: {result.stderr}"

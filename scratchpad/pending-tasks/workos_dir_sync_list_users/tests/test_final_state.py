import os
import subprocess
import json
import pytest

PROJECT_DIR = "/home/user/project"
OUTPUT_FILE = "/home/user/project/users.json"

def test_output_file_exists():
    assert os.path.isfile(OUTPUT_FILE), f"Output file not found at {OUTPUT_FILE}"

def test_amika_validation():
    """Use amika CLI to validate the output."""
    result = subprocess.run(
        ["amika", "validate", OUTPUT_FILE],
        capture_output=True,
        text=True,
        cwd=PROJECT_DIR
    )
    assert result.returncode == 0, f"'amika validate' failed: {result.stderr}"

def test_output_file_content():
    """Verify the file contains a JSON array of users."""
    with open(OUTPUT_FILE) as f:
        try:
            users = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Output file does not contain valid JSON.")
    
    assert isinstance(users, list), "Expected output to be a JSON array (list of users)."
    # Basic check to see if it looks like WorkOS user objects (they typically have 'id' and 'object' == 'directory_user')
    if len(users) > 0:
        assert "id" in users[0], "Expected user objects to have an 'id' field."

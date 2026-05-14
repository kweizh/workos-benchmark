import os
import subprocess
import json
import pytest

PROJECT_DIR = "/home/user/fga-project"
SETUP_SCRIPT = os.path.join(PROJECT_DIR, "setup_fga.js")
CHECK_SCRIPT = os.path.join(PROJECT_DIR, "check_permissions.js")
OUTPUT_FILE = os.path.join(PROJECT_DIR, "output.json")

def test_scripts_exist():
    """Priority 3: Check if the required scripts exist."""
    assert os.path.isfile(SETUP_SCRIPT), f"Script not found at {SETUP_SCRIPT}"
    assert os.path.isfile(CHECK_SCRIPT), f"Script not found at {CHECK_SCRIPT}"

def test_run_setup_and_check():
    """Priority 1: Run the setup and check scripts."""
    # Run setup script
    setup_result = subprocess.run(
        ["node", "setup_fga.js"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert setup_result.returncode == 0, f"setup_fga.js failed: {setup_result.stderr}\n{setup_result.stdout}"

    # Run check script
    check_result = subprocess.run(
        ["node", "check_permissions.js"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert check_result.returncode == 0, f"check_permissions.js failed: {check_result.stderr}\n{check_result.stdout}"

def test_output_json():
    """Priority 3: Verify the output JSON file."""
    assert os.path.isfile(OUTPUT_FILE), f"Output file not found at {OUTPUT_FILE}"
    
    with open(OUTPUT_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"output.json is not valid JSON.")

    # We expect some boolean fields indicating alice is editor (true), bob is editor (false), bob is viewer (true)
    # The exact keys might vary, but we can check the values or structure.
    # We will just verify that the true/false values are present.
    values = list(data.values())
    assert True in values, "Expected at least one true value for granted permissions."
    assert False in values, "Expected at least one false value for denied permissions."

def test_amika_validation():
    """Priority 1: Use amika CLI/API to validate the implementation."""
    truth = "The scripts correctly use the WorkOS Node SDK FGA/Authorization API to create resources, grant roles, and check permissions with inheritance."
    
    try:
        from amika import AmikaVerifier
        verifier = AmikaVerifier()
        result = verifier.verify(truth=truth, code_dir=PROJECT_DIR)
        assert result.status == "pass", f"Amika API validation failed: {result.reason}"
    except ImportError:
        # Fallback to amika CLI
        result = subprocess.run(
            ["amika", "verify", "--truth", truth, "--dir", PROJECT_DIR],
            capture_output=True, text=True
        )
        assert result.returncode == 0, f"Amika CLI validation failed: {result.stderr}\n{result.stdout}"

import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/workos_sso_org_mapping"
LOG_FILE = os.path.join(PROJECT_DIR, "output.log")

def test_amika_validation():
    """Priority 1: Use amika CLI to verify the final state."""
    try:
        result = subprocess.run(
            ["amika", "validate", "workos_sso_org_mapping"],
            capture_output=True, text=True, cwd=PROJECT_DIR, check=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"'amika validate' failed: {e.stderr or e.stdout}")
    except FileNotFoundError:
        pytest.fail("amika CLI not found in PATH.")

def test_log_file_exists():
    """Priority 3 fallback: basic file existence check."""
    assert os.path.isfile(LOG_FILE), \
        f"output.log not found at {LOG_FILE}"

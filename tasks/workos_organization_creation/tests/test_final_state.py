import os
import subprocess
import pytest

ORG_ID_FILE = "/home/user/org_id.txt"

def test_org_id_file_exists():
    """Priority 3 fallback: basic file existence check."""
    assert os.path.isfile(ORG_ID_FILE), f"Organization ID file not found at {ORG_ID_FILE}"

def test_org_id_valid_via_amika():
    """Priority 1: Use amika CLI to verify the organization creation."""
    assert os.path.isfile(ORG_ID_FILE), f"Organization ID file not found at {ORG_ID_FILE}"
    
    with open(ORG_ID_FILE, "r") as f:
        org_id = f.read().strip()
        
    assert org_id, "Organization ID file is empty."
    
    # Run amika validate with the organization ID
    result = subprocess.run(
        ["amika", "validate", org_id],
        capture_output=True, text=True
    )
    
    assert result.returncode == 0, f"'amika validate' failed for organization {org_id}: {result.stderr}\n{result.stdout}"

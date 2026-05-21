import os
import json
import subprocess
import pytest

PROJECT_DIR = "/home/user/app"

def test_results_json_exists():
    results_path = os.path.join(PROJECT_DIR, "results.json")
    assert os.path.isfile(results_path), f"results.json not found at {results_path}"

def test_fga_role_inheritance_results():
    results_path = os.path.join(PROJECT_DIR, "results.json")
    with open(results_path) as f:
        data = json.load(f)
    
    assert "alice_can_read" in data, "Expected 'alice_can_read' in results.json"
    assert "bob_can_delete" in data, "Expected 'bob_can_delete' in results.json"
    
    assert data["alice_can_read"] is True, "Expected alice_can_read to be True because of role inheritance from parent_folder"
    assert data["bob_can_delete"] is False, "Expected bob_can_delete to be False because bob is only an editor"

def test_amika_validation():
    try:
        subprocess.run(['amika', 'validate', 'workos_fga_role_inheritance'], check=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"amika validation failed: {e}")
    except FileNotFoundError:
        pytest.fail("amika CLI not found, but it is required for validation.")
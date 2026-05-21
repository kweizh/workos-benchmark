import os
import subprocess
import pytest

def test_amika_validation():
    # 1. Run the user's script
    result = subprocess.run(
        ["npm", "start"],
        cwd="/home/user/app",
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"npm start failed: {result.stderr}"

    # 2. Check if the output file exists
    output_file = "/home/user/app/audit_logs.json"
    assert os.path.isfile(output_file), f"Output file {output_file} was not created."

    # 3. Use amika to validate the output
    amika_result = subprocess.run(
        ["amika", "validate", output_file],
        capture_output=True,
        text=True
    )
    assert amika_result.returncode == 0, f"amika validation failed: {amika_result.stderr}"

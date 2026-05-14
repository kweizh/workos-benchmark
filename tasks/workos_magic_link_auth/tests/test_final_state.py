import os
import subprocess
import json
import time
import socket
import pytest

PROJECT_DIR = "/home/user/app"

def wait_for_port(port, timeout=30):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(1)
    return False

@pytest.fixture(scope="module")
def start_app():
    # Install dependencies first
    subprocess.run(["npm", "install"], cwd=PROJECT_DIR, check=True)
    
    # Start the app
    process = subprocess.Popen(
        ["node", "index.js"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )
    
    # Wait for the app to be ready
    if not wait_for_port(3000):
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("App failed to start and listen on port 3000.")
    
    yield
    
    # Shut down the app
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=10)

def test_magic_link_flow(start_app):
    """Priority 1: Test the API endpoints directly."""
    import urllib.request
    import urllib.error
    
    # 1. Create Magic Link
    req = urllib.request.Request(
        "http://localhost:3000/api/magic-link",
        data=json.dumps({"email": "test_user@example.com"}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            assert response.status in [200, 201], f"Expected 200 or 201, got {response.status}"
            data = json.loads(response.read().decode("utf-8"))
            assert "code" in data, "Response did not contain a magic link code."
            code = data["code"]
    except urllib.error.HTTPError as e:
        pytest.fail(f"/api/magic-link failed with status {e.code}: {e.read().decode('utf-8')}")

    # 2. Verify Magic Link
    verify_req = urllib.request.Request(
        "http://localhost:3000/api/verify",
        data=json.dumps({"email": "test_user@example.com", "code": code}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(verify_req) as response:
            assert response.status == 200, f"Expected 200, got {response.status}"
            user_data = json.loads(response.read().decode("utf-8"))
            # The returned user object should have an email field matching test_user@example.com
            # Sometimes it's nested under "user" if they return { user, accessToken }
            email = user_data.get("email") or (user_data.get("user", {}).get("email"))
            assert email == "test_user@example.com", f"Expected authenticated email test_user@example.com, got: {email}"
    except urllib.error.HTTPError as e:
        pytest.fail(f"/api/verify failed with status {e.code}: {e.read().decode('utf-8')}")

def test_amika_validation():
    """Priority 1: Use amika CLI to validate the source code."""
    truth = "The Express app correctly implements WorkOS Magic Link authentication with /api/magic-link and /api/verify endpoints using the WorkOS Node SDK methods createMagicAuth and authenticateWithMagicAuth."
    
    result = subprocess.run(
        ["amika", "verify", "--truth", truth, "--dir", PROJECT_DIR],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Amika CLI validation failed: {result.stderr}\n{result.stdout}"

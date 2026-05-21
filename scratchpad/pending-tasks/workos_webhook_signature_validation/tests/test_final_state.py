import os
import subprocess
import time
import socket
import pytest

PROJECT_DIR = "/home/user/app"

def wait_for_port(port, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(1)
    return False

@pytest.fixture(scope="module")
def start_app():
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
        # Kill the process group before failing
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("App failed to start and listen on port 3000.")
    
    yield
    
    # Shut down the app
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=10)

def test_webhook_signature_validation(start_app):
    """Priority 1: Use amika CLI to verify the webhook endpoint."""
    target_url = "http://localhost:3000/webhooks"
    secret = os.environ.get("WORKOS_WEBHOOK_SECRET", "whsec_test_secret")
    
    result = subprocess.run(
        ["amika", "validate", f"target_url={target_url}", f"secret={secret}"],
        capture_output=True, text=True
    )
    
    assert result.returncode == 0, \
        f"'amika validate' failed with exit code {result.returncode}:\\nSTDOUT: {result.stdout}\\nSTDERR: {result.stderr}"

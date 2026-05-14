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
        time.sleep(5)
    return False

@pytest.fixture(scope="module")
def start_app():
    # Start the app
    env = os.environ.copy()
    if "WORKOS_API_KEY" not in env:
        pytest.fail("WORKOS_API_KEY is not set in the environment.")
    if "WORKOS_CLIENT_ID" not in env:
        pytest.fail("WORKOS_CLIENT_ID is not set in the environment.")

    process = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid,
        env=env
    )
    
    # Wait for the app to be ready
    if not wait_for_port(3000):
        # Kill the process group before failing
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("App failed to start and listen on required ports.")
    
    yield
    
    # Shut down the app
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def test_sign_out_using_amika(start_app):
    """Use amika CLI to validate the sign-out functionality."""
    result = subprocess.run(
        ["amika", "validate", "http://localhost:3000"],
        capture_output=True,
        text=True,
        cwd=PROJECT_DIR
    )
    assert result.returncode == 0, f"amika validation failed: {result.stderr}\n{result.stdout}"

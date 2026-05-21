import os
import subprocess
import pytest
import time
import socket

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
    # Start postgresql
    subprocess.run(["service", "postgresql", "start"], check=True)
    
    # Initialize DB
    env = os.environ.copy()
    env["DATABASE_URL"] = "postgres://testuser:testpass@localhost:5432/testdb"
    if "WORKOS_WEBHOOK_SECRET" not in env:
        env["WORKOS_WEBHOOK_SECRET"] = "whsec_test123"
    if "WORKOS_API_KEY" not in env:
        env["WORKOS_API_KEY"] = "sk_test123"
        
    subprocess.run(["node", "init_db.js"], cwd=PROJECT_DIR, env=env, check=True)

    # Start the app
    process = subprocess.Popen(
        ["npm", "start"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid,
        env=env
    )
    
    if not wait_for_port(3000):
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("App failed to start and listen on port 3000.")
    
    yield env
    
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def test_webhook_validation_with_amika(start_app):
    """Priority 1: Use amika CLI to validate the webhook endpoint."""
    target_url = "http://localhost:3000/webhooks/workos"
    try:
        # The prompt explicitly required using amika CLI for validation
        result = subprocess.run(
            ["amika", "validate", target_url],
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"amika validate failed: {e.stderr}\n{e.stdout}")

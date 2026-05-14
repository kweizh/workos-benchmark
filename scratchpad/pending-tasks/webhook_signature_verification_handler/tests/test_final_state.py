import hashlib
import hmac
import json
import os
import signal
import socket
import subprocess
import time
import urllib.error
import urllib.request

import pytest

PROJECT_DIR = "/home/user/myproject"
SERVER_PATH = os.path.join(PROJECT_DIR, "server.js")
LOG_PATH = os.path.join(PROJECT_DIR, "events.log")
PORT = 4000
WEBHOOK_URL = f"http://localhost:{PORT}/webhooks/workos"


def _require_env(name):
    value = os.environ.get(name, "")
    assert value, f"{name} must be set in the verifier environment."
    return value


def _wait_for_port(port, timeout=60):
    start = time.time()
    while time.time() - start < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            if sock.connect_ex(("127.0.0.1", port)) == 0:
                return True
        time.sleep(1)
    return False


def _canonical_body(event_id, event_type="dsync.user.created"):
    obj = {
        "id": event_id,
        "event": event_type,
        "data": {
            "object": "directory_user",
            "id": "directory_user_test_01",
        },
        "created_at": "2024-01-01T00:00:00.000Z",
    }
    # Canonical JSON (no whitespace) — matches JSON.stringify output for the
    # equivalent JS object so that Express + the SDK can recompute the same
    # signed payload after JSON.parse/JSON.stringify roundtrip.
    return json.dumps(obj, separators=(",", ":")).encode("utf-8")


def _sign(body_bytes, secret, timestamp_ms=None):
    if timestamp_ms is None:
        timestamp_ms = int(time.time() * 1000)
    signed_payload = f"{timestamp_ms}.".encode("utf-8") + body_bytes
    digest = hmac.new(
        secret.encode("utf-8"),
        signed_payload,
        hashlib.sha256,
    ).hexdigest()
    header = f"t={timestamp_ms}, v1={digest}"
    return header, timestamp_ms, digest


def _post(body_bytes, signature_header):
    req = urllib.request.Request(
        WEBHOOK_URL,
        data=body_bytes,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "WorkOS-Signature": signature_header,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="replace")


def _read_log_lines():
    if not os.path.isfile(LOG_PATH):
        return []
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        return [ln for ln in f.read().splitlines() if ln.strip()]


@pytest.fixture(scope="module")
def server_process():
    # Make sure the verifier sees a clean log from this run only.
    if os.path.exists(LOG_PATH):
        os.remove(LOG_PATH)

    assert os.path.isfile(SERVER_PATH), (
        f"Expected the agent's Express server at {SERVER_PATH} but it is missing."
    )

    env = os.environ.copy()
    # Required at runtime by the agent's server.
    _require_env("WORKOS_API_KEY")
    _require_env("WORKOS_WEBHOOK_SECRET")

    proc = subprocess.Popen(
        ["node", "server.js"],
        cwd=PROJECT_DIR,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid,
    )

    if not _wait_for_port(PORT, timeout=60):
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        except Exception:
            pass
        stdout, stderr = proc.communicate(timeout=10)
        pytest.fail(
            "Webhook server did not start listening on port "
            f"{PORT}. stdout={stdout!r} stderr={stderr!r}"
        )

    yield proc

    try:
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
    except Exception:
        pass
    try:
        proc.wait(timeout=15)
    except Exception:
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        except Exception:
            pass


def test_server_js_exists():
    assert os.path.isfile(SERVER_PATH), (
        f"Expected the agent's Express server at {SERVER_PATH}, but it was not found."
    )


def test_valid_signature_returns_200_and_logs_event(server_process):
    secret = _require_env("WORKOS_WEBHOOK_SECRET")
    event_id = f"event_pos1_{int(time.time()*1000)}"
    body = _canonical_body(event_id)
    header, _, _ = _sign(body, secret)

    status, resp_body = _post(body, header)
    assert status == 200, (
        f"Expected HTTP 200 for a correctly signed webhook, got {status}. Body: {resp_body!r}"
    )

    # Give the server a moment to flush the append.
    time.sleep(0.5)
    lines = _read_log_lines()
    expected_line = f"{event_id} dsync.user.created"
    assert expected_line in lines, (
        f"Expected log line {expected_line!r} in {LOG_PATH} after a verified event. "
        f"Got: {lines!r}"
    )


def test_tampered_signature_returns_400_and_does_not_log(server_process):
    secret = _require_env("WORKOS_WEBHOOK_SECRET")
    event_id = f"event_neg_tamper_{int(time.time()*1000)}"
    body = _canonical_body(event_id)
    header, ts, digest = _sign(body, secret)

    # Flip the first hex character of the signature to make it invalid.
    flipped = ("0" if digest[0] != "0" else "1") + digest[1:]
    tampered_header = f"t={ts}, v1={flipped}"

    status, resp_body = _post(body, tampered_header)
    assert status == 400, (
        f"Expected HTTP 400 for a tampered signature, got {status}. Body: {resp_body!r}"
    )

    time.sleep(0.3)
    lines = _read_log_lines()
    assert all(event_id not in ln for ln in lines), (
        f"Tampered-signature event id {event_id!r} must NOT appear in {LOG_PATH}. "
        f"Got: {lines!r}"
    )


def test_wrong_secret_signature_returns_400_and_does_not_log(server_process):
    secret = _require_env("WORKOS_WEBHOOK_SECRET")
    event_id = f"event_neg_wrong_{int(time.time()*1000)}"
    body = _canonical_body(event_id)
    header, _, _ = _sign(body, secret + "_wrong")

    status, resp_body = _post(body, header)
    assert status == 400, (
        f"Expected HTTP 400 when the signature is computed with a different secret, "
        f"got {status}. Body: {resp_body!r}"
    )

    time.sleep(0.3)
    lines = _read_log_lines()
    assert all(event_id not in ln for ln in lines), (
        f"Wrong-secret event id {event_id!r} must NOT appear in {LOG_PATH}. Got: {lines!r}"
    )


def test_second_valid_event_is_appended(server_process):
    secret = _require_env("WORKOS_WEBHOOK_SECRET")
    event_id = f"event_pos2_{int(time.time()*1000)}"
    body = _canonical_body(event_id)
    header, _, _ = _sign(body, secret)

    status, resp_body = _post(body, header)
    assert status == 200, (
        f"Expected HTTP 200 for a second correctly signed webhook, got {status}. Body: {resp_body!r}"
    )

    time.sleep(0.5)
    lines = _read_log_lines()
    assert f"{event_id} dsync.user.created" in lines, (
        f"Expected the second verified event {event_id!r} to be appended to {LOG_PATH}. "
        f"Got: {lines!r}"
    )

    # The log must still contain a positive line from the first positive test —
    # proving the handler appends rather than overwrites.
    pos1_lines = [ln for ln in lines if ln.startswith("event_pos1_")]
    assert pos1_lines, (
        f"Expected the first verified 'event_pos1_*' line to still be present in "
        f"{LOG_PATH} after the second valid event (log must be append-only). "
        f"Got: {lines!r}"
    )

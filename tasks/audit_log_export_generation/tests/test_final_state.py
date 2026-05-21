import json
import os
import subprocess

import pytest

PROJECT_DIR = "/home/user/myproject"
INDEX_JS = os.path.join(PROJECT_DIR, "index.js")
EXPORT_JSON = os.path.join(PROJECT_DIR, "export.json")
AUDIT_CSV = os.path.join(PROJECT_DIR, "audit.csv")


def test_index_js_exists():
    assert os.path.isfile(INDEX_JS), f"{INDEX_JS} was not created by the agent."


def test_index_js_uses_create_and_get_export():
    with open(INDEX_JS) as f:
        content = f.read()
    assert "createExport" in content, (
        f"{INDEX_JS} must call workos.auditLogs.createExport(...); not found in the file."
    )
    assert "getExport" in content, (
        f"{INDEX_JS} must call workos.auditLogs.getExport(...); not found in the file."
    )


def test_export_json_exists_and_has_expected_fields():
    assert os.path.isfile(EXPORT_JSON), f"{EXPORT_JSON} was not created by the agent."
    with open(EXPORT_JSON) as f:
        data = json.load(f)
    assert isinstance(data, dict), (
        f"{EXPORT_JSON} must contain a JSON object, got: {type(data).__name__}"
    )

    export_id = data.get("exportId")
    assert isinstance(export_id, str) and export_id, (
        f"{EXPORT_JSON} must contain a non-empty string `exportId`. Got: {data!r}"
    )

    state = data.get("state")
    assert state == "ready", (
        f"{EXPORT_JSON} must contain `state` == \"ready\" after polling. Got: {state!r}"
    )

    url = data.get("url")
    assert isinstance(url, str) and url, (
        f"{EXPORT_JSON} must contain a non-empty string `url`. Got: {data!r}"
    )

    range_start = data.get("rangeStart")
    range_end = data.get("rangeEnd")
    assert isinstance(range_start, str) and range_start, (
        f"{EXPORT_JSON} must contain a non-empty string `rangeStart`. Got: {data!r}"
    )
    assert isinstance(range_end, str) and range_end, (
        f"{EXPORT_JSON} must contain a non-empty string `rangeEnd`. Got: {data!r}"
    )


def test_audit_csv_exists():
    assert os.path.isfile(AUDIT_CSV), (
        f"{AUDIT_CSV} was not created by the agent. The script must download the export URL "
        "contents and write them to this path."
    )


def test_workos_api_reports_export_state_ready():
    api_key = os.environ.get("WORKOS_API_KEY")
    assert api_key, "WORKOS_API_KEY env var must be set in the verifier environment."

    with open(EXPORT_JSON) as f:
        data = json.load(f)
    export_id = data.get("exportId")
    assert isinstance(export_id, str) and export_id, (
        f"{EXPORT_JSON} must contain a non-empty string `exportId` to verify against the API."
    )

    result = subprocess.run(
        [
            "curl",
            "-sS",
            "-o",
            "/tmp/audit_log_export_response.json",
            "-w",
            "%{http_code}",
            "-H",
            f"Authorization: Bearer {api_key}",
            f"https://api.workos.com/audit_logs/exports/{export_id}",
        ],
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, (
        f"curl to WorkOS Audit Logs API failed: stdout={result.stdout!r} stderr={result.stderr!r}"
    )
    status_code = result.stdout.strip()
    assert status_code == "200", (
        f"Expected HTTP 200 from WorkOS Audit Logs API for export {export_id}, "
        f"got status {status_code}."
    )

    with open("/tmp/audit_log_export_response.json") as f:
        body = json.load(f)
    api_state = body.get("state")
    assert api_state == "ready", (
        f"WorkOS Audit Logs API reports state={api_state!r} for export {export_id}; "
        f"expected \"ready\". Full response: {body!r}"
    )

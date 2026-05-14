import json
import os
import subprocess

import pytest

PROJECT_DIR = "/home/user/myproject"
INDEX_JS = os.path.join(PROJECT_DIR, "index.js")
USERS_JSON = os.path.join(PROJECT_DIR, "users.json")


def _read_users_json():
    assert os.path.isfile(USERS_JSON), f"Expected output file {USERS_JSON} does not exist."
    with open(USERS_JSON, "r", encoding="utf-8") as f:
        raw = f.read()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        pytest.fail(f"{USERS_JSON} is not valid JSON: {exc}")
    assert isinstance(data, list), (
        f"{USERS_JSON} must contain a JSON array, got type {type(data).__name__}."
    )
    for entry in data:
        assert isinstance(entry, str), (
            f"Every element of {USERS_JSON} must be a string, got {entry!r}."
        )
    return data


def _fetch_emails_from_live_api():
    api_key = os.environ.get("WORKOS_API_KEY")
    directory_id = os.environ.get("WORKOS_DIRECTORY_ID")
    assert api_key, "WORKOS_API_KEY environment variable is not set in the verifier."
    assert directory_id, "WORKOS_DIRECTORY_ID environment variable is not set in the verifier."

    script = (
        "const { WorkOS } = require('@workos-inc/node');"
        "(async () => {"
        "  const workos = new WorkOS(process.env.WORKOS_API_KEY);"
        "  const all = [];"
        "  let after = undefined;"
        "  for (;;) {"
        "    const page = await workos.directorySync.listUsers({"
        "      directory: process.env.WORKOS_DIRECTORY_ID,"
        "      limit: 100,"
        "      after,"
        "    });"
        "    for (const u of page.data) {"
        "      const primary = (u.emails || []).find(e => e && e.primary);"
        "      const email = primary ? primary.value : (u.emails && u.emails[0] && u.emails[0].value);"
        "      if (email) all.push(email);"
        "    }"
        "    const next = page.listMetadata && page.listMetadata.after;"
        "    if (!next) break;"
        "    after = next;"
        "  }"
        "  process.stdout.write(JSON.stringify(all));"
        "})().catch(err => { console.error(err); process.exit(1); });"
    )

    result = subprocess.run(
        ["node", "-e", script],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        timeout=120,
        env={**os.environ},
    )
    assert result.returncode == 0, (
        f"Verifier failed to call the live WorkOS API: stderr={result.stderr.strip()}"
    )
    try:
        emails = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        pytest.fail(
            f"Verifier could not parse JSON from live WorkOS API call: {exc}; "
            f"stdout={result.stdout!r}"
        )
    assert isinstance(emails, list), "Live WorkOS API returned a non-list payload."
    return emails


def test_index_js_exists_and_uses_workos_sdk():
    assert os.path.isfile(INDEX_JS), f"Expected agent script at {INDEX_JS}."
    with open(INDEX_JS, "r", encoding="utf-8") as f:
        content = f.read()
    assert "@workos-inc/node" in content, (
        "index.js must import the @workos-inc/node SDK to call the live WorkOS API."
    )
    assert "directorySync" in content and "listUsers" in content, (
        "index.js must invoke workos.directorySync.listUsers."
    )


def test_users_json_is_valid_string_array():
    _read_users_json()


def test_users_json_matches_live_workos_api():
    actual = _read_users_json()
    expected = _fetch_emails_from_live_api()

    actual_set = {e.lower() for e in actual}
    expected_set = {e.lower() for e in expected}

    missing = expected_set - actual_set
    extra = actual_set - expected_set
    assert not missing and not extra, (
        f"users.json does not match the live WorkOS Directory Sync listing. "
        f"Missing emails: {sorted(missing)}; Unexpected emails: {sorted(extra)}."
    )


def test_users_json_is_alphabetically_sorted():
    actual = _read_users_json()
    sorted_copy = sorted(actual, key=lambda s: s.lower())
    assert actual == sorted_copy, (
        f"Emails in users.json must be sorted alphabetically (case-insensitive). "
        f"Got: {actual}; expected order: {sorted_copy}."
    )

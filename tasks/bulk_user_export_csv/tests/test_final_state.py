import csv
import io
import json
import os
import subprocess

import pytest

PROJECT_DIR = "/home/user/myproject"
INDEX_JS = os.path.join(PROJECT_DIR, "index.js")
USERS_CSV = os.path.join(PROJECT_DIR, "users.csv")

EXPECTED_HEADER = ["id", "email", "first_name", "last_name", "created_at"]


def _read_csv_text():
    assert os.path.isfile(USERS_CSV), f"Expected output file {USERS_CSV} does not exist."
    with open(USERS_CSV, "r", encoding="utf-8") as f:
        text = f.read()
    assert text, f"{USERS_CSV} is empty."
    return text


def _parse_csv_rows():
    text = _read_csv_text()
    reader = csv.reader(io.StringIO(text))
    rows = list(reader)
    assert len(rows) >= 1, f"{USERS_CSV} must contain at least a header row."
    return rows


def _norm(value):
    return "" if value is None else str(value)


def _fetch_users_from_live_api():
    api_key = os.environ.get("WORKOS_API_KEY")
    organization_id = os.environ.get("WORKOS_ORGANIZATION_ID")
    assert api_key, "WORKOS_API_KEY environment variable is not set in the verifier."
    assert organization_id, "WORKOS_ORGANIZATION_ID environment variable is not set in the verifier."

    script = (
        "const { WorkOS } = require('@workos-inc/node');"
        "(async () => {"
        "  const workos = new WorkOS(process.env.WORKOS_API_KEY);"
        "  const all = [];"
        "  let after = undefined;"
        "  for (;;) {"
        "    const page = await workos.userManagement.listUsers({"
        "      organizationId: process.env.WORKOS_ORGANIZATION_ID,"
        "      limit: 100,"
        "      after,"
        "    });"
        "    for (const u of page.data) {"
        "      all.push({"
        "        id: u.id,"
        "        email: u.email == null ? '' : String(u.email),"
        "        first_name: u.firstName == null ? '' : String(u.firstName),"
        "        last_name: u.lastName == null ? '' : String(u.lastName),"
        "        created_at: u.createdAt == null ? '' : String(u.createdAt),"
        "      });"
        "    }"
        "    const next = page.listMetadata && page.listMetadata.after;"
        "    if (!next) break;"
        "    after = next;"
        "  }"
        "  process.stdout.write(JSON.stringify(all));"
        "})().catch(err => { console.error(err && err.stack ? err.stack : err); process.exit(1); });"
    )

    result = subprocess.run(
        ["node", "-e", script],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        timeout=180,
        env={**os.environ},
    )
    assert result.returncode == 0, (
        f"Verifier failed to call the live WorkOS API: stderr={result.stderr.strip()}"
    )
    try:
        users = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        pytest.fail(
            f"Verifier could not parse JSON from live WorkOS API call: {exc}; "
            f"stdout={result.stdout!r}"
        )
    assert isinstance(users, list), "Live WorkOS API returned a non-list payload."
    return users


def test_index_js_exists_and_uses_workos_sdk():
    assert os.path.isfile(INDEX_JS), f"Expected agent script at {INDEX_JS}."
    with open(INDEX_JS, "r", encoding="utf-8") as f:
        content = f.read()
    assert "@workos-inc/node" in content, (
        "index.js must import the @workos-inc/node SDK to call the live WorkOS API."
    )
    assert "userManagement" in content and "listUsers" in content, (
        "index.js must invoke workos.userManagement.listUsers."
    )
    assert "after" in content, (
        "index.js must use the `after` cursor to paginate through results."
    )


def test_users_csv_has_trailing_newline_and_utf8():
    with open(USERS_CSV, "rb") as f:
        raw = f.read()
    assert raw, f"{USERS_CSV} is empty."
    # UTF-8 decodable, no BOM
    assert not raw.startswith(b"\xef\xbb\xbf"), f"{USERS_CSV} must not start with a UTF-8 BOM."
    try:
        raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        pytest.fail(f"{USERS_CSV} is not valid UTF-8: {exc}")
    assert raw.endswith(b"\n"), f"{USERS_CSV} must end with a trailing newline (\\n)."


def test_users_csv_header_is_exact():
    rows = _parse_csv_rows()
    assert rows[0] == EXPECTED_HEADER, (
        f"CSV header must be exactly {EXPECTED_HEADER}, got {rows[0]}."
    )


def test_users_csv_rows_have_five_columns():
    rows = _parse_csv_rows()
    for i, row in enumerate(rows[1:], start=2):
        assert len(row) == 5, (
            f"Row {i} of {USERS_CSV} must have 5 columns, got {len(row)}: {row!r}."
        )


def test_users_csv_matches_live_workos_api():
    rows = _parse_csv_rows()
    csv_records = [
        {
            "id": r[0],
            "email": r[1],
            "first_name": r[2],
            "last_name": r[3],
            "created_at": r[4],
        }
        for r in rows[1:]
    ]
    expected = _fetch_users_from_live_api()

    assert len(csv_records) == len(expected), (
        f"users.csv row count ({len(csv_records)}) does not match the number of users "
        f"returned by the live WorkOS API ({len(expected)})."
    )

    csv_ids = sorted(rec["id"] for rec in csv_records)
    expected_ids = sorted(u["id"] for u in expected)
    assert csv_ids == expected_ids, (
        f"users.csv ids do not match the live WorkOS API. "
        f"Missing in CSV: {sorted(set(expected_ids) - set(csv_ids))}; "
        f"Unexpected in CSV: {sorted(set(csv_ids) - set(expected_ids))}."
    )

    # Check that there are no duplicate ids in the CSV.
    assert len(set(rec["id"] for rec in csv_records)) == len(csv_records), (
        "users.csv contains duplicate user ids."
    )

    expected_by_id = {u["id"]: u for u in expected}
    for rec in csv_records:
        ref = expected_by_id[rec["id"]]
        for field in ("email", "first_name", "last_name", "created_at"):
            assert rec[field] == _norm(ref[field]), (
                f"Mismatch for user {rec['id']!r} field {field!r}: "
                f"CSV has {rec[field]!r}, live API has {ref[field]!r}."
            )

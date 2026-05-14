import json
import os
import urllib.parse
import urllib.request

import pytest

PROJECT_DIR = "/home/user/myproject"
INDEX_PATH = os.path.join(PROJECT_DIR, "index.js")
LOG_PATH = os.path.join(PROJECT_DIR, "events.log")

API_BASE = "https://api.workos.com/events"
EVENT_TYPE = "dsync.user.created"
PAGE_LIMIT = 2


def _api_key():
    key = os.environ.get("WORKOS_API_KEY", "")
    assert key, "WORKOS_API_KEY env var is not set in the verifier environment."
    return key


def _fetch_page(after):
    params = [("events[]", EVENT_TYPE), ("limit", str(PAGE_LIMIT))]
    if after:
        params.append(("after", after))
    url = f"{API_BASE}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {_api_key()}",
            "Accept": "application/json",
        },
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        assert resp.status == 200, (
            f"WorkOS Events API returned HTTP {resp.status} for {url}"
        )
        body = resp.read().decode("utf-8")
    payload = json.loads(body)
    return payload


def _fetch_all_events():
    collected = []
    after = None
    while True:
        payload = _fetch_page(after)
        data = payload.get("data", []) or []
        for evt in data:
            collected.append((evt.get("id", ""), evt.get("event", "")))
        meta = payload.get("list_metadata", {}) or {}
        next_cursor = meta.get("after")
        if not next_cursor or len(data) == 0:
            break
        after = next_cursor
    return collected


def _read_log():
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        raw = f.read()
    return [line for line in raw.splitlines() if line.strip()]


def test_index_js_exists():
    assert os.path.isfile(INDEX_PATH), (
        f"Expected the agent's Node.js script at {INDEX_PATH}, but it was not found."
    )


def test_events_log_exists_and_non_empty():
    assert os.path.isfile(LOG_PATH), (
        f"Expected the events log at {LOG_PATH}, but it was not found."
    )
    size = os.path.getsize(LOG_PATH)
    assert size > 0, f"Events log at {LOG_PATH} is empty (size=0)."


def test_log_lines_have_expected_format():
    lines = _read_log()
    assert lines, f"Events log at {LOG_PATH} contains no non-empty lines."
    for line in lines:
        parts = line.split(" ", 1)
        assert len(parts) == 2, (
            f"Log line {line!r} is not in the expected '<event_id> <event_type>' format."
        )
        event_id, event_type = parts
        assert event_id.startswith("event_"), (
            f"Log line {line!r} has an event id that does not start with 'event_'."
        )
        assert event_type == EVENT_TYPE, (
            f"Log line {line!r} has event type {event_type!r}, expected {EVENT_TYPE!r}."
        )


def test_log_captures_independent_api_results():
    expected_events = _fetch_all_events()
    assert expected_events, (
        "The test account returned no 'dsync.user.created' events from the live "
        "WorkOS Events API; cannot verify the script's output."
    )

    actual_lines = _read_log()
    actual_pairs = set()
    for line in actual_lines:
        parts = line.split(" ", 1)
        if len(parts) == 2:
            actual_pairs.add((parts[0], parts[1]))

    missing = [pair for pair in expected_events if pair not in actual_pairs]
    assert not missing, (
        f"Events log at {LOG_PATH} is missing {len(missing)} event(s) returned by the "
        f"independent API call; first missing: {missing[:3]}"
    )


def test_log_demonstrates_pagination():
    actual_lines = _read_log()
    # With PAGE_LIMIT == 2, observing 3 or more entries proves that the script
    # advanced past the first page using the `after` cursor at least once.
    assert len(actual_lines) >= PAGE_LIMIT + 1, (
        f"Events log has only {len(actual_lines)} entries; expected at least "
        f"{PAGE_LIMIT + 1} to demonstrate that the script used the `after` cursor "
        "to fetch a second page (limit per page is 2)."
    )

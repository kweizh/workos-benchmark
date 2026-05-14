import json
import os
import urllib.error
import urllib.request

import pytest

PROJECT_DIR = "/home/user/myproject"
ADD_DOMAIN_JS = os.path.join(PROJECT_DIR, "add_domain.js")
ORG_JSON = os.path.join(PROJECT_DIR, "org.json")

WORKOS_API_KEY = os.environ.get("WORKOS_API_KEY")
WORKOS_ORGANIZATION_ID = os.environ.get("WORKOS_ORGANIZATION_ID")
WORKOS_NEW_DOMAIN = os.environ.get("WORKOS_NEW_DOMAIN")


def _extract_domain(entry):
    """Normalize a domain entry from the WorkOS API into a lowercase string."""
    if isinstance(entry, str):
        return entry.lower()
    if isinstance(entry, dict):
        for key in ("domain", "name"):
            value = entry.get(key)
            if isinstance(value, str):
                return value.lower()
    return None


def test_required_env_vars_present():
    assert WORKOS_API_KEY, "WORKOS_API_KEY must be set for verification."
    assert WORKOS_ORGANIZATION_ID, "WORKOS_ORGANIZATION_ID must be set for verification."
    assert WORKOS_NEW_DOMAIN, "WORKOS_NEW_DOMAIN must be set for verification."


def test_add_domain_script_exists():
    assert os.path.isfile(ADD_DOMAIN_JS), (
        f"Expected the implementation script at {ADD_DOMAIN_JS}."
    )


def test_org_json_exists_and_is_valid_json():
    assert os.path.isfile(ORG_JSON), f"Expected {ORG_JSON} to exist after running add_domain.js."
    with open(ORG_JSON) as f:
        data = json.load(f)
    assert isinstance(data, dict), f"{ORG_JSON} should contain a JSON object, got: {type(data)}"


def test_org_json_contains_new_domain():
    with open(ORG_JSON) as f:
        data = json.load(f)

    org_id = data.get("id")
    assert org_id == WORKOS_ORGANIZATION_ID, (
        f"Expected org.json id == {WORKOS_ORGANIZATION_ID}, got: {org_id!r}"
    )

    domains = data.get("domains")
    assert isinstance(domains, list), (
        f"Expected 'domains' in {ORG_JSON} to be a list, got: {type(domains)}"
    )

    normalized = [d for d in (_extract_domain(entry) for entry in domains) if d]
    assert WORKOS_NEW_DOMAIN.lower() in normalized, (
        f"Expected new domain {WORKOS_NEW_DOMAIN!r} to appear in org.json domains, "
        f"got: {normalized}"
    )


def test_workos_api_reflects_new_domain():
    """Independently fetch the organization from WorkOS to confirm the side effect is real."""
    url = f"https://api.workos.com/organizations/{WORKOS_ORGANIZATION_ID}"
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {WORKOS_API_KEY}",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            status = resp.getcode()
            body = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        pytest.fail(
            f"WorkOS API request to {url} failed with HTTP {e.code}: {e.read().decode('utf-8', errors='replace')}"
        )
    except urllib.error.URLError as e:
        pytest.fail(f"WorkOS API request to {url} failed: {e}")

    assert status == 200, f"Expected HTTP 200 from WorkOS API, got {status}: {body}"

    payload = json.loads(body)
    assert payload.get("id") == WORKOS_ORGANIZATION_ID, (
        f"Expected API response id == {WORKOS_ORGANIZATION_ID}, got: {payload.get('id')!r}"
    )

    domains = payload.get("domains")
    assert isinstance(domains, list), (
        f"Expected 'domains' in WorkOS API response to be a list, got: {type(domains)}"
    )

    normalized = [d for d in (_extract_domain(entry) for entry in domains) if d]
    assert WORKOS_NEW_DOMAIN.lower() in normalized, (
        f"Expected new domain {WORKOS_NEW_DOMAIN!r} to be present on the WorkOS "
        f"organization {WORKOS_ORGANIZATION_ID}, but got: {normalized}"
    )

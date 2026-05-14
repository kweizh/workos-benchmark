import json
import os
import pathlib
import subprocess
import urllib.error
import urllib.request

import pytest

PROJECT_DIR = "/home/user/myproject"
SCRIPT_PATH = os.path.join(PROJECT_DIR, "generate_link.js")
PACKAGE_JSON = os.path.join(PROJECT_DIR, "package.json")
LINK_FILE = os.path.join(PROJECT_DIR, "portal_link.txt")


def _http_get(url, headers=None, timeout=30):
    req = urllib.request.Request(url, headers=headers or {})
    return urllib.request.urlopen(req, timeout=timeout)


def test_script_file_exists():
    assert os.path.isfile(SCRIPT_PATH), (
        f"Expected agent-authored script at {SCRIPT_PATH}, but it is missing."
    )


def test_package_json_exists_with_workos_dependency():
    assert os.path.isfile(PACKAGE_JSON), (
        f"Expected {PACKAGE_JSON} to exist (created via `npm init` / `npm install`)."
    )
    pkg = json.loads(pathlib.Path(PACKAGE_JSON).read_text())
    deps = {}
    deps.update(pkg.get("dependencies") or {})
    deps.update(pkg.get("devDependencies") or {})
    assert "@workos-inc/node" in deps, (
        f"Expected '@workos-inc/node' in package.json dependencies, found: {sorted(deps)}"
    )


def test_node_modules_has_workos_sdk():
    workos_pkg = os.path.join(
        PROJECT_DIR, "node_modules", "@workos-inc", "node", "package.json"
    )
    assert os.path.isfile(workos_pkg), (
        f"Expected @workos-inc/node installed locally at {workos_pkg}."
    )


def test_script_uses_workos_sdk_and_sso_intent():
    content = pathlib.Path(SCRIPT_PATH).read_text()
    assert "@workos-inc/node" in content, (
        "Script must import/require '@workos-inc/node'."
    )
    assert "portal.generateLink" in content or "portal . generateLink" in content, (
        "Script must call workos.portal.generateLink(...)."
    )
    # Allow single/double quotes around the intent value.
    assert (
        "intent: 'sso'" in content
        or 'intent: "sso"' in content
        or "intent:'sso'" in content
        or 'intent:"sso"' in content
    ), "Script must pass intent: 'sso' to portal.generateLink."


def test_portal_link_file_exists_and_is_https_url():
    assert os.path.isfile(LINK_FILE), (
        f"Expected {LINK_FILE} to exist after running the script."
    )
    contents = pathlib.Path(LINK_FILE).read_text().strip()
    assert contents, f"{LINK_FILE} must not be empty."
    first_line = contents.splitlines()[0].strip()
    assert first_line.startswith("https://"), (
        f"Expected portal link to start with 'https://', got: {first_line!r}"
    )


def test_portal_link_returns_http_200():
    """Priority 1: hit the real Portal URL produced by the agent and require HTTP 200."""
    url = pathlib.Path(LINK_FILE).read_text().strip().splitlines()[0].strip()
    try:
        with _http_get(url) as resp:
            status = resp.status
    except urllib.error.HTTPError as e:
        pytest.fail(
            f"GET {url} raised HTTPError with status {e.code}: {e.reason}"
        )
    except urllib.error.URLError as e:
        pytest.fail(f"GET {url} failed to connect: {e.reason}")
    assert status == 200, (
        f"Expected HTTP 200 from Portal link, got {status} for {url}."
    )


def test_workos_organization_exists_via_real_api():
    """Priority 1: independently call the real WorkOS API to confirm the org exists,
    which proves the agent's WORKOS_API_KEY + WORKOS_ORGANIZATION_ID are real."""
    api_key = os.environ.get("WORKOS_API_KEY")
    org_id = os.environ.get("WORKOS_ORGANIZATION_ID")
    assert api_key, "WORKOS_API_KEY must be set in the verifier environment."
    assert org_id, "WORKOS_ORGANIZATION_ID must be set in the verifier environment."
    url = f"https://api.workos.com/organizations/{org_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
    }
    try:
        with _http_get(url, headers=headers) as resp:
            status = resp.status
            body = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        pytest.fail(
            f"WorkOS organizations API returned HTTP {e.code}: {e.reason} for org {org_id}"
        )
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to reach WorkOS organizations API: {e.reason}")
    assert status == 200, (
        f"Expected HTTP 200 from WorkOS for org {org_id}, got {status}. Body: {body[:300]}"
    )
    data = json.loads(body)
    assert data.get("id") == org_id, (
        f"WorkOS API returned a different org id than requested: {data.get('id')!r} vs {org_id!r}"
    )

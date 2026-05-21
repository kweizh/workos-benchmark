import json
import os
import subprocess

import pytest

PROJECT_DIR = "/home/user/myproject"
INDEX_JS = os.path.join(PROJECT_DIR, "index.js")
SCHEMA_JSON = os.path.join(PROJECT_DIR, "schema.json")
VERIFY_JS = os.path.join(PROJECT_DIR, "verify.js")


def _extract_resource_types(payload):
    """The list endpoint may return either `{"data": [...]}` or a bare array."""
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("data", "resource_types", "resourceTypes"):
            value = payload.get(key)
            if isinstance(value, list):
                return value
    return []


def _find_type(items, type_slug):
    for item in items:
        if not isinstance(item, dict):
            continue
        if item.get("type") == type_slug or item.get("slug") == type_slug:
            return item
    return None


def _relations_of(item):
    if not isinstance(item, dict):
        return {}
    rel = item.get("relations")
    return rel if isinstance(rel, dict) else {}


def _allowed_types_of(relation_def):
    if not isinstance(relation_def, dict):
        return []
    for key in ("allowed_types", "allowedTypes"):
        value = relation_def.get(key)
        if isinstance(value, list):
            return value
    return []


def _normalize_allowed(allowed):
    """Allowed types may be plain strings or `{ "type": "user" }` objects."""
    result = []
    for entry in allowed:
        if isinstance(entry, str):
            result.append(entry)
        elif isinstance(entry, dict):
            slug = entry.get("type") or entry.get("slug")
            if isinstance(slug, str):
                result.append(slug)
    return result


def test_index_js_exists():
    assert os.path.isfile(INDEX_JS), f"{INDEX_JS} was not created by the agent."


def test_index_js_uses_resource_types_endpoint():
    with open(INDEX_JS) as f:
        content = f.read()
    assert "/fga/v1/resource-types" in content, (
        f"{INDEX_JS} must call the WorkOS FGA resource-types REST endpoint "
        "(`/fga/v1/resource-types`); endpoint path not found in the file."
    )
    for needle in ("folder", "document", "inherit_if"):
        assert needle in content, (
            f"{INDEX_JS} must reference the schema concept `{needle}`; not found."
        )


def test_schema_json_exists_and_contains_required_types():
    assert os.path.isfile(SCHEMA_JSON), f"{SCHEMA_JSON} was not created by the agent."
    with open(SCHEMA_JSON) as f:
        payload = json.load(f)
    items = _extract_resource_types(payload)
    assert items, (
        f"{SCHEMA_JSON} must contain a list of resource types under `data`, "
        f"`resource_types`, or as a top-level array. Got: {payload!r}"
    )

    folder = _find_type(items, "folder")
    assert folder is not None, (
        f"{SCHEMA_JSON} must contain a `folder` resource type. "
        f"Found types: {[i.get('type') for i in items if isinstance(i, dict)]!r}"
    )
    folder_relations = _relations_of(folder)
    assert "parent" in folder_relations, (
        f"`folder` resource type must define a `parent` relation. "
        f"Got relations: {list(folder_relations.keys())!r}"
    )
    folder_parent_allowed = _normalize_allowed(_allowed_types_of(folder_relations["parent"]))
    assert "folder" in folder_parent_allowed, (
        f"`folder.parent` must allow `folder` as a subject type. "
        f"Got allowed_types: {folder_parent_allowed!r}"
    )
    assert "viewer" in folder_relations, (
        f"`folder` resource type must define a `viewer` relation. "
        f"Got relations: {list(folder_relations.keys())!r}"
    )
    folder_viewer_allowed = _normalize_allowed(_allowed_types_of(folder_relations["viewer"]))
    assert "user" in folder_viewer_allowed, (
        f"`folder.viewer` must allow `user` as a subject type. "
        f"Got allowed_types: {folder_viewer_allowed!r}"
    )

    document = _find_type(items, "document")
    assert document is not None, (
        f"{SCHEMA_JSON} must contain a `document` resource type. "
        f"Found types: {[i.get('type') for i in items if isinstance(i, dict)]!r}"
    )
    document_relations = _relations_of(document)
    assert "parent" in document_relations, (
        f"`document` resource type must define a `parent` relation. "
        f"Got relations: {list(document_relations.keys())!r}"
    )
    document_parent_allowed = _normalize_allowed(_allowed_types_of(document_relations["parent"]))
    assert "folder" in document_parent_allowed, (
        f"`document.parent` must allow `folder` as a subject type. "
        f"Got allowed_types: {document_parent_allowed!r}"
    )
    document_viewer = document_relations.get("viewer")
    assert isinstance(document_viewer, dict), (
        f"`document.viewer` relation must be an object describing inheritance. "
        f"Got: {document_viewer!r}"
    )
    document_viewer_allowed = _normalize_allowed(_allowed_types_of(document_viewer))
    assert "user" in document_viewer_allowed, (
        f"`document.viewer` must allow `user` as a subject type. "
        f"Got allowed_types: {document_viewer_allowed!r}"
    )
    inherit_if = document_viewer.get("inherit_if") or document_viewer.get("inheritIf")
    of_type = document_viewer.get("of_type") or document_viewer.get("ofType")
    with_relation = document_viewer.get("with_relation") or document_viewer.get("withRelation")
    assert inherit_if == "viewer", (
        f"`document.viewer` must inherit from `viewer`; got inherit_if={inherit_if!r} "
        f"in {document_viewer!r}"
    )
    assert of_type == "folder", (
        f"`document.viewer` must inherit of_type=`folder`; got of_type={of_type!r} "
        f"in {document_viewer!r}"
    )
    assert with_relation == "parent", (
        f"`document.viewer` must inherit with_relation=`parent`; got "
        f"with_relation={with_relation!r} in {document_viewer!r}"
    )


@pytest.fixture(scope="module")
def write_verify_script():
    """Write a Node.js verifier script that re-fetches resource types from WorkOS."""
    script = r"""
const apiKey = process.env.WORKOS_API_KEY;
if (!apiKey) {
  console.error(JSON.stringify({ error: 'WORKOS_API_KEY env var is not set in verifier' }));
  process.exit(2);
}

(async () => {
  try {
    const resp = await fetch('https://api.workos.com/fga/v1/resource-types?limit=100', {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${apiKey}`,
        'User-Agent': 'workos-benchmark-fga-schema-verifier/1.0',
      },
    });
    const text = await resp.text();
    if (!resp.ok) {
      console.error(JSON.stringify({ error: 'GET /fga/v1/resource-types failed', status: resp.status, body: text }));
      process.exit(3);
    }
    let payload;
    try {
      payload = JSON.parse(text);
    } catch (e) {
      console.error(JSON.stringify({ error: 'response was not JSON', body: text }));
      process.exit(4);
    }
    console.log(JSON.stringify(payload));
  } catch (err) {
    console.error(JSON.stringify({ error: String(err && err.message || err) }));
    process.exit(1);
  }
})();
"""
    with open(VERIFY_JS, "w") as f:
        f.write(script)
    yield VERIFY_JS


def test_live_workos_api_has_required_resource_types(write_verify_script):
    api_key = os.environ.get("WORKOS_API_KEY")
    assert api_key, "WORKOS_API_KEY env var must be set in the verifier environment."

    env = os.environ.copy()
    env["WORKOS_API_KEY"] = api_key

    result = subprocess.run(
        ["node", VERIFY_JS],
        capture_output=True,
        text=True,
        cwd=PROJECT_DIR,
        env=env,
        timeout=120,
    )
    assert result.returncode == 0, (
        f"Verifier script `node verify.js` failed with exit code {result.returncode}.\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )

    stdout_lines = [line for line in result.stdout.strip().splitlines() if line.strip()]
    assert stdout_lines, f"Verifier produced no stdout. stderr: {result.stderr}"
    try:
        payload = json.loads(stdout_lines[-1])
    except json.JSONDecodeError as exc:
        pytest.fail(
            f"Could not parse verifier JSON output: {exc}\nstdout: {result.stdout}"
        )

    items = _extract_resource_types(payload)
    assert items, (
        f"Live WorkOS API response did not contain a `data`/`resource_types` list. "
        f"Got: {payload!r}"
    )

    folder = _find_type(items, "folder")
    assert folder is not None, (
        "Live WorkOS API does not contain a `folder` resource type after the agent run. "
        f"Available types: {[i.get('type') for i in items if isinstance(i, dict)]!r}"
    )
    folder_relations = _relations_of(folder)
    assert "parent" in folder_relations and "viewer" in folder_relations, (
        f"Live `folder` resource type must declare both `parent` and `viewer` relations. "
        f"Got relations: {list(folder_relations.keys())!r}"
    )
    assert "user" in _normalize_allowed(_allowed_types_of(folder_relations["viewer"])), (
        f"Live `folder.viewer` must allow `user`. Got: {folder_relations['viewer']!r}"
    )

    document = _find_type(items, "document")
    assert document is not None, (
        "Live WorkOS API does not contain a `document` resource type after the agent run. "
        f"Available types: {[i.get('type') for i in items if isinstance(i, dict)]!r}"
    )
    document_relations = _relations_of(document)
    assert "parent" in document_relations and "viewer" in document_relations, (
        f"Live `document` resource type must declare both `parent` and `viewer` relations. "
        f"Got relations: {list(document_relations.keys())!r}"
    )
    assert "folder" in _normalize_allowed(_allowed_types_of(document_relations["parent"])), (
        f"Live `document.parent` must allow `folder`. Got: {document_relations['parent']!r}"
    )
    document_viewer = document_relations["viewer"]
    inherit_if = document_viewer.get("inherit_if") or document_viewer.get("inheritIf")
    of_type = document_viewer.get("of_type") or document_viewer.get("ofType")
    with_relation = document_viewer.get("with_relation") or document_viewer.get("withRelation")
    assert inherit_if == "viewer" and of_type == "folder" and with_relation == "parent", (
        f"Live `document.viewer` must inherit `viewer` of_type=`folder` with_relation=`parent`. "
        f"Got: inherit_if={inherit_if!r}, of_type={of_type!r}, with_relation={with_relation!r}, "
        f"full relation def: {document_viewer!r}"
    )

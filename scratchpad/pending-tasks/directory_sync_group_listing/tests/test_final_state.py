import json
import os
import subprocess

import pytest

PROJECT_DIR = "/home/user/myproject"
SCRIPT_PATH = os.path.join(PROJECT_DIR, "list_groups.js")
OUTPUT_PATH = os.path.join(PROJECT_DIR, "groups.txt")


def _read_groups_file():
    with open(OUTPUT_PATH) as f:
        content = f.read()
    # Split on newlines, drop the final blank line produced by a trailing newline,
    # but preserve any group names that contain inner whitespace.
    lines = content.split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]
    return lines


def _fetch_groups_via_workos_api():
    """Independently call the WorkOS API via @workos-inc/node to fetch the authoritative
    list of group names for the configured directory. The verifier MUST NOT mock the
    SDK — it talks to the real WorkOS API.
    """
    api_key = os.environ.get("WORKOS_API_KEY")
    directory_id = os.environ.get("WORKOS_DIRECTORY_ID")
    assert api_key, "WORKOS_API_KEY must be set in the verifier environment."
    assert directory_id, (
        "WORKOS_DIRECTORY_ID must be set in the verifier environment."
    )

    js = r"""
const { WorkOS } = require('@workos-inc/node');

(async () => {
  const workos = new WorkOS(process.env.WORKOS_API_KEY);
  const directory = process.env.WORKOS_DIRECTORY_ID;
  const all = [];
  let after = undefined;
  // Page through all groups so the comparison is exhaustive.
  // eslint-disable-next-line no-constant-condition
  while (true) {
    const params = { directory, limit: 100 };
    if (after) params.after = after;
    const result = await workos.directorySync.listGroups(params);
    for (const g of result.data) all.push(g.name);
    after = result.listMetadata && result.listMetadata.after;
    if (!after) break;
  }
  process.stdout.write(JSON.stringify(all));
})().catch((err) => {
  console.error(err && err.stack ? err.stack : String(err));
  process.exit(1);
});
"""
    result = subprocess.run(
        ["node", "-e", js],
        capture_output=True,
        text=True,
        cwd=PROJECT_DIR,
        env=os.environ.copy(),
    )
    assert result.returncode == 0, (
        "Independent WorkOS API call failed in verifier: "
        f"stdout={result.stdout!r} stderr={result.stderr!r}"
    )
    return json.loads(result.stdout)


def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), (
        f"Expected script not found at {SCRIPT_PATH}."
    )


def test_output_file_exists():
    assert os.path.isfile(OUTPUT_PATH), (
        f"Expected output file not found at {OUTPUT_PATH}."
    )


def test_script_uses_real_workos_sdk():
    """The script must use the real @workos-inc/node SDK and read credentials from env."""
    with open(SCRIPT_PATH) as f:
        source = f.read()
    assert "@workos-inc/node" in source, (
        "list_groups.js must import the @workos-inc/node SDK (no mocks/stubs)."
    )
    assert "listGroups" in source, (
        "list_groups.js must call workos.directorySync.listGroups."
    )
    assert "WORKOS_API_KEY" in source, (
        "list_groups.js must read WORKOS_API_KEY from environment variables."
    )
    assert "WORKOS_DIRECTORY_ID" in source, (
        "list_groups.js must read WORKOS_DIRECTORY_ID from environment variables."
    )


def test_groups_txt_matches_workos_api():
    """Priority 1: independently call the WorkOS API and compare against groups.txt."""
    file_groups = _read_groups_file()
    api_groups = _fetch_groups_via_workos_api()

    # No stray blank lines in the file.
    for line in file_groups:
        assert line.strip() != "" or line == "", (
            f"groups.txt must not contain blank lines, got: {line!r}"
        )

    # Compare as multisets so duplicate group names are still detected.
    assert sorted(file_groups) == sorted(api_groups), (
        "Contents of groups.txt do not match WorkOS Directory Sync API.\n"
        f"  groups.txt ({len(file_groups)}): {sorted(file_groups)!r}\n"
        f"  WorkOS API ({len(api_groups)}): {sorted(api_groups)!r}"
    )

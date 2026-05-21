# Set a Metadata Key on an Existing WorkOS Organization

## Background
WorkOS organizations support a free-form `metadata` map (string keys/values). In this task you will set a metadata key on an existing organization using the SDK and persist the response.

## Requirements
1. Project lives at `/home/user/myproject`.
2. Implement `/home/user/myproject/update_metadata.js` that:
   - Reads `WORKOS_API_KEY`, `WORKOS_ORGANIZATION_ID`, and `ZEALT_RUN_ID`.
   - Uses the fixed metadata key `pochi_benchmark_marker` and value `pochi-mv-${process.env.ZEALT_RUN_ID || 'default'}`.
   - First reads the current organization with `workos.organizations.getOrganization(...)` to preserve existing metadata.
   - Calls `workos.organizations.updateOrganization({ organization, metadata: { ...existing, pochi_benchmark_marker: value } })`.
   - Writes the returned organization as JSON (pretty, 2-space) to `/home/user/myproject/org.json`.
3. Run `node update_metadata.js`.

## Constraints
- Use real WorkOS API; do NOT mock.
- Idempotent: re-running with the same ZEALT_RUN_ID must result in the same metadata key/value.

## Integrations
- WorkOS (Organizations API).

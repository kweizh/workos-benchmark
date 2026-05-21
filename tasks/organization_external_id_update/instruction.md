# Update an Organization's external_id

## Background
Set the `external_id` of an existing WorkOS organization using the Node SDK, then persist the returned org object for downstream tools.

## Requirements
1. Project lives at `/home/user/myproject`.
2. Implement `/home/user/myproject/update_external_id.js` that:
   - Reads `WORKOS_API_KEY`, `WORKOS_ORGANIZATION_ID`, and `ZEALT_RUN_ID`.
   - Derives the new external id as `pochi-ext-${process.env.ZEALT_RUN_ID || 'default'}`. The value is fully derived from `ZEALT_RUN_ID`, so re-runs and parallel runs are isolated.
   - Calls `workos.organizations.updateOrganization({ organization: WORKOS_ORGANIZATION_ID, externalId })`.
   - Writes the returned organization object (pretty JSON, 2-space) to `/home/user/myproject/org.json`.
3. Run `node update_external_id.js`.

## Constraints
- Use real WorkOS API. Do NOT mock.
- Use the camelCase SDK field `externalId`.

## Integrations
- WorkOS (Organizations API).

# Generate an Admin Portal Directory Sync Setup Link

## Background
Generate an Admin Portal link to let an organization administrator configure their own Directory Sync (intent: `dsync`).

## Requirements
1. Project lives at `/home/user/myproject`.
2. Implement `/home/user/myproject/portal_dsync_link.js` that:
   - Reads `WORKOS_API_KEY` and `WORKOS_ORGANIZATION_ID`.
   - Calls `workos.portal.generateLink({ organization, intent: 'dsync' })`.
   - Writes the response object as JSON to `/home/user/myproject/portal_link.json`.
3. Run `node portal_dsync_link.js`.

## Constraints
- Real WorkOS API; no mocks.
- The `link` must be an HTTPS URL on a WorkOS domain.

## Integrations
- WorkOS (Admin Portal API).

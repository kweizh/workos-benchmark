# List WorkOS Invitations for an Organization

## Background
Enumerate every invitation associated with a WorkOS organization, paginating with `limit: 2` to exercise the cursor.

## Requirements
1. Project at `/home/user/myproject`.
2. Implement `/home/user/myproject/list_invitations.js` that:
   - Reads `WORKOS_API_KEY` and `WORKOS_ORGANIZATION_ID`.
   - Pages through `workos.userManagement.listInvitations({ organizationId: process.env.WORKOS_ORGANIZATION_ID, limit: 2, after })`.
   - Writes an array of `{ id, email, state, organization_id }` (strings) to `/home/user/myproject/invitations.json`.
3. Run `node list_invitations.js`.

## Constraints
- Real WorkOS API; no mocks. Page size MUST be 2.

## Integrations
- WorkOS (User Management Invitations API).

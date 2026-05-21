# Paginate Organization Memberships

## Background
List every organization membership (user-to-org relationship) attached to a given WorkOS organization.

## Requirements
1. Project at `/home/user/myproject`.
2. Implement `/home/user/myproject/list_memberships.js` that:
   - Reads `WORKOS_API_KEY` and `WORKOS_ORGANIZATION_ID`.
   - Pages through `workos.userManagement.listOrganizationMemberships({ organizationId, limit: 2, after })`.
   - Writes a JSON array of `{ id, user_id, organization_id, status }` (strings) to `/home/user/myproject/memberships.json`.
3. Run `node list_memberships.js`.

## Constraints
- Real WorkOS API; no mocks. Page size 2.

## Integrations
- WorkOS (User Management API).

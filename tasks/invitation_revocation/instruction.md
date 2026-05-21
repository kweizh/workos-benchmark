# Send and Revoke a WorkOS Invitation

## Background
Send an invitation to an email address inside an organization, then immediately revoke it. The invitee email is derived from `ZEALT_RUN_ID` so reruns are isolated.

## Requirements
1. Project at `/home/user/myproject`.
2. Implement `/home/user/myproject/revoke_invitation.js` that:
   - Reads `WORKOS_API_KEY`, `WORKOS_ORGANIZATION_ID`, and `ZEALT_RUN_ID`.
   - Derives the invitee email as `pochi-invite-${(process.env.ZEALT_RUN_ID || 'default').toLowerCase()}@pochi-benchmark.example`.
   - Calls `workos.userManagement.sendInvitation({ email, organizationId: process.env.WORKOS_ORGANIZATION_ID })`. If the invitation already exists (e.g., from a previous run), look it up via `workos.userManagement.listInvitations({ email, organizationId })` so the script is idempotent.
   - Calls `workos.userManagement.revokeInvitation(invitation.id)`.
   - Writes the revoked invitation object to `/home/user/myproject/invitation.json`.
3. Run `node revoke_invitation.js`.

## Constraints
- Real WorkOS API; no mocks.

## Integrations
- WorkOS (User Management Invitations API).

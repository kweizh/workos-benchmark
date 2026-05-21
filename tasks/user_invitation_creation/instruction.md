# Send a WorkOS User Invitation to an Organization

## Background
A B2B SaaS application uses [WorkOS User Management](https://workos.com/docs/user-management/invitations) to onboard customers' teammates into their organizations. The growth team wants a small command-line utility that issues an organization-scoped invitation and records the resulting invitation `id` and `token` to disk so that the rest of the onboarding pipeline can pick it up.

Your job is to write a small Node.js script that uses the official `@workos-inc/node` SDK to call `workos.userManagement.sendInvitation(...)` and persist the returned `id` and `token` to a JSON file.

## Requirements
- Create a Node.js script at `/home/user/myproject/send_invitation.js`.
- Initialize the WorkOS client using the `WORKOS_API_KEY` environment variable. Do NOT hardcode the API key.
- Read the target organization id from the `WORKOS_ORGANIZATION_ID` environment variable and the recipient email from the `WORKOS_INVITE_EMAIL` environment variable. Do NOT hardcode either value.
- Call `await workos.userManagement.sendInvitation({ email: process.env.WORKOS_INVITE_EMAIL, organizationId: process.env.WORKOS_ORGANIZATION_ID })` from the official `@workos-inc/node` SDK.
- Write the resulting invitation `id` and `token` to `/home/user/myproject/invitation.json` as a JSON object with exactly the keys `id` and `token` (string values). For example: `{"id": "invitation_01...", "token": "..."}`.
- Run the script once so that `invitation.json` is written before the task completes.

## Implementation Guide
1. The directory `/home/user/myproject` already exists and has `@workos-inc/node` installed as a dependency (see `package.json`).
2. Inside that directory, create `send_invitation.js` that:
   - Imports `WorkOS` from `@workos-inc/node`.
   - Constructs the client as `new WorkOS(process.env.WORKOS_API_KEY)`.
   - Calls `await workos.userManagement.sendInvitation({ email: process.env.WORKOS_INVITE_EMAIL, organizationId: process.env.WORKOS_ORGANIZATION_ID })`.
   - Writes `{ id: invitation.id, token: invitation.token }` to `invitation.json` using `JSON.stringify`.
3. Execute the script with `node send_invitation.js` from `/home/user/myproject` so the output file is produced.

## Constraints
- Project path: `/home/user/myproject`
- Script path: `/home/user/myproject/send_invitation.js`
- Output file: `/home/user/myproject/invitation.json`
- Use the `@workos-inc/node` SDK (already installed).
- Use the real WorkOS API; do NOT mock the SDK.
- Read credentials and inputs from environment variables only.

## Integrations
- WorkOS (User Management / Invitations). Requires `WORKOS_API_KEY`, `WORKOS_ORGANIZATION_ID`, and `WORKOS_INVITE_EMAIL`.
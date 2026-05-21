# Send a Verification Email to a WorkOS User

## Background
Trigger WorkOS to send an email verification message to a given user via `sendVerificationEmail`.

## Requirements
1. Project at `/home/user/myproject`.
2. Implement `/home/user/myproject/send_verification.js` that:
   - Reads `WORKOS_API_KEY` and `WORKOS_USER_ID`.
   - Calls `workos.userManagement.sendVerificationEmail({ userId: process.env.WORKOS_USER_ID })`.
   - Writes the returned object as JSON to `/home/user/myproject/verification.json`.
3. Run `node send_verification.js`.

## Constraints
- Real WorkOS API; no mocks.
- Should not throw; on success a JSON object must be persisted.

## Integrations
- WorkOS (User Management API).

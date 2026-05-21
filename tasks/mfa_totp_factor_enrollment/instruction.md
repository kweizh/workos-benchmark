# WorkOS MFA TOTP Factor Enrollment

## Background
WorkOS provides a composable Multi-Factor Authentication (MFA) API that lets developers enroll authentication factors for users (such as Time-based One-Time Password / TOTP). The `@workos-inc/node` SDK exposes this functionality through `workos.mfa.enrollFactor`, which returns a factor object that includes a unique factor `id` and, for TOTP factors, a `qr_code` data URI plus a `secret` for use with authenticator apps such as Google Authenticator or Authy.

In this task you will write a small Node.js program that enrolls a new TOTP factor with the WorkOS MFA API and persists the resulting identifiers to a JSON file so that the rest of an application can later use them.

## Requirements
- Implement the script in the existing project directory `/home/user/myproject`.
- Use the `@workos-inc/node` SDK (already installed in `/home/user/myproject/node_modules`).
- Read the WorkOS API key from the `WORKOS_API_KEY` environment variable when constructing the `WorkOS` client. Do NOT hardcode any secret value.
- Call `workos.mfa.enrollFactor({ type: 'totp', issuer: 'Harbor MFA Task', user: 'mfa-totp-task@example.com' })` to enroll a real TOTP authentication factor against the live WorkOS API.
- Write the returned factor information to `/home/user/myproject/factor.json` as a JSON object with at least the following keys (top-level, exactly these names):
  - `id`: the WorkOS authentication factor id (e.g. `auth_factor_...`).
  - `type`: the factor type, which must be the string `"totp"`.
  - `qr_code`: the base64-encoded data URI returned by the API for the TOTP factor.
- The script must exit with code `0` on success.

## Implementation Guide
1. Create a file `/home/user/myproject/enroll.js`.
2. Import `WorkOS` from `@workos-inc/node` and construct the client using the `WORKOS_API_KEY` environment variable.
3. Call `workos.mfa.enrollFactor({ type: 'totp', issuer: 'Harbor MFA Task', user: 'mfa-totp-task@example.com' })` and `await` the result.
4. Build an object containing `id`, `type`, and `qr_code` from the response (`qr_code` is available on TOTP factors under `factor.totp.qr_code` in the SDK response).
5. Write that object to `/home/user/myproject/factor.json` (pretty-printed JSON is fine).
6. Run the script with `node enroll.js` from `/home/user/myproject` so that `factor.json` is created.

## Constraints
- Project path: `/home/user/myproject`
- Output file: `/home/user/myproject/factor.json`
- Use the real WorkOS MFA API via the `@workos-inc/node` SDK. Do NOT mock the SDK or fabricate the response. The verifier will look up the persisted `id` against the real WorkOS API.
- The `WORKOS_API_KEY` environment variable is provided in the task runtime; never print, log, or commit its value.

## Integrations
- WorkOS

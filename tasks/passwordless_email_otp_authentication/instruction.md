# Passwordless Email OTP Authentication with WorkOS

## Background
WorkOS User Management provides a passwordless authentication method called Magic Auth — a one-time 6-digit code that is delivered to the user's email inbox. In the current `@workos-inc/node` SDK (v8.x), the call `workos.userManagement.createMagicAuth({ email })` creates a one-time-use Magic Auth code and triggers WorkOS to email it to the user. The companion call `workos.userManagement.authenticateWithMagicAuth({ clientId, code, email })` is used later to verify the code.

In this task you must write a small Node.js script that initiates the passwordless email OTP flow against the **live** WorkOS API using the real `@workos-inc/node` SDK, then record the outcome in a log file.

## Requirements
- Create a Node.js project at `/home/user/myproject` (`package.json` already exists; you may extend it).
- Add the `@workos-inc/node` SDK as a dependency and install it.
- Implement `/home/user/myproject/index.js` that:
  1. Reads `WORKOS_API_KEY` and `WORKOS_CLIENT_ID` from `process.env`. Exit with a non-zero status if either is missing.
  2. Instantiates `new WorkOS(process.env.WORKOS_API_KEY, { clientId: process.env.WORKOS_CLIENT_ID })`.
  3. Calls `workos.userManagement.createMagicAuth({ email: 'passwordless-otp-test@example.com' })` to send a Magic Auth (passwordless email OTP) code via the **live** WorkOS API. Do **NOT** mock the API.
  4. On success (i.e. the API returns a Magic Auth object with an `id` starting with `magic_auth_`), append a single line to `/home/user/myproject/output.log` in the exact format:

     ```
     SUCCESS magic_auth_id=<id> email=passwordless-otp-test@example.com
     ```

     where `<id>` is the `id` field returned from the SDK.
  5. On any error, write the line `FAILURE <error message>` to the log and exit non-zero.
- Run the script once (e.g. `node index.js`) so the log file is created.

## Implementation Guide
1. `cd /home/user/myproject`
2. `npm install @workos-inc/node`
3. Create `index.js` with the logic described above, e.g.:
   ```js
   const fs = require('fs');
   const { WorkOS } = require('@workos-inc/node');

   const apiKey = process.env.WORKOS_API_KEY;
   const clientId = process.env.WORKOS_CLIENT_ID;
   if (!apiKey || !clientId) {
     console.error('Missing WORKOS_API_KEY or WORKOS_CLIENT_ID');
     process.exit(1);
   }

   const workos = new WorkOS(apiKey, { clientId });
   const LOG = '/home/user/myproject/output.log';

   (async () => {
     try {
       const magicAuth = await workos.userManagement.createMagicAuth({
         email: 'passwordless-otp-test@example.com',
       });
       fs.appendFileSync(
         LOG,
         `SUCCESS magic_auth_id=${magicAuth.id} email=passwordless-otp-test@example.com\n`,
       );
     } catch (err) {
       fs.appendFileSync(LOG, `FAILURE ${err.message}\n`);
       process.exit(1);
     }
   })();
   ```
4. `node index.js`

## Constraints
- Project path: `/home/user/myproject`
- Log file: `/home/user/myproject/output.log`
- The script MUST use the real `@workos-inc/node` SDK and must call the live WorkOS API. Do NOT mock, stub, or fake the API call.
- The script MUST read `WORKOS_API_KEY` and `WORKOS_CLIENT_ID` from environment variables — do not hardcode them.
- The test email address MUST be exactly `passwordless-otp-test@example.com`.

## Integrations
- WorkOS User Management API (Magic Auth / passwordless email OTP)

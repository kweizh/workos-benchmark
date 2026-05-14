# WorkOS Step-Up MFA

## Background
You are building a step-up MFA (Multi-Factor Authentication) flow for a Node.js Express application using the WorkOS SDK. The application already has a basic Express server set up in `/home/user/app/server.js`, but it lacks the MFA routes.

## Requirements
Implement three endpoints in `server.js` using the `@workos-inc/node` SDK:

1. `POST /enroll`
   - Accepts JSON body: `{ "email": "user@example.com", "issuer": "My App" }`
   - Uses `workos.mfa.enrollFactor` to enroll a `totp` factor.
   - Returns JSON: `{ "factorId": "<factor_id>", "secret": "<totp_secret>" }`

2. `POST /challenge`
   - Accepts JSON body: `{ "factorId": "<factor_id>" }`
   - Uses `workos.mfa.challengeFactor` to create a challenge.
   - Returns JSON: `{ "challengeId": "<challenge_id>" }`

3. `POST /verify`
   - Accepts JSON body: `{ "challengeId": "<challenge_id>", "code": "123456" }`
   - Uses `workos.mfa.verifyChallenge` to verify the code.
   - Returns JSON: `{ "valid": true }` or `{ "valid": false }`

## Constraints
- Project path: `/home/user/app`
- Start command: `npm start`
- Port: `3000`
- The WorkOS API Key is provided via the `WORKOS_API_KEY` environment variable.
- Do not modify the existing server setup code, just add the three routes.
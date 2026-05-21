# WorkOS Admin Portal SSO Connection Setup Link

## Background
When onboarding a new enterprise customer, your SaaS application needs to hand off SSO configuration to the customer's IT contact. WorkOS exposes an Admin Portal that provides a hosted, guided UI for IT contacts to verify domains and configure their SSO connection. Your application generates a short-lived secure URL via `workos.portal.generateLink({ organization, intent: 'sso' })` and redirects the IT contact to it.

You are building a Node.js bootstrap script that programmatically generates such a Portal link for an existing organization and persists the URL to disk so that the IT contact can be redirected to it.

## Requirements
- Create a Node.js project at `/home/user/myproject`.
- Initialize a `package.json` with `"type": "module"` (or use CommonJS, your choice) and install the `@workos-inc/node` SDK.
- Create an executable script `/home/user/myproject/generate_link.js` that:
  1. Reads `WORKOS_API_KEY` from the environment.
  2. Reads `WORKOS_ORGANIZATION_ID` from the environment (this is the WorkOS Organization ID to scope the Admin Portal session to).
  3. Instantiates the WorkOS SDK with the API key.
  4. Calls `workos.portal.generateLink({ organization: <orgId>, intent: 'sso' })`.
  5. Writes the returned `link` URL (and ONLY the URL, no extra whitespace or quotes — a single trailing newline is fine) to `/home/user/myproject/portal_link.txt`.
  6. Also prints the URL to stdout.
- Run the script once (e.g. `node generate_link.js`) so that `/home/user/myproject/portal_link.txt` exists with a real WorkOS Portal link.

## Implementation Guide
1. `cd /home/user/myproject`
2. `npm init -y`
3. `npm install @workos-inc/node`
4. Write `generate_link.js` using the WorkOS Node SDK:
   ```js
   import { WorkOS } from '@workos-inc/node';
   import { writeFileSync } from 'node:fs';

   const workos = new WorkOS(process.env.WORKOS_API_KEY);
   const organizationId = process.env.WORKOS_ORGANIZATION_ID;

   const { link } = await workos.portal.generateLink({
     organization: organizationId,
     intent: 'sso',
   });

   writeFileSync('/home/user/myproject/portal_link.txt', link + '\n');
   console.log(link);
   ```
5. Run the script: `node generate_link.js`.
6. Confirm `/home/user/myproject/portal_link.txt` exists and contains a URL beginning with `https://`.

## Constraints
- Project path: `/home/user/myproject`
- Script path: `/home/user/myproject/generate_link.js`
- Output file: `/home/user/myproject/portal_link.txt`
- The script MUST use the real WorkOS API via the `@workos-inc/node` SDK. Do NOT mock the WorkOS client or stub the network call.
- Use the `WORKOS_API_KEY` and `WORKOS_ORGANIZATION_ID` environment variables; do not hardcode them in the script.
- The intent passed to `generateLink` must be exactly the string `sso`.

## Integrations
- WorkOS (real API; `WORKOS_API_KEY` and `WORKOS_ORGANIZATION_ID` are provided)
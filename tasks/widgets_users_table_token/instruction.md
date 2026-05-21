# Generate a WorkOS Widget Token for the Users Table Widget

## Background
WorkOS Widgets are pre-built React components that let you embed enterprise admin flows (such as a users-management table) directly into your application. Each widget is rendered with a short-lived JWT token that must be generated on the backend with the WorkOS Node SDK. In this task you will create a small Node.js script that calls the WorkOS Widgets API and persists the returned token to a file.

## Requirements
- Initialize a Node.js project at `/home/user/myproject`.
- Add `@workos-inc/node` as a dependency.
- Create a script `generate_token.js` that:
  1. Reads `WORKOS_API_KEY`, `WORKOS_ORGANIZATION_ID`, and `WORKOS_USER_ID` from the process environment.
  2. Instantiates a `WorkOS` client.
  3. Calls `workos.widgets.getToken({ organizationId, userId, scopes: ['widgets:users-table:manage'] })`.
  4. Writes the returned JWT (the raw string contained in `token`) to `/home/user/myproject/widget_token.txt` with no extra whitespace, prefixes, JSON quoting, or trailing newline characters.
- Run the script with `node generate_token.js` so that `widget_token.txt` exists and contains a valid widget token before the verifier runs.

## Implementation Guide
1. `mkdir -p /home/user/myproject && cd /home/user/myproject`.
2. Run `npm init -y` and `npm install @workos-inc/node`.
3. Create `generate_token.js` with the following structure:
   ```js
   const fs = require('fs');
   const { WorkOS } = require('@workos-inc/node');

   async function main() {
     const workos = new WorkOS(process.env.WORKOS_API_KEY);
     const { token } = await workos.widgets.getToken({
       organizationId: process.env.WORKOS_ORGANIZATION_ID,
       userId: process.env.WORKOS_USER_ID,
       scopes: ['widgets:users-table:manage'],
     });
     fs.writeFileSync('/home/user/myproject/widget_token.txt', token);
   }

   main().catch((err) => { console.error(err); process.exit(1); });
   ```
4. Execute `node generate_token.js`.

## Constraints
- Project path: /home/user/myproject
- Output file: /home/user/myproject/widget_token.txt
- Use the real WorkOS Widgets API via `@workos-inc/node`. Do NOT mock the SDK or hand-craft a fake JWT.
- Use Node.js v24 (already installed in the environment).
- Required environment variables (provided to the container): `WORKOS_API_KEY`, `WORKOS_ORGANIZATION_ID`, `WORKOS_USER_ID`.

## Integrations
- WorkOS (Widgets API)
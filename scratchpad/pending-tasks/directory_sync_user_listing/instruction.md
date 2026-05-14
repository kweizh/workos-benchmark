# Directory Sync — List Users with the WorkOS Node SDK

## Background
WorkOS Directory Sync provides a unified API for retrieving users that have been provisioned to a customer's directory (Okta, Azure AD, Google Workspace, etc.). In this task you will use the official `@workos-inc/node` SDK to list every user in a real WorkOS Directory and persist their primary email addresses to disk so that downstream services can consume them.

## Requirements
- Initialize a Node.js project in `/home/user/myproject` (the directory already exists).
- Use the `@workos-inc/node` SDK (already installed) to call `workos.directorySync.listUsers({ directory: <WORKOS_DIRECTORY_ID> })`.
- The API key must be read from the `WORKOS_API_KEY` environment variable and the directory id from the `WORKOS_DIRECTORY_ID` environment variable. Do NOT hardcode either value.
- Extract the primary email (`emails[].value` where `primary === true`; if no entry is marked primary, use the first email) for each returned directory user.
- Write a JSON array of the email strings (sorted alphabetically, case-insensitive) to `/home/user/myproject/users.json` using UTF-8 encoding and a trailing newline.
- The script must be executable via `node /home/user/myproject/index.js` and must exit with code 0 on success.

## Implementation Guide
1. `cd /home/user/myproject`
2. Create `index.js` that:
   - Imports `WorkOS` from `@workos-inc/node`.
   - Instantiates `const workos = new WorkOS(process.env.WORKOS_API_KEY);`.
   - Calls `await workos.directorySync.listUsers({ directory: process.env.WORKOS_DIRECTORY_ID })`.
   - Maps each returned directory user to its primary email value.
   - Sorts the resulting list of emails alphabetically (case-insensitive).
   - Writes the JSON array to `/home/user/myproject/users.json` followed by a single trailing newline (`\n`).
3. Run `node index.js` from `/home/user/myproject` to produce the output file.

## Constraints
- Project path: /home/user/myproject
- Output file: /home/user/myproject/users.json
- The Node.js entrypoint must be located at /home/user/myproject/index.js.
- You MUST use the real `@workos-inc/node` SDK calling the live WorkOS API. Do NOT stub, mock, or hardcode the API response.
- Required environment variables (already provided to the environment): `WORKOS_API_KEY`, `WORKOS_DIRECTORY_ID`.

## Integrations
- WorkOS (Directory Sync API, `@workos-inc/node` SDK)

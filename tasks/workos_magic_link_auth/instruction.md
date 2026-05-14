# WorkOS Magic Link Authentication API

## Background
Implement a backend API for Magic Link authentication using the WorkOS Node.js SDK and Express.

## Requirements
- Initialize an Express application in `/home/user/app`.
- Implement `POST /api/magic-link`: Accepts `{"email": "..."}` in the JSON body. Uses `workos.userManagement.createMagicAuth` to generate a magic link code. Return the `code` in the JSON response.
- Implement `POST /api/verify`: Accepts `{"email": "...", "code": "..."}` in the JSON body. Uses `workos.userManagement.authenticateWithMagicAuth` to authenticate the user. Return the authenticated user object in the JSON response.
- The server should listen on port 3000.

## Constraints
- Project path: /home/user/app
- Start command: `node index.js`
- Port: 3000
- Read `WORKOS_API_KEY` and `WORKOS_CLIENT_ID` from the environment variables.

## Integrations
- WorkOS
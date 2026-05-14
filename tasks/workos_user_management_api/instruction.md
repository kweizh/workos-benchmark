# WorkOS User Management API

## Background
WorkOS provides APIs to manage users. You need to write a Node.js script to create a user and retrieve their ID.

## Requirements
- Initialize a Node.js project in `/home/user/project` and install `@workos-inc/node`.
- Create a Node.js script named `manage_users.js` in `/home/user/project`.
- Use the `@workos-inc/node` SDK to create a user with a unique email (e.g., using a timestamp) and password `Password123!`.
- Save the created User ID to `/home/user/project/output.txt`.

## Constraints
- Project path: /home/user/project
- Log file: /home/user/project/output.txt
- You must use `WORKOS_API_KEY` and `WORKOS_CLIENT_ID` from the environment variables.

## Integrations
- WorkOS
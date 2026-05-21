# WorkOS Directory Sync: List Users

## Background
WorkOS Directory Sync (SCIM) provides automatic user provisioning and deprovisioning from services like Okta or Azure AD. You need to write a simple script to list all users from a specific directory.

## Requirements
- Create a Node.js script `index.js` in `/home/user/project`.
- Use the `@workos-inc/node` SDK to list users for the directory specified in the `WORKOS_DIRECTORY_ID` environment variable.
- Write the resulting JSON array of users to `/home/user/project/users.json`.
- The script must use the `WORKOS_API_KEY` from the environment.

## Constraints
- Project path: `/home/user/project`
- Output file: `/home/user/project/users.json`
- Do not hardcode the API key or directory ID.
- Run the script to generate the output file.
# WorkOS Admin Portal SSO Intent

## Background
WorkOS provides an Admin Portal, a self-service UI for your customers to configure their own SSO and Directory Sync. You can generate a secure link to this portal using the WorkOS SDK.

## Requirements
- Create a Node.js script `generate_portal_link.js` in `/home/user/project`.
- The script should use the `@workos-inc/node` SDK to generate an Admin Portal link with the intent `sso`.
- The script must take an organization ID as a command-line argument.
- It must read the `WORKOS_API_KEY` from the environment.
- The script should print the generated URL to standard output.
- Initialize the project and install the necessary dependencies.

## Constraints
- Project path: `/home/user/project`
- Script path: `/home/user/project/generate_portal_link.js`
- Do not mock the WorkOS API; use the real SDK.
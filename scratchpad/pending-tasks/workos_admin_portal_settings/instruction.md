# WorkOS Admin Portal Settings

## Background
WorkOS provides an Admin Portal that allows your customers to configure their own enterprise features, such as Single Sign-On (SSO) and Directory Sync. You need to implement a feature that generates a secure link to this Admin Portal for an organization admin.

## Requirements
- Create a Node.js script `generate_portal_link.js` in `/home/user/app`.
- The script should use the WorkOS Node SDK to generate an Admin Portal link for an organization.
- The intent must be for configuring SSO (`sso`).
- The script should print the generated URL to stdout.

## Constraints
- Project path: /home/user/app
- Use the `@workos-inc/node` library.
- Use the `WORKOS_API_KEY` and `WORKOS_CLIENT_ID` environment variables.
- You must use the organization ID `org_01H9X5X5X5X5X5X5X5X5X5X5X5` for the link generation.
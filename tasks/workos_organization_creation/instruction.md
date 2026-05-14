# WorkOS Organization Creation

## Background
Create a new WorkOS organization using the official WorkOS Node.js SDK. This is a common administrative task for provisioning new tenants in a B2B SaaS application.

## Requirements
- Create a Node.js script that creates a new WorkOS organization named 'Acme Corp'.
- The organization must have the domain 'acmecorp.com' associated with it.
- The script must use the `WORKOS_API_KEY` environment variable for authentication.
- The script must write the resulting organization ID to `/home/user/org_id.txt`.

## Constraints
- Project path: /home/user
- Script path: /home/user/create_org.js
- Log file: /home/user/org_id.txt
- A `package.json` is already present at `/home/user` with `@workos-inc/node` installed.

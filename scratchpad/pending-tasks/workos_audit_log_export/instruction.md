# WorkOS Audit Log Export

## Background
You need to implement a script that exports WorkOS Audit Logs for a specific organization and saves them to a local file.

## Requirements
- Use the WorkOS Node.js SDK (`@workos-inc/node`).
- Fetch the audit logs for the organization ID specified in the `WORKOS_ORG_ID` environment variable.
- The script should save the exported logs to `/home/user/app/audit_logs.json`.
- The script should be runnable via `npm start`.

## Constraints
- Project path: `/home/user/app`
- Do not use mock data. Use the real WorkOS API.
- Rely on the `WORKOS_API_KEY` and `WORKOS_CLIENT_ID` environment variables.
# WorkOS Audit Log Recording

## Background
You have a Node.js project. You need to use the `@workos-inc/node` SDK to emit an audit log event for an organization.

## Requirements
- Create a script `record_audit_log.js` in `/home/user/workos-task`.
- The script should use the `@workos-inc/node` SDK to emit an audit log event.
- Read `WORKOS_API_KEY`, `WORKOS_CLIENT_ID`, and `WORKOS_ORGANIZATION_ID` from the environment variables.
- The event must have the action `organization.deleted`.
- The event must have an actor with `id` set to `user_123`, `name` set to `Admin User`, and `type` set to `user`.
- The event must have a target with `id` set to the `WORKOS_ORGANIZATION_ID`, and `type` set to `organization`.
- The script should execute successfully and exit.

## Constraints
- Project path: `/home/user/workos-task`
- Use Node.js and `@workos-inc/node` SDK.

## Integrations
- None
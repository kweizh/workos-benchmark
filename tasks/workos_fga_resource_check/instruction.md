# WorkOS FGA Resource Check

## Background
You need to verify if a specific user has access to a document using WorkOS Fine-Grained Authorization (FGA).

## Requirements
- Create a Node.js script at `/home/user/project/check.js`.
- Initialize the WorkOS client using the `WORKOS_API_KEY` environment variable.
- Use the SDK to check if a subject (type: `user`, id: `user_123`) has the `viewer` relation on a resource (type: `document`, id: `doc_456`).
- Print `true` to the console if authorized, and `false` otherwise.

## Constraints
- Project path: `/home/user/project`
- Use `@workos-inc/node` SDK.
- Do not hardcode the API key.

## Integrations
- WorkOS
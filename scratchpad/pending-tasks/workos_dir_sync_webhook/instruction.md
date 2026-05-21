# WorkOS Directory Sync Webhook Handler

## Background
You need to implement a robust webhook handler for WorkOS Directory Sync. This webhook will receive events from WorkOS when users are created, updated, or deleted in a connected enterprise directory (like Okta or Azure AD), and it must synchronize this state to a local PostgreSQL database.

## Requirements
1. Implement an Express.js server that listens for WorkOS webhooks on `POST /webhooks/workos`.
2. The webhook handler must strictly validate the WorkOS webhook signature using the `WORKOS_WEBHOOK_SECRET` environment variable and `@workos-inc/node` SDK.
3. Handle the following Directory Sync events:
   - `directory_user.created`: Insert the user into the `users` table.
   - `directory_user.updated`: Update the user's details and state (active/suspended) in the `users` table.
   - `directory_user.deleted`: Remove the user from the `users` table.
4. The database is PostgreSQL. A table `users` needs to be managed with fields: `id` (WorkOS user ID), `email`, `first_name`, `last_name`, `state` (active/suspended).
5. The server must return a `200 OK` response upon successful processing.

## Constraints
- Project path: `/home/user/app`
- Start command: `npm start`
- Port: 3000
- Log file: `/home/user/app/webhook.log`
- Use the official `@workos-inc/node` SDK for signature validation.
- Database connection string is available in `DATABASE_URL`.
- The webhook secret is available in `WORKOS_WEBHOOK_SECRET`.
- The WorkOS API key is available in `WORKOS_API_KEY`.

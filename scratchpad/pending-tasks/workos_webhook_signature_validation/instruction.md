# WorkOS Webhook Signature Validation

## Background
WorkOS sends webhooks to your application to notify you of events like directory sync updates or user creation. To ensure these requests are genuinely from WorkOS and haven't been tampered with, you must validate the webhook signature.

## Requirements
- Create an Express.js server that listens for POST requests on `/webhooks`.
- Use the `@workos-inc/node` SDK to validate the webhook signature using `workos.webhooks.constructEvent()`.
- The server should expect the raw body of the request for validation.
- If the signature is valid, respond with HTTP status 200.
- If the signature is invalid, respond with HTTP status 401.

## Constraints
- **Project path**: `/home/user/app`
- **Start command**: `node index.js`
- **Port**: 3000
- **Environment Variables**: The server should read `WORKOS_API_KEY` and `WORKOS_WEBHOOK_SECRET` from the environment.
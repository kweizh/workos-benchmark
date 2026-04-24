Correctly validating webhook signatures for Directory Sync events is a known developer friction point, as it requires raw request body access to prevent verification failures in Node.js environments.

You need to build a webhook listener that securely verifies the WorkOS signature and parses a `directory_user.updated` event to log the user's active status in an Express.js application.

**Constraints:**
- Configure the Express endpoint to bypass standard JSON middleware to preserve the raw request body.
- Use the `workos.webhooks.constructEvent` method to validate the payload against the webhook secret header.
- Safely extract and return the `state` property (e.g., active or suspended) from the validated event object.
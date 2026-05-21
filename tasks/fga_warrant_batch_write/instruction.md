# WorkOS FGA: Batch Write Warrants for Document Access

## Background
WorkOS Fine-Grained Authorization (FGA) provides relationship-based access control through *warrants*: tuples that bind a subject (e.g., a user) to a resource (e.g., a document) via a relation (e.g., `viewer`). The Node.js SDK exposes `workos.fga.batchWriteWarrants(...)` so multiple warrants can be created in a single API call. Your job is to use this batch API to grant a list of three users `viewer` access to a single document resource and persist the SDK response for downstream verification.

A pre-existing Node.js project lives at `/home/user/myproject` with the official `@workos-inc/node` SDK already installed. The WorkOS environment behind `WORKOS_API_KEY` already has the `user` and `document` resource types defined with a `viewer` relation.

## Requirements
- Read the current `trial_id` from `/logs/artifacts/trial_id` and strip whitespace. Use this value as a suffix so every run uses unique resource/subject identifiers.
- Derive identifiers as follows (no other suffixes):
  - Document resource: `resourceType="document"`, `resourceId="doc-batch-${trial_id}"`.
  - User subjects: `resourceType="user"`, `resourceId` values `user-batch-1-${trial_id}`, `user-batch-2-${trial_id}`, `user-batch-3-${trial_id}`.
- Create a single Node.js script at `/home/user/myproject/index.js` that:
  1. Instantiates `new WorkOS(process.env.WORKOS_API_KEY)`.
  2. Calls `workos.fga.batchWriteWarrants([...])` exactly once with three `CREATE` warrants — one for each of the three users granting them the `viewer` relation on the document.
  3. Awaits the call and writes the JSON-serialized response (including the `warrantToken` string) to `/home/user/myproject/warrants.json`. The output JSON must contain a top-level `warrantToken` field.
  4. Logs progress and exits with code `0` on success, non-zero on failure.
- Run the script once with `node index.js` from `/home/user/myproject` so that `warrants.json` is produced.

## Implementation Guide
1. `cd /home/user/myproject`
2. Confirm `@workos-inc/node` is already installed (see `node_modules/@workos-inc/node`). Do not reinstall a different version.
3. Author `index.js` (CommonJS or ES modules — `package.json` already uses CommonJS).
4. The batch call should look roughly like:
   ```js
   const { WorkOS } = require('@workos-inc/node');
   const fs = require('fs');
   const trialId = fs.readFileSync('/logs/artifacts/trial_id', 'utf8').trim();
   const workos = new WorkOS(process.env.WORKOS_API_KEY);
   const documentId = `doc-batch-${trialId}`;
   const userIds = [`user-batch-1-${trialId}`, `user-batch-2-${trialId}`, `user-batch-3-${trialId}`];
   const warrantToken = await workos.fga.batchWriteWarrants(
     userIds.map((uid) => ({
       op: 'CREATE',
       resource: { resourceType: 'document', resourceId: documentId },
       relation: 'viewer',
       subject: { resourceType: 'user', resourceId: uid },
     })),
   );
   fs.writeFileSync('/home/user/myproject/warrants.json', JSON.stringify(warrantToken, null, 2));
   ```
5. Execute the script: `node index.js`.

## Constraints
- Project path: `/home/user/myproject`
- Output file: `/home/user/myproject/warrants.json` (must contain the SDK response with a `warrantToken` string)
- Trial ID source: `/logs/artifacts/trial_id`
- You MUST use the real WorkOS API via the `@workos-inc/node` SDK and the `WORKOS_API_KEY` environment variable. NEVER mock or stub the WorkOS client.
- You MUST call `workos.fga.batchWriteWarrants(...)` exactly once with all three warrants — do not loop over `writeWarrant`.
- Do not delete or modify any existing files outside `/home/user/myproject`.

## Integrations
- WorkOS (Fine-Grained Authorization API)
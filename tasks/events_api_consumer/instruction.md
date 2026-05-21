# WorkOS Events API Consumer with Cursor Pagination

## Background
WorkOS exposes an Events API that lets your backend poll for activity occurring inside WorkOS and connected enterprise identity providers (Directory Sync, SSO, AuthKit, etc.). The API uses cursor-based pagination: every call returns a `list_metadata.after` cursor that should be passed back as the `after` query parameter on the next request in order to fetch the next page of results.

In this task, you will build a small Node.js script that uses the official `@workos-inc/node` SDK to poll the Events API, page through results using the `after` cursor, and persist each event's id and type to a log file.

## Requirements
Implement a Node.js script at `/home/user/myproject/index.js` that, when executed via `node index.js`:

1. Reads the WorkOS API key from the `WORKOS_API_KEY` environment variable and instantiates the SDK as `new WorkOS(process.env.WORKOS_API_KEY)`.
2. Calls `workos.events.listEvents({ events: ['dsync.user.created'], limit: 2 })` to fetch the first page of `dsync.user.created` events. The `limit` MUST be exactly `2` so that the script is forced to paginate through results.
3. Pages through ALL available events using cursor pagination. After each page, the script MUST re-issue the call as `workos.events.listEvents({ events: ['dsync.user.created'], limit: 2, after: <cursor> })`, where `<cursor>` is `list_metadata.after` (in the SDK this is exposed as `listMetadata.after`) from the previous response. Continue until the response contains no more events or `list_metadata.after` is missing/empty.
4. For every event returned (across all pages), append a single line to `/home/user/myproject/events.log` in the exact format `<event_id> <event_type>\n` (the event id, a single ASCII space, the event type, and a trailing newline). The order of lines must follow the order events are returned by the API, page by page. Existing contents of the log file MUST be cleared at the start of every run (the file is overwritten, not appended).
5. The script must exit with status code `0` on success and a non-zero status code on any API failure.
6. The script MUST make at least 2 HTTP calls to the Events API (i.e., the `after` cursor must be used at least once) whenever there are more `dsync.user.created` events than the configured page limit. Hardcoding event ids is not allowed; all data must come from the live API.

## Implementation Guide
1. Create the project directory if needed (it is already present at `/home/user/myproject`).
2. Initialize a Node.js project there: `npm init -y`.
3. Install the WorkOS Node SDK: `npm install @workos-inc/node`.
4. Create `index.js` implementing the loop described in the Requirements section. A typical structure looks like:
   ```javascript
   const { WorkOS } = require('@workos-inc/node');
   const fs = require('fs');

   const LOG_PATH = '/home/user/myproject/events.log';
   const workos = new WorkOS(process.env.WORKOS_API_KEY);

   async function main() {
     fs.writeFileSync(LOG_PATH, '');
     let after;
     while (true) {
       const params = { events: ['dsync.user.created'], limit: 2 };
       if (after) params.after = after;
       const response = await workos.events.listEvents(params);
       for (const evt of response.data) {
         fs.appendFileSync(LOG_PATH, `${evt.id} ${evt.event}\n`);
       }
       const next = response.listMetadata && response.listMetadata.after;
       if (!next || response.data.length === 0) break;
       after = next;
     }
   }

   main().catch((err) => { console.error(err); process.exit(1); });
   ```
5. Run the script once: `node index.js`. This populates `/home/user/myproject/events.log` with one line per fetched event.

## Constraints
- Project path: `/home/user/myproject`
- Log file: `/home/user/myproject/events.log`
- Page limit: exactly `2` per request.
- Use only the real WorkOS Events API via `@workos-inc/node`. Do NOT mock, stub, or fabricate event ids or types. All log lines must come from real API responses produced with the provided `WORKOS_API_KEY`.
- The script must run to completion without manual intervention.

## Integrations
- WorkOS (Events API, requires `WORKOS_API_KEY`).
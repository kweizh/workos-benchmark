# List WorkOS Events via the Events API

## Background
The WorkOS Events API is the pull-based alternative to webhooks. Use `workos.events.listEvents({ events: ['organization.created'] })` to fetch a slice of recent events and persist them.

## Requirements
1. Project at `/home/user/myproject`.
2. Implement `/home/user/myproject/list_events.js` that:
   - Reads `WORKOS_API_KEY` and instantiates the SDK.
   - Calls `workos.events.listEvents({ events: ['organization.created'], limit: 10 })`.
   - Maps each event to `{ id, event, created_at }` (strings) and writes the JSON array to `/home/user/myproject/events.json`.
3. Run `node list_events.js`.

## Constraints
- Real WorkOS API; no mocks.
- Output filter must be exactly `events: ['organization.created']`.

## Integrations
- WorkOS (Events API).

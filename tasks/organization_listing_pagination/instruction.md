# Paginate WorkOS Organizations to JSON

## Background
Use the `@workos-inc/node` SDK to enumerate every WorkOS organization accessible to the API key by paginating with the `listMetadata.after` cursor, and persist the results to a JSON file.

## Requirements
1. The project lives at `/home/user/myproject`.
2. Implement a script at `/home/user/myproject/list_orgs.js` that:
   - Reads `WORKOS_API_KEY` from the process environment.
   - Initializes the WorkOS client.
   - Pages through `workos.organizations.listOrganizations({ limit: 2, after })` using the `listMetadata.after` cursor until no more pages remain.
   - Collects every organization, preserving the iteration order.
   - Writes a pretty-printed JSON array (2-space indent) to `/home/user/myproject/organizations.json` where each element has exactly the keys `id` and `name` (strings).
3. Run the script with `node list_orgs.js`.

## Constraints
- Use the real WorkOS API; do NOT mock.
- Page size MUST be `limit: 2` to exercise pagination.
- The order of the JSON array must follow the SDK iteration order.

## Integrations
- WorkOS (User Management / Organizations API).

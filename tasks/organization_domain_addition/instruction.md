# Add a New Domain to an Existing WorkOS Organization

## Background
WorkOS Organizations are the top-level tenant resource in WorkOS. Each Organization can be associated with one or more domains, which are used for SSO routing, JIT provisioning, and email-based organization matching. In this task you will write a small Node.js script that adds a brand new domain to an existing organization via the WorkOS Node SDK and saves the updated organization object to disk.

## Requirements
1. The project lives at `/home/user/myproject`. It already has `package.json` with the `@workos-inc/node` SDK installed.
2. Implement a script at `/home/user/myproject/add_domain.js` that:
   - Reads `WORKOS_API_KEY`, `WORKOS_ORGANIZATION_ID`, `WORKOS_NEW_DOMAIN`, and `ZEALT_RUN_ID` from the process environment.
   - Initializes the WorkOS client (`const workos = new WorkOS(process.env.WORKOS_API_KEY)`).
   - Fetches the existing organization with `workos.organizations.getOrganization(process.env.WORKOS_ORGANIZATION_ID)`.
   - Constructs the new domain to add: if `ZEALT_RUN_ID` is present, prepend it to `WORKOS_NEW_DOMAIN` (e.g., `${process.env.ZEALT_RUN_ID}.${process.env.WORKOS_NEW_DOMAIN}`). Otherwise, use `WORKOS_NEW_DOMAIN`.
   - Builds a `domainData` array that includes every existing domain on the organization (preserving their current `state`) PLUS a new entry for the constructed domain with `state: 'pending'`. Do NOT add the new domain a second time if it is already present.
   - Calls `workos.organizations.updateOrganization({ organization: process.env.WORKOS_ORGANIZATION_ID, domainData })` to persist the change.
   - Writes the JSON serialization of the returned organization object to `/home/user/myproject/org.json` (pretty-printed with 2-space indentation).
3. Run the script with `node add_domain.js` so that `/home/user/myproject/org.json` exists after the run.

## Implementation Guide
1. `cd /home/user/myproject`
2. Create `add_domain.js` using the WorkOS Node SDK (`@workos-inc/node`) as described above.
3. Execute `node add_domain.js`.
4. Confirm `/home/user/myproject/org.json` contains the updated organization object with the new domain.

## Constraints
- Project path: `/home/user/myproject`
- Output file: `/home/user/myproject/org.json`
- Use the real WorkOS API. Do NOT mock the SDK or HTTP layer.
- Use the SDK's `domainData` field (the legacy `domains: string[]` parameter is deprecated).
- The script must be idempotent: re-running it with the same `WORKOS_NEW_DOMAIN` must not produce duplicate domain entries.

## Integrations
- WorkOS (real API key, real organization id, real new domain provided via env vars).
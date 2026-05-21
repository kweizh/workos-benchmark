# Create a WorkOS User with Email + Password

## Background
Use User Management to create a new WorkOS user account with email and password credentials. The email is derived from `ZEALT_RUN_ID` so each run creates a distinct user.

## Requirements
1. Project at `/home/user/myproject`.
2. Implement `/home/user/myproject/create_user.js` that:
   - Reads `WORKOS_API_KEY` and `ZEALT_RUN_ID`.
   - Derives the user email as `pochi-user-${(process.env.ZEALT_RUN_ID || 'default').toLowerCase()}@pochi-benchmark.example`.
   - Uses a fixed strong password literal `PochiBenchmark!2025`.
   - Calls `workos.userManagement.createUser({ email, password, firstName: 'Pochi', lastName: 'Benchmark' })`. If WorkOS returns an `email already exists` error, fall back to `workos.userManagement.listUsers({ email })` and read the first match so the script is idempotent.
   - Writes the resulting user as JSON to `/home/user/myproject/user.json`.
3. Run `node create_user.js`.

## Constraints
- Real WorkOS API; no mocks.
- `id` field must match `^user_`.

## Integrations
- WorkOS (User Management API).

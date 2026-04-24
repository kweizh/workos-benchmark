WorkOS FGA provides Relationship-based access control (ReBAC) for granular, resource-level permissions, which is highly useful for systems like document sharing hierarchies with varying roles.

You need to write an authorization function that verifies if a specific organization member holds the 'edit' permission for a document resource in a Node.js backend.

**Constraints:**
- Use the `workos.authorization.check` method.
- Require and supply `organizationMembershipId`, `permissionSlug` (set to `document:edit`), `resourceId`, and `resourceTypeSlug` (set to `document`).
- The function must cleanly return a boolean value indicating whether the authorization check passed.
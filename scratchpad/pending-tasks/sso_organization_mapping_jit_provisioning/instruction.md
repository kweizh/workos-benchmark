Multi-tenant applications often map WorkOS organizations to internal user models, which requires Just-in-Time (JIT) provisioning logic during the SSO login flow.

You need to create a Node.js function that accepts an SSO authorization code, retrieves the user's profile, and matches the user to an organization based on their email domain in a generic backend environment.

**Constraints:**
- Use the `@workos-inc/node` SDK and the `workos.sso.getProfileAndToken` method.
- Extract the email domain from the retrieved profile.
- Do NOT execute actual database queries; mock the domain-to-organization mapping logic via a static dictionary object.
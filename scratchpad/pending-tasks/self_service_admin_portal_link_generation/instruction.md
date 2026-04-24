WorkOS provides an Admin Portal that acts as a self-service UI for customers to configure their own enterprise SSO and Directory Sync connections. Providing a secure entry point to this portal is crucial for B2B SaaS applications.

You need to implement an API handler that generates and returns a secure WorkOS Admin Portal URL with the intent to configure SSO in an Express.js environment.

**Constraints:**
- Use the `workos.portal.generateLink` method.
- Accept an `organization` ID via request parameters and explicitly set the `intent` argument to `'sso'`.
- Return the generated URL string inside a JSON response with a 200 HTTP status code.
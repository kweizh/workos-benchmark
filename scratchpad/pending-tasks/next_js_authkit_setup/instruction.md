WorkOS AuthKit provides a hosted, customizable authentication UI that abstracts the complexity of building login flows. Modern Next.js applications utilize the App Router to handle seamless authentication callbacks.

You need to implement the authentication callback route handling sign-in and sign-out logic in a Next.js App Router environment.

**Constraints:**
- Use the `@workos-inc/authkit-nextjs` package.
- Implement the logic within a standard App Router API directory structure (e.g., `app/api/auth/[...workos]/route.ts`).
- The route handler must successfully process the WorkOS callback code and return a valid session response.
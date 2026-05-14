# WorkOS AuthKit Sign In

## Background
WorkOS AuthKit provides a hosted, customizable authentication UI that supports email/password, magic links, and SSO. You need to implement a complete sign-in flow in a Next.js application using the WorkOS AuthKit.

## Requirements
- Initialize a Next.js application in `/home/user/app`.
- Install the necessary WorkOS SDK for Next.js (`@workos-inc/authkit-nextjs`).
- Configure AuthKit using `WORKOS_API_KEY` and `WORKOS_CLIENT_ID` from the environment.
- Create a protected route at `/dashboard` that requires authentication. If the user is not authenticated, they should be redirected to the WorkOS AuthKit sign-in page.
- The application must be able to start on port 3000.

## Constraints
- Project path: `/home/user/app`
- Start command: `npm run build && npm start`
- Port: `3000`
- Use real WorkOS API keys (`WORKOS_API_KEY`, `WORKOS_CLIENT_ID`) from the environment.

## Integrations
- WorkOS
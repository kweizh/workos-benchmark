# WorkOS AuthKit Sign Out

## Background
You have a Next.js application using WorkOS AuthKit for authentication. The sign-in flow is working, but the sign-out button on the homepage is currently non-functional.

## Requirements
- Update `src/app/page.tsx` to implement the sign-out functionality using `@workos-inc/authkit-nextjs`.
- The sign-out button is already wrapped in a `<form>`. You need to add a server action to this form that calls the `signOut()` function from AuthKit.
- Ensure the user is signed out when the button is clicked.

## Constraints
- Project path: `/home/user/app`
- Do NOT change the visual appearance or text of the button.
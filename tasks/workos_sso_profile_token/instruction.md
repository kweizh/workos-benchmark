# WorkOS SSO Profile Token

## Background
Integrate Single Sign-On (SSO) using WorkOS to fetch a user profile and access token.

## Requirements
- Create a Node.js script `index.js` that uses the `@workos-inc/node` SDK.
- The script should have a function `getSSOProfileAndToken(code)` that takes an authorization code.
- Inside the function, call the WorkOS API to get the profile and token using the provided code and the `WORKOS_CLIENT_ID` environment variable.
- The function must return the resulting profile and token object.

## Constraints
- Project path: /home/user/app
- Do not mock the WorkOS API. Use the real WorkOS API by relying on the `WORKOS_API_KEY` and `WORKOS_CLIENT_ID` environment variables.

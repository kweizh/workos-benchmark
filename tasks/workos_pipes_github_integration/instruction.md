# WorkOS Pipes GitHub Integration

## Background
WorkOS Pipes allows your users to securely connect their third-party accounts to your application without managing OAuth flows. In this task, you need to use the WorkOS Node.js SDK to fetch a GitHub access token for a connected user and then use that token to fetch their GitHub repositories.

## Requirements
- Initialize a Node.js project in `/home/user/myproject`.
- Install `@workos-inc/node`.
- Write a script `fetch_repos.js` that uses the `WORKOS_API_KEY` and `WORKOS_CLIENT_ID` from the environment.
- Use `workos.pipes.getAccessToken` to fetch an access token for `provider: 'github'` and the `userId` provided in `/home/user/myproject/user_id.txt`.
- Use the obtained access token to make a request to the GitHub API (`https://api.github.com/user/repos`) to fetch the user's repositories.
- Save the repository names as a JSON array of strings to `/home/user/myproject/repos.json`.

## Constraints
- Project path: /home/user/myproject
- Log file: /home/user/myproject/repos.json

## Integrations
- GitHub
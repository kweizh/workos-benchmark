# WorkOS Pipes Slack Integration

## Background
You need to implement a Node.js script that uses WorkOS Pipes to retrieve a user's Slack access token and post a message to a Slack channel on their behalf.

## Requirements
- Create a script `send_slack_message.js` that takes three command-line arguments: `userId`, `channelName`, and `message`.
- Use the `@workos-inc/node` SDK to fetch the access token for the `slack` provider using WorkOS Pipes.
- Use the retrieved access token to post the `message` to the specified `channelName` using the Slack API (`https://slack.com/api/chat.postMessage`).
- Print `Success` to stdout if the message is posted successfully.
- Handle errors gracefully and print `Error: <error message>` to stdout if anything fails (e.g., token not found, Slack API error).

## Implementation Guide
1. Initialize a Node.js project in `/home/user/myproject` and install `@workos-inc/node` and `axios` (or use `fetch`).
2. Create `send_slack_message.js`.
3. Initialize the WorkOS client using the `WORKOS_API_KEY` environment variable.
4. Call `workos.pipes.getAccessToken({ provider: 'slack', userId })`.
5. Extract the Slack access token from the response.
6. Make a POST request to `https://slack.com/api/chat.postMessage` with the token in the `Authorization` header and the channel and text in the body.

## Constraints
- Project path: `/home/user/myproject`
- Log file: `/home/user/myproject/output.log`
- You MUST read the `trial_id` from `/logs/trial_id` and convert it to lowercase.
- When the script is called, the channel name will be provided as an argument. However, if the script is creating a channel (not required here, just posting), ensure you use the exact channel name provided.

## Integrations
- Slack
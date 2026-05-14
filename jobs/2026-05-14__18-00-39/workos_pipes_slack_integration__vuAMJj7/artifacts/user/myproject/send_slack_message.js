// Trial ID: workos_pipes_slack_integration__vuamjj7
const { WorkOS } = require('@workos-inc/node');
const axios = require('axios');

async function sendSlackMessage() {
  const [userId, channelName, message] = process.argv.slice(2);

  if (!userId || !channelName || !message) {
    console.log('Error: Missing arguments. Usage: node send_slack_message.js <userId> <channelName> <message>');
    return;
  }

  const apiKey = process.env.WORKOS_API_KEY;
  if (!apiKey) {
    console.log('Error: WORKOS_API_KEY environment variable is not set');
    return;
  }

  const workos = new WorkOS(apiKey);

  try {
    const { accessToken } = await workos.pipes.getAccessToken({
      provider: 'slack',
      userId,
    });

    if (!accessToken) {
      console.log('Error: Slack access token not found');
      return;
    }

    const response = await axios.post(
      'https://slack.com/api/chat.postMessage',
      {
        channel: channelName,
        text: message,
      },
      {
        headers: {
          Authorization: `Bearer ${accessToken}`,
          'Content-Type': 'application/json',
        },
      }
    );

    if (response.data.ok) {
      console.log('Success');
    } else {
      console.log(`Error: ${response.data.error}`);
    }
  } catch (error) {
    console.log(`Error: ${error.message}`);
  }
}

sendSlackMessage();

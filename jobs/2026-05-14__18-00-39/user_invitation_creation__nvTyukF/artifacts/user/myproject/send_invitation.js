const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');
const path = require('path');

async function sendInvitation() {
  const apiKey = process.env.WORKOS_API_KEY;
  const organizationId = process.env.WORKOS_ORGANIZATION_ID;
  const email = process.env.WORKOS_INVITE_EMAIL;

  if (!apiKey || !organizationId || !email) {
    console.error('Missing required environment variables: WORKOS_API_KEY, WORKOS_ORGANIZATION_ID, or WORKOS_INVITE_EMAIL');
    process.exit(1);
  }

  const workos = new WorkOS(apiKey);

  try {
    const invitation = await workos.userManagement.sendInvitation({
      email,
      organizationId,
    });

    const outputData = {
      id: invitation.id,
      token: invitation.token,
    };

    const outputPath = path.join(__dirname, 'invitation.json');
    fs.writeFileSync(outputPath, JSON.stringify(outputData, null, 2));
    console.log(`Invitation sent and recorded to ${outputPath}`);
  } catch (error) {
    console.error('Error sending invitation:', error);
    process.exit(1);
  }
}

sendInvitation();

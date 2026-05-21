const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');

// Initialize the WorkOS client with the API key from environment variable
const workos = new WorkOS(process.env.WORKOS_API_KEY);

async function sendInvitation() {
  try {
    // Construct the recipient email using ZEALT_RUN_ID
    const email = `test-${process.env.ZEALT_RUN_ID}@example.com`;
    const organizationId = process.env.WORKOS_ORGANIZATION_ID;

    console.log(`Sending invitation to ${email} for organization ${organizationId}...`);

    // Send the invitation using the WorkOS SDK
    const invitation = await workos.userManagement.sendInvitation({
      email: email,
      organizationId: organizationId,
    });

    console.log('Invitation sent successfully!');
    console.log(`Invitation ID: ${invitation.id}`);

    // Write the invitation id and token to invitation.json
    const invitationData = {
      id: invitation.id,
      token: invitation.token,
    };

    fs.writeFileSync(
      '/home/user/myproject/invitation.json',
      JSON.stringify(invitationData, null, 2),
      'utf8'
    );

    console.log('Invitation data written to invitation.json');
  } catch (error) {
    console.error('Error sending invitation:', error);
    process.exit(1);
  }
}

sendInvitation();
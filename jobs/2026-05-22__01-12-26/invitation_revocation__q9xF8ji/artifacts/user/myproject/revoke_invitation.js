const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');
const path = require('path');

// Initialize WorkOS with API key
const workos = new WorkOS(process.env.WORKOS_API_KEY);

// Derive the invitee email from ZEALT_RUN_ID
const runId = (process.env.ZEALT_RUN_ID || 'default').toLowerCase();
const email = `pochi-invite-${runId}@pochi-benchmark.example`;
const organizationId = process.env.WORKOS_ORGANIZATION_ID;

async function sendAndRevokeInvitation() {
  console.log(`Using email: ${email}`);
  console.log(`Using organization ID: ${organizationId}`);

  let invitation;

  try {
    // Try to send the invitation
    console.log('Attempting to send invitation...');
    invitation = await workos.userManagement.sendInvitation({
      email,
      organizationId,
    });
    console.log('Invitation sent successfully:', invitation.id);
  } catch (error) {
    // If the invitation already exists, look it up
    if (error.message && error.message.includes('Invitation already exists')) {
      console.log('Invitation already exists, looking it up...');
      const invitations = await workos.userManagement.listInvitations({
        email,
        organizationId,
      });
      
      if (invitations.data && invitations.data.length > 0) {
        invitation = invitations.data[0];
        console.log('Found existing invitation:', invitation.id);
      } else {
        throw new Error('No existing invitation found despite error message');
      }
    } else {
      throw error;
    }
  }

  // Revoke the invitation
  console.log('Revoking invitation...');
  const revokedInvitation = await workos.userManagement.revokeInvitation(invitation.id);
  console.log('Invitation revoked successfully:', revokedInvitation.id);

  // Write the revoked invitation to JSON file
  const outputPath = path.join(__dirname, 'invitation.json');
  fs.writeFileSync(outputPath, JSON.stringify(revokedInvitation, null, 2));
  console.log(`Revoked invitation written to ${outputPath}`);

  return revokedInvitation;
}

// Run the function
sendAndRevokeInvitation()
  .then((result) => {
    console.log('Script completed successfully');
    process.exit(0);
  })
  .catch((error) => {
    console.error('Error:', error);
    process.exit(1);
  });
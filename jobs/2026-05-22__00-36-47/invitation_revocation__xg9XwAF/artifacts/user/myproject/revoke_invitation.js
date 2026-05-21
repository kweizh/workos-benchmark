const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');
const path = require('path');

async function run() {
  const apiKey = process.env.WORKOS_API_KEY;
  const organizationId = process.env.WORKOS_ORGANIZATION_ID;
  const runId = process.env.ZEALT_RUN_ID || 'default';

  if (!apiKey || !organizationId) {
    console.error('Missing WORKOS_API_KEY or WORKOS_ORGANIZATION_ID');
    process.exit(1);
  }

  const workos = new WorkOS(apiKey);
  const email = `pochi-invite-${runId.toLowerCase()}@pochi-benchmark.example`;

  console.log(`Target email: ${email}`);

  let invitation;

  try {
    console.log('Sending invitation...');
    invitation = await workos.userManagement.sendInvitation({
      email,
      organizationId,
    });
    console.log(`Invitation sent: ${invitation.id}`);
  } catch (error) {
    // Check if invitation already exists
    if (error.code === 'invitation_already_exists' || (error.message && error.message.includes('already exists'))) {
      console.log('Invitation already exists, fetching existing invitation...');
      const invitations = await workos.userManagement.listInvitations({
        email,
        organizationId,
      });
      invitation = invitations.data.find(inv => inv.email === email && inv.state === 'pending');
      if (!invitation) {
        throw new Error(`Could not find pending invitation for ${email}`);
      }
      console.log(`Found existing invitation: ${invitation.id}`);
    } else {
      throw error;
    }
  }

  console.log(`Revoking invitation: ${invitation.id}`);
  const revokedInvitation = await workos.userManagement.revokeInvitation(invitation.id);
  console.log('Invitation revoked successfully.');

  const outputPath = path.join(__dirname, 'invitation.json');
  fs.writeFileSync(outputPath, JSON.stringify(revokedInvitation, null, 2));
  console.log(`Revoked invitation object written to ${outputPath}`);
}

run().catch((error) => {
  console.error('Error:', error);
  process.exit(1);
});

'use strict';

const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');
const path = require('path');

async function main() {
  const apiKey = process.env.WORKOS_API_KEY;
  const organizationId = process.env.WORKOS_ORGANIZATION_ID;
  const runId = process.env.ZEALT_RUN_ID || 'default';

  if (!apiKey) throw new Error('Missing WORKOS_API_KEY');
  if (!organizationId) throw new Error('Missing WORKOS_ORGANIZATION_ID');

  const workos = new WorkOS(apiKey);

  const email = `pochi-invite-${runId.toLowerCase()}@pochi-benchmark.example`;
  console.log(`Invitee email: ${email}`);

  let invitation;

  // Try to send a new invitation; if one already exists, look it up instead.
  try {
    invitation = await workos.userManagement.sendInvitation({
      email,
      organizationId,
    });
    console.log(`Invitation sent. ID: ${invitation.id}`);
  } catch (err) {
    const msg = err?.message || '';
    // WorkOS returns an error when an invitation already exists for this email.
    if (msg.toLowerCase().includes('already') || msg.toLowerCase().includes('exist') || err?.code === 'invitation_already_exists') {
      console.log('Invitation already exists, looking it up...');
      const list = await workos.userManagement.listInvitations({ email, organizationId });
      invitation = list.data[0];
      if (!invitation) {
        throw new Error(`Could not find existing invitation for ${email}`);
      }
      console.log(`Found existing invitation. ID: ${invitation.id}`);
    } else {
      throw err;
    }
  }

  // Revoke the invitation.
  const revoked = await workos.userManagement.revokeInvitation(invitation.id);
  console.log(`Invitation revoked. State: ${revoked.state}`);

  // Write the revoked invitation object to disk.
  const outputPath = path.join(__dirname, 'invitation.json');
  fs.writeFileSync(outputPath, JSON.stringify(revoked, null, 2));
  console.log(`Written to ${outputPath}`);
}

main().catch((err) => {
  console.error('Error:', err);
  process.exit(1);
});

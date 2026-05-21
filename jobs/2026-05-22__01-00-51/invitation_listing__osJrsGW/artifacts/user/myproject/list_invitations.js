const fs = require('fs');
const path = require('path');
const { WorkOS } = require('@workos-inc/node');

const workosApiKey = process.env.WORKOS_API_KEY;
const organizationId = process.env.WORKOS_ORGANIZATION_ID;

if (!workosApiKey) {
  console.error('Missing required environment variable: WORKOS_API_KEY');
  process.exit(1);
}

if (!organizationId) {
  console.error('Missing required environment variable: WORKOS_ORGANIZATION_ID');
  process.exit(1);
}

const workos = new WorkOS(workosApiKey);

async function listInvitations() {
  const invitations = [];
  let after;

  do {
    const response = await workos.userManagement.listInvitations({
      organizationId,
      limit: 2,
      after,
    });

    for (const invitation of response.data) {
      invitations.push({
        id: String(invitation.id),
        email: String(invitation.email),
        state: String(invitation.state),
        organization_id: String(invitation.organization_id),
      });
    }

    after = response.listMetadata.after;
  } while (after);

  const outputPath = path.join(__dirname, 'invitations.json');
  fs.writeFileSync(outputPath, JSON.stringify(invitations, null, 2));

  console.log(`Wrote ${invitations.length} invitations to ${outputPath}`);
}

listInvitations().catch((error) => {
  console.error('Failed to list invitations:', error);
  process.exit(1);
});

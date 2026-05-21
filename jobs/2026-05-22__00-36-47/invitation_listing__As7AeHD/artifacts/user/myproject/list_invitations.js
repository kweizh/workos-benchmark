const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');
const path = require('path');

const workos = new WorkOS(process.env.WORKOS_API_KEY);
const organizationId = process.env.WORKOS_ORGANIZATION_ID;

async function listInvitations() {
  let invitations = [];
  let after = undefined;

  try {
    do {
      const response = await workos.userManagement.listInvitations({
        organizationId: organizationId,
        limit: 2,
        after: after,
      });

      const pageInvitations = response.data.map(inv => ({
        id: inv.id,
        email: inv.email,
        state: inv.state,
        organization_id: inv.organizationId,
      }));

      invitations.push(...pageInvitations);
      after = response.listMetadata.after;

    } while (after);

    fs.writeFileSync(
      path.join(__dirname, 'invitations.json'),
      JSON.stringify(invitations, null, 2)
    );

    console.log(`Successfully wrote ${invitations.length} invitations to invitations.json`);
  } catch (error) {
    console.error('Error listing invitations:', error);
    process.exit(1);
  }
}

listInvitations();

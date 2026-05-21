const { WorkOS } = require('@workos-inc/node');

// Initialize WorkOS client
const workos = new WorkOS(process.env.WORKOS_API_KEY);

async function listInvitations() {
  const invitations = [];
  let cursor = null;
  let hasMore = true;

  while (hasMore) {
    const response = await workos.userManagement.listInvitations({
      organizationId: process.env.WORKOS_ORGANIZATION_ID,
      limit: 2,
      after: cursor,
    });

    // Extract relevant fields from each invitation
    for (const invitation of response.data) {
      invitations.push({
        id: invitation.id,
        email: invitation.email,
        state: invitation.state,
        organization_id: invitation.organizationId,
      });
    }

    // Check if there are more pages
    hasMore = response.listMetadata.hasMore;
    cursor = response.listMetadata.endCursor;
  }

  // Write results to JSON file
  const fs = require('fs');
  fs.writeFileSync(
    '/home/user/myproject/invitations.json',
    JSON.stringify(invitations, null, 2)
  );

  console.log(`Successfully wrote ${invitations.length} invitations to invitations.json`);
}

listInvitations().catch(console.error);
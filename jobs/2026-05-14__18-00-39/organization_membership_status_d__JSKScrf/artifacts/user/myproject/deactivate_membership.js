const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');
const path = require('path');

async function deactivateMembership() {
  const apiKey = process.env.WORKOS_API_KEY;
  const membershipId = process.env.WORKOS_ORG_MEMBERSHIP_ID;

  if (!apiKey || !membershipId) {
    console.error('Missing WORKOS_API_KEY or WORKOS_ORG_MEMBERSHIP_ID environment variables');
    process.exit(1);
  }

  const workos = new WorkOS(apiKey);

  try {
    const membership = await workos.userManagement.deactivateOrganizationMembership(membershipId);
    
    fs.writeFileSync(
      path.join(__dirname, 'membership.json'),
      JSON.stringify(membership, null, 2)
    );
    
    console.log('Membership deactivated successfully');
  } catch (error) {
    console.error('Error deactivating membership:', error);
    process.exit(1);
  }
}

deactivateMembership();

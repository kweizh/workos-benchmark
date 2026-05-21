const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');

// Read environment variables
const apiKey = process.env.WORKOS_API_KEY;
const orgMembershipId = process.env.WORKOS_ORG_MEMBERSHIP_ID;

// Validate environment variables
if (!apiKey) {
  throw new Error('WORKOS_API_KEY environment variable is required');
}
if (!orgMembershipId) {
  throw new Error('WORKOS_ORG_MEMBERSHIP_ID environment variable is required');
}

// Initialize WorkOS client
const workos = new WorkOS(apiKey);

// Deactivate the organization membership
async function deactivateMembership() {
  try {
    console.log(`Deactivating organization membership: ${orgMembershipId}`);
    const membership = await workos.userManagement.deactivateOrganizationMembership(orgMembershipId);
    console.log('Successfully deactivated membership');
    
    // Write the membership object to JSON file with 2-space indentation
    fs.writeFileSync(
      '/home/user/myproject/membership.json',
      JSON.stringify(membership, null, 2),
      'utf-8'
    );
    
    console.log('Membership saved to /home/user/myproject/membership.json');
    console.log(`Membership status: ${membership.status}`);
  } catch (error) {
    console.error('Error deactivating membership:', error);
    throw error;
  }
}

deactivateMembership();
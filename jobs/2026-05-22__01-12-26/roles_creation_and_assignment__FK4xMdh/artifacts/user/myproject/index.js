const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');

async function main() {
  try {
    // Read environment variables
    const apiKey = process.env.WORKOS_API_KEY;
    const organizationMembershipId = process.env.WORKOS_ORG_MEMBERSHIP_ID;

    // Validate required environment variables
    if (!apiKey) {
      console.error('Error: WORKOS_API_KEY environment variable is not set');
      process.exit(1);
    }

    if (!organizationMembershipId) {
      console.error('Error: WORKOS_ORG_MEMBERSHIP_ID environment variable is not set');
      process.exit(1);
    }

    // Instantiate WorkOS client
    const workos = new WorkOS(apiKey);

    console.log(`Updating organization membership ${organizationMembershipId} to admin role...`);

    // Update the organization membership to admin role
    const membership = await workos.userManagement.updateOrganizationMembership(
      organizationMembershipId,
      { roleSlug: 'admin' }
    );

    console.log('Successfully updated membership role to admin');

    // Write the full membership object to result.json
    const resultPath = '/home/user/myproject/result.json';
    fs.writeFileSync(resultPath, JSON.stringify(membership, null, 2), 'utf-8');

    console.log(`Membership details written to ${resultPath}`);
    console.log(`Role slug: ${membership.role.slug}`);

    // Exit with success
    process.exit(0);
  } catch (error) {
    console.error('Error updating organization membership:', error.message);
    process.exit(1);
  }
}

// Run the script
main();
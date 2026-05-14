const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');
const path = require('path');

async function main() {
  const apiKey = process.env.WORKOS_API_KEY;
  const organizationMembershipId = process.env.WORKOS_ORG_MEMBERSHIP_ID;

  if (!apiKey || !organizationMembershipId) {
    console.error('Missing WORKOS_API_KEY or WORKOS_ORG_MEMBERSHIP_ID environment variables');
    process.exit(1);
  }

  const workos = new WorkOS(apiKey);

  try {
    const membership = await workos.userManagement.updateOrganizationMembership(
      organizationMembershipId,
      { roleSlug: 'admin' }
    );

    const resultPath = path.join(__dirname, 'result.json');
    fs.writeFileSync(resultPath, JSON.stringify(membership, null, 2), 'utf8');

    console.log('Successfully updated organization membership and wrote result to result.json');
    process.exit(0);
  } catch (error) {
    console.error('Error updating organization membership:', error);
    process.exit(1);
  }
}

main();

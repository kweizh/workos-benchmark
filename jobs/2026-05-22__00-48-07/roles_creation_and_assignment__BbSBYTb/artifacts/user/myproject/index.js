'use strict';

const fs = require('fs');
const { WorkOS } = require('@workos-inc/node');

async function main() {
  const apiKey = process.env.WORKOS_API_KEY;
  if (!apiKey) {
    console.error('Error: WORKOS_API_KEY environment variable is not set.');
    process.exit(1);
  }

  const organizationMembershipId = process.env.WORKOS_ORG_MEMBERSHIP_ID;
  if (!organizationMembershipId) {
    console.error('Error: WORKOS_ORG_MEMBERSHIP_ID environment variable is not set.');
    process.exit(1);
  }

  const workos = new WorkOS(apiKey);

  const membership = await workos.userManagement.updateOrganizationMembership(
    organizationMembershipId,
    { roleSlug: 'admin' }
  );

  const outputPath = '/home/user/myproject/result.json';
  fs.writeFileSync(outputPath, JSON.stringify(membership, null, 2), 'utf-8');

  console.log(`Membership updated successfully. Result written to ${outputPath}`);
  console.log(`Role slug: ${membership.role?.slug}`);
}

main().catch((err) => {
  console.error('Error updating organization membership:', err.message ?? err);
  process.exit(1);
});

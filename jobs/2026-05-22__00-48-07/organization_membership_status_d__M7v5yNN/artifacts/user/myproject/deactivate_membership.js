'use strict';

const fs = require('fs');
const path = require('path');
const { WorkOS } = require('@workos-inc/node');

const apiKey = process.env.WORKOS_API_KEY;
const membershipId = process.env.WORKOS_ORG_MEMBERSHIP_ID;

if (!apiKey) {
  console.error('Error: WORKOS_API_KEY environment variable is not set.');
  process.exit(1);
}

if (!membershipId) {
  console.error('Error: WORKOS_ORG_MEMBERSHIP_ID environment variable is not set.');
  process.exit(1);
}

const workos = new WorkOS(apiKey);

(async () => {
  const membership = await workos.userManagement.deactivateOrganizationMembership(membershipId);

  const outputPath = path.join(__dirname, 'membership.json');
  fs.writeFileSync(outputPath, JSON.stringify(membership, null, 2));

  console.log(`Membership deactivated. Status: ${membership.status}`);
  console.log(`Result written to ${outputPath}`);
})();

'use strict';

const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');
const path = require('path');

const apiKey = process.env.WORKOS_API_KEY;
const organizationId = process.env.WORKOS_ORGANIZATION_ID;

if (!apiKey) {
  console.error('Error: WORKOS_API_KEY environment variable is not set.');
  process.exit(1);
}

if (!organizationId) {
  console.error('Error: WORKOS_ORGANIZATION_ID environment variable is not set.');
  process.exit(1);
}

const workos = new WorkOS(apiKey);

async function listAllMemberships() {
  const memberships = [];
  let after = undefined;
  let page = 1;

  console.log(`Fetching memberships for organization: ${organizationId}`);

  while (true) {
    console.log(`  Fetching page ${page}${after ? ` (after: ${after})` : ''}...`);

    const response = await workos.userManagement.listOrganizationMemberships({
      organizationId,
      limit: 2,
      ...(after ? { after } : {}),
    });

    for (const membership of response.data) {
      memberships.push({
        id: membership.id,
        user_id: membership.userId,
        organization_id: membership.organizationId,
        status: membership.status,
      });
    }

    console.log(`  Got ${response.data.length} membership(s) on page ${page}.`);

    if (response.listMetadata && response.listMetadata.after) {
      after = response.listMetadata.after;
      page++;
    } else {
      break;
    }
  }

  return memberships;
}

(async () => {
  try {
    const memberships = await listAllMemberships();

    const outputPath = path.join(__dirname, 'memberships.json');
    fs.writeFileSync(outputPath, JSON.stringify(memberships, null, 2));

    console.log(`\nDone. ${memberships.length} membership(s) written to ${outputPath}`);
  } catch (err) {
    console.error('Error fetching memberships:', err.message || err);
    process.exit(1);
  }
})();

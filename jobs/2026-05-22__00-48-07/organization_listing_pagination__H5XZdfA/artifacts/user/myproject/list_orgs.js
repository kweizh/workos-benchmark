'use strict';

const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');
const path = require('path');

async function main() {
  const apiKey = process.env.WORKOS_API_KEY;
  if (!apiKey) {
    console.error('Error: WORKOS_API_KEY environment variable is not set.');
    process.exit(1);
  }

  const workos = new WorkOS(apiKey);

  const allOrgs = [];
  let after = undefined;

  do {
    const response = await workos.organizations.listOrganizations({
      limit: 2,
      after,
    });

    for (const org of response.data) {
      allOrgs.push({ id: org.id, name: org.name });
    }

    after = response.listMetadata.after;
  } while (after);

  const outputPath = path.join(__dirname, 'organizations.json');
  fs.writeFileSync(outputPath, JSON.stringify(allOrgs, null, 2));

  console.log(`Wrote ${allOrgs.length} organization(s) to ${outputPath}`);
}

main().catch((err) => {
  console.error('Fatal error:', err);
  process.exit(1);
});

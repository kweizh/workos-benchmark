const fs = require('fs');
const path = require('path');
const { WorkOS } = require('@workos-inc/node');

const apiKey = process.env.WORKOS_API_KEY;

if (!apiKey) {
  console.error('WORKOS_API_KEY is required');
  process.exit(1);
}

const workos = new WorkOS(apiKey);

async function listOrganizations() {
  const organizations = [];
  let after;

  do {
    const response = await workos.organizations.listOrganizations({
      limit: 2,
      after,
    });

    for (const organization of response.data) {
      organizations.push({
        id: organization.id,
        name: organization.name,
      });
    }

    after = response.listMetadata.after;
  } while (after);

  const outputPath = path.join(__dirname, 'organizations.json');
  fs.writeFileSync(outputPath, JSON.stringify(organizations, null, 2));
}

listOrganizations().catch((error) => {
  console.error(error);
  process.exit(1);
});

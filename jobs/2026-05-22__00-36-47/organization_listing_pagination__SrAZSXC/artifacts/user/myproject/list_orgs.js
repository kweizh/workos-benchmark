const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');
const path = require('path');

const apiKey = process.env.WORKOS_API_KEY;
if (!apiKey) {
  console.error('WORKOS_API_KEY is not set');
  process.exit(1);
}

const workos = new WorkOS(apiKey);

async function listAllOrganizations() {
  let allOrgs = [];
  let after = undefined;

  try {
    do {
      const response = await workos.organizations.listOrganizations({
        limit: 2,
        after: after,
      });

      const { data, listMetadata } = response;
      
      data.forEach(org => {
        allOrgs.push({
          id: org.id,
          name: org.name,
        });
      });

      after = listMetadata.after;
    } while (after);

    const outputPath = path.join(__dirname, 'organizations.json');
    fs.writeFileSync(outputPath, JSON.stringify(allOrgs, null, 2));
    console.log(`Successfully wrote ${allOrgs.length} organizations to organizations.json`);
  } catch (error) {
    console.error('Error listing organizations:', error);
    process.exit(1);
  }
}

listAllOrganizations();

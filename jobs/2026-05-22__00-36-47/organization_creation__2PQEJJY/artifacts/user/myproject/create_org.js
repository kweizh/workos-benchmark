const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');
const path = require('path');

async function run() {
  const apiKey = process.env.WORKOS_API_KEY;
  const runId = process.env.ZEALT_RUN_ID || 'default';
  
  if (!apiKey) {
    console.error('WORKOS_API_KEY is required');
    process.exit(1);
  }

  const workos = new WorkOS(apiKey);
  const name = `pochi-benchmark-org-${runId}`;

  let organization;

  try {
    organization = await workos.organizations.createOrganization({ name });
    console.log(`Created organization: ${organization.id}`);
  } catch (error) {
    console.log(`Creation call failed or rejected. Attempting to find organization by name: ${name}`);
    
    // Fallback: list organizations and filter by name
    let after = undefined;
    while (!organization) {
      const response = await workos.organizations.listOrganizations({ after });
      organization = response.data.find(org => org.name === name);
      
      if (organization) break;
      if (!response.listMetadata.after) break;
      after = response.listMetadata.after;
    }

    if (!organization) {
      console.error(`Failed to create or find organization with name: ${name}`);
      console.error('Original error:', error);
      process.exit(1);
    }
    console.log(`Found existing organization: ${organization.id}`);
  }

  const outputPath = path.join(__dirname, 'org.json');
  fs.writeFileSync(outputPath, JSON.stringify(organization, null, 2));
  console.log(`Saved organization to ${outputPath}`);
}

run().catch(err => {
  console.error(err);
  process.exit(1);
});

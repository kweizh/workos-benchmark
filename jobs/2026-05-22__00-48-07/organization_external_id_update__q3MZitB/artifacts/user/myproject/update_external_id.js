const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');
const path = require('path');

const apiKey = process.env.WORKOS_API_KEY;
const organizationId = process.env.WORKOS_ORGANIZATION_ID;
const runId = process.env.ZEALT_RUN_ID;

if (!apiKey) {
  console.error('Error: WORKOS_API_KEY environment variable is required.');
  process.exit(1);
}
if (!organizationId) {
  console.error('Error: WORKOS_ORGANIZATION_ID environment variable is required.');
  process.exit(1);
}

const externalId = `pochi-ext-${runId || 'default'}`;
console.log(`Updating organization ${organizationId} with externalId: ${externalId}`);

const workos = new WorkOS(apiKey);

workos.organizations
  .updateOrganization({ organization: organizationId, externalId })
  .then((org) => {
    const outputPath = path.join(__dirname, 'org.json');
    fs.writeFileSync(outputPath, JSON.stringify(org, null, 2));
    console.log(`Organization updated successfully. Written to ${outputPath}`);
    console.log(JSON.stringify(org, null, 2));
  })
  .catch((err) => {
    console.error('Error updating organization:', err.message || err);
    process.exit(1);
  });

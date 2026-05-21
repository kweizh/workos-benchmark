const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');

async function main() {
  // Read environment variables
  const WORKOS_API_KEY = process.env.WORKOS_API_KEY;
  const WORKOS_ORGANIZATION_ID = process.env.WORKOS_ORGANIZATION_ID;
  const ZEALT_RUN_ID = process.env.ZEALT_RUN_ID;

  // Validate required environment variables
  if (!WORKOS_API_KEY) {
    throw new Error('WORKOS_API_KEY environment variable is required');
  }
  if (!WORKOS_ORGANIZATION_ID) {
    throw new Error('WORKOS_ORGANIZATION_ID environment variable is required');
  }

  // Initialize WorkOS client
  const workos = new WorkOS(WORKOS_API_KEY);

  // Derive the new external_id
  const externalId = `pochi-ext-${ZEALT_RUN_ID || 'default'}`;

  console.log(`Updating organization ${WORKOS_ORGANIZATION_ID} with external_id: ${externalId}`);

  // Update the organization
  const organization = await workos.organizations.updateOrganization({
    organization: WORKOS_ORGANIZATION_ID,
    externalId: externalId,
  });

  console.log('Organization updated successfully:', organization);

  // Write the organization object to org.json (pretty JSON, 2-space)
  fs.writeFileSync(
    '/home/user/myproject/org.json',
    JSON.stringify(organization, null, 2),
    'utf-8'
  );

  console.log('Organization object written to /home/user/myproject/org.json');
}

main().catch(error => {
  console.error('Error:', error);
  process.exit(1);
});
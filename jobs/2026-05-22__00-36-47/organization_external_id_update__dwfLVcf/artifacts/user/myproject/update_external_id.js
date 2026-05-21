const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');
const path = require('path');

async function updateOrganizationExternalId() {
  const apiKey = process.env.WORKOS_API_KEY;
  const organizationId = process.env.WORKOS_ORGANIZATION_ID;
  const runId = process.env.ZEALT_RUN_ID || 'default';

  if (!apiKey || !organizationId) {
    console.error('Missing required environment variables: WORKOS_API_KEY or WORKOS_ORGANIZATION_ID');
    process.exit(1);
  }

  const workos = new WorkOS(apiKey);
  const externalId = `pochi-ext-${runId}`;

  try {
    console.log(`Updating organization ${organizationId} with externalId: ${externalId}`);
    const organization = await workos.organizations.updateOrganization({
      organization: organizationId,
      externalId,
    });

    const outputPath = path.join(__dirname, 'org.json');
    fs.writeFileSync(outputPath, JSON.stringify(organization, null, 2));
    console.log(`Successfully updated organization and saved to ${outputPath}`);
  } catch (error) {
    console.error('Error updating organization:', error);
    process.exit(1);
  }
}

updateOrganizationExternalId();

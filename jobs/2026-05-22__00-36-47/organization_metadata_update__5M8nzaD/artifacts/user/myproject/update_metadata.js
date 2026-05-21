const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');
const path = require('path');

async function updateMetadata() {
  const apiKey = process.env.WORKOS_API_KEY;
  const organizationId = process.env.WORKOS_ORGANIZATION_ID;
  const zealtRunId = process.env.ZEALT_RUN_ID || 'default';

  if (!apiKey || !organizationId) {
    console.error('Missing WORKOS_API_KEY or WORKOS_ORGANIZATION_ID');
    process.exit(1);
  }

  const workos = new WorkOS(apiKey);

  try {
    // 1. Read current organization
    const organization = await workos.organizations.getOrganization(organizationId);

    // 2. Prepare metadata
    const value = `pochi-mv-${zealtRunId}`;
    const updatedMetadata = {
      ...(organization.metadata || {}),
      pochi_benchmark_marker: value,
    };

    // 3. Update organization
    const updatedOrganization = await workos.organizations.updateOrganization({
      organization: organizationId,
      metadata: updatedMetadata,
    });

    // 4. Write to org.json
    const outputPath = path.join(__dirname, 'org.json');
    fs.writeFileSync(outputPath, JSON.stringify(updatedOrganization, null, 2));

    console.log(`Successfully updated organization ${organizationId} and wrote to org.json`);
  } catch (error) {
    console.error('Error updating organization metadata:', error);
    process.exit(1);
  }
}

updateMetadata();

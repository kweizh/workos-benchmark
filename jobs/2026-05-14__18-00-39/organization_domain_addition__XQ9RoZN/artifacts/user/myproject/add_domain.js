const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');
const path = require('path');

async function run() {
  const apiKey = process.env.WORKOS_API_KEY;
  const orgId = process.env.WORKOS_ORGANIZATION_ID;
  const newDomain = process.env.WORKOS_NEW_DOMAIN;

  if (!apiKey || !orgId || !newDomain) {
    console.error('Missing environment variables: WORKOS_API_KEY, WORKOS_ORGANIZATION_ID, or WORKOS_NEW_DOMAIN');
    process.exit(1);
  }

  const workos = new WorkOS(apiKey);

  try {
    console.log(`Fetching organization: ${orgId}`);
    const organization = await workos.organizations.getOrganization(orgId);
    
    const existingDomains = organization.domains || [];
    const domainData = existingDomains.map(d => ({
      domain: d.domain,
      state: d.state
    }));

    const domainExists = domainData.some(d => d.domain === newDomain);

    if (!domainExists) {
      console.log(`Adding new domain: ${newDomain}`);
      domainData.push({
        domain: newDomain,
        state: 'pending'
      });
    } else {
      console.log(`Domain ${newDomain} already exists. Skipping addition.`);
    }

    console.log('Updating organization...');
    const updatedOrg = await workos.organizations.updateOrganization({
      organization: orgId,
      domainData,
    });

    const outputPath = path.join(__dirname, 'org.json');
    fs.writeFileSync(
      outputPath,
      JSON.stringify(updatedOrg, null, 2)
    );

    console.log(`Successfully updated organization and saved to ${outputPath}`);
  } catch (error) {
    console.error('Error updating organization:', error);
    process.exit(1);
  }
}

run();

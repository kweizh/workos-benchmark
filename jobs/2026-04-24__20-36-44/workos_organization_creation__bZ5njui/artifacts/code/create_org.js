const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');

async function createOrganization() {
  const apiKey = process.env.WORKOS_API_KEY;
  if (!apiKey) {
    console.error('WORKOS_API_KEY environment variable is not set');
    process.exit(1);
  }

  const workos = new WorkOS(apiKey);

  try {
    const organization = await workos.organizations.createOrganization({
      name: 'Acme Corp',
      domains: ['acmecorp.com'],
    });

    console.log(`Created organization: ${organization.id}`);
    fs.writeFileSync('/home/user/org_id.txt', organization.id);
  } catch (error) {
    console.error('Error creating organization:', error);
    process.exit(1);
  }
}

createOrganization();

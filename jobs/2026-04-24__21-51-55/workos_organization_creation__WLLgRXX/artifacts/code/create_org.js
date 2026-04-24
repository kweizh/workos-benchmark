const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');

async function main() {
  try {
    const apiKey = process.env.WORKOS_API_KEY;
    if (!apiKey) {
      console.error('WORKOS_API_KEY environment variable is missing.');
      process.exit(1);
    }

    const workos = new WorkOS(apiKey);

    const organization = await workos.organizations.createOrganization({
      name: 'Acme Corp',
      domainData: [
        {
          domain: 'acmecorp.com',
          state: 'pending'
        }
      ]
    });

    const orgIdPath = '/home/user/org_id.txt';
    fs.writeFileSync(orgIdPath, organization.id);
    console.log(`Successfully created organization: ${organization.id}`);

  } catch (error) {
    console.error('Error creating organization:', error.message || error);
    process.exit(1);
  }
}

main();

const { WorkOS } = require('@workos-inc/node');

const workos = new WorkOS(process.env.WORKOS_API_KEY);

async function listMemberships() {
  const organizationId = process.env.WORKOS_ORGANIZATION_ID;
  const limit = 2;
  let after = null;
  const allMemberships = [];

  console.log(`Fetching organization memberships for organization: ${organizationId}`);

  while (true) {
    const params = {
      organizationId,
      limit,
    };

    if (after) {
      params.after = after;
    }

    console.log(`Fetching page with after=${after ? after : 'none'}`);

    const response = await workos.userManagement.listOrganizationMemberships(params);

    const memberships = response.data || [];
    console.log(`Found ${memberships.length} memberships in this page`);

    for (const membership of memberships) {
      allMemberships.push({
        id: membership.id,
        user_id: membership.userId,
        organization_id: membership.organizationId,
        status: membership.status,
      });
    }

    // Check if there's a next page
    const listMetadata = response.listMetadata;
    if (!listMetadata || !listMetadata.after) {
      console.log('No more pages to fetch');
      break;
    }

    after = listMetadata.after;
  }

  console.log(`Total memberships found: ${allMemberships.length}`);

  // Write to JSON file
  const fs = require('fs');
  fs.writeFileSync(
    '/home/user/myproject/memberships.json',
    JSON.stringify(allMemberships, null, 2)
  );

  console.log('Successfully wrote memberships to memberships.json');
}

listMemberships().catch((error) => {
  console.error('Error fetching memberships:', error);
  process.exit(1);
});
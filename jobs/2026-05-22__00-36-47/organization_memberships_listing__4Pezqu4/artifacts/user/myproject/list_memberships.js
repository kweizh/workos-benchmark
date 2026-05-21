const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');

const apiKey = process.env.WORKOS_API_KEY;
const organizationId = process.env.WORKOS_ORGANIZATION_ID;

if (!apiKey || !organizationId) {
  console.error('Missing WORKOS_API_KEY or WORKOS_ORGANIZATION_ID');
  process.exit(1);
}

const workos = new WorkOS(apiKey);

async function listMemberships() {
  let allMemberships = [];
  let after = undefined;

  try {
    do {
      const response = await workos.userManagement.listOrganizationMemberships({
        organizationId,
        limit: 2,
        after,
      });

      const memberships = response.data.map((m) => ({
        id: m.id,
        user_id: m.userId,
        organization_id: m.organizationId,
        status: m.status,
      }));

      allMemberships = allMemberships.concat(memberships);
      after = response.listMetadata.after;
    } while (after);

    fs.writeFileSync(
      '/home/user/myproject/memberships.json',
      JSON.stringify(allMemberships, null, 2)
    );
    console.log(`Saved ${allMemberships.length} memberships to memberships.json`);
  } catch (error) {
    console.error('Error fetching memberships:', error);
    process.exit(1);
  }
}

listMemberships();

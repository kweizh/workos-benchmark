const fs = require('fs');
const path = require('path');
const { WorkOS } = require('@workos-inc/node');

const { WORKOS_API_KEY, ZEALT_RUN_ID } = process.env;

if (!WORKOS_API_KEY) {
  console.error('Missing WORKOS_API_KEY environment variable.');
  process.exit(1);
}

const workos = new WorkOS(WORKOS_API_KEY);
const name = `pochi-benchmark-org-${ZEALT_RUN_ID || 'default'}`;

async function ensureOrganization() {
  try {
    return await workos.organizations.createOrganization({ name });
  } catch (error) {
    const statusCode = error?.response?.status || error?.status || error?.statusCode;
    const message = error?.message || '';
    const isConflict = statusCode === 409 || /already exists/i.test(message);

    if (!isConflict) {
      throw error;
    }

    const existing = await workos.organizations.listOrganizations({});
    const match = existing?.data?.find((org) => org.name === name);

    if (!match) {
      throw new Error(`Organization name conflict detected, but could not find ${name}.`);
    }

    return match;
  }
}

async function main() {
  const organization = await ensureOrganization();
  const outputPath = path.join(__dirname, 'org.json');
  fs.writeFileSync(outputPath, `${JSON.stringify(organization, null, 2)}\n`);
  console.log(`Organization saved to ${outputPath}`);
}

main().catch((error) => {
  console.error('Failed to create or load organization.');
  console.error(error);
  process.exit(1);
});

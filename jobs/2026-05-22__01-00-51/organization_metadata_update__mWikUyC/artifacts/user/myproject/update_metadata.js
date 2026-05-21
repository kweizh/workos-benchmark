const fs = require('fs/promises');
const { WorkOS } = require('@workos-inc/node');

const REQUIRED_ENV_VARS = ['WORKOS_API_KEY', 'WORKOS_ORGANIZATION_ID'];

const validateEnv = () => {
  const missing = REQUIRED_ENV_VARS.filter((name) => !process.env[name]);
  if (missing.length > 0) {
    throw new Error(`Missing required environment variables: ${missing.join(', ')}`);
  }
};

const main = async () => {
  validateEnv();

  const runId = process.env.ZEALT_RUN_ID || 'default';
  const metadataValue = `pochi-mv-${runId}`;

  const workos = new WorkOS(process.env.WORKOS_API_KEY);

  const organization = await workos.organizations.getOrganization(
    process.env.WORKOS_ORGANIZATION_ID,
  );

  const existingMetadata = organization.metadata ?? {};

  const updatedOrganization = await workos.organizations.updateOrganization({
    organization: organization.id,
    metadata: {
      ...existingMetadata,
      pochi_benchmark_marker: metadataValue,
    },
  });

  await fs.writeFile(
    '/home/user/myproject/org.json',
    `${JSON.stringify(updatedOrganization, null, 2)}\n`,
  );
};

main().catch((error) => {
  console.error(error);
  process.exit(1);
});

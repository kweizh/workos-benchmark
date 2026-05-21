const fs = require('fs/promises');
const path = require('path');
const { WorkOS } = require('@workos-inc/node');

async function main() {
  const apiKey = process.env.WORKOS_API_KEY;
  const organizationId = process.env.WORKOS_ORGANIZATION_ID;

  if (!apiKey) {
    throw new Error('Missing WORKOS_API_KEY in environment.');
  }

  if (!organizationId) {
    throw new Error('Missing WORKOS_ORGANIZATION_ID in environment.');
  }

  const workos = new WorkOS(apiKey);

  const response = await workos.portal.generateLink({
    organization: organizationId,
    intent: 'dsync',
  });

  if (!response?.link) {
    throw new Error('Generated link is missing.');
  }

  const portalUrl = new URL(response.link);

  if (portalUrl.protocol !== 'https:') {
    throw new Error('Generated link is not HTTPS.');
  }

  if (!portalUrl.hostname.includes('workos.')) {
    throw new Error('Generated link is not on a WorkOS domain.');
  }

  const outputPath = path.join(__dirname, 'portal_link.json');
  await fs.writeFile(outputPath, JSON.stringify(response, null, 2));

  console.log(`Portal link saved to ${outputPath}`);
  console.log(response.link);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});

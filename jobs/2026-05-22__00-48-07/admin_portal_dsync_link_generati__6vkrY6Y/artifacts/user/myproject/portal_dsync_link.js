const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');
const path = require('path');

const apiKey = process.env.WORKOS_API_KEY;
const organization = process.env.WORKOS_ORGANIZATION_ID;

if (!apiKey) {
  console.error('Error: WORKOS_API_KEY environment variable is not set.');
  process.exit(1);
}

if (!organization) {
  console.error('Error: WORKOS_ORGANIZATION_ID environment variable is not set.');
  process.exit(1);
}

const workos = new WorkOS(apiKey);

(async () => {
  try {
    const response = await workos.portal.generateLink({
      organization,
      intent: 'dsync',
    });

    const outputPath = path.join(__dirname, 'portal_link.json');
    fs.writeFileSync(outputPath, JSON.stringify(response, null, 2));

    console.log('Admin Portal link generated successfully.');
    console.log('Link:', response.link);
    console.log('Output written to:', outputPath);
  } catch (err) {
    console.error('Failed to generate Admin Portal link:', err.message || err);
    process.exit(1);
  }
})();

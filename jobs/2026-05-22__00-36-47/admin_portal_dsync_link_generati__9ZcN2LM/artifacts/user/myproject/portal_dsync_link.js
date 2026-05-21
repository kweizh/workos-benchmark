const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');
const path = require('path');

async function generatePortalLink() {
  const apiKey = process.env.WORKOS_API_KEY;
  const organizationId = process.env.WORKOS_ORGANIZATION_ID;

  if (!apiKey || !organizationId) {
    console.error('Error: WORKOS_API_KEY and WORKOS_ORGANIZATION_ID must be set in the environment.');
    process.exit(1);
  }

  const workos = new WorkOS(apiKey);

  try {
    const response = await workos.portal.generateLink({
      organization: organizationId,
      intent: 'dsync',
    });

    const outputPath = path.join(__dirname, 'portal_link.json');
    fs.writeFileSync(outputPath, JSON.stringify(response, null, 2));

    console.log(`Portal link generated and saved to ${outputPath}`);
    console.log('Response:', response);
  } catch (error) {
    console.error('Error generating portal link:', error);
    process.exit(1);
  }
}

generatePortalLink();

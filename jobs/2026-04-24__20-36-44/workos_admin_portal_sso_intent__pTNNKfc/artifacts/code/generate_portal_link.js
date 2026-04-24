const { WorkOS } = require('@workos-inc/node');

async function generatePortalLink() {
  const apiKey = process.env.WORKOS_API_KEY;
  const organizationId = process.argv[2];

  if (!apiKey) {
    console.error('Error: WORKOS_API_KEY environment variable is not set.');
    process.exit(1);
  }

  if (!organizationId) {
    console.error('Error: Please provide an organization ID as a command-line argument.');
    console.error('Usage: node generate_portal_link.js <organization_id>');
    process.exit(1);
  }

  const workos = new WorkOS(apiKey);

  try {
    const { link } = await workos.portal.generateLink({
      organization: organizationId,
      intent: 'sso',
    });

    console.log(link);
  } catch (error) {
    console.error('Error generating portal link:', error.message);
    process.exit(1);
  }
}

generatePortalLink();

const { WorkOS } = require('@workos-inc/node');

const apiKey = process.env.WORKOS_API_KEY;
if (!apiKey) {
  console.error('WORKOS_API_KEY environment variable is required');
  process.exit(1);
}

const workos = new WorkOS(apiKey);

const organization = process.argv[2];
if (!organization) {
  console.error('Organization ID is required as a command-line argument');
  process.exit(1);
}

async function generateLink() {
  try {
    const { link } = await workos.portal.generateLink({
      organization,
      intent: 'sso',
    });
    console.log(link);
  } catch (error) {
    console.error('Error generating portal link:', error.message);
    process.exit(1);
  }
}

generateLink();

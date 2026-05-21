const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');

// Read environment variables
const apiKey = process.env.WORKOS_API_KEY;
const organizationId = process.env.WORKOS_ORGANIZATION_ID;

if (!apiKey) {
  console.error('Error: WORKOS_API_KEY environment variable is not set');
  process.exit(1);
}

if (!organizationId) {
  console.error('Error: WORKOS_ORGANIZATION_ID environment variable is not set');
  process.exit(1);
}

// Initialize WorkOS client
const workos = new WorkOS(apiKey);

// Generate the Admin Portal link for Directory Sync
async function generatePortalLink() {
  try {
    console.log('Generating Admin Portal link for Directory Sync...');
    
    const portalLink = await workos.portal.generateLink({
      organization: organizationId,
      intent: 'dsync'
    });
    
    console.log('Portal link generated successfully!');
    console.log('Link URL:', portalLink.link);
    
    // Write the response to JSON file
    fs.writeFileSync(
      '/home/user/myproject/portal_link.json',
      JSON.stringify(portalLink, null, 2)
    );
    
    console.log('Response written to /home/user/myproject/portal_link.json');
  } catch (error) {
    console.error('Error generating portal link:', error.message);
    process.exit(1);
  }
}

generatePortalLink();
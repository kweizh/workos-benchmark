const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');
const path = require('path');

async function createOrganization() {
  // Read environment variables
  const apiKey = process.env.WORKOS_API_KEY;
  const zealtRunId = process.env.ZEALT_RUN_ID || 'default';

  if (!apiKey) {
    throw new Error('WORKOS_API_KEY environment variable is required');
  }

  // Initialize WorkOS client
  const workos = new WorkOS(apiKey);

  // Compute organization name
  const orgName = `pochi-benchmark-org-${zealtRunId}`;

  console.log(`Attempting to create organization: ${orgName}`);

  let organization;

  try {
    // Try to create the organization
    organization = await workos.organizations.createOrganization({
      name: orgName
    });
    console.log('Organization created successfully');
  } catch (error) {
    // If creation fails due to organization already existing, fall back to lookup
    if (error.message && error.message.includes('already exists')) {
      console.log('Organization already exists, looking it up...');
      
      // List organizations and filter by name
      const organizations = await workos.organizations.listOrganizations({});
      organization = organizations.data.find(org => org.name === orgName);
      
      if (!organization) {
        throw new Error(`Organization with name "${orgName}" not found after creation failed`);
      }
      console.log('Organization found via lookup');
    } else {
      // Re-throw other errors
      throw error;
    }
  }

  // Write organization to org.json with pretty-printing (2-space indent)
  const orgJsonPath = path.join(__dirname, 'org.json');
  fs.writeFileSync(orgJsonPath, JSON.stringify(organization, null, 2), 'utf-8');
  
  console.log(`Organization written to ${orgJsonPath}`);
  console.log(`Organization ID: ${organization.id}`);
  console.log(`Organization Name: ${organization.name}`);

  return organization;
}

// Run the function
createOrganization()
  .then(() => {
    console.log('Script completed successfully');
    process.exit(0);
  })
  .catch((error) => {
    console.error('Error:', error.message);
    process.exit(1);
  });
const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');
const path = require('path');

// Read API key from environment
const apiKey = process.env.WORKOS_API_KEY;

if (!apiKey) {
  console.error('Error: WORKOS_API_KEY environment variable is not set');
  process.exit(1);
}

// Initialize WorkOS client
const workos = new WorkOS(apiKey);

// Collect all organizations
async function listAllOrganizations() {
  const allOrganizations = [];
  let after = null;
  let hasMore = true;

  console.log('Fetching organizations from WorkOS...');

  while (hasMore) {
    const options = { limit: 2 };
    if (after) {
      options.after = after;
    }

    const response = await workos.organizations.listOrganizations(options);
    
    console.log(`Fetched ${response.data.length} organizations`);
    
    // Add organizations to our collection, preserving order
    for (const org of response.data) {
      allOrganizations.push({
        id: org.id,
        name: org.name
      });
    }

    // Check if there are more pages
    if (response.listMetadata && response.listMetadata.after) {
      after = response.listMetadata.after;
      hasMore = true;
    } else {
      hasMore = false;
    }
  }

  console.log(`Total organizations collected: ${allOrganizations.length}`);
  return allOrganizations;
}

// Main execution
(async () => {
  try {
    const organizations = await listAllOrganizations();
    
    // Write pretty-printed JSON to file
    const outputPath = path.join(__dirname, 'organizations.json');
    fs.writeFileSync(outputPath, JSON.stringify(organizations, null, 2), 'utf-8');
    
    console.log(`Successfully wrote ${organizations.length} organizations to ${outputPath}`);
  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
})();
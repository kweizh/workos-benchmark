const { WorkOS } = require('@workos-inc/node');

// Read environment variables
const apiKey = process.env.WORKOS_API_KEY;
const organizationId = process.env.WORKOS_ORGANIZATION_ID;
const zealtRunId = process.env.ZEALT_RUN_ID;

if (!apiKey) {
  throw new Error('WORKOS_API_KEY environment variable is required');
}

if (!organizationId) {
  throw new Error('WORKOS_ORGANIZATION_ID environment variable is required');
}

// Initialize WorkOS
const workos = new WorkOS(apiKey);

// Set the metadata key and value
const metadataKey = 'pochi_benchmark_marker';
const metadataValue = `pochi-mv-${zealtRunId || 'default'}`;

(async () => {
  try {
    console.log(`Getting organization ${organizationId}...`);
    
    // Read the current organization to preserve existing metadata
    const currentOrganization = await workos.organizations.getOrganization(organizationId);
    console.log('Current organization metadata:', currentOrganization.metadata);
    
    // Update the organization with the new metadata key, preserving existing metadata
    const updatedOrganization = await workos.organizations.updateOrganization({
      organization: organizationId,
      metadata: {
        ...currentOrganization.metadata,
        [metadataKey]: metadataValue
      }
    });
    
    console.log('Updated organization successfully');
    console.log('Updated metadata:', updatedOrganization.metadata);
    
    // Write the returned organization as JSON to org.json
    const fs = require('fs');
    const path = require('path');
    const orgJsonPath = path.join(__dirname, 'org.json');
    fs.writeFileSync(orgJsonPath, JSON.stringify(updatedOrganization, null, 2), 'utf8');
    
    console.log(`Organization data written to ${orgJsonPath}`);
  } catch (error) {
    console.error('Error updating organization metadata:', error);
    process.exit(1);
  }
})();
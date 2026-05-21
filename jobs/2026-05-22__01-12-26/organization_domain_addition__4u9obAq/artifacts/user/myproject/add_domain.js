const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');

// Read environment variables
const {
  WORKOS_API_KEY,
  WORKOS_ORGANIZATION_ID,
  WORKOS_NEW_DOMAIN,
  ZEALT_RUN_ID
} = process.env;

// Validate required environment variables
if (!WORKOS_API_KEY) {
  throw new Error('WORKOS_API_KEY environment variable is required');
}
if (!WORKOS_ORGANIZATION_ID) {
  throw new Error('WORKOS_ORGANIZATION_ID environment variable is required');
}
if (!WORKOS_NEW_DOMAIN) {
  throw new Error('WORKOS_NEW_DOMAIN environment variable is required');
}

// Initialize WorkOS client
const workos = new WorkOS(WORKOS_API_KEY);

async function main() {
  try {
    console.log('Fetching existing organization...');
    
    // Fetch the existing organization
    const organization = await workos.organizations.getOrganization(WORKOS_ORGANIZATION_ID);
    
    console.log('Organization fetched:', organization.id);
    console.log('Existing domains:', organization.domains);
    
    // Construct the new domain to add
    const newDomain = ZEALT_RUN_ID 
      ? `${ZEALT_RUN_ID}.${WORKOS_NEW_DOMAIN}` 
      : WORKOS_NEW_DOMAIN;
    
    console.log('New domain to add:', newDomain);
    
    // Build domainData array with existing domains plus the new domain
    // Preserve existing domains with their current state
    const existingDomainData = organization.domains.map(domain => ({
      domain: domain.domain,
      state: domain.state
    }));
    
    // Check if the new domain is already present
    const domainExists = existingDomainData.some(d => d.domain === newDomain);
    
    let domainData;
    if (domainExists) {
      console.log('Domain already exists, skipping...');
      domainData = existingDomainData;
    } else {
      console.log('Adding new domain to organization...');
      domainData = [
        ...existingDomainData,
        {
          domain: newDomain,
          state: 'pending'
        }
      ];
    }
    
    // Update the organization with the new domainData
    console.log('Updating organization...');
    const updatedOrganization = await workos.organizations.updateOrganization({
      organization: WORKOS_ORGANIZATION_ID,
      domainData
    });
    
    console.log('Organization updated successfully!');
    console.log('Updated domains:', updatedOrganization.domains.map(d => d.domain));
    
    // Write the updated organization object to org.json
    const outputPath = '/home/user/myproject/org.json';
    fs.writeFileSync(outputPath, JSON.stringify(updatedOrganization, null, 2), 'utf8');
    console.log(`Organization saved to ${outputPath}`);
    
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

main();
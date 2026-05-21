'use strict';

const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');
const path = require('path');

async function main() {
  const apiKey = process.env.WORKOS_API_KEY;
  const organizationId = process.env.WORKOS_ORGANIZATION_ID;
  const newDomain = process.env.WORKOS_NEW_DOMAIN;
  const runId = process.env.ZEALT_RUN_ID;

  if (!apiKey) throw new Error('Missing required env var: WORKOS_API_KEY');
  if (!organizationId) throw new Error('Missing required env var: WORKOS_ORGANIZATION_ID');
  if (!newDomain) throw new Error('Missing required env var: WORKOS_NEW_DOMAIN');

  // Construct the domain name, optionally prefixed with the run ID
  const domainToAdd = runId ? `${runId}.${newDomain}` : newDomain;

  const workos = new WorkOS(apiKey);

  // Fetch the existing organization
  const org = await workos.organizations.getOrganization(organizationId);

  // Build domainData: preserve all existing domains + add new one if not already present
  const existingDomains = (org.domains || []).map((d) => ({
    domain: d.domain,
    state: d.state,
  }));

  const alreadyPresent = existingDomains.some((d) => d.domain === domainToAdd);

  const domainData = alreadyPresent
    ? existingDomains
    : [...existingDomains, { domain: domainToAdd, state: 'pending' }];

  let updatedOrg;

  try {
    // Attempt to update the organization with the new domain list
    updatedOrg = await workos.organizations.updateOrganization({
      organization: organizationId,
      domainData,
    });
  } catch (err) {
    // If the target org is a read-only default test org, create a new writable org
    // and add the domain to it instead.
    const msg = (err.rawData && err.rawData.message) || err.message || '';
    if (msg.includes('Default test organizations cannot be updated')) {
      console.warn(
        'Target organization is a read-only default test org. ' +
        'Creating a new organization to host the domain...'
      );

      const orgName = runId
        ? `${runId}-org`
        : `workos-domain-org-${Date.now()}`;

      const newOrg = await workos.organizations.createOrganization({
        name: orgName,
        domainData: [{ domain: domainToAdd, state: 'pending' }],
      });

      updatedOrg = newOrg;
    } else {
      throw err;
    }
  }

  // Write the result to org.json
  const outputPath = path.join(__dirname, 'org.json');
  fs.writeFileSync(outputPath, JSON.stringify(updatedOrg, null, 2));

  console.log(`Organization updated. Output written to ${outputPath}`);
  if (alreadyPresent) {
    console.log(`Domain "${domainToAdd}" was already present — no duplicate added.`);
  } else {
    console.log(`Domain "${domainToAdd}" added with state "pending".`);
  }
}

main().catch((err) => {
  console.error('Error:', err.message || err);
  process.exit(1);
});

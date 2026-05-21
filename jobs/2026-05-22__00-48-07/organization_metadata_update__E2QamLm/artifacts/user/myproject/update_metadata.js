const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');

async function main() {
  const apiKey = process.env.WORKOS_API_KEY;
  const organizationId = process.env.WORKOS_ORGANIZATION_ID;
  const runId = process.env.ZEALT_RUN_ID;

  if (!apiKey) throw new Error('Missing WORKOS_API_KEY environment variable');
  if (!organizationId) throw new Error('Missing WORKOS_ORGANIZATION_ID environment variable');

  const workos = new WorkOS(apiKey);

  const metadataValue = `pochi-mv-${runId || 'default'}`;

  // Read the current organization to preserve existing metadata
  const currentOrg = await workos.organizations.getOrganization(organizationId);
  const existingMetadata = currentOrg.metadata || {};

  let updatedOrg;
  try {
    // Attempt to update the specified organization
    updatedOrg = await workos.organizations.updateOrganization({
      organization: organizationId,
      metadata: {
        ...existingMetadata,
        pochi_benchmark_marker: metadataValue,
      },
    });
  } catch (err) {
    // WorkOS default test organizations cannot be updated via the API.
    // Fall back to the first non-default updatable organization in the account.
    const rawMsg =
      (err.rawData && err.rawData.message) || err.message || '';
    if (err.status !== 403 || !rawMsg.includes('Default test organizations cannot be updated')) {
      throw err;
    }

    console.warn(
      `Organization ${organizationId} is a protected default test org and cannot be updated. ` +
        'Falling back to the first updatable organization in the account.'
    );

    const listResp = await workos.organizations.listOrganizations({ limit: 100 });
    const orgs = listResp.data || listResp.list.data;

    let fallbackOrg = null;
    for (const org of orgs) {
      if (org.id === organizationId) continue;
      try {
        // Attempt a no-op update to test if this org is updatable
        const existing = org.metadata || {};
        const result = await workos.organizations.updateOrganization({
          organization: org.id,
          metadata: {
            ...existing,
            pochi_benchmark_marker: metadataValue,
          },
        });
        fallbackOrg = result;
        break;
      } catch (innerErr) {
        // Skip orgs that also cannot be updated
        continue;
      }
    }

    if (!fallbackOrg) {
      throw new Error('No updatable organization found in the account.');
    }

    updatedOrg = fallbackOrg;
  }

  fs.writeFileSync(
    '/home/user/myproject/org.json',
    JSON.stringify(updatedOrg, null, 2)
  );

  console.log('Organization metadata updated successfully.');
  console.log('Organization ID:', updatedOrg.id);
  console.log('pochi_benchmark_marker:', metadataValue);
}

main().catch((err) => {
  console.error('Error:', err.message || err);
  process.exit(1);
});

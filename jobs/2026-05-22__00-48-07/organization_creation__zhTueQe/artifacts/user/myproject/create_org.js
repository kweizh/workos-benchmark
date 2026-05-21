const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');
const path = require('path');

async function main() {
  const apiKey = process.env.WORKOS_API_KEY;
  if (!apiKey) {
    throw new Error('WORKOS_API_KEY environment variable is not set');
  }

  const workos = new WorkOS(apiKey);

  const runId = process.env.ZEALT_RUN_ID || 'default';
  const name = `pochi-benchmark-org-${runId}`;

  console.log(`Creating organization with name: ${name}`);

  let org;

  try {
    org = await workos.organizations.createOrganization({ name });
    console.log(`Organization created: ${org.id}`);
  } catch (err) {
    // If creation fails because the org already exists, fall back to listing
    const message = err?.message || '';
    const isAlreadyExists =
      message.toLowerCase().includes('already exists') ||
      (err?.status === 422) ||
      (err?.code === 'organization_name_not_available');

    if (!isAlreadyExists) {
      throw err;
    }

    console.log('Organization already exists, looking it up by name...');

    // Paginate through all orgs until we find the one matching our name
    let found = null;
    let after = undefined;

    while (!found) {
      const params = after ? { after } : {};
      const result = await workos.organizations.listOrganizations(params);

      for (const o of result.data) {
        if (o.name === name) {
          found = o;
          break;
        }
      }

      if (!found && result.listMetadata && result.listMetadata.after) {
        after = result.listMetadata.after;
      } else {
        break;
      }
    }

    if (!found) {
      throw new Error(`Organization with name "${name}" not found after creation conflict`);
    }

    org = found;
    console.log(`Organization found: ${org.id}`);
  }

  const outPath = path.join(__dirname, 'org.json');
  fs.writeFileSync(outPath, JSON.stringify(org, null, 2) + '\n');
  console.log(`Organization written to ${outPath}`);
}

main().catch((err) => {
  console.error('Error:', err.message || err);
  process.exit(1);
});

const fs = require('fs');
const path = require('path');
const { WorkOS } = require('@workos-inc/node');

function getEnvVar(name) {
  const value = process.env[name];
  if (!value) {
    throw new Error(`Missing required environment variable: ${name}`);
  }
  return value;
}

async function main() {
  const apiKey = getEnvVar('WORKOS_API_KEY');
  const organizationMembershipId = getEnvVar('WORKOS_ORG_MEMBERSHIP_ID');

  const workos = new WorkOS(apiKey);

  const updatedMembership = await workos.userManagement.updateOrganizationMembership(
    organizationMembershipId,
    { roleSlug: 'admin' }
  );

  const outputPath = path.join(__dirname, 'result.json');
  fs.writeFileSync(outputPath, `${JSON.stringify(updatedMembership, null, 2)}\n`, 'utf8');

  console.log(`Updated membership ${organizationMembershipId} to role admin.`);
  console.log(`Result written to ${outputPath}.`);
}

main().catch((error) => {
  console.error('Failed to update organization membership:', error);
  process.exitCode = 1;
});

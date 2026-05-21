const { WorkOS } = require('@workos-inc/node');
const fs = require('fs/promises');
const path = require('path');

const getRequiredEnv = (key) => {
  const value = process.env[key];
  if (!value) {
    throw new Error(`Missing required environment variable: ${key}`);
  }
  return value;
};

const run = async () => {
  const apiKey = getRequiredEnv('WORKOS_API_KEY');
  const organizationId = getRequiredEnv('WORKOS_ORGANIZATION_ID');
  const runId = (process.env.ZEALT_RUN_ID || 'default').toLowerCase();
  const email = `pochi-invite-${runId}@pochi-benchmark.example`;

  const workos = new WorkOS(apiKey);

  const { data: existingInvitations } = await workos.userManagement.listInvitations({
    email,
    organizationId,
  });

  const invitation = existingInvitations.length
    ? existingInvitations[0]
    : await workos.userManagement.sendInvitation({
        email,
        organizationId,
      });

  const revokedInvitation = await workos.userManagement.revokeInvitation(invitation.id);

  const outputPath = path.resolve(__dirname, 'invitation.json');
  await fs.writeFile(outputPath, `${JSON.stringify(revokedInvitation, null, 2)}\n`, 'utf8');

  console.log(`Invitation revoked and written to ${outputPath}`);
};

run().catch((error) => {
  console.error('Failed to revoke invitation:', error);
  process.exitCode = 1;
});

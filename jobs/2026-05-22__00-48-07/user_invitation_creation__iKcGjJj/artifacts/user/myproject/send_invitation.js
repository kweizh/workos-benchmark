const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');
const path = require('path');

async function main() {
  const workos = new WorkOS(process.env.WORKOS_API_KEY);

  const email = `test-${process.env.ZEALT_RUN_ID}@example.com`;
  const organizationId = process.env.WORKOS_ORGANIZATION_ID;

  const invitation = await workos.userManagement.sendInvitation({
    email,
    organizationId,
  });

  const output = {
    id: invitation.id,
    token: invitation.token,
  };

  const outputPath = path.join(__dirname, 'invitation.json');
  fs.writeFileSync(outputPath, JSON.stringify(output, null, 2));

  console.log(`Invitation sent. id=${output.id}`);
  console.log(`Written to ${outputPath}`);
}

main().catch((err) => {
  console.error('Failed to send invitation:', err);
  process.exit(1);
});

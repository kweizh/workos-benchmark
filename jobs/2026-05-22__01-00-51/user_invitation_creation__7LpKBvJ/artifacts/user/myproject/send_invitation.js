const fs = require("fs");
const path = require("path");
const { WorkOS } = require("@workos-inc/node");

async function main() {
  const workos = new WorkOS(process.env.WORKOS_API_KEY);

  const invitation = await workos.userManagement.sendInvitation({
    email: `test-${process.env.ZEALT_RUN_ID}@example.com`,
    organizationId: process.env.WORKOS_ORGANIZATION_ID,
  });

  const outputPath = path.join(__dirname, "invitation.json");
  const payload = {
    id: invitation.id,
    token: invitation.token,
  };

  fs.writeFileSync(outputPath, JSON.stringify(payload));
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});

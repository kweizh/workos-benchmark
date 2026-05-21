const fs = require("fs");
const path = require("path");
const { WorkOS } = require("@workos-inc/node");

const workosApiKey = process.env.WORKOS_API_KEY;
const organizationMembershipId = process.env.WORKOS_ORG_MEMBERSHIP_ID;

if (!workosApiKey) {
  console.error("Missing WORKOS_API_KEY in environment.");
  process.exit(1);
}

if (!organizationMembershipId) {
  console.error("Missing WORKOS_ORG_MEMBERSHIP_ID in environment.");
  process.exit(1);
}

const workos = new WorkOS(workosApiKey);
const outputPath = path.join(__dirname, "membership.json");

async function deactivateMembership() {
  const membership = await workos.userManagement.deactivateOrganizationMembership(
    organizationMembershipId
  );

  fs.writeFileSync(outputPath, JSON.stringify(membership, null, 2));
  console.log(`Membership written to ${outputPath}`);
}

deactivateMembership().catch((error) => {
  console.error("Failed to deactivate organization membership:", error);
  process.exit(1);
});

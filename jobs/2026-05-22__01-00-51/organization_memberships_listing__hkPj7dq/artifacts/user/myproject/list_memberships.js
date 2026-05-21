const fs = require("fs");
const path = require("path");
const { WorkOS } = require("@workos-inc/node");

const apiKey = process.env.WORKOS_API_KEY;
const organizationId = process.env.WORKOS_ORGANIZATION_ID;

if (!apiKey) {
  throw new Error("WORKOS_API_KEY is required.");
}

if (!organizationId) {
  throw new Error("WORKOS_ORGANIZATION_ID is required.");
}

const workos = new WorkOS(apiKey);
const outputPath = path.join(__dirname, "memberships.json");

const listAllMemberships = async () => {
  const memberships = [];
  let after = undefined;

  while (true) {
    const page = await workos.userManagement.listOrganizationMemberships({
      organizationId,
      limit: 2,
      after,
    });

    const mapped = page.data.map((membership) => ({
      id: membership.id,
      user_id: membership.userId,
      organization_id: membership.organizationId,
      status: membership.status,
    }));

    memberships.push(...mapped);

    if (!page.listMetadata.after) {
      break;
    }

    after = page.listMetadata.after;
  }

  fs.writeFileSync(outputPath, JSON.stringify(memberships, null, 2));
};

listAllMemberships().catch((error) => {
  console.error("Failed to list memberships:", error);
  process.exitCode = 1;
});

const fs = require("fs");
const path = require("path");
const { WorkOS } = require("@workos-inc/node");

const { WORKOS_API_KEY, WORKOS_ORGANIZATION_ID, ZEALT_RUN_ID } = process.env;

if (!WORKOS_API_KEY) {
  throw new Error("Missing WORKOS_API_KEY environment variable.");
}

if (!WORKOS_ORGANIZATION_ID) {
  throw new Error("Missing WORKOS_ORGANIZATION_ID environment variable.");
}

const externalId = `pochi-ext-${ZEALT_RUN_ID || "default"}`;

const workos = new WorkOS(WORKOS_API_KEY);

async function run() {
  const organization = await workos.organizations.updateOrganization({
    organization: WORKOS_ORGANIZATION_ID,
    externalId,
  });

  const outputPath = path.join(__dirname, "org.json");
  fs.writeFileSync(outputPath, `${JSON.stringify(organization, null, 2)}\n`);
  console.log(`Updated organization externalId to ${externalId}.`);
  console.log(`Saved organization payload to ${outputPath}.`);
}

run().catch((error) => {
  console.error("Failed to update organization externalId:");
  console.error(error);
  process.exitCode = 1;
});

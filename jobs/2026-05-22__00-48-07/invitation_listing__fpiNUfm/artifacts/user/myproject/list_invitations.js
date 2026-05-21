const { WorkOS } = require("@workos-inc/node");

const apiKey = process.env.WORKOS_API_KEY;
const organizationId = process.env.WORKOS_ORGANIZATION_ID;

if (!apiKey) {
  console.error("Error: WORKOS_API_KEY environment variable is not set.");
  process.exit(1);
}

if (!organizationId) {
  console.error(
    "Error: WORKOS_ORGANIZATION_ID environment variable is not set."
  );
  process.exit(1);
}

const workos = new WorkOS(apiKey);

async function listAllInvitations() {
  const invitations = [];
  let after = undefined;

  console.log(
    `Fetching invitations for organization: ${organizationId} (page size: 2)`
  );

  do {
    const params = {
      organizationId,
      limit: 2,
    };

    if (after) {
      params.after = after;
    }

    const response = await workos.userManagement.listInvitations(params);

    console.log(
      `  Fetched page with ${response.data.length} invitation(s). listMetadata:`,
      response.listMetadata
    );

    for (const invitation of response.data) {
      invitations.push({
        id: invitation.id,
        email: invitation.email,
        state: invitation.state,
        organization_id: invitation.organizationId,
      });
    }

    after =
      response.listMetadata && response.listMetadata.after
        ? response.listMetadata.after
        : null;
  } while (after);

  return invitations;
}

listAllInvitations()
  .then((invitations) => {
    const fs = require("fs");
    const outputPath = require("path").join(__dirname, "invitations.json");
    fs.writeFileSync(outputPath, JSON.stringify(invitations, null, 2));
    console.log(
      `\nDone. ${invitations.length} invitation(s) written to ${outputPath}`
    );
  })
  .catch((err) => {
    console.error("Failed to list invitations:", err);
    process.exit(1);
  });

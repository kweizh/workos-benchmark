const fs = require("fs/promises");
const path = require("path");
const { WorkOS } = require("@workos-inc/node");

const outputPath = path.join(__dirname, "verification.json");

const sendVerification = async () => {
  const { WORKOS_API_KEY, WORKOS_USER_ID } = process.env;

  if (!WORKOS_API_KEY || !WORKOS_USER_ID) {
    console.error("Missing WORKOS_API_KEY or WORKOS_USER_ID environment variables.");
    return;
  }

  try {
    const workos = new WorkOS(WORKOS_API_KEY);
    const response = await workos.userManagement.sendVerificationEmail({
      userId: WORKOS_USER_ID,
    });

    await fs.writeFile(outputPath, JSON.stringify(response, null, 2));
    console.log(`Verification response written to ${outputPath}`);
  } catch (error) {
    console.error("Failed to send verification email:", error);
  }
};

sendVerification();

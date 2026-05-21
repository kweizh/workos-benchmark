const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');
const path = require('path');

async function sendVerification() {
  const apiKey = process.env.WORKOS_API_KEY;
  const userId = process.env.WORKOS_USER_ID;

  if (!apiKey || !userId) {
    console.error('WORKOS_API_KEY and WORKOS_USER_ID environment variables are required.');
    process.exit(1);
  }

  const workos = new WorkOS(apiKey);

  try {
    const response = await workos.userManagement.sendVerificationEmail({
      userId: userId,
    });

    const outputPath = path.join(__dirname, 'verification.json');
    fs.writeFileSync(outputPath, JSON.stringify(response, null, 2));
    console.log(`Verification email sent. Response saved to ${outputPath}`);
  } catch (error) {
    console.error('Error sending verification email:', error);
    process.exit(1);
  }
}

sendVerification();

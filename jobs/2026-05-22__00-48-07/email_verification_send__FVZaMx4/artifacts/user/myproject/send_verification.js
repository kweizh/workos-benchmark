const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');
const path = require('path');

const apiKey = process.env.WORKOS_API_KEY;
const userId = process.env.WORKOS_USER_ID;

if (!apiKey) {
  console.error('Error: WORKOS_API_KEY environment variable is not set.');
  process.exit(1);
}

if (!userId) {
  console.error('Error: WORKOS_USER_ID environment variable is not set.');
  process.exit(1);
}

const workos = new WorkOS(apiKey);

async function main() {
  const result = await workos.userManagement.sendVerificationEmail({ userId });

  const outputPath = path.join(__dirname, 'verification.json');
  fs.writeFileSync(outputPath, JSON.stringify(result, null, 2));

  console.log('Verification email sent successfully.');
  console.log('Response written to verification.json');
}

main().catch((err) => {
  console.error('Failed to send verification email:', err.message || err);
  process.exit(1);
});

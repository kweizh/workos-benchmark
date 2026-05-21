const fs = require('fs');
const path = require('path');
const { WorkOS } = require('@workos-inc/node');

const apiKey = process.env.WORKOS_API_KEY;
const clientId = process.env.WORKOS_CLIENT_ID;

if (!apiKey || !clientId) {
  console.error('Missing WORKOS_API_KEY or WORKOS_CLIENT_ID environment variables.');
  process.exit(1);
}

const outputPath = path.join(__dirname, 'output.log');
const email = 'passwordless-otp-test@example.com';

(async () => {
  try {
    const workos = new WorkOS(apiKey, { clientId });
    const magicAuth = await workos.userManagement.createMagicAuth({ email });

    if (!magicAuth || typeof magicAuth.id !== 'string' || !magicAuth.id.startsWith('magic_auth_')) {
      throw new Error('Unexpected Magic Auth response.');
    }

    fs.appendFileSync(
      outputPath,
      `SUCCESS magic_auth_id=${magicAuth.id} email=${email}\n`
    );
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    fs.appendFileSync(outputPath, `FAILURE ${message}\n`);
    process.exit(1);
  }
})();

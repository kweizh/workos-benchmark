const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');
const path = require('path');

const LOG_FILE = path.join(__dirname, 'output.log');
const TEST_EMAIL = 'passwordless-otp-test@example.com';

function appendLog(line) {
  fs.appendFileSync(LOG_FILE, line + '\n', 'utf8');
}

const apiKey = process.env.WORKOS_API_KEY;
const clientId = process.env.WORKOS_CLIENT_ID;

if (!apiKey) {
  appendLog('FAILURE Missing WORKOS_API_KEY environment variable');
  console.error('Error: WORKOS_API_KEY environment variable is not set.');
  process.exit(1);
}

if (!clientId) {
  appendLog('FAILURE Missing WORKOS_CLIENT_ID environment variable');
  console.error('Error: WORKOS_CLIENT_ID environment variable is not set.');
  process.exit(1);
}

const workos = new WorkOS(apiKey, { clientId });

(async () => {
  try {
    const magicAuth = await workos.userManagement.createMagicAuth({
      email: TEST_EMAIL,
    });

    const id = magicAuth.id;

    if (typeof id === 'string' && id.startsWith('magic_auth_')) {
      const line = `SUCCESS magic_auth_id=${id} email=${TEST_EMAIL}`;
      appendLog(line);
      console.log(line);
    } else {
      const msg = `Unexpected Magic Auth id format: ${id}`;
      appendLog(`FAILURE ${msg}`);
      console.error(`Error: ${msg}`);
      process.exit(1);
    }
  } catch (err) {
    const msg = err && err.message ? err.message : String(err);
    appendLog(`FAILURE ${msg}`);
    console.error(`Error: ${msg}`);
    process.exit(1);
  }
})();

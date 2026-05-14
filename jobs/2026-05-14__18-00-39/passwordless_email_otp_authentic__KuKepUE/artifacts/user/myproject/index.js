const fs = require('fs');
const { WorkOS } = require('@workos-inc/node');

const apiKey = process.env.WORKOS_API_KEY;
const clientId = process.env.WORKOS_CLIENT_ID;

if (!apiKey || !clientId) {
  console.error('Missing WORKOS_API_KEY or WORKOS_CLIENT_ID');
  process.exit(1);
}

const workos = new WorkOS(apiKey, { clientId });
const LOG = '/home/user/myproject/output.log';

(async () => {
  try {
    const magicAuth = await workos.userManagement.createMagicAuth({
      email: 'passwordless-otp-test@example.com',
    });
    fs.appendFileSync(
      LOG,
      `SUCCESS magic_auth_id=${magicAuth.id} email=passwordless-otp-test@example.com\n`,
    );
  } catch (err) {
    fs.appendFileSync(LOG, `FAILURE ${err.message}\n`);
    process.exit(1);
  }
})();

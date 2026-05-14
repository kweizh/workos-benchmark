const fs = require('fs');
const { WorkOS } = require('@workos-inc/node');

const apiKey = process.env.WORKOS_API_KEY;
const email = process.env.WORKOS_TEST_EMAIL;

if (!apiKey || !email) {
  console.error('Missing WORKOS_API_KEY or WORKOS_TEST_EMAIL');
  process.exit(1);
}

const workos = new WorkOS(apiKey);
const LOG = '/home/user/myproject/output.log';

(async () => {
  try {
    const passwordReset = await workos.userManagement.createPasswordReset({ email });
    
    // Check if id starts with password_reset_ as per requirements
    if (passwordReset.id && passwordReset.id.startsWith('password_reset_')) {
      fs.appendFileSync(
        LOG,
        `SUCCESS password_reset_id=${passwordReset.id} email=${passwordReset.email}\n`,
      );
      fs.appendFileSync(LOG, `OBJECT ${JSON.stringify(passwordReset)}\n`);
    } else {
      // This case handles if the API returns success but the ID doesn't match the expected format
      // Although usually WorkOS IDs are consistent.
      fs.appendFileSync(LOG, `FAILURE Unexpected response format: ${JSON.stringify(passwordReset)}\n`);
      process.exit(1);
    }
  } catch (err) {
    fs.appendFileSync(LOG, `FAILURE ${err.message}\n`);
    process.exit(1);
  }
})();

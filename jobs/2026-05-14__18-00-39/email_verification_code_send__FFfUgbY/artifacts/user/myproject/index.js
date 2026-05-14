const fs = require('fs');
const { WorkOS } = require('@workos-inc/node');

const apiKey = process.env.WORKOS_API_KEY;
const userId = process.env.WORKOS_USER_ID;
const LOG = '/home/user/myproject/output.log';

if (!apiKey || !userId) {
  console.error('Missing WORKOS_API_KEY or WORKOS_USER_ID');
  process.exit(1);
}

const workos = new WorkOS(apiKey);

(async () => {
  try {
    const response = await workos.userManagement.sendVerificationEmail({ userId });
    // The SDK might return { user } or the user object directly depending on the version/response structure
    const user = response.user || response;
    
    if (user && user.id && user.id.startsWith('user_')) {
      fs.appendFileSync(LOG, `SUCCESS user_id=${user.id} email=${user.email}\n`);
    } else {
      throw new Error('Invalid user object in response');
    }
  } catch (err) {
    fs.appendFileSync(LOG, `FAILURE ${err.message}\n`);
    process.exit(1);
  }
})();

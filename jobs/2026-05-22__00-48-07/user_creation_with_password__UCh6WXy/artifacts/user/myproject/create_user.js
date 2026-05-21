const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');
const path = require('path');

async function main() {
  const apiKey = process.env.WORKOS_API_KEY;
  if (!apiKey) {
    throw new Error('WORKOS_API_KEY environment variable is not set');
  }

  const runId = process.env.ZEALT_RUN_ID || 'default';
  const email = `pochi-user-${runId.toLowerCase()}@pochi-benchmark.example`;
  const password = 'PochiBenchmark!2025';

  const workos = new WorkOS(apiKey);

  let user;
  try {
    user = await workos.userManagement.createUser({
      email,
      password,
      firstName: 'Pochi',
      lastName: 'Benchmark',
    });
  } catch (err) {
    const message = (err && (err.message || '')).toLowerCase();
    if (message.includes('email already exists')) {
      const list = await workos.userManagement.listUsers({ email });
      user = list.data[0];
      if (!user) {
        throw new Error(`User with email ${email} not found after 'email already exists' error`);
      }
    } else {
      throw err;
    }
  }

  const outputPath = path.join(__dirname, 'user.json');
  fs.writeFileSync(outputPath, JSON.stringify(user, null, 2));
  console.log('User written to user.json:');
  console.log(JSON.stringify(user, null, 2));
}

main().catch((err) => {
  console.error('Error:', err.message || err);
  process.exit(1);
});

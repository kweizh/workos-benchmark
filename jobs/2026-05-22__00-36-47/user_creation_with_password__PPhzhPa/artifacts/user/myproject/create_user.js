const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');
const path = require('path');

async function run() {
  const apiKey = process.env.WORKOS_API_KEY;
  const runId = process.env.ZEALT_RUN_ID || 'default';
  
  if (!apiKey) {
    console.error('WORKOS_API_KEY is not set');
    process.exit(1);
  }

  const workos = new WorkOS(apiKey);
  const email = `pochi-user-${runId.toLowerCase()}@pochi-benchmark.example`;
  const password = 'PochiBenchmark!2025';

  let user;
  try {
    user = await workos.userManagement.createUser({
      email,
      password,
      firstName: 'Pochi',
      lastName: 'Benchmark',
    });
    console.log('User created successfully');
  } catch (error) {
    // Check if error is due to email already existing
    // The WorkOS Node SDK typically throws an error with a code or message
    if (error.rawData && error.rawData.code === 'email_already_exists') {
      console.log('User already exists, fetching existing user...');
      const users = await workos.userManagement.listUsers({ email });
      if (users.data && users.data.length > 0) {
        user = users.data[0];
      } else {
        throw new Error(`User with email ${email} reported to exist but not found in list.`);
      }
    } else {
      throw error;
    }
  }

  if (user) {
    const outputPath = path.join(__dirname, 'user.json');
    fs.writeFileSync(outputPath, JSON.stringify(user, null, 2));
    console.log(`User details written to ${outputPath}`);
  }
}

run().catch((err) => {
  console.error('Error:', err);
  process.exit(1);
});

const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');
const path = require('path');

async function manageUsers() {
  const apiKey = process.env.WORKOS_API_KEY;
  const clientId = process.env.WORKOS_CLIENT_ID;

  if (!apiKey || !clientId) {
    console.error('Missing WORKOS_API_KEY or WORKOS_CLIENT_ID');
    process.exit(1);
  }

  const workos = new WorkOS(apiKey, { clientId });

  const email = `user_${Date.now()}@example.com`;
  const password = 'Password123!_Stronger_123';

  try {
    const user = await workos.userManagement.createUser({
      email,
      password,
    });

    console.log(`Created user: ${user.id}`);

    const outputPath = path.join(__dirname, 'output.txt');
    fs.writeFileSync(outputPath, user.id);
    console.log(`Saved User ID to ${outputPath}`);
  } catch (error) {
    console.error('Error creating user:', error);
    process.exit(1);
  }
}

manageUsers();

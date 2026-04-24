const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');

const workos = new WorkOS(process.env.WORKOS_API_KEY, {
  clientId: process.env.WORKOS_CLIENT_ID
});

async function main() {
  try {
    const email = `user_${Date.now()}@example.com`;
    const user = await workos.userManagement.createUser({
      email,
      password: 'Password123!',
      firstName: 'Test',
      lastName: 'User'
    });
    
    fs.writeFileSync('/home/user/project/output.txt', user.id);
    console.log(`Created user with ID: ${user.id}`);
  } catch (error) {
    console.error('Error creating user:', error);
    process.exit(1);
  }
}

main();

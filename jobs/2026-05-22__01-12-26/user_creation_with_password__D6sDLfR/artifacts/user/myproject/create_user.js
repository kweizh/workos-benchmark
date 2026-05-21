const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');
const path = require('path');

// Read environment variables
const apiKey = process.env.WORKOS_API_KEY;
const zealtRunId = process.env.ZEALT_RUN_ID || 'default';

// Validate required environment variables
if (!apiKey) {
  console.error('Error: WORKOS_API_KEY environment variable is required');
  process.exit(1);
}

// Initialize WorkOS client
const workos = new WorkOS(apiKey);

// Derive email from ZEALT_RUN_ID
const email = `pochi-user-${zealtRunId.toLowerCase()}@pochi-benchmark.example`;
const password = 'PochiBenchmark!2025';

console.log(`Creating WorkOS user with email: ${email}`);

async function createUser() {
  try {
    // Attempt to create the user
    const user = await workos.userManagement.createUser({
      email,
      password,
      firstName: 'Pochi',
      lastName: 'Benchmark',
    });

    console.log('User created successfully');
    console.log(`User ID: ${user.id}`);

    // Write user to JSON file
    const outputPath = path.join(__dirname, 'user.json');
    fs.writeFileSync(outputPath, JSON.stringify(user, null, 2));
    console.log(`User data written to: ${outputPath}`);

    return user;
  } catch (error) {
    // Check if error is due to email already existing
    if (error.message && error.message.toLowerCase().includes('email already exists')) {
      console.log('User with this email already exists, retrieving existing user...');

      try {
        // List users by email to find the existing user
        const users = await workos.userManagement.listUsers({
          email,
        });

        if (users.data && users.data.length > 0) {
          const existingUser = users.data[0];
          console.log('Retrieved existing user');
          console.log(`User ID: ${existingUser.id}`);

          // Write existing user to JSON file
          const outputPath = path.join(__dirname, 'user.json');
          fs.writeFileSync(outputPath, JSON.stringify(existingUser, null, 2));
          console.log(`User data written to: ${outputPath}`);

          return existingUser;
        } else {
          console.error('Error: Email already exists but no user found in listUsers response');
          process.exit(1);
        }
      } catch (listError) {
        console.error('Error listing users:', listError.message);
        process.exit(1);
      }
    } else {
      console.error('Error creating user:', error.message);
      if (error.stack) {
        console.error(error.stack);
      }
      process.exit(1);
    }
  }
}

// Execute the function
createUser()
  .then((user) => {
    console.log('Script completed successfully');
    console.log(`Final user ID: ${user.id}`);
    process.exit(0);
  })
  .catch((error) => {
    console.error('Unexpected error:', error);
    process.exit(1);
  });
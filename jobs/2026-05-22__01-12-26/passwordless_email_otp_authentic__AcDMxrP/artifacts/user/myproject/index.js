const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');
const path = require('path');

// Check for required environment variables
const apiKey = process.env.WORKOS_API_KEY;
const clientId = process.env.WORKOS_CLIENT_ID;

if (!apiKey || !clientId) {
  console.error('Error: WORKOS_API_KEY and WORKOS_CLIENT_ID environment variables are required');
  process.exit(1);
}

// Instantiate WorkOS with credentials
const workos = new WorkOS(apiKey, { clientId });

// Log file path
const logFilePath = path.join(__dirname, 'output.log');

// Create Magic Auth (passwordless email OTP)
async function createMagicAuth() {
  try {
    console.log('Creating Magic Auth for passwordless-otp-test@example.com...');
    
    const magicAuth = await workos.userManagement.createMagicAuth({
      email: 'passwordless-otp-test@example.com'
    });

    // Verify the response has the expected structure
    if (!magicAuth.id || !magicAuth.id.startsWith('magic_auth_')) {
      throw new Error('Invalid Magic Auth response: missing or invalid id field');
    }

    // Success - append to log file
    const logLine = `SUCCESS magic_auth_id=${magicAuth.id} email=passwordless-otp-test@example.com\n`;
    fs.appendFileSync(logFilePath, logLine);
    
    console.log('Success! Magic Auth created and logged to output.log');
    console.log(`Magic Auth ID: ${magicAuth.id}`);
    
  } catch (error) {
    // Failure - write error to log file
    const errorMessage = error.message || String(error);
    const logLine = `FAILURE ${errorMessage}\n`;
    fs.appendFileSync(logFilePath, logLine);
    
    console.error(`Error: ${errorMessage}`);
    process.exit(1);
  }
}

// Execute the function
createMagicAuth();
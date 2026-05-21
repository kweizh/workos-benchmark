const { WorkOS } = require('@workos-inc/node');

const workos = new WorkOS(process.env.WORKOS_API_KEY);

async function sendVerificationEmail() {
  try {
    const result = await workos.userManagement.sendVerificationEmail({
      userId: process.env.WORKOS_USER_ID
    });
    
    // Write the result to verification.json
    const fs = require('fs');
    fs.writeFileSync(
      '/home/user/myproject/verification.json',
      JSON.stringify(result, null, 2)
    );
    
    console.log('Verification email sent successfully. Result written to verification.json');
    return result;
  } catch (error) {
    console.error('Error sending verification email:', error);
    throw error;
  }
}

sendVerificationEmail();
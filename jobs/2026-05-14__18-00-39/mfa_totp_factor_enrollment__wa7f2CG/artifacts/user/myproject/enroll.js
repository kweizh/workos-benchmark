const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');
const path = require('path');

async function enroll() {
  const apiKey = process.env.WORKOS_API_KEY;
  if (!apiKey) {
    console.error('WORKOS_API_KEY environment variable is not set');
    process.exit(1);
  }

  const workos = new WorkOS(apiKey);

  try {
    const factor = await workos.mfa.enrollFactor({
      type: 'totp',
      issuer: 'Harbor MFA Task',
      user: 'mfa-totp-task@example.com',
    });

    const factorData = {
      id: factor.id,
      type: factor.type,
      qr_code: factor.totp.qrCode || factor.totp.qr_code,
    };

    fs.writeFileSync(
      path.join(__dirname, 'factor.json'),
      JSON.stringify(factorData, null, 2)
    );

    console.log('Factor enrolled and saved to factor.json');
    process.exit(0);
  } catch (error) {
    console.error('Error enrolling factor:', error);
    process.exit(1);
  }
}

enroll();

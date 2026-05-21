const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');
const path = require('path');

async function main() {
  const apiKey = process.env.WORKOS_API_KEY;
  if (!apiKey) {
    console.error('Error: WORKOS_API_KEY environment variable is not set.');
    process.exit(1);
  }

  const workos = new WorkOS(apiKey);

  const factor = await workos.mfa.enrollFactor({
    type: 'totp',
    issuer: 'Harbor MFA Task',
    user: 'mfa-totp-task@example.com',
  });

  const output = {
    id: factor.id,
    type: factor.type,
    qr_code: factor.totp.qrCode,
  };

  const outputPath = path.join(__dirname, 'factor.json');
  fs.writeFileSync(outputPath, JSON.stringify(output, null, 2));

  console.log('Factor enrolled successfully. Data written to factor.json');
  console.log('Factor ID:', factor.id);
}

main().catch((err) => {
  console.error('Error enrolling factor:', err);
  process.exit(1);
});

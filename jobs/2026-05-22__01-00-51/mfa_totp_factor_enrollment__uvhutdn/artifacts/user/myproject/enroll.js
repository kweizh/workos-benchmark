const { WorkOS } = require('@workos-inc/node');
const fs = require('fs/promises');

async function main() {
  const apiKey = process.env.WORKOS_API_KEY;
  if (!apiKey) {
    throw new Error('WORKOS_API_KEY environment variable is required');
  }

  const workos = new WorkOS(apiKey);

  const factor = await workos.mfa.enrollFactor({
    type: 'totp',
    issuer: 'Harbor MFA Task',
    user: 'mfa-totp-task@example.com',
  });

  const qrCode = factor.totp?.qrCode || factor.totp?.qr_code || factor.qr_code;
  if (!qrCode) {
    throw new Error('TOTP QR code was not returned by WorkOS');
  }

  const output = {
    id: factor.id,
    type: factor.type,
    qr_code: qrCode,
  };

  await fs.writeFile(
    '/home/user/myproject/factor.json',
    JSON.stringify(output, null, 2)
  );
}

main()
  .then(() => {
    process.exit(0);
  })
  .catch((error) => {
    console.error(error.message);
    process.exit(1);
  });

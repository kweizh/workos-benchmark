const fs = require('fs');
const { WorkOS } = require('@workos-inc/node');

async function main() {
  const workos = new WorkOS(process.env.WORKOS_API_KEY);
  const { token } = await workos.widgets.createToken({
    organizationId: process.env.WORKOS_ORGANIZATION_ID,
    userId: process.env.WORKOS_USER_ID,
    scopes: ['widgets:users-table:manage'],
  });
  fs.writeFileSync('/home/user/myproject/widget_token.txt', token);
}

main().catch((err) => { console.error(err); process.exit(1); });
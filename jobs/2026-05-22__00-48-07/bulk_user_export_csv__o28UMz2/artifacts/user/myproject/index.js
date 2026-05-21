'use strict';

const fs = require('fs');
const path = require('path');
const { WorkOS } = require('@workos-inc/node');

const workos = new WorkOS(process.env.WORKOS_API_KEY);

function escapeField(value) {
  const str = (value == null) ? '' : String(value);
  if (str.includes(',') || str.includes('"') || str.includes('\n')) {
    return '"' + str.replace(/"/g, '""') + '"';
  }
  return str;
}

function buildCsv(rows) {
  const header = 'id,email,first_name,last_name,created_at';
  const lines = [header];
  for (const row of rows) {
    lines.push(row.map(escapeField).join(','));
  }
  return lines.join('\n') + '\n';
}

async function main() {
  const organizationId = process.env.WORKOS_ORGANIZATION_ID;
  let after = undefined;
  const rows = [];

  while (true) {
    const page = await workos.userManagement.listUsers({
      organizationId,
      limit: 2,
      after,
    });

    for (const user of page.data) {
      rows.push([
        user.id,
        user.email,
        user.firstName,
        user.lastName,
        user.createdAt,
      ]);
    }

    const next = page.listMetadata && page.listMetadata.after;
    if (!next) break;
    after = next;
  }

  const csv = buildCsv(rows);
  const outPath = path.join(__dirname, 'users.csv');
  fs.writeFileSync(outPath, csv, { encoding: 'utf8' });
  console.log(`Wrote ${rows.length} user(s) to ${outPath}`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});

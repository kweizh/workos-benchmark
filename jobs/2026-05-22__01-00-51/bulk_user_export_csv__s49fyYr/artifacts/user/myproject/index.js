const fs = require('fs');
const { WorkOS } = require('@workos-inc/node');

const { WORKOS_API_KEY, WORKOS_ORGANIZATION_ID } = process.env;

if (!WORKOS_API_KEY || !WORKOS_ORGANIZATION_ID) {
  console.error('Missing WORKOS_API_KEY or WORKOS_ORGANIZATION_ID environment variables.');
  process.exit(1);
}

const workos = new WorkOS(WORKOS_API_KEY);

const CSV_HEADER = 'id,email,first_name,last_name,created_at';
const OUTPUT_PATH = '/home/user/myproject/users.csv';

const toCsvValue = (value) => {
  if (value === null || value === undefined) {
    return '';
  }

  const stringValue = String(value);
  if (/[",\n]/.test(stringValue)) {
    return `"${stringValue.replace(/"/g, '""')}"`;
  }

  return stringValue;
};

const buildCsvRow = (values) => values.map(toCsvValue).join(',');

const exportUsers = async () => {
  const rows = [];
  let after;

  while (true) {
    const page = await workos.userManagement.listUsers({
      organizationId: WORKOS_ORGANIZATION_ID,
      limit: 2,
      after,
    });

    page.data.forEach((user) => {
      rows.push([
        user.id,
        user.email,
        user.firstName,
        user.lastName,
        user.createdAt,
      ]);
    });

    const next = page.listMetadata && page.listMetadata.after;
    if (!next) {
      break;
    }

    after = next;
  }

  const csvLines = [CSV_HEADER, ...rows.map(buildCsvRow)];
  const csvContent = `${csvLines.join('\n')}\n`;

  fs.writeFileSync(OUTPUT_PATH, csvContent, 'utf8');
};

exportUsers()
  .then(() => {
    process.exit(0);
  })
  .catch((error) => {
    console.error('Failed to export users:', error);
    process.exit(1);
  });

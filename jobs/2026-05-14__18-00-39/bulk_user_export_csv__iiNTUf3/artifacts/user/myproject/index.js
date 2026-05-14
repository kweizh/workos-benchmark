const fs = require('fs');
const path = require('path');
const { WorkOS } = require('@workos-inc/node');

async function run() {
  const apiKey = process.env.WORKOS_API_KEY;
  const organizationId = process.env.WORKOS_ORGANIZATION_ID;

  if (!apiKey || !organizationId) {
    console.error('Missing WORKOS_API_KEY or WORKOS_ORGANIZATION_ID environment variables');
    process.exit(1);
  }

  const workos = new WorkOS(apiKey);
  let after = undefined;
  const allUsers = [];

  try {
    while (true) {
      const page = await workos.userManagement.listUsers({
        organizationId,
        limit: 2,
        after,
      });

      allUsers.push(...page.data);

      const next = page.listMetadata && page.listMetadata.after;
      if (!next) {
        break;
      }
      after = next;
    }

    const csvHeader = 'id,email,first_name,last_name,created_at';
    const csvRows = allUsers.map(user => {
      const fields = [
        user.id,
        user.email,
        user.firstName,
        user.lastName,
        user.createdAt
      ];

      return fields.map(field => {
        const val = (field === null || field === undefined) ? '' : String(field);
        if (val.includes(',') || val.includes('"') || val.includes('\n')) {
          return `"${val.replace(/"/g, '""')}"`;
        }
        return val;
      }).join(',');
    });

    const csvContent = [csvHeader, ...csvRows].join('\n') + '\n';
    const outputPath = path.join(__dirname, 'users.csv');
    fs.writeFileSync(outputPath, csvContent, 'utf8');

    console.log(`Successfully exported ${allUsers.length} users to ${outputPath}`);
  } catch (error) {
    console.error('Error exporting users:', error);
    process.exit(1);
  }
}

run();

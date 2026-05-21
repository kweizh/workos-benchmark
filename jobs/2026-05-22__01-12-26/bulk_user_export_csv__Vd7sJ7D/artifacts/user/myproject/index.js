const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');

async function main() {
  // Initialize WorkOS client with API key from environment
  const workos = new WorkOS(process.env.WORKOS_API_KEY);

  // Get organization ID from environment
  const organizationId = process.env.WORKOS_ORGANIZATION_ID;

  // Pagination variables
  let after = undefined;
  const rows = [];

  // Paginate through all users
  while (true) {
    // Fetch a page of users
    const page = await workos.userManagement.listUsers({
      organizationId,
      limit: 2,
      after
    });

    // Extract user data for each user in the page
    for (const user of page.data) {
      rows.push([
        user.id,
        user.email,
        user.firstName,
        user.lastName,
        user.createdAt
      ]);
    }

    // Check if there's a next page
    const next = page.listMetadata && page.listMetadata.after;
    if (!next) {
      break;
    }
    after = next;
  }

  // Helper function to escape CSV values according to RFC 4180
  function escapeCsvField(value) {
    // Treat null/undefined as empty string
    if (value === null || value === undefined) {
      return '';
    }

    const str = String(value);

    // If field contains comma, double quote, or newline, quote it and double internal quotes
    if (str.includes(',') || str.includes('"') || str.includes('\n')) {
      return '"' + str.replace(/"/g, '""') + '"';
    }

    return str;
  }

  // Build CSV content
  const header = ['id', 'email', 'first_name', 'last_name', 'created_at'];
  const csvLines = [header.join(',')];

  for (const row of rows) {
    const escapedRow = row.map(escapeCsvField).join(',');
    csvLines.push(escapedRow);
  }

  // Write CSV to file with UTF-8 encoding and trailing newline
  const csvContent = csvLines.join('\n') + '\n';
  fs.writeFileSync('/home/user/myproject/users.csv', csvContent, 'utf8');

  console.log(`Exported ${rows.length} users to /home/user/myproject/users.csv`);
}

main();
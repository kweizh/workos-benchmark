const fs = require('fs');
const { WorkOS } = require('@workos-inc/node');

async function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

async function main() {
  const apiKey = process.env.WORKOS_API_KEY;
  const organizationId = process.env.WORKOS_ORGANIZATION_ID;

  if (!apiKey || !organizationId) {
    console.error('WORKOS_API_KEY and WORKOS_ORGANIZATION_ID must be set');
    process.exit(1);
  }

  const workos = new WorkOS(apiKey);
  const rangeEnd = new Date();
  const rangeStart = new Date(rangeEnd.getTime() - 24 * 60 * 60 * 1000);

  console.log('Starting audit log export...');
  const created = await workos.auditLogs.createExport({
    organizationId,
    rangeStart,
    rangeEnd,
  });

  const exportId = created.id;
  console.log(`Created export ${exportId}, initial state=${created.state}`);

  const deadline = Date.now() + 5 * 60 * 1000; // 5 minutes timeout
  let current = created;

  while (current.state !== 'ready') {
    if (Date.now() > deadline) {
      console.error(`Export ${exportId} never reached ready (last state=${current.state})`);
      process.exit(2);
    }
    console.log(`Polling export ${exportId}, current state=${current.state}...`);
    await sleep(3000); // Wait 3 seconds
    current = await workos.auditLogs.getExport(exportId);
  }

  console.log(`Export ${exportId} is ready.`);
  const url = current.url;

  console.log(`Downloading CSV from ${url}...`);
  const res = await fetch(url);
  if (!res.ok) {
    console.error(`Download failed with status ${res.status}`);
    process.exit(3);
  }

  const buf = Buffer.from(await res.arrayBuffer());
  fs.writeFileSync('/home/user/myproject/audit.csv', buf);
  console.log('Successfully wrote audit.csv');

  const exportData = {
    exportId,
    state: current.state,
    url,
    rangeStart: rangeStart.toISOString(),
    rangeEnd: rangeEnd.toISOString(),
  };

  fs.writeFileSync(
    '/home/user/myproject/export.json',
    JSON.stringify(exportData, null, 2),
  );
  console.log('Successfully wrote export.json');
  console.log('Done');
}

main().catch((err) => {
  console.error('An error occurred:', err);
  process.exit(1);
});

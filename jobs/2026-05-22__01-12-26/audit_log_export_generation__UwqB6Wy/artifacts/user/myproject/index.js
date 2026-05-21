const fs = require('fs');
const { WorkOS } = require('@workos-inc/node');

async function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
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

  console.log(`Creating export for organization ${organizationId}`);
  console.log(`Range: ${rangeStart.toISOString()} to ${rangeEnd.toISOString()}`);

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

    await sleep(3000);
    current = await workos.auditLogs.getExport(exportId);
    console.log(`Polled export ${exportId}, state=${current.state}`);
  }

  const url = current.url;
  console.log(`Export ready, downloading from ${url}`);

  const res = await fetch(url);
  if (!res.ok) {
    console.error(`Download failed with status ${res.status}`);
    process.exit(3);
  }

  const buf = Buffer.from(await res.arrayBuffer());
  fs.writeFileSync('/home/user/myproject/audit.csv', buf);
  console.log(`Downloaded audit.csv (${buf.length} bytes)`);

  fs.writeFileSync(
    '/home/user/myproject/export.json',
    JSON.stringify(
      {
        exportId,
        state: current.state,
        url,
        rangeStart: rangeStart.toISOString(),
        rangeEnd: rangeEnd.toISOString(),
      },
      null,
      2,
    ),
  );
  console.log('Wrote export.json');
  console.log('Done');
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
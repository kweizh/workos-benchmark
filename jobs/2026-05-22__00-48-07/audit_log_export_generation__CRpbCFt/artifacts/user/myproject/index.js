'use strict';

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

  console.log(`Creating export for range ${rangeStart.toISOString()} → ${rangeEnd.toISOString()}`);

  const created = await workos.auditLogs.createExport({
    organizationId,
    rangeStart,
    rangeEnd,
  });

  const exportId = created.id;
  console.log(`Created export ${exportId}, initial state=${created.state}`);

  // Poll until ready, with a 5-minute deadline
  const deadline = Date.now() + 5 * 60 * 1000;
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

  console.log(`Export ${exportId} is ready, downloading CSV from URL...`);

  const url = current.url;
  const res = await fetch(url);
  if (!res.ok) {
    console.error(`Download failed with HTTP status ${res.status}`);
    process.exit(3);
  }

  const buf = Buffer.from(await res.arrayBuffer());
  fs.writeFileSync('/home/user/myproject/audit.csv', buf);
  console.log(`Wrote audit.csv (${buf.length} bytes)`);

  const exportMeta = {
    exportId,
    state: current.state,
    url,
    rangeStart: rangeStart.toISOString(),
    rangeEnd: rangeEnd.toISOString(),
  };

  fs.writeFileSync(
    '/home/user/myproject/export.json',
    JSON.stringify(exportMeta, null, 2),
  );
  console.log('Wrote export.json');
  console.log('Done.');
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});

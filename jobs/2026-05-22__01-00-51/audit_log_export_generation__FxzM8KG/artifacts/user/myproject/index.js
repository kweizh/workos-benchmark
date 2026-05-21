const fs = require('fs');
const https = require('https');
const { WorkOS } = require('@workos-inc/node');

const EXPORT_PATH = '/home/user/myproject/audit.csv';
const EXPORT_META_PATH = '/home/user/myproject/export.json';
const POLL_INTERVAL_MS = 2000;
const TIMEOUT_MS = 5 * 60 * 1000;

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

const downloadFile = (url, destinationPath) =>
  new Promise((resolve, reject) => {
    const file = fs.createWriteStream(destinationPath);
    const request = https.get(url, (response) => {
      if (response.statusCode !== 200) {
        reject(new Error(`Download failed with status ${response.statusCode}`));
        response.resume();
        return;
      }

      response.pipe(file);
      file.on('finish', () => {
        file.close(resolve);
      });
    });

    request.on('error', (err) => {
      fs.unlink(destinationPath, () => reject(err));
    });

    file.on('error', (err) => {
      fs.unlink(destinationPath, () => reject(err));
    });
  });

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

  console.log('Creating audit log export for last 24 hours...');
  const createdExport = await workos.auditLogs.createExport({
    organizationId,
    rangeStart,
    rangeEnd,
  });

  const exportId = createdExport.id;
  let currentExport = createdExport;
  console.log(`Created export ${exportId}, initial state=${currentExport.state}`);

  const deadline = Date.now() + TIMEOUT_MS;
  while (currentExport.state !== 'ready') {
    if (Date.now() > deadline) {
      console.error(
        `Export ${exportId} did not reach ready within timeout (last state=${currentExport.state})`,
      );
      process.exit(2);
    }

    await sleep(POLL_INTERVAL_MS);
    currentExport = await workos.auditLogs.getExport(exportId);
    console.log(`Polled export ${exportId}, state=${currentExport.state}`);
  }

  const { url } = currentExport;
  if (!url) {
    console.error(`Export ${exportId} is ready but missing download URL.`);
    process.exit(3);
  }

  console.log(`Downloading export to ${EXPORT_PATH}...`);
  await downloadFile(url, EXPORT_PATH);

  const metadata = {
    exportId,
    state: currentExport.state,
    url,
    rangeStart: rangeStart.toISOString(),
    rangeEnd: rangeEnd.toISOString(),
  };

  fs.writeFileSync(EXPORT_META_PATH, JSON.stringify(metadata, null, 2));
  console.log(`Wrote export metadata to ${EXPORT_META_PATH}`);
  console.log('Done.');
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});

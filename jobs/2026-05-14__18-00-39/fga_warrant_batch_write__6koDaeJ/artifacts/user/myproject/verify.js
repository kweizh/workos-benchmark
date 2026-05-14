
const fs = require('fs');
const { WorkOS } = require('@workos-inc/node');

async function main() {
  const trialId = fs.readFileSync('/logs/artifacts/trial_id', 'utf8').trim();
  const documentId = `doc-batch-${trialId}`;
  const userIds = [
    `user-batch-1-${trialId}`,
    `user-batch-2-${trialId}`,
    `user-batch-3-${trialId}`,
  ];

  const warrantsPath = '/home/user/myproject/warrants.json';
  const warrantData = JSON.parse(fs.readFileSync(warrantsPath, 'utf8'));
  const warrantToken = warrantData.warrantToken;
  if (!warrantToken || typeof warrantToken !== 'string') {
    console.error(JSON.stringify({ error: 'warrants.json missing warrantToken', warrantData }));
    process.exit(2);
  }

  const apiKey = process.env.WORKOS_API_KEY;
  if (!apiKey) {
    console.error(JSON.stringify({ error: 'WORKOS_API_KEY env var is not set in verifier' }));
    process.exit(3);
  }

  const workos = new WorkOS(apiKey);
  const results = {};
  for (const userId of userIds) {
    const checkResult = await workos.fga.check(
      {
        checks: [
          {
            resource: { resourceType: 'document', resourceId: documentId },
            relation: 'viewer',
            subject: { resourceType: 'user', resourceId: userId },
          },
        ],
      },
      { warrantToken },
    );
    results[userId] = checkResult.isAuthorized();
  }

  console.log(JSON.stringify({ documentId, results }));
}

main().catch((err) => {
  console.error(JSON.stringify({ error: String(err && err.message || err) }));
  process.exit(1);
});

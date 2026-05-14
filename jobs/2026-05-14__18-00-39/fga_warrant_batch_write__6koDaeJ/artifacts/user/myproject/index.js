const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');
const path = require('path');

async function run() {
  try {
    console.log('Starting WorkOS FGA Batch Write...');
    
    const trialIdPath = '/logs/artifacts/trial_id';
    const trialId = fs.readFileSync(trialIdPath, 'utf8').trim();
    console.log(`Using trial_id: ${trialId}`);

    if (!process.env.WORKOS_API_KEY) {
      throw new Error('WORKOS_API_KEY environment variable is not set');
    }

    const workos = new WorkOS(process.env.WORKOS_API_KEY);
    
    const documentId = `doc-batch-${trialId}`;
    const userIds = [
      `user-batch-1-${trialId}`,
      `user-batch-2-${trialId}`,
      `user-batch-3-${trialId}`
    ];

    console.log(`Granting viewer access to ${documentId} for users: ${userIds.join(', ')}`);

    const response = await workos.fga.batchWriteWarrants(
      userIds.map((uid) => ({
        op: 'CREATE',
        resource: { resourceType: 'document', resourceId: documentId },
        relation: 'viewer',
        subject: { resourceType: 'user', resourceId: uid },
      })),
    );

    console.log('Batch write successful. Writing response to warrants.json...');
    
    const outputPath = '/home/user/myproject/warrants.json';
    fs.writeFileSync(outputPath, JSON.stringify(response, null, 2));
    
    console.log(`Response saved to ${outputPath}`);
    process.exit(0);
  } catch (error) {
    console.error('Error executing batch write:', error);
    process.exit(1);
  }
}

run();

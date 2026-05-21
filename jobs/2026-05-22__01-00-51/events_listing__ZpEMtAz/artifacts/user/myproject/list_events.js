const fs = require('fs/promises');
const path = require('path');
const { WorkOS } = require('@workos-inc/node');

const apiKey = process.env.WORKOS_API_KEY;

if (!apiKey) {
  console.error('WORKOS_API_KEY environment variable is required.');
  process.exit(1);
}

const workos = new WorkOS(apiKey);

async function listEvents() {
  const { data } = await workos.events.listEvents({
    events: ['organization.created'],
    limit: 10,
  });

  const output = data.map((event) => ({
    id: String(event.id),
    event: String(event.event),
    created_at: String(event.created_at),
  }));

  const outputPath = path.join(__dirname, 'events.json');
  await fs.writeFile(outputPath, JSON.stringify(output, null, 2));
  console.log(`Wrote ${output.length} events to ${outputPath}`);
}

listEvents().catch((error) => {
  console.error('Failed to list events:', error);
  process.exit(1);
});

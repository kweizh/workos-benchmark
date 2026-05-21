const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');
const path = require('path');

const apiKey = process.env.WORKOS_API_KEY;
if (!apiKey) {
  console.error('Error: WORKOS_API_KEY environment variable is not set.');
  process.exit(1);
}

const workos = new WorkOS(apiKey);

async function main() {
  const response = await workos.events.listEvents({
    events: ['organization.created'],
    limit: 10,
  });

  const mapped = response.data.map((event) => ({
    id: String(event.id),
    event: String(event.event),
    created_at: String(event.createdAt),
  }));

  const outputPath = path.join(__dirname, 'events.json');
  fs.writeFileSync(outputPath, JSON.stringify(mapped, null, 2));

  console.log(`Wrote ${mapped.length} event(s) to events.json`);
  console.log(JSON.stringify(mapped, null, 2));
}

main().catch((err) => {
  console.error('Failed to list events:', err.message || err);
  process.exit(1);
});

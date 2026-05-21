const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');
const path = require('path');

const apiKey = process.env.WORKOS_API_KEY;
if (!apiKey) {
  console.error('WORKOS_API_KEY is not set');
  process.exit(1);
}

const workos = new WorkOS(apiKey);

async function listEvents() {
  try {
    const response = await workos.events.listEvents({
      events: ['organization.created'],
      limit: 10,
    });

    const mappedEvents = response.data.map(event => ({
      id: event.id,
      event: event.event,
      created_at: event.createdAt,
    }));

    fs.writeFileSync(
      path.join(__dirname, 'events.json'),
      JSON.stringify(mappedEvents, null, 2)
    );
    console.log('Events successfully written to events.json');
  } catch (error) {
    console.error('Error listing events:', error);
    process.exit(1);
  }
}

listEvents();

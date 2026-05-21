const { WorkOS } = require('@workos-inc/node');

// Read WORKOS_API_KEY and instantiate the SDK
const apiKey = process.env.WORKOS_API_KEY;

if (!apiKey) {
  console.error('Error: WORKOS_API_KEY environment variable is not set');
  process.exit(1);
}

const workos = new WorkOS(apiKey);

// Call workos.events.listEvents with the specified filter
async function listEvents() {
  try {
    console.log('Fetching organization.created events...');
    
    const response = await workos.events.listEvents({
      events: ['organization.created'],
      limit: 10
    });

    // Check the response structure
    const eventsList = response.data || response.list || response;
    
    console.log(`Found ${eventsList.length} events`);

    // Map each event to { id, event, created_at } (strings)
    const events = eventsList.map(event => ({
      id: String(event.id),
      event: String(event.event),
      created_at: String(event.createdAt)
    }));

    // Write the JSON array to events.json
    const fs = require('fs');
    const path = require('path');
    
    const filePath = path.join(__dirname, 'events.json');
    fs.writeFileSync(filePath, JSON.stringify(events, null, 2), 'utf-8');
    
    console.log(`Successfully wrote ${events.length} events to ${filePath}`);
  } catch (error) {
    console.error('Error fetching events:', error.message);
    process.exit(1);
  }
}

listEvents();
const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');
const path = require('path');

const LOG_PATH = '/home/user/myproject/events.log';
const workos = new WorkOS(process.env.WORKOS_API_KEY);

async function main() {
  // Ensure the directory exists
  const dir = path.dirname(LOG_PATH);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }

  // Clear existing contents of the log file at the start of every run
  fs.writeFileSync(LOG_PATH, '');

  let after;
  while (true) {
    const params = { events: ['dsync.user.created'], limit: 2 };
    if (after) {
      params.after = after;
    }

    const response = await workos.events.listEvents(params);

    for (const evt of response.data) {
      // The event type is in evt.event according to the prompt's example
      fs.appendFileSync(LOG_PATH, `${evt.id} ${evt.event}\n`);
    }

    const next = response.listMetadata && response.listMetadata.after;
    
    // Continue until the response contains no more events or list_metadata.after is missing/empty
    if (!next || response.data.length === 0) {
      break;
    }
    
    after = next;
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});

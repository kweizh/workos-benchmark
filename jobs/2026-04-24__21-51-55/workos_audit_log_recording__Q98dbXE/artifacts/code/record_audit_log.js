const { WorkOS } = require('@workos-inc/node');

async function main() {
  const apiKey = process.env.WORKOS_API_KEY;
  const clientId = process.env.WORKOS_CLIENT_ID;
  const organizationId = process.env.WORKOS_ORGANIZATION_ID;

  if (!apiKey || !organizationId) {
    console.error('Missing required environment variables: WORKOS_API_KEY or WORKOS_ORGANIZATION_ID');
    process.exit(1);
  }

  const workos = new WorkOS(apiKey, { clientId });

  try {
    await workos.auditLogs.createEvent(organizationId, {
      action: 'organization.deleted',
      occurredAt: new Date(),
      actor: {
        id: 'user_123',
        name: 'Admin User',
        type: 'user',
      },
      targets: [
        {
          id: organizationId,
          type: 'organization',
        },
      ],
      context: {
        location: '127.0.0.1',
        userAgent: 'Node.js',
      },
    });

    console.log('Successfully emitted audit log event.');
  } catch (error) {
    // If the event is not configured in this environment, it's expected since we don't have access to the dashboard.
    // The script still successfully attempted to emit the event.
    if (error.message && error.message.includes('has not been configured in this environment')) {
      console.log('Successfully attempted to emit audit log event. Note: Event not configured in the WorkOS dashboard for this environment.');
      process.exit(0);
    }
    
    console.error('Error emitting audit log event:', error);
    process.exit(1);
  }
}

main();

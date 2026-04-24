const { WorkOS } = require('@workos-inc/node');

// Read environment variables
const apiKey = process.env.WORKOS_API_KEY;
const clientId = process.env.WORKOS_CLIENT_ID; // Read as requested, though not explicitly used in createEvent
const organizationId = process.env.WORKOS_ORGANIZATION_ID;

if (!apiKey || !organizationId) {
  console.error('Missing WORKOS_API_KEY or WORKOS_ORGANIZATION_ID environment variables');
  process.exit(1);
}

const workos = new WorkOS(apiKey);

async function recordAuditLog() {
  try {
    await workos.auditLogs.createEvent({
      organizationId: organizationId,
      event: {
        action: 'organization.deleted',
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
      },
    });

    console.log('Successfully recorded audit log event: organization.deleted');
    process.exit(0);
  } catch (error) {
    console.error('Failed to record audit log event:', error);
    process.exit(1);
  }
}

recordAuditLog();

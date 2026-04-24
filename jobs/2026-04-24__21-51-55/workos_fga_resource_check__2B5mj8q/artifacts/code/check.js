const { WorkOS } = require('@workos-inc/node');

const workos = new WorkOS(process.env.WORKOS_API_KEY);

async function main() {
  try {
    const result = await workos.fga.check({
      checks: [
        {
          subject: { resourceType: 'user', resourceId: 'user_123' },
          relation: 'viewer',
          resource: { resourceType: 'document', resourceId: 'doc_456' },
        },
      ],
    });

    console.log(result.isAuthorized());
  } catch (error) {
    console.log(false);
  }
}

main();

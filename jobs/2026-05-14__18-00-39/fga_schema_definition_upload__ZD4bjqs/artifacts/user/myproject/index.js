const fs = require('fs');
const { WorkOS } = require('@workos-inc/node');

const apiKey = process.env.WORKOS_API_KEY;
if (!apiKey) {
  console.error('WORKOS_API_KEY env var is required');
  process.exit(1);
}

// Construct the SDK client just to validate the key shape; the actual
// schema mutation goes through the REST endpoint because the Node SDK
// does not expose batchUpdateResourceTypes/listResourceTypes directly.
const workos = new WorkOS(apiKey);
void workos;

const resourceTypes = [
  { type: 'user', relations: {} },
  {
    type: 'folder',
    relations: {
      parent: { allowed_types: ['folder'] },
      viewer: { allowed_types: ['user'] },
    },
  },
  {
    type: 'document',
    relations: {
      parent: { allowed_types: ['folder'] },
      viewer: {
        allowed_types: ['user'],
        inherit_if: 'viewer',
        of_type: 'folder',
        with_relation: 'parent',
      },
    },
  },
];

const baseUrl = 'https://api.workos.com';
const authHeaders = {
  Authorization: `Bearer ${apiKey}`,
  'Content-Type': 'application/json',
  'User-Agent': 'workos-benchmark-fga-schema/1.0',
};

(async () => {
  try {
    console.log('Applying schema to WorkOS FGA...');
    const putResp = await fetch(`${baseUrl}/fga/v1/resource-types`, {
      method: 'PUT',
      headers: authHeaders,
      body: JSON.stringify({ resource_types: resourceTypes }),
    });

    if (!putResp.ok) {
      const errorBody = await putResp.text();
      console.error('PUT failed', putResp.status, errorBody);
      process.exit(2);
    }
    console.log('Schema applied successfully:', putResp.status);

    console.log('Fetching applied schema...');
    const getResp = await fetch(`${baseUrl}/fga/v1/resource-types?limit=100`, {
      method: 'GET',
      headers: { Authorization: authHeaders.Authorization },
    });

    if (!getResp.ok) {
      const errorBody = await getResp.text();
      console.error('GET failed', getResp.status, errorBody);
      process.exit(3);
    }

    const body = await getResp.json();
    fs.writeFileSync('/home/user/myproject/schema.json', JSON.stringify(body, null, 2));
    console.log('Successfully wrote schema.json to /home/user/myproject/schema.json');
    process.exit(0);
  } catch (error) {
    console.error('An unexpected error occurred:', error);
    process.exit(4);
  }
})();

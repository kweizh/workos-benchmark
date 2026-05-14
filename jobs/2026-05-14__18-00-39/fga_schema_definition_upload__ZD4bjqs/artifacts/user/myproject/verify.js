
const apiKey = process.env.WORKOS_API_KEY;
if (!apiKey) {
  console.error(JSON.stringify({ error: 'WORKOS_API_KEY env var is not set in verifier' }));
  process.exit(2);
}

(async () => {
  try {
    const resp = await fetch('https://api.workos.com/fga/v1/resource-types?limit=100', {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${apiKey}`,
        'User-Agent': 'workos-benchmark-fga-schema-verifier/1.0',
      },
    });
    const text = await resp.text();
    if (!resp.ok) {
      console.error(JSON.stringify({ error: 'GET /fga/v1/resource-types failed', status: resp.status, body: text }));
      process.exit(3);
    }
    let payload;
    try {
      payload = JSON.parse(text);
    } catch (e) {
      console.error(JSON.stringify({ error: 'response was not JSON', body: text }));
      process.exit(4);
    }
    console.log(JSON.stringify(payload));
  } catch (err) {
    console.error(JSON.stringify({ error: String(err && err.message || err) }));
    process.exit(1);
  }
})();

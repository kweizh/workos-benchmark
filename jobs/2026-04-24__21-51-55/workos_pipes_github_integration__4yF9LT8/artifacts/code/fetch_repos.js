const fs = require('fs');
const { WorkOS } = require('@workos-inc/node');
const axios = require('axios');

async function main() {
  const apiKey = process.env.WORKOS_API_KEY;
  const clientId = process.env.WORKOS_CLIENT_ID;

  if (!apiKey || !clientId) {
    console.error('WORKOS_API_KEY and WORKOS_CLIENT_ID must be set');
    process.exit(1);
  }

  const workos = new WorkOS(apiKey, { clientId });

  const userId = fs.readFileSync('/home/user/myproject/user_id.txt', 'utf8').trim();

  try {
    const tokenResponse = await workos.pipes.getAccessToken({
      provider: 'github',
      userId: userId,
    });

    const accessToken = tokenResponse.accessToken || tokenResponse.token;
    if (!accessToken) {
      throw new Error('Access token not found in response: ' + JSON.stringify(tokenResponse));
    }

    const githubResponse = await axios.get('https://api.github.com/user/repos', {
      headers: {
        Authorization: `Bearer ${accessToken}`,
        Accept: 'application/vnd.github.v3+json',
      },
    });

    const repos = githubResponse.data.map((repo) => repo.name);

    fs.writeFileSync('/home/user/myproject/repos.json', JSON.stringify(repos, null, 2));

    // Save artifacts
    fs.mkdirSync('/logs/artifacts/code', { recursive: true });
    fs.copyFileSync('/home/user/myproject/fetch_repos.js', '/logs/artifacts/code/fetch_repos.js');
    fs.copyFileSync('/home/user/myproject/repos.json', '/logs/artifacts/code/repos.json');

    console.log('Successfully fetched repos');
  } catch (error) {
    console.error('Error:', error.response ? error.response.data : error.message);
    process.exit(1);
  }
}

main();

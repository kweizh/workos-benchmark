const { WorkOS } = require('@workos-inc/node');
const fs = require('fs');
const path = require('path');

const WORKOS_API_KEY = process.env.WORKOS_API_KEY;
const WORKOS_CLIENT_ID = process.env.WORKOS_CLIENT_ID;

if (!WORKOS_API_KEY || !WORKOS_CLIENT_ID) {
  console.error('Missing WORKOS_API_KEY or WORKOS_CLIENT_ID environment variables');
  process.exit(1);
}

const workos = new WorkOS(WORKOS_API_KEY, {
  clientId: WORKOS_CLIENT_ID,
});

async function fetchRepos() {
  try {
    const userId = fs.readFileSync(path.join(__dirname, 'user_id.txt'), 'utf8').trim();

    console.log(`Fetching access token for user: ${userId}`);
    const { accessToken } = await workos.pipes.getAccessToken({
      provider: 'github',
      userId,
    });

    console.log('Fetching repositories from GitHub...');
    const response = await fetch('https://api.github.com/user/repos', {
      headers: {
        Authorization: `Bearer ${accessToken}`,
        'User-Agent': 'WorkOS-Pipes-Integration',
      },
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`GitHub API error: ${response.status} ${errorText}`);
    }

    const repos = await response.json();
    const repoNames = repos.map((repo) => repo.name);

    fs.writeFileSync(
      path.join(__dirname, 'repos.json'),
      JSON.stringify(repoNames, null, 2),
    );

    console.log(`Successfully saved ${repoNames.length} repository names to repos.json`);
  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

fetchRepos();

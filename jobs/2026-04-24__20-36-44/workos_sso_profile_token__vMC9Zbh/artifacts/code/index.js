const { WorkOS } = require('@workos-inc/node');

const workos = new WorkOS(process.env.WORKOS_API_KEY);
const clientId = process.env.WORKOS_CLIENT_ID;

async function getSSOProfileAndToken(code) {
  try {
    const profileAndToken = await workos.sso.getProfileAndToken({
      code,
      clientId,
    });
    return profileAndToken;
  } catch (error) {
    console.error('Error fetching SSO profile and token:', error);
    throw error;
  }
}

module.exports = { getSSOProfileAndToken };

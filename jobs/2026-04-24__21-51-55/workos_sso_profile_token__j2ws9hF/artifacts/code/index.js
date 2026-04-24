const { WorkOS } = require('@workos-inc/node');

const workos = new WorkOS(process.env.WORKOS_API_KEY);

async function getSSOProfileAndToken(code) {
  const profileAndToken = await workos.sso.getProfileAndToken({
    code,
    clientId: process.env.WORKOS_CLIENT_ID,
  });

  return profileAndToken;
}

module.exports = {
  getSSOProfileAndToken,
};

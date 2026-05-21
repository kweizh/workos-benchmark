const fs = require('fs');
const path = require('path');
const { WorkOS } = require('@workos-inc/node');

const requiredEnvVars = [
  'WORKOS_API_KEY',
  'WORKOS_ORGANIZATION_ID',
  'WORKOS_NEW_DOMAIN',
];

for (const envVar of requiredEnvVars) {
  if (!process.env[envVar]) {
    console.error(`Missing required environment variable: ${envVar}`);
    process.exit(1);
  }
}

const workos = new WorkOS(process.env.WORKOS_API_KEY);

const buildNewDomain = () => {
  if (process.env.ZEALT_RUN_ID) {
    return `${process.env.ZEALT_RUN_ID}.${process.env.WORKOS_NEW_DOMAIN}`;
  }

  return process.env.WORKOS_NEW_DOMAIN;
};

const getDomainData = (organization, newDomain) => {
  const existingDomainData = Array.isArray(organization.domainData)
    ? organization.domainData
    : [];

  const domainSet = new Set(
    existingDomainData.map((domain) => domain.domain.toLowerCase())
  );

  if (domainSet.has(newDomain.toLowerCase())) {
    return existingDomainData;
  }

  return [
    ...existingDomainData,
    {
      domain: newDomain,
      state: 'pending',
    },
  ];
};

const main = async () => {
  const organization = await workos.organizations.getOrganization(
    process.env.WORKOS_ORGANIZATION_ID
  );

  const newDomain = buildNewDomain();
  const domainData = getDomainData(organization, newDomain);

  const updatedOrganization = await workos.organizations.updateOrganization({
    organization: process.env.WORKOS_ORGANIZATION_ID,
    domainData,
  });

  const outputPath = path.join(__dirname, 'org.json');
  fs.writeFileSync(
    outputPath,
    JSON.stringify(updatedOrganization, null, 2),
    'utf-8'
  );
};

main().catch((error) => {
  console.error('Failed to update organization domains:', error);
  process.exit(1);
});

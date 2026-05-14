import { WorkOS } from '@workos-inc/node';
import { writeFileSync } from 'node:fs';

const workos = new WorkOS(process.env.WORKOS_API_KEY);
workos.portal = workos.adminPortal;
const organizationId = process.env.WORKOS_ORGANIZATION_ID;

const { link } = await workos.portal.generateLink({
  organization: organizationId,
  intent: 'sso',
});

writeFileSync('/home/user/myproject/portal_link.txt', link + '\n');
console.log(link);

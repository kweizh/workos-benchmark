# WorkOS SSO Organization Mapping

## Background
Implement a flow that automatically assigns users to a specific WorkOS organization based on their email domain during SSO login. 
When a user logs in via SSO, their email domain should be mapped to the correct organization ID using the WorkOS API.

## Requirements
- Create a script or application in `/home/user/workos_sso_org_mapping` that handles the SSO callback.
- The script should extract the user's email domain from the SSO profile.
- Look up the corresponding WorkOS organization for that domain.
- Map the user to the organization.
- Output the mapping result to `/home/user/workos_sso_org_mapping/output.log`.

## Constraints
- Project path: `/home/user/workos_sso_org_mapping`
- Log file: `/home/user/workos_sso_org_mapping/output.log`
- Use real WorkOS API keys (`WORKOS_API_KEY`, `WORKOS_CLIENT_ID`) from the environment.
- Do not mock any dependencies.

### 1. Library Overview
*   **Description**: WorkOS is a developer-friendly platform providing "Enterprise Ready" features for B2B SaaS applications. It abstracts the complexity of enterprise identity and compliance into a set of clean APIs.
*   **Ecosystem Role**: It serves as the bridge between modern SaaS applications and legacy enterprise infrastructure (Okta, Azure AD, Ping Identity). It is frequently used alongside frameworks like Next.js, Remix, and Astro to provide enterprise-grade authentication and provisioning.
*   **Project Setup**:
    1.  **CLI (Recommended)**: Run `npx workos@latest install` to automatically detect your framework (Next.js, React, etc.), install the appropriate SDK, and scaffold authentication routes.
    2.  **Manual SDK Installation**: `npm install @workos-inc/node` (for backend) or `@workos-inc/authkit-nextjs` (for Next.js).
    3.  **Configuration**: Requires `WORKOS_API_KEY` and `WORKOS_CLIENT_ID` from the WorkOS Dashboard.
### 2. Core Primitives & APIs
*   **AuthKit**: A hosted, customizable authentication UI that supports email/password, magic links, and SSO.
    *   [Documentation](https://workos.com/docs/authkit)
    *   `workos.userManagement.getAuthorizationUrl({ provider: 'authkit', ... })`
*   **Single Sign-On (SSO)**: SAML and OIDC integration for enterprise customers.
    *   [Documentation](https://workos.com/docs/sso)
    *   `workos.sso.getProfileAndToken({ code, clientId })`
*   **Directory Sync (SCIM)**: Automatic user provisioning and deprovisioning from services like Okta or Azure AD.
    *   [Documentation](https://workos.com/docs/directory-sync)
    *   `workos.directorySync.listUsers({ directory: 'dir_...' })`
*   **Admin Portal**: A self-service UI for your customers to configure their own SSO and Directory Sync.
    *   [Documentation](https://workos.com/docs/admin-portal)
    *   `workos.portal.generateLink({ organization, intent: 'sso' })`
*   **Fine-Grained Authorization (FGA)**: Relationship-based access control (ReBAC) for resource-level permissions.
    *   [Documentation](https://workos.com/docs/fga)
    *   `workos.authorization.check({ organizationMembershipId, permissionSlug, resourceId, resourceTypeSlug })`
*   **Pipes**: A unified API to connect to third-party data providers (GitHub, Slack, Salesforce) without managing OAuth flows.
    *   [Documentation](https://workos.com/docs/pipes)
    *   `workos.pipes.getAccessToken({ provider, userId })`
### 3. Real-World Use Cases & Templates
*   **Next.js AuthKit Example**: [GitHub Repo](https://github.com/workos/next-authkit-example) - Demonstrates full-stack authentication in a Next.js App Router environment.
*   **FGA Row-Level Security**: [GitHub Repo](https://github.com/workos/fga-row-level-access-control-postgres) - Shows how to use FGA with Postgres for granular permissions in a ticketing system.
*   **RAG Security with FGA**: [Blog/Code](https://workos.com/blog/how-to-secure-rag-applications-with-fine-grained-authorization-tutorial-with-code) - Example of securing vector search results in AI applications.
### 4. Developer Friction Points
*   **Webhook Verification**: Correctly validating signatures for Directory Sync events can be tricky, especially in serverless environments where raw body access is required. [Issue Example](https://github.com/workos/workos-node/issues/520)
*   **Customization Limits**: AuthKit is highly optimized but lacks deep UI customization for non-standard flows (e.g., custom multi-step onboarding).
*   **Multi-tenant Logic**: Developers often struggle with mapping WorkOS `organizations` to their own internal database models, particularly when handling "Just-in-Time" (JIT) provisioning.
### 5. Evaluation Ideas
*   **AuthKit Integration**: Implement a complete sign-in/sign-out flow in a Next.js application using the WorkOS CLI.
*   **SSO Organization Mapping**: Create a flow that automatically assigns users to a specific WorkOS organization based on their email domain during login.
*   **Directory Sync Webhooks**: Build a webhook handler that synchronizes user status (active/suspended) from WorkOS to a local PostgreSQL database.
*   **Self-Service Admin Portal**: Implement a "Settings" page where organization admins can generate a secure link to configure their own SAML connection.
*   **FGA Document Permissions**: Model a "Document Sharing" system with 'owner', 'editor', and 'viewer' roles where permissions are inherited across a folder hierarchy.
*   **Pipes Data Integration**: Develop a feature that uses WorkOS Pipes to fetch and display a user's GitHub repositories.
*   **Step-up MFA**: Implement a security-sensitive route that requires a user to complete an MFA challenge (TOTP or SMS) even if they are already logged in.
*   **Audit Log Recording**: Integrate the Audit Logs API to record and categorize administrative actions like "Organization Deleted" or "Permission Changed."
### 6. Sources
1.  [WorkOS Official Documentation](https://workos.com/docs) - Primary source for API references and guides.
2.  [WorkOS llms.txt](https://workos.com/llms.txt) - Structured overview of the documentation.
3.  [WorkOS Node.js SDK](https://github.com/workos/workos-node) - Official SDK source code and examples.
4.  [WorkOS CLI Documentation](https://workos.com/docs/authkit/cli-installer) - Details on the AI-powered installer.
5.  [WorkOS FGA Row-Level Security Example](https://github.com/workos/fga-row-level-access-control-postgres) - Real-world implementation pattern.
6.  [WorkOS Pipes Announcement](https://workos.com/changelog/pipes) - Overview of the third-party integration product.
7.  [G2 WorkOS Reviews](https://www.g2.com/products/workos/reviews) - Source for developer friction points and common complaints.
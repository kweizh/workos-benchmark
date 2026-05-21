# WorkOS FGA Role Inheritance

## Background
You are building a document management system that requires Fine-Grained Authorization (FGA). You have decided to use WorkOS FGA to manage permissions. The system features folders and documents, where documents reside inside folders, and users can be assigned roles on either folders or documents.

## Requirements
You must write a Node.js script `setup_fga.js` in `/home/user/app` that uses the `@workos-inc/node` SDK to configure the FGA schema and verify role inheritance.

1.  **Schema Definition**:
    *   Define a `folder` resource type with roles: `viewer`, `editor`, `owner`.
    *   Define a `document` resource type with roles: `viewer`, `editor`, `owner`.
    *   A `document` has a `parent_folder` relation pointing to a `folder`.
    *   Permissions on `document`:
        *   `read`: allowed for document's `viewer`, `editor`, `owner`, AND inherited from `parent_folder`'s `viewer`, `editor`, `owner`.
        *   `write`: allowed for document's `editor`, `owner`, AND inherited from `parent_folder`'s `editor`, `owner`.
        *   `delete`: allowed for document's `owner`, AND inherited from `parent_folder`'s `owner`.

2.  **Operations**:
    The script must perform the following operations programmatically using the WorkOS SDK:
    *   Initialize the WorkOS client using the `WORKOS_API_KEY` environment variable.
    *   Create or update the resource types (`folder` and `document`) with the specified schema.
    *   Create a folder resource with ID `folder_sales_2024`.
    *   Create a document resource with ID `doc_q1_report` and set its `parent_folder` to `folder_sales_2024`.
    *   Assign a user (user ID: `user_alice_123`) the `viewer` role on `folder_sales_2024`.
    *   Assign a user (user ID: `user_bob_456`) the `editor` role on `doc_q1_report`.
    *   Query the WorkOS API to check if `user_alice_123` has the `read` permission on `doc_q1_report`.
    *   Query the WorkOS API to check if `user_bob_456` has the `delete` permission on `doc_q1_report`.
    *   Write the boolean results of these two checks to a file named `results.json` in the format:
        `{"alice_can_read": true/false, "bob_can_delete": true/false}`

## Constraints
*   Project path: `/home/user/app`
*   Use the official `@workos-inc/node` SDK.
*   Do not mock any API calls; use the real WorkOS API.
*   The script must be executable via `node setup_fga.js`.
# WorkOS FGA Document Permissions

## Background
You are building a document sharing system using WorkOS Fine-Grained Authorization (FGA). The system has folders and documents, and permissions should be inherited across the folder hierarchy.

## Requirements
1. Initialize a Node.js project in `/home/user/fga-project` and install the WorkOS Node.js SDK.
2. Write a script `setup_fga.js` that uses the WorkOS Node.js SDK to:
   - Create a folder resource `folder_456`.
   - Create a document resource `doc_123` inside `folder_456`.
   - Grant user `user_alice` the `editor` role on `folder_456`.
   - Grant user `user_bob` the `viewer` role on `doc_123`.
3. Write a script `check_permissions.js` that uses the WorkOS Node.js SDK to:
   - Check if `user_alice` has `editor` access to `doc_123` (should be true due to inheritance).
   - Check if `user_bob` has `editor` access to `doc_123` (should be false).
   - Check if `user_bob` has `viewer` access to `doc_123` (should be true).
   - Output the results as JSON to `/home/user/output.json`.

## Constraints
- Project path: /home/user/fga-project
- Log file: /home/user/output.json
- Use real WorkOS API keys (`WORKOS_API_KEY`, `WORKOS_CLIENT_ID`) from the environment.
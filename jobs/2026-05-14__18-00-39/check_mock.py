import json
with open("task_analysis.json") as f:
    data = json.load(f)

for k in ["password_reset_email_send", "roles_creation_and_assignment", "user_invitation_creation", "widgets_users_table_token"]:
    if k in data:
        print(f"=== {k} ===")
        print(data[k]["test_content"][:500])
        if "mock" in data[k]["test_content"]:
            lines = [l for l in data[k]["test_content"].split('\n') if "mock" in l]
            print("Mock lines:", lines)

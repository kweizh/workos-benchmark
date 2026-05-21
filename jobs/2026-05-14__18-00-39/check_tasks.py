import os
import json

tasks_dir = "../../tasks"
task_dirs = os.listdir(tasks_dir)

results = {}

for t in task_dirs:
    p = os.path.join(tasks_dir, t)
    if not os.path.isdir(p): continue
    
    test_file = os.path.join(p, "tests", "test_final_state.py")
    if os.path.exists(test_file):
        with open(test_file, "r") as f:
            content = f.read()
            results[t] = {
                "has_subprocess": "subprocess" in content or "exec" in content or "run" in content,
                "has_mock": "mock" in content or "patch" in content,
                "test_content": content
            }

with open("task_analysis.json", "w") as f:
    json.dump(results, f, indent=2)


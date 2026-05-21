import json

with open("task_analysis.json") as f:
    data = json.load(f)

for k, v in data.items():
    print(f"{k}: subproc={v['has_subprocess']}, mock={v['has_mock']}")

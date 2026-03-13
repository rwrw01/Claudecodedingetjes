import os
import urllib.request
import json

api_key = os.environ.get("DEEPSEEK_API_KEY", "")
req = urllib.request.Request(
    "https://api.deepseek.com/models",
    headers={"Authorization": f"Bearer {api_key}"},
)
with urllib.request.urlopen(req) as resp:
    print(json.dumps(json.loads(resp.read()), indent=2))

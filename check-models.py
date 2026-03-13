import urllib.request
import json

req = urllib.request.Request(
    "https://api.deepseek.com/models",
    headers={"Authorization": "Bearer sk-69d4523bf8604822a321e1c0e5fb1d0c"},
)
with urllib.request.urlopen(req) as resp:
    print(json.dumps(json.loads(resp.read()), indent=2))

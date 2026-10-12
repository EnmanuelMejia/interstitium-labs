import json

path = "/home/hatch/workspace/apex-audit/docs/university/data/courses/stories/il-14-sre-devops-cloud-security-interview-prep-stories.json"
text = open(path).read()
fixed = text.replace('"figures":[],""hook"', '"figures": [], "hook"')
assert fixed != text, "no replacements made"
open(path, "w").write(fixed)
d = json.load(open(path))
print("OK:", len(d["stories"]), "stories")
for s in d["stories"]:
    assert set(s.keys()) == {"id","course","moduleId","title","hook","narrative","bridge","figures","verifiedClaims"}, s["id"]
    assert 300 <= len(s["narrative"].split()) <= 700, (s["id"], len(s["narrative"].split()))
print("schema + word-count checks passed")

#!/usr/bin/env python3
"""Assemble IL-27 labs.json from fragments. Validates with json.load."""
import json, os

BASE = "/home/hatch/workspace/apex-audit/docs/university/data/courses/_il27-build"

def frag(name):
    with open(os.path.join(BASE, name)) as f:
        return json.load(f)

labs = {}
labs["installLabs"] = frag("frag_install_labs.json")

ts = frag("frag_tool_script_labs.json")
labs["toolLabs"] = ts["toolLabs"]
labs["scriptLabs"] = ts["scriptLabs"]

labs["terminalSims"] = frag("frag_terminal_sims.json")

sb = frag("frag_scenarios_branching.json")
labs["scenarios"] = sb["scenarios"]
labs["branchingScenarios"] = sb["branchingScenarios"]

ct = frag("frag_click_train_mock_anim.json")
labs["clickSims"] = ct["clickSims"]
labs["trainers"] = ct["trainers"]
labs["mockTasks"] = ct["mockTasks"]
labs["animations"] = ct["animations"]

ap = frag("frag_adaptive_packs.json")
labs["mathLab"] = ap["mathLab"]
labs["scriptingLab"] = ap["scriptingLab"]

out = os.path.join(BASE, "labs.json")
with open(out, "w") as f:
    json.dump(labs, f, indent=1)

# validate: re-read from disk
with open(out) as f:
    check = json.load(f)

print("keys:", list(check.keys()))
for k, v in check.items():
    n = len(v) if isinstance(v, (list, dict)) else v
    print(f"  {k}: {n}")

# shape spot-checks
il = check["installLabs"][0]
assert set(["id","tool","category","moduleId","estimatedMinutes","gates","platforms","checkpoints","troubleshoot","costNote"]) <= set(il), "installLab shape"
assert isinstance(il["platforms"], list) and isinstance(il["gates"], list)
assert set(il["checkpoints"][0]) >= {"command", "expected"}
t = check["terminalSims"][0]
assert set(["id","title","brief","prompt","commands"]) <= set(t)
assert set(t["commands"][0]) == {"cmd", "out"}
b = check["branchingScenarios"][0]
assert set(["id","moduleId","title","start","nodes"]) <= set(b)
node = b["nodes"][b["start"]]
assert "text" in node and "choices" in node
assert all({"label","next","feedback"} <= set(c) for c in node["choices"])
c = check["clickSims"][0]
assert set(["id","moduleId","title","steps"]) <= set(c)
assert set(c["steps"][0]) >= {"screen","instruction","hotspots","feedback"}
a = check["animations"][0]
assert set(["id","moduleId","title","kind","description"]) <= set(a) and a["kind"] in ("svg","canvas")
assert set(check["mathLab"]) >= {"topics","knowledgeCheck","exerciseBank","generators","masteryModel","masteryMap","progressPersistence"}
assert set(check["scriptingLab"]) >= {"topics","knowledgeCheck","exerciseBank","generators","masteryModel","masteryMap","progressPersistence"}
tl = check["toolLabs"][0]
assert set(["id","title","chain","moduleId","requiresInstall","requiresLab","brief","steps","deliverable","checkpoint"]) <= set(tl)
sl = check["scriptLabs"][0]
assert set(["id","title","moduleId","level","brief","objectives","starterCode","solutionWalkthrough","extension"]) <= set(sl)
sc = check["scenarios"][0]
assert set(["id","moduleId","title","context","objectives","tasks"]) <= set(sc)
tr = check["trainers"][0]
assert set(["id","moduleId","title","kind","description","items"]) <= set(tr)
mk = check["mockTasks"][0]
assert set(["id","moduleId","title","kind","brief","scenario","deliverable","rubric"]) <= set(mk)

# id uniqueness within each list
for k, v in check.items():
    if isinstance(v, list) and v and isinstance(v[0], dict) and "id" in v[0]:
        ids = [x["id"] for x in v]
        assert len(ids) == len(set(ids)), f"duplicate ids in {k}"

# moduleId sanity: all IL27-M## shaped
import re
for k, v in check.items():
    if isinstance(v, list):
        for x in v:
            if isinstance(x, dict) and "moduleId" in x:
                assert re.fullmatch(r"IL27-M\d{2}", x["moduleId"]), (k, x["moduleId"])

size = os.path.getsize(out)
print(f"labs.json OK: {size} bytes, all shape checks passed")

# -*- coding: utf-8 -*-
"""Add il_provides (instructor-voice blurb) to each shard-g path. Preserves all existing data."""
import json
import os

BASE = os.path.expanduser("~/workspace/apex-audit")
SHARD = os.path.join(BASE, "docs/university/data/catalog/shard-g.json")

IL_PROVIDES = {
"sre-interview-prep": (
"I'm your instructor for this path, and here's what I give you: the reliability spine every SRE interview runs on — "
"SLIs, SLOs, and error budgets you can do on a whiteboard, incident command you can narrate minute by minute, "
"observability you can design aloud, and capacity math with the cost of every nine stated. "
"We close with six full design reps and a scored mock circuit, so you walk into the loop with the round shapes already automatic."
),
"devops-interview-prep": (
"I'm your instructor for this path, and here's what I give you: the pipeline as the artifact DevOps interviews are really about — "
"CI stages in fail-fast order, Terraform state/module/drift discipline, containers to Kubernetes, and troubleshooting narrated under time pressure. "
"You'll build a portfolio-grade platform with GitOps and docs, then run the full mock circuit: pipeline design, live debugging, and the behavioral round where ops stories win offers."
),
"cloud-interview-prep": (
"I'm your instructor for this path, and here's what I give you: the conceptual floor every cloud interview stands on — "
"regions, networking you can debug layer by layer, data services chosen by access pattern, and security controls as the trust test. "
"You'll produce one complete, costed, failure-reviewed architecture with an honest estimate, then rehearse the cloud mock circuit until cost-and-tradeoff narration is a reflex."
),
"security-eng-interview-prep": (
"I'm your instructor for this path, and here's what I give you: the defender's interview toolkit — "
"the OWASP Top 10 as mechanisms and fixes, network security you can defend aloud, just-enough cryptography, detection engineering mapped to ATT&CK, and a full STRIDE-lite design review. "
"We close with the security mock circuit: secure design, attacker mindset, incident response — scored the way hiring panels score them."
),
"tech-mock-interview-circuit": (
"I'm your instructor for this final path, and here's what I give you: the dress rehearsal for the whole loop — "
"DSA speed reps with complexity stated aloud, system-design reps on the classics, a bank of ten rehearsed STAR stories, domain deep dives one level past the job post, "
"and a full simulated loop day with rubric scoring. You leave with a debrief habit, a weakness-targeting plan, and the taper that turns preparation into performance."
),
}

with open(SHARD) as f:
    d = json.load(f)

for p in d["paths"]:
    assert p["id"] in IL_PROVIDES, p["id"]
    assert isinstance(p.get("topics", None) or [t for m in p["modules"] for t in m.get("topics", [])], list)
    for m in p["modules"]:
        assert isinstance(m.get("topics"), list) and m["topics"], (p["id"], m["id"])
        for s in m.get("sources", []):
            assert s.get("name") and s.get("url") and s["url"].startswith("https://"), (p["id"], m["id"])
    p["il_provides"] = IL_PROVIDES[p["id"]]
    assert 2 <= len(p["il_provides"].split(". ")) <= 4

tmp = SHARD + ".retrofit-tmp"
with open(tmp, "w") as f:
    json.dump(d, f, indent=1, ensure_ascii=False)
    f.write("\n")
with open(tmp) as f:
    d2 = json.load(f)
assert all("il_provides" in p for p in d2["paths"])
os.replace(tmp, SHARD)
print("shard-g il_provides added to", len(d2["paths"]), "paths; WRITE OK")

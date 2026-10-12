"""Retrofit shard-k.json path entries: add topics (string list), sources
[{name,url,note}] from shard-k-sources.json, il_provides (2-3 sentence
instructor-voice blurb). All existing data preserved.
"""
import json, os

SHARD = "/home/hatch/workspace/apex-audit/docs/university/data/catalog/shard-k.json"
SRCF = "/home/hatch/workspace/apex-audit/docs/university/data/catalog/shard-k-sources.json"

shard = json.load(open(SHARD))
srcs = json.load(open(SRCF))["sources"]

BLURBS = {
"tpm-interview-prep": (
    "I'm your instructor for the TPM track, and IL-18 gives you the full program-management interview craft: "
    "program design for ambiguous mandates, execution discipline for multi-team plans, influence without authority, "
    "and the technical depth to question designs and spot integration risk. Every module ends in reps — guided "
    "program cases and a timed mock circuit — so you walk into the loop with structure under pressure."
),
"em-interview-prep": (
    "I'm your instructor for the EM track, and IL-18 trains the two halves of the engineering manager interview: "
    "people leadership — 1:1s, feedback, coaching, fair performance management — and delivery ownership — honest "
    "estimates, incident culture, and managing up with no surprises. Scenario reps and a full mock circuit turn "
    "judgment into a practiced performance."
),
"pm-interview-prep": (
    "I'm your instructor for the PM track, and IL-18 builds the product interview from the ground up: structured "
    "empathy and product sense, execution under real constraints, metrics and judgment, and behavioral stories "
    "told in tight STAR. Guided product cases and a four-round mock loop make your aloud-thinking crisp, "
    "evidence-backed, and ramble-free."
),
"technical-pm-interview-prep": (
    "I'm your instructor for the technical PM track, and IL-18 gives you enough engineering to be dangerous in "
    "the good way: how systems are built, where they break, and how to reason about scale — plus API and platform "
    "thinking and data literacy with the tools analysts actually use. Technical cases and a hybrid mock circuit "
    "calibrate your depth honestly: credible on systems, clear at the boundary."
),
"genai-for-pm": (
    "I'm your instructor for the Generative AI for PMs track, and IL-18 takes you from GenAI literacy — tokens, "
    "context, cost, and the hype filter — through LLM product patterns, evals and UX for uncertainty, a full "
    "shipping playbook, responsible risk practice, and AI roadmapping. You will size, spec, evaluate, and defend "
    "an AI feature end to end, with margins and mitigations to show for it."
),
}

for p in shard["paths"]:
    pid = p["id"]
    assert pid in BLURBS, pid
    # topics: flatten phase topics, dedupe preserving order
    topics, seen = [], set()
    for ph in p.get("phases", []):
        for t in ph.get("topics", []):
            if t not in seen:
                seen.add(t); topics.append(t)
    p["topics"] = topics
    # sources: reuse repo URLs only, filtered by used_in
    p["sources"] = [
        {"name": s["name"], "url": s["url"], "note": s["description"]}
        for s in srcs if pid in s.get("used_in", [])
    ]
    p["il_provides"] = BLURBS[pid]

for p in shard["paths"]:
    assert isinstance(p["topics"], list) and all(isinstance(t, str) for t in p["topics"]) and p["topics"]
    assert all(set(s.keys()) == {"name", "url", "note"} for s in p["sources"]) and p["sources"]
    assert isinstance(p["il_provides"], str) and len(p["il_provides"].split(". ")) >= 2

tmp = SHARD + ".tmp"
with open(tmp, "w") as f:
    json.dump(shard, f, ensure_ascii=False, indent=2)
    f.write("\n")
os.replace(tmp, SHARD)

after = json.load(open(SHARD))
for p in after["paths"]:
    print(p["id"], "| topics:", len(p["topics"]), "| sources:", len(p["sources"]), "| il_provides chars:", len(p["il_provides"]))
print("shard-k retrofit OK; all pre-existing keys preserved:", all(
    set(p.keys()) >= {"id","academy","title","subtitle","type","difficulty","hours","status","tags","suited_for","tools","phases","modules","assessments"}
    for p in after["paths"]))

"""STEP 5: shard-f.json — add path-level topics, sources, il_provides. Preserve all existing data."""
import json

BASE = "/home/hatch/workspace/apex-audit/docs/university/data/catalog"
P = BASE + "/shard-f.json"
SP = BASE + "/shard-f-sources.json"

s = json.load(open(P))
src_pool = json.load(open(SP))["sources"]

BLURBS = {
"swe-interview-foundations": ("I'm your instructor for the DSA & System Design Core — the shared spine every domain track in IL-13 stands on. "
    "We'll build complexity fluency, the array/string/graph pattern atlas, a repeatable DP method, and system-design fundamentals with estimation math you can defend. "
    "By the end, timed problems and design walkthroughs will feel like reps, not surprises."),
"backend-interview-prep": ("I'm your instructor for Backend Engineering Interview Prep. We'll take APIs, the data layer, caching and queues, concurrency, "
    "and microservices to decision depth — always arguing from access patterns and tradeoffs, never from hype. "
    "You'll leave with two documented design reps and a mock circuit that turns each round into next week's study plan."),
"frontend-interview-prep": ("I'm your instructor for Frontend Engineering Interview Prep. We'll go deep on the language, React internals, the rendering pipeline, "
    "and CSS as engineering — then practice the rounds that decide frontend offers: machine coding under a timer and client-side system design. "
    "By the end, you'll answer 'why did this re-render?' with a mechanism, not a guess."),
"fullstack-interview-prep": ("I'm your instructor for Fullstack Engineering Interview Prep. We'll hold the whole request path in one head — DNS to render — "
    "covering architecture, API styles, auth without hand-waving, data across the stack, and deployment literacy. "
    "You'll ship a contract-first capstone with CI and walk a mock circuit that crosses the stack in a single round."),
"ios-interview-prep": ("I'm your instructor for iOS Engineering Interview Prep. We'll build Swift depth, both UI worlds (UIKit and SwiftUI, honestly held), "
    "structured concurrency, the persistence ladder, and architecture argued with tradeoffs. "
    "You'll finish with a complete list-detail app — networking, cache, tests — ready to walk through as proof of platform fluency."),
"android-interview-prep": ("I'm your instructor for Android Engineering Interview Prep. We'll build Kotlin depth, the framework without folklore, modern coroutines "
    "with lifecycle-aware scopes, the persistence ladder, and offline-first architecture. "
    "You'll finish with a complete offline-first app — Retrofit, Room, Compose — built to be the centerpiece of your Android loop."),
"embedded-swe-interview-prep": ("I'm your instructor for Embedded Software Engineering Interview Prep. We'll work C at the metal, RTOS concepts, drivers and "
    "peripherals, concurrency where the stakes are hardware, and debugging as a demonstrable skill. "
    "You'll finish with a real firmware build — tasks, a driver, a power budget with honest numbers — the artifact that ends 'do you do embedded?' debates."),
"qa-test-interview-prep": ("I'm your instructor for Software Testing & QA Interview Prep. We'll start with strategy before tools — the pyramid, risk-based planning, "
    "test doubles — then cover automation frameworks at selection depth, contract testing, performance testing, and planning craft. "
    "You'll finish with a real automation suite (UI, API, CI, reports) built to be demoed, converting interviews from Q&A into show-and-tell."),
}

changed = []
for p in s["paths"]:
    pid = p["id"]
    # topics: aggregate phase topics, deduped, in order
    topics = []
    for ph in p.get("phases", []):
        for tpc in ph.get("topics", []):
            if tpc not in topics:
                topics.append(tpc)
    # sources: from the repo's sources pool for this path (reuse URLs only)
    pool = [x for x in src_pool if pid in x.get("used_in", [])]
    seen = set()
    sources = []
    for x in pool:
        if x["url"] not in seen:
            seen.add(x["url"])
            sources.append({"name": x["name"], "url": x["url"],
                            "note": x.get("description", "")})
    p["topics"] = topics
    p["sources"] = sources
    p["il_provides"] = BLURBS[pid]
    changed.append((pid, len(topics), len(sources)))

with open(P, "w") as f:
    json.dump(s, f, indent=1, ensure_ascii=False)
    f.write("\n")

s2 = json.load(open(P))
for p in s2["paths"]:
    assert isinstance(p["topics"], list) and all(isinstance(x, str) for x in p["topics"]) and p["topics"], p["id"]
    assert isinstance(p["sources"], list) and p["sources"], p["id"]
    for src in p["sources"]:
        assert set(src) == {"name", "url", "note"} and src["name"] and src["url"] and src["note"], (p["id"], src)
    assert isinstance(p["il_provides"], str) and len(p["il_provides"].split(". ")) >= 2, p["id"]
    # existing data preserved
    assert p["phases"] and p["modules"] and p["assessments"], p["id"]
print("paths retrofitted:")
for pid, nt, ns in changed:
    print(" ", pid, "topics:", nt, "sources:", ns)
print("shard-f validated")

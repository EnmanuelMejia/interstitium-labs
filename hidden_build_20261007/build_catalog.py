#!/usr/bin/env python3
"""Surgical catalog additions, format-preserving. No commit, no deploy."""
import json, re

ROOT = "/home/hatch/workspace/apex-audit"
PO = ROOT + "/docs/university/data/catalog/shard-o.json"
PL = ROOT + "/docs/university/data/catalog/shard-l.json"

ALLOWED_URLS = {
    "https://epoch.ai/publications/estimating-the-agent-population",
    "https://epoch.ai/publications",
    "https://arxiv.org/abs/2211.04325",
    "https://arxiv.org/html/2211.04325v2",
    "https://metr.org/blog/2024-11-22-evaluating-r-d-capabilities-of-llms/",
    "https://arxiv.org/abs/2411.15114",
    "https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/",
    "https://metr.org/blog/2026-1-29-time-horizon-1-1/",
}
COMPETITORS = re.compile(r"aleks|brilliant\.org|khan academy|coursera|udemy|\bedx\b|udacity|datacamp|codecademy|pluralsight|linkedin learning|masterclass|skillshare", re.I)
BANNED = re.compile(r"palantir|\bNSA\b", re.I)

SHARDO_MODULES = [
 {"id": "capability-forecasting-epoch", "title": "Frontier Capability Forecasting", "kind": "core",
  "topics": ["Forecasting from physical inputs: data stocks, chip shipments, cost curves", "The data-wall model: scaling-law demand vs. estimated supply", "Stock estimates and the 2026\u20132032 exhaustion window", "Agent-capacity estimation: A = E \u00d7 c", "Inference cost curves and the capacity-glut question", "The decay lesson: as-of dating and moving constraints"],
  "sources": [
   {"name": "Epoch AI \u2014 How many AI agents could we run?", "url": "https://epoch.ai/publications/estimating-the-agent-population", "note": "October 2026 report read in full; HBM-to-agents method and demand analysis."},
   {"name": "Epoch AI \u2014 Publications index", "url": "https://epoch.ai/publications", "note": "Live corpus index; cost curves, chip-supply tracking, adoption measurement threads."}],
  "il_provides": "The discipline of turning unobservable frontier quantities into bounded, dated forecasts: the data-wall ledger, the A = E \u00d7 c agent-capacity method, and Epoch's inference cost curves. Every figure carries its as-of date, because in capability forecasting the date is part of the claim."},
 {"id": "evaluating-ai-metr", "title": "Measuring AI Itself: RE-Bench and Time Horizons", "kind": "core",
  "topics": ["RE-Bench: 7 contamination-free ML research environments", "Calibrated scoring and the 71-attempt human baseline", "The 2h/8h/32h human-vs-agent crossover", "The time-horizon metric: P50/P80 from fitted success curves", "The ~7-month doubling trend and the TH1.1 refresh", "Reading evaluations critically: contamination, baselines, suite sensitivity"],
  "sources": [
   {"name": "METR \u2014 Evaluating frontier AI R&D capabilities (RE-Bench)", "url": "https://metr.org/blog/2024-11-22-evaluating-r-d-capabilities-of-llms/", "note": "RE-Bench release post; design, baselines, and crossover findings."},
   {"name": "METR \u2014 Measuring AI ability to complete long tasks", "url": "https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/", "note": "Time-horizon methodology and the doubling-time trend."}],
  "il_provides": "The measurement discipline behind autonomy claims: RE-Bench's head-to-head agent-vs-expert design and the time-horizon method that compresses 'how autonomous?' into a fitted number. Taught with METR's own caveats \u2014 suite-specific, dated, and never a claim about whole jobs."}
]
SHARDL_GENAI = {"id": "inference-economics-agent-capacity", "title": "Inference Economics & Agent Capacity", "kind": "elective",
 "topics": ["Epoch's agent-capacity method: A = E \u00d7 c", "Hourly agent economics: $/agent-hour by harness", "The plunging price of thought: ~47%/quarter cost curves", "Capacity glut: when demand, not chips, binds"],
 "sources": [
  {"name": "Epoch AI \u2014 How many AI agents could we run?", "url": "https://epoch.ai/publications/estimating-the-agent-population", "note": "Agent-capacity method and hourly economics (Oct 2026)."},
  {"name": "Epoch AI \u2014 Publications index", "url": "https://epoch.ai/publications", "note": "Inference cost-curve thread ('the plunging price of thought')."}],
 "il_provides": "What an agent hour actually costs and how many the buildout can serve: the serving-economics lens every production agent system needs, dated honestly."}
SHARDL_ML = {"id": "training-data-constraints", "title": "Training-Data Constraints & Scaling Laws", "kind": "elective",
 "topics": ["The data-wall paper: demand vs. supply ledgers", "Chinchilla-optimal data/compute ratios", "Quality filtering and multi-epoch adjustments", "The 2026\u20132032 exhaustion window and its caveats"],
 "sources": [
  {"name": "Villalobos et al. \u2014 Will we run out of data? (arXiv)", "url": "https://arxiv.org/abs/2211.04325", "note": "ICML 2024 position paper; stock estimates and Monte Carlo window."}],
 "il_provides": "The honest account of data as a scaling input: how much public text exists, what adjustments apply, and why the constraint moves \u2014 the scaling-law context behind every data decision."}

errors = []
def scan(o, w):
    if isinstance(o, str):
        if COMPETITORS.search(o): errors.append(f"competitor {w}: {o[:60]}")
        if BANNED.search(o): errors.append(f"banned {w}: {o[:60]}")
    elif isinstance(o, dict):
        for k, v in o.items(): scan(v, w + "." + k)
    elif isinstance(o, list):
        for i, v in enumerate(o): scan(v, f"{w}[{i}]")

for m in SHARDO_MODULES + [SHARDL_GENAI, SHARDL_ML]:
    assert m["kind"] in ("core", "elective")
    assert 4 <= len(m["topics"]) <= 6
    for s in m["sources"]:
        assert s["url"] in ALLOWED_URLS, s["url"]
    scan(m, m["id"])
assert not errors, errors

# shard-o (minified)
do = json.loads(open(PO, encoding="utf-8").read())
po = [p for p in do["paths"] if p["id"] == "il23-ai-frontier"]
assert len(po) == 1 and "modules" not in po[0]
po[0]["modules"] = SHARDO_MODULES
out = json.dumps(do, ensure_ascii=False, separators=(",", ":"))
open(PO, "w", encoding="utf-8").write(out)
json.loads(open(PO, encoding="utf-8").read())

# shard-l (2-space, literal unicode, trailing newline)
dl = json.loads(open(PL, encoding="utf-8").read())
pg = [p for p in dl["paths"] if p["id"] == "aieng-generative-ai"][0]
pm = [p for p in dl["paths"] if p["id"] == "aieng-machine-learning"][0]
assert not any(m["id"] == SHARDL_GENAI["id"] for m in pg.get("modules", []))
assert not any(m["id"] == SHARDL_ML["id"] for m in pm.get("modules", []))
pg.setdefault("modules", []).append(SHARDL_GENAI)
pm.setdefault("modules", []).append(SHARDL_ML)
outl = json.dumps(dl, ensure_ascii=False, indent=2) + "\n"
open(PL, "w", encoding="utf-8").write(outl)
json.loads(open(PL, encoding="utf-8").read())

print("catalog write OK; scan 0 hits")

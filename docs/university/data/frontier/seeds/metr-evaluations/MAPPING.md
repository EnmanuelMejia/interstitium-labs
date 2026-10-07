# 3-way mapping — METR evaluations (RE-Bench + autonomy time horizons)

**Seed:** `metr-evaluations` — METR's RE-Bench benchmark and task-time-horizon methodology

## Decision: (a) YES · (b) YES (full module) · (c) NONE

### (a) Supplemental knowledge — APPLIES

METR's evaluations are the frontier *measurement discipline*; they belong in IL-23 as core content, and they enrich the agent-engineering material in two existing courses:

- **IL-23 · Frontier Knowledge** — the time-horizon trend and RE-Bench's human-vs-agent crossover finding are canonical "state of the field" material for a frontier course. The module fragment (below) is written for IL-23.
- **IL-12 · AI Engineering** — time horizons define the practical autonomy ceiling agents can be built on: any module teaching agentic systems should cite the as-of dated P50 horizon as the reliability boundary engineers design around. Record as a recommended supplement for IL-12's agent-systems modules.
- **IL-16 · Machine Learning / AI Engineering** — RE-Bench tasks (scaling-law fitting, kernel optimization, architecture search under constraints) are concrete ML-research-engineering workflows; cite RE-Bench in IL-16's advanced ML-engineering material as the benchmark that measures agents doing that work.

### (b) Standalone CBT module — APPLIES (full module, IL-23 core)

Evaluation protocols are teachable and load-bearing: a benchmark with an explicit anti-contamination design, calibrated human baselines, and a quantitative autonomy metric is exactly the kind of frontier method IL-23 should teach learners to *use and critique*, not just hear about. The fragment teaches (1) RE-Bench's design and its 2h-vs-8h-vs-32h crossover result, (2) the time-horizon method and the ~7-month doubling trend (with the TH1.1 post-2023 acceleration), (3) what the metric does *not* claim, and (4) how to read a capability evaluation critically (suite composition, baselining quality, infrastructure effects). Fragment written at `module-metr-evaluations.json` (`id: "frontier-seed-metr-evals"`, `as_of: "2026-10-07"`, ready to append).

### (c) Certification mapping — DOES NOT APPLY

No real certification's published exam objectives cover AI capability evaluation protocols or autonomy measurement. Naming one would be invented alignment — rejected under the honesty rules.

## Why

RE-Bench is the benchmark that operationalizes the "can AI do AI R&D?" question with measured human baselines and open data, and the time-horizon trend is the single most cited quantitative summary of agentic progress. Both are primary-source, third-party verifiable, and central to how frontier labs and policymakers frame autonomy risk — a natural IL-23 core module, with genuine supplemental value for IL-12's agent-engineering and IL-16's ML-engineering tracks. No certification claims; no overlap with the X-CBT or recursive-distill pipelines (evaluation methodology, not cybersecurity chatter or course folding).

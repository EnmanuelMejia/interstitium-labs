# Seed summary — METR evaluations: RE-Bench and autonomy time horizons

**Slug:** `metr-evaluations`
**Sources (all verified live, retrieved 2026-10-07):**
- https://metr.org/blog/2024-11-22-evaluating-r-d-capabilities-of-llms/ — METR's RE-Bench release post ("Evaluating frontier AI R&D capabilities of language model agents against human experts"). Content verified: 7 environments, 71 human expert attempts, Claude 3.5 Sonnet + o1-preview results, strengths/weaknesses, benchmark comparison table.
- https://arxiv.org/abs/2411.15114 — "RE-Bench: Evaluating frontier AI R&D capabilities of language model agents against human experts" (submitted 2024-11-22, revised 2025-05-27; Wijk, Lin, Becker et al.). Content verified: abstract read, key findings recorded below.
- https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/ — "Measuring AI Ability to Complete Long Software Tasks" (Kwa et al.). Content verified: time-horizon methodology, doubling-time trend, full summary + conclusion read.
- https://metr.org/blog/2026-1-29-time-horizon-1-1/ — "Time Horizon 1.1". Content verified: TH1.1 suite changes (170→228 tasks), Vivaria→Inspect infrastructure move, updated doubling estimates.
**Disposition:** CONSUMED — processed 2026-10-07

## What it is

The public evaluation program of **METR** (the independent AI-evaluation nonprofit behind metr.org), the field's most cited source for measuring how well AI agents perform long, open-ended software and research tasks compared to human experts. This seed covers two connected outputs: **RE-Bench**, a benchmark for AI-led ML research engineering, and the **task-time-horizon** methodology, which turns "how autonomous is this model?" into a single measurable number. (All fast-moving claims below carry `as_of: 2026-10-07`.)

## RE-Bench: Research Engineering Benchmark (announced 2024-11-22)

**Design.** Seven environments built from scratch (to avoid training-data contamination), each a realistic, open-ended ML research-engineering task — e.g. fitting a scaling law, optimizing a GPU kernel, or designing a model architecture under unusual constraints. Each environment gives the agent (human or AI) a computer (often with several GPUs), a scoring function (maximize accuracy, minimize runtime), and a fixed time limit; the instruction is simply to score as high as possible. Scores are calibrated so 0 = starting score, 1 = METR's reference solution. Task realism was vetted in consultation with ML researchers at academic labs and top industry labs (Anthropic, Google DeepMind, OpenAI, per the companion commentary).

**Human baselines.** 71 paid attempts by 61 distinct human experts, each given up to 8 hours. Per the paper abstract: 82% of expert attempts reached a non-zero score and 24% matched or exceeded METR's strong reference solutions. Human experts and AI agents attempt the same environments with the same resources and information, allowing faithful head-to-head comparison. METR open-sourced the environments, the human data, the analysis code, and full agent transcripts.

**Headline findings (as_of: 2026-10-07, from the paper abstract).**
- At a **2-hour total budget** per environment, the best AI agents scored **4× higher** than human experts (best-of-k over attempts).
- Humans show **better returns to more time**: at an 8-hour budget humans narrowly exceeded the top agent scores; at 32 total hours (across attempts), humans achieved **2×** the top agent score.
- Agents iterate dramatically faster — generating and testing implementations more than ten times faster than humans, at much lower cost — but often fail to react appropriately to novel information or build coherently on earlier progress within a single run.
- Concrete example: on a prefix-sum GPU-kernel task, o1-preview wrote a custom CUDA kernel reaching 0.64 ms, beating the best human expert's 0.67 ms (starting code 4.74 ms, reference solution 1.60 ms).

**Why it exists.** Frontier AI safety policies (and the White House National Security Memorandum on AI and the EU AI Act, per METR) single out *automation of AI R&D by AI agents* as a capability of concern; RE-Bench is designed as a reusable instrument for exactly that monitoring — a measured approach to the recursive-self-improvement question rather than speculation about it.

**Self-declared limitations.** Only 7 environments (deliberately small; most are held back to stay uncontaminated); the tasks have clearer objectives and faster feedback loops (<1 hour to get signal) than real ML research, where goals are ambiguous and feedback can take months; difficulty is finite — fully saturating the benchmark would mean agents significantly outperforming top ML engineers in this setting.

## Autonomy evaluations and the time-horizon metric (2025-03-19, updated 2026-01-29)

**The metric.** METR measures a model's *time horizon*: the human-expert task length at which an agent has an x% chance of success, typically reported at the **50% (P50)** and **80% (P80)** success levels. Procedure: time human experts on a diverse suite of multi-step software/research tasks, fit a logistic curve of model success probability against human task length, and read off the task length where the curve crosses 50%. Current models succeed near 100% on tasks taking humans under 4 minutes and under 10% on tasks over ~4 hours (measured 2025-03-19; as_of: 2026-10-07).

**The trend.** The 50%-reliability task horizon for frontier models has grown exponentially: doubling roughly every **7 months** from 2019 through the 2025 measurement (P50 doubling 195.8 days, 95% CI [162, 223]). METR's sensitivity analysis found the trend robust: even a 10× error in absolute measurement shifts the arrival date of "month-long tasks" by only ~2 years. A separate replication on SWE-bench Verified found an even faster doubling of under 3 months.

**Time Horizon 1.1 (2026-01-29; as_of: 2026-10-07).** METR's first major refresh: task suite expanded from 170 to 228 tasks (+34%), with long tasks (8h+ human time) doubled from 14 to 31 (only 5 of the 31 carry measured human baselines; the rest are estimates); evaluation infrastructure moved from METR's in-house **Vivaria** (built 2023) to the UK AI Security Institute's open-source **Inspect** framework; horizons re-estimated for 14 models. Results: the long-run doubling stays ~7 months (196.5 days), but the **post-2023 trend is 20% faster** — P50 doubling of 130.8 days (95% CI [107, 161]) vs 165.3 days under TH1. METR attributes part of this to a genuinely faster recent trajectory and part to suite composition changes; new estimates fall within TH1 confidence intervals.

**Caveat carried from METR itself:** the time horizon is a fitted, suite-specific estimate of autonomous task-completion capability — not a claim about automating whole jobs or research organizations, and not evidence that models "work for 16 hours" in any ordinary sense. METR also notes measurements above ~16 hours are unreliable with the current suite.

**Adjacent context (secondary, unverified by primary read).** Third-party coverage (e.g. METR's Wikipedia entry) notes METR conducts pre-deployment evaluations for OpenAI and Anthropic models. This is *not* claimed from METR's own pages in this pass; treat as pointer-only until verified against METR's own publications.

## Fair-use note

This summary restates METR's published methodology, numbers, and conclusions in original prose with all sources linked. No METR prose is reproduced at length; direct quotation across this seed's outputs is kept well under 50 words total. Site exposition built from this seed must be original Interstitium writing with METR's pages and the paper linked as anchors. Fast-moving numeric claims (horizon values, doubling times, model scores) are as-of dated and will decay — refresh on re-verification.

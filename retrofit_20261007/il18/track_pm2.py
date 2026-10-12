# PM track, part 2: metrics-judgment, pm-behavioral
# quiz items: (q, [4 choices], answer_index, explain)

RETRO = {}

RETRO["pm-interview-prep--metrics-judgment"] = {
"summary": (
"Welcome back to the PM track — I'm your instructor, and this is Module 2: Metrics and Judgment. "
"Metrics separate PMs who guess from PMs who learn: defining measures that track user value, reading "
"experiments honestly, and debugging moves before reacting to them. By the end of this module you will define "
"success metrics tied to user value, read funnels and cohorts fluently, design A/B tests with significance "
"discipline, debug a moved metric before reacting, estimate sanely, make judgment calls with incomplete data, "
"and spot the failure modes of north-star metrics."
),
"concepts": """- **Success metric** — Tied to user value, measurable, with known failure modes — metrics that track learning, not vanity.
- **Analytics literacy (PM)** — Funnels, cohorts, retention — reading the product's vital signs without waiting for an analyst.
- **Funnel** — The step-by-step conversion path: where users drop is where the product leaks.
- **Cohort analysis** — Behavior compared by group and over time — the diagnostic pair with funnels.
- **A/B testing** — Design upfront, pre-registered metrics, significance discipline, and pitfall awareness: peeking, novelty effects, unexamined segments.
- **Metric debugging** — Instrumentation, segments, confounders, external events — understand the move before reacting to it.
- **Estimation (sane)** — State assumptions, round-number math, sanity-check the answer — the reasoning chain is the grade.
- **Judgment with incomplete data** — Decide reversibly fast, irreversibly carefully — and name what would change your mind.
- **North-star metric** — The one metric that best captures user value delivered — with known failure modes and counter-metrics.
- **Goodhart's law** — When a measure becomes a target, it ceases to be a good measure — the north star's failure mode, guarded with counter-metrics.""" ,
"procedure": """Run the metrics-and-judgment rep set. Work each rep on paper — the reasoning chain is the grade.
1. Define a success metric for a feature you know: tie it to user value, make it measurable, and name its failure modes — vanity check included.
2. Read a funnel: sketch signup-to-value for a product you use, mark where users drop, and write the one question each drop raises.
3. Compare two cohorts in writing: new versus returning users on one behavior — what differs, and what would you test next?
4. Design an A/B test: the hypothesis, the pre-registered primary metric, the sample-size thinking, and the pitfalls you will guard (peeking, novelty, segments).
5. Debug a moved metric: pick a metric that could move, and walk instrumentation → segments → confounders → external events before writing any reaction.
6. Do a guesstimate sanely: state assumptions, do round-number math, sanity-check the answer — the chain matters more than the number.
7. Make a judgment call with incomplete data: decide one reversible thing fast and one irreversible thing carefully — and write what would change your mind.
8. Pick a north-star candidate and name its Goodhart failure mode plus the counter-metric that guards it.""",
"brief": """Your interview prep brief: deliver the metrics-and-judgment portfolio page.
The scenario. Your PM loop includes a metrics round: "our activation metric dropped 15% — what do you do?" and "design an experiment for this feature." This page is your rehearsal artifact.
Deliverables.
- A success-metric definition tied to user value, with failure modes and a vanity check.
- A funnel sketch with drop points and the diagnostic question each drop raises.
- An A/B test design: hypothesis, pre-registered metric, significance discipline, pitfall guards.
- A metric-debugging walkthrough: instrumentation, segments, confounders, external events — before any reaction.
- A sane guesstimate with the full reasoning chain, and a north-star candidate with its Goodhart guard.
Grading lens. Metrics rounds score learning over reacting: did you tie measures to user value, design the experiment before the data, debug before acting, and show the reasoning chain?""",
"honesty": """Preparation only — this module confers no certificate and grants no credential. Metrics judgment must be practiced on real products with real numbers you understand — invented data produces invented judgment. In the round, say what you know, name what you would measure, and never present a fabricated experiment as one you ran.""",
"quiz": [
("Good metrics are:", ["Countable", "Tied to user value, with failure modes known", "Big", "Many"], 1, "The Concepts glossary defines a good success metric as tied to user value, measurable, with known failure modes — tracking learning, not vanity."),
("A/B pitfalls include:", ["Small samples", "Peeking, novelty effects, and unexamined segments", "Math", "Tools"], 1, "The Concepts note lists the pitfalls: peeking, novelty effects, unexamined segments — design discipline matters."),
("When a metric moves, first:", ["React", "Debug: instrumentation, segments, confounders — then act", "Celebrate", "Ignore it"], 1, "The Concepts glossary defines metric debugging as instrumentation, segments, confounders, external events — understand the move before reacting to it."),
("The north star's failure mode is:", ["Too small a metric", "Goodhart's law — the target corrupts; guard with counter-metrics", "Too big a metric", "There is none"], 1, "The Concepts note defines Goodhart's law as the north star's failure mode — when a measure becomes a target it ceases to be a good measure — guarded with counter-metrics."),
("Estimation is graded on:", ["Precision", "Assumptions, round math, sanity check — the chain is graded", "Guessing", "Skipping"], 1, "The Concepts glossary defines sane estimation as state assumptions, round-number math, sanity-check the answer — the reasoning chain is the grade."),
("Funnels diagnose:", ["Revenue directly", "Where users drop — the product's leak points", "Costs", "Nothing"], 1, "The Concepts note defines the funnel as the conversion path where drops reveal where the product leaks."),
("Cohort analysis compares:", ["Teams", "Behavior by group and over time", "Databases", "APIs"], 1, "The Concepts glossary defines cohort analysis as behavior compared by group and over time — the diagnostic pair with funnels."),
("Judgment with incomplete data means:", ["Waiting", "Decide reversibly fast, irreversibly carefully — and name what would change your mind", "Guessing", "Delegating"], 1, "The Concepts note defines the judgment discipline: reversible decisions fast, irreversible ones carefully — and name what would change your mind."),
("A/B tests must pre-register:", ["The winner", "The primary metric — before the data arrives", "The press release", "Nothing"], 1, "The procedure's step 4 requires the pre-registered primary metric — design upfront, before the data."),
("Data-informed differs from data-driven in that:", ["They are the same", "Informed: data inputs to judgment; driven: judgment abdicated to data", "Driven is better", "Informed ignores data"], 1, "The course material distinguishes them: informed means data inputs to judgment — humans decide; driven abdicates judgment to data."),
]}

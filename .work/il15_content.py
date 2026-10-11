# IL-15 expansion content: NEWCARDS {module_id: [(front, back), (front, back)]},
# REWRITE {module_id: {card_index: (front, back)}}, TRAINERS [...]
NEWCARDS = {
"data-eng-interview-prep--sql-for-de": [
("How do you talk about query performance in a SQL interview?",
 "Start with EXPLAIN: show you read the plan, not the query. Name the three big costs — sequential scans on large filtered tables, sorts that spill to disk, and nested loops on big inputs — and the matching fixes: indexes for selective filters, CLUSTER or covering indexes for sorted access, and join-order awareness. The interview line: 'I make the database prove it with EXPLAIN before I rewrite anything.'"),
("What's the interview line for self-joins?",
 "Reach for a self-join when a row must be compared against other rows of the same table — consecutive events, pairs, or 'find what changed'. Alias the table twice (a and b), join on the key plus the ordering condition (b.ts > a.ts), and filter for the nearest match. The honest line: 'Any question with the word consecutive or previous is probably a self-join, so I alias the table twice.'"),
],
"data-eng-interview-prep--python-data-wrangling": [
("When do you reach for Parquet instead of CSV in a pipeline?",
 "CSV is human-readable and universal; Parquet is columnar, compressed, typed, and partitionable. In an interview: choose Parquet the moment a human isn't reading the file — it's 5-10x smaller and lets Spark/presto read only needed columns. The interview line: 'CSV for handoffs to humans, Parquet for everything a machine reads twice.'"),
("How do you discuss testing data transforms in an interview?",
 "Three levels: row-level unit tests on small hand-built frames (pandas.testing or plain asserts), property checks on output (row counts, key uniqueness, no nulls in required fields), and golden-file tests on sampled real data. The line: 'If a transform can't be tested on a 10-row fixture, I don't trust it on 10 million rows.'"),
],
"data-eng-interview-prep--batch-pipelines": [
("Backfills: what makes them safe versus dangerous?",
 "Safe backfills are idempotent and scoped: deterministic date-partition writes, MERGE or overwrite of exactly the rerun window, and a pre-flight check of what downstream will recompute. Dangerous backfills rerun open-ended ranges into non-idempotent sinks with no dry run. The line: 'I backfill by partition, never by vibes.'"),
("How do you answer 'design a daily pipeline' end-to-end?",
 "Structure it aloud: source and extraction (full vs incremental by source capability), landing (raw immutable files by date partition), transform (validated staging to modeled tables), load (idempotent writes with DQ gates), orchestration (DAG with retries and SLA), and observability (row counts, freshness, alerts). The line: 'I narrate the pipeline left to right and name the failure at each arrow.'"),
],
"data-eng-interview-prep--streaming-systems": [
("How do you handle schema evolution in streaming?",
 "Schema registry with compatibility rules: BACKWARD for new consumers reading old events, FORWARD for old consumers reading new ones. Never break contracts — add optional fields, never rename or remove required ones. The interview line: 'Streams are APIs with infinite uptime; I version the schema like I version an API.'"),
("What do you say about stateful stream processing?",
 "Stateful operators keep per-key state across events — session windows, running aggregates, dedup buffers. The hard parts are state size (memory/disk), recovery (checkpoints to durable storage), and late data (watermarks bound the wait). The line: 'Stateless transforms are easy; the moment I keep state, I'm designing for recovery.'"),
],
"data-eng-interview-prep--data-modeling-warehousing": [
("What are conformed, degenerate, and junk dimensions?",
 "Conformed dimensions are shared across facts (one Date table for all marts) so metrics agree. Degenerate dimensions are dimensional attributes with no own table — like order number — parked directly on the fact. Junk dimensions bundle low-cardinality flags (yes/no codes) into one table to avoid a dozen tiny dims. The line: 'Conform so numbers agree, degenerate what's unique, junk what’s trivial.'"),
("How do you handle late-arriving facts in a warehouse design?",
 "Late facts land after the partition was built — restatements, corrections, delayed feeds. The design answer: restatable partitions (recompute the window, don't patch in place), a 'processed-as-of' watermark so consumers know the revision, and idempotent merges. The line: 'Late data is a restatement, not an edit — I rebuild the partition and stamp the revision.'"),
],
"data-eng-interview-prep--pipeline-capstone": [
("How do you discuss monitoring and SLAs for the pipeline?",
 "Three signals: freshness (did today's partition land by the SLA?), volume (row counts vs expectation), and correctness (DQ checks green). Define the SLA up front — 'data ready by 7am for the 9am reports' — then show the alert path when it breaks. The line: 'A pipeline without an SLA is a script; I define ready, then I prove it.'"),
("What does reproducibility mean for a capstone pipeline?",
 "Same inputs, same code, same outputs — pinned dependencies, seeded randomness, immutable raw landing, and versioned transforms. If the reviewer reruns it next week they must get the same tables. The line: 'I defend reproducibility like a scientist: pinned code, frozen inputs, documented environment.'"),
],
"data-eng-interview-prep--de-mock": [
("How do you handle a question you genuinely don't know?",
 "Say so in one sentence, then reason out loud: state your best guess, name what would confirm it, and propose how you'd verify in practice (docs, experiment, EXPLAIN). Interviewers score reasoning under uncertainty higher than a confident bluff. The line: 'I don't know — but here's how I'd figure it out, and here's what I'd check first.'"),
("What should you ask the interviewer about the data stack?",
 "Ask what reveals the real job: data volume and velocity, the orchestration and warehouse stack, who owns DQ when it breaks, and what the team's biggest pipeline pain is right now. Two or three sharp questions beat ten generic ones. The line: 'I ask about their biggest pipeline pain — it tells me what they're really hiring for.'"),
],
"data-science-interview-prep--stats-prob-iv": [
("How do you explain Bayes' rule in a DS interview?",
 "Bayes updates beliefs: posterior = likelihood × prior / evidence. Plain version: start with a base rate, update with how likely the new evidence is under each hypothesis. Use the medical-test example to show base rates dominating. The line: 'Bayes is just disciplined updating — prior belief, new evidence, revised belief.'"),
("When do you bootstrap instead of using formulas?",
 "When the statistic has no clean formula — medians, ratios, custom business metrics — or when assumptions (normality, large n) look shaky. Resample with replacement, recompute the statistic thousands of times, read the interval off the distribution. The line: 'If I can simulate the sampling distribution, I don't need the formula's assumptions.'"),
],
"data-science-interview-prep--pandas-analysis": [
("What do you say about outliers — remove or keep?",
 "Neither by default: investigate first. Plot them, check if they're data errors (typos, unit mixups) or real signal (fraud, whales). Report both versions if the answer moves. The interview line: 'An outlier is a question, not a deletion — I find out which kind before touching it.'"),
("How do you discuss deduplication and record linkage?",
 "Exact dedup on keys is the easy case; the real problem is fuzzy duplicates — same entity, different spellings. Name blocking (reduce candidate pairs), string similarity (edit distance), and the manual-review threshold. The line: 'Exact matches dedupe by key; near-matches dedupe by judgment — I quantify both.'"),
],
"data-science-interview-prep--ml-for-ds": [
("When do you prefer logistic regression over a tree model?",
 "When interpretability and calibrated probabilities matter more than squeezing accuracy — regulated settings, stakeholder explanations, small data where trees overfit. Say it plainly: simpler wins when the decision must be defended. The line: 'I pick logistic regression when the model has to be argued, not just scored.'"),
("How do you discuss class imbalance beyond metrics?",
 "Three levers: change the data (class weights, resampling), change the threshold (tune the decision point to the cost matrix), and change the evaluation (PR curves over ROC on skewed data). Always ask what a false negative costs versus a false positive. The line: 'Imbalance is a cost problem first, a sampling problem second.'"),
],
"data-science-interview-prep--experimentation-ab": [
("How do you explain sample ratio mismatch (SRM)?",
 "SRM is when the observed split differs from the randomization design — say 52/48 instead of 50/50. It signals a broken mechanism: assignment bugs, filtering that differs by arm, or bots. The line: 'Check the split before the result; a broken randomization invalidates everything downstream.'"),
("What do you say about sequential testing and always-valid p-values?",
 "Peeking breaks fixed-horizon math, so either pre-commit to a sample size or use sequential methods with alpha spending — methods that price each interim look. The honest line: 'If the business must peek, I pay for it with sequential testing; free peeking is just p-hacking with extra steps.'"),
],
}
NEWCARDS.update({
"data-science-interview-prep--ds-case-rep": [
("How do you discuss metric choice in a case study?",
 "Tie the metric to the business lever: a marketplace optimizes matches per session, a subscription optimizes retention cohorts, a marketplace optimizes conversion. Say which moves first (leading indicator) and what confirms it (lagging outcome), plus one guardrail. The line: 'I name the north star, the input I move, and the guardrail I won't break.'"),
("What does 'sizing an opportunity' look like in a case?",
 "Multiply: affected population × baseline rate × plausible lift × value per unit. Keep the math on one line and sanity-check against known totals. Precision is fake; the order of magnitude is the point. The line: 'Rough and checked beats precise and wrong — I size to the nearest order of magnitude.'"),
],
"data-science-interview-prep--ds-mock": [
("How do you open a live-analysis screen?",
 "Narrate the plan before touching data: restate the question, list the two or three checks that decide the answer, then run them in that order. Examiners grade structure more than speed. The line: 'I say what I'm about to do before I do it — the plan is half the grade.'"),
("What do you do when your analysis contradicts the business request?",
 "Report the honest result with the evidence, quantify the size of the contradiction, and propose what it suggests instead — then let them decide. Hiding an inconvenient answer is a career-ender. The line: 'The data said no; my job is to make the no useful.'"),
],
"data-analyst-interview-prep--sql-foundations-analyst": [
("How do you debug a query that returns wrong numbers?",
 "Four checks in order: row counts at each join (fan-out doubles aggregates), the grain (what does one row mean?), the filter (WHERE vs HAVING on aggregates), and NULLs (they silently drop rows in joins). The line: 'Wrong numbers are almost always grain or fan-out — I check the row count first.'"),
("What do you say about NULLs in joins and aggregations?",
 "NULL never equals NULL, so joins drop them; COUNT(column) skips them while COUNT(*) doesn't; aggregates like SUM ignore them. In interviews, name the NULL policy for the key columns before writing the query. The line: 'I state my NULL assumptions out loud before the query, not after the bug.'"),
],
"data-analyst-interview-prep--sheets-modeling": [
("How do you discuss data validation in spreadsheets?",
 "Three defenses: input validation rules (dropdowns, ranges), conditional formatting that screams when something's off, and a checksum area (totals, row counts) that must reconcile. The line: 'A spreadsheet without checks is a rumor — I build the alarm into the sheet.'"),
("What do you say when asked to model a forecast in a sheet?",
 "Keep it transparent: show assumptions in their own cells, use scenarios (base/bull/bear) not single numbers, and make every formula traceable back to inputs. The line: 'Forecast cells I can audit; hard-coded numbers I can't defend.'"),
],
"data-analyst-interview-prep--visualization-story": [
("How do you critique a pie chart in an interview?",
 "Name the real issue: humans compare angles poorly — bar charts beat pies for more than two or three slices. But be diplomatic: acknowledge when a pie works (one part-of-whole message, few categories). The line: 'I judge the chart by the question it answers, not the chart type — but pies get scrutinized.'"),
("What do you say about color and accessibility in charts?",
 "Two rules: never let color be the only encoding (add labels or patterns for colorblind viewers), and use color to guide the eye — highlight the insight, gray out the rest. The line: 'Color is a highlighter, not the message — the chart must survive black-and-white.'"),
],
"data-analyst-interview-prep--business-metrics": [
("What do you say about vanity metrics versus actionable metrics?",
 "Vanity metrics feel good and move nothing (total signups); actionable metrics tie to a decision (activated users by cohort, with a lever attached). The test: 'if this moves, what would I do differently?' The line: 'Every metric I report carries a decision, or it doesn't make the slide.'"),
("How do you discuss seasonality versus a real trend change?",
 "Overlay year-over-year comparisons, decompose the series (trend, seasonal, residual), and check whether the change persists after the seasonal adjustment. The line: 'Seasonality is the first suspect; I de-season before I declare a trend.'"),
],
"data-analyst-interview-prep--analyst-guided-project": [
("What makes documentation of an analyst project strong?",
 "Four things: the question and why it matters, data sources with caveats, the analysis steps someone could rerun, and assumptions with their impact if wrong. The line: 'Documentation is how the analysis survives me — question, data, steps, caveats.'"),
("How do you discuss stakeholder feedback changing your analysis mid-project?",
 "Frame it as analysis doing its job: the feedback revealed a missed assumption, you re-scoped, and the answer got better. Name what changed and what the revision taught you — interviewers love a story where challenge improved rigor. The line: 'Feedback didn't break my analysis; it finished it.'"),
],
"data-analyst-interview-prep--analyst-mock": [
("How do you handle the 'walk me through your project' opener?",
 "Sixty seconds, four beats: the question, the hardest data problem, the key finding with its number, and the decision it drove. Save detail for their follow-ups. The line: 'Question, obstacle, finding, impact — sixty seconds, then I let them steer.'"),
("What do you ask when given an ambiguous case prompt?",
 "Clarify the decision behind the question: who decides what, what action follows each possible answer, and what constraints (time, data) bind you. Then restate the narrowed question. The line: 'Ambiguous prompts are decision interviews — I find the decision first.'"),
],
"ml-interview-prep--ml-theory-iv": [
("What do you say about the curse of dimensionality?",
 "In high dimensions, distances concentrate, data gets sparse, and models need exponentially more samples — trees split on noise, k-NN's 'neighbors' stop being near. The defenses: feature selection, regularization, embeddings. The line: 'High dimensions make everything far apart; I fight it with fewer, better features.'"),
("How do you explain generative versus discriminative models?",
 "Discriminative models learn the boundary P(y|x) — how to classify. Generative models learn the data distribution P(x|y) or P(x) — how to generate. Use the analogy: a discriminative model spots the fake painting, a generative one paints it. The line: 'Discriminative draws the line; generative learns the picture.'"),
],
"ml-interview-prep--deep-learning-iv": [
("How do you explain batch normalization?",
 "It normalizes each layer's inputs per mini-batch (zero mean, unit variance, then learnable scale/shift) so later layers see stable distributions — smoother loss landscape, faster training, higher learning rates tolerated. The caveats: batch-size dependence, and train/test mode behavior differs. The line: 'BatchNorm keeps every layer's inputs in a sane range, so gradients stay informative.'"),
("What do you say about the vanishing gradient problem?",
 "Repeated multiplication by small derivatives through many layers shrinks early-layer gradients to nothing — deep nets stop learning at the front. The fixes stack: ReLU-class activations, residual connections, normalization, good initialization. The line: 'Depth is a gradient highway; ReLUs, residuals, and norms keep the signal alive.'"),
],
"ml-interview-prep--ml-system-design": [
("What do you say about online versus batch inference tradeoffs?",
 "Online (real-time) serving gives instant predictions at the cost of latency budgets, infra complexity, and per-request cost; batch scoring is simpler and cheaper but stale between runs. Decide by the decision's time sensitivity. The line: 'If the decision can't wait for the batch, I serve online — and pay for it.'"),
("How do you discuss data pipelines feeding the model?",
 "The model is the easy half — the pipeline is the interview: training-serving consistency (same transforms in both), freshness SLAs, and monitoring for distribution shift at the input. The line: 'Models don't fail in interviews; pipelines do. I design the plumbing first.'"),
],
})
NEWCARDS.update({
"ml-interview-prep--ml-coding": [
("How do you implement train/test split by hand in a coding round?",
 "Shuffle indices with a fixed seed, take the first 80% for train — or stratify by class for imbalanced data. Never split after feature engineering that leaks (scaling fit on train only). The line: 'Split first, fit transforms on train only — leakage in a coding round is an instant fail.'"),
("What do you say when asked to implement logistic regression from scratch?",
 "State the moving parts before coding: sigmoid of the linear score, binary cross-entropy loss, gradient descent on the weights, predict with a 0.5 threshold. Then write clean vectorized NumPy. The line: 'Score, sigmoid, loss, gradient, step — the loop is the same every time.'"),
],
"ml-interview-prep--ml-capstone-project": [
("How do you discuss fairness checks in a capstone?",
 "Slice metrics by sensitive groups, report disparities honestly, and name which definition of fairness you're using (equal opportunity, demographic parity) and its tradeoffs. The line: 'I report group slices whether they flatter me or not — the writeup earns trust that way.'"),
("What does deployment planning look like in a capstone?",
 "Even without real users: an API sketch or batch-scoring script, input validation, latency and resource estimates, and a monitoring plan (what metric you'd watch, what triggers a retrain). The line: 'A capstone that can describe deployment understands the model's job.'"),
],
"ml-interview-prep--ml-mock": [
("How do you answer 'why did you choose this model'?",
 "Three honest reasons allowed: it fits the data shape and metric, it's the strong baseline everything beats, or the constraints demand it (latency, interpretability). 'Because it scored best' only works if you can defend the evaluation. The line: 'I justify models by constraints and evidence, never by fashion.'"),
("What do you do when the interviewer challenges your approach?",
 "Treat it as a gift: restate their objection fairly, say where it's valid, defend where it's not with evidence, and name what you'd test to settle it. Never fold instantly or dig in. The line: 'Pushback is the interview working — I engage the objection, not the ego.'"),
],
"sql-analytics-drills--sql-joins-subqueries": [
("How do you drill anti-joins (NOT EXISTS patterns)?",
 "The pattern: find rows in A with no match in B — churned users (no recent orders), unused inventory. NOT EXISTS (correlated) or LEFT JOIN ... WHERE b.id IS NULL; NOT IN breaks on NULLs. The drill line: 'No-match questions are anti-joins — NOT EXISTS, never NOT IN.'"),
("What's the drill line for self-joins?",
 "Join the table to itself with two aliases for row-to-row comparisons: consecutive events, manager/employee hierarchies, pairs. The condition compares the ordering column across aliases. The drill line: 'Same-table comparison, two aliases — the question usually says consecutive or previous.'"),
],
"sql-analytics-drills--sql-window-functions": [
("How do you drill LAG/LEAD for period-over-period?",
 "LAG(value) OVER (PARTITION BY entity ORDER BY period) grabs the previous period's value on the same row; the delta is value - LAG(...). Watch the first row — it returns NULL, so COALESCE or filter. The drill line: 'Prior period on the same row: LAG over the ordered partition, mind the NULL head.'"),
("What's the drill line for frame clauses (ROWS vs RANGE)?",
 "ROWS counts physical rows; RANGE groups by the ORDER BY value's peers (ties share the frame). Defaults bite: ORDER BY without a frame means RANGE UNBOUNDED PRECEDING. The drill line: 'Default frames use RANGE — ties share the frame. I state ROWS when I mean physical rows.'"),
],
"sql-analytics-drills--sql-ctes-recursive": [
("How do you drill the 'sessions from events' pattern?",
 "Order events per user, then group events into sessions with a gap threshold: flag a new session when LAG(ts) is more than N minutes back, then running-sum the flags as session_id. The drill line: 'Gap-and-island: flag the breaks, cumulative-sum the flags.'"),
("What's the drill line for avoiding CTE bloat?",
 "Name CTEs like pipeline stages (events, sessions, metrics) and keep each one doing exactly one transformation; if a CTE is used once and trivial, inline it. The drill line: 'One job per CTE — if I can't name it, it shouldn't exist.'"),
],
"sql-analytics-drills--analytics-patterns": [
("How do you drill the 'first touch vs last touch' attribution pattern?",
 "Two CTEs: first and last touch per journey (ROW_NUMBER ordered by and reverse by timestamp, filter rn = 1), then attribute the conversion to each. Say which model you chose and why — the business question decides. The drill line: 'Attribution is a modeling choice first, a query second.'"),
("What's the drill line for handling ties in top-N?",
 "Decide the tie policy before querying: RANK/DENSE_RANK for inclusive ties, ROW_NUMBER with a deterministic tiebreaker for exactly N. The drill line: 'Top-N with ties is a policy question — I ask whether ties share the cutoff.'"),
],
"sql-analytics-drills--drill-circuit-final": [
("How do you drill time-boxed pattern recognition?",
 "Give yourself 90 seconds per prompt: name the pattern (top-N, gaps-and-islands, funnel), sketch the clause order on paper, then write. Score pattern-first, syntax-second. The drill line: 'Pattern in the first minute; the query is just transcription.'"),
("What's the circuit line for explaining before querying?",
 "Say the plan in two sentences — what the grain is, which pattern you're using — before writing a single clause. Interviewers grade thinking, and it buys you recovery time when the syntax wobbles. The drill line: 'Explain the grain and the pattern first; the query writes itself.'"),
],
})

REWRITE = {
"data-eng-interview-prep--data-modeling-warehousing": {
 0: ("How do you explain a warehouse design in a whiteboard round?",
     "Three moves: name the grain of the central fact ('one row per order line'), list the dimensions you'd hang off it (date, customer, product, store), then state the SCD policy per dimension (type 1 for corrections, type 2 for tracked history). Draw the star before you speak. The line: 'Facts hold the grain, dimensions hold the context, and I declare both before drawing anything.'"),
},
"data-science-interview-prep--experimentation-ab": {
 1: ("What is a novelty effect, and how do you handle it?",
     "Users engage with the new thing because it's new, not because it's better — the early lift fades. Guard by running long enough for behavior to stabilize and by checking the lift's time trend. The interview line: 'Novelty is the first lie every test tells; I run past the curiosity phase.'"),
},
"data-analyst-interview-prep--business-metrics": {
 0: ("How do you explain a north-star metric versus input metrics?",
     "The north star is the single number that captures value delivered (e.g., nights booked for a travel site); input metrics are the levers teams move (search conversion, listing quality). North star for alignment, inputs for action. The line: 'North star for where we're going, inputs for what I do Monday morning.'"),
},
"data-analyst-interview-prep--analyst-guided-project": {
 2: ("How do you scope an analyst project so it finishes?",
     "One question, one dataset, one decision it informs — written down before touching the data. Cut scope by narrowing the question, never by lowering the bar. The line: 'I scope until I can finish it in the time I have, then I commit to that scope.'"),
},
"ml-interview-prep--ml-system-design": {
 1: ("How do you structure an ML system design answer end-to-end?",
     "Seven beats aloud: business goal and metric, data and labels, baseline model, features, evaluation and error analysis, serving architecture, monitoring and retraining. Spend the most time where the interviewer probes. The line: 'I walk the whole lifecycle, then dive where they push.'"),
},
"ml-interview-prep--ml-mock": {
 0: ("How do you handle ML theory deep-dives under time pressure?",
     "Lead with the definition, then the one equation or diagram that anchors it, then the intuition — stop there unless probed. Depth on demand beats rambling. The line: 'Definition, anchor, intuition — then I hand the steering wheel back.'"),
},
}

TRAINERS = [
 {"id": "sql-query-trainer",
  "title": "SQL pattern trainer",
  "brief": "Rapid-fire SQL interview patterns for the data tracks: joins, window functions, CTEs, and analytics patterns — pick the right clause shape under time pressure, then write the query.",
  "kind": "custom"},
 {"id": "pipeline-design-trainer",
  "title": "Pipeline design trainer",
  "brief": "Whiteboard-style pipeline design reps: batch vs streaming tradeoffs, backfill safety, idempotency, and DQ gates — structured decision drills for system-design rounds.",
  "kind": "custom"},
]

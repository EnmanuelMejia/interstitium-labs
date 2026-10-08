"""IL-15 retrofit: Data/Business Analyst track (6 modules)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load, apply_all

CONTENT = {
    "data-analyst-interview-prep--sql-foundations-analyst": {
        "summary": (
            "Welcome to the Data / Business Analyst Interview Prep track of the IL-15 Data Engineering & "
            "Analytics Interview Prep course. I'm your instructor for this track, and in this module we're going "
            "to build analyst SQL from the ground up: the query shapes behind 'how many users did X,' the join "
            "mistakes that silently wrong-answer them, and the grain discipline that keeps every metric honest."
        ),
        "concepts": (
            "- **logical query order** — FROM → WHERE → GROUP BY → HAVING → SELECT → window functions → ORDER BY: "
            "'I write in SELECT order but think in execution order.'\n"
            "- **inner join** — Keeps only matching rows from both sides; silently shrinks denominators when "
            "matches are missing.\n"
            "- **left join** — Keeps all left rows, NULLs for misses; the safe default when the left side must "
            "survive.\n"
            "- **GROUP BY grain** — The grouping columns define the answer's unit; wrong grain, wrong answer — "
            "'every SELECT column is either grouped or aggregated.'\n"
            "- **HAVING** — Filters groups after aggregation; aggregate conditions in WHERE are always wrong.\n"
            "- **COUNT(*) vs COUNT(column)** — COUNT(*) counts rows; COUNT(column) counts non-NULL values — the "
            "interview trap behind 'how many users?'\n"
            "- **subquery** — A query nested inside another; uncorrelated runs once, correlated runs per outer row.\n"
            "- **EXISTS (semi-join)** — 'Has at least one': stops at the first match, never fans out — 'EXISTS "
            "asks a yes/no question; JOIN brings back data.'\n"
            "- **anti-join** — LEFT JOIN ... WHERE right.key IS NULL or NOT EXISTS: the 'what's missing' pattern "
            "('customers with no orders').\n"
            "- **NOT IN NULL trap** — A single NULL in the subquery makes NOT IN return zero rows; NOT EXISTS has "
            "no such trap.\n"
            "- **orphan rows** — Child rows with no parent (orders with no customer); found with anti-joins, "
            "they signal data-quality problems."
        ),
        "procedure_intro": (
            "The foundations drill: every query is built in the same order — grain, joins, filters, aggregates — "
            "and checked against a three-row mental dataset. Speed comes from the routine, not from rushing."
        ),
        "procedure_steps": [
            "Read the question and state the grain: 'one row per user.' Write it as a comment.",
            "Choose the join by survival: which side must keep all its rows? Default to LEFT when the counted population must survive.",
            "Write FROM and JOINs first, then WHERE (row filters), then GROUP BY, then HAVING (group filters) — execution order, not SELECT order.",
            "Check every non-aggregated SELECT column is in the GROUP BY; check every aggregate filter lives in HAVING.",
            "For 'has at least one' use EXISTS; for 'has none' use NOT EXISTS — never NOT IN on nullable columns.",
            "Verify on a tiny mental dataset: three rows per table, including a NULL and a non-match. Trace the joins by hand.",
            "Read the query back as a sentence: does it still answer the asked question at the stated grain?",
        ],
        "procedure_code": (
            "-- Analyst staple: conversion with the denominator protected\n"
            "SELECT COUNT(DISTINCT o.customer_id) * 1.0\n"
            "       / NULLIF(COUNT(DISTINCT c.customer_id), 0) AS conversion_rate\n"
            "FROM customers c\n"
            "LEFT JOIN orders o\n"
            "  ON o.customer_id = c.customer_id;  -- LEFT keeps every customer\n"
            "\n"
            "-- Anti-join: customers with no orders (NULL-safe)\n"
            "SELECT c.customer_id\n"
            "FROM customers c\n"
            "WHERE NOT EXISTS (SELECT 1 FROM orders o\n"
            "                WHERE o.customer_id = c.customer_id);"
        ),
        "procedure_lang": "sql",
        "project_brief": (
            "Build an analyst SQL workbook: 15 queries over customers/orders/products answering real stakeholder "
            "questions ('how many users did X,' conversion by cohort, orphans report). Each query carries a grain "
            "comment, a join-justification comment (why this join type), and a NULL-handling note. Include the "
            "three classic traps solved correctly: COUNT(*) vs COUNT(column), NOT IN vs NOT EXISTS, and the "
            "inner-join denominator shrink. The workbook is the artifact you re-read before SQL screens."
        ),
        "honesty": (
            "Preparation, not a credential: this module confers no certificate and makes no placement claims. "
            "These foundations are stable SQL semantics — the same in any relational database — but real screens "
            "vary in difficulty and dialect. Timed drills measure current fluency, not your worth as an analyst."
        ),
        "new_card": {
            "front": "What's the interview line for join choice?",
            "back": "'State which side must survive': inner joins silently drop non-matches and shrink your denominator — if you're counting 'all users,' the users table must survive the join. The join type is a business decision, not a syntax choice.",
        },
        "explain_pointer": "Covered in this module's 'Concepts' note.",
        "new_quiz": [
            {
                "q": "SELECT name, COUNT(*) FROM users GROUP BY name fails logically when:",
                "choices": [
                    "Never",
                    "name isn't the grain you meant — grouping by a non-unique column answers a different question than intended",
                    "It's slow",
                    "COUNT needs DISTINCT",
                ],
                "answer": 1,
                "explain": "GROUP BY defines the answer's unit; a sloppy grain gives a confident wrong answer. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "NULLIF in a division protects against:",
                "choices": ["NULL inputs", "Division by zero — NULLIF turns 0 into NULL, yielding NULL instead of an error", "Slow math", "Wrong joins"],
                "answer": 1,
                "explain": "Defensive arithmetic: a zero denominator becomes NULL, not a crashed query. See the 'Hands-on procedure' in this module.",
            },
            {
                "q": "A correlated subquery differs from an uncorrelated one in that it:",
                "choices": [
                    "Is faster",
                    "References the outer query and executes per outer row",
                    "Can't use WHERE",
                    "Returns more columns",
                ],
                "answer": 1,
                "explain": "Correlation ties the inner query to each outer row — EXISTS is the classic case. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "Counting 'all users who ordered' with an INNER JOIN then COUNT(DISTINCT user) is wrong when:",
                "choices": [
                    "Never",
                    "Some users have no orders — inner join silently drops them from the denominator",
                    "It's slow",
                    "DISTINCT is banned",
                ],
                "answer": 1,
                "explain": "The join type decides the population; the count only counts survivors. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "WHERE vs HAVING: the rule is:",
                "choices": [
                    "They're interchangeable",
                    "WHERE filters rows before aggregation; HAVING filters groups after",
                    "HAVING is faster",
                    "WHERE can't use indexes",
                ],
                "answer": 1,
                "explain": "Logical query order: row filters first, group filters after GROUP BY. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "Orphan orders (no matching customer) are found with:",
                "choices": [
                    "An inner join",
                    "An anti-join — LEFT JOIN ... WHERE customer_id IS NULL, or NOT EXISTS",
                    "GROUP BY",
                    "UNION",
                ],
                "answer": 1,
                "explain": "'What's missing' is the anti-join's job; orphans signal data-quality issues. See the 'Concepts' glossary in this module.",
            },
        ],
    },
    "data-analyst-interview-prep--sheets-modeling": {
        "summary": (
            "Welcome to the Data / Business Analyst Interview Prep track of the IL-15 Data Engineering & "
            "Analytics Interview Prep course. I'm your instructor for this track, and in this module we're going "
            "to master the spreadsheet half of analyst screens: fast, correct lookups and pivots — plus the "
            "judgment to know when the data has outgrown the grid."
        ),
        "concepts": (
            "- **XLOOKUP / INDEX-MATCH** — Modern lookups without VLOOKUP's fragility (column-insert breakage, "
            "leftward-lookup limits); the interview-safe lookup family.\n"
            "- **VLOOKUP footguns** — Breaks on inserted columns, can't look left, exact-match flag forgotten; "
            "know why interviewers prefer the alternatives.\n"
            "- **absolute reference ($)** — $A$1 never moves on fill; A$1 locks the row, $A1 locks the column — "
            "'I lock what shouldn't move when the formula fills.'\n"
            "- **relative reference** — Shifts with the fill (A1 → A2 down a column); the default, and the #1 "
            "spreadsheet bug when misapplied.\n"
            "- **pivot table** — Drag-to-aggregate exploration: dimensions to rows/columns, values to aggregation — "
            "'the spreadsheet's GROUP BY.'\n"
            "- **cross-tab** — A pivot's row/column grid of counts or sums; the fastest path to 'break it down "
            "by X.'\n"
            "- **formula-based cleaning** — TRIM, TEXTSPLIT, IFERROR: auditable, re-runnable cleaning — 'formulas "
            "over manual edits.'\n"
            "- **what-if model** — Data tables, scenarios, goal seek: sensitivity analysis showing how outputs "
            "move with inputs.\n"
            "- **reproducibility limit** — The point where manual steps, size, or auditability demand SQL/Python: "
            "'spreadsheets are for exploration; pipelines are for repetition.'"
        ),
        "procedure_intro": (
            "The spreadsheet drill: every exercise is a messy grid and a question, done without touching the raw "
            "data by hand. If a step can't be re-run from formulas, it's not done."
        ),
        "procedure_steps": [
            "Freeze the raw data: work on a copy or a new sheet; raw stays untouched and auditable.",
            "Clean with formulas only: TRIM whitespace, TEXTSPLIT delimited fields, IFERROR for graceful failures — every edit re-runnable.",
            "Lock references deliberately: $ on what shouldn't move when the formula fills; verify by filling and spot-checking.",
            "Look up with XLOOKUP/INDEX-MATCH; handle misses explicitly (IFNA) instead of letting #N/A propagate silently.",
            "Explore with pivot tables before formulas: drag dimensions, check the cross-tab, then formalize the finding.",
            "Build what-if models with data tables/scenarios for sensitivity questions; document the assumptions in cells, not in your head.",
            "State the handoff point: when the data outgrows the grid (size, repetition, auditability), name SQL/Python as the next tool and why.",
        ],
        "project_brief": (
            "Deliver a spreadsheet case: a messy 10k-row sales extract and five stakeholder questions (lookup-"
            "heavy, pivot-heavy, and one what-if). The workbook must contain: untouched raw data, formula-only "
            "cleaning layers, correct absolute/relative references throughout, pivot explorations, a what-if "
            "scenario table, and a 'handoff memo' naming which question outgrows the grid and why. Every formula "
            "auditable; no manual edits anywhere."
        ),
        "honesty": (
            "Preparation, not a credential: this module confers no certificate and makes no placement claims. "
            "Spreadsheet mechanics are stable skills, but UI details vary across tools and versions — the concepts "
            "(references, pivots, reproducibility) transfer; the clicks may differ. Interviewers test judgment "
            "about tool limits as much as formula speed."
        ),
        "new_card": {
            "front": "What's the interview line for the spreadsheet-to-SQL handoff?",
            "back": "'Spreadsheets are for exploration; pipelines are for repetition': when steps must be repeated reliably, data outgrows memory, or the analysis must be auditable, the grid stops being the tool. Naming the handoff point is the senior move.",
        },
        "explain_pointer": "Covered in this module's 'Concepts' note.",
        "new_quiz": [
            {
                "q": "XLOOKUP is preferred over VLOOKUP mainly because:",
                "choices": [
                    "It's newer",
                    "It survives column inserts, looks in any direction, and defaults to exact match — fewer footguns",
                    "It's faster to type",
                    "VLOOKUP is banned",
                ],
                "answer": 1,
                "explain": "Robustness under real spreadsheet edits is the point. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "=$A$1*B1 filled down a column:",
                "choices": [
                    "Both references shift",
                    "A1 stays locked while B1 shifts per row — the classic rate-times-quantity pattern",
                    "Nothing changes",
                    "It errors",
                ],
                "answer": 1,
                "explain": "Lock what shouldn't move (the rate), let the row reference move (the quantity). See the 'Concepts' glossary in this module.",
            },
            {
                "q": "IFNA around a lookup is used to:",
                "choices": [
                    "Speed up calc",
                    "Handle misses explicitly instead of letting #N/A propagate silently through dependents",
                    "Hide all errors",
                    "Sort results",
                ],
                "answer": 1,
                "explain": "Explicit miss handling keeps downstream formulas honest. See the 'Hands-on procedure' in this module.",
            },
            {
                "q": "A pivot table's row/column cross-tab with counts answers:",
                "choices": [
                    "Averages only",
                    "How many rows fall in each combination — the fastest 'break it down by X'",
                    "Nothing useful",
                    "Medians",
                ],
                "answer": 1,
                "explain": "Pivots reshape long data into summary grids in seconds, no formulas. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "Manual cell edits for cleaning are rejected because:",
                "choices": [
                    "They're slow",
                    "They can't be audited or re-run — the cleaning isn't verifiable",
                    "They're ugly",
                    "Formulas are trendier",
                ],
                "answer": 1,
                "explain": "Repeatability is the difference between analysis and anecdote. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "A what-if data table is the right tool when the stakeholder asks:",
                "choices": [
                    "For a chart",
                    "How the outcome moves as an input varies — sensitivity analysis",
                    "For raw data",
                    "To delete rows",
                ],
                "answer": 1,
                "explain": "Scenarios and data tables systematize 'what if' instead of hand-tweaking cells. See the 'Concepts' glossary in this module.",
            },
        ],
    },
    "data-analyst-interview-prep--visualization-story": {
        "summary": (
            "Welcome to the Data / Business Analyst Interview Prep track of the IL-15 Data Engineering & "
            "Analytics Interview Prep course. I'm your instructor for this track, and in this module we're going "
            "to treat charts as arguments: picking the right visual for the question, keeping every axis honest, "
            "and turning dashboards and decks into recommendations that drive decisions."
        ),
        "concepts": (
            "- **chart-question fit** — Trends → line, comparisons → bar, composition → stacked bar, distributions "
            "→ histogram, relationships → scatter; the visual must answer the question asked.\n"
            "- **truncated-axis trap** — A y-axis not starting at zero visually magnifies tiny differences; 'I "
            "check the axis before I believe the chart — including my own.'\n"
            "- **pie-chart limit** — Fine for two or three slices; beyond that, humans can't compare angles — use "
            "bars.\n"
            "- **dashboard** — A UI for decisions: golden signals up top, drill-down from symptom to cause, "
            "time-range comparisons, deploy annotations.\n"
            "- **deploy annotations** — Marks on time-series showing releases; 'what changed?' is the first "
            "incident question, and annotations answer it at a glance.\n"
            "- **insight → implication → recommendation** — The arc: what the data says, why it matters to the "
            "business, what to do with expected impact — 'data without a recommendation is trivia.'\n"
            "- **BLUF (bottom line up front)** — Lead with the recommendation, then the one chart that proves it; "
            "executives decide, evidence follows the decision.\n"
            "- **stakeholder translation** — Plain language, no jargon, caveats named briefly and honestly; 'I "
            "present conclusions, not queries.'\n"
            "- **chart critique** — 'What question is it answering — and does the visual actually answer it?' The "
            "first question for any chart, including your own."
        ),
        "procedure_intro": (
            "The visualization drill: every exercise hands you a dataset and a stakeholder question; you produce "
            "exactly one chart and a three-sentence arc. Constraint breeds clarity — the interviewer sees whether "
            "you can choose."
        ),
        "procedure_steps": [
            "Write the question the chart must answer in one sentence before opening any tool.",
            "Choose the visual from the question type (trend/comparison/composition/distribution/relationship) — defend the choice in one line.",
            "Build it with honest scales: check the axis starts where it should; annotate context (deploys, events) that changes interpretation.",
            "Critique it as an adversary: what question does it actually answer? What could a viewer wrongly conclude?",
            "Write the arc: insight (what the data says), implication (why it matters), recommendation (what to do, expected impact).",
            "Present BLUF: recommendation first, then the one proving chart, caveats briefly, end with the decision you need.",
            "For dashboards: organize by the questions asked at 3am (symptom → cause), not by data source; every view must drive a decision.",
        ],
        "project_brief": (
            "Deliver a stakeholder deck for a product metric deep-dive: five charts max, each with a stated "
            "question, an honest axis, and a place in the insight → implication → recommendation arc. Include "
            "one deliberately-bad chart you then critique and fix (truncated axis or wrong visual), and a "
            "one-page dashboard spec organized by incident questions. Present it in 10 minutes, BLUF-first, "
            "ending with the decision you're asking for."
        ),
        "honesty": (
            "Preparation, not a credential: this module confers no certificate and makes no placement claims. "
            "Visualization principles are stable; tool UIs evolve — the judgment (chart choice, honest axes, "
            "the arc) transfers across every BI tool. A beautiful chart answering the wrong question is still "
            "the wrong chart."
        ),
        "new_card": {
            "front": "What's the interview line for chart critique?",
            "back": "'What question is it answering — and does the visual actually answer it?' Ask it of every chart, including your own, before you ask anything about prettiness. A beautiful chart answering the wrong question is worse than no chart.",
        },
        "explain_pointer": "Covered in this module's 'Concepts' note.",
        "new_quiz": [
            {
                "q": "A line chart with a y-axis from 98 to 100 showing 'huge growth' is:",
                "choices": [
                    "Fine — the data is accurate",
                    "The truncated-axis trap: tiny differences visually magnified — check the axis before believing it",
                    "Better than a bar chart",
                    "Standard practice",
                ],
                "answer": 1,
                "explain": "Honest scales first; the visual must not exaggerate what the numbers don't say. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "For comparing 12 categories' market share, prefer:",
                "choices": ["A pie chart", "Bars — humans compare lengths far better than 12 angles", "A scatter", "A table of raw numbers only"],
                "answer": 1,
                "explain": "Chart-question fit: many-slice pies defeat perception; bars don't. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "Deploy annotations on a metrics dashboard exist to answer:",
                "choices": ["Who deployed", "'What changed?' — correlating behavior shifts with releases, the first incident question", "How pretty it is", "Uptime stats"],
                "answer": 1,
                "explain": "Annotations turn 'the metric moved' into a short suspect list. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "BLUF ordering (recommendation first) works because:",
                "choices": [
                    "It's shorter",
                    "Decision-makers need the ask before the evidence — the analysis follows the decision it serves",
                    "Charts are boring",
                    "It's traditional",
                ],
                "answer": 1,
                "explain": "Lead with what you need decided; the proof earns the decision. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "A dashboard organized by data source (rather than by question) fails because:",
                "choices": [
                    "It's ugly",
                    "Nobody asks 'show me the database' at 3am — views must map to incident questions, symptom to cause",
                    "It's slow",
                    "Sources change",
                ],
                "answer": 1,
                "explain": "A dashboard is a UI for decisions, not a catalog of tables. See the 'Hands-on procedure' in this module.",
            },
            {
                "q": "Naming caveats briefly in a stakeholder presentation:",
                "choices": [
                    "Weakens the case",
                    "Builds trust — honest limits stated up front beat discovered omissions",
                    "Is optional",
                    "Confuses executives",
                ],
                "answer": 1,
                "explain": "'I present conclusions, not queries' — and honest conclusions include their limits. See the 'Concepts' glossary in this module.",
            },
        ],
    },
    "data-analyst-interview-prep--business-metrics": {
        "summary": (
            "Welcome to the Data / Business Analyst Interview Prep track of the IL-15 Data Engineering & "
            "Analytics Interview Prep course. I'm your instructor for this track, and in this module we're going "
            "to build the judgment layer: defining the right metric, slicing it before trusting it, and "
            "diagnosing a movement like a detective."
        ),
        "concepts": (
            "- **North Star metric** — The single metric capturing core product value; everything else ladders up "
            "to it.\n"
            "- **input metrics** — The levers that move the North Star (acquisition, activation, retention "
            "drivers); what teams actually operate day to day.\n"
            "- **funnel** — Step-by-step conversion with drop-off at each stage; analyze segmented, because "
            "aggregate funnels hide the story — 'name the biggest absolute drop first.'\n"
            "- **cohort** — Users grouped by start period; tracked over time-since-start so product changes are "
            "measured against comparable groups.\n"
            "- **retention curve** — Cohort retention over time: flattening above zero signals a sticky core "
            "(product-market fit); decaying to zero is a leaky bucket.\n"
            "- **segmentation** — Cutting metrics by device, channel, cohort, segment before concluding; "
            "'aggregates lie' — Simpson's paradox lives here.\n"
            "- **Simpson's paradox** — An aggregate trend reversing within subgroups; the reason you 'never trust "
            "an aggregate until you've cut it three ways.'\n"
            "- **metric-moved drill** — The diagnostic sequence: verify data quality first (instrumentation, "
            "pipeline, definitions), then segment, then theorize — 'half of all metric moves are measurement "
            "artifacts.'\n"
            "- **guardrail metrics** — Must-not-regress companions to the primary metric; read with confidence "
            "intervals, not point estimates."
        ),
        "procedure_intro": (
            "The metrics drill: every exercise is a moved metric or a vague 'define success' prompt. The routine "
            "is always data-quality first, segments second, theories last — in that order, every time."
        ),
        "procedure_steps": [
            "Define the metric precisely: numerator, denominator, grain, time window — ambiguity here corrupts everything downstream.",
            "Name the North Star it ladders to and the input metrics that move it; check the metric actually measures the decision.",
            "When a metric moves: verify data quality FIRST — instrumentation changes, pipeline delays, definition edits — before any product theory.",
            "Segment three ways (cohort, channel/device, segment): find where the move lives; aggregates lie.",
            "For funnels: compute step-by-step conversion, name the biggest absolute drop — that's the leverage point.",
            "For retention: build the cohort curve, compare across cohorts — flattening vs decaying tells you product health.",
            "Read experiment results honestly: primary metric's interval, guardrails for regressions, segment heterogeneity — then decide.",
        ],
        "project_brief": (
            "Deliver a metrics playbook for a subscription product: the North Star with its input-metric tree, "
            "precise definitions (numerator, denominator, grain, window) for five key metrics, a funnel analysis "
            "with the leverage point named, cohort retention curves with the health read, and three worked "
            "'metric moved' diagnoses following the drill (data quality → segments → theory). Present the "
            "diagnoses as 10-minute detective stories ending in a recommendation."
        ),
        "honesty": (
            "Preparation, not a credential: this module confers no certificate and makes no placement claims. "
            "Metric judgment is product-specific — the frameworks here (North Star, cohorts, the drill) transfer, "
            "but every company's metrics have their own quirks and politics. The drill's first step exists because "
            "measurement artifacts are genuinely common, not because interviewers are tricking you."
        ),
        "new_card": {
            "front": "What's the interview line for a moved metric?",
            "back": "'Data quality first, segments second, theories last': half of all metric moves are measurement artifacts — instrumentation, pipeline, definitions — so you rule those out before theorizing. Then you cut three ways, because aggregates lie.",
        },
        "explain_pointer": "Covered in this module's 'Concepts' note.",
        "new_quiz": [
            {
                "q": "A North Star metric should be:",
                "choices": [
                    "Easy to move",
                    "The single best proxy for core product value — what the business actually sells",
                    "Whatever is tracked",
                    "Revenue always",
                ],
                "answer": 1,
                "explain": "Everything ladders up to it; if it doesn't capture value, the tree is decorative. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "Input metrics differ from the North Star in that they:",
                "choices": [
                    "Matter more",
                    "Are the operable levers teams move day to day to shift the North Star",
                    "Are vanity metrics",
                    "Never change",
                ],
                "answer": 1,
                "explain": "Teams can't 'do' a North Star directly; they operate the inputs. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "An aggregate conversion rate rises while every segment's rate falls. This is:",
                "choices": [
                    "Great news",
                    "Simpson's paradox — composition shifted toward a high-converting segment",
                    "A data bug always",
                    "Impossible",
                ],
                "answer": 1,
                "explain": "Mix shifts deceive aggregates; segment before concluding. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "Cohort analysis (vs calendar-time analysis) is preferred for retention because:",
                "choices": [
                    "It's prettier",
                    "It compares users at the same lifecycle stage — calendar time mixes tenures",
                    "It's faster",
                    "Calendars are wrong",
                ],
                "answer": 1,
                "explain": "Retention is a function of tenure; cohorts hold tenure constant. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "In a funnel, the first number to name is:",
                "choices": [
                    "The final conversion",
                    "The biggest absolute drop between steps — that's where the leverage is",
                    "The first step's volume",
                    "The average",
                ],
                "answer": 1,
                "explain": "Absolute drops size the prize; relative rates can mislead on small bases. See the 'Hands-on procedure' in this module.",
            },
            {
                "q": "A metric definition must include grain because:",
                "choices": [
                    "It's formal",
                    "'Revenue per user' vs 'revenue per order' are different metrics with different values — the unit decides the number",
                    "Stakeholders ask",
                    "Tools require it",
                ],
                "answer": 1,
                "explain": "Ambiguous grain is the quietest way to publish a wrong metric confidently. See the 'Hands-on procedure' in this module.",
            },
        ],
    },
    "data-analyst-interview-prep--analyst-guided-project": {
        "summary": (
            "Welcome to the Data / Business Analyst Interview Prep track of the IL-15 Data Engineering & "
            "Analytics Interview Prep course. I'm your instructor for this track, and in this module you're going "
            "to build the portfolio piece that answers 'walk me through an analysis': one end-to-end analysis — "
            "question, data, exploration, dashboard, recommendation memo — done like a professional."
        ),
        "concepts": (
            "- **question worth answering** — A question with a decision attached; 'decision-less analysis expands "
            "forever; a target decision bounds the work.'\n"
            "- **auditable cleaning** — Every cleaning step re-runnable and reasoned (formulas, code, logged "
            "decisions) — never silent manual edits.\n"
            "- **exploration with a plan** — Time-boxed, question-driven EDA; the plan prevents fishing, the "
            "sanity checks prevent embarrassment.\n"
            "- **insight → action → recommendation** — The arc every deliverable follows: what the data says, why "
            "it matters, what to do.\n"
            "- **recommendation memo** — Decision, evidence, risks — the written artifact stakeholders actually act on.\n"
            "- **stakeholder pushback** — The expected objections, diagnosed early ('often a different question "
            "than you answered') and addressed with data; 'I argue with data, then commit like an owner.'\n"
            "- **dashboard vs deck** — Dashboards monitor recurring questions; decks argue a specific decision — "
            "choose by the job.\n"
            "- **portfolio narrative** — The 10-minute walkthrough: question → approach → findings → "
            "recommendation, with caveats owned proactively."
        ),
        "procedure_intro": (
            "The project build order: question first, then data, then exploration, then the story. The memo is "
            "drafted before the dashboard is polished — decisions drive pixels, not the reverse."
        ),
        "procedure_steps": [
            "Pick a question worth answering: attach the decision it informs and the recommendation it could produce.",
            "Get the data and profile it: shape, quality, grain, gaps — write the data's limits down before analyzing.",
            "Clean auditably: every transformation re-runnable, every judgment (drop/impute/flag) recorded with its reason.",
            "Explore with a plan: question-driven cuts, sanity checks first, one chart per emerging finding.",
            "Build the deliverable around the arc: insight → implication → recommendation — dashboard for monitoring, deck for deciding.",
            "Write the recommendation memo: decision, evidence, risks, caveats owned — one page.",
            "Anticipate pushback: list the three likeliest objections, prepare the data-backed answer to each, rehearse the 10-minute walkthrough.",
        ],
        "project_brief": (
            "Deliver the guided analyst project end to end on a real dataset: the framed question with its "
            "decision, the profiled and auditably-cleaned data, the planned exploration, the dashboard or deck "
            "built on the insight arc, the one-page recommendation memo, and the pushback FAQ with data-backed "
            "answers. Close with a recorded 10-minute walkthrough. This repository is the link you send when they "
            "ask to 'walk me through an analysis.'"
        ),
        "honesty": (
            "Preparation, not a credential: this module confers no certificate and makes no placement claims. A "
            "portfolio project proves you can execute the full loop on one dataset — it doesn't replicate "
            "stakeholder politics, shifting priorities, or production data scale. Claim the craft, not the "
            "context you haven't worked in."
        ),
        "new_card": {
            "front": "What makes an analyst project portfolio-worthy?",
            "back": "A decision-attached question, auditably cleaned data, exploration with a plan, a deliverable on the insight arc, a one-page memo — and a walkthrough that owns the caveats. 'Every step serves the decision': that's what interviewers are checking.",
        },
        "explain_pointer": "Covered in this module's 'Concepts' note.",
        "new_quiz": [
            {
                "q": "Attaching a decision to the question upfront:",
                "choices": [
                    "Is just formality",
                    "Bounds the analysis — you know when you have enough to recommend",
                    "Slows you down",
                    "Is only for executives",
                ],
                "answer": 1,
                "explain": "Decision-less analysis expands forever; a target decision scopes the work. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "Dashboard vs deck: the choice depends on:",
                "choices": [
                    "Tool availability",
                    "The job — dashboards monitor recurring questions, decks argue a specific decision",
                    "Personal taste",
                    "Data size",
                ],
                "answer": 1,
                "explain": "Form follows function: monitoring vs persuasion demand different artifacts. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "When a stakeholder rejects your analysis, the strongest first move is:",
                "choices": [
                    "Defend harder",
                    "Diagnose the real objection — it's often a different question than you answered",
                    "Rebuild everything",
                    "Escalate immediately",
                ],
                "answer": 1,
                "explain": "Most disagreements are misaligned questions; finding the real one resolves them. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "An auditable cleaning step means:",
                "choices": [
                    "It's fast",
                    "It's re-runnable and reasoned — formulas or code with the judgment recorded",
                    "It's automated",
                    "It's documented in email",
                ],
                "answer": 1,
                "explain": "Repeatability is the difference between analysis and anecdote. See the 'Hands-on procedure' in this module.",
            },
            {
                "q": "The pushback FAQ is prepared before presenting because:",
                "choices": [
                    "Stakeholders are hostile",
                    "The likeliest objections are predictable — answering them proactively builds credibility",
                    "It's required",
                    "Memos need length",
                ],
                "answer": 1,
                "explain": "Self-challenged work earns trust faster than perfect-looking work. See the 'Hands-on procedure' in this module.",
            },
            {
                "q": "A portfolio walkthrough that hides caveats:",
                "choices": [
                    "Looks polished",
                    "Backfires — interviewers probe exactly where you're vague, and evasion reads as inexperience",
                    "Saves time",
                    "Is standard",
                ],
                "answer": 1,
                "explain": "Own the limits proactively; credibility comes from the caveats, not despite them. See the 'Honesty note' in this module.",
            },
        ],
    },
    "data-analyst-interview-prep--analyst-mock": {
        "summary": (
            "Welcome to the Data / Business Analyst Interview Prep track of the IL-15 Data Engineering & "
            "Analytics Interview Prep course. I'm your instructor for this track, and in this final track module "
            "we're going to simulate the analyst loop — timed SQL screens, take-home case walkthroughs, metric "
            "deep-dives, dashboard critiques — scored against rubrics with a targeted fix list."
        ),
        "concepts": (
            "- **analyst loop** — The standard sequence: SQL screen, take-home case, metrics deep-dive, behavioral "
            "— each round with its own shape.\n"
            "- **SQL screen shape** — 15-minute playbook: grain (1 min), CTE stages aloud (2 min), write in "
            "passes, verify on a mental dataset, narrate throughout.\n"
            "- **take-home walkthrough** — 'The walkthrough is the interview; the document is the prop': present "
            "question → approach → findings → recommendation, defend caveats proactively, timebox the take-home "
            "itself.\n"
            "- **metric deep-dive** — Define precisely, segment three ways, run the metric-moved drill; graded on "
            "diagnostic order (data quality → segments → theory).\n"
            "- **dashboard critique** — 'What decision does this view drive?' Purpose before pixels: one question "
            "per view, metric with target, trends not snapshots, the 'so what' test.\n"
            "- **stakeholder-disagreement story** — Listen for the real objection, show work and caveats honestly, "
            "propose the resolving test, disagree-and-commit cleanly: 'I argue with data, then commit like an owner.'\n"
            "- **scored review** — Rubric per round (correctness, complexity stated, communication, time); misses "
            "verbatim.\n"
            "- **redrill plan** — Misses converted to specific, dated tasks; the fix list that closes the loop."
        ),
        "procedure_intro": (
            "The analyst mock protocol: simulate the loop in order, real timing, narration mandatory. The "
            "take-home is timeboxed like the real thing — polish the narrative, not the appendix."
        ),
        "procedure_steps": [
            "Run the SQL screen with the 15-minute playbook; narrate grain, stages, and verification aloud.",
            "Timebox a take-home case (set a hard stop); build for the walkthrough narrative, not appendix depth.",
            "Present the walkthrough: question → approach → findings (one chart each) → recommendation; own the caveats before questions.",
            "Run the metric deep-dive: define, segment three ways, run the moved-metric drill in order.",
            "Critique a dashboard live: decision per view, metric definitions, trends vs snapshots, prioritized fixes.",
            "Tell the stakeholder-disagreement story: real objection diagnosed, data argued, clean commit.",
            "Score every round against the rubric immediately; convert each miss to a dated redrill task.",
        ],
        "project_brief": (
            "Run and document three full analyst mock loops over two weeks: SQL screen, timeboxed take-home with "
            "walkthrough, metric deep-dive, dashboard critique, and the disagreement story. Per loop deliver the "
            "prompts, rubric scores with verbatim misses, and the dated redrill plan; close with a readiness "
            "self-assessment naming your strongest round, your costliest miss category, and the plan to fix it."
        ),
        "honesty": (
            "Preparation, not a credential: this module confers no certificate and makes no placement claims. "
            "Mocks approximate the analyst loop's shapes and pressure; real loops vary, and take-home expectations "
            "differ by company — timebox honestly and never misrepresent the effort. Scores aim your redrills; "
            "they don't predict offers."
        ),
        "new_card": {
            "front": "What's the interview line for take-homes?",
            "back": "'The walkthrough is the interview; the document is the prop': timebox the take-home, polish the narrative arc (question → findings → recommendation), and defend the caveats proactively. Nobody hires the appendix.",
        },
        "explain_pointer": "Covered in this module's 'Concepts' note.",
        "new_quiz": [
            {
                "q": "Timeboxing the take-home matters because:",
                "choices": [
                    "It's a rule",
                    "Unbounded polish has diminishing returns — the narrative is what's graded, and real jobs have deadlines",
                    "It's faster",
                    "Reviewers are busy",
                ],
                "answer": 1,
                "explain": "Polish the story, not the appendix; the walkthrough is the interview. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "In a dashboard critique, 'purpose before pixels' means:",
                "choices": [
                    "Ignore design",
                    "Ask 'what decision does this view drive?' before commenting on visuals",
                    "Critique colors first",
                    "Rebuild it",
                ],
                "answer": 1,
                "explain": "A dashboard is a UI for decisions; decoration critique misses the point. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "Proactively addressing caveats in the walkthrough is strong because:",
                "choices": [
                    "It's defensive",
                    "It shows the analysis survived your own skepticism — credibility before they ask",
                    "It fills time",
                    "Critics are harsh",
                ],
                "answer": 1,
                "explain": "Self-challenged work earns trust faster than perfect-looking work. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "The metric deep-dive's diagnostic order is:",
                "choices": [
                    "Theory → data → segments",
                    "Data quality → segments → theory — rule out measurement artifacts first",
                    "Segments → theory → data",
                    "Whatever feels right",
                ],
                "answer": 1,
                "explain": "Half of metric moves are measurement; theorizing first wastes the round. See the 'Hands-on procedure' in this module.",
            },
            {
                "q": "A redrill plan works when it is:",
                "choices": [
                    "Ambitious",
                    "Specific, dated, and tied to named misses from the scored review",
                    "Long",
                    "Shared with friends",
                ],
                "answer": 1,
                "explain": "Specificity turns review into training; vague plans evaporate. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "'Disagree and commit' after the data argument means:",
                "choices": [
                    "Giving up",
                    "Once the decision goes the other way, you execute it fully — ownership survives disagreement",
                    "Sabotage",
                    "Escalation",
                ],
                "answer": 1,
                "explain": "Argue with data, then commit like an owner — that's the story interviewers want. See the 'Concepts' glossary in this module.",
            },
        ],
    },
}

if __name__ == "__main__":
    apply_all(load(), CONTENT)

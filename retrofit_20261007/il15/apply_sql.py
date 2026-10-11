"""IL-15 retrofit: SQL & Analytics Drill Circuit track (5 modules)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load, apply_all

CONTENT = {
    "sql-analytics-drills--sql-joins-subqueries": {
        "summary": (
            "Welcome to the SQL & Analytics Drill Circuit of the IL-15 Data Engineering & Analytics Interview "
            "Prep course. I'm your instructor for this circuit, and in this module we're going to drill join "
            "fluency until it's reflex: which join the question wants, the anti-join for what's missing, "
            "self-joins, EXISTS vs IN — and catching the fan-out before it corrupts the aggregate."
        ),
        "concepts": (
            "- **inner join** — Only matching rows survive; drilled until you feel the denominator shrink.\n"
            "- **left / right / full outer join** — Which side survives: left keeps all left rows, right keeps all "
            "right, full keeps everything.\n"
            "- **anti-join** — 'What's missing': LEFT JOIN ... WHERE right.key IS NULL, or NOT EXISTS "
            "(NULL-safe, unlike NOT IN).\n"
            "- **semi-join** — 'Has at least one': EXISTS or IN; never fans out rows.\n"
            "- **self-join** — A table joined to itself with aliases (employees to managers): hierarchies without "
            "new tables.\n"
            "- **correlated subquery** — References the outer query, executes per outer row; EXISTS is the "
            "canonical case.\n"
            "- **uncorrelated subquery** — Runs once, independently; a precomputed set the outer query uses.\n"
            "- **EXISTS vs IN** — EXISTS: correlated, short-circuits, NULL-safe. IN: set membership, NULL-"
            "poisoned under NOT. ''Has at least one' → EXISTS; 'has none' → NOT EXISTS.'\n"
            "- **fan-out** — Many-to-many joins multiplying rows; caught by key-uniqueness checks and count "
            "assertions before and after."
        ),
        "procedure_intro": (
            "The join drill: 10 minutes per pattern, same sheet of shapes every time. Draw the Venn-style "
            "survival diagram before writing — the picture picks the join, not habit."
        ),
        "procedure_steps": [
            "Read the question and name the survival requirement: which table's rows must all appear in the answer?",
            "Draw the join shape: mark which side survives; pick inner/left/right/full from the picture.",
            "For 'has' questions reach for EXISTS; for 'has none' reach for NOT EXISTS — say the choice aloud.",
            "Check key uniqueness on both join keys before running; state the expected cardinality.",
            "Write the query, then assert: row count vs expectation — fan-out caught here, not in the dashboard.",
            "Re-solve the same question with the alternative construct (EXISTS vs JOIN, subquery vs CTE) and name the tradeoff.",
        ],
        "procedure_code": (
            "-- Self-join: employees and their managers\n"
            "SELECT e.name AS employee,\n"
            "       m.name AS manager\n"
            "FROM employees e\n"
            "LEFT JOIN employees m\n"
            "  ON m.id = e.manager_id;  -- LEFT keeps the CEO (no manager)\n"
            "\n"
            "-- Semi-join: customers WITH at least one order\n"
            "SELECT c.customer_id\n"
            "FROM customers c\n"
            "WHERE EXISTS (SELECT 1 FROM orders o\n"
            "            WHERE o.customer_id = c.customer_id);"
        ),
        "procedure_lang": "sql",
        "project_brief": (
            "Build a join-drill workbook: 20 timed problems covering every pattern in this module — inner/outer "
            "survival, anti-joins, self-joins, correlated vs uncorrelated, EXISTS vs IN — each with the survival "
            "diagram sketched, the join choice justified in one line, and a fan-out check recorded. Score "
            "yourself on pattern recognition speed: the goal is seeing the join in the question before writing."
        ),
        "honesty": (
            "Preparation, not a credential: this module confers no certificate and makes no placement claims. "
            "Join semantics are stable relational fundamentals — drills build recognition speed, which is "
            "precisely what timed screens test. Real schemas are messier than drills; the survival-discipline "
            "transfers, the tidy examples don't."
        ),
        "new_card": {
            "front": "What's the drill line for 'has at least one' vs 'has none'?",
            "back": "'Has at least one' → EXISTS (correlated, short-circuits, NULL-safe). 'Has none' → NOT EXISTS. Never NOT IN on nullable columns — one NULL poisons the whole predicate to zero rows.",
        },
        "explain_pointer": "Covered in this module's 'Concepts' note.",
        "new_quiz": [
            {
                "q": "A self-join requires table aliases because:",
                "choices": [
                    "It's faster",
                    "The same table plays two roles — aliases disambiguate which instance each column comes from",
                    "It's the syntax",
                    "Indexes need them",
                ],
                "answer": 1,
                "explain": "Employees-as-employees vs employees-as-managers: the alias names the role. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "FULL OUTER JOIN keeps:",
                "choices": ["Only matches", "Every row from both sides, NULLs where there's no match", "Only left rows", "Only right rows"],
                "answer": 1,
                "explain": "Full survival both sides — the reconciliation join. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "A correlated EXISTS vs an uncorrelated IN: the practical difference is:",
                "choices": [
                    "Syntax only",
                    "EXISTS short-circuits per outer row and is NULL-safe; IN materializes a set and is NULL-poisoned under NOT",
                    "IN is faster always",
                    "EXISTS needs GROUP BY",
                ],
                "answer": 1,
                "explain": "Semantics differ, not just style — choose by the question's shape. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "Joining orders to order_items doubled your revenue sum. First check:",
                "choices": [
                    "The SELECT list",
                    "Key uniqueness — a many-to-many fan-out multiplied rows before aggregation",
                    "The WHERE clause",
                    "The database version",
                ],
                "answer": 1,
                "explain": "Fan-out is the classic silent aggregate corruptor; count assertions catch it. See the 'Hands-on procedure' in this module.",
            },
            {
                "q": "'Products never sold' is found with:",
                "choices": ["An inner join", "An anti-join — LEFT JOIN ... WHERE order key IS NULL, or NOT EXISTS", "A cross join", "UNION"],
                "answer": 1,
                "explain": "'What's missing' is the anti-join's home turf. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "Sketching the survival diagram before writing the join:",
                "choices": [
                    "Wastes time",
                    "Makes the join choice visual and deliberate — the picture picks the join, not habit",
                    "Is only for beginners",
                    "Slows interviews",
                ],
                "answer": 1,
                "explain": "Method is the deliverable; the diagram is method made visible. See the 'Hands-on procedure' in this module.",
            },
        ],
    },
    "sql-analytics-drills--sql-window-functions": {
        "summary": (
            "Welcome to the SQL & Analytics Drill Circuit of the IL-15 Data Engineering & Analytics Interview "
            "Prep course. I'm your instructor for this circuit, and in this module we're going to drill the "
            "highest-leverage SQL topic in interviews: window functions. Ranking, deltas, running aggregates — "
            "until the frame clause is reflex."
        ),
        "concepts": (
            "- **window function** — Computation across related rows without collapsing them; GROUP BY's "
            "detail-preserving counterpart.\n"
            "- **PARTITION BY** — Divides rows into groups for the window; the 'GROUP BY of windows' — numbering "
            "restarts per partition.\n"
            "- **ORDER BY (in OVER)** — Defines row sequence inside the partition; required for meaningful "
            "ranking, LAG/LEAD, and frames.\n"
            "- **ROW_NUMBER / RANK / DENSE_RANK** — Unique sequence vs tie-honoring rankings (RANK gaps, "
            "DENSE_RANK doesn't).\n"
            "- **LAG / LEAD** — Previous/next row's value in the ordered partition; period-over-period without "
            "self-joins.\n"
            "- **frame clause** — ROWS/RANGE bounds (UNBOUNDED PRECEDING, BETWEEN ... AND ...); ROWS counts "
            "physical rows, RANGE groups peer values.\n"
            "- **running total** — SUM(x) OVER (ORDER BY date ROWS UNBOUNDED PRECEDING): the ordered frame "
            "accumulates.\n"
            "- **NTILE(n)** — Splits ordered rows into n roughly-equal buckets (quartiles, deciles).\n"
            "- **percent_rank** — Relative standing from 0 to 1 within the partition.\n"
            "- **top-N per group** — ROW_NUMBER() in a CTE, filter rn <= N outside: windows can't appear in "
            "WHERE, so the two-step is the pattern.\n"
            "- **windows vs GROUP BY** — Windows keep every row and add context; GROUP BY collapses to one row "
            "per group."
        ),
        "procedure_intro": (
            "The window drill: one function family per session, 10 timed reps each. Every rep states the "
            "partition, the order, and the frame before writing — the three decisions inside every OVER()."
        ),
        "procedure_steps": [
            "Name the three OVER() decisions aloud: PARTITION BY (the groups), ORDER BY (the sequence), frame (the visible rows).",
            "Write the window in a CTE; remember windows evaluate after WHERE — filter on row numbers one level out.",
            "For deltas: LAG/LEAD with the right offset and a default for the edge row; state what the first row's delta means.",
            "For running totals: explicit frame clause (ROWS UNBOUNDED PRECEDING) — never rely on defaults you can't recite.",
            "Check ROWS vs RANGE when ORDER BY has ties: RANGE includes all peers, ROWS counts physical rows — running totals differ.",
            "Verify on a 6-row hand trace: partition boundaries, tie handling, edge rows. The trace is the test.",
        ],
        "procedure_code": (
            "-- Period-over-period delta with LAG\n"
            "WITH monthly AS (\n"
            "  SELECT DATE_TRUNC('month', order_date) AS m,\n"
            "         SUM(amount) AS revenue\n"
            "  FROM orders\n"
            "  GROUP BY 1\n"
            ")\n"
            "SELECT m,\n"
            "       revenue,\n"
            "       revenue - LAG(revenue) OVER (ORDER BY m) AS delta,\n"
            "       SUM(revenue) OVER (ORDER BY m\n"
            "                        ROWS UNBOUNDED PRECEDING) AS running_total\n"
            "FROM monthly;"
        ),
        "procedure_lang": "sql",
        "project_brief": (
            "Build a window-function drill deck: 25 timed problems — ranking with ties, top-N per group, "
            "period-over-period deltas, running totals with explicit frames, NTILE bucketing, session-style "
            "gaps via LAG — each solved with the partition/order/frame stated up front and a 6-row hand trace "
            "verifying the answer. The deck is your pre-screen warmup: run 10 cards the morning of any SQL loop."
        ),
        "honesty": (
            "Preparation, not a credential: this module confers no certificate and makes no placement claims. "
            "Window-function semantics are stable SQL — drills build the reflex that timed screens reward. "
            "Dialect details (frame defaults) vary; verify against your target database's docs before a screen."
        ),
        "new_card": {
            "front": "What are the three decisions inside every OVER()?",
            "back": "PARTITION BY (which rows form a group), ORDER BY (their sequence), and the frame (which rows the function sees). State all three before writing — most window bugs are an unstated frame or a missing order.",
        },
        "explain_pointer": "Covered in this module's 'Concepts' note.",
        "new_quiz": [
            {
                "q": "RANK() vs DENSE_RANK() on tied values:",
                "choices": [
                    "Identical always",
                    "Both honor ties; RANK skips numbers after ties, DENSE_RANK doesn't",
                    "DENSE_RANK is faster",
                    "RANK ignores ties",
                ],
                "answer": 1,
                "explain": "Tie-handling is the whole distinction; pick by whether gaps matter. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "Omitting ORDER BY inside OVER() for ROW_NUMBER gives:",
                "choices": [
                    "An error",
                    "Nondeterministic numbering — the sequence is meaningless without an order",
                    "Sorted output",
                    "A syntax warning only",
                ],
                "answer": 1,
                "explain": "No order, no meaning: the frame and ranking both depend on sequence. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "LAG(amount, 7) OVER (ORDER BY day) is useful for:",
                "choices": [
                    "Running totals",
                    "Week-over-week comparison — the value 7 rows back in day order",
                    "Ranking",
                    "Bucketing",
                ],
                "answer": 1,
                "explain": "Offset LAG reaches back N positions: the period-over-period primitive. See the 'Hands-on procedure' in this module.",
            },
            {
                "q": "With duplicate ORDER BY values, ROWS vs RANGE frames:",
                "choices": [
                    "Are identical",
                    "Differ: RANGE includes all peer rows with tied values, ROWS counts physical rows",
                    "Are deprecated",
                    "Only matter for RANK",
                ],
                "answer": 1,
                "explain": "Peer handling is the subtle difference — running totals over duplicate dates diverge. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "'Each employee with their department's average salary' needs:",
                "choices": [
                    "GROUP BY only",
                    "A window: AVG(salary) OVER (PARTITION BY dept) — detail preserved, context added",
                    "A self-join only",
                    "HAVING",
                ],
                "answer": 1,
                "explain": "GROUP BY alone can't keep row detail; windows add group context per row. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "NTILE(10) over ordered revenue assigns:",
                "choices": ["Percentiles", "Ranks", "Decile buckets 1–10 — roughly equal groups", "Revenue values"],
                "answer": 2,
                "explain": "NTILE divides the ordered set into n buckets as evenly as possible. See the 'Concepts' glossary in this module.",
            },
        ],
    },
    "sql-analytics-drills--sql-ctes-recursive": {
        "summary": (
            "Welcome to the SQL & Analytics Drill Circuit of the IL-15 Data Engineering & Analytics Interview "
            "Prep course. I'm your instructor for this circuit, and in this module we're going to treat CTEs as "
            "query architecture: breaking monsters into named stages, chaining them like a pipeline — plus "
            "recursion for the hierarchy problems that stump the unprepared."
        ),
        "concepts": (
            "- **CTE** — WITH name AS (...): a named, temporary result set structuring the query top-to-bottom.\n"
            "- **chained CTEs** — Each CTE reads earlier ones: clean → enrich → aggregate → rank — 'my CTEs read "
            "like pipeline stages.'\n"
            "- **recursive CTE** — Anchor query (the roots) UNION ALL recursive term (extend one level); "
            "terminates when no new rows appear.\n"
            "- **anchor** — The seed rows (e.g., top-level managers WHERE manager_id IS NULL) the recursion "
            "builds on.\n"
            "- **recursive term** — Joins the CTE to the base table to grow one level per iteration; carries "
            "depth/path columns.\n"
            "- **termination** — Recursion stops when the recursive term returns nothing; missing join "
            "conditions mean infinite loops.\n"
            "- **date spine** — A complete calendar series (recursive CTE or generate_series) left-joined to "
            "sparse facts: 'missing rows are data too.'\n"
            "- **hierarchy walk** — Org charts, category trees, bill-of-materials: anchor the roots, recurse the "
            "edges, track depth.\n"
            "- **CTE vs subquery** — CTEs win on readability (named stages), reuse (referenced twice), and "
            "recursion (impossible in a subquery)."
        ),
        "procedure_intro": (
            "The CTE drill: every monster query gets decomposed into named stages before a line is written. If "
            "you can't name the stages, you don't understand the query yet."
        ),
        "procedure_steps": [
            "Decompose the problem into stages on paper; give each stage a name — those names become your CTEs.",
            "Write the CTEs top-to-bottom in dependency order; each one does exactly one transformation.",
            "For hierarchies: write the anchor first (the roots), verify it alone, then add the recursive term joining CTE to base table.",
            "Carry depth and path columns in recursive CTEs; verify termination logic — the recursion must shrink the frontier.",
            "For time series: build the date spine first (generate_series or recursive), then LEFT JOIN sparse facts — zeros, not gaps.",
            "Re-read the final SELECT: it should read like a summary of named stages, with no buried logic.",
        ],
        "procedure_code": (
            "-- Recursive CTE: org hierarchy with depth\n"
            "WITH RECURSIVE org AS (\n"
            "  SELECT id, name, manager_id, 1 AS depth,\n"
            "         name::text AS path\n"
            "  FROM employees\n"
            "  WHERE manager_id IS NULL          -- anchor: the roots\n"
            "  UNION ALL\n"
            "  SELECT e.id, e.name, e.manager_id, o.depth + 1,\n"
            "         o.path || ' > ' || e.name\n"
            "  FROM employees e\n"
            "  JOIN org o ON o.id = e.manager_id  -- recursive: one level down\n"
            ")\n"
            "SELECT name, depth, path FROM org ORDER BY path;\n"
            "\n"
            "-- Date spine: no gaps in the time series\n"
            "SELECT d.day,\n"
            "       COUNT(o.order_id) AS orders\n"
            "FROM generate_series('2026-01-01'::date,\n"
            "                   '2026-01-31'::date, '1 day') AS d(day)\n"
            "LEFT JOIN orders o ON o.order_date = d.day\n"
            "GROUP BY d.day;"
        ),
        "procedure_lang": "sql",
        "project_brief": (
            "Build a CTE drill workbook: 15 problems — 8 multi-stage monsters decomposed into chained CTEs "
            "(each stage named and single-purpose), 4 hierarchy walks (org chart, category tree with depth and "
            "path), 3 date-spine time series with the gap analysis shown. Every solution includes the stage "
            "diagram drawn before the SQL. The workbook proves you architect queries, not just write them."
        ),
        "honesty": (
            "Preparation, not a credential: this module confers no certificate and makes no placement claims. "
            "CTE structuring is a readability discipline as much as a technique — interviewers read your "
            "structure as evidence of how you think. Recursive-CTE syntax details vary by database; verify "
            "against your target's docs."
        ),
        "new_card": {
            "front": "What's the drill line for recursive CTEs?",
            "back": "'Anchor the roots, recurse the edges': the anchor query seeds the top level, the UNION ALL term joins the CTE back to the base table one level deeper, and depth/path columns make the walk visible. Verify the anchor alone before adding recursion.",
        },
        "explain_pointer": "Covered in this module's 'Concepts' note.",
        "new_quiz": [
            {
                "q": "The anchor query's job in a recursive CTE is to:",
                "choices": [
                    "Join the tables",
                    "Provide the seed rows the recursion builds on",
                    "Terminate the loop",
                    "Sort the output",
                ],
                "answer": 1,
                "explain": "No seeds, no growth: the recursive term extends what the anchor provides. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "A recursive CTE that never terminates usually suffers from:",
                "choices": [
                    "Too few columns",
                    "A recursive term that doesn't actually shrink the frontier — often a wrong or missing join condition",
                    "Slow disks",
                    "Missing ORDER BY",
                ],
                "answer": 1,
                "explain": "Termination needs the frontier to empty; a bad join regrows it forever. See the 'Hands-on procedure' in this module.",
            },
            {
                "q": "generate_series for a date spine is preferred over a recursive CTE when:",
                "choices": [
                    "Never",
                    "The database supports it — it's clearer and purpose-built for sequences",
                    "Dates are sparse",
                    "It's slower",
                ],
                "answer": 1,
                "explain": "Use the purpose-built tool where available; recursion is the portable fallback. See the 'Hands-on procedure' in this module.",
            },
            {
                "q": "LEFT JOIN from the date spine (rather than from the facts) ensures:",
                "choices": [
                    "Speed",
                    "Every calendar day appears — zero-activity days show as zero instead of vanishing",
                    "Correct sorting",
                    "Fewer rows",
                ],
                "answer": 1,
                "explain": "The complete calendar drives; sparse facts can't create gaps. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "Referencing the same CTE twice in the main query is valuable because:",
                "choices": [
                    "It's faster",
                    "Single definition, multiple use — DRY applied to SQL, and the logic stays in one named place",
                    "It's required",
                    "Subqueries can't do it",
                ],
                "answer": 1,
                "explain": "Named stages document the pipeline; duplication buries it. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "Carrying a path column in a hierarchy walk gives you:",
                "choices": [
                    "Faster queries",
                    "The full ancestry per row as readable text — debuggable and presentable",
                    "Less memory",
                    "Automatic sorting",
                ],
                "answer": 1,
                "explain": "Depth plus path makes the recursion's work visible and verifiable. See the 'Hands-on procedure' in this module.",
            },
        ],
    },
    "sql-analytics-drills--analytics-patterns": {
        "summary": (
            "Welcome to the SQL & Analytics Drill Circuit of the IL-15 Data Engineering & Analytics Interview "
            "Prep course. I'm your instructor for this circuit, and in this module we're going to drill the "
            "greatest hits of analytics screens — funnels, cohorts, sessionization, pivots — as reusable query "
            "templates you adapt on the spot."
        ),
        "concepts": (
            "- **funnel query** — Conditional aggregation per step (COUNT(DISTINCT CASE WHEN step >= n THEN "
            "user END)), then successive ratios; segmented by cohort/channel.\n"
            "- **conditional aggregation** — SUM/COUNT(CASE WHEN ...) inside aggregates: pivots and segment "
            "metrics in one scan.\n"
            "- **cohort query** — DATE_TRUNC of first activity per user as the cohort; periods on the columns, "
            "cohorts on the rows.\n"
            "- **retention query** — Per cohort and period offset: active users / cohort size; the curve's shape "
            "is the product-health read.\n"
            "- **sessionization** — Grouping events into sessions via inactivity gaps: LAG timestamps, flag gaps "
            "over the threshold, running-sum the flags into session ids.\n"
            "- **grain discipline** — COUNT(DISTINCT user) vs COUNT(*): 'know what one row represents before "
            "choosing the aggregate.'\n"
            "- **pivot (portable)** — Conditional aggregation per output column; no vendor PIVOT keyword needed.\n"
            "- **metric-moved diagnostic set** — The standard queries: data-quality checks, segment cuts, funnel "
            "step comparison — the 'why did it move' toolkit."
        ),
        "procedure_intro": (
            "The patterns drill: each template is learned once, then adapted under time to three variants. The "
            "goal isn't memorization — it's recognizing which template the question wants within 30 seconds."
        ),
        "procedure_steps": [
            "Classify the question in 30 seconds: funnel, cohort/retention, session, pivot, or diagnostic — name the template aloud.",
            "Write the template skeleton first (CTE stages with the standard shape), then fill in the question's tables and columns.",
            "State the grain before aggregating: per user, per session, per day — and pick COUNT vs COUNT(DISTINCT) accordingly.",
            "For funnels: conditional counts per step, successive ratios, then segment — the aggregate funnel hides the story.",
            "For sessions: LAG the timestamp, flag gaps over threshold, running-sum flags into session ids — verify on a hand trace.",
            "Adapt under time: change the grain, the segment, the window — the template bends, the shape holds.",
        ],
        "procedure_code": (
            "-- Funnel: conditional aggregation per step\n"
            "WITH steps AS (\n"
            "  SELECT user_id,\n"
            "         MAX(CASE WHEN event = 'view'     THEN 1 ELSE 0 END) AS s1,\n"
            "         MAX(CASE WHEN event = 'add_cart' THEN 1 ELSE 0 END) AS s2,\n"
            "         MAX(CASE WHEN event = 'purchase' THEN 1 ELSE 0 END) AS s3\n"
            "  FROM events\n"
            "  GROUP BY user_id\n"
            ")\n"
            "SELECT COUNT(*) AS n,\n"
            "       SUM(s1) AS step1,\n"
            "       SUM(s2) AS step2,\n"
            "       SUM(s3) AS step3,\n"
            "       SUM(s3) * 1.0 / NULLIF(SUM(s1), 0) AS overall_conv\n"
            "FROM steps;"
        ),
        "procedure_lang": "sql",
        "project_brief": (
            "Build the analytics-patterns playbook: one page per template (funnel, cohort/retention, "
            "sessionization, pivot, metric-moved diagnostics) with the canonical query, the grain note, the "
            "three most common variants, and the trap to avoid. Then solve 15 mixed timed problems by "
            "classifying each in 30 seconds and adapting the template. The playbook is your screen-side "
            "reference — recognition speed is the skill."
        ),
        "honesty": (
            "Preparation, not a credential: this module confers no certificate and makes no placement claims. "
            "Templates accelerate recognition; they don't replace thinking — adapt them to the question's grain "
            "and business logic, or they produce confident wrong answers. Real event schemas are messier than "
            "drill tables."
        ),
        "new_card": {
            "front": "What's the drill line for sessionization?",
            "back": "LAG the timestamp, flag gaps over the inactivity threshold, running-sum the flags into session ids. Three window steps turn a flat event stream into sessions — verify the flags on a hand trace before trusting the sums.",
        },
        "explain_pointer": "Covered in this module's 'Concepts' note.",
        "new_quiz": [
            {
                "q": "Classifying the question's template within 30 seconds matters because:",
                "choices": [
                    "It's a rule",
                    "Recognition speed is the timed-screen skill — the template then writes itself",
                    "It's fun",
                    "Interviewers time you",
                ],
                "answer": 1,
                "explain": "Pattern recognition converts panic into procedure. See the 'Hands-on procedure' in this module.",
            },
            {
                "q": "In the funnel query, each step uses COUNT(DISTINCT CASE WHEN ...) to:",
                "choices": [
                    "Speed up",
                    "Count each user once per step even with repeated events — users, not events, convert",
                    "Sort results",
                    "Avoid joins",
                ],
                "answer": 1,
                "explain": "Funnels measure user progression; event counts would inflate. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "Cohort rows with period columns (vs a flat time series) let you:",
                "choices": [
                    "Save space",
                    "Compare same-tenure behavior across cohorts — the apples-to-apples retention read",
                    "Avoid GROUP BY",
                    "Skip segments",
                ],
                "answer": 1,
                "explain": "'Cohort on the rows, periods on the columns' — tenure held constant. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "Sessionization's gap threshold should be chosen based on:",
                "choices": [
                    "Convention (30 min always)",
                    "The product's usage pattern — what inactivity means a session ended here",
                    "Database limits",
                    "Query speed",
                ],
                "answer": 1,
                "explain": "The threshold is a product judgment, not a constant; state your assumption. See the 'Hands-on procedure' in this module.",
            },
            {
                "q": "Portable pivoting (no PIVOT keyword) uses:",
                "choices": ["A join", "Conditional aggregation — one aggregate per output column", "UNION ALL", "A subquery per column"],
                "answer": 1,
                "explain": "CASE inside aggregates reshapes rows to columns on any database. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "The metric-moved diagnostic set starts with:",
                "choices": [
                    "Blaming the product change",
                    "Data-quality queries — instrumentation, pipeline, definitions — before segment cuts",
                    "Rewriting the dashboard",
                    "A meeting",
                ],
                "answer": 1,
                "explain": "Measurement artifacts first; theorizing second. See the 'Concepts' glossary in this module.",
            },
        ],
    },
    "sql-analytics-drills--drill-circuit-final": {
        "summary": (
            "Welcome to the SQL & Analytics Drill Circuit of the IL-15 Data Engineering & Analytics Interview "
            "Prep course. I'm your instructor for this circuit, and in this final module we're going to run full "
            "timed circuits mixing every pattern from the circuit: speed, narration, and recovery — the closest "
            "thing to the real screen without one."
        ),
        "concepts": (
            "- **mixed-pattern circuit** — A timed set spanning joins, windows, CTEs, and analytics patterns; "
            "trains switching, not just depth.\n"
            "- **15-minute playbook** — Grain (1 min), CTE stages aloud (2 min), write in passes, verify on a "
            "mental dataset, narrate throughout.\n"
            "- **narration** — Exposing decomposition and recovery to grading: 'the interviewer scores your "
            "method, not just the final query.'\n"
            "- **recovery** — Naming the bug aloud ('this double-counts because...'), fixing the specific issue, "
            "re-verifying: 'recovery is a skill — I show it instead of freezing.'\n"
            "- **hint reading** — Treating interviewer nudges as directional data: they mark where the "
            "interviewer wants you to go, not failure.\n"
            "- **weak-pattern list** — Your personal miss inventory from circuits; the redrill backlog that makes "
            "each circuit better than the last.\n"
            "- **scored review** — Rubric per circuit: correctness, pattern recognition speed, narration, "
            "recovery, time.\n"
            "- **redrill plan** — Misses to specific, dated tasks: 'three sliding-window problems, timed, by "
            "Thursday.'"
        ),
        "procedure_intro": (
            "The circuit protocol: full mixed sets under the real clock, no pausing, narration mandatory. One "
            "circuit per session, scored immediately, redrills scheduled before the next."
        ),
        "procedure_steps": [
            "Assemble a 60-minute circuit: 4 mixed problems (join, window, CTE, analytics pattern) at 15 minutes each.",
            "Run each with the playbook: grain, stages aloud, passes, mental-dataset verification, continuous narration.",
            "When stuck: say what you'd try next and why — scored recovery beats silent freezing.",
            "Read hints as direction: restate the nudge ('so the grain should be per session...') and adjust visibly.",
            "Score immediately per the rubric: correctness, recognition speed, narration, recovery, time — misses verbatim.",
            "Log every miss into your weak-pattern list; convert each to a dated redrill task before the next circuit.",
            "Track the trend across circuits: which patterns stopped costing you time, which still do — train the remainder.",
        ],
        "project_brief": (
            "Run and document six full mixed circuits over three weeks. Per circuit deliver: the four problems "
            "used, per-problem rubric scores with verbatim misses, the updated weak-pattern list, and the dated "
            "redrill plan. Close with a readiness report: recognition-speed trend per pattern family, your "
            "recovery highlight reel (best in-round save), and the one pattern still costing you points with its "
            "kill plan. This is the training log you review the week of interviews."
        ),
        "honesty": (
            "Preparation, not a credential: this module confers no certificate and makes no placement claims. "
            "Circuits simulate screen pressure; they can't replicate a specific interviewer's style or a "
            "company's data. Scores measure training progress on the day — aim redrills with them, don't predict "
            "offers with them."
        ),
        "new_card": {
            "front": "What's the circuit line for getting stuck?",
            "back": "Say what you'd try next and why — out loud. Freezing scores zero on recovery; a named hypothesis ('the grain is probably per session, let me re-verify') shows the method surviving contact with difficulty. Recovery is a skill you demonstrate, not a secret you hide.",
        },
        "explain_pointer": "Covered in this module's 'Concepts' note.",
        "new_quiz": [
            {
                "q": "Mixed-pattern circuits train switching because:",
                "choices": [
                    "Variety is fun",
                    "Real screens don't announce the pattern — recognition under time is the tested skill",
                    "It's traditional",
                    "Single-pattern is boring",
                ],
                "answer": 1,
                "explain": "Classification speed plus execution: the circuit trains both. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "Saying the bug aloud before fixing it is strong because:",
                "choices": [
                    "It wastes time",
                    "It proves you diagnose before patching — and lets the interviewer follow the fix",
                    "Interviewers like talking",
                    "It's polite",
                ],
                "answer": 1,
                "explain": "Diagnose-then-fix beats flailing; narration turns the fix into evidence. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "An interviewer hint ('what about the grain here?') should be treated as:",
                "choices": [
                    "A failure signal",
                    "Directional data — restate it and adjust visibly; it's where they want you to go",
                    "An insult",
                    "A trick",
                ],
                "answer": 1,
                "explain": "Hints mark the path; following them well is part of the score. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "The weak-pattern list's job is to:",
                "choices": [
                    "Demoralize",
                    "Turn each circuit's misses into the next circuit's redrill backlog — training compounds",
                    "Impress others",
                    "Replace practice",
                ],
                "answer": 1,
                "explain": "The list is the mechanism by which circuits get easier. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "No pausing the circuit clock because:",
                "choices": [
                    "Rules are rules",
                    "Pressure management is part of the training stimulus — removing it removes the conversion",
                    "It's faster",
                    "Rubrics forbid it",
                ],
                "answer": 1,
                "explain": "Circuits convert knowledge into performance under pressure. See the 'Hands-on procedure' in this module.",
            },
            {
                "q": "Your readiness report's most important section is:",
                "choices": [
                    "The high scores",
                    "The remaining costliest pattern with its kill plan — honest about what's left",
                    "The problem list",
                    "The dates",
                ],
                "answer": 1,
                "explain": "Readiness is knowing the gap and the plan, not admiring the strengths. See the 'Project brief' in this module.",
            },
        ],
    },
}

if __name__ == "__main__":
    apply_all(load(), CONTENT)

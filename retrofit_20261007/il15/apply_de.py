"""IL-15 retrofit: Data Engineering track (7 modules). Run with cwd anywhere."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load, apply_all

CONTENT = {
    "data-eng-interview-prep--sql-for-de": {
        "summary": (
            "Welcome to the Data Engineering Interview Prep track of the IL-15 Data Engineering & Analytics "
            "Interview Prep course. I'm your instructor for this track, and in this module we're going to build "
            "the SQL layer DE interviews actually probe: window functions, CTEs, join patterns, and the grain "
            "discipline that separates fast, correct queries from plausible-looking wrong ones. You will write "
            "SQL you can defend line by line — because that's exactly what the interviewer will ask you to do."
        ),
        "concepts": (
            "- **window function** — A calculation across rows related to the current row — ROW_NUMBER, RANK, "
            "LAG/LEAD, running totals — computed without collapsing rows the way GROUP BY does.\n"
            "- **ROW_NUMBER** — Assigns a unique sequential integer within each partition in the specified order; "
            "the tool for top-N-per-group when paired with a CTE and an outer filter.\n"
            "- **RANK / DENSE_RANK** — Rankings that honor ties: RANK leaves gaps after ties, DENSE_RANK does not; "
            "use either when equal values must share a rank.\n"
            "- **LAG / LEAD** — Reads the previous or next row's value inside an ordered partition; the workhorse "
            "for period-over-period deltas without a self-join.\n"
            "- **frame clause** — ROWS or RANGE bounds on a window (e.g. ROWS UNBOUNDED PRECEDING) defining which "
            "rows the function sees; without ORDER BY the frame has no meaning.\n"
            "- **CTE (common table expression)** — A named temporary result set (WITH ...) that structures a query "
            "into readable top-to-bottom stages; chained CTEs read like a pipeline.\n"
            "- **recursive CTE** — A CTE with an anchor query plus a UNION ALL recursive term; the way to walk "
            "hierarchies and generate date spines.\n"
            "- **semi-join** — An existence filter ('has at least one': EXISTS or IN) that never fans out rows; the "
            "safe answer to yes/no membership questions.\n"
            "- **anti-join** — A 'has none' filter: LEFT JOIN ... WHERE right.key IS NULL, or NOT EXISTS "
            "(NULL-safe, unlike NOT IN); the pattern for 'what is missing' questions.\n"
            "- **grain** — The unit one row represents (per customer, per day, per customer-month); GROUP BY must "
            "match the question's grain or the aggregate answers a different question.\n"
            "- **HAVING** — Filters groups after aggregation; WHERE filters rows before it — an aggregate filter "
            "in WHERE is always wrong.\n"
            "- **UNION vs UNION ALL** — UNION dedupes (implicit DISTINCT, costs a sort); UNION ALL keeps duplicates "
            "and skips the pass — faster when duplicates don't matter.\n"
            "- **conditional aggregation** — SUM(CASE WHEN ...) patterns that compute segment metrics in one scan: "
            "'one scan, many answers.'\n"
            "- **query plan (EXPLAIN)** — The database's execution strategy; a sequential scan on a large filtered "
            "table signals a missing or unused index."
        ),
        "procedure_intro": (
            "The drill loop for this module: one pattern at a time, timed, narrated aloud. Each rep follows the "
            "same steps so the method — not the query — becomes the habit you carry into the interview."
        ),
        "procedure_steps": [
            "State the grain out loud before writing anything: 'one row per customer-month.' Write it as a comment at the top of the query.",
            "Sketch the CTE stages on paper or in the editor: clean -> enrich -> aggregate -> rank. Name each stage; never nest subqueries three deep when a CTE would show the work.",
            "Write the core logic first (joins and grain), then layer on window functions in an outer CTE — window functions cannot appear in WHERE, so plan the two-step from the start.",
            "Run the query against a tiny mental dataset (three rows per table) and trace each stage's output by hand; fix grain and join-type mistakes here, not after.",
            "Read the EXPLAIN output: look for sequential scans on large filtered tables, and confirm join order and index use. Be ready to say why the query is fast or slow.",
            "Re-do the same problem with a different construct (self-join vs LAG, subquery vs CTE) and name the tradeoff aloud — interviewers probe the choice, not just the answer.",
        ],
        "procedure_code": (
            "-- Top-N per group: the canonical window-function pattern\n"
            "WITH ranked AS (\n"
            "  SELECT customer_id,\n"
            "         order_date,\n"
            "         amount,\n"
            "         ROW_NUMBER() OVER (PARTITION BY customer_id\n"
            "                          ORDER BY order_date DESC) AS rn\n"
            "  FROM orders\n"
            ")\n"
            "SELECT customer_id, order_date, amount\n"
            "FROM ranked\n"
            "WHERE rn <= 3;  -- latest 3 orders per customer\n"
            "\n"
            "-- Anti-join: customers with no orders (NULL-safe)\n"
            "SELECT c.customer_id\n"
            "FROM customers c\n"
            "WHERE NOT EXISTS (SELECT 1 FROM orders o\n"
            "                WHERE o.customer_id = c.customer_id);"
        ),
        "procedure_lang": "sql",
        "project_brief": (
            "Build the SQL layer of a mock e-commerce warehouse: customers, orders, order_items, products. "
            "Deliver a single .sql file with named CTE stages that answers: (1) top-3 orders per customer, "
            "(2) month-over-month revenue deltas via LAG, (3) customers with no orders in the last 90 days "
            "(anti-join, NULL-safe), and (4) a running revenue total with an explicit frame clause. Every query "
            "gets a one-line grain comment and a one-paragraph EXPLAIN note: which scans happen, which indexes "
            "would help, and why. The deliverable is the interview artifact — defendable line by line."
        ),
        "honesty": (
            "Preparation, not a credential: this module confers no certificate and makes no placement claims. "
            "The patterns here mirror what SQL screens test — window functions, CTEs, joins, grain discipline — "
            "but real interviews vary by company and interviewer. Timed drills measure your current fluency, not "
            "your worth as an engineer; use the misses to aim your redrills."
        ),
        "new_card": {
            "front": "What's the interview line for logical query order?",
            "back": "FROM → WHERE → GROUP BY → HAVING → SELECT → window functions → ORDER BY: 'I write in SELECT order but think in execution order.' It explains why aliases aren't visible in WHERE and why windows can't be filtered in the same level.",
        },
        "explain_pointer": "Covered in this module's 'Concepts' note.",
        "new_quiz": [
            {
                "q": "Which ranking function leaves gaps after ties?",
                "choices": ["ROW_NUMBER", "DENSE_RANK", "RANK", "NTILE"],
                "answer": 2,
                "explain": "RANK assigns the same rank to ties and skips the next numbers; DENSE_RANK doesn't skip. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "To compute each order's running total per customer, you write:",
                "choices": [
                    "SUM(amount) GROUP BY customer_id",
                    "SUM(amount) OVER (PARTITION BY customer_id ORDER BY order_date ROWS UNBOUNDED PRECEDING)",
                    "SUM(amount) OVER (ORDER BY customer_id)",
                    "A self-join on rowid",
                ],
                "answer": 1,
                "explain": "The partition keeps per-customer scope, the order plus frame accumulates correctly. See the 'Hands-on procedure' drill steps in this module.",
            },
            {
                "q": "NOT IN on a nullable subquery column is unsafe because:",
                "choices": [
                    "It's slow",
                    "Any NULL makes the predicate UNKNOWN, returning zero rows",
                    "It's deprecated",
                    "It needs GROUP BY",
                ],
                "answer": 1,
                "explain": "Three-valued logic: NOT IN with a NULL never evaluates true. Use NOT EXISTS. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "A recursive CTE requires which two parts?",
                "choices": [
                    "Two anchor queries",
                    "An anchor query plus a UNION ALL recursive term",
                    "A frame clause and a partition",
                    "GROUP BY and HAVING",
                ],
                "answer": 1,
                "explain": "Anchor seeds the rows; the recursive term extends them until no new rows appear. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "Why does the top-N-per-group pattern need a CTE (or subquery)?",
                "choices": [
                    "CTEs are faster",
                    "Window functions evaluate after WHERE, so you can't filter on the row number in the same query level",
                    "PARTITION BY requires it",
                    "ORDER BY requires it",
                ],
                "answer": 1,
                "explain": "Logical query order puts windows after WHERE — filter one level out. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "SUM(CASE WHEN region = 'west' THEN revenue END) is an example of:",
                "choices": [
                    "A window function",
                    "Conditional aggregation — one scan producing segment metrics",
                    "A recursive CTE",
                    "A correlated subquery",
                ],
                "answer": 1,
                "explain": "'One scan, many answers': the CASE filters inside the aggregate instead of rescanning. See the 'Concepts' glossary in this module.",
            },
        ],
    },
    "data-eng-interview-prep--python-data-wrangling": {
        "summary": (
            "Welcome to the Data Engineering Interview Prep track of the IL-15 Data Engineering & Analytics "
            "Interview Prep course. I'm your instructor for this track, and in this module we're going to master "
            "the coding-screen half of data engineering: turning messy extracts into clean tables with pandas — "
            "groupby, merges, reshapes, chunked reads, and timezone-safe datetimes — in code an interviewer can "
            "follow line by line."
        ),
        "concepts": (
            "- **DataFrame** — pandas' two-dimensional labeled table; the working surface of nearly every wrangling "
            "interview question.\n"
            "- **split-apply-combine** — The groupby grammar: split rows into groups, apply an aggregation or "
            "transform, combine the result; expressed as df.groupby(...).agg/transform/filter.\n"
            "- **merge cardinality** — The expected key uniqueness of a join (one-to-one, many-to-one); asserting it "
            "with validate= turns silent fan-out into a loud error.\n"
            "- **fan-out** — Row multiplication from a many-to-many merge; the classic silent metric corruptor.\n"
            "- **pivot / melt** — Reshaping between wide and long: pivot spreads values into columns, melt gathers "
            "columns into rows.\n"
            "- **vectorization** — Whole-column operations executed in compiled C (NumPy/pandas internals) instead "
            "of Python row loops; typically 10–100x faster and shorter.\n"
            "- **chunksize** — Reading a file in bounded row chunks so a dataset bigger than memory is processed "
            "incrementally.\n"
            "- **naive vs aware datetimes** — Naive timestamps carry no timezone; aware ones do. Mixing them raises "
            "errors, and arithmetic across DST transitions on local time is ambiguous.\n"
            "- **UTC storage** — The convention of persisting timestamps in UTC and converting to local time only at "
            "display; eliminates DST ambiguity at rest.\n"
            "- **type coercion** — pandas silently casting mixed-type columns to object dtype; downstream ops then "
            "sort and sum wrong with no error.\n"
            "- **pure transform function** — A deterministic function of its inputs with no side effects; testable "
            "as plain input/output pairs with no mocks.\n"
            "- **missingness mechanism** — Why data is missing (MCAR/MAR/MNAR); the diagnosis that decides whether "
            "to drop, impute, or flag."
        ),
        "procedure_intro": (
            "The wrangling drill: every exercise starts with a messy extract and ends with a tested, vectorized "
            "transform. Work in passes — profile, clean, reshape, verify — and narrate the cleaning decisions out "
            "loud, because interviewers grade the judgment, not just the output."
        ),
        "procedure_steps": [
            "Profile first: df.shape, df.dtypes, df.isna().sum(), duplicated().sum(). State what you see before touching anything.",
            "Fix types explicitly: pd.to_datetime with a format, astype with errors='raise' thinking — never let silent coercion decide.",
            "Localize datetimes to UTC on ingest (tz_localize / tz_convert); do all arithmetic in UTC and convert to local only for display.",
            "Reshape with vectorized ops: groupby-agg-transform, boolean masks, np.where, string methods. If you type iterrows, stop and rewrite.",
            "Merge defensively: check key uniqueness on both sides first, then merge with validate='m:1' (or the expected cardinality) so fan-out fails loudly.",
            "For files bigger than memory: read with chunksize or usecols, aggregate incrementally, and downcast dtypes; never assume the data fits.",
            "Wrap the transform in a pure function and write input/output assertions for the edge cases: nulls, dupes, DST boundaries.",
        ],
        "procedure_code": (
            "import pandas as pd\n"
            "\n"
            "def clean_orders(df: pd.DataFrame) -> pd.DataFrame:\n"
            "    out = df.copy()\n"
            "    out['order_ts'] = pd.to_datetime(out['order_ts'], utc=True)  # aware, UTC\n"
            "    out = out.drop_duplicates(subset=['order_id'])\n"
            "    # defensive merge: expect many orders to one customer\n"
            "    out = out.merge(customers, on='customer_id', validate='m:1')\n"
            "    # vectorized: no row loops\n"
            "    out['is_weekend'] = out['order_ts'].dt.dayofweek >= 5\n"
            "    return out\n"
            "\n"
            "# chunked read for files bigger than memory\n"
            "chunks = pd.read_csv('orders.csv', chunksize=100_000, usecols=['order_id','order_ts','amount'])\n"
            "total = sum(c['amount'].sum() for c in chunks)"
        ),
        "procedure_lang": "python",
        "project_brief": (
            "Build a wrangling pipeline for a messy e-commerce extract: a 2M-row orders CSV with mixed-type "
            "columns, duplicate order_ids, naive timestamps in three different formats, and a customers table "
            "with a many-to-one relationship. Deliver a single clean_orders.py containing pure transform "
            "functions (UTC-aware datetimes, dedupe on defined keys, validated merges, vectorized features), "
            "a chunked ingestion path that never loads the whole file, and pytest-style input/output assertions "
            "for nulls, dupes, and a DST-boundary timestamp. The README explains each cleaning decision and why."
        ),
        "honesty": (
            "Preparation, not a credential: this module confers no certificate and makes no placement claims. "
            "The pandas idioms here are stable fundamentals, but library APIs evolve — verify signatures against "
            "the current documentation before relying on them in production. Interview screens test method under "
            "pressure; timed reps measure fluency, not engineering worth."
        ),
        "new_card": {
            "front": "What's the interview line for chunked reading?",
            "back": "'I never assume the data fits': chunksize with incremental aggregation, usecols to read only what's needed, dtype downcasting — and if the frame still won't fit, a lazy engine. Memory discipline is a design decision, not an afterthought.",
        },
        "explain_pointer": "Covered in this module's 'Concepts' note.",
        "new_quiz": [
            {
                "q": "df.groupby('dept')['salary'].transform('mean') returns:",
                "choices": [
                    "One row per department",
                    "A Series aligned to the original rows, each row carrying its department's mean",
                    "A pivot table",
                    "An error",
                ],
                "answer": 1,
                "explain": "transform broadcasts the group result back to row shape — the 'keep row detail' half of split-apply-combine. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "validate='m:1' in pd.merge asserts:",
                "choices": [
                    "The merge is fast",
                    "Many rows on the left, unique keys on the right — raising on unexpected fan-out",
                    "One-to-one only",
                    "No nulls allowed",
                ],
                "answer": 1,
                "explain": "Declaring expected cardinality converts silent row multiplication into a loud, catchable error. See the 'Hands-on procedure' in this module.",
            },
            {
                "q": "Arithmetic across a DST fall-back on local (naive) timestamps is dangerous because:",
                "choices": [
                    "It's slow",
                    "The same local time can occur twice — durations and ordering become ambiguous",
                    "pandas can't parse it",
                    "UTC is required by law",
                ],
                "answer": 1,
                "explain": "Store UTC, convert at display: UTC has no DST transitions, so the ambiguity never arises. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "A mixed-type column silently becoming object dtype is dangerous because:",
                "choices": [
                    "It raises immediately",
                    "Numeric-looking strings sort and sum wrong with no error — the problem hides until an aggregate produces nonsense",
                    "It doubles memory",
                    "It breaks groupby",
                ],
                "answer": 1,
                "explain": "Object dtype defers the failure to the worst possible moment. Coerce types explicitly. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "For a 50 GB CSV on a 16 GB machine, the correct first move is:",
                "choices": [
                    "Read it all and hope",
                    "Chunked reading (chunksize) with incremental aggregation, or a lazy engine — never assume the data fits",
                    "Sample 1% and scale up",
                    "Convert to Excel first",
                ],
                "answer": 1,
                "explain": "Bounded-memory processing is the discipline; the procedure spells out the exact loop. See the 'Hands-on procedure' in this module.",
            },
            {
                "q": "melt() is the inverse of:",
                "choices": ["groupby", "pivot — it gathers wide columns back into long rows", "merge", "sort_values"],
                "answer": 1,
                "explain": "pivot spreads values into columns; melt gathers them back. Reshaping fluency is core wrangling. See the 'Concepts' glossary in this module.",
            },
        ],
    },
    "data-eng-interview-prep--batch-pipelines": {
        "summary": (
            "Welcome to the Data Engineering Interview Prep track of the IL-15 Data Engineering & Analytics "
            "Interview Prep course. I'm your instructor for this track, and in this module we're going to whiteboard "
            "batch pipelines end to end — extraction strategy, Airflow orchestration, Spark's partitions and shuffles, "
            "idempotent backfills, and the data-quality gates that catch bad data before stakeholders do. This is the "
            "system-design core of the DE interview."
        ),
        "concepts": (
            "- **full extraction** — Reloading the entire source each run: simple and correct, expensive at scale; "
            "the right default for small dimensions.\n"
            "- **incremental extraction** — Pulling only what changed since a watermark (updated_at, CDC stream): "
            "cheap, but needs late-arrival handling and idempotent loads — 'an optimization with a correctness contract.'\n"
            "- **watermark** — The high-water mark of processed data (a timestamp or offset); everything after it is "
            "new, everything before it is assumed complete.\n"
            "- **DAG (directed acyclic graph)** — Airflow's unit of orchestration: tasks as operators, edges as "
            "dependencies; cycles are forbidden so execution order is always resolvable.\n"
            "- **sensor** — An Airflow operator that waits for external state (a file landing, a partition ready) "
            "before downstream tasks run.\n"
            "- **idempotency** — Safe to retry: repeating an operation doesn't change the outcome beyond the first "
            "application; designed with idempotency keys and partition-scoped writes.\n"
            "- **backfill** — Reprocessing a historical range after a bug or late data; done partition-scoped and "
            "throttled, with a runbook — 'production changes with a plan.'\n"
            "- **partition (Spark)** — The unit of parallelism: data split across workers; too few partitions "
            "starves cores, too many drowns in overhead.\n"
            "- **shuffle** — Repartitioning data across the network (groupBy, join on unpartitioned keys): the most "
            "expensive Spark operation, to be minimized deliberately.\n"
            "- **skew** — One key holding most of the data, so one partition becomes the straggler that bottlenecks "
            "the whole stage; fixed by salting keys or broadcast joins.\n"
            "- **broadcast join** — Replicating a small table to every worker to avoid shuffling the large one; "
            "the standard skew-adjacent optimization.\n"
            "- **data-quality gate** — An in-pipeline check (freshness, volume, schema, distribution) that fails or "
            "quarantines a batch instead of silently passing bad data downstream.\n"
            "- **SLA / alerting** — The on-call contract: how late is too late, who gets paged, and what the "
            "runbook says — interviewers probe this because pipelines are operated, not just built."
        ),
        "procedure_intro": (
            "The whiteboard drill: given a vague 'design a pipeline' prompt, run the same sequence every time — "
            "scope, sketch, walk the data, break it, monitor it. Reps are timed at 30 minutes; the narration is "
            "the deliverable."
        ),
        "procedure_steps": [
            "Scope the problem in the first 3 minutes: sources, volume, freshness requirement, consumers. State the latency need — it decides batch vs streaming.",
            "Draw the stages left to right: extract -> land (raw) -> transform -> serve. Name the storage at each stage and the grain of the data there.",
            "Choose extraction: full for small dimensions, incremental with a watermark for large fact sources; name the late-arrival plan.",
            "Design orchestration: DAG shape, sensors on external dependencies, retries with backoff for transient failures, SLA and alerting for the on-call reality.",
            "Walk a record through the system aloud; then break it: kill the source mid-run, skew one key, deliver late data. Name what each failure does and which gate catches it.",
            "Add the DQ gates: freshness (did it arrive?), volume (counts in band?), schema (shape as expected?), distribution (nulls/dupes/outliers vs history). Fail or quarantine — never silently pass.",
            "Close with the backfill runbook: partition-scoped reruns, throttling, validation against the original run's metrics, and rollback criteria.",
        ],
        "project_brief": (
            "Design and document a batch pipeline for daily e-commerce reporting: orders and clickstream land as "
            "raw files, get modeled into a warehouse, and serve a revenue dashboard. Deliverables: (1) an "
            "architecture diagram (stages, storage, grain at each stage), (2) an Airflow DAG skeleton with tasks, "
            "sensors, retries, and SLA, (3) the DQ gate list with thresholds and fail-vs-quarantine decisions, "
            "(4) a backfill runbook for a corrupted 3-day range, and (5) a Spark note: partition strategy, where "
            "shuffles occur, and the skew-mitigation plan for the top-1% customer key. Present it as a 30-minute "
            "whiteboard talk."
        ),
        "honesty": (
            "Preparation, not a credential: this module confers no certificate and makes no placement claims. "
            "Whiteboard designs are judged on reasoning — tradeoffs named, failure modes covered — not on matching "
            "any single company's stack. Orchestrator and engine APIs evolve; verify current syntax in the official "
            "docs before building for production."
        ),
        "new_card": {
            "front": "What's the interview line for choosing incremental extraction?",
            "back": "'Incremental is an optimization with a correctness contract': you save cost but owe the system a watermark, late-arrival handling, and idempotent loads. If you can't name the contract, you don't get the optimization.",
        },
        "explain_pointer": "Covered in this module's 'Concepts' note.",
        "new_quiz": [
            {
                "q": "A sensor in Airflow is used to:",
                "choices": [
                    "Transform data",
                    "Wait for external state (a file, a partition) before downstream tasks proceed",
                    "Send alerts",
                    "Backfill history",
                ],
                "answer": 1,
                "explain": "Sensors gate the DAG on the outside world — the pipeline doesn't run on data that isn't there yet. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "Salting a skewed join key works by:",
                "choices": [
                    "Encrypting the key",
                    "Appending a random suffix to spread the hot key across partitions, then aggregating the salted pieces back",
                    "Deleting the hot key",
                    "Sorting the key",
                ],
                "answer": 1,
                "explain": "Salt breaks the single hot partition into many; a second-stage aggregation restores correctness. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "A backfill should be partition-scoped because:",
                "choices": [
                    "Partitions are mandatory",
                    "Rerunning everything wastes cost and risks touching good data — scope to the broken range",
                    "It's the Airflow default",
                    "Full reruns are banned",
                ],
                "answer": 1,
                "explain": "Surgical reruns fix the affected range and leave correct history alone. See the 'Hands-on procedure' in this module.",
            },
            {
                "q": "Which failure do Airflow retries with backoff address?",
                "choices": [
                    "Deterministic logic bugs",
                    "Transient failures — flaky APIs, brief outages — where waiting and retrying can succeed",
                    "Schema changes",
                    "Data skew",
                ],
                "answer": 1,
                "explain": "Retries assume temporariness; a deterministic bug needs a code fix, not another attempt. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "A volume gate that fails the batch on a 90% row-count drop is protecting against:",
                "choices": [
                    "Slow queries",
                    "Upstream outages or partial extracts silently producing plausible-looking incomplete data",
                    "Bad SQL syntax",
                    "Too many partitions",
                ],
                "answer": 1,
                "explain": "Row-count anomalies are the cheapest signal that something upstream broke. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "In Spark, the most expensive operation to minimize is:",
                "choices": [
                    "Filtering",
                    "The shuffle — repartitioning data across the network",
                    "Caching",
                    "Column projection",
                ],
                "answer": 1,
                "explain": "Shuffles move data between workers; everything else is comparatively cheap. See the 'Concepts' glossary in this module.",
            },
        ],
    },
    "data-eng-interview-prep--streaming-systems": {
        "summary": (
            "Welcome to the Data Engineering Interview Prep track of the IL-15 Data Engineering & Analytics "
            "Interview Prep course. I'm your instructor for this track, and in this module we're going to tackle "
            "streaming the way interviewers test it: the semantics vocabulary — event time, delivery guarantees, "
            "watermarks, windows — and the judgment call of when streaming is actually worth the complexity."
        ),
        "concepts": (
            "- **event time** — When something happened, recorded in the data; the truth about the world, which "
            "arrives late and out of order.\n"
            "- **processing time** — When the system observed the event (wall clock); convenient but 'lies about "
            "the world' whenever data is delayed.\n"
            "- **watermark** — The system's declaration of how late it's willing to wait: event time up to the "
            "watermark is considered complete; later data is late.\n"
            "- **late data** — Events arriving after their window's watermark; handled via allowed lateness, side "
            "outputs, or corrective updates — every streaming aggregate is a bet about lateness.\n"
            "- **tumbling window** — Fixed, non-overlapping time buckets; each event belongs to exactly one window.\n"
            "- **sliding window** — Overlapping windows advancing by a slide interval; an event contributes to "
            "multiple windows.\n"
            "- **session window** — Activity-based windows split by gaps of inactivity; the right shape for user "
            "sessions.\n"
            "- **topic (Kafka)** — A named, partitioned append-only log; the unit of organization in event streaming.\n"
            "- **partition (Kafka)** — An ordered, immutable sequence within a topic; the unit of parallelism — one "
            "consumer per partition within a group.\n"
            "- **offset** — A partition's per-record sequence number; consumers commit offsets to track progress, "
            "and rewinds replay history.\n"
            "- **at-least-once** — Delivery with retries: no data lost, duplicates possible; the practical default.\n"
            "- **exactly-once (processing)** — Each record's effect applied once, achieved via idempotent consumers or "
            "transactions (Kafka EOS); the strong answer is 'idempotent consumers make at-least-once delivery "
            "effectively exactly-once processing.'\n"
            "- **Lambda architecture** — Batch layer plus speed layer, serving layer merges both; complex, "
            "battle-tested.\n"
            "- **Kappa architecture** — A single streaming pipeline with log replay replacing the batch layer; "
            "simpler, needs a replayable log."
        ),
        "procedure_intro": (
            "The streaming drill: for each scenario, name the semantics before the technology. Interviewers grade "
            "whether you reach for streaming for the right reason — the latency requirement — and whether your "
            "design survives late data and duplicates."
        ),
        "procedure_steps": [
            "State the freshness requirement first: 'how fresh must the data be for the decision it serves?' If hours are fine, defend batch and stop.",
            "Separate event time from processing time; name where late or out-of-order data can enter.",
            "Choose windows (tumbling/sliding/session) from the question's shape, and set the watermark as an explicit lateness bet.",
            "Design the consumer idempotent (idempotency keys, upserts) so at-least-once delivery is safe; name what breaks under duplicates.",
            "Sketch the Kafka layout: topics, partition count from throughput and parallelism needs, consumer groups, offset-commit strategy.",
            "Plan replay: offsets rewind, the log is the source of truth — this is what makes Kappa reprocessing possible.",
            "Name the failure modes: broker loss, consumer lag, poison pills, watermark stalls — and the monitoring that exposes each.",
        ],
        "project_brief": (
            "Design a streaming pipeline for real-time fraud alerts on card transactions: events must be scored "
            "within 60 seconds of authorization. Deliverables: (1) an event-time vs processing-time analysis naming "
            "where late data enters, (2) window and watermark choices with the lateness bet stated, (3) a Kafka "
            "topic/partition/consumer-group layout, (4) the idempotent consumer design that makes at-least-once "
            "safe, (5) a Lambda-vs-Kappa recommendation with the explicit reason, and (6) the lag/lateness "
            "monitoring plan. Defend the complexity: prove minutes matter here."
        ),
        "honesty": (
            "Preparation, not a credential: this module confers no certificate and makes no placement claims. "
            "Streaming semantics are genuinely subtle — this module teaches the interview vocabulary and the "
            "judgment framework, not production operations of any specific streaming platform. Version-specific "
            "delivery guarantees evolve; verify against current documentation before building."
        ),
        "new_card": {
            "front": "What's the interview line for watermarks?",
            "back": "'Every streaming aggregate is a bet about lateness': the watermark is your declared tolerance — how long you wait for stragglers before calling a window complete. Late data past it needs a side output or a correction path.",
        },
        "explain_pointer": "Covered in this module's 'Concepts' note.",
        "new_quiz": [
            {
                "q": "Processing time 'lies about the world' when:",
                "choices": [
                    "Clocks are fast",
                    "Events arrive late or out of order — observation time no longer reflects occurrence time",
                    "Watermarks are set",
                    "Windows overlap",
                ],
                "answer": 1,
                "explain": "Delayed data makes wall-clock assignment wrong; event time tells the truth, late. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "In Kafka, the unit of parallelism for consumers is the:",
                "choices": ["Topic", "Partition — one consumer per partition within a group", "Broker", "Offset"],
                "answer": 1,
                "explain": "Ordering is per-partition, so scaling consumers means scaling partitions. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "Session windows are split by:",
                "choices": [
                    "Fixed 1-hour boundaries",
                    "Gaps of inactivity exceeding a threshold — activity defines the window",
                    "Watermark arrival",
                    "Partition count",
                ],
                "answer": 1,
                "explain": "Sessions follow behavior, not the clock — a gap ends one session and starts the next. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "The strongest defense against duplicate deliveries is:",
                "choices": [
                    "Disabling retries",
                    "Idempotent consumers — reprocessing the same record is harmless",
                    "Faster brokers",
                    "Exactly-once hardware",
                ],
                "answer": 1,
                "explain": "Duplicates are inevitable in distributed systems; idempotency makes them safe. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "Kappa replaces Lambda's batch layer with:",
                "choices": [
                    "A data warehouse",
                    "Log replay — reprocessing the immutable event log through the single streaming pipeline",
                    "Manual backfills",
                    "A second speed layer",
                ],
                "answer": 1,
                "explain": "If the log is replayable, reprocessing replaces batch entirely — one pipeline to maintain. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "Committing Kafka offsets after processing (rather than before) protects against:",
                "choices": [
                    "Duplicates",
                    "Data loss on crash — uncommitted offsets get replayed",
                    "Slow consumers",
                    "Skew",
                ],
                "answer": 1,
                "explain": "Commit-after means a crash replays from the last commit: at-least-once, never lost. See the 'Hands-on procedure' in this module.",
            },
        ],
    },
    "data-eng-interview-prep--data-modeling-warehousing": {
        "summary": (
            "Welcome to the Data Engineering Interview Prep track of the IL-15 Data Engineering & Analytics "
            "Interview Prep course. I'm your instructor for this track, and in this module we're going to do the "
            "work where DE interviews separate memorizers from thinkers: choosing the grain, shaping facts and "
            "dimensions, handling slowly changing dimensions, and knowing why the warehouse is shaped the way it is."
        ),
        "concepts": (
            "- **fact table** — Measurements of business events (orders, clicks): narrow, long, numeric, joined to "
            "dimensions; the grain question is always asked here first.\n"
            "- **dimension table** — Descriptive context (customer, product, date): wide, denormalized in a star "
            "schema, the 'who/what/where' of each fact.\n"
            "- **grain** — The business-event level of a fact table (one row per order line); every modeling "
            "decision flows from declaring it explicitly.\n"
            "- **star schema** — Denormalized dimensions joined directly to the fact table: fewer joins, simpler "
            "queries, faster BI — the analytics default.\n"
            "- **snowflake schema** — Normalized dimensions (dimension tables referencing other dimension tables): "
            "less redundancy, more joins; chosen when storage or write-integrity dominates.\n"
            "- **SCD Type 1** — Overwrite the dimension attribute; history is lost — correct for corrections and "
            "typos.\n"
            "- **SCD Type 2** — New dimension row per change with effective dates and a current flag; history "
            "preserved — the analytics default whenever 'what did we know then?' matters.\n"
            "- **normalization** — Organizing data to reduce redundancy and protect write integrity; the OLTP "
            "virtue, applied to facts.\n"
            "- **denormalization** — Deliberate redundancy for read simplicity and speed; the warehouse virtue, "
            "applied to dimensions.\n"
            "- **bronze layer** — Raw ingested data, immutable and append-only; the system's memory of what "
            "actually arrived.\n"
            "- **silver layer** — Cleaned, validated, conformed data; quality gates sit at the bronze-to-silver "
            "boundary.\n"
            "- **gold layer** — Aggregated, business-ready marts and metrics; what BI and stakeholders consume.\n"
            "- **dbt model** — A versioned SQL transform with tests and documentation as code; the analytics-"
            "engineering unit of warehouse work.\n"
            "- **dbt test** — Data contracts as code: uniqueness, not-null, referential integrity asserted on "
            "every run."
        ),
        "procedure_intro": (
            "The modeling drill: every exercise starts from a business question and ends at a declared grain. "
            "Interviewers don't grade the diagram's beauty — they grade whether you asked 'what's the grain?' "
            "before drawing anything."
        ),
        "procedure_steps": [
            "Restate the business question and name the measurable event: what happened, to whom, when.",
            "Declare the grain explicitly ('one row per order line') and defend it — everything downstream depends on this sentence.",
            "Identify facts (the numbers) vs dimensions (the context); list the dimension attributes the question's slices need.",
            "Choose star vs snowflake: default to star for analytics; reach for snowflake only when you can name the redundancy or write-integrity reason.",
            "For each dimension that changes, pick the SCD type: Type 1 for corrections, Type 2 when history must survive — the interview question is always 'do we need history?'",
            "Layer it bronze/silver/gold: raw landing, conformed cleaning with gates, business-ready marts. Name the contract each layer promises.",
            "Write the dbt-style tests for the model: uniqueness on keys, not-null on required columns, referential integrity to dimensions — contracts, not hopes.",
        ],
        "procedure_code": (
            "-- SCD Type 2: preserve history with effective dates\n"
            "SELECT customer_key,\n"
            "       customer_id,\n"
            "       segment,\n"
            "       effective_from,\n"
            "       effective_to,\n"
            "       is_current\n"
            "FROM dim_customer\n"
            "WHERE '2026-01-15' BETWEEN effective_from\n"
            "      AND COALESCE(effective_to, '9999-12-31');  -- point-in-time correct"
        ),
        "procedure_lang": "sql",
        "project_brief": (
            "Model a warehouse for a subscription SaaS: signups, plans, invoices, cancellations, and product "
            "usage events. Deliverables: (1) a declared grain per fact table with the reasoning, (2) a star schema "
            "diagram (facts, dimensions, keys), (3) SCD decisions per changing dimension with the 'do we need "
            "history?' justification, (4) the bronze/silver/gold layering with the contract each layer promises, "
            "and (5) dbt-style model tests (uniqueness, not-null, relationships). Present the model as a 20-minute "
            "whiteboard walkthrough ending with: 'what breaks if the grain is wrong?'"
        ),
        "honesty": (
            "Preparation, not a credential: this module confers no certificate and makes no placement claims. "
            "Dimensional modeling is a mature discipline — the principles here are stable — but every company's "
            "warehouse has its own conventions; interviews test your reasoning about grain and history, not "
            "allegiance to one school."
        ),
        "new_card": {
            "front": "What's the interview line for SCD type choice?",
            "back": "'Do we need history?' — Type 1 overwrites (corrections, typos: history lost, correctly). Type 2 versions rows with effective dates (history preserved). The question that picks the type is always about the business need for point-in-time truth.",
        },
        "explain_pointer": "Covered in this module's 'Concepts' note.",
        "new_quiz": [
            {
                "q": "The first modeling decision, before any diagram, is:",
                "choices": [
                    "Choosing the database",
                    "Declaring the grain — the business-event level one row represents",
                    "Naming the tables",
                    "Picking SCD types",
                ],
                "answer": 1,
                "explain": "Grain determines facts, keys, and aggregations; everything else follows. See the 'Hands-on procedure' in this module.",
            },
            {
                "q": "A customer changes address and you must keep history. You use:",
                "choices": [
                    "SCD Type 1 — overwrite",
                    "SCD Type 2 — new row with effective dates, history preserved",
                    "Delete and reinsert",
                    "A new fact table",
                ],
                "answer": 1,
                "explain": "'Do we need history?' — yes means versioned rows with date ranges. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "Bronze data is append-only and immutable so that:",
                "choices": [
                    "Queries are fast",
                    "You always have the ground truth of what arrived — reprocessing and auditing stay possible",
                    "Storage is cheap",
                    "BI tools prefer it",
                ],
                "answer": 1,
                "explain": "Bronze is the system's memory; everything downstream is derived and rebuildable from it. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "Snowflake schemas trade away query simplicity for:",
                "choices": [
                    "Speed",
                    "Less redundancy and stronger write integrity in dimensions",
                    "Fewer tables",
                    "Better BI support",
                ],
                "answer": 1,
                "explain": "Normalized dimensions cost joins; the payoff is single-place updates. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "A dbt uniqueness test on a fact's primary key failing means:",
                "choices": [
                    "The query is slow",
                    "The grain contract is broken — duplicate keys, likely a fan-out or double-load",
                    "The schema changed",
                    "The warehouse is down",
                ],
                "answer": 1,
                "explain": "Tests turn the grain assumption into a verified guarantee; a failure names the bug class. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "Denormalizing dimensions in a star schema optimizes for:",
                "choices": [
                    "Write speed",
                    "Read simplicity — analytics queries join less and BI stays fast",
                    "Storage savings",
                    "Ingestion throughput",
                ],
                "answer": 1,
                "explain": "The warehouse is read by analysts; model for the reader. See the 'Concepts' glossary in this module.",
            },
        ],
    },
    "data-eng-interview-prep--pipeline-capstone": {
        "summary": (
            "Welcome to the Data Engineering Interview Prep track of the IL-15 Data Engineering & Analytics "
            "Interview Prep course. I'm your instructor for this track, and in this capstone module you're going to "
            "build the artifact that turns 'tell me about a pipeline' from a story into evidence: one end-to-end "
            "batch pipeline — raw files to tested warehouse models to quality gates — documented and defensible."
        ),
        "concepts": (
            "- **capstone artifact** — A complete, documented build you can walk an interviewer through; evidence "
            "beats narrative in every loop.\n"
            "- **end-to-end lineage** — The traceable path from raw source to served metric: every transformation "
            "named, every stage's contract stated.\n"
            "- **runbook** — The written procedure for operating and recovering the pipeline: backfills, reruns, "
            "rollback — 'backfills are production changes with a plan.'\n"
            "- **reconciliation check** — Comparing pipeline outputs against independent totals (source counts, "
            "prior runs) to prove completeness.\n"
            "- **architecture decision record** — Decision, alternatives considered, why this one, what would "
            "change your mind — the format for narrating design aloud.\n"
            "- **data contract** — The explicit promise between pipeline stages or producers and consumers: "
            "schema, grain, freshness, quality thresholds.\n"
            "- **observability** — Freshness, volume, and distribution signals that tell you the pipeline is "
            "healthy without reading logs.\n"
            "- **defensible design** — A design whose every choice has a stated reason and a named alternative; "
            "what 'narrate the tradeoff, not just the choice' produces."
        ),
        "procedure_intro": (
            "The capstone build sequence: one pipeline, built in order, each stage verified before the next. "
            "Work in vertical slices — a thin end-to-end path first — then harden. The README is written as you "
            "go, not after."
        ),
        "procedure_steps": [
            "Pick the dataset and the business question it answers; attach a decision to the question so you know when the pipeline is 'done.'",
            "Land raw files in bronze: immutable, append-only, with ingestion metadata (source, timestamp, row counts).",
            "Build the silver transforms as named, testable stages (clean -> conform -> model); write the grain comment on every model.",
            "Add DQ gates at the bronze-to-silver boundary: freshness, volume bands, schema checks, null/dup distribution vs history. Fail or quarantine — never silently pass.",
            "Serve the gold layer: the aggregated tables behind one concrete stakeholder question; reconcile outputs against source totals.",
            "Write the backfill and rerun runbook: partition scope, throttling, validation against the original run, rollback criteria.",
            "Draw the architecture diagram and write the README: data flow, grain per stage, decisions with alternatives, and the five-minute narration script.",
            "Rehearse the walkthrough aloud: decision -> alternatives -> why this one -> what would change your mind. Time it at 15 minutes.",
        ],
        "project_brief": (
            "Deliver the capstone: an end-to-end batch pipeline over a public or synthetic e-commerce dataset. "
            "The repository must contain: raw ingestion to bronze, tested silver transforms with declared grains, "
            "DQ gates with thresholds, a gold serving layer answering one stakeholder question, a reconciliation "
            "check against source totals, a backfill runbook, an architecture diagram, and a README with the "
            "decision log. The final deliverable is a 15-minute recorded or live walkthrough: narrate the "
            "tradeoffs, name the failure modes, show a gate catching bad data. This is the portfolio piece you "
            "link when they ask for pipeline experience."
        ),
        "honesty": (
            "Preparation, not a credential: this module confers no certificate and makes no placement claims. A "
            "capstone proves you can build and reason about a pipeline — it doesn't substitute for production "
            "experience, and interviewers will probe the gap honestly. Claim only what the artifact demonstrates; "
            "the decision log is where your real thinking shows."
        ),
        "new_card": {
            "front": "What makes a capstone defensible in an interview?",
            "back": "Every choice has a stated reason and a named alternative: 'we chose X over Y because...' plus a runbook, DQ gates, and a reconciliation check. Interviewers probe decisions, not definitions — the decision log is the artifact they're really reading.",
        },
        "explain_pointer": "Covered in this module's 'Concepts' note.",
        "new_quiz": [
            {
                "q": "A reconciliation check compares pipeline output against:",
                "choices": [
                    "Last year's data",
                    "Independent totals — source counts or prior runs — to prove completeness",
                    "The BI tool",
                    "Nothing; it's optional",
                ],
                "answer": 1,
                "explain": "Completeness needs an external anchor; internal consistency alone can't catch a dropped partition. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "The README's decision log should record, per decision:",
                "choices": [
                    "Only the final choice",
                    "The decision, alternatives considered, why this one, and what would change your mind",
                    "The code",
                    "The timeline",
                ],
                "answer": 1,
                "explain": "Interviewers probe the design space around your choice; the log proves you explored it. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "Building a thin vertical slice first (before hardening) is wise because:",
                "choices": [
                    "It's faster to demo",
                    "End-to-end flow is proven early; hardening then has a working skeleton to attach to",
                    "Tests are easier",
                    "Stakeholders demand it",
                ],
                "answer": 1,
                "explain": "A working thin slice de-risks the architecture; polishing stages in isolation doesn't. See the 'Hands-on procedure' in this module.",
            },
            {
                "q": "When memory blanks on a capstone question, the strongest recovery is:",
                "choices": [
                    "Bluff through",
                    "State what you do know precisely, name the boundary, reason from first principles aloud",
                    "Go silent",
                    "Change the subject",
                ],
                "answer": 1,
                "explain": "Honesty plus reasoning beats confident fabrication — interviewers score both. See the 'Honesty note' in this module.",
            },
            {
                "q": "DQ gates belong at the bronze-to-silver boundary because:",
                "choices": [
                    "It's traditional",
                    "Bad data is cheapest to quarantine at entry — before it flows into every downstream model",
                    "Gold is too late to matter",
                    "Bronze has no schema",
                ],
                "answer": 1,
                "explain": "Gates at layer boundaries stop bad data where fixing it is cheapest. See the 'Hands-on procedure' in this module.",
            },
            {
                "q": "Narrating rejected alternatives during the walkthrough is strong because:",
                "choices": [
                    "It fills time",
                    "Choices are only meaningful against options — it proves you see the design space",
                    "It's humble",
                    "Interviewers expect it",
                ],
                "answer": 1,
                "explain": "A decision without visible alternatives looks like a guess; with them, it's engineering. See the 'Concepts' glossary in this module.",
            },
        ],
    },
    "data-eng-interview-prep--de-mock": {
        "summary": (
            "Welcome to the Data Engineering Interview Prep track of the IL-15 Data Engineering & Analytics "
            "Interview Prep course. I'm your instructor for this track, and in this final track module we're going "
            "to run full interview simulations: timed SQL live-coding, pipeline-design whiteboards, and broken-"
            "pipeline debugging — scored against rubrics, because pressure reps are what convert knowledge into "
            "performance."
        ),
        "concepts": (
            "- **mock circuit** — A full simulated interview loop (SQL screen, system design, debugging, "
            "behavioral) run under real timing with scoring rubrics.\n"
            "- **rubric** — The explicit scoring dimensions: correctness, complexity stated, communication, time "
            "management; what 'scored review' measures against.\n"
            "- **timed SQL round** — Live query writing against the clock; graded on method (grain stated, stages "
            "sketched, narration) as much as the final query.\n"
            "- **whiteboard round** — System-design narration while drawing: components, data flow, failure modes; "
            "'draw the system first so we both know where the deep dive lives.'\n"
            "- **debugging scenario** — A broken pipeline presented as a symptom; graded on systematic narrowing "
            "(extract/transform/load, stage contracts) over log-diving.\n"
            "- **tradeoff argument** — The batch-vs-streaming style debate: arguing from the requirement (latency, "
            "cost, complexity) with both sides' costs named honestly.\n"
            "- **incident story** — The behavioral artifact: bad data, blast radius, quarantine, fix, and the DQ "
            "gate added so it can't recur — 'every data incident ends with a gate.'\n"
            "- **redrill plan** — Misses from scored review converted into specific, dated practice tasks; "
            "'three sliding-window problems, timed, by Thursday' — not 'practice more.'"
        ),
        "procedure_intro": (
            "The mock protocol: simulate the real loop as closely as pressure allows — same timing, same "
            "narration demand, same rubric. One full circuit per session, then scored review, then redrills. No "
            "pausing the clock to think; the clock is the point."
        ),
        "procedure_steps": [
            "Set up the circuit: 15-minute SQL screen, 30-minute pipeline whiteboard, 15-minute debugging scenario, 10-minute incident story. Timer visible, no pauses.",
            "Run the SQL round with the playbook: grain (1 min), CTE stages aloud (2 min), write in passes, verify on a mental dataset, narrate throughout.",
            "Run the whiteboard: draw components and data flow first, then deep-dive where probed; narrate tradeoffs and name rejected alternatives.",
            "Run the debugging scenario: narrow by stage (extract/transform/load), check each stage's contract (counts, schema, gates) — the broken promise names the culprit.",
            "Tell the incident story in STAR with data texture: the bad data, who consumed it, blast radius, quarantine, fix, and the gate you added.",
            "Score every round against the rubric immediately after: correctness, complexity stated, communication, time. Write the misses down verbatim.",
            "Convert each miss into a dated redrill task before the next circuit; the plan is specific and scheduled, or it evaporates.",
        ],
        "project_brief": (
            "Run and document three full mock circuits over two weeks. Deliverables per circuit: (1) the prompts "
            "used (SQL, whiteboard, debugging, behavioral), (2) rubric scores per round with verbatim misses, "
            "(3) the redrill plan with dates, and (4) a one-page trend summary: which miss categories are shrinking "
            "and which persist. The final deliverable is your readiness self-assessment: the three answers you're "
            "proudest of and the one round type still costing you points — with the plan to close it."
        ),
        "honesty": (
            "Preparation, not a credential: this module confers no certificate and makes no placement claims. "
            "Mocks simulate pressure; they can't replicate a specific company's loop or interviewer. Scores measure "
            "your performance on the day against the rubric — use them to aim redrills, not to predict outcomes. "
            "Real interviews also weigh team fit and communication beyond any rubric."
        ),
        "new_card": {
            "front": "What does the rubric actually measure?",
            "back": "Correctness, complexity stated, communication, time management — scored per round, immediately after. The misses go down verbatim and become dated redrill tasks. The rubric turns 'I did badly' into 'I lost points on narration in round 2, redrill Thursday.'",
        },
        "explain_pointer": "Covered in this module's 'Concepts' note.",
        "new_quiz": [
            {
                "q": "The first minute of a timed SQL round should be spent:",
                "choices": [
                    "Writing the SELECT",
                    "Clarifying the grain and edge cases — the question's unit decides the query",
                    "Choosing the editor theme",
                    "Reading the schema twice",
                ],
                "answer": 1,
                "explain": "Grain discipline first; a fast wrong-grain query scores worse than a slower correct one. See the 'Hands-on procedure' in this module.",
            },
            {
                "q": "In a debugging scenario, checking stage contracts first works because:",
                "choices": [
                    "Logs are unavailable",
                    "Each stage promises an output shape — the broken promise localizes the bug",
                    "It's faster than thinking",
                    "Interviewers require it",
                ],
                "answer": 1,
                "explain": "Contract violations pinpoint the stage; log-diving without them is wandering. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "A mock score is most useful when it:",
                "choices": [
                    "Is high",
                    "Is tied to named misses that become dated redrill tasks",
                    "Is shared publicly",
                    "Beats your friend's",
                ],
                "answer": 1,
                "explain": "Specificity turns review into training; the number alone teaches nothing. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "The deciding question in a batch-vs-streaming debate is:",
                "choices": [
                    "Which is more modern",
                    "'How fresh must the data be for the decision it serves?' — latency need sets the architecture",
                    "Team preference",
                    "Cost only",
                ],
                "answer": 1,
                "explain": "Freshness requirements are the only honest arbiter; everything else is preference. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "Ending the incident story with the added DQ gate is strong because:",
                "choices": [
                    "Gates are trendy",
                    "It proves systemic learning — the incident produced prevention, not just a fix",
                    "It's required by the rubric",
                    "Stories need endings",
                ],
                "answer": 1,
                "explain": "Prevention is the deliverable; the fix was just the homework. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "No pausing the mock clock to think — why?",
                "choices": [
                    "Cruelty",
                    "The clock is the training stimulus; pressure management is part of what's being built",
                    "Rubrics forbid it",
                    "Time is limited",
                ],
                "answer": 1,
                "explain": "Mocks convert knowledge into performance under pressure; removing pressure removes the conversion. See the 'Hands-on procedure' in this module.",
            },
        ],
    },
}

if __name__ == "__main__":
    apply_all(load(), CONTENT)

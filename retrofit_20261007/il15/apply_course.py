"""IL-15 retrofit: course-level additions.

- Adds terminalSims (renderer in docs/university/course-shell.js consumes them
  generically: prompt + exact-match cmd/out pairs, fuzzy suggestion).
- Does NOT add trainers: the only interactive trainer kind the renderer
  implements is 'cidr' (CIDR subnet math); any other kind renders a false
  placeholder ('ships with the Phase 2 course document'), and inventing new
  trainer kinds is out of scope.
- Verifies course-level keys (arc, priorities, battlePlan, mockTasks,
  cheatSheets, answerBank, mockMinutes, sourceLinks, honestyNote) exist and
  match the template's shapes.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load, save, COURSE

SQL_SIM = {
    "id": "sql-lab",
    "title": "SQL lab terminal",
    "brief": "Practice the SQL interview patterns from this course — anti-joins, window functions, "
    "CTEs, grain checks — against a small e-commerce schema in a simulated psql session.",
    "prompt": "sql-lab=#",
    "commands": [
        {"cmd": "\\dt", "out": "            List of relations\n Schema |   Name    | Type  |  Owner  \n--------+-----------+-------+---------\n public | customers | table | learner\n public | orders    | table | learner\n public | products  | table | learner\n(3 rows)"},
        {"cmd": "SELECT COUNT(*) FROM customers;", "out": " count \n-------\n  1200\n(1 row)"},
        {"cmd": "SELECT COUNT(*), COUNT(email) FROM customers;", "out": " count | count \n-------+-------\n  1200 |  1187\n(1 row)\n-- 13 customers have NULL email: COUNT(column) skips NULLs"},
        {"cmd": "SELECT customer_id FROM customers WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = customers.customer_id) LIMIT 3;", "out": " customer_id \n-------------\n         104\n         217\n         389\n(3 rows)\n-- anti-join: customers with no orders (NULL-safe)"},
        {"cmd": "SELECT customer_id, amount, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) AS rn FROM orders LIMIT 4;", "out": " customer_id | amount | rn \n-------------+--------+----\n           7 |  49.99 |  1\n           7 |  19.99 |  2\n          12 |  89.00 |  1\n          12 |  12.50 |  2\n(4 rows)\n-- latest orders first per customer: top-N pattern starts here"},
        {"cmd": "WITH ranked AS (SELECT customer_id, amount, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY amount DESC) AS rn FROM orders) SELECT customer_id, amount FROM ranked WHERE rn = 1 LIMIT 3;", "out": " customer_id | amount \n-------------+--------\n           7 |  49.99\n          12 |  89.00\n          31 | 210.00\n(3 rows)\n-- top-1 order per customer: window in CTE, filter one level out"},
        {"cmd": "SELECT DATE_TRUNC('month', order_date) AS m, SUM(amount) AS revenue, SUM(amount) - LAG(SUM(amount)) OVER (ORDER BY DATE_TRUNC('month', order_date)) AS delta FROM orders GROUP BY 1 ORDER BY 1 LIMIT 3;", "out": "          m          | revenue  |  delta  \n---------------------+----------+---------\n 2026-01-01 00:00:00 | 18420.50 |         \n 2026-02-01 00:00:00 | 20110.00 | 1689.50\n 2026-03-01 00:00:00 | 19755.25 | -354.75\n(3 rows)\n-- month-over-month delta via LAG"},
        {"cmd": "SELECT SUM(amount) OVER (ORDER BY order_date ROWS UNBOUNDED PRECEDING) AS running_total FROM orders ORDER BY order_date LIMIT 3;", "out": " running_total \n---------------\n         49.99\n         69.98\n        158.98\n(3 rows)\n-- explicit frame: no surprises"},
        {"cmd": "EXPLAIN SELECT * FROM orders WHERE customer_id = 7;", "out": " Index Scan using orders_customer_id_idx on orders  (cost=0.29..8.31 rows=4 width=72)\n   Index Cond: (customer_id = 7)\n-- index used: no sequential scan on the filtered table"},
        {"cmd": "SELECT d.day, COUNT(o.order_id) FROM generate_series('2026-01-01'::date, '2026-01-03'::date, '1 day') AS d(day) LEFT JOIN orders o ON o.order_date = d.day GROUP BY d.day ORDER BY d.day;", "out": "    day     | count \n------------+-------\n 2026-01-01 |    42\n 2026-01-02 |     0\n 2026-01-03 |    37\n(3 rows)\n-- date spine: zero-activity days show as zero, not gaps"},
        {"cmd": "SELECT user_id, COUNT(DISTINCT CASE WHEN step >= 2 THEN user_id END) FROM funnel GROUP BY user_id LIMIT 1;", "out": "ERROR: column \"user_id\" must appear in the GROUP BY clause or be used in an aggregate\n-- grain check: every non-aggregated SELECT column must be grouped or aggregated"},
        {"cmd": "SELECT COUNT(DISTINCT customer_id) FROM orders;", "out": " count \n-------\n   863\n(1 row)\n-- distinct customers who ordered: grain = one row per customer"},
        {"cmd": "SELECT 'grain: one row per customer-month';", "out": "        ?column?        \n-------------------------\n grain: one row per customer-month\n(1 row)\n-- state the grain before you write the query"},
    ],
}

PANDAS_SIM = {
    "id": "pandas-repl",
    "title": "pandas REPL terminal",
    "brief": "Practice the wrangling idioms from this course — groupby patterns, validated merges, "
    "vectorized transforms — in a simulated Python REPL with a small orders DataFrame.",
    "prompt": ">>>",
    "commands": [
        {"cmd": "df.shape", "out": "(5000, 5)"},
        {"cmd": "df.dtypes", "out": "order_id       int64\ncustomer_id    int64\norder_ts      object   <-- fix me: to_datetime(utc=True)\namount       float64\nsegment       object\ndtype: object"},
        {"cmd": "df['order_ts'] = pd.to_datetime(df['order_ts'], utc=True)", "out": ""},
        {"cmd": "df.duplicated(subset=['order_id']).sum()", "out": "np.int64(17)\n-- 17 duplicate order_ids: dedupe on the defined key"},
        {"cmd": "df = df.drop_duplicates(subset=['order_id'])", "out": ""},
        {"cmd": "df.groupby('segment')['amount'].sum()", "out": "segment\nenterprise    184020.50\nsmb            96110.25\nstartup        40211.00\nName: amount, dtype: float64"},
        {"cmd": "df['seg_mean'] = df.groupby('segment')['amount'].transform('mean')", "out": "-- transform broadcasts back to row shape: every row keeps its identity"},
        {"cmd": "df['is_weekend'] = df['order_ts'].dt.dayofweek >= 5", "out": "-- vectorized: no iterrows, no apply loop"},
        {"cmd": "before = len(df); df = df.merge(customers, on='customer_id', validate='m:1'); len(df) == before", "out": "True\n-- validated merge: cardinality asserted, no silent fan-out"},
        {"cmd": "pd.read_csv('orders.csv', chunksize=100_000)", "out": "<pandas.io.parsers.readers.TextFileReader object>\n-- lazy chunks: process files bigger than memory incrementally"},
        {"cmd": "df.isna().sum()", "out": "order_id       0\ncustomer_id    0\norder_ts       0\namount         4\nsegment        0\ndtype: int64\n-- profile first: 4 missing amounts need a recorded decision"},
        {"cmd": "df['amount'].mean()", "out": "np.float64(61.42)\n-- mean imputation would shrink variance: a choice with consequences, not a default"},
        {"cmd": "df.groupby('customer_id').filter(lambda g: g['amount'].sum() > 1000).shape", "out": "(812, 7)\n-- groupby-filter: keep groups meeting a condition"},
    ],
}

TEMPLATE_KEYS = {
    "arc": ["phase", "title", "body"],
    "priorities": ["label", "minutes"],
    "battlePlan": ["id", "title", "minutes", "detail"],
    "mockTasks": ["id", "type", "q", "choices", "answer", "explain"],
    "cheatSheets": ["title", "blocks"],
    "answerBank": ["q", "a"],
    "sourceLinks": ["name", "url", "retrieved"],
}


def main():
    course = load()

    # course-level key audit vs template shapes
    problems = []
    for key, fields in TEMPLATE_KEYS.items():
        if key not in course:
            problems.append("missing key: %s" % key)
            continue
        items = course[key]
        if not items:
            problems.append("empty list: %s" % key)
            continue
        missing = [f for f in fields if f not in items[0]]
        if missing:
            problems.append("%s[0] missing fields: %s" % (key, missing))
    for key in ["mockMinutes", "honestyNote"]:
        if key not in course:
            problems.append("missing key: %s" % key)
    if not isinstance(course.get("mockMinutes"), int):
        problems.append("mockMinutes is not int")
    # sourceLinks: every entry needs a retrieved date
    for s in course.get("sourceLinks", []):
        if not s.get("retrieved"):
            problems.append("sourceLink missing retrieved: %s" % s.get("name"))

    # mockTasks quiz-shape audit
    for t in course.get("mockTasks", []):
        if len(t.get("choices", [])) != 4 or not (0 <= t.get("answer", -1) <= 3) or not t.get("explain", "").strip():
            problems.append("mockTask shape problem: %s" % t.get("id"))

    if problems:
        raise SystemExit("course-level problems:\n" + "\n".join(problems))
    print("course-level keys OK: arc=%d priorities=%d battlePlan=%d mockTasks=%d cheatSheets=%d answerBank=%d sourceLinks=%d mockMinutes=%d" % (
        len(course["arc"]), len(course["priorities"]), len(course["battlePlan"]),
        len(course["mockTasks"]), len(course["cheatSheets"]), len(course["answerBank"]),
        len(course["sourceLinks"]), course["mockMinutes"]))

    course["terminalSims"] = [SQL_SIM, PANDAS_SIM]
    # keep trainers as-is (empty list); renderer handles [] generically
    if "trainers" not in course:
        course["trainers"] = []
    save(course)
    print("terminalSims added (2); file re-validated")


if __name__ == "__main__":
    main()

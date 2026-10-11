# Fix quiz answer distribution in gen_part1.py to exactly 2/2/2/2 per module
import re

p = '/home/hatch/workspace/apex-audit/docs/university/data/courses/_il26-build/gen_part1.py'
s = open(p).read()

fixes = [
# ---- M41 ----
# q2 -> idx 2
('''["con.execute('SELECT g, AVG(x) AS a FROM df GROUP BY g').df()", "con.execute('SELECT g, AVG(x) FROM df').to_sql()", "duckdb.query(df).mean('x')", "con.register('df'); con.sql('AVG(x) BY g')"]''',
 '''["con.execute('SELECT g, AVG(x) FROM df').to_sql()", "duckdb.query(df).mean('x')", "con.execute('SELECT g, AVG(x) AS a FROM df GROUP BY g').df()", "con.register('df'); con.sql('AVG(x) BY g')"]'''),
# q3 -> idx 3
('''["Keeps the top 3 rows by revenue without needing a subquery around the window function", "Deletes all but 3 rows from the table", "Limits the window frame to 3 preceding rows", "Returns the 3rd row only"]''',
 '''["Deletes all but 3 rows from the table", "Limits the window frame to 3 preceding rows", "Returns the 3rd row only", "Keeps the top 3 rows by revenue without needing a subquery around the window function"]'''),
# q4 -> idx 1
('''["Ingest once into a persistent .duckdb file (or Parquet) and query the stored table thereafter", "Increase the CSV header row count", "Switch to row-by-row Python iteration", "Rename the file with a .parquet extension"]''',
 '''["Increase the CSV header row count", "Ingest once into a persistent .duckdb file (or Parquet) and query the stored table thereafter", "Switch to row-by-row Python iteration", "Rename the file with a .parquet extension"]'''),
# q6 -> idx 2
('''["PIVOT the query ON region USING SUM(amount), feeding the BI tool a wide tidy table", "Export raw rows and pivot manually in the dashboard designer every refresh", "Write one query per region and UNION them by hand each month", "Sort by region and hope the BI tool pivots automatically"]''',
 '''["Export raw rows and pivot manually in the dashboard designer every refresh", "Write one query per region and UNION them by hand each month", "PIVOT the query ON region USING SUM(amount), feeding the BI tool a wide tidy table", "Sort by region and hope the BI tool pivots automatically"]'''),
# q7 -> idx 3
('''["Agree — embedded engines handle all warehouse workloads", "Disagree — warehouses add concurrent writers, governed access, and TB-scale managed storage that embedded DuckDB does not", "Agree — but only on Tuesdays", "Disagree — DuckDB cannot run SQL"]''',
 '''["Agree — embedded engines handle all warehouse workloads", "Agree — but only on Tuesdays", "Disagree — DuckDB cannot run SQL", "Disagree — warehouses add concurrent writers, governed access, and TB-scale managed storage that embedded DuckDB does not"]'''),
# q8 -> idx 0
('''["SELECT * LIMIT 5 and eyeball it", "SELECT COUNT(*), COUNT(amount) FROM orders — compare total rows vs non-null amounts", "Assume the CSV is clean because it loaded without error", "Check the file size in the OS"]''',
 '''["SELECT COUNT(*), COUNT(amount) FROM orders — compare total rows vs non-null amounts", "SELECT * LIMIT 5 and eyeball it", "Assume the CSV is clean because it loaded without error", "Check the file size in the OS"]'''),
# ---- M42 ----
# q3 -> idx 1
('''["df.filter(pl.col('amount') > 100)", "df.where('amount > 100')", "df.query(pl.amount > 100)", "df.loc[pl.col('amount') > 100]"]''',
 '''["df.where('amount > 100')", "df.filter(pl.col('amount') > 100)", "df.query(pl.amount > 100)", "df.loc[pl.col('amount') > 100]"]'''),
# q4 -> idx 1
('''["Projection pushdown reads only the 3 needed columns from disk", "Polars skips the header row", "pandas reads the file twice", "CSV files are natively columnar"]''',
 '''["Polars skips the header row", "Projection pushdown reads only the 3 needed columns from disk", "pandas reads the file twice", "CSV files are natively columnar"]'''),
# q5 -> idx 2
('''["Stay with pandas — ecosystem and team norms outweigh a speed gain you don't need", "Rewrite everything in Polars immediately for principle", "Use Polars but convert at every function boundary for fun", "Ban pandas from the repo"]''',
 '''["Rewrite everything in Polars immediately for principle", "Use Polars but convert at every function boundary for fun", "Stay with pandas — ecosystem and team norms outweigh a speed gain you don't need", "Ban pandas from the repo"]'''),
# q6 -> idx 2
('''["Call .explain() and read the optimized plan before changing anything", "Add more .filter() calls randomly", "Switch to pandas", "Restart the kernel"]''',
 '''["Add more .filter() calls randomly", "Switch to pandas", "Call .explain() and read the optimized plan before changing anything", "Restart the kernel"]'''),
# q7 -> idx 3
('''["Polars has a strict, uniform null type; pandas mixes NaN/None/NaT across dtypes", "pandas has no nulls", "Polars silently drops nulls on read", "Both handle nulls identically"]''',
 '''["pandas has no nulls", "Polars silently drops nulls on read", "Both handle nulls identically", "Polars has a strict, uniform null type; pandas mixes NaN/None/NaT across dtypes"]'''),
# q8 -> idx 3
('''["New modules in Polars, convert at boundaries (.to_pandas()/pl.from_pandas()), no big-bang rewrite", "Rewrite all files in one commit over the weekend", "Run both engines on every query and average results", "Delete pandas from requirements to force the issue"]''',
 '''["Rewrite all files in one commit over the weekend", "Run both engines on every query and average results", "Delete pandas from requirements to force the issue", "New modules in Polars, convert at boundaries (.to_pandas()/pl.from_pandas()), no big-bang rewrite"]'''),
]

for old, new in fixes:
    assert s.count(old) == 1, f'pattern not unique/found: {old[:60]!r} count={s.count(old)}'
    s = s.replace(old, new)

# M41: q5 answer stays 1, q6/q7/q8 were 1 -> now q6=2 q7=3 q8=0. Patch answer fields:
# M41 quiz answers currently: [0,0,0,0,1,1,1,1]; need [0,2,3,1,1,2,3,0]
# M42 currently all 0; need [0,0,1,1,2,2,3,3]
def set_answers(section, new_answers):
    out, idx, pos = [], 0, 0
    import re as _re
    def repl(m):
        nonlocal idx
        v = new_answers[idx]; idx += 1
        return f'"answer": {v}'
    new_section, n = _re.subn(r'"answer": \d', repl, section)
    assert n == len(new_answers), f'expected {len(new_answers)} answers, found {n}'
    return new_section

head, m42 = s.split('M42 = {', 1)
head = set_answers(head, [0,2,3,1,1,2,3,0])
m42 = set_answers(m42, [0,0,1,1,2,2,3,3])
s = head + 'M42 = {' + m42
open(p, 'w').write(s)
print('choice reorder + answers ok')

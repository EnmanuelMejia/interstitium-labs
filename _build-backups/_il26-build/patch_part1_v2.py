# Patch v2: apply choice reorders + answer redistribution to gen_part1.py (current on-disk state)
import re

p = '/home/hatch/workspace/apex-audit/docs/university/data/courses/_il26-build/gen_part1.py'
s = open(p, encoding='utf-8').read()
EM = '\u2014'

def Q(*choices):
    return '[' + ', '.join('"' + c + '"' for c in choices) + ']'

# (old_choices_tuple, new_choices_tuple) using plain quotes; file source has \" which parses to "
reorders = [
 # M41 q2 -> answer idx 2
 (("con.execute('SELECT g, AVG(x) AS a FROM df GROUP BY g').df()",
   "con.execute('SELECT g, AVG(x) FROM df').to_sql()",
   "duckdb.query(df).mean('x')",
   "con.register('df'); con.sql('AVG(x) BY g')"),
  ("con.execute('SELECT g, AVG(x) FROM df').to_sql()",
   "duckdb.query(df).mean('x')",
   "con.execute('SELECT g, AVG(x) AS a FROM df GROUP BY g').df()",
   "con.register('df'); con.sql('AVG(x) BY g')")),
 # M41 q3 -> idx 3
 (("Keeps the top 3 rows by revenue without needing a subquery around the window function",
   "Deletes all but 3 rows from the table",
   "Limits the window frame to 3 preceding rows",
   "Returns the 3rd row only"),
  ("Deletes all but 3 rows from the table",
   "Limits the window frame to 3 preceding rows",
   "Returns the 3rd row only",
   "Keeps the top 3 rows by revenue without needing a subquery around the window function")),
 # M41 q4 -> idx 1
 (("Ingest once into a persistent .duckdb file (or Parquet) and query the stored table thereafter",
   "Increase the CSV header row count",
   "Switch to row-by-row Python iteration",
   "Rename the file with a .parquet extension"),
  ("Increase the CSV header row count",
   "Ingest once into a persistent .duckdb file (or Parquet) and query the stored table thereafter",
   "Switch to row-by-row Python iteration",
   "Rename the file with a .parquet extension")),
 # M41 q6 -> idx 2
 ((f"PIVOT the query ON region USING SUM(amount), feeding the BI tool a wide tidy table",
   "Export raw rows and pivot manually in the dashboard designer every refresh",
   "Write one query per region and UNION them by hand each month",
   "Sort by region and hope the BI tool pivots automatically"),
  ("Export raw rows and pivot manually in the dashboard designer every refresh",
   "Write one query per region and UNION them by hand each month",
   f"PIVOT the query ON region USING SUM(amount), feeding the BI tool a wide tidy table",
   "Sort by region and hope the BI tool pivots automatically")),
 # M41 q7 -> idx 3
 ((f"Agree {EM} embedded engines handle all warehouse workloads",
   f"Disagree {EM} warehouses add concurrent writers, governed access, and TB-scale managed storage that embedded DuckDB does not",
   f"Agree {EM} but only on Tuesdays",
   f"Disagree {EM} DuckDB cannot run SQL"),
  (f"Agree {EM} embedded engines handle all warehouse workloads",
   f"Agree {EM} but only on Tuesdays",
   f"Disagree {EM} DuckDB cannot run SQL",
   f"Disagree {EM} warehouses add concurrent writers, governed access, and TB-scale managed storage that embedded DuckDB does not")),
 # M42 q3 -> idx 1
 (("df.filter(pl.col('amount') > 100)",
   "df.where('amount > 100')",
   "df.query(pl.amount > 100)",
   "df.loc[pl.col('amount') > 100]"),
  ("df.where('amount > 100')",
   "df.filter(pl.col('amount') > 100)",
   "df.query(pl.amount > 100)",
   "df.loc[pl.col('amount') > 100]")),
 # M42 q4 -> idx 1
 (("Projection pushdown reads only the 3 needed columns from disk",
   "Polars skips the header row",
   "pandas reads the file twice",
   "CSV files are natively columnar"),
  ("Polars skips the header row",
   "Projection pushdown reads only the 3 needed columns from disk",
   "pandas reads the file twice",
   "CSV files are natively columnar")),
 # M42 q5 -> idx 2
 ((f"Stay with pandas {EM} ecosystem and team norms outweigh a speed gain you don't need",
   "Rewrite everything in Polars immediately for principle",
   "Use Polars but convert at every function boundary for fun",
   "Ban pandas from the repo"),
  ("Rewrite everything in Polars immediately for principle",
   "Use Polars but convert at every function boundary for fun",
   f"Stay with pandas {EM} ecosystem and team norms outweigh a speed gain you don't need",
   "Ban pandas from the repo")),
 # M42 q6 -> idx 2
 (("Call .explain() and read the optimized plan before changing anything",
   "Add more .filter() calls randomly",
   "Switch to pandas",
   "Restart the kernel"),
  ("Add more .filter() calls randomly",
   "Switch to pandas",
   "Call .explain() and read the optimized plan before changing anything",
   "Restart the kernel")),
 # M42 q7 -> idx 3
 (("Polars has a strict, uniform null type; pandas mixes NaN/None/NaT across dtypes",
   "pandas has no nulls",
   "Polars silently drops nulls on read",
   "Both handle nulls identically"),
  ("pandas has no nulls",
   "Polars silently drops nulls on read",
   "Both handle nulls identically",
   "Polars has a strict, uniform null type; pandas mixes NaN/None/NaT across dtypes")),
 # M42 q8 -> idx 3
 (("New modules in Polars, convert at boundaries (.to_pandas()/pl.from_pandas()), no big-bang rewrite",
   "Rewrite all files in one commit over the weekend",
   "Run both engines on every query and average results",
   "Delete pandas from requirements to force the issue"),
  ("Rewrite all files in one commit over the weekend",
   "Run both engines on every query and average results",
   "Delete pandas from requirements to force the issue",
   "New modules in Polars, convert at boundaries (.to_pandas()/pl.from_pandas()), no big-bang rewrite")),
]

for old_t, new_t in reorders:
    old_s, new_s = Q(*old_t), Q(*new_t)
    assert s.count(old_s) == 1, f'old not unique: {old_s[:70]} count={s.count(old_s)}'
    assert new_s not in s or s.count(new_s) == 0 or True
    s = s.replace(old_s, new_s)

def set_answers(section, new_answers):
    idx = 0
    def repl(m):
        nonlocal idx
        v = new_answers[idx]; idx += 1
        return f'"answer": {v}'
    new_section, n = re.subn(r'"answer": \d', repl, section)
    assert n == len(new_answers), f'expected {len(new_answers)} answers, found {n}'
    return new_section

head, m42 = s.split('M42 = {', 1)
head = set_answers(head, [0,2,3,1,1,2,3,0])
m42 = set_answers(m42, [0,0,1,1,2,2,3,3])
s = head + 'M42 = {' + m42
open(p, 'w', encoding='utf-8').write(s)
print('patch v2 applied')

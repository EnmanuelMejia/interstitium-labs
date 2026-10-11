import json, os

OUT_DIR = "/home/hatch/workspace/apex-audit/docs/university/data/courses/_il26-build"
OUT = os.path.join(OUT_DIR, "interactive.json")
os.makedirs(OUT_DIR, exist_ok=True)

data = {
    "fragment": "G",
    "description": "Interactive element definitions for IL-26 (every module >= 2 elements). All datasets fictional and original. Renderer shell built separately.",
    "sqlPlaygrounds": [],
    "pythonExercises": [],
    "daxPlaygrounds": [],
    "terminalSims": [],
    "branchingScenarios": [],
    "clickSims": [],
    "interactivityAudit": []
}

def sqlpg(pid, mid, title, dname, cols, rows, tasks):
    return {"id": pid, "moduleId": mid, "title": title,
            "dataset": {"name": dname, "columns": cols, "rows": rows},
            "tasks": [{"prompt": p, "starterSQL": s, "solutionSQL": sol,
                       "expectedRows": n, "hint": h} for (p, s, sol, n, h) in tasks]}

def pyex(pid, mid, title, tasks):
    return {"id": pid, "moduleId": mid, "title": title,
            "tasks": [{"prompt": p, "starterCode": s, "solutionCode": sol,
                       "checks": [{"description": d, "test": t} for (d, t) in checks]}
                      for (p, s, sol, checks) in tasks]}

def daxpg(pid, mid, title, tasks):
    return {"id": pid, "moduleId": mid, "title": title,
            "tasks": [{"prompt": p, "table": t, "expectedDAX": e,
                       "accept": a, "explain": x} for (p, t, e, a, x) in tasks]}

def termsim(pid, mid, title, scenario, cmds):
    return {"id": pid, "moduleId": mid, "title": title, "scenario": scenario,
            "gradedCommands": [{"command": c, "response": r, "hint": h} for (c, r, h) in cmds]}

def branch(pid, mid, title, start, nodes):
    return {"id": pid, "moduleId": mid, "title": title, "start": start,
            "nodes": {nid: {"text": txt, "choices": [{"label": l, "next": nx, "feedback": f} for (l, nx, f) in ch]}
                      for (nid, txt, ch) in nodes}}

def clicksim(pid, mid, tool, title, steps):
    return {"id": pid, "moduleId": mid, "tool": tool, "title": title,
            "steps": [{"screen": sc, "instruction": ins, "hotspots": hs, "feedback": fb}
                      for (sc, ins, hs, fb) in steps]}

SP = data["sqlPlaygrounds"]

# ---------- SQL playground: M28 Exponents & Logarithms ----------
SP.append(sqlpg("sql-il26-m28-growth", "IL26-M28", "Logarithms in SQL: linearizing growth",
    "growth_metrics",
    ["company", "month", "users", "revenue"],
    [["Northwind Labs","2026-01",1200,18000],["Northwind Labs","2026-02",1500,22500],
     ["Northwind Labs","2026-03",1900,28500],["Northwind Labs","2026-04",2400,36000],
     ["Beacon Analytics","2026-01",800,9600],["Beacon Analytics","2026-02",1100,13200],
     ["Beacon Analytics","2026-03",1600,19200],["Beacon Analytics","2026-04",2300,27600],
     ["Copperline","2026-01",5000,75000],["Copperline","2026-02",5200,78000],
     ["Copperline","2026-03",5400,81000],["Copperline","2026-04",5650,84750]],
    [
     ("List each company and month with the natural log of users, so exponential growth plots as a straight line.",
      "SELECT company, month, users\nFROM growth_metrics\nORDER BY company, month;",
      "SELECT company, month, LN(users) AS ln_users\nFROM growth_metrics\nORDER BY company, month;",
      12,
      "Use the LN() function on the users column and alias it ln_users."),
     ("Compute the month-over-month growth factor per company: users divided by the prior month's users (use LAG).",
      "SELECT company, month, users\nFROM growth_metrics;",
      "SELECT company, month,\n  users / LAG(users) OVER (PARTITION BY company ORDER BY month) AS growth_factor\nFROM growth_metrics\nORDER BY company, month;",
      12,
      "LAG(users) OVER (PARTITION BY company ORDER BY month) gives the prior month; the first month per company yields NULL."),
     ("Show companies with April users above 2000, with LOG10(users) for a log-scale chart axis.",
      "SELECT company, users\nFROM growth_metrics\nWHERE month = '2026-04';",
      "SELECT company, LOG10(users) AS log10_users\nFROM growth_metrics\nWHERE month = '2026-04' AND users > 2000\nORDER BY company;",
      3,
      "Filter month = '2026-04' and users > 2000; all three companies qualify.")
    ]))

# ---------- SQL playground: M29 Summation Notation ----------
SP.append(sqlpg("sql-il26-m29-summation", "IL26-M29", "Summation notation as SQL aggregates",
    "daily_sales",
    ["store", "day", "amount"],
    [["Harbor","2026-03-01",420],["Harbor","2026-03-02",510],["Harbor","2026-03-03",380],["Harbor","2026-03-04",620],
     ["Lakeshore","2026-03-01",300],["Lakeshore","2026-03-02",290],["Lakeshore","2026-03-03",410],["Lakeshore","2026-03-04",355],
     ["Riverside","2026-03-01",610],["Riverside","2026-03-02",590],["Riverside","2026-03-03",640],["Riverside","2026-03-04",700]],
    [
     ("Total sales per store: a summation over days, grouped by store.",
      "SELECT store, amount\nFROM daily_sales;",
      "SELECT store, SUM(amount) AS total_sales\nFROM daily_sales\nGROUP BY store\nORDER BY store;",
      3,
      "SUM(amount) with GROUP BY store gives Harbor 1930, Lakeshore 1355, Riverside 2540."),
     ("Grand total across all stores and days: the double summation.",
      "SELECT store, SUM(amount)\nFROM daily_sales\nGROUP BY store;",
      "SELECT SUM(amount) AS grand_total\nFROM daily_sales;",
      1,
      "Drop the GROUP BY to collapse everything to one row: 5825."),
     ("For each store, the sum of squared daily amounts: a building block of variance.",
      "SELECT store, SUM(amount)\nFROM daily_sales\nGROUP BY store;",
      "SELECT store, SUM(amount * amount) AS sum_of_squares\nFROM daily_sales\nGROUP BY store\nORDER BY store;",
      3,
      "Square inside the SUM: SUM(amount * amount).")
    ]))

# ---------- SQL playground: M30 Set Theory & Logic ----------
SP.append(sqlpg("sql-il26-m30-sets", "IL26-M30", "Set operations on customer segments",
    "customers",
    ["customer_id", "name", "segment", "signup_month", "lifetime_value"],
    [[1,"Ada","enterprise","2026-01",12000],[2,"Ben","smb","2026-01",3000],
     [3,"Cara","enterprise","2026-02",9500],[4,"Dan","smb","2026-02",4200],
     [5,"Eli","startup","2026-02",1500],[6,"Fay","enterprise","2026-03",15000],
     [7,"Gus","startup","2026-03",2200],[8,"Hal","smb","2026-03",3800],
     [9,"Ivy","enterprise","2026-04",8000],[10,"Jay","startup","2026-04",900],
     [11,"Kay","smb","2026-04",5100],[12,"Leo","enterprise","2026-04",11000]],
    [
     ("UNION: customers who are enterprise OR signed up in 2026-02, one row per customer.",
      "SELECT name FROM customers WHERE segment = 'enterprise';",
      "SELECT name FROM customers WHERE segment = 'enterprise'\nUNION\nSELECT name FROM customers WHERE signup_month = '2026-02'\nORDER BY name;",
      7,
      "UNION deduplicates: 5 enterprise + 3 February signups - 1 overlap (Cara) = 7."),
     ("INTERSECT: customers who are BOTH enterprise AND signed up in 2026-02.",
      "SELECT name FROM customers WHERE segment = 'enterprise';",
      "SELECT name FROM customers WHERE segment = 'enterprise'\nINTERSECT\nSELECT name FROM customers WHERE signup_month = '2026-02';",
      1,
      "Only Cara satisfies both conditions."),
     ("EXCEPT: enterprise customers who did NOT sign up in 2026-02.",
      "SELECT name FROM customers WHERE segment = 'enterprise';",
      "SELECT name FROM customers WHERE segment = 'enterprise'\nEXCEPT\nSELECT name FROM customers WHERE signup_month = '2026-02'\nORDER BY name;",
      4,
      "Removes Cara from the 5 enterprise customers: Ada, Fay, Ivy, Leo.")
    ]))

# ---------- SQL playground: M31 Descriptive Statistics ----------
SP.append(sqlpg("sql-il26-m31-describe", "IL26-M31", "Descriptive statistics with GROUP BY",
    "employee_comp",
    ["emp_id", "dept", "role", "salary", "years_exp"],
    [["E1","Engineering","backend",145000,6],["E2","Engineering","frontend",128000,4],
     ["E3","Engineering","ml",162000,9],["E4","Engineering","qa",118000,3],
     ["A1","Analytics","analyst",98000,5],["A2","Analytics","analyst",87000,3],["A3","Analytics","senior analyst",112000,7],
     ["S1","Sales","ae",76000,4],["S2","Sales","ae",82000,6],["S3","Sales","sdr",69000,2],
     ["P1","Support","tier2",58000,5],["P2","Support","tier2",62000,3],["P3","Support","tier1",55000,8],["P4","Support","tier1",60000,4]],
    [
     ("Average, minimum, and maximum salary per department.",
      "SELECT dept, salary FROM employee_comp;",
      "SELECT dept,\n  AVG(salary) AS avg_salary,\n  MIN(salary) AS min_salary,\n  MAX(salary) AS max_salary\nFROM employee_comp\nGROUP BY dept\nORDER BY dept;",
      4,
      "AVG, MIN, MAX with GROUP BY dept."),
     ("Departments with more than 3 employees, with headcount.",
      "SELECT dept, COUNT(*) FROM employee_comp GROUP BY dept;",
      "SELECT dept, COUNT(*) AS headcount\nFROM employee_comp\nGROUP BY dept\nHAVING COUNT(*) > 3\nORDER BY dept;",
      2,
      "HAVING filters after grouping: Engineering (4) and Support (4)."),
     ("The overall standard deviation of salary: one number describing spread.",
      "SELECT AVG(salary) FROM employee_comp;",
      "SELECT STDDEV(salary) AS salary_stddev\nFROM employee_comp;",
      1,
      "STDDEV (or STDDEV_POP) aggregates the whole table to one row.")
    ]))

# ---------- SQL playground: M34 Calculus Concepts ----------
SP.append(sqlpg("sql-il26-m34-calculus", "IL26-M34", "Discrete calculus: running totals and differences",
    "sensor_readings",
    ["reading_ts", "temp_c"],
    [["2026-05-01 08:00",21.0],["2026-05-01 09:00",21.8],["2026-05-01 10:00",23.1],
     ["2026-05-01 11:00",24.9],["2026-05-01 12:00",26.4],["2026-05-01 13:00",27.2],
     ["2026-05-01 14:00",27.0],["2026-05-01 15:00",26.1],["2026-05-01 16:00",24.8],
     ["2026-05-01 17:00",23.5],["2026-05-01 18:00",22.6],["2026-05-01 19:00",22.0]],
    [
     ("Running total of temperature: a discrete integral, via a windowed SUM ordered by time.",
      "SELECT reading_ts, temp_c FROM sensor_readings;",
      "SELECT reading_ts,\n  SUM(temp_c) OVER (ORDER BY reading_ts\n    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total\nFROM sensor_readings\nORDER BY reading_ts;",
      12,
      "SUM() OVER (ORDER BY reading_ts) accumulates; the explicit frame makes the intent clear."),
     ("Hour-over-hour temperature change: a discrete derivative, via LAG.",
      "SELECT reading_ts, temp_c FROM sensor_readings;",
      "SELECT reading_ts,\n  temp_c - LAG(temp_c) OVER (ORDER BY reading_ts) AS hourly_change\nFROM sensor_readings\nORDER BY reading_ts;",
      12,
      "Subtract the LAG value; the first row has no prior reading so its change is NULL."),
     ("Flag the hours where temperature rose more than 1.0 degree versus the prior hour.",
      "SELECT reading_ts, temp_c FROM sensor_readings;",
      "SELECT reading_ts, temp_c\nFROM (\n  SELECT reading_ts, temp_c,\n    temp_c - LAG(temp_c) OVER (ORDER BY reading_ts) AS chg\n  FROM sensor_readings\n) t\nWHERE chg > 1.0\nORDER BY reading_ts;",
      3,
      "Compute the change in a subquery, then filter: 10:00 (+1.3), 11:00 (+1.8), 12:00 (+1.5).")
    ]))

# ---------- SQL playground: M08 Advanced SQL ----------
SP.append(sqlpg("sql-il26-m08-windows", "IL26-M08", "Window functions, CTEs, and frames",
    "orders",
    ["order_id", "customer", "region", "order_date", "amount"],
    [[101,"Acme","West","2026-01-05",1200],[102,"Beta","West","2026-01-12",3400],
     [103,"Acme","West","2026-02-03",2100],[104,"Delta","East","2026-01-08",950],
     [105,"Echo","East","2026-02-14",5100],[106,"Foxtrot","East","2026-02-20",5100],
     [107,"Gamma","Central","2026-01-15",1800],[108,"Helios","Central","2026-02-02",2200],
     [109,"Acme","West","2026-03-01",1500],[110,"Beta","West","2026-03-10",2900],
     [111,"Delta","East","2026-03-05",1300],[112,"Echo","East","2026-03-18",4700],
     [113,"Foxtrot","East","2026-03-22",1200],[114,"Gamma","Central","2026-03-08",3100],
     [115,"Helios","Central","2026-03-15",1900],[116,"Iris","Central","2026-03-20",2600]],
    [
     ("Rank orders within each region by amount and return the top order per region.",
      "SELECT region, customer, amount FROM orders ORDER BY region, amount DESC;",
      "SELECT region, customer, amount\nFROM (\n  SELECT region, customer, amount,\n    RANK() OVER (PARTITION BY region ORDER BY amount DESC) AS rnk\n  FROM orders\n) t\nWHERE rnk = 1\nORDER BY region;",
      4,
      "RANK (not ROW_NUMBER) keeps ties: East has two orders at 5100, so 4 rows return."),
     ("Running total of amount per region, ordered by order date, with an explicit frame.",
      "SELECT region, order_date, amount FROM orders;",
      "SELECT region, order_date, amount,\n  SUM(amount) OVER (PARTITION BY region ORDER BY order_date\n    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total\nFROM orders\nORDER BY region, order_date;",
      16,
      "PARTITION BY region restarts the total per region; the frame clause states the window explicitly."),
     ("Month-over-month change per customer: aggregate to monthly totals in a CTE, then LAG.",
      "SELECT customer, amount FROM orders;",
      "WITH monthly AS (\n  SELECT customer, SUBSTRING(order_date, 1, 7) AS ym, SUM(amount) AS total\n  FROM orders\n  GROUP BY customer, SUBSTRING(order_date, 1, 7)\n),\nlagged AS (\n  SELECT customer, ym, total,\n    LAG(total) OVER (PARTITION BY customer ORDER BY ym) AS prev\n  FROM monthly\n)\nSELECT customer, ym, total, total - prev AS mom_change\nFROM lagged\nWHERE prev IS NOT NULL\nORDER BY customer, ym;",
      8,
      "The CTE collapses to customer-months; LAG gives the prior month; 8 customer-months have a predecessor."),
     ("Customers whose lifetime total exceeds their region's average customer total (two CTEs).",
      "SELECT customer, region, SUM(amount) FROM orders GROUP BY customer, region;",
      "WITH cust_tot AS (\n  SELECT customer, region, SUM(amount) AS total\n  FROM orders GROUP BY customer, region\n),\nregion_avg AS (\n  SELECT region, AVG(total) AS avg_total\n  FROM cust_tot GROUP BY region\n)\nSELECT c.customer, c.region, c.total\nFROM cust_tot c JOIN region_avg r ON c.region = r.region\nWHERE c.total > r.avg_total\nORDER BY c.customer;",
      5,
      "Beta (West), Echo and Foxtrot (East), Gamma and Helios (Central) clear their regional averages.")
    ]))

# ---------- SQL playground: M10 Statistics & Probability ----------
SP.append(sqlpg("sql-il26-m10-channels", "IL26-M10", "Channel performance: rates and variability in SQL",
    "site_sessions",
    ["session_id", "channel", "converted", "revenue"],
    [["s1","organic",1,45],["s2","organic",0,0],["s3","organic",1,60],["s4","organic",0,0],["s5","organic",1,30],
     ["s6","paid",1,80],["s7","paid",1,55],["s8","paid",0,0],["s9","paid",1,70],["s10","paid",0,0],
     ["s11","referral",1,40],["s12","referral",0,0],["s13","referral",0,0],["s14","referral",1,90]],
    [
     ("Conversion rate and average revenue per channel.",
      "SELECT channel, converted, revenue FROM site_sessions;",
      "SELECT channel,\n  SUM(converted) * 1.0 / COUNT(*) AS conv_rate,\n  AVG(revenue) AS avg_revenue\nFROM site_sessions\nGROUP BY channel\nORDER BY channel;",
      3,
      "A rate is a mean of 0/1 flags: SUM(converted)*1.0/COUNT(*)."),
     ("Revenue variability per channel: standard deviation and maximum.",
      "SELECT channel, AVG(revenue) FROM site_sessions GROUP BY channel;",
      "SELECT channel,\n  STDDEV(revenue) AS revenue_stddev,\n  MAX(revenue) AS max_revenue\nFROM site_sessions\nGROUP BY channel\nORDER BY channel;",
      3,
      "STDDEV next to the mean tells you whether the average is stable or noisy."),
     ("Channels with at least 5 sessions and a conversion rate above 0.5.",
      "SELECT channel, COUNT(*) FROM site_sessions GROUP BY channel;",
      "SELECT channel, SUM(converted) * 1.0 / COUNT(*) AS conv_rate\nFROM site_sessions\nGROUP BY channel\nHAVING COUNT(*) >= 5 AND SUM(converted) * 1.0 / COUNT(*) > 0.5\nORDER BY channel;",
      2,
      "HAVING filters groups: organic (3/5) and paid (3/5) qualify; referral has only 4 sessions.")
    ]))

# ---------- SQL playground: M11 Hypothesis & A/B Testing ----------
SP.append(sqlpg("sql-il26-m11-abtest", "IL26-M11", "A/B test readout in SQL",
    "ab_users",
    ["user_id", "variant", "converted", "minutes", "is_new"],
    [["u1","A",1,12,1],["u2","A",0,3,1],["u3","A",1,18,0],["u4","A",0,5,0],["u5","A",1,9,1],["u6","A",0,2,0],
     ["u7","B",1,15,1],["u8","B",1,22,0],["u9","B",0,4,1],["u10","B",1,11,0],["u11","B",1,19,1],["u12","B",0,6,0]],
    [
     ("Conversion rate and average minutes per variant, with each variant's lift versus the overall average rate.",
      "SELECT variant, AVG(minutes) FROM ab_users GROUP BY variant;",
      "WITH rates AS (\n  SELECT variant,\n    SUM(converted) * 1.0 / COUNT(*) AS conv_rate,\n    AVG(minutes) AS avg_minutes\n  FROM ab_users GROUP BY variant\n)\nSELECT variant, conv_rate, avg_minutes,\n  conv_rate - AVG(conv_rate) OVER () AS lift_vs_avg\nFROM rates\nORDER BY variant;",
      2,
      "AVG() OVER () with no partition computes the grand mean across the two variant rows."),
     ("Sample size per variant: are the arms balanced?",
      "SELECT variant, COUNT(*) FROM ab_users GROUP BY variant;",
      "SELECT variant, COUNT(*) AS n_users\nFROM ab_users\nGROUP BY variant\nORDER BY variant;",
      2,
      "6 and 6: balanced. Unbalanced arms are the first thing to check before trusting a readout."),
     ("Conversion rate by variant AND new-vs-returning segment: does the effect hold in both?",
      "SELECT variant, is_new, converted FROM ab_users;",
      "SELECT variant, is_new,\n  SUM(converted) * 1.0 / COUNT(*) AS conv_rate,\n  COUNT(*) AS n\nFROM ab_users\nGROUP BY variant, is_new\nORDER BY is_new, variant;",
      4,
      "New users: 0.667 both arms (no effect). Returning: 0.333 vs 0.667 (effect concentrated here).")
    ]))

# ---------- SQL playground: M12 Data Modeling ----------
SP.append(sqlpg("sql-il26-m12-grain", "IL26-M12", "Grain checks on a sales fact table",
    "sales_lines",
    ["line_id", "order_id", "product", "category", "qty", "unit_price", "customer_id"],
    [["l1","o1001","Widget A","Tools",2,25.00,"c1"],["l2","o1001","Widget B","Tools",1,40.00,"c1"],
     ["l3","o1002","Gadget X","Electronics",1,199.00,"c2"],["l4","o1003","Widget A","Tools",5,25.00,"c3"],
     ["l5","o1003","Widget A","Tools",5,25.00,"c3"],["l6","o1004","Gadget Y","Electronics",2,149.00,"c2"],
     ["l7","o1005","Cable Z","Accessories",10,9.99,"c4"],["l8","o1006","Widget B","Tools",3,40.00,"c5"],
     ["l9","o1007","Gadget X","Electronics",1,199.00,"c1"],["l10","o1008","Cable Z","Accessories",4,9.99,"c3"],
     ["l11","o1009","Widget A","Tools",1,25.00,"c6"],["l12","o1010","Gadget Y","Electronics",1,149.00,"c6"],
     ["l13","o1010","Gadget Y","Electronics",1,149.00,"c6"],["l14","o1011","Widget C","Tools",2,60.00,"c7"]],
    [
     ("Revenue by category: qty * unit_price summed at fact grain.",
      "SELECT category, qty, unit_price FROM sales_lines;",
      "SELECT category, SUM(qty * unit_price) AS revenue\nFROM sales_lines\nGROUP BY category\nORDER BY revenue DESC;",
      3,
      "Multiply inside the SUM: Electronics 994, Tools 600, Accessories 139.86."),
     ("Grain violations: order_id + product pairs appearing more than once.",
      "SELECT order_id, product FROM sales_lines;",
      "SELECT order_id, product, COUNT(*) AS line_count\nFROM sales_lines\nGROUP BY order_id, product\nHAVING COUNT(*) > 1\nORDER BY order_id;",
      2,
      "o1003/Widget A and o1010/Gadget Y are double-counted: the fact grain is broken there."),
     ("Dimension sanity: distinct customers and distinct orders in one row.",
      "SELECT COUNT(*) FROM sales_lines;",
      "SELECT COUNT(DISTINCT customer_id) AS n_customers,\n  COUNT(DISTINCT order_id) AS n_orders\nFROM sales_lines;",
      1,
      "7 customers, 11 orders: COUNT(DISTINCT ...) measures dimension cardinality.")
    ]))

# ---------- SQL playground: M13 ETL ----------
SP.append(sqlpg("sql-il26-m13-etl", "IL26-M13", "Staging cleanup: dedupe, clean, incremental filter",
    "stg_events",
    ["event_id", "user_id", "event_ts", "event_type", "amount"],
    [["e1","u1","2026-09-01 10:00","purchase",45.00],["e2","u2","2026-09-01 10:05","view",None],
     ["e3","u1","2026-09-01 10:00","purchase",45.00],["e4","u3","2026-09-02 11:00","purchase",120.00],
     ["e5","u2","2026-09-02 11:30","purchase",None],["e6","u4","2026-09-03 09:00","view",None],
     ["e7","u1","2026-09-03 09:15","purchase",60.00],["e8","u3","2026-09-03 09:15","purchase",60.00],
     ["e9","u5","2026-08-28 08:00","purchase",30.00],["e10","u2","2026-09-01 10:05","view",None],
     ["e11","u6","2026-09-04 12:00","purchase",200.00],["e12","u1","2026-09-04 12:05","refund",-45.00],
     ["e13","u7","2026-09-04 12:10","view",None],["e14","u4","2026-09-05 14:00","purchase",88.00]],
    [
     ("Deduplicate: one row per (user_id, event_ts, event_type), keeping the lowest event_id.",
      "SELECT * FROM stg_events;",
      "SELECT event_id, user_id, event_ts, event_type, amount\nFROM (\n  SELECT *,\n    ROW_NUMBER() OVER (PARTITION BY user_id, event_ts, event_type ORDER BY event_id) AS rn\n  FROM stg_events\n) t\nWHERE rn = 1\nORDER BY event_ts;",
      12,
      "Two duplicate pairs (e1/e3, e2/e10) collapse: 14 rows become 12."),
     ("Clean amounts: purchase events only, with NULL amounts replaced by 0.",
      "SELECT * FROM stg_events WHERE event_type = 'purchase';",
      "SELECT event_id, COALESCE(amount, 0) AS clean_amount\nFROM stg_events\nWHERE event_type = 'purchase'\nORDER BY event_id;",
      9,
      "COALESCE(amount, 0) handles the NULL on e5; views and the refund are excluded."),
     ("Incremental load: only events newer than the watermark 2026-09-02.",
      "SELECT * FROM stg_events;",
      "SELECT event_id, event_ts\nFROM stg_events\nWHERE event_ts > '2026-09-02'\nORDER BY event_ts;",
      9,
      "The watermark excludes everything through 2026-09-02: 9 rows remain.")
    ]))

# ---------- SQL playground: M03 Tableau data prep ----------
SP.append(sqlpg("sql-il26-m03-extract", "IL26-M03", "Preparing an analysis-ready extract",
    "retail_txns",
    ["txn_id", "store", "category", "amount", "txn_date"],
    [["t1","Harbor","Outdoor",120,"2025-01-03"],["t2","Harbor","Outdoor",200,"2025-02-10"],
     ["t3","Harbor","Fitness",85,"2025-03-01"],["t4","Lakeshore","Outdoor",150,"2025-01-15"],
     ["t5","Lakeshore","Fitness",95,"2026-01-20"],["t6","Lakeshore","Fitness",110,"2026-02-11"],
     ["t7","Riverside","Outdoor",180,"2025-03-04"],["t8","Riverside","Outdoor",220,"2026-01-05"],
     ["t9","Riverside","Fitness",130,"2026-02-20"],["t10","Harbor","Outdoor",175,"2026-03-02"],
     ["t11","Harbor","Fitness",140,"2026-03-15"],["t12","Lakeshore","Outdoor",160,"2026-01-10"],
     ["t13","Riverside","Outdoor",190,"2025-02-20"],["t14","Riverside","Fitness",105,"2025-03-25"]],
    [
     ("Monthly category totals: the year-month grain a Tableau extract would carry.",
      "SELECT txn_date, category, amount FROM retail_txns;",
      "SELECT SUBSTRING(txn_date, 1, 7) AS ym, category,\n  SUM(amount) AS total\nFROM retail_txns\nGROUP BY SUBSTRING(txn_date, 1, 7), category\nORDER BY ym, category;",
      9,
      "Year-month plus category gives 9 groups across the six months."),
     ("Best month per category by total (RANK over the monthly totals).",
      "SELECT category, SUM(amount) FROM retail_txns GROUP BY category;",
      "WITH m AS (\n  SELECT SUBSTRING(txn_date, 1, 7) AS ym, category, SUM(amount) AS total\n  FROM retail_txns\n  GROUP BY SUBSTRING(txn_date, 1, 7), category\n)\nSELECT ym, category, total\nFROM (SELECT *, RANK() OVER (PARTITION BY category ORDER BY total DESC) AS rnk FROM m) t\nWHERE rnk = 1;",
      2,
      "One row per category: Outdoor peaks 2026-01 (380), Fitness peaks 2026-03 (140)... verify against the CTE."),
     ("Rolling 3-month total per category with an explicit window frame.",
      "SELECT category, txn_date, amount FROM retail_txns;",
      "WITH m AS (\n  SELECT SUBSTRING(txn_date, 1, 7) AS ym, category, SUM(amount) AS total\n  FROM retail_txns\n  GROUP BY SUBSTRING(txn_date, 1, 7), category\n)\nSELECT ym, category,\n  SUM(total) OVER (PARTITION BY category ORDER BY ym\n    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS rolling_3mo\nFROM m\nORDER BY category, ym;",
      9,
      "ROWS BETWEEN 2 PRECEDING AND CURRENT ROW builds the trailing window; early months sum fewer rows.")
    ]))

# ---------- SQL playground: M04 Data+ quality ----------
SP.append(sqlpg("sql-il26-m04-quality", "IL26-M04", "Data-quality profiling in SQL",
    "crm_contacts",
    ["contact_id", "email", "phone", "created_at", "source"],
    [["c1","ana@northwind.com","555-0101","2026-01-02","web"],["c2","ben@beacon.io","555-0102","2026-01-05","web"],
     ["c3","ana@northwind.com","555-0101","2026-02-01","import"],["c4","cara AT beacon.io",None,"2026-02-03","web"],
     ["c5",None,"555-0105","2026-02-10","event"],["c6","dan@copperline.com","555-0106","2026-03-01","web"],
     ["c7","eli@northwind.com","bad-number","2026-03-05","import"],["c8","fay@beacon.io","555-0108","2026-03-10","web"],
     ["c9","gus@copperline","555-0109","2026-03-12","event"],["c10","hal@northwind.com",None,"2026-04-01","web"],
     ["c11","ivy@beacon.io","555-0111","2026-04-05","import"],["c12","ben@beacon.io","555-0102","2026-04-09","web"]],
    [
     ("NULL counts for email and phone in a single row.",
      "SELECT * FROM crm_contacts;",
      "SELECT\n  SUM(CASE WHEN email IS NULL THEN 1 ELSE 0 END) AS email_nulls,\n  SUM(CASE WHEN phone IS NULL THEN 1 ELSE 0 END) AS phone_nulls\nFROM crm_contacts;",
      1,
      "SUM over a CASE expression counts NULLs: 1 email, 2 phones."),
     ("Duplicate emails: values appearing more than once, with counts.",
      "SELECT email FROM crm_contacts;",
      "SELECT email, COUNT(*) AS n\nFROM crm_contacts\nWHERE email IS NOT NULL\nGROUP BY email\nHAVING COUNT(*) > 1\nORDER BY email;",
      2,
      "ana@northwind.com and ben@beacon.io each appear twice."),
     ("Invalid emails: values not matching a basic '%@%.%' pattern.",
      "SELECT contact_id, email FROM crm_contacts;",
      "SELECT contact_id, email\nFROM crm_contacts\nWHERE email IS NOT NULL AND email NOT LIKE '%@%.%'\nORDER BY contact_id;",
      2,
      "'cara AT beacon.io' and 'gus@copperline' fail the pattern; NULLs are excluded first.")
    ]))

# ---------- SQL playground: M06 AWS/Athena ----------
SP.append(sqlpg("sql-il26-m06-athena", "IL26-M06", "Log analytics the Athena way",
    "web_logs",
    ["client_ip", "ts", "path", "status", "bytes"],
    [["192.0.2.10","2026-06-01 08:01","/home",200,5120],["192.0.2.11","2026-06-01 08:02","/pricing",200,3140],
     ["192.0.2.10","2026-06-01 08:05","/api/data",500,210],["192.0.2.12","2026-06-01 08:09","/home",200,4980],
     ["192.0.2.13","2026-06-01 09:01","/api/data",503,190],["192.0.2.11","2026-06-01 09:03","/docs",200,8210],
     ["192.0.2.14","2026-06-01 09:07","/api/data",200,4410],["192.0.2.10","2026-06-01 09:12","/pricing",200,3090],
     ["192.0.2.15","2026-06-01 10:00","/api/data",500,205],["192.0.2.12","2026-06-01 10:04","/home",200,5210],
     ["192.0.2.16","2026-06-01 10:09","/docs",404,320],["192.0.2.13","2026-06-01 10:15","/api/data",200,4600],
     ["192.0.2.17","2026-06-02 08:30","/home",200,5050],["192.0.2.18","2026-06-02 08:45","/api/data",200,4320]],
    [
     ("5xx error rate per hour: errors divided by total requests, grouped by hour.",
      "SELECT ts, status FROM web_logs;",
      "SELECT SUBSTRING(ts, 1, 13) AS hr,\n  SUM(CASE WHEN status >= 500 THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS err_rate\nFROM web_logs\nGROUP BY SUBSTRING(ts, 1, 13)\nORDER BY hr;",
      4,
      "Four distinct hours; the first three each have one 5xx in four requests (0.25)."),
     ("Top 3 paths by total bytes served.",
      "SELECT path, bytes FROM web_logs;",
      "SELECT path, SUM(bytes) AS total_bytes\nFROM web_logs\nGROUP BY path\nORDER BY total_bytes DESC\nLIMIT 3;",
      3,
      "/home (20360), /api/data (13935), /docs (8530)."),
     ("Distinct client IPs per day: a proxy for daily active users.",
      "SELECT client_ip, ts FROM web_logs;",
      "SELECT SUBSTRING(ts, 1, 10) AS day,\n  COUNT(DISTINCT client_ip) AS distinct_ips\nFROM web_logs\nGROUP BY SUBSTRING(ts, 1, 10)\nORDER BY day;",
      2,
      "7 distinct IPs on 2026-06-01, 2 on 2026-06-02.")
    ]))

# ---------- SQL playground: M07 Databricks ----------
SP.append(sqlpg("sql-il26-m07-delta", "IL26-M07", "Versioned tables: current state and change history",
    "delta_orders",
    ["order_id", "customer", "amount", "updated_at", "version"],
    [["o1","Acme",1000,"2026-01-01",1],["o1","Acme",1100,"2026-02-01",2],
     ["o2","Beta",2500,"2026-01-15",1],["o3","Delta",800,"2026-01-20",1],
     ["o3","Delta",850,"2026-03-01",2],["o3","Delta",900,"2026-04-01",3],
     ["o4","Echo",3200,"2026-02-10",1],["o5","Foxtrot",1500,"2026-02-15",1],
     ["o5","Foxtrot",1500,"2026-03-15",2],["o6","Gamma",4100,"2026-03-01",1],
     ["o7","Helios",950,"2026-03-20",1],["o8","Iris",2200,"2026-04-05",1]],
    [
     ("Current state: the latest version of each order (what a MERGE target holds).",
      "SELECT * FROM delta_orders;",
      "SELECT order_id, customer, amount, updated_at\nFROM (\n  SELECT *,\n    ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY version DESC) AS rn\n  FROM delta_orders\n) t\nWHERE rn = 1\nORDER BY order_id;",
      8,
      "One row per order_id: o1 through o8."),
     ("Orders with more than one version: the change-history audit.",
      "SELECT order_id, version FROM delta_orders;",
      "SELECT order_id, COUNT(*) AS versions, MAX(version) AS latest_version\nFROM delta_orders\nGROUP BY order_id\nHAVING COUNT(*) > 1\nORDER BY order_id;",
      3,
      "o1 (2 versions), o3 (3), o5 (2)."),
     ("Orders whose latest amount differs from their first version: real changes, not no-op rewrites.",
      "SELECT order_id, amount, version FROM delta_orders;",
      "WITH v AS (\n  SELECT order_id,\n    MIN(CASE WHEN version = 1 THEN amount END) AS first_amt,\n    MAX(CASE WHEN version = (SELECT MAX(version) FROM delta_orders d2 WHERE d2.order_id = delta_orders.order_id) THEN amount END) AS last_amt\n  FROM delta_orders GROUP BY order_id\n)\nSELECT order_id FROM v WHERE first_amt <> last_amt ORDER BY order_id;",
      2,
      "o1 (1000 to 1100) and o3 (800 to 900); o5 rewrote the same 1500.")
    ]))

# ---------- SQL playground: M24 applications tracker ----------
SP.append(sqlpg("sql-il26-m24-tracker", "IL26-M24", "Job-search analytics on your applications tracker",
    "applications",
    ["company", "role", "applied_date", "stage", "source"],
    [["Harbor Health","Data Analyst","2026-09-01","applied","LinkedIn"],
     ["Lakeshore Bank","Data Analyst","2026-09-03","screening","LinkedIn"],
     ["Riverside Logistics","BI Analyst","2026-09-05","rejected","Indeed"],
     ["Beacon Insurance","Data Analyst","2026-08-10","applied","referral"],
     ["Copperline Retail","Analytics Engineer","2026-09-08","interview","LinkedIn"],
     ["Northwind Labs","Data Analyst","2026-09-10","offer","referral"],
     ["Summit Health","BI Analyst","2026-08-15","rejected","Indeed"],
     ["Prairie Credit Union","Data Analyst","2026-09-12","applied","company site"],
     ["Bluefin Media","Data Analyst","2026-08-20","ghosted","LinkedIn"],
     ["Granite Energy","FP&A Analyst","2026-09-14","screening","Indeed"],
     ["Ferrous Metals","Data Analyst","2026-08-05","rejected","LinkedIn"],
     ["Alloy Systems","Data Analyst","2026-09-15","applied","referral"],
     ["Cobalt Foods","BI Analyst","2026-09-16","interview","company site"],
     ["Ironwood Clinic","Data Analyst","2026-09-18","applied","LinkedIn"]],
    [
     ("Funnel counts by stage: where every application stands.",
      "SELECT stage FROM applications;",
      "SELECT stage, COUNT(*) AS n\nFROM applications\nGROUP BY stage\nORDER BY n DESC;",
      6,
      "Six stages: applied 5, rejected 3, screening 2, interview 2, offer 1, ghosted 1."),
     ("Response rate by source: share of applications reaching screening or beyond.",
      "SELECT source, stage FROM applications;",
      "SELECT source,\n  SUM(CASE WHEN stage IN ('screening','interview','offer') THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS response_rate\nFROM applications\nGROUP BY source\nORDER BY response_rate DESC;",
      4,
      "company site 0.50, Indeed 0.333, referral 0.333, LinkedIn 0.286."),
     ("Stale applications: still 'applied' more than 21 days after applying (today 2026-10-07).",
      "SELECT company, applied_date, stage FROM applications;",
      "SELECT company, applied_date\nFROM applications\nWHERE stage = 'applied'\n  AND applied_date < DATE '2026-10-07' - INTERVAL '21 days'\nORDER BY applied_date;",
      4,
      "Harbor Health, Beacon Insurance, Prairie Credit Union, Alloy Systems; Ironwood is only 19 days old.")
    ]))

# ---------- SQL playground: M35 Palantir SQL bar ----------
SP.append(sqlpg("sql-il26-m35-interview", "IL26-M35", "Interview-pressure SQL: CTE chains, frames, ties",
    "bank_txns",
    ["txn_id", "account", "txn_date", "amount", "txn_type"],
    [["x1","a100","2026-01-02",500,"deposit"],["x2","a100","2026-01-03",-120,"withdrawal"],
     ["x3","a100","2026-01-04",-80,"withdrawal"],["x4","a100","2026-01-05",300,"deposit"],
     ["x5","a100","2026-01-06",-200,"withdrawal"],["x6","a100","2026-01-07",-200,"withdrawal"],
     ["x7","a200","2026-01-02",1000,"deposit"],["x8","a200","2026-01-03",1000,"deposit"],
     ["x9","a200","2026-01-04",-1500,"withdrawal"],["x10","a200","2026-01-05",400,"deposit"],
     ["x11","a300","2026-01-02",250,"deposit"],["x12","a300","2026-01-03",250,"deposit"],
     ["x13","a300","2026-01-04",250,"deposit"],["x14","a300","2026-01-05",-700,"withdrawal"]],
    [
     ("Three-CTE chain: daily net per account, then account totals, then the top 2 accounts by net flow.",
      "SELECT account, SUM(amount) FROM bank_txns GROUP BY account;",
      "WITH daily AS (\n  SELECT account, txn_date, SUM(amount) AS net\n  FROM bank_txns GROUP BY account, txn_date\n),\nacct AS (\n  SELECT account, SUM(net) AS total_net FROM daily GROUP BY account\n),\nranked AS (\n  SELECT account, total_net,\n    RANK() OVER (ORDER BY total_net DESC) AS rnk\n  FROM acct\n)\nSELECT account, total_net FROM ranked WHERE rnk <= 2 ORDER BY rnk;",
      2,
      "Nets: a200 = 900, a100 = 200, a300 = 50. Top 2: a200, a100."),
     ("3-day moving average of daily net flow per account, with an explicit ROWS frame.",
      "SELECT account, txn_date, SUM(amount) FROM bank_txns GROUP BY account, txn_date;",
      "WITH daily AS (\n  SELECT account, txn_date, SUM(amount) AS net\n  FROM bank_txns GROUP BY account, txn_date\n)\nSELECT account, txn_date,\n  AVG(net) OVER (PARTITION BY account ORDER BY txn_date\n    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS ma_3d\nFROM daily\nORDER BY account, txn_date;",
      14,
      "Daily grain: a100 has 6 days, a200 has 4, a300 has 4: 14 rows."),
     ("Top 2 withdrawal amounts per account, keeping ties: DENSE_RANK, not ROW_NUMBER.",
      "SELECT account, amount FROM bank_txns WHERE txn_type = 'withdrawal';",
      "SELECT account, amount\nFROM (\n  SELECT account, amount,\n    DENSE_RANK() OVER (PARTITION BY account ORDER BY ABS(amount) DESC) AS dr\n  FROM bank_txns WHERE txn_type = 'withdrawal'\n) t\nWHERE dr <= 2\nORDER BY account, ABS(amount) DESC;",
      5,
      "a100 keeps both -200 rows (tie for rank 1) plus -120; a200 and a300 contribute one row each."),
     ("For each account, the day with the largest net outflow; ties broken by earliest date.",
      "SELECT account, txn_date, SUM(amount) FROM bank_txns GROUP BY account, txn_date;",
      "WITH daily AS (\n  SELECT account, txn_date, SUM(amount) AS net\n  FROM bank_txns GROUP BY account, txn_date\n)\nSELECT account, txn_date, net\nFROM (\n  SELECT *, ROW_NUMBER() OVER (PARTITION BY account ORDER BY net ASC, txn_date ASC) AS rn\n  FROM daily\n) t\nWHERE rn = 1\nORDER BY account;",
      3,
      "a100: 2026-01-06 (-200, earliest of the tie), a200: 2026-01-04 (-1500), a300: 2026-01-05 (-700).")
    ]))

# ---------- SQL playground: M37 Ontology & pipeline thinking ----------
SP.append(sqlpg("sql-il26-m37-ontology", "IL26-M37", "Objects, links, and properties in SQL",
    "shipments",
    ["shipment_id", "origin", "destination", "carrier", "weight_kg", "ship_date", "delivery_date", "promised_date"],
    [["s1","Chicago Hub","Detroit Depot","Meridian Freight",1200,"2026-02-01","2026-02-03","2026-02-03"],
     ["s2","Chicago Hub","Detroit Depot","Meridian Freight",800,"2026-02-02","2026-02-05","2026-02-04"],
     ["s3","Chicago Hub","Columbus Cross","BlueArrow",1500,"2026-02-01","2026-02-02","2026-02-03"],
     ["s4","Detroit Depot","Chicago Hub","Meridian Freight",600,"2026-02-03","2026-02-04","2026-02-05"],
     ["s5","Columbus Cross","Detroit Depot","BlueArrow",2000,"2026-02-04","2026-02-07","2026-02-06"],
     ["s6","Chicago Hub","Detroit Depot","BlueArrow",950,"2026-02-05","2026-02-06","2026-02-07"],
     ["s7","Detroit Depot","Columbus Cross","Meridian Freight",1100,"2026-02-06","2026-02-08","2026-02-08"],
     ["s8","Columbus Cross","Chicago Hub","BlueArrow",750,"2026-02-07","2026-02-10","2026-02-09"],
     ["s9","Chicago Hub","Columbus Cross","Meridian Freight",1300,"2026-02-08","2026-02-09","2026-02-10"],
     ["s10","Detroit Depot","Chicago Hub","BlueArrow",500,"2026-02-09","2026-02-11","2026-02-11"],
     ["s11","Chicago Hub","Detroit Depot","Meridian Freight",700,"2026-02-10","2026-02-12","2026-02-12"],
     ["s12","Columbus Cross","Detroit Depot","Meridian Freight",1800,"2026-02-11","2026-02-13","2026-02-14"]],
    [
     ("Build the link table: origin to destination pairs with shipment counts and total weight.",
      "SELECT origin, destination FROM shipments;",
      "SELECT origin, destination,\n  COUNT(*) AS shipments,\n  SUM(weight_kg) AS total_kg\nFROM shipments\nGROUP BY origin, destination\nORDER BY shipments DESC;",
      6,
      "Six distinct lanes; Chicago Hub to Detroit Depot is the busiest with 4 shipments."),
     ("Late-delivery rate per carrier: delivered after the promised date.",
      "SELECT carrier, delivery_date, promised_date FROM shipments;",
      "SELECT carrier,\n  SUM(CASE WHEN delivery_date > promised_date THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS late_rate,\n  COUNT(*) AS n\nFROM shipments\nGROUP BY carrier\nORDER BY carrier;",
      2,
      "Meridian 1/7 late, BlueArrow 2/5 late."),
     ("Shipments whose origin handles at least 4 shipments: the hub-and-spoke core.",
      "SELECT origin, COUNT(*) FROM shipments GROUP BY origin;",
      "SELECT shipment_id, origin, destination\nFROM shipments\nWHERE origin IN (\n  SELECT origin FROM shipments GROUP BY origin HAVING COUNT(*) >= 4\n)\nORDER BY shipment_id;",
      6,
      "Only Chicago Hub clears the bar, with 6 shipments.")
    ]))

# ---------- SQL playground: M38 BNY reconciliation ----------
SP.append(sqlpg("sql-il26-m38-recon", "IL26-M38", "Reconciliation: trial balance and breaks",
    "ledger_entries",
    ["entry_id", "account", "side", "amount", "source_system", "value_date"],
    [["r1","1001","debit",5000,"core","2026-09-01"],["r2","1001","credit",5000,"core","2026-09-01"],
     ["r3","1001","debit",5000,"custody","2026-09-01"],["r4","1001","credit",5000,"custody","2026-09-01"],
     ["r5","1002","debit",12000,"core","2026-09-02"],["r6","1002","credit",12000,"core","2026-09-02"],
     ["r7","1002","debit",12000,"custody","2026-09-02"],
     ["r8","1003","debit",7500,"core","2026-09-03"],["r9","1003","credit",7500,"custody","2026-09-03"],
     ["r10","1004","debit",3000,"core","2026-08-20"],["r11","1004","credit",3000,"custody","2026-08-20"],
     ["r12","1005","debit",9000,"core","2026-09-04"],["r13","1005","credit",9000,"core","2026-09-04"],
     ["r14","1005","debit",9000,"custody","2026-09-04"]],
    [
     ("Trial balance per account: total debits, total credits, and the difference.",
      "SELECT account, side, SUM(amount) FROM ledger_entries GROUP BY account, side;",
      "SELECT account,\n  SUM(CASE WHEN side = 'debit' THEN amount ELSE 0 END) AS debits,\n  SUM(CASE WHEN side = 'credit' THEN amount ELSE 0 END) AS credits,\n  SUM(CASE WHEN side = 'debit' THEN amount ELSE -amount END) AS difference\nFROM ledger_entries\nGROUP BY account\nORDER BY account;",
      5,
      "Five accounts; 1002 and 1005 show nonzero differences that need investigation."),
     ("Breaks: (account, side, amount, value_date) tuples in core but missing from custody.",
      "SELECT * FROM ledger_entries WHERE source_system = 'core';",
      "SELECT account, side, amount, value_date\nFROM ledger_entries WHERE source_system = 'core'\nEXCEPT\nSELECT account, side, amount, value_date\nFROM ledger_entries WHERE source_system = 'custody'\nORDER BY account;",
      4,
      "Four one-sided breaks: 1002 credit 12000, 1003 debit 7500, 1004 debit 3000, 1005 credit 9000."),
     ("Aging: breaks (either direction) older than 2 days as of 2026-09-05.",
      "SELECT * FROM ledger_entries;",
      "WITH breaks AS (\n  SELECT account, side, amount, value_date FROM ledger_entries WHERE source_system = 'core'\n  EXCEPT\n  SELECT account, side, amount, value_date FROM ledger_entries WHERE source_system = 'custody'\n  UNION\n  SELECT account, side, amount, value_date FROM ledger_entries WHERE source_system = 'custody'\n  EXCEPT\n  SELECT account, side, amount, value_date FROM ledger_entries WHERE source_system = 'core'\n)\nSELECT * FROM breaks\nWHERE value_date < DATE '2026-09-05' - INTERVAL '2 days'\nORDER BY value_date;",
      2,
      "Only the 2026-08-20 pair for account 1004 is older than 2 days: both its sides."),
     ("Net break exposure per account: unmatched debits positive, unmatched credits negative; show nonzero.",
      "SELECT account, side, amount FROM ledger_entries;",
      "WITH breaks AS (\n  SELECT account, side, amount FROM ledger_entries WHERE source_system = 'core'\n  EXCEPT\n  SELECT account, side, amount FROM ledger_entries WHERE source_system = 'custody'\n  UNION\n  SELECT account, side, amount FROM ledger_entries WHERE source_system = 'custody'\n  EXCEPT\n  SELECT account, side, amount FROM ledger_entries WHERE source_system = 'core'\n)\nSELECT account,\n  SUM(CASE WHEN side = 'debit' THEN amount ELSE -amount END) AS net_exposure\nFROM breaks\nGROUP BY account\nHAVING SUM(CASE WHEN side = 'debit' THEN amount ELSE -amount END) <> 0\nORDER BY account;",
      2,
      "1002 nets to -12000 and 1005 to -9000; 1003 and 1004 offset to zero.")
    ]))

# ---------- SQL playground: M39 controls ----------
SP.append(sqlpg("sql-il26-m39-controls", "IL26-M39", "Control checks on report runs",
    "report_runs",
    ["run_id", "report_name", "run_ts", "row_count", "checksum", "approved_by"],
    [["k1","CCAR Summary","2026-09-01 06:00",1200,"a1b2","maria.s"],
     ["k2","CCAR Summary","2026-09-02 06:00",1200,"a1b2","maria.s"],
     ["k3","CCAR Summary","2026-09-03 06:00",1250,"c3d4",None],
     ["k4","Liquidity Snapshot","2026-09-01 07:00",340,"e5f6","james.l"],
     ["k5","Liquidity Snapshot","2026-09-02 07:00",340,"e5f6","james.l"],
     ["k6","Liquidity Snapshot","2026-09-03 07:00",340,"e5f6","james.l"],
     ["k7","Risk Positions","2026-09-01 08:00",8900,"9a8b","maria.s"],
     ["k8","Risk Positions","2026-09-02 08:00",8900,"9a8b",None],
     ["k9","Risk Positions","2026-09-03 08:00",9100,"7c6d","maria.s"],
     ["k10","CCAR Summary","2026-09-04 06:00",1200,"a1b2","maria.s"],
     ["k11","Liquidity Snapshot","2026-09-04 07:00",340,"e5f6","james.l"],
     ["k12","Fee Schedule","2026-09-04 09:00",75,"1a2b",None]],
    [
     ("Completeness: the 3 daily reports across 4 days; find missing report-days.",
      "SELECT DISTINCT report_name FROM report_runs;",
      "WITH days AS (\n  SELECT DISTINCT SUBSTRING(run_ts, 1, 10) AS day FROM report_runs\n),\nreps AS (\n  SELECT DISTINCT report_name FROM report_runs\n  WHERE report_name IN ('CCAR Summary','Liquidity Snapshot','Risk Positions')\n),\nexpected AS (\n  SELECT day, report_name FROM days CROSS JOIN reps\n)\nSELECT e.day, e.report_name\nFROM expected e\nLEFT JOIN report_runs r\n  ON SUBSTRING(r.run_ts, 1, 10) = e.day AND r.report_name = e.report_name\nWHERE r.run_id IS NULL;",
      1,
      "Risk Positions never ran on 2026-09-04: the one gap in 12 expected report-days."),
     ("Checksum changes: runs whose checksum differs from that report's prior run.",
      "SELECT report_name, run_ts, checksum FROM report_runs ORDER BY report_name, run_ts;",
      "SELECT report_name, run_ts, checksum\nFROM (\n  SELECT report_name, run_ts, checksum,\n    LAG(checksum) OVER (PARTITION BY report_name ORDER BY run_ts) AS prev_checksum\n  FROM report_runs\n) t\nWHERE prev_checksum IS NOT NULL AND checksum <> prev_checksum\nORDER BY run_ts;",
      3,
      "CCAR Summary on 09-03 and 09-04, and Risk Positions on 09-03: results moved between runs."),
     ("Four-eyes violations: runs with no approver recorded.",
      "SELECT run_id, report_name, approved_by FROM report_runs;",
      "SELECT run_id, report_name, run_ts\nFROM report_runs\nWHERE approved_by IS NULL\nORDER BY run_ts;",
      3,
      "k3, k8, and k12 ran without a second pair of eyes.")
    ]))

PE = data["pythonExercises"]

# ---------- Python: M26 arithmetic ----------
PE.append(pyex("py-il26-m26-arithmetic", "IL26-M26", "Arithmetic fluency in Python",
    [
     ("Evaluate (17 * 3 + 8) / 5 - 2 ** 2 and store it in `result`.",
      "result = None",
      "result = (17 * 3 + 8) / 5 - 2 ** 2",
      [("result equals 7.8", "abs(result - 7.8) < 1e-9")]),
     ("Convert the fraction 7/8 to a decimal rounded to 3 places; store it in `result`.",
      "result = None",
      "result = round(7 / 8, 3)",
      [("result equals 0.875", "result == 0.875")]),
     ("Compute the mean of [4, 8, 15, 16, 23, 42] using only sum() and len(); store it in `result`.",
      "values = [4, 8, 15, 16, 23, 42]\nresult = None",
      "values = [4, 8, 15, 16, 23, 42]\nresult = sum(values) / len(values)",
      [("result equals 18.0", "result == 18.0")])
    ]))

# ---------- Python: M26 algebra ----------
PE.append(pyex("py-il26-m26-algebra", "IL26-M26", "Solving equations with Python",
    [
     ("Solve 3x + 7 = 22 for x; store x in `result`.",
      "result = None",
      "result = (22 - 7) / 3",
      [("result equals 5.0", "result == 5.0")]),
     ("Solve the system 2x + y = 10 and x - y = 2 with numpy; store the tuple (x, y) in `result`.",
      "import numpy as np\nresult = None",
      "import numpy as np\nA = np.array([[2, 1], [1, -1]])\nb = np.array([10, 2])\nx, y = np.linalg.solve(A, b)\nresult = (float(x), float(y))",
      [("x is 4 and y is 2", "abs(result[0] - 4) < 1e-9 and abs(result[1] - 2) < 1e-9")]),
     ("Find the roots of x^2 - 5x + 6 = 0 with numpy.roots; store the sorted list in `result`.",
      "import numpy as np\nresult = None",
      "import numpy as np\nresult = sorted(float(r) for r in np.roots([1, -5, 6]))",
      [("roots are [2.0, 3.0]", "len(result) == 2 and abs(result[0] - 2.0) < 1e-9 and abs(result[1] - 3.0) < 1e-9")])
    ]))

# ---------- Python: M27 functions ----------
PE.append(pyex("py-il26-m27-functions", "IL26-M27", "Functions: tabulate, compose, find roots",
    [
     ("Tabulate f(x) = x^2 - 3x + 2 for x in 0..5; store the list in `result`.",
      "result = None",
      "result = [x**2 - 3*x + 2 for x in range(6)]",
      [("result equals [2, 0, 0, 2, 6, 12]", "result == [2, 0, 0, 2, 6, 12]")]),
     ("With g(x) = 2x + 1 and f(x) = x^2, compute f(g(3)); store it in `result`.",
      "result = None",
      "g = lambda x: 2 * x + 1\nf = lambda x: x ** 2\nresult = f(g(3))",
      [("result equals 49", "result == 49")]),
     ("f(x) = x^3 - 2x - 5 changes sign between 2 and 3. Scan in 0.1 steps from 2.0; store the first x where f(x) > 0.",
      "result = None",
      "f = lambda x: x**3 - 2*x - 5\nx = 2.0\nwhile f(x) <= 0:\n    x = round(x + 0.1, 1)\nresult = x",
      [("result is approximately 2.1", "abs(result - 2.1) < 1e-9")])
    ]))

# ---------- Python: M28 exponents & logs ----------
PE.append(pyex("py-il26-m28-explog", "IL26-M28", "Exponential growth and logarithms",
    [
     ("A metric grows 8% per month. Compute the doubling time in months as ln(2)/ln(1.08); store it in `result`.",
      "import math\nresult = None",
      "import math\nresult = math.log(2) / math.log(1.08)",
      [("result is about 9.006 months", "abs(result - 9.006) < 0.01")]),
     ("Values [100, 121, 146.41] grow exponentially. Estimate the per-period growth rate from mean log differences; store it in `result`.",
      "import math\nvalues = [100, 121, 146.41]\nresult = None",
      "import math\nvalues = [100, 121, 146.41]\ndiffs = [math.log(values[i+1]) - math.log(values[i]) for i in range(len(values)-1)]\nresult = sum(diffs) / len(diffs)",
      [("rate is about 0.1906", "abs(result - 0.1906) < 0.001")]),
     ("Normalize [10, 100, 1000, 10000] with log10; store the list in `result`.",
      "import math\nresult = None",
      "import math\nresult = [math.log10(v) for v in [10, 100, 1000, 10000]]",
      [("result equals [1.0, 2.0, 3.0, 4.0]", "result == [1.0, 2.0, 3.0, 4.0]")])
    ]))

# ---------- Python: M29 summation ----------
PE.append(pyex("py-il26-m29-sums", "IL26-M29", "Summation notation as code",
    [
     ("Compute the sum from k=1 to 100 of k^2; store it in `result`.",
      "result = None",
      "result = sum(k**2 for k in range(1, 101))",
      [("result equals 338350", "result == 338350")]),
     ("Compute the double sum over i=1..3 and j=1..4 of i*j; store it in `result`.",
      "result = None",
      "result = sum(i * j for i in range(1, 4) for j in range(1, 5))",
      [("result equals 60", "result == 60")]),
     ("Weighted sum of values [80, 90, 70] with weights [0.5, 0.3, 0.2]; store it in `result`.",
      "result = None",
      "result = sum(w * v for w, v in zip([0.5, 0.3, 0.2], [80, 90, 70]))",
      [("result equals 81.0", "abs(result - 81.0) < 1e-9")])
    ]))

# ---------- Python: M30 logic ----------
PE.append(pyex("py-il26-m30-logic", "IL26-M30", "Boolean logic and set filters",
    [
     ("Over all 8 boolean combos of (A, B, C), count how many make A AND (B OR C) true; store the count in `result`.",
      "import itertools\nresult = None",
      "import itertools\nresult = sum(1 for a, b, c in itertools.product([False, True], repeat=3) if a and (b or c))",
      [("result equals 3", "result == 3")]),
     ("Verify De Morgan's law: NOT (A OR B) equals (NOT A) AND (NOT B) for all 4 combos; store True if every combo matches.",
      "import itertools\nresult = None",
      "import itertools\nresult = all((not (a or b)) == ((not a) and (not b)) for a, b in itertools.product([False, True], repeat=2))",
      [("result is True", "result is True")]),
     ("From the customer list, select names where tier is 'gold' AND spend exceeds 500; store the name list in `result`.",
      "customers = [{'name':'a','tier':'gold','spend':1200},{'name':'b','tier':'silver','spend':400},{'name':'c','tier':'gold','spend':300}]\nresult = None",
      "customers = [{'name':'a','tier':'gold','spend':1200},{'name':'b','tier':'silver','spend':400},{'name':'c','tier':'gold','spend':300}]\nresult = [c['name'] for c in customers if c['tier'] == 'gold' and c['spend'] > 500]",
      [("result equals ['a']", "result == ['a']")])
    ]))

# ---------- Python: M31 descriptive stats ----------
PE.append(pyex("py-il26-m31-numpy", "IL26-M31", "Descriptive statistics with numpy and pandas",
    [
     ("With numpy, compute mean, median, and population std of [12, 15, 18, 22, 30]; store the tuple in `result`.",
      "import numpy as np\nvalues = [12, 15, 18, 22, 30]\nresult = None",
      "import numpy as np\nvalues = [12, 15, 18, 22, 30]\nresult = (float(np.mean(values)), float(np.median(values)), float(np.std(values)))",
      [("mean is 19.4, median 18, std about 6.248", "abs(result[0]-19.4)<1e-9 and result[1]==18.0 and abs(result[2]-6.248)<0.001")]),
     ("Flag outliers in [10,11,12,11,13,12,11,50] with the IQR rule; store the outlier values list in `result`.",
      "import numpy as np\nvalues = [10,11,12,11,13,12,11,50]\nresult = None",
      "import numpy as np\nvalues = [10,11,12,11,13,12,11,50]\nq1, q3 = np.percentile(values, [25, 75])\niqr = q3 - q1\nresult = [v for v in values if v < q1 - 1.5*iqr or v > q3 + 1.5*iqr]",
      [("result equals [50]", "result == [50]")]),
     ("Build a small DataFrame of salaries by dept and compute mean salary per dept; store the dict in `result`.",
      "import pandas as pd\ndf = pd.DataFrame({'dept':['Eng','Eng','Analytics','Analytics'],'salary':[145000,128000,98000,87000]})\nresult = None",
      "import pandas as pd\ndf = pd.DataFrame({'dept':['Eng','Eng','Analytics','Analytics'],'salary':[145000,128000,98000,87000]})\nresult = df.groupby('dept')['salary'].mean().to_dict()",
      [("means are Eng 136500 and Analytics 92500", "result == {'Analytics': 92500.0, 'Eng': 136500.0}")])
    ]))

# ---------- Python: M33 vectors ----------
PE.append(pyex("py-il26-m33-vectors", "IL26-M33", "Vectors: dot products, similarity, norms",
    [
     ("Dot product of [1, 2, 3] and [4, -5, 6]; store it in `result`.",
      "import numpy as np\nresult = None",
      "import numpy as np\nresult = float(np.dot([1, 2, 3], [4, -5, 6]))",
      [("result equals 12.0", "result == 12.0")]),
     ("Cosine similarity between [1, 0] and [1, 1]; store it in `result`.",
      "import numpy as np\nresult = None",
      "import numpy as np\na, b = np.array([1, 0]), np.array([1, 1])\nresult = float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))",
      [("result is about 0.7071", "abs(result - 0.7071) < 0.001")]),
     ("L2 (Euclidean) norm of [3, 4]; store it in `result`.",
      "import numpy as np\nresult = None",
      "import numpy as np\nresult = float(np.linalg.norm([3, 4]))",
      [("result equals 5.0", "result == 5.0")])
    ]))

# ---------- Python: M33 matrices ----------
PE.append(pyex("py-il26-m33-matrices", "IL26-M33", "Matrices: multiply, solve, fit",
    [
     ("Multiply [[1,2],[3,4]] by [[5,6],[7,8]] with numpy; store the nested list in `result`.",
      "import numpy as np\nresult = None",
      "import numpy as np\nresult = (np.array([[1,2],[3,4]]) @ np.array([[5,6],[7,8]])).tolist()",
      [("result equals [[19, 22], [43, 50]]", "result == [[19, 22], [43, 50]]")]),
     ("Solve A x = b for A=[[2,1],[1,3]], b=[8,13]; store [x0, x1] in `result`.",
      "import numpy as np\nresult = None",
      "import numpy as np\nresult = np.linalg.solve(np.array([[2,1],[1,3]]), np.array([8,13])).tolist()",
      [("solution is about [2.2, 3.6]", "abs(result[0]-2.2)<1e-9 and abs(result[1]-3.6)<1e-9")]),
     ("Least-squares line for x=[1,2,3], y=[2.1,3.9,6.2]: store (slope, intercept) in `result`.",
      "import numpy as np\nx = [1,2,3]; y = [2.1,3.9,6.2]\nresult = None",
      "import numpy as np\nx = np.array([1,2,3]); y = np.array([2.1,3.9,6.2])\nA = np.vstack([x, np.ones_like(x)]).T\nslope, intercept = np.linalg.lstsq(A, y, rcond=None)[0]\nresult = (float(slope), float(intercept))",
      [("slope about 2.05, intercept about -0.033", "abs(result[0]-2.05)<0.01 and abs(result[1]+0.0333)<0.01")])
    ]))

# ---------- Python: M34 calculus ----------
PE.append(pyex("py-il26-m34-calculus", "IL26-M34", "Numerical derivatives and integrals",
    [
     ("Numerical derivative of f(x) = x^2 at x=3 via central difference with h=1e-5; store it in `result`.",
      "result = None",
      "f = lambda x: x**2\nh = 1e-5\nresult = (f(3 + h) - f(3 - h)) / (2 * h)",
      [("result is about 6.0", "abs(result - 6.0) < 1e-6")]),
     ("Trapezoid-rule integral of f(x) = 2x from 0 to 4 with n=1000 subintervals; store it in `result`.",
      "import numpy as np\nresult = None",
      "import numpy as np\nx = np.linspace(0, 4, 1001)\nresult = float(np.trapezoid(2 * x, x))",
      [("result is about 16.0", "abs(result - 16.0) < 1e-6")]),
     ("One gradient-descent step on f(x) = (x-5)^2 starting at x=0 with learning rate 0.1; store the new x in `result`.",
      "result = None",
      "grad = 2 * (0 - 5)\nresult = 0 - 0.1 * grad",
      [("result equals 1.0", "result == 1.0")])
    ]))

# ---------- Python: M32 probability simulation ----------
PE.append(pyex("py-il26-m32-probability", "IL26-M32", "Probability by simulation and counting",
    [
     ("Simulate 10000 fair coin flips with numpy seed 42; estimate P(heads); store it in `result`.",
      "import numpy as np\nresult = None",
      "import numpy as np\nrng = np.random.default_rng(42)\nresult = float(rng.random(10000).mean())",
      [("result is between 0.48 and 0.52", "0.48 < result < 0.52")]),
     ("Ad A: 30 clicks of 200 shown. Ad B: 45 clicks of 180 shown. Compute P(click|B) - P(click|A); store it in `result`.",
      "result = None",
      "result = 45/180 - 30/200",
      [("result equals 0.10", "abs(result - 0.10) < 1e-9")]),
     ("A game pays $10 with probability 0.4 and loses $6 with probability 0.6. Compute the expected value; store it in `result`.",
      "result = None",
      "result = 0.4 * 10 + 0.6 * (-6)",
      [("result equals 0.4", "abs(result - 0.4) < 1e-9")])
    ]))

# ---------- Python: M09 pandas ----------
PE.append(pyex("py-il26-m09-pandas", "IL26-M09", "pandas: groupby, merge, pivot",
    [
     ("Group orders by region and sum revenue; store the dict in `result`.",
      "import pandas as pd\ndf = pd.DataFrame({'region':['West','West','East'],'revenue':[100,200,150]})\nresult = None",
      "import pandas as pd\ndf = pd.DataFrame({'region':['West','West','East'],'revenue':[100,200,150]})\nresult = df.groupby('region')['revenue'].sum().to_dict()",
      [("result equals {'East': 150, 'West': 300}", "result == {'East': 150, 'West': 300}")]),
     ("Left-merge orders onto customers by customer_id; fill missing names with 'Unknown'; store the name list in `result`.",
      "import pandas as pd\norders = pd.DataFrame({'customer_id':['c1','c2','c3'],'amount':[50,75,20]})\ncustomers = pd.DataFrame({'customer_id':['c1','c2'],'name':['Alice','Bob']})\nresult = None",
      "import pandas as pd\norders = pd.DataFrame({'customer_id':['c1','c2','c3'],'amount':[50,75,20]})\ncustomers = pd.DataFrame({'customer_id':['c1','c2'],'name':['Alice','Bob']})\nm = orders.merge(customers, on='customer_id', how='left')\nresult = m['name'].fillna('Unknown').tolist()",
      [("result equals ['Alice', 'Bob', 'Unknown']", "result == ['Alice', 'Bob', 'Unknown']")]),
     ("Pivot revenue by region (rows) and quarter (columns) with sum; store the nested dict in `result`.",
      "import pandas as pd\ndf = pd.DataFrame({'region':['West','West','East','East'],'quarter':['Q1','Q2','Q1','Q2'],'revenue':[100,200,150,250]})\nresult = None",
      "import pandas as pd\ndf = pd.DataFrame({'region':['West','West','East','East'],'quarter':['Q1','Q2','Q1','Q2'],'revenue':[100,200,150,250]})\nresult = df.pivot_table(index='region', columns='quarter', values='revenue', aggfunc='sum').to_dict()",
      [("pivot has the four region-quarter cells", "result == {'Q1': {'East': 150, 'West': 100}, 'Q2': {'East': 250, 'West': 200}}")])
    ]))

# ---------- Python: M10 stats ----------
PE.append(pyex("py-il26-m10-stats", "IL26-M10", "Correlation, standardization, percentiles",
    [
     ("Pearson correlation between [1,2,3,4,5] and [2,4,5,4,6] via numpy; store the float in `result`.",
      "import numpy as np\nresult = None",
      "import numpy as np\nresult = float(np.corrcoef([1,2,3,4,5],[2,4,5,4,6])[0,1])",
      [("result is about 0.8528", "abs(result - 0.8528) < 0.001")]),
     ("Z-scores (population std) of [10, 20, 30]; store the list in `result`.",
      "import numpy as np\nresult = None",
      "import numpy as np\nv = np.array([10, 20, 30])\nresult = ((v - v.mean()) / v.std()).tolist()",
      [("z-scores are about [-1.2247, 0, 1.2247]", "abs(result[0]+1.2247)<0.001 and result[1]==0.0 and abs(result[2]-1.2247)<0.001")]),
     ("90th percentile of [5,15,25,35,45,55,65,75,85,95] with numpy; store it in `result`.",
      "import numpy as np\nresult = None",
      "import numpy as np\nresult = float(np.percentile([5,15,25,35,45,55,65,75,85,95], 90))",
      [("result equals 86.0", "result == 86.0")])
    ]))

# ---------- Python: M11 A/B testing ----------
PE.append(pyex("py-il26-m11-abtest", "IL26-M11", "A/B test math in Python",
    [
     ("Conversion rates for A (30/200) and B (45/180), and the relative lift (B-A)/A; store the tuple in `result`.",
      "result = None",
      "pa, pb = 30/200, 45/180\nresult = (pa, pb, (pb - pa) / pa)",
      [("rates 0.15 and 0.25, lift about 0.6667", "abs(result[0]-0.15)<1e-9 and abs(result[1]-0.25)<1e-9 and abs(result[2]-0.6667)<0.001")]),
     ("Two-proportion z-statistic with pooled standard error; store z in `result`.",
      "import math\nna, nb = 200, 180\nxa, xb = 30, 45\nresult = None",
      "import math\nna, nb = 200, 180\nxa, xb = 30, 45\npa, pb = xa/na, xb/nb\np = (xa + xb) / (na + nb)\nse = math.sqrt(p * (1 - p) * (1/na + 1/nb))\nresult = (pb - pa) / se",
      [("z is about 2.445", "abs(result - 2.445) < 0.01")]),
     ("With n=200 per arm and baseline 0.15, is a 5-point lift (to 0.20) significant at 95%? Store True/False in `result`.",
      "import math\nresult = None",
      "import math\npa, pb, n = 0.15, 0.20, 200\np = (pa + pb) / 2\nse = math.sqrt(p * (1 - p) * (2 / n))\nz = (pb - pa) / se\nresult = abs(z) > 1.96",
      [("result is False: z is only about 1.32", "result is False")])
    ]))

# ---------- Python: M36 Palantir python/probability/product ----------
PE.append(pyex("py-il26-m36-product", "IL26-M36", "Probability and product metrics under pressure",
    [
     ("Bayes: 1% prevalence, 95% sensitivity, 90% specificity. Compute P(condition | positive test); store it in `result`.",
      "result = None",
      "result = (0.95 * 0.01) / (0.95 * 0.01 + 0.10 * 0.99)",
      [("result is about 0.0876", "abs(result - 0.0876) < 0.001")]),
     ("Flatten nested events into (user, action) pairs; store the list in `result`.",
      "events = [{'user':'u1','actions':['click','buy']},{'user':'u2','actions':['click']}]\nresult = None",
      "events = [{'user':'u1','actions':['click','buy']},{'user':'u2','actions':['click']}]\nresult = [(e['user'], a) for e in events for a in e['actions']]",
      [("result equals [('u1','click'),('u1','buy'),('u2','click')]", "result == [('u1','click'),('u1','buy'),('u2','click')]")]),
     ("Week-1 actives {u1,u2,u3,u4}, week-2 actives {u2,u3,u5}. Compute week-2 retention of the week-1 cohort; store it in `result`.",
      "result = None",
      "w1 = {'u1','u2','u3','u4'}\nw2 = {'u2','u3','u5'}\nresult = len(w1 & w2) / len(w1)",
      [("result equals 0.5", "result == 0.5")])
    ]))

# ---------- Python: M05 IBM pandas basics ----------
PE.append(pyex("py-il26-m05-pandas", "IL26-M05", "Loading and profiling a CSV with pandas",
    [
     ("Read the CSV text into a DataFrame with StringIO; store the row count in `result`.",
      "import pandas as pd\nfrom io import StringIO\ncsv_text = 'name,age\\nAnn,30\\nBo,25\\nCy,41'\nresult = None",
      "import pandas as pd\nfrom io import StringIO\ncsv_text = 'name,age\\nAnn,30\\nBo,25\\nCy,41'\ndf = pd.read_csv(StringIO(csv_text))\nresult = len(df)",
      [("result equals 3", "result == 3")]),
     ("Compute the mean age from that DataFrame; store it in `result`.",
      "import pandas as pd\nfrom io import StringIO\ncsv_text = 'name,age\\nAnn,30\\nBo,25\\nCy,41'\ndf = pd.read_csv(StringIO(csv_text))\nresult = None",
      "import pandas as pd\nfrom io import StringIO\ncsv_text = 'name,age\\nAnn,30\\nBo,25\\nCy,41'\ndf = pd.read_csv(StringIO(csv_text))\nresult = float(df['age'].mean())",
      [("result equals 32.0", "result == 32.0")]),
     ("Bin ages into 'young' (<=30) and 'mid' (31-45) with pandas cut; store value counts as a dict in `result`.",
      "import pandas as pd\nages = pd.Series([30, 25, 41])\nresult = None",
      "import pandas as pd\nages = pd.Series([30, 25, 41])\nbins = pd.cut(ages, bins=[0, 30, 45], labels=['young', 'mid'])\nresult = bins.value_counts().to_dict()",
      [("young has 2, mid has 1", "result == {'young': 2, 'mid': 1}")])
    ]))

# ---------- Python: M19 portfolio analytics ----------
PE.append(pyex("py-il26-m19-portfolio", "IL26-M19", "Data-driven portfolio decisions",
    [
     ("Rank the projects by views, highest first; store the ordered name list in `result`.",
      "projects = [{'name':'churn','views':1200,'stars':45},{'name':'etl','views':800,'stars':60},{'name':'dashboard','views':2000,'stars':30}]\nresult = None",
      "projects = [{'name':'churn','views':1200,'stars':45},{'name':'etl','views':800,'stars':60},{'name':'dashboard','views':2000,'stars':30}]\nresult = [p['name'] for p in sorted(projects, key=lambda p: p['views'], reverse=True)]",
      [("order is dashboard, churn, etl", "result == ['dashboard', 'churn', 'etl']")]),
     ("Engagement rate = stars / views per project, rounded to 4 decimals; store the dict in `result`.",
      "projects = [{'name':'churn','views':1200,'stars':45},{'name':'etl','views':800,'stars':60},{'name':'dashboard','views':2000,'stars':30}]\nresult = None",
      "projects = [{'name':'churn','views':1200,'stars':45},{'name':'etl','views':800,'stars':60},{'name':'dashboard','views':2000,'stars':30}]\nresult = {p['name']: round(p['stars'] / p['views'], 4) for p in projects}",
      [("etl leads at 0.075", "result == {'churn': 0.0375, 'etl': 0.075, 'dashboard': 0.015}")]),
     ("Composite score = views/100 + stars*2; store the top project's name in `result`.",
      "projects = [{'name':'churn','views':1200,'stars':45},{'name':'etl','views':800,'stars':60},{'name':'dashboard','views':2000,'stars':30}]\nresult = None",
      "projects = [{'name':'churn','views':1200,'stars':45},{'name':'etl','views':800,'stars':60},{'name':'dashboard','views':2000,'stars':30}]\nresult = max(projects, key=lambda p: p['views']/100 + p['stars']*2)['name']",
      [("top project is etl with 128", "result == 'etl'")])
    ]))

DP = data["daxPlaygrounds"]

# ---------- DAX: M02 basics ----------
DP.append(daxpg("dax-il26-m02-basics", "IL26-M02", "Core DAX measures on the Sales table",
    [
     ("Write a measure named Total Revenue that sums Sales[Amount].",
      "Sales",
      "Total Revenue := SUM(Sales[Amount])",
      ["Total Revenue = SUM(Sales[Amount])", "Total Revenue:=SUM(Sales[Amount])"],
      "SUM aggregates the Amount column across whatever filter context the visual applies."),
     ("Write a measure named Avg Deal Size averaging Sales[Amount].",
      "Sales",
      "Avg Deal Size := AVERAGE(Sales[Amount])",
      ["Avg Deal Size = AVERAGE(Sales[Amount])"],
      "AVERAGE is the iterator-free mean of a column; it ignores blank values."),
     ("Write a measure named Order Count counting Sales[OrderID].",
      "Sales",
      "Order Count := COUNT(Sales[OrderID])",
      ["Order Count = COUNT(Sales[OrderID])", "Order Count := COUNTROWS(Sales)"],
      "COUNT tallies non-blank values in the column; COUNTROWS(Sales) is the common equivalent."),
     ("Write a measure named Margin Pct dividing total profit by total revenue.",
      "Sales",
      "Margin Pct := DIVIDE(SUM(Sales[Profit]), SUM(Sales[Amount]))",
      ["Margin Pct = DIVIDE(SUM(Sales[Profit]), SUM(Sales[Amount]))"],
      "DIVIDE guards against divide-by-zero; the plain / operator would error on a zero denominator.")
    ]))

# ---------- DAX: M02 filter context ----------
DP.append(daxpg("dax-il26-m02-context", "IL26-M02", "CALCULATE and filter context",
    [
     ('Write a measure named West Sales: total Sales[Amount] filtered to Region[Name] = "West".',
      "Sales",
      'West Sales := CALCULATE(SUM(Sales[Amount]), Region[Name] = "West")',
      ['West Sales = CALCULATE(SUM(Sales[Amount]), Region[Name] = "West")'],
      "CALCULATE overrides the incoming filter context, keeping only the West region."),
     ("Write a measure named Pct of Total: total revenue divided by revenue with all Sales filters removed.",
      "Sales",
      "Pct of Total := DIVIDE(SUM(Sales[Amount]), CALCULATE(SUM(Sales[Amount]), ALL(Sales)))",
      ["Pct of Total = DIVIDE(SUM(Sales[Amount]), CALCULATE(SUM(Sales[Amount]), ALL(Sales)))"],
      "ALL(Sales) strips filters from the table so the denominator is the grand total."),
     ("Write a measure named Customer Count using DISTINCTCOUNT on Sales[CustomerID].",
      "Sales",
      "Customer Count := DISTINCTCOUNT(Sales[CustomerID])",
      ["Customer Count = DISTINCTCOUNT(Sales[CustomerID])"],
      "DISTINCTCOUNT counts unique customers; COUNT would double-count repeat buyers.")
    ]))

# ---------- DAX: M15 BI measures ----------
DP.append(daxpg("dax-il26-m15-web", "IL26-M15", "Engagement measures for a web-activity model",
    [
     ("Write a measure named Conversion Rate: total Conversions divided by total Visitors.",
      "WebActivity",
      "Conversion Rate := DIVIDE(SUM(WebActivity[Conversions]), SUM(WebActivity[Visitors]))",
      ["Conversion Rate = DIVIDE(SUM(WebActivity[Conversions]), SUM(WebActivity[Visitors]))"],
      "A ratio of two sums; DIVIDE keeps it safe when a segment has zero visitors."),
     ("Write a measure named Avg Session averaging WebActivity[SessionMinutes].",
      "WebActivity",
      "Avg Session := AVERAGE(WebActivity[SessionMinutes])",
      ["Avg Session = AVERAGE(WebActivity[SessionMinutes])"],
      "The simple mean of the session-length column in the current filter context."),
     ('Write a measure named New Visitor Share: visitors where VisitorType = "New" divided by all visitors.',
      "WebActivity",
      'New Visitor Share := DIVIDE(CALCULATE(SUM(WebActivity[Visitors]), WebActivity[VisitorType] = "New"), SUM(WebActivity[Visitors]))',
      ['New Visitor Share = DIVIDE(CALCULATE(SUM(WebActivity[Visitors]), WebActivity[VisitorType] = "New"), SUM(WebActivity[Visitors]))'],
      "CALCULATE narrows the numerator to new visitors while the denominator keeps full context.")
    ]))

TS = data["terminalSims"]

# ---------- Terminal: M08 psql tuning ----------
TS.append(termsim("term-il26-m08-psql", "IL26-M08", "Tune a slow query in psql",
    "You are in psql, connected to the analytics warehouse. A regional-sales summary query is slow; inspect and fix it.",
    [
     ("psql -h warehouse -U analyst -d analytics | psql -d analytics -U analyst -h warehouse",
      "psql (16.x): connected to database analytics as user analyst.",
      "Connect with psql -h warehouse -U analyst -d analytics."),
     ("\\d orders | \\d+ orders",
      "Table orders: columns include region, order_date, amount. Indexes: none on (region, order_date).",
      "Describe the table: \\d orders."),
     ("EXPLAIN ANALYZE SELECT region, SUM(amount) FROM orders GROUP BY region;",
      "Seq Scan on orders (cost high). Planning to add a composite index on the grouping/filter columns.",
      "Prefix the slow query with EXPLAIN ANALYZE."),
     ("CREATE INDEX idx_orders_region_date ON orders (region, order_date);",
      "CREATE INDEX: composite index built on (region, order_date).",
      "CREATE INDEX idx_orders_region_date ON orders (region, order_date);"),
     ("\\timing on",
      "Timing is on. Re-run the query to measure the improvement.",
      "Enable timing with \\timing on."),
     ("\\q",
      "Session closed. With the index, the planner chose an index scan: roughly 40x faster.",
      "Quit psql with \\q.")
    ]))

# ---------- Terminal: M09 python env ----------
TS.append(termsim("term-il26-m09-venv", "IL26-M09", "Set up a clean Python analytics environment",
    "Prepare an isolated Python environment for the analytics project, install the libraries, and run the analysis.",
    [
     ("python -m venv .venv | python3 -m venv .venv",
      "Virtual environment created in .venv/.",
      "Create it with python -m venv .venv."),
     ("source .venv/bin/activate | . .venv/bin/activate",
      "(.venv) prompt active: python and pip now point inside the environment.",
      "Activate with source .venv/bin/activate."),
     ("pip install pandas numpy",
      "Successfully installed pandas and numpy with their dependencies.",
      "Install the libraries: pip install pandas numpy."),
     ("pip freeze > requirements.txt",
      "requirements.txt written with pinned versions for reproducibility.",
      "Pin versions with pip freeze > requirements.txt."),
     ("python analysis.py",
      "Script finished: results written to results.csv.",
      "Run the script: python analysis.py."),
     ("deactivate",
      "Environment deactivated; back to the system Python.",
      "Leave the environment with deactivate.")
    ]))

# ---------- Terminal: M12 psql DDL ----------
TS.append(termsim("term-il26-m12-ddl", "IL26-M12", "Build a star schema in the warehouse",
    "Create the customer dimension and sales fact tables, wire the foreign key, and verify.",
    [
     ("CREATE TABLE dim_customer (customer_id TEXT PRIMARY KEY, name TEXT, segment TEXT);",
      "CREATE TABLE: dim_customer ready.",
      "Define the dimension with a TEXT primary key."),
     ("CREATE TABLE fact_sales (sale_id SERIAL PRIMARY KEY, customer_id TEXT REFERENCES dim_customer(customer_id), amount NUMERIC, sale_date DATE);",
      "CREATE TABLE: fact_sales created with a foreign key to dim_customer.",
      "Add REFERENCES dim_customer(customer_id) on the fact table."),
     ("ALTER TABLE fact_sales ADD COLUMN region TEXT;",
      "ALTER TABLE: column region added.",
      "Extend the fact table with ALTER TABLE ... ADD COLUMN."),
     ("\\d fact_sales",
      "Columns, primary key, and the foreign-key constraint are all shown.",
      "Inspect with \\d fact_sales."),
     ("INSERT INTO dim_customer VALUES ('c1','Acme','enterprise');",
      "INSERT 0 1: one dimension row added.",
      "Seed the dimension with an INSERT."),
     ("SELECT COUNT(*) FROM dim_customer;",
      "count = 1. The dimension is live and joinable.",
      "Verify with SELECT COUNT(*) FROM dim_customer;")
    ]))

# ---------- Terminal: M13 dbt ----------
TS.append(termsim("term-il26-m13-dbt", "IL26-M13", "Run and test the dbt project",
    "The sales-mart dbt project is checked out. Validate the connection, build, test, and document it.",
    [
     ("dbt debug",
      "All checks passed: profile OK, connection OK, 12 models found.",
      "Start with dbt debug to validate the setup."),
     ("dbt run --select stg_orders",
      "Done: 1 of 1 model built (stg_orders).",
      "Build one model first: dbt run --select stg_orders."),
     ("dbt run",
      "Done: 12 of 12 models built.",
      "Build everything with dbt run."),
     ("dbt test",
      "38 tests passed, 0 failed, 0 warnings.",
      "Run the test suite: dbt test."),
     ("dbt docs generate",
      "Documentation generated: open target/index.html.",
      "Generate docs with dbt docs generate."),
     ("dbt run --full-refresh --select marts",
      "Marts rebuilt from scratch with --full-refresh.",
      "Force a rebuild of the marts layer with --full-refresh.")
    ]))

# ---------- Terminal: M14 AWS CLI ----------
TS.append(termsim("term-il26-m14-aws", "IL26-M14", "Explore the data lake with the AWS CLI",
    "The analytics data lake lives in S3 with an Athena workgroup. Explore it and run a query.",
    [
     ("aws s3 ls s3://analytics-lake/",
      "PRE raw/  PRE curated/  PRE results/  PRE logs/",
      "List the bucket: aws s3 ls s3://analytics-lake/."),
     ("aws s3 cp ./sales.csv s3://analytics-lake/raw/sales.csv",
      "upload: ./sales.csv to s3://analytics-lake/raw/sales.csv",
      "Copy the file up: aws s3 cp ./sales.csv s3://analytics-lake/raw/sales.csv."),
     ("aws glue get-tables --database-name analytics",
      "Tables: sales, customers, events.",
      "List catalog tables: aws glue get-tables --database-name analytics."),
     ('aws athena start-query-execution --query-string "SELECT COUNT(*) FROM sales" --result-configuration OutputLocation=s3://analytics-lake/results/',
      "QueryExecutionId returned: the query is running.",
      "Launch it with aws athena start-query-execution and a results location."),
     ("aws s3 ls s3://analytics-lake/results/",
      "Result files present: the query finished.",
      "Check for output: aws s3 ls s3://analytics-lake/results/."),
     ("aws redshift-data execute-statement --cluster-identifier warehouse --database analytics --sql \"SELECT 1\"",
      "Statement submitted to the Redshift cluster.",
      "The Redshift Data API needs cluster, database, and SQL.")
    ]))

# ---------- Terminal: M14 Azure/GCP CLI ----------
TS.append(termsim("term-il26-m14-multicloud", "IL26-M14", "The same lake on Azure and Google Cloud",
    "The team mirrors the lake to Azure Blob Storage and BigQuery. Work both CLIs.",
    [
     ("az storage blob list --container-name raw --account-name analyticlake",
      "Blobs listed: sales.csv, events.csv.",
      "List blobs with az storage blob list, container raw."),
     ("az storage blob upload --file sales.csv --container-name raw --name sales.csv --account-name analyticlake",
      "Upload complete: 1 blob.",
      "Upload with az storage blob upload and the same account/container."),
     ("gcloud bigquery datasets list",
      "Datasets: analytics_mart.",
      "List BigQuery datasets: gcloud bigquery datasets list."),
     ("bq mk analytics_staging",
      "Dataset analytics_staging created.",
      "Create a dataset: bq mk analytics_staging."),
     ('gcloud bigquery query --use_legacy_sql=false "SELECT COUNT(*) FROM analytics_mart.sales"',
      "Query complete: 1 row returned.",
      "Run standard SQL with --use_legacy_sql=false."),
     ("gcloud storage ls gs://analytics-lake/",
      "gs://analytics-lake/raw/  gs://analytics-lake/curated/",
      "List the GCS bucket: gcloud storage ls gs://analytics-lake/.")
    ]))

# ---------- Terminal: M25 R console ----------
TS.append(termsim("term-il26-m25-rscript", "IL26-M25", "Run R from the command line",
    "The Google certificate track uses R. Verify the install, add a package, and run the analysis script.",
    [
     ("Rscript --version",
      "R scripting front-end version 4.3.x.",
      "Check the install: Rscript --version."),
     ('R -e "install.packages(\'dplyr\')" | Rscript -e "install.packages(\'dplyr\')"',
      "dplyr installed into the user library.",
      "Install packages non-interactively with R -e."),
     ("Rscript analysis.R",
      "Attaching dplyr... Summary printed. Script finished with no errors.",
      "Run the script: Rscript analysis.R."),
     ("R CMD BATCH analysis.R",
      "Batch run finished: see analysis.Rout for output.",
      "The classic batch route: R CMD BATCH analysis.R."),
     ('R -q -e "library(dplyr); sessionInfo()"',
      "dplyr loaded; session info printed.",
      "Verify the library loads: R -q -e \"library(dplyr)\".")
    ]))

# ---------- Terminal: M01 bq CLI ----------
TS.append(termsim("term-il26-m01-bq", "IL26-M01", "BigQuery from the command line",
    "The Google Data Analytics certificate leans on BigQuery. Create a dataset, load data, and query it with bq.",
    [
     ("bq ls",
      "Datasets in project: analytics (existing).",
      "List datasets: bq ls."),
     ("bq mk analytics_lab",
      "Dataset analytics_lab created.",
      "Create one: bq mk analytics_lab."),
     ("bq load --source_format=CSV analytics_lab.events ./events.csv",
      "Upload complete: load job finished.",
      "Load the CSV: bq load --source_format=CSV analytics_lab.events ./events.csv."),
     ("bq show analytics_lab.events",
      "Table schema displayed: 5 columns, 1200 rows.",
      "Inspect the table: bq show analytics_lab.events."),
     ("bq query --use_legacy_sql=false \"SELECT COUNT(*) AS n FROM analytics_lab.events\"",
      "Query complete: n = 1200.",
      "Query it with --use_legacy_sql=false for standard SQL."),
     ("bq rm -f -t analytics_lab.events",
      "Table analytics_lab.events deleted.",
      "Clean up: bq rm -f -t analytics_lab.events.")
    ]))

# ---------- Terminal: M06 AWS analytics ----------
TS.append(termsim("term-il26-m06-aws", "IL26-M06", "AWS analytics services from the CLI",
    "The AWS data-analytics certification path: catalog with Glue, query with Athena, govern with Lake Formation.",
    [
     ("aws athena list-databases --catalog-name AwsDataCatalog",
      "Databases: analytics, default.",
      "List Athena databases for the data catalog."),
     ("aws glue start-crawler --name sales-crawler",
      "Crawler sales-crawler started; new partitions will appear in the catalog.",
      "Kick off the crawler: aws glue start-crawler --name sales-crawler."),
     ('aws athena start-query-execution --query-string "SELECT region, SUM(amount) AS total FROM sales GROUP BY region" --result-configuration OutputLocation=s3://analytics-lake/results/',
      "QueryExecutionId returned.",
      "Same start-query-execution pattern, now with a GROUP BY."),
     ("aws lakeformation list-permissions",
      "2 permissions: analyst role has SELECT on analytics.sales.",
      "Check governance: aws lakeformation list-permissions."),
     ("aws s3api head-object --bucket analytics-lake --key raw/sales.csv",
      "Metadata returned: size, ETag, last modified.",
      "Inspect one object: aws s3api head-object with bucket and key."),
     ("aws configure list",
      "Profile default configured in us-east-1.",
      "Verify the CLI setup: aws configure list.")
    ]))

# ---------- Terminal: M07 databricks CLI ----------
TS.append(termsim("term-il26-m07-databricks", "IL26-M07", "Drive Databricks from the CLI",
    "For the Databricks Certified Data Analyst path: authenticate, browse the workspace, and trigger a job.",
    [
     ("databricks --version",
      "Databricks CLI v0.2xx.",
      "Check the install: databricks --version."),
     ("databricks auth login --host https://my-workspace.cloud.databricks.com",
      "Authenticated to the workspace.",
      "Log in against the workspace host."),
     ("databricks workspace ls /Users/analyst",
      "Notebooks listed: sales_analysis, churn_model.",
      "Browse the workspace: databricks workspace ls /Users/analyst."),
     ("databricks clusters list",
      "2 clusters: analytics-cluster (running), job-cluster (terminated).",
      "See compute: databricks clusters list."),
     ("databricks fs ls dbfs:/mnt/lake",
      "raw/  curated/  checkpoints/",
      "Browse the lake mount: databricks fs ls dbfs:/mnt/lake."),
     ("databricks jobs run-now --job-id 4821",
      "Run triggered for job 4821.",
      "Trigger it: databricks jobs run-now --job-id 4821.")
    ]))

# ---------- Terminal: M20 git ----------
TS.append(termsim("term-il26-m20-git", "IL26-M20", "Publish your portfolio repo with git",
    "Your portfolio projects live in ~/portfolio. Initialize the repo and push it to GitHub.",
    [
     ("git init",
      "Initialized empty Git repository in ~/portfolio/.git/.",
      "Start it: git init."),
     ("git add . | git add -A",
      "All project files staged.",
      "Stage everything: git add ."),
     ("git commit -m \"Initial portfolio commit\"",
      "[main (root-commit)] Initial portfolio commit: 14 files.",
      "Commit with a message: git commit -m \"Initial portfolio commit\"."),
     ("git branch -M main",
      "Branch renamed to main.",
      "Standardize the branch: git branch -M main."),
     ("git remote add origin https://github.com/yourname/portfolio.git",
      "Remote origin added.",
      "Point at GitHub: git remote add origin <url>."),
     ("git push -u origin main",
      "Branch main set up to track origin/main. Pushed.",
      "Push and set upstream: git push -u origin main."),
     ("git log --oneline -3",
      "Three commits shown, newest first.",
      "Review history: git log --oneline -3.")
    ]))

# ---------- Terminal: M20 gh CLI ----------
TS.append(termsim("term-il26-m20-gh", "IL26-M20", "Manage the portfolio with the GitHub CLI",
    "Use gh to authenticate, create repos, and run the pull-request workflow without leaving the terminal.",
    [
     ("gh auth login",
      "Authenticated to github.com as yourname.",
      "Authenticate: gh auth login."),
     ("gh repo create portfolio --public --source=. --push",
      "Repository yourname/portfolio created and pushed.",
      "Create and push in one shot with --source and --push."),
     ("gh issue create --title \"Add churn project\" --body \"Portfolio gap: no retention analysis\"",
      "Issue #3 created.",
      "Track the gap: gh issue create with title and body."),
     ("gh pr create --title \"Add churn analysis\" --body \"Closes #3\"",
      "Pull request #4 opened.",
      "Open the PR: gh pr create."),
     ("gh run list",
      "3 workflow runs: all successful.",
      "Check CI: gh run list."),
     ("gh repo view --web",
      "Opening the repository in the browser.",
      "View it: gh repo view --web.")
    ]))

# ---------- Terminal: M22 docker ----------
TS.append(termsim("term-il26-m22-docker", "IL26-M22", "Containerize the capstone",
    "Make the capstone reproducible: build the image, run it, and inspect it.",
    [
     ("docker build -t capstone:latest .",
      "Image capstone:latest built from the Dockerfile.",
      "Build it: docker build -t capstone:latest ."),
     ("docker images",
      "capstone latest ... listed among local images.",
      "Confirm: docker images."),
     ("docker run -d -p 8888:8888 --name capstone capstone:latest",
      "Container capstone started in detached mode.",
      "Run detached with a published port and a name."),
     ("docker ps",
      "capstone is Up, port 8888 mapped.",
      "List running containers: docker ps."),
     ("docker logs capstone",
      "Notebook server log lines streamed.",
      "Read output: docker logs capstone."),
     ("docker compose up -d",
      "Services (notebook, database) started per compose.yaml.",
      "Multi-service route: docker compose up -d."),
     ("docker stop capstone",
      "Container capstone stopped cleanly.",
      "Shut it down: docker stop capstone.")
    ]))

BR = data["branchingScenarios"]

# ---------- Branching: M32 probability interview ----------
BR.append(branch("branch-il26-m32-monty", "IL26-M32", "Interview pressure: the Monty Hall question", "start",
    [
     ("start",
      "The interviewer leans in: three doors, one prize. You pick door 1. The host, who knows where the prize is, opens door 3 to reveal nothing. Stay with door 1 or switch to door 2?",
      [("Switch to door 2", "switch",
        "Right instinct: the host's knowledge concentrates probability."),
       ("Stay with door 1; it is 50/50 now", "stay",
        "Tempting, but the host did not choose randomly.")]),
     ("switch",
      "Good. The interviewer pushes: prove it. Why isn't it 50/50 between the two remaining doors?",
      [("The host's action moves the 2/3 chance onto door 2", "end",
        "Exactly: your door keeps its 1/3; the other unopened door inherits the rest."),
       ("Switching just feels luckier", "end",
        "Weak: interviewers want the mechanism, not the vibe.")]),
     ("stay",
      "The interviewer raises an eyebrow: walk me through the probability, step by step.",
      [("Reconsider: the host gave me information by avoiding the prize", "switch",
        "Good recovery: a non-random reveal is information."),
       ("Two doors remain, so it must be 50/50", "end",
        "This ignores that the host's choice was constrained by knowledge.")]),
     ("end",
      "Debrief: Monty Hall tests whether you update on non-random information. State the mechanism (1/3 stays, 2/3 concentrates), then generalize: always ask whether new information was generated randomly or selectively.",
      [])
    ]))

# ---------- Branching: M17 PII ----------
BR.append(branch("branch-il26-m17-pii", "IL26-M17", "Incident response: the PII dashboard request", "start",
    [
     ("start",
      "Marketing wants customer email addresses added to the shared campaign dashboard for spot-checking. Forty people can see it, including contractors.",
      [("Add the emails; the stakeholder owns the requirement", "pressure",
        "Risky: stakeholder ownership does not transfer privacy risk."),
       ("Propose a hashed customer ID for spot-checks instead", "good",
        "Strong: solve the underlying need without exposing identifiers."),
       ("Add them but restrict the dashboard to the marketing team", "partial",
        "Better, but restriction is a speed bump, not a control.")]),
     ("pressure",
      "Marketing escalates: legal supposedly said it is fine, but you have nothing in writing.",
      [("Require the approval in writing before changing anything", "end",
        "Correct: verbal legal clearance is not clearance."),
       ("Proceed on their verbal assurance", "end",
        "If this goes wrong, the decision trail points at you.")]),
     ("good",
      "The hashed ID works. Now they ask for phone numbers too, same dashboard.",
      [("Apply the same rule: no direct identifiers on shared surfaces", "end",
        "Consistent: the principle does not change with the column."),
       ("Phones are less sensitive; allow it", "end",
        "Phones are direct identifiers and enable the same harm.")]),
     ("partial",
      "Restricted to 8 people. A contractor screenshots the dashboard and emails it outside the company.",
      [("Treat it as an incident: contain, notify, rotate what you can", "end",
        "Right: restriction failed, so incident process takes over."),
       ("It was only 8 people; handle it quietly", "end",
        "Quiet handling hides the blast radius from the people who own the risk.")]),
     ("end",
      "Debrief: default-deny on direct identifiers in shared surfaces, propose safer alternatives that meet the real need, get approvals in writing, and treat restriction as mitigation, never as the control.",
      [])
    ]))

# ---------- Branching: M17 metric pressure ----------
BR.append(branch("branch-il26-m17-metric", "IL26-M17", "Ethics: the metric that lies", "start",
    [
     ("start",
      "Your manager asks you to report active users with a definition that counts anyone who opened the app once. It doubles the number right before the board meeting.",
      [("Use their definition; it is their call", "comply",
        "The number will carry your name when the board asks questions."),
       ("Show both definitions side by side, methodology noted", "honest",
        "Transparent: the board sees the choice instead of inheriting it."),
       ("Refuse outright and escalate above your manager", "refuse",
        "Disproportionate as a first move; negotiation usually works.")]),
     ("comply",
      "The board celebrates. Next quarter the definition quietly reverts and growth goes negative.",
      [("Accept it as a lesson about ownership", "end",
        "The lesson is real, but the credibility damage is too."),
       ("Document your objection now, after the fact", "end",
        "Late documentation protects no one; the moment was before publication.")]),
     ("honest",
      "Your manager is annoyed but the board appreciates the clarity and picks the stricter definition going forward.",
      [("Hold the line on methodology notes in every deck", "end",
        "This is the senior habit: definitions travel with numbers, always."),
       ("Let the manager present it alone next time", "end",
        "Withdrawing avoids conflict but abandons the standard you just set.")]),
     ("refuse",
      "Escalation burns trust with your manager over a disagreement that had a middle path.",
      [("Apologize and propose the side-by-side approach", "end",
        "Recovery is possible: lead with the workable alternative."),
       ("Stand your ground on principle", "end",
        "Principle matters, but so does proportionality; pick battles with no compromise path.")]),
     ("end",
      "Debrief: never publish a number whose definition you would not defend in front of the board. Side-by-side with methodology is the standard move; escalation is the last resort, not the first.",
      [])
    ]))

# ---------- Branching: M18 vague request ----------
BR.append(branch("branch-il26-m18-vague", "IL26-M18", "Stakeholder management: the vague request", "start",
    [
     ("start",
      "A director Slacks you: can you pull some data on churn? No context, no deadline, no decision attached.",
      [("Start querying immediately to show speed", "rush",
        "Speed without direction usually produces the wrong artifact."),
       ("Ask what decision this will inform: the 5 whys", "why",
        "The senior move: scope follows the decision, not the data."),
       ("Send last quarter's churn deck; it is probably fine", "deck",
        "Stale analysis presented as fresh is a quiet credibility risk.")]),
     ("why",
      "Three whys in, the truth surfaces: the CFO is deciding whether to fund a retention program and needs churn by segment, this week.",
      [("Scope it: segments, timeframe, one-page readout by Friday", "end",
        "A scoped commitment beats an open-ended promise every time."),
       ("Promise the full analysis by tomorrow morning", "end",
        "Overpromising sets up the exact failure you were trying to avoid.")]),
     ("rush",
      "You deliver a 40-tab workbook. They needed one number for a meeting in an hour.",
      [("Extract the one number and send it now", "end",
        "Salvageable, but the rework was avoidable with one question."),
       ("Defend the workbook's thoroughness", "end",
        "Thoroughness that misses the decision is just latency.")]),
     ("deck",
      "The deck's churn definition changed two quarters ago; the numbers are not comparable.",
      [("Recall it and rebuild on the current definition", "end",
        "Painful but correct; shipping known-stale numbers is worse."),
       ("Add a footnote about the definition change", "end",
        "A footnote does not fix a misleading headline number.")]),
     ("end",
      "Debrief: vague requests get questions, not queries. Find the decision, the audience, and the deadline first; then commit to a scoped deliverable you can actually hit.",
      [])
    ]))

# ---------- Branching: M18 saying no ----------
BR.append(branch("branch-il26-m18-no", "IL26-M18", "Stakeholder management: saying no with alternatives", "start",
    [
     ("start",
      "Sales wants a forecast, Product wants funnel analysis, Finance wants a variance report. All three say by Friday. You are one analyst.",
      [("Work the weekend and do all three", "burnout",
        "Heroics scale once; expectations scale forever."),
       ("Rank the three by business impact with the requesters, then sequence", "sequence",
        "The professional play: make the tradeoff visible and shared."),
       ("Do the easiest one well and quietly drop the others", "drop",
        "Silent drops surface at the worst possible moment.")]),
     ("sequence",
      "The three leads agree: the forecast unblocks a pricing decision, so it goes first; the variance report can wait until Tuesday.",
      [("Confirm the sequence in writing with dates", "end",
        "Written sequencing is what makes the agreement stick."),
       ("Keep it verbal; everyone seemed aligned", "end",
        "Alignment without a record evaporates by Thursday.")]),
     ("burnout",
      "You ship all three, exhausted. Next week brings four requests.",
      [("Set the sequencing norm now, while the win is fresh", "end",
        "Convert the heroics into a process before the pattern hardens."),
       ("Accept this as the new normal", "end",
        "Unsustainable pace degrades the quality they are praising.")]),
     ("drop",
      "Finance discovers the missing variance report during close.",
      [("Own it and deliver a rush version", "end",
        "Accountability helps, but the trust dent remains."),
       ("Blame competing priorities", "end",
        "Blame without a sequencing process just spreads the frustration.")]),
     ("end",
      "Debrief: no is a complete answer when it comes with a ranked alternative. Make tradeoffs explicit, get them agreed in writing, and never let silent drops or heroics become the operating model.",
      [])
    ]))

# ---------- Branching: M25 R vs Python ----------
BR.append(branch("branch-il26-m25-choice", "IL26-M25", "Tooling judgment: R or Python for this task?", "start",
    [
     ("start",
      "Your team is Python-first, but the certificate project template is in R and the stakeholder's legacy report is an R Markdown file that still runs monthly.",
      [("Rewrite everything in Python immediately", "rewrite",
        "Purity has a cost: rewrites introduce risk with no stakeholder benefit."),
       ("Keep R for the legacy report; use Python for new work", "pragmatic",
        "Pragmatic: match the tool to the job and the team."),
       ("Do the whole project in R to match the template", "ronly",
        "The template is a starting point, not a constraint.")]),
     ("pragmatic",
      "The legacy report keeps running untouched; your new analysis ships in Python and the team can review it.",
      [("Document the boundary: what stays in R and why", "end",
        "Explicit boundaries prevent the next person from re-litigating this."),
       ("Quietly plan to migrate the R report later", "end",
        "A migration needs a reason; if it runs fine, leave it.")]),
     ("rewrite",
      "The rewrite takes two weeks and introduces a subtle aggregation difference nobody catches for a month.",
      [("Add reconciliation checks between old and new outputs", "end",
        "If you must rewrite, prove equivalence before switching."),
       ("Ship it; the logic was straightforward", "end",
        "Straightforward logic still deserves a parity check.")]),
     ("ronly",
      "Nobody on the team can review your R code, and onboarding the next analyst gets harder.",
      [("Add thorough comments to compensate", "end",
        "Comments help, but they do not replace reviewable code."),
       ("Offer to teach the team R", "end",
        "A big ask to solve a problem you created.")]),
     ("end",
      "Debrief: tool choice is a team decision, not a personal preference. Keep working systems working, write new work in the team's stack, and document the boundary.",
      [])
    ]))

# ---------- Branching: M01 cert study plan ----------
BR.append(branch("branch-il26-m01-plan", "IL26-M01", "Certification strategy: planning the Google certificate", "start",
    [
     ("start",
      "You have 8 weeks for the Google Data Analytics certificate. It covers spreadsheets, SQL, R, and a capstone, but your SQL is already strong.",
      [("Study everything equally: two weeks per area", "equal",
        "Equal time ignores your starting position."),
       ("Skim SQL, double down on R and the capstone case study", "focus",
        "Allocate to the gap: strengths need maintenance, weaknesses need reps."),
       ("Skip straight to the capstone; you learn by doing", "capstone",
        "The capstone assumes the foundations; gaps surface mid-project.")]),
     ("focus",
      "R clicks by week 5 and the capstone has a solid week of polish time.",
      [("Do timed practice on the weakest R topics", "end",
        "Targeted reps beat re-reading chapters."),
       ("Re-read the SQL material anyway for completeness", "end",
        "Completeness is the enemy of the schedule; trust the skim.")]),
     ("equal",
      "Week 7 arrives with R still shaky and the capstone untouched.",
      [("Reallocate remaining time to R and the capstone", "end",
        "Late reallocation is better than none, but the plan should have done this."),
       ("Push through on the original schedule", "end",
        "Sunk-cost scheduling: the plan serves you, not the reverse.")]),
     ("capstone",
      "Mid-capstone you hit R data-cleaning tasks the coursework would have made routine.",
      [("Pause the capstone and backfill the R foundations", "end",
        "Correct call: foundations first, even mid-project."),
       ("Work around the gaps with spreadsheets", "end",
        "Workarounds become the permanent, fragile solution.")]),
     ("end",
      "Debrief: study plans allocate time to gaps, not to comfort. Skim strengths, drill weaknesses, and protect capstone time like a deadline.",
      [])
    ]))

# ---------- Branching: M04 data-quality incident ----------
BR.append(branch("branch-il26-m04-feed", "IL26-M04", "Data-quality incident: the broken feed", "start",
    [
     ("start",
      "Monday 8 AM: the executive dashboard shows revenue down 40% overnight. The pipeline ran green.",
      [("Alert everyone that revenue has collapsed", "panic",
        "A green pipeline with a 40% move smells like data, not business."),
       ("Check source row counts before raising any alarm", "triage",
        "Measure first: row counts separate data incidents from real ones."),
       ("Re-run the pipeline; green runs cannot be wrong", "rerun",
        "Re-running a green pipeline reproduces the same wrong result.")]),
     ("triage",
      "The source feed has 60% fewer rows than Friday: the vendor changed the export format over the weekend.",
      [("Pin a data-quality notice on the dashboard and page the vendor contact", "end",
        "Textbook: contain the misinformation, then fix the cause."),
       ("Quietly patch the parser and backfill", "end",
        "A silent fix leaves no audit trail and the notice never goes up.")]),
     ("panic",
      "Leadership spends the morning modeling layoffs before anyone checks the feed.",
      [("Own the false alarm publicly", "end",
        "Owning it is right, but the trust cost was avoidable."),
       ("Blame the pipeline's green status", "end",
        "The pipeline did its job; the verification step was yours.")]),
     ("rerun",
      "Same result, one hour lost, and the dashboard still shows the 40% drop.",
      [("Now check the source row counts", "end",
        "You arrive at triage an hour late; the notice should have been up."),
       ("Escalate to engineering as a pipeline bug", "end",
        "Escalating a data issue as a pipeline bug misdirects the fix.")]),
     ("end",
      "Debrief: a green run is not a correct run. Check row counts and distributions first, contain bad numbers with a visible notice, fix with an audit trail, and never let executives act on unverified moves.",
      [])
    ]))

# ---------- Branching: M05 IBM cert decision ----------
BR.append(branch("branch-il26-m05-study", "IL26-M05", "Certification strategy: the IBM certificate path", "start",
    [
     ("start",
      "The IBM Data Analyst certificate covers Python, SQL, and visualization, but you already hold strong pandas skills from the Python module.",
      [("Take every course in order, front to back", "linear",
        "Linear paths waste your scarcest resource: study hours."),
       ("Test out of the Python sections via the practice assessments, then focus on the gaps", "assess",
        "Assess first: prove the strength, then spend time where it counts."),
       ("Skip the certificate; your portfolio proves the skills", "skip",
        "Portfolios prove skill; certificates prove baseline to HR filters.")]),
     ("assess",
      "You place out of two Python courses and find the SQL-for-analysis section genuinely new.",
      [("Finish the SQL sections and the capstone project", "end",
        "Targeted completion: the credential plus actual new skill."),
       ("Also redo the Python courses for the certificate of completion", "end",
        "Completionism over learning: the hours do not buy you anything.")]),
     ("linear",
      "Week 4: you are re-learning groupby for the third time while the capstone waits.",
      [("Switch to assessment-first now", "end",
        "Pivoting mid-course recovers the schedule."),
       ("Finish what you started", "end",
        "Finishing a misallocated plan is just slower misallocation.")]),
     ("skip",
      "A recruiter screen asks for a baseline credential and moves on to the next candidate.",
      [("Reconsider: the certificate is cheap insurance for HR filters", "end",
        "Pragmatic: credentials open doors portfolios cannot."),
       ("Double down on portfolio only", "end",
        "A defensible strategy, but you accept the filter risk knowingly.")]),
     ("end",
      "Debrief: assess before you study, spend hours on gaps, and treat entry-level certificates as HR-filter insurance rather than learning endpoints.",
      [])
    ]))

# ---------- Branching: M35 whiteboard pressure ----------
BR.append(branch("branch-il26-m35-whiteboard", "IL26-M35", "Interview scenario: SQL on the whiteboard", "start",
    [
     ("start",
      "The interviewer asks for top-2 customers per region by revenue, live on the whiteboard, narrating as you go. Your mind goes blank on window functions.",
      [("Freeze and stare at the board", "freeze",
        "Silence reads as stuck; narration buys thinking time."),
       ("Narrate your plan first: aggregate, then rank, then filter", "narrate",
        "Structure first: interviewers grade the plan as much as the syntax."),
       ("Write a GROUP BY and hope the ranking sorts itself out", "hope",
        "Hoping the query self-assembles is not a strategy.")]),
     ("narrate",
      "You outline: CTE for customer-region totals, RANK() partitioned by region, filter rank <= 2. The interviewer nods.",
      [("Write the CTE carefully, checking each clause aloud", "end",
        "Deliberate and narrated beats fast and silent."),
       ("Rush the syntax to show speed", "end",
        "Speed without checking is how ties and off-by-ones slip in.")]),
     ("freeze",
      "Ten seconds of silence. The interviewer offers: want to talk through the approach first?",
      [("Take the lifeline: describe the plan in words", "narrate",
        "Good recovery: the plan is gradable even without syntax."),
       ("Decline and keep staring", "end",
        "Declining help signals worse than needing it.")]),
     ("hope",
      "The GROUP BY is correct but there is no ranking; the interviewer asks how you limit to top 2 per region.",
      [("Pivot to the window-function plan now", "narrate",
        "Recoverable: name the missing piece explicitly."),
       ("Suggest LIMIT 2", "end",
        "LIMIT 2 gives two rows total, not two per region.")]),
     ("end",
      "Debrief: narrate the plan before the syntax, build in CTE-sized steps you can verify aloud, and treat interviewer prompts as lifelines, not judgments.",
      [])
    ]))

# ---------- Branching: M36 product sense ----------
BR.append(branch("branch-il26-m36-metric", "IL26-M36", "Product sense: defining the right metric", "start",
    [
     ("start",
      "Interview prompt: this analytics product's weekly active users are flat, but the team feels engagement is growing. What do you measure?",
      [("Report WAU anyway; it is the standard metric", "wau",
        "Standards are defaults, not answers."),
       ("Decompose engagement: sessions per active user, depth per session, feature mix", "decompose",
        "Decomposition finds the growth the headline hides."),
       ("Survey users about whether they feel engaged", "survey",
        "Feelings are data, but lagging and noisy for this question.")]),
     ("decompose",
      "Sessions per user are up 20%; a new workflow feature drives it. The interviewer asks: is that good?",
      [("Check retention of the new behavior before celebrating", "end",
        "Senior answer: intensity without retention is a sugar rush."),
       ("Declare victory: engagement is growing", "end",
        "Premature: you have not ruled out novelty effects.")]),
     ("wau",
      "Flat WAU, flat story. The interviewer waits.",
      [("Pivot to decomposition now", "decompose",
        "Better late: the structured answer was always available."),
       ("Argue WAU is the only metric that matters", "end",
        "Doubling down on the flat metric ends the discussion.")]),
     ("survey",
      "Users say they love it. The interviewer asks how you would verify behaviorally.",
      [("Pair the survey with session-depth and return-rate data", "decompose",
        "Attitude plus behavior is the complete answer."),
       ("Trust the survey; users know best", "end",
        "Stated preference without revealed preference is half the picture.")]),
     ("end",
      "Debrief: when the headline metric is flat, decompose before you conclude. Intensity, depth, and retention together tell the engagement story; any one alone can mislead.",
      [])
    ]))

# ---------- Branching: M37 ontology modeling ----------
BR.append(branch("branch-il26-m37-model", "IL26-M37", "Ontology thinking: modeling the domain", "start",
    [
     ("start",
      "You must model a logistics network: shipments move between facilities via carriers, and analysts need late-delivery rates by lane and carrier. Where do you start?",
      [("List tables first: shipments, facilities, carriers", "tables",
        "Tables before concepts risks modeling the source system, not the domain."),
       ("Name the objects, their properties, and the links between them", "ontology",
        "Ontology first: objects, properties, links; tables follow."),
       ("Ask engineering what the source schema looks like", "source",
        "Source-first modeling inherits source-system quirks.")]),
     ("ontology",
      "Objects: Shipment, Facility, Carrier. Links: Shipment runs Facility-to-Facility, is carried by Carrier. Properties: weights, dates, promised vs delivered.",
      [("Derive the lane link table and late-rate measures from the links", "end",
        "The model directly yields the analysis: lanes are links, late rates are link properties."),
       ("Add every attribute anyone might ever want", "end",
        "Attribute hoarding without use cases bloats the model.")]),
     ("tables",
      "You build three tables mirroring the operational database, and late-rate logic gets tangled in joins.",
      [("Refactor around the lane concept explicitly", "ontology",
        "Recovery: name the domain concept and remodel."),
       ("Push through with complex SQL", "end",
        "Complexity compounds; the model debt grows.")]),
     ("source",
      "The source schema has shipment legs split across two systems with different IDs.",
      [("Model the domain linkage independently of source keys", "ontology",
        "Right: the ontology needs its own identity resolution."),
       ("Pick one system's IDs as canonical", "end",
        "Inherits the chosen system's blind spots.")]),
     ("end",
      "Debrief: model the domain before the database. Name objects, properties, and links; let the analysis you need (lanes, late rates) validate the model.",
      [])
    ]))

# ---------- Branching: M38 banking incident ----------
BR.append(branch("branch-il26-m38-break", "IL26-M38", "Banking data: the reconciliation break", "start",
    [
     ("start",
      "Morning reconciliation: account 1002 shows a 12,000 credit in core banking with no matching custody entry. The report goes to risk in two hours.",
      [("Adjust the custody side to match; the amounts must tie", "plug",
        "Plugging breaks is how reconciliation fraud starts; never adjust to force a tie."),
       ("Quarantine the break, age it, and report it as an open item", "quarantine",
        "The control mindset: breaks are reported, not hidden."),
       ("Wait: maybe the custody feed is just late", "wait",
        "Possible, but hope is not a control.")]),
     ("quarantine",
      "The break is logged, aged, and flagged. Risk asks: could it be a timing difference?",
      [("Show the value-date matching rule and the feed cutoff times", "end",
        "Evidence over opinion: the matching rule decides."),
       ("Agree it is probably timing and close it", "end",
        "Closing on probably defeats the purpose of the control.")]),
     ("plug",
      "The report ties. Next week audit finds the manual adjustment with no ticket.",
      [("Document it retroactively", "end",
        "Retroactive documentation does not restore the control."),
       ("Reverse the adjustment and reopen the break", "end",
        "The only clean path, but the trust damage is done.")]),
     ("wait",
      "Two hours pass; the custody feed arrives and the entry is genuinely missing, not late.",
      [("Quarantine and report it now", "quarantine",
        "Late triage is still triage, but the report went out unflagged."),
       ("Roll it into tomorrow's reconciliation", "end",
        "Deferring a known break is a choice with a paper trail.")]),
     ("end",
      "Debrief: reconciliation breaks are reported and aged, never plugged. Timing differences are decided by matching rules and cutoff evidence, not by optimism.",
      [])
    ]))

# ---------- Branching: M39 audit finding ----------
BR.append(branch("branch-il26-m39-audit", "IL26-M39", "Controls: the audit finding", "start",
    [
     ("start",
      "Internal audit finds three report runs last month with no approver recorded, including one CCAR Summary whose checksum changed between runs. The finding draft lands on your desk.",
      [("Dispute it: the reports were correct", "dispute",
        "Correctness is not the finding; the missing control is."),
       ("Accept it and propose a fix: approval gates before publication", "accept",
        "Own the gap: controls, not correctness, are the issue."),
       ("Blame the tooling: the approval field was optional", "blame",
        "Tooling explains; it does not absolve the process owner.")]),
     ("accept",
      "You propose: reports cannot publish without a recorded approver, and checksum changes trigger re-approval.",
      [("Add the rule to the runbook and backfill the missing approvals", "end",
        "Complete: preventive control plus remediation of the gap."),
       ("Implement the gate but skip the backfill", "end",
        "The historical gap stays open for the next audit.")]),
     ("dispute",
      "Audit shows the finding is about control design, not report accuracy. Disputing it escalates the severity.",
      [("Concede and propose the fix", "accept",
        "Recovery is possible once you address the actual finding."),
       ("Escalate to your VP", "end",
        "Escalating a valid finding burns capital for nothing.")]),
     ("blame",
      "The tooling was indeed optional-by-default, but your team owned the process.",
      [("Fix the process and the tooling default", "accept",
        "Both layers: make the control unavoidable."),
       ("Ask IT to lock the field", "end",
        "A technical fix without a process owner still drifts.")]),
     ("end",
      "Debrief: audit findings about controls are answered with controls. Accept the gap, make the control unavoidable, remediate history, and document it.",
      [])
    ]))

# ---------- Branching: M40 incident triage ----------
BR.append(branch("branch-il26-m40-incident", "IL26-M40", "Day in the life: pipeline incident triage", "start",
    [
     ("start",
      "9:12 AM: the 8 AM sales mart refresh failed. The CEO's dashboard is stale and the 10 AM revenue huddle is at risk. PagerDuty names you.",
      [("Restart the job immediately", "restart",
        "Restarting before diagnosis can corrupt partial state."),
       ("Check the failure logs and the last successful run's watermark", "diagnose",
        "Diagnose first: logs, then watermark, then blast radius."),
       ("Tell the CEO the dashboard will be late", "notify",
        "Notification matters, but lead with facts, not just delay.")]),
     ("diagnose",
      "The load step failed on a schema change in the source: a new column broke the insert. The watermark is intact at 7 AM.",
      [("Pin a stale-data notice, fix the schema mapping, rerun from the watermark", "end",
        "Textbook triage: contain, fix forward, rerun cleanly."),
       ("Drop the new column and rerun", "end",
        "Dropping data silently changes the mart's contract.")]),
     ("restart",
      "The restart fails the same way, and now there are two overlapping partial loads.",
      [("Stop, diagnose the schema error, clean the partial load", "diagnose",
        "Recovery costs more than the diagnosis would have."),
       ("Restart once more; third time lucky", "end",
        "Hope is not a runbook.")]),
     ("notify",
      "The CEO appreciates the heads-up and asks what happened and when it will be fixed.",
      [("Diagnose first, then report with a timeline", "diagnose",
        "Right order: facts, then communication."),
       ("Promise it will be fixed by 10", "end",
        "Promising before diagnosing sets up a second failure.")]),
     ("end",
      "Debrief: triage is diagnose, contain, communicate, fix. Never restart blind, never silently change the data contract, and always report with a timeline grounded in the diagnosis.",
      [])
    ]))

# ---------- Branching: M40 executive uncertainty ----------
BR.append(branch("branch-il26-m40-uncertainty", "IL26-M40", "Executive communication under uncertainty", "start",
    [
     ("start",
      "The CFO asks: what will Q4 revenue be? Your model says 4.2M, but the prediction interval is 3.1M to 5.3M and a key input just changed.",
      [("Answer 4.2M confidently", "point",
        "A point estimate without uncertainty is a promise you cannot keep."),
       ("Give the range, the key drivers, and what would move it", "range",
        "Ranges plus drivers: the executive-grade answer."),
       ("Say the model is too uncertain to answer", "dodge",
        "Abdicating the question abandons your seat at the table.")]),
     ("range",
      "The CFO asks which driver matters most and what you recommend.",
      [("Name the top driver, quantify its swing, recommend a hedge", "end",
        "Decision-ready: uncertainty translated into action."),
       ("List all twelve drivers equally", "end",
        "Equal weighting is no weighting; prioritize.")]),
     ("point",
      "Q4 lands at 3.4M. The CFO remembers your confident 4.2M.",
      [("Show the interval you had and explain the miss", "end",
        "Honest post-mortem, but the confident point already spent trust."),
       ("Blame the changed input", "end",
        "The input change was knowable when you answered.")]),
     ("dodge",
      "The CFO turns to someone willing to give a number.",
      [("Re-enter with the range and drivers", "range",
        "Better late: a ranged answer beats no answer."),
       ("Stay out of it", "end",
        "Silence cedes the analysis to whoever speaks.")]),
     ("end",
      "Debrief: executives need ranges, not points; drivers, not dumps; and recommendations, not abdication. Uncertainty communicated well builds more trust than false precision.",
      [])
    ]))

# ---------- Branching: M19 portfolio selection ----------
BR.append(branch("branch-il26-m19-select", "IL26-M19", "Portfolio architecture: choosing projects", "start",
    [
     ("start",
      "You have time for three portfolio projects. Candidates: a churn analysis, an ETL pipeline, a dashboard, a pricing experiment, and a data-quality audit.",
      [("Pick the three you find most fun", "fun",
        "Fun optimizes for you; hiring managers optimize for evidence."),
       ("Cover three hiring signals: analysis, engineering, communication", "cover",
        "Portfolio as evidence: one project per signal."),
       ("Do all five superficially to look productive", "five",
        "Breadth without depth reads as tutorial-following.")]),
     ("cover",
      "You pick churn analysis, the ETL pipeline, and the dashboard. Each needs a README that explains the business question.",
      [("Write decision-focused READMEs: question, method, result, next step", "end",
        "Hiring managers skim for judgment, not code volume."),
       ("Let the code speak for itself", "end",
        "Code without narrative forces the reader to guess the point.")]),
     ("fun",
      "Three fun projects, all exploratory analysis, no engineering or communication evidence.",
      [("Add the missing signals with project number four", "cover",
        "Recovery: rebalance toward the signals."),
       ("Ship them as-is", "end",
        "A portfolio of one signal looks like one skill.")]),
     ("five",
      "Five thin projects; every README says work in progress.",
      [("Cut to three and finish them properly", "cover",
        "Finished beats numerous, every time."),
       ("Ship all five", "end",
        "Unfinished work signals unfinished thinking.")]),
     ("end",
      "Debrief: a portfolio is evidence, not activity. Cover analysis, engineering, and communication; finish fewer projects completely; narrate the business decision in every README.",
      [])
    ]))

# ---------- Branching: M21 dashboard portfolio ----------
BR.append(branch("branch-il26-m21-dash", "IL26-M21", "Dashboard portfolio: what hiring managers want", "start",
    [
     ("start",
      "You are choosing which dashboards to feature. One is visually stunning but answers no business question; another is plain but drove a pricing decision.",
      [("Feature the stunning one; visuals get clicks", "pretty",
        "Clicks are not interviews; hiring managers test for decisions."),
       ("Feature the plain one and explain the decision it drove", "plain",
        "Impact over aesthetics: the story is the product."),
       ("Feature both and let viewers decide", "both",
        "Curation is the skill; abdication is not.")]),
     ("plain",
      "You write up the pricing decision: the analysis, the recommendation, the outcome.",
      [("Include the messy middle: the wrong turns and what you learned", "end",
        "Process transparency is senior signal."),
       ("Present only the polished final view", "end",
        "Polish without process looks like a template.")]),
     ("pretty",
      "In an interview, the hiring manager asks what decision it informed. Silence.",
      [("Pivot to the plain dashboard's story", "plain",
        "The story was always the asset."),
       ("Talk about the design techniques", "end",
        "Technique without purpose does not survive the question.")]),
     ("both",
      "The portfolio page is crowded and the strong piece gets lost.",
      [("Curate down to the decision-driven work", "plain",
        "Editing is part of the craft."),
       ("Keep everything; more is more", "end",
        "More dilutes; curation concentrates.")]),
     ("end",
      "Debrief: feature dashboards that drove decisions, narrate the business question and outcome, show your working, and curate ruthlessly.",
      [])
    ]))

# ---------- Branching: M22 capstone scoping ----------
BR.append(branch("branch-il26-m22-scope", "IL26-M22", "Capstone blueprint: scoping the project", "start",
    [
     ("start",
      "Your capstone idea: predict customer churn, build the pipeline, the model, the dashboard, and a real-time API. Six weeks.",
      [("Build it all; ambition impresses", "all",
        "Ambition without scoping produces five half-systems."),
       ("Cut to the decision: which customers to save, and how the business acts on it", "cut",
        "Scope to the decision: prediction serving retention action."),
       ("Start building and see how far you get", "drift",
        "Drift discovers scope by exhaustion.")]),
     ("cut",
      "Scoped: batch churn scores, a pipeline, and a dashboard the retention team can act on. The API becomes a documented next step.",
      [("Define done: scored, explained, dashboarded, reproducible", "end",
        "A crisp definition of done is what makes six weeks enough."),
       ("Keep the API as a stretch goal", "end",
        "Stretch goals quietly become commitments; document, do not promise.")]),
     ("all",
      "Week 4: the pipeline works, the model is unvalidated, the dashboard is a sketch, the API is a README.",
      [("Cut scope now and finish the core", "cut",
        "Late scoping still beats shipping nothing finished."),
       ("Push harder on all five", "end",
        "More effort on five fronts finishes none.")]),
     ("drift",
      "Week 3 and you are tuning hyperparameters for a model with no pipeline feeding it.",
      [("Stop and write the blueprint: decision, data, deliverables", "cut",
        "The blueprint should have come first; second-best is now."),
       ("Keep tuning; the model is the impressive part", "end",
        "A model with no pipeline is a notebook, not a capstone.")]),
     ("end",
      "Debrief: scope the capstone to a business decision, define done crisply, cut ruthlessly, and let stretch goals live in documentation, not in promises.",
      [])
    ]))

# ---------- Branching: M23 take-home case ----------
BR.append(branch("branch-il26-m23-takehome", "IL26-M23", "Interview loops: the take-home case", "start",
    [
     ("start",
      "The take-home arrives Friday 5 PM, due Monday 9 AM: analyze a messy 50k-row dataset and recommend whether to expand to a new market. No other guidance.",
      [("Start coding immediately; time is short", "code",
        "Coding before framing burns the scarcest hours on the wrong question."),
       ("Spend Friday night framing: the decision, the analyses, the risks", "frame",
        "Framing first: an hour of structure saves ten of rework."),
       ("Email asking for clarification and wait", "ask",
        "Clarification is good; waiting all weekend is not.")]),
     ("frame",
      "Framed: market sizing, unit economics under three scenarios, and the data-quality caveats. Saturday is execution.",
      [("Timebox each analysis and reserve Sunday for the writeup", "end",
        "The writeup is the deliverable; analysis without narrative does not get hired."),
       ("Chase every interesting thread in the data", "end",
        "Interesting is not the same as decision-relevant.")]),
     ("code",
      "Sunday night: twelve charts, no recommendation, and a data-quality issue you noticed too late.",
      [("Write the recommendation from what you have, flagging the caveat", "end",
        "Salvageable if the caveat is front and center."),
       ("Pull an all-nighter to redo it", "end",
        "Exhaustion degrades the judgment the case is testing.")]),
     ("ask",
      "No reply by Saturday noon.",
      [("Proceed with stated assumptions, documented", "frame",
        "Documented assumptions beat waiting."),
       ("Keep waiting; guessing wrong is worse", "end",
        "Waiting consumes the weekend; assumptions are gradable.")]),
     ("end",
      "Debrief: take-homes grade judgment under time pressure. Frame the decision first, timebox ruthlessly, document assumptions, and reserve real time for the narrative: the recommendation is the product.",
      [])
    ]))

# ---------- Branching: M23 behavioral ----------
BR.append(branch("branch-il26-m23-behavioral", "IL26-M23", "Interview loops: behavioral and offers", "start",
    [
     ("start",
      "Final round: tell me about a time your analysis was wrong. You have a real story: a forecast that missed because of a data bug you caught late.",
      [("Tell the polished version where you were the hero", "polish",
        "Polished stories dodge the question; interviewers notice."),
       ("Tell it straight: the miss, the cause, what changed in your process", "straight",
        "STAR with a real failure and a process fix is the strongest answer."),
       ("Say you have never been wrong", "deny",
        "Nobody believes it, and it ends the trust.")]),
     ("straight",
      "They follow up: what would you do differently with the same data today?",
      [("Name the specific check you added: source row-count alerts before modeling", "end",
        "Concrete process change beats abstract lessons."),
       ("Say you would be more careful", "end",
        "Vague; the process fix was the whole point.")]),
     ("polish",
      "The interviewer probes the timeline; the polish cracks.",
      [("Drop the polish and tell the real version", "straight",
        "Honesty under pressure recovers well."),
       ("Hold the polished line", "end",
        "Doubling down on spin is memorable in the wrong way.")]),
     ("deny",
      "Awkward silence. The interviewer moves on, unimpressed.",
      [("Reopen it later with the real story", "straight",
        "Late honesty beats none, barely."),
       ("Let it go", "end",
        "The impression stands.")]),
     ("end",
      "Debrief: behavioral rounds reward honest failure stories with process fixes. STAR format, real miss, specific change. Never polish, never deny.",
      [])
    ]))

# ---------- Branching: M24 90-day roadmap ----------
BR.append(branch("branch-il26-m24-roadmap", "IL26-M24", "90-day roadmap: sequencing the work", "start",
    [
     ("start",
      "Day 1 of your 90-day plan: SQL is solid, Python is decent, statistics is shaky, and you have zero portfolio pieces. Certifications and applications both compete for time.",
      [("Apply to jobs immediately; you can learn on the job", "apply",
        "Applying without evidence burns first impressions you cannot remake."),
       ("Sequence: stats foundations, then portfolio proof, then targeted applications", "sequence",
        "Foundations, then proof, then applications: each phase funds the next."),
       ("Collect three certifications before applying anywhere", "certs",
        "Certificates without proof of work stall at the portfolio review.")]),
     ("sequence",
      "Day 30: statistics is functional and project one is underway. A recruiter asks for your portfolio link.",
      [("Send project one with a clear README, noting two more in progress", "end",
        "Honest momentum beats a finished facade."),
       ("Say the portfolio is coming soon", "end",
        "Soon without evidence is just a promise.")]),
     ("apply",
      "Two rejections cite lack of demonstrated analysis work.",
      [("Pause applications and build the proof", "sequence",
        "The market gave you the feedback; act on it."),
       ("Apply wider", "end",
        "Volume does not fix an evidence gap.")]),
     ("certs",
      "Day 60: three certificates, still no portfolio. Applications ask for work samples.",
      [("Convert cert projects into portfolio pieces now", "sequence",
        "Late but effective: proof over paper."),
       ("Add a fourth certificate", "end",
        "Diminishing returns accelerate from here.")]),
     ("end",
      "Debrief: sequence the 90 days so each phase funds the next: shore up the shakiest foundation, build proof of work, then apply with evidence. Certificates support the story; they are not the story.",
      [])
    ]))

CS = data["clickSims"]

# ---------- ClickSim: M27 Excel graphing ----------
CS.append(clicksim("click-il26-m27-graph", "IL26-M27", "Excel", "Graph f(x) = x^2 - 3x + 2 in Excel",
    [
     ("Blank workbook; columns A (x) and B (f(x)) are empty.",
      "Enter the x values 0 through 5 in cells A2:A7.",
      ["A2:A7", "cell A2"],
      "Values 0 through 5 entered in column A."),
     ("Column A holds 0-5; cell B2 is selected.",
      "In B2, enter =A2^2-3*A2+2 and fill down to B7.",
      ["formula bar", "B2"],
      "f(x) computed for every x; the y-values are 2, 0, 0, 2, 6, 12."),
     ("Range A2:B7 is selected.",
      "Insert a Scatter chart with smooth lines and markers.",
      ["Insert tab", "Scatter chart"],
      "Scatter chart inserted showing the parabola."),
     ("The chart shows the curve with a generic title.",
      "Add axis titles: x for the horizontal axis, f(x) for the vertical.",
      ["Chart Elements", "Axis Titles"],
      "Both axes labeled."),
     ("Axes are labeled; the title still reads Chart Title.",
      "Change the chart title to f(x) = x^2 - 3x + 2.",
      ["Chart Title"],
      "Title set; the chart is presentation-ready."),
     ("Finished, labeled chart.",
      "Verify visually that the curve crosses zero at x = 1 and x = 2.",
      ["data point at x=1", "data point at x=2"],
      "Roots confirmed at 1 and 2, matching the algebra.")
    ]))

# ---------- ClickSim: M15 Tableau ----------
CS.append(clicksim("click-il26-m15-tableau", "IL26-M15", "Tableau", "Build a sales trend view and dashboard",
    [
     ("Tableau start screen with the Connect pane.",
      "Connect to the retail_orders.csv text file.",
      ["Text file", "Connect pane"],
      "Connected; the data source preview appears."),
     ("Data Source page showing fields and sample rows.",
      "Click Sheet 1 to open a worksheet.",
      ["Sheet 1"],
      "Blank worksheet with Dimensions and Measures panes."),
     ("Blank worksheet.",
      "Drag Order Date to Columns and Sales to Rows.",
      ["Order Date", "Sales"],
      "A line chart of sales over time appears."),
     ("Single line chart of total sales.",
      "Drag Category onto Color on the Marks card.",
      ["Color", "Category"],
      "The line splits into one line per category."),
     ("Multi-line chart by category.",
      "Drag Order Date to the Filters shelf and keep only the last 12 months.",
      ["Filters shelf", "Order Date"],
      "View filtered to the trailing 12 months."),
     ("Filtered trend view.",
      "Rename the sheet Sales Trend, then open a new dashboard.",
      ["New Dashboard"],
      "Dashboard canvas is open."),
     ("Empty dashboard canvas.",
      "Drag the Sales Trend sheet onto the canvas and set Fit to Entire View.",
      ["Sales Trend", "Entire View"],
      "Dashboard assembled and fitted.")
    ]))

# ---------- ClickSim: M16a Excel pivot ----------
CS.append(clicksim("click-il26-m16a-pivot", "IL26-M16", "Excel", "Build a pivot table with a slicer",
    [
     ("Sales data in A1:D500: OrderID, Region, Category, Amount.",
      "Select any cell in the data and insert a PivotTable on a new worksheet.",
      ["Insert tab", "PivotTable"],
      "Empty PivotTable created on a new sheet."),
     ("PivotTable Fields pane is open.",
      "Drag Region into the Rows area.",
      ["Region", "Rows"],
      "Regions appear as row labels."),
     ("Rows show the four regions.",
      "Drag Category into the Columns area.",
      ["Category", "Columns"],
      "Category columns appear across the top."),
     ("The matrix scaffold is in place.",
      "Drag Amount into Values and confirm it aggregates as Sum of Amount.",
      ["Amount", "Values"],
      "Sums populate the matrix."),
     ("The pivot shows sums by region and category.",
      "Open Value Field Settings and show values as % of Grand Total.",
      ["Value Field Settings", "Show Values As"],
      "Cells now show percentages of the grand total."),
     ("Percent view is active.",
      "Insert a slicer on the Region field.",
      ["Insert Slicer", "Region"],
      "A Region slicer appears beside the pivot."),
     ("Slicer shows all regions selected.",
      "Click West in the slicer.",
      ["West"],
      "The pivot filters to West; percentages recompute.")
    ]))

# ---------- ClickSim: M16b Excel XLOOKUP + Power Query ----------
CS.append(clicksim("click-il26-m16b-xlookup", "IL26-M16", "Excel", "XLOOKUP pricing and a Power Query cleanup",
    [
     ("Sheet1 lists product IDs in column A; Sheet2 maps ID to price in A:B.",
      "In Sheet1 cell B2, begin an XLOOKUP for the ID in A2 against Sheet2.",
      ["formula bar", "B2"],
      "XLOOKUP started with the lookup value."),
     ("The formula is half-written.",
      "Complete it: =XLOOKUP(A2, Sheet2!A:A, Sheet2!B:B, \"Not found\").",
      ["formula bar"],
      "The lookup returns the price, or Not found for missing IDs."),
     ("Prices are filled down column B.",
      "Select the table and open Power Query via Data > From Table/Range.",
      ["Data tab", "From Table/Range"],
      "The Power Query editor opens with your table."),
     ("Power Query editor showing the loaded table.",
      "Remove the obsolete Discount column.",
      ["Discount column", "Remove Columns"],
      "The column is removed from the query."),
     ("Discount is gone.",
      "Change the Price column data type to Decimal Number.",
      ["Price column", "Data Type"],
      "Price is now a proper decimal type."),
     ("The query is clean.",
      "Choose Close & Load to output the result to a new worksheet.",
      ["Close & Load"],
      "The cleaned table loads to a new sheet.")
    ]))

# ---------- ClickSim: M02 Power BI ----------
CS.append(clicksim("click-il26-m02-powerbi", "IL26-M02", "Power BI", "From CSV to modeled visual",
    [
     ("Power BI Desktop start screen.",
      "Use Get Data to connect to the sales.csv text file.",
      ["Get Data", "Text/CSV"],
      "The Navigator preview appears."),
     ("Navigator preview of sales.csv.",
      "Choose Transform Data to open Power Query.",
      ["Transform Data"],
      "Power Query editor opens."),
     ("Power Query editor with the raw table.",
      "Remove blank rows and set the Amount column to Decimal Number.",
      ["Remove Rows", "Data Type"],
      "The query is cleaned."),
     ("Clean query, no errors.",
      "Click Close & Apply to load it into the model.",
      ["Close & Apply"],
      "Data loads; Report view opens."),
     ("Model view: Sales and Region tables sit unlinked.",
      "Drag Region[RegionID] onto Sales[RegionID] to create the relationship.",
      ["RegionID", "Model view"],
      "A one-to-many relationship is created."),
     ("The relationship line is active.",
      "In Report view, create a new measure: Total Sales = SUM(Sales[Amount]).",
      ["New measure", "formula bar"],
      "The measure appears in the Fields pane."),
     ("Total Sales is available.",
      "Build a clustered column chart with Region on the axis and Total Sales as values.",
      ["Clustered column chart", "Region"],
      "The visual renders revenue per region.")
    ]))

# ---------- ClickSim: M03 Tableau Top-N ----------
CS.append(clicksim("click-il26-m03-topn", "IL26-M03", "Tableau", "Top-N customers with a parameter",
    [
     ("Connected to the orders data source.",
      "Create an integer parameter named Top N, range 1 to 20, current value 10.",
      ["Create Parameter"],
      "The Top N parameter is created."),
     ("Parameter created.",
      "Build a bar chart: Customer on Rows, Sales on Columns, sorted descending.",
      ["Customer", "Sales", "Sort descending"],
      "Customers ranked by sales."),
     ("Ranked bar chart.",
      "Drag Customer to Filters, open the Top tab, and keep the Top N by sum of Sales using the parameter.",
      ["Top tab", "Top N"],
      "The view filters to the top 10 customers."),
     ("Top 10 customers shown.",
      "Right-click the parameter and show the parameter control.",
      ["Show Parameter"],
      "A slider control appears on the view."),
     ("Parameter control is visible.",
      "Set Top N to 5.",
      ["Top N control"],
      "The view updates to the top 5 customers."),
     ("Top 5 view.",
      "From the Analytics pane, add an average reference line for Sales.",
      ["Analytics pane", "Average Line"],
      "The reference line marks the average across the top 5.")
    ]))

# ---------- ClickSim: M21 Tableau dashboard ----------
CS.append(clicksim("click-il26-m21-portfolio", "IL26-M21", "Tableau", "Assemble a portfolio dashboard",
    [
     ("Workbook with three finished sheets: KPI Tiles, Trend, Breakdown.",
      "Open a new dashboard.",
      ["New Dashboard"],
      "A blank dashboard canvas opens."),
     ("Blank dashboard with default sizing.",
      "Set the dashboard Size to Automatic.",
      ["Size: Automatic"],
      "The dashboard will resize responsively."),
     ("Empty responsive canvas.",
      "Drag the KPI Tiles sheet to the top inside a horizontal layout container.",
      ["KPI Tiles", "Horizontal container"],
      "KPIs sit across the top."),
     ("KPIs placed.",
      "Add the Trend and Breakdown sheets side by side underneath.",
      ["Trend", "Breakdown"],
      "The three-part layout is complete."),
     ("Dashboard assembled but static.",
      "Add a dashboard filter action so selecting a category in Trend filters Breakdown.",
      ["Dashboard Actions", "Filter"],
      "Cross-filtering is wired between the sheets."),
     ("Interactive dashboard with filtering.",
      "Add a title and a caption text object noting the data refresh date.",
      ["Title", "Text object"],
      "The dashboard is titled, documented, and portfolio-ready.")
    ]))

# ---------- Interactivity audit ----------
ALL_MODULES = ["IL26-M26","IL26-M27","IL26-M28","IL26-M29","IL26-M30","IL26-M31",
               "IL26-M32","IL26-M33","IL26-M34","IL26-M08","IL26-M09","IL26-M10",
               "IL26-M11","IL26-M12","IL26-M13","IL26-M14","IL26-M15","IL26-M16",
               "IL26-M17","IL26-M18","IL26-M25","IL26-M01","IL26-M02","IL26-M03",
               "IL26-M04","IL26-M05","IL26-M06","IL26-M07","IL26-M35","IL26-M36",
               "IL26-M37","IL26-M38","IL26-M39","IL26-M40","IL26-M19","IL26-M20",
               "IL26-M21","IL26-M22","IL26-M23","IL26-M24"]

coverage = {m: [] for m in ALL_MODULES}
type_of = {}
for coll_name, coll in [("sqlPlayground", data["sqlPlaygrounds"]),
                        ("pythonExercise", data["pythonExercises"]),
                        ("daxPlayground", data["daxPlaygrounds"]),
                        ("terminalSim", data["terminalSims"]),
                        ("branchingScenario", data["branchingScenarios"]),
                        ("clickSim", data["clickSims"])]:
    for el in coll:
        coverage[el["moduleId"]].append(el["id"])
        type_of[el["id"]] = coll_name

audit = []
for m in ALL_MODULES:
    ids = coverage[m]
    audit.append({"moduleId": m, "elementCount": len(ids),
                  "elements": [{"id": i, "type": type_of[i]} for i in ids],
                  "gatePass": len(ids) >= 2})
data["interactivityAudit"] = audit

with open(OUT, "w") as f:
    json.dump(data, f, indent=1)

print("WROTE", OUT)
print("sqlPlaygrounds:", len(data["sqlPlaygrounds"]))
print("pythonExercises:", len(data["pythonExercises"]))
print("daxPlaygrounds:", len(data["daxPlaygrounds"]))
print("terminalSims:", len(data["terminalSims"]))
print("branchingScenarios:", len(data["branchingScenarios"]))
print("clickSims:", len(data["clickSims"]))
total = sum(len(data[k]) for k in ["sqlPlaygrounds","pythonExercises","daxPlaygrounds","terminalSims","branchingScenarios","clickSims"])
print("TOTAL elements:", total)
failing = [a for a in audit if not a["gatePass"]]
print("modules failing >=2 gate:", failing if failing else "NONE")

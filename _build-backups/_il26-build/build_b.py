# Batch B: IL-26 M34 + cert-domain modules M01-M07 (original content)
import json, os
from collections import Counter
OUT = os.path.expanduser("~/workspace/apex-audit/docs/university/data/courses/_il26-build")

def check(mods):
    for m in mods:
        p = m["patch"]
        assert len(p["objectives"]) >= 4, m["id"]
        assert len(p["notes"]) >= 5, (m["id"], "notes")
        for n in p["notes"]:
            assert "```" in n["body"], (m["id"], n["title"])
        assert len(p["cards"]) >= 8, m["id"]
        q = p["quiz"]; assert len(q) >= 8, m["id"]
        c = Counter(x["answer"] for x in q)
        assert dict(c) == {0:2,1:2,2:2,3:2}, (m["id"], dict(c))
        for qi in q:
            assert len(qi["choices"]) == 4 and "explain" in qi and 0 <= qi["answer"] <= 3
        for dr in p["drills"]:
            assert len(dr["items"]) >= 5
        hl = p["handsOnLab"]
        assert len(hl["steps"]) >= 4 and hl["deliverable"] and hl["checkpoint"]
        assert len(p["mockTask"]["choices"]) == 4
        assert p["videoPlaceholders"] is False, m["id"]
    return True

MODULES = []

M34 = {"id": "IL26-M34", "patch": {
 "objectives": [
  "Explain limits, derivatives, and integrals in plain language and connect each to an analyst task (rates, marginal effects, cumulative totals).",
  "Compute derivatives of polynomial, exponential, and logarithmic functions and interpret them as marginal rates of change.",
  "Set up and solve single-variable optimization problems (profit maximization, cost minimization) using first- and second-derivative tests.",
  "Interpret integrals as accumulation and partial derivatives as ceteris-paribus effects in multi-variable business models."],
 "notes": [
  {"title": "Limits: approaching, not touching",
   "body": "A limit describes the value a function approaches as x approaches a point. Continuity means the limit equals the function value — no jumps. Analyst relevance: limits justify every 'instantaneous rate' and every smooth curve fit; a discontinuity in data (a step change) is a regime break, not noise.\n\nWorked example (with solution):\n```text\nlim_{x->2} (x^2 - 4)/(x - 2): direct substitution gives 0/0 (undefined).\nFactor: (x-2)(x+2)/(x-2) = x + 2 for x != 2.\nLimit as x->2: 2 + 2 = 4.\nThe function has a HOLE at x=2 (value 4 approached but never attained).\nAnalyst read: a KPI formula that divides by (x - target) blows up AT the target\nbut is well-behaved near it — handle the edge case explicitly in code.\n```"},
  {"title": "Derivatives: the marginal-everything machine",
   "body": "f'(x) = lim_{h->0} [f(x+h) - f(x)]/h: the instantaneous rate of change, the slope of the tangent. Power rule: d/dx x^n = n*x^(n-1). d/dx e^x = e^x. d/dx ln(x) = 1/x. Marginal cost, marginal revenue, and gradient descent all live here.\n\nWorked example (with solution):\n```python\n# Revenue R(q) = 100q - 2q^2 (q in hundreds of units).\n# Marginal revenue R'(q) = 100 - 4q.\n# At q = 10: MR = 100 - 40 = 60 -> the 11th hundred units adds ~$60.\n# At q = 25: MR = 100 - 100 = 0 -> revenue peaks here.\n# At q = 30: MR = -20 -> selling MORE reduces revenue (price effect dominates).\ndef marginal_revenue(q): return 100 - 4*q\nfor q in (10, 25, 30): print(q, marginal_revenue(q))\n```"},
  {"title": "Optimization: where the derivative is zero",
   "body": "Maxima/minima of a smooth function occur where f'(x) = 0 (critical points). Second-derivative test: f''(x) < 0 -> maximum; f''(x) > 0 -> minimum. Every 'find the best price/spend/bid' problem is this.\n\nWorked example (with solution):\n```text\nProfit P(x) = -2x^2 + 80x - 100 (x = ad spend in $K).\nP'(x) = -4x + 80 = 0 -> x = 20.\nP''(x) = -4 < 0 -> MAXIMUM at x = 20 ($20K spend).\nP(20) = -2(400) + 1600 - 100 = 700 -> $700K max profit.\nEndpoints check: P(0) = -100, P(40) = -100. Interior max confirmed.\nLesson: the optimal spend is where MARGINAL profit hits zero, not where total looks big.\n```"},
  {"title": "Integrals: adding up the small pieces",
   "body": "The definite integral is accumulation: total = integral of rate over time. Integral of marginal cost = total cost. Area under a demand curve = total revenue. The Fundamental Theorem links the two: integration undoes differentiation.\n\nWorked example (with solution):\n```python\n# Signup rate r(t) = 50 + 10t signups/day over 30 days. Total signups?\n# Integral of (50 + 10t) dt from 0 to 30 = 50t + 5t^2 evaluated 0..30.\ntotal = 50*30 + 5*30**2\nprint(total)  # 6000 signups\n# Discrete check: sum(50 + 10t for t in range(30)) = 5850 (left-endpoint sum\n# slightly undercounts; the integral is the continuous truth).\n# Analyst use: converting a rate dashboard into a cumulative total.\n```"},
  {"title": "Partial derivatives: holding everything else equal",
   "body": "For f(x,y), partial df/dx treats y as constant: the ceteris-paribus effect of x. The gradient is the vector of partials — it points in the direction of steepest increase. This is the entire vocabulary of 'controlling for' variables and of gradient-based optimization.\n\nWorked example (with solution):\n```text\nRevenue model R(p, a) = 1000p - 5p^2 + 20a - 0.5a^2 + 0.1pa\n(p = price, a = ad spend).\nPartial w.r.t. price: dR/dp = 1000 - 10p + 0.1a.\nPartial w.r.t. ads:   dR/da = 20 - a + 0.1p.\nAt p=50, a=10: dR/dp = 1000 - 500 + 1 = 501 (raise price!);\ndR/da = 20 - 10 + 5 = 15 (more ads help too).\nThe interaction term 0.1pa means ads make price increases MORE effective:\npartials expose interactions that single-variable thinking misses.\n```"}],
 "cards": [
  {"front": "lim_{x->2} (x^2-4)/(x-2) = ?", "back": "4 (factor to x+2; hole at x=2)."},
  {"front": "Derivative of x^n, e^x, ln(x)?", "back": "n*x^(n-1); e^x; 1/x."},
  {"front": "R(q) = 100q - 2q^2. Marginal revenue at q=10?", "back": "R'(q) = 100-4q; at 10: 60."},
  {"front": "Second-derivative test.", "back": "f''<0 at critical point -> max; f''>0 -> min."},
  {"front": "Maximize P(x) = -2x^2 + 80x - 100.", "back": "x=20 ($20K spend), P=700 ($700K)."},
  {"front": "Signup rate 50+10t/day for 30 days. Total?", "back": "Integral: 50*30 + 5*900 = 6,000."},
  {"front": "What is a partial derivative, in business words?", "back": "The effect of one variable holding all others constant — 'controlling for' in math form."},
  {"front": "What does the gradient point to?", "back": "The direction of steepest increase of the function."}],
 "quiz": [
  {"q": "lim_{x->3} (x^2 - 9)/(x - 3) = ?", "choices": ["6", "0", "Undefined", "9"], "answer": 0, "explain": "Factor: (x-3)(x+3)/(x-3) = x+3 -> 6."},
  {"q": "d/dx (4x^3 - 2x + 7)?", "choices": ["12x^2 + 7", "4x^2 - 2", "12x^3 - 2x", "12x^2 - 2"], "answer": 3, "explain": "Power rule term by term: 12x^2 - 2 + 0."},
  {"q": "R(q) = 100q - 2q^2. At what q does marginal revenue hit zero?", "choices": ["q = 50", "q = 25", "q = 20", "q = 100"], "answer": 1, "explain": "MR = 100 - 4q = 0 -> q = 25 (the revenue peak)."},
  {"q": "Maximize P(x) = -x^2 + 40x - 300.", "choices": ["x = 40", "x = 10", "x = 20", "x = 30"], "answer": 2, "explain": "P' = -2x + 40 = 0 -> x = 20; P'' = -2 < 0 confirms max."},
  {"q": "Integral of rate (50 + 10t) from t=0 to 30?", "choices": ["5,850", "6,000", "1,500", "4,500"], "answer": 1, "explain": "50t + 5t^2 from 0 to 30 = 1500 + 4500 = 6,000."},
  {"q": "R(p,a) = 1000p - 5p^2 + 20a - 0.5a^2 + 0.1pa. dR/dp?", "choices": ["1000 - 10p + 0.1a", "1000 - 5p + 0.1a", "20 - a + 0.1p", "1000 - 10p"], "answer": 0, "explain": "Differentiate term by term treating a as constant: 1000 - 10p + 0.1a."},
  {"q": "d/dx ln(5x)?", "choices": ["5/x", "ln 5", "1/(5x)", "1/x"], "answer": 3, "explain": "ln(5x) = ln5 + ln x; derivative = 1/x."},
  {"q": "A profit function has P'(20)=0 and P''(20)=5. What is x=20?", "choices": ["A maximum.", "An inflection point.", "A minimum.", "A discontinuity."], "answer": 2, "explain": "P''>0 means convex there -> local minimum."},],
 "drills": [{"id": "il26-m34-calc", "title": "Calculus drills", "items": [
   {"prompt": "d/dx x^5 = ?", "answer": "5x^4", "explain": "Power rule."},
   {"prompt": "d/dx e^(2x) = ?", "answer": "2e^(2x)", "explain": "Chain rule: outer derivative times inner (2)."},
   {"prompt": "Critical point of f(x) = x^2 - 6x + 5?", "answer": "x = 3 (minimum)", "explain": "f' = 2x-6 = 0 -> x=3; f''=2>0."},
   {"prompt": "Integral of 3x^2 dx?", "answer": "x^3 + C", "explain": "Reverse power rule."},
   {"prompt": "lim_{x->0} sin(x)/x (famous limit)?", "answer": "1", "explain": "Standard result; foundation of trig derivatives."},
   {"prompt": "d/dx (x^2 * ln x)?", "answer": "2x ln x + x", "explain": "Product rule: 2x*lnx + x^2*(1/x)."}]}],
 "handsOnLab": {"id": "il26-m34-lab", "title": "Marginal profit optimizer", "brief": "Fit a quadratic profit model to spend/profit data, derive the optimal spend analytically, and verify it numerically.",
  "steps": ["Fit P(x) = ax^2 + bx + c to the provided spend/profit points (least squares).", "Compute P'(x) and solve for the critical point by hand.", "Apply the second-derivative test and check endpoints.", "Verify by grid search over spend values.", "Write the recommendation: optimal spend, expected profit, and what the model assumes."],
  "deliverable": "Fitted model, analytic optimum with tests, grid-search verification, recommendation memo.",
  "checkpoint": "Analytic optimum and grid search agree; the memo states the quadratic assumption's limits."},
 "mockTask": {"id": "il26-m34-mock", "type": "choice", "q": "Marginal profit at current spend is positive but shrinking. What should spend do?", "choices": ["Cut spend immediately.", "Hold spend flat.", "Increase spend while marginal profit stays positive; the optimum is where it hits zero.", "Double spend."], "answer": 2, "explain": "Positive marginal profit means the next dollar still earns; keep increasing until the margin hits zero — that is the optimum, not an arbitrary multiple."},
 "crossLinks": [{"course": "il-20-mathematics", "moduleId": "m20-calculus-1", "topic": "Calculus I - limits & derivatives", "why": "IL-20 teaches the formal calculus; this module extracts the analyst intuition."}],
 "videoPlaceholders": False}}

M01 = {"id": "IL26-M01", "patch": {
 "objectives": [
  "Map the Google Data Analytics certificate's eight courses to the underlying skill domains (spreadsheets, SQL, R, Tableau, case study) and sequence them into a study schedule.",
  "Explain how each certificate domain maps to day-one junior analyst tasks, and where the certificate's coverage ends (statistics depth, production SQL, stakeholder management).",
  "Build a study system for the certificate: notes, flashcards, and a capstone-aligned project that converts coursework into portfolio evidence.",
  "Identify the certificate's known assessment patterns and prepare for them with targeted drills rather than passive rewatching."],
 "notes": [
  {"title": "The certificate's architecture: eight courses, five skills",
   "body": "The Google Data Analytics Professional Certificate runs eight courses: Foundations, Ask, Prepare, Process, Analyze, Share, and a Capstone. Underneath, five skills repeat: spreadsheets/Sheets, SQL (BigQuery), R programming, Tableau, and structured problem-solving. The through-line is the data analysis process: Ask -> Prepare -> Process -> Analyze -> Share -> Act.\n\nWorked example (with solution):\n```text\nCourse-to-skill map (study triage):\nFoundations + Ask      -> business understanding, data life cycle, fairness\nPrepare + Process      -> spreadsheets, SQL basics, data cleaning, BigQuery\nAnalyze                -> R programming, dplyr-style wrangling, visualization\nShare                  -> Tableau dashboards, storytelling, presentation\nCapstone               -> end-to-end case study (your portfolio seed)\nStudy rule: weight time toward Process/Analyze/Share (tool skills compound);\nskim Foundations/Ask once (concepts, not mechanics).\n```\nNote: this is independent study guidance, not affiliated with Google; course names and structure change — verify against the current program page."},
  {"title": "Spreadsheets to SQL: the certificate's tool ladder",
   "body": "The program teaches cleaning first in Sheets (filters, pivot tables, VLOOKUP/XLOOKUP) then the same ideas in SQL. Treat every spreadsheet operation as a SQL operation in waiting: filter = WHERE, pivot = GROUP BY, VLOOKUP = JOIN. Learning both mappings is what makes the certificate stick.\n\nWorked example (with solution):\n```sql\n-- 'Pivot table: average revenue by region' in Sheets becomes:\nSELECT region, AVG(revenue) AS avg_revenue, COUNT(*) AS orders\nFROM sales\nGROUP BY region\nORDER BY avg_revenue DESC;\n-- 'VLOOKUP customer name' becomes:\nSELECT o.order_id, c.customer_name\nFROM orders o JOIN customers c ON o.customer_id = c.customer_id;\n```\nDrill: for every Sheets skill you practice, write the SQL equivalent the same day."},
  {"title": "R for the certificate: what to actually learn",
   "body": "The certificate's R portion centers on the tidyverse: readr/dplyr for wrangling, ggplot2 for visualization, RMarkdown for reporting. You do not need all of R — you need filter/select/mutate/summarize/arrange, joins, and ggplot's layered grammar, applied to the Analyze course datasets.\n\nWorked example (with solution):\n```r\n# The certificate's canonical R pattern: clean, summarize, plot.\nlibrary(dplyr); library(ggplot2)\nsummary <- bookings %>%\n  filter(!is.na(lead_time)) %>%\n  group_by(hotel) %>%\n  summarise(avg_lead = mean(lead_time), n = n(), .groups = \"drop\")\nggplot(summary, aes(x = hotel, y = avg_lead, fill = hotel)) +\n  geom_col() + labs(title = \"Average lead time by hotel\")\n# This single pattern answers most 'Analyze' course exercises.\n```"},
  {"title": "Tableau and the Share course: dashboards that communicate",
   "body": "The Share course's Tableau work rewards dashboard hygiene: one message per dashboard, sorted bars, labeled axes, filters that answer 'compared to what'. The certificate's Tableau depth is introductory — real mastery comes from rebuilding the course dashboards with your own data and defending each design choice.\n\nWorked example (with solution):\n```text\nDashboard rubric (apply to every Share-course dashboard you build):\n1. Title states the takeaway, not the topic ('Churn concentrates in month 2', not 'Churn dashboard').\n2. Every chart has a comparison (prior period, target, benchmark).\n3. Filters expose the stakeholder's next question, not every possible slice.\n4. No 3D, no pie charts with >4 slices, no dual axes without justification.\nRebuild one course dashboard against this rubric: that rebuild IS the learning.\n```"},
  {"title": "Where the certificate ends: the gap plan",
   "body": "The certificate under-covers: inferential statistics (it is descriptive-heavy), production SQL (window functions are light), Python/pandas (R only), and stakeholder management. The senior track fills these gaps — schedule them explicitly rather than discovering them in interviews.\n\nWorked example (with solution):\n```text\nGap-closure plan (post-certificate, 4 weeks):\nWeek 1: Window functions + CTEs in SQL (the certificate's SQL stops early).\nWeek 2: pandas equivalents of every dplyr verb you learned (bilingual analyst).\nWeek 3: Hypothesis testing basics (the certificate barely touches inference).\nWeek 4: One stakeholder-facing case study writeup (the certificate's capstone\n        is technical; employers hire for the communication layer).\nEach week ends with a portfolio artifact, not just notes.\n```"}],
 "cards": [
  {"front": "The six phases of the data analysis process taught in the certificate?", "back": "Ask, Prepare, Process, Analyze, Share, Act."},
  {"front": "Sheets pivot table -> SQL equivalent?", "back": "GROUP BY with aggregates (AVG/SUM/COUNT)."},
  {"front": "Sheets VLOOKUP -> SQL equivalent?", "back": "JOIN on the key."},
  {"front": "The three core tidyverse verbs for the certificate's R portion?", "back": "dplyr wrangling (filter/select/mutate/summarise), ggplot2 visualization, RMarkdown reporting."},
  {"front": "Dashboard rubric rule #1?", "back": "Title states the takeaway, not the topic."},
  {"front": "Four gaps the certificate under-covers?", "back": "Inferential statistics, production SQL (windows/CTEs), Python/pandas, stakeholder management."},
  {"front": "Which certificate courses carry the most tool-skill weight?", "back": "Prepare, Process, Analyze, Share — weight study time there."},
  {"front": "What turns the capstone into portfolio evidence?", "back": "Rebuilding it with your own data + a stakeholder-facing writeup, not just the graded submission."}],
 "quiz": [
  {"q": "The certificate's data analysis process phases are:", "choices": ["Ask, Prepare, Process, Analyze, Share, Act", "Collect, Clean, Model, Deploy", "Plan, Do, Check, Act", "Extract, Transform, Load, Serve"], "answer": 0, "explain": "The program's through-line is Ask -> Prepare -> Process -> Analyze -> Share -> Act."},
  {"q": "A Sheets pivot table showing average revenue by region becomes which SQL?", "choices": ["SELECT with WHERE only", "SELECT region, AVG(revenue) ... GROUP BY region", "SELECT DISTINCT region", "ORDER BY revenue"], "answer": 1, "explain": "Pivots are GROUP BY aggregations; the row labels become the GROUP BY keys."},
  {"q": "In the certificate's R track, ggplot2 is used for:", "choices": ["Database connections", "Statistical modeling only", "Reading CSVs", "Visualization with a layered grammar"], "answer": 3, "explain": "ggplot2 builds plots layer by layer (data, aesthetics, geometries)."},
  {"q": "Best dashboard title under the Share-course rubric?", "choices": ["'Churn dashboard'", "'Q3 metrics'", "'Churn concentrates in month 2 — onboarding is the leak'", "'Data overview'"], "answer": 2, "explain": "Titles should state the takeaway, not the topic."},
  {"q": "Which skill does the certificate under-cover relative to senior analyst roles?", "choices": ["Spreadsheets", "Tableau basics", "Inferential statistics", "Data cleaning"], "answer": 2, "explain": "The program is descriptive-heavy; hypothesis testing and inference need separate study."},
  {"q": "VLOOKUP in Sheets maps to which SQL operation?", "choices": ["JOIN", "UNION", "GROUP BY", "ORDER BY"], "answer": 0, "explain": "Looking up values by key across tables is a join."},
  {"q": "The capstone course's main portfolio value is:", "choices": ["The certificate badge itself", "Learning R syntax", "The discussion forums", "An end-to-end case study you can rebuild with your own data and write up for stakeholders"], "answer": 3, "explain": "Employers evaluate the artifact and the communication, not the badge."},
  {"q": "Which courses deserve the most study time?", "choices": ["Foundations and Ask", "Prepare, Process, Analyze, Share", "Only the Capstone", "Foundations only"], "answer": 1, "explain": "Tool skills compound; skim the concept courses once and drill the tool courses."}],
 "drills": [{"id": "il26-m01-gda", "title": "Certificate domain drills", "items": [
   {"prompt": "Name the six phases of the analysis process in order.", "answer": "Ask, Prepare, Process, Analyze, Share, Act", "explain": "The certificate's through-line."},
   {"prompt": "Sheets FILTER -> SQL?", "answer": "WHERE", "explain": "Row filtering is WHERE."},
   {"prompt": "dplyr verb for row filtering?", "answer": "filter()", "explain": "filter() keeps rows matching conditions."},
   {"prompt": "dplyr verb for grouped summaries?", "answer": "group_by() + summarise()", "explain": "The pivot-table equivalent."},
   {"prompt": "ggplot2 geometry for bars?", "answer": "geom_col() / geom_bar()", "explain": "geom_col for precomputed heights, geom_bar for counts."},
   {"prompt": "One gap to close after the certificate?", "answer": "Any of: inferential stats, window functions/CTEs, pandas, stakeholder communication", "explain": "The four documented gaps."}]}],
 "handsOnLab": {"id": "il26-m01-lab", "title": "Certificate study system build", "brief": "Build your study tracker for the certificate: course-by-course checklist, the Sheets-to-SQL translation drill set, and the capstone portfolio plan.",
  "steps": ["List all eight courses with their skill focus and your target completion dates.", "Create the Sheets-to-SQL translation drill sheet (15 operations with both versions).", "Do the dplyr-to-pandas verb map for the Analyze course.", "Rebuild one Share-course dashboard against the 4-rule rubric with your own dataset.", "Write the gap-closure plan with weekly portfolio artifacts."],
  "deliverable": "Study tracker, translation drill sheet, rebuilt dashboard, gap-closure plan.",
  "checkpoint": "Every Sheets operation has a verified SQL equivalent; the rebuilt dashboard passes all 4 rubric rules."},
 "mockTask": {"id": "il26-m01-mock", "type": "choice", "q": "You finished the Google certificate. A job post asks for 'production SQL and A/B testing.' What is the right move?", "choices": ["Apply claiming the certificate covers it.", "Close the two gaps first (window functions/CTEs + hypothesis testing) with portfolio artifacts, then apply citing the artifacts.", "Get another beginner certificate.", "Skip the post."], "answer": 1, "explain": "Certificates open doors; artifacts close them. Two focused weeks of gap work with evidence beats another badge."},
 "crossLinks": [],
 "videoPlaceholders": False}}

MODULES += [M34, M01]

M02 = {"id": "IL26-M02", "patch": {
 "objectives": [
  "Name the PL-300 exam's four domains (prepare, model, visualize/analyze, deploy/maintain) and allocate study time by domain weight.",
  "Build a Power BI data model from raw tables: clean in Power Query, define relationships, and write correct DAX measures.",
  "Choose the right visual and DAX pattern for common business questions, and explain row context vs filter context in plain language.",
  "Prepare for the exam's scenario style: read a business requirement, pick the compliant Power BI implementation, and justify it."],
 "notes": [
  {"title": "The four domains and how to weight them",
   "body": "PL-300 (Microsoft Power BI Data Analyst) tests four areas: Prepare the data, Model the data, Visualize and analyze the data, and Deploy and maintain deliverables. Microsoft publishes the current weights in the skills outline — they shift between revisions, so verify before scheduling. The durable pattern: modeling (relationships + DAX) is the highest-leverage domain because every other domain depends on a correct model.\n\nWorked example (with solution):\n```text\nStudy-time allocation (10-week plan, ~8 hrs/week = 80 hrs):\nPrepare (Power Query, data profiling) ......... 20 hrs\nModel (relationships, DAX, row/filter context) 30 hrs  <- the multiplier\nVisualize (visual choice, interactions) ........ 20 hrs\nDeploy/maintain (workspaces, refresh, RLS) .... 10 hrs\nWhy: a broken model makes every visual wrong; DAX fluency is the exam's\ncenter of gravity. Adjust to the current published weights.\n```\nIndependent study material; not affiliated with Microsoft."},
  {"title": "Prepare: Power Query done right",
   "body": "Power Query (M language) is where data gets shaped before the model: remove errors, fix types, unpivot, merge queries. Golden rules: fix data types at the source step, filter early to reduce refresh cost, and never hard-code values that belong in parameters.\n\nWorked example (with solution):\n```text\nMessy sales extract: dates as text, 'N/A' in revenue, region names inconsistent.\nPower Query steps (in order):\n1. Replace 'N/A' with null in revenue (errors become nulls, not crashes).\n2. Change type: date column -> Date, revenue -> Decimal Number.\n3. Trim + Proper-case the region column (standardize 'north', 'NORTH ' -> 'North').\n4. Filter out rows where date is null BEFORE any merge (smaller = faster refresh).\n5. Reference (not duplicate) this query for downstream transformations.\nEach step is recorded in M: re-runnable, auditable, refresh-safe.\n```"},
  {"title": "Model: relationships and star schemas",
   "body": "Build star schemas: one fact table (measurements, e.g., sales) surrounded by dimension tables (date, product, customer). Single-direction filtering from dimensions to facts. Avoid bi-directional relationships except for well-understood patterns — they create ambiguous filter paths that produce wrong totals.\n\nWorked example (with solution):\n```text\nModel: FactSales (one row per line item) -> DimDate, DimProduct, DimCustomer.\nRelationships: DimDate[Date] -> FactSales[OrderDate] (1:many, single direction).\nWhy star: filter context flows Dim -> Fact cleanly; a matrix of\n[Month] x [Category] with SUM(Sales[Amount]) just works.\nAnti-pattern: snowflaking DimProduct -> DimCategory -> DimSubcategory chains\nadds ambiguity; denormalize into one DimProduct unless the exam scenario\ndemands the snowflake for a stated reason.\n```"},
  {"title": "DAX: row context vs filter context",
   "body": "DAX has two evaluation contexts. Row context: 'for this row' (calculated columns, iterators like SUMX). Filter context: 'for this filter combination' (measures in visuals). CALCULATE modifies filter context — it is the most-tested function on the exam because context transition (row -> filter) is where measures break.\n\nWorked example (with solution):\n```dax\n-- Total sales ignoring the visual's filters:\nTotal Sales All = CALCULATE(SUM(FactSales[Amount]), ALL(DimDate))\n-- Year-over-year growth (needs a proper date table):\nSales YoY % =\nDIVIDE(\n    SUM(FactSales[Amount]) - CALCULATE(SUM(FactSales[Amount]), SAMEPERIODLASTYEAR(DimDate[Date])),\n    CALCULATE(SUM(FactSales[Amount]), SAMEPERIODLASTYEAR(DimDate[Date]))\n)\n-- Why DIVIDE: returns BLANK instead of erroring on divide-by-zero.\n-- Context transition trap: referencing a column inside CALCULATE without an\n-- aggregator silently uses row context -> wrong totals in matrices.\n```"},
  {"title": "Visualize, deploy, and exam-day tactics",
   "body": "Choose visuals by question type: comparison = bar, trend = line, composition = stacked bar (small N) or treemap, distribution = histogram. Deployment: workspaces, scheduled refresh, row-level security (RLS) with DAX filters on roles, and sensitivity labels. Exam scenarios reward the compliant, maintainable answer over the clever one.\n\nWorked example (with solution):\n```text\nScenario: 'Regional managers must see only their region's data in the same report.'\nCorrect: ONE dataset + RLS role per region (DAX filter DimRegion[Region] = USERPRINCIPALNAME()-mapped value), published once.\nWrong: four copies of the report (maintenance nightmare), or slicer-only\n'filtering' (users can remove slicers; not security).\nExam-day tactic: for each scenario, first name the CONSTRAINT (security? refresh?\nscale?), then pick the feature that satisfies it. The constraint names the answer.\n```"}],
 "cards": [
  {"front": "PL-300's four domains?", "back": "Prepare the data; Model the data; Visualize and analyze the data; Deploy and maintain deliverables."},
  {"front": "Which domain is the highest-leverage and why?", "back": "Modeling (relationships + DAX): every visual depends on a correct model."},
  {"front": "Power Query golden rules (3)?", "back": "Fix types at source; filter early; never hard-code values that belong in parameters."},
  {"front": "Star schema in one sentence?", "back": "One fact table of measurements surrounded by dimension tables, single-direction filtering."},
  {"front": "Row context vs filter context?", "back": "Row: 'for this row' (calculated columns, iterators). Filter: 'for this filter combo' (measures in visuals)."},
  {"front": "What does CALCULATE do?", "back": "Modifies filter context — the most-tested DAX function."},
  {"front": "Why use DIVIDE instead of /?", "back": "DIVIDE returns BLANK on divide-by-zero instead of erroring."},
  {"front": "Regional managers, one report, each sees only their region: correct approach?", "back": "One dataset + RLS roles with DAX filters; not report copies or slicer-only filtering."}],
 "quiz": [
  {"q": "Which PL-300 domain carries the highest study leverage?", "choices": ["Deploy and maintain", "Visualize", "Model the data (relationships + DAX)", "Prepare"], "answer": 2, "explain": "Every visual and measure depends on a correct model; DAX fluency is the exam's center of gravity."},
  {"q": "In Power Query, the correct first fixes for a messy extract are:", "choices": ["Replace error values with null, fix data types at the source step, standardize text", "Load everything then fix in DAX", "Delete all nulls immediately", "Merge first, clean later"], "answer": 0, "explain": "Clean at the source step: nulls over errors, correct types early, standardized text."},
  {"q": "A matrix shows wrong totals for a CALCULATE measure referencing a bare column. Likely cause?", "choices": ["Too many visuals", "Row context used where filter context was needed (missing aggregator)", "Wrong color theme", "Dataset too large"], "answer": 1, "explain": "Bare column references inside CALCULATE use row context; totals need an aggregator or explicit filter."},
  {"q": "SAMEPERIODLASTYEAR requires:", "choices": ["A proper date table", "A bar chart", "DirectQuery mode", "A calculated column"], "answer": 3, "explain": "Time-intelligence functions require a contiguous, marked date table."},
  {"q": "Best visual for a monthly trend?", "choices": ["Line chart", "Pie chart", "Donut", "Treemap"], "answer": 0, "explain": "Trends over time = line chart; pies/donuts show composition, not change."},
  {"q": "RLS (row-level security) is implemented with:", "choices": ["Slicers", "Bookmarks", "DAX filter expressions on roles", "Report copies per user"], "answer": 2, "explain": "RLS roles carry DAX filters enforced by the engine; slicers are not security."},
  {"q": "Bi-directional relationships should be:", "choices": ["Used everywhere", "Avoided except for well-understood patterns — they create ambiguous filter paths", "Never mentioned", "The default"], "answer": 1, "explain": "Bi-di filtering can create ambiguity and wrong totals; single-direction is the safe default."},
  {"q": "DIVIDE(SUM(Sales), COUNTROWS(Table)) vs SUM/COUNTROWS: the difference?", "choices": ["None", "DIVIDE returns BLANK on divide-by-zero instead of erroring", "DIVIDE is slower", "DIVIDE only works in DirectQuery"], "answer": 3, "explain": "DIVIDE's alternate-result handling keeps visuals clean when denominators are zero/blank."}],
 "drills": [{"id": "il26-m02-pl300", "title": "PL-300 concept drills", "items": [
   {"prompt": "Function that modifies filter context?", "answer": "CALCULATE", "explain": "The core DAX context-manipulation function."},
   {"prompt": "Iterator that sums an expression row by row?", "answer": "SUMX", "explain": "SUMX(table, expression): row context per row."},
   {"prompt": "Star schema: fact table holds what?", "answer": "Measurements/metrics (e.g., sales amounts)", "explain": "Facts = measurable events; dimensions = descriptors."},
   {"prompt": "M is the language of?", "answer": "Power Query", "explain": "M records each transformation step."},
   {"prompt": "ALL() inside CALCULATE does what?", "answer": "Removes filters from the specified table/column", "explain": "ALL(DimDate) ignores date filters in the visual."},
   {"prompt": "RLS stands for and enforces what?", "answer": "Row-level security: which rows a user can see", "explain": "Engine-enforced via role DAX filters."}]}],
 "handsOnLab": {"id": "il26-m02-lab", "title": "End-to-end Power BI build", "brief": "Build a complete Power BI report from a messy CSV: Power Query cleaning, star schema, DAX measures, visuals, and RLS.",
  "steps": ["Clean the sales CSV in Power Query (types, nulls, text standardization, date table).", "Model a star schema with single-direction relationships.", "Write measures: Total Sales, Sales YoY %, and one CALCULATE/ALL measure.", "Build a 3-visual page: trend line, bar comparison, KPI cards — titles state takeaways.", "Implement one RLS role and verify it filters correctly as a test user."],
  "deliverable": "Published .pbix with clean model, 3 DAX measures, takeaway-titled visuals, working RLS.",
  "checkpoint": "YoY % matches a hand computation for one month; RLS test user sees only their region."},
 "mockTask": {"id": "il26-m02-mock", "type": "choice", "q": "Scenario: executives want one sales report; each regional VP must see only their region, and the data refreshes nightly. What do you implement?", "choices": ["Four separate reports, one per region.", "One dataset with RLS roles + scheduled refresh, published once to a shared workspace.", "One report with a region slicer; trust VPs not to clear it.", "Email static PDFs nightly."], "answer": 1, "explain": "RLS enforces the security at the engine level (slicers don't), one dataset avoids maintenance drift, and scheduled refresh meets the nightly requirement."},
 "crossLinks": [],
 "videoPlaceholders": False}}

M03 = {"id": "IL26-M03", "patch": {
 "objectives": [
  "Map the Tableau Certified Data Analyst exam's domains and connect each to hands-on Tableau skills (connections, calculations, dashboards).",
  "Connect to and prepare data in Tableau: joins, unions, blends vs relationships, and data interpreter use.",
  "Write Tableau calculations (LOD expressions, table calculations, parameters) and predict their results before running.",
  "Design exam-grade dashboards and stories that follow visual best practices and answer the business question directly."],
 "notes": [
  {"title": "Exam domains and the Tableau way of thinking",
   "body": "The Tableau Certified Data Analyst exam centers on: connecting to and preparing data, exploring and analyzing data, and sharing insights (plus Tableau concepts). The Tableau mindset: drag-and-drop builds queries visually, but every shelf placement is a SQL GROUP BY/aggregation decision. Verify current domain weights in the official exam guide — they are revised periodically.\n\nWorked example (with solution):\n```text\nShelf-to-SQL translation (the exam's hidden curriculum):\nRows: [Region] + Columns: [Category], Text: SUM(Sales)\n= SELECT region, category, SUM(sales) FROM data GROUP BY region, category.\nEvery pill placement answers: 'what am I grouping by, and what am I measuring?'\nExam tactic: before answering a scenario, translate the requested view into\nits GROUP BY. The right pills follow.\n```\nIndependent study material; not affiliated with Salesforce/Tableau."},
  {"title": "Connections: joins, unions, blends, relationships",
   "body": "Joins combine tables side-by-side on keys; unions stack tables with matching columns. Tableau's logical layer uses relationships (flexible, context-aware joins); blends combine separate data sources at the aggregate level. The exam tests when each is correct.\n\nWorked example (with solution):\n```text\nScenario: orders table + returns table (different granularity), plus a\nseparate Excel of regional targets.\n- Orders LEFT JOIN returns on order_id: same logical table, row-level keys match.\n- 2024 sales UNION 2025 sales: same columns, stacked years.\n- Regional targets: BLEND (secondary source) at Region granularity, because\n  targets exist only at region level, not order level.\nRule: join when keys align row-for-row; blend when granularities differ.\n```"},
  {"title": "Calculations: row-level, aggregate, LOD, table calcs",
   "body": "Row-level calcs evaluate per row. Aggregate calcs (SUM, AVG) respect the view's grouping. LOD expressions ({FIXED}, {INCLUDE}, {EXCLUDE}) compute at a declared granularity regardless of the view. Table calculations (RUNNING_SUM, RANK) compute across the viz layout — their partitioning/addressing is the exam's favorite trap.\n\nWorked example (with solution):\n```text\n{FIXED [Region] : SUM([Sales])}\n-> total sales per region, independent of what dimensions sit in the view.\nCompare each state's sales to its region total:\nSUM([Sales]) / {FIXED [Region] : SUM([Sales])}  -- per-state share of region.\nTable calc trap: RANK() down a table partitioned by Region ranks WITHIN\nregion only if partitioning is set to Region. Always check 'Compute Using'.\n```"},
  {"title": "Parameters, sets, and interactivity",
   "body": "Parameters are user-controlled values usable in calculations, filters, and reference lines. Sets are custom groupings (top-N, conditional). Combined with dashboard actions (filter, highlight, URL), they turn static views into stakeholder tools.\n\nWorked example (with solution):\n```text\n'What-if' scenario: parameter [Growth Assumption] (0% to 50%, step 5%).\nCalculated field: [Sales] * (1 + [Growth Assumption]).\nReference line on the trend chart at the parameterized forecast.\nStakeholder moves the slider; the forecast and the reference line update.\nExam angle: parameters are the answer whenever a scenario says 'let the user\ncontrol' a threshold, rate, or switched metric.\n```"},
  {"title": "Dashboards, stories, and sharing",
   "body": "Exam-grade dashboards: one message, consistent filters, device layouts considered, tooltips edited (no raw field dumps). Stories sequence views into a narrative. Sharing: publish to Tableau Server/Cloud with permissions, subscriptions, and refresh schedules.\n\nWorked example (with solution):\n```text\nDashboard checklist (use for every practice build):\n1. Title = takeaway. 2. Filters affect all relevant sheets (or say why not).\n3. Tooltips rewritten: show the comparison, hide the field-name salad.\n4. Color used for meaning (one metric = one hue ramp), not decoration.\n5. Published with a refresh schedule + the right audience permissions.\nThe exam's 'sharing insights' scenarios test exactly these choices.\n```"}],
 "cards": [
  {"front": "Tableau Certified Data Analyst's three working domains?", "back": "Connect to and prepare data; explore and analyze data; share insights."},
  {"front": "Pills on Rows/Columns translate to which SQL?", "back": "GROUP BY dimensions + aggregated measures."},
  {"front": "Join vs union vs blend?", "back": "Join: side-by-side on keys. Union: stacked same-schema tables. Blend: separate sources at aggregate level."},
  {"front": "What does {FIXED [Region] : SUM([Sales])} compute?", "back": "Total sales per region, independent of the view's dimensions."},
  {"front": "Table calculation trap to always check?", "back": "Partitioning/addressing ('Compute Using') — e.g., RANK within region vs across all."},
  {"front": "When are parameters the answer?", "back": "Whenever the user must control a threshold, rate, or switched metric."},
  {"front": "Dashboard title rule?", "back": "Title states the takeaway, not the topic."},
  {"front": "Tooltip rule?", "back": "Rewrite them: show the comparison, hide raw field-name dumps."}],
 "quiz": [
  {"q": "Rows: [Region], Text: SUM(Sales). The SQL equivalent?", "choices": ["SELECT * WHERE region", "SELECT DISTINCT region", "SELECT region, SUM(sales) GROUP BY region", "ORDER BY sales"], "answer": 2, "explain": "Dimension pills on shelves = GROUP BY; measure pills = aggregations."},
  {"q": "Two tables at different granularity (orders + regional targets). Correct approach?", "choices": ["Blend at Region granularity", "Inner join on region", "Union", "Cross join"], "answer": 0, "explain": "Different granularities call for blending at the coarser level, not row-level joins."},
  {"q": "{FIXED [Region] : SUM([Sales])} divided into SUM([Sales]) gives:", "choices": ["Total sales", "Average sales", "Region count", "Each state's share of its region's sales"], "answer": 3, "explain": "State-level SUM over region-level FIXED total = share of region."},
  {"q": "RANK() must rank within each region. What must you set?", "choices": ["Color", "Partitioning/addressing (Compute Using) to Region", "Font size", "The data source"], "answer": 1, "explain": "Table calculations follow partitioning; set it to Region to restart ranking per region."},
  {"q": "A 'what-if growth slider' on a forecast chart is built with:", "choices": ["A second data source", "A story point", "A parameter + calculated field", "A filter only"], "answer": 2, "explain": "Parameters hold the user-controlled value; the calc applies it."},
  {"q": "2024 sales UNION 2025 sales requires:", "choices": ["Matching columns", "Same row counts", "A blend", "Identical values"], "answer": 0, "explain": "Unions stack tables; schemas must align (Tableau can merge mismatched names)."},
  {"q": "Best tooltip practice?", "choices": ["Show every field", "Rewrite: show the comparison, hide field-name salad", "Disable tooltips", "Show raw IDs"], "answer": 1, "explain": "Tooltips are micro-storytelling; curate them."},
  {"q": "Publishing for executives with nightly data needs:", "choices": ["Email screenshots", "Desktop-only file", "Public link always", "Publish with refresh schedule + audience permissions"], "answer": 3, "explain": "Server/Cloud publishing gives scheduled refresh and controlled access."},],
 "drills": [{"id": "il26-m03-tab", "title": "Tableau drills", "items": [
   {"prompt": "LOD keywords (3)?", "answer": "FIXED, INCLUDE, EXCLUDE", "explain": "The three LOD scopes."},
   {"prompt": "{EXCLUDE [Region] : SUM(Sales)} computes?", "answer": "Sales total ignoring Region in the view", "explain": "EXCLUDE removes that dimension's grouping."},
   {"prompt": "Table calc for running total?", "answer": "RUNNING_SUM(SUM([Sales]))", "explain": "Classic addressing-dependent calc."},
   {"prompt": "Discrete vs continuous: blue vs green?", "answer": "Blue = discrete, Green = continuous", "explain": "Tableau's pill color code."},
   {"prompt": "Sets are useful for?", "answer": "Custom groupings: top-N, conditional membership", "explain": "Sets define in/out cohorts dynamically."},
   {"prompt": "Dashboard action types (3)?", "answer": "Filter, Highlight, URL (Go to Sheet)", "explain": "The interactivity toolkit."}]}],
 "handsOnLab": {"id": "il26-m03-lab", "title": "Exam-grade Tableau build", "brief": "Build a Tableau workbook end-to-end: blend multi-granularity sources, write LOD and table calculations, parameterize a scenario, and publish a checklist-clean dashboard.",
  "steps": ["Connect orders + returns (join) and union two years of sales.", "Blend regional targets at Region granularity; verify totals.", "Write a FIXED LOD for regional share and a RANK table calc with explicit partitioning.", "Add a growth-assumption parameter driving a forecast calc + reference line.", "Publish the dashboard passing the 5-point checklist."],
  "deliverable": "Published workbook with joins/union/blend, LOD + table calcs, parameter scenario, clean dashboard.",
  "checkpoint": "Regional share LOD reconciles to hand-computed shares; RANK restarts per region as configured."},
 "mockTask": {"id": "il26-m03-mock", "type": "choice", "q": "Scenario: show each product's sales as a share of its category total, with categories as columns. Which calculation?", "choices": ["SUM([Sales]) / TOTAL(SUM([Sales]))", "SUM([Sales]) / {FIXED [Category] : SUM([Sales])}", "RANK(SUM([Sales]))", "AVG([Sales])"], "answer": 1, "explain": "The FIXED LOD pins the denominator at category granularity regardless of the product-level view; TOTAL() would use table addressing and break with layout changes."},
 "crossLinks": [],
 "videoPlaceholders": False}}

MODULES += [M02, M03]

M04 = {"id": "IL26-M04", "patch": {
 "objectives": [
  "Name CompTIA Data+'s domain areas and explain what each domain expects you to DO, not just know.",
  "Apply data concepts (types, structures, formats) and environment knowledge (warehouses, lakes, governance roles) to scenario questions.",
  "Execute the data analysis workflow the exam tests: clean, analyze, visualize, and communicate with appropriate methods.",
  "Answer governance-heavy scenario questions (quality, privacy, controls) with the conservative, documented choice."],
 "notes": [
  {"title": "The domains and the exam's personality",
   "body": "CompTIA Data+ (DA0-002) organizes around five working areas: data concepts and environments, data acquisition/mining, data analysis, visualization and reporting, and data governance/quality/controls. The exam's personality is vendor-neutral and scenario-heavy: it asks what you would DO with a messy dataset, which chart fits a question, and which control fixes a quality problem. Weights shift between revisions — study the current official objectives, not a memorized percentage.\n\nWorked example (with solution):\n```text\nDomain-to-action map:\nConcepts & environments -> 'Name the storage and the data type.' (warehouse vs lake, structured vs semi-structured)\nAcquisition/mining     -> 'Get it and clean it.' (ETL steps, profiling, handling missing/duplicates)\nAnalysis               -> 'Answer it.' (descriptive stats, appropriate tests, correlation vs causation)\nVisualization          -> 'Show it.' (chart choice, dashboard design, audience)\nGovernance/quality     -> 'Protect it and prove it.' (controls, privacy, lineage, documentation)\nEvery scenario question is one of these five verbs in disguise.\n```\nIndependent study material; not affiliated with CompTIA."},
  {"title": "Concepts and environments",
   "body": "Data types: structured (tables), semi-structured (JSON/XML), unstructured (text/images). Environments: databases, warehouses (analytics-optimized), lakes (raw storage), lakehouses. Key exam distinctions: OLTP vs OLAP, batch vs streaming, and when each storage fits.\n\nWorked example (with solution):\n```text\nScenario: 'A retailer needs sub-second lookups of individual orders by cashiers\nAND nightly sales trend analysis.'\nAnswer: OLTP database (e.g., row-store) for the cashier lookups +\nOLAP warehouse for the nightly analytics. One system cannot serve both well:\nOLTP optimizes single-row writes/reads; OLAP optimizes columnar scans.\nExam trap: 'data lake' is wrong for the cashier lookup (lakes are not\ntransactional serving layers).\n```"},
  {"title": "Acquisition, mining, and cleaning",
   "body": "The exam tests the cleaning workflow: profile first (types, ranges, nulls, duplicates), then handle missing data (drop, impute, flag — with justification), standardize formats, and validate. ETL vs ELT: transform before load (ETL) vs load raw then transform in the warehouse (ELT).\n\nWorked example (with solution):\n```python\n# Profiling-first cleaning checklist, applied to a customer extract:\nimport pandas as pd\ndf = pd.read_csv('customers.csv')\nprint(df.dtypes)            # 1. types: is 'zip' numeric? fix to string\nprint(df.isna().sum())      # 2. missingness per column\nprint(df.duplicated().sum())# 3. duplicate rows\n# Decisions (documented, the exam loves documentation):\n# - email missing in 2% -> FLAG as unknown, do not drop (bias risk)\n# - 40 exact-duplicate rows -> drop after verifying same source+timestamp\n# - phone formats mixed -> standardize to E.164 before any join\n```"},
  {"title": "Analysis and visualization choices",
   "body": "Analysis domain: pick the right descriptive tool (central tendency, spread, correlation) and know what it cannot prove. Visualization domain: match chart to question — trends (line), comparisons (bar), composition (stacked bar), relationships (scatter), distributions (histogram). The exam punishes chart junk and misleading axes.\n\nWorked example (with solution):\n```text\n'Which visualization shows whether discount depth relates to units sold?'\nAnswer: scatter plot (discount % on x, units on y), optionally with a trend line.\nWhy not: bar chart (compares categories, hides the continuous relationship),\npie chart (composition only), dual-axis line (invites false correlation reads).\nExam pattern: the right answer names the QUESTION TYPE first (relationship\n-> scatter; trend -> line; comparison -> bar; part-of-whole -> stacked bar).\n```"},
  {"title": "Governance, quality, and controls",
   "body": "The heaviest-weighted area: data quality dimensions (accuracy, completeness, consistency, timeliness, validity, uniqueness), controls (validation rules, access controls, audits), privacy (PII handling, masking, retention), and documentation (data dictionaries, lineage). When in doubt, choose the documented, least-privilege, auditable answer.\n\nWorked example (with solution):\n```text\nScenario: 'Analysts need customer data for churn modeling; the table contains\nSSNs and full card numbers.'\nCorrect: provision a masked/tokenized extract (SSN -> last-4 or hash,\ncard -> token), document the extract in the data catalog, set an expiry.\nWrong: full-table access ('they're employees'), or emailing a CSV.\nExam rule of thumb: privacy questions -> minimize + mask + document.\nQuality questions -> name the DIMENSION (e.g., 'completeness') then the fix.\n```"}],
 "cards": [
  {"front": "Data+'s five domain verbs?", "back": "Name it (concepts), get/clean it (acquisition), answer it (analysis), show it (visualization), protect/prove it (governance)."},
  {"front": "OLTP vs OLAP?", "back": "OLTP: single-row transactions (cashier lookups). OLAP: columnar analytics scans."},
  {"front": "ETL vs ELT?", "back": "ETL: transform before load. ELT: load raw, transform in the warehouse."},
  {"front": "Cleaning workflow order?", "back": "Profile (types/nulls/dups) -> decide (drop/impute/flag with justification) -> standardize -> validate."},
  {"front": "Relationship question -> which chart?", "back": "Scatter plot."},
  {"front": "Data quality dimensions (6)?", "back": "Accuracy, completeness, consistency, timeliness, validity, uniqueness."},
  {"front": "Analysts need PII-heavy data: correct move?", "back": "Masked/tokenized extract, catalogued, expiring — minimize + mask + document."},
  {"front": "Structured vs semi-structured vs unstructured?", "back": "Tables; JSON/XML; text/images/video."}],
 "quiz": [
  {"q": "A retailer needs sub-second order lookups AND nightly trend analysis. Correct architecture?", "choices": ["One data lake for both", "Spreadsheets", "OLTP database for lookups + OLAP warehouse for analytics", "A single OLTP database for both"], "answer": 2, "explain": "OLTP serves single-row transactions; OLAP serves analytic scans. Different workloads, different systems."},
  {"q": "First step when handed a messy customer extract?", "choices": ["Profile it: types, nulls, duplicates, ranges", "Build the dashboard", "Delete all nulls", "Train a model"], "answer": 0, "explain": "Profiling diagnoses before treatment; every cleaning decision needs the profile as evidence."},
  {"q": "Email missing in 2% of rows. Best handling?", "choices": ["Drop the rows silently", "Fill with a fake email", "Ignore it", "Flag as unknown and keep - dropping risks bias"], "answer": 3, "explain": "Missingness can be non-random; flag and document rather than silently dropping."},
  {"q": "Which chart shows whether discount depth relates to units sold?", "choices": ["Pie chart", "Scatter plot with trend line", "Bar chart", "Dual-axis line"], "answer": 1, "explain": "Relationship between two continuous variables = scatter plot."},
  {"q": "Duplicate rows found in a sales extract. Before dropping, you must:", "choices": ["Drop immediately", "Keep them to be safe", "Verify they are true duplicates (same source + timestamp), then drop and document", "Average them"], "answer": 2, "explain": "Near-duplicates can be legitimate (two identical orders); verify provenance, then document the dedup."},
  {"q": "'Completeness' as a data quality dimension means:", "choices": ["All required values are present", "No duplicate rows", "Values are in range", "Data is fresh"], "answer": 0, "explain": "Completeness = presence of required data; validity = conformance to rules; timeliness = freshness."},
  {"q": "Churn modeling needs customer data containing SSNs. Correct provisioning?", "choices": ["Full table access for all analysts", "Masked/tokenized extract, catalogued, with expiry", "Email a CSV", "Deny all access"], "answer": 1, "explain": "Minimize + mask + document: least privilege with an auditable, expiring extract."},
  {"q": "JSON clickstream logs are which data type?", "choices": ["Structured", "Unstructured", "Relational", "Semi-structured"], "answer": 3, "explain": "JSON has organizational structure (keys) without a fixed tabular schema: semi-structured."},],
 "drills": [{"id": "il26-m04-dataplus", "title": "Data+ drills", "items": [
   {"prompt": "Six data quality dimensions?", "answer": "Accuracy, completeness, consistency, timeliness, validity, uniqueness", "explain": "The exam's quality vocabulary."},
   {"prompt": "Trend over time -> chart?", "answer": "Line chart", "explain": "Trends = lines."},
   {"prompt": "Part-of-whole (small N) -> chart?", "answer": "Stacked bar (or pie for very small N)", "explain": "Composition without pie-chart abuse."},
   {"prompt": "Distribution of a continuous variable -> chart?", "answer": "Histogram", "explain": "Binned frequencies show shape."},
   {"prompt": "ELT order of operations?", "answer": "Extract, Load raw, Transform in warehouse", "explain": "Transform happens after loading."},
   {"prompt": "Data dictionary documents what?", "answer": "Column definitions, types, allowed values, owners", "explain": "The contract for every field."}]}],
 "handsOnLab": {"id": "il26-m04-lab", "title": "Data+ scenario gauntlet", "brief": "Work 20 scenario questions spanning all five domains, classifying each by domain verb and writing the justification for every answer.",
  "steps": ["Take the 20-scenario set cold; record answers and confidence.", "Classify each question by its domain verb (name/get/answer/show/protect).", "Write a 2-sentence justification for each answer citing the domain concept.", "Revisit misses: name the exact concept gap, not 'I guessed wrong.'", "Build a personal cheat sheet of the 10 most-missed patterns."],
  "deliverable": "Answered scenario set with domain classifications, justifications, and gap cheat sheet.",
  "checkpoint": "Every miss maps to a named concept; the cheat sheet covers all five domains."},
 "mockTask": {"id": "il26-m04-mock", "type": "choice", "q": "Scenario: two analysts report different average order values from the same table; one used AVG(revenue), the other SUM(revenue)/COUNT(*). The table has NULL revenues. What is the Data+ answer?", "choices": ["One of them has a broken tool.", "Both formulas are valid but answer different questions: AVG skips NULLs while COUNT(*) includes those rows as zero-value; the correct choice depends on what NULL means — document the decision.", "Always use AVG.", "NULLs prove the data is unusable."], "answer": 1, "explain": "The formulas differ exactly in NULL handling. Data+ rewards naming the quality dimension (completeness/validity) and documenting the interpretation."},
 "crossLinks": [{"course": "il-09-adaptive-certification-command", "moduleId": "il09-comptia-data-cloud", "topic": "CompTIA data/cloud certification track", "why": "Same course family covers the CompTIA data certification track for context."}],
 "videoPlaceholders": False}}

M05 = {"id": "IL26-M05", "patch": {
 "objectives": [
  "Sequence the IBM Data Analyst Professional Certificate's courses into a study plan, naming the skill each course builds.",
  "Perform Excel-based analysis (formulas, pivot tables, data cleaning) at the certificate's expected depth.",
  "Build Cognos-style dashboards and explain the dashboard design principles the certificate emphasizes.",
  "Write Python (pandas) and SQL for the certificate's data tasks and complete a capstone-grade project."],
 "notes": [
  {"title": "The certificate's course spine",
   "body": "The IBM Data Analyst Professional Certificate (via Coursera) sequences roughly: introduction to data analytics, Excel fundamentals, data visualization (Cognos Analytics), Python for data science, SQL and relational databases, and a capstone project. The spine moves from spreadsheets to code to databases — each course's tool becomes the next course's assumed skill.\n\nWorked example (with solution):\n```text\nCourse-to-skill triage:\nIntro          -> analytics process, roles, data ecosystem (skim once)\nExcel          -> formulas, pivots, cleaning (drill: the daily tool)\nCognos/viz     -> dashboard assembly, chart choice (build 3 dashboards)\nPython         -> pandas wrangling, numpy basics (translate every Excel task)\nSQL            -> SELECT/JOIN/GROUP BY on a real database (not just the sandbox)\nCapstone       -> one end-to-end project with a stakeholder writeup\nTimebox the intro; the portfolio comes from Excel + Python + SQL + capstone.\n```\nIndependent study material; not affiliated with IBM."},
  {"title": "Excel at certificate depth",
   "body": "The certificate expects fluent formulas: XLOOKUP/VLOOKUP, INDEX-MATCH, IF/IFS, SUMIFS/COUNTIFS/AVERAGEIFS, TEXT/DATE functions, and pivot tables with slicers. The exam-style questions test nested logic and absolute vs relative references.\n\nWorked example (with solution):\n```text\nTiered commission: 5% under $10K, 7% for $10K-$25K, 10% above $25K (on sales in A2):\n=IFS(A2<10000, A2*0.05, A2<=25000, A2*0.07, TRUE, A2*0.10)\nLookup the rep's region from a table (regions in $D$2:$E$50, absolute refs\nso the formula copies down safely):\n=XLOOKUP(B2, $D$2:$D$50, $E$2:$E$50, \"Unknown\")\nAbsolute ($D$2) vs relative (B2): lock the lookup range, let the key move.\n```"},
  {"title": "Dashboards, Cognos-style",
   "body": "Cognos Analytics dashboards assemble visualizations with filters and tabs. The transferable principles: one dashboard = one decision, consistent filter scope, sorted and labeled charts, and drill-through from summary to detail. These principles survive any BI tool.\n\nWorked example (with solution):\n```text\nExecutive sales dashboard (tool-agnostic checklist):\nTab 1 'Overview': KPI tiles (revenue, orders, AOV) + monthly trend + top-5 products.\nTab 2 'Drill': region x category matrix with drill-through to order detail.\nFilters: date range + region, applied consistently to every visualization.\nEvery chart titled with its takeaway; axes labeled with units ($K, not $).\nRebuild this in any BI tool you own: the design transfers, the clicks don't.\n```"},
  {"title": "Python for the certificate: pandas core",
   "body": "The Python course centers on pandas: reading data, selecting/filtering, groupby aggregation, merging, and basic plotting. The winning study move: redo every Excel exercise in pandas, building the bilingual muscle the certificate's capstone rewards.\n\nWorked example (with solution):\n```python\n# Excel pivot (average revenue by region) in pandas:\nimport pandas as pd\ndf = pd.read_csv('sales.csv')\nresult = (df.groupby('region')['revenue']\n            .agg(avg_revenue='mean', orders='count')\n            .sort_values('avg_revenue', ascending=False))\nprint(result)\n# Excel XLOOKUP in pandas: left-merge on the key.\nreps = pd.read_csv('reps.csv')\nenriched = df.merge(reps[['rep_id', 'region']], on='rep_id', how='left')\n```"},
  {"title": "SQL and the capstone",
   "body": "The SQL course covers relational basics through SELECT, WHERE, JOIN, GROUP BY, subqueries, and views — typically on Db2 or a cloud sandbox. The capstone expects you to combine everything: query, analyze in Python/Excel, visualize, and present. Treat the capstone as portfolio project #1, not homework.\n\nWorked example (with solution):\n```sql\n-- Capstone-style: top 3 products by revenue in each region (portable pattern):\nSELECT region, product_name, revenue\nFROM (\n  SELECT region, product_name, SUM(amount) AS revenue,\n         ROW_NUMBER() OVER (PARTITION BY region ORDER BY SUM(amount) DESC) AS rn\n  FROM sales JOIN products USING (product_id)\n  GROUP BY region, product_name\n) t\nWHERE rn <= 3;\n-- Then: export, analyze distributions in pandas, dashboard the result,\n-- and write the one-page stakeholder summary. That stack IS the capstone.\n```"}],
 "cards": [
  {"front": "IBM certificate's tool sequence?", "back": "Excel -> Cognos/viz -> Python -> SQL -> capstone."},
  {"front": "Tiered commission formula pattern?", "back": "IFS with thresholds, e.g., =IFS(A2<10000, A2*0.05, ...)."},
  {"front": "XLOOKUP with absolute refs: why?", "back": "Lock the lookup range ($D$2:$D$50) so it doesn't shift when copying down."},
  {"front": "Dashboard design rule: one dashboard = ?", "back": "One decision. Tabs separate overview from drill detail."},
  {"front": "pandas equivalent of an Excel pivot?", "back": "groupby + agg."},
  {"front": "pandas equivalent of XLOOKUP?", "back": "merge (left join) on the key."},
  {"front": "Top-N per group SQL pattern?", "back": "ROW_NUMBER() OVER (PARTITION BY group ORDER BY metric DESC), filter rn <= N."},
  {"front": "What makes the capstone portfolio-grade?", "back": "Query + analyze + visualize + stakeholder writeup as one end-to-end artifact."}],
 "quiz": [
  {"q": "The IBM certificate's skill spine runs:", "choices": ["SQL first, then Excel", "Capstone first", "Only Python", "Excel -> visualization -> Python -> SQL -> capstone"], "answer": 3, "explain": "Spreadsheets to code to databases; each course's tool becomes the next course's assumed skill."},
  {"q": "Commission tiers in A2: 5%/<10K, 7%/10-25K, 10%/>25K. Correct formula?", "choices": ["=IFS(A2<10000, A2*0.05, A2<=25000, A2*0.07, TRUE, A2*0.10)", "=A2*0.07", "=SUM(A2)*0.05", "=IF(A2>0, A2*0.1)"], "answer": 0, "explain": "IFS handles tiered thresholds cleanly; TRUE is the final catch-all."},
  {"q": "In =XLOOKUP(B2, $D$2:$D$50, $E$2:$E$50), the $ signs:", "choices": ["Are decorative", "Lock B2", "Lock the lookup range so copying down keeps it fixed", "Convert to text"], "answer": 2, "explain": "Absolute references anchor the range; the lookup key B2 stays relative."},
  {"q": "pandas equivalent of a pivot table averaging revenue by region?", "choices": ["df.sort_values('region')", "df.groupby('region')['revenue'].mean()", "df['region'].unique()", "df.merge(reps)"], "answer": 1, "explain": "groupby + aggregation is the pivot operation."},
  {"q": "pandas equivalent of XLOOKUP?", "choices": ["df.describe()", "df.dropna()", "df.pivot()", "df.merge(other, on='key', how='left')"], "answer": 3, "explain": "Key-based enrichment across tables is a join/merge."},
  {"q": "Top 3 products per region in SQL uses:", "choices": ["ROW_NUMBER() OVER (PARTITION BY region ORDER BY SUM(amount) DESC), filter rn<=3", "LIMIT 3", "TOP 3 with GROUP BY", "DISTINCT"], "answer": 0, "explain": "Window functions compute per-group ranks; LIMIT alone cannot do per-group top-N."},
  {"q": "Executive dashboard best structure?", "choices": ["One giant table", "Ten pie charts", "Overview tab (KPIs + trend) + drill tab (matrix with drill-through)", "Raw data export"], "answer": 2, "explain": "One decision per dashboard; tabs separate summary from detail."},
  {"q": "The highest-ROI study move for the Python course?", "choices": ["Memorize syntax", "Redo every Excel exercise in pandas", "Skip to the capstone", "Watch at 2x speed"], "answer": 1, "explain": "Bilingual Excel/pandas fluency is exactly what the capstone and employers test."},],
 "drills": [{"id": "il26-m05-ibm", "title": "IBM certificate drills", "items": [
   {"prompt": "Excel: count orders over $500 in B2:B100?", "answer": "=COUNTIF(B2:B100,\">500\")", "explain": "COUNTIF with a criteria string."},
   {"prompt": "Excel: sum revenue (C) where region (A) = 'West'?", "answer": "=SUMIFS(C:C, A:A, \"West\")", "explain": "SUMIFS(sum_range, criteria_range, criteria)."},
   {"prompt": "pandas: rows where revenue > 500?", "answer": "df[df['revenue'] > 500]", "explain": "Boolean masking."},
   {"prompt": "pandas: average revenue by region?", "answer": "df.groupby('region')['revenue'].mean()", "explain": "The pivot equivalent."},
   {"prompt": "SQL: average revenue by region?", "answer": "SELECT region, AVG(revenue) FROM sales GROUP BY region", "explain": "GROUP BY aggregation."},
   {"prompt": "Nested IF vs IFS: which is cleaner for tiers?", "answer": "IFS", "explain": "Flat threshold list beats nested IFs."}]}],
 "handsOnLab": {"id": "il26-m05-lab", "title": "Bilingual analyst build", "brief": "Take one business question and answer it three ways: Excel, pandas, and SQL — then dashboard the result and write the stakeholder summary.",
  "steps": ["Pick the question: e.g., 'Which regions beat target, and by how much?'", "Answer in Excel (formulas + pivot + chart).", "Answer in pandas (groupby/merge) and verify the numbers match Excel exactly.", "Answer in SQL against a real database; verify again.", "Dashboard the result and write the one-page stakeholder summary (capstone style)."],
  "deliverable": "Three verified analyses + dashboard + stakeholder summary.",
  "checkpoint": "All three tools produce identical numbers to the cent; the summary states the takeaway first."},
 "mockTask": {"id": "il26-m05-mock", "type": "choice", "q": "Your Excel pivot says West averaged $412/order; your pandas groupby says $438. What do you do?", "choices": ["Ship the Excel number; it's the certificate tool.", "Ship the pandas number; code beats spreadsheets.", "Reconcile before shipping: check filters, null handling, and duplicates in each — the mismatch is a data-definition difference, and publishing either unverified is the real error.", "Average the two."], "answer": 2, "explain": "Tool disagreements are definition disagreements (filters, NULLs, dups). Reconcile to a single truth, document it, then publish."},
 "crossLinks": [],
 "videoPlaceholders": False}}

MODULES += [M04, M05]

M06 = {"id": "IL26-M06", "patch": {
 "objectives": [
  "Map the AWS data certification domains (ingestion/transformation, storage, operations, security/governance) to the AWS services that implement each.",
  "Choose the right AWS storage and ingestion service for a scenario (S3 vs Redshift vs DynamoDB vs Kinesis vs Glue) and justify the trade-off.",
  "Explain data security and governance on AWS (IAM, KMS, Lake Formation) as they appear in exam scenarios.",
  "Answer cost- and performance-oriented scenario questions with the AWS-native best practice."],
 "notes": [
  {"title": "The domains and the service map",
   "body": "AWS's data certification (currently the Data Engineer - Associate; the older Data Analytics Specialty retired) tests: data ingestion and transformation, data store management, data operations and support, and data security and governance. The exam is scenario-driven: 'which service, and why' — memorized service definitions fail, but the decision framework passes.\n\nWorked example (with solution):\n```text\nDomain-to-service map (the exam's decision tree):\nIngestion: Kinesis (streaming) vs DMS/Transfer Family (migration/batch)\n  -> 'real-time' in the question = Kinesis; 'migrate the database' = DMS.\nTransformation: Glue (serverless Spark ETL) vs Lambda (event-driven micro-batch)\n  -> 'no servers to manage, Spark-scale' = Glue.\nStorage: S3 (lake), Redshift (warehouse), DynamoDB (key-value), RDS/Aurora (relational)\n  -> 'analytics on petabytes' = S3 + Athena/Redshift; 'millisecond lookups' = DynamoDB.\nSecurity: IAM + KMS + Lake Formation (fine-grained lake access).\nThe question's CONSTRAINT (latency, scale, ops burden) names the service.\n```\nIndependent study material; not affiliated with Amazon/AWS."},
  {"title": "Storage decisions: S3, Redshift, DynamoDB, RDS",
   "body": "S3 is the center of gravity: object storage, 11-nines durability, storage classes for cost tiers. Redshift: MPP columnar warehouse for complex analytics. DynamoDB: single-digit-millisecond key-value at any scale. RDS/Aurora: managed relational for transactional workloads.\n\nWorked example (with solution):\n```text\nScenario: '10 TB of clickstream JSON, queried ad-hoc a few times a day,\nbudget is tight.'\nAnswer: S3 (Intelligent-Tiering) + Athena (serverless SQL, pay per query).\nWhy not Redshift: provisioned clusters idle between the few daily queries\n(pay for uptime); why not DynamoDB: JSON analytics is not key-value lookup.\nCost logic: Athena charges per TB scanned -> partition by date and use\ncolumnar Parquet to cut scanned bytes 10-100x. The exam rewards this\n'two-knob' thinking: service choice + cost control.\n```"},
  {"title": "Ingestion and transformation: Kinesis, Glue, Lambda",
   "body": "Kinesis Data Streams: ordered, replayable streaming ingestion. Kinesis Firehose: streaming delivery to S3/Redshift with optional Lambda transforms. Glue: serverless Spark ETL with crawlers and Data Catalog. Lambda: event-driven functions for light transforms.\n\nWorked example (with solution):\n```python\n# Decision logic as code (the exam's scenario pattern):\ndef pick_ingestion(req):\n    if req.get('replay_needed') or req.get('ordering'):\n        return 'Kinesis Data Streams (replayable, ordered shards)'\n    if req.get('destination') in ('s3', 'redshift') and req.get('near_real_time'):\n        return 'Kinesis Firehose (managed delivery + optional Lambda transform)'\n    if req.get('batch_window'):\n        return 'Glue ETL job on a schedule (serverless Spark)'\n    return 'Lambda on S3 events (lightweight, event-driven)'\nprint(pick_ingestion({'replay_needed': True}))\n# Kinesis Data Streams (replayable, ordered shards)\n```"},
  {"title": "Security and governance: IAM, KMS, Lake Formation",
   "body": "IAM: who can do what (least privilege, roles not long-term keys). KMS: encryption key management (SSE-S3 vs SSE-KMS vs client-side). Lake Formation: fine-grained permissions on lake data (column/row-level). CloudTrail: the audit trail proving who did what.\n\nWorked example (with solution):\n```text\nScenario: 'Analysts need the marketing prefix of the lake, but must never see\nPII columns; every access must be auditable.'\nAnswer: Lake Formation column-level permissions (grant marketing/* except\npii columns) + CloudTrail logging + SSE-KMS encryption.\nWhy not just IAM: IAM grants bucket-level access (too coarse for columns).\nWhy not just masking in the query layer: the exam wants the GOVERNANCE\nservice (Lake Formation), not application logic, for enforcement.\n```"},
  {"title": "Operations, cost, and exam-day tactics",
   "body": "Operations domain: monitoring (CloudWatch), orchestration (Step Functions, MWAA/Managed Airflow), and failure handling (dead-letter queues, retries). Cost tactics: right-size, use Spot for fault-tolerant batch, lifecycle policies on S3, partition to reduce Athena scans. Exam tactic: the cheapest compliant answer usually wins ties.\n\nWorked example (with solution):\n```text\nScenario: 'Nightly Spark job processes the day's logs; occasional failures must\nnot lose data; minimize cost.'\nAnswer: Glue job (serverless, no idle cluster) + S3 source versioning +\njob bookmarks (no reprocessing) + CloudWatch alarms on failure +\ndead-letter handling for poison records.\nCost note: On-Demand is fine for a nightly job; Spot adds complexity the\nscenario doesn't require. The exam punishes over-engineering as much as\nunder-engineering: match the solution to the stated constraints.\n```"}],
 "cards": [
  {"front": "AWS data cert's four domains?", "back": "Ingestion/transformation; data store management; operations/support; security/governance."},
  {"front": "'Real-time' in a question points to?", "back": "Kinesis (Streams for replayable/ordered; Firehose for managed delivery)."},
  {"front": "10 TB JSON, ad-hoc queries, tight budget?", "back": "S3 + Athena, partitioned Parquet to cut scanned bytes."},
  {"front": "Millisecond key-value lookups at scale?", "back": "DynamoDB."},
  {"front": "Column-level lake permissions: which service?", "back": "Lake Formation."},
  {"front": "Glue vs Lambda for ETL?", "back": "Glue: serverless Spark at scale. Lambda: lightweight event-driven transforms."},
  {"front": "Athena cost control knob?", "back": "Partitioning + columnar formats (Parquet) to reduce bytes scanned."},
  {"front": "Who-did-what audit trail?", "back": "CloudTrail."}],
 "quiz": [
  {"q": "Scenario: 'migrate the on-prem database to AWS with minimal downtime.' Correct service?", "choices": ["Kinesis", "Athena", "DMS (Database Migration Service)", "QuickSight"], "answer": 2, "explain": "DMS is the migration service; Kinesis is for streaming, Athena for querying."},
  {"q": "Ordered, replayable streaming ingestion?", "choices": ["Firehose", "Kinesis Data Streams", "SQS standard", "SNS"], "answer": 1, "explain": "Data Streams gives ordered shards with replay; Firehose is managed delivery without replay."},
  {"q": "Complex analytics over petabytes in S3, queried a few times daily, tight budget?", "choices": ["S3 + Athena with partitioned Parquet", "Provisioned Redshift cluster", "DynamoDB", "RDS"], "answer": 0, "explain": "Serverless Athena pays per query; Parquet + partitioning cuts scanned bytes and cost."},
  {"q": "Single-digit-millisecond lookups by primary key at any scale?", "choices": ["Redshift", "S3", "Glue", "DynamoDB"], "answer": 3, "explain": "DynamoDB is the key-value store built for millisecond latency."},
  {"q": "Analysts must see marketing data but never PII columns, with auditing. Correct?", "choices": ["Lake Formation column-level grants + CloudTrail", "Public S3 bucket", "IAM full S3 access", "Email CSVs"], "answer": 0, "explain": "Lake Formation enforces column-level governance; CloudTrail audits access."},
  {"q": "Nightly Spark ETL, no servers to manage?", "choices": ["Self-managed EC2 Spark", "EMR always-on cluster", "Glue", "RDS"], "answer": 2, "explain": "Glue is serverless Spark ETL — no cluster to manage or pay for idle."},
  {"q": "SSE-KMS vs SSE-S3: the difference?", "choices": ["No difference", "SSE-KMS uses customer-managed keys in KMS with audit trail; SSE-S3 uses Amazon-managed keys", "SSE-S3 is client-side", "KMS is only for RDS"], "answer": 1, "explain": "KMS gives key control and CloudTrail-logged key usage; SSE-S3 is simpler Amazon-managed encryption."},
  {"q": "Poison records must not kill a nightly pipeline. Pattern?", "choices": ["Ignore failures", "Bigger instance", "Manual reruns", "Dead-letter queue + retries + CloudWatch alarms"], "answer": 3, "explain": "DLQs isolate bad records, retries handle transients, alarms surface real failures."}],
 "drills": [{"id": "il26-m06-aws", "title": "AWS data drills", "items": [
   {"prompt": "S3 durability figure?", "answer": "11 nines (99.999999999%)", "explain": "The exam's favorite S3 fact."},
   {"prompt": "Redshift is what kind of warehouse?", "answer": "MPP columnar", "explain": "Massively parallel, column-oriented."},
   {"prompt": "Glue Data Catalog is used for?", "answer": "Metadata: table definitions crawled from S3", "explain": "The Hive-compatible metastore."},
   {"prompt": "Kinesis shard ordering guarantee?", "answer": "Ordered within a shard (partition key)", "explain": "Ordering is per-shard, not global."},
   {"prompt": "Athena queries what directly?", "answer": "S3 data via SQL (serverless)", "explain": "No cluster; pay per TB scanned."},
   {"prompt": "Lake Formation replaces which coarse control?", "answer": "Bucket-level IAM-only access for lakes", "explain": "Adds table/column/row granularity."}]}],
 "handsOnLab": {"id": "il26-m06-lab", "title": "Serverless lake query lab", "brief": "Build a mini lake: land CSVs in S3, convert to partitioned Parquet, query with Athena, and compare scanned bytes and cost before/after optimization.",
  "steps": ["Create the bucket layout: raw/ and curated/ prefixes with date partitions.", "Convert CSVs to Parquet partitioned by date (Glue or a local script).", "Run the same 3 analytic queries against CSV vs Parquet; record bytes scanned.", "Add a Lake Formation-style access note: who may read which prefix (documented).", "Write the cost verdict: per-query cost before/after, and the rule you'd enforce."],
  "deliverable": "Query comparison table (bytes scanned, runtime, estimated cost) + access note + cost rule.",
  "checkpoint": "Parquet queries scan an order of magnitude fewer bytes; the access note names prefixes explicitly."},
 "mockTask": {"id": "il26-m06-mock", "type": "choice", "q": "Scenario: clickstream must be queryable within minutes, survive traffic spikes, and allow replaying last week's stream to rebuild aggregates. Pick the ingestion.", "choices": ["Firehose to S3 only", "Kinesis Data Streams (buffered) feeding both real-time consumers and S3 via Firehose", "Nightly batch upload", "Direct writes to Redshift"], "answer": 1, "explain": "Streams gives replay + ordering under spike load; Firehose lands it to S3 for the lake. Firehose alone can't replay; batch misses the minutes requirement."},
 "crossLinks": [{"course": "il-07-data-engineering-analytics-ai", "moduleId": "il07-aws-data", "topic": "AWS data engineering services", "why": "il07-aws-data teaches the AWS data service landscape the exam questions assume."}],
 "videoPlaceholders": False}}

M07 = {"id": "IL26-M07", "patch": {
 "objectives": [
  "Explain the lakehouse concept (Delta Lake + Unity Catalog) and how it differs from classic warehouses and lakes.",
  "Write Databricks SQL for analytics: CTEs, window functions, and Delta Lake time travel / merge patterns.",
  "Describe Unity Catalog governance (schemas, grants, lineage) as tested in Databricks certification scenarios.",
  "Build Databricks SQL dashboards and alerts following the same takeaway-first design rules as any BI tool."],
 "notes": [
  {"title": "The lakehouse: one platform, two old worlds",
   "body": "The lakehouse combines data-lake economics (cheap object storage, open formats) with warehouse reliability (ACID transactions, schema enforcement) via Delta Lake. Unity Catalog adds centralized governance: one permission model across workspaces. The exam tests this positioning against 'why not just a warehouse / just a lake' scenarios.\n\nWorked example (with solution):\n```text\n'Why lakehouse instead of a classic warehouse for our analytics?'\n- Warehouse-only: proprietary format, expensive storage, struggles with\n  semi-structured/ML workloads.\n- Lake-only: no ACID, no schema enforcement, the 'data swamp' problem.\n- Lakehouse (Delta): open Parquet-based format + transactions + time travel\n  + streaming/batch unification, governed by Unity Catalog.\nExam phrasing: the answer always names the RELIABILITY feature (ACID,\nschema enforcement) plus the OPENNESS feature (open format, ML-ready).\n```\nIndependent study material; not affiliated with Databricks."},
  {"title": "Databricks SQL: the analyst's dialect",
   "body": "Databricks SQL is ANSI SQL plus Delta Lake superpowers: time travel (query as of a version/timestamp), MERGE INTO for upserts, COPY INTO for idempotent loads, and OPTIMIZE/Z-ORDER for file layout. The exam rewards knowing which Delta feature solves a data-engineering pain.\n\nWorked example (with solution):\n```sql\n-- Upsert the daily feed into the customer dimension (SCD-1):\nMERGE INTO dim_customer AS t\nUSING stg_customer_daily AS s\nON t.customer_id = s.customer_id\nWHEN MATCHED THEN UPDATE SET *\nWHEN NOT MATCHED THEN INSERT *;\n-- Audit what changed yesterday (time travel):\nSELECT * FROM dim_customer VERSION AS OF 42\nEXCEPT\nSELECT * FROM dim_customer VERSION AS OF 41;\n-- Idempotent load of new files:\nCOPY INTO raw_events FROM 's3://bucket/events/'\n  FILEFORMAT = PARQUET COPY_OPTIONS ('mergeSchema' = 'true');\n```"},
  {"title": "Unity Catalog: governance the exam tests",
   "body": "Unity Catalog's hierarchy: catalog -> schema -> table/volume. Grants (SELECT, MODIFY, USAGE) are managed centrally; data lineage tracks column-level provenance automatically. The exam scenarios test least-privilege grants and lineage-based impact analysis.\n\nWorked example (with solution):\n```sql\n-- Least-privilege analyst access: read on one schema, no modify rights.\nGRANT USAGE ON CATALOG prod TO analysts;\nGRANT USAGE ON SCHEMA prod.mart TO analysts;\nGRANT SELECT ON SCHEMA prod.mart TO analysts;\n-- Impact analysis question: 'If we change column X, what breaks?'\n-- Answer: check Unity Catalog lineage (upstream sources + downstream\n-- tables/dashboards), not grep through notebooks.\n-- PII scenario: dynamic views mask columns per group membership.\n```"},
  {"title": "Performance: Photon, caching, and file layout",
   "body": "Photon is the vectorized query engine (faster scans/aggregations). Delta caching keeps hot data on fast local disks. OPTIMIZE compacts small files; Z-ORDER colocates related data to skip files. The exam tests matching the performance knob to the symptom.\n\nWorked example (with solution):\n```text\nSymptom -> knob mapping:\n'Too many small files, slow scans'        -> OPTIMIZE (compaction)\n'Queries filter on customer_id but scan everything' -> Z-ORDER BY (customer_id)\n'Repeated dashboard queries are slow'     -> Delta cache / warmed SQL warehouse\n'Aggregations over billions of rows lag' -> Photon-enabled warehouse\nExam trap: Z-ORDER helps FILTER-skipping, not join speed; OPTIMIZE helps\nfile-count problems, not skew. Match the knob to the symptom.\n```"},
  {"title": "Dashboards, alerts, and the analyst workflow",
   "body": "Databricks SQL dashboards: parameterized queries, scheduled refreshes, and alerts on thresholds (e.g., 'alert when null-rate > 5%'). The analyst workflow the exam implies: explore in notebooks, productionize as SQL queries, schedule, alert, dashboard.\n\nWorked example (with solution):\n```sql\n-- Data-quality alert query (scheduled, alerts when rows appear):\nSELECT COUNT(*) AS null_email_count\nFROM prod.mart.customers\nWHERE email IS NULL\n  AND updated_at >= current_timestamp() - INTERVAL 1 DAY;\n-- Alert condition: null_email_count > 100 -> notify #data-quality.\n-- Dashboard rule (same as every BI tool): parameterize the date range,\n-- title each chart with its takeaway, and link the alert query's dashboard\n-- tile so on-call analysts land on context, not just a number.\n```"}],
 "cards": [
  {"front": "Lakehouse in one sentence?", "back": "Lake economics + warehouse reliability via Delta Lake (ACID, open format)."},
  {"front": "Delta time travel syntax?", "back": "SELECT ... FROM t VERSION AS OF 42 (or TIMESTAMP AS OF ...)."},
  {"front": "Upsert pattern in Databricks SQL?", "back": "MERGE INTO ... WHEN MATCHED THEN UPDATE / WHEN NOT MATCHED THEN INSERT."},
  {"front": "Unity Catalog hierarchy?", "back": "Catalog -> schema -> table/volume."},
  {"front": "Too many small files: which knob?", "back": "OPTIMIZE (compaction)."},
  {"front": "Filter-skipping on customer_id: which knob?", "back": "Z-ORDER BY customer_id."},
  {"front": "Least-privilege analyst grant pattern?", "back": "USAGE on catalog+schema, SELECT on schema — no MODIFY."},
  {"front": "Data-quality alert pattern?", "back": "Scheduled query counting violations + threshold alert to the data channel."}],
 "quiz": [
  {"q": "The lakehouse's core promise vs a classic warehouse?", "choices": ["Cheaper proprietary storage", "No SQL support", "Open-format storage with ACID transactions and schema enforcement", "Manual file management"], "answer": 2, "explain": "Delta Lake adds warehouse reliability (ACID, schema) to open lake storage."},
  {"q": "Query a table as it looked at version 42?", "choices": ["SELECT * FROM t VERSION AS OF 42", "SELECT * FROM t WHERE version = 42", "RESTORE t TO 42", "SELECT history FROM t"], "answer": 0, "explain": "VERSION AS OF is Delta time travel; WHERE version filters a column."},
  {"q": "Daily upsert of a staging feed into a dimension?", "choices": ["DELETE + INSERT always", "COPY INTO only", "UNION", "MERGE INTO with MATCHED/NOT MATCHED clauses"], "answer": 3, "explain": "MERGE handles matched updates and new inserts atomically."},
  {"q": "Analysts need read access to one schema only. Grants?", "choices": ["GRANT ALL", "USAGE on catalog + schema, SELECT on schema", "MODIFY on catalog", "No grants needed"], "answer": 1, "explain": "Least privilege: USAGE to navigate, SELECT to read, nothing else."},
  {"q": "'Queries filter on customer_id but scan everything.' Fix?", "choices": ["More clusters", "Z-ORDER BY customer_id", "OPTIMIZE only", "Smaller warehouse"], "answer": 1, "explain": "Z-ORDER colocates customer_id values so files can be skipped."},
  {"q": "Idempotent bulk load of new Parquet files?", "choices": ["INSERT OVERWRITE", "Manual file copy", "COPY INTO with mergeSchema", "TRUNCATE first"], "answer": 2, "explain": "COPY INTO tracks loaded files and will not reload them."},
  {"q": "'Which dashboards break if column X changes?' Answered by:", "choices": ["Unity Catalog lineage", "Grep through notebooks", "Asking around", "Guessing"], "answer": 0, "explain": "Lineage tracks column-level upstream/downstream automatically."},
  {"q": "Photon is:", "choices": ["A storage format", "A governance catalog", "A notebook type", "The vectorized query engine for faster scans/aggregations"], "answer": 3, "explain": "Photon accelerates query execution; Delta Lake is the storage format."},],
 "drills": [{"id": "il26-m07-dbx", "title": "Databricks drills", "items": [
   {"prompt": "Delta Lake file format base?", "answer": "Parquet", "explain": "Delta adds a transaction log over Parquet."},
   {"prompt": "ACID stands for?", "answer": "Atomicity, Consistency, Isolation, Durability", "explain": "The transaction guarantees."},
   {"prompt": "OPTIMIZE does what?", "answer": "Compacts small files", "explain": "Reduces file-count overhead."},
   {"prompt": "Z-ORDER does what?", "answer": "Colocates related data for file skipping", "explain": "Multi-dimensional clustering."},
   {"prompt": "Unity Catalog object above schema?", "answer": "Catalog", "explain": "Catalog -> schema -> table."},
   {"prompt": "VACUUM does what (caution)?", "answer": "Deletes old data files beyond retention (breaks time travel past that)", "explain": "Retention default 7 days; lowering it is risky."}]}],
 "handsOnLab": {"id": "il26-m07-lab", "title": "Delta Lake operations lab", "brief": "Practice the Delta operations the exam tests: MERGE upserts, time travel audits, COPY INTO loads, and OPTIMIZE/Z-ORDER tuning.",
  "steps": ["Create a Delta table and load day-1 data with COPY INTO.", "Upsert day-2 changes with MERGE INTO; verify row counts.", "Time-travel to the pre-merge version and diff the two versions.", "Write many small files, measure a filter query, then OPTIMIZE + Z-ORDER and re-measure.", "Set Unity Catalog-style grants (documented) and a data-quality alert query."],
  "deliverable": "Operation log with before/after metrics, grant documentation, alert query.",
  "checkpoint": "Time-travel diff shows exactly the merged changes; post-OPTIMIZE query scans fewer files."},
 "mockTask": {"id": "il26-m07-mock", "type": "choice", "q": "Scenario: a dashboard's numbers changed overnight with no code change. Fastest root-cause path?", "choices": ["Rebuild the dashboard.", "Time-travel the source Delta table to compare versions and check the load job's audit log.", "Blame the BI tool.", "Clear the cache and hope."], "answer": 1, "explain": "VERSION AS OF diffs isolate data changes from code changes; the load log names the job. Data drift is diagnosed, not rebuilt away."},
 "crossLinks": [],
 "videoPlaceholders": False}}

MODULES += [M06, M07]

check(MODULES)
json.dump({"modules": MODULES}, open(OUT + "/flesh_b.json", "w"), indent=1)
print("flesh_b.json written:", len(MODULES), "modules")

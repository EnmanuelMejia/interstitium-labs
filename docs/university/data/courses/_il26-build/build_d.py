# Batch D: IL-26 M16-M18, M25, M35-M38 (original content)
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

M16 = {"id": "IL26-M16", "patch": {
 "objectives": [
  "Write nested logical formulas (IFS, nested IF, SWITCH) and lookup formulas (XLOOKUP, INDEX-MATCH) that survive copying and auditing.",
  "Build pivot tables with slicers and calculated fields to answer ad-hoc business questions in minutes.",
  "Clean data with Power Query: unpivot, split, type-fix, and merge — reproducibly.",
  "Design spreadsheet models with inputs/assumptions separated, auditable formulas, and error checks."],
 "notes": [
  {"title": "Logical formulas: IFS, SWITCH, and nested logic done right",
   "body": "IFS tests conditions in order and returns the first match; SWITCH matches exact values; nested IFs work but rot quickly. Guard every logical formula with a catch-all (TRUE as the last IFS condition) so unexpected inputs can't slip through silently.\n\nWorked example (with solution):\n```text\nRisk tier from days-overdue in D2:\n=IFS(D2=0, \"Current\", D2<=30, \"Watch\", D2<=60, \"Elevated\", D2<=90, \"High\", TRUE, \"Critical\")\nOrder matters: D2=45 hits D2<=60 before D2<=90. The TRUE catch-all\ncatches negatives and text (data errors become 'Critical' -> visible,\nnot silently blank).\nSWITCH for exact codes: =SWITCH(C2, \"W\",\"West\", \"E\",\"East\", \"N\",\"North\", \"S\",\"South\", \"Unknown\")\nAudit rule: any logical formula without a catch-all is a bug waiting for\nthe one input you didn't imagine.\n```"},
  {"title": "Lookups: XLOOKUP and INDEX-MATCH",
   "body": "XLOOKUP(value, lookup_array, return_array, [if_not_found]) searches in any direction with exact match by default. INDEX-MATCH is the legacy flexible combo. Absolute-reference the arrays ($A$2:$A$100) so formulas copy safely down columns.\n\nWorked example (with solution):\n```text\nPrice lookup: product code in B2, price table codes in $F$2:$F$500,\nprices in $G$2:$G$500:\n=XLOOKUP(B2, $F$2:$F$500, $G$2:$G$500, \"NOT FOUND\") * C2\nThe \"NOT FOUND\" fourth argument turns missing codes into visible errors\ninstead of #N/A cascades. Multiply by quantity C2 inline.\nTwo-column return (price AND category):\n=XLOOKUP(B2, $F$2:$F$500, $G$2:$H$500, \"NOT FOUND\")  -- spills both columns\nINDEX-MATCH equivalent: =INDEX($G$2:$G$500, MATCH(B2, $F$2:$F$500, 0))\n```"},
  {"title": "Pivot tables: ad-hoc analysis in minutes",
   "body": "Pivot tables are GROUP BY with a GUI: rows/columns/filters/values. Add slicers for stakeholder-friendly filtering, use 'Show Values As' (% of total, running total, difference from), and refresh discipline (data changes -> refresh, or the pivot lies).\n\nWorked example (with solution):\n```text\nQuestion: 'Which sales rep beats target most consistently by quarter?'\nPivot: Rows=Rep, Columns=Quarter, Values=SUM(Revenue) AND SUM(Target),\nthen a calculated field = SUM(Revenue)/SUM(Target) formatted as %.\n'Show Values As -> % Difference From -> Previous Quarter' reveals momentum.\nSlicer on Region lets the stakeholder self-serve.\nTrap: pivots cache data. After the source updates, RIGHT-CLICK -> Refresh\n(or the numbers are stale and nobody tells you).\n```"},
  {"title": "Power Query: cleaning you can rerun",
   "body": "Power Query (Get & Transform) records every cleaning step as re-runnable M code: split columns, unpivot, fix types, merge queries, fill down. The month-end report becomes 'Refresh All' instead of a morning of manual fixes.\n\nWorked example (with solution):\n```text\nMonthly CSV arrives with: dates as text 'Jan-2026', amounts with '$' and\ncommas, region in merged header cells.\nPower Query steps:\n1. Promote headers; fill down region (merged cells).\n2. Replace '$' and ',' in amount; change type to Decimal.\n3. Parse date text to Date type.\n4. Unpivot the 12 month columns into (Month, Value) rows.\nSave as the month-end template: next month, drop in the new CSV and\nRefresh. Manual cleaning time: 2 hours -> 2 minutes, and auditable.\n```"},
  {"title": "Model design: inputs, calcs, outputs, checks",
   "body": "Professional models separate: INPUTS (assumptions, blue cells), CALCULATIONS (formulas only), OUTPUTS (results/charts), CHECKS (balance/error tests). No hard-coded numbers inside formulas — every assumption lives in INPUTS and is referenced.\n\nWorked example (with solution):\n```text\nForecast model layout:\n[Inputs]      Growth rate: 8% (B2, blue) | Churn: 3% (B3, blue)\n[Calcs]       =B2-B3 for net growth; revenue_t+1 = revenue_t*(1+net)\n[Outputs]     12-month revenue table + chart\n[Checks]     =IF(SUM(checks)<>0,\"ERROR\",\"OK\"): e.g., customer count\n              continuity (start + adds - churns = end), no negative revenue.\nHard-coded sin: =100000*1.08^12 (where did 8% come from? unauditable).\nVirtue: =B5*(1+$B$2)^12 (assumption visible, changeable, documented).\n```"}],
 "cards": [
  {"front": "IFS catch-all pattern?", "back": "TRUE as the last condition: =IFS(..., TRUE, \"fallback\")."},
  {"front": "XLOOKUP 4th argument?", "back": "if_not_found: turns missing keys into visible text instead of #N/A cascades."},
  {"front": "Why absolute-reference lookup arrays?", "back": "So the range doesn't shift when the formula copies down."},
  {"front": "Pivot 'Show Values As' gives what?", "back": "% of total, running total, difference from previous — built-in comparative views."},
  {"front": "Pivot trap after source data updates?", "back": "Stale cache: must Refresh or the numbers lie silently."},
  {"front": "Power Query's superpower?", "back": "Recorded, re-runnable cleaning steps (M code) — Refresh replaces manual redo."},
  {"front": "Model layout: 4 zones?", "back": "Inputs (assumptions), Calculations, Outputs, Checks."},
  {"front": "Hard-coded numbers in formulas: rule?", "back": "Never: every assumption lives in Inputs and is referenced."}],
 "quiz": [
  {"q": "Risk tier from D2 (days overdue): 0=Current, <=30 Watch, <=60 Elevated, <=90 High, else Critical. Formula?", "choices": ["Nested IFs without fallback", "=D2*0.05", "=IFS(D2=0,\"Current\",D2<=30,\"Watch\",D2<=60,\"Elevated\",D2<=90,\"High\",TRUE,\"Critical\")", "=SWITCH(D2)"], "answer": 2, "explain": "IFS in ascending order with TRUE catch-all handles every input including data errors."},
  {"q": "Price lookup with visible handling of missing codes?", "choices": ["=XLOOKUP(B2,$F$2:$F$500,$G$2:$G$500,\"NOT FOUND\")", "=VLOOKUP(B2,F:G,2)", "=B2*G2", "=SUM(F:G)"], "answer": 0, "explain": "XLOOKUP's 4th argument surfaces missing keys; absolute refs keep the range fixed on copy."},
  {"q": "'Rep vs target by quarter with momentum': pivot setup?", "choices": ["Rows=Rep, Values=SUM(Revenue)", "Rows=Rep, Columns=Quarter, Values=SUM(Revenue)/SUM(Target), Show Values As % Difference From previous", "One big table", "A pie chart"], "answer": 1, "explain": "Columns=Quarter enables the % Difference From previous-quarter momentum view."},
  {"q": "After the source data updates, a pivot table:", "choices": ["Auto-updates", "Breaks", "Deletes itself", "Must be refreshed or it shows stale numbers"], "answer": 3, "explain": "Pivots cache; refresh discipline is part of the workflow."},
  {"q": "Sum revenue (C) where region (A)='West' and month (B)='Jan'?", "choices": ["=SUM(C:C)", "=SUMIFS(C:C,A:A,\"West\",B:B,\"Jan\")", "=SUMIF(C:C,\"West\")", "=AVERAGE(C:C)"], "answer": 1, "explain": "SUMIFS takes multiple criteria_range/criteria pairs."},
  {"q": "Model check formulas (ERROR/OK flags) exist to:", "choices": ["Decorate", "Speed up", "Format", "Visibly catch imbalances like broken continuity"], "answer": 3, "explain": "Checks make model errors shout instead of hiding in totals."},
  {"q": "Unpivot in Power Query is for?", "choices": ["Turning month columns into (Month, Value) rows", "Deleting data", "Merging tables", "Sorting"], "answer": 0, "explain": "Unpivot converts wide time columns into long tidy rows."},
  {"q": "Volatile functions (NOW, OFFSET, INDIRECT) in large models?", "choices": ["Always use them", "They are the fastest", "Avoid: they recalculate constantly and slow models", "Required for pivots"], "answer": 2, "explain": "Volatile functions recalc on every change; they are the classic slow-model cause."},],
 "drills": [{"id": "il26-m16-excel", "title": "Excel drills", "items": [
   {"prompt": "SUMIFS revenue (C) where region (A)='West' and month (B)='Jan'?", "answer": "=SUMIFS(C:C,A:A,\"West\",B:B,\"Jan\")", "explain": "Multiple criteria pairs."},
   {"prompt": "COUNTIF orders > 500 in B2:B100?", "answer": "=COUNTIF(B2:B100,\">500\")", "explain": "Criteria as string."},
   {"prompt": "AVERAGEIF non-blank?", "answer": "=AVERAGEIF(C:C,\"<>\")", "explain": "Excludes blanks."},
   {"prompt": "TEXT date as 'mmm-yyyy'?", "answer": "=TEXT(A2,\"mmm-yyyy\")", "explain": "Format codes in TEXT."},
   {"prompt": "IFERROR wrapper purpose?", "answer": "Replace error values with a fallback", "explain": "=IFERROR(formula, \"check\")."},
   {"prompt": "Absolute vs mixed reference?", "answer": "$A$1 locks both; $A1/A$1 lock one axis", "explain": "F4 cycles the lock."}]}],
 "handsOnLab": {"id": "il26-m16-lab", "title": "Month-end close workbook", "brief": "Build a month-end workbook: Power Query cleaning, pivot analysis with slicers, a forecast model with inputs/checks, and a one-page summary.",
  "steps": ["Clean the raw extract with Power Query (recorded steps).", "Build 2 pivot tables answering stakeholder questions + slicers.", "Build the forecast model: Inputs/Calcs/Outputs/Checks zones.", "Add check formulas that flag imbalances visibly.", "Write the one-page summary sheet (takeaway-first)."],
  "deliverable": "Workbook with query steps, pivots, model, checks, summary.",
  "checkpoint": "Refresh All reproduces the analysis on new data; checks show OK; no hard-coded assumptions in formulas."},
 "mockTask": {"id": "il26-m16-mock", "type": "choice", "q": "Interview: 'A 50MB Excel model is slow and full of hard-coded numbers. How do you fix it?'", "choices": ["Buy a faster computer.", "Separate inputs/calculations/outputs/checks, replace hard-codes with referenced assumptions, replace volatile/slow formulas, consider Power Query + data model for the heavy lifting.", "Split into 10 files.", "Convert to PDF."], "answer": 1, "explain": "The professional fix is structural (zones, referenced assumptions) plus mechanical (kill volatile functions, move heavy transforms to Power Query)."},
 "crossLinks": [{"course": "il-15-data-engineering-analytics-interview-prep", "moduleId": "data-analyst-interview-prep--sheets-modeling", "topic": "Spreadsheets and modeling", "why": "Existing spreadsheet modeling module pairs with this Excel/Sheets power module."}],
 "videoPlaceholders": False}}

MODULES += [M16]

M17 = {"id": "IL26-M17", "patch": {
 "objectives": [
  "Apply data-privacy fundamentals (PII identification, minimization, masking, retention) to analyst workflows.",
  "Explain GDPR/CCPA-style rights (access, deletion, opt-out) at the level an analyst needs for compliant analysis.",
  "Design ethical analyses: consent, fairness checks, and honest communication of uncertainty and limits.",
  "Build governance habits: data dictionaries, lineage notes, access justification, and audit-ready documentation."],
 "notes": [
  {"title": "PII: find it, minimize it, mask it",
   "body": "PII = data identifying a person (name, email, SSN, device IDs, precise location). Quasi-identifiers (ZIP + birthdate + gender) re-identify when combined. Analyst rules: collect the minimum, mask in extracts (hash/tokenize/last-4), never email raw PII, and set retention/expiry on every extract.\n\nWorked example (with solution):\n```python\n# Safe analyst extract: hash the email (joinable but not readable),\n# keep only last-4 of phone, drop exact address for ZIP.\nimport hashlib\ndef tokenize(v): return hashlib.sha256(v.encode()).hexdigest()[:16]\n# email -> tokenize(email); phone -> '***-***-' + phone[-4:]; address -> zip only\n# The extract answers the churn question WITHOUT exposing identities.\n# Document: purpose, columns, masking applied, expiry date, approver.\n# Rule: if the analysis doesn't need the identifier, it doesn't ship.\n```"},
  {"title": "Privacy rights an analyst must respect",
   "body": "Modern privacy regimes grant: right to access (see my data), deletion/erasure, opt-out of sale/sharing, and data portability. For analysts this means: honor deletion requests across marts (not just the source), respect opt-out flags in every audience build, and never re-identify anonymized data.\n\nWorked example (with solution):\n```text\nDeletion request arrives for user 48291.\nChecklist:\n1. Source systems: delete/anonymize per policy.\n2. Warehouse marts: rebuild affected partitions (Type-2 dims, aggregates).\n3. Extracts: expire/purge any analyst CSVs containing the user.\n4. Backups: covered by retention policy (documented, not instant).\n5. ML features: retrain or document exclusion.\nThe analyst's job: know WHERE the user's data lives (lineage) and confirm\neach copy's disposition. 'Deleted from prod' is not 'deleted everywhere'.\n```"},
  {"title": "Fairness: check your models and metrics for bias",
   "body": "Analyses can encode bias: training on historical decisions bakes in past discrimination; proxies (ZIP code for race) sneak past removed attributes. Fairness checks: compare error rates and outcomes across groups, test with/without suspect features, and document limitations.\n\nWorked example (with solution):\n```python\n# Fairness audit: approval rates by group for a lead-scoring model.\nimport pandas as pd\ndf = pd.DataFrame({\n    'group': ['A','A','B','B'],\n    'approved': [82, 78, 61, 59],  # per 100 applicants, two periods\n    'applicants': [100, 100, 100, 100]})\nrates = df.groupby('group')['approved'].mean()\nprint(rates)  # A: 80.0, B: 60.0 -> 20-point gap demands investigation\n# Next: check whether the gap persists after controlling for legitimate\n# risk factors; if it does, the model (or the process) needs remediation.\n# Document the audit: method, finding, action. Silence is the failure mode.\n```"},
  {"title": "Ethics of communication: uncertainty and limits",
   "body": "Ethical analysis communication: state uncertainty (CIs, not point estimates), disclose limits (what the data cannot say), correct misreadings even when inconvenient, and never cherry-pick. The analyst's credibility is the product.\n\nWorked example (with solution):\n```text\nDishonest: 'The campaign lifted conversion 25%!' (relative %, no CI, no caveats).\nHonest: 'Conversion rose from 4.0% to 5.0% (+1.0pp, 95% CI +0.2 to +1.8).\nThe test ran 2 weeks; novelty effects may inflate early results. The lift\nis significant but the lower bound is small: recommend a 4-week holdout\nbefore full rollout.'\nSame data. One version informs a decision; the other manufactures one.\nEthics is a communication discipline, not just a data-handling one.\n```"},
  {"title": "Governance habits: dictionaries, lineage, access",
   "body": "Governance for analysts = boring excellence: a data dictionary for every mart (definitions, owners, refresh cadence), lineage notes (where each column came from), access justification (why you have it), and versioned analysis code. Audits are easy when the paperwork already exists.\n\nWorked example (with solution):\n```text\nData dictionary entry (the minimum viable governance):\n  table: mart_daily_revenue\n  owner: Analytics Eng | refresh: daily 06:00 ET | SLA: 09:00 ET\n  grain: one row per date x region\n  columns:\n    date        DATE        'Transaction date (ET)'\n    region      VARCHAR     'Sales region, standardized list'\n    revenue     DECIMAL     'Net paid revenue USD; excludes refunds'\n  lineage: raw_orders -> stg_orders (dbt) -> mart_daily_revenue\n  access: analysts role (SELECT); no PII columns present\nWrite this BEFORE the dashboard, not during the audit.\n```"}],
 "cards": [
  {"front": "PII vs quasi-identifiers?", "back": "PII directly identifies; quasi-identifiers (ZIP+birthdate+gender) re-identify in combination."},
  {"front": "Analyst PII rules (4)?", "back": "Minimize, mask (hash/tokenize/last-4), never email raw, set extract expiry."},
  {"front": "Deletion request: analyst checklist?", "back": "Source, marts (rebuild partitions), extracts (purge), backups (retention policy), ML features."},
  {"front": "Fairness audit: first computation?", "back": "Outcome/error rates by group; investigate gaps, test without suspect features."},
  {"front": "Honest vs dishonest lift reporting?", "back": "Honest: effect + CI + limits + recommendation. Dishonest: bare relative %."},
  {"front": "Data dictionary minimum fields?", "back": "Owner, refresh/SLA, grain, column definitions, lineage, access."},
  {"front": "Proxy discrimination example?", "back": "ZIP code standing in for race after removing the race column."},
  {"front": "'Deleted from prod' vs 'deleted everywhere'?", "back": "Marts, extracts, and features still hold copies — disposition each via lineage."}],
 "quiz": [
  {"q": "Analyst extract needs emails for joining but not reading. Correct?", "choices": ["Hash/tokenize emails (joinable, not readable)", "Include raw emails", "Drop the join", "Email the extract"], "answer": 0, "explain": "Hashed join keys preserve the analysis while minimizing exposure."},
  {"q": "ZIP + birthdate + gender together are:", "choices": ["Not PII", "Safe to publish", "Encrypted", "Quasi-identifiers: re-identifying in combination"], "answer": 3, "explain": "Quasi-identifier combos famously re-identify 'anonymized' datasets."},
  {"q": "A deletion request arrives. The analyst's FIRST move?", "choices": ["Ignore it", "Use lineage to find every copy (marts, extracts, features) and disposition each", "Delete one prod row", "Ask legal to handle everything"], "answer": 1, "explain": "Copies proliferate; lineage tells you where they all live."},
  {"q": "Lead-scoring approval: group A 80%, group B 60%. First step?", "choices": ["Ship it", "Delete group B's data", "Investigate: control for legitimate factors, test without suspect features, document", "Lower the threshold"], "answer": 2, "explain": "A 20-point gap demands a fairness investigation before any deployment."},
  {"q": "Which lift report is ethical?", "choices": ["'Conversion +25%!'", "'4.0% to 5.0% (+1.0pp, 95% CI +0.2 to +1.8); novelty may inflate; recommend holdout'", "No reporting", "Only the p-value"], "answer": 1, "explain": "Effect + uncertainty + limits + recommendation: the honest stack."},
  {"q": "Every analyst extract should document:", "choices": ["Purpose, columns, masking, expiry, approver", "Nothing", "Only the SQL", "The analyst's name"], "answer": 0, "explain": "Purpose-limited, masked, expiring, approved: the governance minimum."},
  {"q": "Removing the 'race' column guarantees a fair model?", "choices": ["Yes", "Yes if accuracy drops", "Only for small data", "No: proxies like ZIP code carry the signal anyway"], "answer": 3, "explain": "Proxy discrimination survives column removal; audit outcomes by group."},
  {"q": "A data dictionary's most important line?", "choices": ["The table name", "The owner", "Grain + column definitions with business meaning", "The refresh time"], "answer": 2, "explain": "Grain and definitions prevent the misreadings that cause wrong analyses."},],
 "drills": [{"id": "il26-m17-gov", "title": "Governance drills", "items": [
   {"prompt": "Three masking techniques?", "answer": "Hashing, tokenization, truncation (last-4)", "explain": "The analyst's masking toolkit."},
   {"prompt": "Privacy rights (4)?", "answer": "Access, deletion, opt-out of sale/sharing, portability", "explain": "The analyst-relevant rights."},
   {"prompt": "Data minimization means?", "answer": "Collect/use the least data needed for the purpose", "explain": "Less data, less risk."},
   {"prompt": "Lineage answers?", "answer": "Where did this column come from; what depends on it", "explain": "Impact analysis + deletion tracking."},
   {"prompt": "Retention policy covers?", "answer": "How long data/extracts/backups are kept, then purged", "explain": "Deletion has a documented timeline."},
   {"prompt": "Cherry-picking is?", "answer": "Reporting only favorable cuts of the analysis", "explain": "An ethics violation in communication."}]}],
 "handsOnLab": {"id": "il26-m17-lab", "title": "Privacy-safe analysis lab", "brief": "Take a PII-heavy dataset, produce a masked analyst extract with full documentation, run a fairness audit, and write the dictionary entry.",
  "steps": ["Inventory PII and quasi-identifiers in the raw table.", "Build the masked extract (hash/tokenize/truncate) with documented purpose and expiry.", "Run the analysis on the masked extract; verify the join still works.", "Fairness-audit one outcome across two groups; document method and finding.", "Write the data dictionary entry for the extract."],
  "deliverable": "Masked extract + documentation + fairness audit + dictionary entry.",
  "checkpoint": "No raw PII in the extract; the fairness audit names its method and next action."},
 "mockTask": {"id": "il26-m17-mock", "type": "choice", "q": "A manager asks for 'the full customer table including SSNs' for a churn model. What do you do?", "choices": ["Send it; they're senior.", "Refuse outright with no alternative.", "Provision a masked, purpose-documented, expiring extract without SSNs (hashed join keys), and explain why raw SSNs can't ship.", "Send a sample of 10 rows."], "answer": 2, "explain": "Least privilege with a workable alternative: the analysis proceeds, the exposure doesn't. Document purpose, masking, expiry."},
 "crossLinks": [{"course": "il-25-cybersecurity-professional-certificate", "moduleId": "IL25-M22", "topic": "Policy and privacy, regulation, and data governance", "why": "Teaches the regulatory/governance framing this module applies to analytics data."}],
 "videoPlaceholders": False}}

M18 = {"id": "IL26-M18", "patch": {
 "objectives": [
  "Run stakeholder discovery: extract the real decision, deadline, and definition of done before touching data.",
  "Manage expectations with written confirmations, interim updates, and honest renegotiation when scope or data slips.",
  "Present findings in pyramid structure (answer first), tailored to executive vs technical audiences.",
  "Handle difficult dynamics: moving goalposts, data disputes, and 'just get me the number' pressure without caving."],
 "notes": [
  {"title": "Discovery: the 15 minutes that save 15 hours",
   "body": "Every request gets discovery before data: What decision will this inform? By when? What does 'done' look like? Which metric definition? What will you do if the answer is X vs Y? The stakeholder who can't answer is telling you the request isn't real yet.\n\nWorked example (with solution):\n```text\nRequest: 'Can you pull churn numbers?'\nDiscovery (5 questions, 15 minutes):\n1. Decision: 'We're deciding whether to fund the win-back campaign.'\n2. Deadline: 'Board deck Friday.'\n3. Definition: 'Logo churn or revenue churn? Which date range?'\n4. Done looks like: 'One slide: churn by cohort with the campaign breakeven.'\n5. If X vs Y: 'If churn > 8%, we fund; under 5%, we kill it.'\nResult: a scoped, decision-shaped deliverable instead of a 'churn numbers'\nswamp. Send the written confirmation email before starting.\n```"},
  {"title": "Written confirmations and expectation management",
   "body": "After discovery, send the confirmation: decision, deadline, definitions, deliverable, and caveats. Interim updates ('on track, found a data gap in X, still Friday') prevent surprise slips. When scope creeps, renegotiate explicitly: 'I can add Y if we move the deadline to Tuesday or drop Z.'\n\nWorked example (with solution):\n```text\nConfirmation email template:\nSubject: Confirming: churn analysis for win-back decision (due Fri)\n- Decision: fund/kill win-back campaign\n- Metric: logo churn, monthly cohorts, Jan-Jun 2026\n- Deliverable: one slide + appendix, by Fri 2pm\n- Caveat: March data has a tracking gap (noted in appendix)\n- If blocked: I'll flag by Wed noon with options\nThis email IS the contract. Scope changes arrive as replies to it,\nnot as hallway ambushes.\n```"},
  {"title": "Pyramid presentations: answer first",
   "body": "Pyramid principle: lead with the answer, then the supporting arguments, then the data. Executives get the one-slide version; technical audiences get the appendix. Never open with methodology — it buries the decision.\n\nWorked example (with solution):\n```text\nBad opening: 'We pulled data from three sources, cleaned it with...' (eyes glaze).\nPyramid opening:\n'RECOMMENDATION: Fund the win-back campaign.\n - Churn is 9.2%, above the 8% funding threshold.\n - Win-back converts 22% of churned logos at $41 CAC vs $120 new-logo CAC.\n - Risk: March tracking gap; sensitivity analysis holds above 8% regardless.'\nThen: the one chart. Then: 'Details in the appendix.'\nThe executive decides in 60 seconds; the analyst's rigor lives underneath.\n```"},
  {"title": "'Just get me the number': holding the line kindly",
   "body": "Pressure for a fast number without definitions is how bad decisions get made. The senior move: deliver a fast DIRECTIONAL answer with written caveats, while the rigorous version runs. Never let a caveat-free number leave your hands.\n\nWorked example (with solution):\n```text\n'Board needs the number in an hour!'\nResponse: 'I'll send a directional estimate by 3pm with caveats in writing;\nthe audited number follows tomorrow 10am. The estimate uses [definition];\nit excludes [segment] because that table isn't refreshed yet.'\nSend BOTH the number AND the caveats in the same message (caveats in a\nseparate doc get separated from the number in forwarding).\nWhat you never do: silently ship the quick number as final. That number\nwill outlive your caveats in every forwarded deck.\n```"},
  {"title": "Disputes and moving goalposts",
   "body": "Data disputes: reproduce their number first (you'll often find the definition difference), then reconcile definitions in writing. Moving goalposts: name it kindly ('This is a new question — I'll scope it separately'), and protect the original deliverable's deadline.\n\nWorked example (with solution):\n```text\n'Your churn number doesn't match Finance's!'\nPlaybook:\n1. Reproduce Finance's number exactly (find their definition).\n2. Typical finding: Finance uses revenue churn, you used logo churn.\n3. Write the reconciliation: 'Finance 6.1% (revenue), Analytics 9.2% (logo).\n   Both correct under their definitions. Recommend: report both, label clearly.'\n4. Add both to the metrics layer so the dispute never recurs.\nYou win disputes by reproducing, not by arguing. Definitions end them.\n```"}],
 "cards": [
  {"front": "Discovery's 5 questions?", "back": "Decision? Deadline? Definition? Done-looks-like? If X vs Y?"},
  {"front": "The confirmation email contains?", "back": "Decision, deadline, definitions, deliverable, caveats — the contract."},
  {"front": "Pyramid principle?", "back": "Answer first, then supporting arguments, then data."},
  {"front": "'Just get me the number' response?", "back": "Directional estimate WITH written caveats now; audited number later. Never a caveat-free number."},
  {"front": "Data dispute playbook?", "back": "Reproduce their number, find the definition difference, reconcile in writing, add to metrics layer."},
  {"front": "Moving goalposts response?", "back": "Name it kindly; scope the new question separately; protect the original deadline."},
  {"front": "Why send caveats WITH the number?", "back": "Caveats in a separate doc get separated in forwarding; the number outlives them."},
  {"front": "Interim updates prevent?", "back": "Surprise slips: 'on track / found gap X / still Friday' beats silence."}],
 "quiz": [
  {"q": "A stakeholder asks for 'churn numbers.' Your first move?", "choices": ["Pull the numbers immediately", "Discovery: decision, deadline, definition, done-looks-like, X-vs-Y", "Ask Finance", "Build a dashboard"], "answer": 1, "explain": "Fifteen minutes of discovery prevents fifteen hours of wrong analysis."},
  {"q": "The confirmation email's job?", "choices": ["To serve as the written contract: decision, deadline, definitions, deliverable, caveats", "To be polite", "To show off", "To CC managers"], "answer": 0, "explain": "Scope changes arrive as replies to the contract, not hallway ambushes."},
  {"q": "Pyramid presentations lead with:", "choices": ["Methodology", "Data sources", "The appendix", "The answer/recommendation"], "answer": 3, "explain": "Answer first, then support, then data. Executives decide in 60 seconds."},
  {"q": "'Board needs the number in an hour!' Best response?", "choices": ["Refuse", "Guess", "Directional estimate with written caveats now; audited number tomorrow", "Ship the quick number as final"], "answer": 2, "explain": "Speed with honesty: caveats travel WITH the number, and the rigorous version follows."},
  {"q": "A stakeholder adds a second question mid-analysis. Response?", "choices": ["Absorb silently", "Drop the original", "Say no", "Scope it separately; protect the original deadline"], "answer": 3, "explain": "Kind naming of the new question keeps both deliverables healthy."},
  {"q": "Finance's churn (6.1%) vs yours (9.2%). Playbook?", "choices": ["Argue yours is right", "Average them", "Reproduce theirs, find the definition difference (revenue vs logo), reconcile in writing", "Hide yours"], "answer": 2, "explain": "Reproduce, do not argue. Definitions end disputes; add both to the metrics layer."},
  {"q": "Scope creep mid-analysis: response?", "choices": ["'I can add Y if we move the deadline or drop Z' - renegotiate explicitly", "Silently absorb it", "Quit", "Ship late silently"], "answer": 0, "explain": "Explicit trade-offs protect quality and trust; silent absorption guarantees a miss."},
  {"q": "Interim update cadence for a Friday deadline?", "choices": ["None until Friday", "At least one mid-week: on track / gaps found / still Friday", "Hourly", "Only if failing"], "answer": 1, "explain": "No-surprise updates are the cheapest trust insurance in stakeholder work."},],
 "drills": [{"id": "il26-m18-stake", "title": "Stakeholder drills", "items": [
   {"prompt": "First question in discovery?", "answer": "What decision will this inform?", "explain": "Decisions shape everything downstream."},
   {"prompt": "Definition of done example?", "answer": "One slide: churn by cohort with campaign breakeven, by Fri 2pm", "explain": "Concrete, dated, formatted."},
   {"prompt": "Pyramid order?", "answer": "Answer -> arguments -> data", "explain": "Top-down communication."},
   {"prompt": "Caveat placement?", "answer": "With the number, same message", "explain": "Separated caveats get lost in forwarding."},
   {"prompt": "Reproduce before?", "answer": "Arguing (in data disputes)", "explain": "Reproduction finds the definition gap."},
   {"prompt": "New question mid-flight?", "answer": "Scope separately; protect original deadline", "explain": "Kind naming of goalpost moves."}]}],
 "handsOnLab": {"id": "il26-m18-lab", "title": "Stakeholder simulation", "brief": "Run a full stakeholder cycle on a vague request: discovery, confirmation email, analysis, pyramid presentation, and a dispute reconciliation.",
  "steps": ["Receive the vague request ('look into engagement').", "Conduct discovery (write the 5 answers).", "Send the confirmation email.", "Do the analysis; prepare the pyramid one-slide + appendix.", "Handle the planted dispute: reproduce, reconcile definitions, update the metrics layer note."],
  "deliverable": "Discovery notes, confirmation email, one-slide + appendix, dispute reconciliation.",
  "checkpoint": "The one-slide states the recommendation in its title; the dispute doc names both definitions."},
 "mockTask": {"id": "il26-m18-mock", "type": "choice", "q": "An executive forwards your caveated estimate WITHOUT the caveats, and it becomes 'the number.' What do you do?", "choices": ["Nothing; it's out there.", "Reply-all with the caveats and the audited timeline, kindly but firmly: 'Sharing the full context — the estimate excludes X; audited number tomorrow 10am.' Then fix the process (watermark estimates as DRAFT).", "Complain privately.", "Delete the email."], "answer": 1, "explain": "Correct the record in the same channel, visibly but kindly, and change the process so estimates can't travel naked again."},
 "crossLinks": [],
 "videoPlaceholders": False}}

MODULES += [M17, M18]

M25 = {"id": "IL26-M25", "patch": {
 "objectives": [
  "Wrangle data with dplyr: filter, select, mutate, summarize, arrange, and joins — the verbs the Google track expects.",
  "Visualize with ggplot2's layered grammar and produce publication-honest charts.",
  "Write RMarkdown reports that combine code, output, and narrative reproducibly.",
  "Translate between R/dplyr and pandas so skills transfer across the bilingual analyst workflow."],
 "notes": [
  {"title": "dplyr: the five verbs",
   "body": "filter() keeps rows, select() keeps columns, mutate() creates columns, summarise() aggregates (usually after group_by()), arrange() sorts. Piped with %>%, they read like sentences. This is the R half of the bilingual analyst.\n\nWorked example (with solution):\n```r\nlibrary(dplyr)\nresult <- orders %>%\n  filter(status == \"paid\") %>%\n  mutate(net = amount - discount,\n         month = format(order_date, \"%Y-%m\")) %>%\n  group_by(region, month) %>%\n  summarise(revenue = sum(net),\n            orders = n_distinct(order_id),\n            .groups = \"drop\") %>%\n  arrange(region, month)\n# n_distinct (not n()) avoids double-counting line items as orders:\n# the same dplyr/pandas discipline in both languages.\n```"},
  {"title": "Joins and reshaping in R",
   "body": "left_join/right_join/inner_join/full_join by a key; pivot_wider spreads long to wide; pivot_longer gathers wide to long. Join validation: check for duplicated keys before merging, or metrics fan out exactly as in pandas.\n\nWorked example (with solution):\n```r\nlibrary(tidyr)\n# Key check BEFORE the join (the fan-out guard):\nany(duplicated(customers$customer_id))  # must be FALSE for many-to-one\nm <- orders %>% left_join(customers, by = \"customer_id\")\n# Wide monthly columns -> long tidy rows:\nlong <- monthly_wide %>%\n  pivot_longer(cols = starts_with(\"m_\"),\n               names_to = \"month\", values_to = \"revenue\")\n```"},
  {"title": "ggplot2: layered grammar",
   "body": "ggplot(data, aes(x, y)) + geom_*(...) + labs(...): data, aesthetics (mappings), geometries (marks), then labels/scales/themes. Build plots additively; every layer is inspectable. Facets (facet_wrap) multiply a chart across groups — the small-multiple superpower.\n\nWorked example (with solution):\n```r\nlibrary(ggplot2)\nggplot(monthly, aes(x = month, y = revenue, color = region, group = region)) +\n  geom_line(linewidth = 1) +\n  geom_point(size = 2) +\n  facet_wrap(~ region) +\n  labs(title = \"Revenue trend by region\",\n       subtitle = \"Takeaway: West recovers in Q3 while East plateaus\",\n       x = NULL, y = \"Revenue ($K)\") +\n  theme_minimal()\n# Subtitle carries the takeaway (the dashboard title rule, in R).\n# facet_wrap gives small multiples: comparisons without overplotting.\n```"},
  {"title": "RMarkdown: reproducible reporting",
   "body": "RMarkdown interleaves narrative, code chunks, and output; knitting renders the report with fresh results every time. Set echo=FALSE for stakeholder versions (output without code), keep code visible for technical review. Reproducibility: set.seed() for randomness, relative paths, sessionInfo() recorded.\n\nWorked example (with solution):\n```r\n# Report chunk pattern:\n# ```{r monthly-chart, echo=FALSE, fig.width=8, message=FALSE}\n# ggplot(monthly, aes(month, revenue)) + geom_col() +\n#   labs(title = \"Monthly revenue\")\n# ```\n# Knit -> HTML/PDF with the chart embedded, computed from current data.\n# Stakeholder version: echo=FALSE hides code. Technical appendix: echo=TRUE.\n# set.seed(42) before any sampling/simulation for exact reproducibility.\n```"},
  {"title": "Bilingual: dplyr <-> pandas translation",
   "body": "Every dplyr verb has a pandas twin: filter->boolean mask, select->[[]], mutate->assign, summarise->agg, arrange->sort_values, group_by->groupby, left_join->merge. Learning the map doubles your employability and lets you verify results across languages.\n\nWorked example (with solution):\n```text\ndplyr                              pandas\nfilter(status==\"paid\")            df[df.status==\"paid\"]\nselect(region, revenue)            df[[\"region\",\"revenue\"]]\nmutate(net = amount-discount)      df.assign(net=df.amount-df.discount)\ngroup_by(region) %>% summarise()    df.groupby(\"region\").agg(...)\narrange(desc(revenue))             df.sort_values(\"revenue\", ascending=False)\nleft_join(customers, by=\"id\")     df.merge(customers, on=\"id\", how=\"left\")\nVerification habit: compute a KPI in both; they must match to the cent.\n```"}],
 "cards": [
  {"front": "dplyr's five verbs?", "back": "filter, select, mutate, summarise, arrange."},
  {"front": "n() vs n_distinct(order_id)?", "back": "n() counts rows; n_distinct counts unique orders (no line-item double count)."},
  {"front": "Join fan-out guard in R?", "back": "any(duplicated(key)) must be FALSE before a many-to-one join."},
  {"front": "ggplot2 layers?", "back": "data + aesthetics + geometries + labels/scales/themes."},
  {"front": "facet_wrap does what?", "back": "Small multiples: one chart panel per group."},
  {"front": "RMarkdown echo=FALSE?", "back": "Hides code, shows output — the stakeholder version."},
  {"front": "dplyr mutate -> pandas?", "back": "assign()."},
  {"front": "dplyr left_join -> pandas?", "back": "merge(..., how='left')."}],
 "quiz": [
  {"q": "Count distinct orders per region in dplyr?", "choices": ["summarise(n = n())", "summarise(n = n_distinct(order_id))", "count(region)", "tally()"], "answer": 1, "explain": "n_distinct avoids double-counting line items; n() counts rows."},
  {"q": "Wide monthly columns to long tidy rows in R?", "choices": ["pivot_wider", "spread", "pivot_longer", "gather only"], "answer": 2, "explain": "pivot_longer gathers wide columns into (name, value) rows."},
  {"q": "Before a many-to-one left_join, check:", "choices": ["any(duplicated(right$key)) is FALSE", "Row counts match", "Column names match", "Nothing"], "answer": 0, "explain": "Duplicated right-side keys fan out rows and inflate metrics."},
  {"q": "ggplot subtitle's job?", "choices": ["Decoration", "Carry the takeaway", "Show the code", "List data sources"], "answer": 1, "explain": "Titles state takeaways; subtitles carry the one-line story."},
  {"q": "Small multiples across regions in ggplot2?", "choices": ["geom_line", "labs()", "theme_minimal()", "facet_wrap(~ region)"], "answer": 3, "explain": "Facets multiply the chart across groups for clean comparison."},
  {"q": "Stakeholder RMarkdown version uses:", "choices": ["echo=FALSE (output without code)", "echo=TRUE always", "No chunks", "Raw R scripts"], "answer": 0, "explain": "Stakeholders get results; technical reviewers get code."},
  {"q": "Reproducibility requirements (3)?", "choices": ["Absolute paths", "Random seeds each run", "No version control", "set.seed(), relative paths, recorded sessionInfo()"], "answer": 3, "explain": "Seeded randomness, portable paths, recorded environment = reproducible."},
  {"q": "pandas equivalent of dplyr's arrange(desc(revenue))?", "choices": ["df.sort()", "df.order()", "df.sort_values('revenue', ascending=False)", "df.head()"], "answer": 2, "explain": "sort_values with ascending=False is the arrange(desc()) twin."},],
 "drills": [{"id": "il26-m25-r", "title": "R drills", "items": [
   {"prompt": "dplyr: keep rows where x > 5?", "answer": "filter(x > 5)", "explain": "Row filtering verb."},
   {"prompt": "dplyr: new column z = x + y?", "answer": "mutate(z = x + y)", "explain": "Column creation verb."},
   {"prompt": "ggplot geometry for points?", "answer": "geom_point()", "explain": "Scatter marks."},
   {"prompt": "ggplot geometry for bars of precomputed values?", "answer": "geom_col()", "explain": "geom_col takes heights; geom_bar counts."},
   {"prompt": "RMarkdown output formats (2)?", "answer": "HTML, PDF (also Word)", "explain": "Knit targets."},
   {"prompt": "Pipe operator?", "answer": "%>% (magrittr; base R |> also works)", "explain": "The chaining operator."}]}],
 "handsOnLab": {"id": "il26-m25-lab", "title": "Bilingual R report", "brief": "Answer a business question in R (dplyr + ggplot2 + RMarkdown), verify against pandas, and knit a stakeholder report.",
  "steps": ["Wrangle the dataset with dplyr (filter/mutate/group_by/summarise).", "Verify the KPI against the pandas version to the cent.", "Build 2 ggplot2 charts with takeaway subtitles.", "Write the RMarkdown report (narrative + echo=FALSE charts).", "Knit and confirm reproducibility (re-knit after clearing the environment)."],
  "deliverable": "Knitted HTML report + .Rmd source + pandas verification log.",
  "checkpoint": "R and pandas KPIs match; re-knit reproduces identical output."},
 "mockTask": {"id": "il26-m25-mock", "type": "choice", "q": "A team uses R; the new role is pandas-based. How do you position your R skills?", "choices": ["Hide the R background.", "As bilingual fluency: dplyr/pandas verb mapping plus a verified cross-language analysis proving transfer.", "Claim pandas expertise you don't have.", "Refuse pandas roles."], "answer": 1, "explain": "The verb map plus a reconciled bilingual artifact proves transfer honestly — stronger than claiming either side alone."},
 "crossLinks": [],
 "videoPlaceholders": False}}

M35 = {"id": "IL26-M35", "patch": {
 "objectives": [
  "Write interview-grade SQL under time pressure: window functions, CTEs, and complex joins with correct first-pass logic.",
  "Narrate your SQL thinking aloud: state assumptions, grain, and edge cases before writing.",
  "Handle follow-ups: optimize a working query, explain the plan, and adapt to schema twists.",
  "Avoid the classic interview traps: fan-out, NULL semantics, duplicate keys, and off-by-one date logic."],
 "notes": [
  {"title": "Thinking aloud: the interview meta-skill",
   "body": "Interviewers score reasoning, not just results. Narrate: restate the question, state the grain ('one row per user per day'), name edge cases (NULLs, duplicates, ties), then write. A correct query with silent assumptions scores lower than a good query with stated assumptions.\n\nWorked example (with solution):\n```text\nQ: 'Daily active users for the last 30 days.'\nAloud: 'DAU = distinct users with an event per day. Grain: one row per\nuser per day. Edge cases: duplicate events (dedupe by user+day), timezone\n(events stored UTC, business day is ET), bots (exclude flagged accounts).\nI'll assume the events table has user_id, event_at, is_bot.'\nThen write:\nSELECT DATE(CONVERT_TZ(event_at,'UTC','America/New_York')) AS day,\n       COUNT(DISTINCT user_id) AS dau\nFROM events\nWHERE event_at >= CURDATE() - INTERVAL 30 DAY AND NOT is_bot\nGROUP BY 1 ORDER BY 1;\nThe narration IS the senior signal.\n```\nIndependent prep material; no affiliation with or endorsement by Palantir."},
  {"title": "Window functions under pressure",
   "body": "The interview core: rank per group, running totals, period-over-period, top-N with ties. Write the PARTITION BY first (it names the grouping), then the ORDER BY, then the frame. Say which rank function and why before writing it.\n\nWorked example (with solution):\n```sql\n-- 'Second purchase date per customer, and days between first and second.'\nWITH ordered AS (\n  SELECT customer_id, order_date,\n         ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) AS rn\n  FROM orders\n)\nSELECT o1.customer_id, o1.order_date AS first_order,\n       o2.order_date AS second_order,\n       DATEDIFF(o2.order_date, o1.order_date) AS days_between\nFROM ordered o1\nJOIN ordered o2 ON o1.customer_id = o2.customer_id\n  AND o1.rn = 1 AND o2.rn = 2;\n-- Aloud: 'ROW_NUMBER (not RANK) because I need exactly the 1st and 2nd\n-- rows; ties broken arbitrarily by order_date, which I'll state.'\n```"},
  {"title": "Joins, fan-out, and NULL traps live",
   "body": "Under pressure, joins break two ways: fan-out (duplicated keys multiply rows) and NULL keys (dropped by inner joins). State the key-uniqueness assumption before joining; use LEFT JOIN deliberately; never NOT IN with nullable subqueries.\n\nWorked example (with solution):\n```sql\n-- 'Customers with no orders in 2026.'\n-- Trap answer: WHERE customer_id NOT IN (SELECT customer_id FROM orders ...)\n--   breaks if any order.customer_id is NULL.\n-- Senior answer:\nSELECT c.customer_id, c.name\nFROM customers c\nWHERE NOT EXISTS (\n  SELECT 1 FROM orders o\n  WHERE o.customer_id = c.customer_id\n    AND o.order_date >= '2026-01-01' AND o.order_date < '2027-01-01'\n);\n-- Aloud: 'NOT EXISTS is NULL-safe; NOT IN is not. I'm also scoping the\n-- date range explicitly rather than YEAR() so an index stays usable.'\n```"},
  {"title": "Date logic without off-by-ones",
   "body": "Half-open intervals [start, end) prevent double-counting and gaps: >= first-day AND < first-of-next. Never YEAR(x)=2026 on indexed columns; never BETWEEN with timestamps (end-of-day gaps). State the timezone.\n\nWorked example (with solution):\n```sql\n-- 'Revenue by month for 2026, no gaps, no double counts.'\nSELECT DATE_FORMAT(order_date, '%Y-%m') AS month,\n       SUM(amount) AS revenue\nFROM orders\nWHERE order_date >= '2026-01-01' AND order_date < '2027-01-01'\nGROUP BY 1 ORDER BY 1;\n-- Aloud: 'Half-open interval: includes Jan 1 00:00, excludes Jan 1 2027\n-- 00:00. BETWEEN '2026-01-01' AND '2026-12-31' would MISS Dec 31 afternoon\n-- timestamps. This is the off-by-one interviewers hunt for.'\n```"},
  {"title": "Follow-ups: optimize and adapt",
   "body": "After a working query, expect: 'Make it faster' (index the filter/join columns, avoid the sort), 'What if the schema changes?' (adapt the grain), 'How do you test it?' (row-count reconciliation, spot checks, edge-case rows). Answer structurally, not defensively.\n\nWorked example (with solution):\n```text\nFollow-up: 'This runs on 500M rows. Make it faster.'\nAnswer aloud: 'First, check the plan for a full scan: the selective filter\nis on status, so I'd index (status, order_date). Second, the GROUP BY sorts\n500M rows: pre-aggregate to a daily mart if this query runs often.\nThird, confirm stats are fresh (ANALYZE) so the planner picks hash join.\nI'd verify with EXPLAIN before and after.'\nFollow-up: 'How do you know it's right?' -> 'Reconcile: total revenue\nmatches the finance mart; spot-check 5 customers by hand; test NULL\nand duplicate edge cases explicitly.'\n```"}],
 "cards": [
  {"front": "Narrate before writing: 3 things to state?", "back": "Restated question, grain, edge cases (NULLs, dups, ties)."},
  {"front": "DAU query: grain?", "back": "One row per user per day (dedupe events to user+day)."},
  {"front": "Second purchase per customer: pattern?", "back": "ROW_NUMBER() per customer by date; self-join rn=1 to rn=2."},
  {"front": "NULL-safe 'customers with no orders'?", "back": "NOT EXISTS, not NOT IN."},
  {"front": "Date range without off-by-ones?", "back": "Half-open: >= start AND < next-start."},
  {"front": "Why not YEAR(x) = 2026 in WHERE?", "back": "Kills index use; use a sargable range."},
  {"front": "'Make it faster' answer structure?", "back": "Plan check -> index filter/join cols -> pre-aggregate if repeated -> fresh stats -> EXPLAIN verify."},
  {"front": "'How do you know it's right?'", "back": "Reconcile totals, spot-check by hand, test NULL/dup edge cases."}],
 "quiz": [
  {"q": "First thing to state aloud before writing interview SQL?", "choices": ["The table names", "Restated question, grain, and edge cases", "Your resume", "The database vendor"], "answer": 1, "explain": "Reasoning is scored: assumptions and edge cases before code."},
  {"q": "'Second purchase date per customer': correct window function?", "choices": ["RANK()", "DENSE_RANK()", "ROW_NUMBER() (need exactly 1st/2nd rows)", "NTILE(2)"], "answer": 2, "explain": "ROW_NUMBER gives exactly one row per position; RANK could return multiple 'firsts' on ties."},
  {"q": "NULL-safe anti-join?", "choices": ["NOT IN", "NOT EXISTS", "LEFT JOIN only", "EXCEPT always"], "answer": 1, "explain": "NOT IN breaks on NULLs in the subquery; NOT EXISTS is NULL-safe."},
  {"q": "'Revenue by month, 2026': correct filter?", "choices": ["WHERE YEAR(order_date)=2026", "WHERE order_date BETWEEN '2026-01-01' AND '2026-12-31'", "WHERE order_date >= '2026-01-01' AND order_date < '2027-01-01'", "WHERE order_date LIKE '2026%'"], "answer": 2, "explain": "Half-open interval: sargable, no timestamp gaps, no double counts."},
  {"q": "Ties on order_date make '3rd order' ambiguous. Best handling?", "choices": ["Ignore ties", "ROW_NUMBER is always fine", "Use LIMIT 3", "State the tie-break rule (add order_id to ORDER BY) or ask the business which tied rows count"], "answer": 3, "explain": "Name the ambiguity and resolve it with a stated rule or a business decision."},
  {"q": "Query is slow on 500M rows with a selective status filter. First fix?", "choices": ["More RAM", "Rewrite in Python", "SELECT *", "Index (status, order_date); check EXPLAIN"], "answer": 3, "explain": "Index the selective filter; verify the plan change with EXPLAIN."},
  {"q": "DAU with duplicate events: fix?", "choices": ["COUNT(DISTINCT user_id) per day", "COUNT(*)", "SUM(users)", "AVG(users)"], "answer": 0, "explain": "Dedupe to user+day grain; raw counts inflate on repeat events."},
  {"q": "Interviewer: 'What if order_date has NULLs?' Best response?", "choices": ["State the handling: exclude from date-bounded analysis and report the NULL count separately", "Ignore it", "Delete the rows silently", "Panic"], "answer": 0, "explain": "Name the edge case, state the rule, and quantify it - that is the senior signal."},],
 "drills": [{"id": "il26-m35-sqliv", "title": "SQL interview drills", "items": [
   {"prompt": "Top 2 per group, ties kept?", "answer": "DENSE_RANK() ... WHERE rnk <= 2", "explain": "Dense rank keeps ties."},
   {"prompt": "Running total?", "answer": "SUM(x) OVER (ORDER BY d ROWS UNBOUNDED PRECEDING)", "explain": "Cumulative frame (default with ORDER BY)."},
   {"prompt": "Month-over-month growth?", "answer": "(x - LAG(x) OVER (ORDER BY m)) / LAG(x) OVER (ORDER BY m)", "explain": "Lag for prior period."},
   {"prompt": "Users active in both Jan and Feb?", "answer": "INTERSECT of monthly user sets (or conditional aggregation)", "explain": "Set intersection on users."},
   {"prompt": "Median without a median function?", "answer": "PERCENTILE_CONT(0.5) or ROW_NUMBER middle", "explain": "Dialect-dependent; know both."},
   {"prompt": "Dedupe keeping latest per key?", "answer": "ROW_NUMBER() OVER (PARTITION BY key ORDER BY ts DESC) = 1", "explain": "The canonical dedup."}]}],
 "handsOnLab": {"id": "il26-m35-lab", "title": "Timed SQL circuit", "brief": "Complete 6 interview-style SQL problems in 60 minutes, narrating aloud (record yourself), then review the recording for missed edge cases.",
  "steps": ["Set a 60-minute timer; 6 problems (ranking, funnel, streaks, MoM, dedup, anti-join).", "For each: narrate (restate, grain, edge cases), then write.", "Run every query; fix errors within the timer.", "Review the recording: score narration completeness per problem.", "Rewrite the 2 weakest with full edge-case handling."],
  "deliverable": "6 solved queries + narration self-review scores + 2 rewrites.",
  "checkpoint": "Every solution states grain and NULL/dup handling; all 6 run correctly."},
 "mockTask": {"id": "il26-m35-mock", "type": "choice", "q": "Live interview: 'Find the 3rd order for each customer.' You write ROW_NUMBER() and filter rn=3. The interviewer asks 'What breaks with ties?' Your answer?", "choices": ["Nothing.", "Ties on order_date make '3rd' ambiguous: ROW_NUMBER breaks ties arbitrarily, so I'd state the tie-break rule (e.g., add order_id to the ORDER BY) or switch to RANK/DENSE_RANK if the business wants all tied rows — and ask which the business means.", "Use RANK instead silently.", "Give up."], "answer": 1, "explain": "Naming the ambiguity and offering the business-defined resolution is exactly the senior interview behavior being tested."},
 "crossLinks": [],
 "videoPlaceholders": False}}

MODULES += [M25, M35]

M36 = {"id": "IL26-M36", "patch": {
 "objectives": [
  "Solve interview probability questions (conditional, Bayes, expectation) with clean, narrated reasoning.",
  "Write pandas solutions for data-wrangling interview tasks and explain complexity trade-offs.",
  "Demonstrate product sense: frame metrics, trade-offs, and experiment designs for a product scenario.",
  "Structure behavioral answers (STAR) around data impact with quantified outcomes."],
 "notes": [
  {"title": "Probability under pressure: the interview toolkit",
   "body": "Interview probability questions reward structured counting: define the sample space, count favorable outcomes, and narrate. Bayes for 'given that' inversions; expectation for decision questions; complements for 'at least one'.\n\nWorked example (with solution):\n```text\nQ: 'A test is 95% accurate; 1% of users have the condition. Positive result:\nprobability of actually having it?'\nAloud: 'Bayes. P(D|+) = P(+|D)P(D) / P(+). P(+) = 0.95*0.01 + 0.05*0.99.'\nNumerator: 0.95 * 0.01 = 0.0095.\nDenominator: 0.0095 + 0.05*0.99 = 0.0095 + 0.0495 = 0.059.\nAnswer: 0.0095/0.059 = 0.161 -> 16%.\nCloser: 'So 84% of positives are false alarms: the base rate dominates.'\nThe closer (business implication) is what separates senior answers.\n```\nIndependent prep material; no affiliation with or endorsement by Palantir."},
  {"title": "Python/pandas live: wrangle and narrate",
   "body": "Live coding tests idiomatic pandas: groupby, merge, window-equivalents (shift, cumsum, rank), and string/datetime handling. Narrate the shape at each step ('now one row per user per day'). Avoid loops; know vectorized alternatives.\n\nWorked example (with solution):\n```python\n# 'For each user, days between signup and first purchase (null if never).'\nimport pandas as pd\nusers = pd.DataFrame({'user_id':[1,2,3], 'signup':pd.to_datetime(['2026-01-01','2026-01-05','2026-01-10'])})\norders = pd.DataFrame({'user_id':[1,1,3], 'order_date':pd.to_datetime(['2026-01-03','2026-01-09','2026-01-10'])})\nfirst = orders.groupby('user_id')['order_date'].min().rename('first_order')\nout = users.merge(first, on='user_id', how='left')\nout['days_to_first'] = (out['first_order'] - out['signup']).dt.days\nprint(out[['user_id','days_to_first']])\n# user 1: 2 days; user 2: NaN (never purchased); user 3: 0 days.\n# Aloud: 'left join keeps non-buyers as NaN; min() takes the FIRST order.'\n```"},
  {"title": "Product sense: metrics and trade-offs",
   "body": "Product-sense questions ('How would you measure success for X?') want: the goal, 2-3 key metrics (one north star + guards), segment cuts, and trade-off discussion. Structure: clarify goal -> propose metrics -> discuss gaming/risks -> experiment design.\n\nWorked example (with solution):\n```text\nQ: 'How would you measure a new onboarding flow?'\n'Goal: activate new users faster without hurting quality.\nNorth star: activation rate (key action within 7 days).\nGuards: Day-30 retention (no junk activations), support tickets/user.\nSegments: by acquisition channel and device (effects differ).\nGaming risk: teams could lower the 'activation' bar; define it as the\n  action correlated with retention, not any click.\nExperiment: randomized rollout, 2-week minimum (novelty), pre-registered\n  primary = activation, guards as veto metrics.'\nStructure + trade-offs + experiment = the complete answer.\n```"},
  {"title": "Estimation: Fermi reasoning that lands",
   "body": "Estimation questions test structured decomposition, not accuracy: break into countable pieces, state assumptions, multiply, sanity-check. Round aggressively; the structure is graded.\n\nWorked example (with solution):\n```text\nQ: 'How many queries does a data warehouse run per day at a mid-size company?'\n'50 analysts. Each runs ~20 queries/day (ad-hoc + refreshes) = 1,000.\nScheduled pipelines: 200 DAGs x 5 queries = 1,000.\nDashboards: 100 dashboards x 10 tiles x 4 refreshes = 4,000.\nTotal ~6,000/day. Sanity: that is ~4/minute average, spiky at 9am:\nplausible for mid-size. I'd state the three buckets explicitly so the\ninterviewer can correct any assumption.'\nBuckets + assumptions + sanity check = full marks.\n```"},
  {"title": "Behavioral: STAR with data quantified",
   "body": "Behavioral rounds want STAR (Situation, Task, Action, Result) with quantified data impact. Prepare 5 stories: disagreement with a stakeholder, a wrong analysis you caught, an experiment that failed, a metric you defined, mentoring. Each ends with a number.\n\nWorked example (with solution):\n```text\n' Tell me about a time your analysis changed a decision.'\nS: 'Marketing planned to cut the affiliate channel (low last-click revenue).'\nT: 'I was asked to validate the cut.'\nA: 'I ran a multi-touch attribution check and found affiliates ASSISTED\n   31% of enterprise deals that closed via direct.'\nR: 'The cut was reversed; affiliate spend was reallocated not removed.\n   Sourced pipeline from affiliates: $2.1M the next quarter.'\nThe number ($2.1M) makes it memorable; the method (attribution check)\nmakes it credible.\n```"}],
 "cards": [
  {"front": "Bayes interview closer?", "back": "State the business implication ('84% of positives are false alarms'), not just the number."},
  {"front": "95% accurate test, 1% base rate. P(condition | positive)?", "back": "~16%."},
  {"front": "pandas: days between signup and first purchase?", "back": "groupby min + left merge + dt.days; non-buyers stay NaN."},
  {"front": "Product-sense answer structure?", "back": "Goal -> metrics (north star + guards) -> segments -> gaming risks -> experiment."},
  {"front": "Fermi structure?", "back": "Buckets + stated assumptions + multiply + sanity check."},
  {"front": "STAR?", "back": "Situation, Task, Action, Result — ending with a quantified number."},
  {"front": "'At least one' probability trick?", "back": "Complement: 1 - P(none)."},
  {"front": "Guard metrics in product measurement?", "back": "Metrics that must not degrade (retention, support load); they can veto."}],
 "quiz": [
  {"q": "95%-accurate test, 1% condition rate. P(condition | positive)?", "choices": ["95%", "50%", "16%", "1%"], "answer": 2, "explain": "0.95*0.01/(0.95*0.01+0.05*0.99) = 0.0095/0.059 = 16%."},
  {"q": "pandas: first purchase per user, keeping non-buyers?", "choices": ["groupby min + left merge (non-buyers -> NaT)", "Inner merge", "dropna first", "Loop"], "answer": 0, "explain": "Left join preserves non-buyers as missing; min() takes the first order."},
  {"q": "Product question: 'measure a new onboarding flow.' The complete answer needs:", "choices": ["More charts", "A longer survey", "Bigger sample only", "A north star + guard metrics + segments + experiment plan"], "answer": 3, "explain": "Complete answers cover goal, metrics, guards, segments, gaming risks, experiment."},
  {"q": "Fermi estimate grading focuses on:", "choices": ["Exact accuracy", "Structure: buckets, assumptions, sanity check", "Speed", "Confidence"], "answer": 1, "explain": "Decomposition and stated assumptions are graded, not the final number."},
  {"q": "P(at least one success in 3 trials, p=0.5 each)?", "choices": ["0.5", "0.75", "1.0", "0.875"], "answer": 3, "explain": "1 - P(none) = 1 - 0.125 = 0.875."},
  {"q": "STAR story's most memorable element?", "choices": ["The situation", "The quantified result (the number)", "The task", "The team size"], "answer": 1, "explain": "Numbers make stories memorable; method makes them credible."},
  {"q": "Gaming risk in activation metrics?", "choices": ["Teams lower the activation bar; define it as the retention-correlated action", "No risk", "More events always better", "Ignore it"], "answer": 0, "explain": "Metrics get gamed; anchor definitions to outcomes, not clicks."},
  {"q": "Novelty effect in onboarding experiments: handle by?", "choices": ["Ship immediately", "Peek daily", "2-week minimum runtime; pre-registered primary", "No control group"], "answer": 2, "explain": "Novelty inflates early results; fixed horizons and pre-registration keep it honest."},],
 "drills": [{"id": "il26-m36-probprod", "title": "Probability + product drills", "items": [
   {"prompt": "P(both independent events, 0.3 and 0.4)?", "answer": "0.12", "explain": "Multiply."},
   {"prompt": "Expected value: 50% win $100, 50% lose $40?", "answer": "$30", "explain": "0.5*100 - 0.5*40 = 30."},
   {"prompt": "Monty Hall: switch or stay?", "answer": "Switch (2/3 vs 1/3)", "explain": "The classic conditional update."},
   {"prompt": "North star metric: definition?", "answer": "The one metric capturing core product value", "explain": "Guards protect everything else."},
   {"prompt": "Segment cuts for experiments (2)?", "answer": "Channel, device (also: tenure, region)", "explain": "Effects differ by segment."},
   {"prompt": "Pre-registration prevents?", "answer": "P-hacking / metric shopping", "explain": "Locks the decision rule upfront."}]}],
 "handsOnLab": {"id": "il26-m36-lab", "title": "Mock loop simulation", "brief": "Run a full mock loop: timed SQL, probability whiteboard, pandas live-coding, product-sense case, and one behavioral story — recorded and self-scored.",
  "steps": ["45-min timed SQL set (3 problems), narrated.", "Whiteboard 3 probability questions with closers.", "Live-code 2 pandas tasks with shape narration.", "Answer 1 product-sense case in the goal->metrics->experiment structure.", "Deliver 1 STAR story; self-score against the rubric."],
  "deliverable": "Recordings + self-score rubric with 2 improvement actions.",
  "checkpoint": "Every answer has the required structure (narration/closer/shape-talk); scores identify the weakest round."},
 "mockTask": {"id": "il26-m36-mock", "type": "choice", "q": "Case: 'Activation is up 15% after the redesign, but revenue is flat.' What is your read?", "choices": ["Celebrate activation.", "Suspect metric gaming or a diluted activation definition: check whether the marginal activated users retain and pay; cut by segment; verify the activation definition still correlates with revenue before claiming success.", "Run more ads.", "Redesign again."], "answer": 1, "explain": "Activation without revenue is a definition problem until proven otherwise — the senior move is to interrogate the metric, not the users."},
 "crossLinks": [],
 "videoPlaceholders": False}}

M37 = {"id": "IL26-M37", "patch": {
 "objectives": [
  "Explain ontology thinking: entities, relationships, and properties as the shared language between business and data.",
  "Map a business domain to an ontology: identify objects, links, and the questions each link answers.",
  "Design pipelines with ontology discipline: raw -> cleaned -> modeled (ontology objects) -> served, with contracts at each boundary.",
  "Evaluate build-vs-buy and data-quality trade-offs through the ontology lens: which objects must be first-class."],
 "notes": [
  {"title": "Ontology: the shared map of the business",
   "body": "An ontology names the business's objects (Customer, Order, Shipment), their properties, and their links (Customer PLACED Order; Order CONTAINS Product). It is the contract between stakeholders ('what we mean') and data ('what we store'). Without it, every team defines 'customer' differently.\n\nWorked example (with solution):\n```text\nE-commerce ontology (fragment):\nObjects: Customer, Order, LineItem, Product, Shipment, Return.\nLinks: Customer PLACED Order (1:many); Order HAS LineItem (1:many);\n       LineItem REFERENCES Product (many:1); Order FULFILLED_BY Shipment;\n       Return AGAINST LineItem.\nQuestions each link answers:\n  PLACED -> 'orders per customer' (the join path)\n  REFERENCES -> 'revenue by product' (the attribution path)\n  AGAINST -> 'return rate by product' (the quality path)\nIf a question has no link path, the ontology (not the query) is missing it.\n```\nIndependent prep material; no affiliation with or endorsement by Palantir."},
  {"title": "From ontology to schema",
   "body": "Ontology objects become tables (or nodes); links become foreign keys (or edges); properties become columns. The discipline: every table maps to an ontology object, every join follows an ontology link. Mystery joins (paths with no business meaning) are a modeling smell.\n\nWorked example (with solution):\n```sql\n-- Ontology-driven schema: each table IS an ontology object.\nCREATE TABLE customer (customer_id PK, name, segment, ...);       -- Object\nCREATE TABLE \"order\" (order_id PK, customer_id FK -> customer, ...); -- Object + link\nCREATE TABLE line_item (line_id PK, order_id FK -> \"order\",\n                         product_id FK -> product, qty, price);     -- Object + 2 links\n-- The join customer -> order -> line_item -> product FOLLOWS the ontology.\n-- Anti-pattern: joining customer straight to shipment with no link in the\n-- ontology ('which shipments belong to which customer?') -> add the link\n-- (Shipment FULFILLS Order) instead of hacking the join.\n```"},
  {"title": "Pipeline thinking: contracts at every boundary",
   "body": "Production pipelines are staged: raw (immutable landings) -> cleaned (typed, deduped) -> modeled (ontology objects) -> served (marts/APIs). Each boundary has a contract: schema, freshness SLA, quality gates. Breaks are diagnosed at boundaries, not in the middle of a 500-line query.\n\nWorked example (with solution):\n```text\nPipeline: raw_events -> stg_events -> fct_orders -> mart_daily\nContracts:\n  raw_events:     append-only, any schema (quarantined on violation)\n  stg_events:     typed, deduped on event_id, <2h freshness\n  fct_orders:     one row per order (grain!), FKs valid, quality gates pass\n  mart_daily:     matches fct_orders totals (reconciliation gate)\nIncident: mart_daily revenue dropped 30%.\nDiagnose at boundaries: mart==fct? fct==stg? stg==raw? The FIRST boundary\nwhere numbers diverge names the broken stage. No guessing.\n```"},
  {"title": "Ontology in interviews: the modeling case",
   "body": "Ontology-style interview cases ('design data for a ride-share app') are won by: naming objects/links first, stating grain per object, then sketching the schema. The interviewer watches whether the model follows the business or the business follows the model.\n\nWorked example (with solution):\n```text\n' Design analytics for ride-share.'\nObjects: Rider, Driver, Trip, Payment, Rating.\nLinks: Rider REQUESTED Trip; Driver ACCEPTED Trip; Trip HAS Payment;\n       Rider RATED Driver; Driver RATED Rider.\nGrain: Trip = one row per completed ride attempt (cancelled = status).\nKey questions -> paths:\n  'Driver utilization' -> ACCEPTED links per driver per hour.\n  'Cancellation rate'  -> Trip.status distribution.\n  'Take rate'          -> Payment.driver_payout vs rider_fare.\nThen schema. The ontology did the hard thinking; SQL is transcription.\n```"},
  {"title": "Data quality through the ontology lens",
   "body": "Ontology discipline makes quality concrete: every object needs identity (unique keys), every link needs referential integrity, every property needs a type and allowed values. Orphaned links (orders with no customer) and identity breaks (duplicated keys) are ontology violations with business meaning.\n\nWorked example (with solution):\n```sql\n-- Ontology-driven quality checks (each maps to a link/identity rule):\n-- 1. Identity: no duplicated order_id\nSELECT order_id, COUNT(*) FROM fct_orders GROUP BY 1 HAVING COUNT(*) > 1;\n-- 2. Link integrity: no orphan line items\nSELECT COUNT(*) FROM line_item l\nLEFT JOIN \"order\" o ON l.order_id = o.order_id WHERE o.order_id IS NULL;\n-- 3. Property validity: quantities positive\nSELECT COUNT(*) FROM line_item WHERE qty <= 0;\n-- Each check has a BUSINESS reading: orphans = lost attribution;\n-- dup keys = double-counted revenue. Quality is ontology enforcement.\n```"}],
 "cards": [
  {"front": "Ontology in one sentence?", "back": "Named business objects + their properties + their links: the shared map."},
  {"front": "Ontology -> schema mapping?", "back": "Objects->tables, links->FKs, properties->columns."},
  {"front": "Pipeline stages (4)?", "back": "Raw -> cleaned -> modeled (ontology) -> served."},
  {"front": "Contracts live where?", "back": "At every stage boundary: schema, freshness SLA, quality gates."},
  {"front": "Diagnosing a metric drop: method?", "back": "Check each boundary in order; the first divergence names the broken stage."},
  {"front": "Ride-share ontology objects?", "back": "Rider, Driver, Trip, Payment, Rating (+ links: requested/accepted/has/rated)."},
  {"front": "Mystery join = ?", "back": "A join with no ontology link: a modeling smell; add the link instead."},
  {"front": "Ontology quality checks (3)?", "back": "Identity (unique keys), link integrity (no orphans), property validity."}],
 "quiz": [
  {"q": "An ontology's three parts?", "choices": ["Objects, properties, links", "Tables, views, indexes", "Users, roles, grants", "Files, folders, buckets"], "answer": 0, "explain": "Objects (entities), their properties, and the links between them."},
  {"q": "'Revenue by product' needs which ontology path?", "choices": ["Customer->Order", "Return->LineItem", "Order->LineItem->Product (REFERENCES)", "Shipment->Order"], "answer": 2, "explain": "Attribution flows through the REFERENCES link to Product."},
  {"q": "A join with no business-meaning path in the ontology is:", "choices": ["Fine", "A modeling smell: add the link or fix the model", "Faster", "Required"], "answer": 1, "explain": "Mystery joins signal a missing link; hacky joins corrupt semantics."},
  {"q": "Pipeline stage contracts specify:", "choices": ["Colors", "Tool versions only", "Team names", "Schema, freshness SLA, quality gates at each boundary"], "answer": 3, "explain": "Contracts make each boundary testable and failures diagnosable."},
  {"q": "mart_daily revenue dropped 30%. First diagnostic?", "choices": ["Rebuild everything", "Blame the source", "Refresh the dashboard", "Walk boundaries raw->stg->fct->mart; first divergence names the broken stage"], "answer": 3, "explain": "Boundary-ordered diagnosis isolates the stage without guessing."},
  {"q": "Ride-share: 'driver utilization' uses which link?", "choices": ["Rider RATED Driver", "Driver ACCEPTED Trip per driver per hour", "Trip HAS Payment", "Customer PLACED Order"], "answer": 1, "explain": "Utilization = accepted trips per driver per hour via the ACCEPTED link."},
  {"q": "Orphaned line items (no matching order) mean:", "choices": ["Nothing", "Faster queries", "Lost attribution: a link-integrity violation with business impact", "Good partitioning"], "answer": 2, "explain": "Orphans break the ontology's links; revenue attribution is corrupted."},
  {"q": "Ontology-first interview case: correct order?", "choices": ["Objects/links/grain first, then schema", "Schema first", "SQL first", "Tools first"], "answer": 0, "explain": "The ontology does the hard thinking; schema and SQL are transcription."},],
 "drills": [{"id": "il26-m37-onto", "title": "Ontology drills", "items": [
   {"prompt": "Object vs property vs link?", "answer": "Object: entity. Property: attribute. Link: relationship.", "explain": "The three primitives."},
   {"prompt": "Grain statement for Trip?", "answer": "One row per ride attempt (cancelled = status)", "explain": "Grain before schema."},
   {"prompt": "Identity rule?", "answer": "Every object has a unique key", "explain": "No identity, no trustworthy joins."},
   {"prompt": "Link integrity rule?", "answer": "Every FK resolves (no orphans)", "explain": "Referential integrity."},
   {"prompt": "Raw layer contract?", "answer": "Append-only, immutable landings", "explain": "History is never rewritten."},
   {"prompt": "Served layer contract?", "answer": "Reconciled to modeled layer; documented definitions", "explain": "What stakeholders touch."}]}],
 "handsOnLab": {"id": "il26-m37-lab", "title": "Ontology-to-pipeline build", "brief": "Pick a business domain, build its ontology, derive the schema, stage the pipeline with contracts, and implement the quality checks.",
  "steps": ["Write the ontology: objects, properties, links (diagram).", "Derive DDL: tables, keys, grain statements.", "Stage the pipeline raw->stg->fct->mart with written contracts.", "Implement 3 ontology quality checks as gates.", "Break one contract deliberately; diagnose via boundary walk."],
  "deliverable": "Ontology diagram + DDL + contracts + gates + diagnosis log.",
  "checkpoint": "Every join follows an ontology link; the planted break is found at the right boundary."},
 "mockTask": {"id": "il26-m37-mock", "type": "choice", "q": "Case: 'Two teams report different 'active user' counts.' Ontology-first response?", "choices": ["Pick the bigger number.", "Ask each team for their object definition: what IS a user, what counts as active, over what window — then reconcile to one ontology definition and implement it once.", "Average them.", "Build a third dashboard."], "answer": 1, "explain": "Divergent metrics are divergent ontologies. Reconcile the definitions first; the implementation follows."},
 "crossLinks": [],
 "videoPlaceholders": False}}

M38 = {"id": "IL26-M38", "patch": {
 "objectives": [
  "Describe banking data domains (deposits, lending, payments, custody, markets) and the entities in each.",
  "Explain the data challenges of financial services: reconciliation, lineage, auditability, and regulatory reporting.",
  "Map banking concepts (GL, subledger, nostro/vostro, settlement) to data-modeling decisions.",
  "Speak the domain language: read a banking process and name the data objects and controls it implies."],
 "notes": [
  {"title": "Banking data domains: the map",
   "body": "A bank's data splits into domains: Deposits (accounts, balances, transactions), Lending (loans, delinquency, provisions), Payments (wires, ACH, cards, settlement), Custody/Asset Servicing (holdings, corporate actions, NAV), Markets (trades, positions, risk). Each has its own systems, clocks, and definitions of 'the truth'.\n\nWorked example (with solution):\n```text\n'Where did yesterday's $2M wire go?' -> trace across domains:\nPayments: wire instruction (sender, receiver, amount, status=settled).\nDeposits: sender account debited, receiver account credited (double-entry).\nGL: the bank's books balance (debits = credits).\nIf Payments says 'settled' but Deposits shows no credit: a reconciliation\nBREAK — the core banking-data failure mode. Analysts live in these breaks.\n```\nIndependent prep material; no affiliation with or endorsement by BNY Mellon."},
  {"title": "Double-entry and the GL: the bank's source of truth",
   "body": "Every financial event posts balanced debits and credits to the General Ledger. Subledgers (loan system, deposit system) must reconcile to the GL. 'Reconciled to the GL' is the banking equivalent of 'tests pass' — nothing ships unaudited against it.\n\nWorked example (with solution):\n```text\nWire of $2M from A to B posts:\n  Dr Customer A deposit liability  $2,000,000\n  Cr Cash / settlement account    $2,000,000   (sender leg)\n  Dr Cash / settlement account    $2,000,000\n  Cr Customer B deposit liability $2,000,000   (receiver leg)\nFour balanced lines. If the subledger sum differs from the GL by $1:\nSTOP. Find the break (timing? fee? failed post?) before any reporting.\nAnalyst rule: never present subledger numbers that don't tie to the GL.\n```"},
  {"title": "Reconciliation: the analyst's core banking skill",
   "body": "Reconciliation = proving two independent records agree (nostro vs GL, custodian vs internal, trades vs settlements). Breaks come from timing (T+1 settlement), fees, FX, failed posts, and duplicates. The analyst builds the break-report: matched, timing-mismatch, true-break.\n\nWorked example (with solution):\n```sql\n-- Nostro reconciliation: bank's record vs correspondent's statement.\nSELECT COALESCE(b.txn_id, c.txn_id) AS txn_id,\n       b.amount AS book_amount, c.amount AS stmt_amount,\n       CASE WHEN b.txn_id IS NULL THEN 'missing in books'\n            WHEN c.txn_id IS NULL THEN 'missing in statement'\n            WHEN b.amount != c.amount THEN 'amount break'\n            WHEN b.value_date != c.value_date THEN 'timing break'\n            ELSE 'matched' END AS status\nFROM book_txns b FULL OUTER JOIN correspondent_stmt c USING (txn_id);\n-- Triage order: timing breaks age out; amount breaks get investigated TODAY.\n```"},
  {"title": "Custody and asset servicing: holdings, NAV, corporate actions",
   "body": "Custody banks safekeep assets and service them: track holdings, process corporate actions (dividends, splits, mergers), compute NAV (net asset value) for funds. Data challenges: position vs transaction views, ex-dates, and multi-currency valuation.\n\nWorked example (with solution):\n```text\nNAV computation (simplified):\n  NAV = (sum of holding market values + cash + accruals - liabilities) / shares_outstanding\nData traps:\n- Corporate action (2:1 split): positions double, price halves; naive\n  'holdings changed!' alerts are false — adjust for the action.\n- Ex-date: the dividend belongs to holders BEFORE ex-date; settling trades\n  across ex-date need special handling.\n- FX: value each holding in fund currency at the right rate AND timestamp.\nAnalyst interview signal: naming ex-dates and corporate-action adjustments\nunprompted.\n```"},
  {"title": "Regulatory reporting and auditability",
   "body": "Banks report to regulators (call reports, stress tests, AML/KYC filings). Every reported number needs lineage: source system -> transform -> report cell, reproducible on demand. 'Show me how you got this number' is a standing exam, not a surprise audit.\n\nWorked example (with solution):\n```text\nAudit-ready reporting checklist:\n1. Lineage: report cell -> mart -> model -> source system (documented).\n2. Reproducibility: re-running the pipeline reproduces the number exactly.\n3. Controls: four-eyes review on methodology changes; change log.\n4. Reconciliation: reported totals tie to the GL.\n5. Retention: inputs retained per policy for re-performance.\nThe analyst's deliverable isn't the number: it's the number PLUS the\nproof. Build every report as if the regulator asks tomorrow.\n```"}],
 "cards": [
  {"front": "Banking data domains (5)?", "back": "Deposits, lending, payments, custody/asset servicing, markets."},
  {"front": "The bank's source of truth?", "back": "The General Ledger (balanced debits = credits)."},
  {"front": "Reconciliation break triage order?", "back": "Timing breaks age out; amount breaks investigated today."},
  {"front": "Nostro account?", "back": "Our account at a correspondent bank (vs vostro: their account with us)."},
  {"front": "NAV formula?", "back": "(Holdings market value + cash + accruals - liabilities) / shares outstanding."},
  {"front": "Corporate-action trap example?", "back": "2:1 split doubles positions; naive 'holdings changed' alerts are false."},
  {"front": "Ex-date matters because?", "back": "Dividend belongs to holders before ex-date; settling trades need special handling."},
  {"front": "Audit-ready number = ?", "back": "The number PLUS lineage, reproducibility, controls, GL tie-out, retention."}],
 "quiz": [
  {"q": "Payments says 'settled' but deposits show no credit. This is:", "choices": ["Normal", "A feature", "A UI bug", "A reconciliation break: the core banking-data failure mode"], "answer": 3, "explain": "Two systems disagree about the same economic event: investigate before reporting."},
  {"q": "Subledger sum differs from GL by $1. Move?", "choices": ["Round it", "STOP: find the break before any reporting", "Ship it", "Ignore"], "answer": 1, "explain": "Nothing ships unaudited against the GL; $1 breaks are how $1M breaks start."},
  {"q": "Nostro vs correspondent statement amount mismatch: triage?", "choices": ["Amount break: investigate today", "Ignore", "Wait a month", "Delete"], "answer": 0, "explain": "Amount breaks do not age out like timing breaks; they need same-day investigation."},
  {"q": "2:1 stock split: holdings double. Correct handling?", "choices": ["Alert 'holdings changed!'", "Sell", "Adjust for the corporate action; no economic change", "Rebuy"], "answer": 2, "explain": "Splits are mechanical; positions double and price halves with no value change."},
  {"q": "NAV includes:", "choices": ["Only cash", "Only holdings", "Holdings value + cash + accruals - liabilities, over shares outstanding", "Liabilities only"], "answer": 2, "explain": "NAV is the full fund economics per share."},
  {"q": "Dividend belongs to holders as of:", "choices": ["Before ex-date", "Pay date", "Whenever", "Settlement date"], "answer": 0, "explain": "Ex-date is the cutoff; buyers on/after ex-date do not get the dividend."},
  {"q": "Regulator asks 'how did you get this number?' You need:", "choices": ["A good memory", "Documented lineage: source -> transform -> report cell, reproducible", "A new number", "An excuse"], "answer": 1, "explain": "Lineage + reproducibility is the standing exam; build for it upfront."},
  {"q": "T+1 settlement causes which break type?", "choices": ["Amount break", "Fraud", "System outage", "Timing break (ages out)"], "answer": 3, "explain": "Settlement-lag mismatches resolve when the lagging leg posts."},],
 "drills": [{"id": "il26-m38-bank", "title": "Banking domain drills", "items": [
   {"prompt": "Double-entry rule?", "answer": "Debits = credits, every event balanced", "explain": "The GL's invariant."},
   {"prompt": "Nostro vs vostro?", "answer": "Nostro: our account at their bank. Vostro: their account at ours.", "explain": "Latin: ours/theirs."},
   {"prompt": "T+1 means?", "answer": "Settlement one business day after trade", "explain": "The timing-break source."},
   {"prompt": "AML stands for?", "answer": "Anti-Money Laundering", "explain": "Transaction monitoring regime."},
   {"prompt": "KYC stands for?", "answer": "Know Your Customer", "explain": "Identity verification regime."},
   {"prompt": "Corporate actions (3)?", "answer": "Dividends, splits, mergers (also spinoffs)", "explain": "Events changing holdings."}]}],
 "handsOnLab": {"id": "il26-m38-lab", "title": "Reconciliation desk simulation", "brief": "Run a nostro reconciliation: match book vs statement, triage breaks, and write the break report with aging.",
  "steps": ["Load book_txns and correspondent_stmt for the week.", "Run the FULL OUTER JOIN break classification.", "Triage: separate timing breaks from amount breaks.", "Age the breaks; escalate amount breaks per the playbook.", "Write the daily break report: matched %, break inventory, actions."],
  "deliverable": "Break report with triage and aging.",
  "checkpoint": "Every break is classified and either aged (timing) or actioned (amount); totals tie to the GL."},
 "mockTask": {"id": "il26-m38-mock", "type": "choice", "q": "Interview: 'Our custody NAV moved 3% overnight with no market move. Where do you look?'", "choices": ["Blame the market.", "Corporate actions (splits/dividends), FX rate/timestamp issues, failed corporate-action processing, or a large flow (subscription/redemption) — check the NAV attribution bridge before anything else.", "Reboot the system.", "Ignore small moves."], "answer": 1, "explain": "NAV attribution decomposes the move; corporate actions and FX are the usual suspects when markets are flat."},
 "crossLinks": [],
 "videoPlaceholders": False}}

MODULES += [M36, M37, M38]

check(MODULES)
json.dump({"modules": MODULES}, open(OUT + "/flesh_d.json", "w"), indent=1)
print("flesh_d.json written:", len(MODULES), "modules")

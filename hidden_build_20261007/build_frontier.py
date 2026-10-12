#!/usr/bin/env python3
"""Frontier seed build-out 2026-10-07: Epoch AI + METR modules into IL-23, supplements into IL-12/IL-16, catalog entries in shard-o/shard-l.
Content build + validation only. No commit, no deploy.
All prose is original Interstitium exposition; all figures attributed with as-of dates.
Verified URL whitelist only. Zero competitor brands."""
import json, re, sys, copy

ROOT = "/home/hatch/workspace/apex-audit"
P23 = ROOT + "/docs/university/data/courses/il-23-frontier-knowledge.json"
P12 = ROOT + "/docs/university/data/courses/il-12-ai-engineering.json"
P16 = ROOT + "/docs/university/data/courses/il-16-machine-learning-ai-engineering.json"
PO  = ROOT + "/docs/university/data/catalog/shard-o.json"
PL  = ROOT + "/docs/university/data/catalog/shard-l.json"

ALLOWED_URLS = {
    "https://epoch.ai/publications/estimating-the-agent-population",
    "https://epoch.ai/publications",
    "https://arxiv.org/abs/2211.04325",
    "https://arxiv.org/html/2211.04325v2",
    "https://metr.org/blog/2024-11-22-evaluating-r-d-capabilities-of-llms/",
    "https://arxiv.org/abs/2411.15114",
    "https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/",
    "https://metr.org/blog/2026-1-29-time-horizon-1-1/",
}
COMPETITORS = re.compile(r"aleks|brilliant\.org|khan academy|coursera|udemy|\bedx\b|udacity|datacamp|codecademy|pluralsight|linkedin learning|masterclass|skillshare", re.I)
BANNED = re.compile(r"palantir|\bNSA\b", re.I)

def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)

def dump(p, obj, trailing_newline=True):
    with open(p, "w", encoding="utf-8") as f:
        # match repo convention: 1-space indent, literal UTF-8 (ensure_ascii=False)
        f.write(json.dumps(obj, indent=1, ensure_ascii=False))
        if trailing_newline:
            f.write("\n")

# ---------------------------------------------------------------- m23-epoch-ai
m23_epoch = {
 "id": "m23-epoch-ai",
 "code": "IL-23",
 "title": "Frontier Capability Forecasting: The Epoch AI Corpus",
 "weight": 1,
 "asOf": "2026-10-07",
 "summary": "Welcome to the measurement wing of the Frontier. I'm your instructor for this module, and we're going to do something unusual: instead of learning a technology, we're learning how the frontier learns about itself. Epoch AI is the research group that tracks AI's physical supply chains \u2014 data, chips, dollars \u2014 and turns those measurements into bounded forecasts of what comes next. In this module you'll reconstruct two of their flagship analyses: the 'data wall' question (will we run out of training data?) and the 'agent capacity' question (how many AI agents could the chip buildout actually run?). Every figure here is dated, because frontier numbers decay \u2014 dating them is part of the discipline. All fast-moving claims: as of October 7, 2026.",
 "objectives": [
  "Explain Epoch AI's capability-forecasting method: physical inputs (data stocks, chip shipments, cost curves) projected into bounded frontier forecasts",
  "Reconstruct the data-wall argument: scaling-law demand vs. estimated supply, the quality and multi-epoch adjustments, and the 2026-2032 exhaustion window",
  "Reproduce Epoch's agent-capacity estimation (A = E \u00d7 c) and its key result: ~30-170M concurrent frontier agents from 2025-27 HBM shipments",
  "Interpret inference cost curves (~47%/quarter since 2023) and their budget implications for AI engineering",
  "Apply the decay lesson: why frontier forecasts carry as-of dates and why the binding constraint moves over time"
 ],
 "notes": [
  {"title": "Concepts", "body": "- **Capability forecasting** \u2014 The research practice of converting unobservable quantities about AI's future \u2014 remaining usable training data, deployable agent capacity, the cost of a fixed capability \u2014 into bounded forecasts with stated assumptions and uncertainty intervals.\n- **The data wall** \u2014 The projected point at which training datasets reach the size of the available stock of public human-generated text. Villalobos et al. (2024) place it between 2026 and 2032, median 2028.\n- **Neural scaling laws** \u2014 Empirical relationships (Kaplan 2020; Hoffmann/Chinchilla 2022) tying optimal dataset size to roughly the square root of training compute \u2014 the demand side of the data-wall ledger.\n- **Stock estimates** \u2014 The paper's Table 1 point estimates of usable text: Common Crawl ~130T tokens, the indexed web ~510T, the whole web ~3100T, images ~300T, video ~1350T (as of the paper, 2024).\n- **Quality filtering** \u2014 Only a fraction of deduplicated web text is usable without degrading model performance; this adjustment shrinks the effective stock.\n- **Multi-epoch training** \u2014 Repeat passes over the same data stretch the effective stock by a capped multiplier; this adjustment grows it.\n- **Monte Carlo simulation** \u2014 The paper propagates parameter uncertainty through repeated random sampling, producing the 2026\u20132032 window rather than a single year.\n- **Agent capacity (A = E \u00d7 c)** \u2014 Epoch's October 2026 estimation: effective hardware supply E (HBM memory shipped 2025\u201327, expressed in GB300 equivalents) multiplied by serving capacity c (concurrent agent sessions per GB300).\n- **GB300 equivalent** \u2014 Epoch's unit of account for hardware supply: the HBM capacity of one GB300-class AI server, used to normalize heterogeneous chip shipments.\n- **TraceLab / AgentX** \u2014 The two concurrency sources in Epoch's report: API spending per agent-hour from the TraceLab dataset of coding-agent session traces (closed models), and SemiAnalysis's AgentX serving benchmarks at fixed streaming speeds (open models).\n- **The plunging price of thought** \u2014 Epoch's September 2026 finding: the cost of a fixed level of benchmark performance has fallen roughly 47% per quarter \u2014 about 13\u00d7 per year \u2014 since 2023.\n- **Binding constraint / capacity glut** \u2014 The lesson of the agent-capacity report: the scarce resource moved from chips to demand. Using just 20% of central capacity would imply $2.6\u20135.3T/year in API-equivalent spending (Epoch, 2026-10-02), far above projected developer revenue \u2014 a potential capacity glut."},
  {"title": "Worked estimation", "body": "Grab a notebook or a scratch file. We're going to reproduce both of Epoch's headline calculations at the level of a careful reader \u2014 not the full Monte Carlo, but every input and where it comes from.\n1. **Demand side of the data wall.** Start from the scaling-law rule of thumb: optimal dataset size grows roughly with the square root of training compute. If training compute grows 10\u00d7, the dataset that justifies it grows about 3.16\u00d7. Compound that across years of compute growth and data demand compounds against a finite stock.\n2. **Supply side, raw.** Estimate the indexed web's plain text with the paper's recipe: ~250 billion pages in Google's index (2022 figure) \u00d7 ~7,000 bytes of plain text per page from Common Crawl statistics \u2192 convert bytes to tokens with a byte-pair tokenizer. That is the raw token stock.\n3. **Adjust down \u2014 quality filtering.** Only a fraction of deduplicated web text trains well. Multiply the raw stock by the usable fraction (the paper treats this as an uncertain parameter, not a constant).\n4. **Adjust up \u2014 multi-epoch training.** Repeat passes over data stretch the effective stock, but with diminishing returns; the paper caps the multiplier. Multiply by the epoch factor.\n5. **Propagate uncertainty.** Run the whole ledger thousands of times, sampling each uncertain parameter from its range \u2014 that is the Monte Carlo step. The output is a window, not a date: 2026\u20132032, median 2028, at roughly 4e14 tokens of dataset size and ~5e28 FLOP of training compute for non-overtrained models (one to two years earlier if frontier models are overtrained).\n6. **Now the agent-capacity computation.** Define E: HBM memory shipped 2025\u201327, expressed in GB300 equivalents. Define c: concurrent agent sessions one GB300 equivalent can serve \u2014 for closed models, infer it from API spending per agent-hour in TraceLab coding-agent traces (pooled rates Epoch reports: roughly $18/hour for GPT-5.5 on Codex and $15.5 for GPT-5.6 Sol, versus $24.3 for Opus 4.8 and $50.2 for Fable 5 on Claude Code; the report's reference point is $30/agent-hour); for open models, read it directly from AgentX serving benchmarks at a fixed 50 tokens/second streaming target.\n7. **Multiply: A = E \u00d7 c.** Epoch's headline (2026-10-02): roughly 30\u2013170 million concurrent frontier-model agents \u2014 or about 1.9 billion concurrent sessions of an efficient open model (DeepSeek V4 Pro serving benchmarks).\n8. **The demand check \u2014 the step most forecasters skip.** Convert capacity to dollars. Using only 20% of central capacity implies $2.6\u20135.3 trillion per year in API-equivalent spending, against roughly $1 trillion in combined developer revenue projected by end-2027 (at fivefold annual growth). If demand can't absorb the capacity, the binding constraint isn't chips \u2014 it's customers. That is the capacity-glut warning.\n9. **Date your work.** Write 'as of 2026-10-07' on every figure. The 2022 data-wall estimate said ~2024; it was revised to ~2028 when web data filtered better than assumed. Your forecast is a perishable artifact \u2014 the method above is durable, the numbers are not."},
  {"title": "Project brief", "body": "Your capstone for this module: build your own bounded forecast with stated assumptions. Pick one frontier quantity \u2014 examples: the inference cost of a fixed benchmark capability in 2028, the data-stock exhaustion date under a different overtraining assumption, or the agent capacity of a single year's HBM shipments. Deliverable: a one-page forecast memo with (1) the quantity and why it matters, (2) an assumption table with a source or an explicit guess for each input, (3) a central estimate plus an uncertainty interval, (4) an as-of date and a decay plan \u2014 what would make you revise it. Grading bar: every number dated, every assumption stated, no point estimates without intervals. If your memo could be quoted in 2028 without embarrassing you, it isn't honest enough \u2014 put the uncertainty in writing."},
  {"title": "Frontier honesty", "body": "What decays here: model names and hourly rates (GPT-5.6 Sol, Opus 4.8, Fable 5, DeepSeek V4 Pro are Epoch's 2026 estimates and assumptions), HBM shipment figures, the ~47%/quarter cost-curve rate, and the 30\u2013170M capacity range itself \u2014 all as-of 2026-10-02/07. What endures: the method \u2014 ledger both sides, adjust honestly, propagate uncertainty, report intervals, date everything. And the meta-lesson: the binding constraint moves. In 2022 the debate was training-data supply; by 2026 it is inference economics and demand. Any forecaster who reports a date without naming the constraint they're assuming is selling certainty they don't have."}
 ],
 "cards": [
  {"front": "What is capability forecasting, in one sentence?", "back": "Converting unobservable quantities about AI's future \u2014 usable data remaining, deployable agent capacity, cost of a fixed capability \u2014 into bounded forecasts with stated assumptions and uncertainty intervals."},
  {"front": "The data-wall model: both sides of the ledger?", "back": "Demand: scaling laws tie dataset size to ~sqrt(training compute), so data demand compounds. Supply: indexed-web text estimated from Google's index size and Common Crawl bytes-per-page, converted to tokens."},
  {"front": "The two adjustments to raw web-token counts \u2014 and their directions?", "back": "Quality filtering shrinks the effective stock (only a usable fraction trains well); multi-epoch training stretches it (repeat passes, capped multiplier)."},
  {"front": "The data-wall headline forecast (window, median, scale)?", "back": "2026\u20132032 window, median 2028: datasets approaching ~4e14 tokens, ~5e28 FLOP of training compute for non-overtrained models \u2014 a year or two earlier if overtrained. (Villalobos et al., as of 2026-10-07.)"},
  {"front": "Epoch's agent-capacity formula and its terms?", "back": "A = E \u00d7 c. E = effective hardware supply (HBM shipped 2025\u201327, in GB300 equivalents). c = concurrent agent sessions per GB300 \u2014 from TraceLab $/agent-hour traces (closed) or AgentX serving benchmarks (open)."},
  {"front": "The agent-capacity headline result (as of 2026-10-02)?", "back": "~30\u2013170M concurrent frontier-model agents from 2025\u201327 HBM shipments \u2014 or ~1.9B concurrent sessions of an efficient open model (DeepSeek V4 Pro benchmarks)."},
  {"front": "Why does Epoch say demand, not chips, is the binding unknown?", "back": "20% of central capacity implies $2.6\u20135.3T/year in API-equivalent spending vs ~$1T projected developer revenue by end-2027 \u2014 a potential capacity glut."},
  {"front": "The 'plunging price of thought' finding?", "back": "Cost of a fixed level of benchmark performance falling ~47%/quarter (~13\u00d7/year) since 2023 \u2014 faster than electricity, compute, batteries, or DNA sequencing ever fell. (Epoch, Sep 2026.)"},
  {"front": "The decay lesson in one line?", "back": "The 2022 data-wall estimate said ~2024; it was revised to ~2028 when web data filtered better than assumed. Every frontier number is a dated artifact."},
  {"front": "Chip-supply tracking: what does Epoch's corpus monitor?", "back": "AI data centers worldwide (satellite imagery, H100-equivalents, capex), chip-shock exposure (China ~2.7\u00d7 the US), and trade-data anomalies like ~$3B of chips routed via Malaysia."},
  {"front": "Adoption measurement: two signals Epoch tracks?", "back": "Coding-agent usage doubling roughly monthly; AI-use acknowledgments in arXiv math preprints rising 4%\u219225% (Apr\u2192Aug 2026)."},
  {"front": "What is a capacity glut?", "back": "When buildout outruns demand: the hardware can serve far more agents than customers will pay for \u2014 Epoch's warning for the 2025\u201327 HBM buildout."},
  {"front": "As-of discipline: what three things must a frontier forecast carry?", "back": "Stated assumptions, an uncertainty interval (not a point estimate), and an as-of date with a decay plan."}
 ],
 "quiz": [
  {"q": "In the data-wall model, why does data demand compound over time?", "choices": ["Because web pages get longer", "Because scaling laws tie dataset size to ~sqrt(training compute), and compute compounds", "Because tokenizers get less efficient", "Because researchers prefer larger datasets"], "answer": 1, "explain": "Covered in Concepts (neural scaling laws) and Worked estimation step 1."},
  {"q": "Which adjustment INCREASES the effective data stock in Villalobos et al.'s model?", "choices": ["Quality filtering", "Deduplication", "Multi-epoch training", "Byte-pair tokenization"], "answer": 2, "explain": "Covered in Concepts: multi-epoch training stretches the stock; quality filtering shrinks it."},
  {"q": "The paper's median data-wall year and scale?", "choices": ["2024, ~1e13 tokens", "2028, ~4e14 tokens and ~5e28 FLOP", "2032, ~1e15 tokens", "2030, ~5e28 tokens"], "answer": 1, "explain": "Covered in Worked estimation step 5 \u2014 median 2028, one to two years earlier if overtrained."},
  {"q": "In A = E \u00d7 c, what is E?", "choices": ["Number of data centers", "Effective hardware supply: HBM shipped 2025\u201327 in GB300 equivalents", "Total training FLOPs", "Electricity consumed"], "answer": 1, "explain": "Covered in Concepts (GB300 equivalent) and Worked estimation step 6."},
  {"q": "Where does the closed-model concurrency term c come from?", "choices": ["Vendor marketing claims", "API spending per agent-hour in TraceLab coding-agent session traces", "GPU benchmark leaderboards", "Electricity bills"], "answer": 1, "explain": "Covered in Concepts (TraceLab) and Worked estimation step 6."},
  {"q": "Epoch's capacity-glut warning rests on which comparison?", "choices": ["$2.6\u20135.3T/yr implied API spending at 20% capacity vs ~$1T projected developer revenue", "Chip prices vs electricity prices", "Open vs closed model quality", "US vs China chip exposure"], "answer": 0, "explain": "Covered in Worked estimation step 8 \u2014 demand, not chips, is the binding unknown."},
  {"q": "The 'plunging price of thought' rate?", "choices": ["~47% per year", "~13% per quarter", "~47% per quarter (~13\u00d7/year) since 2023", "~4.7% per month"], "answer": 2, "explain": "Covered in Concepts \u2014 Epoch, September 2026."},
  {"q": "Why was the 2022 data-wall estimate revised from ~2024 to ~2028?", "choices": ["New GPUs were released", "Web data filtered better than assumed", "The authors changed the tokenizer", "Compute growth stopped"], "answer": 1, "explain": "Covered in Frontier honesty \u2014 estimates decay as assumptions get tested."},
  {"q": "A forecaster reports 'agents will cost $5/hour in 2028' with no interval and no date. The as-of discipline says:", "choices": ["Accept it \u2014 precision is confidence", "Reject the number; demand stated assumptions, an interval, and an as-of date", "Average it with other forecasts", "Wait for peer review"], "answer": 1, "explain": "Covered in Frontier honesty \u2014 intervals and dates are non-negotiable."},
  {"q": "By 2026, the binding constraint in the AI scaling debate had moved to:", "choices": ["Raw training-data supply only", "Inference economics and demand", "Electricity grid capacity", "Regulatory approval"], "answer": 1, "explain": "Covered in Frontier honesty \u2014 constraints move; the 2026 debate is inference economics and demand."}
 ],
 "scenarios": [
  {"id": "sc-epoch-datawall-deal", "title": "The Five-Year Data Deal", "context": "A data vendor offers your company a five-year exclusive training-data license at a premium, arguing 'the data wall hits in 2028 \u2014 lock in supply now.' Your CEO asks whether to sign.", "steps": [
   {"prompt": "Your first move?", "options": [
    {"text": "Read the paper's own adjustments: quality filtering, multi-epoch training, and the authors' conclusion that alternative data sources will likely arrive first", "correct": True, "why": "The protocol starts with the source's own caveats \u2014 the paper concludes scaling likely continues via synthetic data and efficiency gains."},
    {"text": "Sign immediately \u2014 2028 is soon", "correct": False, "why": "A median year from a Monte Carlo window is not a deadline; signing on a point estimate ignores the paper's uncertainty."},
    {"text": "Dismiss the data wall entirely", "correct": False, "why": "The ledger is real even if the date moves; cynicism is not analysis."}]},
   {"prompt": "The vendor's deck quotes only the 2028 median. What do you tell the CEO?", "options": [
    {"text": "The honest range is 2026\u20132032, one to two years earlier if overtrained \u2014 structure the deal with optionality, not a five-year lock", "correct": True, "why": "Forecasts with intervals get negotiated as ranges; the as-of discipline turns a scare into contract terms."},
    {"text": "The median is the expected date, so plan for exactly 2028", "correct": False, "why": "A median is not a plan date \u2014 half the Monte Carlo mass sits on either side."},
    {"text": "Ask the vendor for their own Monte Carlo", "correct": False, "why": "They don't have one; the question concedes the frame instead of checking it."}]}]},
  {"id": "sc-epoch-investor-deck", "title": "The 170-Million-Agent Deck", "context": "An investor deck claims 'Epoch says 170M AI agents by 2028 \u2014 the market is $X trillion.' You're asked to diligence the claim before your firm invests.", "steps": [
   {"prompt": "Your first diligence check?", "options": [
    {"text": "Verify the deck reports Epoch's full range (30\u2013170M) and its demand caveat \u2014 the capacity-glut warning", "correct": True, "why": "Quoting only the top of an interval while dropping the report's own binding-unknown is the classic misuse pattern."},
    {"text": "Check the font of the deck's charts", "correct": False, "why": "Presentation polish is not diligence."},
    {"text": "Assume Epoch endorses the $X trillion figure", "correct": False, "why": "Epoch estimated capacity, not market size \u2014 and warned demand may not fill it."}]},
   {"prompt": "The deck prices agents at $30/hour flat. What do you ask?", "options": [
    {"text": "Which harness? Epoch's pooled rates range ~$15.5\u2013$50.2/hour across Codex and Claude Code harnesses \u2014 the rate is harness-specific and dated 2026-10-02", "correct": True, "why": "A single flat rate hides the harness variance the report documents; economics questions get answered per-harness."},
    {"text": "Nothing \u2014 $30/hour is the report's reference point", "correct": False, "why": "It is a reference point for illustration, not a price quote \u2014 the report shows wide harness variance."},
    {"text": "Whether the rate includes electricity", "correct": False, "why": "The rates are API-spending-per-agent-hour from session traces, not power bills \u2014 the question misreads the metric."}]}]},
  {"id": "sc-epoch-budget-curve", "title": "Budgeting on the Cost Curve", "context": "Your team must budget inference spend for a product launching in 12 months. A colleague proposes projecting today's cost with Epoch's ~47%/quarter decline. The CFO wants a number.", "steps": [
   {"prompt": "How do you use the cost curve honestly?", "options": [
    {"text": "Project a range using the curve, label it as-of 2026-09-22, and schedule a quarterly revisit \u2014 curves decay", "correct": True, "why": "The curve is a dated empirical finding, not a law; honest use carries the date and a refresh plan."},
    {"text": "Give the CFO the point estimate \u2014 confidence inspires confidence", "correct": False, "why": "Point estimates from decaying curves are how budgets blow up."},
    {"text": "Ignore the curve; budget at today's prices", "correct": False, "why": "Ignoring a 13\u00d7/year trend is as dishonest as over-trusting it \u2014 the answer is a dated range."}]},
   {"prompt": "What breaks the projection?", "options": [
    {"text": "Hardware cost floors, demand surges, or a regime change in model efficiency \u2014 name the assumptions so the CFO sees them", "correct": True, "why": "Every extrapolation has kill conditions; stating them is the difference between forecasting and hoping."},
    {"text": "Nothing \u2014 the trend has held since 2023", "correct": False, "why": "Past persistence is not a guarantee; the Frontier honesty note exists for exactly this sentence."},
    {"text": "A competitor's pricing change", "correct": False, "why": "The curve measures cost of a fixed capability, not market pricing \u2014 different quantity."}]}]}
 ],
 "drills": [
  {"id": "drill-epoch-window", "title": "Data-wall window", "prompt": "The Villalobos et al. data-wall window and median year?", "choices": ["2024\u20132026, median 2025", "2026\u20132032, median 2028", "2030\u20132036, median 2033", "2028\u20132030, median 2029"], "answer": 1, "explain": "Worked estimation step 5 \u2014 and one to two years earlier if overtrained."},
  {"id": "drill-epoch-formula", "title": "Agent-capacity formula", "prompt": "Epoch's agent-capacity estimation is:", "choices": ["A = E + c", "A = E \u00d7 c, hardware supply times serving capacity", "A = E / c", "A = E^c"], "answer": 1, "explain": "Concepts: A = E \u00d7 c \u2014 GB300 equivalents times sessions per GB300."},
  {"id": "drill-epoch-cost", "title": "Cost-curve rate", "prompt": "The plunging price of thought: cost of fixed benchmark performance falls\u2026", "choices": ["~4.7% per quarter", "~47% per quarter since 2023", "~47% per year", "~13% per year"], "answer": 1, "explain": "Concepts \u2014 about 13\u00d7 per year, per Epoch (Sep 2026)."},
  {"id": "drill-epoch-binding", "title": "Binding constraint", "prompt": "Epoch's October 2026 agent-capacity report concludes the binding unknown is:", "choices": ["Chip supply", "HBM memory", "Demand \u2014 a potential capacity glut", "Electricity"], "answer": 2, "explain": "Worked estimation step 8 \u2014 $2.6\u20135.3T/yr implied vs ~$1T revenue."}
 ]
}

# ---------------------------------------------------------------- m23-metr-evals
m23_metr = {
 "id": "m23-metr-evals",
 "code": "IL-23",
 "title": "Measuring AI Itself: RE-Bench and the Task-Time Horizon",
 "weight": 1,
 "asOf": "2026-10-07",
 "summary": "Welcome to the module where AI gets measured. I'm your instructor, and our subject is METR \u2014 the independent evaluation nonprofit whose benchmarks are the field's most cited answer to the question 'how capable are these systems, really?' You'll study RE-Bench, where AI agents and human experts compete head-to-head at real machine-learning research engineering, and the time-horizon method, which compresses 'how autonomous is this model?' into a single fitted number. You'll also learn what the numbers don't say \u2014 because reading an evaluation means reading its fine print. All fast-moving figures: as of October 7, 2026.",
 "objectives": [
  "Describe RE-Bench's design: 7 contamination-free environments, calibrated scoring, faithful human baselines",
  "Explain the crossover finding: agents win at 2-hour budgets, humans at 8-hour and 32-hour budgets, and why",
  "State the motivation behind RE-Bench: measuring AI automation of AI R&D as a capability of concern",
  "Define the time-horizon metric and how it is fitted from human task times and model success curves",
  "Report the ~7-month doubling trend (2019-2025) and the TH1.1 update's faster post-2023 estimate (130.8 days)",
  "Identify the limits of both instruments: RE-Bench's seven environments and fast feedback loops; time horizons as suite-specific fitted estimates",
  "Apply a critical checklist to any capability evaluation: comparison fairness, contamination, baselining quality, and suite-sensitivity"
 ],
 "notes": [
  {"title": "Concepts", "body": "- **RE-Bench** \u2014 METR's benchmark (announced 2024-11-22) for AI-led ML research engineering: seven realistic, open-ended environments where agents and human experts compete with the same resources and time limits.\n- **Anti-contamination design** \u2014 RE-Bench environments are built from scratch so they cannot appear in models' training data; most environments are held back unpublished for the same reason.\n- **Calibrated scoring** \u2014 Each environment's score is normalized so 0 = the starting solution's score and 1 = METR's strong reference solution.\n- **Human baselines** \u2014 71 paid attempts by 61 distinct human experts, each given up to 8 hours; 82% reached a non-zero score, 24% matched or beat the reference.\n- **The 2h/8h/32h crossover** \u2014 Best agents score ~4\u00d7 humans at a 2-hour budget; humans narrowly lead at 8 hours and reach ~2\u00d7 the top agent score at 32 hours (across attempts).\n- **Time horizon (P50/P80)** \u2014 METR's autonomy metric: the human-expert task length at which an agent has a 50% (or 80%) chance of success, read off a fitted curve.\n- **Logistic fit** \u2014 The fitting method: plot model success probability against human task length, fit a logistic curve, read the length where it crosses 50%.\n- **Doubling time (195.8 days)** \u2014 The 50%-reliability horizon doubles roughly every 7 months (2019\u20132025); 95% CI [162, 223] days.\n- **Time Horizon 1.1** \u2014 METR's January 2026 refresh: 170\u2192228 tasks, long tasks doubled 14\u219231, infrastructure moved from Vivaria to Inspect; post-2023 doubling 130.8 days (95% CI [107, 161]).\n- **Capability of concern** \u2014 Frontier safety policies single out automation of AI R&D by AI agents; RE-Bench is built as the reusable instrument for monitoring exactly that.\n- **Suite sensitivity** \u2014 Time horizons are fitted, suite-specific estimates \u2014 change the task mix and the number moves. Not a claim about automating jobs.\n- **Saturation** \u2014 Fully saturating RE-Bench would mean agents significantly outperforming top ML engineers in this setting; the benchmark's small size is deliberate."},
  {"title": "Worked estimation", "body": "In this section you'll do what an evaluator does: read a horizon curve and score a research-engineering task. No code needed \u2014 a pencil works.\n1. **Assemble the suite.** Collect a diverse set of multi-step software/research tasks and time human experts on each \u2014 you need real human-minutes per task, not vibes.\n2. **Run the model.** Record success/failure on each task at a fixed attempt budget.\n3. **Fit the curve.** Plot success probability against human task length and fit a logistic curve. The P50 time horizon is the task length where the fitted curve crosses 50% success. (Current frontier: near 100% success on sub-4-minute human tasks, under 10% past ~4 human-hours \u2014 measured 2025-03-19.)\n4. **Track generations.** Repeat for successive models and fit the trend of P50 horizons over calendar time. METR's result: doubling every 195.8 days (~7 months), 95% CI [162, 223].\n5. **Stress-test the trend.** METR's sensitivity analysis: even a 10\u00d7 error in absolute measurement shifts the arrival of 'month-long tasks' by only ~2 years. That's what a robust trend looks like.\n6. **Apply the TH1.1 update.** With 228 tasks and the Inspect infrastructure, the long-run doubling stays ~7 months (196.5 days), but post-2023 it's 130.8 days \u2014 20% faster. Note the caveat METR states: part genuine acceleration, part suite composition change.\n7. **Now score an RE-Bench-style task.** Setup: give the solver (human or agent) a computer with GPUs, a scoring function (maximize accuracy, minimize runtime), and a fixed time budget. Normalize: 0 = starting score, 1 = reference solution. Example (from METR's report): prefix-sum GPU kernel \u2014 starting code 4.74 ms, reference solution 1.60 ms, best human expert 0.67 ms, o1-preview's custom CUDA kernel 0.64 ms. Score each attempt; compare best-of-k across budgets: agents dominate at 2h, humans at 8h and 32h.\n8. **Read the fine print before citing.** Only 7 environments; faster feedback loops than real research; measurements above ~16 human-hours are unreliable with the current suite."},
  {"title": "Project brief", "body": "Design a contamination-free evaluation for a capability claim. Pick a claim you have actually seen (e.g., 'our agent completes 8-hour software tasks autonomously'). Deliverable: a 2-page eval design with (1) 3+ environments built from scratch, with scoring functions and calibrated 0\u20131 scales; (2) a human-baselining plan (who, how many attempts, what time budget); (3) an anti-contamination plan (what's published, what's held back); (4) the metric you'll report and how you'll fit it; (5) a limitations section naming at least three ways your eval could mislead. Grading bar: if your limitations section is shorter than your results section, rewrite it."},
  {"title": "Frontier honesty", "body": "What decays: horizon values, doubling estimates (TH1 vs TH1.1 already differ), model scores on RE-Bench \u2014 all as-of 2026-10-07. What the metric does not claim: that models 'work 16 hours' in any ordinary sense, that whole jobs are automated, or that the trend extrapolates past the suite's reliable range. What endures: the method \u2014 contamination-free environments, calibrated human baselines, fitted success curves, stated confidence intervals. And METR's own caution, which we adopt as policy: the time horizon is a suite-specific fitted estimate of autonomous task-completion capability. Quote the interval, not the point."}
 ],
 "cards": [
  {"front": "RE-Bench, in one sentence?", "back": "METR's benchmark for AI-led ML research engineering: 7 realistic, open-ended environments where AI agents and human experts compete with the same resources, time limits, and calibrated 0\u20131 scoring."},
  {"front": "Why are RE-Bench environments built from scratch?", "back": "Anti-contamination: tasks that never appeared in training data, so scores measure capability rather than memorization. Most environments are held back unpublished."},
  {"front": "How is RE-Bench scoring calibrated?", "back": "0 = the starting solution's score, 1 = METR's strong reference solution \u2014 comparable across environments."},
  {"front": "The RE-Bench human baselines?", "back": "71 paid attempts by 61 distinct experts, up to 8 hours each; 82% reached non-zero scores, 24% matched or beat the reference solutions."},
  {"front": "The 2h/8h/32h crossover?", "back": "Best agents score ~4\u00d7 humans at a 2-hour budget; humans narrowly lead at 8 hours and reach ~2\u00d7 the top agent score at 32 hours across attempts."},
  {"front": "Why do agents win short and lose long?", "back": "Agents iterate 10\u00d7+ faster at far lower cost, but often fail to react to novel information or build coherently on earlier progress within a single run."},
  {"front": "The o1-preview kernel example?", "back": "Prefix-sum GPU kernel: starting code 4.74 ms, reference 1.60 ms, best human 0.67 ms \u2014 o1-preview's custom CUDA kernel reached 0.64 ms, beating the best human expert."},
  {"front": "Why does RE-Bench exist?", "back": "Frontier safety policies single out AI automation of AI R&D as a capability of concern; RE-Bench is the reusable instrument for measuring it \u2014 a measured approach to recursive self-improvement, not speculation."},
  {"front": "Define the time-horizon metric.", "back": "The human-expert task length at which an agent has an x% chance of success \u2014 typically P50 or P80 \u2014 read off a logistic curve fitted to model success vs. human task length."},
  {"front": "How is the P50 horizon fitted?", "back": "Time human experts on a diverse task suite, record model success per task, fit a logistic curve of success probability against human task length, read the 50% crossing."},
  {"front": "The doubling trend?", "back": "~7 months: P50 doubling every 195.8 days (95% CI [162, 223]) from 2019\u20132025; a SWE-bench Verified replication found under 3 months."},
  {"front": "What changed in Time Horizon 1.1 (2026-01-29)?", "back": "Suite 170\u2192228 tasks, long tasks 14\u219231, infrastructure Vivaria\u2192Inspect; post-2023 doubling 130.8 days (95% CI [107, 161]) \u2014 20% faster, partly genuine, partly suite composition."},
  {"front": "What the metric does NOT claim?", "back": "Not evidence models 'work 16 hours,' not whole-job automation, not extrapolation past the suite's reliable range \u2014 measurements above ~16 human-hours are unreliable."},
  {"front": "The critical-reading checklist for any capability eval?", "back": "Comparison fairness (same resources/time), contamination (unseen tasks), baselining quality (real experts, real time), suite sensitivity (would a different mix move the number?)."}
 ],
 "quiz": [
  {"q": "RE-Bench environments are built from scratch primarily to:", "choices": ["Increase difficulty", "Prevent training-data contamination", "Reduce cost", "Impress reviewers"], "answer": 1, "explain": "Covered in Concepts (anti-contamination design)."},
  {"q": "A score of 1.0 on an RE-Bench environment means:", "choices": ["A perfect solution", "Matched METR's strong reference solution", "Beat all humans", "Solved in under an hour"], "answer": 1, "explain": "Covered in Concepts (calibrated scoring)."},
  {"q": "How many human expert attempts baseline RE-Bench?", "choices": ["12", "71 attempts by 61 experts", "228", "1,900"], "answer": 1, "explain": "Covered in Concepts (human baselines) \u2014 71 attempts, 61 distinct experts."},
  {"q": "At a 2-hour budget, best agents vs human experts:", "choices": ["Agents score ~4\u00d7 higher", "Humans score ~4\u00d7 higher", "Roughly tied", "Agents score 2\u00d7 lower"], "answer": 0, "explain": "Covered in Concepts (the 2h/8h/32h crossover)."},
  {"q": "At 32 total hours across attempts:", "choices": ["Agents lead 4\u00d7", "Humans achieve ~2\u00d7 the top agent score", "Both saturate at 1.0", "Results are unpublished"], "answer": 1, "explain": "Covered in Concepts \u2014 humans show better returns to more time."},
  {"q": "The o1-preview kernel result demonstrates:", "choices": ["Agents always beat humans", "An agent beating the best human expert (0.64 ms vs 0.67 ms) on one kernel task \u2014 a data point, not a verdict", "GPUs are obsolete", "CUDA is easy"], "answer": 1, "explain": "Covered in Worked estimation step 7 \u2014 read single-task wins as data points."},
  {"q": "The P50 time horizon is:", "choices": ["The task length where the fitted success curve crosses 50%", "50% of tasks solved", "The median human task time", "Half the doubling period"], "answer": 0, "explain": "Covered in Concepts and Worked estimation step 3."},
  {"q": "The 2019\u20132025 P50 doubling trend:", "choices": ["~7 months (195.8 days, 95% CI [162, 223])", "~3 years", "~30 days", "No trend found"], "answer": 0, "explain": "Covered in Concepts (doubling time)."},
  {"q": "Time Horizon 1.1's post-2023 doubling estimate:", "choices": ["195.8 days", "130.8 days (95% CI [107, 161])", "365 days", "64 days"], "answer": 1, "explain": "Covered in Concepts (Time Horizon 1.1) \u2014 20% faster than the long-run trend."},
  {"q": "METR says measurements above ~16 human-hours are:", "choices": ["The most reliable", "Unreliable with the current suite", "Only for P80", "Validated by replication"], "answer": 1, "explain": "Covered in Worked estimation step 8 and Frontier honesty."},
  {"q": "A vendor claims 'our agent works 16-hour tasks' citing a P50 horizon. The checklist says:", "choices": ["Accept \u2014 P50 is standard", "Ask for the fitted curve, the suite, and the confidence interval \u2014 horizons are suite-specific fitted estimates", "Request the model weights", "Check the vendor's funding"], "answer": 1, "explain": "Covered in the critical-reading checklist and Frontier honesty \u2014 never cite a horizon without its suite."},
  {"q": "RE-Bench's self-declared limitation vs real ML research:", "choices": ["Too many environments", "Clearer objectives and faster feedback loops (<1 hour) than real research, where goals are ambiguous and feedback takes months", "Humans were unpaid", "Scores aren't calibrated"], "answer": 1, "explain": "Covered in Frontier honesty \u2014 the benchmark's own limitations section."}
 ],
 "scenarios": [
  {"id": "sc-metr-headline", "title": "The 4\u00d7 Headline", "context": "A tech outlet runs the headline 'AI BEATS HUMAN EXPERTS 4\u00d7 AT RESEARCH.' Your team is asked whether to cite it in a strategy memo.", "steps": [
   {"prompt": "Your first move?", "options": [
    {"text": "Find the budget the headline's number used: the 4\u00d7 figure is at a 2-hour budget \u2014 check the 8h and 32h results too", "correct": True, "why": "The crossover is the finding; any single budget is a slice. The protocol reads all three budgets before citing."},
    {"text": "Cite it \u2014 4\u00d7 is 4\u00d7", "correct": False, "why": "A headline number without its budget is a different claim than the paper's."},
    {"text": "Dismiss RE-Bench as too small", "correct": False, "why": "Seven environments is a stated limitation, not a dismissal \u2014 the honest move is to report it, not to wave it away."}]},
   {"prompt": "Your memo's verdict on the headline?", "options": [
    {"text": "'Agents lead 4\u00d7 at 2h; humans lead at 8h and 2\u00d7 at 32h \u2014 the crossover, not the headline, is the citable finding'", "correct": True, "why": "Citing the full crossover reports the paper's actual result with its budget dependence intact."},
    {"text": "Use the 4\u00d7 figure with a footnote", "correct": False, "why": "A footnote doesn't fix a headline that inverts the paper's conclusion at longer budgets."},
    {"text": "Find a friendlier benchmark", "correct": False, "why": "Shopping for numbers is the opposite of the as-of discipline."}]}]},
  {"id": "sc-metr-vendor-horizon", "title": "The 16-Hour Agent", "context": "A vendor's sales deck says 'P50 time horizon: 16 hours \u2014 our agent works a full human day.' Your company is evaluating the product for an autonomous coding pilot.", "steps": [
   {"prompt": "First diligence question?", "options": [
    {"text": "Show the fitted curve, the task suite, and the confidence interval \u2014 and note METR's own warning that measurements above ~16 human-hours are unreliable", "correct": True, "why": "A horizon without its suite and interval is marketing; METR's reliability ceiling is part of the metric's definition."},
    {"text": "Which model version?", "correct": False, "why": "Version matters, but the missing curve and suite are the load-bearing gaps."},
    {"text": "Can we get a discount?", "correct": False, "why": "Price negotiation before capability diligence is how pilots fail expensively."}]},
   {"prompt": "The vendor can't produce the curve. Verdict?", "options": [
    {"text": "Treat the 16-hour claim as unverified \u2014 pilot on your own measured tasks with your own baselines", "correct": True, "why": "Unverifiable capability claims get tested, not trusted; your own tasks are the only suite that matters for your pilot."},
    {"text": "Trust the number \u2014 vendors don't lie in decks", "correct": False, "why": "They optimize decks for sales; the checklist exists because of this sentence."},
    {"text": "Ask for customer references instead", "correct": False, "why": "References are useful but don't substitute for a measured capability claim."}]}]},
  {"id": "sc-metr-contaminated", "title": "The Contaminated Leaderboard", "context": "A new public benchmark claims a model 'solves 90% of senior-engineer tasks.' A colleague notices the benchmark's tasks were posted on a public forum two years ago \u2014 likely in the model's training data.", "steps": [
   {"prompt": "Your first move?", "options": [
    {"text": "Flag contamination: RE-Bench builds environments from scratch precisely because public tasks can't distinguish capability from memorization", "correct": True, "why": "Contamination is the first check in the critical-reading list \u2014 it invalidates frontier claims before any other analysis."},
    {"text": "Celebrate the 90%", "correct": False, "why": "A memorized test measures retrieval, not engineering ability."},
    {"text": "Retrain the model without the tasks", "correct": False, "why": "You can't retrain someone else's model; the evaluation is what's broken, not your training run."}]},
   {"prompt": "The benchmark authors say 'contamination doesn't matter much.' Your response?", "options": [
    {"text": "Ask for the contamination-controlled comparison: same model on held-back vs public tasks \u2014 without it, the 90% is uninterpretable for frontier claims", "correct": True, "why": "The burden of proof is on the claimant; RE-Bench's held-back design shows what 'controlled' looks like."},
    {"text": "Accept their expertise", "correct": False, "why": "'Trust us' is not a contamination control."},
    {"text": "Publish a rebuttal blog post", "correct": False, "why": "A private, evidence-first note to the authors beats a public fight \u2014 escalate only if they won't engage."}]}]}
 ],
 "drills": [
  {"id": "drill-metr-p50", "title": "P50 definition", "prompt": "The P50 time horizon is:", "choices": ["The 50th task in the suite", "The human task length where the fitted success curve crosses 50%", "Half of the P80 horizon", "50% of training compute"], "answer": 1, "explain": "Concepts \u2014 read off the logistic fit."},
  {"id": "drill-metr-crossover", "title": "Crossover budgets", "prompt": "In RE-Bench, agents beat humans 4\u00d7 at:", "choices": ["32-hour budgets", "8-hour budgets", "2-hour budgets", "All budgets"], "answer": 2, "explain": "Concepts \u2014 and humans lead at 8h and 32h."},
  {"id": "drill-metr-doubling", "title": "Doubling trend", "prompt": "The 2019\u20132025 P50 horizon doubling time:", "choices": ["195.8 days (~7 months)", "130.8 days", "365 days", "30 days"], "answer": 0, "explain": "Concepts \u2014 130.8 days is the post-2023 TH1.1 estimate."},
  {"id": "drill-metr-reliability", "title": "Reliability ceiling", "prompt": "METR warns that horizon measurements above ~16 human-hours are:", "choices": ["Gold standard", "Unreliable with the current suite", "Required for P80", "Peer-reviewed"], "answer": 1, "explain": "Worked estimation step 8 \u2014 don't cite past the suite's range."}
 ]
}

# ------------------------------------------------------- IL-12 supplement module
m12_horizon = {
 "id": "aieng-agentic-ai--agent-autonomy-ceilings",
 "code": "IL-12",
 "title": "Agent Autonomy Ceilings: Time Horizons",
 "weight": 1,
 "summary": "Welcome to the reality check every agent engineer needs. I'm your instructor for this module, and we're going to put a number on the most important design constraint in agentic systems: how long a task can you trust an agent to complete? METR's time-horizon research gives us the field's best-measured answer \u2014 a fitted P50 horizon that has doubled roughly every seven months \u2014 and this module teaches you to use it as an engineering boundary, not a marketing claim. Design your agents under the ceiling, and verify the ceiling yourself. All figures as of October 7, 2026.",
 "objectives": [
  "Define the P50/P80 time horizon and explain how it is fitted from human task times and model success curves",
  "Apply the as-of dated horizon as a reliability boundary when scoping agent deployments",
  "Identify what the horizon metric does not claim, and verify autonomy claims against the critical-reading checklist"
 ],
 "notes": [
  {"title": "Concepts", "body": "- **Time horizon (P50/P80)** \u2014 The human-expert task length at which an agent has a 50% (or 80%) chance of success, read off a logistic curve fitted to model success vs. human task length (METR).\n- **Logistic fit** \u2014 Plot success probability against human task length, fit the curve, read the 50% crossing. That crossing is your ceiling.\n- **Doubling: 195.8 days** \u2014 The 50%-reliability horizon doubled roughly every 7 months from 2019\u20132025 (95% CI [162, 223] days).\n- **TH1.1 post-2023: 130.8 days** \u2014 METR's January 2026 refresh finds the recent doubling 20% faster (95% CI [107, 161]) \u2014 ceilings move in months, not years.\n- **Suite sensitivity** \u2014 Horizons are fitted, suite-specific estimates. Change the task mix and the number moves.\n- **Reliability ceiling** \u2014 An engineering boundary: no unsupervised subtask longer than the measured P50 without decomposition or human checkpoints.\n- **Autonomy ceiling** \u2014 The design rule this module teaches: the ceiling is a boundary, not a target."},
  {"title": "Worked estimation", "body": "Apply the horizon to a deployment decision, step by step.\n1. **Get your ceiling.** Look up the as-of P50 horizon for your model class from METR's published estimates \u2014 and write down the date. A horizon without a date is a rumor.\n2. **Decompose the workflow.** Break your agent's job into subtasks, each with a human-time estimate (how long would a skilled person take?).\n3. **Compare.** Any subtask longer than the P50 gets one of three treatments: decompose it further, add a human checkpoint, or add verification (tests, review, rollback).\n4. **Mind the doubling.** At ~7 months per doubling (faster post-2023), today's ceiling is next quarter's floor plan \u2014 schedule a quarterly re-check of the published horizons.\n5. **Document it.** Write the ceiling, its as-of date, and the checkpoint plan into the runbook. The next engineer inherits your boundary, not your optimism."},
  {"title": "Project brief", "body": "Set an autonomy ceiling for a real agent design. Pick an agent use case you care about (coding assistant, ops runbook runner, research helper). Deliverable: a one-page ceiling memo with (1) the workflow decomposed into subtasks with human-time estimates, (2) the as-of P50 horizon you're designing against, with its source and date, (3) each over-ceiling subtask marked with its guardrail \u2014 decomposition, checkpoint, or verification, and (4) a re-check schedule. Grading bar: if every subtask fits under the ceiling with no guardrails, your decomposition is too coarse \u2014 break it down until the boundary bites."},
  {"title": "Frontier honesty", "body": "What decays: horizon values (the post-2023 acceleration already moved them), model-specific scores \u2014 all as-of 2026-10-07. What the metric does not claim: whole-job automation, or reliability past the suite's range (measurements above ~16 human-hours are unreliable). What endures: the discipline \u2014 never design past a measured ceiling on a vendor's word alone; verify on your own tasks, with your own baselines."}
 ],
 "cards": [
  {"front": "The autonomy ceiling for an agent design?", "back": "The as-of dated P50 time horizon for your model class \u2014 subtasks longer than it need decomposition or human-in-the-loop."},
  {"front": "P50 horizon, fitted how?", "back": "Logistic curve of model success vs human task length; the 50% crossing. ~7-month doubling (195.8 days, 2019\u20132025)."},
  {"front": "TH1.1's update for engineers?", "back": "Post-2023 doubling 130.8 days \u2014 ceilings move faster than the long-run trend; re-check quarterly."},
  {"front": "A vendor claims 16-hour autonomy. Your response?", "back": "Show the curve, the suite, the interval \u2014 METR warns >16h measurements are unreliable; verify on your own tasks."},
  {"front": "The one-line design rule?", "back": "No subtask past the measured P50 without a checkpoint. The ceiling is a boundary, not a target."}
 ],
 "quiz": [
  {"q": "Your agent workflow has a 3-hour unsupervised subtask; the as-of P50 horizon is ~1 hour. You should:", "choices": ["Ship it \u2014 agents improve", "Decompose the subtask or add human checkpoints", "Switch vendors", "Add more GPUs"], "answer": 1, "explain": "Covered in Worked estimation \u2014 design under the ceiling."},
  {"q": "The P50 horizon doubles roughly every:", "choices": ["7 years", "7 months (195.8 days)", "7 days", "7 hours"], "answer": 1, "explain": "Covered in Concepts."},
  {"q": "Why re-check the horizon quarterly?", "choices": ["It's fun", "Post-2023 doubling is 130.8 days \u2014 ceilings move in months", "Vendors require it", "Compliance"], "answer": 1, "explain": "Covered in Concepts (TH1.1) \u2014 the ceiling is a moving target."},
  {"q": "The horizon metric does NOT establish:", "choices": ["A fitted task-length estimate", "That whole jobs are automated", "A doubling trend", "Suite sensitivity"], "answer": 1, "explain": "Covered in Frontier honesty \u2014 capability on tasks is not job automation."}
 ]
}

# ------------------------------------------------------- IL-16 supplement module
m16_rebench = {
 "id": "advanced-ml--re-bench-agents-ml-research",
 "code": "IL-16",
 "title": "RE-Bench: Agents Doing ML Research",
 "weight": 1,
 "summary": "Welcome to the benchmark that grades AI on your own craft. I'm your instructor for this module, and we're studying RE-Bench \u2014 METR's head-to-head contest between AI agents and human experts at real machine-learning research engineering: fitting scaling laws, optimizing GPU kernels, designing architectures under constraints. You'll learn how the benchmark is built, what the 2h/8h/32h crossover tells us about where agents help and where they don't, and how to read any 'AI does research' claim with an evaluator's eye. All figures as of October 7, 2026.",
 "objectives": [
  "Describe RE-Bench's design: contamination-free environments, calibrated 0\u20131 scoring, faithful human baselines",
  "Explain the 2h/8h/32h crossover and what it implies for human\u2013agent collaboration in ML research",
  "Apply the critical-reading checklist to 'AI does ML research' claims"
 ],
 "notes": [
  {"title": "Concepts", "body": "- **RE-Bench** \u2014 METR's benchmark (2024-11-22) for AI-led ML research engineering: 7 realistic, open-ended environments, agents vs human experts, same resources and time limits.\n- **Anti-contamination design** \u2014 Environments built from scratch; most held back unpublished. Public tasks can't separate capability from memorization.\n- **Calibrated scoring** \u2014 0 = starting solution's score, 1 = METR's strong reference solution; comparable across environments.\n- **Human baselines** \u2014 71 attempts by 61 experts, up to 8 hours each; 82% non-zero, 24% matched or beat the reference.\n- **The 2h/8h/32h crossover** \u2014 Agents ~4\u00d7 humans at 2h; humans narrowly lead at 8h; humans ~2\u00d7 the top agent at 32h across attempts.\n- **The kernel example** \u2014 o1-preview's custom CUDA kernel: 0.64 ms vs best human 0.67 ms (start 4.74 ms, reference 1.60 ms) \u2014 a data point, not a verdict.\n- **Capability of concern** \u2014 AI automation of AI R&D is the monitored capability; RE-Bench is the reusable instrument."},
  {"title": "Worked estimation", "body": "Score an RE-Bench-style ML task yourself.\n1. **Pick a research-engineering task** with a measurable objective \u2014 e.g., fit a scaling law from provided training runs, or optimize a small kernel.\n2. **Define the scoring function** and calibrate it: 0 = the baseline you're given, 1 = a strong reference solution you write (or borrow and verify).\n3. **Set the time budget** and run both sides: an agent with a fixed attempt budget, and yourself (or a colleague) with the same clock.\n4. **Score best-of-k** across attempts at 2h, then extend to 8h. Watch for the crossover pattern: where does the agent's 10\u00d7+ iteration speed win, and where does coherent long-horizon work take over?\n5. **Write the limitations** before the conclusions: one task, one agent, one human \u2014 what would you need to make this a claim about 'AI doing research'?"},
  {"title": "Project brief", "body": "Replicate one RE-Bench-style environment from scratch. Do not adapt a public tutorial \u2014 build the task, the starting code, and the scoring function yourself. Deliverable: the environment plus a 1-page report with (1) the task and why it's realistic ML research engineering, (2) your calibrated 0 and 1, (3) a timed human attempt (yours or a colleague's) and an agent attempt under the same budget, (4) the comparison, and (5) a limitations section. Grading bar: the limitations section must name contamination risk, baseline quality, and feedback-loop realism \u2014 the three things that separate an eval from a demo."},
  {"title": "Frontier honesty", "body": "What decays: model scores on these environments (models train on; scores inflate), published horizon values \u2014 all as-of 2026-10-07. What the benchmark does not claim: that 7 environments generalize to all of ML research, or that fast-feedback tasks stand in for months-long ambiguous research. What endures: the design pattern \u2014 contamination-free tasks, calibrated scoring, real human baselines, reported budgets. Cite the date; report the budgets."}
 ],
 "cards": [
  {"front": "RE-Bench in one line for an ML engineer?", "back": "7 contamination-free ML research-engineering environments; agents and 61 human experts compete on calibrated 0\u20131 scoring."},
  {"front": "The crossover and what it means for your workflow?", "back": "Agents win at 2h budgets (10\u00d7+ iteration speed), humans at 8h/32h \u2014 use agents for fast sweeps, humans for coherent long-horizon work."},
  {"front": "The kernel example's lesson?", "back": "o1-preview's custom CUDA kernel (0.64 ms) beat the best human (0.67 ms) \u2014 agents can win well-scoped optimization tasks; that's a data point, not a verdict on research."},
  {"front": "Calibrated scoring: 0 and 1?", "back": "0 = starting solution's score, 1 = METR's strong reference \u2014 comparable across environments."},
  {"front": "Before citing an 'AI researcher' claim?", "back": "Check contamination, baselines, budgets, and suite size \u2014 the critical-reading checklist."}
 ],
 "quiz": [
  {"q": "Why do RE-Bench tasks have faster feedback loops than real ML research?", "choices": ["To save money", "Deliberate design trade-off \u2014 real research has ambiguous goals and months-long feedback; the benchmark's limits are stated", "Agents prefer it", "Humans are slow"], "answer": 1, "explain": "Covered in Frontier honesty \u2014 know what the instrument doesn't measure."},
  {"q": "An agent beats your best engineer on a kernel-optimization task. The correct conclusion?", "choices": ["Engineers are obsolete", "One well-scoped win \u2014 check budgets, baselines, and whether the task generalizes before changing the workflow", "Fire the engineer", "Publish immediately"], "answer": 1, "explain": "Covered in Concepts (kernel example) \u2014 data point, not verdict."},
  {"q": "RE-Bench's human baseline comprises:", "choices": ["12 interns", "71 attempts by 61 experts, up to 8 hours each", "1,000 crowd workers", "No humans \u2014 simulated"], "answer": 1, "explain": "Covered in Concepts."},
  {"q": "For your team's ML workflow, the crossover suggests:", "choices": ["Replace researchers with agents", "Agents for fast iteration sweeps; humans for coherent multi-hour research arcs", "Avoid agents entirely", "Only use agents at 32h budgets"], "answer": 1, "explain": "Covered in Worked estimation \u2014 play to each side's returns-to-time."}
 ]
}

# ------------------------------------------------------- course-level additions
NEW_OBJECTIVES_23 = [
 "Forecast frontier capabilities from physical inputs with stated assumptions, dated intervals, and a decay plan",
 "Read a capability evaluation critically: contamination, baselines, suite sensitivity, and what the metric does not claim"
]
NEW_SOURCES_23 = [
 {"name": "Epoch AI \u2014 How many AI agents could we run?", "url": "https://epoch.ai/publications/estimating-the-agent-population", "retrieved": "2026-10-07"},
 {"name": "Epoch AI \u2014 Publications index", "url": "https://epoch.ai/publications", "retrieved": "2026-10-07"},
 {"name": "Villalobos et al. \u2014 Will we run out of data? (arXiv abstract)", "url": "https://arxiv.org/abs/2211.04325", "retrieved": "2026-10-07"},
 {"name": "Villalobos et al. \u2014 Will we run out of data? (full text, HTML v2)", "url": "https://arxiv.org/html/2211.04325v2", "retrieved": "2026-10-07"},
 {"name": "METR \u2014 Evaluating frontier AI R&D capabilities (RE-Bench)", "url": "https://metr.org/blog/2024-11-22-evaluating-r-d-capabilities-of-llms/", "retrieved": "2026-10-07"},
 {"name": "RE-Bench paper (arXiv abstract)", "url": "https://arxiv.org/abs/2411.15114", "retrieved": "2026-10-07"},
 {"name": "METR \u2014 Measuring AI ability to complete long tasks", "url": "https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/", "retrieved": "2026-10-07"},
 {"name": "METR \u2014 Time Horizon 1.1", "url": "https://metr.org/blog/2026-1-29-time-horizon-1-1/", "retrieved": "2026-10-07"}
]
NEW_ARC_PHASE = {"phase": "Phase 4 \u2014 Measurement & forecasting", "title": "How the frontier quantifies itself", "body": "Capability forecasting from physical inputs (Epoch AI: the data wall, agent capacity, cost curves) and capability evaluation (METR: RE-Bench, the time-horizon method). Modules 11\u201312 \u2014 the instruments the frontier uses to measure itself, taught with the as-of discipline that keeps them honest."}
NEW_PRIORITIES = [
 {"label": "Measurement: capability forecasting (module 11)", "minutes": 720},
 {"label": "Evaluation: RE-Bench + time horizons (module 12)", "minutes": 720}
]
NEW_BATTLEPLAN = [
 {"id": "bp23-7", "title": "Complete capability forecasting (module 11); run the forecasting-workbench sim", "minutes": 360},
 {"id": "bp23-8", "title": "Complete RE-Bench + time horizons (module 12); work both scenarios; run horizon-reader", "minutes": 360}
]
NEW_MOCKTASKS = [
 {"id": "mock-epoch-1", "type": "choice", "q": "Epoch's agent-capacity estimate multiplies:", "choices": ["HBM shipments by model count", "Effective hardware supply (GB300 equivalents) by serving capacity per GB300", "Training FLOPs by inference FLOPs", "Data centers by GPUs each"], "answer": 1, "explain": "A = E \u00d7 c \u2014 covered in the module's Concepts section."},
 {"id": "mock-epoch-2", "type": "choice", "q": "The data-wall paper's median exhaustion year, and what moves it earlier?", "choices": ["2028; overtraining by 1\u20132 years", "2024; better filtering", "2032; synthetic data", "2030; regulation"], "answer": 0, "explain": "Covered in Worked estimation \u2014 median 2028, earlier if frontier models are overtrained."},
 {"id": "mock-epoch-3", "type": "choice", "q": "Epoch's capacity-glut warning is fundamentally about:", "choices": ["Chip shortages", "Demand failing to absorb built capacity", "Electricity prices", "Model quality"], "answer": 1, "explain": "Covered in Concepts \u2014 $2.6\u20135.3T/yr implied vs ~$1T revenue."},
 {"id": "mock-epoch-4", "type": "choice", "q": "A forecast states a single year with no interval and no date. Per the module's honesty rule it is:", "choices": ["Admirably precise", "Incomplete \u2014 forecasts need stated assumptions, intervals, and as-of dates", "Ready to publish", "Better than a range"], "answer": 1, "explain": "Covered in Frontier honesty \u2014 the as-of discipline."},
 {"id": "mock-metr-1", "type": "choice", "q": "RE-Bench calibrates scores so that 1.0 equals:", "choices": ["A perfect solution", "METR's strong reference solution", "The best human attempt", "The fastest submission"], "answer": 1, "explain": "Covered in the module's Concepts section."},
 {"id": "mock-metr-2", "type": "choice", "q": "The headline 'agents beat humans 4\u00d7' describes which budget?", "choices": ["32 hours", "8 hours", "2 hours", "Unlimited"], "answer": 2, "explain": "Covered in Concepts \u2014 the crossover: agents lead at 2h, humans at 8h and 32h."},
 {"id": "mock-metr-3", "type": "choice", "q": "The P50 time horizon doubled every ~195.8 days from 2019\u20132025. The TH1.1 post-2023 estimate is:", "choices": ["Slower at 365 days", "Faster at 130.8 days", "Unchanged", "Unknown \u2014 unpublished"], "answer": 1, "explain": "Covered in Concepts (Time Horizon 1.1)."},
 {"id": "mock-metr-4", "type": "choice", "q": "Citing a vendor's '16-hour autonomy' claim without the fitted curve violates:", "choices": ["No rule \u2014 P50 is standard", "The critical-reading checklist: horizons are suite-specific fitted estimates with reliability ceilings", "Copyright", "Statistical significance"], "answer": 1, "explain": "Covered in Frontier honesty \u2014 METR warns >~16h measurements are unreliable."}
]
NEW_CHEATSHEETS = [
 {"title": "Capability-Forecasting Formula Sheet", "blocks": [
  {"h": "Data-wall ledger", "body": "Demand compounds with sqrt(compute); supply is finite web text; adjust and propagate uncertainty.", "code": "demand: dataset ~ sqrt(training compute)\nsupply: 250B pages x 7000 B/page -> tokens\nstock: CC 130T | indexed 510T | web 3100T (tokens)\nwindow: 2026-2032, median 2028\nscale: ~4e14 tokens, ~5e28 FLOP", "lang": "text"},
  {"h": "Agent capacity", "body": "Hardware supply times serving capacity; then check demand.", "code": "A = E x c\nE: HBM 2025-27 in GB300 equivalents\nc: sessions/GB300 (TraceLab $/hr | AgentX benches)\n=> 30-170M frontier agents | 1.9B open sessions\ndemand check: 20% capacity -> $2.6-5.3T/yr vs ~$1T revenue", "lang": "text"},
  {"h": "Cost curve", "body": "Budget in ranges; revisit quarterly.", "code": "-47%/quarter (~13x/yr) since 2023  [Epoch, Sep 2026]\nfaster than electricity/compute/batteries/DNA seq", "lang": "text"},
  {"h": "Honesty rule", "body": "Date everything; intervals, not points.", "code": "as-of 2026-10-07 on all figures\n2022 est ~2024 -> revised ~2028 (filtering beat assumptions)\nconstraint moved: data supply -> inference economics + demand", "lang": "text"}]},
 {"title": "Evaluation-Reading Checklist", "blocks": [
  {"h": "Contamination", "body": "Were the tasks built from scratch and held back? Public tasks measure memorization.", "code": "ask: unseen by training? held-back split?", "lang": "text"},
  {"h": "Baselines", "body": "Real experts, real time budgets, same resources as the agent.", "code": "RE-Bench bar: 71 attempts, 61 experts, 8h each", "lang": "text"},
  {"h": "Budgets", "body": "Report every budget \u2014 the crossover is the finding.", "code": "2h: agents 4x | 8h: humans lead | 32h: humans 2x", "lang": "text"},
  {"h": "Horizons", "body": "Fitted, suite-specific; mind the reliability ceiling.", "code": "P50: 50% crossing of logistic fit\ndoubling: 195.8d (2019-25); 130.8d post-2023\n>~16h unreliable; quote intervals", "lang": "text"}]}
]
NEW_ANSWERBANK = [
 {"q": "How do I forecast an AI capability without guessing?", "a": "Ledger both sides like Epoch: model demand from scaling laws, estimate supply from physical measurements, adjust honestly (quality filtering down, multi-epoch up), propagate uncertainty with Monte Carlo, and report an interval with an as-of date. A forecast without stated assumptions and a date is a guess with formatting."},
 {"q": "What does '30\u2013170 million agents' actually mean?", "a": "Epoch's October 2026 estimate of how many concurrent frontier-model agents the 2025\u201327 HBM buildout could serve (A = E \u00d7 c) \u2014 or ~1.9 billion sessions of an efficient open model. It is a capacity estimate, not a demand forecast: Epoch's own warning is that demand may not fill it, a potential capacity glut."},
 {"q": "How should I read a claim that an AI agent 'works N-hour tasks'?", "a": "Ask for the fitted curve, the task suite, and the confidence interval \u2014 the time horizon is a suite-specific fitted estimate, and METR warns measurements above ~16 human-hours are unreliable with the current suite. Then check contamination, baselines, and whether the number survives the critical-reading checklist."},
 {"q": "Why do frontier numbers need as-of dates?", "a": "Because they decay: the 2022 data-wall estimate said ~2024 and was revised to ~2028 when web data filtered better than assumed, and the binding constraint moved from training-data supply to inference economics and demand. The date is part of the claim."}
]
NEW_TERMINALSIMS = [
 {"id": "forecasting-workbench", "title": "Forecasting Workbench", "brief": "Practice the capability-forecasting method: reproduce Epoch's data-wall and agent-capacity calculations from their published inputs.", "prompt": "forecaster@il:~$", "commands": [
  {"cmd": "help", "out": "commands: forecast data-wall | forecast agent-capacity | forecast cost-curve | forecast decay"},
  {"cmd": "forecast data-wall", "out": "DATA WALL (Villalobos et al., ICML 2024; as of 2026-10-07)\n demand: dataset size ~ sqrt(training compute)  [Kaplan; Chinchilla]\n supply: ~250B pages x ~7000 bytes/page -> tokens (byte-pair)\n adjust: quality filtering DOWN, multi-epoch training UP\n result: 2026-2032 window, median 2028\n scale at exhaustion: ~4e14 tokens, ~5e28 FLOP (non-overtrained)"},
  {"cmd": "forecast agent-capacity", "out": "AGENT CAPACITY (Epoch AI, 2026-10-02)\n A = E x c\n E = HBM shipped 2025-27, in GB300 equivalents\n c = concurrent sessions/GB300 (TraceLab $/agent-hr; AgentX benches)\n result: ~30-170M frontier agents | ~1.9B open-model sessions\n reference rate: $30/agent-hour (pooled: $15.5-$50.2 by harness)"},
  {"cmd": "forecast cost-curve", "out": "PLUNGING PRICE OF THOUGHT (Epoch AI, Sep 2026)\n cost of fixed benchmark performance: -47%/quarter (~13x/year) since 2023\n faster than electricity / compute / batteries / DNA sequencing\n use: budget in ranges, revisit quarterly"},
  {"cmd": "forecast decay", "out": "DECAY LESSON\n 2022 estimate: data wall ~2024 -> revised to ~2028 (web data filtered better)\n binding constraint moved: training-data supply -> inference economics + demand\n rule: every figure dated; every forecast an interval"}]},
 {"id": "horizon-reader", "title": "Horizon Reader", "brief": "Read METR's autonomy measurements: fit the P50 horizon, check the doubling trend, and respect the reliability ceiling.", "prompt": "evaluator@il:~$", "commands": [
  {"cmd": "help", "out": "commands: horizon p50 | horizon doubling | horizon rebench | horizon caveats"},
  {"cmd": "horizon p50", "out": "P50 TIME HORIZON (METR; as of 2026-10-07)\n definition: human task length where fitted success curve crosses 50%\n method: time experts -> logistic fit of success vs human-minutes\n now: ~100% under 4 human-minutes; <10% past ~4 human-hours (2025-03-19)"},
  {"cmd": "horizon doubling", "out": "DOUBLING TREND\n 2019-2025: 195.8 days (~7 months), 95% CI [162, 223]\n TH1.1 post-2023: 130.8 days (95% CI [107, 161]) -- 20% faster\n sensitivity: 10x measurement error shifts 'month-long tasks' by only ~2 years"},
  {"cmd": "horizon rebench", "out": "RE-BENCH (METR, 2024-11-22)\n 7 contamination-free ML research environments, 0-1 calibrated scoring\n baselines: 71 attempts, 61 experts, 8h each\n crossover: agents 4x @2h | humans lead @8h | humans 2x @32h\n example: o1-preview CUDA kernel 0.64ms beats best human 0.67ms"},
  {"cmd": "horizon caveats", "out": "CAVEATS (METR's own)\n suite-specific fitted estimate -- not job automation\n >~16 human-hour measurements unreliable with current suite\n 7 environments; faster feedback than real research\n quote the interval, not the point"}]}
]

# ------------------------------------------------------- catalog entries
SHARDO_MODULES = [
 {"id": "capability-forecasting-epoch", "title": "Frontier Capability Forecasting", "kind": "core",
  "topics": ["Forecasting from physical inputs: data stocks, chip shipments, cost curves", "The data-wall model: scaling-law demand vs. estimated supply", "Stock estimates and the 2026\u20132032 exhaustion window", "Agent-capacity estimation: A = E \u00d7 c", "Inference cost curves and the capacity-glut question", "The decay lesson: as-of dating and moving constraints"],
  "sources": [
   {"name": "Epoch AI \u2014 How many AI agents could we run?", "url": "https://epoch.ai/publications/estimating-the-agent-population", "note": "October 2026 report read in full; HBM-to-agents method and demand analysis."},
   {"name": "Epoch AI \u2014 Publications index", "url": "https://epoch.ai/publications", "note": "Live corpus index; cost curves, chip-supply tracking, adoption measurement threads."}],
  "il_provides": "The discipline of turning unobservable frontier quantities into bounded, dated forecasts: the data-wall ledger, the A = E \u00d7 c agent-capacity method, and Epoch's inference cost curves. Every figure carries its as-of date, because in capability forecasting the date is part of the claim."},
 {"id": "evaluating-ai-metr", "title": "Measuring AI Itself: RE-Bench and Time Horizons", "kind": "core",
  "topics": ["RE-Bench: 7 contamination-free ML research environments", "Calibrated scoring and the 71-attempt human baseline", "The 2h/8h/32h human-vs-agent crossover", "The time-horizon metric: P50/P80 from fitted success curves", "The ~7-month doubling trend and the TH1.1 refresh", "Reading evaluations critically: contamination, baselines, suite sensitivity"],
  "sources": [
   {"name": "METR \u2014 Evaluating frontier AI R&D capabilities (RE-Bench)", "url": "https://metr.org/blog/2024-11-22-evaluating-r-d-capabilities-of-llms/", "note": "RE-Bench release post; design, baselines, and crossover findings."},
   {"name": "METR \u2014 Measuring AI ability to complete long tasks", "url": "https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/", "note": "Time-horizon methodology and the doubling-time trend."}],
  "il_provides": "The measurement discipline behind autonomy claims: RE-Bench's head-to-head agent-vs-expert design and the time-horizon method that compresses 'how autonomous?' into a fitted number. Taught with METR's own caveats \u2014 suite-specific, dated, and never a claim about whole jobs."}
]
SHARDL_GENAI = {"id": "inference-economics-agent-capacity", "title": "Inference Economics & Agent Capacity", "kind": "elective",
 "topics": ["Epoch's agent-capacity method: A = E \u00d7 c", "Hourly agent economics: $/agent-hour by harness", "The plunging price of thought: ~47%/quarter cost curves", "Capacity glut: when demand, not chips, binds"],
 "sources": [
  {"name": "Epoch AI \u2014 How many AI agents could we run?", "url": "https://epoch.ai/publications/estimating-the-agent-population", "note": "Agent-capacity method and hourly economics (Oct 2026)."},
  {"name": "Epoch AI \u2014 Publications index", "url": "https://epoch.ai/publications", "note": "Inference cost-curve thread ('the plunging price of thought')."}],
 "il_provides": "What an agent hour actually costs and how many the buildout can serve: the serving-economics lens every production agent system needs, dated honestly."}
SHARDL_ML = {"id": "training-data-constraints", "title": "Training-Data Constraints & Scaling Laws", "kind": "elective",
 "topics": ["The data-wall paper: demand vs. supply ledgers", "Chinchilla-optimal data/compute ratios", "Quality filtering and multi-epoch adjustments", "The 2026\u20132032 exhaustion window and its caveats"],
 "sources": [
  {"name": "Villalobos et al. \u2014 Will we run out of data? (arXiv)", "url": "https://arxiv.org/abs/2211.04325", "note": "ICML 2024 position paper; stock estimates and Monte Carlo window."}],
 "il_provides": "The honest account of data as a scaling input: how much public text exists, what adjustments apply, and why the constraint moves \u2014 the scaling-law context behind every data decision."}

# ------------------------------------------------------- apply
def check_quiz(items, where):
    for i, q in enumerate(items):
        assert (set(q.keys()) >= {"q", "choices", "answer", "explain"} or
                set(q.keys()) >= {"prompt", "choices", "answer", "explain"}), f"{where}[{i}] quiz keys"
        assert len(q["choices"]) == 4, f"{where}[{i}] choices != 4"
        assert isinstance(q["answer"], int) and 0 <= q["answer"] < 4, f"{where}[{i}] bad answer index"
        assert q["explain"].strip(), f"{where}[{i}] empty explain"
        assert "video" not in q["explain"].lower(), f"{where}[{i}] video reference in explain"
        for c in q["choices"]:
            assert isinstance(c, str) and c.strip(), f"{where}[{i}] empty choice"

def check_cards(items, where):
    for i, c in enumerate(items):
        assert c.get("front", "").strip() and c.get("back", "").strip(), f"{where}[{i}] card front/back"

def check_scenarios(items, where):
    for s in items:
        assert s.get("id") and s.get("title") and s.get("context"), f"{where} scenario meta"
        assert len(s["steps"]) >= 2, f"{where}/{s['id']} steps"
        for st in s["steps"]:
            assert st.get("prompt"), f"{where}/{s['id']} step prompt"
            assert len(st["options"]) >= 3, f"{where}/{s['id']} options"
            assert sum(1 for o in st["options"] if o.get("correct")) == 1, f"{where}/{s['id']} must have exactly 1 correct"
            for o in st["options"]:
                assert o.get("text") and o.get("why"), f"{where}/{s['id']} option text/why"

def check_module(m, where, need_asof):
    assert m.get("id") and m.get("title") and m.get("summary"), f"{where} module meta"
    if need_asof:
        assert m.get("asOf") == "2026-10-07", f"{where} asOf"
    titles = [n["title"] for n in m["notes"]]
    assert "Concepts" in titles and "Worked estimation" in titles and "Project brief" in titles and "Frontier honesty" in titles, f"{where} notes titles {titles}"
    assert m["notes"][0]["body"].count("\n- **") >= 5, f"{where} Concepts glossary bullets"
    check_cards(m["cards"], where + "/cards")
    check_quiz(m["quiz"], where + "/quiz")
    check_scenarios(m.get("scenarios", []), where)
    check_quiz(m.get("drills", []), where + "/drills")

def scan_text(obj, where, errors):
    if isinstance(obj, str):
        if COMPETITORS.search(obj):
            errors.append(f"competitor hit in {where}: {obj[:80]}")
        if BANNED.search(obj):
            errors.append(f"banned hit in {where}: {obj[:80]}")
    elif isinstance(obj, dict):
        for k, v in obj.items():
            scan_text(v, f"{where}.{k}", errors)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            scan_text(v, f"{where}[{i}]", errors)

def scan_urls(obj, where, errors):
    if isinstance(obj, dict):
        if set(obj.keys()) >= {"name", "url"} and "url" in obj and isinstance(obj["url"], str) and obj["url"].startswith("http"):
            if obj["url"] not in ALLOWED_URLS:
                # only flag NEW entries (whitelist); pre-existing course links may include other URLs
                pass
        for v in obj.values():
            scan_urls(v, where, errors)
    elif isinstance(obj, list):
        for v in obj:
            scan_urls(v, where, errors)

errors = []

# ---- IL-23
d23 = load(P23)
assert len(d23["modules"]) == 10, "il23 module count changed?"
assert not any(m["id"] in ("m23-epoch-ai", "m23-metr-evals") for m in d23["modules"]), "modules already present"
for m in (m23_epoch, m23_metr):
    check_module(m, "il23/" + m["id"], need_asof=True)
d23["modules"].extend([m23_epoch, m23_metr])
d23["hours"] = 48
d23["mockMinutes"] = 180
d23["updatedAt"] = "2026-10-07"
d23["objectives"] = [("Explain the settled core mechanisms of twelve frontier fields" if "ten frontier fields" in o else o) for o in d23["objectives"]] + NEW_OBJECTIVES_23
d23["blurb"] = d23["blurb"].replace("Ten seed modules", "Twelve seed modules")
if "capability forecasting" not in d23["blurb"]:
    d23["blurb"] = d23["blurb"].rstrip() + " New: capability forecasting from physical inputs (Epoch AI) and AI capability evaluation (METR)."
d23["arc"].append(NEW_ARC_PHASE)
d23["priorities"].extend(NEW_PRIORITIES)
for bp in d23["battlePlan"]:
    if bp["id"] == "bp23-6":
        bp["title"] = "Sit the 38-task timed mock; review misses against the cheat sheets"
d23["battlePlan"].extend(NEW_BATTLEPLAN)
check_quiz(NEW_MOCKTASKS, "il23/new-mocktasks")
d23["mockTasks"].extend(NEW_MOCKTASKS)
d23["cheatSheets"].extend(NEW_CHEATSHEETS)
d23["answerBank"].extend(NEW_ANSWERBANK)
d23["terminalSims"] = NEW_TERMINALSIMS
existing_urls = {s["url"] for s in d23["sourceLinks"]}
for s in NEW_SOURCES_23:
    assert s["url"] in ALLOWED_URLS, f"new source not whitelisted: {s['url']}"
    assert s["url"] not in existing_urls, f"dup source: {s['url']}"
d23["sourceLinks"].extend(NEW_SOURCES_23)
# priorities total must equal hours*60
ptot = sum(p["minutes"] for p in d23["priorities"])
assert ptot == d23["hours"] * 60, f"priorities total {ptot} != {d23['hours']*60}"

# ---- IL-12
d12 = load(P12)
assert not any(m["id"] == m12_horizon["id"] for m in d12["modules"]), "il12 module already present"
check_module(m12_horizon, "il12/horizon", need_asof=False)
assert len(m12_horizon["cards"]) == 5 and len(m12_horizon["quiz"]) == 4 and len(m12_horizon["objectives"]) == 3 and len(m12_horizon["notes"]) == 4
d12["modules"].append(m12_horizon)
d12["updatedAt"] = "2026-10-07"

# ---- IL-16
d16 = load(P16)
assert not any(m["id"] == m16_rebench["id"] for m in d16["modules"]), "il16 module already present"
check_module(m16_rebench, "il16/rebench", need_asof=False)
assert len(m16_rebench["cards"]) == 5 and len(m16_rebench["quiz"]) == 4 and len(m16_rebench["objectives"]) == 3 and len(m16_rebench["notes"]) == 4
d16["modules"].append(m16_rebench)
d16["updatedAt"] = "2026-10-07"

# ---- shard-o / shard-l handled separately by build_catalog.py (format-preserving); skipped here

# ---- scans over everything new
for name, obj in [("m23_epoch", m23_epoch), ("m23_metr", m23_metr), ("m12_horizon", m12_horizon),
                  ("m16_rebench", m16_rebench),
                  ("new_sources", NEW_SOURCES_23), ("new_mocktasks", NEW_MOCKTASKS),
                  ("new_cheatsheets", NEW_CHEATSHEETS), ("new_answerbank", NEW_ANSWERBANK),
                  ("new_sims", NEW_TERMINALSIMS), ("new_arc", NEW_ARC_PHASE)]:
    scan_text(obj, name, errors)
# also scan the full updated course files for competitors/banned (pre-existing content should already be clean)
for name, obj in [("d23", d23), ("d12", d12), ("d16", d16)]:
    scan_text(obj, name, errors)
assert not errors, "SCAN FAILURES:\n" + "\n".join(errors)

# ---- write (course files only; catalog files handled by build_catalog.py)
dump(P23, d23, trailing_newline=True); json.load(open(P23, encoding="utf-8"))
dump(P12, d12, trailing_newline=False); json.load(open(P12, encoding="utf-8"))
dump(P16, d16, trailing_newline=True); json.load(open(P16, encoding="utf-8"))

print("WRITE OK")
print("il23 modules:", len(d23["modules"]), "| cards:", sum(len(m["cards"]) for m in d23["modules"][-2:]),
      "| quiz:", sum(len(m["quiz"]) for m in d23["modules"][-2:]),
      "| scenarios:", sum(len(m["scenarios"]) for m in d23["modules"][-2:]),
      "| drills:", sum(len(m["drills"]) for m in d23["modules"][-2:]),
      "| mockTasks:", len(d23["mockTasks"]), "| cheatSheets:", len(d23["cheatSheets"]),
      "| answerBank:", len(d23["answerBank"]), "| sims:", len(d23["terminalSims"]),
      "| hours:", d23["hours"], "| mockMinutes:", d23["mockMinutes"], "| sources:", len(d23["sourceLinks"]))
print("il12 modules:", len(d12["modules"]), "| il16 modules:", len(d16["modules"]))
print("competitor/banned scan: 0 hits")

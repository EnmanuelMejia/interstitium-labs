"""IL-15 retrofit: Data Science track (6 modules)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load, apply_all

CONTENT = {
    "data-science-interview-prep--stats-prob-iv": {
        "summary": (
            "Welcome to the Data Science Interview Prep track of the IL-15 Data Engineering & Analytics "
            "Interview Prep course. I'm your instructor for this track, and in this module we're going to build "
            "the probability floor every DS interview stands on: distributions, expectation, the central limit "
            "theorem, and the discipline of saying exactly what a p-value means — and what it doesn't."
        ),
        "concepts": (
            "- **normal distribution** — The bell curve parameterized by mean and variance; the limit shape of "
            "sample means via the CLT, and the backbone of classical inference.\n"
            "- **binomial distribution** — Counts of successes in n independent yes/no trials; the model for "
            "conversion counts and click tallies.\n"
            "- **Poisson distribution** — Counts of events over time or space at a constant rate; the model for "
            "arrivals, errors per hour, requests per minute.\n"
            "- **expectation** — The long-run average; linear (E[aX+bY] = aE[X]+bE[Y]) with no independence "
            "required — the workhorse identity of interview probability.\n"
            "- **variance** — Expected squared deviation from the mean; adds across variables only when they're "
            "independent.\n"
            "- **conditioning** — E[X|Y]: slicing expectation by what you know; 'condition on what you know, "
            "average over what you don't.'\n"
            "- **central limit theorem (CLT)** — Averages of many independent samples become approximately normal "
            "regardless of the underlying distribution — why normal-based confidence intervals work on real data; "
            "'independent' and 'enough samples' do the heavy lifting.\n"
            "- **confidence interval** — A procedure with long-run coverage: ~95% of such intervals from repeated "
            "samples contain the true parameter — not '95% chance the truth is in this one.'\n"
            "- **p-value** — The probability of seeing data this extreme if the null were true; NOT the "
            "probability the null is true, and not the size of the effect — 'p-values measure surprise under the "
            "null, nothing more.'\n"
            "- **hypothesis test** — A decision procedure with controlled error rates: reject the null when the "
            "p-value crosses the pre-chosen significance level.\n"
            "- **Bayes' rule** — P(A|B) = P(B|A)P(A)/P(B): updating beliefs with evidence; the tool for base-rate "
            "problems like the '99%-accurate test' trap.\n"
            "- **base rate** — The prevalence of the condition in the population; ignoring it makes even accurate "
            "tests produce mostly false positives for rare conditions."
        ),
        "procedure_intro": (
            "The stats drill: definitions with intuition, then the caveat, then a number. Every concept gets a "
            "tiny worked example — interviewers trust candidates who can compute, not just recite."
        ),
        "procedure_steps": [
            "State the definition precisely, in one sentence, before any intuition.",
            "Give the intuition: what the concept measures in plain language.",
            "Name the caveat unprompted: independence for the CLT, 'under the null' for p-values, the base rate for Bayes.",
            "Work a tiny numeric example (a 2x2 table, ten coin flips) — compute it, don't gesture at it.",
            "Connect to the interview use: which DS question this concept answers (sizing a test, reading a result, catching a fallacy).",
            "Red-team your own statement: what would make it false? Say it before the interviewer does.",
        ],
        "project_brief": (
            "Build a statistics reference notebook: one worked example per concept in this module — distributions "
            "matched to data-generating processes, a CLT simulation showing convergence, confidence intervals with "
            "correct interpretation, a hypothesis test with the p-value explained, and the base-rate disease-test "
            "worked via Bayes' rule. Every example ends with the one-sentence interview version and the caveat. "
            "The notebook must run top-to-bottom with no hidden state. This is the artifact you review the night "
            "before a stats round."
        ),
        "honesty": (
            "Preparation, not a credential: this module confers no certificate and makes no placement claims. "
            "Statistical fluency is built on precise definitions — the ones here are standard, but this module is "
            "interview preparation, not a statistics course; deeper study belongs in a full curriculum. Timed "
            "drills measure current fluency, not your worth as a scientist."
        ),
        "new_card": {
            "front": "What's the interview line for the base-rate trap?",
            "back": "'A 99%-accurate test for a 0.1%-prevalent disease still yields mostly false positives — Bayes' rule says the base rate dominates.' The interview line: 'I never interpret a test result without the prevalence.'",
        },
        "explain_pointer": "Covered in this module's 'Concepts' note.",
        "new_quiz": [
            {
                "q": "Which distribution models the number of website errors per hour?",
                "choices": ["Normal", "Binomial", "Poisson — events over time at a constant rate", "Uniform"],
                "answer": 2,
                "explain": "Match the distribution to the data-generating process: rates over time mean Poisson. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "E[3X + 2] equals:",
                "choices": ["3E[X]", "3E[X] + 2 — linearity of expectation needs no independence", "E[X] + 5", "3E[X] + 4"],
                "answer": 1,
                "explain": "Expectation is linear: constants pull out, shifts add. Independence is irrelevant here. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "Var(X + Y) = Var(X) + Var(Y) requires:",
                "choices": [
                    "Normality",
                    "Independence of X and Y — otherwise the covariance term stays",
                    "Large samples",
                    "Zero means",
                ],
                "answer": 1,
                "explain": "Variance adds only for independent variables; dependence contributes 2Cov(X,Y). See the 'Concepts' glossary in this module.",
            },
            {
                "q": "A p-value of 0.03 does NOT tell you:",
                "choices": [
                    "How surprising the data is under the null",
                    "The probability the null hypothesis is true",
                    "Whether to reject at the 5% level",
                    "The test's significance outcome",
                ],
                "answer": 1,
                "explain": "It's P(data|null), not P(null|data) — the most-tested misreading in DS interviews. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "The CLT lets you use normal-based intervals on sample means when:",
                "choices": [
                    "The data is normal",
                    "Samples are independent and numerous enough — the underlying distribution can be anything",
                    "n > 5 always",
                    "The variance is known",
                ],
                "answer": 1,
                "explain": "'Independent' and 'enough samples' are doing the heavy lifting. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "Wider confidence interval means:",
                "choices": [
                    "More precision",
                    "More uncertainty about the parameter — less information in the sample",
                    "A larger effect",
                    "A smaller p-value",
                ],
                "answer": 1,
                "explain": "Width reflects uncertainty; precision comes from more data, not wider bands. See the 'Concepts' glossary in this module.",
            },
        ],
    },
    "data-science-interview-prep--pandas-analysis": {
        "summary": (
            "Welcome to the Data Science Interview Prep track of the IL-15 Data Engineering & Analytics "
            "Interview Prep course. I'm your instructor for this track, and in this module we're going to turn "
            "analysis into a live-coding skill: from a raw table to an insight with pandas — exploratory analysis, "
            "groupby patterns, merge safety, and the vectorized feature construction interviewers watch for."
        ),
        "concepts": (
            "- **EDA (exploratory data analysis)** — Distributions first, then relationships, then data quality; "
            "narrated as you go, because live analysis is a thinking test wearing a coding costume.\n"
            "- **split-apply-combine** — The groupby grammar: aggregations (one row per group), transforms "
            "(broadcast group stats back to rows), filters (keep groups meeting a condition).\n"
            "- **merge validation** — Asserting expected key cardinality (validate='m:1') so fan-out fails loudly "
            "instead of silently multiplying rows.\n"
            "- **fan-out** — Many-to-many merge row multiplication; the silent aggregate corruptor — check key "
            "uniqueness on both sides first.\n"
            "- **missingness mechanism** — MCAR (missing completely at random), MAR, MNAR: the diagnosis that "
            "decides drop vs impute vs flag.\n"
            "- **imputation** — Filling missing values (median, model-based); mean imputation shrinks variance and "
            "understates uncertainty — a choice with consequences, not a default.\n"
            "- **leakage** — Test-set information contaminating training (features fit before the split); makes "
            "evaluation fiction — 'fit on train only.'\n"
            "- **vectorized feature construction** — Building features with whole-column ops (ratios, rolling "
            "aggregates, encodings) expressing domain knowledge; 'features are where domain knowledge becomes "
            "model power.'\n"
            "- **reproducible notebook** — Restart-and-run-all clean: no hidden out-of-order state, the narrative "
            "is real top-to-bottom.\n"
            "- **outlier** — An extreme value: investigate before deleting — it may be the signal (fraud) or the "
            "noise (sensor glitch); the treatment depends on the cause."
        ),
        "procedure_intro": (
            "The live-analysis drill: every exercise is a raw table and a question, timed at 20 minutes, narrated "
            "end to end. The interviewer scores your investigative method — what you check and in what order — so "
            "the order is the skill."
        ),
        "procedure_steps": [
            "State the question and the grain before touching the data; write the plan (distributions, relationships, quality) in a markdown cell.",
            "Profile: shape, dtypes, missingness, duplicates, basic distributions. Say what surprises you out loud.",
            "Check data quality first: row counts vs expectations, impossible values, join-key uniqueness — garbage in, garbage out.",
            "Explore distributions per key variable, then relationships (groupby cuts, correlations) — narrate what each plot is testing.",
            "Build features vectorized: ratios, time-since-event, rolling aggregates — and fit every learning transform on train only to avoid leakage.",
            "Merge only with validated cardinality; assert row counts before and after every join.",
            "Finish with restart-and-run-all: the notebook must reproduce top-to-bottom with no hidden state.",
        ],
        "procedure_code": (
            "import pandas as pd\n"
            "\n"
            "# EDA skeleton: profile, then relationships, then quality\n"
            "df.info(); print(df.isna().sum()); print(df.duplicated().sum())\n"
            "\n"
            "# groupby patterns: aggregate, transform, filter\n"
            "rev_by_seg = df.groupby('segment')['revenue'].sum()                    # aggregate\n"
            "df['seg_mean'] = df.groupby('segment')['revenue'].transform('mean')    # transform\n"
            "big = df.groupby('customer_id').filter(lambda g: g['revenue'].sum() > 1000)\n"
            "\n"
            "# defensive merge: assert cardinality, check counts\n"
            "before = len(df)\n"
            "df = df.merge(dims, on='customer_id', validate='m:1')\n"
            "assert len(df) == before, 'fan-out detected'"
        ),
        "procedure_lang": "python",
        "project_brief": (
            "Deliver an end-to-end analysis notebook on a real tabular dataset: question stated up front, "
            "analysis plan in markdown, profiled data quality with explicit cleaning decisions (drop/impute/flag "
            "per column with reasons), groupby-driven exploration, validated merges, vectorized features built "
            "without leakage, and a findings section with one chart per insight plus the recommendation. The "
            "notebook restarts and runs clean top-to-bottom. Record a 10-minute narrated walkthrough — the "
            "artifact that answers 'walk me through an analysis.'"
        ),
        "honesty": (
            "Preparation, not a credential: this module confers no certificate and makes no placement claims. "
            "Live analysis screens reward method and narration; this module drills both, but real datasets and "
            "interviewers vary. Library APIs evolve — verify signatures in the current docs before production use."
        ),
        "new_card": {
            "front": "What's the interview line for merge safety?",
            "back": "'I assert cardinality before I trust a merge': check key uniqueness on both sides, merge with validate=, assert row counts before and after. Silent fan-out is the classic way a correct-looking analysis goes wrong.",
        },
        "explain_pointer": "Covered in this module's 'Concepts' note.",
        "new_quiz": [
            {
                "q": "groupby.transform differs from groupby.agg in that it:",
                "choices": [
                    "Is faster",
                    "Returns a result aligned to the original rows instead of one row per group",
                    "Only works on numerics",
                    "Sorts the output",
                ],
                "answer": 1,
                "explain": "transform broadcasts group statistics back to row shape — 'each employee with their department average.' See the 'Concepts' glossary in this module.",
            },
            {
                "q": "Fitting a scaler on the full dataset before train/test split causes:",
                "choices": [
                    "Slower training",
                    "Leakage — test statistics contaminate the training features",
                    "Memory errors",
                    "Nothing measurable",
                ],
                "answer": 1,
                "explain": "Any transform that learns from data must be fit on train only, or evaluation is fiction. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "An outlier should be deleted when:",
                "choices": [
                    "Always — outliers are noise",
                    "After investigating its cause and deciding it represents error rather than signal",
                    "Never",
                    "When it's inconvenient",
                ],
                "answer": 1,
                "explain": "The treatment depends on the cause: fraud signal vs sensor glitch demand opposite actions. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "Row counts changing unexpectedly after a merge signals:",
                "choices": ["Success", "Fan-out or key mismatch — stop and diagnose before proceeding", "Faster joins", "Clean data"],
                "answer": 1,
                "explain": "Count assertions before/after every join turn silent corruption into a loud stop. See the 'Hands-on procedure' in this module.",
            },
            {
                "q": "Median imputation is generally safer than mean imputation because:",
                "choices": [
                    "It's faster",
                    "It's robust to skew and outliers — though it still understates uncertainty and must be recorded",
                    "It's always unbiased",
                    "It needs no code",
                ],
                "answer": 1,
                "explain": "Every imputation is a choice with consequences; the mechanism diagnosis picks it. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "Narrating EDA as you go is graded because:",
                "choices": [
                    "Silence is awkward",
                    "The interviewer scores investigative method — what you check and in what order",
                    "Plots need captions",
                    "It's polite",
                ],
                "answer": 1,
                "explain": "Live analysis is a thinking test wearing a coding costume. See the 'Hands-on procedure' in this module.",
            },
        ],
    },
    "data-science-interview-prep--ml-for-ds": {
        "summary": (
            "Welcome to the Data Science Interview Prep track of the IL-15 Data Engineering & Analytics "
            "Interview Prep course. I'm your instructor for this track, and in this module we're going to build "
            "the modeling vocabulary DS interviews assume: which model for which problem, how you validate it, "
            "and which metric matches the cost of being wrong."
        ),
        "concepts": (
            "- **regression** — Predicting a number (price, demand); evaluated with MSE/MAE and R² (with caveats "
            "— it never decreases with more features).\n"
            "- **classification** — Predicting a class; evaluated with precision/recall, ROC-AUC, and calibration "
            "when probabilities drive decisions.\n"
            "- **overfitting** — The model memorizes noise: training error falls while validation error rises; "
            "fought with more data, regularization, simpler models, and honest validation.\n"
            "- **regularization (L1/L2)** — Penalties on weights: L1 (lasso) drives weights to exactly zero "
            "(feature selection); L2 (ridge) shrinks smoothly (handles correlated features).\n"
            "- **train/validation/test** — Fit on train, select models and hyperparameters on validation, estimate "
            "once on test; tuning on test turns it into validation with extra steps.\n"
            "- **cross-validation** — Rotating validation folds for a stabler performance estimate on small data; "
            "still never touches the test set.\n"
            "- **precision** — Of flagged items, how many were right; the metric when false positives hurt (spam "
            "filters).\n"
            "- **recall** — Of real items, how many were caught; the metric when false negatives hurt (fraud, "
            "disease screening).\n"
            "- **ROC-AUC** — The probability a random positive outranks a random negative, across thresholds; "
            "PR curves are more informative for imbalanced data.\n"
            "- **ablation** — Removing a feature or component and measuring the drop; credit assignment that "
            "proves a feature earns its keep.\n"
            "- **feature engineering judgment** — Knowing which transforms encode real signal vs noise-fitting, "
            "validated by ablations, watched for leakage: 'a feature is a hypothesis — I test it like one.'"
        ),
        "procedure_intro": (
            "The modeling drill: every exercise starts from the decision the prediction serves, not from the "
            "algorithm. Frame first, baseline second, validate honestly — and explain the model choice aloud as if "
            "a stakeholder asked 'why this one?'"
        ),
        "procedure_steps": [
            "Frame the problem: what is predicted, for whom, at what moment, and what does an error cost? The metric follows the cost.",
            "Establish the baseline: a simple model (or heuristic) whose performance every fancier model must beat to justify its complexity.",
            "Split with discipline: train for fitting, validation for selection, test touched once at the end. Say the split strategy aloud.",
            "Choose the metric from the error costs: precision where false positives hurt, recall where misses hurt, ROC-AUC/PR for ranking quality.",
            "Validate honestly: cross-validation where data is small, learning curves to diagnose bias vs variance, ablations to credit features.",
            "Explain the choice aloud: decision → alternatives considered → why this one → what would change your mind.",
        ],
        "project_brief": (
            "Build a model-selection case study on a classification dataset: frame the business decision, derive "
            "the metric from error costs, establish a baseline, compare three model families with cross-validated "
            "evaluation, run ablations on your engineered features, and document the final choice with the "
            "alternatives-rejected reasoning. Deliver the notebook plus a one-page memo: the recommendation, the "
            "evidence, the risks. The memo is the interview artifact."
        ),
        "honesty": (
            "Preparation, not a credential: this module confers no certificate and makes no placement claims. "
            "Model selection here is interview-scale; production modeling adds data pipelines, monitoring, and "
            "stakeholder constraints this module doesn't simulate. Metrics are taught as decision tools, not as "
            "leaderboard targets."
        ),
        "new_card": {
            "front": "What's the interview line for metric choice?",
            "back": "'I start from the decision the prediction serves, then pick the framing': the metric is the business objective, mathematized. Precision when false positives hurt, recall when misses hurt — never the metric I used last time out of habit.",
        },
        "explain_pointer": "Covered in this module's 'Concepts' note.",
        "new_quiz": [
            {
                "q": "R² always (weakly) increases when you add features, so it:",
                "choices": [
                    "Proves the bigger model is better",
                    "Can't be trusted for model comparison — use adjusted R² or validation metrics",
                    "Measures causality",
                    "Is deprecated",
                ],
                "answer": 1,
                "explain": "In-sample fit rewards complexity; honest comparison needs held-out evaluation. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "A spam filter should optimize primarily for:",
                "choices": [
                    "Recall",
                    "Precision — false positives (legit mail flagged) hurt most",
                    "Accuracy",
                    "ROC-AUC only",
                ],
                "answer": 1,
                "explain": "Cost asymmetry decides: when false alarms are expensive, optimize precision. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "Learning curves show high bias (underfitting) when:",
                "choices": [
                    "Validation error keeps falling",
                    "Both training and validation error plateau at a high level — more data won't fix it",
                    "Training error is zero",
                    "The curves cross",
                ],
                "answer": 1,
                "explain": "Converged-but-bad means the model class can't capture the pattern: add capacity or features. See the 'Hands-on procedure' in this module.",
            },
            {
                "q": "Cross-validation's main advantage over a single validation split is:",
                "choices": [
                    "Speed",
                    "A stabler performance estimate — less dependence on one lucky/unlucky split",
                    "No need for a test set",
                    "Guaranteed better models",
                ],
                "answer": 1,
                "explain": "Averaging over folds reduces split variance, especially on small data. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "L1 regularization performs feature selection because:",
                "choices": [
                    "It's faster",
                    "The |w| penalty drives some weights to exactly zero, unlike L2's smooth shrinkage",
                    "It needs less data",
                    "It's newer",
                ],
                "answer": 1,
                "explain": "'L1 selects, L2 shrinks': the geometry of the penalty decides. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "An ablation that removes a feature group with no performance drop tells you:",
                "choices": [
                    "The model is broken",
                    "The group earns no keep — drop it for simplicity, or it rides on correlated companions",
                    "Ablations are useless",
                    "Add more features",
                ],
                "answer": 1,
                "explain": "Credit assignment: features must prove their contribution. See the 'Concepts' glossary in this module.",
            },
        ],
    },
    "data-science-interview-prep--experimentation-ab": {
        "summary": (
            "Welcome to the Data Science Interview Prep track of the IL-15 Data Engineering & Analytics "
            "Interview Prep course. I'm your instructor for this track, and in this module we're going to master "
            "the most-tested DS topic at product companies: experimentation. Design the test, size it, read it "
            "honestly — and name every way it can lie to you."
        ),
        "concepts": (
            "- **randomization** — Random assignment to treatment/control; balances confounders known and unknown, "
            "making outcome differences attributable to the treatment — 'the whole game.'\n"
            "- **treatment / control** — The changed experience vs the baseline; the comparison that isolates the "
            "causal effect.\n"
            "- **power** — The probability of detecting a real effect of a given size; the complement of the "
            "Type II error rate.\n"
            "- **minimum detectable effect (MDE)** — The smallest lift worth detecting; smaller MDEs need larger "
            "samples — sizing starts here.\n"
            "- **sample size** — Determined by power, significance level, baseline variance, and MDE before the "
            "test starts; 'decide the stopping rule before the test starts.'\n"
            "- **primary metric** — The one pre-registered success measure; read via its confidence interval, not "
            "just the point estimate.\n"
            "- **guardrail metrics** — Secondary metrics that must not regress; they catch wins that break "
            "something else.\n"
            "- **peeking** — Checking results mid-test and stopping on significance; each look compounds the "
            "false-positive rate — a sin without sequential methods.\n"
            "- **multiple testing** — Testing many metrics/variants inflates false positives; corrections "
            "(Bonferroni and friends) or pre-registered primaries control it.\n"
            "- **HARKing** — Hypothesizing after results are known; pre-registration of the analysis plan is the "
            "defense.\n"
            "- **network effects / interference** — Users influencing each other breaks randomization's promise: "
            "treatment leaks into control.\n"
            "- **heterogeneous treatment effects** — The effect differs across segments; the average can hide that "
            "a change helps some users and harms others.\n"
            "- **quasi-experiment** — Causal inference without randomization (diff-in-diff, regression "
            "discontinuity); the fallback when A/B testing is impossible or unethical."
        ),
        "procedure_intro": (
            "The experiment-design drill: given a product change, produce the full design on a whiteboard in 20 "
            "minutes — randomization, metrics, sizing, reading plan, and the pre-mortem of everything that can go "
            "wrong. Interviewers grade the sins you name unprompted."
        ),
        "procedure_steps": [
            "State the hypothesis and the decision the test informs; name what would change your mind.",
            "Define the randomization unit (user, session, cluster) and check for interference — network effects kill user-level randomization.",
            "Choose the primary metric before anything else, plus guardrails; pre-register the analysis plan to block HARKing and metric shopping.",
            "Size the test: MDE from business relevance, then sample size and runtime from power analysis. Commit to the runtime — no peeking.",
            "Name the sins and their defenses: peeking (fixed horizon or sequential methods), multiple testing (corrections), novelty effects (run long enough).",
            "Plan the read: primary metric's confidence interval, guardrail check, segment heterogeneity, and the ship/hold/iterate decision rule.",
            "State when you would NOT A/B test: can't randomize cleanly, tiny samples, unethical, or the answer is obvious — and name the quasi-experimental alternative.",
        ],
        "project_brief": (
            "Design three experiments for a fictional subscription product: a checkout-flow change, a pricing "
            "test, and a recommendation-ranking change with likely network effects. For each, deliver: the "
            "hypothesis, randomization unit with interference analysis, primary metric and guardrails, MDE and "
            "sample-size reasoning, the pre-registered analysis plan, the sin pre-mortem, and the read/decision "
            "rule. Present one as a 20-minute whiteboard talk; the other two as one-page designs. The interviewer "
            "will attack the randomization — be ready."
        ),
        "honesty": (
            "Preparation, not a credential: this module confers no certificate and makes no placement claims. "
            "Experiment design here is interview-scale reasoning; real experimentation platforms add sequential "
            "testing, variance reduction, and infrastructure this module doesn't simulate. Power-analysis "
            "arithmetic is taught conceptually — use proper tooling for real sizing."
        ),
        "new_card": {
            "front": "What's the interview line for peeking?",
            "back": "'Decide the stopping rule before the test starts': every interim look is another roll of the dice, and significance under repeated testing isn't 5% anymore. Pre-commit to runtime from the power analysis, or use sequential methods designed for interim looks.",
        },
        "explain_pointer": "Covered in this module's 'Concepts' note.",
        "new_quiz": [
            {
                "q": "Randomizing by user fails when the feature has strong network effects because:",
                "choices": [
                    "Users are slow",
                    "Treatment leaks into control — a treated user's behavior changes their control friends' outcomes",
                    "Metrics break",
                    "Samples shrink",
                ],
                "answer": 1,
                "explain": "Interference violates the independence randomization assumes; consider cluster randomization. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "The MDE should be chosen based on:",
                "choices": [
                    "What the sample size allows",
                    "Business relevance — the smallest lift worth acting on",
                    "Convention (always 5%)",
                    "The baseline metric",
                ],
                "answer": 1,
                "explain": "Sizing follows the decision: detect what matters, not what's convenient. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "A novelty effect threatens experiment validity because:",
                "choices": [
                    "Users hate change",
                    "Early lifts from curiosity fade — the measured effect isn't the steady-state effect",
                    "Metrics are wrong",
                    "Randomization breaks",
                ],
                "answer": 1,
                "explain": "Run long enough for novelty to decay, or the ship decision rests on a mirage. See the 'Hands-on procedure' in this module.",
            },
            {
                "q": "Testing 20 metrics at 5% significance without correction means:",
                "choices": [
                    "Nothing changes",
                    "You expect about one false positive by chance alone — multiple testing inflates the error rate",
                    "More power",
                    "Faster decisions",
                ],
                "answer": 1,
                "explain": "Each test is another roll; pre-register one primary or correct for multiplicity. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "Heterogeneous treatment effects matter because:",
                "choices": [
                    "Averages are wrong",
                    "A positive average can hide harm to a segment — the ship decision needs the segment view",
                    "Segments are trendy",
                    "Power increases",
                ],
                "answer": 1,
                "explain": "Report the average and the segments; 'it works on average' can still be a bad ship. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "Diff-in-diff is appropriate when:",
                "choices": [
                    "You have huge samples",
                    "You can't randomize (e.g. a launched feature) but have a comparable control group and pre-period data",
                    "A/B tests are too slow",
                    "Metrics are missing",
                ],
                "answer": 1,
                "explain": "Quasi-experiments trade randomization's clean identification for feasibility — with stronger assumptions. See the 'Concepts' glossary in this module.",
            },
        ],
    },
    "data-science-interview-prep--ds-case-rep": {
        "summary": (
            "Welcome to the Data Science Interview Prep track of the IL-15 Data Engineering & Analytics "
            "Interview Prep course. I'm your instructor for this track, and in this module we're going to walk a "
            "full case study end to end — ambiguous prompt, metric choice, analysis plan, findings, and the story — "
            "because the case round is where product DS interviews are won or lost."
        ),
        "concepts": (
            "- **case framing** — Restating an ambiguous business question as a measurable one: 'metrics first, "
            "data second — otherwise the data picks the question for you.'\n"
            "- **analysis plan** — Question, metrics, data sources, methods, caveats — written before touching "
            "data; 'the plan prevents fishing.'\n"
            "- **sanity checks** — Row counts, distributions, known totals run first, every time; 'the checks "
            "prevent embarrassment.'\n"
            "- **narrative arc** — Question → approach → key findings (one chart each) → recommendation; the shape "
            "every case presentation follows.\n"
            "- **one-page summary** — Decision, evidence, risks — nothing else; the artifact executives actually read.\n"
            "- **follow-up anticipation** — Naming the biggest objection to your conclusion and addressing it "
            "proactively; credibility before they ask.\n"
            "- **caveats** — The honest limits of the analysis (data gaps, assumptions, alternative explanations); "
            "stated briefly, never buried.\n"
            "- **recommendation** — The decision the analysis supports, with expected impact; data without one is "
            "trivia."
        ),
        "procedure_intro": (
            "The case drill: 45 minutes from ambiguous prompt to one-page summary, narrated throughout. The "
            "discipline is sequence — frame, plan, check, analyze, narrate — never analysis before framing."
        ),
        "procedure_steps": [
            "Restate the ambiguous prompt as a measurable question; confirm the decision it informs before proceeding.",
            "Choose metrics before touching data: primary, guardrails, and what would change your mind.",
            "Write the analysis plan: question, metrics, data sources, methods, caveats — one paragraph each.",
            "Run sanity checks first: row counts, distributions, known totals. Fix or flag data issues before any analysis.",
            "Analyze in the planned order; when the data surprises you, update the plan explicitly — no silent fishing.",
            "Build the narrative arc: one chart per key finding, each earning its place toward the recommendation.",
            "Anticipate the biggest follow-up and address it proactively; write the one-page summary: decision, evidence, risks.",
        ],
        "project_brief": (
            "Complete a full guided case: 'A subscription product's activation rate dropped 12% over six weeks — "
            "diagnose it and recommend action.' Deliver: the framed question, metric choices with reasoning, the "
            "written analysis plan, sanity-check results, the analysis with one chart per finding, the addressed "
            "objections, and the one-page summary (decision, evidence, risks). Present it as a 20-minute stakeholder "
            "walkthrough. The grading lens: did metrics precede data, and does the story survive its own caveats?"
        ),
        "honesty": (
            "Preparation, not a credential: this module confers no certificate and makes no placement claims. "
            "Case reps build the framing-and-narrative muscle, but real cases come with messier data, politics, "
            "and stakeholders this module can't simulate. The one-page summary format is a communication tool, not "
            "a substitute for analytical depth."
        ),
        "new_card": {
            "front": "What's the interview line for case framing?",
            "back": "'Metrics first, data second — otherwise the data picks the question for you.' Restate the ambiguous prompt as a measurable question, choose what would change your mind, then touch the data. The plan prevents fishing; the sanity checks prevent embarrassment.",
        },
        "explain_pointer": "Covered in this module's 'Concepts' note.",
        "new_quiz": [
            {
                "q": "The analysis plan is written before touching data to:",
                "choices": [
                    "Save time",
                    "Prevent fishing — deciding the question and metrics before results can bias them",
                    "Impress stakeholders",
                    "Satisfy process",
                ],
                "answer": 1,
                "explain": "Pre-commitment keeps the analysis honest when the data disappoints. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "A case narrative puts the recommendation:",
                "choices": [
                    "At the very end as a surprise",
                    "Up front (BLUF), then the evidence that earns it",
                    "In the appendix",
                    "Nowhere — let them decide",
                ],
                "answer": 1,
                "explain": "Bottom line up front: busy stakeholders need the ask before the analysis. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "Sanity checks catch:",
                "choices": [
                    "Insights",
                    "Broken data — wrong counts, impossible values — before they become confidently-wrong conclusions",
                    "Slow queries",
                    "Typos",
                ],
                "answer": 1,
                "explain": "An analysis on broken data is worse than none: it's confidently wrong. See the 'Hands-on procedure' in this module.",
            },
            {
                "q": "Addressing the biggest objection proactively works because:",
                "choices": [
                    "It disarms hostility",
                    "It shows the conclusion survived your own skepticism — credibility before they ask",
                    "It's defensive",
                    "Stakeholders are hostile",
                ],
                "answer": 1,
                "explain": "Pre-empting the obvious challenge proves stress-testing, not defensiveness. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "Caveats belong in the presentation:",
                "choices": [
                    "Nowhere — they weaken the case",
                    "Briefly and honestly — buried caveats destroy trust when discovered",
                    "Only if asked",
                    "In a separate meeting",
                ],
                "answer": 1,
                "explain": "Honest limits build credibility; discovered omissions destroy it. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "One chart per key finding (not ten charts per finding) because:",
                "choices": [
                    "Charts are expensive",
                    "Each visual must earn its place in the arc toward the recommendation",
                    "Stakeholders dislike charts",
                    "It's faster",
                ],
                "answer": 1,
                "explain": "Narrative discipline: the arc is question → findings → recommendation, with no decoration. See the 'Hands-on procedure' in this module.",
            },
        ],
    },
    "data-science-interview-prep--ds-mock": {
        "summary": (
            "Welcome to the Data Science Interview Prep track of the IL-15 Data Engineering & Analytics "
            "Interview Prep course. I'm your instructor for this track, and in this final track module we're going "
            "to run full DS-loop simulations — timed stats rounds, live analysis screens, experiment-design "
            "whiteboards, model-choice deep dives — scored against rubrics, because each round has a shape and "
            "you rehearse the shape."
        ),
        "concepts": (
            "- **mock circuit (DS)** — Timed simulations across the four DS round types: stats, coding/analysis, "
            "experimentation, case — each with its own shape and rubric.\n"
            "- **stats round shape** — Definitions with intuition, then the caveat, then a tiny computation; "
            "precision under time.\n"
            "- **live analysis shape** — Narrated EDA: distributions, then relationships, then quality; the "
            "interviewer scores investigative method.\n"
            "- **experiment-design shape** — The full checklist aloud: randomization, metrics, sizing, sins, read "
            "plan; sins named unprompted score highest.\n"
            "- **model-choice shape** — Decision with alternatives: framing, baseline, metric from costs, honest "
            "validation.\n"
            "- **failed-analysis story** — The behavioral artifact: own the miss early, name the cost, show the "
            "concrete process change with evidence it stuck — 'the failure is the setup; the changed practice is "
            "the point.'\n"
            "- **scored review** — Rubric scoring per round immediately after: correctness, complexity stated, "
            "communication, time.\n"
            "- **redrill plan** — Each miss converted to a specific, dated task; 'three power-analysis problems by "
            "Thursday' — not 'practice more.'"
        ),
        "procedure_intro": (
            "The DS mock protocol: one full loop per session, real timing, narration mandatory. Rotate the weak "
            "round to the front — you train the miss, not the strength."
        ),
        "procedure_steps": [
            "Assemble the loop: 15-min stats round, 20-min live analysis screen, 20-min experiment whiteboard, 15-min model-choice deep dive, 10-min failed-analysis story.",
            "Run stats with the shape: definition, intuition, caveat, tiny computation — say the caveat before they ask.",
            "Run live analysis narrated: distributions, relationships, quality checks — in that order, out loud.",
            "Run experiment design with the full checklist aloud; name the sins (peeking, interference, novelty) unprompted.",
            "Run model choice as decision-with-alternatives: framing, baseline, metric from error costs, validation discipline.",
            "Tell the failed-analysis story: own the miss early, the cost, the process change, the evidence it stuck.",
            "Score every round against the rubric immediately; convert each miss to a dated redrill task before the next loop.",
        ],
        "project_brief": (
            "Run and document three full DS mock loops over two weeks. Per loop, deliver: the prompts used for "
            "each of the five rounds, rubric scores with verbatim misses, the redrill plan with dates, and a "
            "trend summary of which miss categories shrink. Final deliverable: a readiness self-assessment naming "
            "your strongest round shape, your costliest remaining miss category, and the dated plan to close it."
        ),
        "honesty": (
            "Preparation, not a credential: this module confers no certificate and makes no placement claims. "
            "Mocks simulate the four round shapes; real loops vary by company and interviewer, and team fit is "
            "scored beyond any rubric. Scores measure performance on the day — aim redrills with them, don't "
            "predict outcomes with them."
        ),
        "new_card": {
            "front": "What are the four DS round shapes?",
            "back": "Stats (definition → intuition → caveat → computation), live analysis (narrated EDA in order), experiment design (full checklist aloud, sins unprompted), model choice (decision with alternatives). 'Each round has a shape — I rehearse the shape.'",
        },
        "explain_pointer": "Covered in this module's 'Concepts' note.",
        "new_quiz": [
            {
                "q": "In a stats round, stating the caveat unprompted is strong because:",
                "choices": [
                    "It fills time",
                    "It proves you know the concept's boundaries — interviewers probe exactly there",
                    "It's humble",
                    "Definitions are boring",
                ],
                "answer": 1,
                "explain": "The caveat is where understanding shows; recitation without it is fragile. See the 'Hands-on procedure' in this module.",
            },
            {
                "q": "Rotating your weakest round to the front of each mock loop:",
                "choices": [
                    "Builds confidence",
                    "Trains the miss while you're fresh — strengths maintain themselves",
                    "Is traditional",
                    "Saves time",
                ],
                "answer": 1,
                "explain": "Deliberate practice targets the gap, not the comfort zone. See the 'Hands-on procedure' in this module.",
            },
            {
                "q": "Owning the miss early in the failed-analysis story works because:",
                "choices": [
                    "It's brave",
                    "Credibility first makes the lesson believable — buried failures read as evasion",
                    "It's quick",
                    "Interviewers forget",
                ],
                "answer": 1,
                "explain": "The story's value is the learning; evasion destroys the value. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "A redrill task like 'practice stats' fails because:",
                "choices": [
                    "Stats are hard",
                    "It's vague — effective redrills are specific, dated, and tied to named misses",
                    "It's too easy",
                    "It's boring",
                ],
                "answer": 1,
                "explain": "Specificity turns review into training; vague plans evaporate. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "In the experiment-design round, the highest-scoring move is:",
                "choices": [
                    "Computing power by hand",
                    "Naming the sins (peeking, interference, novelty) and their defenses unprompted",
                    "Choosing trendy metrics",
                    "Finishing early",
                ],
                "answer": 1,
                "explain": "Interviewers grade whether you see the traps before they point at them. See the 'Hands-on procedure' in this module.",
            },
            {
                "q": "Scoring immediately after each round (not at day's end) matters because:",
                "choices": [
                    "Memory fades",
                    "Fresh misses are verbatim and specific — delayed review smooths them into vagueness",
                    "It's faster",
                    "Rubrics require it",
                ],
                "answer": 1,
                "explain": "Specific misses become specific redrills; vague ones evaporate. See the 'Hands-on procedure' in this module.",
            },
        ],
    },
}

if __name__ == "__main__":
    apply_all(load(), CONTENT)

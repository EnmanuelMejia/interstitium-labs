# IL-16 expansion content
NEWCARDS = {
"ml-in-practice--ml-workflow": [
("What belongs in an iteration log?",
 "Each experiment's hypothesis, data/code version, hyperparameters, validation score, and what you learned — one row per idea, including the failures. The log turns tuning from wandering into evidence. The line: 'If it isn't in the log, the experiment didn't happen.'"),
("How do you pick the first metric?",
 "Choose the metric that matches the decision: the business cost of each error type decides between precision, recall, RMSE, or ranking measures. Start with the simplest defensible one and state its blind spots. The line: 'The metric is the first modeling decision — everything else optimizes it.'"),
],
"ml-in-practice--feature-engineering-practice": [
("When do you bin or bucketize a continuous feature?",
 "When the relationship is nonlinear and trees or linear models would struggle — age bands, price tiers — or when you need robustness to outliers and drift. The cost is lost granularity, so compare binned vs raw on validation. The line: 'Binning trades resolution for robustness; I let validation price the trade.'"),
("How do you discuss feature importance versus feature selection?",
 "Importance ranks what the model uses; selection decides what to keep. Use importance plus ablation (remove and re-measure) to select, and watch for correlated features splitting credit. The line: 'Importance is a hint, ablation is the verdict.'"),
],
"ml-in-practice--model-evaluation-practice": [
("Why prefer PR curves over ROC on imbalanced data?",
 "ROC can look excellent while precision is terrible, because true negatives dominate the false-positive rate denominator. Precision-recall keeps the focus on the rare class you actually care about. The line: 'On skewed data, ROC flatters; precision-recall tells the truth.'"),
("What does a learning curve tell you?",
 "Plot training and validation score versus data size: converging lines mean more data won't help; a wide gap means variance (get data, regularize); both low means bias (bigger model, better features). The line: 'The learning curve diagnoses whether to feed the model data or change the model.'"),
],
"ml-in-practice--ml-pipelines-practice": [
("Why version datasets alongside code?",
 "A model is a function of data and code — rerunning old code on new data is not reproduction. Version the data snapshot (hash, query, or artifact) with the code commit so every experiment is replayable. The line: 'Code without its data version is a recipe without ingredients.'"),
("What does a pipeline contract look like?",
 "The agreed schema, types, ranges, and freshness of each pipeline stage's output — checked at every handoff. Contracts turn silent data drift into loud failures. The line: 'Contracts make data problems arrive as errors, not as wrong predictions.'"),
],
"ml-in-practice--ml-deployment-practice": [
("What is a canary deployment for models?",
 "Route a small slice of live traffic to the new model and compare its predictions and business metrics against the incumbent before full rollout. Canaries catch serving bugs and metric regressions with limited blast radius. The line: 'Canary the model: let 5% of traffic prove it before 100% trusts it.'"),
("How do you monitor data drift in production?",
 "Track input feature distributions against the training baseline — PSI, KS tests, or simple percentile bands — and alert when they move. Drift means the world changed; the model's assumptions may be stale. The line: 'Drift monitoring watches the world, not the model — the model just inherits the world's changes.'"),
],
"ml-in-practice--ml-practice-capstone": [
("How do you choose a capstone dataset?",
 "Real, messy, and scoped: public enough to share, dirty enough to need wrangling, small enough to finish in the time you have. A well-known dataset with an underexplored question beats a novel dataset you can't clean. The line: 'Pick a dataset you can finish, then find the question it almost answers.'"),
("What does 'reproducible' mean for a capstone?",
 "A stranger can rerun everything: pinned dependencies, fixed seeds, scripts that run top to bottom, and data with a documented source. Notebooks must re-execute cleanly. The line: 'Reproducible means the README is a recipe, not a memoir.'"),
],
"advanced-ml--ensemble-methods-practice": [
("What is out-of-bag error?",
 "In bagging, each tree trains on a bootstrap sample — the samples left out are 'out-of-bag' and serve as a free validation set for that tree. Aggregating OOB predictions estimates test error without a separate split. The line: 'OOB is validation you get for free from bootstrapping.'"),
("How do you tune gradient boosting without overfitting?",
 "Constrain the complexity first: shallow trees, low learning rate, subsampling, then early-stop on a validation set with a patience count. Tune in that order — early stopping is the honest guardrail. The line: 'Shrink, subsample, early-stop — then tune.'"),
],
"advanced-ml--probabilistic-ml": [
("What is the difference between aleatoric and epistemic uncertainty?",
 "Aleatoric uncertainty is noise in the data itself — irreducible no matter how much data you collect. Epistemic uncertainty is ignorance of the true model — shrinkable with more data. Know which you're facing before promising better predictions. The line: 'Aleatoric is the dice; epistemic is not knowing the dice — collect data only against the second.'"),
("How do you explain a posterior predictive distribution?",
 "Instead of one point prediction, integrate predictions over the posterior of the parameters — the result is a distribution that carries both data noise and parameter uncertainty. It answers 'what might we see?' not just 'what's most likely?' The line: 'Posterior predictive: the forecast plus an honest admission of how much we don't know.'"),
],
"advanced-ml--deep-architectures-practice": [
("What is the dead-neuron problem in ReLUs?",
 "A ReLU outputs zero for all negative inputs; if a neuron's weights push it permanently negative, its gradient is zero forever and it never recovers — it 'dies'. Leaky ReLU / ELU or careful initialization keep units alive. The line: 'Dead ReLUs are silent forever; leaky variants keep a whisper of gradient.'"),
("How do you read a loss curve?",
 "Smooth decline with train/val tracking is healthy; train falling while val rises is overfitting; both flat is underfitting or too-small a learning rate; spikes suggest unstable optimization. The line: 'The loss curve is the model's diary — train/val divergence is the headline.'"),
],
"advanced-ml--optimization-advanced": [
("What is learning-rate scheduling?",
 "Changing the learning rate during training — warmup then decay, cosine annealing, or step drops — to take big steps early and fine steps late. Schedules let you start aggressive and finish precise. The line: 'Schedule the learning rate like a landing: fast approach, gentle touchdown.'"),
("Why do you normalize inputs before optimizing?",
 "Features on wildly different scales stretch the loss landscape into a narrow valley — gradient descent zigzags and converges slowly. Standardizing inputs makes the landscape round and the optimizer's steps efficient. The line: 'Normalize inputs and the optimizer walks downhill; skip it and it zigzags across a canyon.'"),
],
"advanced-ml--model-interpretation-practice": [
("What do local explanations add over global ones?",
 "Global importance says which features matter overall; local explanations (LIME, SHAP per-instance) say why this specific prediction happened. Audits, appeals, and debugging need the local story. The line: 'Global tells you the model's habits; local tells you its reasoning for this case.'"),
("How do you detect a model relying on a spurious feature?",
 "Ablate it: remove or shuffle the suspect feature and watch performance; check slices where the spurious correlation breaks; inspect explanations for the feature dominating where it shouldn't. The line: 'Spurious features fail the ablation test — performance that vanishes with one feature was never real.'"),
],
"advanced-ml--advanced-ml-project": [
("How do you budget compute for the project?",
 "Estimate before you spend: time one training run, multiply by the experiments you plan, add a 2x buffer, and cap the tuning budget per idea. Kill expensive ideas early with cheap proxies. The line: 'Budget compute like money: estimate the run, price the sweep, cap the spend.'"),
("What makes an ablation honest?",
 "Change exactly one thing versus a fixed baseline, keep seeds and data identical, and report the delta with variance — not the best of five runs. An ablation isolates cause; a sloppy one just adds noise. The line: 'One variable, fixed everything else, reported with error bars — that's an ablation.'"),
],
"python-for-ml--numpy-pandas-practice": [
("What is the difference between a view and a copy?",
 "A view shares memory with the original array — modifying it changes the source; a copy is independent. pandas' SettingWithCopyWarning exists because chained indexing makes this ambiguous. The line: 'When in doubt, .copy() — explicit independence beats silent aliasing.'"),
("When do you use apply, and when do you avoid it?",
 "Use apply for genuinely row-wise logic that has no vectorized form; avoid it for anything NumPy or pandas can do natively — it's a Python loop in disguise and orders of magnitude slower. The line: 'apply is the escape hatch, not the front door — vectorize first.'"),
],
"python-for-ml--visualization-practice": [
("What is small multiples' strength?",
 "Faceting the same chart across categories (one panel per segment) makes comparisons the reader does effortlessly — trends across regions, cohorts, or time. It scales where overlaid lines become spaghetti. The line: 'Small multiples turn comparison into a glance.'"),
("How do you visualize missing data?",
 "Plot the missingness itself: a heatmap of nulls by column, or missingness rates grouped by a key variable. Patterns in what's missing are often the story — missing-not-at-random changes everything. The line: 'Missing data is data about your data collection — chart it.'"),
],
"python-for-ml--sklearn-api-practice": [
("What does cross_val_score actually do?",
 "It clones the estimator, trains and scores it on each fold of the split, and returns one score per fold — estimating how the model generalizes. It does not tune anything; tuning needs a search wrapper. The line: 'cross_val_score measures; GridSearchCV tunes.'"),
("How do you tune hyperparameters with GridSearchCV discipline?",
 "Wrap the full pipeline (preprocessing inside), search a coarse grid first, refine around the winner, and keep an untouched test set for the final number. Report the search space, not just the winner. The line: 'Pipeline in, coarse-to-fine grid, test set untouched — that's the discipline.'"),
],
"python-for-ml--python-ml-ecosystem": [
("What is a requirements file for?",
 "It pins every dependency to an exact version so the environment rebuilds identically — requirements.txt or a lock file. 'It works on my machine' is the failure a lock file prevents. The line: 'Pin it or lose it: the lock file is the environment's memory.'"),
("How do you structure an ML project directory?",
 "Separate concerns: data/ (never committed), notebooks/ (exploration, numbered), src/ (importable code), models/ (artifacts), configs/ (parameters), tests/. If someone can't find the training entry point in 30 seconds, restructure. The line: 'Notebooks explore, src/ ships — never confuse the two.'"),
],
"python-for-ml--working-with-real-data": [
("How do you handle inconsistent date formats?",
 "Never parse by guessing: sample the raw values, identify the formats present, parse with explicit format strings per pattern, and coerce failures to NaT with a logged count. Timezone-naive vs aware must be decided once, up front. The line: 'Dates get one canonical format — I declare it before parsing.'"),
("What goes in a data README?",
 "Source and pull date, schema with types, known quirks (encoding, missingness, duplicates), the grain of each table, and who to ask when it's wrong. Future-you will thank present-you. The line: 'The data README is the contract between you and the next person who touches the data.'"),
],
"python-for-ml--ml-python-project": [
("How do you present results without overselling?",
 "Report the metric with its baseline, the error bars, and the slices where it fails — then state plainly what you would not claim. Honest limits are a feature of the writeup, not a weakness. The line: 'State the number, the baseline, and what you refuse to claim.'"),
("What do you do when the data is worse than expected?",
 "Document exactly what's broken, shrink the question to what the data can answer, and show what a better dataset would unlock. Adapting scope to data quality is a professional skill, not a failure. The line: 'Bad data narrows the question — it doesn't end the project.'"),
],
}
NEWCARDS.update({
"advanced-genai--transformer-arch-practice": [
("What does multi-head attention add over single-head?",
 "Each head learns a different relation — syntax, coreference, position — in its own subspace, and the model combines them. One head is one lens; many heads are a compound eye. The line: 'Multi-head attention lets the model attend to different kinds of relationships at once.'"),
("Why do positional encodings matter?",
 "Attention is permutation-invariant — without position information, 'dog bites man' and 'man bites dog' look identical. Positional encodings (sinusoidal or rotary) inject order back in. The line: 'Attention sees sets; positional encodings restore sequence.'"),
],
"advanced-genai--pretrain-finetune-practice": [
("What is catastrophic forgetting in fine-tuning?",
 "Aggressive fine-tuning can overwrite pretrained knowledge — the model gets better at the new task and worse at everything else. Mitigations: small learning rates, replay of general data, parameter-efficient methods like LoRA. The line: 'Fine-tune too hard and the model forgets what it knew to learn what you taught.'"),
("When is full fine-tuning worth the cost?",
 "When the task needs deep behavioral change across many layers and you have the data and compute to justify it — otherwise LoRA/PEFT gets most of the gain for a fraction of the cost. The line: 'Full fine-tuning for deep change; adapters for everything else.'"),
],
"advanced-genai--alignment-practice": [
("What is a reward model?",
 "A learned function that scores outputs by human preference — trained on ranked comparisons, then used to steer the policy model in RLHF or to rank candidates at inference. It encodes 'what humans liked' as a number. The line: 'The reward model is preference turned into a gradient.'"),
("How do you red-team an aligned model?",
 "Probe systematically for jailbreaks, instruction conflicts, and edge cases: adversarial prompts, multi-turn traps, encoded requests, and role-play frames. Document every break, fix, and re-test. The line: 'Red-teaming is quality assurance for behavior — assume it breaks until proven otherwise.'"),
],
"advanced-genai--genai-eval-practice": [
("What is an eval harness?",
 "Repeatable infrastructure for scoring models: versioned prompts, fixed datasets, metric computation, and run-to-run comparison. Without a harness, every evaluation is a one-off opinion. The line: 'A harness turns evaluation from an event into a habit.'"),
("How do you evaluate factuality?",
 "Check claims against trusted sources: retrieval-grounded verification, claim decomposition with per-claim checks, and human spot-audits on samples. Never trust the model to grade its own facts. The line: 'Factuality is verified against sources, never against vibes.'"),
],
"advanced-genai--inference-serving-practice": [
("What is speculative decoding?",
 "A small draft model proposes tokens and the large model verifies them in parallel — accepting correct runs and correcting the rest. It speeds up inference without changing outputs. The line: 'Speculative decoding: draft fast, verify in bulk, keep the same answers.'"),
("How do you handle long-context requests?",
 "Budget explicitly: context costs memory (KV cache grows with tokens) and latency (attention is quadratic-ish), so truncate, summarize, or retrieve selectively — and price it per request. The line: 'Long context is a budget line item: tokens, memory, latency, dollars.'"),
],
"advanced-genai--genai-capstone": [
("How do you choose the base model?",
 "Match the model to the job: capability on your task's evals, context length, cost per call, latency, and license terms for your use case. Benchmark candidates on your data, not on public leaderboards. The line: 'Leaderboards are marketing; your eval suite is the interview.'"),
("What does a responsible launch checklist include?",
 "Harm review, failure-mode tests, guardrails and monitoring, a rollback plan, user-facing disclosures, and an owner for incidents. Launch readiness is a document, not a feeling. The line: 'If it isn't written down, it isn't launch-ready.'"),
],
"advanced-nlp-practice--nlp-pipelines-practice": [
("When do you lowercase, and when don't you?",
 "Lowercase for case-insensitive matching (search, topic models); preserve case when it carries meaning — named entities, acronyms, sentence starts. The decision is task-specific, not a default. The line: 'Case is information; I only discard it when the task says it's noise.'"),
("How do you handle emojis and social text?",
 "Normalize deliberately: emojis carry sentiment and shouldn't be silently stripped; expand or map them, handle hashtags and mentions as tokens, and expect misspellings. Social text needs its own preprocessing path. The line: 'Social text is a dialect — process it with its own rules.'"),
],
"advanced-nlp-practice--embeddings-practice": [
("What is the anisotropy problem?",
 "In some embedding spaces, vectors cluster in a narrow cone — everything looks similar — which degrades similarity search. Fixes include normalization, centering, or better training objectives. The line: 'Anisotropy is when the embedding space collapses; similarity needs room to vary.'"),
("How do you choose embedding dimensionality?",
 "Bigger captures more nuance but costs storage, memory, and search latency; the practical move is to benchmark candidate sizes on your retrieval task and pick the smallest that doesn't hurt. The line: 'Dimension is a price — I buy only what my task's evals justify.'"),
],
"advanced-nlp-practice--sequence-models-practice": [
("What is the BIO tagging scheme?",
 "A labeling convention for spans: B- marks the beginning of an entity, I- continues it, O is outside any entity. It turns span extraction into per-token classification. The line: 'BIO turns 'find the names' into a token-labeling problem.'"),
("How do you handle class imbalance in text classification?",
 "The same three levers as elsewhere: class weights in the loss, threshold tuning on the PR curve, and resampling — plus checking that the minority class has enough quality labels. The line: 'Imbalance in text is still a cost problem: weight it, threshold it, label it.'"),
],
"advanced-nlp-practice--llm-for-nlp": [
("What is prompt brittleness?",
 "Small prompt changes causing large output swings — the model overfits to phrasing. Defenses: few-shot examples that stabilize format, structured-output constraints, and testing prompt variants. The line: 'Brittle prompts are untested code; I version and test them.'"),
("How do you validate LLM-generated labels?",
 "Audit a stratified sample with human review, measure agreement (and where the model systematically errs), and never let the model label its own eval set. The line: 'LLM labels are draft labels — humans sign off on the sample.'"),
],
"advanced-nlp-practice--retrieval-practice": [
("What is the index build tradeoff?",
 "Dense indexes cost compute to build and memory to serve but answer fast; larger chunks improve recall but hurt precision; reindexing cadence trades freshness against cost. The line: 'Indexing trades build cost for query speed — I size it to the freshness the task needs.'"),
("How do you handle queries with no good answer?",
 "Design for the miss: a relevance threshold below which you abstain or say so, fallback to broader search, and log the misses to improve coverage. Silent bad answers are the worst outcome. The line: 'No good answer is itself an answer — I design the abstention path.'"),
],
"advanced-nlp-practice--nlp-project": [
("How do you define the annotation guideline?",
 "Write the rulebook before labeling: exact definitions, edge-case examples, tie-breaking rules, and a process for disagreements. The guideline is what makes two annotators produce the same labels. The line: 'The guideline is the label's specification — vague rules, vague data.'"),
("What goes in the final demo?",
 "The problem, a live example with visible failure cases, the tradeoff table (accuracy vs cost vs latency), and an honest limits slide. Demos that only show successes get hard questions. The line: 'Demo the failures too — they prove you measured.'"),
],
"ai-enabled-software--llm-apis-practice": [
("What is idempotency for LLM calls?",
 "Making repeated calls safe: deduplicating by request key, caching deterministic outputs, and designing retries that don't double-charge or double-act. Non-deterministic models make this harder — so you engineer it. The line: 'Retries without idempotency are duplicate actions waiting to happen.'"),
("How do you version prompts?",
 "Treat prompts as code: in version control, with changelogs, pinned to model versions, and covered by evals that catch regressions. 'Tweaked the prompt' should be a diff, not a memory. The line: 'Prompts are code — versioned, reviewed, and tested.'"),
],
"ai-enabled-software--rag-practice": [
("What is query rewriting for?",
 "Reformulating the user's question — expanding abbreviations, adding context, splitting compound questions — before retrieval, so the search sees a better query than the raw input. The line: 'Users ask badly; rewriting asks well on their behalf.'"),
("How do you handle multi-hop questions?",
 "Decompose into sub-questions, retrieve for each, and synthesize — possibly iteratively, using intermediate answers to guide the next retrieval. Single-shot retrieval fails when the answer spans documents. The line: 'Multi-hop questions get multi-step retrieval — one hop per sub-question.'"),
],
"ai-enabled-software--eval-harness-practice": [
("What is a failure taxonomy?",
 "A named, counted classification of how the system fails — retrieval miss, hallucination, tool error, format break — so fixes target the biggest category first. Untaxonomized failures get anecdotal fixes. The line: 'Count your failures by type; fix the biggest bucket first.'"),
("How do you measure judge agreement?",
 "Have the LLM judge and humans score the same sample, then compute agreement (Cohen's kappa or simple concordance) — and recalibrate or constrain the judge where they diverge. The line: 'An uncalibrated judge is an opinion; agreement with humans makes it a measurement.'"),
],
"ai-enabled-software--tool-use-practice": [
("What is the ReAct pattern?",
 "Interleaving reasoning traces with actions: the model thinks, acts (calls a tool), observes the result, and repeats. It grounds the model's plans in real tool outputs. The line: 'ReAct: reason, act, observe — the loop that keeps agents honest.'"),
("How do you prevent prompt injection via tools?",
 "Treat tool outputs as untrusted data, never as instructions: sandbox tool results, validate before acting, and keep privilege boundaries so a poisoned document can't trigger sensitive actions. The line: 'Tool output is data, not orders — I never let it outrank the system prompt.'"),
],
"ai-enabled-software--shipping-ai-features": [
("What is a kill switch for AI features?",
 "A fast, tested path to disable the model-backed behavior instantly — feature flag, fallback to the old path, and an alert that fires when it's used. Ship the off-ramp before the feature. The line: 'The kill switch ships before the feature — off must be one click.'"),
("How do you handle latency budgets?",
 "Set a per-request budget, measure p50/p99 (not the mean), and design fallbacks for the tail: timeouts, cached responses, degraded modes. Users feel the tail, not the average. The line: 'Budget the p99, not the mean — the tail is the user experience.'"),
],
"ai-enabled-software--ai-feature-project": [
("How do you demo an AI feature honestly?",
 "Show a real task end-to-end, include a failure case and how the system handles it, and state the eval numbers behind the claims. A demo is a claim; evidence makes it credible. The line: 'Honest demos show the failure mode — that's what makes the success believable.'"),
("What does post-launch monitoring look like?",
 "The eval suite running on live traffic samples, latency and cost dashboards, user-feedback funnels into new eval cases, and a named owner for regressions. Launch is the start of measurement, not the end. The line: 'Launch day is when monitoring starts earning its keep.'"),
],
})
NEWCARDS.update({
"applied-ai-production--problem-framing-ai": [
("How do you frame the counterfactual?",
 "State what happens without the model: the current process, its cost, and its error rate. The counterfactual is the baseline every AI proposal must beat — no model wins against an unmeasured status quo. The line: 'No counterfactual, no business case.'"),
("What is a pre-mortem for AI projects?",
 "Before building, assume the project failed and write down why: data never arrived, labels were noisy, users didn't trust it. Then design against the top risks. The line: 'Pre-mortems turn hindsight into foresight — cheap insurance.'"),
],
"applied-ai-production--data-strategy-ai": [
("What is data lineage for ML?",
 "The recorded path from raw source through every transform to the training rows — so a data bug can be traced to affected models and a model bug traced to its data. Lineage is the audit trail. The line: 'Lineage answers: which models ate this bad data?'"),
("How do you estimate labeling cost?",
 "Cost per label × number of labels × annotators for agreement, plus guideline-writing and QA time. Pilot 100 labels first to measure real throughput before committing. The line: 'Price the pilot, then multiply — labeling budgets surprise everyone once.'"),
],
"applied-ai-production--prototyping-ai": [
("What is a concierge MVP for AI?",
 "A human performs the 'AI' behind the scenes while users interact with the real interface — testing demand and UX before building the model. It validates the problem, not the technology. The line: 'Concierge first: prove someone wants it before proving a model can do it.'"),
("How do you test a prototype with real users?",
 "Give them real tasks, watch without helping, and measure task success plus where they hesitate. Five users find most usability problems; their hesitations are requirements. The line: 'Watch five users struggle and you'll learn more than from fifty surveys.'"),
],
"applied-ai-production--stakeholder-comm-ai": [
("How do you present model risk to executives?",
 "In their currency: probability of failure × business impact, with a mitigation per risk and a named owner. No jargon, no ROC curves — decisions and dollars. The line: 'Executives buy risk in dollars and decisions, not metrics.'"),
("What goes in a model card for stakeholders?",
 "What the model does, what data it learned from, where it performs well and poorly, known limitations, and who to contact. One page, plain language. The line: 'The model card is the model's résumé — capabilities, limits, references.'"),
],
"applied-ai-production--measuring-ai-value": [
("What are leading versus lagging indicators for AI?",
 "Leading indicators move first and predict value — adoption, query volume, user retention. Lagging indicators confirm it — revenue, cost saved. Track both; steer by leading, report by lagging. The line: 'Leading indicators steer, lagging indicators prove.'"),
("How do you attribute revenue to a model?",
 "Compare against the counterfactual: A/B the model-backed experience, or measure the incremental lift versus the pre-model baseline with confounds controlled. Correlation is not attribution. The line: 'Attribution needs a counterfactual — the model's credit is the lift over without-it.'"),
],
"applied-ai-production--applied-ai-capstone": [
("How do you hand off a model to an engineering team?",
 "Transfer the runnable artifacts plus the knowledge: training code, data pipeline, eval suite, known failure modes, monitoring setup, and a walkthrough session. A handoff is complete when they can retrain without you. The line: 'The handoff succeeds when the team can retrain it without calling you.'"),
("What does a runbook for an AI system contain?",
 "Symptom-to-action for the failures you'll see: data drift alerts, latency spikes, quality regressions — each with the check to run and the fix to apply, plus escalation contacts. The line: 'The runbook is the 3am version of you — write it while you're calm.'"),
],
"advanced-ml--re-bench-agents-ml-research": [
("What is the agentic scaffold in RE-Bench?",
 "The tooling wrapper around the model — shell access, code execution, file editing, and time limits — that turns a language model into an agent that can actually do ML research tasks. The scaffold is half the score. The line: 'In agentic evals, the scaffold is the athlete's equipment.'"),
("Why do agents beat humans early but lose late in RE-Bench?",
 "Agents parallelize and iterate tirelessly on short horizons; humans bring taste, deep debugging, and long-horizon strategy that compounds over hours. The crossover point marks where judgment beats speed. The line: 'Agents win the sprint, researchers win the marathon.'"),
("What is score normalization in RE-Bench?",
 "Raw scores are mapped to a 0–1 scale against human expert baselines so different environments (kernels, training runs, agent tasks) become comparable. Normalization is what makes 'better than the expert' a number. The line: 'Normalization turns seven different tasks into one comparable score.'"),
],
})

TRAINERS = [
 {"id": "metric-choice-trainer",
  "title": "Evaluation metric trainer",
  "brief": "Rapid-fire metric selection reps: given a problem shape (imbalanced classes, ranking, regression, cost asymmetry), pick the right metric and defend it — the decision interviewers probe first.",
  "kind": "custom"},
 {"id": "tuning-intuition-trainer",
  "title": "Tuning intuition trainer",
  "brief": "Hyperparameter and optimization judgment drills: learning-rate behavior, batch-size effects, early stopping, and budget discipline — build the instincts behind the tuning loop.",
  "kind": "custom"},
]

TERMINALSIMS = [
 {"id": "ml-cli",
  "title": "ML CLI sandbox",
  "brief": "Practice the machine-learning command line from the Python-for-ML path — project layout, environments, training runs, and experiment tracking — against a realistic sandbox.",
  "prompt": "learner@il:~/ml-project$",
  "commands": [
  {"cmd": "pwd", "out": "/home/learner/ml-project"},
  {"cmd": "ls", "out": "configs  data  models  notebooks  src  tests"},
  {"cmd": "ls src/", "out": "__init__.py  data.py  features.py  train.py  evaluate.py"},
  {"cmd": "cat configs/baseline.yaml", "out": "model: random_forest\nn_estimators: 200\nmax_depth: 12\nseed: 42\ntest_size: 0.2"},
  {"cmd": "python -m venv .venv && echo done", "out": "done"},
  {"cmd": "pip show scikit-learn | head -2", "out": "Name: scikit-learn\nVersion: 1.5.2"},
  {"cmd": "python src/train.py --config configs/baseline.yaml", "out": "Loading data/train.csv ... 48000 rows\nFitting random_forest (n_estimators=200, max_depth=12) ...\nval_f1: 0.8231\nSaved: models/rf_baseline.pkl"},
  {"cmd": "ls -lh models/", "out": "total 18M\n-rw-r--r-- 1 learner learner 18M Oct  7 10:41 rf_baseline.pkl"},
  {"cmd": "python src/evaluate.py --model models/rf_baseline.pkl --split test", "out": "test_accuracy: 0.8914\ntest_f1:      0.8187\ntest_auc:     0.9342"},
  {"cmd": "mlflow runs list --experiment baseline", "out": "run_id    val_f1   params\n9f3a2c1   0.8231   n_estimators=200,max_depth=12\n7b1e90d   0.8155   n_estimators=100,max_depth=8"},
  {"cmd": "git status --short", "out": " M src/features.py\n?? models/rf_baseline.pkl"},
  {"cmd": "git add src/features.py && git commit -m \"add target encoding\" --quiet && echo committed", "out": "committed"},
  {"cmd": "python src/train.py --config configs/baseline.yaml --seed 7", "out": "Loading data/train.csv ... 48000 rows\nFitting random_forest (n_estimators=200, max_depth=12) ...\nval_f1: 0.8219\nSaved: models/rf_baseline.pkl"},
  {"cmd": "echo $PYTHONPATH", "out": "/home/learner/ml-project/src"},
  {"cmd": "head -3 data/train.csv", "out": "id,signup_month,plan,tenure_days,churned\n1001,2024-02,basic,412,0\n1002,2024-02,pro,388,1"},
  {"cmd": "du -sh data/", "out": "214M\tdata/"},
  {"cmd": "history | tail -3", "out": "  31  python src/train.py --config configs/baseline.yaml\n  32  python src/evaluate.py --model models/rf_baseline.pkl --split test\n  33  mlflow runs list --experiment baseline"}
 ]},
 {"id": "model-eval",
  "title": "Model evaluation sandbox",
  "brief": "Practice the evaluation workflow from the Model Evaluation module — metrics, confusion matrices, learning curves, and head-to-head comparison — in a canned eval console.",
  "prompt": "eval> ",
  "commands": [
  {"cmd": "help", "out": "commands: models, eval, confusion-matrix, learning-curve, compare, slices, threshold"},
  {"cmd": "models", "out": "baseline   (logistic regression)\nrf         (random forest, n=200)\nxgb        (gradient boosting, lr=0.05)"},
  {"cmd": "eval --model baseline --metric accuracy", "out": "baseline | accuracy = 0.8914 (n=12000)"},
  {"cmd": "eval --model baseline --metric f1", "out": "baseline | f1 = 0.6231  <- accuracy hides the minority-class weakness"},
  {"cmd": "eval --model rf --metric f1", "out": "rf       | f1 = 0.8187"},
  {"cmd": "eval --model xgb --metric f1", "out": "xgb      | f1 = 0.8412"},
  {"cmd": "confusion-matrix --model baseline", "out": "              pred 0   pred 1\nactual 0      10231      189\nactual 1        745      835\nprecision=0.815  recall=0.529"},
  {"cmd": "confusion-matrix --model xgb", "out": "              pred 0   pred 1\nactual 0      10390      130\nactual 1        402     1078\nprecision=0.892  recall=0.728"},
  {"cmd": "learning-curve --model rf", "out": "n=5k:   train_f1=0.94  val_f1=0.76   (gap: variance)\nn=20k:  train_f1=0.90  val_f1=0.80\nn=48k:  train_f1=0.87  val_f1=0.82   (converging: more data helps little)"},
  {"cmd": "compare --models baseline,rf,xgb --metric f1", "out": "baseline  0.6231\nrf        0.8187\nxgb       0.8412   <- best, but 4x the training cost of rf"},
  {"cmd": "slices --model xgb --by plan", "out": "plan=basic  f1=0.85 (n=8200)\nplan=pro    f1=0.83 (n=3100)\nplan=trial  f1=0.61 (n=700)  <- worst slice: sparse segment"},
  {"cmd": "threshold --model xgb --target recall=0.85", "out": "threshold 0.32 -> recall=0.851, precision=0.774\n(reports the operating point; costs decide if it ships)"},
  {"cmd": "eval --model xgb --metric logloss", "out": "xgb      | logloss = 0.2147  (lower is better; check calibration next)"}
 ]}
]

# re-bench note titles -> course-consistent ('Hands-on procedure', 'Honesty note')
NOTEFIX = {"advanced-ml--re-bench-agents-ml-research":
           {"Worked estimation": "Hands-on procedure",
            "Frontier honesty": "Honesty note"}}

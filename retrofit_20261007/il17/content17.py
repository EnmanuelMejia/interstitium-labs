# Per-module authored content for the IL-17 retrofit.
# Keys are the short module key (part of the course module id after '--').

CONCEPTS_EXTRA = {
 ('agent-starter-build','Adding memory'): "Adding memory — giving the starter agent continuity across steps with a simple summary buffer, so multi-step tasks don't restart from zero every step.",
 ('repo-scale-agents','Indexing large codebases'): "Indexing large codebases — chunking code by file and symbol into a searchable index, so retrieval replaces the impossible goal of fitting the whole repo in context.",
 ('data-agents-core','Result interpretation'): "Result interpretation — translating query results into answers with the caveats a data engineer would add: grain, filters, freshness, and what the data cannot say.",
 ('data-quality-agents','Quality dashboards'): "Quality dashboards — the single page showing check status over time, where green must mean 'checked and healthy', never 'not checked'.",
 ('data-agent-project','Document limits'): "Document limits — writing down what the agent cannot do, the schema corners it misunderstands, and the failures you actually saw, as a first-class deliverable.",
 ('data-agent-project','Project write-up'): "Project write-up — the honest report: what was built, the eval numbers, the guardrails demonstrated, and the limits — numbers and misses, not just the demo.",
 ('pm-agent-playbook','Project write-up'): "Project write-up — the pilot report: metric deltas, guardrail compliance, and the expand/iterate/stop decision with the numbers attached.",
 ('pm-agent-roadmap','Launch checklists'): "Launch checklists — the pre-launch gate: evals green, guardrails instrumented, rollback planned, costs modeled, non-goals agreed — checked before launch, not after.",
 ('incident-agents','Timeline reconstruction'): "Timeline reconstruction — assembling the incident's true sequence from alerts, deploys, and messages, so the postmortem argues about causes, not about what happened when.",
 ('leader-agent-metrics','Reporting to leadership'): "Reporting to leadership — the one-page net: savings minus all costs, quality delta, adoption, and counter-metrics — numbers defensible in a budget review.",
 ('agent-system-design','Trade-off narration'): "Trade-off narration — stating each design choice's cost aloud before being asked: what you gain, what you pay, and what breaks if you're wrong.",
 ('agentic-mock','Feedback integration'): "Feedback integration — the within-24-hours discipline of turning mock misses into fixes, because mocks without iteration are just performance anxiety practice.",
 ('lowcode-platforms','Choosing a platform'): "Choosing a platform — matching the workflow to the platform's strengths (standard connectors, simple logic) and scoring the trade-aways (portability, customization, cost at scale) before building.",
 ('lowcode-prompt-flows','Chaining steps'): "Chaining steps — feeding one prompt's output into the next via variables, watching where the chain helps and where context leaks between steps.",
 ('lowcode-prompt-flows','Testing flows'): "Testing flows — treating flows as code: fixed inputs, expected outputs, pass/fail logs — because untested flows fail in front of users.",
 ('lowcode-prompt-flows','Iterating on prompts'): "Iterating on prompts — changing one prompt at a time, re-running the test set, and keeping the version that scores better: prompt versioning as engineering.",
 ('lowcode-prompt-flows','Sharing flows'): "Sharing flows — handing the flow to a colleague and watching them use it; their confusion is the UX feedback no self-review provides.",
 ('lowcode-connectors','Error handling'): "Error handling — designing what the user sees when the connector fails: revoked credentials, renamed columns, throttled APIs — failure modes tested on purpose, not discovered in production.",
 ('lowcode-project','Project write-up'): "Project write-up — the delivery note: what the agent automates, the user-test results, and the limits — honest enough to hand to the team's future maintainer.",
 ('lowcode-deploy','Versioning'): "Versioning — saving v1 before the first change and practicing the rollback, so 'deploy' never means 'no way back'.",
}

MODULES = {}

# ---------------- agentic-ai-foundations ----------------
MODULES['llm-tool-use'] = {
 'sec2': 'Hands-on procedure',
 'procedure': [
  "Write the contract: define a JSON schema for one read-only tool (for example `lookup_order`) with a name, a human-readable description, typed parameters (`order_id`: string, required), and no write operations.",
  "Draft the calling convention: instruct the model to emit exactly one JSON object matching the schema when it needs the tool, and plain text otherwise — no prose wrapped around the JSON.",
  "Simulate three model replies by hand: one valid call, one with a wrong type (`order_id` as a number), and one naming a tool that does not exist.",
  "Build the validator: a small function that checks the call against the schema — known tool name, required fields present, types correct — and returns a structured error object on failure.",
  "Run the dispatcher: feed the valid call through (validate, then execute a stub returning canned data); feed the two invalid ones and confirm the validator rejects them with errors the model could act on.",
  "Add tool-choice control: implement three modes — auto (model decides), required (force one specific call), none (answer from context only) — and decide per step which your use case needs.",
  "Add retry discipline: transient execution failures return a structured error for one retry with backoff; validation failures escalate immediately instead of retrying.",
  "Log every call: tool name, arguments, latency, outcome — the raw material your eval harness will need in the Agent Evaluation module.",
 ],
 'code': ("python",
  "import json\n\nTOOL_SCHEMAS = {\n    \"lookup_order\": {\n        \"type\": \"object\",\n        \"properties\": {\"order_id\": {\"type\": \"string\"}},\n        \"required\": [\"order_id\"],\n    }\n}\n\ndef validate(tool_name, args):\n    schema = TOOL_SCHEMAS.get(tool_name)\n    if schema is None:\n        return False, {\"error\": \"unknown_tool\", \"tool\": tool_name}\n    for field in schema[\"required\"]:\n        if field not in args:\n            return False, {\"error\": \"missing_field\", \"field\": field}\n    return True, {}\n\ndef dispatch(tool_name, args, tool_choice=\"auto\"):\n    if tool_choice == \"none\":\n        return {\"answer_from_context\": True}\n    ok, err = validate(tool_name, args)\n    if not ok:\n        return {\"rejected\": True, **err}  # structured, model-actionable\n    return {\"result\": f\"stub result for {args}\"}  # real impl goes here"),
 'project': "Contract-first tool server. Design and implement a tiny tool server exposing three read-only tools with JSON schemas, a validator, tool-choice modes (auto/required/none), and structured error returns. Deliverables: the three schema definitions, the validator and dispatcher code, a log of 20 simulated calls including 5 adversarial ones (wrong types, unknown tools, missing fields), and a one-page write-up of what the validator caught and why each rule exists.",
 'honest': "This module teaches contract discipline, not any vendor's SDK — function-calling APIs change, so treat the docs linked below as the live reference (as of October 2026). We stay read-only here; write-capable tools and their approvals arrive in later modules. Ask yourself: could you explain why each validation rule exists, in one sentence each?",
}

MODULES['agent-loops'] = {
 'sec2': 'Hands-on procedure',
 'procedure': [
  "Sketch the loop on paper: boxes for perceive, reason, act, and observe, with the observation feeding back into perceive — the control flow that makes a model an agent.",
  "Define stopping conditions first: a max step count (for example 10), a max wall-clock time, and terminal signals — task complete, explicit escalation, or the same action repeated three times.",
  "Hand-simulate ReAct: take a three-step task, write the thought trace the model should emit before each action, then the action, then a plausible observation.",
  "Implement plan-and-execute: a planner step that decomposes the task into numbered sub-steps, then an executor loop that works the plan, marking steps done or failed.",
  "Add replanning: when a step fails twice, trigger a replan that revises only the remaining steps — never restarts the whole task from scratch.",
  "Build the ambiguity gate: if the instruction lacks a required parameter, the loop asks a clarifying question instead of guessing — implement the check before the first action runs.",
  "Decide loop vs single call: list three tasks from your own work; for each, argue in two sentences whether a loop earns its latency and cost or a single call wins.",
  "Run one full loop against stub tools and confirm each stopping condition fires at least once across your test runs.",
 ],
 'code': ("python",
  "MAX_STEPS = 10\n\ndef run_loop(task, tools):\n    state, steps, last_actions = {\"task\": task}, 0, []\n    while steps < MAX_STEPS:                       # the off-switch: step budget\n        thought = reason(state)                     # ReAct: explicit thought\n        action = decide_action(thought, tools)\n        if action is None:                           # ambiguity gate\n            return ask_clarifying_question(state)\n        if last_actions[-3:] == [action]*3:          # stall detection\n            return escalate(\"repeated action\", state)\n        observation = tools[action.name](action.args)\n        state = update(state, thought, action, observation)\n        last_actions.append(action)\n        steps += 1\n        if task_complete(state):\n            return state[\"result\"]\n    return escalate(\"step budget exhausted\", state)"),
 'project': "Loop with an off-switch. Implement a ReAct-style loop in Python with typed tool stubs, a step budget, stall detection (same action three times stops the run), and a full run transcript. Deliverables: the code, transcripts of three runs — a success, a graceful stop on budget, and a stall detected — and a short note on which stopping condition fired in each run and why.",
 'honest': "Loops feel like intelligence; they are control flow. Nothing here makes the model itself more capable — the loop only organizes what the model can already do. The failure mode we drill, the unbounded loop, is the one that bills you in production. Ask yourself: for your project, what is the cheapest correct stopping condition?",
}

MODULES['memory-context'] = {
 'sec2': 'Hands-on procedure',
 'procedure': [
  "Instrument a loop: add a token counter that logs, per step, how many tokens go to instructions, conversation history, tool outputs, and working space.",
  "Set the budget before running anything: pick a total per-task token budget and split it across those four buckets — write the split down.",
  "Implement verbatim history: keep the last N turns untouched; everything older becomes a candidate for summarization.",
  "Write the summarizer: a prompt that compresses older turns into a running summary preserving decisions, open questions, and tool outcomes — test it on a 20-turn sample transcript and check nothing load-bearing is lost.",
  "Add vector recall: embed each observation (a toy hashing embedder suffices for the exercise), store it, and retrieve the top-3 most similar past observations for a new query.",
  "Build the checkpoint: after each step, persist the full agent state — step number, summary, pending plan — to a JSON file; kill the process mid-run and resume from the file.",
  "Stress it: run a 30-step simulated task, watch which bucket blows its budget first, then rebalance and re-run.",
  "Write the budget postmortem: planned split versus actual spend, and the one change you'd make to the split next time.",
 ],
 'code': ("python",
  "import json\n\ndef save_checkpoint(path, state):\n    with open(path, \"w\") as f:      # atomic write in real use: tmp + rename\n        json.dump(state, f)\n\ndef load_checkpoint(path):\n    try:\n        with open(path) as f:\n            return json.load(f)\n    except FileNotFoundError:\n        return {\"step\": 0, \"summary\": \"\", \"plan\": []}\n\nstate = load_checkpoint(\"agent_state.json\")\n# ... run steps, updating state[\"summary\"] and state[\"plan\"] ...\nsave_checkpoint(\"agent_state.json\", state)  # pause/resume + audit trail"),
 'project': "Budgeted memory. Extend your loop from the Agent Loops module with the four-bucket token budget, running summarization, and JSON checkpoints. Deliverables: the budget table (planned vs actual), a transcript of a run resumed from a checkpoint after a simulated kill, and a one-page analysis of where tokens actually went versus your plan.",
 'honest': "Memory patterns don't fix a model that can't reason — they only organize what it has to work with. Summarization loses detail by design; the discipline is choosing what is safe to lose. Ask yourself: what would break in your agent if the summary dropped one fact?",
}

MODULES['multi-agent-systems'] = {
 'sec2': 'Hands-on procedure',
 'procedure': [
  "Prove one agent is insufficient: take a real task, walk it single-agent on paper, and name the specific bottleneck — context overload, genuinely different skills, or parallelizable subtasks.",
  "Draw the team: a box per agent with its role, its tools, and the typed handoff contract — what it receives and what it must return.",
  "Define the handoff schemas as JSON: include `result`, `confidence`, and `open_questions` fields so uncertainty survives the handoff instead of being smoothed away.",
  "Simulate supervisor/worker by hand: write the supervisor's delegation messages, each worker's reply, and the integration — noting every place context had to be repeated.",
  "Count the overhead: tally tokens spent on coordination versus tokens spent on the actual task, and write the ratio down.",
  "Run the debate variant: two agents argue a judgment call for three rounds, then a judge agent decides — time-box it and note where it added value versus theater.",
  "Write the collapse checklist: five warning signs (repeated clarification requests, conflicting assumptions, cascading retries, chatter without progress, cost far above single-agent) that trigger collapsing back to one agent.",
  "Deliver the verdict for your task: did the team earn its complexity, measured end-to-end?",
 ],
 'code': ("python",
  "HANDOFF_SCHEMA = {\n    \"type\": \"object\",\n    \"properties\": {\n        \"result\": {\"type\": \"string\"},\n        \"confidence\": {\"type\": \"string\", \"enum\": [\"high\", \"medium\", \"low\"]},\n        \"open_questions\": {\"type\": \"array\", \"items\": {\"type\": \"string\"}},\n    },\n    \"required\": [\"result\", \"confidence\", \"open_questions\"],\n}\n# Every handoff between agents is validated against this schema:\n# uncertainty is data, not noise."),
 'project': "Two-agent pipeline, honestly measured. Build a supervisor/worker pair on a decomposable task (for example research-then-draft), with typed handoff schemas. Deliverables: the handoff schemas, the end-to-end transcript, a token and cost comparison against your single-agent baseline, and the verdict — did the team earn its complexity?",
 'honest': "Multi-agent demos are seductive and usually slower and more expensive than one good agent. This module's default — one agent, prove you need two — is the position you should defend in interviews and in production. Ask yourself: what exactly does the second agent know or do that the first cannot?",
}

MODULES['agent-evaluation'] = {
 'sec2': 'Hands-on procedure',
 'procedure': [
  "Fix the task set: write 10 tasks your agent should handle, each with a known-good outcome and the constraints it must respect — this set is your ground truth.",
  "Define the trajectory dimensions: for each task, score task success, steps taken, tool-call efficiency (total calls, redundant calls, failed calls), and safety-constraint adherence.",
  "Build the harness: a runner that executes the agent on all 10 tasks, captures the full trajectory, and writes one JSON row per run.",
  "Add failure injection: for 3 of the tasks, sabotage a tool — return an error, return plausible-but-wrong data, time out — and score whether the agent detects, adapts, or escalates.",
  "Score safety: define 3 rules (for example: never call the write tool without confirmation; never exfiltrate conversation content; stay within the step budget) and grade each trajectory pass/fail per rule.",
  "Run the regression: change one prompt line, re-run all 10 tasks, and diff the scores — this is the workflow that prevents silent regressions from prompt edits.",
  "Write the report: one table, tasks by dimensions, plus the single number you'd put on a dashboard and one paragraph defending why that number.",
 ],
 'code': ("python",
  "def run_eval(agent, tasks):\n    rows = []\n    for t in tasks:\n        traj = agent.run(t[\"prompt\"], sabotage=t.get(\"sabotage\"))\n        rows.append({\n            \"task\": t[\"id\"],\n            \"success\": traj.outcome == t[\"expected\"],\n            \"steps\": len(traj.steps),\n            \"tool_calls\": traj.tool_call_count,\n            \"redundant_calls\": traj.redundant_count,\n            \"safety_pass\": all(rule(traj) for rule in SAFETY_RULES),\n        })\n    return rows  # one JSON row per run: the regression artifact"),
 'project': "Eval harness v1. A runnable harness over your starter agent (or a stub) with 10 tasks, failure injection on 3, and a scored report. Deliverables: the task set with expected outcomes, the harness code, the score table, and a regression run showing a one-line prompt change's effect on the scores.",
 'honest': "Evals measure your task set, not the world — a green harness on 10 friendly tasks proves nothing about task 11. The failure-injection habit matters more than the score. Ask yourself: which realistic failure is missing from your task set?",
}

MODULES['agent-starter-build'] = {
 'sec2': 'Hands-on procedure',
 'procedure': [
  "Scope the slice in writing: one task, at most three read-only tools, written success criteria, and a written list of what the agent will not do.",
  "Choose tools with least privilege: for each tool, justify in one sentence why it needs exactly the permissions it has and no more.",
  "Build the loop by hand first: perceive-reason-act with a step budget and transcript logging, before touching any framework — you need to feel the mechanics.",
  "Port to a framework: reimplement the same agent with your chosen framework's agent primitives; write down what the framework handled versus what it hid.",
  "Add memory: the summary buffer from the Memory module; verify a 15-step run stays inside your token budget.",
  "Evaluate: run your 10-task harness; record success rate, median steps, and safety passes — the three numbers that describe this agent.",
  "Write the honest write-up: what it does, the numbers, and the limits — including the failure you understand least.",
 ],
 'code': ("python",
  "# The hand-rolled loop from Agent Loops, now with memory and a budget:\nstate = {\"summary\": \"\", \"step\": 0}\nwhile state[\"step\"] < STEP_BUDGET:\n    thought = reason(task, state[\"summary\"])\n    action = pick_action(thought, TOOLS)  # TOOLS: <=3, read-only\n    if action is None:\n        break  # nothing safe to do: stop, don't guess\n    obs = TOOLS[action.name](action.args)\n    state[\"summary\"] = summarize(state[\"summary\"], thought, action, obs)\n    state[\"step\"] += 1\n    log(state)  # every step on the transcript"),
 'project': "Ship the starter. The full starter agent: framework implementation, memory, eval numbers, and the honest write-up. Deliverables: a repo with README, the eval table (success rate, median steps, safety passes), and the limits section — the portfolio piece this track builds toward.",
 'honest': "A starter agent is a learning vehicle, not a product. The write-up's limits section is the most important part — it is what separates an engineer from a demo. Ask yourself: what would you need to change before a stranger could depend on this?",
}

# ---------------- agentic-ai-for-swe ----------------
MODULES['code-agents'] = {
 'sec2': 'Hands-on procedure',
 'procedure': [
  "Pick a real small repo you own and choose one bounded issue that already has tests — the tests are your oracle for everything that follows.",
  "Write the task spec the agent will receive: what 'done' looks like, which files are in scope, which APIs are allowed, and what is explicitly out of scope.",
  "Gather context by retrieval: pull only the files relevant to the issue — note which files you retrieved and why, practicing the retrieval discipline from the repo-scale module.",
  "Run the loop: propose a diff, run the tests, read the failure, fix, repeat — cap the run at 10 iterations and log each one.",
  "Review the final diff as a stranger: every hunk needs a reason you can state; flag anything you cannot explain.",
  "Verify with tests the agent didn't write: run the project's own suite, then add one test the agent didn't think of and watch it pass.",
  "Measure the economics: iterations to green, lines changed, wall-clock time, and tokens if measurable — the numbers that describe this workflow's cost.",
 ],
 'code': ("python",
  "for iteration in range(10):  # the cap is the discipline\n    diff = agent.propose_diff(task_spec, retrieved_files)\n    result = run_tests(repo)   # the project's own tests: the oracle\n    log(iteration, diff, result)\n    if result.green:\n        break\n    agent.read_failure(result.output)  # generate -> test -> read -> repeat\nelse:\n    escalate_to_human(task_spec)  # 10 misses means the spec or task is wrong"),
 'project': "Agent-driven fix. One real issue fixed via a coding agent, verified by the project's own tests plus one test you wrote yourself. Deliverables: the diff, the iteration log (all 10 or fewer), your review notes as a stranger, and the economics — iterations, time, and tokens if measurable.",
 'honest': "The agent didn't understand your code — it pattern-matched successfully. That distinction matters the day the pattern is wrong. Tests are the only trust in this module, and even tests only check what someone thought to assert. Ask yourself: what bug could this change hide that the suite wouldn't catch?",
}

MODULES['repo-scale-agents'] = {
 'sec2': 'Hands-on procedure',
 'procedure': [
  "Inventory the repo: count files and lines, identify the major modules — know what 'big' means here before retrieving anything.",
  "Build the index: chunk by file and symbol into a searchable index (even a grep-based index counts for the exercise — the concept is chunking plus lookup).",
  "Practice retrieval: take 5 real questions ('where is auth enforced?') and record which files retrieval returns versus the files you'd actually want — score the gap.",
  "Plan a multi-file change on paper first: every file touched and why — the change set exists before any edit.",
  "Apply the edits with the plan and cross-file references in view; for every renamed symbol, verify each call site was updated.",
  "Budget the context: log tokens (or files) per retrieval; set a per-task retrieval budget and practice saying 'enough'.",
  "Verify completeness: search the repo for the old symbol/API name after the refactor — zero hits is the acceptance criterion.",
 ],
 'code': ("python",
  "# The discipline, as code: plan first, then edit, then verify.\nchange_set = plan_refactor(task)          # files + reasons, before edits\nfor file, edit in agent.apply(change_set, retrieved_context):\n    apply_edit(file, edit)\nleftover = search_repo(old_symbol_name)   # every call site must be gone\nassert not leftover, f\"missed call sites: {leftover}\""),
 'project': "Repo-scale refactor. A real multi-file refactor — a rename, an API migration, or dead-code removal — executed via retrieval-guided agent edits. Deliverables: the written edit plan, the retrieval log (queries and what they returned), the final diff, and the verification search proving all call sites were updated.",
 'honest': "Retrieval is lossy — the file you needed most is the one the index ranked eleventh. Edit discipline (plan first, verify call sites) is the actual skill; the model is just the typist. Ask yourself: how would you know if the agent silently skipped a call site?",
}

MODULES['review-agents'] = {
 'sec2': 'Hands-on procedure',
 'procedure': [
  "Collect 5 real PRs from a repo you know; for each, write down what the human reviewers actually flagged — this is your ground truth.",
  "Run a review agent (or carefully simulate one) over the same PRs and collect every finding it produces.",
  "Score precision: which findings matched human flags, which were noise, and which real issues did the agent miss entirely?",
  "Tune: suppress the noisiest rule category, re-run, and measure precision again — this tune-and-measure loop is the triage discipline.",
  "Generate tests: have the agent write tests for one untested function, then review the assertions for meaning — coverage without meaningful assertions is theater.",
  "Write the gate policy: what the agent may comment on, what it may block, and where the human gate sits — one page, in writing, because the human gate never moves.",
 ],
 'code': ("python",
  "REVIEW_FINDING = {  # every finding the agent emits follows this schema\n    \"type\": \"object\",\n    \"properties\": {\n        \"file\": {\"type\": \"string\"},\n        \"line\": {\"type\": \"integer\"},\n        \"category\": {\"type\": \"string\"},   # style | convention | bug | missing-test\n        \"confidence\": {\"type\": \"string\", \"enum\": [\"high\", \"low\"]},\n        \"suggested_fix\": {\"type\": \"string\"},\n    },\n    \"required\": [\"file\", \"line\", \"category\", \"confidence\"],\n}\n# Policy: low-confidence findings comment only; nothing auto-blocks a merge."),
 'project': "Review bot trial. A compressed trial of review-agent assistance on real PRs, with precision measured and a written gate policy. Deliverables: the findings log with precision numbers (matched/noise/missed), the tuned rule set after one triage pass, and the one-page gate policy.",
 'honest': "A review agent optimizes for finding things, not for being right — precision is the metric that decides whether the team trusts it or mutes it. Coverage from generated tests can be theater. Ask yourself: would you merge on this agent's approval alone? (The answer must be no.)",
}

MODULES['dev-workflow-agents'] = {
 'sec2': 'Hands-on procedure',
 'procedure': [
  "Map your pipeline: list every stage (lint, test, build, deploy) and the permissions each stage's runner holds today — the blast-radius inventory.",
  "Size the blast radius for one agent step: define the smallest permission set it needs, then cut it once more — read-only first, always.",
  "Build the triage agent: classify 20 real issues (bug, feature, question, duplicate), draft reproductions for 3, and hand-score the classification accuracy.",
  "Generate release notes: draft from merged PR titles and diffs for one release; a human approves every line before anything ships — grounding plus approval.",
  "Add the docs check: an agent that flags code merged without doc updates — read-only and advisory only, never blocking.",
  "Draft the on-call assist: triage questions it may answer, runbook steps it may suggest, and the explicit rule that it never pages, acknowledges, or closes incidents itself.",
  "Write the rollback plan for the assist itself: how to disable the agent step in under five minutes if it misbehaves.",
 ],
 'code': ("yaml",
  "# An agent step in the pipeline: scoped like production, because it is.\n- name: agent-triage\n  permissions:\n    contents: read        # least privilege: read-only first\n    issues: write         # only to comment labels, never to close\n    actions: none\n  needs_approval_before: [\"label:needs-human\"]  # destructive acts wait"),
 'project': "One safe pipeline assist. Implement exactly one agent step in a real or realistic pipeline with least-privilege permissions, approvals on anything destructive, and full logging. Deliverables: the permission diff (before vs after), run logs from real pipeline executions, and the rollback plan for the assist itself.",
 'honest': "The pipeline is production — an agent step there has the blast radius of a deploy, not of a chatbot. Every permission you grant is a future incident's attack surface. Ask yourself: if this agent step went rogue at 3 AM, what is the worst it could do, and what stops it?",
}

MODULES['swe-agent-project'] = {
 'sec2': 'Hands-on procedure',
 'procedure': [
  "Choose the task: a real issue, bounded, with tests — and get it in writing (even from yourself) that the team would accept this fix.",
  "Freeze the task set: 5–10 task instances or variants with expected outcomes — this fixed benchmark is what every later number refers to.",
  "Build the loop: context retrieval, diff proposal, test execution, failure reading — instrumented end to end with a transcript.",
  "Run the benchmark: record attempts, green merges, and iterations per task — the raw numbers before any interpretation.",
  "Catalog the failures: every miss gets a row — bad context, wrong API, flaky test, unclear spec — with your diagnosis of the class.",
  "Fix one failure class: change the loop or the prompts, re-run the benchmark, and show the delta in the numbers — the engineering cycle.",
  "Write it up: success rate, failure catalog, limits — the honest report this track has been building toward.",
 ],
 'code': ("python",
  "benchmark = freeze_tasks(repo, n=8)   # fixed set, expected outcomes\nresults = []\nfor task in benchmark:\n    attempt = agent_loop(task, max_iterations=10)\n    results.append({\n        \"task\": task.id,\n        \"green\": attempt.tests_pass,       # the oracle\n        \"iterations\": attempt.iterations,\n        \"failure_class\": classify(attempt) if not attempt.tests_pass else None,\n    })\nsuccess_rate = sum(r[\"green\"] for r in results) / len(results)"),
 'project': "The SWE agent, measured. The full project — agent loop, frozen benchmark, numbers, failure catalog, honest write-up. Deliverables: the repo, the benchmark table (attempts vs green merges), the failure catalog with your diagnoses, and the write-up with limits. This is the portfolio centerpiece of the SWE track.",
 'honest': "Your success rate describes your benchmark, not coding agents in general — resist the urge to generalize from 8 tasks. The failure catalog is the valuable artifact; anyone can show a green run. Ask yourself: which failure class would be most expensive in production?",
}

MODULES['swe-agent-limits'] = {
 'sec2': 'Hands-on procedure',
 'procedure': [
  "Collect 3 agent-generated diffs (or write representative ones); treat every API call in them as suspect until verified.",
  "Verify references: for each function, flag, and import in the diffs, confirm it exists in the actual codebase or dependency tree — log every hallucination you find.",
  "Registry check: for each dependency a diff introduces, verify it exists in the package registry and pin the version you actually checked — invented packages look real.",
  "Security pass: walk the diff against a checklist — injection points, auth checks, secret handling, and error messages that leak internals.",
  "Secrets scan: search the diff for tokens, keys, and credential-shaped strings; verify none, and note where the agent was one prompt away from emitting one.",
  "License review: assess the provenance risk — generated code with murky training-data origins — against your team's policy for what may enter the codebase.",
  "Draft the team policy: allowed tools, review requirements, secret handling, and the no-auto-merge rule — one page, in writing, not tribal knowledge.",
 ],
 'code': ("python",
  "import ast\n\ndef verify_api_refs(diff_source, known_symbols):\n    \"\"\"Every name the generated code touches must exist somewhere real.\"\"\"\n    tree = ast.parse(diff_source)\n    used = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}\n    hallucinations = used - known_symbols - set(dir(__builtins__))\n    return hallucinations  # non-empty = invented APIs: investigate each"),
 'project': "Silent-failure audit. A full audit of agent-generated code against this module's checklist, ending in a written team policy. Deliverables: the audit log (hallucinations found, security findings, secrets-scan result) and the one-page team policy covering tools, review, secrets, and no-auto-merge.",
 'honest': "No checklist catches everything — the most dangerous failures are the ones that look idiomatic and pass tests. Policy only works if the team follows it when the deadline is tight. Ask yourself: what would make you skip the review on a Friday afternoon, and how does the policy survive that?",
}

# ---------------- agentic-ai-for-data ----------------
MODULES['data-agents-core'] = {
 'sec2': 'Hands-on procedure',
 'procedure': [
  "Pick a real schema you know (even 3 tables); write down the tables, keys, and one tricky join — the ground truth the agent must respect.",
  "Build the schema briefing: the context block the agent receives — table and column descriptions in plain language, not just DDL, including the ambiguous column pairs.",
  "Implement the ask-before-running gate: classify questions into 'safe to run' (read-only, bounded, unambiguous) vs 'ask first' (ambiguous, expensive, or touching sensitive columns) — write the rules down.",
  "Run 10 questions: log each generated query, whether the gate fired, and whether the question was actually answerable from the schema.",
  "Practice the honest 'I don't know': craft 3 questions the data cannot answer and verify the agent declines instead of inventing rows.",
  "Interpret results: for each answer, write the one-sentence caveat a data engineer would add — grain, filters, freshness.",
  "Review the gate log: which 'ask first' cases were right, which were over-cautious, and what rule change each suggests.",
 ],
 'code': ("python",
  "def ask_gate(question, schema):\n    \"\"\"Decide: run it, or ask the human first.\"\"\"\n    if touches_sensitive_columns(question, schema):\n        return \"ask\"      # PII or restricted: human decides\n    if is_ambiguous(question, schema):\n        return \"ask\"      # invented rows are worse than slow answers\n    if estimated_cost(question) > QUERY_BUDGET:\n        return \"ask\"      # expensive: confirm before billing\n    return \"run\"          # read-only, bounded, unambiguous"),
 'project': "Read-first data agent. A question-answering agent over a real schema with a schema briefing, an ask-before-running gate, and honest-decline behavior. Deliverables: the schema briefing doc, a 15-question run log with gate decisions, and the caveats list — one per answer.",
 'honest': "The agent doesn't understand your business — it pattern-matches column names. Every answer needs the caveat you'd add yourself. The honest 'I don't know' is the feature; everything else is plumbing. Ask yourself: which question would this agent answer confidently and wrong?",
}

MODULES['pipeline-agents'] = {
 'sec2': 'Hands-on procedure',
 'procedure': [
  "Choose a small real pipeline (or a realistic sketch): source, transform, load — with a DAG you can draw on one page.",
  "Generate the DAG: have the agent scaffold the pipeline definition from your description, then diff it against the hand-written version line by line.",
  "Inject schema drift: add a column upstream and rename another; run the agent's drift handler and check whether it detected, alerted, and adapted — or silently broke.",
  "Plan a backfill: pick a date range, compute the partitions affected, and have the agent produce the backfill plan with idempotency stated explicitly.",
  "Scaffold tests: generate one test per pipeline stage — row counts, schema checks, a business-rule assertion — run them, and fix the ones that assert the wrong thing.",
  "Wire the orchestrator: define where the agent's outputs land (pull requests, not direct commits) and who approves them.",
  "Run the 3 AM test: read the generated pipeline as the on-call engineer — is everything you'd need at 3 AM written down?",
 ],
 'code': ("python",
  "def handle_schema_drift(detected_columns, expected_schema):\n    new_cols = detected_columns - expected_schema\n    missing = expected_schema - detected_columns\n    if new_cols or missing:\n        alert_human(f\"drift detected: +{new_cols} -{missing}\")  # alert first\n        return propose_mapping(new_cols, missing)  # adapt only under a test gate\n    return None  # no drift: the common, boring, good case"),
 'project': "Agent-assisted pipeline. One pipeline with an agent-scaffolded DAG, drift handling, and generated tests — all landing via pull request. Deliverables: the DAG diff (agent vs hand-written), the drift-injection log, the test results, and the approval workflow doc.",
 'honest': "Generated pipelines fail at 3 AM like everyone else's — the agent doesn't get a reliability discount. Drift handling that silently adapts is a data-corruption vector; alerting is the point. Ask yourself: what would the on-call engineer need to know at 3 AM that the agent didn't write down?",
}

MODULES['text-to-sql-agents'] = {
 'sec2': 'Hands-on procedure',
 'procedure': [
  "Fix the schema: 3–5 tables with realistic names, keys, and one deliberately ambiguous column pair (for example `created_at` vs `registered_at`).",
  "Build the schema-linking step: for 10 questions, write by hand which tables and columns each needs — then check what the agent links and score the gap.",
  "Add dialect awareness: pick your warehouse dialect, list 3 functions that differ from standard SQL, and test whether generated queries respect them.",
  "Validate before execution: syntax check first, then EXPLAIN — read the plan for full scans and runaway joins before anything runs.",
  "Set the guardrails as a stack, not one trick: a read-only role, a statement timeout, and a hard block on writes and deletes without human approval — implement all three.",
  "Evaluate: 15 realistic questions with known-correct answers; score exact-match and 'correct result' separately — they measure different things.",
  "Diagnose 3 failures in writing: wrong table, wrong join, or wrong filter — and which pipeline stage should have caught each.",
 ],
 'code': ("python",
  "def guarded_execute(nl_question):\n    query = generate_sql(nl_question)          # schema-linked generation\n    check_syntax(query)                        # parse before anything else\n    plan = explain(query)                      # read the plan: scans? joins?\n    assert is_read_only(query), \"writes need human approval\"\n    assert plan.estimated_cost < QUERY_BUDGET\n    return run_with_timeout(query, TIMEOUT_S)  # the last guardrail"),
 'project': "Guardrailed text-to-SQL. The full pipeline — schema linking, validation, EXPLAIN review, guardrails — evaluated on 15 questions. Deliverables: the eval table (exact-match vs correct-result scores), the guardrail configuration, and 3 failure cases with written diagnoses.",
 'honest': "Text-to-SQL is evaluated on your questions, not the user's — real users ask ambiguous, unanswerable, adversarial things. EXPLAIN plans catch cost, not correctness. Ask yourself: what is the most expensive wrong query this agent could run, and what stops it?",
}

MODULES['data-quality-agents'] = {
 'sec2': 'Hands-on procedure',
 'procedure': [
  "Pick 2 tables you know; define 'healthy' for each: freshness SLA, expected row-count range, and the key columns that must never be null.",
  "Implement freshness and completeness checks first: scheduled queries that alert when the SLA breaks — start with the dumb thresholds before anything 'smart'.",
  "Add anomaly detection: a simple statistical check (z-score on row counts, null-rate spikes) on one metric; tune until the alert rate is livable.",
  "Write contract tests: the schema and semantics downstream expects — run them on every load and fail fast on breakage.",
  "Build the triage agent: given an alert, it gathers context (recent deploys, upstream freshness, similar past alerts) and drafts the triage note — a human still decides severity.",
  "Dashboard it: one page showing check status over time — the agent's job is to keep it green and honest, not green at all costs.",
  "Tune for a week (or simulate one): log every alert as real breakage or noise, and adjust thresholds until the team would trust the page.",
 ],
 'code': ("python",
  "def contract_test(table, expected):\n    \"\"\"Fail fast when upstream breaks the shape downstream expects.\"\"\"\n    assert set(table.columns) >= set(expected[\"required_columns\"])\n    assert table[expected[\"key\"]].is_unique, \"key uniqueness violated\"\n    assert table[expected[\"not_null\"]].notnull().all().all()\n    assert expected[\"row_range\"][0] <= len(table) <= expected[\"row_range\"][1]\n    return \"contract holds\""),
 'project': "Night-watch quality agent. Freshness, completeness, and anomaly checks, contract tests, and triage assistance for real (or realistic) tables. Deliverables: the check definitions, two weeks (or simulated) of alert history with triage notes, and the precision story — real breakage versus noise.",
 'honest': "Every quality check is a future false alarm — the tuning never ends, and alert fatigue kills more pipelines than bad data. An agent that cries wolf gets its alerts ignored, exactly like a human would. Ask yourself: which of your checks will be the first one the team stops believing?",
}

MODULES['data-agent-project'] = {
 'sec2': 'Hands-on procedure',
 'procedure': [
  "Choose the dataset: real tables and real questions from real users — write down 20 questions before building anything.",
  "Decide the agent type: text-to-SQL or quality agent — pick the one whose failure mode you can bound, not the flashier one.",
  "Implement read-only guardrails first: role, timeouts, approval gates for anything beyond reads — before the agent answers its first question.",
  "Build the question set: 20 questions with known-correct answers, including 5 unanswerable ones the agent must decline.",
  "Evaluate: accuracy on answerables, decline rate on unanswerables, and the cost and guardrail log for every query.",
  "Document limits: the questions it can't handle, the schema corners it misunderstands, the failure you saw twice — as a first-class deliverable.",
  "Write it up: numbers, guardrails demonstrated, failures — the honest report that closes the data track.",
 ],
 'code': ("python",
  "question_set = load_questions(n=20, include_unanswerable=5)\nfor q in question_set:\n    with guardrails(read_only=True, timeout_s=30):\n        answer = data_agent.ask(q.text)\n    log({\n        \"q\": q.id, \"answered\": answer is not None,\n        \"correct\": answer == q.expected,          # only for answerables\n        \"declined_correctly\": (answer is None) == (not q.answerable),\n        \"cost\": answer.cost if answer else 0,\n    })"),
 'project': "The data agent, shipped honestly. The complete project — agent, guardrails, 20-question eval, limits doc. Deliverables: the repo, the eval table (accuracy, decline rate, cost per query), the guardrail demonstration log, and the write-up. The data track's portfolio piece.",
 'honest': "Your 20 questions are not your users' questions — the eval measures the demo, not production. Read-only guardrails are the difference between a bad answer and an incident. Ask yourself: what happens the first time a user asks something your eval never covered?",
}

MODULES['data-agent-trust'] = {
 'sec2': 'Worked estimation',
 'estimation': "Work the cost-cap math for a data agent, with your own numbers. Suppose the agent averages 8 tool calls per question — schema lookup, query generation, validation, execution, interpretation (count them from your own runs; this is illustrative). Call one model interaction's cost u. Then one question costs about 8u, and 1,000 questions a day costs about 8,000u a day. Now apply the guardrails as math. (1) A per-query step budget of 12 bounds the worst single question at 12u instead of an unbounded loop — compute your own worst case: budget times u. (2) A daily spend cap C means the agent stops answering after C/u questions — set C from what the answers are worth, not from vibes: if each answered question saves roughly 10 minutes of analyst time, price that time and set C below it. (3) The EXPLAIN-first rule converts 'runaway query' from a warehouse-bill event into a rejected plan — estimate one bad full scan a week without it, and price the scan from your warehouse's billing model. Fill in u from your provider's pricing (as of October 2026 — verify it, don't trust this page), your daily question volume, and your per-question value. The output is a one-page cost policy: per-query budget, daily cap, and the approval threshold above which a human reviews the plan. The estimation habit is the point — every assumption labeled, every number replaceable.",
 'project': "Trust-layer proposal. A written trust layer for a data agent — read-only defaults, cost caps from your estimation, PII handling rules, the audit-log schema, and the human-approval workflow for writes. Deliverables: the one-page cost policy, the audit-log schema, and the approval workflow doc — reviewed as if legal will read it.",
 'honest': "Guardrails don't make the agent trustworthy — they make its failures bounded and visible. PII handling is the one you can't estimate your way out of: know your data classification before the agent touches the warehouse. Ask yourself: which guardrail would you disable first under deadline pressure, and what breaks then?",
 'quiz_sec': 'the Worked estimation',
}

# ---------------- agentic-ai-for-pm ----------------
MODULES['pm-agent-literacy'] = {
 'sec2': 'Worked estimation',
 'estimation': "Price one real agent feature pitch you've heard, with your own numbers. Suppose a support agent would handle 500 conversations a day (illustrative — use your own volume), averaging 6 tool calls per conversation (lookup, policy check, draft, verify, and so on). If one model interaction costs roughly u, the daily model cost is about 3,000u. Now compare: a human-handled conversation costs H. Breakeven needs (3,000u + build + evals + on-call) to be less than (conversations × H × automation_fraction) — and automation_fraction is measured, never assumed; start it at the pilot's measured number, not the demo's. Latency: if each step takes about 2 seconds (model plus tool), a 6-step conversation is about 12 seconds of pure machine time before queueing — map that against your SLA. If the SLA is 30 seconds, 18 seconds of budget remain for everything else; write down what consumes it. Evals: a 200-question golden set, each needing a human-verified answer — estimate the hours to build it (5–10 minutes per question is typical) and price that before promising a launch date. The deliverable is a one-page capability note — what the demo implies versus what production requires — with every assumption labeled. As of October 2026 model pricing moves; verify current numbers, don't memorize them.",
 'project': "Capability note. A one-page honest capability assessment of a real agent feature pitch — measured success rate (or the plan to measure it), cost and latency estimation, eval plan, and the four shippability questions answered. Deliverables: the note, written as if the CTO will read it.",
 'honest': "Demos are adversarial — they show the path that works. Your job as PM is to price the paths that don't. No estimation here survives contact with real users unchanged; the habit of labeling assumptions is what survives. Ask yourself: what would make you kill this feature after the pilot?",
 'quiz_sec': 'the Worked estimation',
}

MODULES['pm-spec-agents'] = {
 'sec2': 'Hands-on procedure',
 'procedure': [
  "Pick a real feature (or a realistic one) and write the five-line version of what it does — the anchor everything else refers back to.",
  "Draft with the agent: generate a PRD skeleton — problem, users, requirements, acceptance criteria — then mark every line as yours, the agent's, or joint.",
  "Generate acceptance criteria: for each requirement, produce testable criteria — then delete every criterion you couldn't actually test.",
  "Run the spec review agent: feed it the draft and collect its flags — missing edge cases, ambiguous terms, untestable claims.",
  "Triage the flags: which were real gaps and which were noise? Keep score — the review-precision habit from the SWE track, applied to prose.",
  "Version it: commit the spec, make one scope change, and diff — practice treating specs as versioned artifacts, not documents.",
  "Decide: mark the sections that still need a human — trade-offs, ethics, the actual decision. The agent proposes; you dispose.",
 ],
 'code': ("python",
  "SPEC_REVIEW_PROMPT = \"\"\"Review this spec draft. For each issue found, emit:\n- location: the section and line\n- category: missing-edge-case | ambiguous-term | untestable-claim | scope-creep\n- severity: blocker | major | minor\n- question: the single question that would resolve it\nDo not rewrite the spec. Do not make product decisions. Flag only.\"\"\n# The agent proposes; the human disposes."),
 'project': "Agent-assisted PRD. A complete PRD drafted and reviewed with agent assistance, with the human-decision sections marked. Deliverables: the PRD (with provenance marks on every line), the review-flag triage log with precision scores, and the version history showing one real scope change.",
 'honest': "An agent can draft a spec that reads perfectly and decides nothing — fluency is not judgment. The decision is the PM's job and can't be delegated to a draft. Ask yourself: which sentence in this PRD is the actual decision, and did you write it?",
}

MODULES['pm-research-agents'] = {
 'sec2': 'Hands-on procedure',
 'procedure': [
  "Define the research question narrowly — one question the business decision actually hinges on, not a fishing expedition.",
  "Run the agent over 5 or more sources; collect every factual claim it makes into a numbered list — claims, not vibes.",
  "Verify each claim: open the cited source and confirm the claim is really there — mark each verified, unverified, or contradicted.",
  "Score the citation discipline: what fraction of claims were verifiable from the cited source? Write the number down — it is the module's key metric.",
  "Synthesize the long sources into a one-page brief, with every paragraph traceable to numbered claims.",
  "Summarize user feedback: feed in 20 real (or realistic) feedback items, then check the summary against 5 items by hand for faithfulness.",
  "Write the ethics note: what data the agent touched, what it must not retain, and where the brief's limits are stated.",
 ],
 'code': ("python",
  "claims = extract_numbered_claims(agent_report)  # every factual claim, numbered\nfor c in claims:\n    source_text = open_source(c.citation)\n    c.verdict = verify(c.text, source_text)  # verified | unverified | contradicted\nprecision = sum(c.verdict == \"verified\" for c in claims) / len(claims)\nprint(f\"citation precision: {precision:.0%} over {len(claims)} claims\")"),
 'project': "Verified research brief. A one-page brief on a real question, with numbered claims, a verification log, and an ethics note. Deliverables: the brief, the claim-by-claim verification table, and the citation-precision number.",
 'honest': "An unverified agent finding is a rumor with formatting — and formatted rumors travel faster than true ones. Verification is the whole job; the synthesis is the easy part. Ask yourself: which claim in your brief would embarrass you if it were wrong?",
}

MODULES['pm-agent-playbook'] = {
 'sec2': 'Hands-on procedure',
 'procedure': [
  "Pick the workflow: real, frequent, and currently painful — write down how often it happens and what it costs today in time, errors, and delay.",
  "Design the assist: what the agent does, what stays human, and the exact handoff between them — draw it on one page.",
  "Define success metrics before building: the primary metric, the guardrail metrics, and the decision rule (expand, iterate, or stop) with numbers attached.",
  "Prototype: low-code if the workflow is standard, API if it isn't — time-box the build to days, not weeks.",
  "Pilot with a small group: 5–10 users for 2–4 weeks; log every failure and every workaround users invent — workarounds are data.",
  "Decide with the numbers: run the decision rule you wrote in step 3 — honor it even if the answer is 'stop'.",
  "Write it up: metric deltas, guardrail compliance, the decision, and what you'd change next time.",
 ],
 'code': ("python",
  "PILOT_SCORECARD = {\n    \"primary_metric\": {\"name\": \"\", \"baseline\": None, \"pilot\": None},\n    \"guardrails\": [{\"name\": \"\", \"threshold\": \"\", \"observed\": \"\"}],\n    \"decision_rule\": \"expand if primary improves >= X% AND all guardrails hold; \"\n                     \"iterate if primary improves < X%; stop if any guardrail breached\",\n    \"decision\": None,  # filled after the pilot, never before\n}\n# The rule is written before the data exists. That ordering is the discipline."),
 'project': "Measured pilot. The complete playbook run — workflow, assist design, metrics, prototype, pilot, decision. Deliverables: the design doc, the pilot data log, and the expand/iterate/stop decision with numbers attached.",
 'honest': "The pilot's job is to produce evidence, not to succeed — a clean 'stop' is a successful pilot. Moving the goalposts after the numbers come in is the failure mode. Ask yourself: did you write the decision rule before you saw the data?",
}

MODULES['pm-agent-metrics'] = {
 'sec2': 'Worked estimation',
 'estimation': "Work the measurement for one agent pilot — use the playbook module's pilot or a realistic one: 8 users, 3 weeks, 240 assisted tasks (illustrative). Step 1, primary metric: suppose the task took 25 minutes manually and 9 minutes assisted (measure both — don't guess). Time saved per task: 16 minutes; total: 240 × 16 = 3,840 minutes, about 64 hours. Step 2, price it honestly: 64 hours at a loaded cost you can defend, minus the pilot's build cost and the agent's run cost (model plus tools plus your time babysitting it). If the net isn't clearly positive, the pilot didn't pay — write that down. Step 3, quality delta: define it before measuring (error rate? rework rate? customer satisfaction?) and measure it the same way for assisted and unassisted work. Step 4, counter-metrics: pick two things the headline could hide (tasks the agent silently skipped; users who quietly stopped using it) and measure those too. Step 5, guardrail metrics: escalation rate, failure rate, cost per task — set the thresholds that would trigger a rollback, in writing, before launch. Work this with your own pilot numbers; the output is the metrics section of a launch doc, with every assumption labeled and the rollback thresholds explicit.",
 'project': "Launch metrics doc. The full metrics section for an agent feature — primary, guardrail, and counter-metrics with rollback thresholds. Deliverables: the doc, written as the page the launch review will actually argue about.",
 'honest': "Metrics are chosen, not found — the metric you pick decides what the team optimizes. Vanity metrics (tasks merely 'touched' by the agent) are the default failure. Ask yourself: which number in your doc would you least want the CEO to ask about?",
 'quiz_sec': 'the Worked estimation',
}

MODULES['pm-agent-roadmap'] = {
 'sec2': 'Worked estimation',
 'estimation': "Do the roadmap math for one agentic feature, honestly. Suppose v1 targets 3 workflows, each needing about 2 weeks of build (your team's velocity, not a vendor's), a 100-question golden eval set per workflow (8–17 hours of human verification each at 5–10 minutes per question — price it), and a 4-week pilot. That's roughly 6 build-weeks plus about 50 eval-hours plus pilot time before you know if any of it works — write your own numbers in. Build-vs-buy: list what you'd buy (orchestration, eval tooling, hosting) versus build (the workflow logic, the evals, the guardrails) and price both over 12 months, including the maintenance nobody puts in the demo. Cost modeling: per-task model cost times projected volume, plus the eval-maintenance cost as the product changes (evals rot — budget to refresh them quarterly). Sequencing: order the 3 workflows by low-risk times high-frequency times measurability, and show why the ambitious one goes last. The output is a one-page roadmap with costs, the sequencing rationale, and the explicit v1 non-goals — what v1 will not do, in writing, agreed with stakeholders.",
 'project': "Honest roadmap. A one-page roadmap for a real agentic feature — sequencing, build-vs-buy, cost model, v1 non-goals. Deliverables: the roadmap doc, with the non-goals section signed off (even if only by you, practicing the conversation).",
 'honest': "Roadmaps are promises with dates — the honest ones list what won't ship. 'AI' on a roadmap without evals, guardrails, and a cost model is a wish. Ask yourself: what is the first thing you'd cut if the quarter went sideways, and is it written down?",
 'quiz_sec': 'the Worked estimation',
}

# ---------------- agentic-ai-for-leaders ----------------
MODULES['program-agents'] = {
 'sec2': 'Hands-on procedure',
 'procedure': [
  "Pick a real program (or a realistic one): 3 or more teams, a deadline, and status scattered across tools — the mess roll-ups are supposed to tame.",
  "Define the roll-up contract: what each team reports, in what format, and what 'red' means — the schema the agent will consume, agreed before automation.",
  "Build the synthesis: feed 3 weeks of (realistic) status updates to the agent, produce the one-page roll-up, and compare it against the roll-up you'd write by hand.",
  "Hunt the mislead: find 2 places where the agent's roll-up smoothed over a real risk — write down the smoothing pattern (averaging, hedging language, missing context).",
  "Design the risk-signal detector: which signals (slipping dates, growing bug counts, quiet channels) trigger a human look — thresholds in writing.",
  "Build the meeting-notes agent: extract decisions, owners, and dates from one real meeting's notes; verify each extraction against the actual meeting.",
  "Write the accountability page: what the agent reports, who owns each deadline, and the sentence 'the agent cannot own a deadline' — into the team handbook.",
 ],
 'code': ("python",
  "ROLLUP_SCHEMA = {\n    \"type\": \"object\",\n    \"properties\": {\n        \"team\": {\"type\": \"string\"},\n        \"status\": {\"type\": \"string\", \"enum\": [\"green\", \"amber\", \"red\"]},\n        \"top_risks\": {\"type\": \"array\", \"items\": {\"type\": \"string\"}},\n        \"date_confidence\": {\"type\": \"string\", \"enum\": [\"high\", \"medium\", \"low\"]},\n        \"owner\": {\"type\": \"string\"},   # a human name: accountability stays human\n    },\n    \"required\": [\"team\", \"status\", \"top_risks\", \"owner\"],\n}"),
 'project': "Program roll-up agent. A working roll-up workflow with risk signals and the accountability page. Deliverables: the roll-up template, 3 weeks of agent roll-ups with your hand-written comparison, the mislead log (smoothing patterns found), and the accountability doc.",
 'honest': "Roll-ups are lossy by design — the agent optimizes for coherent narrative, and coherence hides risk. If leadership acts on the roll-up, the smoothing patterns are safety issues, not style issues. Ask yourself: what risk would this roll-up hide from you?",
}

MODULES['eng-mgmt-agents'] = {
 'sec2': 'Hands-on procedure',
 'procedure': [
  "List the management tasks you'd delegate: onboarding questions, review load, 1:1 prep, knowledge lookup — and mark which ones touch people data.",
  "Build the onboarding assistant: grounded in your real docs (README, runbooks, architecture notes); test it with 10 questions a new hire actually asked, and check every answer.",
  "Design review-load balancing: the agent suggests reviewers by expertise and current load — a human still makes the assignment.",
  "Draft the 1:1 prep: the agent summarizes public work signals (merged PRs, docs written) — never private messages, never sentiment analysis of people.",
  "Draw the privacy boundary: what people data the agent may never touch — written as a policy with concrete examples, not vibes.",
  "Measure team-health signals honestly: pick 2 signals (for example review turnaround, doc freshness), define them precisely, and note what they cannot see.",
  "Write the policy: allowed assists, the people-data boundary, and the review cadence for the policy itself — because policies rot too.",
 ],
 'code': ("python",
  "PEOPLE_DATA_BOUNDARY = [\n    \"never: private messages, DMs, or email content\",\n    \"never: sentiment or performance inference about individuals\",\n    \"never: 1:1 notes or HR-adjacent documents\",\n    \"allowed: public work artifacts (merged PRs, docs, public channels)\",\n    \"allowed: aggregate, anonymized team signals with opt-out\",\n]\n# If an assist needs an exception to this list, it needs a new policy, not a shortcut."),
 'project': "Management assist kit. An onboarding assistant, a review-load suggester, and a 1:1 prep draft — with the privacy policy. Deliverables: the three assists, the privacy-boundary policy with examples, and the test log (10 onboarding questions with answers checked).",
 'honest': "Team trust is not a metric to optimize — the moment the team feels surveilled, every assist becomes a liability. People-data boundaries are load-bearing; 'just this once' is how they fall. Ask yourself: would you be comfortable if the team read the agent's full logs?",
}

MODULES['incident-agents'] = {
 'sec2': 'Hands-on procedure',
 'procedure': [
  "Pick a past incident you know well; write the timeline as it actually happened — this is your ground truth for everything that follows.",
  "Build the triage assistant: given alerts, it suggests severity and the likely runbook — test it against 5 historical alerts and score it by hand.",
  "Encode one runbook: the diagnostic steps as a checklist the agent walks through, with explicit 'stop and escalate' conditions at the risky steps.",
  "Reconstruct the timeline: feed the agent the incident's raw signals (alerts, deploys, messages) and compare its timeline against your ground truth.",
  "Draft the postmortem: the agent drafts, a human owns — mark every line the human changed and why, so the ownership is visible.",
  "Write the paging policy: what the agent may do during an incident (suggest, draft, summarize) and may never do (page, acknowledge, close, declare all-clear).",
  "Run the drill: a tabletop where the agent assists and a human commands — debrief what the agent got wrong under time pressure.",
 ],
 'code': ("python",
  "RUNBOOK_STEP = {\n    \"type\": \"object\",\n    \"properties\": {\n        \"step\": {\"type\": \"string\"},\n        \"check\": {\"type\": \"string\"},          # the diagnostic to run\n        \"escalate_if\": {\"type\": \"string\"},    # stop-and-escalate condition\n        \"never_do\": {\"type\": \"array\", \"items\": {\"type\": \"string\"}},\n    },\n    \"required\": [\"step\", \"check\", \"escalate_if\"],\n}\n# The human commander stays in charge: the agent follows runbooks and drafts;\n# it does not decide."),
 'project': "Incident assist drill. The triage assistant, one encoded runbook, and a tabletop drill debrief. Deliverables: the triage accuracy log (5 historical alerts), the runbook encoding, the drill debrief, and the written paging policy.",
 'honest': "Under incident pressure, a confident wrong suggestion costs more than silence — the agent doesn't feel the pressure, but you do. The human-commander rule isn't bureaucracy; it's what keeps a bad suggestion from becoming a bad action. Ask yourself: in your drill, what did the agent suggest that a tired human might have just done?",
}

MODULES['rollout-playbook'] = {
 'sec2': 'Hands-on procedure',
 'procedure': [
  "Choose the workflow: one team workflow, real users, measurable today — write the baseline numbers before anything else exists.",
  "Design the assist: scope it to the smallest useful thing; write down what it won't do — the non-goals are part of the design.",
  "Define guardrails and approvals: what needs a human sign-off, what the agent may never touch, and the kill switch — with a named owner.",
  "Set pilot metrics: primary, guardrail, and the expand-or-stop thresholds — in writing, before the pilot starts.",
  "Run the pilot: 2–4 weeks with real users; log every incident, workaround, and surprise — surprises are the most valuable data.",
  "Make the call: expand, iterate, or stop — using the thresholds from step 4, with the numbers attached to the decision.",
  "Write it up: the decision memo a director could act on — what you did, what the numbers said, what happens next.",
 ],
 'code': ("python",
  "ROLLOUT_DECISION = {\n    \"workflow\": \"\",\n    \"baseline\": {},          # measured before the pilot\n    \"guardrails\": [],        # each with threshold + named owner\n    \"kill_switch\": \"\",       # how to stop it in under five minutes\n    \"thresholds\": {\"expand\": \"\", \"iterate\": \"\", \"stop\": \"\"},\n    \"pilot_data\": {},        # filled during the pilot\n    \"decision\": None,        # expand | iterate | stop — with numbers attached\n    \"decider\": \"\",           # a human name: who can stop this rollout\n}"),
 'project': "Rollout decision memo. The complete playbook for one workflow, ending in a real expand-or-stop call. Deliverables: the assist design with non-goals, the guardrails and kill switch, the pilot data, and the decision memo.",
 'honest': "Most pilots should end in 'stop' or 'iterate' — if yours always says 'expand', your thresholds were theater. The kill switch only works if someone is willing to pull it. Ask yourself: who, by name, can stop this rollout, and do they know it?",
}

MODULES['leader-agent-governance'] = {
 'sec2': 'Hands-on procedure',
 'procedure': [
  "Inventory the agent's identity: every agent gets a named identity with a human owner — list yours, no anonymous agents.",
  "Map data classification: for each data store the agent touches, write its classification and whether the agent's access matches it — mismatches get fixed or the access gets cut.",
  "Define the audit trail: every agent action logs which agent identity, what action, on whose behalf, and when — write the schema before you need it.",
  "Assess vendor and model risk: for each vendor dependency, note what happens if it changes pricing, terms, or availability (as of October 2026 — verify current terms, don't trust memory).",
  "Write the policy: access controls, classification alignment, logging, and the approval chain for new agent capabilities — one document, in writing.",
  "Set compliance checkpoints: the gates (security review, legal review, data review) an agent passes before touching production data — each with a named owner.",
  "Schedule the review: governance rots — put the policy's next review date in writing now.",
 ],
 'code': ("python",
  "AUDIT_LOG_SCHEMA = {\n    \"type\": \"object\",\n    \"properties\": {\n        \"timestamp\": {\"type\": \"string\"},\n        \"agent_identity\": {\"type\": \"string\"},  # named identity, human owner\n        \"on_behalf_of\": {\"type\": \"string\"},   # whose request triggered this\n        \"action\": {\"type\": \"string\"},\n        \"data_classification\": {\"type\": \"string\"},\n        \"outcome\": {\"type\": \"string\"},\n    },\n    \"required\": [\"timestamp\", \"agent_identity\", \"action\", \"outcome\"],\n}\n# 'Who asked what, when' — for debugging, cost attribution, and compliance."),
 'project': "Governance packet. The complete governance layer for one agent — named identity, classification map, audit schema, policy, checkpoints. Deliverables: the packet, written as if auditors will read it (they might).",
 'honest': "Governance nobody enforces is documentation, not control — the audit trail only matters if someone reads it. Vendor risk is the clause everyone skips until the pricing email arrives. Ask yourself: when did someone last actually review these logs?",
}

MODULES['leader-agent-metrics'] = {
 'sec2': 'Worked estimation',
 'estimation': "Work the honest measurement for one agent pilot — 200 tasks (illustrative; use your real count). Step 1, baseline: time 20 tasks done the old way (note the mean and the variance — say 30 minutes), then time 20 assisted (say 12 minutes). Time saved per task: 18 minutes; over 200 tasks that's about 60 hours. Step 2, cost per assisted task: model cost plus tool cost plus the human time still in the loop (review, corrections, escalations) — add the babysitting; everyone forgets the babysitting. Step 3, quality delta: pick the metric that matters (defect rate? rework rate? customer complaints?) and measure it the same way for assisted and unassisted work — a 60-hour saving with double the defect rate is not a saving. Step 4, adoption: what fraction of the team actually used it by week 4, and what did the non-adopters say? An unused agent saves nothing. Step 5, counter-metrics: two numbers that would embarrass the headline (tasks quietly reverted; escalations the agent caused) — measure them. Step 6, the report: one page for leadership with the net (savings minus all costs), the quality delta, adoption, and the counter-metrics — numbers you'd defend in a budget review. Label every assumption; the estimation is only as honest as its inputs.",
 'project': "Impact report. The one-page leadership report for a real or realistic pilot — net savings, quality delta, adoption, counter-metrics. Deliverables: the report, plus the raw measurement log it rests on.",
 'honest': "Time-saved without a baseline is marketing — and baselines are annoying to collect, which is why most teams skip them. The counter-metrics are the credibility; a report without them is a pitch. Ask yourself: what would you have to believe for these numbers to be wrong?",
 'quiz_sec': 'the Worked estimation',
}

# ---------------- agentic-ai-for-iv ----------------
MODULES['agent-system-design'] = {
 'sec2': 'Worked estimation',
 'estimation': "Estimate the system you'd whiteboard — bring numbers, not just boxes. Suppose the brief: a research assistant over 10,000 internal docs, 200 questions a day (illustrative — use the interview's numbers). Step 1, retrieval budget: if each question fans out to 20 candidate chunks and reranks to 5, that's 25 embedding operations per question × 200 = 5,000 embeddings a day — price them (verify current pricing as of October 2026). Step 2, generation cost: 5 chunks at roughly 500 tokens of context plus instructions is about 3,500 input tokens per question; × 200 questions = 700K input tokens a day. Step 3, latency: retrieval (~1s) + rerank (~1s) + generation (~5–10s) ≈ under 15 seconds per question if nothing queues — write your SLA next to it and see whether it fits. Step 4, eval budget: a 100-question golden set with human-verified answers and citations — 8–17 hours of expert time to build; price it and put it on the plan before the architecture diagram. Step 5, trade-off narration: for each choice (hybrid vs vector-only retrieval, citations vs no citations, the escalation threshold), write the one-line cost of being wrong. The output is the estimation page you'd bring to the whiteboard — numbers first, boxes second.",
 'project': "Whiteboard with numbers. A full system-design practice round — scope, tools, memory, evals — with the estimation page attached. Deliverables: the design narrative (recorded or written), the estimation page, and the trade-off list you'd narrate before being asked.",
 'honest': "Interviewers can tell when the numbers are invented — 'it depends' with a worked example beats a confident fiction. The estimation habit is what they're actually testing: can you reason about cost, latency, and evals, not just draw boxes. Ask yourself: which of your numbers would you defend, and which would you re-derive live?",
 'quiz_sec': 'the Worked estimation',
}

MODULES['llm-depth-iv'] = {
 'sec2': 'Worked estimation',
 'estimation': "Build interview-depth intuition with numbers, not papers. Attention intuition: attention compares every token pair in the sequence — work out what n=4,000 tokens means in pairwise operations (16 million — now you feel why long context is expensive). Training vs inference: training pays once to learn the weights; inference pays per token, forever — estimate which dominates for a model serving a million requests a day (illustrative: if training cost T and each request costs r, inference passes training at T/r requests — do the division with numbers you verify as of October 2026). Fine-tune vs RAG: fine-tuning costs data curation plus training plus the risk of stale knowledge; RAG costs retrieval infra plus per-query context tokens — write the breakeven in terms of how often the knowledge changes. Context limits: a 200K-token window sounds infinite until your agent's loop fills it with tool outputs — budget a 30-step run at roughly 3K tokens per step and watch 90K vanish. Cost and latency: longer outputs cost more and take longer — linear intuition you can do on the whiteboard. The output is your one-page 'numbers I can derive live' sheet — no memorized specs, only reasoning you can reproduce under pressure.",
 'project': "Depth sheet. The one-page derivation sheet plus 5 worked interview Q&As — transformer intuition, fine-tune vs RAG, context budgeting, inference economics, latency. Deliverables: the sheet and the Q&As, each answerable from the sheet's reasoning alone.",
 'honest': "Interview depth is not paper depth — nobody expects you to derive backprop, and reciting papers you half-remember is worse than saying 'I'd work it out like this.' The sheet is the skill: reasoning from first principles, live. Ask yourself: which question on your sheet would you currently bluff?",
 'quiz_sec': 'the Worked estimation',
}

MODULES['agentic-coding'] = {
 'sec2': 'Hands-on procedure',
 'procedure': [
  "Set the timer: 45 minutes, one loop implementation from scratch — no frameworks, no autocomplete heroics. The constraint is the training.",
  "Implement the loop: perceive, reason, act, observe — with a step budget and a transcript log, the pattern from the foundations track.",
  "Write the tool-use parser: take 5 messy model-style outputs (extra prose, malformed JSON, missing fields) and parse-or-reject each one correctly.",
  "Run the multi-step drill: 3 tasks of increasing difficulty (3, 5, and 8 steps); log exactly where each run breaks.",
  "Debug the failures: for each broken trajectory, classify the bug — bad parse, bad plan, bad tool, bad stop — and fix exactly one thing per iteration.",
  "Repeat timed: run the whole set again against the clock — the second pass is where the muscle memory forms.",
  "Narrate a review: talk through your loop's code out loud for 5 minutes, as if to an interviewer — record it, listen, cringe, improve.",
 ],
 'code': ("python",
  "import json, time\n\ndef timed_rep(task, tools, budget=45*60):\n    start, transcript = time.time(), []\n    state, steps = {\"task\": task}, 0\n    while time.time() - start < budget and steps < 10:\n        raw = model_think(state)                 # the messy output\n        action = parse_or_reject(raw)            # parse-or-reject: the drill\n        if action is None:\n            transcript.append((\"reject\", raw)); continue\n        obs = tools[action[\"name\"]](action[\"args\"])\n        transcript.append((action, obs))\n        steps += 1\n    return transcript  # classify every break: parse | plan | tool | stop"),
 'project': "Reps log. Five timed sessions of loop-building and trajectory debugging, with the bug-classification log. Deliverables: the final loop code, the reps log with times per session, and the narration notes (what stumbled, what got cut).",
 'honest': "Reps build fluency, not understanding — if you can't explain why the loop stops, the reps just made you fast at being wrong. The narration is the test: code you can't talk through, you don't own. Ask yourself: what question about your loop would make you freeze?",
}

MODULES['agentic-behavioral'] = {
 'sec2': 'Hands-on procedure',
 'procedure': [
  "Inventory your stories: list 5 real experiences with AI systems — including 2 failures. Real ones; interviewers smell fiction.",
  "STAR each one: Situation, Task, Action, Result — one page per story, with the numbers where they exist.",
  "Write the failure story twice: once defensive, once honest — keep the honest one, and note what changed between drafts.",
  "Prepare the safety answer: one real example of a safety or ethics trade-off you navigated (or would navigate) — with the reasoning, not just the conclusion.",
  "Draft the collaboration story: a disagreement about an AI approach, how it resolved, and what you'd do differently.",
  "Write your interviewer questions: 5 questions that reveal how the team actually builds and ships AI — evals, on-call, safety reviews.",
  "Calibrate seniority: for each story, mark what it signals (IC depth? judgment? ownership?) and find the gap your stories don't cover.",
 ],
 'code': ("text",
  "STAR template — one page per story:\nSITUATION: the context in two sentences. No jargon, no throat-clearing.\nTASK: what was yours to do — the responsibility, not the team's.\nACTION: what you actually did, step by step. Verbs, not adjectives.\nRESULT: the outcome with numbers where they exist — and what you'd do\ndifferently. The last line is what interviewers remember."),
 'project': "Story bank. Five STAR stories (two failures), the safety answer, and the interviewer questions — rehearsed out loud twice. Deliverables: the story bank doc and rehearsal notes (what stumbled, what got cut).",
 'honest': "Behavioral rounds test honesty under pressure — a polished failure story that teaches nothing is worse than an awkward honest one. 'What would you not ship again' is the question; have a real answer. Ask yourself: which of your stories are you tempted to exaggerate?",
}

MODULES['agentic-mock'] = {
 'sec2': 'Hands-on procedure',
 'procedure': [
  "Schedule the circuit: design, coding, behavioral — back to back, with breaks, under realistic conditions. Put it on the calendar; vague plans don't happen.",
  "Run the design mock: 45 minutes at the whiteboard (or blank page), narrating trade-offs — record every question you couldn't answer.",
  "Run the coding mock: timed loop implementation plus trajectory debugging — log the bugs by class (parse, plan, tool, stop).",
  "Run the behavioral mock: story bank out loud — note where you rambled, hedged, or exaggerated.",
  "Integrate the feedback within 24 hours: write down every miss and its fix — mocks without this step are performance anxiety practice.",
  "Pacing check: total time, energy curve, where stamina broke — adjust the next circuit's pacing, breaks, and question order.",
  "Repeat: the circuit runs at least twice — the second run measures whether the feedback integration actually worked.",
 ],
 'code': ("text",
  "Mock scorecard — one per round:\nDESIGN: scope stated? tools justified? memory designed? evals covered?\n  trade-offs narrated before asked? estimation attempted?\nCODING: loop runs? parser rejects cleanly? bugs classified? time kept?\nBEHAVIORAL: stories concrete? failures honest? safety answer real?\n  questions for interviewer asked?\nENERGY: where did stamina break? what gets cut or reordered next time?"),
 'project': "Two circuits, integrated. Two full mock circuits with feedback integration between them. Deliverables: both scorecards, the feedback-integration log, and the delta — what improved, what didn't, and what's still on the fix list.",
 'honest': "Mocks measure your mock performance — the transfer to real interviews is partial, and over-mocking breeds robotic answers. Two honest circuits beat ten anxious ones. Ask yourself: are you practicing the skills, or practicing being nervous?",
}

MODULES['agentic-portfolio'] = {
 'sec2': 'Hands-on procedure',
 'procedure': [
  "Audit your pieces: list every candidate project and keep only the ones you'd defend live — kill your darlings.",
  "Write the limits-first write-up for each piece: lead with what it doesn't do — the honest framing from every project module in this course.",
  "README as evidence: a stranger must be able to run it — test this with a fresh machine or a colleague, and fix everything that breaks.",
  "Record the demo: 3 minutes max, showing the thing working and one failure mode handled — no slideware.",
  "GitHub hygiene: pinned repos, clean READMEs, no committed secrets, issues that show you maintain things.",
  "Practice the talk-through: explain each piece's architecture and trade-offs out loud, without notes, in 5 minutes.",
  "Get one external read: someone technical reviews the portfolio and tells you what's unclear — integrate what they find.",
 ],
 'code': ("text",
  "README checklist — every portfolio piece:\n[ ] One-line what-it-does, up top\n[ ] Setup: exact commands, tested on a fresh machine\n[ ] How to run the demo in under 2 minutes\n[ ] Eval numbers or test results, not adjectives\n[ ] Limits section: what it doesn't do\n[ ] No secrets, no credentials, no personal data in history"),
 'project': "Portfolio, shippable. The finished portfolio — pieces, write-ups, READMEs, demo, hygiene. Deliverables: the portfolio itself, the external-review notes, and the talk-through rehearsal log.",
 'honest': "A portfolio of demos proves you can demo — the write-ups with limits are what prove you can engineer. 'A stranger can run it' is a higher bar than it sounds; most portfolios fail it. Ask yourself: which piece would you least want an interviewer to click into?",
}

# ---------------- agentic-ai-lowcode ----------------
MODULES['lowcode-platforms'] = {
 'sec2': 'Hands-on procedure',
 'procedure': [
  "Map the landscape: list 3 low-code agent platforms you've heard of; for each, write what it handles (hosting, auth, connectors, monitoring) versus what you still own.",
  "Tour one platform: build the 'hello agent' — a single-topic Q&A over a doc you provide — and note every default the platform chose for you.",
  "Price the intuition: find the pricing page (as of October 2026 — verify it, don't memorize it) and work out what 1,000 conversations a month would cost in the platform's own units.",
  "Test the fit: take one real workflow and score it against the platform's strengths (standard connectors, simple logic) and weaknesses (custom code, complex state).",
  "Write the trade-away list: what you give up — portability, deep customization, cost control at scale — in writing, before you're invested.",
  "Decide: platform A vs platform B vs pro-code for your workflow — one paragraph with the reasons, kept with the project.",
 ],
 'code': ("text",
  "Platform comparison — one row per candidate:\nHandles for you: hosting | auth | connectors | monitoring | evals\nYou still own: prompts | data quality | testing | cost control\nTrade-aways: portability | customization ceiling | unit economics at scale\nFit score for MY workflow (1-5): ___ because ___."),
 'project': "Platform brief. The landscape map, the hello-agent build notes, pricing intuition, and the fit decision for one real workflow. Deliverables: the brief — the doc you'd hand a manager asking 'should we use low-code?'",
 'honest': "Low-code platforms are wonderful until they're not — the ceiling arrives exactly when you're invested. Pricing pages are the most honest documentation; read them first. Ask yourself: what happens to your agent if the platform doubles prices next year?",
}

MODULES['lowcode-prompt-flows'] = {
 'sec2': 'Hands-on procedure',
 'procedure': [
  "Build the first flow: one prompt to one output, over your own data — get the trivial case working before chaining anything.",
  "Chain three steps: prompt A's output feeds prompt B via variables, not copy-paste — feel where the chaining helps and where context leaks between steps.",
  "Add branching: a decision step that routes on the input type; test all branches, including the one you think never fires.",
  "Test like software: 10 inputs with expected outputs; run the flow; log pass/fail — flows are code, test them as code.",
  "Iterate the prompts: change one prompt, re-run the 10 tests, keep the version that scores better — the prompt-versioning habit.",
  "Share it: export or share the flow with one colleague, watch them use it, and note every confusion — that's your UX feedback.",
 ],
 'code': ("text",
  "Flow test log — 10 cases:\n# | input | expected | actual | pass? | notes\n1 | ...     | ...      | ...    |       |\nIteration rule: change ONE prompt per iteration, re-run all 10,\nkeep the winner. Version every prompt you keep."),
 'project': "Tested flow. A 3+ step prompt flow with branching, a 10-case test set, and one documented iteration. Deliverables: the flow export or configuration, the test log, and the iteration note (what changed, what the scores did).",
 'honest': "Visual flows hide complexity — a 12-step flow with 4 branches is harder to debug than the code it replaced. 'Tested like software' is the bar; most flows never meet it. Ask yourself: at what step count would you rewrite this as code?",
}

MODULES['lowcode-connectors'] = {
 'sec2': 'Hands-on procedure',
 'procedure': [
  "Pick one real system to connect (email, spreadsheet, ticket queue) and write down exactly what data the agent needs — no more than that.",
  "Set up auth with the least-privilege identity available: a service account with narrow scopes, never your admin login.",
  "Scope the data access: restrict to the folders, tables, or queues the workflow needs; verify by listing what the connection can actually see.",
  "Add a trigger: a schedule or event that starts the flow — test it with a real event, not just the platform's 'test' button.",
  "Break it on purpose: revoke the credential, rename a column, throttle the API — log how the flow fails and what the user sees.",
  "Monitor: set up run-history review — check the last 20 runs for silent failures (success status, wrong outcome), the failure mode flows hide best.",
 ],
 'code': ("text",
  "Connector scope doc — one per connection:\nSystem: ___  Identity used: ___ (service account, never personal admin)\nScopes granted: ___  Data visible: ___ (verified by listing)\nTrigger: ___  Tested with real event? [ ]\nFailure modes tested: revoked creds [ ] renamed field [ ] throttling [ ]\nWhat the user sees on failure: ___"),
 'project': "Connected flow, hardened. A flow connected to a real system with scoped auth, a trigger, a failure-mode log, and monitoring. Deliverables: the scope doc, the failure-mode log, and the monitoring checklist.",
 'honest': "Connectors are credentials with a UI — every connection is an identity with permissions, and permissions drift. The 'test' button lies; real events are the test. Ask yourself: whose data can this flow touch right now, and would they be surprised?",
}

MODULES['lowcode-project'] = {
 'sec2': 'Hands-on procedure',
 'procedure': [
  "Pick the workflow: real, frequent, annoying — and small enough to finish; write the 'done' criteria first.",
  "Build the agent: topics and flows for the happy path first — resist the urge to handle every edge case on day one.",
  "Connect the data with scoped connectors from the previous module — no admin credentials, ever.",
  "Test with 5 real users: watch them use it; log every failure, confusion, and workaround — the user test is the eval.",
  "Gather feedback systematically: 3 questions per user (what worked, what broke, what you'd change); theme the answers.",
  "Iterate once: fix the top theme, re-test with 2 users, and show the delta.",
  "Write it up: what it automates, the user-test results, the limits — the honest delivery note.",
 ],
 'code': ("text",
  "User test script — same 3 questions per user:\n1. What worked? (let them show you, don't lead)\n2. What broke or confused you? (timestamp it in the run log)\n3. What would you change first?\nLog: failures | confusions | workarounds invented | top theme"),
 'project': "Shipped low-code agent. The complete project — built, connected, user-tested, written up. Deliverables: the agent itself, the user-test log (5 users), and the delivery note with limits.",
 'honest': "Five real users beat fifty imagined ones — the workflow you automated is not the workflow they have. 'It works in the builder' is the low-code version of 'it works on my machine.' Ask yourself: what did the users do that you never predicted?",
}

MODULES['lowcode-deploy'] = {
 'sec2': 'Hands-on procedure',
 'procedure': [
  "Publish deliberately: move from workspace to shared — note every setting that changes (permissions, data access, quotas).",
  "Set sharing and permissions: who can use it, who can edit it, and who owns it when you leave — write the ownership down, with a name.",
  "Turn on usage monitoring: runs per day, failure rate, and the one metric that tells you it's still working — check it weekly for a month.",
  "Build the feedback loop: where users report problems and who triages — a channel with an owner, not a void.",
  "Version it: export or save v1 before the first change; practice rolling back to it so 'deploy' never means 'no way back'.",
  "Write the handoff doc: architecture, where credentials live (never the values), monitoring, known limits — the doc that keeps the agent alive after you move on.",
  "Schedule the review: 30/60/90-day check-ins on usage, cost, and whether the agent is still needed at all.",
 ],
 'code': ("text",
  "Handoff doc — the agent's survival kit:\nWhat it does / who it's for / owner (name): ___\nArchitecture: flows, connectors, triggers\nCredentials: where stored (values never in this doc)\nMonitoring: dashboard link, the one metric that matters, check cadence\nKnown limits: ___  Rollback: how to restore v1\nReview dates: 30 / 60 / 90 days"),
 'project': "Deployed with a handoff. A published agent with monitoring, versioning, and the handoff doc. Deliverables: the handoff doc, the monitoring checklist or dashboard, and the review schedule.",
 'honest': "Deployed agents are orphans by default — nobody owns them, nobody monitors them, and they quietly rot. The handoff doc is the difference between a delivery and an abandonment. Ask yourself: if you left tomorrow, how long until someone notices this agent broke?",
}

MODULES['lowcode-limits'] = {
 'sec2': 'Worked estimation',
 'estimation': "Work the ceiling math before you hit it. Customization ceiling: list 5 things your flow might need (a custom auth flow? complex state? sub-second latency? bulk operations? offline use?) and mark which the platform can't do — count the workarounds; each workaround is future tech debt with interest. Cost at scale: take your current usage (say 2,000 runs a month — illustrative) and project 10× — price both tiers from the pricing page (as of October 2026, verify it); low-code unit costs that look trivial at pilot scale often exceed pro-code hosting at 10×. Write the crossover point: at what monthly volume does rebuilding in code get cheaper? Lock-in: list everything that doesn't export cleanly (flow definitions? prompt versions? conversation history? connector configs?) and estimate the rebuild cost in weeks if you had to leave. Governance: who approves new flows, who reviews data access, where the audit log lives — price the process, not just the tool. The output is the graduation decision doc: stay, graduate, or hybrid — with the crossover volume and rebuild cost as the deciding numbers.",
 'project': "Graduation decision. The stay/graduate/hybrid analysis for a real low-code agent — ceiling list, cost-at-scale math, lock-in inventory, governance. Deliverables: the decision doc with the crossover volume highlighted.",
 'honest': "The ceiling is a when, not an if — the skill is seeing it before you're trapped under it. 'We'll graduate later' without the crossover number is procrastination with extra steps. Ask yourself: what would force the graduation decision, and would you see it coming?",
 'quiz_sec': 'the Worked estimation',
}

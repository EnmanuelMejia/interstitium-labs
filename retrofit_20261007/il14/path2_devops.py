# -*- coding: utf-8 -*-
"""IL-14 retrofit content — Path 2: DevOps Engineering Interview Prep (6 modules)."""
# pylint: disable=line-too-long

P2_SUMMARY = {
"devops-interview-prep--devops-ci-cd": (
"Welcome to the DevOps Engineering Interview Prep path of the Interstitium Labs SRE, DevOps, Cloud & Security Interview Prep course. "
"I'm your instructor for this path, and we start with the artifact DevOps interviews are really about: the pipeline. CI stages in fail-fast order, immutable artifacts, deployment strategies by blast-radius tolerance, and the rollback plan that proves you have shipped before. "
"This is Module 1: CI/CD Systems. By the end you'll design a pipeline aloud — stages, gates, strategies — and defend every choice like someone who has been paged by a bad deploy."
),
"devops-interview-prep--devops-iac": (
"Welcome back. I'm your instructor for the DevOps Interview Prep path, and this is Module 2: Infrastructure as Code Patterns. "
"IaC interviews probe three topics that separate users from operators: state, modules, and drift. Declarative vs imperative, the Terraform plan-apply loop with remote state and locking, flat module composition, drift detection, and policy-as-code at plan time. "
"You'll leave able to whiteboard a Terraform workflow and explain why plan-before-apply is non-negotiable."
),
"devops-interview-prep--devops-containers": (
"Welcome back. I'm your instructor for the DevOps Interview Prep path, and this is Module 3: Containers and Orchestration. "
"Containers to orchestration in one arc: what Docker packages, what Kubernetes schedules, and where each breaks. Layers and cache order, tagging discipline, the core objects — Pod, Deployment, Service, Ingress, ConfigMap, Secret — and Helm for packaging it all. "
"By the end you'll walk the 'run it, find it, expose it' story without notes."
),
"devops-interview-prep--devops-troubleshoot": (
"Welcome back. I'm your instructor for the DevOps Interview Prep path, and this is Module 4: Troubleshooting Under Pressure. "
"This is the live round, rehearsed: timed failure drills where the graded skill is structured diagnosis narrated in real time. Reading logs under pressure, five whys with evidence, network debugging layer by layer, Kubernetes failure modes. "
"You'll learn the loop that wins these rounds: hypothesis → test → observe → update, said out loud."
),
"devops-interview-prep--devops-platform-build": (
"Welcome back. I'm your instructor for the DevOps Interview Prep path, and this is Module 5: Guided Platform Build. "
"Now we build the artifact: a portfolio-grade platform — repo scaffold with app plus Dockerfile, VPC via Terraform, scripted cluster bootstrap, CI pipeline, GitOps deploy with Argo CD — documented well enough to walk an interviewer through. "
"Platforms have customers, and their API is documentation: runbooks, ADRs, onboarding docs. You'll ship all three."
),
"devops-interview-prep--devops-mock": (
"Welcome back. I'm your instructor for the DevOps Interview Prep path, and this is Module 6: DevOps Mock Circuit. "
"The full DevOps loop simulated: a pipeline-design round, a live troubleshooting round, and the behavioral round where ops stories win offers. STAR for ops, questions that reveal the job's reality, and offer-negotiation basics. "
"You'll run the circuit timed, score it against a rubric, and turn the weakest round into next week's plan."
),
}

P2_NOTES = {
"devops-interview-prep--devops-ci-cd": [
{"title": "Concepts", "body": (
"- **Trunk-based development** — small, frequent merges to main behind feature flags: branches are inventory, and this keeps inventory near zero.\n"
"- **CI stages** — lint → unit tests → build → integration tests → security scans → artifact publish: fast-first so failures surface in minutes, not at minute 39.\n"
"- **Immutable artifact** — build once, promote the same artifact through environments: what you tested is what you ship.\n"
"- **Registry** — where immutable artifacts live (container/image, package): makes 'what's running where' answerable.\n"
"- **Blue-green** — two full environments, instant cutover and rollback: costs double capacity.\n"
"- **Canary** — new version to a small percentage first, promoted on observed metrics: safest for risky changes.\n"
"- **Rolling** — gradual replacement of old with new: simplest, slowest rollback.\n"
"- **Pipeline-as-code** — the pipeline versioned, reviewed, and reproducible like the app: if it isn't in version control, it's folklore.\n"
"- **Rollback vs fix-forward** — the decision hinges on blast radius and diagnosis confidence: big blast or uncertain cause means roll back."
)},
{"title": "Hands-on procedure", "body": (
"Design a CI/CD pipeline for a sample containerized API, on paper, in 30 minutes.\n"
"1. **Pick the branching model.** Trunk-based: short-lived branches, merge to main daily, feature flags for incomplete work. Write the one-sentence case for it.\n"
"2. **Order the CI stages fail-fast.** Lint + unit tests (minutes) → build → integration tests → security scans → artifact publish. Mark the expected duration of each stage.\n"
"3. **Define the artifact.** One immutable image per commit, tagged with the git SHA; floating tags never deploy to prod. State where it's stored.\n"
"4. **Choose the deploy strategy per environment.** Rolling to dev, canary (5% → 50% → 100% on metrics) to prod. Justify by blast-radius tolerance.\n"
"5. **Write the rollback plan.** Automated rollback trigger (error-rate or latency SLO breach within 10 minutes of deploy), plus the manual command. State the rollback-vs-fix-forward rule.\n"
"6. **Narrate it in 5 minutes.** Stages, gates, strategy, rollback — ending with: 'if the pipeline isn't in version control, it's folklore.'"
)},
{"title": "Project brief", "body": (
"Your deliverable: a pipeline design document for a sample service, written as a design-review artifact.\n"
"- **Pipeline diagram**: stages in order with durations, gates, and owners; the artifact and its tagging scheme.\n"
"- **Strategy matrix**: blue-green vs canary vs rolling per environment, with the blast-radius reasoning.\n"
"- **Rollback runbook**: triggers, commands, and the decision rule — when you roll back vs fix forward.\n"
"- **Pipeline-as-code**: the workflow file layout in the repo and how changes to it are reviewed.\n"
"- **Present it as a 10-minute design round**, then answer: 'your canary metrics look fine but users complain — what now?' in writing.\n"
"Reference shelf (module sources): **GitHub Actions Documentation** (https://docs.github.com/en/actions) — pipeline-as-code reference. **Jenkins Documentation** (https://jenkins.io/doc/) — the classic CI server most interview pipelines were built on."
)},
{"title": "Honesty note", "body": (
"Preparation only — this course confers no certificate, and a paper pipeline is not a production delivery system. "
"Real pipelines accumulate years of edge cases, flaky tests, and 3am lessons that no design doc reproduces. What transfers is the structure: fail-fast stages, immutable artifacts, strategy by blast radius, and a rollback story told before anyone asks. "
"Tool specifics follow vendor documentation, which changes; verify current GitHub Actions and Jenkins syntax against the linked sources as of their retrieval dates."
)},
],
"devops-interview-prep--devops-iac": [
{"title": "Concepts", "body": (
"- **Declarative** — state the desired end state; the tool converges (Terraform, Kubernetes manifests): idempotent and auditable.\n"
"- **Imperative** — script the steps: flexible but order-dependent and drift-prone.\n"
"- **Plan / apply** — Terraform's loop: preview the diff, then converge. Plan-before-apply is non-negotiable.\n"
"- **State** — Terraform's record of reality: lives in a remote backend with locking, never on a laptop.\n"
"- **Module** — a reusable unit of infrastructure (one concern each: network, compute, data): modules are functions, environment roots are the programs that call them.\n"
"- **Drift** — reality diverging from declared config (the manual console click): detected by scheduled plan runs, prevented by making the console read-only.\n"
"- **Policy-as-code** — governance enforced at plan time: violations are blocked before they exist, because prevention beats detection."
)},
{"title": "Hands-on procedure", "body": (
"Walk a Terraform change end to end on paper — this is the whiteboard exercise.\n"
"1. **Write the intent.** A small module: one VPC with two subnets, inputs for CIDR and environment, outputs for subnet IDs. Flat composition — no nesting.\n"
"2. **Run plan mentally.** List what the plan would show: 3 resources to add, 0 to change, 0 to destroy. Say why you read the plan before anything else.\n"
"3. **Apply with state discipline.** Remote backend, state locking enabled: two engineers applying at once can't corrupt state. Say what breaks without locking.\n"
"4. **Simulate drift.** Someone clicked in the console and changed a subnet. Your scheduled plan run shows a diff — narrate the response: alert on the diff, revert through code, never click to fix a click.\n"
"5. **Add policy-as-code.** A plan-time rule: no security group may open 0.0.0.0/0 to SSH. Violations fail the plan — prevention beats detection.\n"
"6. **Close with the line.** 'I declare the destination; the tool figures out the route. Drift is how outages hide.'"
)},
{"title": "Project brief", "body": (
"Your deliverable: an IaC repository design for a sample two-environment setup (staging, prod).\n"
"- **Layout**: modules (network, compute, data) plus environment roots that compose them with explicit inputs — flat, no deep nesting.\n"
"- **State strategy**: remote backend per environment, locking on, and the rule for who may touch state directly (nobody, except break-glass).\n"
"- **Workflow**: branch → plan in CI with the diff posted for review → apply on merge. Plan-before-apply, always.\n"
"- **Drift program**: scheduled plan runs that alert on diffs, and the console policy (read-only for humans).\n"
"- **One policy-as-code rule** with its justification, and the story of the outage it would have prevented.\n"
"- **Defend it in 10 minutes**, ending with the state-management traps you'd warn a junior about.\n"
"Reference shelf (module sources): **Terraform Documentation** (https://developer.hashicorp.com/terraform/docs) — workflow, state, and module references."
)},
{"title": "Honesty note", "body": (
"Preparation only — this course confers no certificate, and a paper Terraform design is not production infrastructure. "
"Real state files carry years of imports, taints, and 3am applies that no exercise reproduces; the module teaches the discipline that keeps them manageable: remote state, locking, flat modules, everything through code. "
"Provider and tool syntax changes; verify current Terraform behavior against the linked documentation as of its retrieval date."
)},
],
"devops-interview-prep--devops-containers": [
{"title": "Concepts", "body": (
"- **Image layer** — each Dockerfile instruction is a cached layer: order slow-changing steps (dependency install) before fast-changing ones (code copy) to maximize cache hits.\n"
"- **Multi-stage build** — build in one stage, ship only artifacts in the final stage: keeps runtime images small.\n"
"- **Tagging discipline** — immutable tags per build (git SHA); floating tags like 'latest' for convenience only, never deployed to prod.\n"
"- **Pod** — Kubernetes' smallest unit: one or more tightly-coupled containers.\n"
"- **Deployment** — declares desired pods with replica counts and the rolling-update strategy.\n"
"- **Service** — stable networking (virtual IP + DNS) for a set of ephemeral pods.\n"
"- **Ingress** — external HTTP routing (host/path → service): the resource declares intent, the controller (nginx, traefik) does the work.\n"
"- **ConfigMap / Secret** — config separation: non-sensitive config vs sensitive values. Secrets are base64-encoded — obfuscated, not encrypted — so real protection means etcd encryption or an external secret manager.\n"
"- **Helm values** — one chart, many values files: dev/staging/prod differ by values, not by forked manifests."
)},
{"title": "Hands-on procedure", "body": (
"Containerize a sample app and put it on Kubernetes, on paper, in 30 minutes.\n"
"1. **Write the Dockerfile.** Multi-stage: dependencies installed before code copy for cache hits, minimal final image, non-root user. Annotate each instruction with its layer-cache reasoning.\n"
"2. **Set tagging.** Image tagged with the git SHA at build time; 'latest' never leaves the dev registry. Write the rule: 'mutable tags make what's-running unanswerable.'\n"
"3. **Write the Deployment.** Replicas, image with SHA tag, resource requests/limits, liveness and readiness probes — and say what each probe protects against.\n"
"4. **Add the Service and Ingress.** ClusterIP Service selecting the pods; Ingress with host/path rules; note that the controller is the actual proxy.\n"
"5. **Separate config.** ConfigMap for non-sensitive settings, Secret for credentials — mounted, never baked into the image. Note the base64 caveat and the real protection.\n"
"6. **Narrate the three layers.** 'Run it (Deployment), find it (Service), expose it (Ingress)' — then name where you'd put a Helm chart and why."
)},
{"title": "Project brief", "body": (
"Your deliverable: a containerization-and-deploy package for a sample service, review-ready.\n"
"- **Dockerfile** with layer-cache annotations and a written justification for the base image choice.\n"
"- **Manifests or a Helm chart**: Deployment, Service, Ingress, ConfigMap, Secret references — one chart with values per environment if you choose Helm.\n"
"- **Tagging and promotion policy**: SHA tags, how images move dev → staging → prod, and the rule against 'latest'.\n"
"- **Failure notes**: what CrashLoopBackOff, ImagePullBackOff, and OOMKilled each mean for this app, and the first command you'd run for each.\n"
"- **Walk an interviewer through it in 10 minutes**, from `docker build` to the Ingress serving traffic.\n"
"Reference shelf (module sources): **Docker Documentation** (https://docs.docker.com/) — image builds and registries. **Kubernetes Documentation** (https://kubernetes.io/docs/) — core objects, networking, failure modes."
)},
{"title": "Honesty note", "body": (
"Preparation only — this course confers no certificate, and paper manifests are not a production cluster. "
"Real clusters accumulate admission policies, network policies, and upgrade scars that no exercise covers; the module teaches the object model and the discipline (immutable tags, config outside images) that keep them operable. "
"Kubernetes and Docker behavior changes across versions; verify current syntax against the linked documentation as of its retrieval date."
)},
],
"devops-interview-prep--devops-troubleshoot": [
{"title": "Concepts", "body": (
"- **Hypothesis-driven diagnosis** — hypothesis → test → observe → update: the loop that makes debugging gradable when narrated.\n"
"- **Five whys** — asking 'why' iteratively from the symptom, each answer grounded in evidence, until reaching a systemic cause with an action item.\n"
"- **Layer bisection** — DNS resolves? TCP connects? TLS handshakes? HTTP responds? Each layer's test isolates the fault.\n"
"- **CrashLoopBackOff** — the container starts then exits: bad command, missing config, or a failing startup probe. `kubectl describe` tells the story; events are the narrator.\n"
"- **ImagePullBackOff** — the image can't be fetched: registry, tag, or auth problem.\n"
"- **OOMKilled** — the container exceeded its memory limit: limits vs reality.\n"
"- **Thinking aloud** — narrating hypotheses, what each command tests, and what the output means: silent debugging is unscoreable."
)},
{"title": "Hands-on procedure", "body": (
"Run this 15-minute timed drill on a sample failure: 'the API returns 502s after a deploy.'\n"
"1. **State the hypothesis set (1 min).** Bad deploy, downstream down, config missing. Rank by likelihood and cheapness to test.\n"
"2. **Check what changed (2 min).** Deploy annotations, recent deploys — 'what changed?' is the first incident question.\n"
"3. **Bisect the network (3 min).** `curl -v`: does DNS resolve? Does TCP connect? Does TLS handshake? Name which layer each failure implicates.\n"
"4. **Read the pods (3 min).** `kubectl get pods`, then `describe` on the failing one: CrashLoopBackOff? OOMKilled? Read the events like a narrator.\n"
"5. **Filter the logs (3 min).** Time window around the incident, the failing service first, errors before info — 'narrow before I read.'\n"
"6. **Decide and narrate (3 min).** Mitigation first (rollback?), then the five-whys chain with evidence per 'why' — said out loud, the whole way."
)},
{"title": "Project brief", "body": (
"Your deliverable: a troubleshooting drill pack — three timed scenarios with answer keys.\n"
"- **Scenario A**: pods CrashLooping after a config change — the `kubectl describe` reading drill.\n"
"- **Scenario B**: `curl -v` failing at 'Could not resolve host' — the DNS-layer bisection drill.\n"
"- **Scenario C**: 502s after a deploy with healthy pods — the 'what changed' + downstream drill.\n"
"- Each scenario: the symptom, the time box, the expected hypothesis-test-observe chain, and the narrated answer.\n"
"- **Run all three with a partner timing you**, then write the debrief: where your narration broke down and the drill that fixes it.\n"
"Reference shelf (module sources): **Kubernetes Documentation** (https://kubernetes.io/docs/) — failure modes and kubectl references. **Grafana Documentation** (https://grafana.com/docs/) — dashboards used in the troubleshooting modules."
)},
{"title": "Honesty note", "body": (
"Preparation only — this course confers no certificate, and drills are not production incidents. "
"Real failures involve incomplete telemetry, misleading symptoms, and pressure that a 15-minute timer only gestures at. What transfers is the method: hypotheses ranked by cheapness, layer bisection, evidence per 'why', and narration throughout. "
"Command syntax changes across tool versions; verify current kubectl, curl, and openssl usage against the linked documentation as of its retrieval date."
)},
],
"devops-interview-prep--devops-platform-build": [
{"title": "Concepts", "body": (
"- **Platform scaffold** — repo layout (app + infra + pipeline), VPC via Terraform, scripted cluster bootstrap, CI pipeline, GitOps deploy: the platform's first impression.\n"
"- **GitOps** — git as the single source of truth for desired state; an agent (Argo CD/Flux) continuously reconciles the cluster to it. Declared state wins automatically.\n"
"- **Cluster bootstrap** — scripted, reviewable cluster creation: the cluster becomes code, not folklore.\n"
"- **ADR (Architecture Decision Record)** — the decision, its context, alternatives considered, and consequences: the 'why' behind the design.\n"
"- **Runbook** — the operator's procedure for a known failure: the platform team's API to its customers.\n"
"- **Documentation as deliverable** — platforms have customers; undocumented automation is a ticket queue with extra steps."
)},
{"title": "Hands-on procedure", "body": (
"Build the platform scaffold on paper, in order, in 40 minutes.\n"
"1. **Lay out the repo.** `app/` (code + Dockerfile), `infra/` (Terraform: VPC, cluster), `pipeline/` (CI workflows), `gitops/` (Argo CD app manifests), `docs/` (ADRs, runbooks). Justify each directory.\n"
"2. **Terraform the VPC.** Module with public/private subnets, NAT, route tables — the network the cluster will live on.\n"
"3. **Script the bootstrap.** Every cluster-creation step as a script or IaC: no clicks. State why: reproducible, reviewable, auditable.\n"
"4. **Wire the CI pipeline.** Lint → test → build → scan → push SHA-tagged image — the pipeline from the CI/CD module, reused.\n"
"5. **Add the GitOps deploy.** Argo CD watches the repo; merges to main reconcile the cluster. Narrate the drift story: manual changes get reverted automatically.\n"
"6. **Write one ADR and one runbook.** ADR: why Argo CD over push-based deploys. Runbook: pods CrashLooping — the triage procedure from the troubleshooting module."
)},
{"title": "Project brief", "body": (
"Your deliverable: the platform-build portfolio piece — the artifact you walk an interviewer through.\n"
"- **Repo scaffold** with the full layout and a README that explains the whole system in one page.\n"
"- **Terraform for the VPC**, **scripted cluster bootstrap**, **CI pipeline**, **GitOps deploy** — each piece committed as code.\n"
"- **Two ADRs**: the GitOps choice and one infrastructure choice, each with context, alternatives, and consequences.\n"
"- **One runbook**: the CrashLooping triage procedure, written for a teammate at 3am.\n"
"- **The 10-minute walkthrough**: repo → cluster → pipeline → deploy, ending with 'the scaffold is the platform's first impression.'\n"
"Reference shelf (module sources): **Terraform Documentation** (https://developer.hashicorp.com/terraform/docs). **GitHub Actions Documentation** (https://docs.github.com/en/actions). **Kubernetes Documentation** (https://kubernetes.io/docs/)."
)},
{"title": "Honesty note", "body": (
"Preparation only — this course confers no certificate, and a scaffold is not a production platform. "
"Real platforms serve real developers with real SLAs, and their hardest problems are organizational — adoption, ownership, support load — not YAML. What the build teaches is the shape: automated, documented, reconcilable, and reviewable. "
"Describe it in interviews as a portfolio build with stated simplifications, never as production platform experience you don't have."
)},
],
"devops-interview-prep--devops-mock": [
{"title": "Concepts", "body": (
"- **Pipeline-design round** — stages in order, artifact promotion, rollback story: design shows judgment.\n"
"- **Live troubleshooting round** — hypothesis → test → observe, narrated, time-boxed: troubleshooting shows method.\n"
"- **STAR for ops** — Situation, Task, Action (yours, the bulk), Result (measurable + lesson): the evidence unit for behavioral rounds.\n"
"- **Ops behavioral stories** — on-call nights, incident decisions, disagreements about risk, learning from outages: all blameless.\n"
"- **Interviewer questions** — 'what does success look like in 6 months?', 'what's the hardest technical problem?', 'how are on-call and incidents handled?', 'why is this role open?' Never ask what the website answers.\n"
"- **Total-compensation negotiation** — base, equity, bonus, start date: negotiate the whole package, informed and in good faith, and get it in writing."
)},
{"title": "Hands-on procedure", "body": (
"Run the DevOps mock circuit with a partner, timed.\n"
"1. **Pipeline-design round (45 min).** Given a sample service: stages, artifact, strategy per environment, rollback plan — narrated, with tradeoffs.\n"
"2. **Live troubleshooting round (30 min).** A seeded failure (502s after deploy): hypothesis → test → observe → update, aloud, time-boxed.\n"
"3. **Behavioral round (30 min).** Three STAR stories: an on-call night, a disagreement about risk, an outage you learned from — all blameless.\n"
"4. **Your questions (10 min).** Ask the interviewer the four reality-revealing questions; practice listening for the health of the team in the answers.\n"
"5. **Score it.** Rubric per round: design judgment, diagnostic method, story evidence, communication. Name the lowest axis.\n"
"6. **Write the debrief.** The weakest round becomes next week's drills; the strongest story goes in the bank, rehearsed."
)},
{"title": "Project brief", "body": (
"Your deliverable: a DevOps interview dossier.\n"
"- **Pipeline design doc** from a timed round, with the rollback story and the strategy matrix.\n"
"- **Troubleshooting debrief**: the seeded failure, your hypothesis chain, where narration broke down, the fix.\n"
"- **Story bank**: five STAR ops stories (on-call, incident, disagreement, failure, learning) — each with a measurable result.\n"
"- **Your interviewer questions**, with notes on what good vs worrying answers sound like.\n"
"- **Compensation worksheet**: your market range from data, the whole-package checklist, and the 'negotiate once, informed and in good faith' plan.\n"
"- **The taper plan**: no new topics in the final two weeks — redrill, mock, rest.\n"
"Reference shelf (module sources): **GitHub Actions Documentation** (https://docs.github.com/en/actions). **Indeed Career Guide: Interviewing** (https://www.indeed.com/career-advice) — STAR format and preparation checklists."
)},
{"title": "Honesty note", "body": (
"Preparation only — this course confers no certificate, and mock rounds are not real loops. "
"Partners are kinder than panels, and practiced stories must stay truthful: never invent on-call heroics you didn't live — interviewers probe stories, and fabricated ones collapse. Rehearse real experience; frame drill experience as drills. "
"Compensation guidance is general information, not financial advice; market data moves — verify ranges against current sources when you negotiate."
)},
],
}

P2_NEW_CARDS = {
"devops-interview-prep--devops-ci-cd": {
"front": "How do you keep a 40-minute pipeline from failing at minute 39?",
"back": "Order stages fail-fast: lint and unit tests in the first minutes, then build, integration, scans, publish. Fast, cheap failures first; slow, expensive verification only for code that earned it. The interview line: 'fail fast and cheap — a 40-minute pipeline that fails at minute 39 teaches nothing quickly.'",
},
"devops-interview-prep--devops-iac": {
"front": "Why is 'plan-before-apply' non-negotiable?",
"back": "The plan is the diff between declared and actual — it's the review, the blast-radius estimate, and the last chance to catch a typo that deletes the database. Applying blind is clicking 'yes' on a dialog you didn't read. The interview line: 'the plan is the change's résumé; I read résumés before hiring.'",
},
"devops-interview-prep--devops-containers": {
"front": "How do you shrink a 1.2 GB container image?",
"back": "Multi-stage build (ship only runtime artifacts), minimal base image, dependencies before code copy for cache efficiency, and audit what's inside — build tools and caches don't sail to prod. Smaller images pull faster, scan faster, and shrink the attack surface. The interview line: 'the image should contain the app, not the workshop.'",
},
"devops-interview-prep--devops-troubleshoot": {
"front": "What's your first move when the dashboard is red but nobody knows why?",
"back": "Ask 'what changed?' — check deploy annotations and recent deploys before touching anything. Most production mysteries are deployments in disguise, and the answer is usually in the last hour's timeline. The interview line: 'I investigate the timeline before I investigate the system.'",
},
"devops-interview-prep--devops-platform-build": {
"front": "How do you convince a team to adopt your platform?",
"back": "Make the paved road the easy road: golden-path templates, self-service deploys, docs that answer before they ask — and never mandate what you can't support. Adoption is the platform's real metric; a platform nobody uses is a hobby. The interview line: 'I measure the platform by its customers' deploys, not by its features.'",
},
"devops-interview-prep--devops-mock": {
"front": "How do you answer 'tell me about a disagreement with a teammate'?",
"back": "STAR with the conflict as the situation: what each side wanted, the data or principle that decided it, what you actually did (listened, proposed, conceded or persuaded), and the result — including what you'd do differently. Blameless, specific, and about the work. The interview line: 'disagreements are design reviews with feelings; I treat them that way.'",
},
}

def _q(q, choices, answer, explain):
    assert len(choices) == 4 and 0 <= answer <= 3 and explain
    return {"q": q, "choices": choices, "answer": answer, "explain": explain}

P2_NEW_QUIZ = {
"devops-interview-prep--devops-ci-cd": [
_q("Security scans belong in the CI pipeline:",
   ["After production deploy", "After integration tests, before artifact publish — nothing ships unscanned", "Only on Fridays", "In a separate repo"], 1,
   "Scans gate promotion: the artifact that ships is the artifact that was scanned — the stage order in the Concepts."),
_q("A hotfix to production at 2am still goes through:",
   ["A manual SCP of the binary", "The same pipeline — emergencies need the pipeline's safety most", "Email approval only", "Direct database edits"], 1,
   "The pipeline is the safe path especially under pressure; bypassing it is how 2am becomes 6am."),
_q("Blue-green's main cost vs canary is:",
   ["Complexity", "Double capacity — two full environments standing by", "Slower deploys", "No rollback"], 1,
   "Instant cutover and rollback are bought with a second full environment — the Concepts."),
_q("Feature flags support trunk-based development by:",
   ["Hiding bugs", "Decoupling deploy from release — incomplete work merges safely behind a flag", "Speeding builds", "Replacing tests"], 1,
   "Flags let small frequent merges land without exposing unfinished work — the Hands-on procedure step 1."),
_q("The pipeline's rollback trigger should be:",
   ["A manager's email", "Automatic on SLO breach after deploy, with a manual path — decided before the incident", "Never automatic", "A calendar reminder"], 1,
   "Rollback criteria written during calm are followed during panic — the Project brief's runbook."),
_q("Publishing the artifact only after all stages pass ensures:",
   ["Faster builds", "The registry holds only verified, immutable artifacts — 'what's running where' stays answerable", "Smaller images", "Fewer stages"], 1,
   "The registry is the source of truth for what's shippable; unverified artifacts don't enter it."),
],
"devops-interview-prep--devops-iac": [
_q("Two engineers applying Terraform at once is safe only with:",
   ["Loud voices", "Remote state with locking — concurrent applies can't corrupt state", "Separate laptops", "Good intentions"], 1,
   "Locking serializes applies; without it, state corrupts — the Hands-on procedure step 3."),
_q("A scheduled 'terraform plan' that alerts on diffs is:",
   ["Wasteful", "Drift detection — reality diverging from declared config gets caught", "A backup", "A test"], 1,
   "Detection is the scheduled plan run; prevention is everything-through-code — the Concepts."),
_q("Environment roots composing small modules with explicit inputs beat deep nesting because:",
   ["It's trendy", "Inputs stay visible — deep nesting tunnels them opaquely and both debugging and reuse suffer", "It's faster", "State prefers it"], 1,
   "Flat composition keeps the dependency graph legible — 'modules are functions; roots are the programs.'"),
_q("Policy-as-code at plan time beats post-deploy auditing because:",
   ["Auditors prefer it", "Violations are blocked before they exist — prevention beats detection", "It's cheaper", "It's faster"], 1,
   "The bad change never reaches the cloud — the Hands-on procedure step 5."),
_q("Making the cloud console read-only for humans prevents drift by:",
   ["Slowing everyone down", "Forcing every change through code, so reality can't silently diverge", "Saving money", "Pleasing auditors"], 1,
   "If all changes flow through IaC, the declared state stays the actual state — the Project brief."),
_q("Storing Terraform state on a laptop is wrong because:",
   ["Laptops are slow", "State is shared truth — it needs a remote backend with locking, versioning, and access control", "It's too big", "JSON is ugly"], 1,
   "State tracks reality for the whole team; a laptop is a single point of loss and conflict — the Concepts."),
],
"devops-interview-prep--devops-containers": [
_q("Putting dependency install before code copy in a Dockerfile:",
   ["Is traditional", "Maximizes layer cache hits — slow-changing steps cache, fast-changing code rebuilds cheaply", "Is required", "Shrinks the base"], 1,
   "Cache order is the Dockerfile's performance story — the Hands-on procedure step 1."),
_q("A Pod stuck in Pending most often means:",
   ["A bad image", "No schedulable node or insufficient resources for its requests", "DNS failure", "A full disk"], 1,
   "Pending = the scheduler can't place it: resources, taints, or affinity — triage from the Concepts."),
_q("Running containers as root inside the image is discouraged because:",
   ["It's slower", "A container escape then runs as root on the host — least privilege applies inside containers too", "It's trendy to avoid", "Logs break"], 1,
   "Defense in depth: non-root users contain the blast radius of an escape."),
_q("ConfigMaps vs Secrets: the real distinction is:",
   ["Size", "Secrets hold sensitive values with access controls — but both are just Kubernetes objects, and Secrets are only base64, not encrypted", "Speed", "Format"], 1,
   "The base64 caveat: obfuscated, not encrypted — real protection is etcd encryption or external managers, per the Concepts."),
_q("An Ingress without an Ingress controller:",
   ["Still routes traffic", "Is just config — no proxy implements the routing, so nothing happens", "Uses DNS instead", "Falls back to NodePort"], 1,
   "The resource declares intent; the controller does the work — the Hands-on procedure step 4."),
_q("Helm values files per environment beat forked manifests because:",
   ["YAML is fun", "One chart, many values — environments differ by configuration, not by duplicated templates", "It's faster", "Charts are small"], 1,
   "Duplicated manifests drift; values keep one source of truth — the Concepts."),
],
"devops-interview-prep--devops-troubleshoot": [
_q("Five whys stops being useful when:",
   ["You reach exactly five", "Answers become speculation — each 'why' needs evidence from logs, metrics, or deploys", "People agree", "It's too fast"], 1,
   "Whys without evidence are storytelling; the method works grounded in telemetry — the Concepts."),
_q("`kubectl describe pod` is the first read because:",
   ["It's short", "Events narrate the pod's story — scheduling, pulls, probes, kills — in one place", "It's required", "Logs are slow"], 1,
   "'Events are the narrator' — the failure-mode reading in the Hands-on procedure step 4."),
_q("OOMKilled in the events means:",
   ["The node died", "The container exceeded its memory limit — compare limits against reality", "The image is bad", "DNS failed"], 1,
   "Limits vs reality: the fix is measurement, then the right limit — the Concepts."),
_q("Filtering logs by time window and service before reading works because:",
   ["Logs are short", "Narrowing first turns an unreadable flood into a relevant signal — 'guilty until filtered innocent'", "Grep is fun", "It's required"], 1,
   "Volume defeats reading; filters defeat volume — the Hands-on procedure step 5."),
_q("In a troubleshooting round, saying 'my hypothesis is X, and this command tests it' helps because:",
   ["It fills time", "It makes your method gradable — the interviewer scores hypotheses and updates, not just the answer", "It's polite", "Typing is slow"], 1,
   "Narration turns invisible reasoning into scorable evidence — the Concepts' thinking-aloud."),
_q("Time-boxing each diagnostic step matters because:",
   ["Clocks are fun", "Rabbit holes are the failure mode — the box forces hypothesis updates instead of tunnel vision", "It's traditional", "Partners insist"], 1,
   "Unbounded digging on one hypothesis is how rounds are lost; the box enforces the loop."),
],
"devops-interview-prep--devops-platform-build": [
_q("Scripting the cluster bootstrap instead of clicking matters because:",
   ["It's faster once", "It's reproducible and reviewable — the cluster becomes code, not folklore", "It's trendy", "Clicks are banned"], 1,
   "Unscripted setup can't be rebuilt, reviewed, or audited — the Hands-on procedure step 3."),
_q("In GitOps, someone hand-edits a deployment in the cluster. The result is:",
   ["A promotion", "The agent reconciles it back to the git-declared state — drift gets reverted automatically", "A celebration", "Nothing"], 1,
   "Continuous reconciliation: declared state wins — the Concepts."),
_q("An ADR's most valuable section is:",
   ["The title", "Alternatives considered and consequences — the 'why', not just the 'what'", "The date", "The author"], 1,
   "Future readers need the reasoning that chose this path over the others — the Concepts."),
_q("A runbook written 'for a teammate at 3am' must be:",
   ["Long", "Runnable half-asleep: symptoms, exact commands, expected outputs, escalation point", "Theoretical", "Funny"], 1,
   "The runbook is the platform's API to its customers — clarity under fatigue is the spec, per the Project brief."),
_q("The platform's adoption metric that matters is:",
   ["Features shipped", "Developers' deploys through the paved road — a platform nobody uses is a hobby", "Lines of YAML", "Meetings held"], 1,
   "Platforms have customers; usage is the scoreboard — the new card's interview line."),
_q("Putting pipeline, infra, and app in one repo layout helps because:",
   ["Monorepos are trendy", "The whole system's change story is reviewable together — app, infra, and delivery in one PR view", "It's faster", "Git prefers it"], 1,
   "The scaffold's first impression is coherence: one place where the system is understood — the Concepts."),
],
"devops-interview-prep--devops-mock": [
_q("In a pipeline-design mock, the rollback story is graded because:",
   ["It's easy", "It proves you've shipped before — anyone can draw stages; rollback proves operations", "It's short", "Interviewers love it"], 1,
   "Design shows judgment; the rollback story shows experience — the Concepts."),
_q("A STAR 'Action' that says 'we decided' is weak because:",
   ["Teams don't matter", "It hides your contribution — interviewers evaluate you, so your decisions must be explicit", "It's long", "It's humble"], 1,
   "'We' stories hide the candidate; the A is yours — the Concepts."),
_q("Asking 'why is this role open?' reveals:",
   ["Gossip", "The job's reality — growth, backfill, or churn — which predicts your actual experience", "Salary", "Nothing"], 1,
   "You're interviewing them too; the answer predicts your day-to-day — the Concepts."),
_q("Negotiating the whole package (not just base) matters because:",
   ["Base is irrelevant", "Equity, bonus, and benefits often outweigh base deltas — the package is the number", "It's polite", "HR expects it"], 1,
   "Single-dimension negotiation leaves money unclaimed — the Project brief's worksheet."),
_q("A troubleshooting mock where you narrate nothing scores poorly because:",
   ["Silence is rude", "Silent debugging is unscoreable — the method can't be graded if it isn't spoken", "Typing is slow", "Partners get bored"], 1,
   "The round grades method under pressure; narration is the method made visible — the Hands-on procedure."),
_q("After the mock circuit, the story bank's purpose is:",
   ["Entertainment", "Rehearsed, truthful STAR stories ready for the behavioral round — won before the interview", "Homework", "Networking"], 1,
   "Behavioral rounds are won in preparation: banked stories, practiced aloud — the Project brief."),
],
}

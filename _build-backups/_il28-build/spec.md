# IL-28 Build Spec — module authoring contract

You are authoring modules for **IL-28 · DevSecOps & Cloud Infrastructure — Production Mastery Bootcamp** (courseId `il-28-devsecops-cloud-infrastructure-mastery`, code `IL-28`), built to the same completeness bar as IL-26 (schema v4).

## Output
Write a JSON array of module objects to your assigned file (e.g. `~/workspace/apex-audit/docs/university/data/courses/_il28-build/batch-A.json`). The file must contain ONLY the JSON array (valid JSON, parseable by `json.load`).

## Module object — ALL fields required, no exceptions
```json
{
  "id": "IL28-M01",
  "code": "IL-28",
  "title": "Binary, Hexadecimal & Two's Complement",
  "summary": "One-to-two sentence description of what the module teaches and why it matters in DevSecOps.",
  "objectives": ["4 to 5 concrete learning objectives as strings"],
  "notes": [
    {"title": "Note title", "body": "Complete original exposition, 120-300 words. Include worked examples WITH full solutions inline. Every concept gets at least one worked example. 5 to 8 notes per module."}
  ],
  "cards": [{"front": "Question/prompt", "back": "Answer"}] ,
  "quiz": [{"q": "question", "choices": ["4 options"], "answer": 0, "explain": "why the answer is right"}],
  "weight": 1,
  "prerequisiteFor": ["IL28-Mxx"],
  "drills": [{"id": "il28-m01-<slug>", "title": "Drill title", "items": [{"prompt": "...", "answer": "...", "explain": "..."}]}],
  "handsOnLab": {"id": "il28-m01-lab", "title": "...", "brief": "2-3 sentences", "steps": ["8-14 concrete steps"], "deliverable": "what the learner produces", "checkpoint": "how they verify success"},
  "mockTask": {"id": "il28-m01-mock", "type": "choice", "q": "...", "choices": ["4 options"], "answer": 0, "explain": "..."},
  "crossLinks": [],
  "videos": [{"title": "...", "url": "https://...", "source": "...", "durationMin": 30, "order": 1, "watchBefore": "notes", "blurb": "1-2 sentences"}],
  "estimatedMinutes": 480
}
```

## Volume per module (minimum — this is the "worth-paying-for" bar)
- objectives: 4-5
- notes: 5-8, each 120-300 words, with worked examples and solutions
- cards: 10-14 flashcards
- quiz: 8-10 questions (4 choices each, answer index, explanation)
- drills: 1-2 drills, each with 6-8 items (prompt/answer/explain)
- handsOnLab: 8-14 steps + deliverable + checkpoint
- mockTask: at least 1 (panel-interview-style question where relevant)
- videos: 1-2 per module
- estimatedMinutes: compute honestly as weight*120 + notes*12 + cards*4 + quiz*8 + drillItems*4 + 90 (lab) + min(180, videoMinutes/2). Round to nearest 30.

## Content rules (hard)
1. ALL content is ORIGINAL exposition you write. Never copy text from vendor docs, blogs, or other sources.
2. NO invented facts, metrics, credentials, salary figures, or exam pass-rate claims. No "BNY uses X" claims. No vendor affiliation, endorsement, or certification-conferral claims. The course confers no certificate.
3. Terminal commands shown must be real and correct (verify syntax from knowledge; prefer the exact commands from the interview sessions: ss, lsof, netstat, telnet, nc, ping, traceroute, df -i, lsof +L1, kubectl describe/get/logs/exec, terraform plan/import/apply, az aks nodepool scale, docker build with multi-stage, etc.).
4. Python code samples must be runnable and correct. Predict-output drills must have VERIFIED answers (trace the code yourself).
5. Videos: include ONLY URLs you are highly confident exist — official channels only (e.g. youtube.com/@HashiCorp, youtube.com/@Kubernetes, Microsoft Learn / learn.microsoft.com pages, freeCodeCamp full courses you know). Format like IL-26 videos. If uncertain, use fewer videos rather than fake ones; the assembler will drop any that fail HTTP checks. Prefer 1-2 you trust over 3 you guess.
6. Interview-driven modules: the course's north star is INDEPENDENT mastery — the learner must answer panel questions with NO copilot. Convert every listed panel question into drills/quizzes/mocks with full model answers in the `explain` fields.
7. Interview module (M50) is special: every real panel question from the session list below becomes a timed drill item + a mock task with a STAR-structured model answer in `explain`. Behavioral questions get STAR scaffolds.

## Real BNY/BNY panel questions (from the user's 2025 interview sessions) — embed these as drills/mocks in the relevant modules
Terraform/Ansible: biggest difference Terraform vs Ansible; if Ansible can create VMs why not just use Ansible; difference removing resources (Terraform vs Ansible); what exactly to do in a Terraform file to remove a resource (destroy vs remove block + apply).
Linux/RHEL: preferred OS; Red Hat familiarity / Red Hat Satellite; "no space on disk" but df shows free space (inodes); other causes of intermittent "no space" with free space (file descriptors, quotas, /tmp); check open ports (netstat, ss, lsof); simplest tool to check a port server A to server B (telnet/nc); troubleshoot connection issues between two servers (ping, traceroute, telnet, firewall rules); UDP vs TCP.
Git: rebase vs merge.
Python: read a car-counting script and predict console output; how many Kia cars printed (write YOUR OWN original script-reading drills — do not copy the session's script); requirements.txt review (requests, flask, flask-cors, asyncio, setuptools, pandas, pytest): approve the MR? what must change (pin versions).
Docker: optimize container image size; what RUN does in a Dockerfile (layers); replacing cleanup step with `echo hello` — does size change; does removing files in a later layer reduce size (whiteout — earlier layers retain data).
Kubernetes: troubleshoot an app in a pod (kubectl get/describe/logs/exec/events); pod keeps restarting — next steps; check exit code/reason (describe pod, State/Last State); Pod YAML review — frontend pod, image nginx:v4, requests memory 16Gi cpu 0.5, limits memory 32Gi cpu 8 — what issues later; if nginx needs min 2Gi to start, works?; request 1Gi but needs 2Gi — works? (OOMKilled risk); container svc-basic terminated exit code 137 — why killed (OOMKilled).
Jenkins: pipelines with what tools/languages (Groovy); Groovy directly in Jenkinsfile; standardize Jenkinsfiles across repos (shared libraries); written shared libraries?
Helm: why Helm instead of plain YAML.
K8s concepts: how many services/applications can run in a pod.
Behavioral: prefer coding or infrastructure.
Terraform deep: self-rating; resources via Terraform — full lifecycle walkthrough testing→dev/stage/QA→prod; Azure Blob/storage accounts; scenario — dev team needs a storage account, given container names, codify in Terraform; requirements change — per-container access type (private/blob/container), modify code (for_each over list → map of name→access type); state drift — VM data disk added manually in Azure, not in repo, must keep it (terraform plan + import); for_each import address escaping (terraform import 'azurerm_managed_disk.example["disk1"]' <id>); how Terraform was run at previous job — code on GitHub, secrets via env vars, tfvars not in git, Jenkins credential injection, HashiCorp Vault, Consul for config/service discovery.
Azure networking: exposed K8s endpoints via Application Gateway; expose internal Azure endpoint to internet; App Gateway vs Load Balancer (L7 vs L4); traffic flow browser→DNS→App Gateway→backend (AKS); Private Links — which services (storage, SQL, Key Vault, App Service, ACR); private link custom DNS (Private DNS zone, A record, VNet link, conditional forwarding).
Ansible: manage others' playbooks vs write new; most interesting role created; capture command output (register).
K8s/AKS: benefit of multiple node pools vs one giant pool; pod stuck in Pending — troubleshoot; "insufficient resources"/"out of nodes" — fix; manually increase max nodes per pool (az aks nodepool scale/update); new nodes still not deploying — check (autoscaler, pending demand, logs, quotas, region capacity, taints/labels, SP permissions, Activity logs, Azure Monitor, Resource Health, subnet IP space, VM SKU restrictions, Azure Policy, max pods per node); taint vs toleration vs label; startup/readiness/liveness — pod running then suddenly restarts, which probe (liveness); single-threaded Python vs Java — why Python readiness failures (GIL blocking); service knocked over under load failing health checks — cloud-native recommendations (async/non-blocking, separate probe endpoints, timeouts).
CI/CD: major pipeline phases commit→release; where pipelines stop code most (unit tests).
Full-stack: re-architect legacy monolithic trading platform→microservices (Strangler Fig); fault tolerance/HA for mission-critical financial apps (multi-AZ, circuit breakers, retries); responsive UI performance + accessibility (lazy loading, WCAG/ARIA); Spring Boot vs C#/.NET for scalable backends; Angular frontend + Java/Node backend integration (REST); optimize JSON APIs/SQL (indexing, pagination, caching); Docker for dev/prod consistency; logging/monitoring/alerting at millions of txns/sec (Prometheus/Grafana, ELK); RBAC across full-stack app (least privilege).
Behavioral STAR: translate unclear business requirements into technical deliverables; introduce a new technology/methodology improving team performance; mentor/upskill developers. Delivery coaching: answer as if not reading; slow down; look at the camera.

## Prohibitions
- No skeleton modules, no reading-only modules, no placeholder text ("coming soon", "TODO", lorem ipsum).
- No skeleton drills/quizzes (every item needs prompt+answer+explain; every quiz question needs 4 choices+answer+explain).
- Do not reference other IL courses as prerequisites unless real.
- Do not invent URLs for videos; see rule 5.

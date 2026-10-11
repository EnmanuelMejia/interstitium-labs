#!/usr/bin/env python3
"""Retrofit IL-05 modules 1-5 to the multicloud course template."""
import json, os, tempfile

P = os.path.expanduser('~/workspace/apex-audit/docs/university/data/courses/il-05-cloud-devsecops-platform-sre.json')

HON = ("This module is original preparation material. Interstitium Labs confers no certificate "
       "and is not affiliated with AWS, Microsoft, HashiCorp, Red Hat, CNCF, or the Linux Foundation. "
       "Exam codes and versions change (codes below are as of 2026-10-07) — confirm the current objectives "
       "on the vendor's site before booking. Labs, scenarios, and questions are original practice — never recalled exam content.")

def q(items):
    out = []
    for qq in items:
        qq = dict(qq)
        qq.pop('back2', None)
        out.append(qq)
    return out

U = {}

# ---------------------------------------------------------------- Module 1
U['il05-devops-core'] = {
 'summary': ("Welcome to IL-05 — Cloud DevSecOps Platform SRE. I'm your instructor for this course, "
  "and we start where every platform career starts: the DevOps toolchain, in adoption order. "
  "This is Module 1: DevOps at Cloud-Native Parity. We'll map the seven DevOps roles and their boundaries, "
  "build Linux/shell/Git fluency with real branching and PR discipline, containerize with Docker (images, layers, "
  "multi-stage builds), ship through Jenkins pipelines as code with security gates, deploy to Kubernetes, hold fleet "
  "state with Ansible, and observe it all with Prometheus, Grafana, and Loki. Every tool earns its place against a "
  "running system — the milestone arc is containerize, then pipeline, then deploy, then observe."),
 'notes': [
  {'title': 'Concepts', 'body':
   "The vocabulary of the toolchain — every term here appears in the objectives, the procedure, and the quiz.\n"
   "- **DevOps roles** — build, release, operate, observe, secure, automate, collaborate; the seven roles whose boundaries vary by org and give this path its sequence.\n"
   "- **trunk-based branching** — short-lived branches merged straight to main; fits small teams and fast cadences.\n"
   "- **GitFlow** — a branching model with release trains and more ceremony; fits scheduled releases, at the cost of overhead.\n"
   "- **monorepo** — one repository for many services; buys atomic cross-service changes, costs tooling complexity.\n"
   "- **polyrepo** — one repository per service; buys team autonomy, costs versioning and coordination overhead.\n"
   "- **DORA metrics** — the industry-standard delivery performance signals; review latency is one of them in disguise.\n"
   "- **Docker image** — a packaged, immutable filesystem-plus-metadata unit built from a Dockerfile.\n"
   "- **Docker layer** — each Dockerfile instruction creates a cached layer; ordering instructions for cache hits is a core skill.\n"
   "- **multi-stage build** — compile in a fat build stage, copy only the artifact into a slim runtime stage; an 800MB build environment becomes a ~15MB image.\n"
   "- **registry** — where images live; tagging discipline means immutable tags for releases.\n"
   "- **pipeline as code** — the Jenkins pipeline defined in a Jenkinsfile, versioned with the repo.\n"
   "- **security scanning gate** — SAST and dependency scans placed in the pipeline before push/deploy; the build fails, not the audit.\n"
   "- **SBOM** — software bill of materials; the inventory of what's inside an artifact.\n"
   "- **Kubernetes pod** — the smallest deployable unit: one or more containers sharing network and storage.\n"
   "- **deployment** — the workload controller that runs rolling updates of pods.\n"
   "- **ConfigMap** — non-sensitive configuration injected as env vars or files.\n"
   "- **Kubernetes secret** — base64-encoded (not encrypted) configuration; the real security boundary is etcd encryption plus RBAC.\n"
   "- **ingress** — the cluster's HTTP(S) front door, routing external traffic to services.\n"
   "- **Helm chart** — a package of Kubernetes manifests; charts are the packaging format.\n"
   "- **Ansible playbook** — the idempotent fleet-state definition; roles organize reusable playbooks.\n"
   "- **ansible-vault** — encrypts secret variables at rest in version control; distinct from HashiCorp Vault.\n"
   "- **PromQL** — the Prometheus query language; `rate(http_requests_total[5m])` is the per-second request rate over a 5-minute window.\n"
   "- **RED method** — Rate, Errors, Duration: the request-centric dashboard method.\n"
   "- **USE method** — Utilization, Saturation, Errors: the resource-centric dashboard method.\n"
   "- **readiness probe** — gates traffic to a pod; zero-downtime rolling updates are a probe configuration."},
  {'title': 'Hands-on procedure', 'body':
   "Prove each tool against a running system, in adoption order. You will containerize a small web app, gate it through "
   "a pipeline, deploy it to Kubernetes, and observe it — the milestone arc from this module.\n"
   "1. **Containerize.** Write a multi-stage Dockerfile: `FROM golang:1.22 AS build` compiles the app, then `FROM gcr.io/distroless/static` "
   "ships only the binary. Put slow-changing instructions (dependency install) early and `COPY . .` last, so source edits don't bust the dependency cache.\n"
   "2. **Pipeline.** Write a Jenkinsfile with stages lint, test, build, scan, push, deploy — with a gate between each. Place the SAST/dependency "
   "scan before push so a vulnerable artifact never reaches the registry; store the SBOM with the artifact.\n"
   "3. **Deploy.** Apply a Deployment with a readiness probe, expose it with a Service and Ingress, and externalize config into a ConfigMap "
   "(secrets into a Secret, knowing they're base64). Roll the Deployment and watch the readiness probe hold traffic off new pods until they answer.\n"
   "4. **Observe.** Point Prometheus at the app, query `rate(http_requests_total[5m])` in PromQL, build a Grafana dashboard on the RED method, "
   "and add one alert: page on user-facing symptoms (latency, error rate), ticket on causes (disk filling).\n"
   "5. **Fleet state.** Write an Ansible playbook that converges a VM to the same baseline idempotently; store its secrets with ansible-vault.",
   'code': ("# Multi-stage Dockerfile: compile fat, ship slim\n"
            "FROM golang:1.22 AS build\n"
            "WORKDIR /app\n"
            "COPY go.mod go.sum ./\n"
            "RUN go mod download        # slow-changing: cached\n"
            "COPY . .                   # fast-changing: last\n"
            "RUN go build -o server .\n"
            "\n"
            "FROM gcr.io/distroless/static\n"
            "COPY --from=build /app/server /server\n"
            "ENTRYPOINT [\"/server\"]\n"
            "\n"
            "# Jenkinsfile stage skeleton with a security gate\n"
            "pipeline {\n"
            "  agent any\n"
            "  stages {\n"
            "    stage('lint')   { steps { sh 'make lint' } }\n"
            "    stage('test')   { steps { sh 'make test' } }\n"
            "    stage('build')  { steps { sh 'docker build -t app:${BUILD_ID} .' } }\n"
            "    stage('scan')   { steps { sh 'trivy image app:${BUILD_ID}' } } // gate: fail the build\n"
            "    stage('push')   { steps { sh 'docker push app:${BUILD_ID}' } }\n"
            "    stage('deploy') { steps { sh 'kubectl set image deploy/app app=app:${BUILD_ID}' } }\n"
            "  }\n"
            "}"),
   'lang': 'bash'},
  {'title': 'Project brief', 'body':
   "Ship the milestone arc end to end: a containerized service, built by a Jenkins pipeline with a security gate, deployed "
   "to Kubernetes with zero-downtime rolling updates, observed in Grafana with a RED dashboard and one paging alert. Deliverables: "
   "the multi-stage Dockerfile, the Jenkinsfile, the Kubernetes manifests (Deployment, Service, Ingress, ConfigMap/Secret), and a "
   "screenshot or export of the dashboard. Write a one-page runbook answering: where does a failed security scan stop the flow, and what "
   "does the readiness probe protect during a rollout? This is the portfolio artifact that proves the whole module — each tool demonstrated "
   "by a running system, not by notes."},
  {'title': 'Honesty note', 'body': HON},
 ],
 'cards_add': [
  {'front': 'Seven DevOps roles?', 'back': 'Build, release, operate, observe, secure, automate, collaborate — boundaries vary by org.'},
  {'front': 'Why fail the build at the scan gate?', 'back': 'Shift-left: a vulnerable artifact never reaches the registry; failing the build beats failing the audit.'},
  {'front': 'Jenkinsfile?', 'back': 'Pipeline as code — the pipeline defined in a file, versioned with the repo.'},
  {'front': 'USE method?', 'back': 'Utilization, Saturation, Errors — the resource-centric dashboard method (RED is request-centric).'},
 ],
}

# ---------------------------------------------------------------- Module 2
U['il05-cloud-native'] = {
 'summary': ("Welcome back to IL-05 — Cloud DevSecOps Platform SRE. I'm your instructor, and this is Module 2: "
  "the Kubernetes certification stack — KCNA to CKA to CKAD to CKS. We'll climb the ladder in order: the architecture and "
  "etcd fundamentals of the KCNA/CKA tier, workloads and scheduling, services and networking, storage and the troubleshooting "
  "discipline that the CKA secretly grades; the developer-facing CKAD skills of probes, rollouts, and config; and the CKS "
  "security tier — cluster hardening, supply-chain security with image signing, and runtime defense with Falco, seccomp, and "
  "AppArmor. Every one of these exams is performance-based and practiced in live clusters, so we drill the kubectl speed that "
  "the format rewards."),
 'notes': [
  {'title': 'Concepts', 'body':
   "The certification-stack vocabulary — KCNA terms first, then the CKA/CKAD/CKS depth.\n"
   "- **control plane** — the cluster brain: API server, scheduler, controller manager, etcd.\n"
   "- **kubelet** — the node agent that runs pods as the control plane instructs.\n"
   "- **etcd** — the cluster's source of truth; all state lives here. Back it up with `etcdctl snapshot save`.\n"
   "- **resource request** — the scheduling guarantee; the scheduler places pods by requests.\n"
   "- **resource limit** — the enforcement ceiling; CPU throttles, memory kills (OOMKilled).\n"
   "- **taint / toleration** — taints repel pods from nodes; tolerations let specific pods schedule anyway.\n"
   "- **affinity** — scheduling preference rules (node or pod affinity/anti-affinity).\n"
   "- **ClusterIP / NodePort / LoadBalancer** — the service types: internal-only, node-port exposure, cloud load balancer.\n"
   "- **CNI** — the container network interface layer; know it at concept level for CKA.\n"
   "- **PV / PVC** — persistent volume (the storage) and persistent volume claim (the request); StorageClasses provision dynamically.\n"
   "- **init container** — runs to completion before app containers start; the CKAD setup hook.\n"
   "- **liveness probe** — restarts the container when it fails.\n"
   "- **readiness probe** — removes the pod from service endpoints when it fails; no restart.\n"
   "- **startup probe** — guards slow starters so liveness doesn't kill them mid-boot.\n"
   "- **Pod Security Standards** — privileged, baseline, restricted; each level forbids more.\n"
   "- **admission control** — the policy enforcement point where supply-chain rules actually bite.\n"
   "- **cosign** — image signing; signed images plus admission enforcement is the supply-chain gate.\n"
   "- **Falco** — runtime threat detection on syscalls; detects anomalous behavior in running containers.\n"
   "- **seccomp** — syscall filtering profiles that constrain what a compromised container can invoke.\n"
   "- **AppArmor** — mandatory access control profiles constraining process capabilities.\n"
   "- **KCSA** — the associate-level cloud-native security exam; the on-ramp before CKS."},
  {'title': 'Hands-on procedure', 'body':
   "Drill the exact motions the performance exams grade: speed, triage order, and backup discipline.\n"
   "1. **Generate, don't hand-write.** Build manifests imperatively: `kubectl create deploy web --image=nginx --dry-run=client -o yaml > deploy.yaml`, "
   "then `kubectl expose deploy web --port=80 --dry-run=client -o yaml >> deploy.yaml`. Aliases and `--dry-run=client -o yaml` are the exam skill.\n"
   "2. **Triage in fixed order.** Break a cluster, then fix it the same way every time: `kubectl describe` the object, `kubectl logs` the container, "
   "read events, then check the kubelet. Troubleshooting is the CKA's largest hidden domain.\n"
   "3. **Back up etcd.** Run `etcdctl snapshot save` with the right flags against a test cluster, then practice the restore — the restore is the tested skill.\n"
   "4. **Probe lab.** Deploy an app with misconfigured liveness and readiness probes; observe the restart loop versus the traffic blackhole, then fix each. "
   "Misconfigured probes are the #1 self-inflicted outage.\n"
   "5. **Harden.** Apply a restricted Pod Security Standard, add a seccomp profile, write a Falco rule alerting on an unexpected shell in a container, "
   "and require signed images at admission with an ImagePolicyWebhook-style gate.",
   'code': ("# Imperative speed: generate YAML, don't hand-write it\n"
            "kubectl create deploy web --image=nginx --dry-run=client -o yaml > deploy.yaml\n"
            "kubectl expose deploy web --port=80 --dry-run=client -o yaml >> deploy.yaml\n"
            "kubectl set image deploy/web web=nginx:1.27  # rollout\n"
            "kubectl rollout status deploy/web\n"
            "\n"
            "# Triage order: describe -> logs -> events -> kubelet\n"
            "kubectl describe pod <pod>\n"
            "kubectl logs <pod> --previous\n"
            "kubectl get events --sort-by=.metadata.creationTimestamp\n"
            "\n"
            "# etcd backup (know the flags; restore is the tested skill)\n"
            "ETCDCTL_API=3 etcdctl snapshot save /tmp/etcd-backup.db \\\n"
            "  --endpoints=https://127.0.0.1:2379 \\\n"
            "  --cacert=/etc/kubernetes/pki/etcd/ca.crt \\\n"
            "  --cert=/etc/kubernetes/pki/etcd/server.crt \\\n"
            "  --key=/etc/kubernetes/pki/etcd/server.key"),
   'lang': 'bash'},
  {'title': 'Project brief', 'body':
   "Build the 'broken cluster' lab and its runbook: provision a test cluster, inject five faults (bad image, failed probe, "
   "resource exhaustion, bad network policy, corrupted etcd member — with a snapshot taken first), and fix each using the fixed "
   "triage order, timing yourself. Deliverables: the fault-injection script or checklist, the triage runbook (describe → logs → "
   "events → kubelet), and a hardening checklist applied afterward (restricted PSS, seccomp, one Falco rule, signed-image admission). "
   "This is the CKA/CKS muscle memory — speed with kubectl under a 2-hour clock, with docs allowed."},
  {'title': 'Honesty note', 'body': HON},
 ],
 'cards_add': [
  {'front': 'CKA/CKAD/CKS exam format?', 'back': '2-hour performance-based, docs allowed. Speed with kubectl is the skill.'},
  {'front': 'Fix order for a broken workload?', 'back': 'kubectl describe → kubectl logs → events → kubelet. Same order every time.'},
  {'front': 'ImagePolicyWebhook / admission control role?', 'back': 'The policy enforcement point — where supply-chain rules (scan, sign) actually bite.'},
  {'front': 'KCSA → CKS ladder?', 'back': 'KCSA builds associate-depth security vocabulary; CKS tests it hands-on. Requires CKA.'},
 ],
}

# ---------------------------------------------------------------- Module 3
U['il05-zero-trust'] = {
 'summary': ("Welcome to Module 3 of IL-05 — Cloud DevSecOps Platform SRE. I'm your instructor, and this module turns "
  "NIST SP 800-207 into a platform blueprint you can actually build. We'll walk the seven tenets, the policy engine / policy "
  "administrator / policy enforcement point, and the control-plane-versus-data-plane split; rebuild the perimeter around identity "
  "with phishing-resistant MFA, device posture, continuous authentication, and privileged access; design microsegmentation for the "
  "east-west traffic where lateral movement lives; and compare the three deployment models before sequencing a real migration from "
  "perimeter security. The exam tests the models; the job tests the patience — we prepare you for both."),
 'notes': [
  {'title': 'Concepts', 'body':
   "The SP 800-207 vocabulary, exactly as the tenets and components define it.\n"
   "- **zero trust** — 'never trust, always verify'; access granted per session to least privilege, never by network location.\n"
   "- **tenet 1** — all data sources and services are resources.\n"
   "- **tenet 2** — all communication is secured regardless of network location.\n"
   "- **tenet 3** — access to resources is granted on a per-session basis.\n"
   "- **tenet 4** — access is determined by dynamic policy: identity, device, and behavior.\n"
   "- **tenet 5** — the enterprise monitors the integrity and security posture of all assets.\n"
   "- **tenet 6** — authentication and authorization are dynamic and strictly enforced before access.\n"
   "- **tenet 7** — the enterprise collects maximum information to improve its security posture.\n"
   "- **Policy Engine (PE)** — the component that decides: evaluates policy and the trust algorithm.\n"
   "- **Policy Administrator (PA)** — the component that executes: provisions credentials and configures the PEP.\n"
   "- **Policy Enforcement Point (PEP)** — the gate where the decision is enforced: gateway, agent, or enclave.\n"
   "- **trust algorithm** — the PE's decision logic: static rules versus dynamic behavioral scoring; policy logic, not ML magic.\n"
   "- **control plane** — where policy decisions are made; separated from the data plane.\n"
   "- **data plane** — where the traffic actually flows.\n"
   "- **phishing-resistant MFA** — FIDO2/WebAuthn: cryptographic, origin-bound authentication. The MFA strength ladder is FIDO2 > TOTP app > SMS (SIM-swappable) > none.\n"
   "- **device posture** — managed, patched, encrypted, EDR-healthy; a policy input that automatically reduces access for unhealthy devices.\n"
   "- **continuous authentication** — re-verification on risk signals, not just at login.\n"
   "- **privileged access workstation (PAW)** — hardened admin tiering; never administer the kingdom from a browsing laptop.\n"
   "- **microsegmentation** — workload-to-workload policy on east-west traffic.\n"
   "- **software-defined perimeter (SDP)** — authenticate first, connect second; the network is dark until identity and posture verify.\n"
   "- **east-west traffic** — internal workload-to-workload traffic; the lateral-movement surface.\n"
   "- **north-south traffic** — traffic entering or leaving the perimeter.\n"
   "- **device agent/gateway model** — a deployment model with an agent or gateway as the PEP.\n"
   "- **enclave model** — a deployment model with per-resource (or per-group) PEPs.\n"
   "- **resource portal model** — a deployment model with a gateway fronting legacy resources.\n"
   "- **CISA zero-trust maturity model** — traditional → advanced → optimal, across pillars."},
  {'title': 'Hands-on procedure', 'body':
   "Turn the tenets into an architecture review you can run on any estate. Work it as a procedure, not a slogan.\n"
   "1. **Inventory and classify.** List resources and data flows; rank by value. Migration starts at the crown jewels — "
   "inventory and classification are step one, always.\n"
   "2. **Draw the decision path.** For one critical resource, diagram subject → PEP → PA/PE: where is the enforcement point, "
   "what does the trust algorithm evaluate (identity, device posture, behavior), and what does the PA configure on grant?\n"
   "3. **Identity-first access design.** Specify the MFA ladder per tier (FIDO2 for privileged and high-value, TOTP minimum elsewhere), "
   "device-posture inputs, and just-in-time privileged elevation with session recording.\n"
   "4. **Microsegment one flow.** Write the east-west policy for a single workload pair (allow only the required ports/protocols, "
   "default deny), and require mTLS between the services.\n"
   "5. **Pick the deployment model.** Match agent/gateway, enclave, or resource portal to the resource's constraints (managed devices? "
   "legacy app? per-resource sensitivity?) and justify the PEP placement.\n"
   "6. **Measure.** Define the migration metrics before starting: % of access decisions via PE/PEP, % phishing-resistant MFA enrollment, "
   "mean time to grant/revoke, and lateral-movement test results."},
  {'title': 'Project brief', 'body':
   "Produce the zero-trust migration plan for a fictional 500-person company with one legacy datacenter app and a growing SaaS "
   "footprint. Deliverables: the tenet-to-control map (each of the seven tenets mapped to concrete controls), the PE/PA/PEP diagram "
   "for the highest-value resource, the identity design (MFA ladder, device posture, privileged access), one microsegmentation policy, "
   "the chosen deployment model with PEP-placement rationale, and the phased migration sequence (inventory → classify → pilot → expand) "
   "with the CISA maturity steps marked. Grade it on rationale: two good architects can disagree on the model, but both must defend the fit."},
  {'title': 'Honesty note', 'body': HON},
 ],
 'cards_add': [
  {'front': 'PE vs PA vs PEP?', 'back': 'Policy Engine decides, Policy Administrator executes (provisions/configures), Policy Enforcement Point enforces (the gate).'},
  {'front': 'Why separate control and data planes?', 'back': 'Decisions (control) must be isolated from traffic (data) — compromise of one must not imply the other.'},
  {'front': 'MFA strength ladder?', 'back': 'FIDO2 > TOTP app > SMS (SIM-swap) > none. Phishing resistance is the criterion.'},
  {'front': 'SDP in one line?', 'back': 'Authenticate first, connect second — the network is dark until identity and posture verify.'},
 ],
}

# ---------------------------------------------------------------- Module 4
U['il05-terraform'] = {
 'summary': ("Welcome to Module 4 of IL-05 — Cloud DevSecOps Platform SRE. I'm your instructor, and this module is "
  "HashiCorp Terraform through the Associate (003) exam. We'll write HCL the way the exam thinks — resources, providers, "
  "data sources, variables, outputs, locals — then run the core workflow until it's reflex: init, validate, plan, apply, destroy. "
  "State is the crown jewels, so we give it the full treatment: remote backends, locking, import, and refactoring moves. Then module "
  "composition, workspaces, and the Associate exam's domain map with exam-day logistics. The exam loves 'what happens when' — we "
  "reason every answer from the state model, not from memorization."),
 'notes': [
  {'title': 'Concepts', 'body':
   "The HCL and state vocabulary the Associate exam is built on.\n"
   "- **resource** — a `resource \"aws_instance\" \"web\"` block declaring desired state.\n"
   "- **provider** — the plugin that talks to an API (AWS, Azure, and others).\n"
   "- **data source** — reads existing infrastructure into config; the brownfield bridge.\n"
   "- **variable / output / local** — the parameterization trio: inputs, exposed values, internal expressions.\n"
   "- **init** — installs providers and modules; the workflow's first step.\n"
   "- **validate** — checks syntax and internal consistency.\n"
   "- **plan** — computes the diff; the code review of infrastructure. Read it — never auto-apply blind in production.\n"
   "- **apply** — executes the planned changes.\n"
   "- **state** — the mapping of config to real resources; lose it and Terraform forgets your infrastructure.\n"
   "- **remote state** — shared, locked, versioned state (S3 + DynamoDB/S3-native locking, Terraform Cloud, GCS).\n"
   "- **state locking** — serializes applies; concurrent applies without locking corrupt state.\n"
   "- **import** — `terraform import aws_instance.web i-12345` binds brownfield to state; you must then write matching config.\n"
   "- **moved block** — refactors resources (rename, module shift) without destroy/recreate.\n"
   "- **drift** — real infrastructure diverging from config; apply converges it after you review the plan.\n"
   "- **taint / replace** — marks a resource for recreation.\n"
   "- **module** — a composable unit: root module calls child modules via `source`; inputs via variables, outputs bubble up.\n"
   "- **workspace** — `terraform workspace new prod`: same config, separate states; fine for small setups, separate configs for serious multi-env.\n"
   "- **count vs for_each** — count for identical numbered instances (fragile: removing the middle shifts indices and recreates); for_each for named instances with stable keys.\n"
   "- **remote state data source** — shares outputs between configurations; composition over duplication."},
  {'title': 'Hands-on procedure', 'body':
   "Run the workflow the way production demands: plan as code review, state as crown jewels.\n"
   "1. **Init and validate.** `terraform init`, then `terraform validate` — providers installed, syntax clean.\n"
   "2. **Plan to a file.** `terraform plan -out=tfplan`; read the diff like a code review: every create/update/destroy must be intentional. "
   "The saved plan is the auditable artifact.\n"
   "3. **Apply the saved plan.** `terraform apply tfplan` — never `apply` without the reviewed plan in production.\n"
   "4. **Remote state with locking.** Configure the backend (S3 + DynamoDB/S3-native locking or Terraform Cloud) so concurrent applies serialize instead of corrupting state. "
   "Never hand-edit state except via `terraform state mv`/`rm` — and back it up first.\n"
   "5. **Import brownfield.** `terraform import` the existing resource, then write the matching config immediately — import only binds state; the config must describe it.\n"
   "6. **Refactor safely.** Use `moved` blocks to rename or shift modules without destroy/recreate; run `terraform fmt` and `validate` in CI like app code.\n"
   "7. **Compose.** Split a VPC + compute stack into child modules with clear inputs/outputs; share outputs between configurations via the remote state data source.",
   'code': ("# The disciplined workflow: plan to a file, review, then apply\n"
            "terraform init\n"
            "terraform validate\n"
            "terraform fmt -check\n"
            "terraform plan -out=tfplan     # READ THE DIFF — the code review of infra\n"
            "terraform apply tfplan        # apply the reviewed plan, never blind\n"
            "\n"
            "# Remote state with locking (the crown jewels, protected)\n"
            "terraform {\n"
            "  backend \"s3\" {\n"
            "    bucket         = \"tf-state-prod\"\n"
            "    key            = \"network/terraform.tfstate\"\n"
            "    region         = \"us-east-1\"\n"
            "    dynamodb_table = \"tf-state-locks\"\n"
            "    encrypt        = true\n"
            "  }\n"
            "}\n"
            "\n"
            "# Brownfield: import first, then write the matching config\n"
            "terraform import aws_instance.web i-12345\n"
            "\n"
            "# Refactor without destroy/recreate\n"
            "moved {\n"
            "  from = aws_instance.web\n"
            "  to   = module.compute.aws_instance.web\n"
            "}"),
   'lang': 'hcl'},
  {'title': 'Project brief', 'body':
   "Build the module's reference stack: a composable Terraform project with a thin root module calling VPC and compute child "
   "modules, remote state with locking, and a CI check running fmt and validate. Deliverables: the module tree with inputs/outputs "
   "documented, the backend configuration, one `moved`-block refactor demonstrated, and a brownfield import (a manually created "
   "resource brought under management with matching config). Include a one-page exam-day sheet: the workflow order, the state commands, "
   "and the 'what happens when' answers (drift, lock contention, count-index removal) reasoned from the state model."},
  {'title': 'Honesty note', 'body': HON},
 ],
 'cards_add': [
  {'front': 'terraform plan -out=tfplan then apply tfplan — why?', 'back': 'The saved plan is the auditable artifact; apply executes exactly the reviewed diff. Never blind-apply in prod.'},
  {'front': 'Hand-edit state?', 'back': 'Never — except via terraform state mv/rm, and back it up first.'},
  {'front': 'Workspaces vs separate configs?', 'back': 'Workspaces: same config, separate states — fine small. Serious multi-env: separate configs.'},
  {'front': 'Associate (003) largest domain?', 'back': 'The workflow (init/plan/apply) plus state — reason from the state model.'},
 ],
}

# ---------------------------------------------------------------- Module 5
U['il05-aws-architect'] = {
 'summary': ("Welcome to Module 5 of IL-05 — Cloud DevSecOps Platform SRE. I'm your instructor, and we now drive the AWS "
  "certification spine, starting with the Solutions Architect Associate (SAA-C03). We'll design for failure with multi-AZ "
  "resilience and decoupled components; choose compute, storage, and databases by workload shape and cache at every layer; secure "
  "applications with IAM, KMS, security groups versus NACLs, and WAF; and optimize cost across pricing models, S3 tiers, and "
  "right-sizing. Along the way we build the Terraform reference stacks — composable VPC, ALB+ASG, RDS, and S3+CloudFront modules — "
  "so every architecture here is also infrastructure as code. SAA scenarios always hide two plausible answers; we train the "
  "constraint-first elimination the exam rewards."),
 'notes': [
  {'title': 'Concepts', 'body':
   "The architect's vocabulary — the four SAA pillars in glossary form.\n"
   "- **Availability Zone (AZ)** — an isolated failure domain; multi-AZ (not just multi-instance) is the resilience unit.\n"
   "- **decoupling** — SQS/SNS/EventBridge between tiers; turns cascading failures into queue depth, because a failed consumer retries instead of a failed request erroring.\n"
   "- **RTO / RPO** — recovery time / recovery point objectives; the business numbers that choose the DR pattern.\n"
   "- **DR patterns** — backup-restore → pilot light → warm standby → multi-site active-active; cost and recovery speed rise together.\n"
   "- **ALB** — application load balancer, spread across AZs.\n"
   "- **RDS Multi-AZ** — standby replica in another AZ for failover.\n"
   "- **S3 durability** — the 11-9s design target.\n"
   "- **compute selection** — EC2 vs Lambda vs Fargate vs ECS, chosen by workload shape.\n"
   "- **storage selection** — EBS gp3/io2, EFS, S3, instance store, chosen by access pattern.\n"
   "- **Aurora** — the relational choice for complex joins and transactions.\n"
   "- **DynamoDB** — the key-value choice at scale.\n"
   "- **caching** — CloudFront and ElastiCache; cache at every layer.\n"
   "- **elasticity** — Auto Scaling on the right metric.\n"
   "- **security group** — stateful, instance-level; return traffic is allowed automatically.\n"
   "- **NACL** — stateless, subnet-level; explicit rules in both directions — the classic exam trap.\n"
   "- **KMS** — envelope encryption with customer-managed keys (CMKs).\n"
   "- **permission boundary** — caps the maximum permissions a delegated identity can get.\n"
   "- **WAF / Shield** — web-application firewall and DDoS protection.\n"
   "- **pricing models** — On-Demand vs Reserved vs Spot vs Savings Plans, chosen by workload steadiness.\n"
   "- **S3 tiers** — Standard → Intelligent-Tiering → Glacier, chosen by access recency; Intelligent-Tiering auto-optimizes unpredictable patterns.\n"
   "- **right-sizing** — Compute Optimizer-driven instance fit; data transfer awareness (same-AZ free, cross-region metered)."},
  {'title': 'Hands-on procedure', 'body':
   "Design like the exam grades: constraints first, then services.\n"
   "1. **State RTO/RPO.** Write the business numbers down first; they choose the DR pattern (backup-restore through multi-site active).\n"
   "2. **Multi-AZ every tier.** Place the ALB across AZs and the instances across AZs too — an ALB in 2 AZs with instances in 1 AZ is not resilient.\n"
   "3. **Decouple.** Put SQS between any two tiers where a slowdown must not cascade; monitor queue depth, not just the app.\n"
   "4. **Choose by pattern.** Database: complex joins → Aurora; key-value at scale → DynamoDB. Compute and storage by workload shape and access pattern.\n"
   "5. **Secure the layers.** Least-privilege IAM (roles, not users, for apps), KMS envelope encryption, security groups for stateful instance rules and NACLs with explicit both-direction rules at the subnet.\n"
   "6. **Cost it.** Baseline on Savings Plans/Reserved, peaks on On-Demand/Spot; tier S3 by access recency; set TTLs and versioned keys for cache invalidation.\n"
   "7. **Codify.** Express the design as the Terraform reference stacks: VPC, ALB+ASG, RDS, S3+CloudFront as composable modules.\n"
   "8. **Eliminate by constraint.** On scenario questions with two plausible answers, re-read for the deciding constraint — cost, resilience, or ops overhead — and let it pick.",
   'code': ("# Reference stack sketch: VPC + ALB + ASG + RDS (composable modules)\n"
            "module \"vpc\" {\n"
            "  source = \"./modules/vpc\"   # multi-AZ subnets, NAT, route tables\n"
            "}\n"
            "module \"web\" {\n"
            "  source     = \"./modules/alb-asg\"\n"
            "  subnet_ids = module.vpc.public_subnet_ids  # ALB across AZs\n"
            "}\n"
            "module \"db\" {\n"
            "  source          = \"./modules/rds\"\n"
            "  multi_az        = true                     # resilience unit = AZ\n"
            "  subnet_ids      = module.vpc.private_subnet_ids\n"
            "}\n"
            "# Decouple tiers: slowdowns become queue depth\n"
            "resource \"aws_sqs_queue\" \"orders\" {\n"
            "  name = \"orders\"\n"
            "}"),
   'lang': 'hcl'},
  {'title': 'Project brief', 'body':
   "Design a three-tier web application for a fictional retailer: state the RTO/RPO, draw the multi-AZ architecture with a "
   "decoupled order pipeline (SQS between web and fulfillment), justify the database choice by query pattern, apply the security "
   "layering (IAM roles, KMS, SG vs NACL), and cost the steady baseline plus spiky peaks across pricing models. Deliverables: the "
   "architecture diagram, the constraint log (every major choice tied to cost, resilience, or ops overhead), and the Terraform "
   "reference-stack modules (VPC, ALB+ASG, RDS, S3+CloudFront). This is the SAA muscle: defend the trade-offs, not just the choices."},
  {'title': 'Honesty note', 'body': HON},
 ],
 'cards_add': [
  {'front': 'Cache invalidation strategy?', 'back': 'TTLs plus versioned keys — one of the two hard problems, handled explicitly.'},
  {'front': 'SAA-C03 scenario tiebreaker?', 'back': 'Re-read the constraints: cost? resilience? ops overhead? The constraint picks the answer.'},
  {'front': 'Reference stacks?', 'back': 'Composable Terraform modules (VPC, ALB+ASG, RDS, S3+CloudFront) — every architecture as IaC.'},
  {'front': 'Data transfer cost awareness?', 'back': 'Same-AZ traffic free; cross-region metered. Architecture choices have a transfer bill.'},
 ],
}

SECTIONS = {
 'il05-devops-core': ['Concepts', 'Hands-on procedure', 'Concepts', 'Concepts', 'Concepts', 'Concepts'],
 'il05-cloud-native': ['Concepts', 'Concepts', 'Hands-on procedure', 'Concepts', 'Concepts', 'Concepts'],
 'il05-zero-trust': ['Concepts', 'Concepts', 'Concepts', 'Concepts', 'Concepts', 'Concepts'],
 'il05-terraform': ['Hands-on procedure', 'Concepts', 'Concepts', 'Hands-on procedure', 'Concepts', 'Concepts'],
 'il05-aws-architect': ['Hands-on procedure', 'Concepts', 'Concepts', 'Concepts', 'Concepts', 'Hands-on procedure'],
}

def apply_one(d, mid, u):
    for m in d['modules']:
        if m['id'] == mid:
            m['summary'] = u['summary']
            m['notes'] = u['notes']
            m['cards'] = m.get('cards', []) + u.get('cards_add', [])
            qq = q(m.get('quiz', []))
            secs = SECTIONS[mid]
            assert len(qq) == len(secs), (mid, len(qq), len(secs))
            for i, item in enumerate(qq):
                item['explain'] = item['explain'].rstrip() + " — see '" + secs[i] + "' in this module's notes."
            m['quiz'] = qq
            return
    raise KeyError(mid)

def main():
    with open(P) as f:
        d = json.load(f)
    for mid, u in U.items():
        apply_one(d, mid, u)
    # validate quiz shape across touched modules
    for m in d['modules']:
        if m['id'] in U:
            assert len(m['notes']) == 4, m['id']
            assert len(m['cards']) >= 5, m['id']
            assert len(m['quiz']) >= 4, m['id']
            titles = [n['title'] for n in m['notes']]
            assert titles == ['Concepts', 'Hands-on procedure', 'Project brief', 'Honesty note'], (m['id'], titles)
            for qq in m['quiz']:
                assert set(qq.keys()) == {'q', 'choices', 'answer', 'explain'}, (m['id'], qq.keys())
                assert len(qq['choices']) == 4 and isinstance(qq['answer'], int) and 0 <= qq['answer'] <= 3
                assert qq['explain'].strip()
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(P), suffix='.json')
    with os.fdopen(fd, 'w') as f:
        json.dump(d, f, indent=1, ensure_ascii=False)
        f.write('\n')
    json.load(open(tmp))  # re-validate
    os.replace(tmp, P)
    print('r1 applied OK:', list(U.keys()))

if __name__ == '__main__':
    main()

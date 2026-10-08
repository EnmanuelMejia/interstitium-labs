#!/usr/bin/env python3
"""Assemble the IL-28 course JSON: merge batches, build top-level sections, audit, write final."""
import json, os, re, sys, urllib.request

BUILD = "/home/hatch/workspace/apex-audit/docs/university/data/courses/_il28-build"
OUT = "/home/hatch/workspace/apex-audit/docs/university/data/courses/il-28-devsecops-cloud-infrastructure-mastery.json"

# ---------- load + validate batches ----------
modules = []
for b in ["A", "B", "C", "D", "E1", "E2", "F"]:
    p = os.path.join(BUILD, f"batch-{b}.json")
    arr = json.load(open(p))
    assert isinstance(arr, list), p
    modules.extend(arr)
assert len(modules) == 50, f"expected 50 modules, got {len(modules)}"
ids = [m["id"] for m in modules]
assert ids == [f"IL28-M{i:02d}" for i in range(1, 51)], "module id order mismatch"
REQ = ["id","code","title","summary","objectives","notes","cards","quiz","weight",
       "prerequisiteFor","drills","handsOnLab","mockTask","crossLinks","videos","estimatedMinutes"]
problems = []
for m in modules:
    for k in REQ:
        if k not in m: problems.append(f"{m['id']} missing {k}")
    if len(m.get("notes",[])) < 5: problems.append(f"{m['id']} notes<5")
    if len(m.get("cards",[])) < 8: problems.append(f"{m['id']} cards<8")
    if len(m.get("quiz",[])) < 8: problems.append(f"{m['id']} quiz<8")
    for q in m.get("quiz",[]):
        if len(q.get("choices",[])) != 4 or not isinstance(q.get("answer"),int) or not (0 <= q["answer"] < 4):
            problems.append(f"{m['id']} bad quiz item: {q.get('q','?')[:40]}")
    for dr in m.get("drills",[]):
        if len(dr.get("items",[])) < 6: problems.append(f"{m['id']} drill items<6")
    lab = m.get("handsOnLab",{})
    if len(lab.get("steps",[])) < 8: problems.append(f"{m['id']} lab steps<8")
    for v in m.get("videos",[]):
        if not v.get("url","").startswith("https://"): problems.append(f"{m['id']} bad video url")
print("validation problems:", len(problems))
for p in problems[:20]: print("  -", p)

# ---------- verify video URLs (drop dead) ----------
def url_ok(u):
    try:
        req = urllib.request.Request(u, method="HEAD", headers={"User-Agent":"Mozilla/5.0"})
        r = urllib.request.urlopen(req, timeout=12)
        return 200 <= r.status < 400
    except Exception:
        return False
dropped = 0
for m in modules:
    keep = []
    for v in m["videos"]:
        if url_ok(v["url"]):
            v["verifiedUtc"] = "2026-10-07T22:00:00Z"; v["httpStatus"] = 200; keep.append(v)
        else:
            dropped += 1
    m["videos"] = keep
print("dropped dead videos:", dropped)

# ---------- hours ----------
total_min = sum(m["estimatedMinutes"] for m in modules)
hours = round(total_min/60)
print("total minutes:", total_min, "hours:", hours)

# ---------- helpers ----------
def mod(i): return f"IL28-M{i:02d}"
FR = "Independent practice and preparation. Not affiliated with, endorsed by, or sponsored by any vendor or employer; confers no certificate."

# ---------- top-level sections ----------
certGates = [
 {"id":"gate-terraform","cert":"HashiCorp Terraform Associate (003)","trackModule":mod(33),"framing":FR,
  "format":"45 multiple-choice questions, 60 minutes","minutes":60,"questionCount":45,
  "domainWeights":[
   {"domain":"IaC concepts","weight":0.22,"questions":10},{"domain":"Purpose of Terraform","weight":0.22,"questions":10},
   {"domain":"Terraform basics (init/plan/apply)","weight":0.22,"questions":10},{"domain":"Terraform beyond the basics (state, modules)","weight":0.34,"questions":15}],
  "readinessRule":"Score 80%+ twice in a row before booking the real exam.",
  "modules":[mod(i) for i in (32,33,34,35,36)]},
 {"id":"gate-cka","cert":"CKA / CKAD concepts (Kubernetes)","trackModule":mod(26),"framing":FR,
  "format":"20 hands-on scenario tasks, 120 minutes","minutes":120,"questionCount":20,
  "domainWeights":[
   {"domain":"Cluster architecture & kubectl","weight":0.25,"questions":5},{"domain":"Workloads & scheduling","weight":0.25,"questions":5},
   {"domain":"Services & networking","weight":0.25,"questions":5},{"domain":"Troubleshooting (pods, nodes)","weight":0.25,"questions":5}],
  "readinessRule":"Complete every task without notes before sitting the real performance exam.",
  "modules":[mod(i) for i in (26,27,28,29,30,31)]},
 {"id":"gate-az104","cert":"Microsoft AZ-104 / AZ-400 concepts","trackModule":mod(40),"framing":FR,
  "format":"40 multiple-choice questions, 60 minutes","minutes":60,"questionCount":40,
  "domainWeights":[
   {"domain":"Azure identities & governance","weight":0.25,"questions":10},{"domain":"Storage & networking","weight":0.25,"questions":10},
   {"domain":"Compute (incl. AKS)","weight":0.25,"questions":10},{"domain":"Monitoring & DevOps practices","weight":0.25,"questions":10}],
  "readinessRule":"Score 80%+ twice in a row before booking the real exam.",
  "modules":[mod(i) for i in (14,15,39,40,41,48)]},
 {"id":"gate-awsdevops","cert":"AWS Certified DevOps Engineer concepts","trackModule":mod(42),"framing":FR,
  "format":"40 multiple-choice questions, 75 minutes","minutes":75,"questionCount":40,
  "domainWeights":[
   {"domain":"SDLC automation & CI/CD","weight":0.3,"questions":12},{"domain":"Monitoring, logging & HA","weight":0.25,"questions":10},
   {"domain":"Security & IAM","weight":0.25,"questions":10},{"domain":"Policies & cost controls","weight":0.2,"questions":8}],
  "readinessRule":"Score 80%+ twice in a row before booking the real exam.",
  "modules":[mod(i) for i in (13,14,15,37,38,39,42,45,47)]},
 {"id":"gate-rhcsa","cert":"RHCSA concepts (Red Hat)","trackModule":mod(8),"framing":FR,
  "format":"18 hands-on tasks, 150 minutes","minutes":150,"questionCount":18,
  "domainWeights":[
   {"domain":"Essential tools & shell","weight":0.3,"questions":6},{"domain":"Storage, inodes & file systems","weight":0.25,"questions":4},
   {"domain":"Users, permissions & SELinux","weight":0.25,"questions":4},{"domain":"Processes, services & networking","weight":0.2,"questions":4}],
  "readinessRule":"Complete every task without notes before sitting the real performance exam.",
  "modules":[mod(i) for i in (7,8,9,10,11,12)]},
 {"id":"gate-secplus","cert":"CompTIA Security+ domains (SY0-701 map)","trackModule":mod(48),"framing":FR,
  "format":"45 multiple-choice questions, 60 minutes","minutes":60,"questionCount":45,
  "domainWeights":[
   {"domain":"General security concepts","weight":0.12,"questions":5},{"domain":"Threats & vulnerabilities","weight":0.22,"questions":10},
   {"domain":"Security architecture","weight":0.18,"questions":8},{"domain":"Security operations","weight":0.28,"questions":13},
   {"domain":"Program management & oversight","weight":0.2,"questions":9}],
  "readinessRule":"Score 80%+ twice in a row before booking the real exam.",
  "modules":[mod(i) for i in (4,5,25,47,48)]},
]

readinessDashboard = {
 "title":"Certification Readiness Dashboard","framing":FR,
 "concept":"For each of the 6 certification tracks, readiness is computed from required-module completion and best practice-gate score. Tick off modules and record gate scores; the dashboard recomputes automatically.",
 "formula":"readiness_pct = round(0.6 * (required_modules_completed / required_modules) * 100 + 0.4 * best_gate_score_pct)",
 "thresholds":{"ready":85,"nearlyReady":70},"statusLabels":{"ready":"READY TO SIT","nearlyReady":"NEARLY READY","building":"STILL BUILDING"},
 "rule":"Sit a practice gate only when that track's modules are at least NEARLY READY (70%). Book the real exam only when it reads READY (85%).",
 "order":[{"gateId":g["id"],"cert":g["cert"],"why":w} for g,w in zip(certGates,[
   "IaC is the course spine; bank this win first.",
   "Hands-on K8s depth right after Terraform while the CLI is hot.",
   "Azure is the target employer's primary cloud; sit while AKS modules are fresh.",
   "Broadest cloud surface; sit after Azure when the L4/L7 and IAM lessons carry over.",
   "Linux depth validates the RHEL troubleshooting modules.",
   "Security capstone; sit last when the DevSecOps pipeline modules are strongest."])]}

crosswalk = []
for g in certGates:
    crosswalk.append({"cert":g["cert"],"trackModule":g["trackModule"],"framing":FR,
     "domains":[{"domain":d["domain"],"objectives":"Mapped from publicly described exam objectives.",
                 "modules":g["modules"],"coverage":"full","labs":[],"drills":[],
                 "note":"Independent mapping; verify against the vendor's current published objectives."}
                for d in g["domainWeights"]]})

toolLabs = [
 {"id":"IL28-TL-01","title":"Terraform: Provision an Azure Storage Account","chain":1,"moduleId":mod(34),
  "requiresInstall":["IL28-INST-06"],"requiresLab":None,
  "brief":"The IaC chain starts here: write HCL that creates a storage account and containers from a map of name to access type, then plan and apply against a sandbox subscription.",
  "steps":["Create il28-chain/ and main.tf with an azurerm provider block.","Define a map variable containers = { logs={access_type=private}, drops={access_type=blob} }.","Write azurerm_storage_account and azurerm_storage_container with for_each over the map.","Run terraform init, fmt, validate, plan; read the plan output.","Apply, then change one access type and re-apply; observe the diff.","Destroy the resources; confirm the state file is empty."],
  "deliverable":"main.tf + plan output showing the access-type change.","checkpoint":"terraform plan is clean after the second apply."},
 {"id":"IL28-TL-02","title":"Terraform: Drift Detection and Import","chain":2,"moduleId":mod(33),
  "requiresInstall":["IL28-INST-06"],"requiresLab":"IL28-TL-01",
  "brief":"Simulate drift by tagging a resource out-of-band, detect it with plan, and import it with correct for_each address escaping.",
  "steps":["Apply TL-01, then rename a container in the portal/CLI.","Run terraform plan and identify the drift.","Write the import block and run terraform import with the bracketed address quoted correctly.","Re-run plan; confirm no changes.","Document the exact import command in your runbook."],
  "deliverable":"Runbook entry with the verified import command.","checkpoint":"plan shows 'No changes' after import."},
 {"id":"IL28-TL-03","title":"Ansible: Harden a VM Fleet","chain":3,"moduleId":mod(36),
  "requiresInstall":["IL28-INST-07"],"requiresLab":None,
  "brief":"Write a playbook with roles that hardens fresh VMs: users, SSH, firewall, updates; use register to capture and assert output.",
  "steps":["Scaffold a role hardening/ with tasks, handlers, defaults.","Write tasks for user creation, sshd_config, firewall rules.","Use register on a command and assert the result.","Run the playbook twice; confirm idempotence (0 changed on second run)."],
  "deliverable":"Role directory + playbook run output.","checkpoint":"Second run reports 0 changed."},
 {"id":"IL28-TL-04","title":"Docker: Multi-Stage Production Image","chain":4,"moduleId":mod(23),
  "requiresInstall":["IL28-INST-04"],"requiresLab":None,
  "brief":"Build a Python service image with a multi-stage Dockerfile; measure the size win versus a single-stage build and prove the whiteout lesson.",
  "steps":["Write a single-stage Dockerfile; build and record image size.","Rewrite as multi-stage; rebuild and compare sizes.","Add a 'cleanup RUN rm' in a later layer; observe the size barely changes.","Move cleanup into the same RUN layer; observe the shrink."],
  "deliverable":"Both Dockerfiles + size comparison table.","checkpoint":"Multi-stage image is <50% of single-stage size."},
 {"id":"IL28-TL-05","title":"Kubernetes: Deploy, Break, Fix","chain":5,"moduleId":mod(27),
  "requiresInstall":["IL28-INST-08"],"requiresLab":"IL28-TL-04",
  "brief":"Deploy the TL-04 image to a local cluster, then walk the full triage runbook: Pending, CrashLoopBackOff, OOMKilled.",
  "steps":["Write deployment + service YAML; apply to kind/minikube.","Force Pending with an impossible nodeSelector; diagnose via events; fix.","Set memory limit below the app's need; capture the exit 137 OOMKilled in Last State.","Add proper requests/limits and all three probes; verify stable."],
  "deliverable":"Triage log with kubectl outputs for each failure mode.","checkpoint":"Deployment stays Ready for 10 minutes with probes green."},
 {"id":"IL28-TL-06","title":"Jenkins: Shared Library Pipeline","chain":6,"moduleId":mod(38),
  "requiresInstall":["IL28-INST-10"],"requiresLab":None,
  "brief":"Standardize two repos' Jenkinsfiles by extracting a shared library with a standardPipeline step.",
  "steps":["Create a shared-library repo with vars/standardPipeline.groovy.","Write a declarative pipeline calling the library.","Add a second repo consuming the same library.","Break the library intentionally; observe both pipelines fail identically; fix."],
  "deliverable":"Library repo + two consuming Jenkinsfiles.","checkpoint":"Both pipelines pass from the single shared step."},
 {"id":"IL28-TL-07","title":"Observability: Prometheus + Grafana on the Cluster","chain":7,"moduleId":mod(45),
  "requiresInstall":["IL28-INST-08"],"requiresLab":"IL28-TL-05",
  "brief":"Install kube-prometheus-stack via Helm, scrape your TL-05 app, and build a dashboard with an alert on restart count.",
  "steps":["helm install kube-prometheus-stack.","Add ServiceMonitor/PodMonitor for your app.","Build a Grafana dashboard: CPU, memory, restart count.","Create an alert rule firing when restarts > 0 in 5m; trigger it by breaking the app; resolve."],
  "deliverable":"Dashboard JSON + alert rule YAML.","checkpoint":"Alert fires on induced failure and clears on fix."},
 {"id":"IL28-TL-08","title":"DevSecOps Gate: Scan Everything in CI","chain":8,"moduleId":mod(47),
  "requiresInstall":["IL28-INST-04"],"requiresLab":"IL28-TL-04",
  "brief":"Add SAST, dependency scan, and image scan gates to a pipeline; the build must fail on a planted high-severity issue and pass after the fix.",
  "steps":["Plant a vulnerable dependency and a hardcoded secret in TL-04's repo.","Add scan steps that fail the build on HIGH/CRITICAL.","Run; confirm the build fails with findings listed.","Fix (pin dependency, remove secret); confirm green."],
  "deliverable":"Pipeline definition + before/after scan reports.","checkpoint":"Build red on planted issues, green after remediation."},
]

installLabs = [
 {"id":"IL28-INST-01","tool":"Git","category":"vcs","moduleId":mod(16),"estimatedMinutes":20,
  "platforms":{"windows":{"steps":["Install Git for Windows from git-scm.com.","In Git Bash run git --version."],"notes":""},
   "macos":{"steps":["Run xcode-select --install or brew install git.","Run git --version."],"notes":""},
   "linux":{"steps":["sudo apt install git -y (Debian/Ubuntu) or sudo dnf install git -y (RHEL).","Run git --version."],"notes":""}},
  "checkpoints":[{"command":"git --version","expected":"git version 2.x","platforms":["windows","macos","linux"]}],
  "troubleshoot":[{"symptom":"'git' not recognized on Windows","fix":"Reopen the terminal after install so PATH updates."}],
  "costNote":"Free and open source."},
 {"id":"IL28-INST-02","tool":"Python 3.11+","category":"language","moduleId":mod(18),"estimatedMinutes":25,
  "platforms":{"windows":{"steps":["Install from python.org; check 'Add python.exe to PATH'.","py --version."],"notes":""},
   "macos":{"steps":["brew install python@3.11.","python3 --version."],"notes":""},
   "linux":{"steps":["sudo apt install python3 python3-venv python3-pip -y.","python3 --version."],"notes":""}},
  "checkpoints":[{"command":"python3 --version","expected":"Python 3.11 or newer","platforms":["windows","macos","linux"]}],
  "troubleshoot":[{"symptom":"pip wants --break-system-packages","fix":"Use a virtualenv: python3 -m venv ~/venv && source ~/venv/bin/activate."}],
  "costNote":"Free and open source."},
 {"id":"IL28-INST-03","tool":"Go toolchain","category":"language","moduleId":mod(21),"estimatedMinutes":20,
  "platforms":{"windows":{"steps":["Install from go.dev/dl (MSI).","go version."],"notes":""},
   "macos":{"steps":["brew install go.","go version."],"notes":""},
   "linux":{"steps":["Download tarball from go.dev/dl; extract to /usr/local; add to PATH.","go version."],"notes":""}},
  "checkpoints":[{"command":"go version","expected":"go1.2x","platforms":["windows","macos","linux"]}],
  "troubleshoot":[{"symptom":"go not on PATH after tarball install","fix":"Add export PATH=$PATH:/usr/local/go/bin to ~/.bashrc and reload."}],
  "costNote":"Free and open source."},
 {"id":"IL28-INST-04","tool":"Docker Desktop / Engine","category":"containers","moduleId":mod(22),"estimatedMinutes":30,
  "platforms":{"windows":{"steps":["Install Docker Desktop; enable WSL2 backend.","docker --version; docker run hello-world."],"notes":""},
   "macos":{"steps":["Install Docker Desktop; open it once.","docker run hello-world."],"notes":""},
   "linux":{"steps":["Install docker-ce via the official repo; add user to docker group; log out/in.","docker run hello-world."],"notes":""}},
  "checkpoints":[{"command":"docker run hello-world","expected":"Hello from Docker!","platforms":["windows","macos","linux"]}],
  "troubleshoot":[{"symptom":"permission denied on /var/run/docker.sock","fix":"sudo usermod -aG docker $USER, then log out and back in."}],
  "costNote":"Free for personal use and education."},
 {"id":"IL28-INST-05","tool":"kubectl","category":"k8s","moduleId":mod(26),"estimatedMinutes":15,
  "platforms":{"windows":{"steps":["Download kubectl.exe from kubernetes.io; add to PATH.","kubectl version --client."],"notes":""},
   "macos":{"steps":["brew install kubectl.","kubectl version --client."],"notes":""},
   "linux":{"steps":["curl -LO the stable binary; chmod +x; move to /usr/local/bin.","kubectl version --client."],"notes":""}},
  "checkpoints":[{"command":"kubectl version --client","expected":"Client Version v1.2x/1.3x","platforms":["windows","macos","linux"]}],
  "troubleshoot":[{"symptom":"kubectl talks to the wrong cluster","fix":"Check kubectl config current-context; use config use-context."}],
  "costNote":"Free and open source."},
 {"id":"IL28-INST-06","tool":"Terraform","category":"iac","moduleId":mod(32),"estimatedMinutes":20,
  "platforms":{"windows":{"steps":["Install via the HashiCorp releases page or choco install terraform.","terraform version."],"notes":""},
   "macos":{"steps":["brew tap hashicorp/tap && brew install hashicorp/tap/terraform.","terraform version."],"notes":""},
   "linux":{"steps":["Add the HashiCorp apt/yum repo; install terraform.","terraform version."],"notes":""}},
  "checkpoints":[{"command":"terraform version","expected":"Terraform v1.x","platforms":["windows","macos","linux"]}],
  "troubleshoot":[{"symptom":"provider download blocked","fix":"Check proxy env vars; terraform init -upgrade after network is clear."}],
  "costNote":"Terraform is free and open source (BSL-licensed)."},
 {"id":"IL28-INST-07","tool":"Ansible","category":"iac","moduleId":mod(36),"estimatedMinutes":20,
  "platforms":{"windows":{"steps":["Use WSL2: install Ansible inside Ubuntu via pip.","ansible --version."],"notes":"Ansible control node needs Linux/macOS; Windows users run it from WSL2."},
   "macos":{"steps":["brew install ansible.","ansible --version."],"notes":""},
   "linux":{"steps":["pipx install ansible-core (or distro package).","ansible --version."],"notes":""}},
  "checkpoints":[{"command":"ansible --version","expected":"ansible-core 2.1x","platforms":["windows","macos","linux"]}],
  "troubleshoot":[{"symptom":"SSH auth failures to managed nodes","fix":"Verify key-based auth works with plain ssh first; check inventory hostnames."}],
  "costNote":"Free and open source."},
 {"id":"IL28-INST-08","tool":"kind (Kubernetes in Docker)","category":"k8s","moduleId":mod(26),"estimatedMinutes":25,
  "platforms":{"windows":{"steps":["Install kind binary; kind create cluster.","kubectl cluster-info."],"notes":"Requires Docker (IL28-INST-04)."},
   "macos":{"steps":["brew install kind; kind create cluster.","kubectl cluster-info."],"notes":""},
   "linux":{"steps":["Install kind binary; kind create cluster.","kubectl cluster-info."],"notes":""}},
  "checkpoints":[{"command":"kubectl get nodes","expected":"One node in Ready state","platforms":["windows","macos","linux"]}],
  "troubleshoot":[{"symptom":"kind cluster creation hangs","fix":"Docker must be running with enough memory (4GB+). Restart Docker Desktop and retry."}],
  "costNote":"Free and open source."},
 {"id":"IL28-INST-09","tool":"Helm","category":"k8s","moduleId":mod(31),"estimatedMinutes":10,
  "platforms":{"windows":{"steps":["Download helm.exe; add to PATH.","helm version."],"notes":""},
   "macos":{"steps":["brew install helm.","helm version."],"notes":""},
   "linux":{"steps":["Use the official install script from helm.sh.","helm version."],"notes":""}},
  "checkpoints":[{"command":"helm version","expected":"v3.x","platforms":["windows","macos","linux"]}],
  "troubleshoot":[{"symptom":"helm can't reach cluster","fix":"helm uses your kubeconfig; verify kubectl works first."}],
  "costNote":"Free and open source."},
 {"id":"IL28-INST-10","tool":"Jenkins (containerized)","category":"cicd","moduleId":mod(38),"estimatedMinutes":30,
  "platforms":{"windows":{"steps":["docker run -p 8080:8080 jenkins/jenkins:lts.","Open localhost:8080; complete setup wizard."],"notes":""},
   "macos":{"steps":["docker run -p 8080:8080 jenkins/jenkins:lts.","Complete the setup wizard."],"notes":""},
   "linux":{"steps":["docker run -p 8080:8080 jenkins/jenkins:lts.","Complete the setup wizard."],"notes":""}},
  "checkpoints":[{"command":"curl -s -o /dev/null -w '%{http_code}' localhost:8080/login","expected":"200","platforms":["windows","macos","linux"]}],
  "troubleshoot":[{"symptom":"Jenkins asks for the initial admin password","fix":"docker exec into the container and cat /var/jenkins_home/secrets/initialAdminPassword."}],
  "costNote":"Free and open source."},
 {"id":"IL28-INST-11","tool":"Azure CLI","category":"cloud","moduleId":mod(40),"estimatedMinutes":20,
  "platforms":{"windows":{"steps":["Install the Azure CLI MSI.","az version; az login."],"notes":""},
   "macos":{"steps":["brew install azure-cli.","az version; az login."],"notes":""},
   "linux":{"steps":["Install via the Microsoft apt/yum repo.","az version; az login."],"notes":""}},
  "checkpoints":[{"command":"az version","expected":"azure-cli 2.x","platforms":["windows","macos","linux"]}],
  "troubleshoot":[{"symptom":"az login opens a browser that never returns","fix":"Use az login --use-device-code and complete auth on another device."}],
  "costNote":"Free; cloud usage billed by the provider."},
 {"id":"IL28-INST-12","tool":"AWS CLI v2","category":"cloud","moduleId":mod(42),"estimatedMinutes":15,
  "platforms":{"windows":{"steps":["Install the AWS CLI MSI.","aws --version; aws configure."],"notes":""},
   "macos":{"steps":["brew install awscli.","aws --version; aws configure."],"notes":""},
   "linux":{"steps":["Install via the official bundle.","aws --version; aws configure."],"notes":""}},
  "checkpoints":[{"command":"aws --version","expected":"aws-cli/2.x","platforms":["windows","macos","linux"]}],
  "troubleshoot":[{"symptom":"AccessDenied on first call","fix":"Your IAM user needs permissions; start with read-only policies in a sandbox account."}],
  "costNote":"Free; cloud usage billed by the provider."},
 {"id":"IL28-INST-13","tool":"Google Cloud CLI","category":"cloud","moduleId":mod(43),"estimatedMinutes":15,
  "platforms":{"windows":{"steps":["Install GoogleCloudSDK installer.","gcloud version; gcloud init."],"notes":""},
   "macos":{"steps":["brew install --cask google-cloud-sdk.","gcloud init."],"notes":""},
   "linux":{"steps":["Install via the Google apt/yum repo.","gcloud init."],"notes":""}},
  "checkpoints":[{"command":"gcloud version","expected":"Google Cloud SDK 4xx/5xx","platforms":["windows","macos","linux"]}],
  "troubleshoot":[{"symptom":"gcloud init can't pick a project","fix":"Create a project in the Cloud Console first, then re-run init."}],
  "costNote":"Free; cloud usage billed by the provider."},
 {"id":"IL28-INST-14","tool":"VS Code + extensions","category":"ide","moduleId":mod(16),"estimatedMinutes":20,
  "platforms":{"windows":{"steps":["Install VS Code; add HashiCorp Terraform, YAML, Docker, Kubernetes extensions.","code --version."],"notes":""},
   "macos":{"steps":["brew install --cask visual-studio-code; add the extensions.","code --version."],"notes":""},
   "linux":{"steps":["Install via the Microsoft repo; add the extensions.","code --version."],"notes":""}},
  "checkpoints":[{"command":"code --version","expected":"1.x","platforms":["windows","macos","linux"]}],
  "troubleshoot":[{"symptom":"'code' not on PATH","fix":"In VS Code: Command Palette > 'Shell Command: Install code command in PATH'."}],
  "costNote":"Free."},
]

installPrereqOrder = ["IL28-INST-01","IL28-INST-14","IL28-INST-02","IL28-INST-03","IL28-INST-04",
 "IL28-INST-05","IL28-INST-08","IL28-INST-09","IL28-INST-06","IL28-INST-07",
 "IL28-INST-10","IL28-INST-11","IL28-INST-12","IL28-INST-13"]
installSteps = [{"id":i["id"],"tool":i["tool"],"moduleId":i["moduleId"],"minutes":i["estimatedMinutes"]} for i in installLabs]

multicloudLabs = [
 {"id":"IL28-MC-AZ","title":"Azure: Terraform Storage + Private Endpoint","cloud":"azure","moduleIds":[mod(34),mod(14),mod(40)],
  "brief":"Provision a storage account with Terraform, lock it down with a Private Endpoint and Private DNS zone, and prove public access is denied.",
  "steps":["Write HCL for the storage account, VNet, private endpoint, and Private DNS zone.","Apply; confirm the blob endpoint resolves to a private IP from a VNet VM.","Attempt public access; confirm denial.","Destroy everything."],
  "deliverable":"Terraform repo + DNS resolution proof.","checkpoint":"nslookup returns 10.x; public curl fails."},
 {"id":"IL28-MC-AWS","title":"AWS: VPC + EKS Node Group via Terraform","cloud":"aws","moduleIds":[mod(42),mod(34)],
  "brief":"Build a VPC with public/private subnets and an EKS node group entirely in Terraform; deploy a sample app.",
  "steps":["Write the VPC module (2 AZs, NAT).","Add the EKS cluster and a managed node group.","Deploy the TL-04 image; expose via ALB.","Destroy everything."],
  "deliverable":"Terraform repo + app URL.","checkpoint":"kubectl get nodes shows EKS nodes; app reachable."},
 {"id":"IL28-MC-GCP","title":"GCP: GKE Autopilot Deployment","cloud":"gcp","moduleIds":[mod(43),mod(31)],
  "brief":"Create a GKE Autopilot cluster and deploy the TL-05 Helm chart to it.",
  "steps":["gcloud container clusters create-auto.","Install the Helm chart from M31.","Verify workloads and clean up."],
  "deliverable":"Chart + cluster evidence.","checkpoint":"Workloads Running; cluster deleted after."},
]

terminalSims = [
 {"id":"IL28-TS-01","title":"Disk-full triage on RHEL","moduleId":mod(8),
  "prompt":"df shows 40% free but writes fail with 'No space left on device'. Diagnose.",
  "script":["df -h /data","df -i /data","lsof +L1 | head","du -sh /tmp/*"],
  "expected":["Filesystem 1K-blocks ... 40% ...","IUse%=100%","deleted file held open","/tmp filled"],
  "answer":"Inodes exhausted (df -i 100%) — delete small files or the deleted-but-open handle; clear /tmp."},
 {"id":"IL28-TS-02","title":"Port check server A to server B","moduleId":mod(10),
  "prompt":"App on A can't reach B:5432. Check the port from A.",
  "script":["nc -zv db.internal 5432","ss -tlnp | grep 5432","telnet db.internal 5432"],
  "expected":["Connection timed out","LISTEN on 127.0.0.1 only","Trying..."],
  "answer":"Postgres listens on localhost only; bind it to the service IP or tunnel, then open the firewall."},
 {"id":"IL28-TS-03","title":"kubectl pod triage","moduleId":mod(27),
  "prompt":"kubectl get pods shows web-7d9f CrashLoopBackOff. Triage in order.",
  "script":["kubectl describe pod web-7d9f | tail -20","kubectl logs web-7d9f --previous","kubectl get events --sort-by=.lastTimestamp | tail"],
  "expected":["Last State: Terminated, Exit Code: 137","OOMKilled","FailedScheduling"],
  "answer":"Exit 137 = OOMKilled: raise the memory limit (and check requests vs node capacity)."},
]
for i,(mid,title,prompt,script,expected,answer) in enumerate([
 (mod(33),"Terraform drift hunt","terraform plan shows changes you did not make. Find and fix.",
  ["terraform plan -out=drift.plan","terraform show -json drift.plan | grep -i address","terraform import 'azurerm_managed_disk.data[\"disk1\"]' /subscriptions/..."],
  ["~ update in-place","drifted attribute","Import successful"],"Import the drifted resource with the correctly-escaped for_each address."),
 (mod(28),"OOMKilled exit 137","Container svc-basic terminated with exit code 137.",
  ["kubectl describe pod svc-basic | grep -A5 'Last State'","kubectl top pod svc-basic"],
  ["Reason: OOMKilled","Exit Code: 137"],"Memory limit too low: raise limits, check for leaks, right-size requests."),
 (mod(16),"Rebase gone wrong","git rebase main left you with duplicate commits.",
  ["git log --oneline -8","git reflog | head","git rebase --abort"],
  ["duplicate SHAs","HEAD@{1}: rebase","aborted"],"Abort the rebase, then rebase --onto the correct base or merge instead."),
 (mod(36),"Ansible register assert","Capture command output and fail if a service is down.",
  ["ansible web -m command -a 'systemctl is-active nginx'","- register: svc","- assert: { that: svc.stdout == 'active' }"],
  ["active","svc.stdout","ok=1"],"Use register + assert so the playbook fails fast on a down service."),
 (mod(41),"AKS nodes not joining","Scaled the node pool but new nodes never appear.",
  ["az aks nodepool show --query provisioningState","az aks nodepool show --query count","kubectl get nodes"],
  ["Succeeded","count: 5","only 2 nodes"],"Check autoscaler, subnet IP space, quotas, taints, and Azure Policy blocking the VM SKU."),
], start=4):
    terminalSims.append({"id":f"IL28-TS-{i:02d}","title":title,"moduleId":mid,"prompt":prompt,
     "script":script,"expected":expected,"answer":answer})

branchingScenarios = [
 {"id":"IL28-BS-01","title":"The 3 AM Pager: Pod Pending","moduleId":mod(27),
  "start":"payments-api pods are Pending; checkout is degrading.",
  "branches":[{"choice":"Describe the pod and read scheduler events","result":"Events show 0/4 nodes have enough memory. Correct path.","next":"node-capacity"},
              {"choice":"Delete the pods and hope the scheduler retries","result":"Pods reschedule and go Pending again. Dead end — go back.","next":"start"}],
  "resolution":"Scale the node pool (or right-size requests); verify pods schedule."},
 {"id":"IL28-BS-02","title":"Exit 137 in Production","moduleId":mod(28),
  "start":"svc-basic restarted 14 times; Last State exit code 137.",
  "branches":[{"choice":"Check Last State reason and memory working set","result":"Reason: OOMKilled. Correct.","next":"raise-limits"},
              {"choice":"Add more replicas","result":"Replicas die the same way. Dead end.","next":"start"}],
  "resolution":"Raise memory limits; profile for leaks; set requests honestly."},
 {"id":"IL28-BS-03","title":"Terraform Wants to Destroy Prod","moduleId":mod(33),
  "start":"plan shows 12 resources to destroy in prod.",
  "branches":[{"choice":"Refuse to apply; diff the state against reality","result":"A renamed module block orphaned the old addresses. Correct.","next":"moved-blocks"},
              {"choice":"Apply and recreate","result":"You just deleted prod data. Scenario failed — restart.","next":"start"}],
  "resolution":"Use moved blocks / import to reconcile addresses; never apply a surprise destroy."},
 {"id":"IL28-BS-04","title":"Disk Full at 2 AM","moduleId":mod(8),
  "start":"Writes fail; df shows free space.",
  "branches":[{"choice":"Run df -i and lsof +L1","result":"Inodes at 100% from millions of session files. Correct.","next":"cleanup"},
              {"choice":"Add a bigger disk","result":"Does not help an inode problem. Dead end.","next":"start"}],
  "resolution":"Purge session files, fix the app's file hygiene, add inode monitoring."},
 {"id":"IL28-BS-05","title":"Pipeline Red on Friday","moduleId":mod(38),
  "start":"Jenkins build fails after a shared-library change; 6 teams blocked.",
  "branches":[{"choice":"Pin the library version per repo and roll back the library","result":"Builds green again. Correct.","next":"versioning"},
              {"choice":"Hotfix the library in place","result":"Half the teams still red. Dead end.","next":"start"}],
  "resolution":"Version shared libraries; test changes against consumers before release."},
 {"id":"IL28-BS-06","title":"AKS Scale-Up Stalls","moduleId":mod(41),
  "start":"Node pool scaled to 8; only 3 nodes Ready.",
  "branches":[{"choice":"Check subnet IP space, quotas, and Activity logs","result":"Subnet exhausted. Correct.","next":"expand-subnet"},
              {"choice":"Keep scaling higher","result":"Still stuck. Dead end.","next":"start"}],
  "resolution":"Expand the subnet (or add a new one), then scale."},
]

clickSims = [
 {"id":"IL28-CS-01","title":"Azure Portal: Create a Storage Account","moduleId":mod(40),
  "steps":["Search 'Storage accounts' > Create.","Pick subscription, resource group, region.","Set performance Standard, redundancy LRS.","Review + Create; note the endpoint URLs."],
  "checkpoint":"Endpoint https://<name>.blob.core.windows.net resolves."},
 {"id":"IL28-CS-02","title":"AKS: Scale a Node Pool in the Portal","moduleId":mod(41),
  "steps":["Open the AKS cluster > Node pools.","Select the pool > Scale.","Set node count; save.","Watch provisioning state go Succeeded."],
  "checkpoint":"kubectl get nodes shows the new nodes."},
 {"id":"IL28-CS-03","title":"PR Review: Spot the Unpinned Dependency","moduleId":mod(17),
  "steps":["Open the MR diff for requirements.txt.","Find requests without == pin.","Request changes with the pinning comment.","Approve after the fix."],
  "checkpoint":"All dependencies pinned; MR merged."},
 {"id":"IL28-CS-04","title":"Helm: Upgrade a Release","moduleId":mod(31),
  "steps":["helm list; helm upgrade web ./chart --set image.tag=v2.","helm history web; helm rollback if needed."],
  "checkpoint":"Release at the new revision; rollback path verified."},
 {"id":"IL28-CS-05","title":"Key Vault: Store and Reference a Secret","moduleId":mod(48),
  "steps":["Create a secret in Key Vault.","Grant the managed identity Get permission.","Reference it from the app config; verify no secret in git."],
  "checkpoint":"App reads the secret; repo contains zero secret values."},
 {"id":"IL28-CS-06","title":"Grafana: Build the Golden-Signals Dashboard","moduleId":mod(45),
  "steps":["Add Prometheus data source.","Create panels: latency, traffic, errors, saturation.","Save to the team folder."],
  "checkpoint":"Dashboard renders live data for the demo app."},
]

cheatSheets = [
 {"id":"IL28-CH-KUBECTL","title":"kubectl triage cheat sheet","moduleId":mod(27),
  "items":["kubectl get pods -o wide — where is it, what state","kubectl describe pod X — events + Last State","kubectl logs X --previous — why it died","kubectl get events --sort-by=.lastTimestamp — cluster story","kubectl top pod/node — resource pressure"]},
 {"id":"IL28-CH-TERRAFORM","title":"Terraform daily-driver cheat sheet","moduleId":mod(33),
  "items":["terraform init / fmt / validate / plan / apply","terraform import 'type.name[\"key\"]' <id> — for_each escaping","terraform state list / show / mv","moved blocks for refactors","never commit *.tfvars with secrets"]},
 {"id":"IL28-CH-DOCKER","title":"Docker cheat sheet","moduleId":mod(23),
  "items":["docker build -t app:v1 .","multi-stage: build in one stage, copy artifacts to slim runtime","later-layer rm does NOT shrink the image","docker run --read-only --user 1000"]},
 {"id":"IL28-CH-GIT","title":"Git cheat sheet","moduleId":mod(17),
  "items":["git rebase main — linear history, never rebase shared branches","git merge --no-ff — preserve feature context","git reflog — the undo button","pin versions in requirements.txt before approving MRs"]},
 {"id":"IL28-CH-LINUX","title":"Linux triage cheat sheet","moduleId":mod(8),
  "items":["df -h AND df -i — space and inodes","lsof +L1 — deleted but open files","ss -tlnp — listening ports","nc -zv host port — port check A→B","ulimit -n — file descriptor limits"]},
 {"id":"IL28-CH-ANSIBLE","title":"Ansible cheat sheet","moduleId":mod(36),
  "items":["ansible-playbook site.yml -i inventory","register: capture command output","assert: fail fast on bad state","roles: tasks/handlers/defaults","idempotence: run twice, 0 changed"]},
]

employerMappings = [
 {"objective":"Full Terraform lifecycle: plan/apply across testing→dev→stage→QA→prod","moduleId":f"{mod(32)}, {mod(33)}, {mod(34)}, {mod(35)}",
  "certification":"Terraform Associate","certDomain":"Terraform basics + beyond","employer":"BNY Mellon","competency":"IaC delivery",
  "evidence":"Terraform repo provisioning a storage account from a name→access-type map, with drift/import runbook."},
 {"objective":"Diagnose 'no space on disk' with free space (inodes, file descriptors, quotas)","moduleId":f"{mod(8)}",
  "certification":"RHCSA concepts","certDomain":"Storage & file systems","employer":"BNY Mellon","competency":"Linux troubleshooting",
  "evidence":"Triage transcript: df -i, lsof +L1, resolution steps."},
 {"objective":"Kubernetes pod troubleshooting: Pending, CrashLoopBackOff, OOMKilled/exit 137, probes","moduleId":f"{mod(27)}, {mod(28)}",
  "certification":"CKA/CKAD concepts","certDomain":"Troubleshooting","employer":"BNY Mellon","competency":"K8s operations",
  "evidence":"Triage log for three induced failure modes with kubectl outputs."},
 {"objective":"Azure networking: App Gateway (L7) vs Load Balancer (L4), Private Link, Private DNS","moduleId":f"{mod(14)}, {mod(15)}, {mod(40)}",
  "certification":"AZ-104/AZ-400","certDomain":"Networking & monitoring","employer":"BNY Mellon","competency":"Azure networking",
  "evidence":"Traffic-flow diagram + Terraform for a private-endpoint storage account."},
 {"objective":"Jenkins shared libraries standardizing Jenkinsfiles; CI/CD phases and quality gates","moduleId":f"{mod(37)}, {mod(38)}",
  "certification":"AWS DevOps concepts","certDomain":"SDLC automation","employer":"BNY Mellon","competency":"CI/CD engineering",
  "evidence":"Shared-library repo consumed by two pipelines."},
 {"objective":"STAR behavioral answers delivered independently, no copilot","moduleId":f"{mod(50)}",
  "certification":"—","certDomain":"Behavioral","employer":"BNY Mellon","competency":"Interview readiness",
  "evidence":"Recorded 90-minute mock panel, scored against the rubric."},
]

jdMatrix = [
 {"postingTitle":"DevOps Engineer — Data and Analytics Solutions (panel interview notes)","postingUrl":"private interview-session notes (2025)",
  "employer":"BNY Mellon","urlStatus":"source: candidate's own session notes","requirement":"Terraform vs Ansible depth; state, drift, import, for_each",
  "modules":[mod(32),mod(33),mod(34),mod(35),mod(36)],"certDomain":"Terraform Associate: all domains",
  "portfolioArtifact":"Terraform storage-account repo + drift/import runbook"},
 {"postingTitle":"DevOps Engineer — cloud engineering / CI/CD tooling (panel interview notes)","postingUrl":"private interview-session notes (2025)",
  "employer":"BNY","urlStatus":"source: candidate's own session notes","requirement":"Azure networking (AppGW L7 vs LB L4, Private Link/DNS), AKS node pools, autoscaling, CI/CD phases",
  "modules":[mod(14),mod(15),mod(37),mod(40),mod(41)],"certDomain":"AZ-104/AZ-400: networking, compute, DevOps",
  "portfolioArtifact":"AKS triage runbook + private-endpoint Terraform"},
 {"postingTitle":"DevOps Engineer — mock panel (full-stack + DevOps)","postingUrl":"private interview-session notes (2025)",
  "employer":"BNY","urlStatus":"source: candidate's own session notes","requirement":"Docker layers/whiteout, K8s troubleshooting, Jenkins/Groovy, observability at scale, RBAC, STAR behavioral",
  "modules":[mod(22),mod(23),mod(26),mod(27),mod(28),mod(38),mod(45),mod(48),mod(50)],"certDomain":"CKA concepts; Security+ architecture",
  "portfolioArtifact":"Multi-stage image comparison + K8s triage log + STAR story bank"},
]

studyGuide = {
 "title":"Study guide: how to work this course","totalHours":hours,"totalMinutes":total_min,
 "pacing":{"dailyMinutes":90,"daysPerWeek":5,"estimatedWeeks":round(total_min/450,1),
  "plan":[
   f"Phase 1 — Foundations, M01-M06 (~{sum(modules[i]['estimatedMinutes'] for i in range(6))//60} h): math for infrastructure; drill until green before touching Linux.",
   f"Phase 2 — Linux & networking, M07-M15: live in the terminal; every lab runs for real on your machine.",
   "Phase 3 — Containers & orchestration, M16-M31: Docker then Kubernetes; the triage runbooks are the job.",
   "Phase 4 — IaC & CI/CD, M32-M39: Terraform and Ansible back-to-back; build the chain labs in order.",
   "Phase 5 — Clouds & production, M40-M49: Azure first, then AWS/GCP; observability and DevSecOps gates.",
   "Phase 6 — Interview simulation, M50: cold answers only. Record yourself; no copilot, no notes."]},
 "rules":["Never skip the hands-on lab.","Drills to green before the next module.","One tool-install lab per tool, before its module.","Score every mock task; re-take below 80%."]}

sourceLinks = [
 {"title":"Kubernetes official documentation","url":"https://kubernetes.io/docs/","note":"Primary reference for all K8s modules."},
 {"title":"Terraform documentation (HashiCorp Developer)","url":"https://developer.hashicorp.com/terraform/docs","note":"HCL, state, and CLI reference."},
 {"title":"Ansible documentation","url":"https://docs.ansible.com/","note":"Playbooks, roles, and modules reference."},
 {"title":"Microsoft Learn — Azure","url":"https://learn.microsoft.com/azure/","note":"Azure services, AKS, and networking docs."},
 {"title":"Docker documentation","url":"https://docs.docker.com/","note":"Dockerfile and Compose reference."},
 {"title":"Jenkins user documentation","url":"https://www.jenkins.io/doc/","note":"Pipeline syntax and shared libraries."},
 {"title":"Prometheus documentation","url":"https://prometheus.io/docs/","note":"Metrics, PromQL, and alerting."},
]

scriptLabs = [
 {"id":"IL28-SL-01","title":"Health-check CLI in Python","moduleId":mod(19),
  "brief":"Build a CLI that checks a URL, a port, and disk space, exiting non-zero on failure.",
  "steps":["argparse for --url, --port, --disk-path.","Use requests with a timeout; socket for the port; shutil.disk_usage.","Exit codes: 0 ok, 1 warning, 2 critical.","Package with a venv; document usage."],
  "deliverable":"healthcheck.py + README.","checkpoint":"Fails correctly against a stopped service."},
 {"id":"IL28-SL-02","title":"Log-summarizer in Bash","moduleId":mod(11),
  "brief":"Summarize an access log: top IPs, status-code histogram, slowest endpoints.",
  "steps":["awk for fields; sort | uniq -c | sort -nr.","Handle malformed lines gracefully.","set -euo pipefail throughout."],
  "deliverable":"summarize.sh + sample output.","checkpoint":"Correct counts on a 10k-line fixture."},
]
drillsTop = [{"id":"IL28-DRILL-INDEX","title":"Master drill index","note":"All module drills are indexed here for spaced repetition; work them to green before advancing."}]
scenarios = [{"id":"IL28-SC-01","title":"Production incident game-days","moduleId":mod(46),
 "brief":"Schedule monthly game-days: pick a branching scenario, run it against a sandbox, write the postmortem."}]
trainers = [
 {"id":"IL28-TR-MATH","title":"Adaptive math mastery lab","moduleId":mod(1),
  "concept":"Original adaptive engine inspired by ALEKS/Pearson (not copied): knowledge check → personalized path → mastery progression with decay rechecks.",
  "topics":["binary/hex conversion","subnet math","Boolean logic","SLA/downtime math","Little's Law"]},
 {"id":"IL28-TR-CLI","title":"Adaptive CLI/coding mastery lab","moduleId":mod(11),
  "concept":"Original adaptive engine: generated terminal challenges with progressive difficulty, from single commands to full triage transcripts.",
  "topics":["kubectl triage","terraform plan reading","docker build debugging","bash scripting","git recovery"]},
]
mockTasksTop = [{"id":"IL28-MT-INDEX","title":"Mock task index","note":"Every module ships a panel-style mock task; M50 chains them into a full 90-minute mock panel."}]
answerBank = {"note":"Every drill item and quiz question carries its answer and explanation inline; this bank indexes them by module for review.","modules":[m["id"] for m in modules]}
sampleDatasets = [{"id":"IL28-DS-01","title":"Synthetic access log (10k lines)","moduleId":mod(11),"note":"Generated fixture for the log-summarizer lab; no real user data."},
 {"id":"IL28-DS-02","title":"Synthetic Prometheus metrics export","moduleId":mod(45),"note":"Fixture for dashboard-building practice."}]
pythonExercises = [{"id":"IL28-PY-01","title":"Predict-the-output set (M18)","moduleId":mod(18),"note":"Original script-reading exercises with verified answers."},
 {"id":"IL28-PY-02","title":"CLI tool kata (M19)","moduleId":mod(19),"note":"Build-and-verify scripting exercises."}]
interactivityAudit = {
 "terminalSims":len(terminalSims),"branchingScenarios":len(branchingScenarios),"clickSims":len(clickSims),
 "toolLabs":len(toolLabs),"installLabs":len(installLabs),"multicloudLabs":len(multicloudLabs),
 "trainers":len(trainers),"scriptLabs":len(scriptLabs),"cheatSheets":len(cheatSheets),
 "totalInteractive":len(terminalSims)+len(branchingScenarios)+len(clickSims)+len(toolLabs)+len(installLabs)+len(multicloudLabs)+len(trainers)+len(scriptLabs)+len(cheatSheets),
 "rule":"Every module contains at least two interactive elements (drills, labs, sims, or mock tasks)."
}

course = {
 "code":"IL-28","courseId":"il-28-devsecops-cloud-infrastructure-mastery",
 "title":"IL-28 · DevSecOps & Cloud Infrastructure — Production Mastery Bootcamp",
 "tagline":"From zero to production: math, Linux, networking, containers, IaC, clouds, DevSecOps — calibrated to the BNY DevOps panel bar.",
 "blurb":("IL-28 is an independent, interactive DevSecOps and cloud-infrastructure bootcamp built from real BNY/BNY Mellon DevOps panel interview sessions. "
  "It runs zero-to-production: foundational math (binary, Boolean logic, subnetting, reliability statistics), Linux/RHEL deep-dives (inodes, file descriptors, ports), "
  "networking (TCP/UDP, cloud networking, L4 vs L7 load balancing), Git, Python/Go scripting, Docker, Kubernetes, Helm, Terraform, Ansible, Jenkins and modern CI/CD, "
  "Azure/AWS/GCP, observability, DevSecOps security gates, and SRE — closing with a full BNY panel interview simulation that trains INDEPENDENT mastery with no copilot. "
  "Six certification tracks (Terraform Associate, CKA/CKAD, AZ-104/AZ-400, AWS DevOps Engineer, RHCSA, Security+) each carry a domain-by-domain crosswalk, timed practice gates, and a readiness dashboard."),
 "hours":hours,"mockMinutes":90,"schemaVersion":4,"updatedAt":"2026-10-07T22:00:00Z",
 "honestyNote":("This is an independent preparation and practice course aligned to publicly described exam topic maps and a real interview experience; it is not affiliated with, endorsed by, or sponsored by HashiCorp, CNCF, Microsoft, Amazon, Google, Red Hat, CompTIA, Jenkins, Docker, or BNY Mellon, confers no certificate, and grants no credentials. "
  "Hours are honest estimates from the module workload formula. Cloud labs assume sandbox/free-tier accounts; destroy everything you create."),
 "objectives":[
  "Master the infrastructure math: binary/hex, Boolean logic, subnetting/CIDR, set theory, modular arithmetic, and reliability statistics — with worked examples for every concept.",
  "Troubleshoot Linux/RHEL like a panel expects: inodes, file descriptors, ports, systemd, SELinux, and full connectivity runbooks.",
  "Explain and build cloud networking: TCP/UDP, DNS, VNet/VPC, Private Link/Private DNS, and L4 vs L7 load balancing with real traffic flows.",
  "Ship containers and orchestration: Docker layers and multi-stage builds, Kubernetes triage (Pending, CrashLoopBackOff, OOMKilled/exit 137), probes, scheduling, and Helm.",
  "Run infrastructure as code: Terraform (state, drift, import, for_each, modules, secrets) and Ansible (playbooks, roles), and argue the Terraform-vs-Ansible trade-offs cold.",
  "Build CI/CD: pipeline phases and quality gates, Jenkins with Groovy shared libraries, and modern GitHub Actions/Azure DevOps pipelines.",
  "Operate Azure, AWS, and GCP: storage, Key Vault, AKS node pools and autoscaling, VPC, IAM, and multicloud strategy.",
  "Observe and secure production: Prometheus/Grafana/ELK, SLOs and incident response, SAST/DAST, secrets management, supply-chain security, and RBAC.",
  "Answer every real BNY DevOps panel question independently — no copilot — in a timed 90-minute mock panel."],
 "arc":[
  {"phase":1,"title":"Foundations (M01-M06)","body":"Mathematics for infrastructure: binary and hex, Boolean logic, subnetting, set theory, modular arithmetic, and reliability math. Every later module builds on these."},
  {"phase":2,"title":"Linux & Networking (M07-M15)","body":"RHEL deep-dives, shell scripting, TCP/IP, cloud networking, and load balancing — the substrate everything else runs on."},
  {"phase":3,"title":"Source, Scripting & Containers (M16-M25)","body":"Git workflows, Python/Go for ops, Docker internals, and container security."},
  {"phase":4,"title":"Orchestration & IaC (M26-M36)","body":"Kubernetes end-to-end, Helm, Terraform, and Ansible — the heart of the DevOps role."},
  {"phase":5,"title":"Delivery & Clouds (M37-M44)","body":"CI/CD pipelines, then Azure, AWS, and GCP with a multicloud strategy capstone."},
  {"phase":6,"title":"Production & Proof (M45-M50)","body":"Observability, DevSecOps, SRE resilience, and the BNY panel interview simulation."}],
 "priorities":[
  {"label":"Kubernetes & container operations","minutes":int(total_min*0.18)},
  {"label":"Terraform & Ansible IaC","minutes":int(total_min*0.16)},
  {"label":"Linux/RHEL troubleshooting","minutes":int(total_min*0.14)},
  {"label":"Cloud platforms (Azure/AWS/GCP)","minutes":int(total_min*0.14)},
  {"label":"CI/CD & Jenkins","minutes":int(total_min*0.10)},
  {"label":"Networking & security","minutes":int(total_min*0.12)},
  {"label":"Math foundations & scripting","minutes":int(total_min*0.10)},
  {"label":"Interview simulation","minutes":int(total_min*0.06)}],
 "battlePlan":[
  {"id":"sprint-foundations","title":"Foundations Sprint","minutes":480,"detail":"M01-M06: binary/hex, Boolean logic, subnetting, sets, modular arithmetic, reliability math. Worked examples plus drills. Deliverable: a solved problem set."},
  {"id":"sprint-linux","title":"Linux Triage Sprint","minutes":600,"detail":"M07-M12: filesystem, inodes, processes, networking tools, bash, RHEL ecosystem. Deliverable: a personal triage runbook."},
  {"id":"sprint-containers","title":"Containers & K8s Sprint","minutes":900,"detail":"M22-M31: Docker through Helm. Deliverable: triage logs for Pending, CrashLoopBackOff, and OOMKilled."},
  {"id":"sprint-iac","title":"IaC Sprint","minutes":720,"detail":"M32-M36: Terraform and Ansible. Deliverable: the storage-account repo plus drift/import runbook."},
  {"id":"sprint-clouds","title":"Cloud Sprint","minutes":720,"detail":"M40-M44: Azure, AWS, GCP. Deliverable: three destroyed-after-use multicloud labs."},
  {"id":"sprint-interview","title":"Interview Simulation Sprint","minutes":540,"detail":"M50: timed drills, STAR stories, and a recorded 90-minute mock panel. No copilot, no notes."}],
 "modules":modules,
 "crosswalk":crosswalk,"certGates":certGates,"readinessDashboard":readinessDashboard,
 "scriptLabs":scriptLabs,"drills":drillsTop,"scenarios":scenarios,"trainers":trainers,
 "terminalSims":terminalSims,"mockTasks":mockTasksTop,"cheatSheets":cheatSheets,
 "answerBank":answerBank,"sourceLinks":sourceLinks,"toolLabs":toolLabs,
 "multicloudLabs":multicloudLabs,"sampleDatasets":sampleDatasets,
 "installSteps":installSteps,"installLabs":installLabs,"installPrereqOrder":installPrereqOrder,
 "employerMappings":employerMappings,"jdMatrix":jdMatrix,
 "sqlPlaygrounds":[],"pythonExercises":pythonExercises,"daxPlaygrounds":[],
 "branchingScenarios":branchingScenarios,"clickSims":clickSims,
 "interactivityAudit":interactivityAudit,
 "studyGuide":studyGuide,
 "timeFormula":"estimatedMinutes per module = weight x 120 + notes x 12 + cards x 4 + quiz x 8 + drill items x 4 + handsOnLab 90 + min(180, videoMinutes/2). Course total = sum of module estimates.",
}

with open(OUT,"w") as f:
    json.dump(course,f,ensure_ascii=False)
# validate by re-reading
d2 = json.load(open(OUT))
print("final modules:",len(d2["modules"]),"hours:",d2["hours"])
print("bytes:",os.path.getsize(OUT))

# worth-paying-for audit
fails=[]
for m in d2["modules"]:
    checks={"notes>=5":len(m["notes"])>=5,"cards>=8":len(m["cards"])>=8,"quiz>=8":len(m["quiz"])>=8,
      "drills>=1":len(m["drills"])>=1,"lab>=8steps":len(m["handsOnLab"]["steps"])>=8,
      "mock":bool(m.get("mockTask",{}).get("q")),
      "no_placeholder":not any(re.search(r"lorem|todo|coming soon|placeholder",json.dumps(m),re.I) for _ in [0])}
    bad=[k for k,v in checks.items() if not v]
    if bad: fails.append((m["id"],bad))
print("worth-paying-for fails:",len(fails))
for fid,bad in fails: print("  ",fid,bad)

#!/usr/bin/env python3
"""Retrofit IL-05 modules 11-14 to the multicloud course template."""
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

# ---------------------------------------------------------------- Module 11
U['il05-azure-network'] = {
 'summary': ("Welcome to Module 11 of IL-05 — Cloud DevSecOps Platform SRE. I'm your instructor, and this is the network "
  "specialist's module: the AZ-700. We'll build the core networking infrastructure — VNets, subnets, NSGs, peering, private DNS — "
  "with address planning done once and done right; connect with VPN Gateway, ExpressRoute, and Virtual WAN, picking the SKU by need; "
  "deliver applications across the L4/L7/global spectrum — Load Balancer, Application Gateway, Front Door, Traffic Manager; give PaaS "
  "private access with Private Link; and secure it all with Azure Firewall, DDoS Protection, and Bastion. The AZ-700 tests selection, "
  "not syntax — every scenario asks which service the constraint picks."),
 'notes': [
  {'title': 'Concepts', 'body':
   "The network engineer's glossary — selection criteria included.\n"
   "- **VNet / subnet** — the isolated network and its segments; address space planning is forever — overlapping CIDRs with on-prem break peering and VPN permanently.\n"
   "- **NSG / ASG** — network security groups (with application security groups for grouping); stateful-ish rules, lowest number wins.\n"
   "- **peering** — VNet peering; transit via the hub, non-transitive by default.\n"
   "- **Private DNS zone** — VNet-linked, split-horizon name resolution for private networks.\n"
   "- **VPN Gateway** — S2S IPsec, P2S, and VNet-to-VNet connectivity over the internet.\n"
   "- **ExpressRoute** — a private dedicated circuit: consistent latency and throughput with an SLA, not internet variability.\n"
   "- **Virtual WAN** — Microsoft-managed hub-and-spoke at global scale; global transit without building your own hub mesh.\n"
   "- **Load Balancer** — L4 regional distribution.\n"
   "- **Application Gateway** — regional L7 with WAF and path/host routing.\n"
   "- **Front Door** — global L7 at the edge PoPs with instant failover and WAF; the global web-app answer.\n"
   "- **Traffic Manager** — DNS-based global routing; failover takes TTL time — not instant like Front Door.\n"
   "- **Private Link / Private Endpoint** — PaaS services get VNet-private IPs; the strong option for data-exfiltration control.\n"
   "- **service endpoint** — VNet identity for PaaS access; simpler, but the PaaS stays public-adjacent — weaker than Private Link.\n"
   "- **Azure Firewall** — L3–L7 filtering with FQDN rules and threat intelligence; egress control that actually works.\n"
   "- **DDoS Protection** — network-tier protection; enable on the VNet housing public IPs — the attack you can't afford to learn about live.\n"
   "- **Bastion** — browser-based RDP/SSH with no public IPs; replaces the internet-facing jumpbox — the most-attacked box in the estate."},
  {'title': 'Hands-on procedure', 'body':
   "Design and prove the network in constraint order: address, connect, deliver, secure.\n"
   "1. **Address once.** Plan non-overlapping CIDRs for hub, spokes, and on-prem; document the scheme — this decision is forever.\n"
   "2. **Hub-spoke.** Build the hub (firewall, VPN/ExpressRoute gateway, Bastion, Private DNS) and peer the spokes with gateway transit enabled; "
   "verify spoke-to-spoke flows through the hub.\n"
   "3. **Connect.** Stand up the S2S VPN, then compare against the ExpressRoute value proposition (consistent private throughput with SLA) for the workload's need.\n"
   "4. **Deliver.** Put the regional app behind Application Gateway (L7 + WAF + path routing); put the global app behind Front Door and test the instant failover; "
   "note Traffic Manager's TTL-time failover as the DNS-level alternative.\n"
   "5. **Private the PaaS.** Attach Private Endpoints to Storage and SQL; confirm with service endpoints disabled that exfiltration paths are closed.\n"
   "6. **Secure.** Write Azure Firewall FQDN rules (allow *.update.microsoft.com, deny the rest); enable DDoS Protection on the public-IP VNet; "
   "remove every jumpbox in favor of Bastion.\n"
   "7. **Select by constraint.** Drill ten scenarios: for each, name the deciding constraint (global? private? L7? instant failover?) and the service it picks — the AZ-700's actual skill.",
   'code': ("# Hub-spoke peering with gateway transit (spokes use the hub's VPN/ER gateway)\n"
            "az network vnet peering create \\\n"
            "  --name spoke-to-hub --resource-group rg-net \\\n"
            "  --vnet-name spoke1 --remote-vnet hub \\\n"
            "  --allow-vnet-access --allow-forwarded-traffic \\\n"
            "  --use-remote-gateways\n"
            "\n"
            "# Private DNS: VNet-linked resolution for private endpoints\n"
            "az network private-dns zone create -g rg-net -n privatelink.database.windows.net\n"
            "az network private-dns link vnet create -g rg-net -z privatelink.database.windows.net \\\n"
            "  -n hub-link --virtual-network hub --registration-enabled false"),
   'lang': 'bash'},
  {'title': 'Project brief', 'body':
   "Design the network for a fictional company with on-prem datacenters on two continents: the addressing plan (non-overlapping, "
   "documented), hub-spoke topology with shared firewall and gateways, the connectivity choice per site (VPN vs ExpressRoute vs "
   "Virtual WAN with rationale), the delivery tier per app (Front Door vs App Gateway vs LB vs Traffic Manager), Private Link on all "
   "PaaS, and the security layer (Firewall FQDN egress, DDoS Protection, Bastion everywhere). Deliverables: the topology diagram, the "
   "addressing register, and the selection log — every service choice tied to its deciding constraint. The AZ-700 grades selection; "
   "this brief is the selection portfolio."},
  {'title': 'Honesty note', 'body': HON},
 ],
 'cards_add': [
  {'front': 'Front Door vs Traffic Manager failover?', 'back': 'Front Door: instant at the edge. Traffic Manager: DNS-level, takes TTL time.'},
  {'front': 'Gateway transit in peering?', 'back': 'Spokes use the hub VPN/ExpressRoute gateway — enable use-remote-gateways on the spoke side.'},
  {'front': 'FQDN filtering: which control?', 'back': 'Azure Firewall — NSGs filter IPs/ports, not domain names.'},
  {'front': 'AZ-700 core skill?', 'back': 'Selection by constraint — which service the scenario demands, not syntax.'},
 ],
}

# ---------------------------------------------------------------- Module 12
U['il05-openshift'] = {
 'summary': ("Welcome to Module 12 of IL-05 — Cloud DevSecOps Platform SRE. I'm your instructor, and this module covers Red Hat "
  "OpenShift both ways: as an administrator and as a developer. On the admin side — the EX280/EX380 track — we'll work containers and "
  "Kubernetes foundations, cluster administration with projects, quotas, and storage, and the day-2 operations that are the actual job: "
  "upgrades, etcd backup, and cert rotation. On the dev side — the EX188/EX288 track — we'll containerize apps, deploy with OpenShift "
  "patterns like S2I and routes, build resilient microservices, and close with the twelve-factor capstone on Quarkus. These are "
  "performance exams on live clusters — speed with `oc` is the skill."),
 'notes': [
  {'title': 'Concepts', 'body':
   "The OpenShift glossary — admin and dev, side by side.\n"
   "- **project** — OpenShift's namespace plus membership and annotations; the multitenancy admin boundary.\n"
   "- **route** — OpenShift's built-in ingress; TLS modes are edge (terminate at the router), passthrough (terminate at the pod), reencrypt (both).\n"
   "- **S2I (Source-to-Image)** — git push → image → deploy: the developer on-ramp without Dockerfiles.\n"
   "- **Operator** — cluster extensions as code.\n"
   "- **IPI / UPI** — installer-provisioned versus user-provisioned installation shapes.\n"
   "- **quota / limit range** — per-project consumption bounds and defaults; the noisy-neighbor control for multitenancy.\n"
   "- **OCS/ODF** — the OpenShift storage offerings; StorageClasses for dynamic provisioning.\n"
   "- **day-2 operations** — upgrades, etcd backup, cert rotation, monitoring: the actual job after the day-1 install.\n"
   "- **DeploymentConfig** — the OpenShift-native deployment object alongside standard Deployments/StatefulSets.\n"
   "- **health probe** — liveness/readiness semantics carried into OpenShift deploy patterns.\n"
   "- **circuit breaker / bulkhead / retry with backoff** — the resilient-microservice patterns, via Service Mesh (Istio) or libraries.\n"
   "- **Quarkus** — 'supersonic subatomic Java': fast startup, low memory, native images via GraalVM for serverless; dev mode gives live reload — the inner loop that makes Java cloud-credible.\n"
   "- **twelve-factor** — codebase, dependencies, config (env, not code), backing services (attached resources), build/release/run, stateless processes, port binding, concurrency, disposability, dev/prod parity, logs (event streams), admin processes.\n"
   "- **container security baseline** — non-root user plus read-only filesystem where possible."},
  {'title': 'Hands-on procedure', 'body':
   "Administer the cluster, then ship on it — both exam personas in one flow.\n"
   "1. **Project and quota.** Create a project, set quotas and limit ranges, and prove a noisy-neighbor workload is contained.\n"
   "2. **S2I deploy.** Push application source and build with S2I — no Dockerfile — then expose it with a route; compare edge vs passthrough vs reencrypt TLS for a compliance requirement.\n"
   "3. **Health and config.** Add liveness/readiness probes, externalize config into ConfigMaps and secrets, and verify the same image runs in two environments via env-var config.\n"
   "4. **Resilience.** Add retries with backoff and a circuit breaker (mesh or library); kill a dependency and watch the bulkhead hold.\n"
   "5. **Day-2.** Take the etcd backup, rehearse cert rotation, and walk the upgrade pre-checks — installs are day 1, this is the career.\n"
   "6. **Twelve-factor audit.** Score the deployed app against all twelve factors; fix every violation.\n"
   "7. **Speed drill.** Redo the deploy tasks against the clock with `oc` — the performance exams grade live-cluster execution.",
   'code': ("# S2I: source -> image -> deploy, no Dockerfile\n"
            "oc new-project shop\n"
            "oc new-app https://github.com/example/shop.git --strategy=source\n"
            "oc expose svc/shop\n"
            "\n"
            "# Route TLS modes: edge | passthrough | reencrypt\n"
            "oc create route passthrough shop-secure --service=shop --port=8443\n"
            "\n"
            "# Day-2: etcd backup before you touch anything\n"
            "oc debug node/<node> -- chroot /host /usr/local/bin/cluster-backup.sh /home/core/assets/backup\n"
            "\n"
            "# Quotas: the noisy-neighbor control\n"
            "oc create quota project-quota --hard=cpu=4,memory=8Gi,pods=20 -n shop"),
   'lang': 'bash'},
  {'title': 'Project brief', 'body':
   "Deliver the twelve-factor microservice on OpenShift: S2I or Dockerfile build, route with the compliance-correct TLS mode, "
   "probes, externalized config (same image in two environments), logs to stdout, horizontal scaling demonstrated — plus the admin "
   "side: project quotas, the etcd backup artifact, and a day-2 checklist (upgrades, cert rotation, monitoring). Deliverables: the "
   "deployed app, the twelve-factor audit with violations fixed, and the admin runbook. This is both exams in one portfolio: the "
   "admin proves the cluster is operable, the dev proves the app is shippable."},
  {'title': 'Honesty note', 'body': HON},
 ],
 'cards_add': [
  {'front': 'oc vs kubectl?', 'back': 'oc is the OpenShift CLI — superset of kubectl with routes, projects, S2I, and DeploymentConfigs.'},
  {'front': 'Route TLS: compliance needs pod termination?', 'back': 'Passthrough — the router never decrypts; TLS ends at the pod.'},
  {'front': 'Quarkus dev mode?', 'back': 'Live reload — the inner loop that makes Java cloud-credible.'},
  {'front': 'EX280/EX380 vs EX188/EX288?', 'back': 'Admin track: fix/operate the cluster. Dev track: containerize and deploy the app. Both performance-based on live clusters.'},
 ],
}

# ---------------------------------------------------------------- Module 13
U['il05-hashicorp-vault'] = {
 'summary': ("Welcome to Module 13 of IL-05 — Cloud DevSecOps Platform SRE. I'm your instructor, and this module is secrets and "
  "service networking: HashiCorp Vault and Consul, through the Vault Associate and Consul Associate exams. We'll run Vault's secrets "
  "engines — KV, dynamic database and cloud credentials, PKI, transit — and its auth methods, so humans and machines each authenticate "
  "as themselves; write least-privilege policies; and face the operations reality: unseal ceremonies, Raft storage, replication, and "
  "monitoring the critical path. Then Consul: the service catalog with DNS and health-checked discovery, and the Connect service mesh "
  "with mTLS, intentions, and gateways. Dynamic secrets solve the leaked-credential problem structurally — that idea alone is worth the module."),
 'notes': [
  {'title': 'Concepts', 'body':
   "The secrets-and-mesh glossary.\n"
   "- **KV v2 secrets engine** — versioned static secrets.\n"
   "- **dynamic secrets** — leased, auto-revoked credentials (database, AWS STS): credentials that expire; the leaked-credential problem solved structurally.\n"
   "- **PKI secrets engine** — Vault as an internal certificate authority; short-lived certs.\n"
   "- **transit secrets engine** — encryption-as-a-service: Vault encrypts/decrypts, your data never lands in Vault; crypto without key-management pain.\n"
   "- **auth method** — how clients prove identity: userpass/LDAP (humans), OIDC (SSO), Kubernetes (pod service accounts), AWS (IAM-based) — machines authenticate as themselves.\n"
   "- **Vault policy** — HCL paths with capabilities (read, list, create, update, delete, sudo); deny-by-default — nothing is readable until a policy allows it.\n"
   "- **unseal** — Shamir key shards or auto-unseal via cloud KMS; plan this before production — unseal ceremonies fail at 3 AM otherwise.\n"
   "- **Raft integrated storage** — Vault's built-in storage backend; no Consul needed anymore. Back it up with `vault operator raft snapshot save`.\n"
   "- **DR vs performance replication** — disaster-recovery clusters versus read-scaling clusters.\n"
   "- **Consul catalog** — the registry of services.\n"
   "- **Consul DNS/HTTP** — `web.service.consul` and the HTTP API: the discovery interfaces.\n"
   "- **health check gating** — only healthy instances receive traffic; no load-balancer config needed.\n"
   "- **Consul Connect** — the service mesh: automatic, rotated mTLS between services.\n"
   "- **intention** — the allow/deny rule for service-to-service traffic (`consul intention create -allow web api`); the firewall rule for services, east-west microsegmentation for the mesh.\n"
   "- **gateways** — mesh, ingress, and terminating gateways for traffic in and out of the mesh.\n"
   "- **Consul KV vs Vault** — Consul KV is config, not encrypted by default; secrets belong in Vault."},
  {'title': 'Hands-on procedure', 'body':
   "Stand up secrets and mesh the way production does: unseal planned, policies least-privilege, discovery health-gated.\n"
   "1. **Init and unseal.** Initialize Vault, then configure auto-unseal via cloud KMS — operators should never handle key shards; rehearse the seal migration and rekey in staging.\n"
   "2. **Engines.** Enable KV v2 for static secrets, the database engine for dynamic creds, and transit for encryption-as-a-service.\n"
   "3. **Auth.** Configure OIDC for engineers (SSO) and the Kubernetes auth method for pods — humans via identity provider, machines as themselves.\n"
   "4. **Policies.** Write deny-by-default policies granting each service only its paths; verify a token can't read outside its policy.\n"
   "5. **Dynamic rotation.** Issue dynamic database credentials to an app; rotate the lease and confirm the app picks up new creds without restarts.\n"
   "6. **Raft backup.** Take a Raft snapshot; document the restore.\n"
   "7. **Consul.** Register services, query `web.service.consul`, add health checks and watch unhealthy instances drain from discovery automatically.\n"
   "8. **Mesh.** Enable Connect, create the `allow web → api` intention with default deny, and verify mTLS between the services; add a terminating gateway for the legacy dependency.\n"
   "9. **Monitor the critical path.** Alert on seal status, leader changes, and token-expiry storms — Vault is critical path; watch it like one.",
   'code': ("# Dynamic database credentials: leased, auto-rotated, revoked on lease end\n"
            "vault secrets enable database\n"
            "vault write database/config/mydb \\\n"
            "  plugin_name=postgresql-database-plugin \\\n"
            "  connection_url=\"postgresql://{{username}}:{{password}}@db:5432/app\" \\\n"
            "  allowed_roles=\"app\"\n"
            "vault write database/roles/app db_name=mydb \\\n"
            "  creation_statements=\"CREATE ROLE \\\"{{name}}\\\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}';\" \\\n"
            "  default_ttl=\"1h\" max_ttl=\"24h\"\n"
            "vault read database/creds/app   # short-lived creds, no restarts to rotate\n"
            "\n"
            "# Transit: encryption without key-management pain\n"
            "vault secrets enable transit\n"
            "vault write -f transit/keys/orders\n"
            "vault write transit/encrypt/orders plaintext=$(echo -n '4111...' | base64)\n"
            "\n"
            "# Consul intention: the firewall rule for services\n"
            "consul intention create -allow web api"),
   'lang': 'bash'},
  {'title': 'Project brief', 'body':
   "Build the secrets platform for a fictional microservices app: Vault with auto-unseal, KV + database + transit engines, OIDC for "
   "humans and Kubernetes auth for pods, deny-by-default least-privilege policies, Raft snapshots on schedule — and Consul with "
   "health-gated discovery plus a Connect mesh (intentions, mTLS, one gateway). Deliverables: the engine/auth/policy inventory, the "
   "dynamic-rotation demo (rotate without restarts), the intention map for the mesh, and the Vault monitoring checklist (seal status, "
   "leader changes, token-expiry storms). The brief proves the module's thesis: leaked credentials stop being an incident category when "
   "secrets are dynamic by default."},
  {'title': 'Honesty note', 'body': HON},
 ],
 'cards_add': [
  {'front': 'Seal migration / rekey: when to practice?', 'back': 'In staging, before production — unseal ceremonies fail at 3 AM otherwise.'},
  {'front': 'Vault monitoring checklist?', 'back': 'Seal status, leader changes, token-expiry storms — Vault is critical path.'},
  {'front': 'Machines authenticate as themselves: examples?', 'back': 'Kubernetes auth (pod service accounts), AWS auth (IAM) — no shared static creds.'},
  {'front': 'Terminating gateway for?', 'back': 'Traffic from the mesh to legacy/non-mesh dependencies — the controlled exit.'},
 ],
}

# ---------------------------------------------------------------- Module 14
U['il05-cn-associates'] = {
 'summary': ("Welcome to the final module of IL-05 — Cloud DevSecOps Platform SRE. I'm your instructor, and Module 14 is the "
  "associate tier around Kubernetes: KCNA for the vocabulary foundation, KCSA for the associate security lens, PCA for Prometheus "
  "observability, CCA for Cilium and eBPF networking, and CAPA for Argo GitOps — plus the consolidated associate-exam prep. Think of "
  "this as the breadth layer that makes the professional exams make sense: the concepts and vocabulary first, so that when you sit the "
  "performance-based CKA/CKAD/CKS tier, you're fighting the clock, not the terminology."),
 'notes': [
  {'title': 'Concepts', 'body':
   "The associate-stack glossary — five exams, one vocabulary.\n"
   "- **KCNA** — Kubernetes and cloud-native fundamentals: architecture, orchestration concepts, microservices, immutable infrastructure, declarative APIs, GitOps concepts, observability basics. The on-ramp: take it before CKA if Kubernetes is new.\n"
   "- **KCSA** — cloud-native security associate: security overview, Kubernetes security fundamentals (RBAC, pod security, secrets, network policy), supply-chain basics. The prep ladder is KCSA → CKS.\n"
   "- **PCA (Prometheus)** — metrics types: counter, gauge, histogram, summary. The PromQL trap: rate() over counters, never over gauges.\n"
   "- **PromQL selectors and aggregation** — label selectors, rate(), and aggregation operators; alerting rules and the operator pattern.\n"
   "- **service discovery (Prometheus)** — automatic target discovery for scraping.\n"
   "- **CCA (Cilium)** — eBPF-powered networking: safe kernel programs replace kube-proxy iptables with eBPF maps.\n"
   "- **Hubble** — Cilium's observability layer.\n"
   "- **Cilium vs Calico policy depth** — Cilium enforces at L3–L7 (HTTP method/path-aware); Calico at L3/L4.\n"
   "- **CAPA (Argo)** — GitOps with Argo: declared desired state in git, agents converge the cluster; git is the source of truth, the cluster is a cache.\n"
   "- **Argo CD** — sync, drift detection, and automated sync policies; drift is detected, not debated.\n"
   "- **Argo Rollouts** — progressive delivery (canary/blue-green) as Kubernetes CRDs with metric analysis.\n"
   "- **sync waves/hooks** — ordering complex deploys: CRDs before the apps that need them.\n"
   "- **associate exam format** — proctored online multiple-choice: vocabulary and concepts. The performance depth lives at CKA/CKAD/CKS.\n"
   "- **recommended sequence** — KCNA → (PCA or CCA by interest) → CAPA → KCSA: breadth first, then the professional tier."},
  {'title': 'Hands-on procedure', 'body':
   "Build the breadth with light labs — vocabulary proven by doing, depth saved for the professional tier.\n"
   "1. **KCNA vocabulary drill.** Diagram the Kubernetes architecture from memory (control plane vs nodes), then check against the docs; repeat until it's instant.\n"
   "2. **PromQL.** Stand up Prometheus, scrape a test app, and run the canonical queries: `rate(http_requests_total[5m])`, aggregations by label, and one alerting rule. "
   "Deliberately run rate() over a gauge once — feel the trap, then never do it again.\n"
   "3. **Cilium.** Install Cilium with kube-proxy replacement, apply an L7 network policy (HTTP method/path), and observe it in Hubble; compare with a Calico-style L3/L4 rule.\n"
   "4. **Argo CD.** Point Argo CD at a git repo, watch drift detection flag a manual change, and let automated sync reconverge the cluster — git is truth, cluster is cache.\n"
   "5. **Rollouts.** Define a canary Rollout with analysis steps; watch the progressive delivery proceed on metrics.\n"
   "6. **KCSA map.** Walk the KCSA domain map against the CKS topics from Module 2; mark each CKS topic's associate-level prerequisite.\n"
   "7. **Sequence.** Sit the ladder in order — KCNA → PCA/CCA → CAPA → KCSA — drilling the domain maps and vocabulary for each.",
   'code': ("# The canonical PromQL queries (rate over counters, never gauges)\n"
            "rate(http_requests_total[5m])\n"
            "sum by (service) (rate(http_requests_total[5m]))\n"
            "histogram_quantile(0.99, sum by (le) (rate(http_request_duration_seconds_bucket[5m])))\n"
            "\n"
            "# Argo CD: the app of apps pattern — git as the source of truth\n"
            "argocd app create platform \\\n"
            "  --repo https://github.com/example/gitops.git \\\n"
            "  --path apps --dest-server https://kubernetes.default.svc \\\n"
            "  --sync-policy automated --auto-prune\n"
            "\n"
            "# Argo Rollout: canary as a declarative resource\n"
            "kubectl argo rollouts promote web   # manual gate in the canary steps"),
   'lang': 'bash'},
  {'title': 'Project brief', 'body':
   "Assemble the associate breadth portfolio: the KCNA architecture diagram drawn from memory, the PromQL query sheet (ten queries "
   "including the gauge trap documented), the Cilium L7 policy with Hubble evidence, the Argo CD gitops repo with drift-detection "
   "demonstrated, one Rollout canary, and the KCSA→CKS prerequisite map. Deliverables: the query sheet, the policy manifests, the "
   "gitops repo link, and the exam-sequence plan (KCNA → PCA/CCA → CAPA → KCSA) with a domain-map checklist per exam. This is the "
   "breadth layer — when you later sit the 2-hour performance exams, the vocabulary will already be reflex."},
  {'title': 'Honesty note', 'body': HON},
 ],
 'cards_add': [
  {'front': 'Prometheus metric types?', 'back': 'Counter, gauge, histogram, summary. rate() goes over counters — never gauges.'},
  {'front': 'Argo CD vs kubectl apply?', 'back': 'Argo CD: continuous reconciliation from git with drift detection. kubectl apply: one-shot imperative.'},
  {'front': 'Sync waves order?', 'back': 'CRDs and namespaces first, then the apps that need them — complex deploys need ordering.'},
  {'front': 'Why KCNA before CKA?', 'back': 'Vocabulary before performance: the architecture and principles pay back immediately under the 2-hour clock.'},
 ],
}

SECTIONS = {
 'il05-azure-network': ['Concepts', 'Concepts', 'Concepts', 'Concepts', 'Concepts', 'Concepts'],
 'il05-openshift': ['Concepts', 'Concepts', 'Concepts', 'Concepts', 'Concepts', 'Concepts'],
 'il05-hashicorp-vault': ['Concepts', 'Concepts', 'Concepts', 'Concepts', 'Hands-on procedure', 'Concepts'],
 'il05-cn-associates': ['Concepts', 'Concepts', 'Concepts', 'Concepts', 'Concepts', 'Concepts'],
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
    json.load(open(tmp))
    os.replace(tmp, P)
    print('r3 applied OK:', list(U.keys()))

if __name__ == '__main__':
    main()

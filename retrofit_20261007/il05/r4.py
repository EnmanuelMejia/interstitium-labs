#!/usr/bin/env python3
"""Retrofit IL-05 paths in catalog shards B and D: add path-level topics, sources, il_provides."""
import json, os, tempfile

FILES = [
    os.path.expanduser('~/workspace/apex-audit/docs/university/data/catalog/shard-b.json'),
    os.path.expanduser('~/workspace/apex-audit/docs/university/data/catalog/shard-d.json'),
]

TOPICS = {
 'il05-devops-core': ["The seven DevOps roles and their boundaries", "Linux, shell, and Git for DevOps",
   "Docker: images, layers, multi-stage builds", "Jenkins pipelines as code with security gates",
   "Kubernetes foundations: pods to Helm", "Ansible for fleet state", "Observability: Prometheus, Grafana, Loki"],
 'il05-cloud-native': ["Kubernetes architecture and etcd", "Workloads, scheduling, and troubleshooting (CKA)",
   "Application deployment for developers (CKAD)", "Cluster hardening and supply-chain security (CKS)",
   "Performance-based exam technique: kubectl speed"],
 'il05-zero-trust': ["NIST SP 800-207: the seven tenets", "Policy engine, administrator, and enforcement point",
   "Identity as the perimeter: phishing-resistant MFA, device posture", "Microsegmentation and east-west traffic",
   "Deployment models and migration from perimeter security"],
 'il05-terraform': ["HCL: resources, providers, variables, outputs", "The core workflow: init, validate, plan, apply",
   "State: remote backends, locking, import, refactoring", "Module composition and workspaces",
   "Terraform Associate (003) exam domains"],
 'il05-azure-admin': ["Entra ID and RBAC with PIM", "Governance: management groups, policy, locks",
   "Storage accounts: tiers, redundancy, lifecycle", "Compute: VMs, VMSS, containers",
   "Virtual networking and Private Endpoints", "Monitoring, backup, and recovery"],
 'il05-azure-architect': ["Identity, governance, and monitoring design", "Data design: Azure SQL, Cosmos DB, Storage",
   "Business continuity to RTO/RPO", "Infrastructure design: compute, hub-spoke network, migrations",
   "Architecture capstone with trade-off documentation"],
 'il05-azure-network': ["VNet design: addressing, peering, private DNS", "Connectivity: VPN Gateway, ExpressRoute, Virtual WAN",
   "Application delivery: LB, App Gateway, Front Door, Traffic Manager", "Private Link and service endpoints",
   "Azure Firewall, DDoS Protection, Bastion"],
 'il05-aws-architect': ["Resilient architectures: multi-AZ, decoupling, DR", "High-performing: compute, storage, database selection",
   "Secure: IAM, KMS, security groups vs NACLs, WAF", "Cost-optimized: pricing models, S3 tiers, right-sizing",
   "Terraform reference stacks"],
 'il05-aws-cloudops': ["Deployment and provisioning: CloudFormation, blue/green", "Reliability and business continuity",
   "Security and compliance operations", "Networking and content delivery", "Cost and performance optimization"],
 'il05-aws-devops': ["SDLC automation: CodePipeline, canary, feature flags", "IaC at scale: nested stacks, StackSets",
   "Resilient multi-region solutions", "Monitoring and logging: CloudWatch, X-Ray", "Incident response and pipeline security"],
 'il05-aws-security': ["Threat detection and incident response", "Security logging and monitoring",
   "Infrastructure security", "IAM: boundaries, SCPs, ABAC, cross-account roles",
   "Data protection and the hardened landing zone"],
 'il05-openshift-admin': ["Containers and Kubernetes foundations", "OpenShift cluster administration: projects, quotas, storage",
   "Operators and day-2 operations", "Automation and multi-cluster management"],
 'il05-openshift-dev': ["Containerizing applications", "OpenShift deploy patterns: S2I, routes, probes",
   "Resilient microservices and service mesh", "Quarkus cloud-native development", "Twelve-factor capstone"],
 'il05-hashicorp-vault': ["Vault secrets engines: KV, dynamic, PKI, transit", "Auth methods and least-privilege policies",
   "Vault operations: unseal, Raft, replication", "Consul service discovery", "Consul Connect service mesh"],
 'il05-cn-associates': ["KCNA: Kubernetes and cloud-native fundamentals", "KCSA: cloud-native security associate",
   "PCA: Prometheus observability", "CCA: Cilium and eBPF networking", "CAPA: Argo GitOps"],
}

BLURBS = {
 'il05-devops-core': ("Welcome to the path that sequences the whole DevOps toolchain for you, in adoption order. "
  "I'm your instructor, and we'll move role by role — from Linux and Git through Docker, Jenkins, Kubernetes, Ansible, "
  "and observability — with milestone projects that prove each tool against a running system. You finish with the full "
  "containerize-to-observe arc as a portfolio artifact."),
 'il05-cloud-native': ("This is the Kubernetes certification ladder, climbed in order: KCNA vocabulary, CKA administration and "
  "troubleshooting, CKAD developer workflows, then the CKS security tier. I'm your instructor, and every exam here is "
  "performance-based, so we drill the kubectl speed and the fixed triage order the 2-hour clock rewards. You finish able "
  "to fix a broken cluster live — which is the actual job."),
 'il05-zero-trust': ("We turn NIST SP 800-207 from a publication into a platform blueprint you can build. I'm your instructor: "
  "we'll walk the seven tenets and the policy engine/administrator/enforcement point, rebuild the perimeter around identity, "
  "microsegment the east-west traffic where lateral movement lives, and sequence a real migration from perimeter security. "
  "The exam tests the models; the job tests the patience — we prepare you for both."),
 'il05-terraform': ("HashiCorp Terraform through the Associate exam, taught as a discipline. I'm your instructor, and we treat "
  "the plan as the code review of infrastructure and state as the crown jewels — remote, locked, and never hand-edited. You'll "
  "compose modules, import brownfield, refactor without destroy/recreate, and reason every 'what happens when' from the state model."),
 'il05-azure-admin': ("Run Azure like a production tenant, not a demo. I'm your instructor: we start with identity as the control "
  "plane — Entra ID, RBAC, and PIM with no standing admin — then govern with management groups and policy, and operate storage, "
  "compute, networking, and monitoring on a real subscription. Every objective is labbed; the portal is the exam."),
 'il05-azure-architect': ("Design, not administer — that's the AZ-305 shift. I'm your instructor, and we'll design identity, data, "
  "continuity, and infrastructure for a multi-subscription enterprise, closing with the architecture capstone: a full design with "
  "documented trade-offs. Two good architects can disagree here; both must defend. That's the grading bar."),
 'il05-azure-network': ("Packets don't lie; configs do. I'm your instructor for the AZ-700 network specialist track: addressing "
  "planned once and forever, hub-spoke with shared security services, connectivity picked by SLA, delivery picked by layer and "
  "scope, PaaS made private, and Bastion everywhere. The exam tests selection, not syntax — we drill the constraint that picks "
  "each service."),
 'il05-aws-architect': ("Well-Architected, by construction. I'm your instructor: we design for failure across AZs, decouple with "
  "queues, choose compute/storage/database by workload pattern, layer security from IAM to WAF, and cost it across pricing models "
  "and tiers — then codify every architecture as composable Terraform modules. SAA scenarios hide two plausible answers; we train "
  "the constraint-first elimination."),
 'il05-aws-cloudops': ("The operator's exam, taught as runbooks. I'm your instructor: blue/green deploys with real rollback stories, "
  "backups proven by tested restores, drift detection that finds the console cowboys, and the GuardDuty-to-remediation response loop. "
  "Every domain here is a monitor → detect → respond decision — the SysOps exam is scenario-dense, and so are we."),
 'il05-aws-devops': ("The professional tier: ship it safely, prove it shipped. I'm your instructor, and we'll build gated canary "
  "pipelines with automatic rollback, feature flags that decouple deploy from release, IaC at org scale with StackSets, X-Ray-traced "
  "systems, chaos-proven resilience, and signed artifacts. It's 180 minutes of scenarios — we train the pace and the elimination."),
 'il05-aws-security': ("Assume breach, prove control. I'm your instructor for the security specialty: detect with GuardDuty and "
  "investigate with Detective, log everything into an immutable org trail, bound IAM with SCPs and ABAC, protect data with envelope "
  "encryption, and assemble the hardened landing zone. Secure by default, compliant by construction — every control shows its "
  "enforcement, not just its existence."),
 'il05-openshift-admin': ("Kubernetes with an opinion — learn the opinion. I'm your instructor for the OpenShift administrator track: "
  "projects and quotas for multitenancy, S2I and routes for developers, Operators as code, and the day-2 operations that are the "
  "actual job — upgrades, etcd backup, cert rotation. These are performance exams on live clusters; speed with oc is the skill."),
 'il05-openshift-dev': ("Ship twelve-factor apps on the platform teams actually run. I'm your instructor: containerize cleanly, deploy "
  "with OpenShift patterns, build resilient microservices with mesh-backed fault tolerance, and develop cloud-native Java with "
  "Quarkus — closing with the twelve-factor capstone. One immutable image, every environment, config in the environment."),
 'il05-hashicorp-vault': ("Never hardcode a secret again. I'm your instructor: Vault's engines for static, dynamic, and transit secrets; "
  "auth methods so humans and machines each authenticate as themselves; deny-by-default policies; and the operations reality of unseal, "
  "Raft, and replication. Then Consul: health-gated discovery and a Connect mesh with intentions. Dynamic secrets solve the "
  "leaked-credential problem structurally."),
 'il05-cn-associates': ("The associate layer, all of it — the breadth that makes the professional exams make sense. I'm your instructor: "
  "KCNA for vocabulary, KCSA for the security lens, PCA for Prometheus, CCA for Cilium and eBPF, CAPA for Argo GitOps. Breadth first, "
  "then the performance tier — when you sit the 2-hour exams, the terminology will already be reflex."),
}

def harvest_sources(path):
    seen = {}
    for mod in path.get('modules', []):
        for s in mod.get('sources', []):
            url = s.get('url', '')
            if url and url not in seen:
                seen[url] = {'name': s.get('name', url), 'url': url,
                             'note': (s.get('note', '') or '')[:220]}
            if len(seen) >= 3:
                break
        if len(seen) >= 3:
            break
    return list(seen.values())

def main():
    touched = {}
    for fp in FILES:
        with open(fp) as f:
            d = json.load(f)
        n = 0
        for path in d['paths']:
            pid = path.get('id', '')
            if pid in TOPICS:
                path['topics'] = TOPICS[pid]
                path['sources'] = harvest_sources(path)
                assert path['sources'], pid  # must have harvested in-repo URLs
                path['il_provides'] = BLURBS[pid]
                n += 1
        fd, tmp = tempfile.mkstemp(dir=os.path.dirname(fp), suffix='.json')
        with os.fdopen(fd, 'w') as f:
            json.dump(d, f, indent=1, ensure_ascii=False)
            f.write('\n')
        json.load(open(tmp))
        os.replace(tmp, fp)
        touched[fp] = n
    print('shard retrofit OK:', touched)

if __name__ == '__main__':
    main()

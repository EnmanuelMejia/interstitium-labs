#!/usr/bin/env python3
"""Build IL28-M44 module object -> part_f_m44.json"""
import json

notes = [
{"title": "When to Use Which Cloud: A Decision Framework",
"body": "Choose a cloud per workload, not per fashion. The framework has five lenses. (1) Service fit: each cloud leads somewhere — if your data warehouse and analytics gravity is BigQuery, GCP pulls; if your enterprise identity is Microsoft Entra and your apps are .NET, Azure pulls; if you need the broadest service catalog and region count, AWS pulls. (2) Team skill: a team fluent in ARM/Bicep and Azure networking will ship faster on Azure than relearning IAM and VPCs under deadline. (3) Commercial terms: existing enterprise agreements, committed-use discounts, and credits can outweigh technical preferences. (4) Latency and residency: users and regulators pin regions; the cloud with the right region wins regardless of features. (5) Exit cost: managed services with proprietary APIs (the serverless and AI offerings especially) raise switching costs; VMs and Kubernetes keep you portable. Worked example: a .NET shop on Entra with a new Python analytics workload. Solution: keep the .NET estate on Azure (identity and skill fit), but evaluate the analytics workload independently — if it is mostly BigQuery-shaped, a deliberate two-cloud footprint with Terraform managing both beats forcing analytics onto the wrong platform. The anti-pattern is 'we are a single-cloud shop' as dogma, and equally 'every team picks its own cloud' as anarchy — the framework forces a written reason per workload."},
{"title": "Terraform as the Cloud-Agnostic Control Plane",
"body": "Terraform is the closest thing to a neutral control plane: one language, one state model, one plan/apply workflow across providers. The portability is real but partial, and panels probe the boundary. What transfers: resource lifecycle thinking, module composition, for_each patterns, state management, and CI-driven applies. What does not transfer: provider schemas (an azurerm_virtual_network and an aws_vpc share nothing but the concept), IAM models (role assignments vs policies vs bindings), and identity federation for the pipeline itself. The professional pattern is a thin provider-specific module per cloud exposing a common interface: module 'network' with inputs like cidr_block and outputs like subnet_ids, implemented once per cloud. Worked example: provision a two-tier network on both Azure and AWS from one root module. Solution sketch: root module calls module/network-azure and module/network-aws, each wrapping the native resources; shared locals define the CIDR plan once; outputs converge to subnet IDs consumed identically downstream. The trap: writing 'cloud-agnostic' HCL that secretly depends on one provider's defaults (e.g. assuming AWS-style security groups exist on Azure) — abstraction without testing is fiction. Test every module against every provider it claims to support, in CI, on every change."},
{"title": "Case Study (Hypothetical): A Large Bank Standardizes on One Primary Cloud",
"body": "Exercise — hypothetical, no claims about any real institution: a large bank with 40,000 employees decides to standardize on one primary cloud while keeping a second for specific workloads. Walk the decision the way a panel wants to hear it. Drivers for standardizing: one identity model for auditors, one network architecture for the security team to certify, one skill ladder for hiring, volume pricing on commits, and a single incident-response playbook. Drivers for keeping the second cloud: a trading analytics team already productive on its data platform, a regulator requiring in-country processing where only one cloud has the region, and acquisition targets running elsewhere. The decision output is not 'Azure' or 'AWS' — it is a written cloud strategy: primary cloud for 80% of workloads, approved exceptions with sunset reviews, Terraform modules for both, and a landing-zone per cloud with identical guardrails (policy, logging, identity). The interview answer the panel wants: 'Standardize the operating model, not necessarily the provider; make exceptions explicit, reviewed, and temporary.' The failure mode is shadow multicloud — teams adopting a second cloud without the security team knowing, which is how breaches and surprise bills happen. Governance first, provider second."},
{"title": "Data Gravity and Egress Economics",
"body": "Data has gravity: the larger the dataset and the more services touch it, the harder it is to move, and every cloud bills for data leaving its network. The economics are qualitative but decisive: ingress is generally free, egress and cross-region transfer are metered, and moving a multi-terabyte warehouse between clouds can cost more than a year of compute. Design consequences: keep compute next to data (same region, ideally same cloud); replicate only what DR truly requires and compress before transfer; prefer private connectivity (ExpressRoute, Direct Connect, Interconnect) for steady high-volume flows over the public internet. Worked example: a 50 TB analytics dataset queried daily by dashboards, with a proposal to run the dashboards' compute on a different cloud 'because the BI tool is nicer there'. Analysis: every dashboard refresh would pull data across clouds over metered egress, and the BI tool would need a full replica to be usable — the 'nicer tool' premium is dwarfed by transfer costs and replica management. Solution: run the BI compute in the same cloud and region as the data, or formally cost the replica plus egress before deciding. The panel one-liner: 'Data gravity decides the cloud; compute follows the data, not the other way around.'"},
{"title": "Regulatory, Residency, and Sovereignty Constraints",
"body": "Regulators and contracts constrain cloud choice more than engineers like to admit. Financial services face requirements around data residency (customer data stays in-country), audit access (regulators can inspect), operational resilience (survive a provider outage), and increasingly sovereignty (data under domestic legal control). The practical toolkit: region selection with in-country regions, customer-managed keys (CMK/BYOK) so the provider cannot read data at rest without your key, private connectivity instead of public endpoints, and contractual terms covering audit rights and exit assistance. Worked example: a payments workload must keep cardholder data in-country and survive a cloud region failure. Solution: primary deployment in the in-country region with CMK-encrypted storage, private endpoints (Private Link / Private Service Connect) so traffic never traverses the public internet, and a tested failover to a second in-country region — with the failover's data residency verified, not assumed. The trap: assuming 'the cloud is compliant' — compliance is a property of your architecture plus the provider's attestations, never of the provider alone. You inherit the audit burden for everything you configure."},
{"title": "Operating Model: The Hidden Cost of Multicloud",
"body": "The dominant cost of multicloud is cognitive, not metered: every additional cloud multiplies the runbooks, IAM models, network designs, incident playbooks, and hiring profiles your platform team must master. A team that is expert in one cloud and novice in two ships slower and incidents worse on all three. The operating-model decision therefore precedes the provider decision: will you run a central platform team (one paved road, opinionated modules, self-service), embedded product teams (each owns its cloud footprint), or a hybrid? The central platform team is the enterprise answer: it publishes Terraform modules, enforces policy, and absorbs the multicloud complexity so product teams see one interface. Worked example: three product teams each built their own networking on three clouds; an incident requires correlating logs across all three at 3 AM. Solution going forward: the platform team publishes one 'landing zone' module per approved cloud with identical guardrails — logging to the central SIEM, identity via the corporate IdP, policy denying public storage — and product teams may only deploy through it. New clouds require platform-team certification first. The panel answer: 'Multicloud without a platform team is just three separate clouds with three times the toil.'"},
]

cards = [
{"front": "Five lenses of the cloud decision framework", "back": "Service fit, team skill, commercial terms, latency/residency, exit cost — one written reason per workload"},
{"front": "What Terraform portability really covers (and what it does not)", "back": "Transfers: lifecycle thinking, modules, for_each, state, CI applies. Does NOT transfer: provider schemas, IAM models, pipeline identity federation"},
{"front": "The professional multicloud Terraform pattern", "back": "Thin provider-specific modules exposing a common interface (inputs/outputs); shared locals; every module tested against every claimed provider in CI"},
{"front": "Hypothetical bank case study: the decision output is not a provider name — what is it?", "back": "A written cloud strategy: primary cloud for most workloads, explicit reviewed exceptions, landing zones with identical guardrails on each approved cloud"},
{"front": "What is shadow multicloud and why is it dangerous?", "back": "Teams adopting clouds without security/governance knowledge — breaches, surprise bills, unaudited data flows. Governance first, provider second"},
{"front": "Data gravity in one line", "back": "Compute follows the data: keep compute in the same cloud/region as the dataset; metered egress makes cross-cloud data flows expensive"},
{"front": "Design consequences of egress economics", "back": "Compute next to data; replicate only for real DR; compress before transfer; private connectivity for steady high-volume flows"},
{"front": "Regulatory toolkit for financial workloads", "back": "In-country regions, customer-managed keys, private endpoints (no public internet traversal), tested failover with verified residency, contractual audit rights"},
{"front": "'The cloud is compliant' — why is this wrong?", "back": "Compliance is a property of YOUR architecture plus provider attestations; you inherit the audit burden for everything you configure"},
{"front": "The dominant cost of multicloud", "back": "Cognitive: multiplied runbooks, IAM models, network designs, playbooks, hiring profiles — the platform team absorbs it or everyone pays it during incidents"},
{"front": "Enterprise answer to multicloud complexity", "back": "Central platform team publishing opinionated landing-zone Terraform modules with identical guardrails; product teams deploy only through them"},
{"front": "Panel one-liner: standardize what, not which?", "back": "Standardize the operating model, not necessarily the provider — exceptions explicit, reviewed, and temporary"},
]

quiz = [
{"q": "A .NET shop on Entra needs a new Python analytics workload. Best approach per the framework?",
"choices": ["Force it onto the existing stack regardless of fit", "Evaluate it independently: keep .NET on Azure, but allow the analytics workload on the best-fit platform with Terraform managing both", "Rewrite the .NET estate first", "Let every team pick randomly"],
"answer": 1,
"explain": "The framework demands a written reason per workload: identity/skill fit keeps .NET where it is, while analytics gets its own evaluation. Dogma and anarchy both fail."},
{"q": "What does Terraform's portability NOT give you across clouds?",
"choices": ["Shared lifecycle and module patterns", "Identical provider schemas and IAM models", "One plan/apply workflow", "State management concepts"],
"answer": 1,
"explain": "Providers expose entirely different schemas and identity models; only the workflow patterns and abstractions transfer. Assuming schema parity is the classic trap."},
{"q": "A module claims to support AWS and Azure but was only tested on AWS. What is the verdict?",
"choices": ["Ship it", "Abstraction without testing is fiction — test against every claimed provider in CI", "Delete the Azure code path", "It will probably work"],
"answer": 1,
"explain": "Untested provider paths rot silently on provider defaults and schema drift. The professional pattern requires CI-tested parity."},
{"q": "In the hypothetical bank case study, what is 'shadow multicloud'?",
"choices": ["A backup cloud region", "Teams adopting clouds without security/governance knowledge", "A dark-mode console theme", "Encrypted cloud storage"],
"answer": 1,
"explain": "Untracked adoption bypasses guardrails — the source of breaches and surprise bills. Governance first, provider second."},
{"q": "A proposal moves BI compute to another cloud while the 50 TB dataset stays put. What is the flaw?",
"choices": ["BI tools do not work cross-cloud", "Metered egress on every refresh plus replica management dwarfs the tool's advantage — compute follows the data", "Datasets cannot be queried remotely", "It is always cheaper"],
"answer": 1,
"explain": "Data gravity: the transfer and replica costs dominate. Cost the replica plus egress formally before deciding."},
{"q": "Cardholder data must stay in-country and survive a region failure. Which design is correct?",
"choices": ["Single region, provider-managed keys, public endpoints", "In-country primary + second in-country region, customer-managed keys, private endpoints, verified failover residency", "Store it in two different countries for safety", "Rely on the provider's compliance badge alone"],
"answer": 1,
"explain": "Residency plus resilience requires two in-country regions, CMK, no public-internet traversal, and verified — not assumed — failover residency."},
{"q": "Why is 'the cloud is compliant' a dangerous belief?",
"choices": ["Clouds are never compliant", "Compliance is a property of your architecture plus attestations; you inherit the audit burden for everything you configure", "Auditors dislike clouds", "Compliance does not apply to finance"],
"answer": 1,
"explain": "The provider's certifications cover their controls; your configurations, keys, networks, and IAM are your audit burden."},
{"q": "Three teams built their own networking on three clouds; 3 AM incidents are chaos. What is the structural fix?",
"choices": ["A fourth cloud", "A central platform team publishing certified landing-zone modules with identical guardrails; new clouds require certification", "More dashboards", "Ban Terraform"],
"answer": 1,
"explain": "The cognitive cost is the problem; the platform team absorbs multicloud complexity behind one interface with enforced guardrails."},
{"q": "Which statement best captures the module's strategy thesis?",
"choices": ["Always use exactly one cloud", "Always use all clouds", "Standardize the operating model; make provider exceptions explicit, reviewed, and temporary", "Cost does not matter"],
"answer": 2,
"explain": "The thesis: governance and operating model are the standardization target; provider choice follows workload reasons with explicit exception handling."},
]

drills = [
{"id": "il28-m44-decision", "title": "Timed drill: cloud decision reasoning",
"items": [
{"prompt": "90 seconds: name the five lenses for choosing a cloud per workload.", "answer": "Service fit, team skill, commercial terms, latency/residency, exit cost.",
"explain": "Recite all five, then apply: one written reason per workload, no dogma, no anarchy."},
{"prompt": ".NET on Entra plus a new Python analytics workload. Your recommendation?", "answer": "Keep .NET on Azure (identity + skill fit); evaluate analytics independently — best-fit platform, Terraform managing both.",
"explain": "Per-workload reasoning beats single-cloud dogma and per-team anarchy."},
{"prompt": "What transfers across clouds in Terraform, and what does not?", "answer": "Transfers: lifecycle, modules, for_each, state, CI applies. Does not: provider schemas, IAM models, pipeline federation.",
"explain": "Say both halves — panels probe the boundary, not just the promise."},
{"prompt": "Sketch the portable network module pattern.", "answer": "Thin provider-specific modules with a common interface (cidr_block in, subnet_ids out); shared locals; CI-tested per provider.",
"explain": "Common interface, native implementation, tested parity — the professional pattern."},
{"prompt": "Define data gravity and its design consequence.", "answer": "Large datasets attract compute; metered egress punishes separation. Consequence: compute follows the data — same cloud/region.",
"explain": "One line plus consequence; use the 50 TB BI example if asked to elaborate."},
{"prompt": "50 TB dataset, BI compute proposed on another cloud. Your analysis?", "answer": "Egress on every refresh + replica management dwarfs the tool advantage. Formally cost replica + egress, or co-locate.",
"explain": "Force the numbers before the decision — qualitative is fine, hand-waving is not."},
{"prompt": "State the multicloud strategy thesis in one sentence.", "answer": "Standardize the operating model, not necessarily the provider; exceptions explicit, reviewed, temporary.",
"explain": "This is the answer to 'should we be multicloud?' — governance first."},
]},
{"id": "il28-m44-governance", "title": "Timed drill: governance and operating model",
"items": [
{"prompt": "What is shadow multicloud and why does it matter?", "answer": "Untracked cloud adoption by teams; bypasses guardrails; causes breaches and surprise bills.",
"explain": "Governance first, provider second — say why, not just what."},
{"prompt": "Name four regulatory controls for a financial workload.", "answer": "In-country regions, customer-managed keys, private endpoints, verified failover residency (+ audit rights).",
"explain": "Residency, encryption control, network path, resilience proof."},
{"prompt": "Why is 'the cloud is compliant' wrong?", "answer": "Compliance = your architecture + provider attestations; you inherit the audit burden for everything you configure.",
"explain": "Their certs cover their controls; your configs are your burden."},
{"prompt": "What is the dominant cost of multicloud?", "answer": "Cognitive: multiplied runbooks, IAM models, networks, playbooks, hiring profiles.",
"explain": "Not the meter — the minds. This justifies the platform team."},
{"prompt": "Structural fix for three teams, three DIY clouds, chaotic incidents?", "answer": "Central platform team; certified landing-zone modules with identical guardrails; certification required for new clouds.",
"explain": "Absorb complexity behind one interface; enforce guardrails in code."},
{"prompt": "Two failure modes of cloud strategy — name both.", "answer": "Single-cloud dogma ('one cloud no matter the fit') and per-team anarchy (every team picks its own).",
"explain": "The framework exists to steer between these two ditches."},
{"prompt": "A regulator asks for audit access to your cloud estate. What did you prepare in advance?", "answer": "Contractual audit rights, centralized logging to the SIEM, CMK key inventory, and architecture docs showing residency and network paths.",
"explain": "Audit readiness is designed in — residency, keys, logs, contracts."},
]},
]

handsOnLab = {
"id": "il28-m44-lab",
"title": "Lab: one Terraform root, two clouds, one decision record",
"brief": "You will write a Terraform root module that provisions a two-tier network on two providers through a common module interface, validate both plans, and write the architecture decision record a panel would expect. Uses only plan (no apply), so there is no cloud spend.",
"steps": [
"Create the repo layout: root main.tf, modules/network-aws/, modules/network-azure/, each exposing variables cidr_block, az_count and outputs subnet_ids.",
"Write modules/network-aws: aws_vpc, public/private aws_subnets across az_count AZs, aws_internet_gateway, aws_nat_gateway with EIP, route tables. Keep it to ~60 lines.",
"Write modules/network-azure: azurerm_virtual_network, subnets, NAT gateway, route tables with equivalent topology. Same interface, native resources.",
"Write the root module: shared locals for the CIDR plan (10.10.0.0/16 etc.), one module block per cloud, outputs converging to {aws_subnets, azure_subnets}.",
"Run terraform init and terraform plan with dummy provider credentials (plan-only; use -refresh=false where needed). Confirm both providers plan cleanly.",
"Break portability deliberately: reference an AWS-only concept in the Azure module, watch plan fail, then fix it — document the failure as the 'abstraction without testing' lesson.",
"Write the decision record (ADR): workload = internal analytics VPC; evaluate AWS vs Azure vs GCP on the five lenses; record the choice and the rejected options with reasons.",
"Add the data-gravity section to the ADR: dataset location, query pattern, and why compute stays in the same region/cloud.",
"Add the governance section: which landing-zone guardrails apply (no public storage, centralized logging, corporate IdP) and who certifies a new cloud.",
"Run terraform fmt -check and terraform validate; fix all findings.",
"Peer-review swap: trade ADRs with a study partner (or self-review after 24h) and challenge one lens they underweighted.",
"Archive the ADR in the repo under docs/adr/0001-cloud-selection.md with status 'accepted'."],
"deliverable": "A Terraform repo with a common-interface network module implemented for two providers (plan-validated), plus a written architecture decision record covering the five lenses, data gravity, and governance.",
"checkpoint": "terraform validate passes for both modules; the ADR records a choice with explicit rejected options and reasons; docs/adr/0001-cloud-selection.md exists."
}

mockTask = {"id": "il28-m44-mock", "type": "choice",
"q": "Leadership proposes moving all analytics compute to Cloud X 'because the BI tool is nicer' while the 50 TB warehouse stays on Cloud Y. As the platform engineer, what is your response?",
"choices": ["Approve — tool preference decides", "Require a formal cost model: metered egress per refresh plus replica management, versus co-locating compute with the data; decide on numbers, not preference", "Move the warehouse too, immediately", "Ban BI tools"],
"answer": 1,
"explain": "Data gravity makes this a cost-architecture decision, not a tool-preference one. The formal model (egress + replica + ops) usually favors compute-follows-data; if the numbers still favor the move, it becomes an explicit, reviewed exception."}

module = {
"id": "IL28-M44", "code": "IL-28",
"title": "Multicloud Strategy & Comparison",
"summary": "Make deliberate cloud decisions: a five-lens selection framework, Terraform as the neutral control plane, data-gravity and egress economics, regulatory constraints, and the platform-team operating model that makes multicloud survivable.",
"objectives": [
"Apply the five-lens framework to choose a cloud per workload with written reasons",
"Design Terraform modules with a common interface across providers and test parity in CI",
"Reason about data gravity and egress economics in architecture decisions",
"Apply residency, sovereignty, and audit controls to financial-services workloads",
"Define the platform-team operating model that contains multicloud cognitive cost"],
"notes": notes, "cards": cards, "quiz": quiz, "weight": 2,
"prerequisiteFor": ["IL28-M49"],
"drills": drills, "handsOnLab": handsOnLab, "mockTask": mockTask,
"crossLinks": ["IL28-M49", "IL28-M41"],
"videos": [{"title": "Terraform Course - Automate your AWS cloud infrastructure", "url": "https://www.youtube.com/watch?v=SLB_c_ayRMo", "source": "YouTube - freeCodeCamp.org", "durationMin": 150, "order": 1, "watchBefore": "notes", "blurb": "Terraform foundations used here as the neutral control plane: focus on modules, state, and multi-provider patterns."}],
"estimatedMinutes": 660,
}

with open("/home/hatch/workspace/apex-audit/docs/university/data/courses/_il28-build/part_f_m44.json", "w") as f:
    json.dump(module, f, indent=2, ensure_ascii=False)
print("M44 written")

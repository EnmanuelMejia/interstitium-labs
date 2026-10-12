#!/usr/bin/env python3
"""Retrofit IL-05 modules 6-10 to the multicloud course template."""
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

# ---------------------------------------------------------------- Module 6
U['il05-aws-cloudops'] = {
 'summary': ("Welcome to Module 6 of IL-05 — Cloud DevSecOps Platform SRE. I'm your instructor, and this module is the "
  "operator's exam: the AWS Certified SysOps Administrator Associate. We'll provision with CloudFormation and ship blue/green "
  "deployments whose rollback story is the feature; design reliability and business continuity around backups, multi-AZ patterns, "
  "and Route 53 failover; run security and compliance operations with CloudTrail, Config, IAM Access Analyzer, and GuardDuty; "
  "and master the networking and cost/performance domains — VPC endpoints, CloudFront, right-sizing, and Graviton. The SysOps "
  "exam is scenario-dense: every domain is a runbook, so we drill monitor → detect → respond until it's reflex."),
 'notes': [
  {'title': 'Concepts', 'body':
   "The operator's glossary — every pair the exam loves to test.\n"
   "- **CloudFormation** — declarative infrastructure stacks; drift detection finds the console cowboys; StackSets extend to multi-account.\n"
   "- **blue/green deployment** — CodeDeploy shifts traffic between environments; the rollback story is the feature.\n"
   "- **Systems Manager** — Patch Manager, Run Command, Parameter Store: the operator's console.\n"
   "- **golden AMI** — baked, tested, distributed images via EC2 Image Builder; immutable infrastructure starts here.\n"
   "- **AWS Backup** — centralized backup policies with cross-region copy.\n"
   "- **Route 53 health checks + failover routing** — DNS steers away from the dead region.\n"
   "- **CloudTrail** — who did what: the API-activity audit log.\n"
   "- **Config** — what changed: resource state over time, with rules and remediation. The exam pairs Trail and Config constantly.\n"
   "- **IAM Access Analyzer** — finds unintended, over-permissive access; the least-privilege auditor.\n"
   "- **GuardDuty** — threat detection on the logs; findings feed EventBridge → Lambda/SSM for the automated response loop.\n"
   "- **Security Hub** — the aggregated security posture view.\n"
   "- **VPC Gateway endpoint** — S3/DynamoDB access off the internet; free, via a route-table entry.\n"
   "- **VPC Interface endpoint** — PrivateLink-powered access to other services; hourly charge.\n"
   "- **CloudFront signed URLs/cookies + OAC** — private content delivered through the CDN with authorized access.\n"
   "- **routing policies** — failover, latency-based, geoproximity: the Route 53 traffic shapes.\n"
   "- **Cost Explorer + Budgets** — spend visibility and guardrails.\n"
   "- **Compute Optimizer** — right-sizing recommendations.\n"
   "- **S3 lifecycle policies** — automatic tiering and expiry by age.\n"
   "- **gp3 over gp2** — cheaper and independently tunable.\n"
   "- **Graviton** — the price-performance processor option.\n"
   "- **untested backup** — a rumor; the RTO is only real if restores are proven on schedule."},
  {'title': 'Hands-on procedure', 'body':
   "Operate it like the exam's scenarios: deploy, back up, detect drift, respond.\n"
   "1. **Deploy blue/green.** Ship a CodeDeploy blue/green deployment; rehearse the rollback — the rollback story is the feature, "
   "and deploying without one is a hope.\n"
   "2. **Bake a golden AMI.** Use EC2 Image Builder to bake, test, and distribute an AMI; deploy from it so infrastructure stays immutable.\n"
   "3. **Back up to RTO/RPO.** Create an AWS Backup plan with cross-region copy, then actually test a restore — untested backups are rumors.\n"
   "4. **Wire the response loop.** Enable GuardDuty, route findings through EventBridge to a Lambda/SSM Automation remediation — "
   "detect to remediate without humans in the path.\n"
   "5. **Find the cowboys.** Run CloudFormation drift detection on a stack someone touched in the console; import or revert deliberately.\n"
   "6. **Audit access.** Run IAM Access Analyzer and remediate one over-permissive grant toward least privilege.\n"
   "7. **Cut the transfer bill.** Replace NAT-gateway S3 traffic with a Gateway VPC endpoint; serve private media via CloudFront "
   "signed URLs with Origin Access Control.",
   'code': ("# Gateway VPC endpoint: S3 traffic stays on the AWS network (free)\n"
            "aws ec2 create-vpc-endpoint \\\n"
            "  --vpc-id vpc-12345678 \\\n"
            "  --service-name com.amazonaws.us-east-1.s3 \\\n"
            "  --route-table-ids rtb-abcdef12\n"
            "\n"
            "# Drift detection: find the console cowboys\n"
            "aws cloudformation detect-stack-drift --stack-name web-prod\n"
            "aws cloudformation describe-stack-resource-drifts --stack-name web-prod\n"
            "\n"
            "# Who did what: recent API activity via CloudTrail lookup\n"
            "aws cloudtrail lookup-events --lookup-attributes AttributeKey=EventName,AttributeValue=ConsoleLogin"),
   'lang': 'bash'},
  {'title': 'Project brief', 'body':
   "Build the operator's runbook pack for a fictional two-tier app: the blue/green deployment procedure with its rollback steps, "
   "the backup plan (RTO/RPO stated, cross-region copy, restore-test schedule), the GuardDuty → EventBridge → SSM response loop for "
   "one finding type, and the monthly ops checklist (drift detection, Access Analyzer review, Cost Explorer + Compute Optimizer pass). "
   "Deliverables: the runbook document, the CloudFormation template, and evidence of one tested restore. The SysOps exam grades "
   "runbook decisions — monitor → detect → respond — and so does this brief."},
  {'title': 'Honesty note', 'body': HON},
 ],
 'cards_add': [
  {'front': 'Drift detection finds?', 'back': 'Console changes that bypassed CloudFormation — compare stack template to reality, then import or revert.'},
  {'front': 'Golden AMI via?', 'back': 'EC2 Image Builder: bake, test, distribute — immutable infrastructure starts here.'},
  {'front': 'CloudFront OAC + signed URLs?', 'back': 'Private bucket, CDN-delivered, authorized access — the pattern for private media.'},
  {'front': 'SysOps exam shape?', 'back': 'Scenario-dense: every question is a runbook decision — monitor → detect → respond.'},
 ],
}

# ---------------------------------------------------------------- Module 7
U['il05-aws-devops'] = {
 'summary': ("Welcome to Module 7 of IL-05 — Cloud DevSecOps Platform SRE. I'm your instructor, and we now climb to the "
  "professional tier: the AWS Certified DevOps Engineer Professional (DOP-C02). We'll automate the SDLC with CodePipeline, "
  "canary and linear deployments, and feature flags that decouple deploy from release; manage IaC at scale with nested stacks, "
  "StackSets, and drift governance; design resilient multi-region solutions with honest data-replication thinking and chaos "
  "experiments; trace systems with CloudWatch Logs Insights and X-Ray; and run incident response and pipeline security — signed "
  "artifacts, scanning gates, least-privilege pipeline roles. It's the longest exam at 180 minutes of scenarios; we train the "
  "pace and the constraint-first elimination it demands."),
 'notes': [
  {'title': 'Concepts', 'body':
   "The professional-tier vocabulary.\n"
   "- **CodePipeline** — the AWS SDLC automation service: source → build → deploy stages.\n"
   "- **canary deployment** — release in percentage steps (10% → 50% → 100%) with metric gates and automatic rollback on regression.\n"
   "- **linear deployment** — release a fixed percentage every N minutes.\n"
   "- **all-at-once deployment** — fastest, riskiest; no safety net.\n"
   "- **feature flag** — decouples deploy from release; the safest deployment is the one you can turn off without redeploying.\n"
   "- **nested stack** — CloudFormation composition: stacks calling stacks.\n"
   "- **StackSet** — one template deployed across N accounts and regions; the org-scale deployment primitive and the landing-zone tool.\n"
   "- **drift governance** — detecting and reconciling template-vs-reality drift at scale.\n"
   "- **active-active multi-region** — Route 53 plus replicated data; compute is the easy part, data replication is the hard part.\n"
   "- **chaos thinking / Fault Injection Simulator (FIS)** — prove resilience with injected failures; resilience is proven, not asserted.\n"
   "- **CloudWatch composite alarm** — alarms on the AND of symptoms; reduces noise versus alarming on each symptom.\n"
   "- **Logs Insights** — query language over CloudWatch Logs (e.g. filter @message like /ERROR/).\n"
   "- **X-Ray** — distributed tracing; the service map draws itself — start every latency hunt there.\n"
   "- **SSM Automation document** — the executable runbook; incident response as code.\n"
   "- **artifact signing** — CodeSigner/signer Lambda provenance: deploy only signed artifacts; unsigned artifacts don't deploy.\n"
   "- **pipeline IAM role** — the pipeline's identity is a blast radius; scope it with least privilege to exactly the deploy actions.\n"
   "- **blameless post-incident review** — fix the system, not the person."},
  {'title': 'Hands-on procedure', 'body':
   "Ship the professional way: gated rollouts, traced systems, signed artifacts.\n"
   "1. **Pipeline.** Build a CodePipeline (source → build → deploy) with a scanning gate before the deploy stage — SAST, dependency, and container scans.\n"
   "2. **Canary.** Deploy with a canary strategy (10% → 50% → 100%), gating each step on canary-vs-baseline error rate and latency with automatic rollback on regression.\n"
   "3. **Flag it.** Wrap the new feature in a feature flag so a bad release is mitigated by flipping the flag — no redeploy.\n"
   "4. **Scale the IaC.** Convert the stack to nested stacks, then deploy it across two regions with a StackSet.\n"
   "5. **Trace.** Instrument with X-Ray; open the service map and run one Logs Insights query to find the slow dependency.\n"
   "6. **Game day.** Run a Fault Injection Simulator experiment against the multi-region setup and record what actually failed over.\n"
   "7. **Sign.** Add artifact signing to the pipeline; verify an unsigned artifact is rejected at the deploy stage.\n"
   "8. **Pace.** Drill 180-minute scenario blocks: eliminate by constraint, flag the 50/50s, keep moving.",
   'code': ("# Logs Insights: find the errors fast\n"
            "fields @timestamp, @message\n"
            "| filter @message like /ERROR/\n"
            "| stats count() by bin(5m)\n"
            "\n"
            "# X-Ray: trace a request through 40 microservices\n"
            "aws xray get-trace-summaries \\\n"
            "  --start-time $(date -u -d '1 hour ago' +%s) \\\n"
            "  --end-time $(date -u +%s) \\\n"
            "  --filter-expression 'service(\"checkout-api\") { error = true }'"),
   'lang': 'bash'},
  {'title': 'Project brief', 'body':
   "Deliver the professional release train for a fictional checkout service: a CodePipeline with scanning and signing gates, a "
   "canary deployment with metric gates and automatic rollback, feature flags on the risky paths, the stack expressed as nested "
   "stacks deployed via StackSet to two regions, X-Ray tracing with one documented latency hunt, and an FIS game-day report. "
   "Deliverables: the pipeline definition, the canary/rollback runbook, the game-day findings, and a pacing plan for the 180-minute "
   "exam. The brief is graded on safety at scale — every shortcut must have its gate."},
  {'title': 'Honesty note', 'body': HON},
 ],
 'cards_add': [
  {'front': 'Canary metric gates watch?', 'back': 'Error rate + latency on the canary vs baseline — automatic rollback on regression.'},
  {'front': 'Active-active: the hard part?', 'back': 'Data replication (DynamoDB global tables, Aurora global) — compute is the easy part.'},
  {'front': 'Composite alarms reduce?', 'back': 'Noise — alarm on the AND of symptoms, not each symptom alone.'},
  {'front': 'SSM Automation document?', 'back': 'The executable runbook — incident response as code.'},
 ],
}

# ---------------------------------------------------------------- Module 8
U['il05-aws-security'] = {
 'summary': ("Welcome to Module 8 of IL-05 — Cloud DevSecOps Platform SRE. I'm your instructor, and this is the security "
  "specialty: the AWS Certified Security Specialty (SCS-C03). We'll detect and respond with GuardDuty, Detective, Security Hub, "
  "and Macie; log everything with org-wide CloudTrail, Config aggregators, and Athena forensics; lock IAM down with permission "
  "boundaries, SCPs, ABAC, and cross-account roles; protect data with KMS envelope encryption and hardened S3; and assemble the "
  "hardened landing zone — Control Tower with preventive and detective guardrails. The landing zone is the exam's favorite scenario: "
  "a new org, secure by default, compliant by construction."),
 'notes': [
  {'title': 'Concepts', 'body':
   "The specialty's glossary — detection, identity, data, and the landing zone.\n"
   "- **GuardDuty** — threat detection over the logs; produces findings.\n"
   "- **Detective** — investigation graphs: pivot from a finding to the entity to the timeline, in clicks not grep marathons.\n"
   "- **Security Hub** — aggregated security posture across accounts.\n"
   "- **Macie** — discovers and classifies PII in S3 at scale.\n"
   "- **org CloudTrail** — the multi-account API audit log; pair with an immutable bucket + Object Lock so attackers can't delete it.\n"
   "- **Config aggregator** — multi-account resource-state collection for compliance.\n"
   "- **Athena over CloudTrail** — SQL forensics over the log lake without a SIEM budget.\n"
   "- **incident response order** — isolate (revoke creds, quarantine security groups), eradicate, recover — with runbooks, not improvisation.\n"
   "- **permission boundary** — the maximum permissions a delegated admin can grant; caps their power.\n"
   "- **SCP (service control policy)** — org-level guardrail; bounds even root. SCPs restrict — they never grant.\n"
   "- **ABAC** — attribute-based access control: tag principals and resources, write one policy; scales where RBAC explodes.\n"
   "- **cross-account role** — temporary credentials for partner/third-party access; no long-lived keys, no rotation burden.\n"
   "- **WAF** — managed rules plus rate limiting; rate-based rules stop brute-force and scraping floods.\n"
   "- **Shield Advanced** — managed DDoS protection.\n"
   "- **Network Firewall** — VPC-level stateful inspection.\n"
   "- **PrivateLink** — access AWS services and partner services without traversing the internet.\n"
   "- **KMS envelope encryption** — the data key (DEK) encrypts the data; the KMS master key (KEK) encrypts the DEK — scale without KMS throttling.\n"
   "- **S3 Block Public Access** — set at the account level first; bucket policies are then defense in depth.\n"
   "- **S3 Object Lock** — immutability for compliance and log protection.\n"
   "- **Control Tower** — the account factory plus guardrails: the hardened landing zone.\n"
   "- **preventive guardrail** — SCPs (deny unencrypted S3, deny wrong regions): stops the bad action.\n"
   "- **detective guardrail** — Config rules and Security Hub findings: catches what slipped through."},
  {'title': 'Hands-on procedure', 'body':
   "Build the secure-by-default org, then prove you can investigate inside it.\n"
   "1. **Org trail.** Enable an org-wide CloudTrail into a dedicated log account with Object Lock on the bucket — the audit log attackers can't delete.\n"
   "2. **Aggregate.** Turn on the Config aggregator and Security Hub across the org; note one finding end to end.\n"
   "3. **Guardrails.** Apply preventive SCPs (deny unencrypted S3, deny deployments outside approved regions) and one detective Config rule; "
   "verify a violating action is blocked, not just flagged.\n"
   "4. **IAM depth.** Create a delegated admin with a permission boundary; write one ABAC policy using principal tags; grant a partner temporary "
   "access via a cross-account role — no access keys.\n"
   "5. **Data.** Enable account-level S3 Block Public Access; encrypt a bucket with a customer-managed KMS key (envelope encryption in action); "
   "run Macie on a test bucket.\n"
   "6. **Investigate.** Take a GuardDuty finding, pivot through Detective's graph to the root cause, and query the org trail with Athena for the full timeline.\n"
   "7. **Respond.** Execute the isolate → eradicate → recover runbook on a simulated compromised credential: revoke, quarantine the security group, rotate.",
   'code': ("# Athena forensics over the org CloudTrail lake (no SIEM budget needed)\n"
            "SELECT eventtime, useridentity.arn, eventname, sourceipaddress\n"
            "FROM cloudtrail_logs\n"
            "WHERE eventname = 'ConsoleLogin'\n"
            "  AND eventtime > date_add('day', -30, current_date)\n"
            "ORDER BY eventtime DESC\n"
            "LIMIT 100;\n"
            "\n"
            "# Preventive guardrail: deny unencrypted S3 org-wide (SCP)\n"
            "{\n"
            "  \"Version\": \"2012-10-17\",\n"
            "  \"Statement\": [{\n"
            "    \"Sid\": \"DenyUnencryptedS3\",\n"
            "    \"Effect\": \"Deny\",\n"
            "    \"Action\": \"s3:PutObject\",\n"
            "    \"Resource\": \"*\",\n"
            "    \"Condition\": { \"StringNotEquals\": { \"s3:x-amz-server-side-encryption\": \"aws:kms\" } }\n"
            "  }]\n"
            "}"),
   'lang': 'sql'},
  {'title': 'Project brief', 'body':
   "Stand up the hardened landing zone for a fictional company: org CloudTrail with Object Lock, Config aggregation, Security Hub, "
   "the preventive SCP set (deny unencrypted S3, deny unapproved regions) plus detective Config rules, account-level S3 Block Public "
   "Access, KMS envelope encryption on data stores, and the incident-response runbook (isolate → eradicate → recover) with one "
   "Detective-to-Athena investigation documented. Deliverables: the guardrail inventory (preventive vs detective), the IAM design "
   "(boundaries, one ABAC policy, cross-account pattern), and the investigation write-up. Graded on 'secure by default, compliant by "
   "construction' — every control must show its enforcement, not just its existence."},
  {'title': 'Honesty note', 'body': HON},
 ],
 'cards_add': [
  {'front': 'SCPs vs permission boundaries?', 'back': 'Both bound, never grant. SCPs: org-level, even root. Boundaries: cap what a delegated admin can grant.'},
  {'front': 'WAF rate-based rule vs Shield?', 'back': 'Rate rules: L7 request floods (brute-force/scraping). Shield: DDoS. Different layers.'},
  {'front': 'Detective + GuardDuty workflow?', 'back': 'GuardDuty finds; Detective graphs the pivot to root cause; Athena gives the full timeline.'},
  {'front': 'Landing zone in one line?', 'back': 'Control Tower: account factory + preventive (SCP) and detective (Config/Hub) guardrails.'},
 ],
}

# ---------------------------------------------------------------- Module 9
U['il05-azure-admin'] = {
 'summary': ("Welcome to Module 9 of IL-05 — Cloud DevSecOps Platform SRE. I'm your instructor, and we cross to the Azure "
  "spine, starting with administration: the AZ-104. We'll run Entra ID and RBAC — users, groups, devices, licenses, roles, scopes, "
  "least privilege, and PIM for just-in-time elevation; govern with management groups, Azure Policy, locks, and tagging; operate "
  "storage accounts with tiers, redundancy, and lifecycle management; run compute from VMs and VMSS to containers; build virtual "
  "networks with NSGs, peering, and Private Endpoints; and close with monitoring, backup, and recovery. Identity is the control plane "
  "and the exam's heaviest domain — we lab every objective on a real subscription."),
 'notes': [
  {'title': 'Concepts', 'body':
   "The AZ-104 glossary — identity first, then the platform.\n"
   "- **Entra ID** — the identity plane: users, groups (security vs Microsoft 365), devices (join/register), licenses.\n"
   "- **RBAC** — role-based access: Owner/Contributor/Reader plus granular roles; who can do what.\n"
   "- **RBAC scope** — management group → subscription → resource group → resource; assignments inherit downward.\n"
   "- **least privilege** — the standing rule for every assignment.\n"
   "- **PIM (Privileged Identity Management)** — just-in-time elevation: eligible assignments with approval, time-bound. Standing admin is the vulnerability.\n"
   "- **management group** — the hierarchy above subscriptions; assign policy and RBAC once, inherit everywhere.\n"
   "- **Azure Policy** — compliance as code: deny, audit, deployIfNotExists effects; governs what configurations are allowed.\n"
   "- **resource lock** — CanNotDelete / ReadOnly; CanNotDelete on production resource groups is the cheapest outage insurance.\n"
   "- **storage tiers** — Hot / Cool / Cold / Archive; cost follows access recency.\n"
   "- **redundancy ladder** — LRS (3 copies, 1 datacenter) → ZRS (3 zones) → GRS (+ paired region) → RA-GRS; durability and cost rise together.\n"
   "- **lifecycle management** — rules that tier aging blobs down automatically; storage cost is a policy, not a hope.\n"
   "- **SAS vs keys** — shared access signatures (scoped, expiring) versus storage account keys.\n"
   "- **availability set vs zone** — sets survive rack loss; zones survive datacenter loss. Zones are the resilience default.\n"
   "- **VMSS** — virtual machine scale sets: autoscaling VM fleets.\n"
   "- **NSG** — network security group: lowest rule number wins; defaults deny inbound internet.\n"
   "- **peering** — VNet peering; transit goes via the hub.\n"
   "- **Private Endpoint** — PaaS services (Storage, SQL) get VNet-private IPs; off the public internet.\n"
   "- **Load Balancer** — L4 regional distribution.\n"
   "- **Application Gateway** — L7 with WAF and path/host routing.\n"
   "- **Azure Monitor / Log Analytics** — metrics and logs; KQL queries over the workspace.\n"
   "- **Recovery Services vault** — Azure Backup policies and Site Recovery for DR."},
  {'title': 'Hands-on procedure', 'body':
   "Administer a real subscription, identity first.\n"
   "1. **Kill standing admin.** Move the admin accounts to PIM-eligible assignments with approval and time bounds; verify an elevation request and its audit trail.\n"
   "2. **RBAC by scope.** Create a custom role with least privilege, assign it at the resource-group scope, and confirm inheritance blocks at the subscription level.\n"
   "3. **Govern once.** Build the management-group hierarchy, assign an Azure Policy initiative (e.g. deny public storage) at the top, and confirm a violating deployment is denied.\n"
   "4. **Lock production.** Apply CanNotDelete locks to the production resource groups; attempt a delete and watch it fail safely.\n"
   "5. **Tier the storage.** Create a storage account, write a lifecycle rule (Hot → Cool → Archive by age), and compare the redundancy options on the durability/cost ladder.\n"
   "6. **Zone the compute.** Deploy across availability zones (not sets); put a VMSS behind the load balancer with autoscale.\n"
   "7. **Private the PaaS.** Add a Private Endpoint to the storage account; verify traffic no longer needs the public endpoint.\n"
   "8. **Query.** Learn five KQL queries against Log Analytics (CPU spikes, failed sign-ins, and three of your choosing) and save them; set one alert with an action group.",
   'code': ("# KQL: CPU spikes over 5-minute windows\n"
            "AzureMetrics\n"
            "| where MetricName has 'Percentage CPU'\n"
            "| summarize avg(Average) by bin(TimeGenerated, 5m), Resource\n"
            "| where avg_Average > 80\n"
            "\n"
            "# KQL: failed sign-ins (identity is the control plane — watch it)\n"
            "SigninLogs\n"
            "| where ResultType != 0\n"
            "| summarize count() by UserPrincipalName, bin(TimeGenerated, 1h)\n"
            "| order by count_ desc"),
   'lang': 'kql'},
  {'title': 'Project brief', 'body':
   "Run a production-grade Azure subscription for a fictional team: Entra ID with PIM (no standing admin), RBAC custom roles at "
   "proper scopes, the management-group hierarchy with a policy initiative and production locks, zoned compute behind load balancing, "
   "lifecycle-managed storage, Private Endpoints on PaaS, and the five saved KQL queries with one alerting action group. Deliverables: "
   "the governance diagram (hierarchy → policy → locks), the identity design (PIM workflow documented), and the ops handover sheet. "
   "The AZ-104 grades administrators — this brief is the admin's portfolio."},
  {'title': 'Honesty note', 'body': HON},
 ],
 'cards_add': [
  {'front': 'Groups: security vs Microsoft 365?', 'back': 'Security groups: access control. M365 groups: collaboration (Teams/SharePoint) plus optional access.'},
  {'front': 'Policy effects?', 'back': 'Deny, audit, deployIfNotExists (and append/modify) — compliance as code at assignment scope.'},
  {'front': 'ZRS vs GRS choice?', 'back': 'ZRS: regional resilience, 3 zones. GRS: + paired-region copy for regional disaster. Cost vs blast radius.'},
  {'front': 'Cheapest outage insurance?', 'back': 'CanNotDelete locks on production resource groups.'},
 ],
}

# ---------------------------------------------------------------- Module 10
U['il05-azure-architect'] = {
 'summary': ("Welcome to Module 10 of IL-05 — Cloud DevSecOps Platform SRE. I'm your instructor, and we shift from administering "
  "Azure to designing it: the AZ-305. We'll design identity, governance, and monitoring for a multi-subscription enterprise; choose "
  "data services by workload pattern — Azure SQL, Cosmos DB with its five consistency levels, Storage, and the analytics tier; design "
  "business continuity where RTO/RPO choose between backup and Site Recovery; and design infrastructure across compute, network, and "
  "migrations. It all caps in the architecture capstone: a full design with documented trade-offs, graded on rationale — two good "
  "architects can disagree, but both must defend."),
 'notes': [
  {'title': 'Concepts', 'body':
   "The architect's design vocabulary.\n"
   "- **landing zone** — the enterprise scaffold: platform subscriptions plus workload subscriptions under management groups, governed centrally.\n"
   "- **hybrid identity** — Entra Connect sync versus federation; B2B/B2C for external identity shapes.\n"
   "- **Access Reviews** — recurring, auditable certification of access; governance that doesn't rot.\n"
   "- **policy initiative** — bundled policies assigned at the management group for org-wide compliance.\n"
   "- **Log Analytics workspace strategy** — central versus regional workspaces; alert routing and workbooks for the business view.\n"
   "- **Azure SQL** — the relational, familiar choice.\n"
   "- **Cosmos DB** — global NoSQL with five consistency levels: Strong → Bounded Staleness → Session → Consistent Prefix → Eventual; latency and availability trade per level.\n"
   "- **hot/warm/cold path** — stream (Event Hubs) → serve (Cosmos DB) → analyze (Synapse): the lambda/kappa shapes.\n"
   "- **backup vs Site Recovery** — backup: RPO-hours, cheap. Site Recovery: replication with failover runbooks, RPO-minutes, for tier-1 workloads. The numbers choose.\n"
   "- **compute selection** — App Service vs AKS vs VMs vs Functions, chosen by workload shape.\n"
   "- **hub-spoke** — shared services in the hub (firewall, DNS, VPN), workloads in spokes; peering is non-transitive by default, so spoke-to-spoke routes via the hub.\n"
   "- **ExpressRoute vs VPN** — dedicated private circuit versus internet VPN; the SLA and consistency need decides.\n"
   "- **Azure Migrate** — assess → replicate → test cutover → cutover; migrations run in waves, never big-bang.\n"
   "- **design grading criterion** — rationale fit to constraints; defend the trade-offs, not just the choices."},
  {'title': 'Hands-on procedure', 'body':
   "Design in the order the exam asks: identity, data, continuity, infrastructure — then defend it.\n"
   "1. **Identity design.** Sketch the tenant shape (single vs B2B/B2C), hybrid approach (sync vs federation), and the PIM + Access Reviews governance loop.\n"
   "2. **Governance design.** Draw the management-group hierarchy (platform vs workload subscriptions), the policy initiatives, and the tagging + cost-management strategy.\n"
   "3. **Data design.** For each workload, pick by pattern: relational → Azure SQL; global NoSQL with tunable consistency → Cosmos DB (choose the level deliberately); "
   "blobs/files/queues/tables → Storage by pattern; analytics → Synapse/Fabric.\n"
   "4. **Continuity design.** Write the RTO/RPO per tier; assign backup (RPO-hours) or Site Recovery (RPO-minutes) accordingly — the numbers choose the tool.\n"
   "5. **Infrastructure design.** Select compute by workload, draw hub-spoke with the firewall and gateway in the hub, and plan the migration in waves with Azure Migrate.\n"
   "6. **Monitoring design.** Choose the workspace strategy (central vs regional), alert routing, and the workbooks the business will actually read.\n"
   "7. **Trade-off log.** For every major choice, record the constraint it serves (compliance? cost? operability?) and the rejected alternative — the exam grades the fit.",
   'code': ("# Cosmos DB consistency choice (Session: the sweet spot for most global apps)\n"
            "az cosmosdb update \\\n"
            "  --name mycosmos --resource-group rg-data \\\n"
            "  --default-consistency-level Session\n"
            "\n"
            "# Hub-spoke: spoke UDR forces traffic through the hub firewall\n"
            "az network route-table route create \\\n"
            "  --resource-group rg-net --route-table-name spoke-rt \\\n"
            "  --name to-hub-firewall \\\n"
            "  --address-prefix 0.0.0.0/0 \\\n"
            "  --next-hop-type VirtualAppliance \\\n"
            "  --next-hop-ip-address 10.0.0.4"),
   'lang': 'bash'},
  {'title': 'Project brief', 'body':
   "Deliver the architecture capstone: a full design for a fictional company's Azure estate — requirements, constraints, service "
   "selections with rationale, network topology (hub-spoke with Private Endpoints), identity plan (hybrid + PIM + Access Reviews), "
   "business-continuity plan (RTO/RPO per tier), cost estimate, and the trade-off log. Deliverables: the design document, the "
   "topology diagram, and the constraint log where every choice cites compliance, cost, or operability. This is the AZ-305 in "
   "miniature: graded on rationale, where two good architects can disagree but both must defend."},
  {'title': 'Honesty note', 'body': HON},
 ],
 'cards_add': [
  {'front': 'Session consistency: why the sweet spot?', 'back': 'Read-your-writes within a session with global low latency — Strong costs latency, Eventual costs correctness.'},
  {'front': 'Landing zone subscriptions?', 'back': 'Platform (identity, connectivity, management) + workload subscriptions, all under management groups.'},
  {'front': 'Migrate: assess with what?', 'back': 'Azure Migrate appliance: discover, assess readiness/cost, then replicate in waves.'},
  {'front': 'Workbooks for?', 'back': 'The business view of monitoring — curated dashboards over the Log Analytics data.'},
 ],
}

SECTIONS = {
 'il05-aws-cloudops': ['Hands-on procedure', 'Concepts', 'Concepts', 'Concepts', 'Concepts', 'Concepts'],
 'il05-aws-devops': ['Concepts', 'Concepts', 'Concepts', 'Concepts', 'Concepts', 'Concepts'],
 'il05-aws-security': ['Concepts', 'Concepts', 'Hands-on procedure', 'Concepts', 'Concepts', 'Concepts'],
 'il05-azure-admin': ['Concepts', 'Concepts', 'Concepts', 'Concepts', 'Concepts', 'Hands-on procedure'],
 'il05-azure-architect': ['Concepts', 'Hands-on procedure', 'Concepts', 'Concepts', 'Hands-on procedure', 'Concepts'],
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
    print('r2 applied OK:', list(U.keys()))

if __name__ == '__main__':
    main()

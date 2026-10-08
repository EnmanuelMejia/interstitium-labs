#!/usr/bin/env python3
"""Build IL28-M42 module object -> part_f_m42.json"""
import json

notes = [
{"title": "VPC: Your Private Network in AWS",
"body": "A Virtual Private Cloud (VPC) is an isolated software-defined network you own inside AWS, defined by a CIDR block such as 10.0.0.0/16. Inside it you carve subnets: public subnets whose route table sends 0.0.0.0/0 to an Internet Gateway, and private subnets whose default route points at a NAT Gateway so instances can reach out (for patches, package downloads) without being reachable inbound. Route tables are the actual routing decisions — a subnet is 'public' only because its route table says so. Security groups are stateful instance-level firewalls (return traffic is automatically allowed); network ACLs are stateless subnet-level filters (you must allow return traffic explicitly). Worked example: an EC2 instance in a private subnet cannot curl https://example.com. Diagnose: (1) route table for the subnet — does 0.0.0.0/0 point to a NAT Gateway in a public subnet? (2) the NAT Gateway itself — is it in a public subnet with an Elastic IP, and is it 'available'? (3) the security group — does it allow outbound HTTPS (default allows all outbound, but a hardened SG may not)? (4) the NACL — stateless, so ephemeral return ports 1024-65535 must be allowed inbound. Solution in most real cases: the NAT Gateway was placed in the private subnet, or the route table points at a deleted NAT Gateway. Fix the route, not the instance."},
{"title": "EC2: Instances, Lifecycle, and Pricing Models",
"body": "EC2 provides virtual machines with a lifecycle every operator must know cold: pending -> running -> (reboot keeps the instance; stop/start moves it to new hardware and changes a non-EIP public IP) -> stopped -> terminated. Key instance facts: the AMI defines the OS and preinstalled software; the instance type (e.g. m6i.large) defines vCPU/RAM/network; EBS volumes persist independently of the instance; instance store volumes are ephemeral and vanish on stop. Pricing models map to workload shapes: On-Demand for unpredictable short work, Reserved/Savings Plans for steady 1-3 year baselines, and Spot for fault-tolerant batch at deep discounts with 2-minute interruption warnings. Worked example: a nightly ETL job runs 2 hours on 8 vCPUs and tolerates restarts. Solution: run it on Spot — checkpoint progress to S3 every 15 minutes, handle the interruption notice, and the job costs a fraction of On-Demand. Counter-example: the primary database goes on On-Demand or Reserved, never Spot — an interruption there is an outage, not a retry. The exam-style trap: 'stopped' instances still incur EBS charges; only 'terminated' stops the meter for the instance itself. Always verify state with aws ec2 describe-instances --query 'Reservations[].Instances[].[InstanceId,State.Name]'."},
{"title": "S3: Object Storage, Storage Classes, and Consistency",
"body": "S3 stores objects in buckets: flat key/value storage with 11-nines durability design, unlimited scale, and strong read-after-write consistency for all operations. Buckets are global-named but region-resident — pick the region near your compute to avoid cross-region latency and transfer costs. Storage classes trade retrieval cost for storage cost: Standard for hot data, Intelligent-Tiering for unknown patterns, Standard-IA/One Zone-IA for infrequent access, Glacier Instant/Flexible/Deep Archive for backups with minutes-to-hours retrieval. Lifecycle policies automate transitions (e.g. logs -> Standard-IA after 30 days -> Glacier after 90 -> expire after 365). Versioning keeps every overwrite as a new version — your cheapest accidental-deletion insurance. Worked example: application logs, 500 GB/month, rarely read after 7 days, must be retained 1 year for audit. Solution: bucket with lifecycle rule — transition to Standard-IA at 30 days, to Glacier Flexible at 90 days, expire at 365; enable versioning plus MFA delete on the audit prefix. The classic cost mistake is leaving everything in Standard forever; the classic availability mistake is assuming cross-region replication is on by default — it is not, enable CRR explicitly for DR."},
{"title": "IAM: Users, Roles, Policies, and Least Privilege",
"body": "IAM is AWS's identity system and the foundation of least privilege: no identity gets permissions it does not need, and permissions shrink over time. Users are long-lived identities (humans, or legacy service accounts); roles are assumed temporarily via STS and are what EC2 instances, Lambda functions, and EKS pods should use — never embed access keys on an instance when an instance profile (role) does the job. Policies are JSON documents with Allow/Deny statements; an explicit Deny always wins. The policy evaluation order to recite in interviews: explicit Deny > explicit Allow > default implicit Deny. Attach policies to groups and roles, not individual users. Worked example: a CI job needs to push images to ECR and nothing else. Bad solution: an IAM user with AdministratorAccess and keys in the pipeline. Correct solution: an IAM role with a policy allowing only ecr:GetAuthorizationToken, ecr:BatchCheckLayerAvailability, ecr:PutImage, and related push actions on the specific repository ARN, assumed by the CI runner via OIDC federation — no long-lived keys at all. Verify effective permissions before deploying with aws iam simulate-principal-policy --policy-source-arn <role-arn> --action-names ecr:PutImage --resource-arns <repo-arn>. Rotate any remaining access keys on a schedule and delete unused ones; keys older than 90 days are an audit finding."},
{"title": "EKS and the Kubernetes-on-AWS Map",
"body": "EKS is AWS's managed Kubernetes: AWS runs the control plane (API server, etcd) across multiple AZs while you own the worker nodes (managed node groups, Fargate profiles, or self-managed). The concepts from AKS transfer directly: node groups are the EKS analogue of node pools, the cluster autoscaler works the same way, and IAM Roles for Service Accounts (IRSA) map Kubernetes service accounts to IAM roles — the AWS-native answer to workload identity. Networking: pods run in your VPC (VPC CNI assigns VPC IPs, so subnet sizing matters exactly as with Azure CNI), and exposure uses either an Application/Network Load Balancer via the AWS Load Balancer Controller or an Ingress resource. Worked example: a pod needs to read from S3. Anti-pattern: baking AWS keys into the container image. Solution: create an IAM role with s3:GetObject on the bucket, annotate the Kubernetes service account with eks.amazonaws.com/role-arn, and the pod's AWS SDK calls assume the role automatically via the projected OIDC token — no secrets to rotate. EKS vs AKS vs GKE in one line each: EKS leans on IAM/IRSA and VPC CNI; AKS leans on Azure AD workload identity and Azure CNI; GKE leans on Workload Identity and alias IPs. The control plane is managed in all three; your job is nodes, networking, and identity in all three."},
{"title": "ALB vs NLB: The L4/L7 Lesson, AWS Edition",
"body": "This is the AWS retelling of the App Gateway vs Load Balancer distinction, and panels love the mapping. The Network Load Balancer (NLB) operates at Layer 4: it forwards TCP/UDP (and TLS passthrough) with ultra-low latency and static IPs, preserving the client source IP — the right choice for gaming, VoIP, or any non-HTTP protocol. The Application Load Balancer (ALB) operates at Layer 7: it understands HTTP/HTTPS, routes by host header and path, terminates TLS, and integrates with WAF — the right choice for web APIs and microservices, and the natural target of a Kubernetes Ingress via the AWS Load Balancer Controller. Worked example: expose payments.example.com/api to the payments service and payments.example.com/ to the storefront, both TLS-terminated with WAF. Solution: one ALB with two listener rules — host+path condition /api/* -> payments target group, default -> storefront target group, ACM certificate on the HTTPS listener, WAF ACL associated. The trap: choosing NLB for HTTP routing because 'it is faster' — you then reimplement path routing in every service. And the cost trap: an ALB per microservice instead of one ALB with path rules multiplies the hourly charge by the service count. One ALB, many rules; NLB only when the protocol is not HTTP."},
]

cards = [
{"front": "What makes a subnet 'public' in AWS?", "back": "Its route table sends 0.0.0.0/0 to an Internet Gateway — the label is a consequence of routing, not a property of the subnet"},
{"front": "Security group vs network ACL (stateful vs stateless)", "back": "Security groups are stateful (return traffic auto-allowed) at the instance/ENI level; NACLs are stateless at the subnet level — you must explicitly allow return ephemeral ports"},
{"front": "EC2 stop vs terminate (billing + behavior)", "back": "Stop: instance halts, EBS persists and still bills, public IP may change on start. Terminate: instance deleted; EBS bills until volumes are deleted too"},
{"front": "AWS CLI: list instance IDs and states", "back": "aws ec2 describe-instances --query 'Reservations[].Instances[].[InstanceId,State.Name]' --output table"},
{"front": "S3 storage class for logs rarely read after a week, kept 1 year", "back": "Lifecycle policy: Standard -> Standard-IA (30d) -> Glacier Flexible (90d) -> expire (365d); enable versioning for the audit prefix"},
{"front": "IAM policy evaluation order", "back": "Explicit Deny beats explicit Allow beats implicit (default) Deny"},
{"front": "How should an EC2 instance or pod get AWS permissions? (no keys)", "back": "Assume an IAM role: instance profile for EC2, IRSA (IAM Roles for Service Accounts) for EKS pods via OIDC"},
{"front": "AWS CLI: test whether a role can push to ECR before deploying", "back": "aws iam simulate-principal-policy --policy-source-arn <role> --action-names ecr:PutImage --resource-arns <repo>"},
{"front": "EKS analogue of an AKS node pool", "back": "Managed node group (plus Fargate profiles); cluster autoscaler and IRSA map 1:1 from AKS concepts"},
{"front": "ALB vs NLB in one line each", "back": "ALB = Layer 7: HTTP host/path routing, TLS termination, WAF. NLB = Layer 4: TCP/UDP, ultra-low latency, static IP, preserves source IP"},
{"front": "Why not one ALB per microservice?", "back": "Each ALB bills hourly — use one ALB with host/path listener rules fanning out to many target groups"},
{"front": "VPC CNI IP planning gotcha (mirrors Azure CNI)", "back": "Pods consume real VPC IPs, so subnets must be sized for max pods; exhaustion blocks scheduling and node joins"},
]

quiz = [
{"q": "An EC2 instance in a private subnet cannot reach the internet. The NAT Gateway exists and is 'available'. What do you check FIRST?",
"choices": ["The instance's CPU credits", "The subnet's route table: does 0.0.0.0/0 point to that NAT Gateway?", "The S3 bucket policy", "The IAM user's MFA status"],
"answer": 1,
"explain": "Outbound routing is decided by the route table. A NAT Gateway in the wrong subnet or a route pointing at a deleted gateway are the classic causes; CPU credits are irrelevant to networking."},
{"q": "A security group allows inbound 443 but the app still fails. The NACL is custom. What is the likely NACL mistake?",
"choices": ["NACLs cannot filter 443", "The stateless NACL does not allow the ephemeral return ports (1024-65535) inbound", "Security groups override NACLs", "NACLs only apply to public subnets"],
"answer": 1,
"explain": "NACLs are stateless: the HTTPS response returns on ephemeral ports, which must be explicitly allowed inbound. Security groups are stateful and handle this automatically."},
{"q": "Which EC2 pricing model fits a fault-tolerant 2-hour nightly ETL that checkpoints to S3?",
"choices": ["On-Demand", "Dedicated Hosts", "Spot", "Reserved for 3 years with no checkpointing"],
"answer": 2,
"explain": "Spot gives deep discounts for interruptible work; checkpointing to S3 makes the 2-minute interruption warning survivable. Databases and steady baselines do not belong on Spot."},
{"q": "A stopped EC2 instance is still generating charges. Why?",
"choices": ["AWS bills stopped instances at full price", "Attached EBS volumes keep billing until deleted", "The Elastic IP is free", "Stopped instances consume vCPU quota"],
"answer": 1,
"explain": "Stopping halts the instance meter, but EBS volumes persist and bill independently. Only deleting the volumes (or terminating with delete-on-termination) stops storage charges."},
{"q": "500 GB/month of logs, rarely read after 7 days, 1-year retention required. Best S3 design?",
"choices": ["Standard with no lifecycle rules", "Lifecycle: Standard-IA at 30 days, Glacier Flexible at 90 days, expire at 365 days, versioning on", "One Zone-IA for everything with no expiry", "Store logs in EBS instead"],
"answer": 1,
"explain": "Lifecycle transitions match cost to access pattern; expiry enforces retention; versioning protects the audit trail. Standard forever is the classic cost mistake."},
{"q": "A CI pipeline needs to push images to one ECR repo. Most secure design?",
"choices": ["IAM user with AdministratorAccess, keys in pipeline variables", "IAM role assumable via OIDC with a policy allowing only ECR push actions on that repo ARN", "Root access keys rotated yearly", "Public ECR repo with no auth"],
"answer": 1,
"explain": "OIDC-assumed roles eliminate long-lived keys entirely, and scoping to push-only actions on one ARN is least privilege. Admin keys in CI are a breach waiting to happen."},
{"q": "In IAM, a policy Allows s3:* and another attached policy Denies s3:DeleteBucket. Can the identity delete the bucket?",
"choices": ["Yes, Allow wins", "No, explicit Deny always wins", "Only on weekends", "Yes, the most recent policy wins"],
"answer": 1,
"explain": "Explicit Deny overrides any Allow. Evaluation order: explicit Deny > explicit Allow > implicit Deny."},
{"q": "An EKS pod needs read access to one S3 bucket. Correct approach?",
"choices": ["Bake AWS access keys into the container image", "IRSA: IAM role with s3:GetObject on the bucket, mapped to the pod's service account via OIDC annotation", "Open the bucket to the public", "SSH into the node and configure the AWS CLI"],
"answer": 1,
"explain": "IRSA gives the pod short-lived credentials for exactly one role with no keys to rotate or leak. Keys in images end up in registries and git history."},
{"q": "You need host/path routing with TLS termination and WAF for HTTP microservices on AWS. Which load balancer?",
"choices": ["Network Load Balancer", "Application Load Balancer", "Gateway Load Balancer", "Classic Load Balancer"],
"answer": 1,
"explain": "ALB is Layer 7: host/path rules, TLS termination, WAF integration. NLB is Layer 4 for TCP/UDP; it cannot do HTTP routing."},
]

drills = [
{"id": "il28-m42-vpc-triage", "title": "Timed drill: VPC and EC2 triage",
"items": [
{"prompt": "60 seconds: private-subnet instance cannot reach the internet. Your 4 checks in order?", "answer": "Route table 0.0.0.0/0 -> NAT GW; NAT GW in public subnet + available; security group outbound; NACL ephemeral return ports.",
"explain": "Routing first, then the gateway's own placement, then stateful SG, then stateless NACL. Say it in this order."},
{"prompt": "What single route-table fact makes a subnet public?", "answer": "A route sending 0.0.0.0/0 to an Internet Gateway.",
"explain": "'Public' is a routing property, not a subnet property — the panel wants this exact framing."},
{"prompt": "Stateful vs stateless: which is the security group, which the NACL?", "answer": "Security group = stateful (return auto-allowed). NACL = stateless (explicit both directions).",
"explain": "This distinction explains every 'SG allows it but traffic still fails' mystery."},
{"prompt": "Command: list all EC2 instance IDs with their states in a table.", "answer": "aws ec2 describe-instances --query 'Reservations[].Instances[].[InstanceId,State.Name]' --output table",
"explain": "JMESPath query keeps it to the two fields you need during triage."},
{"prompt": "Stop vs terminate: what keeps billing after each?", "answer": "Stop: EBS volumes keep billing. Terminate: nothing, once volumes are deleted.",
"explain": "The instance meter stops on stop; the storage meter does not."},
{"prompt": "Spot vs On-Demand: which for the primary database, and why?", "answer": "On-Demand (or Reserved). Spot interruptions are fine for checkpointed batch, never for a database.",
"explain": "Match pricing to interruptibility — say the 2-minute warning and who can tolerate it."},
{"prompt": "S3: name the storage classes for hot, unknown-pattern, and archival data.", "answer": "Hot: Standard. Unknown: Intelligent-Tiering. Archive: Glacier Flexible/Deep Archive.",
"explain": "Three buckets of the lifecycle: hot, unknown, cold — with lifecycle policies automating the transitions."},
]},
{"id": "il28-m42-iam-least-privilege", "title": "Timed drill: IAM and least privilege",
"items": [
{"prompt": "Recite the IAM policy evaluation order.", "answer": "Explicit Deny > explicit Allow > implicit (default) Deny.",
"explain": "One line, no hesitation — panels use it as a warm-up check."},
{"prompt": "EC2 instance needs S3 read. Keys on the instance or instance profile?", "answer": "Instance profile (IAM role). Never long-lived keys on compute.",
"explain": "Roles give short-lived credentials automatically; keys get leaked, forgotten, and never rotated."},
{"prompt": "Command: simulate whether a role can ecr:PutImage on a repo.", "answer": "aws iam simulate-principal-policy --policy-source-arn <role-arn> --action-names ecr:PutImage --resource-arns <repo-arn>",
"explain": "Simulate before deploying — it evaluates the real policy set without making the call."},
{"prompt": "EKS pod needs S3 access. Name the mechanism and the annotation.", "answer": "IRSA — annotate the ServiceAccount with eks.amazonaws.com/role-arn.",
"explain": "IAM Roles for Service Accounts: OIDC-projected token, role assumption, no secrets."},
{"prompt": "CI pushes to one ECR repo. Scope the policy.", "answer": "Allow only ECR push actions (GetAuthorizationToken, BatchCheckLayerAvailability, PutImage, Initiate/UploadPart/CompleteLayerUpload) on that repo ARN.",
"explain": "Name the actions and the ARN scope — 'ECR full access' fails the least-privilege question."},
{"prompt": "ALB vs NLB: which terminates TLS and does path routing?", "answer": "ALB (Layer 7). NLB is Layer 4 TCP/UDP passthrough.",
"explain": "Map to Azure: ALB ~ Application Gateway, NLB ~ Azure Load Balancer."},
{"prompt": "Cost trap: one ALB per microservice. Fix?", "answer": "One ALB with host/path listener rules to many target groups.",
"explain": "ALBs bill hourly each — fan out with rules, not with load balancers."},
]},
]

handsOnLab = {
"id": "il28-m42-lab",
"title": "Lab: VPC, least-privilege IAM, and EKS with IRSA",
"brief": "You will build a two-tier VPC, launch an EC2 instance in the private tier, create a least-privilege IAM role, stand up a small EKS cluster, and give a pod S3 access through IRSA with no long-lived keys. Tear everything down at the end; expect a few dollars of charges if completed same-day.",
"steps": [
"Create the VPC and tiers: aws ec2 create-vpc --cidr-block 10.1.0.0/16; create public subnet 10.1.1.0/24 and private subnet 10.1.2.0/24 in the same AZ; create and attach an Internet Gateway; add 0.0.0.0/0 -> IGW on the public route table.",
"Create a NAT Gateway with an Elastic IP in the public subnet; add 0.0.0.0/0 -> NAT Gateway on the private route table. Verify with aws ec2 describe-route-tables.",
"Launch an Amazon Linux EC2 instance in the private subnet with no public IP and an instance profile role allowing only s3:GetObject on one bucket; SSH via Session Manager and curl https://example.com to prove NAT egress works.",
"Create an S3 bucket with versioning enabled; write a lifecycle rule (console or CLI) moving objects to Standard-IA after 30 days; upload a test object and confirm aws s3 ls shows it.",
"Draft the CI deployer policy: JSON allowing only ECR push actions on one repository ARN; run aws iam simulate-principal-policy against it for ecr:PutImage (expect allowed) and iam:* (expect denied).",
"Create the EKS cluster: eksctl create cluster --name il28-m42 --region us-east-1 --nodegroup-name workers --node-type t3.medium --nodes 2 --nodes-min 1 --nodes-max 4 (or the equivalent aws eks create-cluster + nodegroup commands).",
"Create an IAM role for IRSA with s3:GetObject on your bucket; associate the OIDC provider; annotate a Kubernetes ServiceAccount with eks.amazonaws.com/role-arn.",
"Deploy a test pod using that ServiceAccount that runs aws s3 ls s3://<bucket>; confirm it lists objects with no keys present in the pod (env | grep AWS shows nothing).",
"Expose the pod via an Ingress and the AWS Load Balancer Controller: confirm an ALB is provisioned and routes by path to your service.",
"Document the ALB-vs-NLB decision for three workloads (public REST API, game voice chat UDP, internal TCP service) in your lab notes.",
"Delete in order: eksctl delete cluster, NAT Gateway + Elastic IP release, EC2 termination, VPC deletion; verify with aws ec2 describe-vpcs that nothing remains.",
"Write the one-page incident note: 'private instance lost internet' with the 4-check triage from the drill."],
"deliverable": "A (then deleted) VPC with public/private tiers, a least-privilege IAM role validated by simulation, an EKS cluster where a pod reads S3 via IRSA with zero keys, and an ALB-vs-NLB decision note.",
"checkpoint": "curl from the private instance succeeds; the pod lists S3 objects with no AWS keys in its env; aws ec2 describe-vpcs shows the lab VPC gone after teardown."
}

mockTask = {"id": "il28-m42-mock", "type": "choice",
"q": "Your EKS pods need to read objects from one S3 bucket. A teammate proposes baking an IAM user's access keys into the container image 'because it is simple'. What do you do?",
"choices": ["Approve it — simplicity wins", "Use IRSA: an IAM role scoped to s3:GetObject on that bucket, mapped to the pod's ServiceAccount via OIDC", "Make the bucket public and skip IAM", "Put the keys in a ConfigMap instead"],
"answer": 1,
"explain": "IRSA issues short-lived credentials scoped to one role with no keys to rotate, leak, or commit. Keys in images end up in registries and layer history; ConfigMaps are not secret storage; public buckets are a breach."}

module = {
"id": "IL28-M42", "code": "IL-28",
"title": "AWS Core: VPC, EC2, S3, IAM & EKS",
"summary": "Build AWS fundamentals end to end — VPC networking and triage, EC2 lifecycle and pricing, S3 storage classes, IAM least privilege with real CLI verification, EKS with IRSA, and the ALB-vs-NLB L4/L7 mapping.",
"objectives": [
"Design a two-tier VPC and triage loss of internet egress using route tables, NAT, security groups, and NACLs",
"Choose EC2 pricing models and lifecycle actions correctly and predict their billing effects",
"Apply S3 storage classes and lifecycle policies to match cost with access patterns",
"Implement least privilege with IAM roles, policy simulation, and zero long-lived keys",
"Run workloads on EKS with IRSA and choose ALB vs NLB by protocol layer"],
"notes": notes, "cards": cards, "quiz": quiz, "weight": 2,
"prerequisiteFor": ["IL28-M44"],
"drills": drills, "handsOnLab": handsOnLab, "mockTask": mockTask,
"crossLinks": ["IL28-M44", "IL28-M41"],
"videos": [{"title": "AWS Certified Solutions Architect - Associate 2020 (PASS THE EXAM!)", "url": "https://www.youtube.com/watch?v=Ia-UEYYR44s", "source": "YouTube - freeCodeCamp.org", "durationMin": 600, "order": 1, "watchBefore": "notes", "blurb": "Full AWS foundations course; focus on VPC, EC2, S3, and IAM sections as the base for this module's hands-on work."}],
"estimatedMinutes": 750,
}

with open("/home/hatch/workspace/apex-audit/docs/university/data/courses/_il28-build/part_f_m42.json", "w") as f:
    json.dump(module, f, indent=2, ensure_ascii=False)
print("M42 written")

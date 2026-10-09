#!/usr/bin/env python3
"""Group D v4 builder: IL-19, IL-20, IL-21, IL-22, IL-23, IL-24, IL-25.
Preserves ALL existing content; adds missing v4 top-level + module fields.
"""
import json, copy, os, math

BASE = os.path.expanduser('~/workspace/apex-audit/docs/university/data/courses')
UPDATED = "2026-10-09"
TIME_FORMULA = ("estimatedMinutes per module = instruction + videos + drills + hands-on lab, "
                "set per module by the author; course total = sum of module estimates. "
                "Declared hours are the honest rounded sum.")
INDEP_FRAMING = ("Independent practice and preparation. Not affiliated with, endorsed by, "
                 "or sponsored by any vendor or employer; confers no certificate.")


def study_guide(code, title_weeks, modules, phases):
    total_min = sum(m.get('estimatedMinutes', 0) for m in modules)
    return {
        "title": f"Study guide: how to work {code} in {title_weeks}",
        "totalHours": round(total_min / 60),
        "totalMinutes": total_min,
        "note": ("totalHours/totalMinutes are computed from the sum of module estimatedMinutes; "
                 "declared hours are the honest rounded sum."),
        "pacing": phases,
        "rules": [
            "Do the modules in order — each module's objectives feed the next.",
            "Complete every hands-on lab; reading without doing does not count.",
            "Quiz mastery gate: 70% or higher to mark a module mastered.",
            "Use the flashcards daily; spaced recall beats re-reading.",
        ],
    }


def interactivity_audit(d):
    mods = d.get('modules', [])
    counts = {
        "terminalSims": len(d.get('terminalSims', [])),
        "branchingScenarios": len(d.get('branchingScenarios', [])),
        "clickSims": len(d.get('clickSims', [])),
        "toolLabs": len(d.get('toolLabs', [])),
        "installLabs": len(d.get('installLabs', [])),
        "multicloudLabs": len(d.get('multicloudLabs', [])),
        "trainers": len(d.get('trainers', [])),
        "scriptLabs": len(d.get('scriptLabs', [])),
        "cheatSheets": len(d.get('cheatSheets', [])),
    }
    counts["totalInteractive"] = sum(v for k, v in counts.items() if k != "cheatSheets")
    counts["rule"] = ("Every module ships notes, flashcards, quiz, drills, a hands-on lab, and a mock task; "
                      "interactivity is counted, not claimed.")
    return counts


def readiness_dashboard(code, gate_ids):
    return {
        "title": f"{code} Readiness Dashboard",
        "framing": INDEP_FRAMING,
        "concept": ("Each module has a quiz mastery gate. You are ready for the next phase "
                    "when you clear each module's gate and complete its hands-on lab."),
        "formula": "readiness = (all module quiz gates >= 70%) AND (all hands-on labs complete)",
        "thresholds": "Quiz mastery gate: 70% per module. Readiness: 100% of modules complete.",
        "statusLabels": ["not started", "in progress", "gates clearing", "ready"],
        "rule": "Clear every module's quiz gate before moving to the capstone/final phase.",
        "order": gate_ids,
    }


def phase_row(weeks, label, mods, total_min):
    hrs = round(total_min / 60)
    ids = ", ".join(m['id'] for m in mods)
    return f"{weeks} — {label} ({ids}, ~{hrs} hrs): " + "; ".join(
        m['title'] for m in mods[:4]) + ("; ..." if len(mods) > 4 else "")


# ---------------------------------------------------------------- IL-19 sections
IL19_BS = [
    {"id": "il19-bs-cost", "title": "The surprise bill: $40,000 in us-east-1",
     "moduleId": "AWS-06",
     "start": "alert",
     "nodes": {
         "alert": {"text": "Monday 08:00. The AWS bill alert fires: this month's spend is 8x forecast. CloudWatch shows a spike in NAT gateway data processing and a fleet of unattached EBS volumes. What do you do first?",
                   "choices": [{"t": "Identify the top cost drivers with Cost Explorer before touching anything", "to": "explore"},
                               {"t": "Terminate every running instance to stop the bleeding", "to": "kill"},
                               {"t": "Open a support case and wait", "to": "wait"}]},
         "explore": {"text": "Cost Explorer shows 70% of the spike is NAT gateway data processing from one VPC, plus 200 unattached gp3 volumes. Best next move?",
                     "choices": [{"t": "Move cross-AZ traffic behind VPC endpoints and delete unattached volumes after snapshot review", "to": "fix"},
                                 {"t": "Move everything to a new region", "to": "wrong"}]},
         "fix": {"text": "Correct. VPC endpoints for S3/DynamoDB cut the NAT bill, unattached volumes are snapshotted and deleted, and you set a budget alert at 80% of forecast. The module's cost discipline, applied.", "end": True},
         "kill": {"text": "You terminated production. The bill stopped — so did the business. Cost control never means blind destruction: always identify before you act.", "end": True},
         "wait": {"text": "The meter keeps running while you wait. Cost incidents need the same triage discipline as outages: identify, contain, remediate.", "end": True},
         "wrong": {"text": "A region migration to fix a billing spike is a month of work for a problem a VPC endpoint solves in an afternoon. Match the fix to the cause.", "end": True}}},
    {"id": "il19-bs-k8s", "title": "CrashLoopBackOff at 3 AM",
     "moduleId": "DO-06",
     "start": "page",
     "nodes": {
         "page": {"text": "03:12. PagerDuty: the payments deployment is CrashLoopBackOff after a routine image update. Rollout just finished. First command?",
                  "choices": [{"t": "kubectl rollout status + kubectl get events — see what the rollout did", "to": "status"},
                              {"t": "kubectl delete pod and hope the new one is healthy", "to": "delete"},
                              {"t": "Scale the deployment to zero to stop the noise", "to": "scale"}]},
         "status": {"text": "Events show the new pods fail the readiness probe: the app binds to 127.0.0.1 instead of 0.0.0.0 in the new image. Fix?",
                     "choices": [{"t": "kubectl rollout undo deployment/payments — restore the last known-good ReplicaSet", "to": "undo"},
                                 {"t": "Edit the deployment in place to change the bind address", "to": "edit"}]},
         "undo": {"text": "Correct. Roll back first, fix the image second. The rollout undo is the practiced move; the root-cause fix ships in the next release, not at 3 AM.", "end": True},
         "delete": {"text": "The new pod crashes identically — the image is the problem, not the pod. Deleting pods treats the symptom.", "end": True},
         "scale": {"text": "You just took payments to zero yourself. The outage is now total and self-inflicted.", "end": True},
         "edit": {"text": "Editing a live deployment at 3 AM without a tested image is how 3 AM becomes 6 AM. Roll back, then fix properly.", "end": True}}},
    {"id": "il19-bs-cicd", "title": "The pipeline that shipped the bug",
     "moduleId": "DO-07",
     "start": "report",
     "nodes": {
         "report": {"text": "A customer-facing bug shipped through Jenkins yesterday. The pipeline is green. Where do you look first?",
                    "choices": [{"t": "The pipeline's test stage — what ran, what was skipped, what the gates actually check", "to": "tests"},
                                {"t": "Blame the developer who merged last", "to": "blame"},
                                {"t": "Add more stages to the pipeline", "to": "stages"}]},
         "tests": {"text": "The test stage runs unit tests only — no integration tests, no canary, and the 'smoke test' step is a commented-out shell line. The durable fix?",
                    "choices": [{"t": "Restore the smoke test, add integration tests for the changed path, and gate promotion on them", "to": "durable"},
                                {"t": "Require two approvals on every merge", "to": "approvals"}]},
         "durable": {"text": "Correct. A green pipeline that tests nothing is decoration. Gates must verify the thing you fear breaking.", "end": True},
         "blame": {"text": "The pipeline let it through — that's a system failure, not a person failure. Fix the system.", "end": True},
         "stages": {"text": "More stages that check nothing add time, not safety. One real gate beats five decorative ones.", "end": True},
         "approvals": {"text": "Approvals slow merges but don't catch what tests don't check. Humans are a poor substitute for an integration test.", "end": True}}},
]

IL19_CS = [
    {"id": "il19-cs-iam", "moduleId": "AWS-02", "tool": "AWS console — IAM",
     "title": "Attach a least-privilege policy to a deploy role",
     "steps": [
         {"screen": "IAM → Roles → the CI deploy role; the Permissions tab shows AdministratorAccess attached.",
          "action": "Select the role and open 'Add permissions → Create inline policy'."},
         {"screen": "Visual policy editor: choose the S3 service, the exact actions (PutObject, GetObject), and the single deploy bucket ARN as resource.",
          "action": "Build the statement scoped to that bucket only; no wildcards on actions or resources."},
         {"screen": "Review: the policy simulator flags no overly broad grants.",
          "action": "Create the policy, then detach AdministratorAccess from the role."},
         {"screen": "The role now shows only the scoped inline policy.",
          "action": "Run the deploy — it succeeds, and the blast radius is one bucket."}]},
    {"id": "il19-cs-terraform", "moduleId": "DO-03", "tool": "Terminal — Terraform CLI",
     "title": "Plan and apply a Terraform change safely",
     "steps": [
         {"screen": "Terminal in the infrastructure repo; main.tf defines an S3 bucket and an IAM role.",
          "action": "Run terraform fmt and terraform validate — both clean."},
         {"screen": "terraform plan shows 2 to add, 0 to change, 0 to destroy.",
          "action": "Read every line of the plan; confirm no resource will be replaced or destroyed."},
         {"screen": "Plan approved. terraform apply asks for confirmation.",
          "action": "Type yes, watch the apply complete, then verify the resources exist in the console."},
         {"screen": "State file updated; outputs show the bucket name.",
          "action": "Commit the plan output to the PR record for review traceability."}]},
    {"id": "il19-cs-k8s", "moduleId": "DO-06", "tool": "Terminal — kubectl",
     "title": "Deploy an app to Kubernetes and expose it",
     "steps": [
         {"screen": "deployment.yaml: 3 replicas of the app image, resource limits set, readiness probe defined.",
          "action": "kubectl apply -f deployment.yaml, then kubectl rollout status."},
         {"screen": "All 3 pods Running; the readiness probe gates traffic correctly.",
          "action": "kubectl apply -f service.yaml to create the ClusterIP service."},
         {"screen": "Service has endpoints; pods are registered.",
          "action": "Port-forward and curl the health endpoint — 200 OK."},
         {"screen": "The app is live inside the cluster with bounded resources.",
          "action": "Record the rollout revision for the runbook."}]},
]

IL19_TOOLLABS = [
    {"id": "il19-tool-awscli", "title": "AWS CLI sandbox drills",
     "brief": "Guided aws-cli exercises against a free-tier account: describe regions, list buckets, and query EC2 state with --query filters. Read-only commands first; nothing is created or destroyed in this lab.",
     "moduleId": "AWS-01"},
    {"id": "il19-tool-kubectl", "title": "kubectl playground",
     "brief": "Against a local kind cluster: get/describe/logs/exec across namespaces, then practice rollout undo on a deliberately broken deployment. The cluster is disposable; the muscle memory is not.",
     "moduleId": "DO-06"},
    {"id": "il19-tool-terraform", "title": "Terraform validate + plan lab",
     "brief": "Take a provided Terraform module with three planted errors. Run fmt, validate, and plan until the plan is clean and minimal. No apply — the discipline is in reading the plan.",
     "moduleId": "DO-03"},
]

IL19_MULTICLOUD = [
    {"id": "il19-mc-replicate", "title": "Cross-cloud image replication design",
     "brief": "Design (on paper, then in the consoles) a pipeline that builds one golden image and replicates it to AWS (AMI), Azure (managed image), and GCP (custom image). Compare the replication primitives each cloud offers and where the design leaks.",
     "moduleIds": ["AWS-03", "AZ-03", "GCP-04"]},
    {"id": "il19-mc-interconnect", "title": "Azure ↔ OCI interconnect lab",
     "brief": "Walk through the dedicated interconnect between Azure and OCI: what the peering gives you (low-latency private path) and what still needs VPN or ExpressRoute/FastConnect equivalents for other pairs. Diagram the traffic path for the Beacon Ridge scenario.",
     "moduleIds": ["AZ-04", "OCI-03"]},
    {"id": "il19-mc-failover", "title": "Multi-region failover tabletop",
     "brief": "Tabletop exercise: primary region fails for the Meridian Markets stack. Work the runbook — DNS failover, data replication lag math, and the RTO/RPO tradeoff — without touching production.",
     "moduleIds": ["AWS-04", "GCP-06"]},
]

IL19_INSTALL = [
    {"id": "install-aws-cli", "title": "Install the AWS CLI",
     "steps": ["Download the installer for your OS from the vendor's official install page.",
               "Verify with aws --version.", "Run aws configure with your access key (free-tier account).",
               "Set a budget alert BEFORE creating any resource."],
     "verify": "aws sts get-caller-identity returns your account."},
    {"id": "install-azure-cli", "title": "Install the Azure CLI",
     "steps": ["Install via the vendor's official package for your OS.", "Verify with az --version.",
               "Run az login and select your subscription.", "Set a spending cap alert."],
     "verify": "az account show returns your subscription."},
    {"id": "install-gcloud", "title": "Install the Google Cloud SDK",
     "steps": ["Install via the vendor's official installer.", "Verify with gcloud --version.",
               "Run gcloud init and pick your project.", "Enable billing alerts."],
     "verify": "gcloud projects list shows your project."},
    {"id": "install-terraform-kubectl", "title": "Install Terraform and kubectl",
     "steps": ["Install Terraform from the vendor's official releases.", "Install kubectl matching your cluster version.",
               "Verify both with --version.", "Point kubectl at a local kind cluster."],
     "verify": "terraform version and kubectl cluster-info both succeed."},
]
IL19_INSTALL_ORDER = ["install-aws-cli", "install-azure-cli", "install-gcloud", "install-terraform-kubectl"]

IL19_PYEX = [
    {"id": "il19-py-boto3-list", "title": "Boto3: inventory your buckets",
     "brief": "Write a Python script using boto3 that lists every S3 bucket, its region, and its versioning status. Read-only: no bucket is created or modified.",
     "moduleId": "DO-09"},
    {"id": "il19-py-boto3-ec2", "title": "Boto3: stopped-instance reporter",
     "brief": "Write a Python script that lists EC2 instances stopped for more than 7 days with their estimated monthly EBS cost — the report that feeds the cost module's cleanup runbook.",
     "moduleId": "DO-09"},
]

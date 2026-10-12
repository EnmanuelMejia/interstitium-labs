"""Batch 3: Cloud PDFs — Architecture Patterns, Kubernetes, CI/CD Pipelines."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bbg_style import *


def pdf_cloud_patterns(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Cloud Architecture\nPatterns",
               "The building blocks of reliable cloud systems:\nregions, scaling, and surviving failure.",
               "Cloud", None); pg += 1

    y = section_header(c, 1, 6, "Regions & Availability Zones",
                       "Geography is the first layer of reliability.")
    box(c, 72, 420, 468, 80, BOX_BLUE, "Region: us-east-1", "a geographic area")
    for i, bx in enumerate([90, 236, 382]):
        box(c, bx, 440, 128, 48, BOX_GREEN, f"AZ-{chr(97+i)}", "isolated datacenter")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawString(72, 380, "AZs: separate power, cooling, networking — a fire in one doesn't touch the others.")
    c.drawString(72, 362, "Deploy across ≥2 AZs; replicate data across regions for disaster recovery.")
    note(c, 72, 260, 468, "Rule of thumb: survive one AZ failure with zero downtime; survive one region failure with bounded RTO/RPO.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Auto Scaling: Match Capacity to Demand",
                       "Add machines when busy, remove them when idle — automatically.")
    # demand curve
    c.setStrokeColor(MUTED); c.setLineWidth(1)
    c.line(90, 300, 540, 300); c.line(90, 300, 90, 520)
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9)
    c.drawString(90, 528, "demand")
    import math
    c.setStrokeColor(ACCENT); c.setLineWidth(2.5)
    pts = []
    for i in range(90, 541, 6):
        t = (i - 90) / 450
        yy = 300 + 40 + 150 * abs(math.sin(t * 6.28)) * (0.5 + 0.5 * t)
        pts.append((i, yy))
    p = c.beginPath(); p.moveTo(*pts[0])
    for pt in pts[1:]: p.lineTo(*pt)
    c.drawPath(p)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawString(90, 250, "Scaling policies: target-tracking (keep CPU at 60%), step scaling, scheduled (known peaks).")
    c.drawString(90, 232, "Cooldowns prevent flapping — don't scale in and out on every blip.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Stateless Services + External State",
                       "Any instance can die; the system doesn't care.")
    box(c, 72, 440, 130, 60, BOX_GREEN, "App-1", "stateless")
    box(c, 216, 440, 130, 60, BOX_GREEN, "App-2", "stateless")
    box(c, 360, 440, 130, 60, BOX_GREEN, "App-3", "stateless")
    box(c, 72, 320, 200, 60, BOX_ORANGE, "Managed Database", "RDS / Cloud SQL")
    box(c, 300, 320, 200, 60, BOX_BLUE, "Object Storage", "S3 / GCS")
    for bx in [137, 281, 425]:
        arrow(c, bx, 438, bx, 382, color=ACCENT, width=1.5)
    c.setStrokeColor(RED); c.setLineWidth(2)
    c.line(300, 470, 380, 470)
    c.setFillColor(RED); c.setFont(TITLE_FONT, 11)
    c.drawCentredString(340, 480, "✗ App-2 dies")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawCentredString(306, 260, "Sessions, uploads, and state live outside the instances — in managed stores.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Decouple with Queues",
                       "Buffers absorb spikes; workers scale independently.")
    box(c, 72, 420, 120, 60, BOX_BLUE, "API", "accepts fast")
    box(c, 246, 420, 120, 60, BOX_ORANGE, "Queue", "SQS / Pub/Sub")
    box(c, 420, 420, 120, 60, BOX_GREEN, "Workers", "scale on depth")
    arrow(c, 192, 450, 244, 450, color=ACCENT, label="enqueue")
    arrow(c, 366, 450, 418, 450, color=ACCENT, label="dequeue")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawString(72, 360, "Traffic spike? The queue grows; workers scale up; nothing is dropped.")
    c.drawString(72, 342, "Dead-letter queues capture poison messages for inspection instead of infinite retry.")
    note(c, 72, 240, 468, "Queue depth is the autoscaling signal. This is the backbone of event-driven architecture.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Infrastructure as Code",
                       "Environments defined in files — versioned, reviewed, reproducible.")
    box(c, 72, 430, 220, 60, BOX_TEAL, "Terraform / Pulumi", "declarative")
    box(c, 320, 430, 220, 60, BOX_BLUE, "CloudFormation / ARM", "native")
    arrow(c, 306, 490, 306, 560, color=MUTED, width=1.5)
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9)
    c.drawCentredString(306, 575, "git repo")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    items = ["• plan → review → apply: changes are previewed like code diffs",
             "• State files track reality; drift detection flags manual changes",
             "• Modules = reusable components (a VPC module, a DB module)"]
    yy = 360
    for it in items:
        c.drawString(90, yy, it); yy -= 22
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Well-Architected: The Checklist",
                       "Five pillars every design gets judged against.")
    pillars = [("Reliability", "Survive failures; recover fast", BOX_GREEN),
               ("Security", "Least privilege, encryption everywhere", BOX_RED),
               ("Cost", "Right-size, kill idle, use commitments wisely", BOX_ORANGE),
               ("Performance", "Scale horizontally; cache aggressively", BOX_BLUE),
               ("Operations", "Automate everything; observe everything", BOX_TEAL)]
    yy = y
    for name, desc, fill in pillars:
        box(c, 72, yy - 48, 468, 52, fill, name, desc, font_size=12)
        yy -= 66
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Cloud Patterns — Remember",
                 ["Spread across AZs; replicate across regions. Geography is reliability.",
                  "Auto-scale on real signals (CPU, queue depth) with cooldowns against flapping.",
                  "Keep services stateless; push state to managed databases and object storage.",
                  "Queues decouple producers from consumers and absorb spikes gracefully.",
                  "Define infrastructure as code — versioned, reviewed, reproducible."],
                 pg)
    c.save(); print("wrote", path)


def pdf_kubernetes(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Kubernetes\nArchitecture",
               "Pods, Services, Deployments —\nhow the orchestrator runs your containers.",
               "Cloud", None); pg += 1

    y = section_header(c, 1, 6, "The Big Picture: Control Plane + Nodes",
                       "You declare desired state; Kubernetes makes it real.")
    box(c, 72, 440, 468, 90, BOX_PURP, "Control Plane", "API server • scheduler • controller manager • etcd")
    for i, bx in enumerate([72, 246, 420]):
        box(c, bx, 320, 100, 80, BOX_GREEN, f"Node {i+1}", "kubelet + pods")
        arrow(c, 306, 438, bx + 50, 402, color=ACCENT, width=1.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawString(72, 280, "etcd = the brain's memory: every object, every desired state, strongly consistent.")
    c.drawString(72, 262, "Nodes just run what they're told. If a node dies, the scheduler replaces its pods.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Pod: The Smallest Unit",
                       "One or more containers sharing network + storage. Ephemeral by design.")
    box(c, 156, 380, 300, 110, BOX_BLUE, "Pod", "one IP • shared localhost • shared volumes")
    box(c, 186, 400, 120, 56, BOX_GREEN, "app", "container")
    box(c, 316, 400, 120, 56, BOX_ORANGE, "sidecar", "logging/proxy")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawString(72, 340, "Pods die — never attach to them. Controllers keep the DESIRED COUNT alive.")
    c.drawString(72, 322, "Sidecars extend pods: service mesh proxies, log shippers, config reloaders.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Deployment: Declarative Rollouts",
                       "Say '3 replicas of v2' — the controller converges reality.")
    box(c, 72, 440, 200, 60, BOX_BLUE, "Deployment", "replicas: 3, image: v2")
    for i, bx in enumerate([72, 186, 300]):
        box(c, bx, 340, 100, 60, BOX_GREEN, f"Pod v2", "")
        arrow(c, 172, 438, bx + 50, 402, color=ACCENT, width=1.5)
    box(c, 430, 340, 110, 60, BOX_RED, "Pod v1", "terminating")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawString(72, 290, "Rolling update: new pods come up, old pods drain — zero downtime by default.")
    c.drawString(72, 272, "Rollback = set image back to v1. The controller reverses the rollout.")
    note(c, 72, 190, 468, "Readiness probes gate traffic; liveness probes restart stuck containers. Get these right.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Service: Stable Address for Ephemeral Pods",
                       "Pods churn; the Service IP and DNS name don't.")
    box(c, 216, 440, 180, 60, BOX_TEAL, "Service: orders", "ClusterIP 10.0.4.7 • DNS: orders")
    for i, bx in enumerate([106, 256, 406]):
        box(c, bx, 330, 100, 60, BOX_GREEN, f"Pod", f"10.0.1.{10+i}")
        arrow(c, 306, 438, bx + 50, 392, color=ACCENT, width=1.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawCentredString(306, 280, "Clients call the Service; kube-proxy load-balances to healthy pods.")
    c.drawString(72, 240, "Types: ClusterIP (internal), NodePort, LoadBalancer (cloud LB), Ingress (HTTP routing).")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Config & Secrets: Keep Config Out of Images",
                       "Same image, different environments.")
    items = [("ConfigMap", "Non-secret config: env vars, config files. Mount as env or volume.", BOX_BLUE),
             ("Secret", "Sensitive data, base64-encoded (encrypt etcd at rest!).", BOX_RED),
             ("Volumes", "emptyDir (ephemeral), PVC (persistent), config/secret mounts.", BOX_GREEN),
             ("Namespaces", "Virtual clusters: dev / staging / prod isolation + quotas.", BOX_ORANGE)]
    yy = y
    for name, desc, fill in items:
        box(c, 72, yy - 54, 468, 58, fill, name, desc, font_size=11.5)
        yy -= 72
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Autoscaling in Kubernetes",
                       "Two dimensions: more pods, bigger nodes.")
    box(c, 72, y - 56, 225, 90, BOX_GREEN, "HPA", "Horizontal Pod Autoscaler\nmore replicas on CPU/RAM/custom", font_size=11)
    box(c, 315, y - 56, 225, 90, BOX_BLUE, "Cluster Autoscaler", "adds/removes NODES\nwhen pods can't schedule", font_size=11)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    yy = y - 180
    for t in ["• HPA: 'keep avg CPU at 60% — add pods as needed'",
              "• VPA: right-size requests/limits from history",
              "• Cluster autoscaler: provisions cloud VMs when pending pods pile up",
              "• Scale-to-zero (Knative/KEDA): event-driven, pay-per-use"]:
        c.drawString(90, yy, t); yy -= 22
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Kubernetes — Remember",
                 ["Control plane declares desired state; nodes run it. etcd is the source of truth.",
                  "Pods are ephemeral — Deployments keep the right count alive with rolling updates.",
                  "Services give stable IPs/DNS to churning pods; Ingress routes HTTP.",
                  "ConfigMaps/Secrets separate config from images; namespaces isolate environments.",
                  "Autoscale pods with HPA, nodes with the cluster autoscaler."],
                 pg)
    c.save(); print("wrote", path)


def pdf_cicd(path):
    c = new_canvas(path); pg = 1
    title_page(c, "CI/CD Pipelines\nVisual Guide",
               "From git push to production\nin minutes — safely, repeatedly, automatically.",
               "Cloud", None); pg += 1

    y = section_header(c, 1, 6, "The Pipeline: Stages of Trust",
                       "Every commit climbs a ladder of verification.")
    stages = [("Commit", BOX_BLUE), ("Build", BOX_TEAL), ("Test", BOX_GREEN),
              ("Scan", BOX_ORANGE), ("Deploy\nStaging", BOX_PURP), ("Deploy\nProd", ACCENT)]
    bx = 52
    for i, (name, col) in enumerate(stages):
        c.setFillColor(col); c.roundRect(bx, 420, 76, 76, 10, fill=1, stroke=0)
        c.setFillColor(white); c.setFont(TITLE_FONT, 9)
        yy2 = 462
        for ln in name.split("\n"):
            c.drawCentredString(bx + 38, yy2, ln); yy2 -= 12
        if i < len(stages) - 1:
            arrow(c, bx + 76, 458, bx + 92, 458, color=INK, width=1.5)
        bx += 92
    note(c, 72, 300, 468, "Fail fast: cheap checks (lint, unit) run first; expensive ones (e2e, perf) run later. A red stage stops the line.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Continuous Integration",
                       "Merge small, merge often — let robots catch the breakage.")
    yy = bullet_list(c, 72, y,
        ["Every push triggers: checkout → build → unit tests → lint/typecheck.",
         "Branch protection: no merge without green checks + review.",
         "Trunk-based development: short-lived branches (< 1 day) beat month-long feature branches.",
         "The build artifact (container image) is versioned once and promoted unchanged through stages."],
        font_size=11, gap=26)
    box(c, 72, 200, 468, 60, BOX_GREEN, "Golden rule", "If the build is red, fixing it is everyone's top priority.", font_size=11)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Security Gates: Shift Left",
                       "Scan everything, early — before it reaches production.")
    scans = [("SAST", "Static analysis of source: injection, secrets, bad patterns", BOX_BLUE),
             ("Dependency scan", "Known CVEs in libraries (Dependabot, Snyk, Trivy)", BOX_ORANGE),
             ("Container scan", "Image layers checked for vulns + misconfig", BOX_TEAL),
             ("DAST / IAST", "Running-app tests: fuzz inputs, probe auth", BOX_RED)]
    yy = y
    for name, desc, fill in scans:
        box(c, 72, yy - 54, 468, 58, fill, name, desc, font_size=11.5)
        yy -= 72
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Deployment Strategies",
                       "How new versions reach users without drama.")
    strats = [("Rolling", "Replace instances gradually. Simple; mixed versions briefly.", BOX_GREEN),
              ("Blue/Green", "Two full environments; flip the router. Instant rollback.", BOX_BLUE),
              ("Canary", "1% → 10% → 50% → 100%, watching metrics at each step.", BOX_ORANGE),
              ("Feature flags", "Deploy code dark, enable per-user/cohort at runtime.", BOX_TEAL)]
    yy = y
    for name, desc, fill in strats:
        box(c, 72, yy - 54, 468, 58, fill, name, desc, font_size=11.5)
        yy -= 72
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "GitOps: Git as the Source of Truth",
                       "The cluster converges to what's in git — automatically.")
    box(c, 72, 440, 150, 60, BOX_BLUE, "Git repo", "desired state")
    box(c, 272, 440, 150, 60, BOX_GREEN, "ArgoCD/Flux", "sync agent")
    box(c, 72, 320, 350, 60, BOX_PURP, "Kubernetes cluster", "actual state → converges")
    arrow(c, 222, 470, 270, 470, color=ACCENT, label="watch")
    arrow(c, 347, 438, 300, 382, color=ACCENT, width=1.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawString(72, 270, "Rollbacks = git revert. Drift (manual kubectl edits) gets auto-corrected.")
    c.drawString(72, 252, "Pull requests become the change-management audit trail.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "DORA Metrics: Are We Actually Good at This?",
                       "Four numbers that predict engineering performance.")
    metrics = [("Deploy frequency", "How often to prod — elite: on demand", BOX_GREEN),
               ("Lead time", "Commit → prod — elite: < 1 hour", BOX_BLUE),
               ("Change fail rate", "% of deploys causing incidents — elite: < 15%", BOX_ORANGE),
               ("MTTR", "Restore service after incident — elite: < 1 hour", BOX_TEAL)]
    yy = y
    for name, desc, fill in metrics:
        box(c, 72, yy - 54, 468, 58, fill, name, desc, font_size=11.5)
        yy -= 72
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "CI/CD — Remember",
                 ["Pipeline stages climb in cost: lint/unit first, e2e/perf later; red stops the line.",
                  "Build the artifact once; promote the identical image through every stage.",
                  "Shift security left: SAST, dependency, container, and DAST scans in-pipeline.",
                  "Deploy progressively: rolling, blue/green, canary, feature flags.",
                  "GitOps makes git the source of truth; DORA metrics tell you if it's working."],
                 pg)
    c.save(); print("wrote", path)


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(out, exist_ok=True)
    pdf_cloud_patterns(os.path.join(out, "bbg-cloud-patterns.pdf"))
    pdf_kubernetes(os.path.join(out, "bbg-kubernetes.pdf"))
    pdf_cicd(os.path.join(out, "bbg-cicd-pipeline.pdf"))

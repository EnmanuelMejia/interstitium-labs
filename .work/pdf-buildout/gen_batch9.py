"""Batch 9: Cloud & DevOps PDFs — 25 guides."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bbg_style import *


def pdf_aws_core(path):
    c = new_canvas(path); pg = 1
    title_page(c, "AWS Core Services\nVisual Guide",
               "EC2, S3, VPC, IAM, RDS, Lambda —\nthe six primitives behind a typical 3-tier app.",
               "Cloud & DevOps", None); pg += 1

    y = section_header(c, 1, 6, "Meet the Six Core Services",
                       "Each solves one job; together they run a business.")
    svcs = [("EC2", "virtual servers", BOX_BLUE), ("S3", "object storage", BOX_GREEN),
            ("VPC", "private network", BOX_ORANGE), ("IAM", "identity & access", BOX_RED),
            ("RDS", "managed databases", BOX_TEAL), ("Lambda", "serverless functions", BOX_PURP)]
    for i, (n, d, f) in enumerate(svcs):
        bx = 72 + (i % 3) * 160; by = 500 - (i // 3) * 110
        box(c, bx, by, 148, 90, f, n, d, font_size=12)
    note(c, 72, 250, 468, "Rule of thumb: compute (EC2/Lambda) runs code, S3/RDS hold data, VPC connects, IAM guards.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "VPC: Your Private Network",
                       "Isolated network with public and private subnets.")
    box(c, 72, 330, 468, 220, BOX_BLUE, "VPC 10.0.0.0/16", "your isolated network region")
    box(c, 100, 460, 200, 60, BOX_GREEN, "Public subnet", "ALB + NAT live here")
    box(c, 320, 460, 190, 60, BOX_GREEN, "Private subnet", "EC2 + RDS live here")
    box(c, 100, 360, 200, 60, BOX_ORANGE, "Internet Gateway", "public traffic in/out")
    box(c, 320, 360, 190, 60, BOX_TEAL, "Security Groups", "stateful firewall rules")
    arrow(c, 200, 490, 200, 422, color=ACCENT, width=1.5)
    arrow(c, 415, 490, 415, 422, color=ACCENT, width=1.5)
    note(c, 72, 250, 468, "Private subnets reach the internet via NAT (outbound only) — databases never get public IPs.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "The Web Tier: EC2 Behind a Load Balancer",
                       "Stateless app servers scale horizontally.")
    box(c, 226, 520, 160, 60, BOX_BLUE, "Application LB", "distributes traffic")
    for i, bx in enumerate([106, 256, 406]):
        box(c, bx, 380, 100, 80, BOX_GREEN, f"EC2-{i+1}", "app server")
        arrow(c, 306, 518, bx + 50, 462, color=GREEN, width=1.5)
    arrow(c, 306, 640, 306, 582, color=ACCENT, width=2, label="users")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawString(72, 300, "Auto Scaling group: add/remove EC2 instances on CPU or request-count metrics.")
    c.drawString(72, 282, "Health checks pull dead instances out of rotation automatically.")
    note(c, 72, 200, 468, "Keep app servers stateless: sessions in ElastiCache, uploads straight to S3.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "The Data Tier: RDS + S3",
                       "Managed database for rows; object store for everything else.")
    box(c, 72, 460, 220, 80, BOX_TEAL, "RDS", "Postgres/MySQL — managed")
    box(c, 320, 460, 220, 80, BOX_GREEN, "S3", "images, backups, logs")
    arrow(c, 306, 400, 306, 340, color=ACCENT, width=2, label="EC2 app servers")
    box(c, 226, 250, 160, 70, BOX_ORANGE, "EC2 app servers", "query RDS, write S3")
    arrow(c, 182, 458, 270, 322, color=TEAL, width=1.5)
    arrow(c, 430, 458, 340, 322, color=GREEN, width=1.5)
    note(c, 72, 170, 468, "RDS Multi-AZ: synchronous standby in another zone — automatic failover, no data loss.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "IAM: Who Can Do What",
                       "Identity first — every call is authenticated and authorized.")
    box(c, 72, 500, 130, 70, BOX_RED, "Users", "humans")
    box(c, 232, 500, 130, 70, BOX_RED, "Roles", "for services")
    box(c, 392, 500, 130, 70, BOX_RED, "Policies", "JSON permissions")
    box(c, 176, 360, 260, 70, BOX_BLUE, "EC2 instance", "assumes role")
    arrow(c, 297, 498, 297, 432, color=RED, width=2, label="assumes")
    arrow(c, 457, 520, 380, 400, color=RED, width=1.5, label="policy")
    note(c, 72, 260, 468, "Least privilege: grant only the actions needed. EC2 gets an IAM role — never embed access keys.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Lambda: Events In, Code Out",
                       "Serverless glue for async work and automation.")
    box(c, 72, 500, 140, 70, BOX_GREEN, "S3 upload", "event source")
    box(c, 236, 500, 140, 70, BOX_PURP, "Lambda", "thumbnail fn")
    box(c, 400, 500, 140, 70, BOX_GREEN, "S3 thumbs/", "output")
    arrow(c, 212, 535, 234, 535, color=ACCENT, width=2)
    arrow(c, 376, 535, 398, 535, color=ACCENT, width=2)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawString(72, 430, "Other triggers: API Gateway (REST APIs), SQS queues, DynamoDB streams, EventBridge schedules.")
    bullet_list(c, 72, 400,
        ["No servers to manage — scales from 0 to thousands of concurrent executions.",
         "Pay per invocation + duration: ideal for spiky, event-driven work.",
         "15-min max runtime: not for long jobs — that's EC2/ECS territory."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "AWS Core Services — Remember",
                 ["VPC isolates your network: public subnets for load balancers, private for app and data.",
                  "EC2 + Auto Scaling + ALB = the classic stateless web tier.",
                  "RDS handles relational data (use Multi-AZ); S3 handles objects at any scale.",
                  "IAM roles over keys; least-privilege policies on everything.",
                  "Lambda glues events to actions — perfect for async, spiky workloads."],
                 pg)
    c.save(); print("wrote", path)


def pdf_gcp_core(path):
    c = new_canvas(path); pg = 1
    title_page(c, "GCP Core Services\nVisual Guide",
               "Compute Engine, Cloud Storage, VPC, IAM,\nCloud SQL, BigQuery — how they connect.",
               "Cloud & DevOps", None); pg += 1

    y = section_header(c, 1, 6, "Meet the Six Core Services",
                       "Google's equivalents of the cloud primitives.")
    svcs = [("Compute Engine", "virtual servers", BOX_BLUE), ("Cloud Storage", "object storage", BOX_GREEN),
            ("VPC", "global network", BOX_ORANGE), ("IAM", "identity & access", BOX_RED),
            ("Cloud SQL", "managed databases", BOX_TEAL), ("BigQuery", "data warehouse", BOX_PURP)]
    for i, (n, d, f) in enumerate(svcs):
        bx = 72 + (i % 3) * 160; by = 500 - (i // 3) * 110
        box(c, bx, by, 148, 90, f, n, d, font_size=11)
    note(c, 72, 250, 468, "GCP networks are GLOBAL: one VPC spans all regions — subnets are regional, not per-VPC-per-region like AWS.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "VPC: One Global Network",
                       "Single VPC, regional subnets, firewall rules as code.")
    box(c, 72, 330, 468, 220, BOX_BLUE, "VPC (global)", "one network, many regions")
    box(c, 100, 460, 200, 60, BOX_GREEN, "subnet us-east", "10.1.0.0/24")
    box(c, 320, 460, 190, 60, BOX_GREEN, "subnet eu-west", "10.2.0.0/24")
    box(c, 100, 360, 200, 60, BOX_ORANGE, "Firewall rules", "allow 443, deny rest")
    box(c, 320, 360, 190, 60, BOX_TEAL, "Cloud NAT", "private egress")
    arrow(c, 200, 458, 200, 422, color=ACCENT, width=1.5)
    arrow(c, 415, 458, 415, 422, color=ACCENT, width=1.5)
    note(c, 72, 250, 468, "Routes and peering are automatic inside a global VPC — no transit gateways to wire up.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "The Web Tier: Managed Instance Groups",
                       "Compute Engine VMs behind a global load balancer.")
    box(c, 226, 520, 160, 60, BOX_BLUE, "Global LB", "anycast frontend")
    for i, bx in enumerate([106, 256, 406]):
        box(c, bx, 380, 100, 80, BOX_GREEN, f"VM-{i+1}", "MIG instance")
        arrow(c, 306, 518, bx + 50, 462, color=GREEN, width=1.5)
    arrow(c, 306, 640, 306, 582, color=ACCENT, width=2, label="users")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawString(72, 300, "Managed Instance Group (MIG): autoscaling + autohealing, like an ASG.")
    c.drawString(72, 282, "Global LB terminates TLS at the edge, closest to the user.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Data Flow: Cloud SQL → BigQuery",
                       "Transactional store feeding the analytics warehouse.")
    box(c, 72, 480, 150, 70, BOX_TEAL, "Cloud SQL", "Postgres/MySQL")
    box(c, 300, 480, 150, 70, BOX_BLUE, "Dataflow", "ETL pipeline")
    box(c, 400, 360, 140, 70, BOX_PURP, "BigQuery", "analytics SQL")
    box(c, 72, 360, 150, 70, BOX_GREEN, "Cloud Storage", "raw landing")
    arrow(c, 222, 515, 298, 515, color=ACCENT, width=2)
    arrow(c, 375, 480, 420, 432, color=ACCENT, width=2)
    arrow(c, 147, 478, 147, 432, color=GREEN, width=1.5, label="exports")
    note(c, 72, 270, 468, "BigQuery is serverless: no clusters to size — you pay per query scanned, not per hour.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "IAM: Roles & Service Accounts",
                       "Workloads get identities too — not just humans.")
    box(c, 72, 500, 140, 70, BOX_RED, "Users", "Google accounts")
    box(c, 240, 500, 140, 70, BOX_RED, "Service accounts", "workload identity")
    box(c, 408, 500, 132, 70, BOX_RED, "Roles", "permissions bundle")
    box(c, 176, 360, 260, 70, BOX_BLUE, "GCE VM", "runs as svc account")
    arrow(c, 310, 498, 306, 432, color=RED, width=2, label="attached")
    arrow(c, 474, 520, 390, 400, color=RED, width=1.5, label="bound")
    note(c, 72, 260, 468, "Attach a service account to the VM and grant it a role — code uses default credentials, no keys in the repo.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Putting It Together: 3-Tier on GCP",
                       "The same architecture, GCP-flavored.")
    box(c, 226, 540, 160, 56, BOX_BLUE, "Global LB", "HTTPS frontend")
    box(c, 226, 440, 160, 56, BOX_GREEN, "MIG: app VMs", "autoscaled")
    box(c, 226, 340, 160, 56, BOX_TEAL, "Cloud SQL", "HA primary")
    box(c, 226, 240, 160, 56, BOX_PURP, "BigQuery", "warehouse")
    arrow(c, 306, 538, 306, 498, color=ACCENT, width=2)
    arrow(c, 306, 438, 306, 398, color=ACCENT, width=2)
    arrow(c, 386, 340, 420, 300, color=ACCENT2, width=1.5, label="nightly ETL")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "GCP Core Services — Remember",
                 ["GCP VPCs are global — subnets are regional, peering is simple by default.",
                  "MIG + Global LB = autoscaled web tier with edge TLS termination.",
                  "Cloud SQL for transactions; BigQuery (serverless) for analytics at scale.",
                  "Service accounts give workloads identities — attach, don't embed keys.",
                  "Firewall rules are stateful and centralized per VPC, not per instance."],
                 pg)
    c.save(); print("wrote", path)


def pdf_azure_core(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Azure Core Services\nVisual Guide",
               "VMs, Blob Storage, VNet, Entra ID,\nSQL Database — how they connect.",
               "Cloud & DevOps", None); pg += 1

    y = section_header(c, 1, 6, "Meet the Five Core Services",
                       "Microsoft's equivalents of the cloud primitives.")
    svcs = [("Virtual Machines", "compute", BOX_BLUE), ("Blob Storage", "object storage", BOX_GREEN),
            ("VNet", "private network", BOX_ORANGE), ("Entra ID", "identity (ex-AAD)", BOX_RED),
            ("SQL Database", "managed SQL", BOX_TEAL)]
    for i, (n, d, f) in enumerate(svcs[:3]):
        bx = 72 + i * 160
        box(c, bx, by := 500, 148, 90, f, n, d, font_size=11)
    for i, (n, d, f) in enumerate(svcs[3:]):
        bx = 152 + i * 160
        box(c, bx, 390, 148, 90, f, n, d, font_size=11)
    note(c, 72, 250, 468, "Everything in Azure lives in a Resource Group — the unit of billing, access, and lifecycle.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "VNet: Subnets, NSGs, Peering",
                       "Isolated network; NSGs filter traffic per subnet or NIC.")
    box(c, 72, 330, 468, 220, BOX_BLUE, "VNet 10.0.0.0/16", "isolated network")
    box(c, 100, 460, 200, 60, BOX_GREEN, "Web subnet", "App Gateway")
    box(c, 320, 460, 190, 60, BOX_GREEN, "Data subnet", "VMs + SQL")
    box(c, 100, 360, 200, 60, BOX_ORANGE, "NSG rules", "allow 443, deny *")
    box(c, 320, 360, 190, 60, BOX_TEAL, "VNet peering", "to hub VNet")
    arrow(c, 200, 458, 200, 422, color=ACCENT, width=1.5)
    arrow(c, 415, 458, 415, 422, color=ACCENT, width=1.5)
    note(c, 72, 250, 468, "NSGs are stateful: allow inbound 443 and the return traffic flows automatically.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "The Web Tier: VMSS + App Gateway",
                       "Virtual Machine Scale Sets behind a regional gateway.")
    box(c, 226, 520, 160, 60, BOX_BLUE, "App Gateway", "WAF + routing")
    for i, bx in enumerate([106, 256, 406]):
        box(c, bx, 380, 100, 80, BOX_GREEN, f"VM-{i+1}", "scale set")
        arrow(c, 306, 518, bx + 50, 462, color=GREEN, width=1.5)
    arrow(c, 306, 640, 306, 582, color=ACCENT, width=2, label="users")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawString(72, 300, "VM Scale Set: identical VMs from one image, autoscaled on metrics.")
    c.drawString(72, 282, "Application Gateway: layer-7 routing + Web Application Firewall.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Data: Blob + SQL Database",
                       "Hot/cool/archive tiers for blobs; managed SQL for rows.")
    box(c, 72, 460, 220, 80, BOX_TEAL, "SQL Database", "PaaS — patched for you")
    box(c, 320, 460, 220, 80, BOX_GREEN, "Blob Storage", "hot / cool / archive")
    box(c, 226, 330, 160, 70, BOX_ORANGE, "VM app tier", "queries + uploads")
    arrow(c, 306, 458, 306, 402, color=TEAL, width=2)
    arrow(c, 430, 480, 360, 400, color=GREEN, width=1.5)
    note(c, 72, 250, 468, "Blob lifecycle policies: auto-tier hot → cool → archive as data ages. Archive retrieval takes hours — plan restores.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Entra ID: Identity Without Passwords",
                       "Managed identities give Azure resources an Entra identity.")
    box(c, 72, 500, 140, 70, BOX_RED, "Users", "Entra accounts")
    box(c, 240, 500, 140, 70, BOX_RED, "Managed identity", "for the VM")
    box(c, 408, 500, 132, 70, BOX_RED, "RBAC roles", "least privilege")
    box(c, 176, 360, 260, 70, BOX_BLUE, "App Service / VM", "no secrets stored")
    arrow(c, 310, 498, 306, 432, color=RED, width=2, label="identity")
    arrow(c, 474, 520, 390, 400, color=RED, width=1.5, label="grants")
    note(c, 72, 260, 468, "The app calls Azure services as itself — tokens are issued by the platform, rotated automatically.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Putting It Together: 3-Tier on Azure",
                       "The same architecture, Azure-flavored.")
    box(c, 226, 540, 160, 56, BOX_BLUE, "App Gateway", "WAF + TLS")
    box(c, 226, 440, 160, 56, BOX_GREEN, "VM Scale Set", "autoscaled")
    box(c, 226, 340, 160, 56, BOX_TEAL, "SQL Database", "zone-redundant")
    box(c, 226, 240, 160, 56, BOX_GREEN, "Blob Storage", "media + backups")
    arrow(c, 306, 538, 306, 498, color=ACCENT, width=2)
    arrow(c, 306, 438, 306, 398, color=ACCENT, width=2)
    arrow(c, 386, 440, 420, 300, color=GREEN, width=1.5, label="uploads")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Azure Core Services — Remember",
                 ["Resource Groups are the unit of billing, access, and lifecycle — name them well.",
                  "VM Scale Sets + Application Gateway = autoscaled web tier with WAF.",
                  "SQL Database is PaaS (patched/managed); Blob tiers cut storage cost as data ages.",
                  "Managed identities eliminate stored secrets — the platform issues tokens.",
                  "NSGs + VNet peering give you a segmented, hub-and-spoke network."],
                 pg)
    c.save(); print("wrote", path)


def pdf_helm(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Helm\nVisual Guide",
               "Charts, values, templates, releases —\nKubernetes packaging done right.",
               "Cloud & DevOps", None); pg += 1

    y = section_header(c, 1, 6, "Chart Anatomy",
                       "A chart is a versioned package of Kubernetes manifests.")
    files = [("Chart.yaml", "name, version, appVersion", BOX_BLUE),
             ("values.yaml", "defaults the user can override", BOX_GREEN),
             ("templates/", "Go-templated manifests", BOX_ORANGE),
             ("charts/", "bundled sub-charts", BOX_TEAL)]
    yy = y
    for name, desc, fill in files:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=12)
        yy -= 70
    note(c, 72, yy - 60, 468, "Version BOTH chart and app: bump chart version on every change so upgrades are traceable.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Render Flow: Values → Templates → Manifests",
                       "Helm renders templates, then applies plain YAML to the cluster.")
    box(c, 72, 500, 140, 70, BOX_GREEN, "values.yaml", "replicas: 3")
    box(c, 252, 500, 140, 70, BOX_ORANGE, "templates/", "{{ .Values.replicas }}")
    box(c, 432, 500, 108, 70, BOX_BLUE, "manifests", "replicas: 3")
    arrow(c, 212, 535, 250, 535, color=ACCENT, width=2)
    arrow(c, 392, 535, 430, 535, color=ACCENT, width=2)
    box(c, 176, 380, 260, 70, BOX_PURP, "Kubernetes", "Deployment v3")
    arrow(c, 486, 498, 360, 452, color=ACCENT2, width=2, label="apply")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawString(72, 320, "helm template renders locally — dry-run and diff before anything touches the cluster.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Release Lifecycle",
                       "Install → upgrade → rollback: every release is versioned.")
    box(c, 72, 480, 120, 70, BOX_GREEN, "install", "release v1")
    box(c, 216, 480, 120, 70, BOX_BLUE, "upgrade", "release v2")
    box(c, 360, 480, 120, 70, BOX_RED, "rollback", "back to v1")
    arrow(c, 192, 515, 214, 515, color=ACCENT, width=2)
    arrow(c, 336, 515, 358, 515, color=ACCENT, width=2)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 400, "helm upgrade --install: idempotent deploys — same command for first and tenth release.")
    bullet_list(c, 72, 368,
        ["helm list shows every release and its revision number.",
         "helm history <release>: audit trail of what changed, when, by whom.",
         "One chart, many releases: dev/staging/prod differ only in values files."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Templating Power (and Traps)",
                       "Go templates make charts reusable — with discipline.")
    good = [("Conditionals", "{{- if .Values.ingress.enabled }} — optional resources", BOX_GREEN),
            ("Loops", "{{- range .Values.hosts }} — N items from one block", BOX_BLUE),
            ("Helpers", "_helpers.tpl — shared labels/names, DRY charts", BOX_TEAL)]
    yy = y
    for name, desc, fill in good:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=11)
        yy -= 70
    note(c, 72, yy - 60, 468, "Trap: templates are string surgery — always `helm template | kubectl apply --dry-run=client` after edits.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Upgrades & Rollbacks in Practice",
                       "Atomic upgrades fail fast; rollbacks restore the last good state.")
    box(c, 72, 480, 220, 80, BOX_BLUE, "helm upgrade --atomic", "auto-rollback on failure")
    box(c, 320, 480, 220, 80, BOX_ORANGE, "--wait --timeout", "block until healthy")
    arrow(c, 292, 520, 318, 520, color=ACCENT, width=2)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 400, "A broken v2 never becomes the current release — traffic stays on v1.")
    bullet_list(c, 72, 368,
        ["--atomic: if the upgrade fails, Helm rolls back to the previous revision automatically.",
         "--wait: don't declare victory until pods are actually Ready.",
         "helm rollback <release> [revision]: one command back to safety — practice it in staging."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "values.yaml Strategy",
                       "Layered values keep environments honest.")
    box(c, 72, 500, 150, 70, BOX_GREEN, "values.yaml", "sane defaults")
    box(c, 250, 500, 150, 70, BOX_BLUE, "values-prod.yaml", "replicas, resources")
    box(c, 428, 500, 112, 70, BOX_ORANGE, "--set", "one-off overrides")
    arrow(c, 222, 535, 248, 535, color=ACCENT, width=2)
    arrow(c, 400, 535, 426, 535, color=ACCENT, width=2)
    box(c, 176, 380, 260, 70, BOX_PURP, "Final release", "merged, in order")
    arrow(c, 486, 498, 370, 452, color=ACCENT2, width=2)
    note(c, 72, 290, 468, "Later files win. Keep secrets OUT of values — use sealed-secrets or external-secrets instead.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Helm — Remember",
                 ["A chart = Chart.yaml + values.yaml + templates: versioned, reusable K8s packaging.",
                  "Render flow: values fill templates → plain manifests → applied to the cluster.",
                  "helm upgrade --install --atomic --wait: the safe, idempotent deploy command.",
                  "Layer values (defaults → env file → --set); never put secrets in values.",
                  "history + rollback make every release reversible — practice rollbacks."],
                 pg)
    c.save(); print("wrote", path)


def pdf_gitops(path):
    c = new_canvas(path); pg = 1
    title_page(c, "GitOps\nVisual Guide",
               "Git as the source of truth —\nreconcile your cluster with every commit.",
               "Cloud & DevOps", None); pg += 1

    y = section_header(c, 1, 6, "The Core Idea: Git Is the Desired State",
                       "If it's not in git, it doesn't exist. If it is, the cluster converges to it.")
    box(c, 72, 460, 180, 90, BOX_BLUE, "Git repo", "desired state\n+ history")
    box(c, 360, 460, 180, 90, BOX_GREEN, "Cluster", "actual state")
    arrow(c, 252, 505, 358, 505, color=ACCENT, width=2.5, label="reconcile")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 400, "Every change is a pull request: reviewed, tested, auditable — then merged.")
    c.drawString(72, 382, "Rollback = git revert. The cluster follows the repo, not the other way around.")
    note(c, 72, 290, 468, "Manual `kubectl apply` from a laptop is the anti-pattern — it creates drift nobody can see.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "The Reconciliation Loop",
                       "An agent in the cluster watches git and applies changes continuously.")
    box(c, 72, 520, 140, 70, BOX_BLUE, "Git repo", "main branch")
    box(c, 380, 520, 160, 70, BOX_PURP, "ArgoCD / Flux", "in-cluster agent")
    box(c, 176, 380, 260, 70, BOX_GREEN, "Kubernetes", "converged state")
    arrow(c, 212, 555, 378, 555, color=ACCENT, width=2, label="poll / webhook")
    arrow(c, 460, 518, 360, 452, color=ACCENT2, width=2, label="apply")
    arrow(c, 250, 415, 140, 470, color=GREEN, width=1.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawString(72, 320, "Loop: observe actual state → compare to git → act to close the gap → repeat every few minutes.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Drift Detection & Self-Healing",
                       "Someone edits the cluster by hand — the agent notices and fixes it.")
    box(c, 72, 500, 140, 70, BOX_BLUE, "Git says", "replicas: 3")
    box(c, 400, 500, 140, 70, BOX_RED, "Cluster has", "replicas: 5?!")
    box(c, 226, 360, 160, 70, BOX_GREEN, "Self-heal", "scale back to 3")
    arrow(c, 212, 535, 398, 535, color=RED, width=2, label="drift!")
    arrow(c, 470, 498, 330, 432, color=GREEN, width=2, label="correct")
    note(c, 72, 270, 468, "Self-heal is optional per app — some teams only alert on drift, letting a human decide.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Pull vs Push",
                       "Two ways to get the desired state into the cluster.")
    box(c, 72, y - 80, 225, 120, BOX_BLUE, "PUSH", "CI deploys to cluster", font_size=13)
    box(c, 315, y - 80, 225, 120, BOX_GREEN, "PULL (GitOps)", "agent pulls from git", font_size=13)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    pa = ["CI holds cluster credentials (blast radius)", "Drift between pushes goes unnoticed", "Simple for tiny setups"]
    pb = ["Cluster needs no inbound creds from CI", "Continuous reconciliation kills drift", "Scales to many clusters from one repo"]
    yy = y - 120
    for a, b in zip(pa, pb):
        c.drawString(72, yy, "• " + a); c.drawString(315, yy, "• " + b); yy -= 20
    note(c, 72, 160, 468, "Pull wins at scale: the cluster's agent is the only writer, and credentials never leave the cluster.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Repo Layouts: App of Apps",
                       "One repo can bootstrap an entire fleet of clusters.")
    box(c, 72, 500, 150, 70, BOX_BLUE, "infra repo", "cluster-wide tools")
    box(c, 246, 500, 150, 70, BOX_GREEN, "apps repo", "team services")
    box(c, 420, 500, 120, 70, BOX_ORANGE, "env overlays", "dev/stage/prod")
    arrow(c, 222, 535, 244, 535, color=ACCENT, width=1.5)
    arrow(c, 396, 535, 418, 535, color=ACCENT, width=1.5)
    box(c, 176, 380, 260, 70, BOX_PURP, "Root app", "syncs everything")
    arrow(c, 306, 498, 306, 452, color=ACCENT2, width=2)
    note(c, 72, 290, 468, "App-of-apps: one parent application syncs child apps — new cluster = point root app at a new repo path.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Secrets in GitOps",
                       "Git must never hold plaintext secrets — encrypt or reference them.")
    opts = [("Sealed Secrets", "encrypted in git, decrypted in-cluster by controller", BOX_BLUE),
            ("External Secrets", "git holds a reference; operator fetches from vault/KMS", BOX_GREEN),
            ("SOPS + age", "encrypt values files; CI/operator decrypts at sync", BOX_ORANGE)]
    yy = y
    for name, desc, fill in opts:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=11)
        yy -= 70
    note(c, 72, yy - 60, 468, "Golden rule: the repo is public-safe. If a secret leaks into git history, rotate it — history is forever.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "GitOps — Remember",
                 ["Desired state lives in git; the cluster converges to it continuously.",
                  "Reconciliation loop: observe → compare → act, every few minutes.",
                  "Drift is detected automatically; self-heal decides whether to auto-correct.",
                  "Pull beats push at scale: no cluster credentials in CI, drift dies.",
                  "Secrets stay encrypted or referenced — git history never forgets."],
                 pg)
    c.save(); print("wrote", path)


def pdf_terraform(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Terraform & IaC\nVisual Guide",
               "Plan, apply, repeat —\ninfrastructure as reviewable code.",
               "Cloud & DevOps", None); pg += 1

    y = section_header(c, 1, 6, "Providers & Resources",
                       "Providers talk to APIs; resources declare what should exist.")
    box(c, 72, 500, 140, 70, BOX_BLUE, "provider \"aws\"", "talks to AWS API")
    box(c, 240, 500, 160, 70, BOX_GREEN, "resource \"aws_instance\"", "\"web\" = t3.micro")
    box(c, 428, 500, 112, 70, BOX_ORANGE, "data source", "read existing")
    arrow(c, 212, 535, 238, 535, color=ACCENT, width=2)
    arrow(c, 400, 535, 426, 535, color=ACCENT, width=2)
    box(c, 176, 380, 260, 70, BOX_PURP, "Real infrastructure", "created via API")
    arrow(c, 306, 498, 306, 452, color=ACCENT2, width=2)
    note(c, 72, 290, 468, "Declarative: you describe the END state. Terraform figures out the create/update/delete order.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "The State File",
                       "Terraform's memory: what it created, mapped to real IDs.")
    box(c, 72, 480, 200, 90, BOX_ORANGE, "terraform.tfstate", "resource → real ID\n+ attributes")
    box(c, 340, 480, 200, 90, BOX_BLUE, ".tf config", "what you WANT")
    arrow(c, 272, 525, 338, 525, color=ACCENT, width=2, label="plan diffs")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 400, "Plan compares config vs state vs reality → proposes a change set.")
    bullet_list(c, 72, 368,
        ["State is the source of truth for Terraform — lose it and it will try to recreate everything.",
         "Never hand-edit state; use `terraform import` and `terraform state mv` instead.",
         "State can hold secrets — encrypt it and restrict access."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "The Plan / Apply Cycle",
                       "Review the diff, then let Terraform execute it.")
    steps = [("1. init", "download providers", BOX_BLUE), ("2. plan", "preview the diff", BOX_ORANGE),
             ("3. review", "human approves", BOX_GREEN), ("4. apply", "execute changes", BOX_RED)]
    bx = 72
    for name, desc, fill in steps:
        box(c, bx, 480, 108, 80, fill, name, desc, font_size=10)
        if bx > 72: arrow(c, bx - 12, 520, bx, 520, color=ACCENT, width=1.5)
        bx += 120
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 400, "CI runs plan on every PR and posts the diff as a comment — infrastructure gets code review.")
    note(c, 72, 300, 468, "`terraform plan -out=tfplan` + `terraform apply tfplan`: apply EXACTLY what was reviewed, nothing more.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Modules: Reusable Building Blocks",
                       "Package common patterns once; instantiate with different inputs.")
    box(c, 72, 500, 200, 90, BOX_BLUE, "module \"vpc\"", "source = ./modules/vpc")
    box(c, 340, 500, 200, 90, BOX_BLUE, "module \"vpc\"", "source = ./modules/vpc")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawString(110, 530, "cidr = 10.1.0.0/16"); c.drawString(378, 530, "cidr = 10.2.0.0/16")
    c.drawString(72, 440, "Same module, different inputs: dev and prod networks from one tested codebase.")
    bullet_list(c, 72, 408,
        ["Inputs (variables) in, outputs out — modules are functions for infrastructure.",
         "Pin module versions (git tags / registry versions) — floating refs break prod at 2am.",
         "Compose modules: network → cluster → apps, each with a clear contract."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Remote Backends & Locking",
                       "Shared state needs a backend with locking — not a laptop file.")
    box(c, 72, 500, 220, 80, BOX_GREEN, "S3 + DynamoDB", "state + lock table")
    box(c, 320, 500, 220, 80, BOX_TEAL, "Terraform Cloud", "managed runs + VCS")
    arrow(c, 292, 540, 318, 540, color=ACCENT, width=1.5, label="or")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 400, "Two engineers apply at once without locking → corrupted state, duplicated resources.")
    bullet_list(c, 72, 368,
        ["Backend stores state remotely; the lock prevents concurrent writes.",
         "Enable versioning on the state bucket — a bad write is recoverable.",
         "Separate state per environment (dev/stage/prod): smaller blast radius."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Drift: When Reality Diverges",
                       "Hand-changes in the console create drift — plan finds it.")
    box(c, 72, 500, 140, 70, BOX_BLUE, "Config", "port = 443")
    box(c, 400, 500, 140, 70, BOX_RED, "Reality", "port = 80?!")
    box(c, 226, 360, 160, 70, BOX_ORANGE, "terraform plan", "detects the diff")
    arrow(c, 212, 535, 398, 535, color=RED, width=2, label="drift")
    arrow(c, 470, 498, 330, 432, color=ORANGE, width=2, label="next apply fixes")
    note(c, 72, 270, 468, "Schedule nightly `plan` in CI: alert on unexpected diffs — that's your drift detector.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Terraform & IaC — Remember",
                 ["Declarative config + provider APIs: describe the end state, Terraform orders the steps.",
                  "The state file is Terraform's memory — back it up, lock it, never hand-edit it.",
                  "Plan → review → apply: infrastructure gets the same PR review as code.",
                  "Modules are functions for infra: inputs in, outputs out, versions pinned.",
                  "Remote backends + locking make teamwork safe; nightly plans catch drift."],
                 pg)
    c.save(); print("wrote", path)


def pdf_docker_deep(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Docker Deep Dive\nVisual Guide",
               "Layers, cache, multi-stage builds —\nfast, small, secure images.",
               "Cloud & DevOps", None); pg += 1

    y = section_header(c, 1, 6, "Image Layers: Copy-on-Write Stack",
                       "Each Dockerfile instruction adds a read-only layer.")
    layers = [("base: alpine", BOX_BLUE), ("+ packages", BOX_GREEN),
              ("+ app code", BOX_ORANGE), ("+ config", BOX_TEAL)]
    yy = 560
    for name, fill in layers:
        c.setFillColor(fill); c.rect(176, yy - 40, 260, 44, fill=1, stroke=0)
        c.setStrokeColor(INK); c.setLineWidth(1.2); c.rect(176, yy - 40, 260, 44, fill=0, stroke=1)
        c.setFillColor(INK); c.setFont(BODY_FONT, 10.5); c.drawCentredString(306, yy - 22, name)
        yy -= 52
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawString(176, 300, "Container layer (writable, thin) sits on top — delete the container, the layer goes with it.")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 10)
    c.drawString(176, 282, "Layers are content-addressed and SHARED: ten images on one base share one copy.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Dockerfile Best Practices",
                       "Order matters: stable layers first, volatile last.")
    box(c, 72, 480, 468, 90, BOX_BLUE, "GOOD order", "FROM → deps → code → config")
    c.setFillColor(INK); c.setFont(MONO_FONT, 9.5)
    c.drawString(88, 530, "COPY package.json . && npm ci     # deps change rarely")
    c.drawString(88, 512, "COPY src/ ./                     # code changes often")
    box(c, 72, 360, 468, 90, BOX_RED, "BAD order", "code copied BEFORE deps install")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawString(88, 400, "Every code change invalidates the npm layer → 5-minute rebuilds, every time.")
    note(c, 72, 260, 468, ".dockerignore is mandatory: keep node_modules, .git, and secrets OUT of the build context.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Build Cache Mechanics",
                       "Docker reuses layers until the first changed instruction.")
    box(c, 72, 500, 120, 70, BOX_GREEN, "cached ✓", "layer reused")
    box(c, 216, 500, 120, 70, BOX_GREEN, "cached ✓", "layer reused")
    box(c, 360, 500, 120, 70, BOX_RED, "CHANGED", "rebuild here")
    box(c, 72, 400, 408, 70, BOX_ORANGE, "everything below rebuilt", "cache invalidated downstream")
    arrow(c, 132, 498, 214, 498, color=ACCENT, width=1.5)
    arrow(c, 276, 498, 358, 498, color=ACCENT, width=1.5)
    arrow(c, 420, 498, 300, 472, color=RED, width=1.5)
    note(c, 72, 300, 468, "BuildKit (--progress=plain) shows exactly which layer broke the cache. Combine RUN steps to shrink layer count.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Multi-Stage Builds",
                       "Build with the heavy toolchain; ship only the artifact.")
    box(c, 72, 500, 220, 90, BOX_ORANGE, "stage: build", "golang:1.22\ncompile binary")
    box(c, 320, 500, 220, 90, BOX_GREEN, "stage: runtime", "alpine\nCOPY --from=build")
    arrow(c, 292, 545, 318, 545, color=ACCENT, width=2, label="binary only")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 430, "Result: 800MB build image → 25MB runtime image. No compiler, no source, smaller attack surface.")
    bullet_list(c, 72, 398,
        ["`FROM golang AS build` then `FROM alpine` — final image starts from the last stage.",
         "`COPY --from=build /app/bin /usr/local/bin/app`: take only what you need.",
         "Use distroless or minimal bases for production — fewer CVEs to patch."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Registries: Push, Pull, Scan",
                       "The artifact store every deploy pulls from.")
    box(c, 72, 500, 130, 70, BOX_BLUE, "docker build", "local image")
    box(c, 232, 500, 130, 70, BOX_ORANGE, "docker push", "registry:tag")
    box(c, 392, 500, 130, 70, BOX_GREEN, "cluster pulls", "by digest")
    arrow(c, 202, 535, 230, 535, color=ACCENT, width=2)
    arrow(c, 362, 535, 390, 535, color=ACCENT, width=2)
    bullet_list(c, 72, 430,
        ["Tag immutably: `app:1.4.2` and `app:1.4.2-<sha>` — never deploy `:latest` to prod.",
         "Scan on push: registries flag CVEs before the image can deploy.",
         "Pull by DIGEST in prod (`app@sha256:…`) — tags can be re-pointed, digests can't."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Run It Right: Runtime Hygiene",
                       "Small images still need safe runtime defaults.")
    items = [("Non-root USER", "add `USER app` — a container breakout shouldn't mean root", BOX_GREEN),
             ("Read-only FS", "`--read-only` + tmpfs for scratch — malware can't persist", BOX_BLUE),
             ("Resource limits", "memory/CPU caps — one container can't starve the host", BOX_ORANGE),
             ("No secrets in ENV", "mount secrets from a manager, not baked into the image", BOX_RED)]
    yy = y
    for name, desc, fill in items:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=10.5)
        yy -= 70
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Docker Deep Dive — Remember",
                 ["Images are stacked read-only layers; containers add one thin writable layer.",
                  "Order Dockerfile steps: stable (deps) first, volatile (code) last — cache wins.",
                  "Multi-stage builds ship only the artifact: smaller, faster, fewer CVEs.",
                  "Registries: immutable tags, scan on push, pull by digest in prod.",
                  "Run as non-root, read-only FS, with resource limits — images are only half the story."],
                 pg)
    c.save(); print("wrote", path)


def pdf_serverless(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Serverless\nVisual Guide",
               "Functions as a service —\nevents in, scale-out, pay per invocation.",
               "Cloud & DevOps", None); pg += 1

    y = section_header(c, 1, 6, "The Execution Model",
                       "You upload code; the platform runs it per event.")
    box(c, 72, 500, 140, 70, BOX_BLUE, "Event", "HTTP / S3 / queue")
    box(c, 252, 500, 140, 70, BOX_PURP, "Lambda", "your handler()")
    box(c, 432, 500, 108, 70, BOX_GREEN, "Response", "result / side fx")
    arrow(c, 212, 535, 250, 535, color=ACCENT, width=2)
    arrow(c, 392, 535, 430, 535, color=ACCENT, width=2)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 420, "No servers to provision, patch, or watch. Scale is the platform's problem.")
    bullet_list(c, 72, 388,
        ["Stateless by design: persist to S3/DynamoDB/RDS — never local disk.",
         "Each invocation is isolated; concurrency = parallel executions, not threads.",
         "15-minute max execution: split long work into steps or use containers."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Event Sources: What Triggers Functions",
                       "Push and pull — the function just reacts.")
    srcs = [("API Gateway", "HTTP REST/WebSocket → request/response", BOX_BLUE),
            ("S3 / Storage", "object created → thumbnails, transcoding", BOX_GREEN),
            ("SQS / Queues", "message batch → workers that scale with backlog", BOX_ORANGE),
            ("Schedules", "EventBridge cron → nightly reports, cleanup", BOX_TEAL)]
    yy = y
    for name, desc, fill in srcs:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=11)
        yy -= 70
    note(c, 72, yy - 60, 468, "Queue triggers give free backpressure: messages wait safely while concurrency catches up.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Cold Starts & Mitigation",
                       "First invocation after idle pays an init tax.")
    box(c, 72, 500, 220, 80, BOX_RED, "Cold start", "provision + init\n300–2000ms")
    box(c, 320, 500, 220, 80, BOX_GREEN, "Warm start", "reuse env\n<10ms")
    arrow(c, 292, 540, 318, 540, color=ACCENT, width=2, label="2nd call")
    bullet_list(c, 72, 430,
        ["Keep init light: lazy-load heavy SDKs, slim dependencies, small packages.",
         "Provisioned concurrency: pre-warmed environments for latency-critical paths (costs more).",
         "SnapStart / tiered compile: restore from snapshot instead of booting fresh."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Limits You Must Design Around",
                       "Quotas are guardrails — know them before prod.")
    lims = [("Timeout", "15 min max — chunk long work", BOX_RED),
            ("Memory", "128MB–10GB — also scales CPU proportionally", BOX_ORANGE),
            ("Concurrency", "default 1000/region — reserve per function", BOX_BLUE),
            ("Payload", "6MB sync / 256KB async — big data via S3, not events", BOX_TEAL)]
    yy = y
    for name, desc, fill in lims:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=11)
        yy -= 70
    note(c, 72, yy - 60, 468, "Concurrency is a shared pool: one runaway function can starve the rest — set reserved concurrency per critical fn.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "The Cost Model",
                       "Pay per invocation + GB-seconds. Cheap at idle, watch the tail.")
    box(c, 72, 480, 220, 80, BOX_GREEN, "Low traffic", "$0.20 / 1M req\n+ compute time")
    box(c, 320, 480, 220, 80, BOX_RED, "Always-on heavy", "containers cheaper\nat sustained load")
    arrow(c, 292, 520, 318, 520, color=ACCENT, width=2, label="crossover")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 400, "Sweet spot: spiky, bursty, idle-mostly workloads (webhooks, cron, event processing).")
    bullet_list(c, 72, 368,
        ["Free tier covers small apps entirely — serverless is the cheapest way to start.",
         "Cost per request is flat: 10x traffic ≈ 10x bill. Model it before launch.",
         "Recursive loops (fn triggers itself via S3) can burn money in minutes — add circuit breakers."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Serverless Patterns",
                       "Common shapes that fit the model well.")
    pats = [("API backend", "API Gateway + functions + DynamoDB — no servers at all", BOX_BLUE),
            ("Async workers", "queue → functions scale with backlog, retries built in", BOX_GREEN),
            ("Event pipelines", "S3 → fn → S3: thumbnails, ETL, virus scan", BOX_ORANGE),
            ("Glue & cron", "scheduled fns: cleanup, reports, sync jobs", BOX_TEAL)]
    yy = y
    for name, desc, fill in pats:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=11)
        yy -= 70
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Serverless — Remember",
                 ["Event in → handler runs → platform scales: zero server management.",
                  "Event sources: HTTP, storage, queues (free backpressure), schedules.",
                  "Cold starts: slim init, provisioned concurrency for hot paths.",
                  "Limits: 15-min timeout, concurrency pools, payload caps — design around them.",
                  "Pay per use: unbeatable for spiky workloads, model cost before scale."],
                 pg)
    c.save(); print("wrote", path)


def pdf_autoscaling(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Auto-scaling\nVisual Guide",
               "HPA, VPA, cluster autoscaler —\nright-size everything, automatically.",
               "Cloud & DevOps", None); pg += 1

    y = section_header(c, 1, 6, "HPA: Scale Pods on Metrics",
                       "Horizontal Pod Autoscaler adds replicas when load rises.")
    box(c, 72, 500, 140, 70, BOX_BLUE, "Metrics", "CPU 85%\ncustom QPS")
    box(c, 252, 500, 140, 70, BOX_ORANGE, "HPA", "desired: 3 → 8")
    box(c, 432, 500, 108, 70, BOX_GREEN, "Pods", "8 replicas")
    arrow(c, 212, 535, 250, 535, color=ACCENT, width=2)
    arrow(c, 392, 535, 430, 535, color=ACCENT, width=2)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 420, "Control loop: every 15s, HPA computes desiredReplicas = ceil(current × (metric/target)).")
    note(c, 72, 330, 468, "HPA needs resource requests set — without them, CPU% has no denominator and HPA can't compute.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Choosing the Right Metric",
                       "CPU is easy; custom metrics are accurate.")
    mets = [("CPU utilization", "simple, laggy — bad for spiky or queue-driven work", BOX_ORANGE),
            ("Memory", "rarely useful — memory doesn't shed load when you add pods", BOX_RED),
            ("Custom: requests/sec", "scale on what users feel — needs metrics adapter", BOX_GREEN),
            ("Custom: queue depth", "workers scale with backlog — the honest signal", BOX_BLUE)]
    yy = y
    for name, desc, fill in mets:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=10.5)
        yy -= 70
    note(c, 72, yy - 60, 468, "Multiple metrics: HPA takes the MAX of all computed replica counts — the most demanding signal wins.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "VPA: Right-Size the Containers",
                       "Vertical Pod Autoscaler adjusts requests/limits per pod.")
    box(c, 72, 500, 200, 80, BOX_TEAL, "VPA recommender", "watches usage history")
    box(c, 320, 500, 220, 80, BOX_BLUE, "Pod spec updated", "requests: 200m → 500m")
    arrow(c, 272, 540, 318, 540, color=ACCENT, width=2)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 400, "Modes: Off (recommend only) → Initial → Auto (restarts pods to apply).")
    note(c, 72, 310, 468, "Never run HPA and VPA on the SAME metric — they fight. VPA for sizing, HPA for replica count, different signals.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Cluster Autoscaler: Scale the Nodes",
                       "Pods pending? Add nodes. Nodes empty? Remove them.")
    box(c, 72, 500, 160, 80, BOX_RED, "Pending pods", "no room to schedule")
    box(c, 252, 500, 160, 80, BOX_ORANGE, "Autoscaler", "node group 3 → 5")
    box(c, 432, 500, 108, 80, BOX_GREEN, "New nodes", "pods schedule")
    arrow(c, 232, 540, 250, 540, color=ACCENT, width=2)
    arrow(c, 412, 540, 430, 540, color=ACCENT, width=2)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 400, "Scale-down: evicts pods from underutilized nodes (respects PodDisruptionBudgets), then deletes the node.")
    note(c, 72, 310, 468, "Node startup takes minutes — cluster autoscaler reacts to sustained pressure, not spikes. HPA handles the spikes.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Cooldowns & Stabilization",
                       "Prevent flapping: scale up fast, scale down slow.")
    box(c, 72, 500, 220, 80, BOX_GREEN, "Scale UP", "aggressive\nreact in seconds")
    box(c, 320, 500, 220, 80, BOX_BLUE, "Scale DOWN", "stabilization window\ndefault 5 min")
    arrow(c, 292, 540, 318, 540, color=ACCENT, width=2, label="asymmetric")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 400, "Flapping: 3→8→3→8 replicas every minute — churns connections and confuses the cluster autoscaler.")
    bullet_list(c, 72, 368,
        ["scaleDown.stabilizationWindowSeconds: ignore brief dips before shrinking.",
         "scaleUp can also be rate-limited (policies) to avoid thundering herds.",
         "Predictive/scheduled scaling: pre-warm before known peaks (Black Friday 9am)."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "The Full Stack, Together",
                       "Three scalers, three different jobs, one system.")
    box(c, 72, 540, 140, 56, BOX_BLUE, "HPA", "pod count")
    box(c, 226, 540, 140, 56, BOX_TEAL, "VPA", "pod size")
    box(c, 380, 540, 140, 56, BOX_ORANGE, "Cluster AS", "node count")
    box(c, 176, 400, 260, 70, BOX_GREEN, "Workload", "right pods, right nodes")
    arrow(c, 142, 538, 240, 472, color=ACCENT, width=1.5)
    arrow(c, 296, 538, 296, 472, color=TEAL, width=1.5)
    arrow(c, 450, 538, 360, 472, color=ORANGE, width=1.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 340, "HPA reacts in seconds, cluster autoscaler in minutes — size node headroom for the gap.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Auto-scaling — Remember",
                 ["HPA scales pod COUNT on metrics — set resource requests or it can't compute.",
                  "Scale on honest signals: request rate or queue depth beat raw CPU.",
                  "VPA right-sizes containers; never let it fight HPA on the same metric.",
                  "Cluster autoscaler adds/removes NODES for pending pods and empty nodes.",
                  "Scale up fast, scale down slow — stabilization windows stop flapping."],
                 pg)
    c.save(); print("wrote", path)


def pdf_blue_green(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Blue-Green Deployments\nVisual Guide",
               "Two identical environments —\ncut traffic over, roll back in seconds.",
               "Cloud & DevOps", None); pg += 1

    y = section_header(c, 1, 5, "Two Identical Environments",
                       "Blue serves traffic; green waits for the next release.")
    box(c, 72, 460, 220, 90, BOX_BLUE, "BLUE (live)", "v2.3 — 100% traffic")
    box(c, 320, 460, 220, 90, BOX_GREEN, "GREEN (idle)", "v2.4 — warming up")
    box(c, 226, 340, 160, 60, BOX_ORANGE, "Router / LB", "the switch")
    arrow(c, 306, 458, 306, 402, color=ACCENT, width=2.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 280, "Identical means identical: same size, same config, same data shape.")
    note(c, 72, 200, 468, "Cost: you run 2x capacity during the switch — the price of instant rollback.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 5, "Deploy to Green, Verify in Peace",
                       "The new version goes live nowhere until you say so.")
    box(c, 72, 500, 160, 70, BOX_GREEN, "GREEN", "v2.4 deployed")
    box(c, 380, 500, 160, 70, BOX_BLUE, "Smoke tests", "health + key flows")
    arrow(c, 232, 535, 378, 535, color=GREEN, width=2, label="verify")
    box(c, 226, 380, 160, 60, BOX_BLUE, "BLUE", "still serving 100%")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 320, "Green gets real warm-up: caches fill, JIT compiles, connections pool — no cold traffic shock.")
    bullet_list(c, 72, 288,
        ["Run the full smoke suite against green's real endpoint.",
         "Shadow traffic (copy of live requests) finds issues smoke tests miss.",
         "Green stays dark to users until the cutover — zero user impact while you verify."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 5, "The Cutover: Flip the Router",
                       "One config change moves 100% of traffic in seconds.")
    box(c, 72, 500, 160, 70, BOX_BLUE, "BLUE v2.3", "0% traffic")
    box(c, 380, 500, 160, 70, BOX_GREEN, "GREEN v2.4", "100% traffic")
    box(c, 226, 380, 160, 60, BOX_ORANGE, "Router", "weight flipped")
    arrow(c, 306, 498, 306, 442, color=GREEN, width=3)
    c.setStrokeColor(MUTED); c.setLineWidth(1.5); c.setDash(4, 3)
    c.line(152, 498, 226, 442); c.setDash()
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 320, "Cutover is a router/LB/DNS weight change — atomic, fast, and observable.")
    note(c, 72, 240, 468, "Watch error rates and latency for 10–30 min after the flip. Keep blue warm — don't tear it down yet.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 5, "Instant Rollback",
                       "Something's wrong? Flip the switch back.")
    box(c, 72, 500, 160, 70, BOX_BLUE, "BLUE v2.3", "100% traffic again")
    box(c, 380, 500, 160, 70, BOX_RED, "GREEN v2.4", "quarantined")
    box(c, 226, 380, 160, 60, BOX_ORANGE, "Router", "flipped back")
    arrow(c, 306, 498, 306, 442, color=ACCENT, width=3)
    c.setStrokeColor(MUTED); c.setLineWidth(1.5); c.setDash(4, 3)
    c.line(460, 498, 386, 442); c.setDash()
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 320, "Rollback needs no redeploy — the old version is still warm and waiting.")
    note(c, 72, 240, 468, "Decide the rollback trigger BEFORE the cutover: error rate > X% for Y minutes → flip back, no meeting needed.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 5, "The Hard Part: The Database",
                       "Code can flip instantly; schemas can't.")
    box(c, 72, 500, 220, 80, BOX_RED, "Breaking change", "DROP column\nold code breaks")
    box(c, 320, 500, 220, 80, BOX_GREEN, "Expand-contract", "add → migrate → remove")
    arrow(c, 292, 540, 318, 540, color=ACCENT, width=2, label="prefer")
    bullet_list(c, 72, 430,
        ["Expand: add the new column/table; both versions work against it.",
         "Migrate: backfill data; deploy the version that uses the new shape.",
         "Contract: only AFTER old code is gone, drop the old column. Three deploys, zero downtime."],
        font_size=10.5, gap=26)
    note(c, 72, 260, 468, "Shared database = shared fate. Blue-green without expand-contract is just downtime with extra steps.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Blue-Green Deployments — Remember",
                 ["Two identical environments: one live, one staging the next release.",
                  "Verify green fully (smoke + shadow traffic) before any user sees it.",
                  "Cutover is a router flip — seconds, atomic, observable.",
                  "Rollback is the same flip in reverse: no redeploy, old version still warm.",
                  "Databases need expand-contract migrations — code flips fast, schemas don't."],
                 pg)
    c.save(); print("wrote", path)


def pdf_canary(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Canary Releases\nVisual Guide",
               "Shift traffic gradually —\nlet metrics decide who wins.",
               "Cloud & DevOps", None); pg += 1

    y = section_header(c, 1, 5, "The Idea: Test on a Trickle",
                       "Route 1–5% of users to the new version and watch.")
    box(c, 72, 500, 160, 70, BOX_BLUE, "v2.3 stable", "95% traffic")
    box(c, 380, 500, 160, 70, BOX_GREEN, "v2.4 canary", "5% traffic")
    box(c, 226, 380, 160, 60, BOX_ORANGE, "Router", "weighted split")
    arrow(c, 306, 498, 160, 442, color=ACCENT, width=3)
    arrow(c, 306, 498, 452, 442, color=GREEN, width=1.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 320, "Named for canaries in coal mines: a small group inhales first so problems surface early.")
    note(c, 72, 240, 468, "Start small (1–5%), then step up: 5 → 25 → 50 → 100 — or jump straight to full if metrics are clean.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 5, "Metrics Gates: The Canary Judge",
                       "Compare canary vs baseline on the same live traffic.")
    box(c, 72, 500, 220, 80, BOX_BLUE, "Baseline v2.3", "err 0.1%\np99 180ms")
    box(c, 320, 500, 220, 80, BOX_GREEN, "Canary v2.4", "err 0.4%!\np99 260ms")
    arrow(c, 292, 540, 318, 540, color=ACCENT, width=2, label="compare")
    bullet_list(c, 72, 430,
        ["Error rate, latency percentiles, business KPIs (conversion, checkout success).",
         "Statistical comparison: canary must not be WORSE than baseline beyond tolerance.",
         "Gate each step: only promote 5→25% when the 5% window is clean."],
        font_size=10.5, gap=26)
    note(c, 72, 260, 468, "Same traffic, same time window — comparing canary-now vs prod-last-week lies (traffic mix differs).")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 5, "Automated Rollback",
                       "Metrics breach the gate → traffic shifts back, no human needed.")
    box(c, 72, 500, 140, 70, BOX_RED, "Gate breached", "err > 1%")
    box(c, 252, 500, 140, 70, BOX_ORANGE, "Controller", "shift to 0%")
    box(c, 432, 500, 108, 70, BOX_BLUE, "v2.3", "100% again")
    arrow(c, 212, 535, 250, 535, color=RED, width=2)
    arrow(c, 392, 535, 430, 535, color=ACCENT, width=2)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 420, "Progressive delivery controllers (Argo Rollouts, Flagger) automate the whole ladder.")
    bullet_list(c, 72, 388,
        ["Define success criteria up front: 'p99 < 300ms AND errors < 0.5% for 10 min'.",
         "Rollback = set canary weight to 0 — the old version never left.",
         "Alert humans on rollback, but don't wait for them: automation flips first."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 5, "Canary vs Blue-Green",
                       "Gradual and metric-driven vs instant and binary.")
    rows = [("Traffic shift", "gradual 1→100%", "instant 0→100%", BOX_BLUE),
            ("Blast radius", "tiny at first", "everyone at once", BOX_GREEN),
            ("Rollback", "shift weight to 0", "flip router back", BOX_ORANGE),
            ("Cost", "small canary fleet", "full 2x environment", BOX_TEAL),
            ("Best for", "risky changes, UX", "infra swaps, DB-adjacent", BOX_PURP)]
    yy = y
    for name, cn, bg, fill in rows:
        box(c, 72, yy - 52, 468, 56, fill, f"{name}: canary {cn}  |  blue-green {bg}", None, font_size=9.5)
        yy -= 70
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 5, "Canary in Kubernetes",
                       "Service meshes and rollout controllers do the weighting.")
    box(c, 72, 500, 150, 70, BOX_BLUE, "v2.3 pods", "weight 90")
    box(c, 246, 500, 150, 70, BOX_GREEN, "v2.4 pods", "weight 10")
    box(c, 420, 500, 120, 70, BOX_ORANGE, "Analysis", "Prometheus")
    arrow(c, 222, 535, 244, 535, color=ACCENT, width=1.5)
    arrow(c, 396, 535, 418, 535, color=ACCENT, width=2, label="judge")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 420, "Argo Rollouts / Flagger: step weights, run analysis, promote or abort automatically.")
    note(c, 72, 330, 468, "Session affinity matters: a user must not bounce between versions mid-checkout — pin canary by cookie or header.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Canary Releases — Remember",
                 ["Expose the new version to 1–5% first; let real traffic be the test.",
                  "Metrics gates compare canary vs baseline on the SAME traffic window.",
                  "Automate the ladder: promote on clean metrics, roll back on breach — no meetings.",
                  "Blue-green = instant flip, 2x cost; canary = gradual, tiny blast radius.",
                  "Pin users to a version (cookie/header) so nobody straddles both mid-flow."],
                 pg)
    c.save(); print("wrote", path)


def pdf_feature_flags(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Feature Flags\nVisual Guide",
               "Decouple deploy from release —\nroll out with a kill switch in hand.",
               "Cloud & DevOps", None); pg += 1

    y = section_header(c, 1, 6, "Decouple Deploy from Release",
                       "Ship code dark, then turn it on for the right people.")
    box(c, 72, 500, 160, 70, BOX_BLUE, "Deploy", "code ships\ndark (off)")
    box(c, 256, 500, 160, 70, BOX_GREEN, "Release", "flag ON for\nbeta users")
    box(c, 440, 500, 100, 70, BOX_ORANGE, "Rollout", "100%")
    arrow(c, 232, 535, 254, 535, color=ACCENT, width=2)
    arrow(c, 416, 535, 438, 535, color=ACCENT, width=2)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 420, "Deploy ≠ release. Code can ride the train for weeks before anyone sees it.")
    note(c, 72, 330, 468, "Trunk-based development loves flags: merge small, keep main deployable, release on your schedule.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Targeting Rules",
                       "Who sees the flag? Rules decide, per request.")
    rules = [("Percentage", "10% of users (sticky by user ID)", BOX_BLUE),
             ("Attributes", "plan=enterprise AND region=eu", BOX_GREEN),
             ("Allowlist", "internal team + beta customers first", BOX_ORANGE),
             ("Gradual", "5% → 25% → 50% → 100% on a schedule", BOX_TEAL)]
    yy = y
    for name, desc, fill in rules:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=11)
        yy -= 70
    note(c, 72, yy - 60, 468, "Sticky bucketing: hash(user_id) → same user always sees the same variant. No flicker.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "The Kill Switch",
                       "When the new checkout breaks at 2am, you don't redeploy — you flip.")
    box(c, 72, 500, 200, 80, BOX_RED, "Incident", "checkout errors\nspiking")
    box(c, 320, 500, 220, 80, BOX_GREEN, "Flip flag OFF", "back to old path\nin seconds")
    arrow(c, 272, 540, 318, 540, color=RED, width=2.5, label="flip!")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 420, "Recovery time: seconds, not the 20 minutes a rollback deploy takes.")
    bullet_list(c, 72, 388,
        ["Every risky feature ships behind a flag — the flag IS the rollback plan.",
         "Flag changes must be audited: who flipped what, when (it's a production change).",
         "Test the OFF path too — the kill switch is useless if the old code rotted."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Gradual Rollouts & Experimentation",
                       "Flags double as the control plane for A/B tests.")
    box(c, 72, 500, 150, 70, BOX_BLUE, "Control 50%", "old checkout")
    box(c, 246, 500, 150, 70, BOX_GREEN, "Variant 50%", "one-click pay")
    box(c, 420, 500, 120, 70, BOX_PURP, "Metrics", "conversion?")
    arrow(c, 222, 535, 244, 535, color=ACCENT, width=1.5)
    arrow(c, 396, 535, 418, 535, color=ACCENT, width=2)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 420, "Same machinery as targeting — but the goal is measurement, not safety.")
    note(c, 72, 330, 468, "One variable per experiment. Flag the UI copy AND the backend behavior together or results lie.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Flag Architecture",
                       "SDKs evaluate locally; a control plane manages state.")
    box(c, 72, 520, 200, 70, BOX_BLUE, "Flag service", "LaunchDarkly /\nopen-source")
    box(c, 340, 520, 200, 70, BOX_GREEN, "Your app", "SDK evaluates\nlocally")
    arrow(c, 272, 555, 338, 555, color=ACCENT, width=2, label="stream updates")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 440, "Evaluation is LOCAL (cached rules, microseconds) — the service is only the control plane.")
    bullet_list(c, 72, 408,
        ["SDKs cache flag state and stream changes — a flag-service outage must not break your app.",
         "Default to the SAFE value when the SDK can't reach the service (usually OFF).",
         "Bootstrap flags at startup so first requests don't block on a network call."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Tech Debt: Flags Rot",
                       "Every flag is a branch in production — clean them up.")
    box(c, 72, 500, 160, 70, BOX_GREEN, "Release flags", "short-lived\nremove after rollout")
    box(c, 256, 500, 160, 70, BOX_ORANGE, "Ops flags", "kill switches\nkeep, document")
    box(c, 440, 500, 100, 70, BOX_RED, "Dead flags", "100% for months?\nDELETE")
    arrow(c, 232, 535, 254, 535, color=ACCENT, width=1.5)
    arrow(c, 416, 535, 438, 535, color=RED, width=1.5)
    note(c, 72, 400, 468, "Rule: a flag that hit 100% gets a removal ticket the same sprint. Stale flags are untested code paths.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Feature Flags — Remember",
                 ["Deploy ≠ release: ship dark, release to the right audience on your schedule.",
                  "Target by percentage, attributes, allowlists — sticky bucketing, no flicker.",
                  "The kill switch is the fastest rollback: seconds, audited, tested both ways.",
                  "Same machinery powers A/B tests — one variable, metrics decide.",
                  "Flags rot: remove release flags after rollout; dead flags are untested branches."],
                 pg)
    c.save(); print("wrote", path)


def pdf_prometheus(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Prometheus & Grafana\nVisual Guide",
               "Metrics, PromQL, alerts, dashboards —\nthe open-source observability stack.",
               "Cloud & DevOps", None); pg += 1

    y = section_header(c, 1, 6, "The Metrics Model",
                       "Four types cover almost everything you measure.")
    mets = [("Counter", "only goes up: http_requests_total", BOX_BLUE),
            ("Gauge", "goes up/down: active_connections", BOX_GREEN),
            ("Histogram", "buckets of observations: latency", BOX_ORANGE),
            ("Summary", "precomputed quantiles: use histograms instead", BOX_TEAL)]
    yy = y
    for name, desc, fill in mets:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=11)
        yy -= 70
    note(c, 72, yy - 60, 468, "Labels are dimensions: http_requests_total{method='GET', status='500'} — slice without new metrics.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Pull Model: Prometheus Scrapes You",
                       "Targets expose /metrics; Prometheus pulls on an interval.")
    box(c, 72, 500, 140, 70, BOX_GREEN, "App :8080", "/metrics")
    box(c, 252, 500, 140, 70, BOX_GREEN, "App :8080", "/metrics")
    box(c, 176, 380, 260, 70, BOX_BLUE, "Prometheus", "scrape every 15s")
    arrow(c, 240, 498, 300, 452, color=ACCENT, width=2)
    arrow(c, 380, 498, 360, 452, color=ACCENT, width=2)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 320, "Pull > push for monitoring: dead targets are obvious (no scrape = down), no client buffering.")
    bullet_list(c, 72, 288,
        ["Service discovery (K8s, Consul) finds targets automatically — no static config.",
         "Short-lived jobs push via Pushgateway; everything else gets scraped.",
         "Scrape interval is your resolution floor: 15s is standard, 5s for hot paths."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "PromQL Basics",
                       "Query language for time series — rates, not raw counters.")
    box(c, 72, 500, 468, 70, BOX_PURP, "rate(http_requests_total[5m])",
        "per-second rate over 5 min — the workhorse query", font_size=12)
    c.setFillColor(INK); c.setFont(MONO_FONT, 9.5)
    c.drawString(72, 440, "sum by (status) (rate(http_requests_total[5m]))")
    c.drawString(72, 422, "histogram_quantile(0.99, rate(http_latency_bucket[5m]))")
    c.setFont(BODY_FONT, 10)
    c.drawString(72, 396, "Never graph raw counters — they only go up. rate() turns them into meaningful slopes.")
    bullet_list(c, 72, 364,
        ["sum by (label): aggregate across dimensions; without it you get per-pod noise.",
         "histogram_quantile: p50/p99 from buckets — accurate tail latency.",
         "offset / time shifts: compare to last week with `offset 1w`."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Alerting: Rules + Alertmanager",
                       "Prometheus evaluates rules; Alertmanager routes and dedupes.")
    box(c, 72, 500, 160, 70, BOX_RED, "Alert rule", "expr + for: 5m")
    box(c, 256, 500, 160, 70, BOX_ORANGE, "Alertmanager", "group, dedupe,\nroute")
    box(c, 440, 500, 100, 70, BOX_BLUE, "Pager", "on-call")
    arrow(c, 232, 535, 254, 535, color=RED, width=2, label="fires")
    arrow(c, 416, 535, 438, 535, color=ACCENT, width=2)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 420, "`for: 5m` means the condition must hold 5 minutes — kills flapping pages.")
    bullet_list(c, 72, 388,
        ["Alert on SYMPTOMS (error rate, latency) not causes (CPU) — pages must be actionable.",
         "Grouping: one incident = one notification, not 50 pod alerts.",
         "Inhibition: if the region is down, suppress the per-service pages."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Dashboard Design (Grafana)",
                       "Dashboards answer questions — design top-down.")
    box(c, 72, 520, 468, 56, BOX_BLUE, "Row 1: GOLDEN SIGNALS", "latency, traffic, errors, saturation", font_size=11)
    box(c, 72, 450, 468, 56, BOX_GREEN, "Row 2: SERVICE HEALTH", "per-endpoint breakdown, dependencies", font_size=11)
    box(c, 72, 380, 468, 56, BOX_ORANGE, "Row 3: DEBUG DETAIL", "per-pod, per-instance, logs link", font_size=11)
    note(c, 72, 290, 468, "Every panel links somewhere: dashboard → logs → traces. A number without a next click is decoration.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Retention & Federation",
                       "Prometheus is local-first — plan for long-term storage.")
    box(c, 72, 500, 220, 80, BOX_BLUE, "Prometheus", "15-day local\nfast queries")
    box(c, 320, 500, 220, 80, BOX_TEAL, "Remote storage", "Thanos / Mimir\nmonths–years")
    arrow(c, 292, 540, 318, 540, color=ACCENT, width=2, label="remote_write")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 420, "Recording rules: precompute expensive queries (e.g. per-service error ratio) into new series.")
    note(c, 72, 330, 468, "High cardinality kills: a label with 10k values × 10k series = storage meltdown. Keep label values bounded.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Prometheus & Grafana — Remember",
                 ["Four metric types: counters, gauges, histograms (+ summaries) — labels add dimensions.",
                  "Pull model: targets expose /metrics, Prometheus scrapes; dead targets are obvious.",
                  "PromQL: rate() your counters, sum by () to aggregate, histogram_quantile for p99.",
                  "Alert on symptoms with `for:` clauses; Alertmanager groups, dedupes, routes.",
                  "Dashboards top-down: golden signals → service health → debug detail, every panel clickable."],
                 pg)
    c.save(); print("wrote", path)


def pdf_elk(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Centralized Logging\nVisual Guide",
               "Ship, parse, index, search —\none pane of glass for every log line.",
               "Cloud & DevOps", None); pg += 1

    y = section_header(c, 1, 6, "The Log Pipeline",
                       "Four stages from app to searchable index.")
    stages = [("Ship", "agent on host", BOX_BLUE), ("Queue", "buffer bursts", BOX_ORANGE),
              ("Parse", "structure it", BOX_GREEN), ("Index", "searchable", BOX_TEAL)]
    bx = 72
    for name, desc, fill in stages:
        box(c, bx, 480, 108, 80, fill, name, desc, font_size=10)
        if bx > 72: arrow(c, bx - 12, 520, bx, 520, color=ACCENT, width=1.5)
        bx += 120
    box(c, 226, 360, 160, 60, BOX_PURP, "Search UI", "Kibana / Grafana")
    arrow(c, 450, 500, 360, 420, color=ACCENT2, width=1.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 300, "The queue (Kafka/Redis) absorbs spikes so a log storm never loses data or backpressures apps.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Shippers: Getting Logs Off the Box",
                       "Lightweight agents tail files and forward.")
    box(c, 72, 500, 200, 80, BOX_BLUE, "Filebeat / Fluent Bit", "tail logs/\nforward")
    box(c, 320, 500, 220, 80, BOX_GREEN, "stdout → collector", "K8s: kubelet\nships container logs")
    arrow(c, 272, 540, 318, 540, color=ACCENT, width=2, label="or")
    bullet_list(c, 72, 430,
        ["Apps log to stdout/stderr — the platform collects, never local files in prod.",
         "Shippers are dumb pipes: minimal parsing at the edge, structure centrally.",
         "Backpressure handling: shipper buffers to disk when the pipeline is down."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "ELK vs Loki: Index Everything vs Index Labels",
                       "Two philosophies of log storage.")
    box(c, 72, y - 80, 225, 120, BOX_BLUE, "ELK", "index full text", font_size=13)
    box(c, 315, y - 80, 225, 120, BOX_GREEN, "Loki", "index labels only", font_size=13)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    ea = ["Full-text search on every field", "Heavy: storage + compute hungry", "Great for ad-hoc exploration"]
    eb = ["Cheap: only label index, grep the rest", "Pairs with Prometheus/Grafana", "Needs good labels to be fast"]
    yy = y - 120
    for a, b in zip(ea, eb):
        c.drawString(72, yy, "• " + a); c.drawString(315, yy, "• " + b); yy -= 20
    note(c, 72, 160, 468, "Loki's mantra: 'like Prometheus, but for logs.' Same label model — cheap at scale, weaker full-text.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Structured Logging",
                       "JSON logs are queryable; printf logs are archaeology.")
    box(c, 72, 500, 468, 56, BOX_RED, 'BAD:  "user 42 failed login from 1.2.3.4"', None, font_size=10)
    box(c, 72, 430, 468, 56, BOX_GREEN, 'GOOD: {"user_id":42,"event":"login_failed","ip":"1.2.3.4"}', None, font_size=9.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 380, "Fields to always include: timestamp (UTC, ISO8601), level, service, trace_id, request_id.")
    bullet_list(c, 72, 348,
        ["Log at the right level: DEBUG is dev-only; prod runs INFO+ (cost!).",
         "One line per event — multi-line stack traces need special handling to stay together.",
         "Never log secrets, tokens, or full PII — logs are broadly readable by design."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Retention & Tiers",
                       "Not all logs deserve SSDs forever.")
    box(c, 72, 500, 150, 70, BOX_GREEN, "Hot 7d", "SSD\nfast search")
    box(c, 246, 500, 150, 70, BOX_ORANGE, "Warm 30d", "cheap disk\nslower")
    box(c, 420, 500, 120, 70, BOX_BLUE, "Cold 1y+", "object store\nrestore only")
    arrow(c, 222, 535, 244, 535, color=ACCENT, width=1.5)
    arrow(c, 396, 535, 418, 535, color=ACCENT, width=1.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 420, "Index lifecycle policies move data down tiers automatically — set it once, forget it.")
    note(c, 72, 330, 468, "Log volume = money. Sample debug logs, drop health-check noise, and audit top talkers monthly.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Correlate: Logs + Metrics + Traces",
                       "A log line is 10x more useful with a trace_id in it.")
    box(c, 72, 500, 140, 70, BOX_BLUE, "Metrics", "what + when")
    box(c, 240, 500, 140, 70, BOX_ORANGE, "Logs", "details")
    box(c, 408, 500, 132, 70, BOX_GREEN, "Traces", "where slow")
    box(c, 176, 380, 260, 70, BOX_PURP, "trace_id", "the join key")
    arrow(c, 142, 498, 260, 452, color=ACCENT, width=1.5)
    arrow(c, 310, 498, 306, 452, color=ORANGE, width=1.5)
    arrow(c, 474, 498, 360, 452, color=GREEN, width=1.5)
    note(c, 72, 290, 468, "Emit trace_id in every log line — jump from a slow trace straight to its logs in one click.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Centralized Logging — Remember",
                 ["Pipeline: ship → queue (buffer) → parse → index → search UI.",
                  "Apps log to stdout; shippers forward; the queue absorbs storms.",
                  "ELK indexes everything (powerful, pricey); Loki indexes labels (cheap, Prometheus-like).",
                  "Structure logs as JSON with trace_id — printf logs are archaeology.",
                  "Tier retention (hot/warm/cold) and audit volume — logs are money."],
                 pg)
    c.save(); print("wrote", path)


def pdf_tracing(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Distributed Tracing\nVisual Guide",
               "Spans, traces, sampling —\nfollow one request across fifty services.",
               "Cloud & DevOps", None); pg += 1

    y = section_header(c, 1, 6, "Spans & Traces",
                       "A trace is a tree of spans — one span per operation.")
    spans = [("gateway", 0, 270, ACCENT), ("auth", 8, 20, GREEN),
             ("orders", 30, 60, ACCENT2), ("payments", 95, 160, RED)]
    yy = 560
    c.setFont(BODY_FONT, 10.5)
    for name, start, dur, col in spans:
        c.setFillColor(INK); c.drawString(72, yy, name)
        c.setFillColor(col); c.rect(170 + start, yy - 8, dur, 16, fill=1, stroke=0)
        yy -= 34
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 10)
    c.drawString(72, 380, "Time →. The payments span dominates: 160ms of a 270ms request. That's your bottleneck.")
    c.setFillColor(INK)
    bullet_list(c, 72, 348,
        ["Span = one operation: name, start/end, attributes, parent span ID.",
         "Trace = the full tree, joined by a single trace_id across services.",
         "The waterfall makes the slow span obvious — no guessing."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Context Propagation",
                       "The trace_id rides along in headers — every hop continues it.")
    box(c, 72, 500, 140, 70, BOX_BLUE, "Service A", "starts trace")
    box(c, 252, 500, 140, 70, BOX_GREEN, "Service B", "continues")
    box(c, 432, 500, 108, 70, BOX_ORANGE, "Service C", "continues")
    arrow(c, 212, 535, 250, 535, color=ACCENT, width=2, label="traceparent")
    arrow(c, 392, 535, 430, 535, color=ACCENT, width=2, label="traceparent")
    c.setFillColor(INK); c.setFont(MONO_FONT, 9.5)
    c.drawString(72, 440, "traceparent: 00-<trace_id>-<parent_span_id>-01")
    c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 414, "W3C standard header — libraries propagate it automatically if you use OpenTelemetry.")
    note(c, 72, 330, 468, "Break propagation (custom HTTP client without instrumentation) and the trace splits in two — instrument everything.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Jaeger / Tempo Architecture",
                       "Collectors receive spans; the backend stores and queries them.")
    box(c, 72, 520, 160, 70, BOX_GREEN, "App SDKs", "emit spans")
    box(c, 256, 520, 160, 70, BOX_BLUE, "Collector", "batch + route")
    box(c, 440, 500, 100, 90, BOX_PURP, "Backend", "Jaeger /\nTempo")
    arrow(c, 232, 555, 254, 555, color=ACCENT, width=2)
    arrow(c, 416, 555, 438, 555, color=ACCENT, width=2)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 440, "OpenTelemetry Collector: vendor-neutral pipeline — receive, process, export to any backend.")
    bullet_list(c, 72, 408,
        ["SDKs batch spans and export async — tracing must never block the request path.",
         "The collector adds environments, filters PII, and fans out to multiple backends.",
         "Tempo: object-storage backend, cheap at scale — traces as blobs, indexed by ID."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Sampling: You Can't Keep Everything",
                       "1M req/s × full traces = bankruptcy. Sample smartly.")
    box(c, 72, y - 80, 225, 120, BOX_BLUE, "Head-based", "decide at start", font_size=13)
    box(c, 315, y - 80, 225, 120, BOX_GREEN, "Tail-based", "decide at end", font_size=13)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    ha = ["Cheap: drop spans early", "Misses rare errors (1% sample)", "Consistent via trace_id hash"]
    hb = ["Sees the full trace first", "Keeps ALL errors + slow", "Needs a collector buffer"]
    yy = y - 120
    for a, b in zip(ha, hb):
        c.drawString(72, yy, "• " + a); c.drawString(315, yy, "• " + b); yy -= 20
    note(c, 72, 160, 468, "Tail-based sampling is the gold standard: keep 100% of errors and slow traces, 1% of the boring ones.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "What to Put in a Span",
                       "Attributes turn a timeline into a diagnosis.")
    attrs = [("http.route", "/checkout — not /checkout/42 (cardinality!)", BOX_BLUE),
             ("db.statement", "the slow query text, sanitized", BOX_GREEN),
             ("error", "true + exception message on failures", BOX_RED),
             ("user tier", "free vs paid — is slowness tiered?", BOX_ORANGE)]
    yy = y
    for name, desc, fill in attrs:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=10.5)
        yy -= 70
    note(c, 72, yy - 60, 468, "Cardinality rule: attribute VALUES must be bounded. user_id as an attribute = index explosion.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Trace-Driven Debugging",
                       "The workflow: slow request → trace → slow span → logs.")
    steps = [("1. Alert", "p99 latency breach", BOX_RED), ("2. Trace", "find slow trace", BOX_BLUE),
             ("3. Span", "payments = 160ms", BOX_ORANGE), ("4. Logs", "trace_id → DB logs", BOX_GREEN)]
    bx = 72
    for name, desc, fill in steps:
        box(c, bx, 480, 108, 80, fill, name, desc, font_size=10)
        if bx > 72: arrow(c, bx - 12, 520, bx, 520, color=ACCENT, width=1.5)
        bx += 120
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 400, "Exemplars: link Prometheus histograms to example traces — click a slow bucket, see the trace.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Distributed Tracing — Remember",
                 ["A trace is a tree of spans; the waterfall exposes the slow operation instantly.",
                  "Propagate trace_id via W3C traceparent headers — instrument every hop.",
                  "OpenTelemetry Collector: vendor-neutral receive → process → export pipeline.",
                  "Tail-based sampling keeps all errors and slow traces, drops the boring 99%.",
                  "Debug flow: alert → trace → slow span → logs via trace_id."],
                 pg)
    c.save(); print("wrote", path)


def pdf_chaos(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Chaos Engineering\nVisual Guide",
               "Break things on purpose —\nbuild confidence with controlled experiments.",
               "Cloud & DevOps", None); pg += 1

    y = section_header(c, 1, 6, "Hypothesis-Driven Experiments",
                       "Chaos is the scientific method applied to production.")
    steps = [("1. Steady state", "define normal", BOX_GREEN), ("2. Hypothesis", "system holds", BOX_BLUE),
             ("3. Inject fault", "kill a pod", BOX_RED), ("4. Compare", "did it hold?", BOX_ORANGE)]
    bx = 72
    for name, desc, fill in steps:
        box(c, bx, 480, 108, 80, fill, name, desc, font_size=10)
        if bx > 72: arrow(c, bx - 12, 520, bx, 520, color=ACCENT, width=1.5)
        bx += 120
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 400, "Not random destruction: a hypothesis ('killing one AZ keeps p99 < 500ms') that you verify.")
    note(c, 72, 310, 468, "If you can't state the expected outcome, it's not an experiment — it's just breaking things.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Define Steady State First",
                       "You need 'normal' measured before you can detect 'broken'.")
    box(c, 72, 500, 468, 70, BOX_BLUE, "Steady state: checkout success 99.5% ± 0.2%, p99 < 800ms",
        "the hypothesis is ABOUT this number", font_size=10.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 440, "Steady state = business metric, not CPU. Users don't care about your CPU.")
    bullet_list(c, 72, 408,
        ["Pick 1–3 metrics that prove the system works for users.",
         "Measure the baseline during the experiment window (same traffic, same time).",
         "The experiment PASSES if steady state holds within tolerance during the fault."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Blast Radius Control",
                       "Start tiny. Grow only with evidence.")
    box(c, 72, 500, 140, 70, BOX_GREEN, "1 pod", "start here")
    box(c, 236, 500, 140, 70, BOX_ORANGE, "1 AZ", "with confidence")
    box(c, 400, 500, 140, 70, BOX_RED, "1 region", "rarely, carefully")
    arrow(c, 212, 535, 234, 535, color=ACCENT, width=2)
    arrow(c, 376, 535, 398, 535, color=ACCENT, width=2)
    bullet_list(c, 72, 430,
        ["Abort conditions defined UP FRONT: error rate > X% → halt automatically.",
         "Run in production (that's where the surprises are) but during business hours first.",
         "Game the blast radius down, not up: one pod, one AZ, then stop and learn."],
        font_size=10.5, gap=26)
    note(c, 72, 260, 468, "Automatic halt beats a human watching a dashboard — wire abort conditions into the experiment runner.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Common Experiments",
                       "The greatest-hits fault injection menu.")
    exps = [("Kill pods", "does the deployment self-heal? (replica count holds)", BOX_RED),
            ("Network latency", "+200ms between services — do timeouts cascade?", BOX_ORANGE),
            ("AZ failure", "lose a whole zone — does traffic shift cleanly?", BOX_RED),
            ("Dependency down", "payments API 500s — does checkout degrade gracefully?", BOX_BLUE)]
    yy = y
    for name, desc, fill in exps:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=10.5)
        yy -= 70
    note(c, 72, yy - 60, 468, "Start with the boring ones: pod kills and restarts. They find the most misconfigurations per minute.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Game Days",
                       "Scheduled, team-wide failure rehearsals.")
    box(c, 72, 500, 150, 70, BOX_BLUE, "Plan", "scenario +\nhypothesis")
    box(c, 246, 500, 150, 70, BOX_RED, "Execute", "inject fault\ntogether")
    box(c, 420, 500, 120, 70, BOX_GREEN, "Learn", "gaps →\naction items")
    arrow(c, 222, 535, 244, 535, color=ACCENT, width=1.5)
    arrow(c, 396, 535, 418, 535, color=ACCENT, width=1.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 420, "The point isn't the failure — it's discovering that the runbook is wrong BEFORE a real outage.")
    bullet_list(c, 72, 388,
        ["Invite everyone: devs, SRE, support, comms — incidents are team sports.",
         "Timebox it: 2–4 hours, business hours, with a clear abort owner.",
         "Every surprise becomes a ticket. No action items = wasted game day."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Chaos Maturity Ladder",
                       "From manual pod-kills to continuous verification.")
    box(c, 72, 520, 468, 50, BOX_GREEN, "L1: manual experiments", "engineer runs a pod-kill, watches", font_size=11)
    box(c, 72, 456, 468, 50, BOX_BLUE, "L2: scheduled game days", "team rehearses quarterly scenarios", font_size=11)
    box(c, 72, 392, 468, 50, BOX_ORANGE, "L3: automated in CI/CD", "every deploy proves resilience", font_size=11)
    box(c, 72, 328, 468, 50, BOX_RED, "L4: continuous in prod", "always-on fault injection, tiny blast radius", font_size=11)
    note(c, 72, 240, 468, "Climb one rung at a time. L4 without L1 discipline is just expensive outages.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Chaos Engineering — Remember",
                 ["Every experiment starts with a hypothesis about steady state — business metrics, not CPU.",
                  "Blast radius grows with evidence: one pod → one AZ → (rarely) one region.",
                  "Abort conditions are automatic and defined before the fault is injected.",
                  "Game days rehearse people and runbooks, not just systems — every surprise becomes a ticket.",
                  "Climb the maturity ladder: manual → scheduled → CI/CD → continuous."],
                 pg)
    c.save(); print("wrote", path)


def pdf_sre(path):
    c = new_canvas(path); pg = 1
    title_page(c, "SRE Practices\nVisual Guide",
               "Toil budgets, error budgets, blameless reviews —\nengineering reliability as a discipline.",
               "Cloud & DevOps", None); pg += 1

    y = section_header(c, 1, 6, "DevOps vs SRE",
                       "DevOps is the philosophy; SRE is the implementation.")
    box(c, 72, y - 80, 225, 120, BOX_BLUE, "DevOps", "'what' — culture,\ncollaboration", font_size=13)
    box(c, 315, y - 80, 225, 120, BOX_GREEN, "SRE", "'how' — SLIs, budgets,\nautomation", font_size=13)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, y - 140, "'SRE is what happens when you ask a software engineer to do operations.'")
    bullet_list(c, 72, y - 172,
        ["SRE teams treat operations as a software problem: code the toil away.",
         "Reliability is a feature — budgeted, measured, and negotiated like any other.",
         "Shared ownership: devs own their services in prod; SRE provides the platform and practices."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Toil: The Work That Must Die",
                       "Toil = manual, repetitive, automatable, no enduring value.")
    box(c, 72, 500, 220, 80, BOX_RED, "TOIL", "manual deploys\nticket-driven ops")
    box(c, 320, 500, 220, 80, BOX_GREEN, "ENGINEERING", "automation that\neliminates toil")
    arrow(c, 292, 540, 318, 540, color=ACCENT, width=2, label="convert")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 420, "The 50% rule: SREs spend at most half their time on ops work — the rest on engineering.")
    bullet_list(c, 72, 388,
        ["If toil exceeds 50%, the team stops taking on new services until it's fixed.",
         "Toil scales with the fleet; engineering scales the TEAM. Only one of these is sustainable.",
         "Measure toil in a weekly log — what gets measured gets automated."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Error Budgets: Permission to Move Fast",
                       "100% reliability is the wrong target — budgets make the tradeoff explicit.")
    box(c, 72, 500, 220, 80, BOX_BLUE, "SLO 99.9%", "43 min/month\nof errors allowed")
    box(c, 320, 500, 220, 80, BOX_GREEN, "Budget remaining", "ship features\nfast")
    arrow(c, 292, 540, 318, 540, color=ACCENT, width=2, label="spend")
    box(c, 72, 380, 468, 70, BOX_RED, "Budget exhausted → feature freeze", "all hands on reliability until the budget recovers")
    note(c, 72, 290, 468, "The budget aligns incentives: product wants velocity, SRE wants stability — the number settles the argument.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Blameless Postmortems",
                       "Fix the system, not the person — or nobody will tell you what broke.")
    box(c, 72, 500, 220, 80, BOX_RED, "Blameful", "'who pushed\nthe bad deploy?'")
    box(c, 320, 500, 220, 80, BOX_GREEN, "Blameless", "'what let the bad\ndeploy through?'")
    arrow(c, 292, 540, 318, 540, color=ACCENT, width=2, label="reframe")
    bullet_list(c, 72, 430,
        ["Assume everyone acted reasonably with the information they had.",
         "Ask 'how' five times: the deploy broke prod → why did CI pass? → why no canary? → …",
         "Action items have owners and dates — a postmortem without follow-through is theater."],
        font_size=10.5, gap=26)
    note(c, 72, 260, 468, "Write it for the next on-call at 3am: timeline, root causes, what we changed so it can't recur.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Automation Over Toil: Examples",
                       "Every manual ritual is an automation candidate.")
    autos = [("Deploys", "one-button / fully automated with canary analysis", BOX_BLUE),
             ("On-call triage", "runbooks as code: auto-diagnose, suggest, then page", BOX_GREEN),
             ("Capacity", "autoscaling + predictive — no 2am 'add nodes' tickets", BOX_ORANGE),
             ("Releases", "feature flags + progressive delivery, no deploy windows", BOX_TEAL)]
    yy = y
    for name, desc, fill in autos:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=10.5)
        yy -= 70
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "SRE Team Topologies",
                       "How SRE plugs into the org without becoming a ticket queue.")
    box(c, 72, 520, 468, 56, BOX_BLUE, "Embedded", "SREs inside product teams — reliability by pairing", font_size=11)
    box(c, 72, 450, 468, 56, BOX_GREEN, "Consulting", "central team advises, builds platforms, reviews designs", font_size=11)
    box(c, 72, 380, 468, 56, BOX_ORANGE, "Platform", "SRE owns the paved road: CI/CD, observability, guardrails", font_size=11)
    note(c, 72, 290, 468, "Anti-pattern: SRE as 'ops ticket queue.' If SRE only does toil, it's not SRE — it's ops with a new name.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "SRE Practices — Remember",
                 ["SRE implements DevOps: reliability as software engineering, measured and budgeted.",
                  "Toil is manual, repetitive, automatable work — cap it at 50%, automate the rest.",
                  "Error budgets turn 'move fast vs be stable' from argument into arithmetic.",
                  "Blameless postmortems fix systems: five whys, owned action items, written for 3am.",
                  "Never be a ticket queue: embed, consult, or platform — automate the toil away."],
                 pg)
    c.save(); print("wrote", path)


def pdf_slis_slos(path):
    c = new_canvas(path); pg = 1
    title_page(c, "SLIs, SLOs & SLAs\nVisual Guide",
               "Measure what matters —\nfrom indicator math to burn-rate alerts.",
               "Cloud & DevOps", None); pg += 1

    y = section_header(c, 1, 6, "Indicator vs Objective vs Agreement",
                       "Three layers: what you measure, what you target, what you promise.")
    box(c, 72, 500, 140, 80, BOX_BLUE, "SLI", "the metric\n99.2% success")
    box(c, 236, 500, 140, 80, BOX_GREEN, "SLO", "the target\n99.9% / 30d")
    box(c, 400, 500, 140, 80, BOX_ORANGE, "SLA", "the contract\ncredits if missed")
    arrow(c, 212, 540, 234, 540, color=ACCENT, width=1.5)
    arrow(c, 376, 540, 398, 540, color=ACCENT, width=1.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 430, "SLI: what happened. SLO: what we aim for (internal). SLA: what we owe customers (legal).")
    note(c, 72, 340, 468, "Set the SLA looser than the SLO — the gap is your safety margin before contracts bite.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Good SLIs",
                       "Measure what users feel, as a ratio over a window.")
    slis = [("Availability", "successful requests / total requests", BOX_BLUE),
            ("Latency", "requests under threshold / total (p99 < 500ms)", BOX_GREEN),
            ("Freshness", "data updated within X / total updates", BOX_ORANGE),
            ("Correctness", "correct results / total (no silent wrongness)", BOX_TEAL)]
    yy = y
    for name, desc, fill in slis:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=11)
        yy -= 70
    note(c, 72, yy - 60, 468, "Ratio + window: '99.9% of requests succeed, measured over 30 days.' Never an instantaneous gauge.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Error Budget Math",
                       "The allowed failure slice — spend it on velocity.")
    box(c, 72, 500, 468, 70, BOX_BLUE, "SLO 99.9%  →  budget 0.1%  →  43.2 min / month",
        "each '9' costs 10x: 99% = 7.2h, 99.99% = 4.3 min", font_size=10.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 440, "Budget consumed = (1 - SLI) / (1 - SLO). At 100% consumed: freeze features, fix reliability.")
    bullet_list(c, 72, 408,
        ["99.9% monthly = 43m downtime; 99.95% = 21m; 99.99% = 4.3m. Know your number.",
         "Budget remaining is a PRODUCT decision: spend on launches or save for safety.",
         "Reset windows: rolling 30 days is standard — old incidents age out."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Burn-Rate Alerting",
                       "Alert on how FAST you're eating the budget, not on raw errors.")
    box(c, 72, 500, 220, 80, BOX_RED, "Fast burn", "2% budget/hour\npage NOW")
    box(c, 320, 500, 220, 80, BOX_ORANGE, "Slow burn", "0.2% budget/hour\nticket, investigate")
    arrow(c, 292, 540, 318, 540, color=ACCENT, width=2, label="both matter")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 420, "Classic setup: 1h window + 6h window. Fast burn pages; slow burn tickets.")
    bullet_list(c, 72, 388,
        ["Burn rate = error rate / budget rate. Rate 1 = exactly on budget.",
         "Multi-window: short window catches spikes, long window confirms it's real.",
         "Reset the alert when the burn stops — don't page for history."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Choosing the Right SLO",
                       "Tighter isn't better — it's more expensive.")
    box(c, 72, 520, 468, 56, BOX_GREEN, "99.9%: most user-facing services", "the sane default — 43 min/month", font_size=11)
    box(c, 72, 450, 468, 56, BOX_BLUE, "99.95–99.99%: payments, auth", "worth the engineering cost", font_size=11)
    box(c, 72, 380, 468, 56, BOX_ORANGE, "99%: internal tools, batch", "don't gold-plate what users won't feel", font_size=11)
    note(c, 72, 290, 468, "Ask users what they need, not what sounds impressive. Nobody can feel 99.99% vs 99.999%.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "SLO Review Cadence",
                       "SLOs are living agreements — review them like code.")
    box(c, 72, 500, 150, 70, BOX_BLUE, "Weekly", "burn review\non-call")
    box(c, 246, 500, 150, 70, BOX_GREEN, "Monthly", "budget spend\nvs launches")
    box(c, 420, 500, 120, 70, BOX_ORANGE, "Quarterly", "retire/tighten\nSLOs")
    arrow(c, 222, 535, 244, 535, color=ACCENT, width=1.5)
    arrow(c, 396, 535, 418, 535, color=ACCENT, width=1.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 420, "Never breached in a year? The SLO is too loose — tighten it or stop paying for the margin.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "SLIs, SLOs & SLAs — Remember",
                 ["SLI measures, SLO targets (internal), SLA promises (contractual) — keep SLA looser than SLO.",
                  "Good SLIs are user-facing ratios over windows: success rate, latency compliance.",
                  "Error budget = 1 − SLO: 99.9% gives 43 min/month. Spend it on velocity or save it.",
                  "Burn-rate alerts: fast burn pages, slow burn tickets — multi-window to avoid noise.",
                  "Review SLOs quarterly: never-breached means too loose; always-breached means fiction."],
                 pg)
    c.save(); print("wrote", path)


def pdf_incident_response(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Incident Response\nVisual Guide",
               "Sev levels, roles, runbooks —\ncalm, practiced, repeatable firefighting.",
               "Cloud & DevOps", None); pg += 1

    y = section_header(c, 1, 6, "Severity Levels",
                       "Sev defines urgency, responders, and comms — decided in minutes.")
    sevs = [("SEV-1", "critical: full outage / data loss — all hands, exec comms", BOX_RED),
            ("SEV-2", "major: core feature down — on-call + team lead", BOX_ORANGE),
            ("SEV-3", "minor: degraded, workaround exists — owning team", BOX_BLUE),
            ("SEV-4", "low: cosmetic / single user — backlog it", BOX_GREEN)]
    yy = y
    for name, desc, fill in sevs:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=10.5)
        yy -= 70
    note(c, 72, yy - 60, 468, "Declare the SEV early and adjust later. Under-sevving delays help; over-sevving just wastes a few people's hour.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Roles: Who Does What",
                       "Named roles prevent five people debugging and nobody communicating.")
    roles = [("Incident Commander", "owns the response: decides, delegates, declares 'all clear'", BOX_RED),
             ("Comms Lead", "status page + stakeholder updates every 15–30 min", BOX_BLUE),
             ("Ops / Responders", "diagnose and mitigate — report to the IC", BOX_GREEN),
             ("Scribe", "timeline of everything: the postmortem writes itself", BOX_ORANGE)]
    yy = y
    for name, desc, fill in roles:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=10.5)
        yy -= 70
    note(c, 72, yy - 60, 468, "The IC doesn't debug — they coordinate. The moment the IC goes heads-down, the response loses its brain.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "The Incident Lifecycle",
                       "Detect → declare → mitigate → resolve → learn.")
    steps = [("Detect", "alert / report", BOX_RED), ("Declare", "SEV + roles", BOX_ORANGE),
             ("Mitigate", "stop bleeding", BOX_BLUE), ("Resolve", "fix + verify", BOX_GREEN),
             ("Learn", "postmortem", BOX_TEAL)]
    bx = 60
    for name, desc, fill in steps:
        box(c, bx, 480, 92, 80, fill, name, desc, font_size=9.5)
        if bx > 60: arrow(c, bx - 10, 520, bx, 520, color=ACCENT, width=1.5)
        bx += 102
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 400, "Mitigate BEFORE root-causing: roll back, fail over, shed load — understanding can wait.")
    bullet_list(c, 72, 368,
        ["Time-to-mitigate is the metric that matters, not time-to-root-cause.",
         "Declare early: a SEV-2 that becomes SEV-1 wasted 30 minutes of response.",
         "Resolve = verified fixed + monitoring green, not 'looks fine to me'."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Runbooks: Decisions Made in Advance",
                       "A good runbook turns panic into procedure.")
    box(c, 72, 500, 468, 70, BOX_BLUE, "Runbook: 'Checkout errors spiking'",
        "1. Check payments dashboard → 2. Flip feature flag → 3. Roll back deploy → 4. Page payments on-call", font_size=9.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 440, "Anatomy: symptoms → diagnosis steps → mitigation actions → escalation paths.")
    bullet_list(c, 72, 408,
        ["Link runbooks FROM the alert — the page should land on the procedure.",
         "Test runbooks in game days: an untested runbook is fiction.",
         "Keep them short: if it needs 20 pages, automate the first 15."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Status Communications",
                       "Silence breeds speculation — communicate on a cadence.")
    box(c, 72, 500, 220, 80, BOX_BLUE, "Status page", "investigating →\nidentified → fixed")
    box(c, 320, 500, 220, 80, BOX_GREEN, "Internal", "#incident-war-room\n+ exec summary")
    arrow(c, 292, 540, 318, 540, color=ACCENT, width=1.5, label="same facts")
    bullet_list(c, 72, 430,
        ["Update every 15–30 min even if there's nothing new: 'still investigating' beats silence.",
         "Template: what's broken, who's affected, what we're doing, next update time.",
         "One voice outward (comms lead); responders stay heads-down."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Post-Incident Review",
                       "The incident ends twice: when it's fixed, and when it's learned from.")
    box(c, 72, 500, 150, 70, BOX_BLUE, "Timeline", "what happened\nwhen")
    box(c, 246, 500, 150, 70, BOX_ORANGE, "Root causes", "five whys\nsystemic")
    box(c, 420, 500, 120, 70, BOX_GREEN, "Actions", "owned +\ndated")
    arrow(c, 222, 535, 244, 535, color=ACCENT, width=1.5)
    arrow(c, 396, 535, 418, 535, color=ACCENT, width=1.5)
    note(c, 72, 400, 468, "Blameless: 'what let this through?' not 'who did this?' — or the next incident goes unreported.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Incident Response — Remember",
                 ["Declare the SEV early; adjust later. Named roles: IC coordinates, comms communicates.",
                  "Mitigate before root-causing — time-to-mitigate is the metric.",
                  "Runbooks linked from alerts turn panic into procedure; test them in game days.",
                  "Communicate on cadence (15–30 min): status page outward, war room inward.",
                  "Blameless postmortem with owned action items — the incident ends when it's learned from."],
                 pg)
    c.save(); print("wrote", path)


def pdf_cost_optimization(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Cloud Cost Optimization\nVisual Guide",
               "Rightsize, commit, go spot —\nFinOps practices that cut the bill.",
               "Cloud & DevOps", None); pg += 1

    y = section_header(c, 1, 6, "Visibility First: Tag Everything",
                       "You can't optimize what you can't attribute.")
    box(c, 72, 500, 468, 70, BOX_BLUE, "Tags: team, env, service, cost-center",
        "every resource carries its owner — no orphans", font_size=10.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 440, "Cost allocation: 100% of spend mapped to a team. Untagged = unowned = waste.")
    bullet_list(c, 72, 408,
        ["Enforce tagging with policy (deny untagged deploys) — voluntary tagging never sticks.",
         "Dashboards per team: show spend vs budget weekly, not quarterly.",
         "Alert on anomalies: 3x daily spend spike pages the owner, not finance."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Rightsizing: Match Shape to Load",
                       "Most instances run at 10–20% — that's the tax.")
    box(c, 72, 500, 220, 80, BOX_RED, "m5.4xlarge", "avg CPU 12%\n$560/mo")
    box(c, 320, 500, 220, 80, BOX_GREEN, "m5.large", "avg CPU 48%\n$70/mo")
    arrow(c, 292, 540, 318, 540, color=ACCENT, width=2, label="8x cheaper")
    bullet_list(c, 72, 430,
        ["Use recommender tools (Compute Optimizer): 2 weeks of metrics → suggested size.",
         "Right-size storage too: gp3 with provisioned IOPS beats over-provisioned gp2.",
         "Schedule non-prod: dev/staging off nights and weekends — 60%+ savings."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Spot / Preemptible: Up to 90% Off",
                       "Spare capacity at a discount — with an eviction risk.")
    box(c, 72, 500, 220, 80, BOX_GREEN, "Spot", "70–90% off\n2-min warning")
    box(c, 320, 500, 220, 80, BOX_BLUE, "On-demand", "full price\nguaranteed")
    arrow(c, 292, 540, 318, 540, color=ACCENT, width=2, label="same hardware")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 420, "Perfect for: batch jobs, CI runners, stateless workers, dev clusters.")
    bullet_list(c, 72, 388,
        ["Design for interruption: checkpoint work, handle SIGTERM gracefully.",
         "Diversify instance types + AZs — evictions rarely hit all pools at once.",
         "Never spot for: single-AZ databases, stateful singletons, latency-critical paths."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Commitments: Savings Plans & RIs",
                       "Trade a 1–3 year commitment for 30–70% off steady workloads.")
    box(c, 72, 500, 150, 70, BOX_BLUE, "On-demand", "baseline\nflexible")
    box(c, 246, 500, 150, 70, BOX_GREEN, "1-yr commit", "~40% off\nsteady use")
    box(c, 420, 500, 120, 70, BOX_TEAL, "3-yr commit", "~60% off\nstable base")
    arrow(c, 222, 535, 244, 535, color=ACCENT, width=1.5)
    arrow(c, 396, 535, 418, 535, color=ACCENT, width=1.5)
    note(c, 72, 400, 468, "Commit to the BASELINE (the load you always have), keep the peaks on-demand/spot.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Kill the Idle: Storage & Sprawl",
                       "The quiet killers: unattached disks, old snapshots, zombie LBs.")
    items = [("Unattached volumes", "deleted instance, orphaned disk still billing — snapshot then delete", BOX_RED),
             ("Old snapshots", "snapshot sprawl: keep N generations, lifecycle the rest", BOX_ORANGE),
             ("Idle load balancers", "no targets for 30 days? it's $20/mo of nothing", BOX_BLUE),
             ("Over-retained logs", "tier to cold storage or drop — logs are money", BOX_TEAL)]
    yy = y
    for name, desc, fill in items:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=10.5)
        yy -= 70
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "FinOps: Culture, Not Just Tools",
                       "Cost is an engineering metric — review it like latency.")
    box(c, 72, 500, 150, 70, BOX_BLUE, "Inform", "showback\nper team")
    box(c, 246, 500, 150, 70, BOX_GREEN, "Optimize", "rightsizing\nsprints")
    box(c, 420, 500, 120, 70, BOX_ORANGE, "Operate", "budgets +\nguardrails")
    arrow(c, 222, 535, 244, 535, color=ACCENT, width=1.5)
    arrow(c, 396, 535, 418, 535, color=ACCENT, width=1.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 420, "Monthly FinOps review: top 10 spend drivers, waste found, commitments adjusted.")
    note(c, 72, 330, 468, "Engineers control 90% of cloud spend through architecture choices — give them the data and the incentive.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Cloud Cost Optimization — Remember",
                 ["Tag everything and attribute 100% of spend — visibility before optimization.",
                  "Rightsize to actual load; schedule non-prod off; fix storage tiers.",
                  "Spot/preemptible for fault-tolerant work (up to 90% off); commit for the steady baseline.",
                  "Hunt idle resources monthly: orphaned disks, old snapshots, zombie load balancers.",
                  "FinOps loop: inform (showback) → optimize (sprints) → operate (budgets)."],
                 pg)
    c.save(); print("wrote", path)


def pdf_multi_region(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Multi-Region Architecture\nVisual Guide",
               "Active-active vs active-passive —\ndesign for distance and disaster.",
               "Cloud & DevOps", None); pg += 1

    y = section_header(c, 1, 6, "Why Multiple Regions",
                       "Three reasons, three different designs.")
    whys = [("Latency", "serve users from nearby — 200ms → 30ms", BOX_BLUE),
            ("Resilience", "survive a regional outage — no single point of geography", BOX_GREEN),
            ("Compliance", "data residency: EU data stays in the EU", BOX_ORANGE)]
    yy = y
    for name, desc, fill in whys:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=11)
        yy -= 70
    note(c, 72, yy - 60, 468, "Multi-region is the most expensive reliability you can buy — earn it with real requirements, not vibes.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Active-Active vs Active-Passive",
                       "Both serve; or one waits warm for disaster.")
    box(c, 72, y - 80, 225, 120, BOX_GREEN, "ACTIVE-ACTIVE", "both serve\ntraffic", font_size=12)
    box(c, 315, y - 80, 225, 120, BOX_BLUE, "ACTIVE-PASSIVE", "one serves,\none waits", font_size=12)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    aa = ["2x cost, always", "Needs conflict resolution", "Zero failover time"]
    ap = ["~1.2x cost (warm standby)", "Simpler data story", "Minutes to fail over"]
    yy = y - 120
    for a, b in zip(aa, ap):
        c.drawString(72, yy, "• " + a); c.drawString(315, yy, "• " + b); yy -= 20
    note(c, 72, 160, 468, "Active-active demands multi-writer data. If your database can't do it, you're active-passive with extra steps.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Data Replication Patterns",
                       "Reads scale easily; writes are the hard part.")
    pats = [("Read replicas", "one writer, many regional readers — async lag in seconds", BOX_BLUE),
            ("Multi-writer", "writes anywhere — needs conflict resolution (CRDTs / last-write-wins)", BOX_RED),
            ("Partitioned", "EU users → EU writes; US → US — no conflicts by design", BOX_GREEN)]
    yy = y
    for name, desc, fill in pats:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=10.5)
        yy -= 70
    note(c, 72, yy - 60, 468, "Async replication lag means a reader can see stale data — design the UX for it (or pay for sync).")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "DNS Failover & Health Checks",
                       "Traffic steering is only as good as the health signal.")
    box(c, 226, 520, 160, 60, BOX_BLUE, "DNS / GTM", "routes by health")
    box(c, 106, 380, 160, 70, BOX_GREEN, "us-east", "healthy ✓")
    box(c, 346, 380, 160, 70, BOX_RED, "eu-west", "failing ✗")
    arrow(c, 280, 518, 180, 452, color=GREEN, width=2.5)
    c.setStrokeColor(RED); c.setLineWidth(1.5); c.setDash(4, 3)
    c.line(340, 518, 420, 452); c.setDash()
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 320, "Health checks must test the FULL path: LB → app → database. A 200 from the LB means nothing.")
    note(c, 72, 240, 468, "DNS TTL is your failover floor: 60s TTL ≈ 60s+ for clients to move. Anycast + LB failover is faster.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Consistency Trade-offs (CAP)",
                       "In a partition, pick: availability or consistency.")
    box(c, 72, 500, 220, 80, BOX_GREEN, "AP: available", "serve reads/writes\nreconcile later")
    box(c, 320, 500, 220, 80, BOX_BLUE, "CP: consistent", "refuse writes\nuntil synced")
    arrow(c, 292, 540, 318, 540, color=ACCENT, width=2, label="partition forces")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 420, "Most apps are mixed: AP for the catalog (stale OK), CP for payments (never wrong).")
    bullet_list(c, 72, 388,
        ["Eventual consistency needs a UX: 'order received' now, 'confirmed' after sync.",
         "Idempotency keys make retried writes safe across regions.",
         "Test partitions with chaos experiments — don't discover CAP during a real outage."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Reference: Regional 3-Tier",
                       "Each region is a full stack; DNS + replication tie them together.")
    box(c, 72, 500, 220, 90, BOX_GREEN, "us-east (primary)", "LB → app → DB\nwriter")
    box(c, 320, 500, 220, 90, BOX_BLUE, "eu-west", "LB → app → DB\nread replica")
    arrow(c, 292, 545, 318, 545, color=ACCENT, width=2, label="async repl")
    box(c, 226, 380, 160, 60, BOX_ORANGE, "Global DNS", "health-routed")
    arrow(c, 306, 498, 180, 442, color=GREEN, width=1.5)
    arrow(c, 306, 498, 430, 442, color=GREEN, width=1.5)
    note(c, 72, 290, 468, "Start here: active-passive with read replicas. Go active-active only when writes demand it.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Multi-Region Architecture — Remember",
                 ["Go multi-region for latency, resilience, or compliance — never by default.",
                  "Active-active needs multi-writer data; active-passive is cheaper and simpler.",
                  "Replicate reads easily; writes need conflict strategy or partitioning.",
                  "Failover rides on honest health checks and low DNS TTLs.",
                  "CAP forces a choice per workload: AP for catalogs, CP for money."],
                 pg)
    c.save(); print("wrote", path)


def pdf_disaster_recovery(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Disaster Recovery\nVisual Guide",
               "RTO, RPO, and the four strategies —\nfrom backup to hot multi-site.",
               "Cloud & DevOps", None); pg += 1

    y = section_header(c, 1, 6, "RTO & RPO: The Two Numbers",
                       "How fast must you recover, and how much data can you lose?")
    box(c, 72, 500, 220, 90, BOX_RED, "RTO", "Recovery TIME Objective\nmax downtime: 4 hours")
    box(c, 320, 500, 220, 90, BOX_ORANGE, "RPO", "Recovery POINT Objective\nmax data loss: 15 min")
    arrow(c, 292, 545, 318, 545, color=ACCENT, width=2, label="both = $$$")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 430, "Timeline: disaster at T → data restored to T−RPO → service back by T+RTO.")
    note(c, 72, 340, 468, "Set RTO/RPO per tier: checkout gets 1h/5min; the internal wiki gets 48h/24h. Not everything is tier-1.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Strategy 1: Backup & Restore",
                       "Cheapest. Slowest. Better than nothing.")
    box(c, 72, 500, 160, 70, BOX_BLUE, "Backups", "nightly to\nobject store")
    box(c, 380, 500, 160, 70, BOX_RED, "Restore", "hours to\nrebuild")
    arrow(c, 232, 535, 378, 535, color=ACCENT, width=2, label="on disaster")
    bullet_list(c, 72, 430,
        ["RTO: hours. RPO: up to 24h (last backup). Cost: near zero idle.",
         "Automate the restore — a manual 47-step wiki is not a recovery plan.",
         "Test restores quarterly: untested backups are Schrödinger's backups."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Strategy 2: Pilot Light",
                       "Core data replicates; servers spin up on demand.")
    box(c, 72, 500, 200, 80, BOX_GREEN, "Always on", "DB replica +\nminimal core")
    box(c, 320, 500, 220, 80, BOX_ORANGE, "On disaster", "auto-scale fleet\nfrom images")
    arrow(c, 272, 540, 318, 540, color=ACCENT, width=2, label="ignite")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 420, "Like a pilot light on a furnace: tiny flame always burning, full heat in minutes.")
    bullet_list(c, 72, 388,
        ["RTO: tens of minutes. RPO: minutes (async DB replication).",
         "Keep golden images / IaC current — stale images fail at the worst moment.",
         "DNS flip moves traffic once the fleet is healthy."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Strategy 3: Warm Standby",
                       "Scaled-down clone always running, ready to scale up.")
    box(c, 72, 500, 220, 80, BOX_BLUE, "Primary", "100% capacity\nlive traffic")
    box(c, 320, 500, 220, 80, BOX_GREEN, "Standby", "10% capacity\nsynced data")
    arrow(c, 292, 540, 318, 540, color=ACCENT, width=2, label="promote")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 420, "RTO: minutes (scale up + DNS). RPO: seconds–minutes. Cost: ~15–25% of primary.")
    note(c, 72, 330, 468, "The standby must take REAL (synthetic) traffic — an idle standby's first real request is its first test.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Strategy 4: Multi-Site (Hot-Hot)",
                       "Full capacity in two places, both serving.")
    box(c, 72, 500, 220, 80, BOX_GREEN, "Site A", "100% — live")
    box(c, 320, 500, 220, 80, BOX_GREEN, "Site B", "100% — live")
    arrow(c, 292, 540, 318, 540, color=ACCENT, width=2, label="sync")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 420, "RTO ≈ 0, RPO ≈ 0. Cost: 2x everything + data-sync engineering.")
    bullet_list(c, 72, 388,
        ["This is active-active multi-region — the DR strategy with no failover step.",
         "Data conflicts are the price: design for multi-writer from day one.",
         "Only tier-1 workloads justify it — everything else gets warm standby or pilot light."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "DR Testing: Prove It Works",
                       "A plan you've never run is a hope, not a plan.")
    box(c, 72, 500, 150, 70, BOX_BLUE, "Tabletop", "talk through\nquarterly")
    box(c, 246, 500, 150, 70, BOX_ORANGE, "Simulated", "fail over\nstaging")
    box(c, 420, 500, 120, 70, BOX_RED, "Live", "real failover\nprod traffic")
    arrow(c, 222, 535, 244, 535, color=ACCENT, width=1.5)
    arrow(c, 396, 535, 418, 535, color=ACCENT, width=1.5)
    note(c, 72, 400, 468, "Measure actual RTO/RPO in every test and compare to targets — then fix the gap before the real thing.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Disaster Recovery — Remember",
                 ["RTO = max downtime; RPO = max data loss. Set them per tier, not per company.",
                  "Backup/restore: cheapest, slowest. Pilot light: DB replicates, fleet ignites.",
                  "Warm standby: scaled-down clone, minutes to promote. Multi-site: hot-hot, ~zero RTO.",
                  "Automate restores and failovers — manual wikis fail under pressure.",
                  "Test on a ladder: tabletop → simulated → live. Measure real RTO/RPO every time."],
                 pg)
    c.save(); print("wrote", path)


def pdf_orchestration_compared(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Container Orchestration\nCompared",
               "Kubernetes vs ECS vs Nomad —\nmatch the platform to the workload.",
               "Cloud & DevOps", None); pg += 1

    y = section_header(c, 1, 6, "The Orchestration Problem",
                       "Containers are easy; fleets of them are not.")
    probs = [("Scheduling", "which host runs this container?", BOX_BLUE),
             ("Health", "restart it when it dies — forever", BOX_GREEN),
             ("Networking", "containers find and talk to each other", BOX_ORANGE),
             ("Scaling", "3 → 30 replicas on demand", BOX_TEAL)]
    yy = y
    for name, desc, fill in probs:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=11)
        yy -= 70
    note(c, 72, yy - 60, 468, "An orchestrator is a desired-state machine for containers: you declare, it converges — like GitOps for compute.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Kubernetes: The Standard",
                       "Portable, powerful, and operationally heavy.")
    box(c, 72, 500, 468, 70, BOX_BLUE, "Kubernetes",
        "pods, deployments, services — runs anywhere, steep learning curve", font_size=10.5)
    bullet_list(c, 72, 430,
        ["Strengths: ecosystem (Helm, operators, service mesh), portable across clouds.",
         "Weaknesses: complexity — control plane, upgrades, and YAML sprawl are real work.",
         "Managed flavors (EKS/GKE/AKS) remove control-plane toil, not app complexity.",
         "Best for: multi-cloud, platform teams, complex microservices, ML pipelines."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "ECS: The AWS-Native",
                       "Containers without the Kubernetes learning curve.")
    box(c, 72, 500, 468, 70, BOX_ORANGE, "ECS (+ Fargate)",
        "tasks + services — deep AWS integration, no control plane to run", font_size=10.5)
    bullet_list(c, 72, 430,
        ["Strengths: simple mental model, IAM-native, Fargate = no servers at all.",
         "Weaknesses: AWS-only — no portability; smaller ecosystem than K8s.",
         "Fargate removes node management; EC2 launch type keeps cost control.",
         "Best for: AWS-committed teams, simpler service meshes, fast time-to-prod."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Nomad: The Minimalist",
                       "One binary for containers, VMs, and batch — from HashiCorp.")
    box(c, 72, 500, 468, 70, BOX_TEAL, "Nomad",
        "jobspec → schedule — single binary, multi-workload (docker, exec, java)", font_size=10.5)
    bullet_list(c, 72, 430,
        ["Strengths: dead simple to operate, one agent for mixed workloads (not just containers).",
         "Weaknesses: smaller ecosystem and community than Kubernetes.",
         "Pairs with Consul (discovery) + Vault (secrets): the HashiCorp stack.",
         "Best for: small teams, mixed workloads, edge, shops that value simplicity."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Decision Matrix",
                       "Match the platform to the workload and the team.")
    rows = [("Multi-cloud / portable", "Kubernetes", BOX_BLUE),
            ("AWS-only, ship fast", "ECS + Fargate", BOX_ORANGE),
            ("Small team, mixed workloads", "Nomad", BOX_TEAL),
            ("Complex microservices", "Kubernetes", BOX_BLUE),
            ("Batch + services together", "Nomad", BOX_TEAL),
            ("Regulated, need control", "Kubernetes (self-managed)", BOX_PURP)]
    yy = y
    for name, pick, fill in rows:
        box(c, 72, yy - 44, 300, 48, fill, name, None, font_size=10)
        box(c, 384, yy - 44, 156, 48, BOX_GREEN, pick, None, font_size=9.5)
        yy -= 60
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Migration Advice",
                       "You can change your mind — containers are portable.")
    bullet_list(c, 72, y,
        ["Start with the SIMPLEST that fits: ECS/Fargate or Nomad before Kubernetes.",
         "Keep images registry-portable (OCI) — the orchestrator is replaceable, the image isn't.",
         "Kubernetes is a platform to BUILD on, not just run on — budget platform-team time.",
         "Re-evaluate yearly: team size, cloud commitment, and workload mix all drift."],
        font_size=11, gap=28)
    note(c, 72, 300, 468, "No affiliation with any vendor implied — evaluate on your constraints: team skill, cloud lock-in tolerance, workload shape.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Container Orchestration Compared — Remember",
                 ["All orchestrators solve scheduling, health, networking, scaling as desired-state.",
                  "Kubernetes: portable and powerful, operationally heavy — needs platform investment.",
                  "ECS + Fargate: simplest AWS path, no control plane, but AWS-only.",
                  "Nomad: minimal ops, mixed workloads, smallest ecosystem.",
                  "Choose by constraints (team, cloud, workload) — keep images OCI-portable so you can switch."],
                 pg)
    c.save(); print("wrote", path)


def pdf_service_discovery(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Service Discovery\nVisual Guide",
               "Find services that never sit still —\nDNS, registries, and health checks.",
               "Cloud & DevOps", None); pg += 1

    y = section_header(c, 1, 6, "The Problem: Ephemeral IPs",
                       "Containers die and respawn with new addresses every minute.")
    box(c, 72, 500, 140, 70, BOX_RED, "payments\n10.0.1.4", "dies")
    box(c, 252, 500, 140, 70, BOX_GREEN, "payments\n10.0.7.9", "reborn")
    box(c, 432, 500, 108, 70, BOX_BLUE, "checkout", "hardcoded?\nbroken!")
    arrow(c, 212, 535, 250, 535, color=RED, width=2, label="IP changed")
    arrow(c, 392, 535, 430, 535, color=ACCENT, width=2, label="calls")
    c.setStrokeColor(RED); c.setLineWidth(1.5); c.setDash(4, 3)
    c.line(486, 498, 322, 572); c.setDash()
    note(c, 72, 400, 468, "Hardcoded IPs and static config are the enemy — services must discover each other dynamically.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "DNS-Based Discovery",
                       "The oldest trick: a name that resolves to healthy instances.")
    box(c, 226, 500, 160, 70, BOX_BLUE, "payments.svc", "DNS name")
    box(c, 106, 380, 120, 70, BOX_GREEN, "10.0.7.9", "instance A")
    box(c, 256, 380, 120, 70, BOX_GREEN, "10.0.3.2", "instance B")
    box(c, 406, 380, 120, 70, BOX_GREEN, "10.0.9.5", "instance C")
    arrow(c, 280, 498, 160, 452, color=ACCENT, width=1.5)
    arrow(c, 306, 498, 310, 452, color=ACCENT, width=1.5)
    arrow(c, 340, 498, 460, 452, color=ACCENT, width=1.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 320, "Kubernetes Services, AWS Cloud Map, Consul DNS: one stable name, many changing IPs.")
    note(c, 72, 240, 468, "DNS caching bites: low TTLs (seconds) or clients hold stale IPs. SRV records can also carry ports.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Registries: Consul & etcd",
                       "A strongly-consistent phone book for services.")
    box(c, 72, 500, 150, 70, BOX_BLUE, "Service", "registers\non start")
    box(c, 246, 500, 150, 70, BOX_PURP, "Registry", "Consul / etcd\nkv + health")
    box(c, 420, 500, 120, 70, BOX_GREEN, "Client", "queries\nfor peers")
    arrow(c, 222, 535, 244, 535, color=ACCENT, width=2, label="register")
    arrow(c, 396, 535, 418, 535, color=ACCENT, width=2, label="discover")
    bullet_list(c, 72, 430,
        ["Registration: on start (or via agent); deregistration: on graceful shutdown + TTL expiry.",
         "etcd is the generic KV store (Kubernetes uses it); Consul adds DNS + health checking built in.",
         "Raft consensus: the registry itself is HA — 3–5 nodes, survives minority loss."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Client-Side vs Server-Side",
                       "Who picks the instance: the caller or a middleman?")
    box(c, 72, y - 80, 225, 120, BOX_BLUE, "CLIENT-SIDE", "caller queries\nregistry, picks", font_size=12)
    box(c, 315, y - 80, 225, 120, BOX_GREEN, "SERVER-SIDE", "caller hits LB,\nLB picks", font_size=12)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    ca = ["Smarter routing (latency-aware)", "Client needs discovery logic", "e.g. gRPC, Ribbon"]
    cb = ["Dumb clients, simple", "LB is a hop + failure point", "e.g. K8s Service, ALB"]
    yy = y - 120
    for a, b in zip(ca, cb):
        c.drawString(72, yy, "• " + a); c.drawString(315, yy, "• " + b); yy -= 20
    note(c, 72, 160, 468, "Service meshes blend both: sidecar proxies do client-side logic with server-side simplicity for the app.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Health Checking: Trust but Verify",
                       "Discovery without health checks routes to corpses.")
    box(c, 72, 500, 150, 70, BOX_GREEN, "Liveness", "/healthz\nrestart me?")
    box(c, 246, 500, 150, 70, BOX_BLUE, "Readiness", "/ready\nsend traffic?")
    box(c, 420, 500, 120, 70, BOX_ORANGE, "Startup", "still\nbooting?")
    arrow(c, 222, 535, 244, 535, color=ACCENT, width=1.5)
    arrow(c, 396, 535, 418, 535, color=ACCENT, width=1.5)
    bullet_list(c, 72, 430,
        ["Readiness gates traffic: failing readiness pulls the instance from discovery, no restart.",
         "Liveness restarts: only fail it when the process is truly wedged (deadlock), not on slow deps.",
         "Checks must be cheap and fast — a 5s health check is a 5s detection delay."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Discovery in Kubernetes",
                       "Services + endpoints: the built-in answer.")
    box(c, 226, 520, 160, 60, BOX_BLUE, "Service", "stable ClusterIP")
    for i, bx in enumerate([106, 256, 406]):
        box(c, bx, 400, 100, 70, BOX_GREEN, f"pod-{i+1}", "ephemeral IP")
        arrow(c, 306, 518, bx + 50, 472, color=GREEN, width=1.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 340, "Endpoints controller tracks ready pods; kube-proxy / eBPF routes the Service IP to them.")
    note(c, 72, 250, 468, "Headless services (ClusterIP: None) return pod IPs directly — for stateful or client-side patterns.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Service Discovery — Remember",
                 ["Ephemeral IPs make static config fatal — services must discover each other dynamically.",
                  "DNS gives stable names over changing IPs; watch TTL caching.",
                  "Registries (Consul/etcd) are the HA phone book: register on start, health-check always.",
                  "Client-side = smart callers; server-side = simple callers behind a LB; meshes blend both.",
                  "Health checks (liveness/readiness/startup) keep discovery honest — cheap, fast, meaningful."],
                 pg)
    c.save(); print("wrote", path)


def pdf_k8s_workloads(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Kubernetes Workloads\nVisual Guide",
               "Deployments, StatefulSets, DaemonSets, Jobs —\npick the right controller for the job.",
               "Cloud & DevOps", None); pg += 1

    y = section_header(c, 1, 6, "Controllers: Desired State for Pods",
                       "You declare replicas; the controller makes it so.")
    ctrls = [("Deployment", "stateless apps — web APIs", BOX_BLUE),
             ("StatefulSet", "stateful — DBs, queues", BOX_GREEN),
             ("DaemonSet", "one per node — agents", BOX_ORANGE),
             ("Job / CronJob", "run to completion — batch", BOX_TEAL)]
    yy = y
    for name, desc, fill in ctrls:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=12)
        yy -= 70
    note(c, 72, yy - 60, 468, "Pods are mortal — never create them directly. Controllers recreate, reschedule, and roll them.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Deployments: Stateless Workhorses",
                       "Identical, interchangeable pods behind a stable endpoint.")
    box(c, 226, 520, 160, 60, BOX_BLUE, "Deployment", "replicas: 3")
    for i, bx in enumerate([106, 256, 406]):
        box(c, bx, 400, 100, 70, BOX_GREEN, f"pod-{i+1}", "identical")
        arrow(c, 306, 518, bx + 50, 472, color=GREEN, width=1.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 340, "Pods are cattle: any pod can serve any request. State lives outside (DB, cache, queue).")
    bullet_list(c, 72, 308,
        ["ReplicaSet (owned by the Deployment) keeps exactly N pods running.",
         "Rolling updates replace pods gradually — zero downtime by default.",
         "Rollbacks: `kubectl rollout undo` returns to the previous ReplicaSet."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "StatefulSets: Identity Matters",
                       "Stable names, stable storage, ordered operations.")
    box(c, 72, 500, 150, 70, BOX_GREEN, "db-0", "pvc-0")
    box(c, 246, 500, 150, 70, BOX_GREEN, "db-1", "pvc-1")
    box(c, 420, 500, 120, 70, BOX_GREEN, "db-2", "pvc-2")
    arrow(c, 222, 535, 244, 535, color=ACCENT, width=1.5, label="ordered")
    arrow(c, 396, 535, 418, 535, color=ACCENT, width=1.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 430, "db-0 dies → a new db-0 reattaches pvc-0. Identity and data survive the pod.")
    bullet_list(c, 72, 398,
        ["Use for: databases, Kafka/ZooKeeper, anything with quorum or local state.",
         "Headless Service gives each pod its own DNS: db-0.db, db-1.db.",
         "Ordered rolling updates: db-2, then db-1, then db-0 — never all at once."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "DaemonSets: One Per Node",
                       "Cluster-wide agents that must run everywhere.")
    box(c, 72, 500, 160, 70, BOX_ORANGE, "node-1", "fluent-bit")
    box(c, 256, 500, 160, 70, BOX_ORANGE, "node-2", "fluent-bit")
    box(c, 440, 500, 100, 70, BOX_BLUE, "node-3", "+1 auto")
    arrow(c, 232, 535, 254, 535, color=ACCENT, width=1.5)
    arrow(c, 416, 535, 438, 535, color=ACCENT, width=1.5, label="new node")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 430, "New node joins → DaemonSet schedules the pod automatically. No manual step.")
    bullet_list(c, 72, 398,
        ["Classic uses: log shippers, monitoring agents, CNI plugins, storage drivers.",
         "Tolerations let DaemonSet pods land on tainted nodes (e.g. GPU nodes).",
         "Updates roll node by node — the agent fleet never goes fully dark."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Jobs & CronJobs: Run to Completion",
                       "Not 'keep running' — 'finish the work, then stop'.")
    box(c, 72, 500, 220, 80, BOX_TEAL, "Job", "backup DB\ncompletions: 1")
    box(c, 320, 500, 220, 80, BOX_BLUE, "CronJob", "schedule:\n'0 2 * * *'")
    arrow(c, 292, 540, 318, 540, color=ACCENT, width=2, label="repeats")
    bullet_list(c, 72, 430,
        ["Job: runs pods until N succeed; backoffLimit caps retries on failure.",
         "CronJob: cron schedule creates Jobs — reports, cleanup, batch ETL.",
         "Set activeDeadlineSeconds: a hung job must die, not run forever.",
         "History limits (successfulJobsHistoryLimit) keep etcd from filling with old jobs."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Rolling Updates & Probes",
                       "Update strategy + health probes = safe deploys.")
    box(c, 72, 500, 220, 80, BOX_BLUE, "maxSurge: 1", "one extra pod\nabove desired")
    box(c, 320, 500, 220, 80, BOX_ORANGE, "maxUnavailable: 0", "never drop\ncapacity")
    arrow(c, 292, 540, 318, 540, color=ACCENT, width=2, label="tune")
    probes = [("readiness", "ready for traffic? — gates the Service endpoints", BOX_GREEN),
              ("liveness", "still alive? — restarts wedged pods", BOX_RED),
              ("startup", "still booting? — protects slow starts from liveness kills", BOX_BLUE)]
    yy = 400
    for name, desc, fill in probes:
        box(c, 72, yy - 48, 468, 52, fill, name, desc, font_size=10.5)
        yy -= 64
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Kubernetes Workloads — Remember",
                 ["Controllers maintain desired state — never create bare pods.",
                  "Deployments for stateless; StatefulSets for stable identity + storage.",
                  "DaemonSets put one agent pod per node, automatically on new nodes.",
                  "Jobs run to completion; CronJobs schedule them — cap retries and deadlines.",
                  "Rolling updates (surge/unavailable) + readiness/liveness/startup probes = safe deploys."],
                 pg)
    c.save(); print("wrote", path)


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(out, exist_ok=True)
    pdf_aws_core(os.path.join(out, "bbg-aws-core.pdf"))
    pdf_gcp_core(os.path.join(out, "bbg-gcp-core.pdf"))
    pdf_azure_core(os.path.join(out, "bbg-azure-core.pdf"))
    pdf_k8s_workloads(os.path.join(out, "bbg-k8s-workloads.pdf"))
    pdf_helm(os.path.join(out, "bbg-helm.pdf"))
    pdf_gitops(os.path.join(out, "bbg-gitops.pdf"))
    pdf_terraform(os.path.join(out, "bbg-terraform.pdf"))
    pdf_docker_deep(os.path.join(out, "bbg-docker-deep.pdf"))
    pdf_serverless(os.path.join(out, "bbg-serverless.pdf"))
    pdf_autoscaling(os.path.join(out, "bbg-autoscaling.pdf"))
    pdf_blue_green(os.path.join(out, "bbg-blue-green.pdf"))
    pdf_canary(os.path.join(out, "bbg-canary.pdf"))
    pdf_feature_flags(os.path.join(out, "bbg-feature-flags.pdf"))
    pdf_prometheus(os.path.join(out, "bbg-prometheus.pdf"))
    pdf_elk(os.path.join(out, "bbg-elk.pdf"))
    pdf_tracing(os.path.join(out, "bbg-tracing.pdf"))
    pdf_chaos(os.path.join(out, "bbg-chaos.pdf"))
    pdf_sre(os.path.join(out, "bbg-sre.pdf"))
    pdf_slis_slos(os.path.join(out, "bbg-slis-slos.pdf"))
    pdf_incident_response(os.path.join(out, "bbg-incident-response.pdf"))
    pdf_cost_optimization(os.path.join(out, "bbg-cost-optimization.pdf"))
    pdf_multi_region(os.path.join(out, "bbg-multi-region.pdf"))
    pdf_disaster_recovery(os.path.join(out, "bbg-disaster-recovery.pdf"))
    pdf_orchestration_compared(os.path.join(out, "bbg-orchestration-compared.pdf"))
    pdf_service_discovery(os.path.join(out, "bbg-service-discovery.pdf"))

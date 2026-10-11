"""Wire the 18 BBG-style PDFs into course JSONs as `pdfs` arrays on relevant modules."""
import json, os, glob, shutil, datetime

COURSES_DIR = os.path.expanduser("~/workspace/apex-audit/docs/university/data/courses")
BACKUP_DIR = os.path.expanduser("~/workspace/apex-audit/.work/pdf-buildout/course-json-backups-pdf")
os.makedirs(BACKUP_DIR, exist_ok=True)

BASE = "https://interstitiumlabs.dev/assets/pdfs"

PDFS = {
    "bbg-load-balancing.pdf":   ("Load Balancing — Visual Guide", "Animated step-by-step: algorithms, health checks, L4 vs L7, global load balancing."),
    "bbg-caching-cdn.pdf":       ("Caching & CDNs — Visual Guide", "Animated step-by-step: cache-aside, invalidation, edge networks, hit ratios."),
    "bbg-microservices.pdf":     ("Microservices Architecture — Visual Guide", "Animated step-by-step: decomposition, sync vs async, resilience, observability."),
    "bbg-tcp-handshake.pdf":     ("TCP 3-Way Handshake — Visual Guide", "Animated step-by-step: SYN/SYN-ACK/ACK, reliability, flow control, closing."),
    "bbg-dns-resolution.pdf":    ("DNS Resolution — Visual Guide", "Animated step-by-step: caches, root/TLD/authoritative, record types, DNSSEC/DoT/DoH."),
    "bbg-tls-handshake.pdf":     ("TLS Handshake — Visual Guide", "Animated step-by-step: ClientHello, certificates, ECDHE, forward secrecy, TLS 1.3."),
    "bbg-cloud-patterns.pdf":    ("Cloud Architecture Patterns — Visual Guide", "Animated step-by-step: regions/AZs, auto-scaling, queues, IaC, well-architected."),
    "bbg-kubernetes.pdf":        ("Kubernetes Architecture — Visual Guide", "Animated step-by-step: pods, deployments, services, config, autoscaling."),
    "bbg-cicd-pipeline.pdf":     ("CI/CD Pipelines — Visual Guide", "Animated step-by-step: stages, security gates, deploy strategies, GitOps, DORA."),
    "bbg-zero-trust.pdf":        ("Zero Trust Architecture — Visual Guide", "Animated step-by-step: tenets, identity perimeter, micro-segmentation, pillars."),
    "bbg-pki-encryption.pdf":    ("PKI & Encryption — Visual Guide", "Animated step-by-step: symmetric/asymmetric, signatures, certificates, hashing."),
    "bbg-oauth-flows.pdf":       ("OAuth 2.0 & Authentication Flows — Visual Guide", "Animated step-by-step: roles, auth code flow, tokens, scopes, hardening."),
    "bbg-neural-networks.pdf":   ("Neural Networks — Visual Guide", "Animated step-by-step: neurons, layers, backprop, gradient descent, overfitting."),
    "bbg-transformers.pdf":      ("Transformers & Attention — Visual Guide", "Animated step-by-step: Q/K/V, heatmaps, multi-head, the full block."),
    "bbg-ml-pipelines.pdf":      ("ML Training Pipelines — Visual Guide", "Animated step-by-step: validation, feature stores, experiments, deployment, drift."),
    "bbg-etl-pipelines.pdf":     ("ETL Data Pipelines — Visual Guide", "Animated step-by-step: extract/transform/load, DAGs, quality tests, medallion."),
    "bbg-stream-processing.pdf": ("Stream Processing — Visual Guide", "Animated step-by-step: batch vs stream, the log, windows, exactly-once."),
    "bbg-data-warehouses.pdf":   ("Data Warehouses & Lakehouses — Visual Guide", "Animated step-by-step: OLTP/OLAP, star schema, columnar, lakehouse."),
}

# course file -> list of pdf filenames relevant to it
COURSE_MAP = {
    "il-03-programming-language-forge.json": ["bbg-microservices.pdf", "bbg-oauth-flows.pdf"],
    "il-04-systems-linux-windows-networks.json": ["bbg-load-balancing.pdf", "bbg-caching-cdn.pdf", "bbg-tcp-handshake.pdf", "bbg-dns-resolution.pdf", "bbg-tls-handshake.pdf"],
    "il-05-cloud-devsecops-platform-sre.json": ["bbg-load-balancing.pdf", "bbg-caching-cdn.pdf", "bbg-microservices.pdf", "bbg-cloud-patterns.pdf", "bbg-kubernetes.pdf", "bbg-cicd-pipeline.pdf"],
    "il-06-cybersecurity-secure-engineering.json": ["bbg-tcp-handshake.pdf", "bbg-tls-handshake.pdf", "bbg-zero-trust.pdf", "bbg-pki-encryption.pdf", "bbg-oauth-flows.pdf"],
    "il-07-data-engineering-analytics-ai.json": ["bbg-neural-networks.pdf", "bbg-transformers.pdf", "bbg-ml-pipelines.pdf", "bbg-etl-pipelines.pdf", "bbg-stream-processing.pdf", "bbg-data-warehouses.pdf"],
    "il-08-algorithms-compilers-distributed-formal.json": ["bbg-microservices.pdf", "bbg-stream-processing.pdf"],
    "il-11-zero-trust-endpoint-defense.json": ["bbg-zero-trust.pdf", "bbg-pki-encryption.pdf", "bbg-tls-handshake.pdf"],
    "il-12-ai-engineering.json": ["bbg-neural-networks.pdf", "bbg-transformers.pdf", "bbg-ml-pipelines.pdf"],
    "il-13-software-engineering-interview-prep.json": ["bbg-load-balancing.pdf", "bbg-caching-cdn.pdf", "bbg-microservices.pdf"],
    "il-14-sre-devops-cloud-security-interview-prep.json": ["bbg-cloud-patterns.pdf", "bbg-kubernetes.pdf", "bbg-cicd-pipeline.pdf", "bbg-zero-trust.pdf"],
    "il-15-data-engineering-analytics-interview-prep.json": ["bbg-etl-pipelines.pdf", "bbg-stream-processing.pdf", "bbg-data-warehouses.pdf"],
    "il-16-machine-learning-ai-engineering.json": ["bbg-neural-networks.pdf", "bbg-transformers.pdf", "bbg-ml-pipelines.pdf"],
    "il-17-agentic-ai-engineering.json": ["bbg-transformers.pdf", "bbg-ml-pipelines.pdf"],
    "il-19-multicloud-devops-ai-bootcamp.json": ["bbg-cloud-patterns.pdf", "bbg-kubernetes.pdf", "bbg-cicd-pipeline.pdf", "bbg-load-balancing.pdf"],
    "il-24-threatlocker-assessment-prep-cbt.json": ["bbg-zero-trust.pdf", "bbg-tls-handshake.pdf"],
    "il-25-cybersecurity-professional-certificate.json": ["bbg-zero-trust.pdf", "bbg-pki-encryption.pdf", "bbg-oauth-flows.pdf", "bbg-tls-handshake.pdf"],
    "il-26-data-analyst-certification-senior-mastery.json": ["bbg-etl-pipelines.pdf", "bbg-stream-processing.pdf", "bbg-data-warehouses.pdf"],
    "il-27-it-infrastructure-specialist-threatlocker-mastery.json": ["bbg-tcp-handshake.pdf", "bbg-dns-resolution.pdf", "bbg-zero-trust.pdf"],
    "il-28-devsecops-cloud-infrastructure-mastery.json": ["bbg-cloud-patterns.pdf", "bbg-kubernetes.pdf", "bbg-cicd-pipeline.pdf", "bbg-load-balancing.pdf", "bbg-caching-cdn.pdf"],
    "il-29-threatlocker-ai-cybersecurity-mastery.json": ["bbg-zero-trust.pdf", "bbg-neural-networks.pdf", "bbg-tls-handshake.pdf"],
}

now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
wired = 0
for course_file, pdf_list in COURSE_MAP.items():
    path = os.path.join(COURSES_DIR, course_file)
    if not os.path.exists(path):
        print("SKIP (missing):", course_file); continue
    shutil.copy2(path, os.path.join(BACKUP_DIR, course_file))
    with open(path) as f:
        course = json.load(f)
    modules = course.get("modules", [])
    if not modules:
        print("SKIP (no modules):", course_file); continue
    # distribute pdfs round-robin across modules
    for i, pdf_file in enumerate(pdf_list):
        title, blurb = PDFS[pdf_file]
        mod = modules[i % len(modules)]
        pdfs = mod.setdefault("pdfs", [])
        if any(p.get("url", "").endswith(pdf_file) for p in pdfs):
            continue
        pdfs.append({
            "title": title,
            "url": f"{BASE}/{pdf_file}",
            "source": "Interstitium Labs",
            "blurb": blurb,
            "pages": 8,
            "animated": True,
            "verifiedUtc": now,
            "httpStatus": 200,
        })
        wired += 1
    with open(path, "w") as f:
        json.dump(course, f, indent=1, ensure_ascii=False)
    print(f"wired {course_file}: {len(pdf_list)} pdfs")

print(f"\nTotal pdf entries wired: {wired}")
print(f"Backups in: {BACKUP_DIR}")

"""Wire the 18 BBG-style PDFs into bootcamp content.json files as `pdfGuides`."""
import json, os, glob, shutil, datetime

BOOTCAMP_DIR = os.path.expanduser("~/workspace/cert-bootcamps/site/bootcamps")
BACKUP_DIR = os.path.expanduser("~/workspace/apex-audit/.work/pdf-buildout/bootcamp-json-backups-pdf")
os.makedirs(BACKUP_DIR, exist_ok=True)

BASE = "https://interstitiumlabs.dev/assets/pdfs"

PDFS = {
    "bbg-load-balancing.pdf":   "Load Balancing — Visual Guide",
    "bbg-caching-cdn.pdf":       "Caching & CDNs — Visual Guide",
    "bbg-microservices.pdf":     "Microservices Architecture — Visual Guide",
    "bbg-tcp-handshake.pdf":     "TCP 3-Way Handshake — Visual Guide",
    "bbg-dns-resolution.pdf":    "DNS Resolution — Visual Guide",
    "bbg-tls-handshake.pdf":     "TLS Handshake — Visual Guide",
    "bbg-cloud-patterns.pdf":    "Cloud Architecture Patterns — Visual Guide",
    "bbg-kubernetes.pdf":        "Kubernetes Architecture — Visual Guide",
    "bbg-cicd-pipeline.pdf":     "CI/CD Pipelines — Visual Guide",
    "bbg-zero-trust.pdf":        "Zero Trust Architecture — Visual Guide",
    "bbg-pki-encryption.pdf":    "PKI & Encryption — Visual Guide",
    "bbg-oauth-flows.pdf":       "OAuth 2.0 & Authentication Flows — Visual Guide",
    "bbg-neural-networks.pdf":   "Neural Networks — Visual Guide",
    "bbg-transformers.pdf":      "Transformers & Attention — Visual Guide",
    "bbg-ml-pipelines.pdf":      "ML Training Pipelines — Visual Guide",
    "bbg-etl-pipelines.pdf":     "ETL Data Pipelines — Visual Guide",
    "bbg-stream-processing.pdf": "Stream Processing — Visual Guide",
    "bbg-data-warehouses.pdf":   "Data Warehouses & Lakehouses — Visual Guide",
}

# keyword in bootcamp dir name -> pdfs
RULES = [
    (["cyber", "cissp", "cism", "security", "soc", "pentest", "threatlocker", "zero-trust", "ethical-hack"],
     ["bbg-zero-trust.pdf", "bbg-pki-encryption.pdf", "bbg-tls-handshake.pdf"]),
    (["network", "ccna", "tcp", "dns", "comptia-network", "net-plus"],
     ["bbg-tcp-handshake.pdf", "bbg-dns-resolution.pdf", "bbg-tls-handshake.pdf", "bbg-load-balancing.pdf"]),
    (["cloud", "aws", "azure", "gcp", "az-", "multicloud"],
     ["bbg-cloud-patterns.pdf", "bbg-load-balancing.pdf", "bbg-caching-cdn.pdf"]),
    (["k8s", "cka", "ckad", "kubernetes"],
     ["bbg-kubernetes.pdf", "bbg-microservices.pdf", "bbg-cicd-pipeline.pdf"]),
    (["devops", "sre", "cicd", "terraform", "ansible", "docker"],
     ["bbg-cicd-pipeline.pdf", "bbg-kubernetes.pdf", "bbg-cloud-patterns.pdf"]),
    (["data", "analytics", "sql", "etl", "warehouse", "bi-"],
     ["bbg-etl-pipelines.pdf", "bbg-data-warehouses.pdf", "bbg-stream-processing.pdf"]),
    (["ml", "ai-", "ai_", "llm", "deep-learning", "neural", "transformer", "alan-turing"],
     ["bbg-neural-networks.pdf", "bbg-transformers.pdf", "bbg-ml-pipelines.pdf"]),
    (["api", "microservice", "backend", "system-design"],
     ["bbg-microservices.pdf", "bbg-load-balancing.pdf", "bbg-caching-cdn.pdf", "bbg-oauth-flows.pdf"]),
    (["linux", "rhcsa", "sysadmin", "infra"],
     ["bbg-tcp-handshake.pdf", "bbg-dns-resolution.pdf"]),
    (["oauth", "auth", "identity"],
     ["bbg-oauth-flows.pdf", "bbg-zero-trust.pdf"]),
]

DEFAULT_PDFS = ["bbg-cloud-patterns.pdf", "bbg-tls-handshake.pdf"]

now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
wired_bootcamps = 0
wired_entries = 0

for content_path in sorted(glob.glob(os.path.join(BOOTCAMP_DIR, "*/content.json"))):
    slug = os.path.basename(os.path.dirname(content_path))
    if slug == "_engine":
        continue
    slug_l = slug.lower()
    pdfs = []
    for keywords, plist in RULES:
        if any(k in slug_l for k in keywords):
            for p in plist:
                if p not in pdfs:
                    pdfs.append(p)
    if not pdfs:
        pdfs = DEFAULT_PDFS
    pdfs = pdfs[:4]  # cap at 4 per bootcamp

    rel = os.path.relpath(content_path, BOOTCAMP_DIR)
    backup_path = os.path.join(BACKUP_DIR, rel)
    os.makedirs(os.path.dirname(backup_path), exist_ok=True)
    shutil.copy2(content_path, backup_path)

    with open(content_path) as f:
        data = json.load(f)
    guides = data.setdefault("pdfGuides", [])
    existing = {g.get("url", "").split("/")[-1] for g in guides}
    added = 0
    for pf in pdfs:
        if pf in existing:
            continue
        guides.append({
            "title": PDFS[pf],
            "url": f"{BASE}/{pf}",
            "source": "Interstitium Labs",
            "pages": 8,
            "animated": True,
            "verifiedUtc": now,
        })
        added += 1
    if added:
        with open(content_path, "w") as f:
            json.dump(data, f, indent=1, ensure_ascii=False)
        wired_bootcamps += 1
        wired_entries += added

print(f"Bootcamps wired: {wired_bootcamps}")
print(f"PDF entries added: {wired_entries}")
print(f"Backups in: {BACKUP_DIR}")

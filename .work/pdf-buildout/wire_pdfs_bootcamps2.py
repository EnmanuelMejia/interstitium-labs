"""Wire the 224 new BBG-style PDFs into bootcamp content.json files as `pdfGuides`.
Extends wire_pdfs_bootcamps.py (original 18, original RULES kept, lists extended).
Backups -> bootcamp-json-backups-pdf2/. Cap 6 per bootcamp. Idempotent (dedupes by URL)."""
import json, os, glob, shutil, datetime, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pdf_meta import PDFS, BASE, PAGES

BOOTCAMP_DIR = os.path.expanduser("~/workspace/cert-bootcamps/site/bootcamps")
BACKUP_DIR = os.path.expanduser("~/workspace/apex-audit/.work/pdf-buildout/bootcamp-json-backups-pdf2")
os.makedirs(BACKUP_DIR, exist_ok=True)

# keyword in bootcamp dir name -> pdf filenames (order = priority)
RULES = [
    (["cyber", "cissp", "cism", "security", "soc", "pentest", "threatlocker", "zero-trust", "zerotrust",
      "ethical-hack", "dod-8140", "isc2", "secops", "blue-team", "nice-framework", "nsa-codebreaker",
      "hackers-arise", "ai-agent-sec", "ml-defense", "sc-200", "sc-300", "endpoint"],
     ["bbg-zero-trust.pdf", "bbg-pki-encryption.pdf", "bbg-tls-handshake.pdf",
      "bbg-threat-modeling.pdf", "bbg-incident-response.pdf", "bbg-ir-playbooks.pdf",
      "bbg-siem.pdf", "bbg-edr.pdf", "bbg-forensics.pdf", "bbg-pentest.pdf",
      "bbg-firewalls.pdf", "bbg-vpns.pdf", "bbg-oauth-flows.pdf", "bbg-jwt.pdf",
      "bbg-mfa.pdf", "bbg-sqli.pdf", "bbg-xss.pdf", "bbg-web-security.pdf"]),
    (["network", "ccna", "tcp", "dns", "comptia-network", "net-plus", "network-plus"],
     ["bbg-tcp-handshake.pdf", "bbg-dns-resolution.pdf", "bbg-tls-handshake.pdf",
      "bbg-load-balancing.pdf", "bbg-subnets-cidr.pdf", "bbg-vlans.pdf", "bbg-nat.pdf",
      "bbg-osi-model.pdf", "bbg-routing-protocols.pdf", "bbg-tcp-teardown.pdf",
      "bbg-udp.pdf", "bbg-dhcp.pdf", "bbg-dns-security.pdf", "bbg-vpns.pdf"]),
    (["cloud", "aws", "azure", "gcp", "az-", "multicloud", "oracle-oci", "oci", "openshift"],
     ["bbg-cloud-patterns.pdf", "bbg-load-balancing.pdf", "bbg-caching-cdn.pdf",
      "bbg-aws-core.pdf", "bbg-azure-core.pdf", "bbg-gcp-core.pdf",
      "bbg-multi-region.pdf", "bbg-cost-optimization.pdf", "bbg-serverless.pdf",
      "bbg-disaster-recovery.pdf", "bbg-terraform.pdf", "bbg-kubernetes.pdf"]),
    (["k8s", "cka", "ckad", "kubernetes"],
     ["bbg-kubernetes.pdf", "bbg-microservices.pdf", "bbg-cicd-pipeline.pdf",
      "bbg-k8s-workloads.pdf", "bbg-helm.pdf", "bbg-docker-deep.pdf",
      "bbg-service-mesh.pdf", "bbg-gitops.pdf"]),
    (["devops", "sre", "cicd", "terraform", "ansible", "docker", "iac", "gitops", "platform"],
     ["bbg-cicd-pipeline.pdf", "bbg-kubernetes.pdf", "bbg-cloud-patterns.pdf",
      "bbg-terraform.pdf", "bbg-docker-deep.pdf", "bbg-gitops.pdf",
      "bbg-prometheus.pdf", "bbg-tracing.pdf", "bbg-elk.pdf", "bbg-sre.pdf",
      "bbg-slis-slos.pdf", "bbg-chaos.pdf", "bbg-disaster-recovery.pdf",
      "bbg-blue-green.pdf", "bbg-canary.pdf", "bbg-helm.pdf"]),
    (["data", "analytics", "sql", "etl", "warehouse", "bi-", "dp-203", "snowflake", "dbt"],
     ["bbg-etl-pipelines.pdf", "bbg-data-warehouses.pdf", "bbg-stream-processing.pdf",
      "bbg-sql-fundamentals.pdf", "bbg-joins.pdf", "bbg-star-schema.pdf",
      "bbg-dimensional-modeling.pdf", "bbg-airflow.pdf", "bbg-spark.pdf",
      "bbg-kafka-deep.pdf", "bbg-dbt.pdf", "bbg-data-quality.pdf",
      "bbg-normalization.pdf", "bbg-snowflake.pdf", "bbg-elt.pdf",
      "bbg-data-governance.pdf", "bbg-query-optimization.pdf"]),
    (["ml", "ai-", "ai_", "llm", "deep-learning", "neural", "transformer", "alan-turing",
      "nlp", "neuroai", "nvidia-ai", "datascience", "data-science"],
     ["bbg-neural-networks.pdf", "bbg-transformers.pdf", "bbg-ml-pipelines.pdf",
      "bbg-embeddings.pdf", "bbg-rag.pdf", "bbg-llm-eval.pdf", "bbg-finetuning.pdf",
      "bbg-prompt-engineering.pdf", "bbg-vector-db.pdf", "bbg-backprop.pdf",
      "bbg-cnns.pdf", "bbg-mlops.pdf", "bbg-quantization.pdf", "bbg-xai.pdf",
      "bbg-fairness.pdf", "bbg-model-serving.pdf", "bbg-calculus-ml.pdf",
      "bbg-linear-algebra.pdf", "bbg-probability.pdf", "bbg-statistics.pdf"]),
    (["api", "microservice", "backend", "system-design", "fullstack", "spring", "dotnet"],
     ["bbg-microservices.pdf", "bbg-load-balancing.pdf", "bbg-caching-cdn.pdf",
      "bbg-oauth-flows.pdf", "bbg-rest-design.pdf", "bbg-graphql.pdf", "bbg-grpc.pdf",
      "bbg-api-gateway.pdf", "bbg-rate-limiting.pdf", "bbg-message-queues.pdf",
      "bbg-consistent-hashing.pdf", "bbg-circuit-breaker.pdf"]),
    (["linux", "rhcsa", "rhce", "sysadmin", "infra", "windows-admin", "m365", "systems"],
     ["bbg-tcp-handshake.pdf", "bbg-dns-resolution.pdf", "bbg-bash.pdf",
      "bbg-systemd.pdf", "bbg-permissions.pdf", "bbg-processes.pdf",
      "bbg-filesystem.pdf", "bbg-troubleshooting.pdf", "bbg-ssh.pdf",
      "bbg-boot.pdf", "bbg-cron.pdf", "bbg-packages.pdf", "bbg-selinux.pdf",
      "bbg-firewalld.pdf", "bbg-lvm-raid.pdf", "bbg-memory.pdf", "bbg-kernel.pdf"]),
    (["oauth", "auth", "identity", "vault-consul", "active-directory"],
     ["bbg-oauth-flows.pdf", "bbg-zero-trust.pdf", "bbg-jwt.pdf", "bbg-mfa.pdf",
      "bbg-oidc-saml.pdf", "bbg-password-hashing.pdf", "bbg-vault.pdf",
      "bbg-pki-encryption.pdf"]),
    (["dsa", "algorithm", "interview", "leetcode", "systems-cs", "embedded-interview",
      "android-interview", "ios-interview"],
     ["bbg-big-o.pdf", "bbg-sorting.pdf", "bbg-arrays.pdf", "bbg-hash-tables.pdf",
      "bbg-stacks-queues.pdf", "bbg-trees.pdf", "bbg-graphs.pdf", "bbg-dp.pdf",
      "bbg-recursion.pdf", "bbg-load-balancing.pdf", "bbg-caching-strategies.pdf",
      "bbg-consistent-hashing.pdf", "bbg-oop.pdf", "bbg-solid.pdf"]),
    (["python", "java", "c-lang", "cpp", "c_plus", "javascript", "react", "frontend",
      "creative-code", "enochian-programming", "python-systems", "python-web", "dotnet", "forge"],
     ["bbg-big-o.pdf", "bbg-arrays.pdf", "bbg-hash-tables.pdf", "bbg-oop.pdf",
      "bbg-solid.pdf", "bbg-git-internals.pdf", "bbg-recursion.pdf",
      "bbg-patterns-1.pdf", "bbg-async.pdf", "bbg-threads.pdf", "bbg-gc.pdf",
      "bbg-regex.pdf", "bbg-types.pdf"]),
    (["blockchain", "web3", "solidity", "smart-contract"],
     ["bbg-blockchain.pdf", "bbg-smart-contracts.pdf", "bbg-crypto-math.pdf",
      "bbg-p2p.pdf", "bbg-hashing.pdf", "bbg-consensus.pdf"]),
    (["mobile", "android", "ios", "flutter", "react-native"],
     ["bbg-mobile-arch.pdf", "bbg-api-gateway.pdf", "bbg-rest-design.pdf",
      "bbg-oauth-flows.pdf", "bbg-http-caching.pdf"]),
    (["math", "aleks", "statistics", "probability", "quant", "quantum"],
     ["bbg-statistics.pdf", "bbg-probability.pdf", "bbg-linear-algebra.pdf",
      "bbg-discrete-math.pdf", "bbg-calculus-ml.pdf", "bbg-info-theory.pdf",
      "bbg-queueing.pdf"]),
    (["db", "database", "oracle-db", "oracle-sql", "mongodb", "postgres", "mysql",
      "cassandra", "redis", "elasticsearch", "dynamodb", "nosql"],
     ["bbg-sql-fundamentals.pdf", "bbg-joins.pdf", "bbg-normalization.pdf",
      "bbg-db-indexing.pdf", "bbg-query-optimization.pdf", "bbg-db-replication.pdf",
      "bbg-db-sharding.pdf", "bbg-acid.pdf", "bbg-postgres.pdf", "bbg-mongodb.pdf",
      "bbg-redis.pdf", "bbg-nosql-types.pdf", "bbg-lsm-trees.pdf",
      "bbg-elasticsearch.pdf", "bbg-dynamodb.pdf", "bbg-cassandra.pdf",
      "bbg-newsql.pdf", "bbg-indexing-deep.pdf"]),
    (["comptia-a", "a-plus", "comptia-core", "helpdesk", "it-support", "fullstack-desk",
      "career-launch", "adaptive-foundations", "ms-fundamentals", "fundamentals"],
     ["bbg-tcp-handshake.pdf", "bbg-dns-resolution.pdf", "bbg-troubleshooting.pdf",
      "bbg-bash.pdf", "bbg-systemd.pdf", "bbg-ssh.pdf", "bbg-big-o.pdf",
      "bbg-git-internals.pdf"]),
    (["pmp", "agile", "scrum", "project", "leadership", "management", "entrepreneurship",
      "deep-work", "study-protocol", "career"],
     ["bbg-sre.pdf", "bbg-slis-slos.pdf", "bbg-incident-response.pdf",
      "bbg-chaos.pdf", "bbg-cost-optimization.pdf", "bbg-threat-modeling.pdf"]),
    (["web", "frontend", "react-frontend", "css", "browser"],
     ["bbg-browser-rendering.pdf", "bbg-css-layout.pdf", "bbg-http-caching.pdf",
      "bbg-web-security.pdf", "bbg-xss.pdf", "bbg-rest-design.pdf"]),
    (["acad-command"],
     ["bbg-zero-trust.pdf", "bbg-siem.pdf", "bbg-incident-response.pdf",
      "bbg-threat-modeling.pdf", "bbg-tls-handshake.pdf", "bbg-big-o.pdf"]),
    (["electrician", "hvac", "plumbing", "trade"],
     ["bbg-troubleshooting.pdf", "bbg-systemd.pdf"]),
]

DEFAULT_PDFS = ["bbg-cloud-patterns.pdf", "bbg-tls-handshake.pdf", "bbg-big-o.pdf"]

CAP = 6
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
wired_bootcamps = 0
wired_entries = 0
defaulted = []

for content_path in sorted(glob.glob(os.path.join(BOOTCAMP_DIR, "*/content.json"))):
    slug = os.path.basename(os.path.dirname(content_path))
    if slug == "_engine":
        continue
    slug_l = slug.lower()
    pdfs = []
    for keywords, plist in RULES:
        if any(k in slug_l for k in keywords):
            for p in plist:
                if p not in pdfs and p in PDFS:
                    pdfs.append(p)
    if not pdfs:
        pdfs = DEFAULT_PDFS
        defaulted.append(slug)
    pdfs = pdfs[:CAP]

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
        cat, title, desc = PDFS[pf]
        guides.append({
            "title": f"{title} — Visual Guide",
            "url": f"{BASE}/{pf}",
            "source": "Interstitium Labs",
            "blurb": desc,
            "pages": PAGES,
            "animated": True,
            "verifiedUtc": now,
        })
        added += 1
    if added:
        with open(content_path, "w") as f:
            json.dump(data, f, indent=1, ensure_ascii=False)
        with open(content_path) as f:
            json.load(f)  # validate
        wired_bootcamps += 1
        wired_entries += added

print(f"Bootcamps wired: {wired_bootcamps}")
print(f"PDF entries added: {wired_entries}")
print(f"Defaulted ({len(defaulted)}): {defaulted}")
print(f"Backups in: {BACKUP_DIR}")

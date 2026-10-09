"""Wire the 224 new BBG-style PDFs into course JSONs as `pdfs` arrays on relevant modules.
Extends wire_pdfs_courses.py (original 18). Backups -> course-json-backups-pdf2/."""
import json, os, shutil, datetime, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pdf_meta import PDFS, BASE, PAGES

COURSES_DIR = os.path.expanduser("~/workspace/apex-audit/docs/university/data/courses")
BACKUP_DIR = os.path.expanduser("~/workspace/apex-audit/.work/pdf-buildout/course-json-backups-pdf2")
os.makedirs(BACKUP_DIR, exist_ok=True)

# course file -> list of pdf slugs relevant to it
COURSE_MAP = {
    "il-02-mathematical-maturity-engine.json": [
        "bbg-calculus-ml.pdf", "bbg-linear-algebra.pdf", "bbg-discrete-math.pdf",
        "bbg-probability.pdf", "bbg-statistics.pdf", "bbg-info-theory.pdf",
        "bbg-queueing.pdf", "bbg-crypto-math.pdf", "bbg-graph-theory.pdf",
    ],
    "il-03-programming-language-forge.json": [
        "bbg-compilers.pdf", "bbg-git-internals.pdf", "bbg-oop.pdf", "bbg-solid.pdf",
        "bbg-functional.pdf", "bbg-recursion.pdf", "bbg-types.pdf", "bbg-async.pdf",
        "bbg-concurrency.pdf", "bbg-threads.pdf", "bbg-locks.pdf", "bbg-gc.pdf",
        "bbg-regex.pdf", "bbg-patterns-1.pdf", "bbg-patterns-2.pdf", "bbg-patterns-3.pdf",
        "bbg-hashing.pdf", "bbg-hash-tables.pdf", "bbg-memory.pdf", "bbg-processes.pdf",
    ],
    "il-04-systems-linux-windows-networks.json": [
        "bbg-tcp-handshake.pdf", "bbg-tcp-teardown.pdf", "bbg-udp.pdf",
        "bbg-dns-resolution.pdf", "bbg-dns-security.pdf", "bbg-tls-handshake.pdf",
        "bbg-subnets-cidr.pdf", "bbg-ipv4-ipv6.pdf", "bbg-osi-model.pdf", "bbg-nat.pdf",
        "bbg-dhcp.pdf", "bbg-vlans.pdf", "bbg-routing-protocols.pdf", "bbg-quic.pdf",
        "bbg-http2-http3.pdf", "bbg-arp-icmp.pdf", "bbg-anycast.pdf", "bbg-sdn.pdf",
        "bbg-bash.pdf", "bbg-systemd.pdf", "bbg-boot.pdf", "bbg-kernel.pdf",
        "bbg-cgroups.pdf", "bbg-processes.pdf", "bbg-threads.pdf", "bbg-memory.pdf",
        "bbg-filesystem.pdf", "bbg-lvm-raid.pdf", "bbg-permissions.pdf", "bbg-selinux.pdf",
        "bbg-firewalld.pdf", "bbg-packages.pdf", "bbg-cron.pdf", "bbg-net-commands.pdf",
        "bbg-troubleshooting.pdf", "bbg-ssh.pdf", "bbg-perf.pdf",
    ],
    "il-05-cloud-devsecops-platform-sre.json": [
        "bbg-cloud-patterns.pdf", "bbg-kubernetes.pdf", "bbg-k8s-workloads.pdf",
        "bbg-cicd-pipeline.pdf", "bbg-docker-deep.pdf", "bbg-containers-vms.pdf",
        "bbg-gitops.pdf", "bbg-helm.pdf", "bbg-terraform.pdf", "bbg-prometheus.pdf",
        "bbg-tracing.pdf", "bbg-elk.pdf", "bbg-chaos.pdf", "bbg-autoscaling.pdf",
        "bbg-blue-green.pdf", "bbg-canary.pdf", "bbg-feature-flags.pdf",
        "bbg-cost-optimization.pdf", "bbg-disaster-recovery.pdf", "bbg-sre.pdf",
        "bbg-slis-slos.pdf", "bbg-multi-region.pdf", "bbg-serverless.pdf",
        "bbg-orchestration-compared.pdf", "bbg-aws-core.pdf", "bbg-azure-core.pdf",
        "bbg-gcp-core.pdf",
    ],
    "il-06-cybersecurity-secure-engineering.json": [
        "bbg-zero-trust.pdf", "bbg-pki-encryption.pdf", "bbg-oauth-flows.pdf",
        "bbg-jwt.pdf", "bbg-mfa.pdf", "bbg-oidc-saml.pdf", "bbg-password-hashing.pdf",
        "bbg-hmac-signatures.pdf", "bbg-firewalls.pdf", "bbg-waf.pdf", "bbg-ddos.pdf",
        "bbg-csrf-ssrf.pdf", "bbg-xss.pdf", "bbg-sqli.pdf", "bbg-web-security.pdf",
        "bbg-pentest.pdf", "bbg-threat-modeling.pdf", "bbg-incident-response.pdf",
        "bbg-ir-playbooks.pdf", "bbg-forensics.pdf", "bbg-siem.pdf", "bbg-edr.pdf",
        "bbg-container-security.pdf", "bbg-supply-chain.pdf", "bbg-compliance.pdf",
        "bbg-vpns.pdf", "bbg-kms-hsm.pdf", "bbg-sast-dast.pdf",
    ],
    "il-07-data-engineering-analytics-ai.json": [
        "bbg-etl-pipelines.pdf", "bbg-elt.pdf", "bbg-airflow.pdf", "bbg-spark.pdf",
        "bbg-kafka-deep.pdf", "bbg-stream-processing.pdf", "bbg-cdc.pdf",
        "bbg-delta-lake.pdf", "bbg-dbt.pdf", "bbg-data-quality.pdf",
        "bbg-data-governance.pdf", "bbg-data-catalogs.pdf", "bbg-data-lineage.pdf",
        "bbg-data-versioning.pdf", "bbg-schema-evolution.pdf",
        "bbg-dimensional-modeling.pdf", "bbg-star-schema.pdf", "bbg-olap-oltp.pdf",
        "bbg-sql-fundamentals.pdf", "bbg-joins.pdf", "bbg-normalization.pdf",
        "bbg-data-warehouses.pdf", "bbg-snowflake.pdf", "bbg-elasticsearch.pdf",
        "bbg-timeseries.pdf", "bbg-migrations.pdf", "bbg-db-backup.pdf",
    ],
    "il-08-algorithms-compilers-distributed-formal.json": [
        "bbg-big-o.pdf", "bbg-arrays.pdf", "bbg-linked-lists.pdf", "bbg-stacks-queues.pdf",
        "bbg-hash-tables.pdf", "bbg-trees.pdf", "bbg-btrees.pdf", "bbg-heaps.pdf",
        "bbg-graphs.pdf", "bbg-graph-theory.pdf", "bbg-sorting.pdf", "bbg-searching.pdf",
        "bbg-recursion.pdf", "bbg-dp.pdf", "bbg-discrete-math.pdf", "bbg-info-theory.pdf",
        "bbg-bloom-filters.pdf", "bbg-consistent-hashing.pdf", "bbg-cap-theorem.pdf",
        "bbg-consensus.pdf", "bbg-2pc.pdf", "bbg-crdts.pdf", "bbg-vector-clocks.pdf",
        "bbg-p2p.pdf", "bbg-queueing.pdf", "bbg-compilers.pdf",
    ],
    "il-09-adaptive-certification-command.json": [
        "bbg-big-o.pdf", "bbg-load-balancing.pdf", "bbg-tcp-handshake.pdf",
        "bbg-zero-trust.pdf", "bbg-sql-fundamentals.pdf",
    ],
    "il-11-zero-trust-endpoint-defense.json": [
        "bbg-zero-trust.pdf", "bbg-edr.pdf", "bbg-siem.pdf", "bbg-threat-modeling.pdf",
        "bbg-incident-response.pdf", "bbg-vpns.pdf", "bbg-firewalls.pdf",
        "bbg-container-security.pdf", "bbg-forensics.pdf", "bbg-ir-playbooks.pdf",
    ],
    "il-12-ai-engineering.json": [
        "bbg-neural-networks.pdf", "bbg-transformers.pdf", "bbg-attention-deep.pdf",
        "bbg-backprop.pdf", "bbg-cnns.pdf", "bbg-rnns.pdf", "bbg-gans.pdf",
        "bbg-diffusion.pdf", "bbg-embeddings.pdf", "bbg-bert-gpt.pdf", "bbg-finetuning.pdf",
        "bbg-quantization.pdf", "bbg-prompt-engineering.pdf", "bbg-rag.pdf",
        "bbg-llm-eval.pdf", "bbg-xai.pdf", "bbg-fairness.pdf", "bbg-federated.pdf",
        "bbg-distributed-training.pdf", "bbg-rl.pdf", "bbg-mlops.pdf",
        "bbg-ml-pipelines.pdf", "bbg-model-drift.pdf", "bbg-model-serving.pdf",
        "bbg-feature-engineering.pdf", "bbg-vector-db.pdf", "bbg-semantic-search.pdf",
        "bbg-calculus-ml.pdf", "bbg-linear-algebra.pdf", "bbg-probability.pdf",
        "bbg-statistics.pdf",
    ],
    "il-13-software-engineering-interview-prep.json": [
        "bbg-big-o.pdf", "bbg-sorting.pdf", "bbg-arrays.pdf", "bbg-hash-tables.pdf",
        "bbg-stacks-queues.pdf", "bbg-trees.pdf", "bbg-graphs.pdf", "bbg-dp.pdf",
        "bbg-recursion.pdf", "bbg-load-balancing.pdf", "bbg-caching-strategies.pdf",
        "bbg-consistent-hashing.pdf", "bbg-microservices.pdf", "bbg-rest-design.pdf",
        "bbg-api-gateway.pdf", "bbg-rate-limiting.pdf", "bbg-message-queues.pdf",
        "bbg-oop.pdf", "bbg-solid.pdf", "bbg-git-internals.pdf",
    ],
    "il-14-sre-devops-cloud-security-interview-prep.json": [
        "bbg-sre.pdf", "bbg-slis-slos.pdf", "bbg-incident-response.pdf",
        "bbg-troubleshooting.pdf", "bbg-kubernetes.pdf", "bbg-cicd-pipeline.pdf",
        "bbg-terraform.pdf", "bbg-prometheus.pdf", "bbg-tracing.pdf", "bbg-chaos.pdf",
        "bbg-disaster-recovery.pdf", "bbg-cloud-patterns.pdf", "bbg-zero-trust.pdf",
        "bbg-autoscaling.pdf", "bbg-blue-green.pdf", "bbg-canary.pdf", "bbg-gitops.pdf",
        "bbg-docker-deep.pdf", "bbg-bash.pdf", "bbg-systemd.pdf",
    ],
    "il-15-data-engineering-analytics-interview-prep.json": [
        "bbg-sql-fundamentals.pdf", "bbg-joins.pdf", "bbg-normalization.pdf",
        "bbg-etl-pipelines.pdf", "bbg-elt.pdf", "bbg-airflow.pdf", "bbg-spark.pdf",
        "bbg-kafka-deep.pdf", "bbg-star-schema.pdf", "bbg-dimensional-modeling.pdf",
        "bbg-dbt.pdf", "bbg-data-warehouses.pdf", "bbg-snowflake.pdf",
        "bbg-stream-processing.pdf", "bbg-probability.pdf", "bbg-statistics.pdf",
        "bbg-query-optimization.pdf", "bbg-data-quality.pdf", "bbg-cdc.pdf",
    ],
    "il-16-machine-learning-ai-engineering.json": [
        "bbg-neural-networks.pdf", "bbg-transformers.pdf", "bbg-backprop.pdf",
        "bbg-cnns.pdf", "bbg-rnns.pdf", "bbg-embeddings.pdf", "bbg-finetuning.pdf",
        "bbg-quantization.pdf", "bbg-rag.pdf", "bbg-mlops.pdf", "bbg-ml-pipelines.pdf",
        "bbg-model-drift.pdf", "bbg-model-serving.pdf", "bbg-feature-engineering.pdf",
        "bbg-llm-eval.pdf", "bbg-xai.pdf", "bbg-fairness.pdf",
        "bbg-distributed-training.pdf", "bbg-rl.pdf", "bbg-calculus-ml.pdf",
        "bbg-linear-algebra.pdf", "bbg-probability.pdf", "bbg-statistics.pdf",
        "bbg-info-theory.pdf",
    ],
    "il-17-agentic-ai-engineering.json": [
        "bbg-transformers.pdf", "bbg-attention-deep.pdf", "bbg-prompt-engineering.pdf",
        "bbg-rag.pdf", "bbg-llm-eval.pdf", "bbg-embeddings.pdf", "bbg-vector-db.pdf",
        "bbg-semantic-search.pdf", "bbg-quantization.pdf", "bbg-model-serving.pdf",
        "bbg-bert-gpt.pdf", "bbg-xai.pdf",
    ],
    "il-18-technical-leadership-interview-prep.json": [
        "bbg-sre.pdf", "bbg-slis-slos.pdf", "bbg-incident-response.pdf", "bbg-chaos.pdf",
        "bbg-cost-optimization.pdf", "bbg-microservices.pdf", "bbg-cap-theorem.pdf",
        "bbg-scaling.pdf", "bbg-disaster-recovery.pdf", "bbg-threat-modeling.pdf",
    ],
    "il-19-multicloud-devops-ai-bootcamp.json": [
        "bbg-aws-core.pdf", "bbg-azure-core.pdf", "bbg-gcp-core.pdf", "bbg-terraform.pdf",
        "bbg-kubernetes.pdf", "bbg-k8s-workloads.pdf", "bbg-cicd-pipeline.pdf",
        "bbg-gitops.pdf", "bbg-cloud-patterns.pdf", "bbg-multi-region.pdf",
        "bbg-cost-optimization.pdf", "bbg-disaster-recovery.pdf", "bbg-docker-deep.pdf",
        "bbg-serverless.pdf",
    ],
    "il-20-mathematics.json": [
        "bbg-calculus-ml.pdf", "bbg-linear-algebra.pdf", "bbg-discrete-math.pdf",
        "bbg-probability.pdf", "bbg-statistics.pdf", "bbg-info-theory.pdf",
        "bbg-queueing.pdf", "bbg-crypto-math.pdf", "bbg-graph-theory.pdf",
    ],
    "il-24-threatlocker-assessment-prep-cbt.json": [
        "bbg-zero-trust.pdf", "bbg-tls-handshake.pdf", "bbg-tcp-handshake.pdf",
        "bbg-dns-resolution.pdf", "bbg-edr.pdf", "bbg-siem.pdf", "bbg-threat-modeling.pdf",
        "bbg-incident-response.pdf", "bbg-vpns.pdf", "bbg-firewalls.pdf",
        "bbg-selinux.pdf", "bbg-systemd.pdf", "bbg-boot.pdf", "bbg-permissions.pdf",
        "bbg-ssh.pdf", "bbg-mfa.pdf",
    ],
    "il-25-cybersecurity-professional-certificate.json": [
        "bbg-zero-trust.pdf", "bbg-pki-encryption.pdf", "bbg-oauth-flows.pdf",
        "bbg-jwt.pdf", "bbg-mfa.pdf", "bbg-oidc-saml.pdf", "bbg-password-hashing.pdf",
        "bbg-hmac-signatures.pdf", "bbg-firewalls.pdf", "bbg-waf.pdf", "bbg-ddos.pdf",
        "bbg-csrf-ssrf.pdf", "bbg-xss.pdf", "bbg-sqli.pdf", "bbg-web-security.pdf",
        "bbg-pentest.pdf", "bbg-threat-modeling.pdf", "bbg-incident-response.pdf",
        "bbg-ir-playbooks.pdf", "bbg-forensics.pdf", "bbg-siem.pdf", "bbg-edr.pdf",
        "bbg-compliance.pdf", "bbg-vpns.pdf", "bbg-kms-hsm.pdf", "bbg-sast-dast.pdf",
        "bbg-tls-handshake.pdf", "bbg-tcp-handshake.pdf",
    ],
    "il-26-data-analyst-certification-senior-mastery.json": [
        "bbg-sql-fundamentals.pdf", "bbg-joins.pdf", "bbg-normalization.pdf",
        "bbg-star-schema.pdf", "bbg-dimensional-modeling.pdf", "bbg-olap-oltp.pdf",
        "bbg-data-quality.pdf", "bbg-data-governance.pdf", "bbg-data-lineage.pdf",
        "bbg-data-catalogs.pdf", "bbg-dbt.pdf", "bbg-statistics.pdf", "bbg-probability.pdf",
        "bbg-etl-pipelines.pdf", "bbg-elt.pdf", "bbg-airflow.pdf",
        "bbg-data-warehouses.pdf", "bbg-snowflake.pdf", "bbg-elasticsearch.pdf",
        "bbg-timeseries.pdf", "bbg-query-optimization.pdf",
    ],
    "il-27-it-infrastructure-specialist-threatlocker-mastery.json": [
        "bbg-tcp-handshake.pdf", "bbg-tcp-teardown.pdf", "bbg-udp.pdf",
        "bbg-dns-resolution.pdf", "bbg-dhcp.pdf", "bbg-subnets-cidr.pdf", "bbg-vlans.pdf",
        "bbg-nat.pdf", "bbg-osi-model.pdf", "bbg-troubleshooting.pdf",
        "bbg-net-commands.pdf", "bbg-ssh.pdf", "bbg-firewalld.pdf", "bbg-systemd.pdf",
        "bbg-boot.pdf", "bbg-lvm-raid.pdf", "bbg-db-backup.pdf",
        "bbg-disaster-recovery.pdf", "bbg-vpns.pdf", "bbg-zero-trust.pdf", "bbg-mfa.pdf",
        "bbg-incident-response.pdf",
    ],
    "il-28-devsecops-cloud-infrastructure-mastery.json": [
        "bbg-cloud-patterns.pdf", "bbg-kubernetes.pdf", "bbg-k8s-workloads.pdf",
        "bbg-cicd-pipeline.pdf", "bbg-gitops.pdf", "bbg-terraform.pdf",
        "bbg-docker-deep.pdf", "bbg-container-security.pdf", "bbg-supply-chain.pdf",
        "bbg-vault.pdf", "bbg-prometheus.pdf", "bbg-tracing.pdf", "bbg-elk.pdf",
        "bbg-sast-dast.pdf", "bbg-password-hashing.pdf", "bbg-oauth-flows.pdf",
        "bbg-siem.pdf", "bbg-autoscaling.pdf", "bbg-blue-green.pdf", "bbg-helm.pdf",
        "bbg-serverless.pdf",
    ],
    "il-29-threatlocker-ai-cybersecurity-mastery.json": [
        "bbg-zero-trust.pdf", "bbg-neural-networks.pdf", "bbg-threat-modeling.pdf",
        "bbg-edr.pdf", "bbg-siem.pdf", "bbg-tls-handshake.pdf",
        "bbg-prompt-engineering.pdf", "bbg-incident-response.pdf", "bbg-forensics.pdf",
        "bbg-ir-playbooks.pdf", "bbg-supply-chain.pdf", "bbg-container-security.pdf",
        "bbg-xai.pdf", "bbg-fairness.pdf",
    ],
}

now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
wired = 0
skipped = 0
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
    for i, pdf_file in enumerate(pdf_list):
        if pdf_file not in PDFS:
            print("SKIP (unknown pdf):", pdf_file); skipped += 1; continue
        cat, title, desc = PDFS[pdf_file]
        mod = modules[i % len(modules)]
        pdfs = mod.setdefault("pdfs", [])
        if any(p.get("url", "").endswith(pdf_file) for p in pdfs):
            continue
        pdfs.append({
            "title": f"{title} — Visual Guide",
            "url": f"{BASE}/{pdf_file}",
            "source": "Interstitium Labs",
            "blurb": desc,
            "pages": PAGES,
            "animated": True,
            "verifiedUtc": now,
            "httpStatus": 200,
        })
        wired += 1
    with open(path, "w") as f:
        json.dump(course, f, indent=1, ensure_ascii=False)
    # validate
    with open(path) as f:
        json.load(f)
    print(f"wired {course_file}: +{len(pdf_list)} pdfs")

print(f"\nTotal pdf entries wired: {wired} (skipped unknown: {skipped})")
print(f"Backups in: {BACKUP_DIR}")

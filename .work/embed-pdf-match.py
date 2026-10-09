#!/usr/bin/env python3
"""Keyword-match modules to PDF guides; emit assignments + review table.
Does NOT edit course JSONs."""
import json, os, re

BASE = os.path.expanduser("~/workspace/apex-audit/docs/university/data/courses")
WORK = os.path.expanduser("~/workspace/apex-audit/.work")
PDF_BASE = "https://interstitiumlabs.dev/assets/pdfs"

CATALOG = [
 # (slug, title, blurb, keywords)
 ("bbg-zero-trust", "Zero Trust Architecture \u2014 Visual Guide",
  "Animated step-by-step: tenets, identity perimeter, micro-segmentation, pillars.",
  ["zero trust","ztna","microsegmentation","micro-segmentation","least privilege","never trust","identity perimeter","endpoint defense","endpoint security","allowlist","allow list","deny by default","default-deny","default deny","application control","ringfenc","threatlocker","policy engine","attack graph","threat hunting","edr","xdr","soc"]),
 ("bbg-tls-handshake", "TLS Handshake \u2014 Visual Guide",
  "Animated step-by-step: cipher suites, key exchange, certificates in motion.",
  ["tls","ssl","https","cipher suite","key exchange","handshake"]),
 ("bbg-pki-encryption", "PKI & Encryption \u2014 Visual Guide",
  "Animated step-by-step: CAs, certificates, symmetric/asymmetric keys.",
  ["pki","public key","private key","rsa","diffie","digital signature","certificate authority","hashing","cryptographic","cryptography","encryption","aes","sha-","md5","number theory","modular arithmetic"]),
 ("bbg-oauth-flows", "OAuth 2.0 & OIDC Flows \u2014 Visual Guide",
  "Animated step-by-step: grants, tokens, scopes, SSO.",
  ["oauth","oidc","openid","saml","jwt","sso","single sign-on","multi-factor","mfa","passkey","authentication","authorization","identity and access","iam","rbac","abac","active directory","ldap","kerberos","credential","token"]),
 ("bbg-dns-resolution", "DNS Resolution \u2014 Visual Guide",
  "Animated step-by-step: recursive/iterative queries, records, caching.",
  ["dns","domain name","resolver","cname","a record","aaaa","mx record","name resolution","dhcp"]),
 ("bbg-tcp-handshake", "TCP 3-Way Handshake \u2014 Visual Guide",
  "Animated step-by-step: SYN/SYN-ACK/ACK, reliability, flow control, closing.",
  ["tcp","three-way","syn","packet","socket","osi","subnet","vlan","ip address","networking","latency","udp","icmp","wireshark","osi model","ethernet","switching","routing","router","firewall"]),
 ("bbg-load-balancing", "Load Balancing \u2014 Visual Guide",
  "Animated step-by-step: algorithms, health checks, scaling traffic.",
  ["load balanc","high availability","failover","reverse proxy","nginx","haproxy","traffic distribution","autoscal","scaling"]),
 ("bbg-caching-cdn", "Caching & CDNs \u2014 Visual Guide",
  "Animated step-by-step: cache layers, TTL, edge delivery.",
  ["cach","cdn","content delivery","edge server","edge cache","edge location","at the edge","redis","memcached","ttl","varnish"]),
 ("bbg-microservices", "Microservices \u2014 Visual Guide",
  "Animated step-by-step: decomposition, contracts, service mesh.",
  ["microservice","service mesh","api gateway","monolith","containerization","container","docker","rest","graphql","api design"]),
 ("bbg-cloud-patterns", "Cloud Architecture Patterns \u2014 Visual Guide",
  "Animated step-by-step: regions/AZs, auto-scaling, queues, IaC, well-architected.",
  ["cloud","aws","azure","gcp","serverless","iaas","paas","saas","well-architected","shared responsibility","terraform","iac","infrastructure as code","s3","ec2"]),
 ("bbg-kubernetes", "Kubernetes \u2014 Visual Guide",
  "Animated step-by-step: pods, services, deployments, scheduling.",
  ["kubernetes","k8s","pod","helm","orchestration","kubectl","deployment","replicaset","ingress"]),
 ("bbg-cicd-pipeline", "CI/CD Pipelines \u2014 Visual Guide",
  "Animated step-by-step: build, test, deploy stages, GitOps.",
  ["ci/cd","cicd","continuous integration","continuous deployment","continuous delivery","jenkins","github actions","gitlab","gitops","devops","sdlc","release","artifact","canary","blue-green","pipeline"]),
 ("bbg-neural-networks", "Neural Networks \u2014 Visual Guide",
  "Animated step-by-step: perceptrons, backpropagation, layers.",
  ["neural network","deep learning","perceptron","backprop","cnn","rnn","lstm","gradient descent","activation function"]),
 ("bbg-transformers", "Transformers & Attention \u2014 Visual Guide",
  "Animated step-by-step: attention, encoder/decoder, the model family.",
  ["transformer","attention","llm","gpt","bert","embedding","tokeniz","prompt","rag","retrieval-augmented","fine-tun","agent","agentic"]),
 ("bbg-ml-pipelines", "ML Pipelines \u2014 Visual Guide",
  "Animated step-by-step: training, evaluation, deployment, monitoring.",
  ["machine learning","mlops","model training","feature engineering","supervised","unsupervised","classification","regression","clustering","anomaly detection","anomaly","overfit","cross-validation","confusion matrix","precision","recall","f1","ml","ai"]),
 ("bbg-etl-pipelines", "ETL Data Pipelines \u2014 Visual Guide",
  "Animated step-by-step: extract/transform/load, DAGs, quality tests, medallion.",
  ["etl","elt","data pipeline","data ingestion","spark","airflow","dag","dbt","medallion","bronze","silver","gold","data engineer","data lake","ingest"]),
 ("bbg-stream-processing", "Stream Processing \u2014 Visual Guide",
  "Animated step-by-step: events, windows, exactly-once, Kafka-style flows.",
  ["stream processing","kafka","real-time","event-driven","flink","windowing","event stream","streaming"]),
 ("bbg-data-warehouses", "Data Warehouses \u2014 Visual Guide",
  "Animated step-by-step: star schema, OLAP, partitioning, the modern stack.",
  ["data warehouse","snowflake","bigquery","redshift","olap","star schema","dimensional","data mart","lakehouse","sql","window function","cte","pandas","numpy","excel","tableau","power bi","dashboard","kpi","descriptive statistic","hypothesis","a/b","bayes","probability","distribution","variance","correlation","analytics","data analyst","business intelligence","oltp","normalization","schema","join","group by","order by","aggregate"]),
]

FALLBACK = {
    "il-24-threatlocker-assessment-prep-cbt": ["bbg-zero-trust","bbg-tls-handshake","bbg-pki-encryption","bbg-oauth-flows"],
    "il-25-cybersecurity-professional-certificate": ["bbg-zero-trust","bbg-pki-encryption","bbg-tls-handshake","bbg-oauth-flows"],
    "il-26-data-analyst-certification-senior-mastery": ["bbg-data-warehouses","bbg-etl-pipelines","bbg-stream-processing"],
    "il-27-it-infrastructure-specialist-threatlocker-mastery": ["bbg-zero-trust","bbg-tcp-handshake","bbg-dns-resolution","bbg-tls-handshake"],
    "il-28-devsecops-cloud-infrastructure-mastery": ["bbg-kubernetes","bbg-cicd-pipeline","bbg-cloud-patterns","bbg-load-balancing"],
    "il-29-threatlocker-ai-cybersecurity-mastery": ["bbg-zero-trust","bbg-tls-handshake","bbg-pki-encryption","bbg-oauth-flows"],
}

OVERRIDES = {
    ("il-24-threatlocker-assessment-prep-cbt","m24-ueba"): ["bbg-ml-pipelines","bbg-data-warehouses"],
    ("il-24-threatlocker-assessment-prep-cbt","m24-capstone"): ["bbg-ml-pipelines","bbg-zero-trust"],
    ("il-25-cybersecurity-professional-certificate","IL25-M06"): ["bbg-oauth-flows","bbg-zero-trust"],
    ("il-25-cybersecurity-professional-certificate","IL25-M11"): ["bbg-zero-trust","bbg-etl-pipelines"],
    ("il-25-cybersecurity-professional-certificate","IL25-M12"): ["bbg-zero-trust","bbg-tcp-handshake"],
    ("il-25-cybersecurity-professional-certificate","IL25-M17"): ["bbg-zero-trust","bbg-tcp-handshake"],
    ("il-25-cybersecurity-professional-certificate","IL25-M22"): ["bbg-zero-trust","bbg-pki-encryption"],
    ("il-25-cybersecurity-professional-certificate","IL25-M24"): ["bbg-zero-trust","bbg-tcp-handshake"],
    ("il-25-cybersecurity-professional-certificate","IL25-M08"): ["bbg-zero-trust","bbg-pki-encryption"],
    ("il-25-cybersecurity-professional-certificate","IL25-M19"): ["bbg-tcp-handshake","bbg-zero-trust"],
    ("il-25-cybersecurity-professional-certificate","IL-25-PM-NUMTH"): ["bbg-pki-encryption","bbg-tls-handshake"],
    ("il-26-data-analyst-certification-senior-mastery","IL26-M13"): ["bbg-etl-pipelines","bbg-stream-processing"],
    ("il-26-data-analyst-certification-senior-mastery","IL26-M14"): ["bbg-data-warehouses","bbg-cloud-patterns"],
    ("il-26-data-analyst-certification-senior-mastery","IL26-M37"): ["bbg-etl-pipelines","bbg-data-warehouses"],
    ("il-26-data-analyst-certification-senior-mastery","IL26-M39"): ["bbg-data-warehouses","bbg-etl-pipelines"],
    ("il-26-data-analyst-certification-senior-mastery","IL26-M21"): ["bbg-data-warehouses","bbg-etl-pipelines"],
    ("il-26-data-analyst-certification-senior-mastery","IL26-M24"): ["bbg-data-warehouses","bbg-etl-pipelines"],
    ("il-26-data-analyst-certification-senior-mastery","IL26-M40"): ["bbg-data-warehouses","bbg-etl-pipelines"],
    ("il-26-data-analyst-certification-senior-mastery","IL26-M45"): ["bbg-stream-processing","bbg-data-warehouses"],
    ("il-27-it-infrastructure-specialist-threatlocker-mastery","IL27-M04"): ["bbg-zero-trust","bbg-tcp-handshake"],
    ("il-27-it-infrastructure-specialist-threatlocker-mastery","IL27-M09"): ["bbg-tcp-handshake","bbg-tls-handshake"],
    ("il-27-it-infrastructure-specialist-threatlocker-mastery","IL27-M11"): ["bbg-zero-trust","bbg-tcp-handshake"],
    ("il-27-it-infrastructure-specialist-threatlocker-mastery","IL27-M12"): ["bbg-oauth-flows","bbg-zero-trust"],
    ("il-27-it-infrastructure-specialist-threatlocker-mastery","IL27-M15"): ["bbg-zero-trust","bbg-cicd-pipeline"],
    ("il-27-it-infrastructure-specialist-threatlocker-mastery","IL27-M18"): ["bbg-cloud-patterns","bbg-load-balancing"],
    ("il-27-it-infrastructure-specialist-threatlocker-mastery","IL27-M19"): ["bbg-cloud-patterns","bbg-zero-trust"],
    ("il-27-it-infrastructure-specialist-threatlocker-mastery","IL27-M32"): ["bbg-stream-processing","bbg-etl-pipelines"],
    ("il-27-it-infrastructure-specialist-threatlocker-mastery","IL27-M34"): ["bbg-stream-processing","bbg-tcp-handshake"],
    ("il-27-it-infrastructure-specialist-threatlocker-mastery","IL27-M35"): ["bbg-load-balancing","bbg-cloud-patterns"],
    ("il-27-it-infrastructure-specialist-threatlocker-mastery","IL27-M23"): ["bbg-dns-resolution","bbg-cicd-pipeline"],
    ("il-27-it-infrastructure-specialist-threatlocker-mastery","IL27-MX03"): ["bbg-tcp-handshake","bbg-dns-resolution"],
    ("il-27-it-infrastructure-specialist-threatlocker-mastery","IL27-M39"): ["bbg-zero-trust","bbg-tcp-handshake"],
    ("il-27-it-infrastructure-specialist-threatlocker-mastery","IL27-FT02"): ["bbg-zero-trust","bbg-tcp-handshake"],
    ("il-28-devsecops-cloud-infrastructure-mastery","IL28-M06"): ["bbg-load-balancing","bbg-cloud-patterns"],
    ("il-28-devsecops-cloud-infrastructure-mastery","IL28-M15"): ["bbg-load-balancing","bbg-tls-handshake"],
    ("il-28-devsecops-cloud-infrastructure-mastery","IL28-M34"): ["bbg-cloud-patterns","bbg-cicd-pipeline"],
    ("il-28-devsecops-cloud-infrastructure-mastery","IL28-M38"): ["bbg-cicd-pipeline","bbg-cloud-patterns"],
    ("il-28-devsecops-cloud-infrastructure-mastery","IL28-M45"): ["bbg-stream-processing","bbg-etl-pipelines"],
    ("il-28-devsecops-cloud-infrastructure-mastery","IL28-M46"): ["bbg-load-balancing","bbg-cloud-patterns"],
    ("il-28-devsecops-cloud-infrastructure-mastery","IL-28-PM-LOGIC"): ["bbg-kubernetes","bbg-cicd-pipeline"],
    ("il-28-devsecops-cloud-infrastructure-mastery","IL-28-PM-NUMTH"): ["bbg-pki-encryption","bbg-tls-handshake"],
    ("il-29-threatlocker-ai-cybersecurity-mastery","IL29-M08"): ["bbg-zero-trust","bbg-cicd-pipeline"],
    ("il-29-threatlocker-ai-cybersecurity-mastery","IL29-M09"): ["bbg-zero-trust","bbg-oauth-flows"],
    ("il-29-threatlocker-ai-cybersecurity-mastery","IL29-M10"): ["bbg-zero-trust","bbg-tcp-handshake"],
    ("il-29-threatlocker-ai-cybersecurity-mastery","IL29-M11"): ["bbg-zero-trust","bbg-tcp-handshake"],
    ("il-29-threatlocker-ai-cybersecurity-mastery","IL29-M12"): ["bbg-zero-trust","bbg-cicd-pipeline"],
    ("il-29-threatlocker-ai-cybersecurity-mastery","IL29-M17"): ["bbg-oauth-flows","bbg-tls-handshake"],
    ("il-29-threatlocker-ai-cybersecurity-mastery","IL29-M19"): ["bbg-zero-trust","bbg-pki-encryption"],
    ("il-29-threatlocker-ai-cybersecurity-mastery","IL29-M21"): ["bbg-pki-encryption","bbg-tls-handshake"],
    ("il-29-threatlocker-ai-cybersecurity-mastery","IL29-M23"): ["bbg-ml-pipelines","bbg-stream-processing"],
    ("il-29-threatlocker-ai-cybersecurity-mastery","IL29-M28"): ["bbg-pki-encryption","bbg-zero-trust"],
    ("il-29-threatlocker-ai-cybersecurity-mastery","IL29-M29"): ["bbg-pki-encryption","bbg-tcp-handshake"],
    ("il-29-threatlocker-ai-cybersecurity-mastery","IL29-M37"): ["bbg-zero-trust","bbg-tls-handshake"],
    ("il-29-threatlocker-ai-cybersecurity-mastery","IL29-M38"): ["bbg-zero-trust","bbg-tls-handshake"],
    ("il-29-threatlocker-ai-cybersecurity-mastery","IL29-M40"): ["bbg-zero-trust","bbg-tcp-handshake"],
    ("il-29-threatlocker-ai-cybersecurity-mastery","IL29-M42"): ["bbg-pki-encryption","bbg-zero-trust"],
    ("il-29-threatlocker-ai-cybersecurity-mastery","IL29-M47"): ["bbg-zero-trust","bbg-tls-handshake"],
}

LIBRARY_COURSES = {"il-21-humanities","il-22-esoteric-secret-knowledge","il-23-frontier-knowledge"}
COURSES = list(FALLBACK.keys()) + sorted(LIBRARY_COURSES)

def text_of(m):
    parts = [m.get("title",""), m.get("summary","")]
    parts += m.get("objectives", []) or []
    return " ".join(parts).lower()

def kw_hit(text, kw):
    kw = kw.strip()
    if " " not in kw and len(kw) <= 4:
        return re.search(r"\b" + re.escape(kw) + r"\b", text) is not None
    return kw in text

assignments, review_lines = {}, []
for c in COURSES:
    d = json.load(open(os.path.join(BASE, c + ".json")))
    review_lines.append(f"##### {c}")
    for m in d["modules"]:
        mid = m.get("id")
        existing = {(p.get("url") or "") for p in (m.get("pdfs") or [])}
        need = 2 - len(existing)
        if c in LIBRARY_COURSES:
            picks = ["LIBRARY", "LIBRARY2"][:max(need, 0)]
            assignments.setdefault(c, {})[mid] = picks
            review_lines.append(f"{mid} | {m.get('title','')[:60]} | -> library x{len(picks)}")
            continue
        if need <= 0:
            assignments.setdefault(c, {})[mid] = []
            continue
        if (c, mid) in OVERRIDES:
            picks = [s for s in OVERRIDES[(c, mid)] if f"{PDF_BASE}/{s}.pdf" not in existing][:need]
            assignments.setdefault(c, {})[mid] = picks
            review_lines.append(f"{mid} | {m.get('title','')[:55]} | need={need} -> {picks} | [override]")
            continue
        text = text_of(m)
        title = m.get("title", "").lower()
        scored = []
        for slug, stitle, blurb, kws in CATALOG:
            if f"{PDF_BASE}/{slug}.pdf" in existing:
                continue
            hits = [k for k in kws if kw_hit(text, k)]
            thits = [k for k in kws if kw_hit(title, k)]
            if hits:
                scored.append((len(thits), len(hits), slug, hits))
        # title matches break ties first: a guide named in the module title wins
        scored.sort(key=lambda t: (t[0], t[1], t[2]), reverse=True)
        picks, reasons = [], []
        for nth, n, slug, hits in scored:
            if len(picks) >= need: break
            picks.append(slug); reasons.append(f"{slug}:{n}kw" + (f"+{nth}T" if nth else ""))
        for slug in FALLBACK[c]:
            if len(picks) >= need: break
            if f"{PDF_BASE}/{slug}.pdf" in existing or slug in picks: continue
            picks.append(slug); reasons.append(f"{slug}:fallback")
        assignments.setdefault(c, {})[mid] = picks
        review_lines.append(f"{mid} | {m.get('title','')[:55]} | need={need} -> {picks} | {reasons}")

json.dump(assignments, open(os.path.join(WORK, "embed-pdf-assignments.json"), "w"), indent=1)
open(os.path.join(WORK, "embed-pdf-review.txt"), "w").write("\n".join(review_lines))
print("courses:", len(assignments))
print("total picks:", sum(len(v) for c in assignments.values() for v in c.values()))

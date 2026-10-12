#!/usr/bin/env python3
"""Embed gap-fill: wire 2-3 relevant PDFs into every module of il-07..il-12.
Preserves existing pdfs; tops up to exactly 3 per module.
Does NOT touch: videos, handsOnLab, glossary, quiz, cards, drills.
Depth check: every module must already have 3+ quiz, 5+ cards, 1+ drills."""
import json, shutil, os, sys
from datetime import datetime

BASE = os.path.expanduser("~/workspace/apex-audit")
COURSES = os.path.join(BASE, "docs/university/data/courses")
BACKUP = os.path.join(BASE, ".work/course-json-backups-embed")
os.makedirs(BACKUP, exist_ok=True)

PDFS = {
 "bbg-load-balancing": ("Load Balancing — Visual Guide",
   "https://interstitiumlabs.dev/assets/pdfs/bbg-load-balancing.pdf",
   "Animated step-by-step: algorithms, health checks, L4 vs L7, global load balancing.",
   ["load balanc","balancing","traffic","availability","failover","redundan","scale-out","high avail"]),
 "bbg-caching-cdn": ("Caching & CDNs — Visual Guide",
   "https://interstitiumlabs.dev/assets/pdfs/bbg-caching-cdn.pdf",
   "Animated step-by-step: cache-aside, invalidation, edge networks, hit ratios.",
   ["cach","cdn","edge network","latency","content delivery","cache-aside"]),
 "bbg-microservices": ("Microservices Architecture — Visual Guide",
   "https://interstitiumlabs.dev/assets/pdfs/bbg-microservices.pdf",
   "Animated step-by-step: decomposition, sync vs async, resilience, observability.",
   ["microservice","service mesh","soa","distributed system","container orchestration","api design","decompos"]),
 "bbg-tcp-handshake": ("TCP 3-Way Handshake — Visual Guide",
   "https://interstitiumlabs.dev/assets/pdfs/bbg-tcp-handshake.pdf",
   "Animated step-by-step: SYN/SYN-ACK/ACK, reliability, flow control, closing.",
   ["tcp","three-way","handshake","socket","transport layer","flow control","binary","hex","bit ","packet"]),
 "bbg-dns-resolution": ("DNS Resolution — Visual Guide",
   "https://interstitiumlabs.dev/assets/pdfs/bbg-dns-resolution.pdf",
   "Animated step-by-step: caches, root/TLD/authoritative, record types, DNSSEC/DoT/DoH.",
   ["dns","domain name","record type","nameserver","authoritative"]),
 "bbg-tls-handshake": ("TLS Handshake — Visual Guide",
   "https://interstitiumlabs.dev/assets/pdfs/bbg-tls-handshake.pdf",
   "Animated step-by-step: ClientHello, certificates, ECDHE, forward secrecy, TLS 1.3.",
   ["tls","ssl","certificate","https","cipher","forward secrecy","clienthello","x.509"]),
 "bbg-cloud-patterns": ("Cloud Architecture Patterns — Visual Guide",
   "https://interstitiumlabs.dev/assets/pdfs/bbg-cloud-patterns.pdf",
   "Animated step-by-step: regions/AZs, auto-scaling, queues, IaC, well-architected.",
   ["cloud","aws","azure","gcp","serverless","well-architected","region","iaas","paas","startup infra"]),
 "bbg-kubernetes": ("Kubernetes Architecture — Visual Guide",
   "https://interstitiumlabs.dev/assets/pdfs/bbg-kubernetes.pdf",
   "Animated step-by-step: pods, deployments, services, config, autoscaling.",
   ["kubernetes","k8s"," pod","deployment","cluster","orchestrat"]),
 "bbg-cicd-pipeline": ("CI/CD Pipelines — Visual Guide",
   "https://interstitiumlabs.dev/assets/pdfs/bbg-cicd-pipeline.pdf",
   "Animated step-by-step: stages, security gates, deploy strategies, GitOps, DORA.",
   ["ci/cd","cicd","ci cd","deploy","release","gitops","jenkins","pipeline","devops","automation"]),
 "bbg-zero-trust": ("Zero Trust Architecture — Visual Guide",
   "https://interstitiumlabs.dev/assets/pdfs/bbg-zero-trust.pdf",
   "Animated step-by-step: tenets, identity perimeter, micro-segmentation, pillars.",
   ["zero trust","zero-trust","never trust","micro-segment","microsegment","least privilege",
    "identity perimeter","nist 800-207","conditional access","phishing","social engineering","endpoint"]),
 "bbg-pki-encryption": ("PKI & Encryption — Visual Guide",
   "https://interstitiumlabs.dev/assets/pdfs/bbg-pki-encryption.pdf",
   "Animated step-by-step: symmetric/asymmetric, signatures, certificates, hashing.",
   ["pki","encrypt","public key","private key","rsa","hash","integrity","signature",
    "blockchain","number theory","certificate authority","boolean","logic","cryptograph"]),
 "bbg-oauth-flows": ("OAuth 2.0 & Authentication Flows — Visual Guide",
   "https://interstitiumlabs.dev/assets/pdfs/bbg-oauth-flows.pdf",
   "Animated step-by-step: roles, auth code flow, tokens, scopes, hardening.",
   ["oauth","openid","sso","token","jwt","authentication","authorization","login",
    "identity lifecycle","active directory","kerberos","entra","mfa","directory"]),
 "bbg-neural-networks": ("Neural Networks — Visual Guide",
   "https://interstitiumlabs.dev/assets/pdfs/bbg-neural-networks.pdf",
   "Animated step-by-step: neurons, layers, backprop, gradient descent, overfitting.",
   ["neural","backprop","gradient","perceptron","deep learning","linear algebra","matrix",
    "pytorch","brain","tensor"," ai ","artificial intelligence"]),
 "bbg-transformers": ("Transformers & Attention — Visual Guide",
   "https://interstitiumlabs.dev/assets/pdfs/bbg-transformers.pdf",
   "Animated step-by-step: Q/K/V, heatmaps, multi-head, the full block.",
   ["transformer","attention","llm","gpt","bert","language model","embedding","diffusion",
    "prompt","genai"," rag ","statistic"," ai ","artificial intelligence"]),
 "bbg-ml-pipelines": ("ML Training Pipelines — Visual Guide",
   "https://interstitiumlabs.dev/assets/pdfs/bbg-ml-pipelines.pdf",
   "Animated step-by-step: validation, feature stores, experiments, deployment, drift.",
   ["ml pipeline","machine learning","mlops","feature","training","evaluation",
    "experiment","hyperparameter","supervised","unsupervised","reinforcement","validation",
    "statistic","humanmetric","behavioral"," ai ","artificial intelligence"," ml "]),
 "bbg-etl-pipelines": ("ETL Data Pipelines — Visual Guide",
   "https://interstitiumlabs.dev/assets/pdfs/bbg-etl-pipelines.pdf",
   "Animated step-by-step: extract/transform/load, DAGs, quality tests, medallion.",
   ["etl","elt","ingest","data pipeline","extract","transform","batch","medallion","dag",
    "pandas","dataframe","data wrangl","python","sql for","warehousing load"]),
 "bbg-stream-processing": ("Stream Processing — Visual Guide",
   "https://interstitiumlabs.dev/assets/pdfs/bbg-stream-processing.pdf",
   "Animated step-by-step: batch vs stream, the log, windows, exactly-once.",
   ["stream","real-time","real time","kafka","event","window","exactly-once","kql",
    "log analytics","siem","quant","finance","market"]),
 "bbg-data-warehouses": ("Data Warehouses & Lakehouses — Visual Guide",
   "https://interstitiumlabs.dev/assets/pdfs/bbg-data-warehouses.pdf",
   "Animated step-by-step: OLTP/OLAP, star schema, columnar, lakehouse.",
   ["warehouse","lakehouse","olap","analytic","reporting","star schema"," power bi","datamart",
    "sql","decision","quant"]),
}

FALLBACK = {
 "il-07": ["bbg-etl-pipelines","bbg-stream-processing","bbg-data-warehouses","bbg-ml-pipelines",
           "bbg-neural-networks","bbg-transformers","bbg-caching-cdn"],
 "il-08": ["bbg-dns-resolution","bbg-tcp-handshake","bbg-load-balancing","bbg-microservices",
           "bbg-caching-cdn","bbg-cicd-pipeline","bbg-cloud-patterns"],
 "il-09": ["bbg-tls-handshake","bbg-pki-encryption","bbg-zero-trust","bbg-tcp-handshake",
           "bbg-dns-resolution","bbg-oauth-flows","bbg-cicd-pipeline","bbg-cloud-patterns",
           "bbg-data-warehouses","bbg-ml-pipelines"],
 "il-10": ["bbg-ml-pipelines","bbg-data-warehouses","bbg-cloud-patterns","bbg-microservices",
           "bbg-stream-processing","bbg-cicd-pipeline","bbg-caching-cdn"],
 "il-11": ["bbg-zero-trust","bbg-pki-encryption","bbg-oauth-flows","bbg-tls-handshake",
           "bbg-tcp-handshake","bbg-dns-resolution","bbg-load-balancing","bbg-caching-cdn",
           "bbg-cicd-pipeline","bbg-microservices","bbg-cloud-patterns"],
 "il-12": ["bbg-neural-networks","bbg-transformers","bbg-ml-pipelines","bbg-etl-pipelines",
           "bbg-stream-processing","bbg-data-warehouses","bbg-cicd-pipeline","bbg-kubernetes",
           "bbg-microservices","bbg-cloud-patterns","bbg-oauth-flows","bbg-tls-handshake",
           "bbg-tcp-handshake","bbg-dns-resolution","bbg-caching-cdn","bbg-load-balancing"],
}

FILES = {
 "il-07": "il-07-data-engineering-analytics-ai.json",
 "il-08": "il-08-algorithms-compilers-distributed-formal.json",
 "il-09": "il-09-adaptive-certification-command.json",
 "il-10": "il-10-portfolio-career-professional-practice.json",
 "il-11": "il-11-zero-trust-endpoint-defense.json",
 "il-12": "il-12-ai-engineering.json",
}

def score_pdf(key, text):
    title, url, blurb, kws = PDFS[key]
    s = 0
    for kw in kws:
        if kw in text:
            s += 3 if len(kw) > 5 else 1
    return s

def entry(key):
    title, url, blurb, kws = PDFS[key]
    return {"title": title, "url": url, "source": "Interstitium Labs",
            "blurb": blurb, "pages": 8, "animated": True}

def wire(course_key, fname):
    path = os.path.join(COURSES, fname)
    bak = os.path.join(BACKUP, fname + ".embed20261009.bak")
    if not os.path.exists(bak):
        shutil.copy2(path, bak)
    with open(path) as f:
        data = json.load(f)
    modules = data.get("modules", [])
    assert isinstance(modules, list) and modules, f"{course_key}: no flat modules"
    touched = 0
    report_lines = []
    for m in modules:
        # DEPTH CHECK
        q = len(m.get("quiz") or []); c = len(m.get("cards") or []); dr = len(m.get("drills") or [])
        if q < 3 or c < 5 or dr < 1:
            raise RuntimeError(f"{course_key}/{m.get('id')}: THIN (quiz={q} cards={c} drills={dr})")
        existing = [p.get("url","").split("/")[-1].replace(".pdf","") for p in (m.get("pdfs") or [])]
        text = ((m.get("id") or "") + " " + (m.get("title") or "")).lower()
        ranked = sorted(((score_pdf(k, text), k) for k in PDFS if k not in existing),
                        key=lambda t: -t[0])
        picks = []
        for s, k in ranked:
            if s > 0 and len(existing) + len(picks) < 3:
                picks.append(k)
        for k in FALLBACK[course_key]:
            if len(existing) + len(picks) >= 3: break
            if k not in existing and k not in picks:
                picks.append(k)
        if picks:
            m.setdefault("pdfs", [])
            m["pdfs"].extend(entry(k) for k in picks)
            touched += 1
            report_lines.append((m.get("id"), m.get("title"), [PDFS[k][0] for k in picks]))
    # atomic write + validate
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
    json.load(open(tmp))
    os.replace(tmp, path)
    return touched, len(modules), report_lines

summary = {}
for ck, fn in FILES.items():
    touched, total, lines = wire(ck, fn)
    summary[ck] = (touched, total, lines)
    print(f"{ck}: modules={total} topped_up={touched}")

with open(os.path.join(BACKUP, "wire-report.json"), "w") as f:
    json.dump({k: [(i, t, p) for i, t, p in v[2]] for k, v in summary.items()},
              f, ensure_ascii=False, indent=1)
print("OK — all files validated")

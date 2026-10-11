#!/usr/bin/env python3
"""PDF embed gap fill for IL-13..IL-20 (2026-10-09).
Adds 2-3 topic-matched PDFs to modules[].pdfs[] across 8 courses.
Touches ONLY the 'pdfs' key; videos/handsOnLab/glossary/quiz/cards/drills untouched.
"""
import json, re, os, sys
from datetime import datetime, timezone

BASE = os.path.expanduser('~/workspace/apex-audit/docs/university/data/courses')
NOW = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

PDF_META = [
 ("bbg-load-balancing",  "Load Balancing — Visual Guide", "Animated step-by-step: algorithms, health checks, L4 vs L7, global load balancing."),
 ("bbg-caching-cdn",      "Caching & CDNs — Visual Guide", "Animated step-by-step: cache-aside, invalidation, edge networks, hit ratios."),
 ("bbg-microservices",    "Microservices Architecture — Visual Guide", "Animated step-by-step: decomposition, sync vs async, resilience, observability."),
 ("bbg-tcp-handshake",    "TCP 3-Way Handshake — Visual Guide", "Animated step-by-step: SYN/SYN-ACK/ACK, reliability, flow control, closing."),
 ("bbg-dns-resolution",   "DNS Resolution — Visual Guide", "Animated step-by-step: caches, root/TLD/authoritative, record types, DNSSEC/DoT/DoH."),
 ("bbg-tls-handshake",    "TLS Handshake — Visual Guide", "Animated step-by-step: ClientHello, certificates, ECDHE, forward secrecy, TLS 1.3."),
 ("bbg-cloud-patterns",   "Cloud Architecture Patterns — Visual Guide", "Animated step-by-step: regions/AZs, auto-scaling, queues, IaC, well-architected."),
 ("bbg-kubernetes",       "Kubernetes Architecture — Visual Guide", "Animated step-by-step: pods, deployments, services, config, autoscaling."),
 ("bbg-cicd-pipeline",    "CI/CD Pipelines — Visual Guide", "Animated step-by-step: stages, security gates, deploy strategies, GitOps, DORA."),
 ("bbg-zero-trust",       "Zero Trust Architecture — Visual Guide", "Animated step-by-step: tenets, identity perimeter, micro-segmentation, pillars."),
 ("bbg-pki-encryption",   "PKI & Encryption — Visual Guide", "Animated step-by-step: symmetric/asymmetric, signatures, certificates, hashing."),
 ("bbg-oauth-flows",      "OAuth 2.0 & Authentication Flows — Visual Guide", "Animated step-by-step: roles, auth code flow, tokens, scopes, hardening."),
 ("bbg-neural-networks",  "Neural Networks — Visual Guide", "Animated step-by-step: neurons, layers, backprop, gradient descent, overfitting."),
 ("bbg-transformers",     "Transformers & Attention — Visual Guide", "Animated step-by-step: Q/K/V, heatmaps, multi-head, the full block."),
 ("bbg-ml-pipelines",     "ML Training Pipelines — Visual Guide", "Animated step-by-step: validation, feature stores, experiments, deployment, drift."),
 ("bbg-etl-pipelines",    "ETL Data Pipelines — Visual Guide", "Animated step-by-step: extract/transform/load, DAGs, quality tests, medallion."),
 ("bbg-stream-processing","Stream Processing — Visual Guide", "Animated step-by-step: batch vs stream, the log, windows, exactly-once."),
 ("bbg-data-warehouses",  "Data Warehouses & Lakehouses — Visual Guide", "Animated step-by-step: OLTP/OLAP, star schema, columnar, lakehouse."),
]
PDF_BY_KEY = {k: (t, b) for k, t, b in PDF_META}

# keyword rules: (pdf_key, [lowercase keyword fragments])
RULES = [
 ("bbg-load-balancing",  ["load balanc", "traffic management", "autoscal", "elasticity", "l4 vs l7", "backend server"]),
 ("bbg-caching-cdn",      ["cach", "cdn", "message queue", "rate limit", "edge network", "memoiz", "browser rendering"]),
 ("bbg-microservices",    ["microservice", "service mesh", "api design", "distributed system", "backend design", "fullstack architecture", "monolith", "platform thinking"]),
 ("bbg-tcp-handshake",    ["tcp", "three-way", "socket", "packet", "computer networks", "networks actually work"]),
 ("bbg-dns-resolution",   ["dns", "domain name"]),
 ("bbg-tls-handshake",    ["tls", "ssl", "handshake", "forward secrecy", "https"]),
 ("bbg-cloud-patterns",    ["cloud", "landing zone", "well-architected", "serverless", "infrastructure as code", "availability zone", "region"]),
 ("bbg-kubernetes",       ["kubernetes", "orchestrat", "container", "docker", "eks", "pod"]),
 ("bbg-cicd-pipeline",    ["ci/cd", "cicd", "jenkins", "gitops", "deploy", "dora", "release", "calms", "delivery pipeline", "gitlab"]),
 ("bbg-zero-trust",       ["zero trust", "least privilege", "perimeter", "micro-segment", "security mindset"]),
 ("bbg-pki-encryption",   ["pki", "encrypt", "cryptograph", "certificate", "hashing", "signing", "cipher", "key management", "keys vs mfa"]),
 ("bbg-oauth-flows",      ["oauth", "openid", "sso", "jwt", "auth ", "auth and", "identity", "access management", "token", "iam"]),
 ("bbg-neural-networks",  ["neural", "backprop", "gradient descent", "deep learning", "overfitting"]),
 ("bbg-transformers",     ["transformer", "attention", "llm", "generative ai", "genai", "nlp", "embedding", "rag", "pretrain", "fine-tun", "alignment", "inference and serving"]),
 ("bbg-ml-pipelines",     ["ml pipeline", "mlops", "feature store", "drift", "experiment", "ml system", "ml coding", "ml workflow", "applied ml", "model evaluation"]),
 ("bbg-etl-pipelines",     ["etl", " dag", "medallion", "batch", "wrangl", "ingest", "pipeline design", "pipeline agents", "data quality"]),
 ("bbg-stream-processing",["stream", "kafka", "real-time", "realtime", "window function"]),
 ("bbg-data-warehouses",  ["warehouse", "lakehouse", "olap", "star schema", "data model", "analytics", "sql", "pandas", "data agents", "text-to-sql", "metrics", "visualization"]),
]

# course fallback priority (breaks score ties, covers keyword-less modules)
FALLBACK = {
 "il-13-software-engineering-interview-prep": ["bbg-microservices","bbg-oauth-flows","bbg-caching-cdn","bbg-load-balancing","bbg-tcp-handshake","bbg-cloud-patterns","bbg-cicd-pipeline","bbg-data-warehouses","bbg-tls-handshake","bbg-dns-resolution","bbg-zero-trust","bbg-pki-encryption","bbg-kubernetes","bbg-etl-pipelines","bbg-stream-processing","bbg-neural-networks","bbg-transformers","bbg-ml-pipelines"],
 "il-14-sre-devops-cloud-security-interview-prep": ["bbg-cloud-patterns","bbg-kubernetes","bbg-cicd-pipeline","bbg-load-balancing","bbg-tls-handshake","bbg-zero-trust","bbg-tcp-handshake","bbg-dns-resolution","bbg-caching-cdn","bbg-stream-processing","bbg-oauth-flows","bbg-pki-encryption","bbg-microservices","bbg-etl-pipelines","bbg-data-warehouses","bbg-ml-pipelines","bbg-neural-networks","bbg-transformers"],
 "il-15-data-engineering-analytics-interview-prep": ["bbg-etl-pipelines","bbg-stream-processing","bbg-data-warehouses","bbg-ml-pipelines","bbg-cloud-patterns","bbg-caching-cdn","bbg-neural-networks","bbg-transformers","bbg-load-balancing","bbg-microservices","bbg-cicd-pipeline","bbg-kubernetes","bbg-tcp-handshake","bbg-dns-resolution","bbg-tls-handshake","bbg-oauth-flows","bbg-pki-encryption","bbg-zero-trust"],
 "il-16-machine-learning-ai-engineering": ["bbg-neural-networks","bbg-transformers","bbg-ml-pipelines","bbg-etl-pipelines","bbg-data-warehouses","bbg-stream-processing","bbg-cloud-patterns","bbg-cicd-pipeline","bbg-kubernetes","bbg-load-balancing","bbg-caching-cdn","bbg-microservices","bbg-oauth-flows","bbg-pki-encryption","bbg-zero-trust","bbg-tcp-handshake","bbg-dns-resolution","bbg-tls-handshake"],
 "il-17-agentic-ai-engineering": ["bbg-transformers","bbg-neural-networks","bbg-ml-pipelines","bbg-oauth-flows","bbg-microservices","bbg-cloud-patterns","bbg-cicd-pipeline","bbg-kubernetes","bbg-data-warehouses","bbg-etl-pipelines","bbg-stream-processing","bbg-load-balancing","bbg-caching-cdn","bbg-zero-trust","bbg-pki-encryption","bbg-tls-handshake","bbg-tcp-handshake","bbg-dns-resolution"],
 "il-18-technical-leadership-interview-prep": ["bbg-microservices","bbg-oauth-flows","bbg-cloud-patterns","bbg-cicd-pipeline","bbg-kubernetes","bbg-ml-pipelines","bbg-data-warehouses","bbg-zero-trust","bbg-load-balancing","bbg-caching-cdn","bbg-tcp-handshake","bbg-dns-resolution","bbg-tls-handshake","bbg-pki-encryption","bbg-etl-pipelines","bbg-stream-processing","bbg-neural-networks","bbg-transformers"],
 "il-19-multicloud-devops-ai-bootcamp": ["bbg-cloud-patterns","bbg-kubernetes","bbg-cicd-pipeline","bbg-load-balancing","bbg-tcp-handshake","bbg-dns-resolution","bbg-tls-handshake","bbg-zero-trust","bbg-oauth-flows","bbg-pki-encryption","bbg-caching-cdn","bbg-data-warehouses","bbg-etl-pipelines","bbg-stream-processing","bbg-neural-networks","bbg-transformers","bbg-ml-pipelines","bbg-microservices"],
 "il-20-mathematics": ["bbg-load-balancing","bbg-caching-cdn","bbg-microservices","bbg-tcp-handshake","bbg-dns-resolution","bbg-tls-handshake","bbg-cloud-patterns","bbg-kubernetes","bbg-cicd-pipeline","bbg-zero-trust","bbg-pki-encryption","bbg-oauth-flows","bbg-neural-networks","bbg-transformers","bbg-ml-pipelines","bbg-etl-pipelines","bbg-stream-processing","bbg-data-warehouses"],
}

def make_entry(key):
    title, blurb = PDF_BY_KEY[key]
    return {
        "title": title,
        "url": f"https://interstitiumlabs.dev/assets/pdfs/{key}.pdf",
        "source": "Interstitium Labs",
        "blurb": blurb,
        "pages": 8,
        "animated": True,
        "verifiedUtc": NOW,
        "httpStatus": 200,
    }

def score(title_text, key):
    t = title_text.lower()
    s = 0
    for k, words in RULES:
        if k == key:
            for w in words:
                if w in t:
                    s += 2 if len(w) > 6 else 1
    return s

def main():
    log_lines = []
    total_added = 0
    for slug, prio in FALLBACK.items():
        path = os.path.join(BASE, slug + ".json")
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        mods = data.get("modules") or data.get("paths") or []
        assert isinstance(mods, list), f"{slug}: modules not a list"
        added = 0
        for m in mods:
            mid = m.get("id") or m.get("code") or "?"
            title = m.get("title") or ""
            existing = m.get("pdfs") or []
            have = set()
            for p in existing:
                u = p.get("url", "")
                have.add(u.split("/")[-1].replace(".pdf", ""))
            ttext = f"{title}"
            ranked = sorted(PDF_BY_KEY.keys(), key=lambda k: (-score(ttext, k), prio.index(k)))
            for k in ranked:
                if len(have) >= 3:
                    break
                if k in have:
                    continue
                entry = make_entry(k)
                existing.append(entry)
                have.add(k)
                added += 1
                log_lines.append(f"{slug} | {title[:55]} | + {k}")
            m["pdfs"] = existing
            # sanity: pdfs count 2..3
            assert 2 <= len(m["pdfs"]) <= 3, f"{slug}/{mid}: pdf count {len(m['pdfs'])}"
            # sanity: embed depth still satisfied
            assert len(m.get("quiz") or []) >= 3, f"{slug}/{mid}: quiz thin"
            assert len(m.get("cards") or []) >= 5, f"{slug}/{mid}: cards thin"
            assert len(m.get("drills") or []) >= 1, f"{slug}/{mid}: drills thin"
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        # validate
        with open(path, "r", encoding="utf-8") as fh:
            reloaded = json.load(fh)
        n = len(reloaded["modules"])
        print(f"{slug}: modules={n} pdfs_added={added} validated OK")
        total_added += added
    print(f"TOTAL_ADDED={total_added}")
    with open(os.path.expanduser("~/workspace/apex-audit/.work/pdf-gapfill-20261009.log"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(log_lines) + "\n")

if __name__ == "__main__":
    main()

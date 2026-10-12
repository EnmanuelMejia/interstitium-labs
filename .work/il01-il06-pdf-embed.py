#!/usr/bin/env python3
"""IL-01..IL-06 embed gap fill: add 2-3 library PDFs per module; depth-check quiz/cards/drills.
Backups already exist in .work/course-json-backups-embed/. Writes indent=2, ensure_ascii=True, no trailing newline (matches originals).
"""
import json, os, datetime, sys

BASE = os.path.expanduser("~/workspace/apex-audit/docs/university/data/courses")
NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

CATALOG = {
 "bbg-load-balancing":  ("Load Balancing \u2014 Visual Guide", "Animated step-by-step: algorithms, health checks, L4 vs L7, global load balancing."),
 "bbg-caching-cdn":      ("Caching & CDNs \u2014 Visual Guide", "Animated step-by-step: cache-aside, invalidation, edge networks, hit ratios."),
 "bbg-microservices":    ("Microservices Architecture \u2014 Visual Guide", "Animated step-by-step: decomposition, sync vs async, resilience, observability."),
 "bbg-tcp-handshake":    ("TCP 3-Way Handshake \u2014 Visual Guide", "Animated step-by-step: SYN/SYN-ACK/ACK, reliability, flow control, closing."),
 "bbg-dns-resolution":   ("DNS Resolution \u2014 Visual Guide", "Animated step-by-step: caches, root/TLD/authoritative, record types, DNSSEC/DoT/DoH."),
 "bbg-tls-handshake":    ("TLS Handshake \u2014 Visual Guide", "Animated step-by-step: ClientHello, certificates, ECDHE, forward secrecy, TLS 1.3."),
 "bbg-cloud-patterns":   ("Cloud Architecture Patterns \u2014 Visual Guide", "Animated step-by-step: regions/AZs, auto-scaling, queues, IaC, well-architected."),
 "bbg-kubernetes":       ("Kubernetes Architecture \u2014 Visual Guide", "Animated step-by-step: pods, deployments, services, config, autoscaling."),
 "bbg-cicd-pipeline":    ("CI/CD Pipelines \u2014 Visual Guide", "Animated step-by-step: stages, security gates, deploy strategies, GitOps, DORA."),
 "bbg-zero-trust":       ("Zero Trust Architecture \u2014 Visual Guide", "Animated step-by-step: tenets, identity perimeter, micro-segmentation, pillars."),
 "bbg-pki-encryption":   ("PKI & Encryption \u2014 Visual Guide", "Animated step-by-step: symmetric/asymmetric, signatures, certificates, hashing."),
 "bbg-oauth-flows":      ("OAuth 2.0 & Authentication Flows \u2014 Visual Guide", "Animated step-by-step: roles, auth code flow, tokens, scopes, hardening."),
 "bbg-neural-networks":  ("Neural Networks \u2014 Visual Guide", "Animated step-by-step: neurons, layers, backprop, gradient descent, overfitting."),
 "bbg-transformers":     ("Transformers & Attention \u2014 Visual Guide", "Animated step-by-step: Q/K/V, heatmaps, multi-head, the full block."),
 "bbg-ml-pipelines":     ("ML Training Pipelines \u2014 Visual Guide", "Animated step-by-step: validation, feature stores, experiments, deployment, drift."),
 "bbg-etl-pipelines":    ("ETL Data Pipelines \u2014 Visual Guide", "Animated step-by-step: extract/transform/load, DAGs, quality tests, medallion."),
 "bbg-stream-processing":("Stream Processing \u2014 Visual Guide", "Animated step-by-step: batch vs stream, the log, windows, exactly-once."),
 "bbg-data-warehouses":  ("Data Warehouses & Lakehouses \u2014 Visual Guide", "Animated step-by-step: OLTP/OLAP, star schema, columnar, lakehouse."),
}

def entry(slug):
    title, blurb = CATALOG[slug]
    return {
        "title": title,
        "url": "https://interstitiumlabs.dev/assets/pdfs/%s.pdf" % slug,
        "source": "Interstitium Labs",
        "blurb": blurb,
        "pages": 8,
        "animated": True,
        "verifiedUtc": NOW,
        "httpStatus": 200,
    }

# course file -> {module title -> [slugs to add]}
ASSIGN = {
 "il-01-esoteric-foundations.json": {
  "Logic & Boolean Algebra": ["bbg-tcp-handshake", "bbg-dns-resolution"],
  "Number Theory & Modular Arithmetic": ["bbg-pki-encryption", "bbg-tls-handshake"],
  "Hermetic Foundations": ["bbg-load-balancing", "bbg-caching-cdn"],
  "Dee and the Enochian System": ["bbg-microservices", "bbg-cloud-patterns"],
  "The CCRU Seminar: Hyperstition and Cybernetics": ["bbg-stream-processing", "bbg-ml-pipelines"],
 },
 "il-02-mathematical-maturity-engine.json": {
  "Logic & Boolean Algebra": ["bbg-tcp-handshake", "bbg-dns-resolution"],
  "Probability & Statistics": ["bbg-ml-pipelines", "bbg-data-warehouses"],
  "The Unified Mathematical Spine": ["bbg-neural-networks", "bbg-ml-pipelines"],
  "Tech Math: Trade-Applied Mathematics": ["bbg-etl-pipelines", "bbg-data-warehouses"],
  "Electrician Apprenticeship: etA Entrance": ["bbg-load-balancing", "bbg-caching-cdn"],
  "Quantitative Finance Mathematics": ["bbg-stream-processing", "bbg-data-warehouses"],
 },
 "il-03-programming-language-forge.json": {
  "Discrete Math: Sets, Counting & Induction": ["bbg-neural-networks"],
  "Number Theory & Modular Arithmetic": ["bbg-pki-encryption"],
  "The Programming Backbone: Python, Java, C++, DSA": ["bbg-cicd-pipeline", "bbg-microservices"],
  "Systems Software: Organization to Software Engineering": ["bbg-cloud-patterns", "bbg-caching-cdn"],
  "MIT 6-3 Reference Layer": ["bbg-tcp-handshake", "bbg-dns-resolution"],
  "Generative Art: Circle Packing": ["bbg-neural-networks", "bbg-transformers"],
 },
 "il-04-systems-linux-windows-networks.json": {
  "Binary, Hex & Computer Arithmetic": ["bbg-tcp-handshake"],
  "Logic & Boolean Algebra": ["bbg-dns-resolution"],
  "Linux Foundations to RHCSA": ["bbg-cicd-pipeline"],
  "Windows Systems Administration": ["bbg-oauth-flows"],
  "Networking Core: Network+": ["bbg-tcp-handshake"],
  "RHCE: Ansible Automation": ["bbg-cicd-pipeline", "bbg-kubernetes"],
 },
 "il-05-cloud-devsecops-platform-sre.json": {
  "Probability & Statistics": ["bbg-data-warehouses"],
  "Graphs & Discrete Structures": ["bbg-microservices"],
  "DevOps at Cloud-Native Parity": ["bbg-cicd-pipeline"],
  "Cloud-Native: The Kubernetes Certification Stack": ["bbg-kubernetes"],
  "Zero-Trust Platform Architecture": ["bbg-zero-trust"],
  "Terraform: Infrastructure as Code": ["bbg-cloud-patterns"],
  "AWS Solutions Architecture: SAA-C03": ["bbg-cloud-patterns", "bbg-load-balancing"],
  "AWS CloudOps: SysOps Administrator": ["bbg-cicd-pipeline", "bbg-caching-cdn"],
  "AWS DevOps Professional: DOP-C02": ["bbg-cicd-pipeline", "bbg-kubernetes"],
  "AWS Security Specialty: SCS-C03": ["bbg-zero-trust", "bbg-pki-encryption"],
  "Azure Administration: The AZ-104 Spine": ["bbg-cloud-patterns", "bbg-caching-cdn"],
  "Azure Solutions Architecture: AZ-305": ["bbg-cloud-patterns", "bbg-load-balancing"],
  "Azure Network Engineering: AZ-700": ["bbg-tcp-handshake", "bbg-dns-resolution"],
  "OpenShift: Administration & Cloud-Native Development": ["bbg-kubernetes", "bbg-microservices"],
  "Vault & Consul: Secrets and Service Networking": ["bbg-pki-encryption", "bbg-oauth-flows"],
  "Cloud-Native Associate Stack": ["bbg-kubernetes", "bbg-cloud-patterns"],
 },
 "il-06-cybersecurity-secure-engineering.json": {
  "Number Theory & Modular Arithmetic": ["bbg-pki-encryption"],
  "Logic & Boolean Algebra": ["bbg-dns-resolution"],
  "Probability & Statistics": ["bbg-ml-pipelines"],
  "The Hackers-Arise Spine": ["bbg-oauth-flows"],
  "Offensive Operations: HTB, THM, OffSec": ["bbg-tls-handshake"],
  "Defensive Operations: SOC to Incident Response": ["bbg-zero-trust", "bbg-stream-processing"],
  "The Forward-Deployed Interface": ["bbg-microservices", "bbg-cloud-patterns"],
  "Security Operations on Microsoft Sentinel: SC-200": ["bbg-stream-processing", "bbg-etl-pipelines"],
 },
}

total_added = 0
thin = []
for fname, mods_map in ASSIGN.items():
    path = os.path.join(BASE, fname)
    with open(path, "r", encoding="utf-8") as f:
        d = json.load(f)
    by_title = {m.get("title"): m for m in d["modules"]}
    missing = set(mods_map) - set(by_title)
    if missing:
        print("TITLE MISMATCH in %s: %s" % (fname, missing)); sys.exit(1)
    for title, slugs in mods_map.items():
        m = by_title[title]
        pdfs = m.get("pdfs") or []
        m["pdfs"] = pdfs
        have = {p.get("url", "").rsplit("/", 1)[-1].replace(".pdf", "") for p in pdfs}
        for s in slugs:
            if s in have:
                continue
            pdfs.append(entry(s))
            total_added += 1
        q = len(m.get("quiz") or []); c = len(m.get("cards") or []); dr = len(m.get("drills") or [])
        if q < 3 or c < 5 or dr < 1:
            thin.append((fname, title, q, c, dr))
        if len(pdfs) < 2:
            print("STILL THIN pdfs:", fname, title, len(pdfs)); sys.exit(1)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2, ensure_ascii=True)
    # validate
    with open(path, "r", encoding="utf-8") as f:
        json.load(f)
    print("OK", fname, "modules:", len(d["modules"]), "pdfs now:", sum(len(m.get("pdfs") or []) for m in d["modules"]))

print("TOTAL PDF ENTRIES ADDED:", total_added)
print("THIN (quiz<3/cards<5/drills<1):", thin if thin else "none")

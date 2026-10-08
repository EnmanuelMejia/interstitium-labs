#!/usr/bin/env python3
"""Phase 2 for IL-01..IL-15:
 1. mockTask on every existing module (derived from quiz[1]).
 2. Normalize every module to the _module-template.json key set/order.
 3. Prepend prereq-math modules (computed math builders).
 4. Add crosswalk / certGates / readinessDashboard per course (verified certs only).
 5. Extend priorities + battlePlan with math modules; recompute hours.
Idempotent: skips courses already processed (marker check).
"""
import json, glob, os, sys, hashlib, random, shutil

BASE = os.path.expanduser("~/workspace/apex-audit/docs/university/data/courses")
WORK = os.path.expanduser("~/workspace/apex-audit/.work")
sys.path.insert(0, WORK)
from mathmods_a import BUILDERS_A
from mathmods_b import BUILDERS_B
BUILDERS = {**BUILDERS_A, **BUILDERS_B}

TEMPLATE_ORDER = ["cards","code","crossLinks","drills","estimatedMinutes","handsOnLab",
                  "id","mockTask","notes","objectives","prerequisiteFor","quiz","summary",
                  "title","videos","weight"]

FRAMING = ("Independent practice and preparation. Not affiliated with, endorsed by, "
           "or sponsored by any vendor or institution; confers no certificate.")

MATH_PLAN = {
 "il-01-esoteric-foundations": [
   ("logic", "Formal logic is the machinery for tiering claims without fooling yourself: valid argument forms keep DOCUMENTED separate from TRADITIONAL."),
   ("numtheory", "Number theory also carries the historical thread of this course: number lore belongs to the TRADITIONAL tier unless primary sources say otherwise.")],
 "il-02-mathematical-maturity-engine": [
   ("logic", "Proof is the language of the unified spine: every module below leans on these argument forms."),
   ("stats", "Statistics feeds directly into the Quantitative Finance module and the trade-applied work.")],
 "il-03-programming-language-forge": [
   ("discrete", "Counting and induction are the mathematics of algorithms: complexity analysis is applied discrete math."),
   ("numtheory", "Modular arithmetic underlies hashing, cryptography, and random-number generation in the systems modules.")],
 "il-04-systems-linux-windows-networks": [
   ("binmath", "Every address, mask, and permission bit in the modules below is computed exactly this way."),
   ("logic", "Firewall rules, SELinux booleans, and access policies are boolean expressions; simplify them with these laws.")],
 "il-05-cloud-devsecops-platform-sre": [
   ("stats", "SLOs, error budgets, and capacity planning are applied statistics."),
   ("graphs", "Networks, service meshes, and IaC dependency graphs are graphs; traverse them with these algorithms.")],
 "il-06-cybersecurity-secure-engineering": [
   ("numtheory", "Modern cryptography is number theory deployed: RSA, Diffie-Hellman, elliptic curves."),
   ("logic", "Detection rules are logical expressions over events; write them precisely."),
   ("stats", "Risk math and alert triage are probability: base rates decide whether a detection program works.")],
 "il-07-data-engineering-analytics-ai": [
   ("stats", "Every ML module below assumes this: distributions, expectation, Bayes."),
   ("linalg", "Data is vectors; models are matrix operations. This is the language.")],
 "il-08-algorithms-compilers-distributed-formal": [
   ("discrete", "This module is the toolkit for the entire course: proofs, counting, recurrences."),
   ("logic", "Formal systems start here: propositions, quantifiers, and what 'proof' means.")],
 "il-09-adaptive-certification-command": [
   ("binmath", "Exam math: binary, hex, and subnet computation recur across the A+, Network+, and Linux+ tracks."),
   ("logic", "Troubleshooting methodologies are applied logic: eliminate by cases.")],
 "il-10-portfolio-career-professional-practice": [
   ("quantreason", "Career decisions are quantitative: offers, growth, break-evens, and honest salary statistics.")],
 "il-11-zero-trust-endpoint-defense": [
   ("numtheory", "Hashing, encryption, and key exchange in the modules below are number theory deployed."),
   ("logic", "Allowlist policies are boolean expressions; the default-deny architecture is applied logic.")],
 "il-12-ai-engineering": [
   ("linalg", "Neural networks are linear algebra plus nonlinearity: start here."),
   ("stats", "Training, evaluation, and uncertainty are statistics."),
   ("discrete", "Counting and induction for algorithm analysis in the ML modules.")],
 "il-13-software-engineering-interview-prep": [
   ("discrete", "Complexity analysis is discrete math applied: recurrences, counting, induction."),
   ("stats", "Randomized algorithms and experiment-style reasoning need probability.")],
 "il-14-sre-devops-cloud-security-interview-prep": [
   ("stats", "SLOs, error budgets, and capacity math are statistics; this module is their foundation."),
   ("logic", "Alerting rules are boolean expressions over signals.")],
 "il-15-data-engineering-analytics-interview-prep": [
   ("stats", "The analyst and data-science modules assume this entire module."),
   ("linalg", "ML modules represent data as vectors and matrices.")],
}

# cert config: course_id -> list of tracks
# modules: 'MATH' expands to that course's math module ids; other ids literal.
CERTS = {
 "il-02-mathematical-maturity-engine": [
  {"cert": "SOA Exam P — Probability", "gate": "gate-soa-p", "track": "MATH:stats",
   "practice": (40, 60, "questions"), "vendor": None,
   "modules": ["MATH:stats", "il02-quant-math", "il02-math-spine"],
   "note": "Independent preparation for the probability syllabus: distributions, expectation, and joint/conditional probability, mapped to the course's statistics prereq and quantitative finance modules.",
   "domains": [("Probability foundations", .35), ("Distributions and expectation", .40), ("Problem reps", .25)]},
  {"cert": "SOA Exam FM — Financial Mathematics", "gate": "gate-soa-fm", "track": "il02-quant-math",
   "practice": (40, 60, "questions"), "vendor": None,
   "modules": ["MATH:stats", "il02-quant-math", "il02-tech-math"],
   "note": "Independent preparation for the financial-mathematics syllabus: interest, annuities, and valuation math via the quant finance module.",
   "domains": [("Time value of money", .40), ("Annuities and valuation", .35), ("Problem reps", .25)]},
 ],
 "il-03-programming-language-forge": [
  {"cert": "Oracle Certified Professional, Java SE (1Z0-808 / 1Z0-809)", "gate": "gate-ocp-java", "track": "il03-programming-backbone",
   "practice": (40, 60, "questions"), "vendor": None,
   "modules": ["MATH:discrete", "il03-programming-backbone"],
   "note": "Independent preparation for the Java SE programmer exams: language fundamentals, OOP, and flow control through the programming backbone module.",
   "domains": [("Java fundamentals", .40), ("Object-oriented programming", .35), ("Flow control and APIs", .25)]},
  {"cert": "Python Institute PCEP (PCEP-30-02)", "gate": "gate-pcep", "track": "il03-programming-backbone",
   "practice": (30, 40, "questions"), "vendor": "Published format: 30 questions, 40 minutes, 70% to pass (PCEP-30-02).",
   "modules": ["MATH:discrete", "il03-programming-backbone"],
   "note": "Independent preparation for the entry-level Python programmer exam: syntax, control flow, collections, functions.",
   "domains": [("Python fundamentals", .35), ("Control flow and collections", .40), ("Functions and exceptions", .25)]},
  {"cert": "Python Institute PCAP", "gate": "gate-pcap", "track": "il03-programming-backbone",
   "practice": (40, 60, "questions"), "vendor": None,
   "modules": ["MATH:discrete", "il03-programming-backbone", "il03-systems-software"],
   "note": "Independent preparation for the associate-level Python exam: OOP-heavy syllabus via the backbone and systems modules.",
   "domains": [("Object-oriented programming", .40), ("Modules and packages", .25), ("Strings, exceptions, I/O", .35)]},
 ],
 "il-04-systems-linux-windows-networks": [
  {"cert": "Red Hat Certified System Administrator (RHCSA), EX200", "gate": "gate-rhcsa", "track": "il04-linux",
   "practice": (12, 120, "tasks"), "vendor": "Performance-based tasks on a live RHEL system.",
   "modules": ["MATH:binmath", "MATH:logic", "il04-linux"],
   "note": "Independent preparation for the performance-based RHCSA exam: timed hands-on admin tasks on a live system.",
   "domains": [("Essential tools and file systems", .35), ("Users, storage, networking", .35), ("Timed task reps", .30)]},
  {"cert": "Red Hat Certified Engineer (RHCE), EX294", "gate": "gate-rhce", "track": "il04-rhce",
   "practice": (10, 120, "tasks"), "vendor": "Performance-based Ansible automation tasks.",
   "modules": ["MATH:logic", "il04-rhce", "il04-linux"],
   "note": "Independent preparation for the Ansible-automation RHCE exam: playbooks, roles, and multi-host automation.",
   "domains": [("Ansible automation", .50), ("Playbooks and roles", .30), ("Timed task reps", .20)]},
  {"cert": "CompTIA Linux+", "gate": "gate-linux-plus", "track": "il04-linux",
   "practice": (40, 60, "questions"), "vendor": None,
   "modules": ["MATH:binmath", "il04-linux"],
   "note": "Independent preparation for the Linux+ syllabus: administration, security, and troubleshooting.",
   "domains": [("System administration", .40), ("Security and automation", .35), ("Troubleshooting", .25)]},
 ],
 "il-05-cloud-devsecops-platform-sre": [
  {"cert": "AWS Certified Solutions Architect – Associate (SAA-C03)", "gate": "gate-saa-c03", "track": "il05-aws-architect",
   "practice": (40, 60, "questions"), "vendor": "Published format: 65 questions, 130 minutes, 720/1000 to pass.",
   "modules": ["MATH:stats", "MATH:graphs", "il05-aws-architect", "il05-devops-core"],
   "note": "Independent preparation for the SAA-C03 syllabus: secure, resilient, high-performing, cost-optimized architectures.",
   "domains": [("Secure architectures", .30), ("Resilient architectures", .30), ("Performance and cost", .25), ("Scenario reps", .15)]},
  {"cert": "AWS Certified DevOps Engineer – Professional (DOP-C02)", "gate": "gate-dop-c02", "track": "il05-aws-devops",
   "practice": (40, 60, "questions"), "vendor": None,
   "modules": ["il05-aws-devops", "il05-terraform", "il05-devops-core"],
   "note": "Independent preparation for the DevOps Professional syllabus: CI/CD, automation, and monitoring.",
   "domains": [("CI/CD and automation", .40), ("Monitoring and resilience", .35), ("Scenario reps", .25)]},
  {"cert": "Microsoft Certified: Azure Administrator Associate (AZ-104)", "gate": "gate-az-104", "track": "il05-azure-admin",
   "practice": (40, 60, "questions"), "vendor": "Published format: 40–60 questions.",
   "modules": ["MATH:graphs", "il05-azure-admin"],
   "note": "Independent preparation for the AZ-104 syllabus: identity, storage, compute, networking, monitoring.",
   "domains": [("Identity and governance", .25), ("Compute and storage", .30), ("Networking and monitoring", .30), ("Scenario reps", .15)]},
  {"cert": "Certified Kubernetes Administrator (CKA)", "gate": "gate-cka", "track": "il05-cloud-native",
   "practice": (8, 90, "tasks"), "vendor": "Published format: 15–20 performance tasks, 120 minutes.",
   "modules": ["MATH:graphs", "il05-cloud-native", "il05-cn-associates"],
   "note": "Independent preparation for the performance-based CKA exam: cluster operations via timed kubectl tasks.",
   "domains": [("Workloads and scheduling", .30), ("Services and networking", .30), ("Storage and troubleshooting", .40)]},
  {"cert": "HashiCorp Certified: Terraform Associate (003)", "gate": "gate-terraform-003", "track": "il05-terraform",
   "practice": (40, 60, "questions"), "vendor": "Published format: ~57 questions, 60 minutes.",
   "modules": ["il05-terraform", "il05-devops-core"],
   "note": "Independent preparation for the Terraform Associate syllabus: workflow, state, modules, HCL.",
   "domains": [("IaC concepts and workflow", .35), ("State and configuration", .40), ("Modules", .25)]},
 ],
 "il-06-cybersecurity-secure-engineering": [
  {"cert": "CompTIA Security+ (SY0-701)", "gate": "gate-security-plus", "track": "il06-defensive",
   "practice": (40, 60, "questions"), "vendor": "Published format: up to 90 questions, 90 minutes.",
   "modules": ["MATH:numtheory", "MATH:logic", "MATH:stats", "il06-hackers-arise", "il06-defensive", "il06-offensive"],
   "note": "Independent preparation for the SY0-701 syllabus: concepts, threats, architecture, operations, governance.",
   "domains": [("Security concepts and architecture", .30), ("Threats and operations", .40), ("Governance", .15), ("Scenario reps", .15)]},
  {"cert": "CompTIA CySA+ (CS0-003)", "gate": "gate-cysa-plus", "track": "il06-defensive",
   "practice": (40, 60, "questions"), "vendor": None,
   "modules": ["MATH:stats", "MATH:logic", "il06-defensive"],
   "note": "Independent preparation for the CySA+ analyst syllabus: detection, analysis, and response.",
   "domains": [("Threat detection and analysis", .45), ("Incident response", .30), ("Scenario reps", .25)]},
  {"cert": "CompTIA PenTest+ (PT0-002)", "gate": "gate-pentest-plus", "track": "il06-offensive",
   "practice": (40, 60, "questions"), "vendor": None,
   "modules": ["MATH:numtheory", "il06-offensive"],
   "note": "Independent preparation for the PenTest+ syllabus: methodology-driven offensive assessment.",
   "domains": [("Methodology and planning", .30), ("Attacks and exploitation", .40), ("Reporting", .30)]},
  {"cert": "ISC2 CISSP", "gate": "gate-cissp", "track": "il06-fde-interface",
   "practice": (50, 75, "questions"), "vendor": None,
   "modules": ["MATH:numtheory", "MATH:logic", "MATH:stats", "il06-hackers-arise", "il06-offensive", "il06-defensive", "il06-fde-interface", "il06-azure-soc"],
   "note": "Independent preparation across the eight CISSP domains; breadth-first with managerial framing.",
   "domains": [("Security and risk management", .25), ("Architecture and engineering", .30), ("Operations and IAM", .30), ("Scenario reps", .15)]},
  {"cert": "Microsoft Certified: Security Operations Analyst Associate (SC-200)", "gate": "gate-sc-200", "track": "il06-azure-soc",
   "practice": (40, 60, "questions"), "vendor": None,
   "modules": ["MATH:stats", "MATH:logic", "il06-azure-soc", "il06-defensive"],
   "note": "Independent preparation for the SC-200 syllabus: Sentinel, Defender XDR, and KQL-driven response.",
   "domains": [("Threat detection with Sentinel", .40), ("Investigation and response", .35), ("KQL and hunting reps", .25)]},
 ],
 "il-07-data-engineering-analytics-ai": [
  {"cert": "AWS Certified Data Engineer – Associate (DEA-C01)", "gate": "gate-dea-c01", "track": "il07-aws-data",
   "practice": (40, 60, "questions"), "vendor": None,
   "modules": ["MATH:stats", "MATH:linalg", "il07-aws-data", "il07-data-schools", "il07-mongodb"],
   "note": "Independent preparation for the data-engineer syllabus: ingestion, storage, pipelines, governance.",
   "domains": [("Ingestion and transformation", .35), ("Storage and modeling", .30), ("Operations and governance", .20), ("Scenario reps", .15)]},
  {"cert": "AWS Certified Machine Learning Engineer – Associate (MLA-C01)", "gate": "gate-mla-c01", "track": "il07-aws-ml",
   "practice": (40, 60, "questions"), "vendor": "Published format: 65 questions, 130 minutes.",
   "modules": ["MATH:stats", "MATH:linalg", "il07-aws-ml", "il07-ai-ml"],
   "note": "Independent preparation for the ML-engineer syllabus: data prep, modeling, deployment, monitoring.",
   "domains": [("Data preparation", .30), ("Modeling", .30), ("Deployment and monitoring", .25), ("Scenario reps", .15)]},
  {"cert": "Databricks Certified Data Engineer Associate", "gate": "gate-databricks-de", "track": "il07-aws-data",
   "practice": (40, 60, "questions"), "vendor": "Published format: 45 questions, 90 minutes.",
   "modules": ["MATH:stats", "il07-data-schools", "il07-aws-data"],
   "note": "Independent preparation for the Databricks lakehouse syllabus: Spark SQL, Delta Lake, pipelines.",
   "domains": [("Lakehouse platform", .25), ("ELT with Spark SQL", .40), ("Pipelines and governance", .35)]},
  {"cert": "CompTIA Data+", "gate": "gate-data-plus", "track": "il07-data-schools",
   "practice": (40, 60, "questions"), "vendor": None,
   "modules": ["MATH:stats", "il07-data-schools"],
   "note": "Independent preparation for the Data+ syllabus: data concepts, mining, visualization, governance.",
   "domains": [("Data concepts and environments", .35), ("Analysis and visualization", .40), ("Governance", .25)]},
 ],
 "il-09-adaptive-certification-command": [
  {"cert": "CompTIA A+ (Core 1 & Core 2)", "gate": "gate-a-plus", "track": "il09-comptia-core",
   "practice": (40, 60, "questions"), "vendor": None,
   "modules": ["MATH:binmath", "MATH:logic", "il09-comptia-core"],
   "note": "Independent preparation for both A+ core exams: hardware, networking, OS, security, procedures.",
   "domains": [("Hardware and networking", .35), ("Operating systems", .30), ("Security and procedures", .35)]},
  {"cert": "CompTIA Network+ (N10-009)", "gate": "gate-network-plus", "track": "il09-comptia-core",
   "practice": (40, 60, "questions"), "vendor": None,
   "modules": ["MATH:binmath", "il09-comptia-core"],
   "note": "Independent preparation for the Network+ syllabus: subnetting, protocols, troubleshooting.",
   "domains": [("Networking concepts", .35), ("Protocols and subnetting", .35), ("Troubleshooting", .30)]},
  {"cert": "CompTIA Security+ (SY0-701)", "gate": "gate-security-plus", "track": "il09-comptia-security",
   "practice": (40, 60, "questions"), "vendor": "Published format: up to 90 questions, 90 minutes.",
   "modules": ["MATH:logic", "il09-comptia-security", "il09-comptia-core"],
   "note": "Independent preparation for the SY0-701 syllabus via the security track.",
   "domains": [("Concepts and architecture", .35), ("Threats and operations", .40), ("Governance", .25)]},
  {"cert": "CompTIA CySA+ (CS0-003)", "gate": "gate-cysa-plus", "track": "il09-comptia-security",
   "practice": (40, 60, "questions"), "vendor": None,
   "modules": ["MATH:logic", "il09-comptia-security"],
   "note": "Independent preparation for the CySA+ analyst syllabus.",
   "domains": [("Detection and analysis", .50), ("Response", .30), ("Scenario reps", .20)]},
  {"cert": "CompTIA PenTest+ (PT0-003)", "gate": "gate-pentest-plus", "track": "il09-comptia-security",
   "practice": (40, 60, "questions"), "vendor": None,
   "modules": ["il09-comptia-security"],
   "note": "Independent preparation for the PenTest+ syllabus: planning, exploitation, reporting.",
   "domains": [("Planning and methodology", .30), ("Exploitation", .40), ("Reporting", .30)]},
  {"cert": "CompTIA Cloud+ (CV0-004)", "gate": "gate-cloud-plus", "track": "il09-comptia-data-cloud",
   "practice": (40, 60, "questions"), "vendor": None,
   "modules": ["il09-comptia-data-cloud"],
   "note": "Independent preparation for the Cloud+ syllabus: architecture, deployment, operations.",
   "domains": [("Architecture and design", .35), ("Deployment and operations", .40), ("Security", .25)]},
  {"cert": "CompTIA Linux+ (XK0-006)", "gate": "gate-linux-plus", "track": "il09-comptia-data-cloud",
   "practice": (40, 60, "questions"), "vendor": None,
   "modules": ["MATH:binmath", "il09-comptia-data-cloud"],
   "note": "Independent preparation for the Linux+ syllabus: administration and automation.",
   "domains": [("Administration", .45), ("Security and automation", .35), ("Troubleshooting", .20)]},
  {"cert": "CompTIA Server+ (SK0-005)", "gate": "gate-server-plus", "track": "il09-comptia-data-cloud",
   "practice": (40, 60, "questions"), "vendor": None,
   "modules": ["il09-comptia-data-cloud"],
   "note": "Independent preparation for the Server+ syllabus: hardware, administration, DR.",
   "domains": [("Server hardware", .35), ("Administration", .35), ("DR and security", .30)]},
  {"cert": "CompTIA Data+ (DA0-002)", "gate": "gate-data-plus", "track": "il09-comptia-data-cloud",
   "practice": (40, 60, "questions"), "vendor": None,
   "modules": ["il09-comptia-data-cloud"],
   "note": "Independent preparation for the Data+ syllabus: data concepts through governance.",
   "domains": [("Data concepts", .40), ("Analysis and visualization", .35), ("Governance", .25)]},
 ],
 "il-11-zero-trust-endpoint-defense": [
  {"cert": "Microsoft Certified: Identity and Access Administrator Associate (SC-300)", "gate": "gate-sc-300", "track": "il11-entra-identity--sc300-exam-prep",
   "practice": (40, 60, "questions"), "vendor": None,
   "modules": ["MATH:logic", "il11-entra-identity--sc300-lifecycle", "il11-entra-identity--sc300-zerotrust-ca", "il11-entra-identity--sc300-auth", "il11-entra-identity--sc300-hybrid", "il11-entra-identity--sc300-governance", "il11-entra-identity--sc300-troubleshoot", "il11-entra-identity--sc300-exam-prep"],
   "note": "Independent preparation for the SC-300 syllabus: Entra ID lifecycle, conditional access, governance.",
   "domains": [("Identity lifecycle and auth", .40), ("Conditional access and governance", .40), ("Troubleshooting", .20)]},
  {"cert": "Microsoft Certified: Cybersecurity Architect Expert (SC-100)", "gate": "gate-sc-100", "track": "il11-zero-trust-foundations--zt-nist-tenets",
   "practice": (40, 60, "questions"), "vendor": None,
   "modules": ["MATH:logic", "MATH:numtheory", "il11-zero-trust-foundations--zt-perimeter-fall", "il11-zero-trust-foundations--zt-nist-tenets", "il11-zero-trust-foundations--zt-cisa-maturity", "il11-zero-trust-foundations--zt-default-deny"],
   "note": "Independent preparation for the SC-100 architect syllabus: zero-trust strategy across identity, devices, data.",
   "domains": [("Zero-trust architecture", .45), ("Identity and access strategy", .30), ("Data and device strategy", .25)]},
  {"cert": "CompTIA Security+ (SY0-701)", "gate": "gate-security-plus", "track": "il11-zero-trust-foundations--zt-default-deny",
   "practice": (40, 60, "questions"), "vendor": "Published format: up to 90 questions, 90 minutes.",
   "modules": ["MATH:numtheory", "il11-network-crypto-foundations--zt-hashing", "il11-network-crypto-foundations--zt-encryption", "il11-red-blue-operations--zt-social-engineering", "il11-red-blue-operations--zt-blue-detect"],
   "note": "Independent preparation for SY0-701 via the crypto, attack, and detection modules.",
   "domains": [("Cryptography and integrity", .35), ("Threats and social engineering", .35), ("Detection and response", .30)]},
 ],
 "il-12-ai-engineering": [
  {"cert": "AWS Certified Machine Learning Engineer – Associate (MLA-C01)", "gate": "gate-mla-c01", "track": "aieng-production--prod-mlops-framing",
   "practice": (40, 60, "questions"), "vendor": "Published format: 65 questions, 130 minutes.",
   "modules": ["MATH:linalg", "MATH:stats", "MATH:discrete", "aieng-machine-learning--supervised-learning", "aieng-production--prod-mlops-framing", "aieng-production--prod-monitoring"],
   "note": "Independent preparation for the ML-engineer syllabus: data prep, modeling, deployment, monitoring.",
   "domains": [("Data preparation", .30), ("Modeling", .30), ("Deployment and monitoring", .25), ("Scenario reps", .15)]},
  {"cert": "Databricks Certified Data Engineer Associate", "gate": "gate-databricks-de", "track": "aieng-data-science--sql-for-ai-engineers",
   "practice": (40, 60, "questions"), "vendor": "Published format: 45 questions, 90 minutes.",
   "modules": ["MATH:stats", "aieng-data-science--pandas-wrangling", "aieng-data-science--sql-for-ai-engineers"],
   "note": "Independent preparation for the Databricks lakehouse syllabus: Spark SQL, Delta Lake, pipelines.",
   "domains": [("Lakehouse platform", .25), ("ELT with Spark SQL", .40), ("Pipelines and governance", .35)]},
 ],
 "il-14-sre-devops-cloud-security-interview-prep": [
  {"cert": "Certified Kubernetes Administrator (CKA)", "gate": "gate-cka", "track": "devops-interview-prep--devops-containers",
   "practice": (8, 90, "tasks"), "vendor": "Published format: 15–20 performance tasks, 120 minutes.",
   "modules": ["MATH:logic", "devops-interview-prep--devops-containers"],
   "note": "The container-orchestration interview skills in this course overlap the CKA performance syllabus; mapped for independent preparation.",
   "domains": [("Workloads and scheduling", .35), ("Services and networking", .35), ("Troubleshooting", .30)]},
  {"cert": "AWS Certified DevOps Engineer – Professional (DOP-C02)", "gate": "gate-dop-c02", "track": "devops-interview-prep--devops-ci-cd",
   "practice": (40, 60, "questions"), "vendor": None,
   "modules": ["devops-interview-prep--devops-ci-cd", "devops-interview-prep--devops-iac"],
   "note": "The CI/CD and IaC interview skills overlap the DevOps Professional syllabus; mapped for independent preparation.",
   "domains": [("CI/CD and automation", .45), ("IaC patterns", .35), ("Scenario reps", .20)]},
  {"cert": "HashiCorp Certified: Terraform Associate (003)", "gate": "gate-terraform-003", "track": "devops-interview-prep--devops-iac",
   "practice": (40, 60, "questions"), "vendor": "Published format: ~57 questions, 60 minutes.",
   "modules": ["MATH:logic", "devops-interview-prep--devops-iac"],
   "note": "The IaC interview skills overlap the Terraform Associate syllabus; mapped for independent preparation.",
   "domains": [("Workflow and CLI", .40), ("State and configuration", .40), ("Modules", .20)]},
 ],
 "il-15-data-engineering-analytics-interview-prep": [
  {"cert": "AWS Certified Data Engineer – Associate (DEA-C01)", "gate": "gate-dea-c01", "track": "data-eng-interview-prep--batch-pipelines",
   "practice": (40, 60, "questions"), "vendor": None,
   "modules": ["MATH:stats", "data-eng-interview-prep--sql-for-de", "data-eng-interview-prep--batch-pipelines", "data-eng-interview-prep--streaming-systems", "data-eng-interview-prep--data-modeling-warehousing"],
   "note": "The pipeline-design interview skills overlap the data-engineer syllabus; mapped for independent preparation.",
   "domains": [("Ingestion and transformation", .40), ("Storage and modeling", .30), ("Operations", .30)]},
  {"cert": "Databricks Certified Data Engineer Associate", "gate": "gate-databricks-de", "track": "data-eng-interview-prep--batch-pipelines",
   "practice": (40, 60, "questions"), "vendor": "Published format: 45 questions, 90 minutes.",
   "modules": ["MATH:stats", "data-eng-interview-prep--batch-pipelines"],
   "note": "The batch/streaming interview skills overlap the Databricks lakehouse syllabus; mapped for independent preparation.",
   "domains": [("ELT with Spark SQL", .45), ("Pipelines", .35), ("Governance", .20)]},
 ],
}

NO_CERT_NOTE = {
 "il-01-esoteric-foundations": "No accredited certification exists for Western esotericism; this course is independent scholarship. No certification track is mapped rather than inventing one.",
 "il-08-algorithms-compilers-distributed-formal": "No accredited certification maps to algorithms, compilers, or formal methods; the course is foundational theory. No track mapped.",
 "il-10-portfolio-career-professional-practice": "No accredited certification maps to portfolio/career practice as a discipline; the course builds evidence, not credentials. No track mapped.",
 "il-13-software-engineering-interview-prep": "Technical interviews have no accredited certification; the course prepares performance, not credentials. No track mapped.",
}

def _rng(seed):
    return random.Random(int(hashlib.sha256(seed.encode()).hexdigest(), 16) % (2**31))

def make_mock(mid, quiz):
    src = [q for q in (quiz or []) if isinstance(q, dict) and q.get("choices") and len(q["choices"]) >= 3 and q.get("explain")]
    q = src[1] if len(src) > 1 else src[0]
    r = _rng(mid + "|mock")
    choices = list(q["choices"]); r.shuffle(choices)
    return {"id": f"{mid}--mock", "type": "choice", "q": q["q"], "choices": choices,
            "answer": choices.index(q["choices"][q["answer"]]), "explain": q["explain"]}

def normalize_module(m):
    m.setdefault("videos", []); m.setdefault("crossLinks", []); m.setdefault("prerequisiteFor", [])
    return {k: m.get(k) for k in TEMPLATE_ORDER}

def build_gate(course_code, t, math_ids):
    pq, pm, ptype = t["practice"]
    unit = "questions" if ptype == "questions" else "tasks"
    fmt = f"Practice gate: {pq} {unit}, {pm} minutes (course-authored)."
    if t["vendor"]:
        fmt += f" Vendor's published live-exam format: {t['vendor']}"
    else:
        fmt += " Live-exam format: check the vendor's current exam guide before booking."
    mods = [(math_ids[sub.split(":")[1]] if isinstance(sub, str) and sub.startswith("MATH:") else sub) for sub in t["modules"]]
    track = math_ids[t["track"].split(":")[1]] if t["track"].startswith("MATH:") else t["track"]
    checklist = [
        "Complete every mapped module, including its hands-on lab and both drills.",
        f"Clear this practice gate at 80%+ twice, on different days.",
        "Re-take the two weakest drills from the mapped modules and clear them.",
        "Rebuild the mapped modules' lab deliverables from a blank page, closed-notes.",
        "For every missed gate item, write the explanation in your own words until you can teach it.",
    ]
    return {
        "id": t["gate"], "cert": t["cert"], "trackModule": track, "framing": FRAMING,
        "format": fmt, "minutes": pm, "questionCount": pq,
        "domainWeights": [{"domain": dn, "weight": w, "questions": max(1, round(pq * w))} for dn, w in t["domains"]],
        "readinessRule": "Clear the practice gate at 80%+ on two consecutive attempts, on different days, before booking the vendor exam.",
        "readinessChecklist": checklist, "modules": mods,
    }

def process(path, only_marks=False):
    fn = os.path.basename(path)
    d = json.load(open(path))
    cid = d["courseId"]
    if d.get("_phase2_done"):
        return {"file": fn, "skipped": True}
    existing_ids = [m["id"] for m in d["modules"]]
    # 1. mockTask + normalize existing modules
    for m in d["modules"]:
        if not m.get("mockTask"):
            m["mockTask"] = make_mock(m["id"], m.get("quiz"))
    d["modules"] = [normalize_module(m) for m in d["modules"]]
    # 2. math modules
    math_ids = {}
    new_mods = []
    for suffix, ctx in MATH_PLAN.get(cid, []):
        mod = BUILDERS[suffix](cid, d["code"], existing_ids, ctx)
        math_ids[suffix] = mod["id"]
        new_mods.append(mod)
    d["modules"] = new_mods + d["modules"]
    # 3. cert mapping
    tracks = CERTS.get(cid, [])
    if tracks:
        d["crosswalk"] = [{"cert": t["cert"],
                           "modules": [(math_ids[s.split(":")[1]] if isinstance(s, str) and s.startswith("MATH:") else s) for s in t["modules"]],
                           "note": t["note"]} for t in tracks]
        d["certGates"] = [build_gate(d["code"], t, math_ids) for t in tracks]
        d["readinessDashboard"] = {
            "title": f"{d['code']} Certification Readiness Dashboard",
            "framing": FRAMING,
            "concept": "Each track has a course-authored timed practice gate. You are ready to book the vendor exam when you clear the gate threshold twice in a row, on different days.",
            "formula": "readiness = (gate attempt 1 >= 80%) AND (gate attempt 2 >= 80%), attempts on separate days",
            "thresholds": "Per-gate thresholds are listed on each certGate (80%+ twice).",
            "statusLabels": ["not started", "in progress", "gate cleared once", "ready"],
            "rule": "Two consecutive 80%+ clears on different days before booking any exam.",
            "order": [t["gate"] for t in tracks],
        }
    elif cid in NO_CERT_NOTE:
        d["crosswalk"] = []; d["certGates"] = []
        d["_noCertNote"] = NO_CERT_NOTE[cid]
    # 4. priorities + battlePlan extensions
    pr = d.get("priorities") or []
    bp = d.get("battlePlan") or []
    for mod in new_mods:
        pr.append({"label": mod["title"], "minutes": mod["estimatedMinutes"]})
        bp.append({"id": mod["id"], "title": mod["title"], "minutes": mod["estimatedMinutes"],
                   "detail": "Prerequisite math — complete before the technical modules."})
    d["priorities"] = pr; d["battlePlan"] = bp
    # 5. hours
    total = sum(m.get("estimatedMinutes", 0) for m in d["modules"])
    d["hours"] = round(total / 60)
    d["updatedAt"] = "2026-10-08"
    d["_phase2_done"] = True
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(d, f, indent=1, ensure_ascii=False); f.write("\n")
    json.load(open(tmp))
    shutil.copy2(path, os.path.join(WORK, "backups-il01-15", fn + ".phase1.bak"))
    os.replace(tmp, path)
    return {"file": fn, "math_added": len(new_mods), "gates": len(tracks),
            "modules": len(d["modules"]), "hours": d["hours"]}

if __name__ == "__main__":
    files = sorted(glob.glob(os.path.join(BASE, "il-0[1-9]-*.json")) + glob.glob(os.path.join(BASE, "il-1[0-5]-*.json")))
    for f in files:
        print(process(f), flush=True)

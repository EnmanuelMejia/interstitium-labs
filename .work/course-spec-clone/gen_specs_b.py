#!/usr/bin/env python3
"""Generate spec sheets for Group B (IL-07..IL-12) from the built JSON."""
import json

BASE = '/home/hatch/workspace/apex-audit/docs/university/data/courses/'
OUT = '/home/hatch/workspace/apex-audit/.work/course-spec-clone/specs/'
FRAMING = ("Independent practice and preparation. Not affiliated with, endorsed by, "
           "or sponsored by any vendor or employer; confers no certificate.")

STATIC = {
"IL-07": {
 "prereqs": ["None formal — entry level for data work.", "Basic SQL familiarity recommended (not required).", "IL-02 concepts are assumed only through the embedded math primers."],
 "m00": "Embedded math primers serve as the M00 supplement (drawn from IL-02 topics, cross-linked to IL-02): Probability & Statistics and Linear Algebra Foundations.",
 "outcomes": [
  "Model and query document databases: aggregation pipelines, embedding-vs-referencing, indexing (MongoDB).",
  "Build data pipelines: ingestion, orchestration, warehousing, quality, and governance.",
  "Apply probability and linear algebra to analytics and ML tasks (embedded math primers).",
  "Train and evaluate ML models: supervised learning through reinforcement learning first contact.",
  "Engineer LLM systems: RAG, vector databases, fine-tuning (LoRA/QLoRA), evaluation, agents, MLOps.",
  "Self-host open-weight models: quantization, Ollama/llama.cpp/vLLM, licensing literacy.",
  "Build agents: the ReAct loop, LangGraph-style state machines, MCP tools, evaluation.",
  "Track frontier AI topics and cite the survey source (IL-23) for further reading.",
  "Prepare independently for AWS DEA-C01/MLA-C01, Databricks Data Engineer Associate, CompTIA Data+, and dbt Analytics Engineering.",
  "Operate on AWS data and ML services through vendor-neutral engineering patterns.",
 ],
 "certs": [
  ("AWS Certified Data Engineer – Associate (DEA-C01)", "il07-aws-data", "Independent preparation aligned to published objectives."),
  ("AWS Certified Machine Learning Engineer – Associate (MLA-C01)", "il07-aws-ml", "Independent preparation aligned to published objectives."),
  ("Databricks Certified Data Engineer Associate", "il07-data-schools, il07-aws-data", "Independent preparation aligned to published objectives."),
  ("CompTIA Data+ (DA0-002)", "il-07-data-engineering-analytics-ai-math-stats, il07-data-schools", "Independent preparation aligned to published objectives."),
  ("dbt Analytics Engineering Certification", "il07-data-schools, il07-mongodb", "Independent preparation aligned to published objectives (65 questions, 120 min, 65% to pass — verify current version before booking)."),
 ],
 "hn": None,  # filled from JSON
 "merge_comp": "IL-26 (Data Analyst Certification & Senior Mastery — analyst track), IL-16 (Machine Learning & AI Engineering — ML depth)",
 "merge_frontier": "Data frontier topics (lakehouse, streaming) folded into the frontier + data-schools modules",
 "merge_xlinks": "All 11 modules carry cross-links: math primers → IL-02, ML/AI modules → IL-16, analytics modules → IL-26, frontier → IL-23",
},
"IL-08": {
 "prereqs": ["IL-02 (Mathematical Maturity Engine) recommended.", "IL-03 (Programming Language Forge) or equivalent programming experience."],
 "m00": "Embedded math primers serve as the M00 supplement (drawn from IL-02 topics, cross-linked to IL-02): Discrete Math (sets, counting, induction) and Logic & Boolean Algebra.",
 "outcomes": [
  "Prove: induction, contradiction, invariants — the mathematician's toolkit for CS.",
  "Analyze algorithms: asymptotics, divide-and-conquer, dynamic programming, graphs, NP-completeness.",
  "Build systems: from gates to processors, C to kernels, single-node to distributed.",
  "Reason about concurrency, databases, and operating systems at the implementation level.",
  "Read MIT 6-3, CMU, and Stanford curricula with load-bearing-idea discipline.",
  "Translate proofs into code and measurements (every algorithm proven is implemented and timed).",
 ],
 "certs": [],
 "hn": None,
 "merge_comp": "IL-02 (Mathematical Maturity Engine — the prereq primer)",
 "merge_frontier": "None folded (foundational course)",
 "merge_xlinks": "Math primers cross-linked to IL-02",
},
"IL-09": {
 "prereqs": ["None — entry level.", "Basic IT literacy assumed for the CompTIA core stack."],
 "m00": "Exempt per plan (professional/command course). Existing math primers (binary/hex arithmetic, logic) are cross-linked to IL-02.",
 "outcomes": [
  "Sequence the CompTIA core stack (A+, Network+, Security+) into one campaign with stackable credentials.",
  "Prepare the CompTIA security track (CySA+, PenTest+, SecurityX) with domain-weighted drills and original scenarios.",
  "Cover the CompTIA data/cloud expansion (Cloud+, Linux+, Server+, Data+, DataSys+, Project+).",
  "Tier the vendor AI credential landscape honestly: proctored exams, academy badges, and pilot programs.",
  "Prepare Oracle's Java, SQL, and OCI certification families from official objectives.",
  "Prepare the Linux Foundation's live blockchain certifications (HFCP, BCP).",
  "Prepare the C++ Institute and Python Institute language credential ladders.",
  "Run the adaptive command deck: schedule, gate, and reschedule from weakest domains.",
 ],
 "certs": [
  ("CompTIA A+ / Network+ / Security+ / CySA+ / PenTest+ / Cloud+ / Linux+ / Server+ / Data+ (9 tracks)", "il09-comptia-core, il09-comptia-security, il09-comptia-data-cloud", "Independent preparation aligned to published objectives — existing tracks preserved, no new vendor certs added."),
  ("Oracle Java / SQL / OCI", "il09-oracle", "Independent preparation aligned to published objectives."),
  ("Linux Foundation HFCP / BCP", "il09-lf-blockchain", "Independent preparation aligned to published objectives."),
  ("C++ Institute / Python Institute", "il09-cpp-python", "Independent preparation aligned to published objectives."),
 ],
 "hn": None,
 "merge_comp": "None assigned (certification command center)",
 "merge_frontier": "None folded",
 "merge_xlinks": "Math primers cross-linked to IL-02",
},
"IL-10": {
 "prereqs": ["None — entry level."],
 "m00": "Exempt per plan (professional-practice course). Existing quantitative-reasoning primer is cross-linked to IL-02.",
 "outcomes": [
  "Run the forward-deployed career arc: discover, model, prove, integrate, operate, generalize.",
  "Build interview systems: technical depth, system design, behavioral narrative, offer evaluation.",
  "Use self-knowledge (typology) as working-style data for career decisions.",
  "Build ventures: problem discovery, MVP discipline, unit economics, fundraising literacy.",
  "Climb the quant ladder: prerequisites audit → MicroMasters → PhD/consulting prep.",
  "Apply quantitative reasoning to career decisions (embedded primer).",
 ],
 "certs": [],
 "hn": None,
 "merge_comp": "IL-18 (Technical Leadership Interview Prep — interview-prep cluster)",
 "merge_frontier": "None folded (professional course)",
 "merge_xlinks": "Quantitative-reasoning primer cross-linked to IL-02",
},
"IL-11": {
 "prereqs": ["IL-04 (Systems, Linux, Windows, Networks) recommended.", "IL-06 (Cybersecurity & Secure Engineering) foundations recommended."],
 "m00": "Exempt per plan (applied/practitioner course). Existing math primers (number theory, logic) are cross-linked to IL-06's math primers.",
 "outcomes": [
  "Explain the Zero Trust doctrine — never trust, always verify — and why the perimeter model failed.",
  "Map attack classes to OSI and TCP/IP layers; apply hashing and encryption controls correctly.",
  "Describe Active Directory structure and how attackers abuse Kerberos, hashes, and replication.",
  "Design application allowlisting and ringfencing policies that contain threats without breaking the business.",
  "Analyze phishing, web-application, and session attacks from red-team and blue-team perspectives.",
  "Run detection and response: triage alerts, contain incidents, close the post-incident learning loop.",
  "Administer Entra ID identity lifecycle, Conditional Access, authentication, hybrid identity, and governance.",
  "Troubleshoot identity and endpoint issues with PowerShell and KQL.",
  "Apply number theory and logic to crypto and policy reasoning (embedded math primers).",
  "Prepare independently for CompTIA Security+ SY0-701 and CySA+ CS0-003, plus Microsoft SC-300/SC-100 readiness.",
 ],
 "certs": [
  ("CompTIA Security+ (SY0-701)", "il11-zero-trust-foundations-*, il11-red-blue-operations-*, il11-cyber-hero-prep-*", "Independent preparation aligned to published objectives."),
  ("CompTIA CySA+ (CS0-003)", "il11-red-blue-operations--zt-blue-detect, il11-allowlisting-ringfencing-*, il11-cyber-hero-prep-*", "Independent preparation aligned to published objectives (up to 85 questions, 165 min, 750/900 to pass)."),
  ("Microsoft SC-300 (Identity and Access Administrator Associate)", "il11-entra-identity-*", "Independent preparation aligned to published objectives."),
  ("Microsoft SC-100 (Cybersecurity Architect Expert)", "il11-zero-trust-foundations-*, il11-entra-identity-*", "Independent preparation aligned to published objectives."),
 ],
 "hn": None,
 "merge_comp": "IL-06 (Cybersecurity & Secure Engineering — foundation), IL-29 (ThreatLocker Zero-Trust CBT — flagship)",
 "merge_frontier": "Quantum/post-quantum crypto folded into the encryption/crypto modules",
 "merge_xlinks": "All 27 modules carry cross-links: zero-trust modules → IL-29, ops/crypto modules → IL-06, identity modules → IL-29 MIT-6.858 + IL-06 defensive",
},
"IL-12": {
 "prereqs": ["IL-03 (Programming Language Forge) or equivalent Python.", "IL-02 concepts assumed only through the embedded math primers."],
 "m00": "Embedded math primers serve as the M00 supplement (drawn from IL-02 topics, cross-linked to IL-16's prereq-math modules): Linear Algebra, Probability & Statistics, Discrete Math.",
 "outcomes": [
  "Write the Python AI engineers actually use: syntax, objects/modules, environments, concurrency.",
  "Wrangle data with NumPy, pandas, SQL, and honest statistics — preventing leakage from day one.",
  "Train and evaluate classical ML models with rigorous validation and cost-matched metrics.",
  "Build neural networks in PyTorch: gradients, optimization, regularization, hand-written training loops.",
  "Work with transformers, diffusion, and LLMs: prompting, RAG, vector search, parameter-efficient fine-tuning.",
  "Engineer NLP and agentic systems: tokenization, tool use, MCP, context engineering.",
  "Ship production AI: serving patterns, monitoring/drift response, cost control, red-teaming.",
  "Complete a deployed capstone: evaluation, model card, responsible-AI review.",
  "Apply linear algebra, probability, and discrete math to ML (embedded math primers).",
  "Prepare independently for AWS MLA-C01, Databricks Data Engineer Associate, and the TensorFlow Developer Certificate.",
 ],
 "certs": [
  ("AWS Certified Machine Learning Engineer – Associate (MLA-C01)", "aieng-production-*, aieng-machine-learning-*", "Independent preparation aligned to published objectives."),
  ("Databricks Certified Data Engineer Associate", "aieng-data-science-*, aieng-production--prod-pipelines", "Independent preparation aligned to published objectives."),
  ("TensorFlow Developer Certificate", "aieng-deep-learning-*, aieng-nlp-*, aieng-capstone-*", "Independent preparation aligned to published objectives (5 hands-on tasks, 300 min, open book — no officially published passing score; verify current setup before booking)."),
 ],
 "hn": None,
 "merge_comp": "IL-16 (Machine Learning & AI Engineering — ML depth), IL-17 (Agentic AI Engineering — agents)",
 "merge_frontier": "AI frontier topics folded into the frontier-adjacent modules (advanced retrieval, agent autonomy ceilings)",
 "merge_xlinks": "All 72 modules carry cross-links: math primers → IL-16 prereq-math, ML modules → IL-16, agentic modules → IL-17, data-science → IL-16 python-for-ml",
},
}

def cert_rows(code, gates):
    rows = []
    for g in gates:
        mods = ", ".join(g["modules"][:4]) + ("…" if len(g["modules"]) > 4 else "")
        rows.append("| %s | %s | %s |" % (g["cert"], mods,
            "Independent preparation aligned to published objectives. " + FRAMING))
    return "\n".join(rows)

def spec_md(code, fn):
    d = json.load(open(BASE + fn))
    s = STATIC[code]
    total_min = sum(m["estimatedMinutes"] for m in d["modules"])
    hn = d["honestyNote"]
    lines = []
    A = lines.append
    A("# %s · %s — Spec Sheet" % (code, d["title"]))
    A("")
    A("## Identity")
    A("- code: %s" % code)
    A("- courseId: %s" % d["courseId"])
    A("- title: %s" % d["title"])
    A("- tagline: %s" % d["tagline"])
    A("- blurb: %s" % d["blurb"])
    A("")
    A("## Hours (honest math)")
    A("- Declared hours: %d (must equal sum of module estimatedMinutes ÷ 60, rounded)" % d["hours"])
    A('- Time formula: "estimatedMinutes per module = instruction + videos + drills + hands-on lab, set per module by the author; course total = sum of module estimates. Declared hours are the honest rounded sum."')
    A("- Module minutes sum: %d → %.2f → %d" % (total_min, total_min / 60, d["hours"]))
    A("")
    A("## Prerequisites")
    for p in s["prereqs"]:
        A("- %s" % p)
    A("- Prereq math supplement: %s" % s["m00"])
    A("")
    A("## Learning Outcomes (objectives)")
    for i, o in enumerate(s["outcomes"], 1):
        A("%d. %s" % (i, o))
    A("")
    A("## Certification Mapping (independent-prep framing)")
    if s["certs"]:
        A("| Cert | Modules | Notes |")
        A("|------|---------|-------|")
        for cert, mods, notes in s["certs"]:
            A("| %s | %s | %s |" % (cert, mods, notes))
        A("")
    else:
        A("No vendor certifications — foundational/professional course. (`_noCertNote` preserved in JSON.)")
        A("")
    A("Each certGates entry carries:")
    A('  framing: "%s"' % FRAMING)
    A("- JSON certGates count: %d" % len(d.get("certGates", [])))
    A("")
    A("## Module Plan")
    A("| # | Module ID | Title | Est. Minutes | Cert alignment |")
    A("|---|-----------|-------|--------------|----------------|")
    gate_mods = set()
    for g in d.get("certGates", []):
        gate_mods.update(g.get("modules", []))
    for i, m in enumerate(d["modules"], 1):
        cal = "cert-track" if m["id"] in gate_mods else "—"
        A("| %d | %s | %s | %d | %s |" % (i, m["id"], m["title"].replace("|", "/"), m["estimatedMinutes"], cal))
    A("")
    A("## Honesty Note (required verbatim pattern)")
    A("")
    A("> %s" % hn)
    A("")
    A("## Merge / Cross-link Notes")
    A("- Complementary courses: %s" % s["merge_comp"])
    A("- Frontier topics folded in: %s" % s["merge_frontier"])
    A("- Cross-links added: %s" % s["merge_xlinks"])
    A("")
    A("---")
    A("*Generated from %s · updatedAt %s · schemaVersion %s*" % (fn, d["updatedAt"], d["schemaVersion"]))
    return "\n".join(lines) + "\n"

FILES = {
 "IL-07": "il-07-data-engineering-analytics-ai.json",
 "IL-08": "il-08-algorithms-compilers-distributed-formal.json",
 "IL-09": "il-09-adaptive-certification-command.json",
 "IL-10": "il-10-portfolio-career-professional-practice.json",
 "IL-11": "il-11-zero-trust-endpoint-defense.json",
 "IL-12": "il-12-ai-engineering.json",
}

if __name__ == "__main__":
    for code, fn in FILES.items():
        md = spec_md(code, fn)
        with open(OUT + code + ".md", "w") as f:
            f.write(md)
        print("wrote", OUT + code + ".md", len(md))

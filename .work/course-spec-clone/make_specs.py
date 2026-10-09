#!/usr/bin/env python3
"""Generate spec sheets for Group D from built JSON + authored metadata."""
import json, os

BASE = os.path.expanduser('~/workspace/apex-audit/docs/university/data/courses')
OUT = os.path.expanduser('~/workspace/apex-audit/.work/course-spec-clone/specs')
os.makedirs(OUT, exist_ok=True)

def mod_table(d, cert_col=None):
    rows = ["| # | Module ID | Title | Est. Minutes | Cert alignment |",
            "|---|-----------|-------|--------------|----------------|"]
    for i, m in enumerate(d["modules"], 1):
        ca = cert_col(m["id"]) if cert_col else ""
        rows.append(f"| {i} | {m['id']} | {m['title']} | {m.get('estimatedMinutes')} | {ca} |")
    return "\n".join(rows)

def noah_section(d):
    nt = d.get("noahTutoring", {})
    lines = ["## Noah AI Integration (required)",
             "",
             f"> {nt.get('framing','')}",
             "",
             f"**Driver:** {nt.get('driver','')}",
             "",
             "**Personas → modules:**",
             ""]
    for p in nt.get("personas", []):
        lines.append(f"- **{p['name']}** — {p['role']} _(modules: {', '.join(p['moduleIds'])})_")
    lines += ["",
              f"**Voices:** {nt['voices']['count']} natural voices. {nt['voices']['note']}",
              "",
              f"**Adaptive:** {nt['adaptive']['method']}. {nt['adaptive']['note']}",
              "",
              f"**Course-aware:** {nt['courseAware']['note']}",
              ""]
    if nt.get("frontierNote"):
        lines += [f"**Frontier note:** {nt['frontierNote']}", ""]
    if nt.get("courseNote"):
        lines += [f"**Course note:** {nt['courseNote']}", ""]
    return "\n".join(lines)

SPECS = {}

SPECS["IL-19"] = dict(
    file="il-19-multicloud-devops-ai-bootcamp.json",
    tagline="Six clouds. One discipline. Noah-tutored.",
    blurb=("IL-19 is a multicloud DevOps and AI bootcamp spanning AWS, Azure, GCP, and OCI plus the full "
           "DevOps toolchain (Git, Terraform, Ansible, Docker, Kubernetes, Jenkins, observability, Python/Boto3 automation) "
           "and applied generative AI. It opens with computer fundamentals and career strategy, embeds three prereq-math "
           "modules, and closes with cloud certification paths. Built for operator depth, not slideware."),
    prereqs="None — entry level. The CF fundamentals block (CF-01–CF-06) assumes no prior background.",
    math_supplement="Pre-existing and preserved: IL-19-PM-LOGIC, IL-19-PM-STATS, IL-19-PM-DISCRETE (300 min each), drawn from IL-02. No new M00 added — the supplement already exists.",
    outcomes=[
        "Architect workloads across AWS, Azure, GCP, and OCI, comparing each cloud's core services on real tradeoffs.",
        "Apply IAM least-privilege design and identity federation in AWS, Azure, GCP, and OCI.",
        "Build and operate CI/CD pipelines with Jenkins, GitHub Actions patterns, and infrastructure as code (Terraform, Ansible).",
        "Containerize applications with Docker and run them on Kubernetes (EKS patterns), including break-fix triage.",
        "Implement observability: metrics, logs, traces, and alerting across a full stack.",
        "Automate cloud operations with Python and Boto3.",
        "Reason about cloud cost: pricing models, budgets, alerts, and landing-zone guardrails.",
        "Use generative AI services across clouds (AWS, Azure, GCP) and build a RAG capstone with LangChain.",
        "Prepare independently for AWS SAA-C03, Azure AZ-104, CKA, and Terraform Associate aligned to public exam objectives.",
        "Present a hireable portfolio: migration projects, LinkedIn, resume, and interview plan.",
    ],
    cert_table=[
        ("AWS Certified Solutions Architect – Associate (SAA-C03)", "AWS-01–AWS-07, CF-04", "Independent preparation aligned to published objectives."),
        ("Microsoft Certified: Azure Administrator Associate (AZ-104)", "AZ-01–AZ-08", "Independent preparation aligned to published objectives."),
        ("Certified Kubernetes Administrator (CKA)", "DO-06", "Independent preparation aligned to published objectives."),
        ("HashiCorp Terraform Associate (004)", "DO-03", "Independent preparation aligned to published objectives."),
    ],
    cert_framing="Independent practice and preparation. Not affiliated with, endorsed by, or sponsored by any vendor or employer; confers no certificate.",
    honesty_note='"Preparation only — this course confers no certificate. Cloud certification exams are taken through each vendor\'s own portal. Certification tracks are independent preparation aligned to each vendor\'s publicly published exam objectives as of October 2026; this course is not affiliated with, endorsed by, or sponsored by AWS, Microsoft, Google, Oracle, HashiCorp, or CNCF."',
    merge=["Complementary courses: IL-05 (Cloud, DevSecOps, Platform & SRE), IL-28 (DevSecOps & Cloud Infrastructure — production depth), IL-14 (SRE/DevOps interview prep).",
           "Internal module chain: every module cross-links to its neighbors; no cross-course module links added (other groups own IL-05/IL-28 sides).",
           "Frontier topics folded in: none — IL-19 is a foundations bootcamp; frontier AI/cloud topics live in IL-12/IL-16/IL-17 with IL-23 as survey."],
)

SPECS["IL-20"] = dict(
    file="il-20-mathematics.json",
    tagline="The mathematical spine of engineering.",
    blurb=("IL-20 is the full mathematics treatment for engineers and scientists: sets and logic, proof methods, "
           "counting, relations, three modules of linear algebra, two of calculus, series, multivariable calculus, "
           "probability, statistics, graphs and recurrences, numerical methods, and linear systems with optimization. "
           "It opens with a new M00 readiness primer drawn from IL-02 and closes every module with pencil-and-paper problem work."),
    prereqs="IL-02 (Mathematical Maturity Engine) recommended; M00 readiness primer embedded for self-assessment.",
    math_supplement="NEW in this build: IL-20-M00 · Mathematical Maturity Primer — Readiness for IL-20 (300 min), drawn from IL-02 (logic, truth tables, proof methods, study habits). IL-20 is itself the math spine for the other technical courses.",
    outcomes=[
        "Prove statements with direct, contrapositive, contradiction, and induction methods.",
        "Count with permutations, combinations, and recurrence relations.",
        "Operate fluently with vectors, matrices, eigenvalues, and linear transformations.",
        "Differentiate and integrate single-variable and multivariable functions; apply the Fundamental Theorem.",
        "Test series for convergence and work with power series representations.",
        "Model uncertainty with probability: Bayes, distributions, expectation.",
        "Apply statistical inference: estimation, hypothesis testing, regression.",
        "Solve linear systems and formulate optimization problems (Lagrange, gradient reasoning).",
        "Verify mathematical claims computationally with Python (SymPy, numeric methods).",
        "Read and write mathematics at the level the technical courses (IL-03–IL-08, IL-12, IL-16, IL-17) assume.",
    ],
    cert_table=[],
    cert_framing="N/A — no vendor certs. Academic/foundational: no accredited certification exists for general engineering mathematics as a standalone credential (see _noCertNote, preserved).",
    honesty_note='"Original instructional content written for this course — standard mathematics, no invented theorems. Practice material only; confers no certificate and is not affiliated with any university or vendor."',
    merge=["Math cluster: IL-02 is the prereq primer; IL-20 is the full treatment. IL-20's modules are the source for prereq-math supplements across technical courses.",
           "Internal module chain: sequential cross-links; M00 cross-links to IL-02 source modules.",
           "No vendor certifications mapped — academic/foundational by design."],
)

SPECS["IL-21"] = dict(
    file="il-21-humanities.json",
    tagline="Philosophy, history, writing, rhetoric, economics, and law — the disciplines that make a technologist wise.",
    blurb=("IL-21 gives technologists the humanities spine: what philosophy is, logic and argumentation, two modules of ethics "
           "(traditions, then technology and responsibility), epistemology and philosophy of science, history of science "
           "(antiquity to Newton, 1800 to present), history of technology, technical writing, rhetoric and persuasion, "
           "economics for engineers (markets, incentives, games), law and policy literacy, and a synthesis module. "
           "Two prereq-math modules (logic, stats) are embedded."),
    prereqs="None — entry level.",
    math_supplement="Pre-existing and preserved: IL-21-PM-LOGIC, IL-21-PM-STATS (300 min each). Non-technical course; exempt from new M00 per merge plan (already has supplements).",
    outcomes=[
        "Distinguish the branches of philosophy and state what philosophy is for.",
        "Analyze and construct arguments: premises, inferences, objections, fallacies.",
        "Apply the three ethical traditions (utilitarian, deontological, virtue) to technology decisions.",
        "Reason about responsibility for autonomous and AI-mediated systems.",
        "Explain how scientific knowledge is made and revised (epistemology, philosophy of science).",
        "Narrate the history of science and technology from antiquity to the present.",
        "Write clear technical prose: structure, precision, revision.",
        "Argue persuasively and ethically: rhetoric for real rooms.",
        "Apply economic reasoning (costs, incentives, game theory) to engineering decisions.",
        "Read law and policy as a technologist: literacy, not legal advice.",
    ],
    cert_table=[],
    cert_framing="N/A — no vendor certs. Academic/foundational.",
    honesty_note='"Original instructional content; historical and philosophical claims are well-established facts attributed to their traditions — ideas are paraphrased, quotations are not fabricated. Not legal advice. Confers no certificate. It is not affiliated with, endorsed by, or sponsored by any university, publisher, or institution; it confers no certificate and grants no credentials."',
    merge=["Standalone humanities track; complements every technical course as the judgment spine.",
           "No cross-course module links (non-technical, exempt per merge plan).",
           "No vendor certifications — academic/foundational."],
)

SPECS["IL-22"] = dict(
    file="il-22-esoteric-secret-knowledge.json",
    tagline="Kabbalah, Hermeticism, alchemy, astrology, tarot, Enochian, Rosicrucianism — the deep library, critically read.",
    blurb=("IL-22 is the deep dive into esoteric and secret knowledge: approaching the traditions, Kabbalah and Jewish mysticism, "
           "Hermeticism and the Corpus Hermeticum, alchemy's history and symbolism, astrology's framework, tarot's history and the "
           "Major Arcana, Dee and Kelley's Enochian system, Rosicrucianism, Theosophy, the Golden Dawn, ceremonial magic and the "
           "grimoires, Gnosticism, Eastern esoteric traditions, divination systems, symbolism and sacred geometry, and the modern "
           "occult revival — taught with source criticism throughout. IL-01 (Esoteric Foundations) is the prereq; IL-22 goes deep."),
    prereqs="IL-01 (Esoteric Foundations) — the prereq survey; IL-22 is the deep dive.",
    math_supplement="Pre-existing and preserved: IL-22-PM-NUMTH, IL-22-PM-LOGIC (300 min each). Non-technical course; exempt from new M00 per merge plan.",
    outcomes=[
        "Distinguish primary texts from later receptions across the Western esoteric traditions.",
        "Explain Kabbalah's core structures and its historical development within Jewish mysticism.",
        "Read the Hermetic corpus with attention to its late-antique context.",
        "Interpret alchemical symbolism historically rather than anachronistically.",
        "Describe astrology's framework and tarot's history as cultural systems.",
        "Evaluate Enochian, grimoire, and ceremonial-magic claims against manuscript evidence.",
        "Compare Rosicrucianism, Theosophy, and the Golden Dawn as modern movements.",
        "Apply source criticism: date, language, and manuscript tradition before interpretation.",
        "Discuss Eastern esoteric traditions with comparative care.",
        "Read contemporary occult revivals critically — enthusiasm with evidence.",
    ],
    cert_table=[],
    cert_framing="N/A — no vendor certs. Academic/foundational; historical and critical study, no credential claims.",
    honesty_note='"Original instructional content. Esoteric material is presented descriptively as the traditions present it — history, symbolism, and practice as claimed by practitioners — never as verified science. No invented lineages, revelations, or quotations. Confers no certificate. It is not affiliated with, endorsed by, or sponsored by any religious, esoteric, or academic organization; it confers no certificate and grants no credentials."',
    merge=["Esoteric cluster: IL-01 is the prereq; IL-22 is the deep dive. Cross-linked both ways at module level (IL-22 modules now carry IL-01 cross-links: hermeticism→il01-hermetic-foundations, enochian→il01-dee-enochian, modern revival→il01-ccru-seminar, symbolism→IL-01 number-theory module, PM modules→IL-01 math modules).",
           "IL-01's side of the cross-linking is owned by the group building IL-01.",
           "No vendor certifications — academic/foundational."],
)

SPECS["IL-23"] = dict(
    file="il-23-frontier-knowledge.json",
    tagline="Transformers, quantum, CRISPR, fusion, BCIs, agents, chips, synbio, space — the frontier, distilled.",
    blurb=("IL-23 surveys cutting-edge research: transformer architectures, quantum computing basics, CRISPR and gene editing, "
           "fusion energy status, brain–computer interfaces, AI agents and inference-time compute, semiconductor scaling beyond Moore, "
           "synthetic biology, space infrastructure, the Epoch AI capability-forecasting corpus, METR-style evaluation of AI itself, "
           "and the Frontier Method for reading fast-moving fields. Three prereq-math modules (stats, linear algebra, logic) are embedded. "
           "IL-23 stays the survey; depth lives in the fold-in courses."),
    prereqs="None — entry level; PM stats/linear-algebra/logic modules embedded for the quantitative sections.",
    math_supplement="Pre-existing and preserved: IL-23-PM-STATS, IL-23-PM-LINALG, IL-23-PM-LOGIC (300 min each).",
    outcomes=[
        "Explain the transformer architecture and why attention scaled.",
        "Describe what quantum computers can and cannot do, and the post-quantum migration logic.",
        "Summarize CRISPR's mechanism and the state of gene-editing applications.",
        "Evaluate fusion energy claims against demonstrated physical results.",
        "Compare BCI approaches and their current capabilities.",
        "Reason about AI agents, inference-time compute, and the task-time horizon.",
        "Explain semiconductor scaling challenges beyond Moore's law.",
        "Survey synthetic biology and space infrastructure developments.",
        "Read capability-forecasting work (Epoch AI corpus) with appropriate skepticism.",
        "Apply the Frontier Method: cruxes, demonstrated results, and updating from evidence.",
    ],
    cert_table=[],
    cert_framing="N/A — no vendor certs. Academic/foundational survey; the frontier has no certification body.",
    honesty_note='"Original instructional content. Frontier topics are dated as-of 2026-10-07 and flagged as fast-moving; leadership and product claims carry short half-lives and must be re-verified before citing. Confers no certificate. It is not affiliated with, endorsed by, or sponsored by any research lab, company, or institution named; it confers no certificate and grants no credentials."',
    merge=["Frontier DISTILL (merge plan): IL-23 stays the survey; topics fold into depth courses, each citing IL-23 as survey source:",
           "  - AI frontier (transformers, agents, evals) → IL-12, IL-16, IL-17",
           "  - Quantum/post-quantum crypto → IL-06, IL-11",
           "  - Semiconductors/edge → IL-05, IL-28 (edge/on-device)",
           "  - Data frontier → IL-07",
           "  - CRISPR, fusion, BCI, synbio, space: no fold target — survey-only, noted honestly.",
           "Fold-in notes added to IL-23 module notes naming exact target module IDs."],
)

SPECS["IL-24"] = dict(
    file="il-24-threatlocker-assessment-prep-cbt.json",
    tagline="Zero Trust endpoint defense + security graphs + AI-aided SOC — assessment prep, independent.",
    blurb=("IL-24 is assessment preparation for ThreatLocker-style zero-trust endpoint defense roles: know the company cold, "
           "answer like an operator (STAR + triage logic), default-deny operations from Learning Mode to least privilege, "
           "approve/deny/ringfence triage decisions, endpoint posture, attack graphs, graph-powered defense, ML threat defense, "
           "UEBA, securing AI agents, the AI-aided SOC, Bayes and honest metrics, a timed assessment simulation circuit, and a "
           "capstone. Cross-linked to IL-29 (flagship) throughout. INDEPENDENT PREP — not affiliated with ThreatLocker."),
    prereqs="Basic IT/security literacy recommended; PM stats/logic modules embedded.",
    math_supplement="Pre-existing and preserved: IL-24-PM-STATS, IL-24-PM-LOGIC (300 min each). Applied assessment-prep course; exempt from new M00.",
    outcomes=[
        "Describe ThreatLocker's zero-trust endpoint approach from public materials, in your own words.",
        "Answer behavioral questions with operator-grade STAR stories.",
        "Work default-deny triage: approve, deny, or ringfence with documented reasoning.",
        "Explain allowlisting, ringfencing, elevation control, storage control, and network control operations.",
        "Read endpoint posture: services, egress, file identity.",
        "Think in attack graphs: nodes, edges, paths — and defend from the graph.",
        "Explain how ML models and UEBA contribute to threat defense, honestly.",
        "Reason about prompt injection and tool poisoning for AI agents.",
        "Work an AI-aided SOC workflow: lifecycle, detection engineering, governance.",
        "Apply Bayes and honest metrics to security claims; prove readiness under time in the simulation circuit.",
    ],
    cert_table=[
        ("ThreatLocker Cyber Hero Certification", "m24-default-deny, m24-approve-deny-ringfence, m24-assessment-sim", "Independent preparation. Not affiliated with, endorsed by, or sponsored by ThreatLocker; vendor exam format/duration/passing standard per the vendor's current exam page."),
    ],
    cert_framing="Independent practice and preparation. Not affiliated with, endorsed by, or sponsored by any vendor or employer; confers no certificate.",
    honesty_note='"Independent interview-prep material by Interstitium Labs — not affiliated with, endorsed by, or sponsored by ThreatLocker. Confers no certificate, no employment, and no product experience. All scenarios, tickets, and labs are original practice content; no vendor or course material is reproduced. Vendor figures (founding facts, customer counts, response times) are the company\'s own public claims, stated as such."',
    merge=["Cybersecurity cluster: IL-24 cross-links to IL-29 (flagship) at module level — every IL-24 module carries IL-29 cross-links (default-deny→IL29-M01/M02, ringfence→IL29-M03, posture→IL29-M05/M06, SOC→IL29-M07/M10, capstone→IL29-M11).",
           "IL-29 keeps the flagship branding and its own independent-prep disclaimer.",
           "ThreatLocker independent-prep disclaimer is prominent in honestyNote, certGates framing, and noahTutoring."],
)

SPECS["IL-25"] = dict(
    file="il-25-cybersecurity-professional-certificate.json",
    tagline="Think like an attacker. Defend like a professional.",
    blurb=("IL-25 is a professional cybersecurity certificate-prep track in three arcs: risk management (risk, foundations, federal role, "
           "threats, critical infrastructure, IAM, job prep), defensive operations (defensive intro, cryptography, SOC, incident response, "
           "secure sysadmin and netadmin, cloud security, job prep), and offensive cybersecurity (offensive intro, pentesting I & II, "
           "social engineering, AI in cybersecurity, policy/privacy/governance, OT/IoT risk, capstone). Three prereq-math modules embedded. "
           "Cross-linked to IL-29 (flagship). Independent prep for Security+ and CySA+."),
    prereqs="Basic IT literacy recommended; PM number-theory/stats/logic modules embedded.",
    math_supplement="Pre-existing and preserved: IL-25-PM-NUMTH, IL-25-PM-STATS, IL-25-PM-LOGIC (300 min each). Applied cert-prep course; exempt from new M00.",
    outcomes=[
        "Manage cybersecurity risk: frameworks, assessment, and communication to leadership.",
        "Explain the federal government's role in cybersecurity: law, operations, standards.",
        "Analyze threats and vulnerabilities with structured prioritization.",
        "Design and evaluate IAM: concepts, layers, and technology.",
        "Operate defensively: SOC workflows, cryptography, incident response.",
        "Administer systems and networks securely, including cloud.",
        "Plan and scope penetration tests ethically and legally.",
        "Recognize and defend against social engineering.",
        "Apply AI in cybersecurity with honest understanding of its limits.",
        "Navigate policy, privacy, regulation, data governance, and OT/IoT risk.",
    ],
    cert_table=[
        ("CompTIA Security+ (SY0-701)", "IL25-M01–M16", "Independent preparation aligned to published objectives."),
        ("CompTIA CySA+ (CS0-003)", "IL25-M09–M16", "Independent preparation aligned to published objectives."),
        ("ISC2 SSCP", "IL25-M01–M16", "Independent preparation aligned to published objectives."),
    ],
    cert_framing="Independent practice and preparation. Not affiliated with, endorsed by, or sponsored by any vendor or employer; confers no certificate.",
    honesty_note='"This is an independent preparation course aligned to publicly published exam objectives; it is not affiliated with, endorsed by, or sponsored by CompTIA, ISC2, or any vendor; it confers no certificate and grants no credentials. Exam facts (domains, weights, question counts, durations, passing scores) reflect publicly published objectives as of October 2026."',
    merge=["Cybersecurity cluster: IL-25 cross-links to IL-29 (flagship) at module level — every IL-25 module carries IL-29 cross-links (risk→IL29-M01, SOC/IR→IL29-M07, IAM→IL29-M04, capstone→IL29-M11).",
           "Complementary: IL-06 (foundation), IL-11 (zero-trust depth).",
           "Noah AI drives the prep: persona-mapped tutoring across all three arcs."],
)

TIME_FORMULA = ("estimatedMinutes per module = instruction + videos + drills + hands-on lab, set per module by the author; "
                "course total = sum of module estimates. Declared hours are the honest rounded sum.")

def _num(mid):
    import re
    m = re.search(r"M(\d+)$", mid)
    return int(m.group(1)) if m else None

def align_19(mid):
    hits = []
    if mid.startswith("AWS-") or mid.startswith("CF-"):
        hits.append("SAA-C03")
    if mid.startswith("AZ-"):
        hits.append("AZ-104")
    if mid == "DO-06":
        hits.append("CKA")
    if mid == "DO-03":
        hits.append("TF-004")
    return "; ".join(hits)

def align_24(mid):
    return "Cyber Hero" if (mid.startswith("m24-") or mid.startswith("IL-24-PM")) else ""

def align_25(mid):
    hits = []
    n = _num(mid)
    pm = mid.startswith("IL-25-PM")
    if (n is not None and n <= 16) or pm:
        hits += ["Security+", "SSCP"]
    if (n is not None and 9 <= n <= 16) or pm:
        hits.append("CySA+")
    return "; ".join(hits)

ALIGN = {"IL-19": align_19, "IL-24": align_24, "IL-25": align_25}

def build_spec(code):
    spec = SPECS[code]
    d = json.load(open(os.path.join(BASE, spec["file"])))
    total_min = sum(m.get("estimatedMinutes", 0) for m in d["modules"])
    L = []
    L.append(f"# {code} · {d['title']} — Spec Sheet")
    L.append("")
    L.append("## Identity")
    L.append(f"- code: {code}")
    L.append(f"- courseId: {d['courseId']}")
    L.append(f"- title: {d['title']}")
    L.append(f"- tagline: {spec['tagline']}")
    L.append(f"- blurb: {spec['blurb']}")
    L.append("")
    L.append("## Hours (honest math)")
    L.append(f"- Declared hours: {d['hours']} (sum of module estimatedMinutes = {total_min} min ÷ 60 = {total_min/60:.1f}, rounded)")
    L.append(f'- Time formula: "{TIME_FORMULA}"')
    L.append("")
    L.append("## Prerequisites")
    L.append(f"- {spec['prereqs']}")
    L.append(f"- Prereq math supplement: {spec['math_supplement']}")
    L.append("")
    L.append("## Learning Outcomes (objectives)")
    for i, o in enumerate(spec["outcomes"], 1):
        L.append(f"{i}. {o}")
    L.append("")
    L.append("## Certification Mapping (independent-prep framing)")
    if spec["cert_table"]:
        L.append("| Cert | Modules | Notes |")
        L.append("|------|---------|-------|")
        for cert, mods, notes in spec["cert_table"]:
            L.append(f"| {cert} | {mods} | {notes} |")
    else:
        L.append("No vendor certifications mapped — academic/foundational.")
    L.append("")
    L.append(f'Framing on every certGates entry: "{spec["cert_framing"]}"')
    L.append("")
    L.append("## Module Plan")
    L.append(mod_table(d, ALIGN.get(code)))
    L.append("")
    L.append("## Honesty Note (required verbatim pattern)")
    L.append(spec["honesty_note"])
    L.append("")
    L.append("## Merge / Cross-link Notes")
    for m in spec["merge"]:
        L.append(f"- {m}")
    L.append("")
    L.append(noah_section(d))
    L.append("## Audit status")
    L.append("See companion audit file: IL-XX-AUDIT.md")
    L.append("")
    return "\n".join(L)

if __name__ == "__main__":
    import sys
    only = sys.argv[1:] or list(SPECS.keys())
    for code in only:
        text = build_spec(code)
        out = os.path.join(OUT, f"{code}.md")
        with open(out, "w") as f:
            f.write(text)
        print("wrote", out, f"({len(text)} chars)")

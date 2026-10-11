# Part 4 — Noah tutoring builder + main build logic
import sys
sys.path.insert(0, __import__('os').path.expanduser('~/workspace/apex-audit/.work/course-spec-clone'))
from build_group_d import *
from build_group_d_p2 import *
from build_group_d_p3 import *
import copy

# ---------------- Noah tutoring section ----------------
NOAH_FRAMING = (
    "Noah AI is the core learning-experience driver for this course — not a bolt-on. "
    "Every module is taught with Noah as the Socratic tutor: learners work through the material "
    "in conversation with Noah, which is course-aware (grounded in this course's modules, notes, "
    "labs, quizzes, and drills), adapts with SM-2 spaced repetition, and speaks with 5 natural voices "
    "for a voice-first experience. Learners can talk with Noah via voice chat while working through modules — "
    "asking questions, working problems aloud, and getting challenged back before answers are given."
)

def noah_tutoring(personas, frontier=False, extra_note=""):
    pt = {
        "framing": NOAH_FRAMING,
        "driver": ("Noah drives the learning experience: guided Socratic walkthroughs of each module, "
                   "Socratic questioning before answers, drill generation from the learner's weak spots, "
                   "and lab debriefs that connect hands-on work back to the module's objectives."),
        "personas": personas,
        "voices": {
            "count": 5,
            "note": ("Five natural voices. Voice-first: learners talk with Noah via voice chat while working "
                     "through modules — hands free for labs, terminals, and notebooks."),
        },
        "adaptive": {
            "method": "SM-2 spaced repetition",
            "note": ("Noah schedules flashcard and drill reviews with the SM-2 algorithm, prioritizing cards "
                     "and modules the learner gets wrong. Forgetting curves are fought per-learner, not per-cohort."),
        },
        "courseAware": {
            "groundedIn": "This course's modules, notes, hands-on labs, quizzes, drills, and branching scenarios.",
            "note": ("Noah tutors from the course itself — every explanation, hint, and drill references the "
                     "module content the learner is on. No generic answers; everything is grounded in this course."),
        },
    }
    if frontier:
        pt["frontierNote"] = (
            "The frontier moves fast — papers, benchmarks, and capability curves update monthly. "
            "Noah's course-aware tutoring keeps learners current: it flags where a module's snapshot "
            "may have moved on, teaches the frontier method for evaluating new claims, and drills the "
            "skill of updating beliefs from new evidence rather than memorizing a frozen snapshot."
        )
    if extra_note:
        pt["courseNote"] = extra_note
    return pt

def persona(name, role, module_ids):
    return {"name": name, "role": role, "moduleIds": module_ids}

# ---------------- Branching-scenario shape converter ----------------
# Authored shape: nodes {id: {"text", "choices":[{"t","to"}]}} or {"text","end":True}
# Target (IL-29) shape: {"text","choices":[{"label","feedback","next"}]}, terminal next=null, + resolution.
INTERMEDIATE_FEEDBACK = {
    # (scenario_id, choice_target) -> feedback for choices pointing at non-terminal nodes
    ("il19-bs-cost", "explore"): "Good instinct — identify before you act. Cost Explorer will show exactly which service and which resources drive the spike.",
    ("il19-bs-k8s", "status"): "Right — read the rollout state before touching anything. The events will tell you what changed.",
    ("il19-bs-cicd", "tests"): "Right — a green pipeline that tests nothing is decoration. Inspect what the gates actually verify.",
}

def convert_bs(bs):
    nodes = bs["nodes"]
    out_nodes = {}
    correct_text = ""
    for nid, node in nodes.items():
        if node.get("end"):
            if node["text"].startswith("Correct"):
                correct_text = node["text"]
            out_nodes[nid] = {"text": node["text"], "choices": []}
        else:
            ch = []
            for c in node["choices"]:
                tgt = c["to"]
                if nodes.get(tgt, {}).get("end"):
                    fb = nodes[tgt]["text"]
                    ch.append({"label": c["t"], "feedback": fb, "next": None})
                else:
                    fb = INTERMEDIATE_FEEDBACK.get((bs["id"], tgt), "")
                    ch.append({"label": c["t"], "feedback": fb, "next": tgt})
            out_nodes[nid] = {"text": node["text"], "choices": ch}
    resolution = bs.get("resolution") or ("The winning path: " + correct_text if correct_text else "")
    return {"id": bs["id"], "title": bs["title"], "moduleId": bs["moduleId"],
            "start": bs["start"], "nodes": out_nodes, "resolution": resolution}

# ---------------- install shape converters (IL-28 pattern) ----------------
def to_install_steps(items, module_id, minutes=20):
    out = []
    for it in items:
        tool = it["title"].replace("Install the ", "").replace("Install ", "").replace("Build the ", "")
        out.append({"id": it["id"], "tool": tool, "moduleId": module_id, "minutes": minutes})
    return out

def to_install_labs(items, module_id):
    labs = []
    for it in items:
        steps = it.get("steps", [])
        labs.append({
            "id": it["id"], "tool": it["title"], "category": "tooling",
            "moduleId": module_id, "estimatedMinutes": 20,
            "platforms": {p: {"steps": steps, "notes": ""} for p in ("windows", "macos", "linux")},
        })
    return labs

# ---------------- study guide pacing ----------------
def make_pacing(code, modules, phase_defs):
    """phase_defs: list of (weeks_label, label, module_id_list)."""
    by_id = {m["id"]: m for m in modules}
    rows = []
    for weeks, label, ids in phase_defs:
        mods = [by_id[i] for i in ids if i in by_id]
        tot = sum(m.get("estimatedMinutes", 0) for m in mods)
        rows.append(f"{weeks} — {label} ({', '.join(ids)}, ~{round(tot/60)} hrs): " +
                    "; ".join(m["title"] for m in mods[:3]) + ("; ..." if len(mods) > 3 else ""))
    return rows

def chunk_ids(ids, n):
    k = (len(ids) + n - 1) // n
    return [ids[i:i+k] for i in range(0, len(ids), k)]

# ---------------- per-course Noah persona maps ----------------
NOAH_19 = noah_tutoring([
    persona("Visionary", "Paints where multicloud is going — why the six-cloud discipline compounds into architecture judgment.",
            ["AWS-01", "CF-04", "AI-01"]),
    persona("Engineer", "Drills the operator skills: IAM policies, Terraform plans, kubectl, CI/CD pipelines — precision over vibes.",
            ["AWS-02", "DO-03", "DO-06", "DO-07", "DO-09"]),
    persona("Philosopher", "Asks why: the tradeoffs behind every architecture decision — cost vs. resilience, control vs. velocity.",
            ["AWS-06", "DO-01", "DO-08"]),
    persona("Mentor", "Guides the career track: certification paths, portfolio, interview prep — the CS and CM modules.",
            ["CS-01", "CS-02", "CS-03", "CS-04", "CS-05", "CM-01", "CM-02", "CM-03"]),
    persona("Trickster", "Breaks things on purpose: hands you a broken Terraform plan, a CrashLoopBackOff, a surprise bill — and makes you diagnose it.",
            ["DO-06", "DO-07", "AWS-06"]),
])

NOAH_20 = noah_tutoring([
    persona("Visionary", "Shows where the mathematics leads — how linear algebra becomes ML, how calculus becomes optimization.",
            ["m20-linear-algebra-1", "m20-calculus-1", "m20-linear-systems-optimization"]),
    persona("Engineer", "Makes you compute: works problems step by step, checks your algebra, never lets a hand-wavy step pass.",
            ["m20-linear-algebra-2", "m20-calculus-2", "m20-numerical-methods"]),
    persona("Philosopher", "Asks what a proof really is — why rigor matters, what 'obvious' is hiding.",
            ["m20-proof-methods", "m20-sets-logic"]),
    persona("Mentor", "Paces the long road: study habits, readiness checks, when to push and when to review.",
            ["IL-20-M00", "m20-series"]),
    persona("Trickster", "Plants the classic traps: the broken induction, the divergent series that looks convergent, the 'obvious' false step.",
            ["m20-proof-methods", "m20-series", "m20-probability"]),
])

NOAH_21 = noah_tutoring([
    persona("Visionary", "Connects the humanities to the technologist's future — why philosophy and history compound into judgment.",
            ["m21-what-is-philosophy", "m21-synthesis"]),
    persona("Engineer", "Treats arguments as systems: premises in, conclusions out — debug the inference like code.",
            ["m21-logic-argument", "m21-technical-writing"]),
    persona("Philosopher", "Home turf: the three ethical traditions, epistemology, philosophy of science — Socratic dialogue at full depth.",
            ["m21-ethics-1", "m21-ethics-2", "m21-epistemology"]),
    persona("Mentor", "Coaches writing and rhetoric: drafts, feedback, revision — the craft of being understood.",
            ["m21-technical-writing", "m21-rhetoric"]),
    persona("Trickster", "Steelmans the other side: argues the position you despise better than you can, then asks you to beat it.",
            ["m21-rhetoric", "m21-ethics-2", "m21-economics-2"]),
])

NOAH_22 = noah_tutoring([
    persona("Visionary", "Traces the long arc: how hermetic ideas echo through centuries into modern culture and technology.",
            ["m22-hermeticism", "m22-modern-revival"]),
    persona("Engineer", "Demands source criticism: dates, manuscripts, languages — the philology behind the mystique.",
            ["m22-grimoires", "m22-enochian", "m22-kabbalah"]),
    persona("Philosopher", "Explores the ideas on their own terms: what the traditions claim about reality, mind, and symbol.",
            ["m22-hermeticism", "m22-gnosticism", "m22-symbolism"]),
    persona("Mentor", "Teaches critical reading: how to approach esoteric texts with both openness and rigor.",
            ["m22-approaching", "m22-modern-revival"]),
    persona("Trickster", "Tests your credulity: presents the sensational claim, then reveals the manuscript facts.",
            ["m22-grimoires", "m22-divination", "m22-modern-revival"]),
])

NOAH_23 = noah_tutoring([
    persona("Visionary", "Lives here: extrapolates the curves — what transformers, fusion, and BCIs imply for the next decade.",
            ["m23-transformers", "m23-fusion", "m23-bci", "m23-epoch-ai"]),
    persona("Engineer", "Grounds the hype in mechanisms: how attention actually works, what a qubit actually does.",
            ["m23-transformers", "m23-quantum", "m23-semiconductors"]),
    persona("Philosopher", "Asks the hard questions the papers skip: what would change your mind, what is the crux?",
            ["m23-frontier-method", "m23-metr-evals"]),
    persona("Mentor", "Teaches the frontier method itself: how to read a fast-moving field without drowning.",
            ["m23-frontier-method", "m23-epoch-ai"]),
    persona("Trickster", "Plays the hype merchant: pitches the breathless press release, then makes you find the buried caveat.",
            ["m23-fusion", "m23-crispr", "m23-synbio"]),
], frontier=True)

NOAH_24 = noah_tutoring([
    persona("Visionary", "Shows the operator you are becoming: the Cyber Hero mindset — default-deny as a discipline, not a product.",
            ["m24-company-cold", "m24-star-operator"]),
    persona("Engineer", "Drills the controls: allowlisting, ringfencing, elevation, storage, network — exact, procedural, no shortcuts.",
            ["m24-default-deny", "m24-approve-deny-ringfence", "m24-endpoint-posture"]),
    persona("Philosopher", "Asks why the attacker thinks the way they do: nodes, edges, paths — the graph view of malice.",
            ["m24-attack-graphs", "m24-graph-defense"]),
    persona("Mentor", "Runs the assessment simulation with you: STAR stories, triage logic, interview-day game plan.",
            ["m24-star-operator", "m24-assessment-sim"]),
    persona("Trickster", "Is the attacker in the simulation: crafts the phishing lure, the malicious macro, the bypass attempt — and grades your response.",
            ["m24-approve-deny-ringfence", "m24-ai-aided-soc", "m24-capstone"]),
], extra_note=("Independent preparation: Noah tutors from this course's original practice scenarios and publicly "
                "documented concepts. Not affiliated with, endorsed by, or sponsored by ThreatLocker; no vendor "
                "material is reproduced."))

NOAH_25 = noah_tutoring([
    persona("Visionary", "Maps the career: from risk management to SOC to offensive — where each track leads.",
            ["IL25-M01", "IL25-M08", "IL25-M16", "IL25-M24"]),
    persona("Engineer", "Drills the technical core: crypto, IAM, networks, cloud — precise and procedural.",
            ["IL25-M06", "IL25-M07", "IL25-M10", "IL25-M14", "IL25-M15"]),
    persona("Philosopher", "Interrogates the ethics: offensive work, disclosure, privacy — the responsibilities of capability.",
            ["IL25-M17", "IL25-M20", "IL25-M22"]),
    persona("Mentor", "Prepares you for the job: SOC workflows, IR order-of-operations, certification readiness.",
            ["IL25-M09", "IL25-M11", "IL25-M12"]),
    persona("Trickster", "Red-teams your defenses: the phishing email, the misconfigured firewall, the unpatched host — find it before it finds you.",
            ["IL25-M04", "IL25-M14", "IL25-M18", "IL25-M19"]),
], extra_note=("Independent certification preparation aligned to publicly published exam objectives "
                "(CompTIA Security+, CySA+). Not affiliated with, endorsed by, or sponsored by any vendor; "
                "confers no certificate."))

# ---------------- course build configs ----------------
def il19_phases(mods):
    ids = [m["id"] for m in mods if not m["id"].startswith("IL-19-PM")]
    pm = [m["id"] for m in mods if m["id"].startswith("IL-19-PM")]
    return [
        ("Weeks 1-2", "Prereq math spine", pm),
        ("Weeks 3-5", "Cloud foundations: AWS, Azure, GCP, OCI", [i for i in ids if i.split("-")[0] in ("AWS","AZ","GCP","OCI")][:16]),
        ("Weeks 6-8", "Cloud depth + DevOps toolchain", [i for i in ids if i.split("-")[0] in ("AWS","AZ","GCP","OCI")][16:] + [i for i in ids if i.startswith("DO-")]),
        ("Weeks 9-10", "AI services + fundamentals + career", [i for i in ids if i.startswith("AI-") or i.startswith("CF-") or i.startswith("CS-") or i.startswith("CM-")]),
    ]

COURSES = {
    "IL-19": {
        "file": "il-19-multicloud-devops-ai-bootcamp.json",
        "m00": None,  # prereq math already embedded as 3 PM modules
        "xlinks": {},
        "add": lambda d: {
            "toolLabs": IL19_TOOLLABS,
            "multicloudLabs": IL19_MULTICLOUD,
            "sampleDatasets": [],
            "installSteps": to_install_steps(IL19_INSTALL, "AWS-01"),
            "installLabs": to_install_labs(IL19_INSTALL, "AWS-01"),
            "installPrereqOrder": IL19_INSTALL_ORDER,
            "employerMappings": [],
            "jdMatrix": [],
            "sqlPlaygrounds": [],
            "pythonExercises": IL19_PYEX,
            "daxPlaygrounds": [],
            "branchingScenarios": [convert_bs(b) for b in IL19_BS],
            "clickSims": IL19_CS,
            "interactivityAudit": interactivity_audit(d),
            "studyGuide": study_guide("IL-19", "10 weeks", d["modules"], il19_phases(d["modules"])),
            "timeFormula": TIME_FORMULA,
            "noahTutoring": NOAH_19,
        },
    },
    "IL-20": {
        "file": "il-20-mathematics.json",
        "m00": IL20_M00,
        "xlinks": {},
        "add": lambda d: {
            "crosswalk": [],
            "certGates": [],
            "readinessDashboard": readiness_dashboard("IL-20", []),
            "toolLabs": IL20_TOOLLABS,
            "multicloudLabs": [],
            "sampleDatasets": [],
            "installSteps": to_install_steps(IL20_INSTALL, "IL-20-M00"),
            "installLabs": to_install_labs(IL20_INSTALL, "IL-20-M00"),
            "installPrereqOrder": IL20_INSTALL_ORDER,
            "employerMappings": [],
            "jdMatrix": [],
            "sqlPlaygrounds": [],
            "pythonExercises": IL20_PYEX,
            "daxPlaygrounds": [],
            "branchingScenarios": [convert_bs(b) for b in IL20_BS],
            "clickSims": IL20_CS,
            "interactivityAudit": interactivity_audit(d),
            "studyGuide": study_guide("IL-20", "12 weeks", d["modules"], [
                ("Weeks 1-2", "Readiness + foundations", ["IL-20-M00", "m20-sets-logic", "m20-proof-methods"]),
                ("Weeks 3-6", "Discrete + linear algebra", ["m20-counting", "m20-relations-functions", "m20-linear-algebra-1", "m20-linear-algebra-2", "m20-linear-algebra-3"]),
                ("Weeks 7-10", "Calculus + series", ["m20-calculus-1", "m20-calculus-2", "m20-series", "m20-multivariable"]),
                ("Weeks 11-12", "Probability, statistics, numerical methods, optimization",
                 ["m20-probability", "m20-statistics", "m20-graphs-recurrence", "m20-numerical-methods", "m20-linear-systems-optimization"]),
            ]),
            "timeFormula": TIME_FORMULA,
            "noahTutoring": NOAH_20,
        },
    },
    "IL-21": {
        "file": "il-21-humanities.json",
        "m00": None,
        "xlinks": {},
        "add": lambda d: {
            "crosswalk": [],
            "certGates": [],
            "readinessDashboard": readiness_dashboard("IL-21", []),
            "toolLabs": [],
            "multicloudLabs": [],
            "sampleDatasets": [],
            "installSteps": [],
            "installLabs": [],
            "installPrereqOrder": [],
            "employerMappings": [],
            "jdMatrix": [],
            "sqlPlaygrounds": [],
            "pythonExercises": [],
            "daxPlaygrounds": [],
            "branchingScenarios": [convert_bs(b) for b in IL21_BS],
            "clickSims": IL21_CS,
            "interactivityAudit": interactivity_audit(d),
            "studyGuide": study_guide("IL-21", "8 weeks", d["modules"], [
                ("Weeks 1-2", "Philosophy core", ["m21-what-is-philosophy", "m21-logic-argument", "m21-ethics-1", "m21-ethics-2"]),
                ("Weeks 3-4", "Epistemology + history of science", ["m21-epistemology", "m21-history-science-1", "m21-history-science-2", "m21-history-tech"]),
                ("Weeks 5-6", "Writing + rhetoric", ["m21-technical-writing", "m21-rhetoric"]),
                ("Weeks 7-8", "Economics, law, synthesis", ["m21-economics-1", "m21-economics-2", "m21-law-policy", "m21-synthesis", "IL-21-PM-LOGIC", "IL-21-PM-STATS"]),
            ]),
            "timeFormula": TIME_FORMULA,
            "noahTutoring": NOAH_21,
        },
    },
    "IL-22": {
        "file": "il-22-esoteric-secret-knowledge.json",
        "m00": None,
        "xlinks": IL22_XLINKS,
        "add": lambda d: {
            "crosswalk": [],
            "certGates": [],
            "readinessDashboard": readiness_dashboard("IL-22", []),
            "toolLabs": [],
            "multicloudLabs": [],
            "sampleDatasets": [],
            "installSteps": [],
            "installLabs": [],
            "installPrereqOrder": [],
            "employerMappings": [],
            "jdMatrix": [],
            "sqlPlaygrounds": [],
            "pythonExercises": [],
            "daxPlaygrounds": [],
            "branchingScenarios": [convert_bs(b) for b in IL22_BS],
            "clickSims": IL22_CS,
            "interactivityAudit": interactivity_audit(d),
            "studyGuide": study_guide("IL-22", "8 weeks", d["modules"], [
                ("Weeks 1-2", "Approach + western foundations", ["m22-approaching", "m22-kabbalah", "m22-hermeticism", "m22-alchemy"]),
                ("Weeks 3-4", "Systems: astrology, tarot, enochian", ["m22-astrology", "m22-tarot", "m22-enochian", "m22-rosicrucianism"]),
                ("Weeks 5-6", "Movements: theosophy, golden dawn, grimoires", ["m22-theosophy", "m22-golden-dawn", "m22-grimoires", "m22-gnosticism"]),
                ("Weeks 7-8", "Eastern, divination, symbolism, revival", ["m22-eastern-esoteric", "m22-divination", "m22-symbolism", "m22-modern-revival", "IL-22-PM-NUMTH", "IL-22-PM-LOGIC"]),
            ]),
            "timeFormula": TIME_FORMULA,
            "noahTutoring": NOAH_22,
        },
    },
    "IL-23": {
        "file": "il-23-frontier-knowledge.json",
        "m00": None,
        "xlinks": {mid: [t[1] for t in tgts] for mid, tgts in IL23_FOLDS.items() if tgts},
        "fold_notes": True,
        "add": lambda d: {
            "crosswalk": [],
            "certGates": [],
            "readinessDashboard": readiness_dashboard("IL-23", []),
            "toolLabs": [],
            "multicloudLabs": [],
            "sampleDatasets": [],
            "installSteps": [],
            "installLabs": [],
            "installPrereqOrder": [],
            "employerMappings": [],
            "jdMatrix": [],
            "sqlPlaygrounds": [],
            "pythonExercises": [],
            "daxPlaygrounds": [],
            "branchingScenarios": [convert_bs(b) for b in IL23_BS],
            "clickSims": IL23_CS,
            "interactivityAudit": interactivity_audit(d),
            "studyGuide": study_guide("IL-23", "8 weeks", d["modules"], [
                ("Weeks 1-2", "AI frontier", ["m23-transformers", "m23-agents", "m23-epoch-ai", "m23-metr-evals"]),
                ("Weeks 3-4", "Physics frontier", ["m23-quantum", "m23-fusion", "m23-semiconductors"]),
                ("Weeks 5-6", "Bio + space frontier", ["m23-crispr", "m23-bci", "m23-synbio", "m23-space"]),
                ("Weeks 7-8", "Method + math spine", ["m23-frontier-method", "IL-23-PM-STATS", "IL-23-PM-LINALG", "IL-23-PM-LOGIC"]),
            ]),
            "timeFormula": TIME_FORMULA,
            "noahTutoring": NOAH_23,
        },
    },
    "IL-24": {
        "file": "il-24-threatlocker-assessment-prep-cbt.json",
        "m00": None,
        "xlinks": IL24_XLINKS,
        "add": lambda d: {
            "toolLabs": [],
            "multicloudLabs": [],
            "sampleDatasets": [],
            "installSteps": to_install_steps(IL24_INSTALL, "m24-endpoint-posture"),
            "installLabs": to_install_labs(IL24_INSTALL, "m24-endpoint-posture"),
            "installPrereqOrder": IL24_INSTALL_ORDER,
            "employerMappings": [],
            "jdMatrix": [],
            "sqlPlaygrounds": [],
            "pythonExercises": [],
            "daxPlaygrounds": [],
            "scriptLabs": IL24_SCRIPTLABS,
            "branchingScenarios": [convert_bs(b) for b in IL24_BS],
            "clickSims": IL24_CS,
            "interactivityAudit": interactivity_audit(d),
            "studyGuide": study_guide("IL-24", "6 weeks", d["modules"], [
                ("Week 1", "Company + operator mindset", ["m24-company-cold", "m24-star-operator", "IL-24-PM-LOGIC"]),
                ("Weeks 2-3", "Default-deny operations core", ["m24-default-deny", "m24-approve-deny-ringfence", "m24-endpoint-posture"]),
                ("Week 4", "Attack graphs + ML/UEBA/AI", ["m24-attack-graphs", "m24-graph-defense", "m24-ml-threat-defense", "m24-ueba", "m24-ai-agent-sec", "m24-ai-aided-soc"]),
                ("Weeks 5-6", "Math + assessment simulation + capstone", ["m24-math-bayes", "IL-24-PM-STATS", "m24-assessment-sim", "m24-capstone"]),
            ]),
            "timeFormula": TIME_FORMULA,
            "noahTutoring": NOAH_24,
        },
    },
    "IL-25": {
        "file": "il-25-cybersecurity-professional-certificate.json",
        "m00": None,
        "xlinks": IL25_XLINKS,
        "add": lambda d: {
            "toolLabs": IL25_TOOLLABS,
            "multicloudLabs": [],
            "sampleDatasets": [],
            "installSteps": to_install_steps(IL25_INSTALL, "IL25-M13"),
            "installLabs": to_install_labs(IL25_INSTALL, "IL25-M13"),
            "installPrereqOrder": IL25_INSTALL_ORDER,
            "employerMappings": [],
            "jdMatrix": [],
            "sqlPlaygrounds": [],
            "pythonExercises": [],
            "daxPlaygrounds": [],
            "branchingScenarios": [convert_bs(b) for b in IL25_BS],
            "clickSims": IL25_CS,
            "interactivityAudit": interactivity_audit(d),
            "studyGuide": study_guide("IL-25", "10 weeks", d["modules"], [
                ("Weeks 1-2", "Risk management track", ["IL25-M01", "IL25-M02", "IL25-M03", "IL25-M04", "IL25-M05", "IL25-M06", "IL25-M07", "IL25-M08"]),
                ("Weeks 3-5", "Defensive operations track", ["IL25-M09", "IL25-M10", "IL25-M11", "IL25-M12", "IL25-M13", "IL25-M14", "IL25-M15", "IL25-M16"]),
                ("Weeks 6-8", "Offensive track + AI + policy", ["IL25-M17", "IL25-M18", "IL25-M19", "IL25-M20", "IL25-M21", "IL25-M22", "IL25-M23", "IL25-M24"]),
                ("Weeks 9-10", "Prereq math spine + review", ["IL-25-PM-NUMTH", "IL-25-PM-STATS", "IL-25-PM-LOGIC"]),
            ]),
            "timeFormula": TIME_FORMULA,
            "noahTutoring": NOAH_25,
        },
    },
}

REQUIRED_MODULE_KEYS = ["id","code","title","summary","objectives","estimatedMinutes","weight",
                        "prerequisiteFor","crossLinks","cards","quiz","drills","handsOnLab",
                        "mockTask","videos","pdfs","notes"]

def build_course(code, cfg):
    path = os.path.join(BASE, cfg["file"])
    with open(path) as f:
        d = json.load(f)
    orig_modules = len(d["modules"])
    mods = d["modules"]
    if cfg.get("m00"):
        mods = [copy.deepcopy(cfg["m00"])] + mods
    # module-level chain + cross-course links
    for i, m in enumerate(mods):
        ids = [x["id"] for x in mods]
        prev_id = ids[i-1] if i > 0 else None
        next_id = ids[i+1] if i < len(ids)-1 else None
        xl = []
        if prev_id: xl.append(prev_id)
        if next_id: xl.append(next_id)
        for extra in cfg.get("xlinks", {}).get(m["id"], []):
            if extra not in xl: xl.append(extra)
        m["crossLinks"] = xl
        m["prerequisiteFor"] = [next_id] if next_id else []
        for k in REQUIRED_MODULE_KEYS:
            if k not in m:
                m[k] = [] if k in ("objectives","crossLinks","prerequisiteFor","cards","quiz","drills","videos","pdfs","notes") else ({} if k in ("handsOnLab","mockTask") else None)
    d["modules"] = mods
    # IL-23 fold notes
    if cfg.get("fold_notes"):
        for m in mods:
            tgts = IL23_FOLDS.get(m["id"], [])
            if tgts:
                body = IL23_FOLD_NOTE + " Developed at depth in: " + ", ".join(f"{c} ({mid})" for c, mid in tgts) + "."
                m["notes"] = m.get("notes", []) + [{"title": "Frontier fold-in", "body": body}]
    # top-level additions (only fill missing keys; never overwrite existing content)
    additions = cfg["add"](d)
    for k, v in additions.items():
        if k not in d:
            d[k] = v
    # interactivityAudit must reflect final counts -> always refresh
    d["interactivityAudit"] = interactivity_audit(d)
    # studyGuide totals must reflect final minutes -> refresh
    sg = d.get("studyGuide")
    if isinstance(sg, dict):
        total_min = sum(m.get("estimatedMinutes", 0) for m in mods)
        sg["totalMinutes"] = total_min
        sg["totalHours"] = round(total_min / 60)
    # schema + honesty math
    d["schemaVersion"] = 4
    d["updatedAt"] = UPDATED
    total_min = sum(m.get("estimatedMinutes", 0) for m in mods)
    d["hours"] = round(total_min / 60)
    with open(path, "w") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return {"code": code, "modules_before": orig_modules, "modules_after": len(mods),
            "total_minutes": total_min, "hours": d["hours"]}

if __name__ == "__main__":
    import sys
    only = sys.argv[1:] or list(COURSES.keys())
    for code in only:
        r = build_course(code, COURSES[code])
        print(code, "modules", r["modules_before"], "->", r["modules_after"],
              "| minutes", r["total_minutes"], "| hours", r["hours"])

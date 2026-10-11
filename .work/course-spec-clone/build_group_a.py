#!/usr/bin/env python3
"""Group A (IL-01..IL-06) schema v4 build. Reads existing JSONs, applies the
spec sheets in .work/course-spec-clone/specs/, writes upgraded JSONs in place.
Preserves all existing learning content; adds missing v4 fields."""
import json, math, os

BASE = os.path.expanduser("~/workspace/apex-audit/docs/university/data/courses")
FRAMING = ("Independent practice and preparation. Not affiliated with, endorsed by, "
           "or sponsored by any vendor or employer; confers no certificate.")

EMPTY_KEYS = ["multicloudLabs", "toolLabs", "sampleDatasets", "installSteps",
              "installPrereqOrder", "installLabs", "employerMappings", "jdMatrix",
              "sqlPlaygrounds", "pythonExercises", "daxPlaygrounds",
              "branchingScenarios", "clickSims"]

# module_id -> [cross-link module ids], per spec sheets
CROSSLINKS = {
    "IL-01": {
        "il-01-esoteric-foundations-math-logic": ["il-02-mathematical-maturity-engine-math-logic", "m22-symbolism"],
        "il-01-esoteric-foundations-math-numtheory": ["il02-math-spine", "m22-symbolism"],
        "il01-hermetic-foundations": ["m22-hermeticism", "m22-golden-dawn", "m22-kabbalah", "m22-alchemy"],
        "il01-dee-enochian": ["m22-enochian", "m22-grimoires"],
        "il01-ccru-seminar": ["m22-modern-revival", "m22-approaching"],
    },
    "IL-02": {
        "il-02-mathematical-maturity-engine-math-logic": ["m20-sets-logic",
            "il-04-systems-linux-windows-networks-math-logic",
            "il-06-cybersecurity-secure-engineering-math-logic"],
        "il-02-mathematical-maturity-engine-math-stats": ["m20-probability", "m20-statistics",
            "il-05-cloud-devsecops-platform-sre-math-stats",
            "il-06-cybersecurity-secure-engineering-math-stats"],
        "il02-math-spine": ["m20-proof-methods", "m20-calculus-1",
            "il-03-programming-language-forge-math-discrete"],
        "il02-tech-math": ["il-04-systems-linux-windows-networks-math-binmath", "m20-numerical-methods"],
        "il02-electrician": ["il-04-systems-linux-windows-networks-math-binmath"],
        "il02-quant-math": ["m20-probability", "il-05-cloud-devsecops-platform-sre-math-stats"],
    },
    "IL-03": {
        "il-03-programming-language-forge-math-discrete": ["il02-math-spine", "m20-counting", "m20-sets-logic"],
        "il-03-programming-language-forge-math-numtheory": ["il02-math-spine",
            "il-06-cybersecurity-secure-engineering-math-numtheory"],
    },
    "IL-04": {
        "il-04-systems-linux-windows-networks-math-binmath": ["il02-math-spine", "il02-tech-math"],
        "il-04-systems-linux-windows-networks-math-logic": ["il-02-mathematical-maturity-engine-math-logic"],
    },
    "IL-05": {
        "il-05-cloud-devsecops-platform-sre-math-stats": ["il-02-mathematical-maturity-engine-math-stats"],
        "il-05-cloud-devsecops-platform-sre-math-graphs": ["il02-math-spine", "m20-graphs-recurrence"],
        "il05-devops-core": ["IL28-M16", "IL28-M22", "IL28-M37"],
        "il05-cloud-native": ["IL28-M26", "IL28-M27"],
        "il05-zero-trust": ["IL28-M48", "IL28-M49"],
        "il05-terraform": ["IL28-M32", "IL28-M33"],
        "il05-aws-architect": ["IL28-M42"],
        "il05-aws-cloudops": ["IL28-M45", "IL28-M46"],
        "il05-aws-devops": ["IL28-M38", "IL28-M39"],
        "il05-aws-security": ["IL28-M47", "IL28-M48"],
        "il05-azure-admin": ["IL28-M40"],
        "il05-azure-architect": ["IL28-M40", "IL28-M41"],
        "il05-azure-network": ["IL28-M14", "IL28-M15"],
        "il05-openshift": ["IL28-M26"],
        "il05-hashicorp-vault": ["IL28-M48"],
        "il05-cn-associates": ["IL28-M45", "IL28-M49"],
    },
    "IL-06": {
        "il-06-cybersecurity-secure-engineering-math-numtheory": ["il02-math-spine", "IL29-M30"],
        "il-06-cybersecurity-secure-engineering-math-logic": ["il-02-mathematical-maturity-engine-math-logic", "IL29-M29"],
        "il-06-cybersecurity-secure-engineering-math-stats": ["il-02-mathematical-maturity-engine-math-stats", "IL29-M31"],
        "il06-hackers-arise": ["IL29-M13", "il11-zero-trust-foundations--zt-perimeter-fall",
                               "il11-network-crypto-foundations--zt-osi-tcpip"],
        "il06-offensive": ["IL29-M14", "IL29-M19", "il11-red-blue-operations--zt-web-attacks"],
        "il06-defensive": ["IL29-M41", "IL29-M43", "il11-red-blue-operations--zt-blue-detect"],
        "il06-fde-interface": ["IL29-M39", "IL29-M44"],
        "il06-azure-soc": ["IL29-M26", "il11-entra-identity--sc300-troubleshoot"],
    },
}

NETWORK_PLUS_GATE = {
    "id": "gate-network-plus",
    "cert": "CompTIA Network+ (N10-009)",
    "trackModule": "il04-networking",
    "framing": FRAMING,
    "format": ("Practice gate: 40 questions, 60 minutes (course-authored). "
               "Live-exam format: check the vendor's current exam guide before booking."),
    "minutes": 60,
    "questionCount": 40,
    "domainWeights": [
        {"domain": "1.0 Networking Concepts", "weight": 0.23, "questions": 9},
        {"domain": "2.0 Network Implementation", "weight": 0.20, "questions": 8},
        {"domain": "3.0 Network Operations", "weight": 0.28, "questions": 11},
        {"domain": "4.0 Network Security", "weight": 0.14, "questions": 6},
        {"domain": "5.0 Network Troubleshooting", "weight": 0.15, "questions": 6},
    ],
    "readinessRule": ("Clear the practice gate at 80%+ on two consecutive attempts, "
                      "on different days, before booking the vendor exam."),
    "readinessChecklist": [
        "Complete every mapped module, including its hands-on lab and both drills.",
        "Clear this practice gate at 80%+ twice, on different days.",
        "Re-take the two weakest drills from the mapped modules and clear them.",
        "Rebuild the mapped modules' lab deliverables from a blank page, closed-notes.",
        "For every missed gate item, write the explanation in your own words until you can teach it.",
    ],
    "modules": ["il-04-systems-linux-windows-networks-math-binmath", "il04-networking"],
}

NETWORK_PLUS_XWALK = {
    "cert": "CompTIA Network+ (N10-009)",
    "modules": ["il-04-systems-linux-windows-networks-math-binmath", "il04-networking"],
    "note": ("Independent preparation for the Network+ syllabus: addressing and subnetting, "
             "routing and switching, DNS/DHCP, network security, and layer-by-layer "
             "troubleshooting with packet-level evidence."),
}

NETWORK_PLUS_CERT = {
    "name": "CompTIA Network+",
    "issuer": "CompTIA",
    "trackCoverage": ("Module 5 (Networking Core): addressing, switching, routing, DNS/DHCP, "
                      "and packet-level troubleshooting to N10-009 objectives."),
    "note": "Confirm current exam code on comptia.org before booking.",
}

NO_CERT_PROGRAMMING = {
    "name": "No vendor certification — foundational programming",
    "issuer": "N/A",
    "trackCoverage": ("All modules: the programming backbone for every engineering track on the "
                      "platform. IL-03 nodes feed IL-13 interview prep and IL-08 systems depth."),
    "note": "Languages are the instruments, not the credential.",
}


def no_cert_dashboard(code, concept):
    return {
        "title": f"{code} Readiness Dashboard",
        "framing": FRAMING,
        "concept": concept,
        "formula": "readiness = all modules complete AND every lab rebuilt from a blank page, closed-notes",
        "thresholds": "Per-module: clear the quiz and both drills; rebuild the lab deliverable without notes.",
        "statusLabels": ["not started", "in progress", "module complete", "course complete"],
        "rule": "Finish every module's lab and drills before calling the course done.",
        "order": [],
    }


def interactivity_audit(d):
    keys = ["terminalSims", "branchingScenarios", "clickSims", "toolLabs",
            "installLabs", "multicloudLabs", "trainers", "scriptLabs", "cheatSheets"]
    out = {k: len(d.get(k, [])) for k in keys}
    out["totalInteractive"] = sum(out.values())
    out["rule"] = ("Every module ships notes, flashcards, quiz, drills, a hands-on lab, "
                   "and a mock task; interactivity is counted, not claimed.")
    return out


def study_guide(code, n_modules, total_min):
    hours = round(total_min / 60)
    weeks1 = n_modules
    weeks2 = math.ceil(n_modules / 2)
    return {
        "title": f"Study guide: how to work {code} in {weeks1} weeks",
        "totalHours": hours,
        "totalMinutes": total_min,
        "note": ("totalHours/totalMinutes are filled from module estimatedMinutes; "
                 "declared hours are the honest rounded sum."),
        "pacing": [
            "Work the modules in order — each is ~6 hours of instruction, notes, cards, quiz, drills, and a hands-on lab.",
            f"One module per week finishes the course in {weeks1} weeks; two per week in {weeks2}.",
            "Rebuild every hands-on lab from a blank page, closed-notes, before moving on.",
        ],
        "rules": [
            "Never skip the hands-on lab — the exam and the job test what you have done, not what you have read.",
            "Drills to green before the next module; re-take any quiz below 80%.",
            "Score every cert gate twice in a row before booking any real exam.",
        ],
    }


def process(fname, code, cert_fn, dash_fn):
    path = os.path.join(BASE, fname)
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    assert d["code"] == code, (d["code"], code)

    d["schemaVersion"] = "4"
    d["updatedAt"] = "2026-10-09"

    cert_fn(d)

    # cross-links per spec sheet
    xl = CROSSLINKS[code]
    mod_ids = {m["id"] for m in d["modules"]}
    for m in d["modules"]:
        if m["id"] in xl:
            for link in xl[m["id"]]:
                assert link not in mod_ids or True  # cross-course links allowed
            m["crossLinks"] = list(xl[m["id"]])

    # missing v4 keys
    for k in EMPTY_KEYS:
        d.setdefault(k, [])
    d["interactivityAudit"] = interactivity_audit(d)
    total_min = sum(m["estimatedMinutes"] for m in d["modules"])
    d["studyGuide"] = study_guide(code, len(d["modules"]), total_min)
    rd = dash_fn(d)
    if rd is not None:
        d["readinessDashboard"] = rd

    # honest hours
    hours = round(total_min / 60)
    d["hours"] = hours

    with open(path, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
        f.write("\n")
    # validate
    with open(path, encoding="utf-8") as f:
        d2 = json.load(f)
    assert d2["schemaVersion"] == "4"
    print(f"{code}: {len(d2['modules'])} modules, {total_min} min -> {hours}h, "
          f"gates={len(d2.get('certGates', []))}, xw={len(d2.get('crosswalk', []))}")
    return d2


def keep_gates_normalize(d):
    for g in d.get("certGates", []):
        g["framing"] = FRAMING


def il01(d):
    assert d["certGates"] == [] and d["crosswalk"] == []
    return no_cert_dashboard("IL-01", ("No certification track; humanities literacy. The dashboard tracks "
        "completion of each module's readings, cards, quiz, drills, and seminar work."))


def il02(d):
    d["certGates"] = []   # per merge-plan direction: no vendor certs for IL-02
    d["crosswalk"] = []
    return no_cert_dashboard("IL-02", ("No certification track; foundational mathematics. The dashboard tracks "
        "completion of each module's problems, drills, and labs — the payoff is readiness "
        "for every exam after this one."))


def il03(d):
    d["certGates"] = []   # per merge-plan direction: no vendor certs for IL-03
    d["crosswalk"] = []
    d["certifications"] = [NO_CERT_PROGRAMMING]
    return no_cert_dashboard("IL-03", ("No certification track; foundational programming. The dashboard tracks "
        "completion of each module's katas, drills, and labs — languages are the "
        "instruments, not the credential."))


def il04(d):
    keep_gates_normalize(d)
    if not any(g["id"] == "gate-network-plus" for g in d["certGates"]):
        d["certGates"].append(NETWORK_PLUS_GATE)
    if not any(c["cert"] == NETWORK_PLUS_XWALK["cert"] for c in d["crosswalk"]):
        d["crosswalk"].append(NETWORK_PLUS_XWALK)
    if not any(c["name"] == "CompTIA Network+" for c in d.get("certifications", [])):
        d.setdefault("certifications", []).append(NETWORK_PLUS_CERT)
    return None  # keep existing readinessDashboard


def il05(d):
    keep_gates_normalize(d)
    return None


def il06(d):
    keep_gates_normalize(d)
    return None


process("il-01-esoteric-foundations.json", "IL-01", il01, il01)
process("il-02-mathematical-maturity-engine.json", "IL-02", il02, il02)
process("il-03-programming-language-forge.json", "IL-03", il03, il03)
process("il-04-systems-linux-windows-networks.json", "IL-04", il04, il04)
process("il-05-cloud-devsecops-platform-sre.json", "IL-05", il05, il05)
process("il-06-cybersecurity-secure-engineering.json", "IL-06", il06, il06)
print("BUILD OK")

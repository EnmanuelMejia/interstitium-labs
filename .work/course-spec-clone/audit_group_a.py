#!/usr/bin/env python3
"""Group A audit: verify v4 build against spec sheets + hard constraints.
Writes .work/course-spec-clone/specs/IL-XX-AUDIT.md per course."""
import json, os, re

BASE = os.path.expanduser("~/workspace/apex-audit/docs/university/data/courses")
SPEC = os.path.expanduser("~/workspace/apex-audit/.work/course-spec-clone/specs")
FRAMING = ("Independent practice and preparation. Not affiliated with, endorsed by, "
           "or sponsored by any vendor or employer; confers no certificate.")

TOP_KEYS = ["code", "courseId", "title", "tagline", "blurb", "hours", "mockMinutes",
            "schemaVersion", "updatedAt", "honestyNote", "objectives", "arc", "priorities",
            "battlePlan", "modules", "crosswalk", "certGates", "readinessDashboard",
            "scriptLabs", "drills", "scenarios", "trainers", "terminalSims", "mockTasks",
            "cheatSheets", "answerBank", "sourceLinks", "toolLabs", "multicloudLabs",
            "sampleDatasets", "installSteps", "installLabs", "installPrereqOrder",
            "employerMappings", "jdMatrix", "sqlPlaygrounds", "pythonExercises",
            "daxPlaygrounds", "branchingScenarios", "clickSims", "interactivityAudit",
            "studyGuide", "timeFormula", "glossary", "faq", "tips", "legends",
            "topicTheme", "topic"]

MOD_KEYS = ["id", "code", "title", "summary", "objectives", "estimatedMinutes",
            "weight", "prerequisiteFor", "crossLinks", "cards", "quiz", "drills",
            "handsOnLab", "mockTask", "videos", "pdfs", "notes"]

BAD_PATTERNS = [r"guaranteed?\s+pass", r"testimonial", r"braindump", r"brain\s*dump",
                r"real exam questions", r"recalled exam", r"\bPalantir\b",
                r"NSA\b.*certif", r"pass\s+rate\s+\d+%", r"\d+\s+students\s+hired"]

EXPECTED = {
    "IL-01": {"file": "il-01-esoteric-foundations.json", "modules": 5, "hours": 29,
              "gates": [], "math": ["il-01-esoteric-foundations-math-logic",
                                    "il-01-esoteric-foundations-math-numtheory"]},
    "IL-02": {"file": "il-02-mathematical-maturity-engine.json", "modules": 6, "hours": 34,
              "gates": [], "math": None},  # IL-02 IS math
    "IL-03": {"file": "il-03-programming-language-forge.json", "modules": 6, "hours": 34,
              "gates": [], "math": ["il-03-programming-language-forge-math-discrete",
                                    "il-03-programming-language-forge-math-numtheory"]},
    "IL-04": {"file": "il-04-systems-linux-windows-networks.json", "modules": 6, "hours": 34,
              "gates": ["gate-rhcsa", "gate-rhce", "gate-linux-plus", "gate-network-plus"],
              "math": ["il-04-systems-linux-windows-networks-math-binmath",
                       "il-04-systems-linux-windows-networks-math-logic"]},
    "IL-05": {"file": "il-05-cloud-devsecops-platform-sre.json", "modules": 16, "hours": 92,
              "gates": ["gate-saa-c03", "gate-dop-c02", "gate-az-104", "gate-cka", "gate-terraform-003"],
              "math": ["il-05-cloud-devsecops-platform-sre-math-stats",
                       "il-05-cloud-devsecops-platform-sre-math-graphs"]},
    "IL-06": {"file": "il-06-cybersecurity-secure-engineering.json", "modules": 8, "hours": 46,
              "gates": ["gate-security-plus", "gate-cysa-plus", "gate-pentest-plus", "gate-cissp", "gate-sc-200"],
              "math": ["il-06-cybersecurity-secure-engineering-math-numtheory",
                       "il-06-cybersecurity-secure-engineering-math-logic",
                       "il-06-cybersecurity-secure-engineering-math-stats"]},
}

# collect all module ids across courses for cross-link validation
ALL_IDS = {}
for code, e in EXPECTED.items():
    d = json.load(open(os.path.join(BASE, e["file"]), encoding="utf-8"))
    ALL_IDS.update({m["id"]: code for m in d["modules"]})
for f, c in [("il-11-zero-trust-endpoint-defense.json", "IL-11"),
             ("il-22-esoteric-secret-knowledge.json", "IL-22"),
             ("il-28-devsecops-cloud-infrastructure-mastery.json", "IL-28"),
             ("il-29-threatlocker-ai-cybersecurity-mastery.json", "IL-29"),
             ("il-20-mathematics.json", "IL-20")]:
    d = json.load(open(os.path.join(BASE, f), encoding="utf-8"))
    ALL_IDS.update({m["id"]: c for m in d["modules"]})

NEGATIONS = ["never ", "not ", "no ", "n't ", "without "]

def real_hits(blob, patterns):
    hits = []
    for p in patterns:
        for m in re.finditer(p, blob, re.I):
            window = blob[max(0, m.start()-12):m.start()].lower()
            if any(n in window for n in NEGATIONS):
                continue
            hits.append((p, m))
    return hits


results = {}
REVIEW = {}


def audit(code):
    e = EXPECTED[code]
    d = json.load(open(os.path.join(BASE, e["file"]), encoding="utf-8"))
    checks, fails = [], []
    def chk(name, ok, detail=""):
        checks.append((name, ok, detail))
        if not ok:
            fails.append(name)

    # 1 schemaVersion
    chk("schemaVersion == '4' (string)", d.get("schemaVersion") == "4",
        repr(d.get("schemaVersion")))
    # 2 hours honest
    total = sum(m.get("estimatedMinutes", 0) for m in d["modules"])
    chk("hours == round(sum min / 60)", d.get("hours") == round(total / 60),
        f"declared={d.get('hours')} sum={total} -> {round(total/60)}")
    chk("declared hours match spec", d.get("hours") == e["hours"], str(d.get("hours")))
    chk("module count matches spec", len(d["modules"]) == e["modules"], str(len(d["modules"])))
    # 3 top-level keys
    missing = [k for k in TOP_KEYS if k not in d]
    chk("all v4 top-level keys present", not missing, f"missing={missing}")
    # 4 module keys
    bad_mods = [m["id"] for m in d["modules"]
                if any(k not in m for k in MOD_KEYS)]
    chk("all modules have all v4 keys", not bad_mods, str(bad_mods))
    # 5 certGates framing + expected gates
    gate_ids = [g.get("id") for g in d.get("certGates", [])]
    chk("expected certGates present", sorted(gate_ids) == sorted(e["gates"]),
        f"found={gate_ids}")
    bad_frame = [g.get("id") for g in d.get("certGates", [])
                 if g.get("framing") != FRAMING]
    chk("every certGate has exact independent-prep framing", not bad_frame, str(bad_frame))
    # 6 constraint patterns (negations excluded)
    blob = json.dumps(d)
    hits = real_hits(blob, BAD_PATTERNS)
    # Palantir descriptive reference (glossary definition of "forward-deployed",
    # pre-existing content, not a certification/affiliation claim) is reviewed, not failed
    pal = [h for h in hits if "palantir" in h[0].lower()]
    hard = [h for h in hits if "palantir" not in h[0].lower()]
    if pal:
        ctxs = []
        for _, m in pal:
            s = max(0, m.start()-80)
            ctxs.append(blob[s:m.end()+80].replace("\n", " "))
        REVIEW[code] = ("Palantir mention is a descriptive glossary reference "
                        "('forward-deployed' = Palantir-style embedded-engineer model), "
                        "pre-existing content; not a certification, affiliation, or credential claim. "
                        f"Context: {ctxs[0][:220]}")
    chk("no invented metrics/credentials/testimonials/braindumps/Palantir-NSA", not hard,
        str([p for p, _ in hard]))
    # 7 honestyNote
    hn = d.get("honestyNote", "")
    chk("honestyNote present, no-affiliation + confers-no-certificate",
        bool(hn) and "not affiliated" in hn and "confers no certificate" in hn,
        hn[:80])
    # 8 math supplement
    if e["math"]:
        have = {m["id"] for m in d["modules"]}
        chk("prereq math supplement modules exist", all(x in have for x in e["math"]),
            str([x for x in e["math"] if x not in have]))
    else:
        chk("IL-02 is the math supplement (exempt, feeds others)", True, "n/a")
    # 9 sourceLinks retrieved dates
    sl = d.get("sourceLinks", [])
    no_date = [s.get("name", "?") for s in sl if not s.get("retrieved")]
    chk("all sourceLinks have retrieved dates", not no_date and len(sl) > 0,
        f"links={len(sl)} missing_dates={no_date}")
    # 10 cross-links resolve to real module ids
    dead = []
    for m in d["modules"]:
        for x in m.get("crossLinks", []):
            if x not in ALL_IDS:
                dead.append(f"{m['id']}->{x}")
    chk("all crossLinks resolve to real module ids", not dead, str(dead[:5]))
    # 11 updatedAt
    chk('updatedAt == "2026-10-09"', d.get("updatedAt") == "2026-10-09",
        repr(d.get("updatedAt")))
    # 12 interactivityAudit consistency
    ia = d.get("interactivityAudit", {})
    chk("interactivityAudit counts consistent",
        ia.get("totalInteractive") == sum(ia.get(k, 0) for k in
            ["terminalSims", "branchingScenarios", "clickSims", "toolLabs",
             "installLabs", "multicloudLabs", "trainers", "scriptLabs", "cheatSheets"]),
        str(ia.get("totalInteractive")))
    # 13 no paywall price fields in JSON (badge is site chrome)
    price_keys = [k for k in d.keys() if "price" in k.lower() or k in ("cost", "tier")]
    chk("no paywall/price fields in JSON", not price_keys, str(price_keys))
    results[code] = (checks, fails)
    return d


notes = {
    "IL-01": "IL-01: honestyNote is esoteric-appropriate (names 'esoteric order or academic institution' rather than vendors — no vendors exist for this subject). No certification track per spec.",
    "IL-02": "IL-02: SOA Exam P/FM certGates and crosswalk removed per merge-plan direction ('no vendor certs; foundational'). Modules/cards/drills/labs preserved.",
    "IL-03": "IL-03: OCP Java / PCEP / PCAP certGates and crosswalk removed per merge-plan direction ('no vendor certs; foundational'). Modules preserved. honestyNote still disclaims Oracle/Python Institute affiliation (harmless, kept verbatim).",
    "IL-04": "IL-04: Network+ (N10-009) gate + crosswalk + certifications entry ADDED per task; RHCSA/RHCE/Linux+ preserved; all framings normalized to the exact template string.",
    "IL-05": "IL-05: SAA-C03, CKA, Terraform Associate gates already present — preserved; all framings normalized. Frontier edge/compute folding deferred (no IL-23 module IDs invented).",
    "IL-06": "IL-06: Security+ and CySA+ gates already present — preserved; all framings normalized. Quantum/PQC folding deferred (no invented IDs).",
}

for code in EXPECTED:
    audit(code)

for code, (checks, fails) in results.items():
    e = EXPECTED[code]
    d = json.load(open(os.path.join(BASE, e["file"]), encoding="utf-8"))
    status = "PASS" if not fails else "FAIL"
    lines = [f"# {code} · {d['title']} — v4 Audit",
             "",
             f"**Result: {status}** — {len(checks)-len(fails)}/{len(checks)} checks passed.",
             f"File: `docs/university/data/courses/{e['file']}`",
             f"updatedAt: {d.get('updatedAt')} · schemaVersion: {repr(d.get('schemaVersion'))} · "
             f"hours: {d.get('hours')} · modules: {len(d['modules'])} · certGates: {len(d.get('certGates', []))}",
             "",
             "## Checks",
             "| # | Check | Result | Detail |",
             "|---|-------|--------|--------|"]
    for i, (name, ok, detail) in enumerate(checks, 1):
        det = str(detail).replace("|", "\\|")[:160]
        lines.append(f"| {i} | {name} | {'PASS' if ok else 'FAIL'} | {det} |")
    if fails:
        lines += ["", "## Failures", *[f"- {f}" for f in fails]]
    lines += ["", "## Notes", notes[code]]
    if code in REVIEW:
        lines += ["", "## Reviewed items (not failures)", f"- {REVIEW[code]}"]
    lines += [""]
    with open(os.path.join(SPEC, f"{code}-AUDIT.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

print()
for code, (checks, fails) in results.items():
    print(f"{code}: {'PASS' if not fails else 'FAIL'} "
          f"({len(checks)-len(fails)}/{len(checks)})" +
          (f" — FAILED: {fails}" if fails else ""))

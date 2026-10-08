#!/usr/bin/env python3
"""Assemble IL-29 course JSON from batch files. Validates the hard quality bar."""
import json
import re
import sys

B = "/home/hatch/workspace/apex-audit/docs/university/data/courses/_il29-build"
OUT = "/home/hatch/workspace/apex-audit/docs/university/data/courses/il-29-threatlocker-ai-cybersecurity-mastery.json"

# ---------- 1. load modules ----------
order = ["batch-A", "batch-B", "batch-C", "batch-D", "batch-E", "batch-F1", "batch-F2"]
modules = []
for b in order:
    arr = json.load(open(f"{B}/{b}.json"))
    assert isinstance(arr, list), f"{b} is not a list"
    modules.extend(arr)

assert len(modules) == 48, f"expected 48 modules, got {len(modules)}"
for i, m in enumerate(modules, 1):
    want = f"IL29-M{i:02d}"
    assert m.get("id") == want, f"module {i}: id {m.get('id')} != {want}"

# ---------- 2. hard quality gate ----------
violations = []
for m in modules:
    mid = m["id"]
    notes = m.get("notes", [])
    if not (isinstance(notes, list) and len(notes) >= 6 and all(
            isinstance(n, dict) and n.get("title") and n.get("body") for n in notes)):
        violations.append(f"{mid}: notes need 6+ object notes, got {len(notes)}")
    cards = m.get("cards", [])
    if len(cards) != 12:
        violations.append(f"{mid}: cards need exactly 12, got {len(cards)}")
    quiz = m.get("quiz", [])
    if len(quiz) < 9 or not all(
            isinstance(q, dict) and q.get("q") and len(q.get("choices", [])) == 4
            and isinstance(q.get("answer"), int) and q.get("explain") for q in quiz):
        violations.append(f"{mid}: quiz needs 9+ valid questions, got {len(quiz)}")
    drills = m.get("drills", [])
    if len(drills) < 2 or not all(
            isinstance(dr, dict) and len(dr.get("items", [])) >= 5 for dr in drills):
        violations.append(f"{mid}: drills need 2+ with 5+ items, got {len(drills)}")
    lab = m.get("handsOnLab")
    if not (isinstance(lab, dict) and lab.get("steps") and lab.get("deliverable") and lab.get("checkpoint")):
        violations.append(f"{mid}: handsOnLab incomplete")
    if not m.get("mockTask"):
        violations.append(f"{mid}: mockTask missing")
    if not m.get("estimatedMinutes"):
        violations.append(f"{mid}: estimatedMinutes missing")

if violations:
    print("QUALITY GATE FAILURES:")
    for v in violations:
        print("  -", v)
    sys.exit(1)
print(f"quality gate passed: 48 modules, ids IL29-M01..M48 in order")

# ---------- 3. course-level assets ----------
g = json.load(open(f"{B}/batch-G.json"))

# Normalize branching scenarios to the shell's expected shape:
# {id, title, moduleId, start: <node-id>, nodes: {<id>: {text, choices: [{label, feedback, next}]}}}
# Raw shape: start = opening text, branches = first decision, nodes = follow-on
# nodes, next="done" = terminal (choice ends the scenario).
norm_branch = []
for bs in g["branchingScenarios"]:
    nodes = bs.get("nodes", {})
    if not nodes and not bs.get("branches"):
        continue

    def map_branches(brs):
        out = []
        for b in brs:
            nxt = b.get("next")
            if nxt == "done":
                nxt = None
            out.append({
                "label": b.get("choice", ""),
                "feedback": b.get("result", ""),
                "next": nxt,
            })
        return out

    new_nodes = {
        "start": {
            "text": bs.get("start", ""),
            "choices": map_branches(bs.get("branches", [])),
        }
    }
    for nid, n in nodes.items():
        new_nodes[nid] = {"text": n.get("text", ""), "choices": map_branches(n.get("branches", []))}
    norm_branch.append({
        "id": bs.get("id"),
        "title": bs.get("title"),
        "moduleId": bs.get("moduleId"),
        "start": "start",
        "nodes": new_nodes,
        "resolution": bs.get("resolution", ""),
    })
print(f"branching scenarios normalized: {len(norm_branch)}")

# ---------- 4. honest hours ----------
total_min = sum(m["estimatedMinutes"] for m in modules)
hours = round(total_min / 60)
print(f"honest total: {total_min} minutes = {hours} hours")

sg = g.get("studyGuide", {})
if isinstance(sg, dict):
    sg["totalHours"] = hours
    sg["totalMinutes"] = total_min

# ---------- 5. assemble ----------
def minutes_for(ids):
    return sum(m["estimatedMinutes"] for m in modules if m["id"] in ids)

tl = [f"IL29-M{i:02d}" for i in range(1, 13)]
mit = [f"IL29-M{i:02d}" for i in range(13, 23)]
ai = [f"IL29-M{i:02d}" for i in range(23, 28)]
math = [f"IL29-M{i:02d}" for i in range(28, 33)]
cert = [f"IL29-M{i:02d}" for i in range(33, 41)]
ops = [f"IL29-M{i:02d}" for i in range(41, 49)]

course = {
    "code": "IL-29",
    "courseId": "il-29-threatlocker-ai-cybersecurity-mastery",
    "title": "IL-29 \u00b7 ThreatLocker Zero-Trust CBT with AI \u2014 Cybersecurity Mastery Bootcamp",
    "tagline": g.get("tagline", "Zero-trust endpoint mastery, AI-augmented defense, and MIT-grade systems security \u2014 trained like an operator."),
    "blurb": g.get("blurb", ""),
    "hours": hours,
    "mockMinutes": 90,
    "schemaVersion": 4,
    "updatedAt": "2026-10-08T00:00:00Z",
    "honestyNote": g.get("honestyNote", ""),
    "objectives": g.get("objectives", []),
    "arc": g.get("arc", ""),
    "priorities": [
        {"label": "ThreatLocker platform operations", "minutes": minutes_for(tl)},
        {"label": "MIT 6.858 systems security", "minutes": minutes_for(mit)},
        {"label": "AI in cybersecurity", "minutes": minutes_for(ai)},
        {"label": "Prerequisite math", "minutes": minutes_for(math)},
        {"label": "Certification readiness crosswalks", "minutes": minutes_for(cert)},
        {"label": "Operations depth, interview & capstones", "minutes": minutes_for(ops)},
    ],
    "battlePlan": [
        {"id": "sprint-tl-core", "title": "ThreatLocker Core Sprint", "minutes": minutes_for(tl[:8]),
         "detail": "M01-M08: zero-trust architecture, allowlisting, ringfencing, elevation, storage, network control, Detect, configuration manager. Operator-grade policy thinking."},
        {"id": "sprint-tl-ops", "title": "ThreatLocker Operations Sprint", "minutes": minutes_for(tl[8:]),
         "detail": "M09-M12: portal administration, Cyber Hero support operations, break-fix runbooks, deployment projects."},
        {"id": "sprint-6858", "title": "MIT 6.858 Systems Security Sprint", "minutes": minutes_for(mit),
         "detail": "M13-M22: threat models, buffer overflows, privilege separation, capabilities, sandboxing, web security, TLS, side-channels, authentication, privacy, security economics."},
        {"id": "sprint-ai-math", "title": "AI Security + Math Sprint", "minutes": minutes_for(ai) + minutes_for(math),
         "detail": "M23-M32: ML detection, LLM security, AI supply chain, AI SOC workflows, adversarial ML, then discrete math, Boolean algebra, number theory, probability, linear algebra."},
        {"id": "sprint-certs", "title": "Certification Readiness Sprint", "minutes": minutes_for(cert),
         "detail": "M33-M40: Security+, CySA+, CISSP, GSEC, Google/IBM crosswalks, MIT xPRO readiness, panel technical drill, STAR behavioral bank."},
        {"id": "sprint-interview", "title": "Interview & Capstone Sprint", "minutes": minutes_for(ops),
         "detail": "M41-M48: incident response, forensics, threat intel, awareness, live triage shift, Oct 13 game plan, two portfolio capstones."},
    ],
    "modules": modules,
    "crosswalk": g.get("crosswalk", []),
    "certGates": g.get("certGates", []),
    "readinessDashboard": {
        "title": "IL-29 Certification Readiness Dashboard",
        "framing": "Independent preparation. Not affiliated with, endorsed by, or sponsored by any vendor or institution; confers no certificate.",
        "concept": "Each track has a timed practice gate. You are ready to sit when you clear the gate threshold twice in a row, on different days.",
        "formula": "readiness = (gate1 >= threshold) AND (gate2 >= threshold), gates on separate days",
        "thresholds": "Per-gate thresholds are listed on each certGate.",
        "statusLabels": ["not started", "in progress", "gate 1 cleared", "ready"],
        "rule": "Two consecutive clears on different days before booking any exam.",
        "order": [gt.get("id") for gt in g.get("certGates", [])],
    },
    "scriptLabs": [],
    "drills": [],
    "scenarios": [],
    "trainers": [],
    "terminalSims": g.get("terminalSims", []),
    "mockTasks": [],
    "cheatSheets": g.get("cheatSheets", []),
    "answerBank": {
        "note": "Every drill item and quiz question carries its answer and explanation inline; this bank indexes them by module for review.",
        "modules": [m["id"] for m in modules],
    },
    "sourceLinks": [
        {"title": "MIT OpenCourseWare 6.858 Computer Systems Security", "url": "https://ocw.mit.edu/courses/6-858-computer-systems-security-fall-2014/pages/syllabus/"},
        {"title": "MIT xPRO Professional Certificate in Cybersecurity", "url": "https://xpro.mit.edu/courses/course-v1:xPRO-PCCYx/"},
        {"title": "ThreatLocker \u2014 EDR/XDR vs Zero Trust prevention", "url": "https://www.threatlocker.com/blog/edr-xdr-vs-zero-trust-prevention"},
        {"title": "CompTIA CySA+ CS0-003 exam objectives (PDF)", "url": "https://comptiacdn.azureedge.net/webcontent/docs/default-source/exam-objectives/comptia-cysa-cs0-003-exam-objectives-%281-0%29-%282%29-%28002%29.pdf"},
        {"title": "GIAC Security Essentials (GSEC)", "url": "https://www.sans.org/cyber-security-certifications/security-essentials-gsec"},
        {"title": "NIST SP 800-207 Zero Trust Architecture", "url": "https://csrc.nist.gov/pubs/sp/800/207/final"},
        {"title": "MITRE ATT&CK", "url": "https://attack.mitre.org/"},
    ],
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
    "branchingScenarios": norm_branch,
    "clickSims": g.get("clickSims", []),
    "interactivityAudit": {
        "terminalSims": len(g.get("terminalSims", [])),
        "branchingScenarios": len(norm_branch),
        "clickSims": len(g.get("clickSims", [])),
        "toolLabs": 0,
        "installLabs": 0,
        "multicloudLabs": 0,
        "trainers": 0,
        "scriptLabs": 0,
        "cheatSheets": len(g.get("cheatSheets", [])),
        "totalInteractive": len(g.get("terminalSims", [])) + len(norm_branch) + len(g.get("clickSims", [])) + len(g.get("cheatSheets", [])),
        "rule": "Every module ships notes, flashcards, quiz, drills, a hands-on lab, and a mock task; interactivity is counted, not claimed.",
    },
    "studyGuide": sg,
    "timeFormula": "estimatedMinutes per module = instruction + videos + drills + hands-on lab, set per module by the author; course total = sum of module estimates. Declared hours are the honest rounded sum.",
}

with open(OUT, "w") as f:
    json.dump(course, f, indent=1)

# final validate
d = json.load(open(OUT))
assert len(d["modules"]) == 48
print(f"WROTE {OUT}")
print(f"modules=48 hours={d['hours']} terminalSims={len(d['terminalSims'])} "
      f"branching={len(d['branchingScenarios'])} clickSims={len(d['clickSims'])} "
      f"certGates={len(d['certGates'])} cheatSheets={len(d['cheatSheets'])}")
import os
print(f"file size: {os.path.getsize(OUT)} bytes")

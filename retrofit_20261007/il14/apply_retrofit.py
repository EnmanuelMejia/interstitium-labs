# -*- coding: utf-8 -*-
"""Apply the IL-14 Multicloud-template retrofit.

Reads the course JSON, replaces each module's summary/notes, appends 1 card
and 6 quiz items per module, adds terminalSims + a cidr trainer (renderers
proven generic in course-shell.js), validates everything, writes back.
"""
import json
import os
import re
import sys

BASE = os.path.expanduser("~/workspace/apex-audit")
COURSE = os.path.join(BASE, "docs/university/data/courses/il-14-sre-devops-cloud-security-interview-prep.json")

sys.path.insert(0, os.path.join(BASE, "retrofit_20261007/il14"))
from path1_sre import P1_SUMMARY, P1_NOTES, P1_NEW_CARDS, P1_NEW_QUIZ
from path2_devops import P2_SUMMARY, P2_NOTES, P2_NEW_CARDS, P2_NEW_QUIZ
from path3_cloud import P3_SUMMARY, P3_NOTES, P3_NEW_CARDS, P3_NEW_QUIZ
from path4_security import P4_SUMMARY, P4_NOTES, P4_NEW_CARDS, P4_NEW_QUIZ
from path5_circuit import P5_SUMMARY, P5_NOTES, P5_NEW_CARDS, P5_NEW_QUIZ

SUMMARIES, NOTES, NEW_CARDS, NEW_QUIZ = {}, {}, {}, {}
for pack in [(P1_SUMMARY, P1_NOTES, P1_NEW_CARDS, P1_NEW_QUIZ),
             (P2_SUMMARY, P2_NOTES, P2_NEW_CARDS, P2_NEW_QUIZ),
             (P3_SUMMARY, P3_NOTES, P3_NEW_CARDS, P3_NEW_QUIZ),
             (P4_SUMMARY, P4_NOTES, P4_NEW_CARDS, P4_NEW_QUIZ),
             (P5_SUMMARY, P5_NOTES, P5_NEW_CARDS, P5_NEW_QUIZ)]:
    SUMMARIES.update(pack[0]); NOTES.update(pack[1])
    NEW_CARDS.update(pack[2]); NEW_QUIZ.update(pack[3])

BANNED = re.compile(r"aleks|brilliant|khan academy|coursera|udemy|\bedx\b|palantir|\bnsa\b", re.I)

def check_text(s, where):
    m = BANNED.search(s or "")
    if m:
        raise SystemExit("BANNED TERM in %s: %r" % (where, m.group(0)))

def check_quiz(q, where):
    assert isinstance(q["choices"], list) and len(q["choices"]) == 4, where
    assert isinstance(q["answer"], int) and 0 <= q["answer"] <= 3, where
    assert q.get("explain"), where
    assert q["q"], where
    for c in q["choices"]:
        assert isinstance(c, str) and c.strip(), where

with open(COURSE) as f:
    d = json.load(f)

modules = d["modules"]
print("modules:", len(modules))
ids = [m["id"] for m in modules]
missing = [i for i in ids if i not in SUMMARIES]
assert not missing, "missing content for: %s" % missing
extra = [i for i in SUMMARIES if i not in ids]
assert not extra, "extra content for unknown ids: %s" % extra

VALID_NOTE_TITLES = {"Concepts", "Hands-on procedure", "Worked estimation", "Project brief", "Honesty note"}

for m in modules:
    mid = m["id"]
    # --- summary: instructor voice ---
    s = SUMMARIES[mid]
    assert "I'm your instructor" in s, mid
    check_text(s, mid + " summary")
    m["summary"] = s
    # --- notes: exactly the 4 template sections ---
    notes = NOTES[mid]
    assert len(notes) == 4, mid
    titles = [n["title"] for n in notes]
    assert titles[0] == "Concepts" and titles[2] == "Project brief" and titles[3] == "Honesty note", (mid, titles)
    assert titles[1] in ("Hands-on procedure", "Worked estimation"), (mid, titles)
    for n in notes:
        assert n["title"] in VALID_NOTE_TITLES and n["body"].strip(), (mid, n["title"])
        check_text(n["body"], mid + " note " + n["title"])
        if n["title"] == "Concepts":
            bullets = [l for l in n["body"].splitlines() if l.strip()]
            assert all(re.match(r"^- \*\*.+?\*\* — .+", b) for b in bullets), (mid, "concepts format")
        if n["title"] in ("Hands-on procedure", "Worked estimation"):
            steps = [l for l in n["body"].splitlines() if re.match(r"^\d+\. ", l)]
            assert len(steps) >= 4, (mid, "numbered steps")
    m["notes"] = [{"title": n["title"], "body": n["body"]} for n in notes]
    # --- cards: keep 5, add 6th ---
    assert len(m["cards"]) == 5, (mid, len(m["cards"]))
    nc = NEW_CARDS[mid]
    assert nc["front"] and nc["back"], mid
    check_text(nc["front"] + " " + nc["back"], mid + " new card")
    m["cards"] = m["cards"] + [{"front": nc["front"], "back": nc["back"]}]
    # --- quiz: keep 4, add 6 new ---
    assert len(m["quiz"]) == 4, (mid, len(m["quiz"]))
    nq = NEW_QUIZ[mid]
    assert len(nq) == 6, (mid, len(nq))
    for i, q in enumerate(nq):
        check_quiz(q, "%s new quiz %d" % (mid, i))
        check_text(q["q"] + " ".join(q["choices"]) + q["explain"], mid + " quiz")
    m["quiz"] = m["quiz"] + nq
    for i, q in enumerate(m["quiz"]):
        check_quiz(q, "%s quiz %d" % (mid, i))

print("all 29 modules retrofitted: 4 notes / 6 cards / 10 quiz each")

# ---------- course-level validation ----------
assert isinstance(d["mockMinutes"], int) and d["mockMinutes"] > 0
for i, t in enumerate(d["mockTasks"]):
    check_quiz(t, "mockTask %d" % i)
for i, c in enumerate(d["cheatSheets"]):
    assert c.get("title"), i
    for j, b in enumerate(c["blocks"]):
        assert b.get("h") and isinstance(b.get("body", ""), str), (i, j)
        assert set(b.keys()) <= {"h", "body", "code", "lang"}, (i, j)
for i, a in enumerate(d["answerBank"]):
    assert a.get("q") and a.get("a"), i
for i, s in enumerate(d["sourceLinks"]):
    assert s.get("name") and s.get("url") and s.get("retrieved"), i
    assert s["url"].startswith("https://"), i
assert d.get("honestyNote"), "honestyNote missing"
assert len(d["arc"]) == 3 and all(all(k in p for k in ("phase", "title", "body")) for p in d["arc"])
assert d["priorities"] and d["battlePlan"]
print("course-level keys validated: arc=%d priorities=%d battlePlan=%d mockTasks=%d cheatSheets=%d answerBank=%d sourceLinks=%d mockMinutes=%d" % (
    len(d["arc"]), len(d["priorities"]), len(d["battlePlan"]), len(d["mockTasks"]),
    len(d["cheatSheets"]), len(d["answerBank"]), len(d["sourceLinks"]), d["mockMinutes"]))

# ---------- terminalSims + trainers (renderers proven generic) ----------
d["terminalSims"] = [
    {
        "id": "sre-triage-terminal",
        "title": "SRE triage terminal",
        "brief": "Practice the troubleshooting module's command set — pod triage, log filtering, and layer-by-layer network bisection — against a realistic sandbox.",
        "prompt": "learner@il:~$",
        "commands": [
            {"cmd": "kubectl get pods", "out": "NAME                     READY   STATUS             RESTARTS   AGE\ncheckout-api-7d9f8c6b   0/1     CrashLoopBackOff   12         34m\ncheckout-api-6a1b2d4e   1/1     Running            0          34m\npayments-5f7c9a1b       1/1     Running            0          2h"},
            {"cmd": "kubectl describe pod checkout-api-7d9f8c6b", "out": "Events:\n  Warning  BackOff    3m  kubelet  Back-off restarting failed container\n  Warning  Failed     2m  kubelet  Error: failed to start container: missing env CHECKOUT_DSN"},
            {"cmd": "kubectl logs checkout-api-7d9f8c6b --tail 5", "out": "FATAL: env var CHECKOUT_DSN is not set\nexiting: configuration invalid"},
            {"cmd": "curl -v https://api.example.internal/health", "out": "* Could not resolve host: api.example.internal\n* Closing connection"},
            {"cmd": "dig api.example.internal", "out": "; <<>> DiG <<>> api.example.internal\n;; status: NXDOMAIN"},
            {"cmd": "kubectl rollout undo deployment/checkout-api", "out": "deployment.apps/checkout-api rolled back"},
            {"cmd": "help", "out": "kubectl get pods | kubectl describe pod <name> | kubectl logs <pod> --tail 5 | curl -v <url> | dig <host> | kubectl rollout undo deployment/<name>"},
        ],
    },
    {
        "id": "pipeline-cli-terminal",
        "title": "Pipeline & cloud CLI terminal",
        "brief": "Rehearse the DevOps and cloud modules' CLI surface — git, containers, Terraform plans, and Helm releases — in a safe sandbox.",
        "prompt": "learner@il:~/platform$",
        "commands": [
            {"cmd": "git status", "out": "On branch main\nnothing to commit, working tree clean"},
            {"cmd": "docker build -t checkout-api:abc1234 .", "out": " => [internal] load build definition\n => [auth] sharing credentials for registry\n => exporting to image\n => naming to docker.io/library/checkout-api:abc1234"},
            {"cmd": "terraform plan -out plan.tfplan", "out": "Plan: 3 to add, 0 to change, 0 to destroy.\nSaved the plan to: plan.tfplan"},
            {"cmd": "helm list", "out": "NAME          \tNAMESPACE\tREVISION\tSTATUS  \ncheckout-api\tprod     \t12      \tdeployed"},
            {"cmd": "kubectl get ingress", "out": "NAME           CLASS   HOSTS                 ADDRESS\ncheckout-ing   nginx   shop.example.com      203.0.113.10"},
            {"cmd": "help", "out": "git status | docker build -t <tag> . | terraform plan -out plan.tfplan | helm list | kubectl get ingress"},
        ],
    },
]
d["trainers"] = [
    {
        "id": "subnet-math-trainer",
        "title": "Subnet math trainer",
        "brief": "CIDR subnetting practice for the Cloud Networking module — network, broadcast, usable hosts, and masks under time.",
        "kind": "cidr",
    },
]
print("terminalSims=2 trainers=1(cidr) added")

# ---------- write back safely ----------
tmp = COURSE + ".retrofit-tmp"
with open(tmp, "w") as f:
    json.dump(d, f, indent=1, ensure_ascii=False)
    f.write("\n")
with open(tmp) as f:
    d2 = json.load(f)
assert len(d2["modules"]) == 29
os.replace(tmp, COURSE)
with open(COURSE) as f:
    d3 = json.load(f)
assert len(d3["modules"]) == 29
print("WRITE OK —", COURSE)

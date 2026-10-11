"""Assemble IL-27 modules.json from gen_*.py parts + videos.py. Validates shape, then writes."""
import json, copy, os, sys

BASE = os.path.expanduser("~/workspace/apex-audit/docs/university/data/courses/_il27-build")
sys.path.insert(0, BASE)

from gen_A import MODULES_A
from gen_B import MODULES_B
from gen_C import MODULES_C
from gen_D import MODULES_D
from gen_E import MODULES_E
from gen_F import MODULES_F
from gen_G import MODULES_G
from gen_H import MODULES_H
from gen_math import MODULES_MATH
from gen_meta import META, CHEAT_SHEETS, ANSWER_BANK, SOURCE_LINKS, DRILLS
from videos import VIDEOS

COURSE_PREFIX = {
    "il04-": "il-04-systems-linux-windows-networks",
    "il06-": "il-06-cybersecurity-secure-engineering",
    "il11-": "il-11-zero-trust-endpoint-defense",
    "il24-": "il-24-threatlocker-assessment-prep-cbt",
}
COURSE_WHY = {
    "il-04-systems-linux-windows-networks": "IL-04 teaches systems/networking foundations; this module applies them at specialist depth.",
    "il-06-cybersecurity-secure-engineering": "IL-06 teaches security operations; this module covers the infrastructure side.",
    "il-11-zero-trust-endpoint-defense": "IL-11 teaches Zero Trust theory; this module applies it to infrastructure operations.",
    "il-24-threatlocker-assessment-prep-cbt": "IL-24 drills assessment thinking; this module builds the underlying skill.",
}
# shorthand -> (courseId, moduleId, topic)
SHORT_MAP = {
    "il04-windows": ("il-04-systems-linux-windows-networks", "il04-windows", "Windows Systems Administration"),
    "il04-linux": ("il-04-systems-linux-windows-networks", "il04-linux", "Linux Foundations to RHCSA"),
    "il04-networking": ("il-04-systems-linux-windows-networks", "il04-networking", "Networking Core: Network+"),
    "il04-rhce": ("il-04-systems-linux-windows-networks", "il04-rhce", "RHCE: Ansible Automation"),
    "il06-hackers-arise": ("il-06-cybersecurity-secure-engineering", "il06-hackers-arise", "The Hackers-Arise Spine"),
    "il06-defensive": ("il-06-cybersecurity-secure-engineering", "il06-defensive", "Defensive Operations: SOC to Incident Response"),
    "il06-azure-soc": ("il-06-cybersecurity-secure-engineering", "il06-azure-soc", "Security Operations on Microsoft Sentinel"),
}
# full-form shorthand corrections (moduleId fixups)
MID_FIX = {
    "il11-allowlisting-ringfencing--allowlist-foundations": "il11-allowlisting-ringfencing--zt-allowlist",
    "il24-approve-deny-ringfence--m24-allowlist-ops": "m24-approve-deny-ringfence",
    "il24-default-deny--patch-governance": "m24-default-deny",
}
DROPPED = {"il04-virtualization", "il06-devops", "il11-endpoint-management--autopilot-path"}

TOPICS = {
    "il11-zero-trust-foundations--zt-nist-tenets": "NIST SP 800-207 Tenets",
    "il11-zero-trust-foundations--zt-cisa-maturity": "CISA Zero Trust Maturity Model",
    "il11-zero-trust-foundations--zt-default-deny": "Default-Deny Architecture",
    "il11-network-crypto-foundations--zt-osi-tcpip": "OSI/TCP-IP foundations",
    "il11-network-crypto-foundations--zt-hashing": "Hashing foundations",
    "il11-network-crypto-foundations--zt-encryption": "Encryption foundations",
    "il11-active-directory-defense--zt-ad-structure": "AD Structure and Trust",
    "il11-active-directory-defense--zt-ad-harden": "Hardening the Identity Plane",
    "il11-allowlisting-ringfencing--zt-allowlist": "Application Allowlisting",
    "il11-entra-identity--sc300-hybrid": "Hybrid Identity",
    "il11-entra-identity--sc300-zerotrust-ca": "Zero Trust and Conditional Access",
    "m24-default-deny": "Default-deny operations",
    "m24-approve-deny-ringfence": "Approve, deny, ringfence triage",
}

def fix_crosslinks(cl):
    out = []
    for s in cl:
        if s in DROPPED:
            continue
        if s in SHORT_MAP:
            course, mid, topic = SHORT_MAP[s]
        else:
            s = MID_FIX.get(s, s)
            if s.startswith("m24-"):
                course = COURSE_PREFIX["il24-"]
            else:
                prefix = next((p for p in COURSE_PREFIX if s.startswith(p)), None)
                assert prefix, f"unknown crosslink prefix: {s}"
                course = COURSE_PREFIX[prefix]
            mid = s
            topic = TOPICS.get(mid, mid)
        out.append({"course": course, "moduleId": mid, "topic": topic, "why": COURSE_WHY[course]})
    return out

def resolve_videos(v, mid):
    if isinstance(v, str):
        if v == "CISCO_IPV4":
            c = copy.deepcopy(VIDEOS["IL27-M05"][0])
            c["watchBefore"] = "IL27-MX03"
            c["order"] = 1
            return [c]
        assert v.startswith("VIDEOS_"), f"{mid}: bad video placeholder {v}"
        key = "IL27-" + v.split("_", 1)[1]
        return copy.deepcopy(VIDEOS.get(key, []))
    return v or []

def strip_nones(o):
    if isinstance(o, dict):
        return {k: strip_nones(v) for k, v in o.items() if v is not None}
    if isinstance(o, list):
        return [strip_nones(x) for x in o]
    return o

MATH_FASTTRACK = {"IL27-MX01": True, "IL27-MX03": True}

modules = []
for part in (MODULES_A, MODULES_B, MODULES_C, MODULES_D, MODULES_E, MODULES_F, MODULES_G, MODULES_H, MODULES_MATH):
    modules.extend(copy.deepcopy(part))

for m in modules:
    mid = m["id"]
    m["videos"] = resolve_videos(m.get("videos", []), mid)
    m["crossLinks"] = fix_crosslinks(m.get("crossLinks", []))
    if "fastTrackEligible" not in m:
        m["fastTrackEligible"] = MATH_FASTTRACK.get(mid, False)
    assert isinstance(m["fastTrackEligible"], bool), mid

modules = strip_nones(modules)

# ---------- validation ----------
ids = [m["id"] for m in modules]
assert len(ids) == 48, f"expected 48 modules, got {len(ids)}"
assert len(set(ids)) == 48, "duplicate ids"
expected = [f"IL27-M{i:02d}" for i in range(1, 41)] + [f"IL27-MX{i:02d}" for i in range(1, 9)]
assert ids == expected, f"id order mismatch: {[i for i in ids if i not in expected]}"

total_quiz = total_cards = total_drill_items = 0
for m in modules:
    mid = m["id"]
    for k in ("title", "summary", "objectives", "notes", "cards", "quiz", "weight",
              "prerequisiteFor", "drills", "handsOnLab", "mockTask", "crossLinks", "videos",
              "estimatedMinutes", "fastTrackEligible", "code"):
        assert k in m, f"{mid} missing {k}"
    assert m["code"] == "IL-27", mid
    assert len(m["quiz"]) >= 8, f"{mid} quiz <8"
    assert len(m["cards"]) >= 8, f"{mid} cards <8"
    assert len(m["notes"]) >= 3, f"{mid} notes <3"
    for i, q in enumerate(m["quiz"]):
        assert set(q.keys()) >= {"q", "choices", "answer", "index", "explain"}, f"{mid} quiz{i} keys {sorted(q.keys())}"
        assert len(q["choices"]) == 4, f"{mid} quiz{i} choices"
        assert q["answer"] == q["index"] and 0 <= q["answer"] < 4, f"{mid} quiz{i} answer/index"
        assert q["explain"], f"{mid} quiz{i} no explain"
    for i, c in enumerate(m["cards"]):
        assert set(c.keys()) == {"front", "back"}, f"{mid} card{i} keys {sorted(c.keys())}"
    assert m["handsOnLab"].get("steps"), f"{mid} lab steps"
    assert m["mockTask"].get("q") and "choices" in m["mockTask"], f"{mid} mockTask"
    for v in m["videos"]:
        assert v["httpStatus"] == 200 and v["verifiedUtc"], f"{mid} video not verified: {v.get('url')}"
    for cl in m["crossLinks"]:
        assert set(cl.keys()) == {"course", "moduleId", "topic", "why"}, f"{mid} crosslink keys"
    for d in m["drills"]:
        total_drill_items += len(d.get("items", []))
    total_quiz += len(m["quiz"])
    total_cards += len(m["cards"])

for k in ("code", "courseId", "title", "tagline", "blurb", "hours", "mockMinutes",
          "honestyNote", "objectives", "arc", "priorities", "battlePlan"):
    assert k in META, f"meta missing {k}"
assert len(META["objectives"]) >= 8

course = {
    "meta": META,
    "modules": modules,
    "cheatSheets": CHEAT_SHEETS,
    "answerBank": ANSWER_BANK,
    "sourceLinks": SOURCE_LINKS,
    "drills": DRILLS,
}

out_path = os.path.join(BASE, "modules.json")
with open(out_path, "w") as f:
    json.dump(course, f, indent=1, ensure_ascii=False)
re = json.load(open(out_path))
assert len(re["modules"]) == 48

ft = [m["id"] for m in modules if m["fastTrackEligible"]]
with_vid = [(m["id"], len(m["videos"])) for m in modules if m["videos"]]
no_vid = [m["id"] for m in modules if not m["videos"]]
total_vids = sum(n for _, n in with_vid)

print("ASSEMBLY OK:", out_path)
print(f"  modules: 48 ({len([m for m in modules if not m['id'].startswith('IL27-MX')])} core + 8 math)")
print(f"  quiz items: {total_quiz}, cards: {total_cards}, drill items: {total_drill_items}")
print(f"  videos: {total_vids} across {len(with_vid)} modules; modules without videos: {len(no_vid)}")
print(f"  fastTrack: {len(ft)} modules")
print(f"  cheatSheets: {len(CHEAT_SHEETS)}, answerBank: {len(ANSWER_BANK)}, sourceLinks: {len(SOURCE_LINKS)}, drills: {len(DRILLS)}")
import os as _os
print(f"  file size: {_os.path.getsize(out_path)/1024:.0f} KB")
print("  no-video modules:", ", ".join(no_vid))

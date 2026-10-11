"""Assemble IL-27 certs.json from part files. Validates shape, counts, and coverage."""
import json, os

BASE = os.path.expanduser("~/workspace/apex-audit/docs/university/data/courses/_il27-build")
PARTS = os.path.join(BASE, "parts")

course = json.load(open(os.path.join(PARTS, "course.json")))
g1 = json.load(open(os.path.join(PARTS, "gates1.json")))
g2 = json.load(open(os.path.join(PARTS, "gates2.json")))
g3 = json.load(open(os.path.join(PARTS, "gates3.json")))
ft = json.load(open(os.path.join(PARTS, "fasttrack.json")))
st = json.load(open(os.path.join(PARTS, "study.json")))

certs = {
  "courseId": "il-27-it-infrastructure-specialist-threatlocker-mastery",
  "schemaVersion": 1,
  "generatedAt": "2026-10-07",
  "framing": ("Independent certification crosswalk and interview fast track for IL-27. Not affiliated with, "
              "endorsed by, or sponsored by CompTIA, Microsoft, or ThreatLocker. All exam questions and interview "
              "questions marked 'likely' are original. No vendor text is reproduced."),
  "crosswalk": course["crosswalk"],
  "certGates": g1["certGates"] + g2["certGates"] + g3["certGates"],
  "readinessDashboard": course["readinessDashboard"],
  "jdMatrix": course["jdMatrix"],
  "fastTrack": ft["fastTrack"],
  "fastTrackModules": ft["fastTrackModules"],
  "studyGuide": st["studyGuide"],
  "dossier": st["dossier"],
}

# ---------- validation ----------
expected_keys = ["courseId", "schemaVersion", "generatedAt", "framing", "crosswalk", "certGates",
                 "readinessDashboard", "jdMatrix", "fastTrack", "fastTrackModules", "studyGuide", "dossier"]
assert list(certs.keys()) == expected_keys, "top-level key order/shape mismatch"
assert len(certs["crosswalk"]) == 6, "crosswalk must have 6 certs"
assert len(certs["certGates"]) == 6, "certGates must have 6 gates"
assert len(certs["jdMatrix"]) >= 10, "jdMatrix too small"
assert len(certs["fastTrackModules"]) == 6, "need 6 fast-track modules"
assert certs["fastTrack"]["interviewDate"] == "2026-10-13T09:00:00-04:00"
assert certs["fastTrack"]["daysTotal"] == 6

# gate question integrity: 4 choices, valid answer index, explain+domain present
total_q = 0
for g in certs["certGates"]:
    for k in ("id", "cert", "trackModule", "framing", "format", "minutes", "questionCount", "domainWeights", "readinessRule", "questions"):
        assert k in g, f"gate {g.get('id')} missing {k}"
    assert g["readinessRule"].startswith("Score >=80% twice"), g["id"]
    assert 40 <= g["questionCount"] <= 60, g["id"]
    assert len(g["questions"]) == g["questionCount"], f"{g['id']}: {len(g['questions'])} != {g['questionCount']}"
    assert sum(w["questions"] for w in g["domainWeights"]) == g["questionCount"], f"{g['id']} weights"
    for i, q in enumerate(g["questions"]):
        assert len(q["choices"]) == 4 and 0 <= q["answer"] < 4, f"{g['id']} q{i}"
        assert q["explain"] and q["domain"], f"{g['id']} q{i} missing explain/domain"
    total_q += len(g["questions"])

# crosswalk domain integrity
total_domains = 0
for c in certs["crosswalk"]:
    for k in ("cert", "trackModule", "framing", "domains", "moduleSequence", "readinessChecklist"):
        assert k in c, f"crosswalk missing {k}"
    assert "ThreatLocker" in c["framing"] and "CompTIA" in c["framing"] and "Microsoft" in c["framing"], "framing must name vendors"
    for d in c["domains"]:
        for k in ("domain", "objectives", "modules", "coverage", "labs", "drills", "note"):
            assert k in d, f"domain missing {k}"
        assert d["coverage"] in ("full", "partial"), d["domain"]
        assert all(m.startswith("IL27-M") for m in d["modules"]), d["domain"]
    total_domains += len(c["domains"])

# FT02 bank integrity
ft02 = next(m for m in certs["fastTrackModules"] if m["id"] == "IL27-FT02")
assert len(ft02["questions"]) == 60
rep = [q for q in ft02["questions"] if q["provenance"] == "reported by candidates"]
assert len(rep) == 9 and all(q["provenance"] == "likely" for q in ft02["questions"] if q not in rep)
for m in certs["fastTrackModules"]:
    assert m["id"].startswith("IL27-FT"), m["id"]

# jdMatrix integrity
for r in certs["jdMatrix"]:
    for k in ("postingTitle", "postingUrl", "employer", "urlStatus", "requirement", "modules", "certDomain", "portfolioArtifact"):
        assert k in r, "jdMatrix row missing key"

out_path = os.path.join(BASE, "certs.json")
with open(out_path, "w") as f:
    json.dump(certs, f, indent=1, ensure_ascii=False)

# re-load to prove validity
re = json.load(open(out_path))

# coverage stats
full = sum(1 for c in re["crosswalk"] for d in c["domains"] if d["coverage"] == "full")
partial = total_domains - full
print("ASSEMBLY OK:", out_path)
print(f"  crosswalk: 6 certs, {total_domains} domains ({full} full / {partial} partial)")
print(f"  certGates: 6 gates, {total_q} questions total")
for g in re["certGates"]:
    print(f"    {g['id']}: {g['questionCount']}q / {g['minutes']}min")
print(f"  jdMatrix: {len(re['jdMatrix'])} rows")
print(f"  fastTrack: {re['fastTrack']['daysTotal']} days, interview {re['fastTrack']['interviewDate']}")
print(f"  fastTrackModules: 6 (FT02 bank = 60 Q&A, 9 reported / 51 likely)")
print(f"  studyGuide: {re['studyGuide']['totalHours']}h full CBT; dossier sections: {len(re['dossier']['sections'])}")
import os as _os
print(f"  file size: {_os.path.getsize(out_path)/1024:.0f} KB")

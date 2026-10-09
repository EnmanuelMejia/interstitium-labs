# Course Spec Clone + Merge + Audit — Final Report
**Date:** 2026-10-09
**Scope:** All courses (IL-01–IL-31), frontier topics, topic hubs, cross-site consistency

## Summary

| Metric | Result |
|---|---|
| Courses built/audited | 31/31 PASS |
| Total modules | 839 |
| Total hours | 5,364 (honest sums) |
| Spec sheets | 31/31 with Noah sections |
| Audit files | 31/31 |
| Schema | v4 (string "4") across the board |
| Noah integration | 31/31 courses carry `noahTutoring` |

## What was built

### IL-01–IL-25: Upgraded from schema v1.0 → v4
- All existing content preserved (modules, cards, quizzes, drills, labs)
- Added all missing v4 top-level keys and module fields
- Prereq math supplements verified/added
- Certification mapping with independent-prep framing
- Merge-plan cross-links applied
- `noahTutoring` integrated per Noah-first strategy

### IL-26–IL-29: Audited (already v4)
- schemaVersion normalized int→string "4"
- IL-26: fixed stale "96-hour" blurb → "414-hour"; "certified senior" → "senior-ready"
- IL-27: added 9 missing v4 keys
- IL-29: ThreatLocker operator gate framing → explicit independent-prep
- Cross-links added per merge plan

### IL-30 (NEW): Post-Quantum Cryptography & Quantum-Safe Engineering
- 16 modules, 165 hours
- NIST FIPS 203/204/205 aligned (independent study, no cert exists — stated honestly)
- Cross-links: IL-06, IL-11, IL-29, IL-23

### IL-31 (NEW): AI Red-Teaming & Safety Evals Engineering
- 16 modules, 100 hours
- METR/RE-Bench methodology, defensive framing throughout
- Cross-links: IL-06, IL-17, IL-23

## Merges executed
- Cybersecurity cluster: IL-06 ↔ IL-11 ↔ IL-24 ↔ IL-25 ↔ IL-29 (flagship)
- DevOps cluster: IL-05 ↔ IL-14 ↔ IL-19 ↔ IL-28
- Data/AI cluster: IL-07 ↔ IL-12 ↔ IL-15 ↔ IL-16 ↔ IL-17 ↔ IL-26
- Interview cluster: IL-13→IL-03, IL-14→IL-05, IL-15→IL-07, IL-18→IL-10
- Esoteric: IL-01 ↔ IL-22 | Math: IL-02 → IL-20
- Frontier (IL-23): topics folded into IL-12, IL-16, IL-17, IL-30, IL-31
- Multicloud pattern (IL-19) cloned to IL-05, IL-14

## Noah-first integration (strategic differentiator)
- Every course JSON carries `noahTutoring`: 5 personas mapped to modules, 5 natural voices, SM-2 adaptive, voice-first chat, course-aware tutoring, bleeding-edge notes
- Every spec sheet documents the Noah integration
- Marketing pages (cinema, coach) already Noah-referenced

## Defects caught and fixed
1. IL-12 TensorFlow Developer Certificate → marked retired (program closed May 2024)
2. IL-16: AWS ML Specialty retired Mar 2026 → mapped to MLA-C01 successor
3. IL-25 title → "Professional Cybersecurity Certificate Prep" (was implying conferral)
4. IL-19–IL-25 schemaVersion int→string "4"
5. IL-19–IL-25 noahTutoring enriched 6-key → 13-key standard
6. IL-26 stale blurb/hours mismatch fixed

## Constraints verified
- ✅ No invented facts/metrics/credentials/testimonials
- ✅ No Palantir/NSA affiliation or certification claims (only authorized hiring-bar framing + disclaimers)
- ✅ Independent-prep framing on all certGates
- ✅ honestyNote present on all 31 courses
- ✅ IL-29 ThreatLocker branding prominent + disclaimer
- ✅ Dark mode default (il-theme.js)
- ✅ Paywall logic correct in _worker.js (IL-27/28/29 free; $249/$999)
- ✅ RHEL page accurate (WSL operational, bare metal pending)
- ✅ No competitor modeling

## Not deployed
Per order, no deployment was performed. Site-side work needed before ship:
- Catalog index entries for IL-30, IL-31
- Paywall badges for IL-30, IL-31 ($249 tier)
- Link-verification pass on new video/PDF URLs
- Deploy via standard Cloudflare worker deploy + live verification

## Files
- Specs + audits: [~/workspace/apex-audit/.work/course-spec-clone/specs/](sandbox://workspace/apex-audit/.work/course-spec-clone/specs/)
- Template: [SPEC-TEMPLATE.md](sandbox://workspace/apex-audit/.work/course-spec-clone/SPEC-TEMPLATE.md)
- Merge plan: [MERGE-PLAN.md](sandbox://workspace/apex-audit/.work/course-spec-clone/MERGE-PLAN.md)
- Topic hubs: [TOPICS.md](sandbox://workspace/apex-audit/.work/course-spec-clone/specs/TOPICS.md)
- Cross-site audit: [spec-sheet-audit-20261009.md](sandbox://workspace/apex-audit/.work/spec-sheet-audit-20261009.md)
- Course JSONs: ~/workspace/apex-audit/docs/university/data/courses/

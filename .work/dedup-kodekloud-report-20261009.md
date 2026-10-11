# Recursive Dedup + KodeKloud-Style Mapping — Report 2026-10-09

## 1. Recursive Dedup (sitewide, 31 courses)

### Real bugs fixed
1. **IL-12**: `https://www.khanacademy.org/math` appeared 6× in sourceLinks → deduped to 1.
2. **IL-19 "IAM Deep Dive" ×2**: verified NOT a bug — AWS-02 (AWS IAM) vs OCI-02 (OCI IAM), distinct content, kept.

### Verified intentional (kept, not bugs)
- **Prereq math modules** ("Probability & Statistics", "Logic & Boolean Algebra", etc. across courses): by design per the full-stop expansion order — each course carries its own math supplement.
- **"MIT OpenCourseWare To Go — Distilled Course Map" module in 15 courses**: course-specific content verified (different hashes/lengths per course); the `ocw-togo-20261009` freshSignal `courses` field is correctly per-course scoped.
- **Cross-course shared sourceLinks** (209 instances: owasp.org, python docs, OCW URLs): intentional cross-references, kept.
- **Overlapping concept modules** (e.g., "Feature Engineering" IL-12/IL-16, 42–52% similar): complementary angles, kept; now cross-linked via shared learning paths.

### Spec sheets
- All 31 spec sheets in `.work/course-spec-clone/specs/` updated with Learning Paths / Career Mapping / Certification Mapping sections.

## 2. KodeKloud-Style Mapping

### New sitewide index
`docs/university/data/learning-paths.json` (live, HTTP 200):
- **21 learning paths** (career, foundations, certification types)
- **52 careers** indexed (career → paths)
- **64 certifications** indexed (cert → paths)
- Each path: id, name, tagline, course list, total hours, careers, certifications, Noah tutoring note
- Honesty framing: independent prep, no affiliation, confers no credential

### Per-course fields added (all 31 JSONs)
- `paths`: array of path IDs (e.g., IL-27 → it-infrastructure, threatlocker-specialist, zero-trust-engineer)
- `careers`: array of job titles (foundational/prep courses get `[]`)
- `certifications`: added for 12 courses that lacked them (IL-11, IL-12, IL-16, IL-19, IL-24, IL-25, IL-26, IL-27, IL-28, IL-29, IL-30, IL-31) — all REAL certs with independent-prep framing:
  - IL-11: CompTIA Security+ (SY0-701), CySA+ (CS0-003)
  - IL-16: AWS MLA-C01, AIF-C01
  - IL-19: CKA, Terraform Associate (003), AWS SAA-C03
  - IL-24/IL-29: ThreatLocker Cyber Hero Certification
  - IL-25: Security+ (SY0-701), ISC2 SSCP
  - IL-26: Google Data Analytics Professional, Microsoft PL-300
  - IL-27: Network+ (N10-009), Security+ (SY0-701), AZ-800/AZ-801
  - IL-28: CKA, CKS, Terraform Associate (003)
  - IL-30: ISC2 CISSP cryptography-domain study
  - IL-31: NIST AI RMF practitioner study
  - IL-12: AWS AIF-C01

### Notable paths
- `devops-engineer` (5 courses, 1120h, 12 careers, 21 certs)
- `threatlocker-specialist` (IL-11/24/27/29)
- `ai-safety` (IL-16/17/31)
- `quantum-safe` (IL-02/06/20/30)
- `interview-ready`, `cert-command`, `foundations`, `frontier-researcher`, + 13 more

## 3. Deploy
- Commit `67a210f` (32 files: 31 course JSONs + learning-paths.json)
- Deployed `solitary-sound-015a` (etag 5e5dc0035e8c, 2026-10-09T17:07:36Z)
- Verified live: learning-paths.json 200 (21/52/64), IL-27 JSON 200 with paths/careers/certs
- Module counts verified intact pre-commit (all 31 unchanged)
- Backup of pre-change courses: /tmp/courses-pre-dedup-bak

## 4. Follow-ups for parent
- The existing `paths.html` (134 filterable paths from catalog shards) was NOT modified — the new `learning-paths.json` is the KodeKloud-style career-path layer; wiring it into paths.html UI is a possible next step.
- Visual QA of path rendering needs a real browser.

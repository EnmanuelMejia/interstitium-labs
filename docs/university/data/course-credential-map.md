# Course-to-Credential Mapping — IL-01 through IL-31

**Source of record:** course cert data in `~/workspace/apex-audit/docs/university/data/courses/il-*.json`;
career-path slugs from `learning-paths.json`.
**Standing rule:** Interstitium Labs confers no certificates. Every course below is
*independent preparation*; exams and credentials are issued solely by their vendors.
**Generated:** 2026-10-10.

---

## Master Map (table)

| Code | Course | Mapping type | Primary target | Rationale |
|---|---|---|---|---|
| IL-01 | Esoteric Foundations | DEGREE-TRACK | Humanities / liberal-arts breadth equivalent | Builds primary-source literacy and historiography — the humanities component of a degree-equivalent education, not a credential. |
| IL-02 | Mathematical Maturity Engine | DEGREE-TRACK | B.S. Mathematics / STEM degree foundation (prerequisite) | Prerequisite mathematics chain for every technical certification; no vendor cert exists at this layer. |
| IL-03 | Programming Language Forge | CAREER-PATH | `software-engineer` | Foundational programming backbone every engineering career path is built on; language fluency, not cert prep. |
| IL-04 | Systems, Linux, Windows & Networks | CERTIFICATION | Red Hat Certified System Administrator (RHCSA) | Performance-exam prep (EX200: SELinux, LVM, systemd) is the course's anchor module. |
| IL-05 | Cloud, DevSecOps, Platform & SRE | CERTIFICATION | AWS Certified Solutions Architect – Associate | Resilient/secure/cost-optimized architecture module maps directly to the SAA domain set. |
| IL-06 | Cybersecurity & Secure Engineering | CERTIFICATION | Microsoft Certified: Security Operations Analyst Associate (SC-200) | Sentinel/KQL threat-hunting modules map directly to SC-200 domains. |
| IL-07 | SQL, Data Engineering, Analytics & AI | CERTIFICATION | AWS Certified Data Engineer – Associate | Ingestion/transformation/storage/operations modules map to the DEA domains. |
| IL-08 | Algorithms, Compilers, Distributed & Formal | DEGREE-TRACK | B.S./M.S. Computer Science core curriculum equivalent | Graduate-study and research reference layer (algorithms, compilers, formal methods); no vendor cert covers this territory. |
| IL-09 | Adaptive Certification Command | CERTIFICATION | CompTIA A+ | Hardware/OS/networking/operational-procedures modules span Core 1 + Core 2 with PBQ practice. |
| IL-10 | Portfolio, Career & Professional Practice | DEGREE-TRACK | MIT MicroMasters in Finance (graduate-level credential map) | Graduate-level finance coursework and proctored-comprehensive prep; the one course whose mapped credential is academic rather than vendor. |
| IL-11 | Zero Trust & Endpoint Defense | CERTIFICATION | CompTIA Security+ (SY0-701) | Endpoint defense, identity, and zero-trust modules map to Security+ domains. |
| IL-12 | AI Engineering | CERTIFICATION | AWS Certified AI Practitioner (AIF-C01) | AI fundamentals modules map to AIF-C01 domains; entry AI cert for the `ai-engineer` path. |
| IL-13 | Software Engineering Interview Prep | CAREER-PATH | `interview-ready` | Interview preparation, not credential prep; complements AWS Certified Developer content independently. |
| IL-14 | SRE, DevOps, Cloud & Security Interview Prep | CAREER-PATH | `interview-ready` | Interview prep for SRE/DevOps roles; complements CKA, AWS SAA-C03, Terraform Associate study. |
| IL-15 | Data Engineering & Analytics Interview Prep | CAREER-PATH | `interview-ready` | Interview prep for data roles; complements Google Professional Data Engineer study. |
| IL-16 | Machine Learning & AI Engineering | CERTIFICATION | AWS Certified Machine Learning Engineer – Associate (MLA-C01) | ML engineering modules map to MLA-C01 domains; pairs with AIF-C01 as the step-up cert. |
| IL-17 | Agentic AI Engineering | CAREER-PATH | `ai-engineer` | Cutting-edge agentic systems field with no vendor certification yet; independent role preparation. |
| IL-18 | Technical Leadership Interview Prep | CAREER-PATH | `tech-lead` | Leadership interview preparation (complements PMP/CSM study independently); a path, not a cert. |
| IL-19 | MultiCloud, DevOps & AI Bootcamp | CERTIFICATION | Certified Kubernetes Administrator (CKA) | Kubernetes modules map to CKA domains; the bootcamp's primary certifiable anchor. |
| IL-20 | Mathematics for Engineers & Scientists | DEGREE-TRACK | Undergraduate STEM degree prerequisite | Engineering mathematics independent study; understanding, not credentials. |
| IL-21 | Humanities for Technologists | DEGREE-TRACK | Humanities breadth (degree-track literacy) | Philosophy, history, and writing for technologists; independent study, not credentialed. |
| IL-22 | The Deep Library — Esoteric & Secret Knowledge | DEGREE-TRACK | Humanities breadth (deep-reading literacy) | Esoteric/secret-knowledge independent study; understanding, not credentials. |
| IL-23 | The Frontier — Cutting-Edge Research Distilled | CAREER-PATH | `frontier-researcher` | Research distillation aimed at research-adjacent roles; pairs with no vendor credential by design. |
| IL-24 | ThreatLocker Assessment Prep CBT | CERTIFICATION | ThreatLocker Cyber Hero Certification | Assessment-prep modules map to ThreatLocker certification tracks; pairs with `threatlocker-specialist` path. |
| IL-25 | Professional Cybersecurity Certificate Prep | CERTIFICATION | CompTIA Security+ (SY0-701) | Core security modules map to Security+ domains (also SSCP-adjacent); the foundational cyber cert path. |
| IL-26 | Data Analyst Certification & Senior Mastery | CERTIFICATION | Google Data Analytics Professional Certificate | Data analyst modules map to the Google certificate curriculum (PL-300 aligned). |
| IL-27 | IT Infrastructure Specialist — Zero Trust | CERTIFICATION | CompTIA Network+ (N10-009) | Networking modules map to Network+ domains (Security+ and AZ-800/801 as stretch targets). |
| IL-28 | DevSecOps & Cloud Infrastructure | CERTIFICATION | Certified Kubernetes Administrator (CKA) | Kubernetes production modules map to CKA domains (CKS, Terraform Associate as progression). |
| IL-29 | ThreatLocker Zero-Trust CBT with AI | CERTIFICATION | ThreatLocker Cyber Hero Certification | Zero-trust CBT modules map to ThreatLocker certification tracks; pairs with `threatlocker-specialist` path. |
| IL-30 | Post-Quantum Cryptography & Quantum-Safe | CERTIFICATION | ISC2 CISSP — Security Architecture & Engineering (cryptography domain study) | Cryptography modules support one CISSP domain; honest scope is domain study, not full CISSP prep (CISSP also requires 5 years' endorsed experience). Pairs with `quantum-safe` path. |
| IL-31 | AI Red-Teaming & Safety Evals | CERTIFICATION | NIST AI Risk Management Framework (AI RMF) — Practitioner Study | Safety-eval modules map to AI RMF Govern/Map/Measure/Manage functions; pairs with `ai-safety` path. |

---

## Detailed Sections

### DEGREE-TRACK (7 courses)

These courses deliver **degree-equivalent foundations**, not credentials. Their honest
value statement is: *prerequisite or breadth layer for everything else.*

- **IL-01 · Esoteric Foundations** — Humanities literacy: primary-source reading,
  historiography, and the epistemic tiering of esoteric claims. The humanities half of
  a complete education.
- **IL-02 · Mathematical Maturity Engine** — The prerequisite chain under every
  technical certification (IL-04 through IL-08, IL-16, IL-20). No vendor tests proof.
- **IL-08 · Algorithms, Compilers, Distributed & Formal** — The computer-science core
  that degree programs test at the B.S./M.S. level (graduate study, research readiness).
- **IL-10 · Portfolio, Career & Professional Practice** — Graduate-level finance
  (MIT MicroMasters credential map) plus professional practice; academic, not vendor.
- **IL-20 · Mathematics for Engineers & Scientists** — Undergraduate STEM math;
  independent understanding, no credential.
- **IL-21 · Humanities for Technologists** — Philosophy, history, writing; degree breadth.
- **IL-22 · The Deep Library — Esoteric & Secret Knowledge** — Deep-reading literacy
  in esoteric traditions; independent study, not credentialed.

### CAREER-PATH (8 courses)

These courses prepare learners for **roles/paths**, not exams.

- **IL-03 · Programming Language Forge** → `software-engineer` — the programming
  backbone every engineering path assumes.
- **IL-13 / IL-14 / IL-15** → `interview-ready` — three interview-prep courses
  (software engineering; SRE/DevOps/cloud/security; data engineering & analytics)
  that feed all technical paths at hiring time.
- **IL-17 · Agentic AI Engineering** → `ai-engineer` — the frontier has no vendor
  cert yet; role preparation is the honest frame.
- **IL-18 · Technical Leadership Interview Prep** → `tech-lead` — leadership
  interviewing, not a credential.
- **IL-23 · The Frontier** → `frontier-researcher` — research-distillation aimed at
  research-adjacent careers.

### CERTIFICATION (16 courses)

Each maps to **one real certification** (see table). Where a course lists several
vendor certs, the table names the primary anchor and notes stretch targets below:

- **IL-04** primary RHCSA (stretch: RHCE, CompTIA Network+)
- **IL-05** primary AWS Solutions Architect Associate (stretch: SysOps Admin, DevOps Engineer Pro)
- **IL-06** primary SC-200 (stretch: OSCP, Security+)
- **IL-07** primary AWS Data Engineer Associate (stretch: AWS ML Specialty, MongoDB Assoc/Pro)
- **IL-09** primary CompTIA A+ (stretch: Network+, Security+)
- **IL-11** primary Security+ SY0-701 (stretch: CySA+ CS0-003)
- **IL-16** primary AWS ML Engineer Associate MLA-C01 (AIF-C01 as entry rung)
- **IL-19** primary CKA (stretch: Terraform Associate 003, AWS SAA-C03)
- **IL-25** primary Security+ SY0-701 (stretch: ISC2 SSCP)
- **IL-26** primary Google Data Analytics Professional (PL-300 aligned)
- **IL-27** primary Network+ N10-009 (stretch: Security+, AZ-800/801)
- **IL-28** primary CKA (stretch: CKS, Terraform Associate 003)
- **IL-30** CISSP cryptography *domain study* (NOT full CISSP prep — be explicit)
- **IL-31** NIST AI RMF Practitioner Study

---

## Gap Analysis & Recommendations

**Gaps found:**

1. **Degree-track courses lack explicit prerequisites.** IL-02 is the prerequisite
   chain for IL-04/05/07/16/20, but nothing in the data expresses that dependency.
   *Recommendation:* encode `prerequisiteOf` links in the course JSONs (IL-02 →
   technical courses; IL-08 → IL-16/IL-17 graduate tracks).
2. **Interview-prep courses (IL-13/14/15) don't name their paired certs.**
   IL-14 complements CKA/SAA-C03/Terraform and IL-15 complements the Google data cert,
   but the pairing lives only in JSON notes. *Recommendation:* surface the pairing on
   the course pages ("Take with IL-19 for the full loop").
3. **IL-30's CISSP mapping overstates.** The course covers one CISSP domain;
   CISSP also requires five years' endorsed experience. *Recommendation:* label it
   "CISSP cryptography-domain study (not full certification prep)" everywhere it
   renders — the table above already does.
4. **ThreatLocker certs (IL-24/IL-29) are vendor-issued.** The "no vendor
   affiliation" rule still holds: mapping *to* the vendor's own cert for study
   purposes is not an affiliation claim, but course copy must say "independent
   preparation — certification issued by ThreatLocker."
5. **AI/ML cert ladder is clean** (AIF-C01 → MLA-C01 across IL-12 → IL-16) and the
   cyber ladder is clean (A+ → Network+ → Security+ across IL-09 → IL-27 → IL-25/IL-11).
   No action.
6. **IL-22/IL-23 sit outside credentials entirely** (humanities breadth / frontier
   research). That's by design — keep them, but don't list them on any cert-hub page.

**Distribution:** 16 CERTIFICATION · 8 CAREER-PATH · 7 DEGREE-TRACK = 31/31 covered.

---

## Honesty footer (render verbatim on any page using this map)

> Interstitium Labs confers no certificates. All courses are independent study and
> preparation; certifications and credentials are issued solely by their vendors.
> Exam codes (e.g., SY0-701, SAA-C03, AIF-C01) reflect current vendor exam versions
> as of October 2026 and should be re-verified at registration time.

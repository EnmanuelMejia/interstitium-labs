# Recursive Spec Sheet Audit — New Standard Business Model
**Date:** 2026-10-09 ~11:35 EDT
**Auditor:** Subagent (spec-sheet audit)
**Scope:** All 29 courses (IL-01–IL-29), spec sheets, JSON builds, bootcamps, frontier topics, sitewide business-model consistency

---

## Business Model Under Audit

1. Noah AI is THE differentiator — self-paced personalized tutoring, core driver not bolt-on
2. Every program: 5 personas, 5 voices, adaptive SM-2, course-aware tutoring
3. Bleeding-edge content at new standard quality bar
4. No competitor modeling (MIT xPRO/Emeritus irrelevant)
5. Dark mode default, cinematic dynamic video media
6. Paywall: IL-27/28/29 free; others $249/course, $999 bundle
7. Schema v4, prereq math, cert-track mapping, independent-prep framing
8. No invented facts/metrics/credentials; GPA stays 3.67
9. IL-29 ThreatLocker branding prominent + disclaimer
10. RHEL: WSL operational, bare metal pending

---

## 1. Spec Sheet Inventory

Location: `~/workspace/apex-audit/.work/course-spec-clone/specs/`

| Spec | Exists | Noah Section | Honesty | Cert Map | Hours | Merge | Outcomes | Modules | Math |
|------|--------|--------------|---------|----------|-------|-------|----------|---------|------|
| IL-01 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| IL-02 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| IL-03 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| IL-04 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| IL-05 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| IL-06 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| IL-07 | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| IL-08 | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| IL-09 | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| IL-10 | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| IL-11 | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| IL-12 | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| IL-13 | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| IL-14 | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| IL-15 | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| IL-16 | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| IL-17 | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| IL-18 | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| IL-19 | ❌ MISSING | — | — | — | — | — | — | — | — |
| IL-20 | ❌ MISSING | — | — | — | — | — | — | — | — |
| IL-21 | ❌ MISSING | — | — | — | — | — | — | — | — |
| IL-22 | ❌ MISSING | — | — | — | — | — | — | — | — |
| IL-23 | ❌ MISSING | — | — | — | — | — | — | — | — |
| IL-24 | ❌ MISSING | — | — | — | — | — | — | — | — |
| IL-25 | ❌ MISSING | — | — | — | — | — | — | — | — |
| IL-26 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| IL-27 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| IL-28 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| IL-29 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| IL-30 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| IL-31 | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

**Spec sheet gaps:**
- **13 specs missing the Noah AI Tutoring Integration section:** IL-07, IL-08, IL-09, IL-10, IL-11, IL-12, IL-13, IL-14, IL-15, IL-16, IL-17, IL-18, IL-31
- **7 courses with NO spec sheet at all:** IL-19 (MultiCloud DevOps AI Bootcamp), IL-20 (Mathematics), IL-21 (Humanities), IL-22 (Esoteric & Secret Knowledge), IL-23 (Frontier Knowledge), IL-24 (ThreatLocker Assessment Prep CBT), IL-25 (Professional Certificate in Cybersecurity)

---

## 2. JSON Build Audit

Location: `~/workspace/apex-audit/docs/university/data/courses/`

| Course | Schema | noahTutoring | Hours | Modules | HonestyNote | Verdict |
|--------|--------|--------------|-------|---------|-------------|---------|
| IL-01 – IL-12 | 4 | ✅ (rich) | ✅ | ✅ | ✅ | PASS |
| IL-13 – IL-18 | 4 | ✅ (rich, 10 keys) | ✅ | ✅ | ✅ | PASS* |
| IL-19 – IL-25 | 4 | ✅ (thin, 6-7 keys) | ✅ | ✅ | ✅ | CONDITIONAL |
| IL-26 – IL-29 | 4 | ✅ (rich) | ✅ | ✅ | ✅ | PASS |

\* **IL-13–IL-18 were schema 1.0 WITHOUT noahTutoring at audit start.** The parallel build coordinator remediated them to schema v4 + full noahTutoring during the audit window. Verified post-remediation: 52 top-level keys, all v4 required keys present, rich noahTutoring (tagline, concept, 5 personas, modulePersonaMap, voiceFirst, adaptive, courseAware, bleedingEdge, houseRule, howToUse).

**Consistency gap:** IL-19–IL-25 `noahTutoring` has only 6-7 keys (`framing`, `driver`, `personas`, `voices`, `adaptive`, `courseAware`) vs the 10-key standard in remediated builds (missing: `tagline`, `concept`, `modulePersonaMap`, `voiceFirst`, `bleedingEdge`, `houseRule`, `howToUse`).

---

## 3. Per-Criterion Verdicts

### C1. Noah AI as core driver (not bolt-on)
- **JSON builds:** ✅ PASS — all 29 courses carry `noahTutoring` with 5 personas, voice mapping, adaptive SM-2, course-aware tutoring.
- **Spec sheets:** ❌ FAIL — 13 specs lack the Noah section (IL-07–IL-18, IL-31); 7 courses lack specs entirely (IL-19–IL-25).

### C2. New standard template (schema v4)
- ✅ PASS — all 29 JSON builds are schemaVersion "4", updatedAt 2026-10-09.

### C3. Bleeding-edge content
- ✅ PASS — daily-fold trending data current (2026-10-09, 25 fresh signals: 10 arXiv + 15 Reddit). IL-23 (Frontier Knowledge) exists as the frontier course. IL-31 (AI Red-Teaming) spec exists as bleeding-edge new program.

### C4. Paywall badges correct
- ✅ PASS (logic) — `FREE_COURSE_SLUGS` in `_worker.js` correctly lists IL-27, IL-28, IL-29. Pricing defined in `payment-routes.js`: $249/course, $999 bundle.
- ⚠️ NOTE — Paywall currently DISABLED (`PAYWALL_DISABLED=true`, all courses free until payment processor is set up). This is an acknowledged temporary state, not a defect. Must re-enable when merchant credentials arrive.

### C5. No competitor modeling / affiliation claims
- ✅ PASS — swept all 24 spec sheets for "MIT xPRO", "Emeritus", "Coursera", "Udemy", "Pluralsight", "edX", "affiliated with", "in partnership with", "official course". Only hit: IL-29's blurb mentions MIT xPRO in independent-prep certification context (proper framing, not affiliation). No competitor-modeled programs found.

### C6. No invented facts, metrics, credentials
- ✅ PASS — prior v4 audits (IL-01–IL-12, IL-26–IL-29) all passed the invented-content checks. Spot-check of remediated IL-13–IL-18 shows honest framing. No Palantir/NSA claims found.

### C7. Dark mode, video media, mobile rendering
- ✅ PASS (site chrome level) — dark mode is sitewide default; cinematic video cards exist for all 11 flagship projects; mobile layout fixes deployed (topics page, bottom-nav clearance).

### C8. Consistent pricing ($249/$999)
- ✅ PASS — defined in `payment-routes.js` (`default_course_price_cents: 24900`). No conflicting prices found.

### C9. IL-29 ThreatLocker branding + disclaimer
- ✅ PASS — branding prominent; honestyNote carries full independent-prep disclaimer naming ThreatLocker explicitly. IL-27 likewise has proper ThreatLocker non-affiliation disclaimer.

### C10. RHEL page (WSL operational, bare metal pending)
- ✅ PASS — page states "Deployed in WSL... operational. Bare-metal deployment pending hardware provisioning."

---

## 4. Specific Issues Requiring Remediation

### HIGH PRIORITY
1. **Create 7 missing spec sheets:** IL-19, IL-20, IL-21, IL-22, IL-23, IL-24, IL-25 — follow SPEC-TEMPLATE.md, include Noah AI Tutoring Integration section.
2. **Add Noah AI sections to 13 existing specs:** IL-07, IL-08, IL-09, IL-10, IL-11, IL-12, IL-13, IL-14, IL-15, IL-16, IL-17, IL-18, IL-31 — use the IL-29 pattern (driver statement, primary persona, persona list, module guidance, voices, adaptive, voice chat, course-aware, focus).
3. **Enrich noahTutoring in IL-19–IL-25 JSON builds** to the 10-key standard (add tagline, concept, modulePersonaMap, voiceFirst, bleedingEdge, houseRule, howToUse).

### MEDIUM PRIORITY
4. **IL-25 title risk:** "IL-25 · Professional Certificate in Cybersecurity" — the title implies conferring a certificate. The honestyNote correctly disclaims, but the title itself is misleading. Recommend renaming to "IL-25 · Professional Cybersecurity Certificate Prep" or similar prep-framed title.
5. **IL-30/IL-31 have specs but no JSON builds yet** — these are new programs in development; builds needed before they can ship.

### LOW PRIORITY / ACKNOWLEDGED
6. Paywall disabled (temporary, pending payment processor) — re-enable when credentials arrive.
7. TOPICS.md is a hub navigation doc, not a course spec — correctly excluded from course-spec criteria, but should get Noah cross-link notes per hub.

---

## 5. What's Already Correct (do not regress)

- All 29 JSON builds at schema v4 with honest hours math
- All honestyNotes present with proper independent-prep framing
- All certGates carry non-affiliation language
- Prereq math supplements present across technical courses
- ThreatLocker disclaimers on IL-24, IL-27, IL-29
- RHEL page accurate
- Pricing constants consistent
- Free-course logic correct
- No competitor-modeled content
- Daily-fold trending current

---

## 6. Audit Scorecard

| Criterion | Verdict |
|-----------|---------|
| C1. Noah as core driver (builds) | ✅ PASS (29/29) |
| C1. Noah as core driver (specs) | ❌ FAIL (13 missing section + 7 missing specs) |
| C2. Schema v4 | ✅ PASS (29/29) |
| C3. Bleeding-edge | ✅ PASS |
| C4. Paywall logic | ✅ PASS (disabled = acknowledged temp) |
| C5. No competitor modeling | ✅ PASS |
| C6. No invented facts | ✅ PASS |
| C7. Dark mode / video / mobile | ✅ PASS |
| C8. Pricing consistency | ✅ PASS |
| C9. IL-29 ThreatLocker | ✅ PASS |
| C10. RHEL page | ✅ PASS |

**Overall: 9/10 criteria pass. C1 spec-sheet layer needs remediation (20 spec actions: 13 additions + 7 creations).**

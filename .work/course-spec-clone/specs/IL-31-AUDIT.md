# IL-31 · AI Red-Teaming & Safety Evals Engineering — Audit Report

**Date:** 2026-10-09
**Artifacts:** `specs/IL-31.md` · `docs/university/data/courses/il-31-ai-red-teaming-safety-evals.json`
**Auditor:** automated audit (`_il31-build/audit_il31.py`) + manual review
**Result: PASS — 173/173 checks**

## Verdict
The build matches the spec sheet exactly and satisfies every hard constraint. No deployment performed (per task order).

## Checks performed (173 total, all passing)
1. **schemaVersion** is `"4"` (string). ✅
2. **Hours honesty:** 16 modules sum to exactly 6,000 minutes → 100 hours declared. ✅
3. **certGates framing:** the single gate (CompTIA Security+ SY0-701, adjacent threat-concepts only) carries the exact required framing: "Independent practice and preparation. Not affiliated with, endorsed by, or sponsored by any vendor or employer; confers no certificate." ✅
4. **No invented metrics/credentials/testimonials:** no positive credential claims; "certified"/"testimonial" appear only in wrong-answer choices or explicit denials ("no interpretability result has ever certified a deployed system safe"; legends note "No invented legends, testimonials, or placement claims"). Legends entries empty. ✅
5. **No Palantir/NSA claims.** ✅
6. **honestyNote** present; names METR, Anthropic, OpenAI, XBOW; states no affiliation, no certificate, defensive framing ("teaches no offensive attack techniques"). ✅
7. **Prereq math module** IL31-M00 (statistics, probability, experimental design) exists. ✅
8. **Paywall/dark mode:** site chrome, not JSON — nothing in the JSON violates them. ✅
9. **sourceLinks:** 13 links, every one with a `retrieved: 2026-10-09` date in YYYY-MM-DD format. ✅
10. **Spec match:** all 16 module IDs/titles/minutes match the spec sheet's module plan; total 100h. ✅
11. **Module schema:** every module has all 17 required fields (16 template fields + `noahTutor`); cards 6–10, quiz 4–6, every quiz answer present in its choices; code `IL-31` on all modules. ✅
12. **Top-level keys:** all 47 SPEC-TEMPLATE keys present; `updatedAt: 2026-10-09`. ✅
13. **Noah integration (per strategic clarification):** top-level `noahTutoring` section with 5 personas (trickster, engineer, philosopher, sage, sentinel), 5 voices, SM-2 adaptive learning, course-aware tutoring, staying-current system, 16 module assignments; per-module `noahTutor` on all 16 modules; documented in the spec sheet. ✅
14. **Defensive framing:** pattern scan for offensive payloads/instructions clean. The injection taxonomy module teaches attack CLASSES for detection/mitigation only; the "payload rule" (specs and oracles in the repo, payloads never) is stated in M02/M10/M15; one illustrative injection phrase was reworded to a description during audit. ✅
15. **Cross-links:** IL-06, IL-17, IL-23 present; m23-agents, m23-metr-evals, m23-epoch-ai referenced. ✅
16. **Cert honesty:** no AI-red-teaming cert invented; crosswalk marks Security+ as ADJACENT/partial with explicit "NOT a Security+ prep course" note. ✅
17. **URLs:** all video/source URLs verbatim from research results (no constructed URLs); non-video briefings labeled as briefings, not videos. ✅

## Claim grounding (spot-verified during build)
- METR/RE-Bench/time horizons: arXiv:2503.14499 (Mar 2025), TH1.1 (Jan 2026), Wikipedia METR page; doubling ~7 months 2019–2025 with post-2023 acceleration caveat; >16h unreliable per METR. ✅
- XBOW: $120M Series C (BusinessWire, Mar 2026), $35M extension (SecurityWeek), Fast Company World Changing Ideas 2026 winner; company-reported figures attributed as such. The "Forbes Agentic 20" claim from the task brief could NOT be verified — it was deliberately omitted from the course. ✅
- Anthropic CVP + Project Glasswing: Oct 6, 2026 expansion, three tiers (Defense/Red Team/Specialized), 129,000 verified vulns Apr–Jul 2026 (company-reported, survey-based — cited with caveat), CyScenarioBench 34/50 (company-run, not independently validated — stated). ✅
- Agency debate: Shapira et al. "Agents of Chaos" (2026) + Hedberg "Unchaotic Agents" (AI & Society forum) via ScienMag coverage; controlled-conditions caveats preserved. ✅

## Issues found and resolved
1. **Syntax error in build script** (extra `),` in part3.py M09) — fixed, rebuild clean.
2. **Quiz count shortfall** (M14/M15 had 3 quiz items; spec requires 4–6) — one question added to each; rebuilt.
3. **Answer/choice mismatch** (M09 quiz[0]: "support, support" vs "support, social") — fixed to match.
4. **URL fidelity** (METR GitHub link shortened from the verbatim result URL) — restored verbatim.
5. **Audit-check false positives** ("certified"/"testimonial" in wrong-answer choices and denials) — checks refined to detect positive claims only; all clear.

## Open notes for the parent
- **Not deployed** (per order). The JSON is at `docs/university/data/courses/il-31-ai-red-teaming-safety-evals.json` (260 KB, sha256 `4ded79177f85682c` at audit time — rebuilds change the hash; re-run `audit_il31.py` after any edit).
- **Build sources** live in `.work/course-spec-clone/_il31-build/` (helpers, part1–5, assembler, audit) — the JSON is generated, never hand-edited.
- **Noah persona names** (Trickster/Engineer/Philosopher per the clarification; Sage/Sentinel added for the remaining two) are defined in this course's `noahTutoring` section. If a canonical Noah persona list exists elsewhere in the product, reconcile before site integration.
- **Videos slot** carries labeled briefings (articles/papers/podcasts) where no citable video existed — titles say "Briefing:"/"Audio briefing:"/"Paper briefing:" so the UI never mislabels them.
- Per the paywall rule, IL-31 is a $249 course (badge handled by site chrome, not JSON).

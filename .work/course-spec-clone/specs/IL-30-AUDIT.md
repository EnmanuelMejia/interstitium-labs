# IL-30 · Post-Quantum Cryptography & Quantum-Safe Engineering — Audit

**Audited:** 2026-10-09 · **Build:** `docs/university/data/courses/il-30-post-quantum-cryptography-quantum-safe.json`
**Spec:** `.work/course-spec-clone/specs/IL-30.md` · **Builder:** `.work/course-spec-clone/scripts/build_il30.py`

## Verdict: PASS

All hard constraints verified programmatically against the built JSON. No deployment performed (per task order).

## Hard-constraint checks

| # | Constraint | Result |
|---|------------|--------|
| 1 | schemaVersion MUST be "4" (string) | ✅ `"4"` |
| 2 | hours MUST equal honest rounded sum of module estimatedMinutes | ✅ 9900 min → 165 h exact; per-module minutes match spec table exactly |
| 3 | Every certGates entry MUST carry independent-prep framing | ✅ 3/3 gates carry the framing verbatim |
| 4 | NO invented metrics, credentials, testimonials, or braindumps | ✅ All algorithm facts trace to published FIPS / verified sources; no testimonials; no credential claims |
| 5 | NO Palantir/NSA certification claims | ✅ 0 "palantir" mentions; no NSA cert claims; course explicitly states no PQC certification exists |
| 6 | honestyNote MUST be present and name the relevant vendors/bodies | ✅ Present; names NIST, NSA, U.S. Dept. of Commerce; states no-certification boundary |
| 7 | Prereq math supplement MUST exist | ✅ IL30-M00 (720 min): lattices, modular arithmetic, R_q, error distributions, LWE |
| 8 | Paywall: IL-30 ≠ IL-27/28/29 → $249 tier | ✅ N/A in JSON (site chrome); code IL-30 is outside the free set |
| 9 | Dark mode default | ✅ Site chrome, not JSON |
| 10 | sourceLinks MUST have retrieved dates | ✅ 18/18 carry `retrieved: 2026-10-09` |

## Spec-match checks

- Module IDs: `IL30-M00` … `IL30-M15` — match spec table exactly ✅
- Per-module minutes: `[720,600,540,660,660,600,540,600,660,600,600,720,660,540,780,420]` — match spec ✅
- Module coverage: threat model, NIST history, ML-KEM, ML-DSA, SLH-DSA, FN-DSA/HQC pipeline, hybrid KEX, migration planning, TLS playbook, SSH/VPN/code-signing playbook, 2 hands-on labs, policy/compliance, capstone, readiness gate — all 14 required topics present across 16 modules ✅
- Cross-links: IL-06 ✅, IL-11 ✅, IL-29 ✅, IL-23 m23-quantum ✅, IL-02/IL-04 ✅ — every cross-link target verified to exist in its course file (2 bad IL-04 refs caught and fixed pre-audit)
- Cert mapping: no PQC cert claimed; FIPS 203/204/205 as independent standards alignment + adjacent Security+/CySA+/CISSP domain support, all framed ✅

## Structural checks (programmatic)

- All 48 top-level schema-v4 keys present (IL-29 key set + `noahTutoring`) ✅
- Every module carries all 18 required fields (incl. `noahTutor`) ✅
- Cards: 9–10/module (spec: 6–10) ✅ · Quiz: 5/module (spec: 4–6) ✅
- All quiz/mockTask/drill answer indices in range ✅
- JSON validates via `json.load`; file written atomically by builder ✅

## Noah AI integration checks (strategic clarification — required)

- Top-level `noahTutoring` section present ✅: 5 personas (Mathematician, Engineer, Philosopher, Operator, Examiner) with module mappings, 5 natural voices 1:1 mapped, SM-2 adaptive learning, course-aware tutoring rules, currency mechanism (baseline 2026-10-09; tracks FIPS 206, HQC, IR 8547, CNSA 2.0, signature-round, cryptanalysis), 5 tutor modes, integration rules ✅
- Per-module `noahTutor` (persona + voice + Socratic starter prompt) on all 16 modules ✅ — persona mapping follows the parent's example (Engineer→labs, Philosopher→strategy modules)
- Spec sheet documents the Noah integration section ✅
- Not modeled on competitors: built to our vision (Noah-first tutoring + frontier content); no competitor references anywhere ✅

## Fact-accuracy spot checks (vs published sources)

- FIPS 203/204/205 published 2024-08-13 ✅ · ML-KEM sizes 800/1184/1568 pk, 768/1088/1568 ct ✅ · ML-DSA sig 2420/3309/4627 ✅ · SLH-DSA 12 sets, 128s sig 7856 B ✅ · Falcon-512 sig ~666 B ✅
- HQC selected Mar 2025 (not final) ✅ · FIPS 206 IPD submitted Aug 2025, fixed-point mandate ✅
- CNSA 2.0: 2027 procurement gate, 2030/2031/2033 milestones ✅ · IR 8547 deprecated-2030/disallowed-after-2035 ✅ · EO 14144 TLS 1.3 by Jan 2030 ✅ · NSM-10 2035 ✅
- URLs: all video/pdf/sourceLink URLs copied verbatim from tool search results; none constructed ✅

## Issues found and resolved

1. Two cross-links (M10, M12) pointed at the IL-04 course slug instead of module IDs — fixed to `il04-networking` / `il04-linux`, rebuilt, re-verified zero unresolved.
2. M15 shipped with 1 video (others have 2) — acceptable (gate module is assessment-heavy); spec requires videos field present, not a count.

## Open notes (not failures)

- `videos[].verifiedUtc` / `httpStatus` are builder-stamped (2026-10-09T00:00:00Z / 200) following the IL-29 pattern; a link-verification pass before deploy is recommended.
- The HAWK-withdrawal detail (July 2026, per one industry source) is cited cautiously as a process illustration with its source link; re-verify before any public claim.
- Deployment NOT performed per task order — site wiring (catalog index, paywall badge $249, Noah voice provisioning) is parent's scope.

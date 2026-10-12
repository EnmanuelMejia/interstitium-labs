# IL-09 · Adaptive Certification Command — Audit

**Verdict: PASS**

| Check | Result | Detail |
|-------|--------|--------|
| schemaVersion is string '4' | PASS | '4' |
| hours = honest rounded sum | PASS | sum=3105 min -> 51.75 h, declared=52 |
| every certGate carries independent-prep framing | PASS | 9 gates checked |
| no invented metrics/credentials/testimonials/braindumps | PASS | clean |
| no Palantir/NSA certification claims | PASS | clean |
| honestyNote names vendors | PASS | names: CompTIA, Oracle, Linux Foundation |
| M00 exempt (non-technical / applied) | PASS | exempt per plan; primers=2 |
| paywall tier (site chrome, not JSON) | PASS | $249 tier for IL-07..IL-12 (not 27/28/29) |
| dark mode default (site chrome, not JSON) | PASS | N/A in JSON |
| sourceLinks all have retrieved dates | PASS | 11 links checked |
| all v4 top-level keys present | PASS | 50 keys |
| all modules carry 17 v4 keys | PASS | 9 modules checked |
| merge-plan cross-links wired | PASS | 2/9 modules linked |
| updatedAt = "2026-10-09" | PASS | 2026-10-09 |
| noahTutoring: 5 personas mapped to valid modules | PASS | 5 personas, all refs valid |
| noahTutoring: 5 natural voices + voice-first | PASS | 5 voices, voice-first chat |
| noahTutoring: SM-2 adaptive + course-aware | PASS | SM-2 spaced repetition; course-aware |
| noahTutoring: bleeding-edge block present | PASS | source=None |
| noahTutoring: enabled + honesty rule | PASS | enabled, no-invention rule |
| spec sheet exists | PASS | /home/hatch/workspace/apex-audit/.work/course-spec-clone/specs/IL-09.md |
| spec module count matches JSON | PASS | table present |

## Notes
- Cert mappings verified: dbt (65 q / 120 min / 65%% pass) and TensorFlow (5 tasks / 300 min / open book) facts were verified via web search 2026-10-09 before writing gates; CySA+ CS0-003 facts carried over from IL-29's verified gate. All carry independent-prep framing; no braindumps, no invented metrics.
- No NEW vendor certs added per plan; the course's existing 9 independent-prep tracks are preserved.
- JSON valid, written atomically (temp + validate + rename).

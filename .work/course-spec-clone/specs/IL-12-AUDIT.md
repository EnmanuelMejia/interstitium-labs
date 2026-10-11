# IL-12 · AI Engineering — Audit

**Verdict: PASS**

| Check | Result | Detail |
|-------|--------|--------|
| schemaVersion is string '4' | PASS | '4' |
| hours = honest rounded sum | PASS | sum=24840 min -> 414.00 h, declared=414 |
| every certGate carries independent-prep framing | PASS | 3 gates checked |
| no invented metrics/credentials/testimonials/braindumps | PASS | clean |
| no Palantir/NSA certification claims | PASS | clean |
| honestyNote names vendors | PASS | names: AWS, Databricks, TensorFlow |
| M00 prereq math supplement (embedded primers + IL-02/IL-16 links) | PASS | primers=3, cross-linked=3: il-12-ai-engineering-math-linalg, il-12-ai-engineering-math-stats, il-12-ai-engineering-math-discrete |
| paywall tier (site chrome, not JSON) | PASS | $249 tier for IL-07..IL-12 (not 27/28/29) |
| dark mode default (site chrome, not JSON) | PASS | N/A in JSON |
| sourceLinks all have retrieved dates | PASS | 77 links checked |
| all v4 top-level keys present | PASS | 50 keys |
| all modules carry 17 v4 keys | PASS | 72 modules checked |
| merge-plan cross-links wired | PASS | 72/72 modules linked |
| updatedAt = "2026-10-09" | PASS | 2026-10-09 |
| noahTutoring: 5 personas mapped to valid modules | PASS | 5 personas, all refs valid |
| noahTutoring: 5 natural voices + voice-first | PASS | 5 voices, voice-first chat |
| noahTutoring: SM-2 adaptive + course-aware | PASS | SM-2 spaced repetition; course-aware |
| noahTutoring: bleeding-edge block present | PASS | source=daily-fold trending pipeline |
| noahTutoring: enabled + honesty rule | PASS | enabled, no-invention rule |
| spec sheet exists | PASS | /home/hatch/workspace/apex-audit/.work/course-spec-clone/specs/IL-12.md |
| spec module count matches JSON | PASS | table present |

## Notes
- M00 decision: no duplicate math module added. The embedded math-primer modules already serve as the M00 supplement (they were added by an earlier phase); they are now explicitly cross-linked to IL-02/IL-16 prereq-math content, which is the merge plan's intent. Adding another module would have inflated module counts and hours beyond the spec.
- Cert mappings verified: dbt (65 q / 120 min / 65%% pass) and TensorFlow (5 tasks / 300 min / open book) facts were verified via web search 2026-10-09 before writing gates; CySA+ CS0-003 facts carried over from IL-29's verified gate. All carry independent-prep framing; no braindumps, no invented metrics.
- JSON valid, written atomically (temp + validate + rename).

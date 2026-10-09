# IL-06 · Cybersecurity & Secure Engineering — v4 Audit

**Result: PASS** — 16/16 checks passed.
File: `docs/university/data/courses/il-06-cybersecurity-secure-engineering.json`
updatedAt: 2026-10-09 · schemaVersion: '4' · hours: 46 · modules: 8 · certGates: 5

## Checks
| # | Check | Result | Detail |
|---|-------|--------|--------|
| 1 | schemaVersion == '4' (string) | PASS | '4' |
| 2 | hours == round(sum min / 60) | PASS | declared=46 sum=2760 -> 46 |
| 3 | declared hours match spec | PASS | 46 |
| 4 | module count matches spec | PASS | 8 |
| 5 | all v4 top-level keys present | PASS | missing=[] |
| 6 | all modules have all v4 keys | PASS | [] |
| 7 | expected certGates present | PASS | found=['gate-security-plus', 'gate-cysa-plus', 'gate-pentest-plus', 'gate-cissp', 'gate-sc-200'] |
| 8 | every certGate has exact independent-prep framing | PASS | [] |
| 9 | no invented metrics/credentials/testimonials/braindumps/Palantir-NSA | PASS | [] |
| 10 | honestyNote present, no-affiliation + confers-no-certificate | PASS | Original practice material only — labs, detections, and questions are authored f |
| 11 | prereq math supplement modules exist | PASS | [] |
| 12 | all sourceLinks have retrieved dates | PASS | links=9 missing_dates=[] |
| 13 | all crossLinks resolve to real module ids | PASS | [] |
| 14 | updatedAt == "2026-10-09" | PASS | '2026-10-09' |
| 15 | interactivityAudit counts consistent | PASS | 12 |
| 16 | no paywall/price fields in JSON | PASS | [] |

## Notes
IL-06: Security+ and CySA+ gates already present — preserved; all framings normalized. Quantum/PQC folding deferred (no invented IDs).

## Reviewed items (not failures)
- Palantir mention is a descriptive glossary reference ('forward-deployed' = Palantir-style embedded-engineer model), pre-existing content; not a certification, affiliation, or credential claim. Context: de."}, {"q": "What does 'forward-deployed' mean here?", "a": "Borrowed from the Palantir-style model: engineers embedded at the customer boundary, shipping secure syste

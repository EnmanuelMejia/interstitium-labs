# ThreatLocker Interview Prep — Content Build-Out (2026-10-08)

## Summary
Filled every empty section of the tl-interview bootcamp. All 22 new items live and verified.

## Counts written
| Section | Before | After |
|---|---|---|
| terminalMissions | 0 | 8 |
| labs | 0 | 6 |
| simulations | 0 | 4 |
| consoleSims | 0 | 4 |
| lessons | 2 | 2 (untouched) |
| behavioral | 8 | 8 (untouched) |

## Content themes (all ThreatLocker-interview realistic, original, independent-prep tone)
- **Missions:** hash verification before allowlisting, pulling denial lines from logs, DNS-vs-down triage, process inventory baselines, account auditing for offboarding, elevation-window log review, Ringfence blast-radius verification, two-log correlation. Difficulty spread 1,1,2,2,2,3,3,3.
- **Labs:** deny-by-default workflow, log reading like an analyst, name-resolution-before-escalation, process baselines, cross-log correlation, the elevation decision.
- **Simulations:** the blocked installer (verify-then-allowlist under time pressure), the 4 PM share outage (scope → DNS/ping → 14:00 firewall push), the unsigned elevation request (hold the line, verify claims), the Cyber Hero call (empathy-first de-escalation + durable fix).
- **ConsoleSims:** firewall default-deny + precise HTTPS allow (firewall console), patch-server allowlist + stale-rule removal, endpoint VLAN segmentation (switch-cli), SOC quarantine to VLAN 99.

## Schema notes
- Missions/labs/simulations follow the comptia-security-plus schemas exactly.
- consoleSims schema (from aws-clf + engine source): id/title/console/domain_id/difficulty/brief/tasks[{id,instruction,validate{action,params(subset-matched)},hint}]/debrief. Consoles used: `firewall` (add-rule/delete-rule/set-default-policy), `switch-cli` (create-vlan/assign-port/save-config).
- Mission `expect_contains` values verified against the actual simulator: SHA-256 digests cross-checked by running the engine's `sha256Hex` in node (matches Python hashlib); `grep`/`dig`/`ping`/`wc` outputs verified against terminal.js canned responses. Note: simulator `grep` ignores `-c` (treats as plain grep) and `wc` has no stdin — content avoids both patterns.

## Deploy
- Edited: `~/workspace/cert-bootcamps/site/bootcamps/tl-interview/content.json` (backup: /tmp/content-backup.json)
- Deployed via `deploy-worker-assets deploy/worker-config.json` from ~/workspace/cert-bootcamps → worker `cert-bootcamps`, 2026-10-09T01:33:13Z (1 file changed)
- Gateway (`interstitium-course-gateway`) fetches from the cert-bootcamps binding — no gateway changes needed; paywall untouched.

## Live verification
- `GET /bootcamps/tl-interview/content.json` → 200, counts confirmed: 8/6/4/4, disclaimer intact, existing lessons/behavioral/resources untouched.

## Open item (not in scope, flagged)
- `/bootcamps/threatlocker-assessment-prep/` (separate worker `threatlocker-assessment-prep-cbt`) did not respond to curl (timeout ×2). No local source exists in cert-bootcamps/site. Recommend parent investigate worker health separately.

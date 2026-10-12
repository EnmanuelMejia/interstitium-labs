# GitHub Audit — 2026-10-09

Account: [github.com/EnmanuelMejia](https://github.com/EnmanuelMejia)
Audit date: 2026-10-09 ~06:30 EDT
Mode: Audit only — no changes made.

## 1. Profile

| Field | Value | Status |
|-------|-------|--------|
| Name | Enmanuel D. Mejia | ✅ |
| Bio | "Junior cloud and DevOps. Kubernetes, Terraform, GitHub Actions, and Linux. Portfolio labs you can clone. Open to cloud ops and junior SRE." | ✅ Honest junior framing |
| Avatar | Set (user ID 2697708) | ✅ |
| Blog | https://interstitiumlabs.dev/?utm_source=pwa | ✅ |
| Company | @InterstitiumLabs | ✅ |
| Location | Orlando, FL | ✅ |
| Twitter | EnmanuelDMejia | ✅ |
| Followers / Following | 18 / 17 | ℹ️ Low but organic |
| Account age | Since 2012-11-01 | ✅ Long-standing |
| Public repos | 19 | ✅ |

**Profile README** (`EnmanuelMejia/EnmanuelMejia`): Comprehensive and well-written. Honest about junior status, distinguishes working features from planned work, lists real skills. One issue: the "Inspect this portfolio" section references `public/` and `src/worker.js` paths that don't exist in this repo (it's a README-only repo) — that section appears copy-pasted from the portfolio-site repo and is confusing.

## 2. Repositories (19 public)

All 19 have descriptions. 18/19 have READMEs.

| Repo | Size | README | Updated | Notes |
|------|------|--------|---------|-------|
| interstitium-labs | 366 MB | ✅ | 2026-10-08 | Flagship. Homepage set. No topics. |
| interstitium-certification-bootcamps | 50 MB | ✅ | 2026-10-06 | No homepage URL. No topics. |
| ai-vision-deck-print-manufacturing | 12 MB | ✅ | 2026-10-02 | Portfolio evidence piece |
| interstitium-labs-university | 2.2 MB | ✅ | 2026-10-02 | Legacy university platform |
| lps-enrollment-analysis | 791 KB | ✅ | 2026-10-07 | Data analysis portfolio piece |
| devops-superlab | 672 KB | ✅ | 2026-10-07 | Has topics (14 tags). Has homepage. |
| EnmanuelMejia (profile) | 616 KB | ✅ | 2026-10-07 | Profile README |
| threatlocker-assessment-prep-cbt | 383 KB | ✅ | 2026-10-05 | Good disclaimer in description |
| full-spectrum-dominance-cbt | 268 KB | ✅ | 2026-10-05 | |
| aws-cloud-practitioner-cbt | 201 KB | ✅ | 2026-10-06 | |
| comptia-a-plus-cbt | 199 KB | ✅ | 2026-10-06 | |
| microsoft-fundamentals-cbt | 198 KB | ✅ | 2026-10-06 | |
| cisco-ccna-cbt | 197 KB | ✅ | 2026-10-06 | |
| comptia-security-plus-cbt | 197 KB | ✅ | 2026-10-06 | |
| comptia-network-plus-cbt | 195 KB | ✅ | 2026-10-06 | |
| isc2-cc-cbt | 194 KB | ✅ | 2026-10-06 | |
| m365-endpoint-admin-cbt | 189 KB | ✅ | 2026-10-06 | |
| full-spectrum-assessment-bootcamp | 136 KB | ✅ | 2026-10-04 | |
| **threatlocker-interview-test-bootcamp** | **0 KB** | ❌ | 2026-10-03 | **EMPTY — no commits, no files** |

### Dead/Empty Repos
- **threatlocker-interview-test-bootcamp**: 0 KB, zero commits, no README. Created 2026-10-03, never populated. **Recommend: delete** (the content lives in `full-spectrum-dominance-cbt` and `threatlocker-assessment-prep-cbt`).

### Missing Topics/Tags
Only `devops-superlab` has topics. All others have empty topic lists. Topics improve discoverability. Recommend adding relevant topics to at least: interstitium-labs, interstitium-certification-bootcamps, lps-enrollment-analysis, ai-vision-deck-print-manufacturing.

### Missing Homepage URLs
- `interstitium-certification-bootcamps`: no homepage (should link to bootcamp catalog)
- `threatlocker-assessment-prep-cbt`, `full-spectrum-dominance-cbt`: no homepage links
- `interstitium-labs`: ✅ has https://interstitiumlabs.dev
- `devops-superlab`: ✅ has GitHub Pages URL

## 3. Pinned Repositories

**Status: NONE pinned.** This is the biggest gap.

GitHub allows 6 pinned repos on the profile. Currently showing zero, which wastes prime profile real estate.

**Recommended pins** (reflecting current work):
1. `interstitium-labs` — flagship knowledge OS
2. `devops-superlab` — DevOps portfolio centerpiece
3. `interstitium-certification-bootcamps` — 68 bootcamps
4. `lps-enrollment-analysis` — data analysis evidence
5. `ai-vision-deck-print-manufacturing` — AI architecture portfolio piece
6. `threatlocker-assessment-prep-cbt` — timely (ThreatLocker interview Oct 13)

## 4. Commit Activity

Strong recent activity:
- Oct 8: Multiple pushes to interstitium-labs (5+ pushes)
- Oct 7: Pushes to devops-superlab, profile README, interstitium-labs
- Oct 6: CBT repo updates across the board
- Oct 5: ThreatLocker prep repos
- Oct 4: Assessment bootcamp
- Oct 3: Interview test bootcamp (empty), threatlocker repos
- Oct 2: University, AI vision deck

Contribution graph will show solid recent activity. No gaps in the last 7 days.

## 5. Security

- **Secret scanning alerts**: 0 on interstitium-labs, 0 on devops-superlab (the two largest/most active repos)
- **Credential files**: No `.env`, `credentials`, `*.pem`, `*.key`, or password files found in top-level directory listings of the two main repos
- **Note**: Full secret scan across all 19 repos was not performed (would require cloning). The two highest-risk repos (largest, most active) are clean.

## 6. Issues Summary

### Critical
None.

### Major
1. **No pinned repositories** — profile shows zero pinned repos, wasting the most visible profile section
2. **Empty repo** (`threatlocker-interview-test-bootcamp`) — 0 KB, should be deleted

### Minor
3. **Missing topics** on 18/19 repos — hurts discoverability
4. **Missing homepage URLs** on several repos — reduces click-through to live sites
5. **Profile README confusion** — "Inspect this portfolio" section references non-existent paths in the profile repo

## 7. Recommendations (not yet applied)

1. Pin 6 repos (list above)
2. Delete `threatlocker-interview-test-bootcamp` (empty)
3. Add topics to major repos
4. Add homepage URLs to bootcamp/CBT repos
5. Fix profile README "Inspect this portfolio" section
6. Consider archiving `interstitium-labs-university` (legacy, superseded by flagship) — or add a deprecation notice to its README

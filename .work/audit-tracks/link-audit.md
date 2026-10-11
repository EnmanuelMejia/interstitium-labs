# LINK AUDIT — Track 1
**Date:** 2026-10-08 ~21:22–22:35 EDT (audit-only, no code changed)
**Method:** curl against live URLs (followed redirects, `-o /dev/null -w '%{http_code}'`).
Discovery: (a) `sitemap.xml` from each host, (b) `href`/`src` grep over all 176 HTML files in `docs/`,
(c) nav links scraped from the live homepages of each host. Every internal link was checked;
a 60-link external sample (one per domain + all of the user's own profiles/repos) was checked.

## Counts
| Host | Internal links checked | Result |
|---|---|---|
| interstitiumlabs.dev | 592 unique (580 from repo + 120 sitemap + 9 course URLs + 2 bootcamp URLs) | 591 × 200, 1 × 307→200 on re-verify |
| learn.interstitiumlabs.dev | 70 (homepage nav) | 70 × 200 |
| app.interstitiumlabs.dev | 68 (homepage nav) | 68 × 200 |
| enmanueldmejia.com | 9 (homepage nav) | 9 × 200 |
| External sample | 60 | 58 verified OK, 2 bot-gated (see couldn't-check), 0 verified broken |
| **Total** | **739 internal + 60 external = 799** | |

## Broken links (verified 404/500)
**None.** Zero verified-broken links across all four hosts.

## Couldn't-check (not verified-broken)
1. `https://en.cppreference.com/c/io` — 403 even with a real browser UA; cppreference blocks datacenter/bot IPs. Source: `learn/sequences/c-language/index.html`. Couldn't distinguish bot-block from dead link via curl.
2. `https://chat.deepseek.com/share/4j6jplmxg2zcfxo34q` — 403 with audit UA, 202 (challenge page) with browser UA; DeepSeek share links require JS/session. Source: `prep/drills/instrument-desk/index.html`. Not verified broken.
3. Authenticated-only content behind `/account/` (sign-in page, 200) and `/admin/` (200) — the public pages return 200; anything requiring a login session was not checked per scope.
4. External links outside the 60-link sample (397 total external links in repo, mostly docs references: kubernetes.io, learn.microsoft.com, arxiv.org, github.com project pages, etc.) — not individually checked.

## Notes
- One transient anomaly: `https://interstitiumlabs.dev/university/assess.html?a=` returned 307 once (canonical redirect to `/university/assess?a=`); re-verified manually → 200 after a single redirect. Not broken.
- The first pass (30 parallel curls) produced mass `000` timeouts from parallel overload/rate-limiting; all were re-checked at 8 parallel with a 45 s timeout and resolved to 200. One early `/tmp` wipe during the run forced a restart; scripts and results now live in `.work/scratch/` (streaming, restart-safe).
- All 9 tested university course URLs returned 200: `il-01, il-06, il-11, il-12, il-20, il-26, il-27, il-28, il-29` (`/university/course?course=<id>`).
- Both bootcamp pages return 200 anonymously: `/bootcamps/tl-interview/`, `/bootcamps/threatlocker-assessment-prep/`.
- The user's own GitHub profile and all linked repos (`github.com/EnmanuelMejia`, `devops-superlab` and subpaths, `interstitium-labs`, `ai-vision-deck-print-manufacturing`, `lps-enrollment-analysis`) return 200.
- No LinkedIn/Instagram/X/TikTok profile URLs exist anywhere in the site source, so there were none to check.

## 5-line summary
1. 739 internal links checked across all 4 hosts — every single one returns 200; zero broken internal links.
2. 60-link external sample: 58 verified OK, zero verified broken; 2 couldn't be distinguished from bot-blocking (cppreference, DeepSeek share link).
3. All 9 tested university course URLs (IL-01→IL-29 mix) and both bootcamp pages return 200 anonymously.
4. Sitemaps healthy: 120 URLs on interstitiumlabs.dev (+ mirrored on learn/app), 1 on enmanueldmejia.com; all live.
5. User-impact verdict: no link repairs needed; only follow-ups are the 2 bot-gated externals (manual check if desired) and un-checkable logged-in content.

Raw results: `.work/scratch/res_flagship.jsonl`, `res_learn.jsonl`, `res_app.jsonl`, `res_emd.jsonl`, `res_external.jsonl`.

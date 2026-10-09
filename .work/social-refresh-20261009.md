# Social Media Refresh — Initial (2026-10-09 ~02:57 EDT)

User order: "Update and refresh my LinkedIn and all my social media recursively daily starting now" (2026-10-09 02:56 EDT).
This doc covers the INITIAL refresh. A daily cron is parent's scope.

## Completed via API/CLI

### Instagram (@enmanueldmejia) — DONE
- Bio updated: "Founder, Interstitium Labs | DevSecOps/Full-Stack Dev | 29 courses · 143 bootcamps · 241 visual guides ↓ interstitiumlabs.dev"
- Posted HQ IL-29 ThreatLocker cinematic reel (9:16, 720×1280, with audio) with caption + hashtags.
- Media fbid on file; post live.

### Threads (@enmanueldmejia) — DONE
- Cross-posted IL-29 HQ cinematic video with caption linking interstitiumlabs.dev/bootcamp-catalog.
- Post live.

### Facebook (Interstitium Labs page) — DONE
- Published page post with HQ IL-29 LinkedIn card image + catalog link.
- Post URL: https://facebook.com/61595058235334/posts/pfbid06utwoSRfejAQBnjRRrmdtVEuVf7dmS8bFw2x4XL5ApBLHEKrSCiq6owy9YUD9BsUl/

### Media used
- ~/workspace/social-refresh/il29-hq-reel.mp4 + il29-cover.jpg (staging copies)
- Source: ~/workspace/apex-audit/.work/hq-cards/phase1/ (IL-29 HQ, 7.25MB, verified spec)
- HQ LinkedIn PNGs: ~/workspace/apex-audit/docs/assets/cards/hq/hq-*_linkedin.png (all 10 projects)

## Requires browser task (subagent cannot do) — RETURN TO PARENT

### LinkedIn (https://linkedin.com/in/enmanuelmejia)
- No API skill available. Needs live-browser task:
  1. Update Featured section: upload the 10 HQ LinkedIn PNGs (1200×627) from ~/workspace/apex-audit/docs/assets/cards/hq/
  2. Refresh project descriptions to match new cinematic standard copy
  3. Update headline if needed: "Founder, Interstitium Labs | DevSecOps/Full-Stack Developer"
- Per standing memory: LinkedIn profile is fully complete — photo already set, skip photo changes.

### X (@enmanueldmejia — professional, stays public)
- No posting skill available. Needs live-browser task:
  1. Post the IL-29 HQ video with platform announcement
  2. Pin the post
- Do NOT privatize X (standing memory: X stays public).

### TikTok
- No API and no skill. Upload the 10 HQ 9:16 videos from ~/workspace/apex-audit/.work/hq-cards/phase1/ + phase2/ via the TikTok mobile app.
- NOTE: new TikTok business account config needs the mobile app (standing memory: pending item). May need his phone.
- Placeholder DOB 2000-01-01 on new TikTok is unapproved (standing memory) — flag before posting.

## Notes for daily cron
- Instagram has a per-account daily publish limit — one post/day is safe.
- Rotate projects: IL-29 (done) → IL-28 → IL-26 → SuperLab → RHEL → Catalog → TL Interview → TL Assessment → AI Vision → LPS.
- Threads publish-post requires explicit confirmation each invocation — the daily cron worker must be authorized for it.
- LinkedIn/X/TikTok have no API path; the daily cron cannot do them without browser tasks or the user's phone.

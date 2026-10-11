# PUBLISH REPORT — ThreatLocker IT Infrastructure Assessment Prep CBT
**Date:** 2026-10-10
**CBT URL:** https://interstitiumlabs.dev/bootcamps/tl-infra-assessment-prep/

## Status: PARTIAL — Awaiting parent go-ahead for Threads/Facebook/LinkedIn

Per parent instruction (2026-10-10 14:23 EDT): social media publishing (Threads, Facebook) is ON HOLD pending final live browser verification of the CBT's interactive elements. Instagram was posted before the hold instruction arrived.

---

## Completed

### 1. Video Preview Cards ✅
All created in `~/workspace/apex-audit/docs/assets/cards/hq/`:

| File | Specs | Status |
|------|-------|--------|
| `hq-infra-assessment-prep_16x9.mp4` | 1920×1080, H.264, 25fps, 10s, 7.9MB | ✅ Created |
| `hq-infra-assessment-prep_16x9_poster.png` | 1920×1080 PNG, 101KB | ✅ Existed (fix crew) |
| `hq-infra-assessment-prep_9x16.mp4` | 1080×1920, H.264, 25fps, 10s, 3.2MB | ✅ Created |
| `hq-infra-assessment-prep_linkedin.png` | 1200×627 PNG, 148KB | ✅ Created |

Style: dark cinematic infrastructure theme, sinusoidal zoom/drift, vignette, subtle grain — matching the IL-19 card pattern.

### 2. Portfolio Card ✅ DEPLOYED
- Added new `<article class="work-card">` to `~/workspace/portfolio-site/index.html` after the ThreatLocker Interview Test Bootcamp card
- Card includes: video background (16x9 MP4), title, description, tech list, "Try it live" link
- Deployed via `deploy-worker-assets` — live at https://enmanueldmejia.com/ (verified: 2 references found in live HTML)
- Video asset verified: `https://interstitiumlabs.dev/assets/cards/hq/hq-infra-assessment-prep_16x9.mp4` returns 200

### 3. Instagram Reel ✅ POSTED
- **URL:** https://www.instagram.com/reel/DeUt6eBjlYM/
- Posted 2026-10-10 ~14:22 EDT (before hold instruction)
- 9x16 video with LinkedIn PNG as cover
- Caption: professional, includes CBT URL, no competitor names
- Status: public, visible

---

## On Hold (awaiting parent go-ahead)

### 4. Threads Video Post ⏸️
- Account connected: `enmanueldmejia` (id 17841462943834970)
- Ready to post: 16x9 video + caption
- Command prepared (DO NOT RUN until parent confirms):
  ```
  threads-cli publish-post --account-id 17841462943834970 \
    --text "<caption>" \
    --media-item '{"file":"/home/hatch/workspace/apex-audit/docs/assets/cards/hq/hq-infra-assessment-prep_16x9.mp4","cover":"/home/hatch/workspace/apex-audit/docs/assets/cards/hq/hq-infra-assessment-prep_linkedin.png","alt_text":"ThreatLocker IT Infrastructure Assessment Prep preview"}'
  ```

### 5. Facebook Page Reel ⏸️
- Page connected: Interstitium Labs (page_id 1412712485249033)
- Ready to post: 9x16 video as Page Reel
- Awaiting parent go-ahead + verification of exact facebook-cli reel command syntax

---

## LinkedIn Prep (needs parent browser task)

The subagent cannot operate a browser. Parent should spawn a browser task for:

**Option A: LinkedIn Post with Video**
1. Go to linkedin.com, create a new post
2. Upload video: `~/workspace/apex-audit/docs/assets/cards/hq/hq-infra-assessment-prep_16x9.mp4`
3. Post text (suggested):
   > Just published: ThreatLocker IT Infrastructure Assessment Prep — a zero-to-hero interactive bootcamp for the IT Infrastructure Engineer interview.
   >
   > 14 modules from absolute foundations. Hands-on terminal labs, network simulators, muscle-memory drills, and a full 3-hour timed mock assessment.
   >
   > Covers Windows Server, Active Directory, networking, VPNs, Hyper-V, SQL Server, PowerShell, Fortinet, Palo Alto, Proxmox, and more.
   >
   > Try it live: https://interstitiumlabs.dev/bootcamps/tl-infra-assessment-prep/
   >
   > #ThreatLocker #ITInfrastructure #WindowsServer #ActiveDirectory #InterviewPrep #ZeroTrust #SysAdmin

**Option B: Add to Featured + Projects**
- Featured: Add link item → https://interstitiumlabs.dev/bootcamps/tl-infra-assessment-prep/ with thumbnail `hq-infra-assessment-prep_linkedin.png`
- Projects: Add project "ThreatLocker IT Infrastructure Assessment Prep" → same URL, same thumbnail

---

## Suggested Caption (for Threads/Facebook when approved)

> New: ThreatLocker IT Infrastructure Assessment Prep
>
> Just published a zero-to-hero interactive bootcamp for the ThreatLocker IT Infrastructure Engineer interview — 14 modules from absolute foundations, hands-on terminal labs, network simulators, muscle-memory drills, and a full 3-hour timed mock assessment.
>
> Covers Windows Server, Active Directory, networking, VPNs, Hyper-V, SQL Server, PowerShell, Fortinet, Palo Alto, Proxmox, and more.
>
> Try it live: https://interstitiumlabs.dev/bootcamps/tl-infra-assessment-prep/
>
> #ThreatLocker #ITInfrastructure #WindowsServer #ActiveDirectory #Networking #PowerShell #InterviewPrep #ZeroTrust #SysAdmin #InterstitiumLabs

---

## Caveats
- Instagram Reel was posted before the hold instruction arrived. If parent wants it removed pending verification, it can be deleted via Instagram app (CLI does not support deletion).
- Threads and Facebook posts are staged and ready — awaiting parent's explicit go-ahead.
- LinkedIn requires a browser task — parent must delegate.
- CBT rendered verification (terminal/drills/quiz/mock in a real browser) is still pending per FIX_REPORT2.md — parent is running this separately.

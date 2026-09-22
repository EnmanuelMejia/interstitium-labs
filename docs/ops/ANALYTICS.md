# Analytics — first-party

## What ships

- `/assets/il-analytics.js` — `ILAnalytics.track(name, props)`
- Ring buffer: `localStorage il.analytics.v1` (~400 events)
- Config: `/analytics/config.js` (`endpoint: null` until Worker URL)
- A/B: `localStorage il.exp.v1` via `ILAnalytics.assignVariant(expId, variants)`
- Insights: `/admin/insights/`
- Iteration: `/assets/il-iterate.js` (`ILIterate`) → `il.iterate.v1`

## Events (exact names)

| Name | When |
|------|------|
| `page_view` | Boot |
| `cta_click` | Tracked / main CTAs |
| `enroll_click` | `/enroll/` links |
| `path_open` | `/paths/` links |
| `checklist_tick` | Progress checkboxes |
| `quest_claim` / `hud_level_up` | `il:game` bridge |
| `lang_select` | Language picker (`il:lang`) |
| `friction_reload` | ≥4 reloads / 60s |
| `exp_assign` | A/B assignment |

## Remote beacon

Paste Worker ingest URL into `docs/analytics/config.js` → `endpoint`. Local buffer works until then.

## Cloudflare Web Analytics (optional)

Set `cloudflareBeaconToken` to a **real** token from Cloudflare → Web Analytics. Leave `null` to skip (no fake tokens).

```html
<a href="/enroll/" data-il-track="enroll_click" data-il-exp="cta_enroll_copy" data-il-exp-b="Join the cohort">Enroll</a>
```


## Events (2026-09-22)
- `demo_path_complete` · `trending_open` · `exam_answer`

## Frontier Tracks events

| Name | When |
|------|------|
| `frontier_open` | Frontier mount / filter render |
| `frontier_click` | External course link or Muse/Adapt/Lab overlay |
| `frontier_complete` | Learner marks a Frontier card done |
| `frontier_thumb_up` / `frontier_thumb_down` | Card quality votes |

Scores roll into `il.frontier.scores.v1` and feed `ILIterate` weekly promote/demote. See `TRENDING-COURSES-X-LINKEDIN-MIT.md`.


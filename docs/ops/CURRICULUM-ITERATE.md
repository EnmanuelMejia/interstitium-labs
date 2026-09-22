# Curriculum iterate — Frontier promote / demote

Weekly (~15 min) loop so Frontier cards earn their rank from **local** first-party analytics — not vanity metrics.

## Ritual

1. Browse `/paths/frontier/` on a device that already has site traffic (buffer is local).
2. Open `/admin/insights/` → **Refresh** (`ILIterate.run()`).
3. Read Frontier section: clicks, completes, thumbs → `il.frontier.scores.v1`.
4. Act on top recommendation: promote high-score cards (already auto-sorted by `il-trending.js`) or demote noise by labeling/removing stale X-signal rows in the catalog.
5. Ship a small catalog/HTML/i18n diff; push `main`.

## Heuristics

| Signal | Action |
|--------|--------|
| High `frontier_click` + low `frontier_complete` | Check link rot; prefer OCW/public pages over login walls |
| High `frontier_thumb_down` | Demote / annotate honesty gap; do not invent replacements |
| Zero Frontier events + healthy `path_open` | Surface Frontier CTA on `/paths/` and `/learn/` |
| LinkedIn clicks with bounce | Keep `accessNote`; never claim we include the video |
| Muse overlay clicks | Good — deep-link only; do not fork `il-muse*` |

## Do not

- Invent Stripe keys, Cloudflare tokens, MIT course numbers, or X like counts
- Pirate or mirror paid video
- Meta-skin the Interstitium chrome
- Block on CF redeploy from another agent — push cleanly
- Regress Muse or exceed path pages while refreshing Frontier

## Storage keys

| Key | Owner |
|-----|-------|
| `il.analytics.v1` | `il-analytics.js` |
| `il.frontier.scores.v1` | `il-trending.js` |
| `il.iterate.v1` | `il-iterate.js` |
| `il.paths.v1` | path exceed progress (untouched here) |

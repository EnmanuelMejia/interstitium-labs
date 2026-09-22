# Iteration loop (Enmanuel)

## Weekly ritual (~15 min)

1. Open https://interstitiumlabs.dev/admin/insights/ on a browser that has browsed the site (buffer is local).
2. Click **Refresh** — `ILIterate.run()` reads `il.analytics.v1`, writes `il.iterate.v1`.
3. Read funnel: Views → CTA → Enroll.
4. Act on the top recommendation; ship a small HTML/CSS/i18n diff; push `main`.
5. Optional: when Worker `endpoint` exists, compare to aggregates.

## Heuristics

- Prep CTA underperforms vs Founders → A/B copy (`data-il-exp="cta_prep_copy"`)
- Views + CTAs but zero `enroll_click` → dead enroll path
- `friction_reload` bursts → mobile HUD / layout
- Language mix → prioritize long-form for top non-EN locales
- Dead `/enroll/` CTA → contrast / mid-page repeat

## Do not

- Invent Stripe keys or fake Cloudflare tokens
- Block on CF redeploy from another agent — push cleanly

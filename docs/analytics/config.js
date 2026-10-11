/**
 * First-party analytics config (public, client-side).
 *
 * HONEST STATUS (updated 2026-10-11): endpoint is live — the flagship
 * worker serves POST /api/analytics/ingest, which folds events into
 * per-day aggregates in KV (no IPs, no user ids, no raw payloads).
 * Local ring buffer always works (`il.analytics.v1`).
 *
 * Cloudflare Web Analytics: set cloudflareBeaconToken from
 * Cloudflare → Web Analytics → Manage site. Leave null to skip (no fake tokens).
 * See /ops/ANALYTICS.md
 */
window.IL_ANALYTICS = {
  endpoint: "/api/analytics/ingest", // same-origin flagship worker endpoint
  cloudflareBeaconToken: null, // paste real token only
  sampleRate: 1,
  maxBuffer: 400,
  version: 1
};

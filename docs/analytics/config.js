/**
 * First-party analytics config (public, client-side).
 *
 * HONEST STATUS: endpoint is null until Enmanuel pastes a Cloudflare Worker /
 * Analytics Engine ingest URL. Local ring buffer always works (`il.analytics.v1`).
 *
 * Cloudflare Web Analytics: set cloudflareBeaconToken from
 * Cloudflare → Web Analytics → Manage site. Leave null to skip (no fake tokens).
 * See /ops/ANALYTICS.md
 */
window.IL_ANALYTICS = {
  endpoint: null, // e.g. "https://analytics.interstitiumlabs.dev/ingest"
  cloudflareBeaconToken: null, // paste real token only
  sampleRate: 1,
  maxBuffer: 400,
  version: 1
};

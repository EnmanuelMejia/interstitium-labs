# Platform Upgrades — 2026-10-09

User order ~03:55 EDT. Four major changes deployed to flagship worker `solitary-sound-015a`.

## 1. Paywall TEMPORARILY DISABLED ✅

**Status:** All courses FREE until payment processor is set up.

**Changes:**
- `_worker.js`: Added `PAYWALL_DISABLED = true` constant. `courseGate()` returns passthrough immediately when true.
- Payment infrastructure preserved intact (payment-routes.js, entitlement tokens, checkout UI) — just bypassed.
- `/enroll/`: Added "🎉 Free during beta" banner linking to all courses.

**To re-enable:** Set `PAYWALL_DISABLED = false` in `_worker.js`, rebuild bundle, redeploy.

**Verified:** Gated course page (il-01) returns 200. Gated course JSON returns 200 (was 402).

## 2. Social Login (OAuth) ✅

**Status:** Infrastructure complete. OAuth app credentials NOT yet configured.

**Providers:** GitHub, Google, LinkedIn, X (Twitter), Facebook.

**Routes:**
- `GET /api/auth/oauth/providers` → JSON list of providers + configured status
- `GET /auth/oauth/:provider` → 302 redirect to provider authorize URL
- `GET /auth/oauth/:provider/callback` → exchange code, create session, redirect to /progress/

**Sessions:** Reuses existing `il_session` cookie + `IL_ACCOUNTS` KV. Stores `{email, name, avatar, provider}`.

**Frontend:** `/account/` sign-in form now shows "Continue with GitHub/Google/LinkedIn/X/Facebook" buttons. Unconfigured providers are greyed out.

**TO CONFIGURE (user action required):**
For each provider, create an OAuth app and set secrets via `wrangler secret put`:
- `GITHUB_CLIENT_ID` / `GITHUB_CLIENT_SECRET` — https://github.com/settings/developers
- `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` — https://console.cloud.google.com/
- `LINKEDIN_CLIENT_ID` / `LINKEDIN_CLIENT_SECRET` — https://developer.linkedin.com/
- `TWITTER_CLIENT_ID` / `TWITTER_CLIENT_SECRET` — https://developer.twitter.com/
- `FACEBOOK_CLIENT_ID` / `FACEBOOK_CLIENT_SECRET` — https://developers.facebook.com/

Callback URL for all: `https://interstitiumlabs.dev/auth/oauth/{provider}/callback`

**Verified:** `/api/auth/oauth/providers` returns correct JSON with all 5 providers showing `configured: false`.

## 3. Noah AI Voice Chat ✅

**Status:** Fully implemented (frontend).

**Files:**
- `assets/noah-voice.js` (new, 12KB) — auto-loaded by `noah-ai.js`
- `assets/noah-ai.js` (modified) — auto-loads voice module

**Features:**
- 🎤 **Microphone button** in chat input — uses Web Speech API (SpeechRecognition) for speech-to-text. Auto-sends transcribed text.
- 🔊 **Speaker toggle** in chat header — uses speechSynthesis for text-to-speech. Noah's replies are read aloud when enabled. Preference saved to localStorage.
- Graceful degradation where Web Speech API is unsupported (button disabled with tooltip).

**Note:** Browser-native APIs (no server dependency). Works in Chrome/Edge/Safari. Firefox has limited SpeechRecognition support.

## 4. Noah AI Open-Source Capabilities ✅

**Status:** Fully implemented (backend + frontend).

**Backend (`_worker.js`):**
- `POST /api/noah` now accepts `model` (validated against allowlist) and `mode` (`tutor` | `general`).
- `GET /api/noah/models` → JSON list of available models.
- **Models:**
  - Llama 3.3 70B (default) — best quality
  - Mistral 7B — fast general purpose
  - Qwen 2.5 Coder 32B — code generation specialist
  - DeepSeek Math 7B — math specialist
- **Modes:**
  - `tutor` (default) — Socratic, course-aware, uses knowledge base
  - `general` — Open ChatGPT-like assistant, no Socratic doctrine, 1200 token limit

**Frontend (`noah-voice.js`):**
- **Model selector dropdown** in chat header — populated from `/api/noah/models`
- **Mode toggle** (Tutor / General pills) — switches between Socratic tutoring and open assistant
- Preferences saved to localStorage
- Model/mode injected into `/api/noah` POST body via fetch patch

**Verified:**
- `/api/noah/models` returns 4 models with labels
- General mode with default model returns proper open-assistant response
- Tutor mode still works (default behavior unchanged)

## Deploy History
- 2026-10-09T07:58:37Z — Initial deploy (etag 96f4eea9a3d7)
- 2026-10-09T07:59:25Z — Added run_worker_first routes (etag 96f4eea9a3d7)
- 2026-10-09T08:00:31Z — Fixed model allowlist (etag 23dda501f358)

## Files Modified
- `docs/_worker.js` — paywall bypass, OAuth routes, Noah model/mode support
- `docs/_worker.bundle.js` — rebuilt
- `docs/assets/noah-voice.js` — NEW: voice chat + model selector + mode toggle
- `docs/assets/noah-ai.js` — auto-loads voice module
- `docs/assets/il-account.js` — OAuth login buttons
- `docs/enroll/index.html` — "Free during beta" banner
- `.work/flagship-deploy-config-20261008.json` — added 12 OAuth/Noah routes to run_worker_first

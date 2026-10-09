# Noah AI Persona & Voice Expansion — 2026-10-09

## Overview
Major expansion of Noah AI with personas, human-like voices, expanded models,
avatar customization, adaptive voice tech, and adaptive learning engine.

## 1. Multiple AI Voices
**File:** `docs/assets/noah-personas.js`

5 voice profiles with descriptive labels (NOT named after real people):
| Profile | Label | Character | TTS Voice | Rate | Pitch |
|---------|-------|-----------|-----------|------|-------|
| scholar | Scholar 📖 | Measured, precise | MAI_01 (Warm) | 0.92 | 0.95 |
| narrator | Narrator 🎙️ | Warm, engaging | MAI_03 (Smooth) | 1.00 | 1.00 |
| guide | Guide 🧭 | Clear, encouraging | MAI_01 (Warm) | 1.00 | 1.10 |
| sage | Sage 🦉 | Deep, contemplative | MAI_03 (Smooth) | 0.85 | 0.80 |
| spark | Spark ⚡ | Energetic, quick | MAI_01 (Warm) | 1.15 | 1.15 |

### Voice Naturalness (user requirement 2026-10-09)
All voices prioritize natural, human-like sound. The `pickBestVoice()` function:
1. **Excludes** robotic/synthetic voices (filters: robot, espeak, festival, flite, pico, svox, eloquence, dectalk)
2. **Prioritizes** natural/human/neural/wavenet voices
3. **Prefers** premium/enhanced voices
4. Falls back to per-profile distinct voices from the natural pool

Server-side TTS ranking (per skill docs — MAI_01/MAI_03 are "recommended, production-quality"):
1. `avocado_v2:MAI_01` (Warm) — most natural
2. `avocado_v2:MAI_03` (Smooth) — most natural
3. `avocado_v2:rumi`
4. `avocado_v2:chip`
5. `avocado_v2:briggs`

All 5 tested 2026-10-09 — all generate successfully. MAI_01 and MAI_03 used for all voice profiles.

UI shows active voice name in the widget so users can verify quality.

## 2. Persona Modes
**Backend:** `docs/_worker.js` (`NOAH_PERSONAS` constant)
**Frontend:** `docs/assets/noah-personas.js`

5 original personas (no real-person impersonation):

| Persona | Icon | Style | Voice | Avatar | Accent |
|---------|------|-------|-------|--------|--------|
| Visionary | 🔭 | Bold, first-principles, future-focused | Narrator | Sigil | Gold |
| Engineer | ⚙️ | Precise, systems-thinking, pragmatic | Scholar | Orrery | Cyan |
| Philosopher | 🏛️ | Socratic, deep, questioning | Sage | Monas | Violet |
| Mentor | 🌱 | Encouraging, practical wisdom | Guide | Wisp | Emerald |
| Trickster | 🃏 | Playful, lateral thinking, comedic | Spark | Sigil | Cyan |

Each persona:
- Sends `persona` param to POST /api/noah
- Backend injects persona-specific system prompt modifier
- Auto-switches to matched voice profile + avatar style
- Persists selection in localStorage

## 3. Open-Source Models (Expanded)
**Backend:** `docs/_worker.js` (`NOAH_MODELS`)

Expanded from 4 → 14 models:
- Llama 3.3 70B (default), Llama 3.1 8B, Llama 3.2 3B, Llama 3.2 1B
- Mistral 7B v0.3, Mistral 7B v0.2
- Qwen 2.5 Coder 32B, Qwen 2.5 14B, Qwen 1.5 14B
- DeepSeek Math 7B, Gemma 2 9B, Phi-2, Falcon 7B, DiscoLM 7B

GET /api/noah/models returns models + personas + defaults.

## 4. Avatar Customization
**Frontend:** `docs/assets/noah-personas.js` (picker UI)
**Existing:** `docs/assets/il-noah-avatar.js` (4 procedural WebGL avatars)

Picker UI in Noah widget:
- 4 avatar styles: Monas 💠, Orrery 🪐, Sigil ✨, Wisp 🌌
- 4 accent colors: Cyan, Gold, Violet, Emerald
- Click to select; persists in localStorage
- Persona auto-switches avatar unless user has customized

All avatars are procedural/original — no real-person likenesses.

## 5. Voice/Video Adaptive Tech
**Frontend:** `docs/assets/noah-personas.js`

### Adaptive Speech Rate
`analyzeComplexity()` analyzes text and adjusts rate 0.8x–1.15x:
- Dense technical content → slower
- Casual conversation → faster
- Factors: sentence length, technical terms, code blocks, numbers

### Emotion-Aware TTS
`detectEmotion()` detects tone and adjusts pitch/rate:
- Encouraging (great, amazing, proud) → pitch 1.15x, rate 1.05x
- Serious (critical, warning, risk) → pitch 0.9x, rate 0.9x
- Playful (funny, joke, absurd) → pitch 1.2x, rate 1.1x
- Inquiring (multiple ?) → pitch 1.1x, rate 0.95x

### Lip-Sync
- Drives avatar "speaking" state via speechSynthesis events
- Word-level sync via `onboundary` events → avatar pulse per word
- `onstart`/`onend`/`onerror` → speaking/idle state transitions

## 6. Adaptive Learning Engine
**File:** `docs/assets/noah-adaptive.js`
**Backend:** `docs/_worker.js` (adaptive context injection)

### Topic Mastery Tracking
- Records quiz/drill/lab attempts per topic
- Weighted moving average for mastery score (0–1)
- Minimum 2 attempts before classification as weak/strong

### Spaced Repetition (SM-2)
- Full SM-2 algorithm: easiness factor, interval, repetitions
- Quality 4 for correct, 1 for incorrect
- `getDueReviews()` returns overdue topics sorted by urgency
- `getUpcomingReviews()` returns topics due within 48h

### Learning Style Detection
Tracks interaction patterns across 4 dimensions:
- Visual (video, diagram, image interactions)
- Hands-on (lab, drill, terminal interactions)
- Theoretical (reading, text interactions)
- Socratic (quiz, discussion interactions)

Normalizes to 0–1 weights. Dominant style influences AI explanations.

### Socratic Depth Control (1–5)
UI slider in Noah widget:
- 1/5 Direct: Give direct answers immediately
- 2/5 Light: Answer + one follow-up question
- 3/5 Balanced: Default Socratic guidance
- 4/5 Deep: Prefer questions, answer only when stuck
- 5/5 Maximum: Questions only, never direct answers

Backend injects depth-specific modifier into system prompt.

### Session Memory
- Persistent cross-session (localStorage, max 50 sessions)
- Tracks topics covered per session
- 4-hour inactivity timeout for session expiry
- `getMemorySummary()` provides AI context: recent topics, weak/strong areas, style, depth

### Progress Analytics Dashboard
Collapsible panel in Noah widget showing:
- Learning style breakdown with percentages
- Per-topic mastery bars (color-coded: green ≥80%, yellow ≥50%, red <50%)
- Spaced review due/overdue items
- Stats: total interactions, topics tracked, sessions

### Quiz Auto-Detection
MutationObserver watches for quiz result indicators (correct/incorrect classes/text).
Click tracking detects content type interactions for style detection.
Topic detection from page data attributes, URL patterns, or path fallback.

### Backend Integration
POST /api/noah accepts:
- `adaptiveContext`: pre-built learner profile string (max 2000 chars)
- `socraticDepth`: 1–5 integer

Backend injects adaptive context + depth modifier into system prompt.
Response includes `persona` and `socraticDepth` for confirmation.

## Privacy
All adaptive data stored device-local (localStorage). No cloud sync.
Session memory is conversation-scoped for AI context but profile persists locally.
No PII transmitted — only anonymized topic IDs and mastery scores in adaptive context.

## Files Changed
- `docs/_worker.js`: NOAH_MODELS expanded (4→14), NOAH_PERSONAS added, handleNoah accepts persona/adaptiveContext/socraticDepth, /api/noah/models returns personas
- `docs/assets/noah-ai.js`: Auto-loads noah-personas.js and noah-adaptive.js
- `docs/assets/noah-personas.js`: NEW — personas, voices, avatars, adaptive voice tech (22KB)
- `docs/assets/noah-adaptive.js`: NEW — adaptive learning engine (27KB)

## Deployment
Deployed to flagship worker `solitary-sound-015a` on 2026-10-09.
All JS syntax validated with `node --check`.
Worker bundle validated.

## Constraints Honored
- ✅ No voice cloning of real people
- ✅ No celebrity/tech leader likenesses
- ✅ All voices are original AI creations with descriptive labels
- ✅ All avatars are procedural/original geometric designs
- ✅ Personas are original speaking styles, not impersonations

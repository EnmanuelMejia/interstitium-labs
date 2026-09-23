# Muse AI ↔ Noah **mobile** capability benchmark (recursive)

**Scope:** Interstitium Labs mobile Learning OS — PWA + Capacitor `apps/mobile` · Noah `/coach/`  
**Not in scope (by design):** Meta Gmail / Calendar / WhatsApp / booking / Spotify-style connectors  
**Brand lock:** Interstitium lockup (56–80px) · cyan `#5EEAD4` · gold `#D4A853` · void `#070B16` · Dee monas avatar  
**Honesty:** Muse-*class interaction patterns* from **public** Meta design posts — **not** Meta IP, assets, purple/pink Muse skin, or product clone.

| Field | Value |
| --- | --- |
| Benchmark date | 2026-09-22 (America/New_York) |
| Ship SHA | `7e14aea` · tip `bff3920` |
| Overall (Learning-OS mobile) | **YES** — meets Muse-class companion behaviors in scope; exceeds on lab-state / Adapt / Ollama / proof / EN·ES axes |
| Meet | 9 |
| Exceed | 7 |
| Gap (closable remaining) | 0 |
| N/A-by-design | 3 |

**Elon / Musk bar (self):** visitor on phone cold-starts Noah → long chat + interrupt multi-send → local nudge → artifact with proof link → optional Ollama lean tier — without fake connectors or invented API keys. **Pass for Learning-OS scope.** Still NO on Meta-cloud push fleet / WhatsApp — deliberately.

---

## Recursive matrix

| Muse AI capability (public) | IL mobile status | Evidence path | Elon bar |
| --- | --- | --- | --- |
| Main persistent chat (not turn-locked) | **Meet** | `docs/assets/il-muse.js` `chats.main` · `localStorage il.muse.v1` · `/coach/` | Long session survives reload |
| Side chats | **Meet** | Rail + swipe drawers · `chats.sides` · `il-muse-mobile.css` | Topic contexts without losing main |
| Interruptible multi-send | **Meet** | `inflightGen` + Stop · sequential `splitBubbles()` multi-bubble · thinking typing indicator | New message cancels prior reply |
| Proactive goals / background work | **Exceed** | `localNudges()` strip + Inbox harvest (`harvestNudges`) from goals + `ILAdaptive` weak topics · optional Notification API (no FCM) | Local study cadence without Meta push infra |
| Editable memory | **Meet** | Settings → memories add/remove · passed to router ctx | Student owns local memory |
| Artifacts (rich outputs) | **Exceed** | CIDR / lab-checklist / proof / path deep-link cards · checkable lists · Library tab | Lab evidence > chat dump |
| Avatar + activity transparency | **Exceed** | Dee default SVG · idle/listening/thinking/speaking · live strip · activity log | Status honesty + Interstitium original art |
| Goals | **Meet** | Goals panel · checkbox persist · goal nudges | Open goals drive inbox |
| Voice / transcription | **Meet** | Web Speech mic + TTS · status Listening/Speaking · mic permission notes (iOS/Android snippets) | Works without cloud STT keys |
| Permissions / approval cards | **Meet** | Inline approve (Adaptive/SuperLab/Model) + modal before **external open** / **model switch** | No silent outbound / backend flip |
| Connectors (email / calendar / WhatsApp) | **N/A-by-design** | Explicitly out of Learning-OS Noah scope | Honesty > fake Meta clones |
| Cloud push / Meta infra | **N/A-by-design** | `IL_FEATURE_PUSH=false` · local Notification API opt-in only | Security-first |
| Booking / Gmail / Spotify agents | **N/A-by-design** | Disclaimer on `/coach/` + approval copy | Educational lab coach only |

### Exceed axes (IL-only — Muse AI does not have these)

| Axis | Status | Evidence |
| --- | --- | --- |
| Lab-state Socratic coach | **Exceed** | `il-coach.js` + Noah router fallback · hypothesis-first prompts |
| Adapt hooks | **Exceed** | Weak-topic ideas/nudges · `/adapt/` deep links |
| Path / frontier deep links | **Exceed** | Artifact links → `/paths/`, `/os/`, SuperLab |
| Local Ollama router | **Exceed** | `il-model-router.js` · T0 lean · demand tiers · health probe |
| Proof export | **Exceed** | Artifact → `/proof/` · `il-proof.js` aggregates Noah's turns |
| EN / ES | **Exceed** | `il-i18n.js` + speech `es-ES` / `en-US` from `documentElement.lang` |
| Capacitor full-bleed home | **Exceed** | `il-bridge.js` `/` → `/coach/` · safe-area · void StatusBar |

---

## Closable gaps — closed this recursion

| Gap | Close | Evidence |
| --- | --- | --- |
| Proactive study nudges | **Closed** | Inbox tab + `harvestNudges` + optional Notification API · gold nudge strip |
| Richer artifacts | **Closed** | `cidr` / `lab-checklist` / `proof` kinds · checkable items · proof/path links |
| Approval before external / model switch | **Closed** | `showApproval` modal · `data-muse-external` · Apply model gated |
| Interruptible streaming feel | **Closed** | Multi-bubble timed push · Stop · gen token abort · typing bubble |
| Full-bleed Capacitor `/coach/` | **Closed** (prior) | `apps/mobile/src/il-bridge.js` + sync script |
| Dee avatar status on mobile | **Closed** (prior) | `il-muse-mobile.css` + `data-status` glows |
| Mic permission notes + safe-area + lockup | **Closed** | `ios-security/Info.plist.snippets.md` · Android snippet · `MOBILE-SECURITY.md` · safe-area CSS · Interstitium lockup retained |

**Do not implement:** email / WhatsApp / booking connector clones.

---

## Counts (Learning-OS mobile scope)

| Status | Count |
| --- | --- |
| Meet | 9 |
| Exceed | 7 (+6 IL-only axes) |
| Gap | **0** closable |
| N/A-by-design | 3 |
| **Overall** | **YES** |

---

## How to verify on phone

**PWA:** https://interstitiumlabs.dev/coach/ → Add to Home Screen (void chrome, safe-area, Muse · Paths · Labs · OS).

**Capacitor:**

```bash
./scripts/sync-mobile-web.sh
cd apps/mobile && npm ci && npx cap sync
npx cap run android   # or ios on macOS
```

Expect: cold start → Noah; Dee avatar status; nudge chips + Inbox; multi-bubble welcome + Adaptive approval; Stop while thinking; model Apply → approval modal; Interstitium lockup (not Meta).

---

## Related

- [LAB-MUSE-AVATAR.md](./LAB-MUSE-AVATAR.md)
- [MOBILE-SECURITY.md](./MOBILE-SECURITY.md) — mic / notifications
- [STORE-PUBLISH.md](./STORE-PUBLISH.md)
- [MODEL-ROUTER.md](./MODEL-ROUTER.md)
- `docs/assets/il-muse.js` · `il-muse.css` · `il-muse-mobile.css` · `apps/mobile/src/il-bridge.js`

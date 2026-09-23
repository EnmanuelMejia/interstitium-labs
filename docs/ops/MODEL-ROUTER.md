# Model router — Noah / Coach

Local-first OSS model routing for Interstitium Labs. **Prefer lean defaults. Scale relative to demand.**

## Files

| Asset | Role |
|-------|------|
| `/assets/il-model-catalog.json` | Backends, models, demand tiers T0–T2, P920/P1000 hardware profiles |
| `/assets/il-model-router.js` | Selection, health, chat fallback chain, policy (`il.model.router.v1`) |
| `/assets/il-model-analytics.js` | Latency / errors / thumbs → rolling scores → promote challenger; scale signals |
| `/assets/il-muse.js` | Muse UI: Model panel shows **current tier** + scale-when-demand-grows note |

## Demand tiers (lean → grow)

| Tier | Intent | Typical models on P920 + Quadro P1000 4GB |
|------|--------|-------------------------------------------|
| **T0 Lean** (default) | Solo lab / low concurrency | `local-rules` always; GPU ≤3B Q4/Q5; CPU 7B if needed |
| **T1 Standard** | Light concurrent seats | More CPU workers / 7B; same-origin lab-control proxy |
| **T2 Heavy** | Demand grew (latency/errors/concurrency) | Remote OSS proxies (Groq/Fireworks/Together/vLLM fleet) via **proxy only** |

Honesty: a P1000 4GB **cannot** run 70B. Router never claims otherwise.

## Browser config (no fake keys)

```js
// Optional — set on a private page or lab-control inject; never commit secrets
window.IL_MUSE = {
  endpoint: 'https://lab-control.example/v1', // OpenAI-compatible coach proxy
  ollamaEndpoint: 'http://127.0.0.1:11434'     // local only; do not expose publicly
};
```

Credentials for cloud OSS backends belong in **lab-control / Worker env**, not the static site.
Router stores optional base URL locally in `il.model.creds.v1` (operator-entered). Empty key is fine for Ollama.

## Policy knobs (`ILModelRouter.setPolicy`)

```js
ILModelRouter.setPolicy({
  mode: 'auto',              // or 'manual'
  primary: 'qwen2.5-coder-3b',
  challengers: ['phi-3-mini', 'qwen2.5-coder-7b'],
  demand_tier: 'T0',
  backend: 'ollama',
  healthy_only: true,
  min_samples: 8,
  win_rate_margin: 0.08
});
```

Auto mode: among **healthy** models allowed on the current demand tier, explore/challenger promote when analytics win-rate + latency thresholds clear.

## Fallback chain

1. Selected / primary (if healthy & tier-allowed)  
2. Challengers / same-tier catalog  
3. `local-rules` Socratic engine (`ILCoach.ask`) — **always** last resort  

## Analytics → switch

`ILModelAnalytics.record` / `logCompletion` / `thumb` feed rolling scores.  
`shouldPromote` / `recommendPrimary` can move `primary` after N samples.  
`scaleRecommendation` suggests T0→T1→T2 when demand signals rise — **does not auto-buy hardware**.

## Worker / edge stub

Same-origin Worker or lab-control `/api/coach` should:

1. Accept OpenAI-compatible `POST /v1/chat/completions`
2. Attach server-side API keys from env
3. Optionally inject lab state (namespace, failed pods) into the system prompt
4. Never reflect secrets to the browser

Document CSP `connect-src` for your lab-control origin when enabling remote backends.

## Ollama pull list (T0 lean on P920)

```bash
ollama pull qwen2.5-coder:3b
ollama pull phi3:mini
ollama pull llama3.2:3b
# CPU when GPU is saturated:
ollama pull qwen2.5-coder:7b-instruct-q4_K_M
```

See also: [SELF-HOST-PLAYGROUNDS-AND-LAB-LLM.md](./SELF-HOST-PLAYGROUNDS-AND-LAB-LLM.md).


## Admin / coach panel

| Asset | Role |
|-------|------|
| `/assets/il-model-panel.js` | Mount `data-il-model-panel` — primary switcher, auto-iterate, live scores, scale note |
| `/assets/il-model-panel.css` | Panel styles |

Wired on `/coach/`, `/admin/`, `/admin/insights/`. Muse Model tab uses the same router/analytics (lean↔T0 aliases).

## `IL_LLM_BASE` + tunnel

```bash
# lab-control env (server proxy preferred)
export IL_LLM_BASE=http://127.0.0.1:11434
```

```js
window.IL_LLM_BASE = 'http://127.0.0.1:11434';
// or Access-gated Cloudflare Tunnel hostname — never public :11434
```

```bash
cloudflared tunnel create il-llm
# ingress → authenticated reverse proxy → Ollama/llama.cpp
# Do not expose raw :11434 to the public Internet
```

**CORS:** Ollama lacks browser CORS by default. Prefer same-origin Worker `/api/llm/*`, or serve Learning OS from lab-control during local labs. Coach/admin CSP allows localhost LLM ports for workstation labs; production should stay on a same-origin proxy.

## Smoke test

```bash
node scripts/tests/model-router-scoring.test.js
```

## API surface

```js
IL_MODEL_ROUTER.selectModel({ task, forceId })
IL_MODEL_ROUTER.chat(messages, ctx)
IL_MODEL_ROUTER.healthCheck()
IL_MODEL_ROUTER.setPolicy({ mode, primary, challengers, demand_tier })
IL_MODEL_ROUTER.recommend()  // includes scale suggestion
```

Aliases: `ILModelRouter` (Muse), Muse tiers `lean|standard|heavy` ↔ catalog `T0|T1|T2`.

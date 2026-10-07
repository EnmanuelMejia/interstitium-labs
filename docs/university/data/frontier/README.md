# Frontier module pipeline — append contract

`il-23-frontier-knowledge.json` is designed for a daily pipeline that appends
new modules to `modules[]`. Rules:

1. **Append only.** New modules go at the END of `modules[]` (stable ids,
   progress keys `ilc:il-23-frontier-knowledge:module:<id>` must never shift).
2. **Module shape** (same as seed modules):
   `{ id, code:"IL-23", title, weight, asOf:"YYYY-MM-DD", summary,
      objectives[], notes[{title,body,code?,lang?}], cards[{front,back}],
      quiz[{q,choices[],answer (0-based),explain}] }`
   - `id`: `m23-<slug>` (unique, URL-safe).
   - `asOf`: the date the module's claims were verified. REQUIRED.
   - `weight`: 1 unless the pipeline has a documented reason otherwise.
3. **Content rules** (UNIFIED-STANDARD §5 + course honestyNote):
   - Original content only; no invented facts, quotes, credentials, metrics.
   - Separate durable mechanism-core from perishable edge in notes.
   - Frontier claims get explicit half-life framing; leadership/product claims
     must be re-verifiable, never stated as settled.
   - Every module's `sourceLinks`-worthy claims should be traceable; the
     pipeline maintains a per-module source note in its own run log
     (not in the course JSON).
4. **Quotas**: 3–5 quiz items, 4–6 cards, 2–4 notes per module (matches seeds).
5. **Validation**: after appending, run `python3 -c "import json;
   d=json.load(open('il-23-frontier-knowledge.json')); ..."` checks —
   ids unique, quiz answers in range, no empty titles/summaries — then
   `cd /tmp/verify && node verify.mjs` (0 console errors).
6. **Counts**: module appends change site totals; update the meta-copy counts
   in `docs/university/*.html` (academies/paths/modules) when modules are added.

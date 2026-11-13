/**
 * 2026-11-10 Musk-bar pass: seeded CKS paper variants (il-immersive-cks-paper.js v1.1.0 + il-immersive-3d.js v1.14.0).
 * Every paper seed re-draws each task's names (namespace, user, ServiceAccount, Secret, AppArmor profile, port, registry,
 * image tags) as a strict canonical↔variant SWAP at the terminal boundary. Pure: pool hygiene against the whole CLI/sim
 * corpus, the swap is an involution, every task is solvable by typing the variant commands for 40 seeds with nothing
 * canonical leaking into the shell, and a drill replay (typing the canonical names) does not pass.
 */
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

const require = createRequire(import.meta.url);
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const S = require(path.join(root, 'docs/assets/il-immersive-sims.js'));
globalThis.ILImmersiveSims = S;
const C = require(path.join(root, 'docs/assets/il-immersive-cli.js'));
require(path.join(root, 'docs/assets/il-immersive-troubleshoot.js'));
const K = require(path.join(root, 'docs/assets/il-immersive-cks-paper.js'));

const split = (h) => String(h).split(/\s{2}then\s{2}/);
const esc = (t) => t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
const word = (t) => new RegExp('(^|[^A-Za-z0-9_])' + esc(t) + '(?![A-Za-z0-9_])');
const corpus = readFileSync(path.join(root, 'docs/assets/il-immersive-cli.js'), 'utf8') + '\n' + readFileSync(path.join(root, 'docs/assets/il-immersive-sims.js'), 'utf8');
const SEEDS = Array.from({ length: 40 }, (_, i) => i + 1);

/** A terminal like the stage's: learner line → swap → rules engine; every printed line → swap. */
function terminal(inc, pairs) {
  const sw = K.swapper(pairs);
  let { state, ctx } = K.stage(C, S, { ...inc, cka: true });
  const printed = [];
  return {
    type(line) {
      const r = C.run(inc.simId, state, sw(line), ctx);
      if (r.set) state = S.merge(state, r.set);
      C.reconcile(inc.simId, state, ctx);
      r.out.forEach((ln) => printed.push(sw(ln)));
      return r;
    },
    status() { return C.taskStatus(inc.simId, inc.taskId, state, ctx); },
    printed
  };
}

test('v1.1.0 pools: every task has a VARY entry, pools are disjoint, never canonical, and never a word anywhere in the CLI packs or sims', () => {
  assert.match(K.VERSION, /^1\.[123]\.0$/, 'name variants since v1.1.0; v1.2.0 (2026-11-11) adds fault variants');
  assert.deepEqual(Object.keys(K.VARY).sort(), K.INCIDENTS.map((x) => x.id).sort());
  const canon = Object.keys(K.POOLS), seen = new Set();
  for (const [c, pool] of Object.entries(K.POOLS)) {
    assert.ok(pool.length >= 3, c + ' has a real pool');
    for (const v of pool) {
      assert.equal(seen.has(v), false, v + ' is in two pools'); seen.add(v);
      assert.equal(canon.includes(v), false, v + ' is canonical');
      assert.equal(word(v).test(corpus), false, v + ' already occurs in the rules engine — the swap would not be a bijection');
    }
  }
  const varied = K.INCIDENTS.filter((x) => K.VARY[x.id].length);
  assert.equal(varied.length, 21, '21 of 24 tasks vary; the 3 kube-bench tasks keep real CIS ids, ports and paths');
  for (const x of varied) {
    for (const t of K.VARY[x.id]) {
      assert.ok(K.POOLS[t], x.id + ' ' + t + ' has a pool');
      const tk = C.task(x.simId, x.taskId);
      const where = x.ticket + '\n' + tk.steps.map((s) => s.hint).join('\n');
      assert.ok(word(t).test(where), x.id + ': ' + t + ' is not a no-op (appears in the ticket or the commands)');
    }
  }
});

test('swapper: whole-word, involution, longest token first; identity without pairs', () => {
  const sw = K.swapper([['payments', 'ledger'], ['registry.example.com', 'cr.acme.internal'], ['2.4.1', '3.0.4'], ['8080', '7070']]);
  assert.equal(sw('kubectl -n payments get deploy payments-api'), 'kubectl -n ledger get deploy ledger-api');
  assert.equal(sw('registry.example.com/payments/api:2.4.1'), 'cr.acme.internal/ledger/api:3.0.4');
  assert.equal(sw('system:serviceaccount:payments:api-sa port 8080/TCP'), 'system:serviceaccount:ledger:api-sa port 7070/TCP');
  assert.equal(sw('paymentsX 12.4.1 80800 ledger'), 'paymentsX 12.4.1 80800 payments');
  for (const s of ['a payments b', 'cr.acme.internal x registry.example.com', 'ledger-api:3.0.4']) assert.equal(sw(sw(s)), s);
  assert.equal(K.swapper([])('payments'), 'payments');
  assert.equal(K.swapper(null)('x'), 'x');
});

test('variantFor: deterministic per (seed, task), independent of the task draw, and actually varies across seeds', () => {
  for (const x of K.INCIDENTS) {
    assert.deepEqual(K.variantFor(x.id, 9), K.variantFor(x.id, 9));
    if (!K.VARY[x.id].length) { assert.deepEqual(K.variantFor(x.id, 9).pairs, []); continue; }
    const labels = new Set(SEEDS.map((s) => K.variantFor(x.id, s).label));
    assert.ok(labels.size >= 3, x.id + ' gets ' + labels.size + ' distinct variants over 40 seeds');
    for (const s of SEEDS) K.variantFor(x.id, s).pairs.forEach(([c, v]) => assert.ok(K.POOLS[c].includes(v)));
  }
  for (const seed of SEEDS) {
    const on = K.buildPaper(C, { seed, count: 12 }), off = K.buildPaper(C, { seed, count: 12, variants: false });
    assert.deepEqual(on.incidents.map((i) => i.id), off.incidents.map((i) => i.id), 'variants do not change which tasks are drawn');
    assert.equal(on.variants, true); assert.equal(off.variants, false);
    assert.ok(off.incidents.every((i) => i.variant === null && i.ticket === K.get(i.id).ticket));
  }
});

test('buildPaper: tickets and titles speak the variant names — no canonical varied token survives', () => {
  for (const seed of SEEDS) {
    for (const inc of K.buildPaper(C, { seed, count: 18 }).incidents) {
      if (!inc.variant) { assert.deepEqual(K.VARY[inc.id], []); continue; }
      for (const [c, v] of inc.variant.pairs) {
        assert.equal(word(c).test(inc.ticket), false, inc.id + ' ticket leaks ' + c + ' (seed ' + seed + ')');
        assert.equal(word(c).test(inc.title), false, inc.id + ' title leaks ' + c);
        if (word(c).test(K.get(inc.id).ticket)) assert.ok(word(v).test(inc.ticket), inc.id + ' ticket names ' + v);
      }
    }
  }
});

test('every varied task is solvable at 100% by typing the variant commands (40 seeds), and the shell never prints a canonical name', () => {
  for (const x of K.INCIDENTS) {
    const tk = C.task(x.simId, x.taskId);
    const files = Object.keys((C.pack(x.simId) || {}).files || {});
    for (const seed of K.VARY[x.id].length ? SEEDS : [1]) {
      const v = K.variantFor(x.id, seed), sw = K.swapper(v.pairs);
      const term = terminal(x, v.pairs);
      for (const st of tk.steps) for (const cmd of split(st.hint)) term.type(sw(cmd));
      const status = term.status();
      assert.equal(status.done, true, x.id + ' seed ' + seed + ' (' + v.label + ')');
      const inc = { ...x, cka: true, steps: tk.steps.length, variant: v.pairs.length ? v : null };
      assert.equal(K.gradeIncident(inc, status, [], { cmds: 9 }).pct, 100);
      /* lab files and help speak the variant too */
      term.type('help'); term.type('ls');
      files.forEach((f) => term.type('cat ' + sw(f)));
      const out = term.printed.join('\n');
      for (const [c] of v.pairs) assert.equal(word(c).test(out), false, x.id + ' seed ' + seed + ': shell output leaks canonical ' + c);
    }
  }
});

test('a drill replay does not pass: typing the free-play names into a varied paper leaves the task unresolved', () => {
  let checked = 0;
  for (const x of K.INCIDENTS) {
    if (!K.VARY[x.id].length) continue;
    const tk = C.task(x.simId, x.taskId);
    const v = K.variantFor(x.id, 4);
    const usesName = tk.steps.some((st) => v.pairs.some(([c]) => word(c).test(st.hint)));
    if (!usesName) continue;
    const term = terminal(x, v.pairs);
    for (const st of tk.steps) for (const cmd of split(st.hint)) term.type(cmd); /* canonical = the replay */
    assert.equal(term.status().done, false, x.id + ': the canonical replay must not resolve a ' + v.label + ' paper');
    checked += 1;
  }
  assert.ok(checked >= 18, 'replay checked on ' + checked + ' tasks');
});

test('results screen: hinted / missed checkpoints show this paper\'s commands, not the drill\'s', () => {
  const p = K.buildPaper(C, { seed: 21, count: 6 });
  for (const inc of p.incidents) {
    if (!inc.variant) continue;
    inc.result = K.gradeIncident(inc, null, [], { skipped: true });
    assert.equal(inc.result.variant, inc.variant.label);
    for (const n of inc.result.notes) for (const [c] of inc.variant.pairs) {
      assert.equal(word(c).test(n.cmd || ''), false, inc.id + ' note cmd leaks ' + c);
      assert.equal(word(c).test(n.label), false, inc.id + ' note label leaks ' + c);
    }
  }
  assert.match(p.honesty, /re-drawn per paper seed/);
});

test('wiring: player v1.14.0 swaps the CLI boundary, boot passes cliExam.swap, page has the variants toggle, manifest + docs', () => {
  const player = readFileSync(path.join(root, 'docs/assets/il-immersive-3d.js'), 'utf8');
  assert.match(player, /version: '1\.1[45]\.0'/);
  assert.match(player, /cliExamVariants: true/);
  assert.match(player, /function makeSwap\(pairs\)/);
  assert.match(player, /swapFn && !this\._cliReplaying \? this\.cfg\.cliExam\.swapFn\(raw\) : raw/);
  assert.match(player, /kind === 'cmd' \? String\(ln\) : String\(self\._swapText\(ln\)\)/);
  const boot = readFileSync(path.join(root, 'docs/assets/il-immersive-troubleshoot-boot.js'), 'utf8');
  assert.match(boot, /swap: inc\.variant \? inc\.variant\.pairs : null/);
  assert.match(boot, /variants=0/);
  const page = readFileSync(path.join(root, 'docs/immersive/cks/index.html'), 'utf8');
  assert.match(page, /data-il-ts-variants checked/);
  assert.match(page, /surface variants over the same staged fault/);
  const m = JSON.parse(readFileSync(path.join(root, 'docs/assets/scenes/manifest.json'), 'utf8'));
  assert.equal(m.cks_paper.variants.version, '1.1.0');
  assert.equal(m.cks_paper.variants.varied_tasks, 21);
  assert.match(readFileSync(path.join(root, 'docs/ops/MUSK-BAR-RECURSIVE.md'), 'utf8'), /2026-11-10/);
});

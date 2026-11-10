/**
 * 2026-11-09 Musk-bar pass: hands-on CKS paper (il-immersive-cks-paper.js v1.0.0) + the CKS review queue
 * (il-immersive-review.js v1.4.0 queue({ track: 'CKS' })). Pure: bank, domain coverage, ticket hygiene, staging,
 * every task solvable by typing, blueprint-weighted scoring, weakest-domain ranking, history, remediation.
 */
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { createRequire } from 'node:module';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

const require = createRequire(import.meta.url);
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const S = require(path.join(root, 'docs/assets/il-immersive-sims.js'));
globalThis.ILImmersiveSims = S;
const C = require(path.join(root, 'docs/assets/il-immersive-cli.js'));
const E = require(path.join(root, 'docs/assets/il-immersive-exam.js'));
const T = require(path.join(root, 'docs/assets/il-immersive-troubleshoot.js'));
const K = require(path.join(root, 'docs/assets/il-immersive-cks-paper.js'));
const R = require(path.join(root, 'docs/assets/il-immersive-review.js'));

const split = (h) => String(h).split(/\s{2}then\s{2}/);
function play(inc, { upto = Infinity, hintAt = [] } = {}) {
  let { state, ctx } = K.stage(C, S, inc);
  const tk = C.task(inc.simId, inc.taskId);
  const hinted = [];
  for (let i = inc.pre, n = 0; i < tk.steps.length && n < upto; i++, n++) {
    if (hintAt.includes(n)) {
      const c = C.coach(inc.simId, inc.taskId, state, ctx, { count: false, level: 'hint' });
      assert.equal(c.step, i);
      hinted.push(c.step);
    }
    for (const cmd of split(tk.steps[i].hint)) {
      const r = C.run(inc.simId, state, cmd, ctx);
      if (r.set) state = S.merge(state, r.set);
      C.reconcile(inc.simId, state, ctx);
    }
  }
  return { status: C.taskStatus(inc.simId, inc.taskId, state, ctx), hinted };
}
const idx = (html) => readFileSync(path.join(root, 'docs/immersive/index.html'), 'utf8').includes(html);

test('v1.0.0 bank: 24 typed CKS tasks across all six CNCF CKS domains, each on a real CLI task over an authored .glb', () => {
  assert.equal(K.VERSION, '1.0.0');
  const b = K.bank(C);
  assert.equal(b.length, 24);
  assert.equal(new Set(b.map(x => x.id)).size, 24);
  assert.equal(new Set(b.map(x => x.simId + ':' + x.taskId)).size, 24, 'no task twice');
  assert.deepEqual([...new Set(b.map(x => x.area))].sort(), [...K.AREA_ORDER].sort());
  const per = {}; b.forEach(x => { per[x.area] = (per[x.area] || 0) + 1; });
  assert.deepEqual(per, { setup: 5, hardening: 3, system: 1, microservice: 5, supply: 7, runtime: 3 });
  for (const x of b) {
    const tk = C.task(x.simId, x.taskId);
    assert.ok(tk && x.pre === 0 && tk.steps.length >= 4, x.id);
    assert.ok(existsSync(path.join(root, 'docs', S.get(x.simId).glb)), x.id + ' authored glb');
    assert.ok(idx('id="' + K.ANCHOR[x.simId] + '"'), x.id + ' drill anchor on /immersive/');
  }
  /* every sim's CKS packs are in the bank: the 21 CKS-pack tasks + 3 shared RBAC/NetworkPolicy tasks */
  const cksTasks = C.list().filter(id => /^cks-/.test(id)).reduce((n, id) => n + C.pack(id).tasks.length, 0);
  assert.equal(cksTasks, 21);
  assert.equal(b.filter(x => /^cks-/.test(x.simId)).length, 21);
});

test('domains and weights are the CNCF CKS blueprint used by the predict paper (ILImmersiveExam.CKS_BLUEPRINT)', () => {
  const bp = {}; E.CKS_BLUEPRINT.forEach(b => { bp[b.domain] = b.weight; });
  const mine = {}; K.AREA_ORDER.forEach(k => { mine[K.AREAS[k].domain] = K.AREAS[k].weight; });
  assert.deepEqual(mine, bp);
  assert.equal(Object.values(mine).reduce((a, b) => a + b, 0), 100);
  for (const k of K.AREA_ORDER) assert.ok(idx('id="' + K.AREAS[k].anchor + '"'), k);
});

test('tickets are task statements: names, files and what to prove — never a command or a step label', () => {
  for (const x of K.INCIDENTS) {
    const tk = C.task(x.simId, x.taskId);
    assert.ok(x.ticket.length > 80, x.id);
    tk.steps.forEach((st) => {
      for (const cmd of split(st.hint)) assert.equal(x.ticket.includes(cmd), false, x.id + ' leaks ' + cmd);
      assert.equal(x.ticket.includes(st.label), false, x.id + ' leaks a step label');
    });
    assert.doesNotMatch(x.ticket, /sed -i|kubectl |systemctl |apparmor_parser|--exit-code|chmod 700|enabled: true|--profiling=false|readOnlyPort: 0/, x.id);
  }
});

test('every task is solvable by typing its pack commands from the staged state (100%, resolved); staging verifies nothing', () => {
  for (const x of K.INCIDENTS) {
    const inc = { ...x, cka: true, steps: C.task(x.simId, x.taskId).steps.length };
    const { state, ctx } = K.stage(C, S, inc);
    assert.equal(C.taskStatus(x.simId, x.taskId, state, ctx).completed, 0, x.id + ' starts at 0');
    const { status } = play(inc);
    const r = K.gradeIncident(inc, status, [], { cmds: 9, ms: 1000 });
    assert.equal(r.pct, 100, x.id + ' ' + r.feedback);
    assert.equal(r.resolved, true, x.id);
  }
});

test('buildPaper: deterministic per seed; 6 tasks touch all six domains; 3 tasks land on the three 20% domains; 1..18 clamp', () => {
  const a = K.buildPaper(C, { seed: 7, now: 0 }), b = K.buildPaper(C, { seed: 7, now: 0 });
  assert.deepEqual(a.incidents.map(i => i.id), b.incidents.map(i => i.id));
  assert.equal(a.kind, 'cks'); assert.equal(a.minutes, 36); assert.equal(a.passPct, 67); assert.equal(a.endsAt, 36 * 60000);
  for (let seed = 1; seed <= 40; seed++) {
    const p6 = K.buildPaper(C, { seed, count: 6 });
    assert.equal(new Set(p6.incidents.map(i => i.area)).size, 6, 'seed ' + seed);
    const p3 = K.buildPaper(C, { seed, count: 3 });
    assert.deepEqual(p3.incidents.map(i => i.area).sort(), ['microservice', 'runtime', 'supply'], 'seed ' + seed);
    const p12 = K.buildPaper(C, { seed, count: 12 });
    assert.equal(new Set(p12.incidents.map(i => i.id)).size, 12);
  }
  assert.equal(K.buildPaper(C, { seed: 1, count: 99 }).incidents.length, 18);
  assert.match(a.incidents[0].areaLabel, / · (10|15|20)%$/);
  assert.match(a.honesty, /SIMULATED shell[\s\S]*not the CNCF CKS/);
});

test('summarize: CKS-weighted score over tested domains, unweighted mean alongside, weakest by points at stake, drill link to the worst task', () => {
  const p = K.buildPaper(C, { seed: 3, count: 6 });
  const byArea = {}; p.incidents.forEach(i => { byArea[i.area] = i; });
  const grade = (inc, frac) => {
    const steps = C.task(inc.simId, inc.taskId).steps.length;
    const upto = Math.round(steps * frac);
    const { status } = play(inc, { upto });
    inc.result = K.gradeIncident(inc, status, [], { cmds: upto });
    return inc.result.pct;
  };
  const pct = {};
  pct.setup = grade(byArea.setup, 1); pct.hardening = grade(byArea.hardening, 1); pct.system = grade(byArea.system, 0);
  pct.microservice = grade(byArea.microservice, 1); pct.supply = grade(byArea.supply, 0.5); pct.runtime = grade(byArea.runtime, 1);
  const sum = K.summarize(p);
  const w = { setup: 15, hardening: 15, system: 10, microservice: 20, supply: 20, runtime: 20 };
  const want = Math.round(Object.keys(w).reduce((a, k) => a + w[k] * pct[k], 0) / 100);
  assert.equal(sum.pct, want);
  assert.equal(sum.coveragePct, 100); assert.deepEqual(sum.untested, []);
  assert.equal(sum.rawPct, Math.round(Object.values(pct).reduce((a, b) => a + b, 0) / 6));
  /* system 10% at 0% → 10 points at stake; supply 20% at ~50% → ~10 — the rank is weight × loss, ties by checkpoints lost */
  const sys = sum.areas.find(a => a.area === 'system'), sup = sum.areas.find(a => a.area === 'supply');
  assert.equal(sys.atStake, 10);
  assert.equal(sum.weakest.area, sup.atStake > sys.atStake || (sup.atStake === sys.atStake && sup.lost > sys.lost) ? 'supply' : 'system');
  assert.equal(sum.weakest.href, '/immersive/#' + K.ANCHOR[byArea[sum.weakest.area].simId]);
  assert.equal(sum.passed, sum.pct >= 67);
  assert.match(K.ui.summary(sum), /^CKS score: \d+% \(weighted by the CNCF CKS domain weights over the 100% of the blueprint/);
  assert.match(K.ui.blueprint(sum), /all six domains/);
});

test('summarize: an untested domain is never counted as passed — coverage shrinks and the weights renormalise', () => {
  const p = K.buildPaper(C, { seed: 11, count: 3 });
  p.incidents.forEach(inc => { inc.result = K.gradeIncident(inc, play(inc).status, [], { cmds: 5 }); });
  const sum = K.summarize(p);
  assert.equal(sum.pct, 100); assert.equal(sum.coveragePct, 60);
  assert.deepEqual(sum.untested, ['Cluster Setup', 'Cluster Hardening', 'System Hardening']);
  assert.equal(sum.weakest, null);
  assert.match(K.ui.blueprint(sum), /60% of the exam weight was tested \(not on this paper: Cluster Setup, Cluster Hardening, System Hardening\)/);
  const none = K.summarize(K.buildPaper(C, { seed: 11, count: 2 }));
  assert.equal(none.pct, 0); assert.equal(none.passed, false); assert.equal(none.resolved, 0);
});

test('history + remediation: attempts stay on device; first gap per task becomes a cks-paper CLI card; CKS review queue serves only CKS cards', () => {
  const store = {};
  globalThis.localStorage = { getItem: k => (k in store ? store[k] : null), setItem: (k, v) => { store[k] = String(v); }, removeItem: k => { delete store[k]; } };
  try {
    R.reset();
    const p = K.buildPaper(C, { seed: 5, count: 3 });
    p.incidents.forEach((inc, i) => { inc.result = K.gradeIncident(inc, play(inc, { upto: i === 0 ? Infinity : 1, hintAt: i === 1 ? [0] : [] }).status, i === 1 ? [0] : [], { cmds: 2 }); });
    const sum = K.summarize(p);
    K.recordAttempt(p, sum);
    assert.equal(K.loadStore().last.pct, sum.pct);
    assert.match(K.ui.history(K.loadStore().last), /^Last CKS paper on this device: \d+% \(CKS-weighted, 60% of the blueprint tested\)/);
    const rem = K.remediate(p, R);
    assert.equal(rem.queued, 2);
    const cards = Object.values(R.load().cards).filter(c => c.kind === 'cli');
    assert.equal(cards.length, 2);
    assert.ok(cards.every(c => c.src['cks-paper'] === 1));
    /* a CKA CLI card on the same device must not leak into the CKS queue */
    R.recordCli({ simId: 'node-troubleshoot', taskId: 'runtime-down', step: 1, how: 'solution' });
    const cks = R.queue(S, { C, track: 'CKS', limit: 10 });
    assert.equal(cks.length, 2);
    assert.ok(cks.every(x => x.kind === 'cli' && x.cks === true));
    const all = R.queue(S, { C, limit: 10 });
    assert.ok(all.some(x => x.simId === 'node-troubleshoot'));
    assert.equal(R.cksDue(S, C), 2);
    assert.equal(R.queue(S, { C, track: 'CKS' }).filter(x => x.reason !== 'relearn' && x.reason !== 'due').length, 0, 'no CKA top-ups in the CKS queue');
  } finally { R.reset(); delete globalThis.localStorage; }
});

test('wiring: /immersive/cks/ page, shared boot reads ILCksPaper, nav + section links, manifest, sitemap', () => {
  const page = readFileSync(path.join(root, 'docs/immersive/cks/index.html'), 'utf8');
  assert.match(page, /data-il-ts-module="ILCksPaper"/);
  for (const s of ['il-immersive-troubleshoot.js', 'il-immersive-cks-paper.js', 'il-immersive-3d.js', 'il-immersive-troubleshoot-boot.js']) assert.ok(page.includes('/assets/' + s), s);
  assert.ok(page.indexOf('il-immersive-troubleshoot.js') < page.indexOf('il-immersive-cks-paper.js'), 'grading rules load first');
  assert.match(page, /not killer\.sh/);
  assert.match(readFileSync(path.join(root, 'docs/assets/il-immersive-troubleshoot-boot.js'), 'utf8'), /data-il-ts-module/);
  assert.ok(idx('href="/immersive/cks/"'));
  assert.match(readFileSync(path.join(root, 'docs/immersive/exam/index.html'), 'utf8'), /href="\/immersive\/cks\/"/);
  assert.match(readFileSync(path.join(root, 'docs/immersive/review/index.html'), 'utf8'), /data-il-review-start-cks/);
  const m = JSON.parse(readFileSync(path.join(root, 'docs/assets/scenes/manifest.json'), 'utf8'));
  assert.equal(m.cks_paper.page, '/immersive/cks/');
  assert.equal(m.cks_paper.tasks, 24);
  assert.match(readFileSync(path.join(root, 'docs/sitemap.xml'), 'utf8'), /immersive\/cks\//);
});

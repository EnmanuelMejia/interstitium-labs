/**
 * 2026-10-28 Musk-bar pass: hands-on mixed-incident Troubleshooting exam paper (il-immersive-troubleshoot.js v1.0.0).
 * Pure: the bank, paper builder, incident staging (silent replay of `pre` steps), partial-credit grading, area /
 * weakest-area summary, CKA Troubleshooting blueprint view, on-device history and review-card remediation.
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

const split = (h) => String(h).split(/\s{2}then\s{2}/);
/** Stage an incident, then type each learner step's own command (optionally only the first `upto` learner steps). */
function play(inc, { upto = Infinity, hintAt = [] } = {}) {
  let { state, ctx } = T.stage(C, S, inc);
  const tk = C.task(inc.simId, inc.taskId);
  const hinted = [];
  for (let i = inc.pre, n = 0; i < tk.steps.length && n < upto; i++, n++) {
    if (hintAt.includes(n)) {
      const c = C.coach(inc.simId, inc.taskId, state, ctx, { count: false, level: 'hint' });
      assert.equal(c.step, i, 'hint targets the next unverified checkpoint');
      hinted.push(c.step);
    }
    for (const cmd of split(tk.steps[i].hint)) {
      const r = C.run(inc.simId, state, cmd, ctx);
      if (r.set) state = S.merge(state, r.set);
      C.reconcile(inc.simId, state, ctx);
    }
  }
  return { status: C.taskStatus(inc.simId, inc.taskId, state, ctx), hinted, ctx };
}
const full = (id) => ({ ...T.get(id), cka: T.AREAS[T.get(id).area].cka, steps: C.task(T.get(id).simId, T.get(id).taskId).steps.length });

test('v1.0.0 bank: 14 CKA incidents in 4 areas + 2 opt-in mesh incidents, every one maps to a real CLI task on an authored .glb', () => {
  assert.equal(T.VERSION, '1.0.0');
  const cka = T.bank(C, {}), all = T.bank(C, { mesh: true });
  assert.equal(cka.length, 14);
  assert.equal(all.length, 16);
  assert.deepEqual([...new Set(cka.map(x => x.area))].sort(), ['components', 'network', 'nodes', 'services']);
  assert.ok(cka.every(x => T.AREAS[x.area].cka) && all.filter(x => !T.AREAS[x.area].cka).every(x => x.area === 'mesh'));
  for (const x of all) {
    const tk = C.task(x.simId, x.taskId);
    assert.ok(tk, x.id + ' task exists');
    assert.ok(x.pre >= 0 && x.pre < tk.steps.length - 1, x.id + ' leaves ≥2 learner checkpoints');
    const glb = S.get(x.simId).glb;
    assert.ok(existsSync(path.join(root, 'docs', glb)), x.id + ' anchors to authored ' + glb);
    assert.ok(new RegExp('id="' + T.AREAS[x.area].anchor + '"').test(readFileSync(path.join(root, 'docs/immersive/index.html'), 'utf8')), x.area + ' drill anchor exists');
  }
});

test('tickets describe symptoms, never the fix: no step command or step label leaks into a ticket', () => {
  for (const x of T.INCIDENTS) {
    const tk = C.task(x.simId, x.taskId);
    assert.ok(x.ticket.length > 60, x.id);
    tk.steps.slice(x.pre).forEach((st) => {
      for (const cmd of split(st.hint)) assert.equal(x.ticket.includes(cmd), false, x.id + ' leaks ' + cmd);
      assert.equal(x.ticket.includes(st.label), false, x.id + ' leaks a step label');
    });
    assert.doesNotMatch(x.ticket, /daemon-reload|rmi --prune|forwrd|targetPort|istio-injection=enabled|kubeadm init phase|ippool|--replicas=1/, x.id);
  }
});

test('stage(): setup state + silent replay of `pre` steps — those are verified, history is wiped, learner steps are not', () => {
  for (const x of T.INCIDENTS) {
    const { state, ctx } = T.stage(C, S, x);
    const st = C.taskStatus(x.simId, x.taskId, state, ctx);
    assert.equal(st.completed, x.pre, x.id + ' pre steps verified, nothing more');
    assert.deepEqual(ctx.history, [], x.id + ' `history` cannot reveal the replayed break');
  }
  const api = T.get('cp-api-down');
  const { state } = T.stage(C, S, api);
  assert.equal(state.apiUp, false, 'the API server really is down when the learner gets the shell');
});

test('every incident is solvable from its staged state with the pack’s own commands → 100%, resolved', () => {
  for (const x of T.bank(C, { mesh: true })) {
    const inc = full(x.id);
    const { status } = play(inc);
    const r = T.gradeIncident(inc, status, []);
    assert.equal(r.resolved, true, x.id);
    assert.equal(r.pct, 100, x.id);
    assert.equal(r.total, status.total - inc.pre);
    assert.match(r.feedback, /^Resolved: all \d+ checkpoints verified without help\.$/);
  }
});

test('partial credit: verified checkpoints count, a hint halves its checkpoint, the first gap names the next step + command', () => {
  const inc = full('node-kubelet-203');
  const half = play(inc, { upto: 4 });
  const r = T.gradeIncident(inc, half.status, []);
  assert.equal(r.total, 8); assert.equal(r.verified, 4); assert.equal(r.pct, 50); assert.equal(r.resolved, false);
  assert.equal(r.firstMiss, 4);
  assert.equal(r.notes[0].how, 'missed');
  assert.match(r.notes[0].label, /ExecStart/);
  assert.match(r.notes[0].cmd, /sed -i/);
  assert.match(r.feedback, /^Stalled after 4\/8 checkpoints\. Next checkpoint: Point ExecStart/);
  const hinted = play(inc, { hintAt: [0, 5] });
  const h = T.gradeIncident(inc, hinted.status, hinted.hinted);
  assert.equal(h.resolved, true);
  assert.equal(h.credit, 7);
  assert.equal(h.pct, 88);
  assert.equal(h.hints, 2);
  assert.match(h.feedback, /Resolved with 2 hints \(88% credit\)/);
  assert.deepEqual(h.notes.map(n => n.how), ['hinted', 'hinted']);
  const none = T.gradeIncident(inc, null, [], { skipped: true });
  assert.equal(none.total, 8, 'unstaged incidents still count their checkpoints'); assert.equal(none.pct, 0);
  assert.match(none.feedback, /^Skipped — 0\/8 checkpoints\./);
});

test('pre-broken control-plane incident: only learner checkpoints are graded (pre steps are not free credit)', () => {
  const inc = full('cp-pending');
  const s0 = T.stage(C, S, inc);
  const r0 = T.gradeIncident(inc, C.taskStatus(inc.simId, inc.taskId, s0.state, s0.ctx), []);
  assert.equal(r0.total, 3); assert.equal(r0.verified, 0); assert.equal(r0.pct, 0);
});

test('buildPaper: deterministic per seed, round-robins areas (4+ incidents cover all 4), mesh only when opted in, timed', () => {
  const a = T.buildPaper(C, { count: 5, minutes: 30, seed: 7, now: 1000 });
  const b = T.buildPaper(C, { count: 5, minutes: 30, seed: 7, now: 1000 });
  assert.deepEqual(a.incidents.map(i => i.id), b.incidents.map(i => i.id));
  assert.equal(a.incidents.length, 5);
  assert.equal(new Set(a.incidents.map(i => i.area)).size, 4);
  assert.equal(new Set(a.incidents.map(i => i.id)).size, 5, 'no duplicates');
  assert.ok(a.incidents.every(i => i.cka));
  assert.equal(a.endsAt - a.startedAt, 30 * 60 * 1000);
  assert.match(a.honesty, /SIMULATED shell/); assert.match(a.honesty, /not a live cluster/i); assert.match(a.honesty, /not killer\.sh/);
  const q = T.buildPaper(C, { count: 3, seed: 11 });
  assert.equal(new Set(q.incidents.map(i => i.area)).size, 3, 'quick paper = 3 distinct areas');
  const m = T.buildPaper(C, { count: 3, seed: 11, mesh: true });
  assert.equal(m.incidents.length, 4);
  assert.equal(m.incidents[3].area, 'mesh'); assert.equal(m.incidents[3].cka, false);
  const seeds = new Set();
  for (let s = 1; s <= 30; s++) seeds.add(T.buildPaper(C, { count: 5, seed: s }).incidents.map(i => i.id).join());
  assert.ok(seeds.size > 10, 'papers vary by seed (' + seeds.size + ')');
});

test('summarize: CKA % over CKA incidents only, per-area table, weakest area by credit then checkpoints lost, Troubleshooting blueprint at 30%', () => {
  const paper = T.buildPaper(C, { count: 4, seed: 3, mesh: true });
  const [i0, i1, i2, i3, mesh] = paper.incidents;
  i0.result = T.gradeIncident(i0, play(i0).status, []);
  i1.result = T.gradeIncident(i1, play(i1, { upto: 1 }).status, []);
  const p2 = play(i2, { hintAt: [0] }); i2.result = T.gradeIncident(i2, p2.status, p2.hinted);
  /* i3 never touched → result null; mesh resolved */
  mesh.result = T.gradeIncident(mesh, play(mesh).status, []);
  const s = T.summarize(paper, E);
  assert.equal(s.ckaIncidents, 4);
  const expect = Math.round(((1 + 1 / i1.result.total + i2.result.credit / i2.result.total + 0) / 4) * 100);
  assert.equal(s.pct, expect);
  assert.equal(s.passed, s.pct >= 66);
  assert.equal(s.resolved, 3, 'i0, i2, mesh');
  assert.deepEqual(s.mesh, { pct: 100, resolved: true });
  assert.equal(s.areas.length, 5);
  assert.equal(s.areas.find(a => a.area === 'mesh').cka, false);
  assert.equal(s.weakest.area, i3.area, 'the untouched incident\'s area is weakest');
  assert.match(s.weakest.href, /^\/immersive\/#cka-/);
  assert.equal(s.blueprint.domain, 'Troubleshooting'); assert.equal(s.blueprint.weight, 30);
  assert.equal(s.blueprint.pct, s.pct);
  assert.equal(s.blueprint.atStake, Math.round(30 * (100 - s.pct)) / 100);
  assert.match(s.blueprint.honesty, /not a predicted CNCF exam score/);
  const clean = T.buildPaper(C, { count: 2, seed: 5 });
  clean.incidents.forEach(i => { i.result = T.gradeIncident(i, play(i).status, []); });
  const cs = T.summarize(clean, E);
  assert.equal(cs.pct, 100); assert.equal(cs.weakest, null); assert.equal(cs.passed, true);
});

test('history stays on device; remediation turns each incident’s first gap into a CLI review card', () => {
  const store = {};
  globalThis.localStorage = { getItem: k => (k in store ? store[k] : null), setItem: (k, v) => { store[k] = String(v); } };
  const paper = T.buildPaper(C, { count: 3, seed: 9 });
  paper.incidents[0].result = T.gradeIncident(paper.incidents[0], play(paper.incidents[0]).status, []);
  paper.incidents[1].result = T.gradeIncident(paper.incidents[1], play(paper.incidents[1], { upto: 2 }).status, []);
  const s = T.summarize(paper, E);
  const db = T.recordAttempt(paper, s);
  assert.equal(db.last.incidents, 3); assert.equal(db.last.resolved, 1); assert.equal(db.last.pct, s.pct);
  assert.ok(JSON.parse(store[T.STORE_KEY]).attempts.length === 1);
  const calls = [];
  const out = T.remediate(paper, { recordCli: (o) => { calls.push(o); return {}; } });
  assert.equal(out.queued, 1, 'resolved incident queues nothing; unreached incident has no step notes');
  assert.equal(calls[0].taskId, paper.incidents[1].taskId);
  assert.equal(calls[0].step, paper.incidents[1].pre + 2);
  assert.equal(calls[0].how, 'exam-miss');
  assert.deepEqual(T.remediate(paper, null), { queued: 0, cards: [] });
  delete globalThis.localStorage;
});

test('page + assets: relative offline load, graded CLI stage, honesty copy, linked from /immersive/, the CKA exam and the sitemap', () => {
  const html = readFileSync(path.join(root, 'docs/immersive/troubleshoot/index.html'), 'utf8');
  for (const f of ['il-immersive-sims.js', 'il-immersive-cli.js', 'il-immersive-exam.js', 'il-immersive-review.js', 'il-immersive-troubleshoot.js', 'il-immersive-3d.js', 'il-immersive-troubleshoot-boot.js'])
    assert.ok(html.includes('src="/assets/' + f + '"'), f);
  assert.ok(html.indexOf('il-immersive-cli.js') < html.indexOf('il-immersive-3d.js'), 'CLI packs load before the player');
  assert.equal(html.includes('https://interstitiumlabs.dev/assets/'), false);
  assert.match(html, /simulated shell/i); assert.match(html, /not<\/strong> a live cluster, not killer\.sh/);
  assert.match(html, /data-il-ts-start data-count="5" data-minutes="30"/);
  assert.match(html, /data-il-ts-mesh/);
  assert.doesNotMatch(html, /Unreal|Pixel Streaming/, 'no engine claims on this page');
  assert.match(readFileSync(path.join(root, 'docs/immersive/index.html'), 'utf8'), /href="\/immersive\/troubleshoot\/"/);
  assert.match(readFileSync(path.join(root, 'docs/immersive/exam/index.html'), 'utf8'), /href="\/immersive\/troubleshoot\/"/);
  assert.match(readFileSync(path.join(root, 'docs/sitemap.xml'), 'utf8'), /immersive\/troubleshoot\//);
  const p3d = readFileSync(path.join(root, 'docs/assets/il-immersive-3d.js'), 'utf8');
  assert.match(p3d, /cfg\.cliExam = j && j\.exam && j\.cliExam/);
  assert.match(p3d, /solution is off during the paper/);
});

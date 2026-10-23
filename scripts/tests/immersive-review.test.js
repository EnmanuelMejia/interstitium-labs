/**
 * Adaptive remediation loop tests (2026-10-13): ILImmersiveReview scheduler + exam focus.
 * Pure: no browser. Loads il-immersive-sims.js, il-immersive-exam.js, il-immersive-review.js via vm
 * into ONE sandbox so they share an in-memory localStorage.
 */
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import vm from 'node:vm';
import test from 'node:test';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
function sandbox() {
  const sb = { console, localStorage: {
    _d: {},
    getItem(k) { return Object.prototype.hasOwnProperty.call(this._d, k) ? this._d[k] : null; },
    setItem(k, v) { this._d[k] = String(v); },
    removeItem(k) { delete this._d[k]; }
  } };
  sb.globalThis = sb; sb.window = sb;
  for (const f of ['il-immersive-sims.js', 'il-immersive-exam.js', 'il-immersive-review.js']) {
    vm.runInNewContext(readFileSync(path.join(root, 'docs/assets', f), 'utf8'), sb, { filename: f });
  }
  return { S: sb.ILImmersiveSims, E: sb.ILImmersiveExam, R: sb.ILImmersiveReview, ls: sb.localStorage };
}
const T0 = Date.UTC(2026, 9, 13, 13, 0, 0);
const MIN = 60e3, DAY = 864e5;

test('review checkpoints mirror the exam pool exactly (same CKA scope + domains)', () => {
  const { S, E, R } = sandbox();
  const cps = R.checkpoints(S);
  const pool = E.pool(S);
  assert.equal(cps.length, pool.length);
  assert.deepEqual(new Set(cps.map(c => c.k)), new Set(pool.map(p => p.simId + '::' + p.scenarioId)));
  for (const p of pool) assert.equal(R.CKA_DOMAIN[p.simId], p.domain, p.simId);
  assert.match(R.honesty, /not FSRS/i);
  assert.match(R.honesty, /not a live cluster/);
});

test('Leitner transitions: miss → 0, slow-correct holds, good promotes, caps at MAX_BOX', () => {
  const { R } = sandbox();
  assert.equal(R.gradeOf(false, 100), 'again');
  assert.equal(R.gradeOf(true, R.SLOW_MS + 1), 'hard');
  assert.equal(R.gradeOf(true, 2000), 'good');
  assert.equal(R.nextBox(4, 'again', false), 0);
  assert.equal(R.nextBox(3, 'hard', false), 3);
  assert.equal(R.nextBox(0, 'hard', false), 1);
  assert.equal(R.nextBox(2, 'good', false), 3);
  assert.equal(R.nextBox(R.MAX_BOX, 'good', false), R.MAX_BOX);
  assert.equal(R.nextBox(0, 'good', true, 'exam'), 2, 'correct first sighting on a timed paper → 1 day');
  assert.equal(R.nextBox(0, 'good', true, 'drill'), 1);
  assert.deepEqual([...R.INTERVALS], [0, 10 * MIN, DAY, 3 * DAY, 7 * DAY, 16 * DAY, 35 * DAY]);
});

test('ingestExam: misses + timeouts are due now; correct items re-check in 1 day', () => {
  const { S, E, R, ls } = sandbox();
  const exam = E.buildExam(S, { count: 6, minutes: 8, seed: 11, now: T0 });
  exam.items.forEach((it, i) => {
    if (i === 5) return; /* clock ran out on the last item */
    const pick = i < 3 ? it.answer : (it.answer + 1) % it.options.length;
    const g = E.gradeItem(it, pick, 3000);
    it.choice = g.choice; it.correct = g.correct; it.ms = g.ms;
  });
  const fed = R.ingestExam(exam, { now: T0 });
  assert.deepEqual({ q: fed.queued, l: fed.lapses, t: fed.timeouts, c: fed.correct }, { q: 6, l: 3, t: 1, c: 3 });
  const db = JSON.parse(ls.getItem(R.STORE_KEY));
  assert.equal(Object.keys(db.cards).length, 6);
  assert.equal(db.examsIngested, 1);
  const due = R.queue(S, { now: T0 + 1, limit: 10, topUp: false });
  assert.equal(due.length, 3, 'only the 3 lapses are due immediately');
  assert.ok(due.every(x => x.reason === 'relearn' && /incl\. timed exam/.test(x.reasonText)));
  const missedKeys = exam.items.filter((it, i) => i >= 3).map(it => it.simId + '::' + it.scenarioId).sort();
  assert.deepEqual(due.map(x => x.k).sort(), missedKeys);
  /* After a day, the correct ones come due too. */
  assert.equal(R.queue(S, { now: T0 + DAY + 1, limit: 10, topUp: false }).length, 6);
});

test('queue tops up with unseen checkpoints from the weakest evidenced domain and says why', () => {
  const { S, R } = sandbox();
  const cps = R.checkpoints(S);
  const net = cps.filter(c => c.domain === 'Networking');
  const store = cps.filter(c => c.domain === 'Storage');
  /* Networking: one miss. Storage: one strong correct. */
  R.record({ simId: net[0].simId, scenarioId: net[0].scenarioId, correct: false, ms: 4000, src: 'drill', now: T0 });
  for (let i = 0; i < 4; i++) R.record({ simId: store[0].simId, scenarioId: store[0].scenarioId, correct: true, ms: 3000, src: 'review', now: T0 + i * 40 * DAY });
  const weak = R.weakDomains(S, 3, { now: T0 + 200 * DAY });
  assert.equal(weak[0], 'Networking');
  const q = R.queue(S, { now: T0 + 1, limit: 5 });
  assert.equal(q[0].k, net[0].k);
  assert.equal(q[0].reason, 'relearn');
  const top = q.filter(x => x.reason === 'weak-domain');
  assert.ok(top.length >= 1);
  assert.ok(top.some(x => x.domain === 'Networking'), 'weakest domain feeds first new card');
  assert.ok(top.every(x => /^New · weak domain: /.test(x.reasonText)));
  const untested = q.filter(x => x.reason === 'untested-domain');
  assert.ok(untested.length >= 1, 'untested domains get a card after the weak ones');
  assert.ok(untested.every(x => x.domain !== 'Networking' && x.domain !== 'Storage' && /^New · untested domain: /.test(x.reasonText)));
  assert.ok(q.findIndex(x => x.reason === 'untested-domain') > q.findIndex(x => x.reason === 'weak-domain'), 'weak before untested');
  assert.equal(new Set(q.map(x => x.k)).size, q.length, 'no duplicates');
});

test('cold start (no evidence) labels top-up honestly and spans domains', () => {
  const { S, R } = sandbox();
  const q = R.queue(S, { now: T0, limit: 8 });
  assert.equal(q.length, 8);
  assert.ok(q.every(x => x.reason === 'cold-start' && /no on-device evidence yet/.test(x.reasonText)));
  assert.ok(new Set(q.map(x => x.domain)).size >= 6, 'cold start spans domains');
  assert.deepEqual([...R.focusSims(S, 3, { now: T0 })], [], 'no evidence → no adaptive focus (standard paper)');
});

test('mastery counts unseen checkpoints as 0 and orders weakest first', () => {
  const { S, R } = sandbox();
  const m0 = R.mastery(S, { now: T0 });
  assert.ok(m0.length >= 7);
  assert.ok(m0.every(d => d.pct === 0 && d.seen === 0 && d.accuracy === null));
  const cfg = R.checkpoints(S).filter(c => c.domain === 'Configuration');
  for (const c of cfg) for (let i = 0; i < 8; i++) R.record({ simId: c.simId, scenarioId: c.scenarioId, correct: true, ms: 1000, src: 'review', now: T0 + i * 40 * DAY });
  const m1 = R.mastery(S, { now: T0 + 400 * DAY });
  const conf = m1.find(d => d.domain === 'Configuration');
  assert.equal(conf.pct, 100);
  assert.equal(m1[m1.length - 1].domain, 'Configuration', 'strongest last');
  assert.equal(m1[0].pct, 0);
});

test('stats: retention only counts due reviews of graduated cards; streak uses local days', () => {
  const { S, R } = sandbox();
  const c = R.checkpoints(S)[0];
  const rec = (ok, t, src = 'review') => R.record({ simId: c.simId, scenarioId: c.scenarioId, correct: ok, ms: 2000, src, now: t });
  rec(true, T0, 'exam');            /* new → box 2 (exam evidence), not a review */
  rec(true, T0 + 2 * DAY);          /* due review from box 2 → 3: counts, ok */
  rec(false, T0 + 6 * DAY);         /* due review from box 3 → 0: counts, miss */
  rec(true, T0 + 6 * DAY + 1000);   /* box 0 → 1 relearn: from < 2 → excluded */
  const st = R.stats({ now: T0 + 6 * DAY + 2000 });
  assert.equal(st.reviews, 3);
  assert.equal(st.retentionN, 2);
  assert.equal(st.retentionPct, 50);
  assert.equal(st.cards, 1);
  assert.equal(st.learning, 1);
  assert.equal(st.dueNow, 0);
  assert.equal(st.nextDueAt, T0 + 6 * DAY + 1000 + 10 * MIN);
  assert.equal(st.streakDays, 1, 'gap days break the streak');
  const ex = JSON.parse(R.exportJson({ now: T0 }));
  assert.equal(ex.version, R.VERSION);
  assert.ok(ex.store.cards[c.k]);
  assert.match(ex.honesty, /no server or cohort data/);
  R.reset();
  assert.equal(R.stats({ now: T0 }).cards, 0);
});

test('adaptive exam: focus sims fill ≥60% of the paper; no focus = unchanged v1.0 selection', () => {
  const { S, E, R } = sandbox();
  const plain = E.buildExam(S, { count: 10, seed: 42, now: T0 });
  const plainEmpty = E.buildExam(S, { count: 10, seed: 42, now: T0, focus: [] });
  assert.deepEqual(plain.items.map(i => i.simId + i.scenarioId), plainEmpty.items.map(i => i.simId + i.scenarioId));
  assert.deepEqual([...plain.focus], []);
  /* Seed evidence: miss everything in Networking. */
  for (const c of R.checkpoints(S).filter(x => x.domain === 'Networking')) R.record({ simId: c.simId, scenarioId: c.scenarioId, correct: false, ms: 5000, src: 'exam', now: T0 });
  const focus = R.focusSims(S, 1, { now: T0 });
  assert.deepEqual([...focus].sort(), ['cni-network', 'gateway-api', 'ingress-routing', 'netpol-isolation']);
  const ad = E.buildExam(S, { count: 10, seed: 42, now: T0, focus });
  assert.equal(ad.items.length, 10);
  const inFocus = ad.items.filter(i => focus.includes(i.simId)).length;
  assert.ok(inFocus >= Math.ceil(10 * E.FOCUS_SHARE), 'focus share ' + inFocus);
  assert.ok(new Set(ad.items.map(i => i.simId)).size >= 6, 'still keeps cross-domain coverage');
  assert.equal(new Set(ad.items.map(i => i.simId + '::' + i.scenarioId)).size, 10, 'no duplicate checkpoints');
  assert.deepEqual([...ad.focus].sort(), [...focus].sort());
  assert.match(E.VERSION, /^1\.[12]\./);
});

test('review page + wiring: relative assets, honest copy, drills feed the loop but exam/review stages do not double-count', () => {
  const html = readFileSync(path.join(root, 'docs/immersive/review/index.html'), 'utf8');
  for (const f of ['il-immersive-review.js', 'il-immersive-review-boot.js', 'il-immersive-sims.js', 'il-immersive-3d.js', 'il-scene-kit.js']) assert.ok(html.includes('/assets/' + f), f);
  assert.equal(html.includes('https://interstitiumlabs.dev/assets/'), false, 'no absolute CDN assets');
  assert.match(html, /not FSRS/i);
  assert.match(html, /not a live cluster/);
  assert.match(html, /data-il-review-start/);
  assert.match(html, /"review":true/);
  const exam = readFileSync(path.join(root, 'docs/immersive/exam/index.html'), 'utf8');
  assert.match(exam, /il-immersive-review\.js/);
  assert.match(exam, /data-adaptive="1"/);
  assert.match(exam, /data-il-exam-remediate/);
  const idx = readFileSync(path.join(root, 'docs/immersive/index.html'), 'utf8');
  assert.match(idx, /il-immersive-review\.js/);
  assert.match(idx, /data-il-review-due-badge/);
  const player = readFileSync(path.join(root, 'docs/assets/il-immersive-3d.js'), 'utf8');
  assert.match(player, /cfg\.owned = !!\(j && \(j\.exam \|\| j\.review\)\)/);
  assert.match(player, /!this\.cfg\.owned && g\.ILImmersiveReview/);
  const boot = readFileSync(path.join(root, 'docs/assets/il-immersive-review-boot.js'), 'utf8');
  assert.equal(/\.innerHTML\s*=/.test(boot), false, 'review boot builds DOM with textContent only');
  const manifest = JSON.parse(readFileSync(path.join(root, 'docs/assets/scenes/manifest.json'), 'utf8'));
  assert.equal(manifest.sims.review.path, '/immersive/review/');
  assert.match(manifest.sims.review.storage, /device only/);
});

test('speakLine (2026-10-14 Lab Muse queue briefing): counts by reason, weakest seen domain, honest empty state', () => {
  const { S, R } = sandbox();
  assert.match(R.VERSION, /^1\.3\./);
  assert.match(R.speakLine({ dueNow: 0 }, [], []), /^Lab Muse: nothing is due on this device\./);
  const q = [{ reason: 'relearn' }, { reason: 'relearn' }, { reason: 'due' }, { reason: 'weak-domain' }];
  const mast = [{ domain: 'Untouched', pct: 0, seen: 0 }, { domain: 'Troubleshooting', pct: 17, seen: 3 }];
  const line = R.speakLine({ dueNow: 3 }, q, mast);
  assert.equal(line, 'Lab Muse: 3 checkpoints due now on this device. Next session is 4 cards: 2 to relearn from misses, 1 due for spaced review, 1 new from your weakest domains. Weakest domain: Troubleshooting, 17 percent mastery. Start the session to re-serve them on the authored 3D scenes.');
  assert.match(R.speakLine({ dueNow: 1 }, [{ reason: 'relearn' }], []), /1 checkpoint due now.*1 card: 1 to relearn/);
  /* Real data path: a cold device still yields a sentence (cold-start top-ups), never a fake count. */
  const cold = R.speakLine(R.stats(), R.queue(S, { limit: 10 }), R.mastery(S));
  assert.match(cold, /^Lab Muse: 0 checkpoints due now on this device\. Next session is \d+ cards?: \d+ cold-start\./);
});

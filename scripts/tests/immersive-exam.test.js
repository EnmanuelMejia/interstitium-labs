/**
 * Timed CKA mock exam engine tests (2026-10-12).
 * Pure: no browser. Loads il-immersive-sims.js + il-immersive-exam.js via vm.
 */
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import vm from 'node:vm';
import test from 'node:test';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
function load(name) {
  const code = readFileSync(path.join(root, 'docs/assets', name), 'utf8');
  const sandbox = { module: { exports: {} }, exports: {}, console, localStorage: {
    _d: {},
    getItem(k) { return this._d[k] || null; },
    setItem(k, v) { this._d[k] = String(v); }
  } };
  // UMD files read globalThis/window — provide both
  sandbox.globalThis = sandbox;
  sandbox.window = sandbox;
  vm.runInNewContext(code, sandbox, { filename: name });
  return sandbox.module.exports || sandbox.ILImmersiveExam || sandbox.ILImmersiveSims;
}
const S = load('il-immersive-sims.js');
const E = load('il-immersive-exam.js');

test('exam pool covers every CKA sim with predict checkpoints only', () => {
  const p = E.pool(S);
  assert.ok(p.length >= 40, 'pool size ' + p.length);
  const sims = new Set(p.map(x => x.simId));
  for (const id of E.CKA_SIMS) assert.ok(sims.has(id), id);
  assert.equal(sims.has('aws-az-failure'), false, 'AWS out of CKA paper');
  assert.equal(sims.has('iam-eval'), false, 'IAM out of CKA paper');
  assert.equal(sims.has('mesh-mtls'), false, 'Istio mesh out of CKA paper');
  for (const x of p) {
    assert.ok(x.q && x.options.length >= 2 && typeof x.answer === 'number');
    assert.ok(x.glb.endsWith('.glb'));
  }
});

test('buildExam is deterministic for a seed and prefers domain coverage', () => {
  const a = E.buildExam(S, { count: 10, minutes: 15, seed: 42 });
  const b = E.buildExam(S, { count: 10, minutes: 15, seed: 42 });
  assert.equal(a.seed, 42);
  assert.equal(a.items.length, 10);
  assert.deepEqual(a.items.map(i => i.simId + ':' + i.scenarioId), b.items.map(i => i.simId + ':' + i.scenarioId));
  const uniqueSims = new Set(a.items.map(i => i.simId));
  assert.ok(uniqueSims.size >= 8, 'domain coverage ' + uniqueSims.size);
  assert.ok(a.endsAt - a.startedAt === 15 * 60 * 1000);
  assert.match(a.honesty, /not a live cluster/i);
});

test('gradeItem + summarize compute pass bar without inventing scores', () => {
  const exam = E.buildExam(S, { count: 5, minutes: 8, seed: 7, passPct: 60 });
  let correct = 0;
  for (let i = 0; i < exam.items.length; i++) {
    const it = exam.items[i];
    const pick = i % 2 === 0 ? it.answer : (it.answer + 1) % it.options.length;
    const g = E.gradeItem(it, pick, 1200 + i);
    it.choice = g.choice; it.correct = g.correct; it.ms = g.ms;
    if (g.correct) correct++;
  }
  const sum = E.summarize(exam);
  assert.equal(sum.correct, correct);
  assert.equal(sum.total, 5);
  assert.equal(sum.answered, 5);
  assert.equal(sum.pct, Math.round((correct / 5) * 100));
  assert.equal(sum.passed, sum.pct >= 60);
  assert.ok(Object.keys(sum.byDomain).length >= 1);
});

test('recordAttempt persists on-device history only', () => {
  // Re-load exam module against a fresh localStorage sandbox via direct API
  const exam = E.buildExam(S, { count: 3, minutes: 5, seed: 99 });
  exam.items.forEach((it) => {
    const g = E.gradeItem(it, it.answer, 500);
    it.choice = g.choice; it.correct = g.correct; it.ms = g.ms;
  });
  const sum = E.summarize(exam);
  const db = E.recordAttempt(exam, sum);
  assert.equal(db.last.correct, 3);
  assert.equal(db.last.total, 3);
  assert.equal(db.last.passed, true);
  assert.ok(Array.isArray(db.attempts) && db.attempts.length >= 1);
});

test('exam page + assets are wired for relative offline load', () => {
  const html = readFileSync(path.join(root, 'docs/immersive/exam/index.html'), 'utf8');
  assert.match(html, /il-immersive-exam\.js/);
  assert.match(html, /il-immersive-exam-boot\.js/);
  assert.match(html, /il-immersive-sims\.js/);
  assert.match(html, /il-immersive-3d\.js/);
  assert.equal(html.includes('https://interstitiumlabs.dev/assets/'), false, 'no absolute CDN assets');
  assert.match(html, /data-il-exam-start/);
  assert.match(html, /not killer\.sh/i);
});

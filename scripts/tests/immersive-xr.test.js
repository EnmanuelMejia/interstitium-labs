/**
 * WebXR entry + world-space predict HUD tests (2026-10-14 / 2026-10-15): pure helpers on ILImmersive3D.xr.
 * Loads docs/assets/il-immersive-3d.js in a vm sandbox with a stub document that never fires
 * DOMContentLoaded, so nothing mounts; only the exported helpers are exercised.
 */
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import vm from 'node:vm';
import test from 'node:test';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const SRC = readFileSync(path.join(root, 'docs/assets/il-immersive-3d.js'), 'utf8');

function load(navigator = {}) {
  const sb = {
    console, Promise, navigator,
    performance: { now: () => 0 },
    document: { readyState: 'loading', addEventListener() {}, querySelectorAll: () => [] },
    addEventListener() {},
    matchMedia: () => ({ matches: false })
  };
  sb.globalThis = sb; sb.window = sb;
  vm.runInNewContext(SRC, sb, { filename: 'il-immersive-3d.js' });
  return sb.ILImmersive3D;
}
const plain = (o) => JSON.parse(JSON.stringify(o));

test('exports v1.11.0 (v1.8.0 HUD + v1.9.0 CLI lab + v1.10.0 coach + v1.11.0 CLI review cards / voice input) with webxr flag and an honest (non-Unreal, non-hosted) label', () => {
  const API = load();
  assert.equal(API.version, '1.11.0');
  assert.equal(API.cliLab, true);
  assert.equal(API.cliReviewCards, true);
  assert.equal(API.cliVoiceInput, true);
  assert.equal(API.webxr, true);
  assert.deepEqual(plain(API.xr.modes), { vr: 'immersive-vr', ar: 'immersive-ar' });
  assert.match(API.xr.honesty, /WebXR over the authored glTF/);
  assert.match(API.xr.honesty, /not Unreal Pixel Streaming/);
  assert.match(API.xr.honesty, /not a hosted cluster/);
  assert.doesNotMatch(API.xr.honesty, /Quest/i, 'no headset-vendor exclusivity claim');
});

test('source stays CSP-clean: no CDN Three / remote script, no fake keys', () => {
  assert.doesNotMatch(SRC, /unpkg|jsdelivr|cdnjs|three\.module|import\s*\(/);
  assert.doesNotMatch(SRC, /BEGIN [A-Z ]*PRIVATE KEY|api[_-]?key\s*[:=]/i);
});

test('probe: absent navigator.xr / missing isSessionSupported → unsupported', async () => {
  const { xr } = load();
  assert.deepEqual(plain(await xr.probe({}, false)), { vr: false, ar: false, reason: 'no-webxr' });
  assert.deepEqual(plain(await xr.probe(undefined, false)), { vr: false, ar: false, reason: 'no-webxr' });
  assert.deepEqual(plain(await xr.probe({ xr: {} }, false)), { vr: false, ar: false, reason: 'no-webxr' });
});

test('probe: prefers-reduced-motion hides XR even when a device is present', async () => {
  const { xr } = load();
  let asked = 0;
  const nav = { xr: { isSessionSupported: () => { asked++; return Promise.resolve(true); } } };
  assert.deepEqual(plain(await xr.probe(nav, true)), { vr: false, ar: false, reason: 'reduced-motion' });
  assert.equal(asked, 0, 'does not even ask the UA');
});

test('probe: asks for immersive-vr and immersive-ar separately', async () => {
  const { xr } = load();
  const asked = [];
  const nav = { xr: { isSessionSupported: (m) => { asked.push(m); return Promise.resolve(m === 'immersive-vr'); } } };
  assert.deepEqual(plain(await xr.probe(nav, false)), { vr: true, ar: false, reason: 'supported' });
  assert.deepEqual(asked.sort(), ['immersive-ar', 'immersive-vr']);
  const both = { xr: { isSessionSupported: () => Promise.resolve(true) } };
  assert.deepEqual(plain(await xr.probe(both, false)), { vr: true, ar: true, reason: 'supported' });
});

test('probe: rejecting, throwing or truthy-non-boolean answers count as unsupported', async () => {
  const { xr } = load();
  const rej = { xr: { isSessionSupported: () => Promise.reject(new Error('SecurityError')) } };
  assert.deepEqual(plain(await xr.probe(rej, false)), { vr: false, ar: false, reason: 'no-xr-device' });
  const thr = { xr: { isSessionSupported: () => { throw new Error('boom'); } } };
  assert.deepEqual(plain(await xr.probe(thr, false)), { vr: false, ar: false, reason: 'no-xr-device' });
  const weird = { xr: { isSessionSupported: () => Promise.resolve('yes') } };
  assert.equal((await xr.probe(weird, false)).vr, false);
});

test('sessionInit: nothing required; local-floor optional; dom-overlay only for AR with a root', () => {
  const { xr } = load();
  const vr = plain(xr.sessionInit('vr', { id: 'x' }));
  assert.deepEqual(vr, { requiredFeatures: [], optionalFeatures: ['local-floor'] });
  const arNoRoot = plain(xr.sessionInit('ar'));
  assert.deepEqual(arNoRoot, { requiredFeatures: [], optionalFeatures: ['local-floor'] });
  const rootEl = { tag: 'div' };
  const ar = xr.sessionInit('ar', rootEl);
  assert.deepEqual([...ar.optionalFeatures], ['local-floor', 'dom-overlay']);
  assert.equal(ar.domOverlay.root, rootEl);
  assert.equal(ar.requiredFeatures.length, 0);
});

test('requestRefSpace: local-floor preferred, falls back to local on reject / throw / null', async () => {
  const { xr } = load();
  assert.deepEqual([...xr.refSpaceOrder()], ['local-floor', 'local']);
  const ok = await xr.requestRefSpace({ requestReferenceSpace: (t) => Promise.resolve({ t }) });
  assert.equal(ok.type, 'local-floor');
  const asked = [];
  const rej = await xr.requestRefSpace({ requestReferenceSpace: (t) => { asked.push(t); return t === 'local' ? Promise.resolve({ t }) : Promise.reject(new Error('NotSupportedError')); } });
  assert.equal(rej.type, 'local');
  assert.deepEqual(asked, ['local-floor', 'local']);
  const thr = await xr.requestRefSpace({ requestReferenceSpace: (t) => { if (t === 'local-floor') throw new Error('sync'); return { t }; } });
  assert.equal(thr.type, 'local');
  const nul = await xr.requestRefSpace({ requestReferenceSpace: (t) => (t === 'local-floor' ? null : { t }) });
  assert.equal(nul.type, 'local');
  await assert.rejects(xr.requestRefSpace({ requestReferenceSpace: () => Promise.reject(new Error('no')) }), /no-reference-space/);
});

test('session state machine: idle → requesting → active → ending → idle; denial and stray events are safe', () => {
  const { xr } = load();
  const run = (evts, s = 'idle') => evts.reduce((st, e) => xr.transition(st, e), s);
  assert.equal(run(['request']), 'requesting');
  assert.equal(run(['request', 'granted']), 'active');
  assert.equal(run(['request', 'granted', 'end']), 'ending');
  assert.equal(run(['request', 'granted', 'end', 'ended']), 'idle');
  assert.equal(run(['request', 'granted', 'ended']), 'idle', 'UA/system ended the session');
  assert.equal(run(['request', 'denied']), 'idle');
  assert.equal(run(['request', 'request']), 'requesting', 'double click does not re-request');
  assert.equal(run(['granted']), 'idle', 'grant without request ignored');
  assert.equal(run(['request', 'granted', 'request']), 'active');
  assert.equal(run(['ended', 'end']), 'idle');
  assert.equal(xr.transition('bogus', 'request'), 'requesting');
  assert.equal(xr.transition('bogus', 'nope'), 'idle');
});

test('buttons model: hidden without support; one session at a time; Exit label on the live mode', () => {
  const { xr } = load();
  let m = xr.buttons({ vr: false, ar: false }, 'idle');
  assert.equal(m.vr.hidden && m.ar.hidden, true);
  m = xr.buttons({ vr: true, ar: false }, 'idle');
  assert.deepEqual(plain(m.vr), { hidden: false, label: 'Enter VR', pressed: false, disabled: false });
  assert.equal(m.ar.hidden, true);
  m = xr.buttons({ vr: true, ar: true }, 'requesting', 'vr');
  assert.equal(m.vr.disabled && m.ar.disabled, true);
  m = xr.buttons({ vr: true, ar: true }, 'active', 'ar');
  assert.deepEqual(plain(m.ar), { hidden: false, label: 'Exit AR', pressed: true, disabled: false });
  assert.equal(m.vr.disabled, true, 'cannot start VR while AR runs');
  m = xr.buttons({ vr: true, ar: true }, 'idle', null, true);
  assert.equal(m.vr.disabled && m.ar.disabled, true, 'another stage owns the session');
});

test('placement: diorama in front of the learner, floor-aware, smaller tabletop scale for AR', () => {
  const { xr } = load();
  const vf = plain(xr.placement('vr', 'local-floor'));
  const vl = plain(xr.placement('vr', 'local'));
  const af = plain(xr.placement('ar', 'local-floor'));
  assert.ok(vf.z < 0 && vl.z < 0 && af.z < 0, 'in front (-Z)');
  assert.ok(vf.y > 0.5 && vf.y < 1.5, 'waist/table height above floor');
  assert.ok(vl.y < 0, 'below eye level when origin is the head');
  assert.ok(af.s < vf.s, 'AR tabletop is smaller');
  /* Authored scenes span ≈ ±2.5 units → keep the diorama within arm-ish reach (< 1.6 m wide). */
  assert.ok(vf.s * 5 <= 1.6 && af.s * 5 <= 1.1);
});

test('curriculum manifest declares the WebXR entry honestly (no hosted cluster / Pixel Streaming claim)', () => {
  const m = JSON.parse(readFileSync(path.join(root, 'docs/assets/scenes/manifest.json'), 'utf8'));
  const x = m.sims.webxr;
  assert.deepEqual(x.modes, ['immersive-vr', 'immersive-ar']);
  assert.deepEqual(x.requiredFeatures, []);
  assert.deepEqual(x.referenceSpaces, ['local-floor', 'local']);
  assert.match(x.honesty, /not Unreal Pixel Streaming, not a hosted cluster/);
  assert.match(x.honesty, /not a physical headset/);
  assert.match(m.sims.player, /v1\.11\.0/);
});


test('exports xr.hud helpers with honest (non-UMG, non-Pixel-Streaming) label', () => {
  const API = load();
  assert.equal(API.xrHud, true);
  assert.match(API.xr.hud.honesty, /not Unreal UMG/);
  assert.match(API.xr.hud.honesty, /not a Pixel Streaming HUD/);
  assert.match(API.xr.hud.honesty, /not a hosted cluster/);
});

test('hud model: predict options keep origIdx through shuffle order; cursor clamps', () => {
  const { xr } = load();
  const m = xr.hud.model({
    phase: 'predict',
    prompt: 'Predict first: quorum?',
    options: [{ origIdx: 2, label: 'C' }, { origIdx: 0, label: 'A' }, { origIdx: 1, label: 'B' }],
    cursor: 99
  });
  assert.equal(m.phase, 'predict');
  assert.equal(m.cursor, 2);
  assert.deepEqual(plain(m.options.map(o => o.origIdx)), [2, 0, 1]);
  assert.deepEqual(plain(m.options.map(o => o.letter)), ['A', 'B', 'C']);
  assert.equal(xr.hud.model({ phase: 'idle' }).options.length, 0);
});

test('hud layout: prompt + selectable option quads + honesty chip; reveal swaps options for result', () => {
  const { xr } = load();
  const predict = xr.hud.model({
    phase: 'predict', prompt: 'Q?', options: [{ origIdx: 1, label: 'yes' }, { origIdx: 0, label: 'no' }], cursor: 1
  });
  const layout = xr.hud.layout(predict);
  assert.ok(layout.some(q => q.kind === 'prompt'));
  const opts = layout.filter(q => q.kind === 'option');
  assert.equal(opts.length, 2);
  assert.equal(opts[1].origIdx, 0);
  assert.ok(opts[1].glow > opts[0].glow, 'cursor option glows more');
  assert.ok(layout.some(q => q.kind === 'honesty'));
  assert.ok(opts.every(q => q.fg === '#F5E6A8' || q.fg === '#E8EEF5'));
  const reveal = xr.hud.layout(xr.hud.model({ phase: 'reveal', prompt: 'Q?', reveal: { correct: true, text: 'Correct. because' } }));
  assert.ok(reveal.some(q => q.kind === 'reveal' && /Correct/.test(q.text)));
  assert.equal(reveal.filter(q => q.kind === 'option').length, 0);
  const next = xr.hud.layout(xr.hud.model({ phase: 'next', nextLabel: 'Lose majority' }));
  assert.ok(next.some(q => q.kind === 'next' && q.selectable));
});

test('hud hitTest: ray through an option AABB returns its layout index; misses return -1', () => {
  const { xr } = load();
  const layout = xr.hud.layout(xr.hud.model({
    phase: 'predict', prompt: 'Q?', options: [{ origIdx: 0, label: 'a' }, { origIdx: 1, label: 'b' }], cursor: 0
  }));
  const opt0 = layout.find(q => q.kind === 'option' && q.origIdx === 0);
  const hit = xr.hud.hitTest([opt0.x, opt0.y, opt0.z + 2], [0, 0, -1], layout);
  assert.ok(hit >= 0);
  assert.equal(layout[hit].origIdx, 0);
  assert.equal(xr.hud.hitTest([0, 10, 2], [0, 0, -1], layout), -1);
  assert.equal(xr.hud.hitTest([0, 0, 2], [0, 0, -1], []), -1);
});

test('hud advanceCursor wraps and rebuilds highlight target', () => {
  const { xr } = load();
  let m = xr.hud.model({ phase: 'predict', prompt: 'Q?', options: [{ origIdx: 0, label: 'a' }, { origIdx: 1, label: 'b' }], cursor: 0 });
  m = xr.hud.advanceCursor(m, 1);
  assert.equal(m.cursor, 1);
  m = xr.hud.advanceCursor(m, 1);
  assert.equal(m.cursor, 0);
});

test('curriculum manifest declares world HUD honesty (not UMG / Pixel Streaming HUD)', () => {
  const m = JSON.parse(readFileSync(path.join(root, 'docs/assets/scenes/manifest.json'), 'utf8'));
  const h = m.sims.webxr.hud;
  assert.equal(h.version, '1.8.0');
  assert.match(h.honesty, /not Unreal UMG/);
  assert.match(h.honesty, /not a Pixel Streaming HUD/);
  assert.match(m.sims.webxr.honesty, /In-headset predict HUD/);
});

/**
 * WebXR entry tests (2026-10-14): pure helpers exported on ILImmersive3D.xr.
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

test('exports v1.7.0 with webxr flag and an honest (non-Unreal, non-hosted) label', () => {
  const API = load();
  assert.equal(API.version, '1.7.0');
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
  assert.match(m.sims.player, /v1\.7\.0/);
});

/**
 * 2026-10-21 Musk-bar pass: Gateway API drill + CLI pack (gateway-api on the authored ingress-gateway.glb), ConfigMap &
 * Secret CLI pack (config-propagation), and the official CNCF CKA blueprint score (exam + on-device review).
 * Pure UMD — the browser runs exactly this code. Generic tip/focus/hint-replay coverage for the two new packs comes from
 * the loops in immersive-cli.test.js / immersive-cli-packs.test.js, which iterate C.list() (now 11 packs).
 */
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import vm from 'node:vm';
import test from 'node:test';

const require = createRequire(import.meta.url);
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const S = require(path.join(root, 'docs/assets/il-immersive-sims.js'));
const C = require(path.join(root, 'docs/assets/il-immersive-cli.js'));
const E = require(path.join(root, 'docs/assets/il-immersive-exam.js'));

function session(sim, taskId, extra) {
  const tk = taskId ? C.task(sim, taskId) : null;
  let state = S.merge(S.merge(S.get(sim).initial, tk ? tk.setup : {}), extra || {});
  const ctx = C.newCtx(taskId);
  return {
    ctx,
    get state() { return state; },
    run(line) { const r = C.run(sim, state, line, ctx); if (r.set) state = S.merge(state, r.set); return r; },
    status() { return C.taskStatus(sim, taskId, state, ctx); },
    derived() { return S.get(sim).derive(state); }
  };
}
const ORDERS = 'curl -sI https://shop.example.com/api/v1/orders';
const status = r => (/^HTTP\/2 (\d+)/.exec(r.out[0]) || [])[1];

/* ── Gateway API rules engine ─────────────────────────────────────────────── */
test('gateway-api sim: Gateway API spec semantics over the SAME authored ingress-gateway.glb', () => {
  const sim = S.get('gateway-api');
  assert.ok(['1.4.0', '1.5.0', '1.6.0', '1.7.0'].includes(S.VERSION), 'gateway-api arrived in v1.4.0; v1.5.0 (2026-10-22), v1.6.0 (2026-10-23) and v1.7.0 (2026-10-29) keep it');
  assert.equal(sim.glb, S.get('ingress-routing').glb, 'no new asset — the Blender-polished ingress-gateway.glb read as Gateway API');
  const at = set => S.gatewayDecide(S.merge(sim.initial, set));
  const codes = set => at(set).clients.map(c => c.status);
  assert.deepEqual(codes({}), [200, 200, 200]);
  assert.equal(sim.derive(sim.initial).verdict, 'healthy');
  const pend = at({ gwcAccepted: false });
  assert.deepEqual(pend.clients.map(c => c.status), ['no-route', 'no-route', 'no-route']);
  assert.equal(pend.gatewayProgrammed, 'Unknown', 'no controller → status stays Unknown (Pending), never False');
  assert.equal(pend.address, null);
  assert.deepEqual(codes({ routeAttached: false }), [404, 404, 404], 'unattached route (NoMatchingListenerHostname) → 404 for every path');
  assert.equal(at({ routeAttached: false }).routeAccepted, 'NoMatchingListenerHostname');
  assert.deepEqual(codes({ routeExact: true }), [404, 200, 200], 'Exact /api: whole-path only; /web unaffected');
  assert.deepEqual(codes({ refGrant: false }), [500, 500, 200], 'invalid backendRef MUST get 500; same-namespace /web keeps working');
  assert.equal(at({ refGrant: false }).routeResolvedRefs, 'RefNotPermitted');
  assert.deepEqual(codes({ certRef: false }), ['tls-fail', 'tls-fail', 'tls-fail'], 'no fallback certificate is promised');
  assert.equal(at({ certRef: false }).listener, 'InvalidCertificateRef');
  assert.equal(sim.derive(S.merge(sim.initial, { certRef: false })).verdict, 'down');
  assert.equal(sim.derive(S.merge(sim.initial, { refGrant: false })).verdict, 'degraded');
  assert.match(sim.derive(S.merge(sim.initial, { refGrant: false })).caption, /RefNotPermitted/);
  const keys = sim.scenarios.filter(sc => sc.predict).map(sc => sc.predict.answer);
  assert.equal(keys.length, 5);
  assert.equal(new Set(keys).size, 3, 'keyed answers spread over positions 0-2');
  for (const v of ['healthy', 'degraded', 'down']) assert.notEqual(S.verdictTone(v), 'info');
});

test('Gateway API pack: Pending GatewayClass → install → 200; listener cert missing → curl 35 even with -k', () => {
  const s = session('gateway-api', 'gw-pending');
  let r = s.run(ORDERS);
  assert.equal(r.exit, 7);
  assert.match(r.out.join('\n'), /no ADDRESS/);
  r = s.run('kubectl get gateway');
  assert.match(r.out[1], /^shop-gw\s+lab-gw\s+Unknown\s+12d$/, 'empty ADDRESS, PROGRAMMED Unknown');
  r = s.run('kubectl get gatewayclass');
  assert.match(r.out[1], /lab-gw\s+example\.net\/lab-gateway-controller\s+Unknown/);
  assert.match(s.run('kubectl describe gatewayclass lab-gw').out.join('\n'), /Reason:\s+Pending[\s\S]*Waiting for controller/);
  s.run('kubectl apply -f gateway-controller.yaml');
  assert.match(s.run('kubectl get gateway').out[1], /203\.0\.113\.20\s+True/);
  assert.equal(status(s.run(ORDERS)), '200');
  assert.equal(s.status().done, true);
  assert.equal(s.derived().verdict, 'healthy', 'typed commands re-tint the authored scene');

  const t = session('gateway-api', 'gw-cert');
  r = t.run('curl -skI https://shop.example.com/api');
  assert.equal(r.exit, 35, '-k cannot rescue an unprogrammed listener');
  const g = t.run('kubectl describe gateway shop-gw').out.join('\n');
  assert.match(g, /ResolvedRefs[\s\S]*Status:\s+False[\s\S]*InvalidCertificateRef/);
  assert.match(g, /Programmed[\s\S]*Status:\s+False/);
  t.run('kubectl create secret tls shop-tls --cert=shop.crt --key=shop.key');
  r = t.run('curl -sI https://shop.example.com/api');
  assert.equal(status(r), '200');
  assert.ok(r.events.includes('curl-200-verified'));
});

test('Gateway API pack: RefNotPermitted → 500; the grant lives in the TARGET namespace; hostname patch attaches the route', () => {
  const s = session('gateway-api', 'gw-refgrant');
  let r = s.run(ORDERS);
  assert.equal(status(r), '500');
  assert.match(r.out.join('\n'), /RefNotPermitted/);
  assert.equal(status(s.run('curl -sI https://shop.example.com/web/cart')), '200', 'same-namespace backend unaffected');
  assert.match(s.run('kubectl describe httproute shop-route').out.join('\n'), /Type:\s+ResolvedRefs\n\s+Status:\s+False\n\s+Reason:\s+RefNotPermitted/);
  r = s.run('kubectl get referencegrant');
  assert.match(r.out.join('\n'), /No resources found in default namespace[\s\S]*namespace that owns the target/);
  assert.ok(!r.events.includes('get-refgrant-none'), 'looking in the wrong namespace does not satisfy the step');
  assert.match(s.run('kubectl get referencegrant -n shop-api').out[0], /No resources found in shop-api namespace/);
  assert.match(s.run('cat shop-api-refgrant.yaml').out.join('\n'), /namespace: shop-api[\s\S]*kind: HTTPRoute[\s\S]*kind: Service/);
  assert.match(s.run('kubectl apply -f shop-api-refgrant.yaml').out[0], /referencegrant\.gateway\.networking\.k8s\.io\/allow-default-routes created/);
  assert.equal(status(s.run(ORDERS)), '200');
  assert.equal(s.status().done, true);

  const h = session('gateway-api', 'gw-hostname');
  assert.equal(status(h.run(ORDERS)), '404');
  assert.match(h.run('kubectl get httproute').out[1], /shop-route\s+\["shop\.example\.org"\]/);
  assert.match(h.run('kubectl describe httproute shop-route').out.join('\n'), /NoMatchingListenerHostname/);
  const bad = h.run('kubectl patch httproute shop-route --type=json -p \'[{"op":"replace","path":"/spec/rules/0/matches/0/path/type","value":"Prefix"}]\'');
  assert.equal(bad.exit, 1);
  assert.match(bad.out[0], /Unsupported value: "Prefix": supported values: "Exact", "PathPrefix", "RegularExpression"/, 'Ingress spelling is rejected like the CRD validation does');
  h.run('kubectl patch httproute shop-route --type=merge -p \'{"spec":{"hostnames":["shop.example.com"]}}\'');
  assert.equal(h.state.routeAttached, true);
  h.run('kubectl patch httproute shop-route --type=json -p \'[{"op":"replace","path":"/spec/rules/0/matches/0/path/type","value":"Exact"}]\'');
  assert.equal(status(h.run(ORDERS)), '404');
  assert.match(h.run('kubectl get httproute shop-route -o yaml').out.join('\n'), /type: Exact/);
  assert.equal(status(h.run('curl -sI https://shop.example.com/api')), '200');
});

test('Gateway API pack is honest: lab implementation (not a vendor), real kinds, Ingress stays in the Ingress drill', () => {
  const s = session('gateway-api');
  const help = s.run('help').out.join('\n');
  assert.match(help, /lab implementation computed by the rules engine — not Envoy Gateway, Istio, Cilium or NGINX Gateway Fabric/);
  assert.match(help, /Simulated shell/);
  const ar = s.run('kubectl api-resources --api-group=gateway.networking.k8s.io').out.join('\n');
  for (const k of ['GatewayClass', 'Gateway', 'HTTPRoute', 'GRPCRoute', 'ReferenceGrant']) assert.match(ar, new RegExp('\\b' + k + '\\b'));
  assert.match(ar, /referencegrants\s+refgrant\s+gateway\.networking\.k8s\.io\/v1beta1/);
  assert.match(s.run('kubectl get ingress').out.join('\n'), /not an Ingress/);
  assert.equal(s.run('kubectl get gtw shop-gw').exit, 0, 'short name gtw');
  assert.equal(s.run('kubectl get gateway nope').exit, 1);
});

/* ── ConfigMap & Secret pack ──────────────────────────────────────────────── */
test('ConfigMap pack: volume refreshes only after the kubelet sync (simulated sleep); env only after a rollout', () => {
  const s = session('config-propagation', 'volume-vs-env');
  const file = 'kubectl exec deploy/api -- cat /etc/config/LOG_LEVEL', env = 'kubectl exec deploy/api -- printenv LOG_LEVEL';
  assert.equal(s.run(file).out[0], 'info');
  assert.match(s.run('kubectl patch configmap app-config -p \'{"data":{"LOG_LEVEL":"debug"}}\'').out[0], /configmap\/app-config patched/);
  assert.match(s.run('kubectl get configmap app-config -o yaml').out.join('\n'), /LOG_LEVEL: debug/, 'the API has the new value at once');
  assert.equal(s.run(file).out[0], 'info', 'projected volume not refreshed yet');
  assert.match(s.run('sleep 30').out[0], /probably not re-synced/);
  assert.equal(s.run(file).out[0], 'info');
  assert.match(s.run('sleep 90').out[0], /simulated, nothing waited/);
  assert.equal(s.run(file).out[0], 'debug');
  assert.equal(s.run(env).out[0], 'info', 'env vars are resolved at container start');
  assert.equal(s.derived().verdict, 'stale');
  assert.match(s.run('kubectl rollout restart deployment/api').out[0], /deployment\.apps\/api restarted/);
  assert.equal(s.run(env).out[0], 'debug');
  assert.match(s.run('kubectl get pods').out[1], /^api-5f6b7-q8w2n\s+1\/1\s+Running/, 'new pod name after the rollout');
  assert.equal(s.status().done, true);
});

test('ConfigMap pack: immutable rejects the edit with the real message; only delete + recreate + rollout changes it', () => {
  const s = session('config-propagation', 'immutable');
  const r = s.run('kubectl patch configmap app-config -p \'{"data":{"LOG_LEVEL":"debug"}}\'');
  assert.equal(r.exit, 1);
  assert.equal(r.out[0], 'The ConfigMap "app-config" is invalid: data: Forbidden: field is immutable when `immutable` is set');
  assert.equal(s.derived().verdict, 'rejected', 'the scene shows the rejection');
  assert.match(s.run('kubectl get configmap app-config -o yaml').out.join('\n'), /LOG_LEVEL: info[\s\S]*immutable: true/);
  assert.match(s.run('kubectl create configmap app-config --from-literal=LOG_LEVEL=debug').out[0], /already exists/);
  s.run('kubectl delete configmap app-config');
  assert.equal(s.run('kubectl get configmap app-config').exit, 1);
  assert.equal(s.run('kubectl exec deploy/api -- printenv LOG_LEVEL').out[0], 'info', 'running pods keep their copy');
  s.run('kubectl create configmap app-config --from-literal=LOG_LEVEL=debug');
  assert.equal(s.state.immutable, false);
  s.run('kubectl rollout restart deployment/api');
  assert.equal(s.run('kubectl exec deploy/api -- printenv LOG_LEVEL').out[0], 'debug');
  assert.equal(s.status().done, true);
});

test('Secret pack: missing secretKeyRef key → CreateContainerConfigError with the kubelet reason; stringData patch fixes it; etcd at rest', () => {
  const s = session('config-propagation', 'missing-key');
  assert.match(s.run('kubectl get pods').out[1], /0\/1\s+CreateContainerConfigError/);
  assert.match(s.run('kubectl describe pods -l app=api').out.join('\n'), /Error: couldn't find key password in Secret default\/db-creds/);
  const d = s.run('kubectl describe secret db-creds').out.join('\n');
  assert.match(d, /username:\s+5 bytes/);
  assert.doesNotMatch(d, /password/);
  assert.doesNotMatch(d, /admin|s3cr3t/, 'describe never prints values');
  assert.match(s.run('kubectl exec deploy/api -- printenv LOG_LEVEL').out[0], /container not found/);
  assert.equal(s.run('kubectl rollout status deployment/api').exit, 1);
  s.run('kubectl patch secret db-creds -p \'{"stringData":{"password":"s3cr3t-lab"}}\'');
  assert.match(s.run('kubectl get pods').out[1], /1\/1\s+Running/);
  assert.equal(s.status().done, true);
  const e = session('config-propagation');
  assert.match(e.run('ETCDCTL_API=3 etcdctl get /registry/secrets/default/db-creds').out.join('\n'), /s3cr3t-lab[\s\S]*base64 in the API is encoding, not encryption/);
  const enc = session('config-propagation', null, { encryptAtRest: true });
  const out = enc.run('etcdctl get /registry/secrets/default/db-creds').out.join('\n');
  assert.match(out, /k8s:enc:aescbc:v1:key1:/);
  assert.doesNotMatch(out, /s3cr3t/);
});

test('pack totals: 16 packs · 49 tasks · 255 steps (15 · 44 · 226 on 2026-10-27; 11 · 30 · 136 on 2026-10-21; 12 · 34 · 160 on 2026-10-22; 13 · 38 · 184 on 2026-10-23); every new step focuses real nodes in its own authored .glb', () => {
  const tasks = C.list().reduce((n, id) => n + C.pack(id).tasks.length, 0);
  const steps = C.list().reduce((n, id) => n + C.pack(id).tasks.reduce((m, t) => m + t.steps.length, 0), 0);
  assert.deepEqual([C.list().length, tasks, steps], [16, 49, 255]);
  assert.equal(C.pack('gateway-api').tasks.length, 4);
  assert.equal(C.pack('config-propagation').tasks.length, 3);
  const m = JSON.parse(readFileSync(path.join(root, 'docs/assets/scenes/manifest.json'), 'utf8'));
  assert.match(m.sims.cli.gatewayNote, /not a live Gateway/);
  assert.match(m.sims.player, /16 packs/);
});

/* ── Official CKA blueprint ───────────────────────────────────────────────── */
test('blueprint: the 5 published CNCF CKA domains and weights; every CKA drill maps to exactly one', () => {
  assert.ok(['1.2.0', '1.3.0'].includes(E.VERSION), 'CKA blueprint since v1.2.0; v1.3.0 (2026-10-29) adds the CKS track and keeps it');
  assert.deepEqual(E.BLUEPRINT.map(b => [b.domain, b.weight]), [
    ['Troubleshooting', 30], ['Cluster Architecture, Installation & Configuration', 25], ['Services & Networking', 20], ['Workloads & Scheduling', 15], ['Storage', 10]]);
  assert.equal(E.BLUEPRINT.reduce((n, b) => n + b.weight, 0), 100);
  const mapped = E.BLUEPRINT.flatMap(b => b.sims);
  assert.deepEqual([...mapped].sort(), [...E.CKA_SIMS].sort(), 'every exam sim mapped, none twice');
  assert.equal(new Set(mapped).size, mapped.length);
  assert.ok(E.CKA_SIMS.includes('gateway-api'));
  assert.equal(E.OFFICIAL['gateway-api'], 'Services & Networking');
  assert.equal(E.OFFICIAL['config-propagation'], 'Workloads & Scheduling', 'ConfigMaps & Secrets is a Workloads & Scheduling competency');
  assert.equal(E.OFFICIAL['rbac-authz'], 'Cluster Architecture, Installation & Configuration');
  const html = readFileSync(path.join(root, 'docs/immersive/index.html'), 'utf8');
  for (const id of E.CKA_SIMS) assert.match(html, new RegExp('id="' + E.ANCHOR[id] + '"'), id + ' drill anchor exists on /immersive/');
});

test('blueprintScore: weakest = most points at stake (a 30% domain at 50% beats a 10% domain at 0%); untested never counts as passed', () => {
  const bp = E.blueprintScore({ Troubleshooting: { correct: 1, total: 2 }, Storage: { correct: 0, total: 1 }, 'Services & Networking': { correct: 2, total: 2 } });
  assert.equal(bp.weakest.domain, 'Troubleshooting');
  assert.equal(bp.weakest.atStake, 15);
  assert.equal(bp.rows.find(r => r.domain === 'Storage').atStake, 10);
  assert.deepEqual(bp.untested, ['Cluster Architecture, Installation & Configuration', 'Workloads & Scheduling']);
  assert.equal(bp.coveragePct, 60);
  assert.equal(bp.weightedPct, Math.round((30 * 50 + 10 * 0 + 20 * 100) / 60));
  assert.equal(bp.drill.href, '/immersive/#cka-control-plane');
  assert.match(bp.honesty, /not a predicted CNCF exam score/);
  const perfect = E.blueprintScore({ Storage: { correct: 1, total: 1 } });
  assert.equal(perfect.weakest, null);
  assert.equal(perfect.weightedPct, 100);
  assert.equal(E.blueprintScore({}).weightedPct, null, 'no evidence → no score, not 0 or 100');
});

test('summarize(): finished papers carry the blueprint view; unanswered items count as misses', () => {
  const exam = E.buildExam(S, { count: 11, seed: 7 });
  exam.items.forEach((it, i) => { if (i % 2 === 0) { it.choice = it.answer; it.correct = true; } });
  const sum = E.summarize(exam);
  const bp = sum.blueprint;
  assert.equal(bp.rows.reduce((n, r) => n + r.total, 0), 11);
  assert.equal(bp.rows.reduce((n, r) => n + r.correct, 0), sum.correct);
  for (const r of bp.rows) if (r.total) assert.equal(r.pct, Math.round(r.correct / r.total * 100));
  assert.ok(E.pool(S).some(p => p.simId === 'gateway-api'), 'Gateway API checkpoints are in the timed-exam pool');
});

function sandbox() {
  const sb = { console, localStorage: { _d: {}, getItem(k) { return Object.prototype.hasOwnProperty.call(this._d, k) ? this._d[k] : null; }, setItem(k, v) { this._d[k] = String(v); }, removeItem(k) { delete this._d[k]; } } };
  sb.globalThis = sb; sb.window = sb;
  for (const f of ['il-immersive-sims.js', 'il-immersive-exam.js', 'il-immersive-review.js']) vm.runInNewContext(readFileSync(path.join(root, 'docs/assets', f), 'utf8'), sb, { filename: f });
  return { S: sb.ILImmersiveSims, E: sb.ILImmersiveExam, R: sb.ILImmersiveReview };
}
test('review blueprint: unseen = 0% (never strong); evidence moves the weighted readiness and the weakest callout; Lab Muse names it', () => {
  const { S: S2, R } = sandbox();
  assert.match(R.VERSION, /^1\.3\./, 'blueprint() since v1.3.0; v1.3.1 (2026-10-29) only labels CKS CLI cards');
  let bp = R.blueprint(S2);
  assert.equal(bp.evidence, false);
  assert.equal(bp.weightedPct, 0);
  assert.ok(bp.rows.every(r => r.pct === 0 && r.total > 0), 'every official domain has checkpoints');
  assert.ok(R.checkpoints(S2).some(c => c.simId === 'gateway-api'));
  const T0 = Date.UTC(2026, 9, 21, 13, 0, 0);
  /* Troubleshooting has two drills since 2026-10-22 and three since 2026-10-23 (+ service-dns): answer them all. */
  for (const sim of ['control-plane-failure', 'node-troubleshoot', 'service-dns']) for (const sc of S2.get(sim).scenarios.filter(x => x.predict)) R.record({ simId: sim, scenarioId: sc.id, correct: true, ms: 5000, src: 'exam', now: T0 });
  R.record({ simId: 'storage-csi', scenarioId: S2.get('storage-csi').scenarios[0].id, correct: false, ms: 5000, src: 'exam', now: T0 });
  bp = R.blueprint(S2);
  assert.equal(bp.evidence, true);
  const tr = bp.rows.find(r => r.domain === 'Troubleshooting');
  assert.equal(tr.pct, Math.round(2 / 6 * 100), 'correct first exam sighting → box 2 of 6');
  assert.ok(bp.weightedPct > 0);
  assert.equal(bp.weakest.domain, 'Cluster Architecture, Installation & Configuration', '25% weight at 0% outranks Storage (10%) and Troubleshooting (30% at 33%)');
  assert.equal(bp.rows.find(r => r.domain === 'Storage').seen, 1);
  const line = R.speakLine(R.stats({ now: T0 }), R.queue(S2, { now: T0, limit: 10 }), R.mastery(S2), bp);
  assert.match(line, /Biggest gap on the official CKA blueprint: Cluster Architecture, Installation & Configuration, weighted 25 percent/);
  assert.doesNotMatch(R.speakLine(R.stats(), R.queue(S2, { limit: 10 }), R.mastery(S2), { evidence: false, weakest: bp.weakest }), /Biggest gap/);
});

test('wiring: gateway-api drill on /immersive/, published in the curriculum mirror, manifest + review page load the blueprint', () => {
  const html = readFileSync(path.join(root, 'docs/immersive/index.html'), 'utf8');
  assert.match(html, /id="cka-gateway-api"[\s\S]*?data-il-sim="gateway-api"\s*\n\s*data-gltf="\/assets\/immersive\/ingress-gateway\.glb"/);
  assert.match(html, /GatewayClass <code translate="no">lab-gw<\/code> is a lab implementation, not a live Gateway/);
  for (const f of ['labs.json', 'mirror.json']) {
    const j = JSON.parse(readFileSync(path.join(root, 'docs/curriculum-os', f), 'utf8'));
    const lab = (j.items || j.labs).find(l => l.immersive && l.immersive.sim === 'gateway-api');
    assert.ok(lab && lab.publishStatus === 'published' && lab.gltf === '/assets/immersive/ingress-gateway.glb', f);
  }
  const m = JSON.parse(readFileSync(path.join(root, 'docs/assets/scenes/manifest.json'), 'utf8'));
  assert.ok(m.sims.list.includes('gateway-api') && m.cka_coverage.interactive.includes('gateway-api'));
  assert.equal(m.sims.exam.version, E.VERSION);
  assert.match(m.sims.exam.blueprint.honesty, /not a predicted CNCF exam score/);
  assert.equal(m.cka_coverage.liveUnrealHost, false);
  assert.equal(m.cka_coverage.hostedFleet, false);
  const rv = readFileSync(path.join(root, 'docs/immersive/review/index.html'), 'utf8');
  assert.ok(rv.indexOf('il-immersive-exam.js') > -1 && rv.indexOf('il-immersive-exam.js') < rv.indexOf('il-immersive-review.js'), 'review page loads the blueprint before the review runtime');
  assert.match(rv, /data-il-review-blueprint/);
  const ex = readFileSync(path.join(root, 'docs/immersive/exam/index.html'), 'utf8');
  assert.match(ex, /data-il-exam-blueprint/);
  assert.match(ex, /data-il-exam-weakest/);
});

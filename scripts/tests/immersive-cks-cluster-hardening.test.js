/**
 * 2026-11-04 Musk-bar pass: CKS track part 4 — Cluster Setup (15% of the CKS): the CIS benchmark with kube-bench, the last
 * CKS topic the manifest listed as not modelled. A NEW authored asset, cks-cluster-hardening.glb (kit-v2 + Blender CLI
 * polish), its rules-engine drill (7 predict checkpoints), a 3-task CLI pack (kubelet auth + restart, etcd data dir + API
 * server profiling, read-only port), and the CKS paper drawing from it. Generic tip/focus/replay/example coverage for the
 * new pack comes from the loops in immersive-cli.test.js / immersive-cli-packs.test.js (19 packs).
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
const C = require(path.join(root, 'docs/assets/il-immersive-cli.js'));
const E = require(path.join(root, 'docs/assets/il-immersive-exam.js'));
const R = require(path.join(root, 'docs/assets/il-immersive-review.js'));
const SIM = 'cks-cluster-hardening';
const KCFG = '/var/lib/kubelet/config.yaml';
const APIM = '/etc/kubernetes/manifests/kube-apiserver.yaml';
const CURL = 'curl -sk https://localhost:10250/pods';
const CURL_RO = 'curl -s http://localhost:10255/pods';

function session(taskId, extra) {
  const tk = taskId ? C.task(SIM, taskId) : null;
  let state = S.merge(S.merge(S.get(SIM).initial, tk ? tk.setup : {}), extra || {});
  const ctx = C.newCtx(taskId);
  return {
    ctx,
    get state() { return state; },
    run(line) { const r = C.run(SIM, state, line, ctx); if (r.set) state = S.merge(state, r.set); return r; },
    status() { return C.taskStatus(SIM, taskId, state, ctx); },
    verdict() { return S.get(SIM).derive(state).verdict; }
  };
}
function glbJson(rel) {
  const buf = readFileSync(path.join(root, 'docs', rel));
  const jl = buf.readUInt32LE(12);
  return JSON.parse(buf.toString('utf8', 20, 20 + jl).trim());
}

test('NEW asset: cks-cluster-hardening.glb is authored + Blender-polished, the fourth CKS scene; sim-* nodes hidden when secure', () => {
  const sim = S.get(SIM);
  assert.ok(['1.10.0', '1.11.0'].includes(S.VERSION), 'cks-cluster-hardening arrived in v1.10.0; v1.11.0 (2026-11-05) keeps it');
  assert.equal(sim.cert, 'CKS');
  assert.equal(sim.glb, '/assets/immersive/cks-cluster-hardening.glb');
  assert.ok(!S.list().filter(id => id !== SIM).map(id => S.get(id).glb).includes(sim.glb), 'a new asset, not a re-read of an existing scene');
  assert.deepEqual(S.list().filter(id => S.get(id).cert === 'CKS'), ['cks-pod-security', 'cks-supply-chain', 'cks-runtime-security', SIM, 'cks-static-analysis']);
  const j = glbJson('assets/immersive/cks-cluster-hardening.glb');
  const names = j.nodes.map(n => n.name);
  for (const n of ['cp-node', 'kube-apiserver', 'apiserver-manifest', 'sim-profiling-on', 'etcd-db', 'etcd-dir', 'sim-etcd-open', 'kubelet', 'kubelet-config', 'sim-stale-config',
    'authn-gate', 'authz-gate', 'port-10250', 'port-10255', 'sim-ro-port-open', 'sim-kubelet-open', 'sim-kubelet-denied', 'kube-bench', 'bench-report', 'sim-bench-fail', 'sim-bench-pass',
    'pod-network', 'attacker-pod', 'sim-attacker-probe', 'edge-kubelet-gates', 'edge-kubelet-sar', 'edge-api-etcd', 'edge-bench-api', 'edge-bench-etcd', 'edge-bench-kubelet',
    'edge-probe-kubelet', 'edge-probe-ro']) assert.ok(names.includes(n), n);
  assert.ok(names.some(n => /_LOD1$/.test(n)), 'Blender CLI polish ran (LOD1 decimate duplicates present)');
  const k = j.nodes.find(n => n.name === 'kubelet');
  assert.equal(k.extras.il.topic, SIM, 'pedagogy extras survive polish');
  assert.equal(k.extras.il.domain, 'cluster-setup');
  assert.equal(j.nodes.find(n => n.name === 'sim-kubelet-open').extras.simOnly, true);
  const base = sim.derive(sim.initial);
  assert.equal(base.verdict, 'healthy');
  for (const n of ['sim-profiling-on', 'sim-etcd-open', 'sim-stale-config', 'sim-ro-port-open', 'sim-kubelet-open', 'sim-kubelet-denied', 'sim-bench-fail', 'sim-bench-pass', 'sim-attacker-probe'])
    assert.equal(S.styleFor(n, base.rules).hide, true, n + ' hidden when secure');
  const at = set => sim.derive(S.merge(sim.initial, set)).rules;
  assert.equal(S.styleFor('sim-kubelet-open', at({ anonOff: false, webhookAuthz: false, probe: true })).hide, false);
  assert.equal(S.styleFor('sim-kubelet-denied', at({ probe: true })).hide, false);
  assert.equal(S.styleFor('sim-ro-port-open', at({ roPortClosed: false })).hide, false);
  assert.equal(S.styleFor('sim-stale-config', at({ kubeletRestarted: false })).hide, false);
  assert.equal(S.styleFor('sim-bench-pass', at({ kubeletRestarted: false })).hide, false, 'a green report next to a stale kubelet');
  assert.equal(S.styleFor('sim-etcd-open', at({ etcdLocked: false })).hide, false);
  assert.equal(S.styleFor('sim-profiling-on', at({ profilingOff: false })).hide, false);
  assert.equal(S.styleFor('sim-bench-fail', at({ profilingOff: false })).hide, false);
});

test('rules engine: authn vs authz, read-only port, restart after edits, CIS ids and results', () => {
  const sim = S.get(SIM);
  const at = set => S.cksHardenDecide(S.merge(sim.initial, set));
  const v = set => sim.derive(S.merge(sim.initial, set)).verdict;
  assert.deepEqual(S.CH_CHECKS.map(c => c.id), ['1.1.11', '1.2.15', '4.2.1', '4.2.2', '4.2.4']);
  assert.equal(at({ anonOff: false, webhookAuthz: false }).kubeletCode, 200);
  const w = at({ anonOff: false });
  assert.deepEqual([w.kubeletCode, w.kubeletMsg], [403, 'Forbidden (user=system:anonymous, verb=get, resource=nodes, subresource=proxy)']);
  assert.deepEqual(w.fails.map(b => b.id + ' ' + b.result), ['4.2.1 FAIL'], 'Webhook saves the day, but anonymous auth is still a FAIL');
  assert.deepEqual([at({}).kubeletCode, at({}).kubeletMsg], [401, 'Unauthorized']);
  assert.equal(at({ webhookAuthz: false, probeToken: true }).kubeletCode, 200, 'any SA token gets in under AlwaysAllow');
  assert.equal(at({ probeToken: true }).kubeletCode, 403);
  assert.deepEqual(at({ roPortClosed: false }).fails.map(b => b.result), ['WARN'], '4.2.4 is a Manual check');
  const stale = at({ kubeletRestarted: false });
  assert.deepEqual([stale.allPass, stale.stale, stale.kubeletCode, stale.roOpen], [true, true, 200, true], 'PASS on file, old config running');
  assert.equal(at({ kubeletRestarted: false, runAnonOff: true, runWebhookAuthz: true, runRoClosed: true }).stale, false, 'snapshot = file → nothing pending');
  assert.equal(v({ anonOff: false, webhookAuthz: false, probe: true }), 'exposed');
  assert.equal(v({ anonOff: false, webhookAuthz: false }), 'degraded', 'a FAIL with nobody probing is a gap');
  assert.equal(v({ etcdLocked: false }), 'degraded');
  assert.equal(v({ roPortClosed: false, probe: true }), 'exposed');
  assert.equal(S.verdictTone(v({ kubeletRestarted: false, probe: true })), 'bad');
  const pre = sim.scenarios.filter(sc => sc.predict);
  assert.equal(pre.length, 7);
  assert.equal(new Set(pre.map(sc => sc.predict.answer)).size, 3, 'keyed answers spread across positions 0-2');
  for (const sc of pre) {
    assert.notEqual(sim.derive(S.merge(sim.initial, sc.set)).verdict, 'healthy', sc.id + ' breaks something');
    assert.ok(sc.predict.why.length > 200, sc.id + ' explains the mechanism');
  }
  assert.match(sim.scenarios.find(s => s.id === 'no-restart').predict.why, /restart/);
  assert.match(sim.scenarios.find(s => s.id === 'readonly-port').predict.why, /Manual/);
});

test('kubelet-auth: FAIL 4.2.1/4.2.2 → 200 PodList → line-addressed sed → restart → 401 → PASS; 7/7', () => {
  const s = session('kubelet-auth');
  assert.equal(s.verdict(), 'degraded');
  const b = s.run('kube-bench run --targets node').out;
  assert.ok(b.includes('[FAIL] 4.2.1 Ensure that the --anonymous-auth argument is set to false (Automated)'));
  assert.ok(b.includes('[FAIL] 4.2.2 Ensure that the --authorization-mode argument is not set to AlwaysAllow (Automated)'));
  assert.ok(b.includes('== Summary node =='));
  assert.ok(b.includes('2 checks FAIL'));
  assert.match(b.join('\n'), /systemctl restart kubelet\.service/);
  assert.match(s.run(CURL).out[0], /^\{"kind":"PodList"/);
  const n = s.run('cat -n ' + KCFG).out;
  assert.match(n[4], /^\s+5\t    enabled: true$/);
  const bad = s.run("sed -i 's/enabled: true/enabled: false/' " + KCFG);
  assert.equal(bad.exit, 1);
  assert.match(bad.out[0], /webhook: enabled: true/);
  assert.equal(s.state.anonOff, false, 'refused edit writes nothing');
  s.run("sed -i '5s/true/false/' " + KCFG);
  s.run("sed -i 's/mode: AlwaysAllow/mode: Webhook/' " + KCFG);
  assert.deepEqual([s.state.anonOff, s.state.webhookAuthz, s.state.kubeletRestarted], [true, true, false]);
  assert.match(s.run(CURL).out[0], /^\{"kind":"PodList"/, 'not restarted: the old config still serves');
  assert.ok(s.run('kube-bench run --targets node --check 4.2.1,4.2.2').out.includes('[PASS] 4.2.1 Ensure that the --anonymous-auth argument is set to false (Automated)'), 'kube-bench reads the file');
  assert.match(s.run('systemctl daemon-reload').out[0], /was not restarted/);
  assert.match(s.run(CURL).out[0], /PodList/);
  s.run('systemctl restart kubelet');
  assert.deepEqual(s.run(CURL).out, ['Unauthorized']);
  assert.equal(s.verdict(), 'healthy');
  assert.equal(s.status().done, false, 'the PASS seen before the restart does not count: re-run after proving the 401');
  s.run('kube-bench run --targets node --check 4.2.1,4.2.2');
  assert.equal(s.status().total, 7);
  assert.equal(s.status().done, true);
});

test('control-plane: FAIL 1.1.11/1.2.15 → stat 755 → chmod 700 → --profiling=false in the static-pod manifest → PASS; 6/6', () => {
  const s = session('control-plane');
  const b = s.run('kube-bench run --targets master').out;
  assert.ok(b.includes('[FAIL] 1.1.11 Ensure that the etcd data directory permissions are set to 700 or more restrictive (Automated)'));
  assert.ok(b.includes('[FAIL] 1.2.15 Ensure that the --profiling argument is set to false (Automated)'));
  assert.deepEqual(s.run('stat -c %a /var/lib/etcd').out, ['755']);
  assert.equal(s.run('chmod 600 /var/lib/etcd').exit, 1, 'owner needs x on a directory');
  s.run('chmod 700 /var/lib/etcd');
  assert.match(s.run('ls -ld /var/lib/etcd').out[0], /^drwx------ /);
  assert.deepEqual(s.run('grep profiling ' + APIM).out, ['    - --profiling=true']);
  assert.equal(s.run('systemctl restart kube-apiserver').exit, 5);
  const ed = s.run("sed -i 's/--profiling=true/--profiling=false/' " + APIM);
  assert.match(ed.out[0], /--profiling=false — the kubelet sees the manifest change and re-creates/);
  const p = s.run('kube-bench run --targets master --check 1.1.11,1.2.15').out;
  assert.ok(p.includes('2 checks PASS'));
  assert.equal(s.verdict(), 'healthy');
  assert.equal(s.status().total, 6);
  assert.equal(s.status().done, true);
});

test('readonly-port: leak over HTTP → [WARN] 4.2.4 → readOnlyPort 0 → restart → connection refused; other kubelet settings stay secure while pending; 5/5', () => {
  const s = session('readonly-port');
  assert.match(s.run(CURL_RO).out[0], /PodList/);
  const w = s.run('kube-bench run --targets node --check 4.2.4').out;
  assert.ok(w.includes('[WARN] 4.2.4 Verify that if defined, the --read-only-port argument is set to 0 (Manual)'));
  assert.ok(w.includes('0 checks FAIL'));
  s.run("sed -i 's/readOnlyPort: 10255/readOnlyPort: 0/' " + KCFG);
  assert.deepEqual(s.run(CURL).out, ['Unauthorized'], 'the running kubelet kept its secure auth settings (snapshot)');
  assert.match(s.run(CURL_RO).out[0], /PodList/, 'port still open until restart');
  s.run('systemctl restart kubelet');
  const c = s.run(CURL_RO);
  assert.equal(c.exit, 7);
  assert.match(c.out[0], /Failed to connect to localhost port 10255/);
  assert.equal(s.status().total, 5);
  assert.equal(s.status().done, true);
});

test('token under AlwaysAllow: anonymous off is not enough', () => {
  const s = session(null, { webhookAuthz: false });
  assert.deepEqual(s.run(CURL).out, ['Unauthorized']);
  assert.match(s.run('curl -sk -H "Authorization: Bearer $TOKEN" https://localhost:10250/pods').out[0], /PodList/);
  s.run('fault authz fix');
  assert.deepEqual(s.run('curl -sk -H "Authorization: Bearer $TOKEN" https://localhost:10250/pods').out, ['Forbidden (user=system:serviceaccount:default:default, verb=get, resource=nodes, subresource=proxy)']);
});

test('honesty: unmodelled forms never invent output; help and note say simulated', () => {
  const s = session();
  assert.equal(s.run('kube-bench run --targets etcd').exit, 2);
  assert.equal(s.run('kube-bench run --targets node --check 4.1.1').exit, 2);
  assert.equal(s.run('curl -sk https://localhost:10250/runningpods').exit, 2);
  assert.equal(s.run('chmod 700 /etc/kubernetes/pki').exit, 2);
  assert.equal(s.run('trivy k8s cluster').exit, 127);
  assert.match(s.run('kube-bench run --targets node').out.join('\n'), /representative kube-bench output/);
  const help = s.run('help').out.join('\n');
  assert.match(help, /Simulated shell/);
  assert.match(help, /no real kube-bench, kubelet, etcd or systemd/);
});

test('CKS paper: Cluster Setup links to the CIS drill, pool +7 (36)', () => {
  assert.ok(['1.6.0', '1.7.0'].includes(E.VERSION));
  const cs = E.CKS_BLUEPRINT.find(b => b.domain === 'Cluster Setup');
  assert.equal(cs.sims[0], SIM);
  for (const sc of S.get(SIM).scenarios.filter(x => x.predict)) assert.equal(E.cksDomain(SIM, sc.id), 'Cluster Setup', sc.id);
  assert.ok(E.CKS_SIMS.includes(SIM));
  assert.equal(E.pool(S, 'CKS').filter(it => it.simId === SIM).length, 7);
  assert.ok(E.pool(S, 'CKS').length >= 36, '36 on 2026-11-04, 43 since 2026-11-05');
  assert.ok(!E.pool(S).some(it => it.simId === SIM), 'the CKA paper never draws a CKS checkpoint');
  for (const seed of [1, 7, 42, 2026]) {
    const ex = E.buildExam(S, { track: 'CKS', seed });
    assert.equal(ex.count, 8);
    assert.equal(new Set(ex.items.map(i => i.domain)).size, 6, 'one item per official domain first (seed ' + seed + ')');
    assert.doesNotMatch(ex.honesty, /not modelled yet/);
  }
  const ex2 = E.buildExam(S, { track: 'CKS', seed: 7 });
  ex2.items.forEach(it => { const miss = it.domain === 'Cluster Setup'; it.choice = miss ? (it.answer + 1) % 3 : it.answer; it.correct = !miss; });
  const bp = E.summarize(ex2).blueprint;
  assert.equal(bp.coveragePct, 100);
  assert.equal(bp.weakest.domain, 'Cluster Setup');
  assert.deepEqual(bp.drill, { sim: SIM, href: '/immersive/#cks-cluster-hardening' });
  assert.match(bp.honesty, /the CIS benchmark \(kube-bench\) since 2026-11-04/);
});

test('review: CIS coach cards get an honest CKS label; CKA mastery stays CKA-only', () => {
  assert.match(R.VERSION, /^1\.3\.[45]$/);
  const cards = R.cliCheckpoints(C, S).filter(c => c.simId === SIM);
  assert.equal(cards.length, 18);
  assert.ok(cards.every(c => c.domain === 'CKS · Cluster setup (CIS benchmark)'));
  assert.ok(!R.checkpoints(S).some(c => c.simId === SIM));
});

test('wiring: /immersive/ host, exam lobby copy, curriculum rows, manifest (new scene, cks_coverage, pack, honest notes)', () => {
  const html = readFileSync(path.join(root, 'docs/immersive/index.html'), 'utf8');
  assert.match(html, /id="cks-cluster-hardening"/);
  assert.match(html, /data-il-sim="cks-cluster-hardening"\s*\n\s*data-gltf="\/assets\/immersive\/cks-cluster-hardening\.glb"/);
  assert.match(html, /no real kube-bench, kubelet, etcd or systemd, and no clock/);
  assert.doesNotMatch(html, /kube-bench is not modelled yet/);
  const exam = readFileSync(path.join(root, 'docs/immersive/exam/index.html'), 'utf8');
  assert.match(exam, /cluster-setup \(added 2026-11-04/);
  assert.doesNotMatch(exam, /kube-bench is not modelled yet/);
  for (const f of ['labs.json', 'mirror.json']) {
    const j = JSON.parse(readFileSync(path.join(root, 'docs/curriculum-os', f), 'utf8'));
    const row = (j.items || j.labs).find(l => l.id === 'lab-sim-cks-cluster-hardening');
    assert.ok(row, f);
    assert.equal(row.gltf, S.get(SIM).glb);
    assert.equal(row.immersive.sim, SIM);
    assert.equal(row.immersive.mode, '3d-first');
    assert.match(row.summary, /no live cluster, real kube-bench, kubelet or etcd/);
  }
  const m = JSON.parse(readFileSync(path.join(root, 'docs/assets/scenes/manifest.json'), 'utf8'));
  const sc = m.scenes.find(x => x.sim === SIM);
  assert.deepEqual([sc.gltf, sc.cert, sc.polish, sc.polishedOn], [S.get(SIM).glb, 'CKS', 'blender-cli', '2026-11-04']);
  assert.ok(m.sims.list.includes(SIM));
  assert.ok(!m.cka_coverage.interactive.includes(SIM), 'not counted as CKA coverage');
  assert.deepEqual(m.cks_coverage.interactive.slice(0, 4), ['cks-pod-security', 'cks-supply-chain', 'cks-runtime-security', SIM]);
  assert.match(m.cks_coverage.covered['Cluster Setup'], /kube-bench/);
  assert.ok(!m.cks_coverage.notCovered.includes('CIS benchmark (kube-bench)'));
  assert.equal(m.cks_coverage.hostedFleet, false);
  assert.equal(m.cks_coverage.liveUnrealHost, false);
  assert.equal(m.sims.runtime_version, S.VERSION);
  assert.equal(m.sims.exam.version, E.VERSION);
  assert.equal(m.sims.cli.version, C.VERSION);
  assert.deepEqual(m.sims.cli.packs.find(p => p.sim === SIM).tasks, ['kubelet-auth', 'control-plane', 'readonly-port']);
  assert.match(m.sims.cli.hardeningNote, /No live cluster, no real kube-bench, kubelet, etcd or systemd, no clock/);
});

test('voice: "kube bench" normalises to kube-bench', () => {
  assert.match(C.fromSpeech('kube bench run dash dash targets node', SIM).line, /^kube-bench run --targets node$/);
});

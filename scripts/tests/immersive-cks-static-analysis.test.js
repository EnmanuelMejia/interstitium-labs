/**
 * 2026-11-05 Musk-bar pass: CKS track part 5 — Supply Chain Security (20% of the CKS): static analysis of user workloads
 * with kubesec and KubeLinter, the first half of the "static analysis of manifests (kubesec / KubeLinter) and keyless
 * signing" item the manifest listed as not modelled. A NEW authored asset, cks-static-analysis.glb (kit-v2 + Blender CLI
 * polish), its rules-engine drill (7 predict checkpoints), a 3-task CLI pack (kubesec + CI gate, KubeLinter fixes, image
 * user vs runAsNonRoot), and the CKS paper drawing from it. Generic tip/focus/replay/example coverage for the new pack
 * comes from the loops in immersive-cli.test.js / immersive-cli-packs.test.js (20 packs).
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
const SIM = 'cks-static-analysis';
const F = 'payments-api.yaml';
const LINT = 'kube-linter lint --config .kube-linter.yaml ' + F;

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
const kubesecJson = r => JSON.parse(r.out.filter(l => !/^\(sim\)/.test(l)).join('\n'));

test('NEW asset: cks-static-analysis.glb is authored + Blender-polished, the fifth CKS scene; sim-* nodes hidden when secure', () => {
  const sim = S.get(SIM);
  assert.equal(S.VERSION, '1.11.0');
  assert.equal(sim.cert, 'CKS');
  assert.equal(sim.glb, '/assets/immersive/cks-static-analysis.glb');
  assert.ok(!S.list().filter(id => id !== SIM).map(id => S.get(id).glb).includes(sim.glb), 'a new asset, not a re-read of an existing scene');
  assert.deepEqual(S.list().filter(id => S.get(id).cert === 'CKS'), ['cks-pod-security', 'cks-supply-chain', 'cks-runtime-security', 'cks-cluster-hardening', SIM]);
  const j = glbJson('assets/immersive/cks-static-analysis.glb');
  const names = j.nodes.map(n => n.name);
  for (const n of ['git-repo', 'manifest-file', 'field-privileged', 'field-nonroot', 'field-rootfs', 'field-resources', 'field-secret', 'field-image', 'lint-ignore', 'sim-secret-leak',
    'kubesec', 'kubesec-score', 'sim-kubesec-critical', 'kube-linter', 'lint-report', 'sim-lint-fail', 'ci-pipeline', 'ci-gate', 'sim-gate-block', 'sim-gate-bypass',
    'kube-apiserver', 'ns-payments', 'image-layer', 'payments-pod', 'sim-ccce', 'sim-privileged-flare',
    'edge-manifest-kubesec', 'edge-manifest-linter', 'edge-scan-gate', 'edge-gate-api', 'edge-api-pod']) assert.ok(names.includes(n), n);
  assert.ok(names.some(n => /_LOD1$/.test(n)), 'Blender CLI polish ran (LOD1 decimate duplicates present)');
  const k = j.nodes.find(n => n.name === 'kubesec');
  assert.equal(k.extras.il.topic, SIM, 'pedagogy extras survive polish');
  assert.equal(k.extras.il.domain, 'supply-chain-security');
  assert.equal(j.nodes.find(n => n.name === 'sim-gate-bypass').extras.simOnly, true);
  const base = sim.derive(sim.initial);
  assert.equal(base.verdict, 'healthy');
  for (const n of ['sim-secret-leak', 'sim-kubesec-critical', 'sim-lint-fail', 'sim-gate-block', 'sim-gate-bypass', 'sim-ccce', 'sim-privileged-flare'])
    assert.equal(S.styleFor(n, base.rules).hide, true, n + ' hidden when secure');
  const at = set => sim.derive(S.merge(sim.initial, set)).rules;
  assert.equal(S.styleFor('sim-kubesec-critical', at({ privOff: false })).hide, false);
  assert.equal(S.styleFor('sim-gate-block', at({ privOff: false })).hide, false);
  assert.equal(S.styleFor('sim-privileged-flare', at({ privOff: false })).hide, true, 'the gate holds: nothing privileged runs');
  assert.equal(S.styleFor('sim-privileged-flare', at({ privOff: false, ciGate: false })).hide, false);
  assert.equal(S.styleFor('sim-gate-bypass', at({ privOff: false, ciGate: false })).hide, false);
  assert.equal(S.styleFor('sim-secret-leak', at({ secretRef: false, ciGate: false })).hide, false);
  assert.equal(S.styleFor('sim-lint-fail', at({ secretRef: false })).hide, false);
  assert.equal(S.styleFor('sim-ccce', at({ pinned: false, ciGate: false })).hide, false);
});

test('rules engine: kubesec sums points (exit 2 at ≤ 0), KubeLinter checks, gate vs || true, kubelet image-user check', () => {
  const sim = S.get(SIM);
  const at = set => S.cksStaticDecide(S.merge(sim.initial, set));
  const v = set => sim.derive(S.merge(sim.initial, set)).verdict;
  const ok = at({});
  assert.deepEqual([ok.score, ok.kubesecMsg, ok.kubesecExit, ok.lint.length], [6, 'Passed with a score of 6 points', 0, 0]);
  assert.deepEqual(ok.critical.map(r => r.id), ['SecretsAsEnvironmentVariables'], 'kubesec scores secretKeyRef env at -5');
  assert.deepEqual(ok.passed.map(r => r.points).reduce((a, b) => a + b, 0), 11);
  const priv = at({ privOff: false });
  assert.deepEqual([priv.score, priv.kubesecMsg, priv.kubesecExit], [-24, 'Failed with a score of -24 points', 2]);
  assert.deepEqual(priv.lint.map(l => l.check), ['privileged-container', 'privilege-escalation-container']);
  assert.deepEqual(at({ privOff: false, noIgnore: false }).lint.map(l => l.check), ['privilege-escalation-container'], 'the annotation silences one check only');
  const lit = at({ secretRef: false });
  assert.deepEqual([lit.score, lit.kubesecExit], [11, 0], 'kubesec cannot see a literal secret; the score goes up');
  assert.deepEqual(lit.lint.map(l => l.check), ['env-var-secret']);
  assert.equal(lit.lint[0].msg, 'environment variable PAYMENTS_API_SECRET in container "api" found');
  assert.deepEqual([at({ requestsSet: false, limitsSet: false }).score, at({ requestsSet: false, limitsSet: false }).kubesecExit], [2, 0], 'advice costs nothing');
  assert.deepEqual(at({ requestsSet: false, limitsSet: false }).lint.map(l => l.msg), ['container "api" has cpu request 0', 'container "api" has memory limit 0']);
  assert.equal(at({ roRoot: false }).kubesecMsg, 'Passed with a score of 5 points', 'a critical entry under a passing score');
  assert.deepEqual([at({ pinned: false }).ccce, at({ pinned: false, ciGate: false }).ccce], [false, true], 'gated: latest-tag stops it before the kubelet ever sees it');
  assert.deepEqual([at({ nonRoot: false, pinned: false, ciGate: false }).ccce], [false], 'no runAsNonRoot → root runs (and KubeLinter says so)');
  assert.equal(at({ privOff: false }).podStatus, 'Running (previous revision — the gate stopped this one)');
  assert.equal(v({ privOff: false }), 'degraded', 'blocked: red pipeline, nothing unsafe running');
  assert.equal(v({ privOff: false, ciGate: false }), 'exposed');
  assert.equal(v({ secretRef: false, ciGate: false }), 'exposed');
  assert.equal(v({ pinned: false, ciGate: false }), 'degraded');
  assert.equal(S.verdictTone(v({ privOff: false, ciGate: false })), 'bad');
  const pre = sim.scenarios.filter(sc => sc.predict);
  assert.equal(pre.length, 7);
  assert.equal(new Set(pre.map(sc => sc.predict.answer)).size, 3, 'keyed answers spread across positions 0-2');
  for (const sc of pre) {
    assert.notEqual(sim.derive(S.merge(sim.initial, sc.set)).verdict, 'healthy', sc.id + ' breaks something');
    assert.ok(sc.predict.why.length > 200, sc.id + ' explains the mechanism');
  }
  assert.match(sim.scenarios.find(s => s.id === 'privileged').predict.options[1], /-24 points/);
  assert.match(sim.scenarios.find(s => s.id === 'nonroot-runtime').predict.why, /kubelet/);
});

test('kubesec-gate: Failed -24 → ungated CI ships it → remove || true → gate blocks → privileged false → Passed → ship; 7/7', () => {
  const s = session('kubesec-gate');
  assert.equal(s.verdict(), 'exposed');
  const r = s.run('kubesec scan ' + F);
  assert.equal(r.exit, 2);
  const j = kubesecJson(r);
  assert.equal(j[0].object, 'Deployment/payments-api.payments');
  assert.equal(j[0].message, 'Failed with a score of -24 points');
  assert.deepEqual(j[0].scoring.critical.map(x => [x.id, x.points]), [['Privileged', -30], ['SecretsAsEnvironmentVariables', -5]]);
  const ci = s.run('./ci/lint.sh');
  assert.equal(ci.exit, 0);
  assert.match(ci.out.join('\n'), /\|\| true swallowed the findings/);
  assert.equal(s.run("sed -i '3s/ || true//' ci/lint.sh").exit, 1, 'line addresses are not modelled in this pack: refused, nothing written');
  assert.equal(s.state.ciGate, false);
  s.run("sed -i 's/ || true//' ci/lint.sh");
  assert.equal(s.state.ciGate, true);
  assert.deepEqual(s.run('cat ci/lint.sh').out.slice(2, 4), ['kubesec scan ' + F, 'kube-linter lint --config .kube-linter.yaml ' + F]);
  const blk = s.run('./ci/lint.sh');
  assert.equal(blk.exit, 2);
  assert.match(blk.out.join('\n'), /kubectl apply never ran/);
  assert.equal(s.verdict(), 'degraded');
  s.run("sed -i 's/privileged: true/privileged: false/' " + F);
  assert.equal(kubesecJson(s.run('kubesec scan ' + F))[0].message, 'Passed with a score of 6 points');
  s.run('./ci/lint.sh');
  assert.equal(s.verdict(), 'healthy');
  assert.equal(s.status().total, 7);
  assert.equal(s.status().done, true);
});

test('kube-linter: ignore annotation still fails privilege-escalation → delete it, fix privileged, secretKeyRef, pin → No lint errors found!; 6/6', () => {
  const s = session('kube-linter');
  const r = s.run(LINT);
  assert.equal(r.exit, 1);
  const out = r.out.join('\n');
  assert.doesNotMatch(out, /check: privileged-container/, 'silenced by the annotation');
  assert.match(out, /payments-api\.yaml: \(object: payments\/payments-api apps\/v1, Kind=Deployment\) container "api" is Privileged hence allows privilege escalation\. \(check: privilege-escalation-container, remediation: /);
  assert.match(out, /\(check: env-var-secret,/);
  assert.match(out, /\(check: latest-tag,/);
  assert.match(out, /Error: found 3 lint errors/);
  s.run("sed -i '/ignore-check/d' " + F);
  assert.ok(!s.run('cat ' + F).out.some(l => /annotations:|ignore-check/.test(l)), 'no dangling annotations key');
  assert.match(s.run(LINT).out.join('\n'), /check: privileged-container/, 'with the annotation gone, both checks fire');
  s.run("sed -i 's/privileged: true/privileged: false/' " + F);
  assert.equal(s.run("sed -i 's/sk_live_lab_only/hunter2/' " + F).exit, 1, 'unmodelled values are refused, not invented');
  s.run("sed -i 's/value: \"sk_live_lab_only\"/valueFrom: {secretKeyRef: {name: payments-api, key: api-secret}}/' " + F);
  s.run("sed -i 's/payments-api:latest/payments-api:1.4.2/' " + F);
  assert.deepEqual(s.run(LINT).out.slice(-1), ['No lint errors found!']);
  assert.equal(s.status().total, 6);
  assert.equal(s.status().done, true);
  assert.match(s.run('kube-linter lint ' + F).out.join('\n'), /without --config the real tool also runs its other default checks/);
});

test('image-user: apply → CreateContainerConfigError (old pods serve) → kubelet reason → lint sees only latest-tag → pin → Running; 7/7', () => {
  const s = session('image-user');
  assert.match(s.run('kubectl get pods -n payments').out.join('\n'), /previous revision/);
  s.run('kubectl apply -f ' + F);
  const pods = s.run('kubectl get pods -n payments').out;
  assert.equal(pods.filter(l => / Running /.test(l)).length, 2, 'maxUnavailable rounds down to 0: both old pods keep serving');
  assert.ok(pods.some(l => /0\/1\s+CreateContainerConfigError/.test(l)));
  assert.match(s.run('kubectl describe pod -n payments -l app=payments-api').out.join('\n'), /kubelet  Error: container has runAsNonRoot and image will run as root \(pod: "payments-api-[a-z0-9-]+_payments\(/);
  assert.equal(kubesecJson(s.run('kubesec scan ' + F))[0].message, 'Passed with a score of 6 points', 'kubesec cannot see the image user');
  const l = s.run(LINT).out.join('\n');
  assert.match(l, /check: latest-tag/);
  assert.doesNotMatch(l, /run-as-non-root/, 'the manifest is fine; the image is not');
  s.run("sed -i 's/payments-api:latest/payments-api:1.4.2/' " + F);
  s.run('kubectl apply -f ' + F);
  const ok = s.run('kubectl get pods -n payments').out;
  assert.equal(ok.filter(x => /1\/1\s+Running/.test(x)).length, 2);
  assert.ok(!ok.some(x => /CreateContainerConfigError|5f6b7c9d4/.test(x)));
  assert.equal(s.status().total, 7);
  assert.equal(s.status().done, true);
  assert.equal(s.verdict(), 'healthy');
});

test('honesty: unmodelled forms never invent output; help and note say simulated', () => {
  const s = session();
  assert.equal(s.run('kubesec scan other.yaml').exit, 2);
  assert.equal(s.run('kube-linter checks list').exit, 2);
  assert.equal(s.run('kube-linter lint --config nope.yaml ' + F).exit, 1);
  assert.equal(s.run('sed -i s/a/b/ Dockerfile').exit, 2);
  assert.equal(s.run('hadolint Dockerfile').exit, 127);
  assert.match(s.run('kubesec scan ' + F).out.join('\n'), /\(sim\) representative kubesec v2 report/);
  assert.equal(s.run("sed -i 's/privileged: false/privileged: maybe/' " + F).exit, 1);
  assert.equal(s.state.privOff, true, 'refused edit writes nothing');
  const help = s.run('help').out.join('\n');
  assert.match(help, /Simulated shell/);
  assert.match(help, /no real kubesec, KubeLinter, CI runner or kubelet/);
});

test('CKS paper: the 7 checkpoints count for Supply Chain Security, gap link stays on cks-supply-chain, pool +7 (43)', () => {
  assert.equal(E.VERSION, '1.7.0');
  const sc = E.CKS_BLUEPRINT.find(b => b.domain === 'Supply Chain Security');
  assert.deepEqual(sc.sims, ['cks-supply-chain', SIM]);
  for (const x of S.get(SIM).scenarios.filter(y => y.predict)) assert.equal(E.cksDomain(SIM, x.id), 'Supply Chain Security', x.id);
  assert.ok(E.CKS_SIMS.includes(SIM));
  assert.equal(E.pool(S, 'CKS').filter(it => it.simId === SIM).length, 7);
  assert.equal(E.pool(S, 'CKS').length, 43);
  assert.ok(!E.pool(S).some(it => it.simId === SIM), 'the CKA paper never draws a CKS checkpoint');
  for (const seed of [1, 7, 42, 2026]) {
    const ex = E.buildExam(S, { track: 'CKS', seed });
    assert.equal(ex.count, 8);
    assert.equal(new Set(ex.items.map(i => i.domain)).size, 6, 'one item per official domain first (seed ' + seed + ')');
    assert.match(ex.honesty, /kubesec and KubeLinter run on a rules engine/);
  }
  const ex2 = E.buildExam(S, { track: 'CKS', seed: 7 });
  ex2.items.forEach(it => { const miss = it.domain === 'Supply Chain Security'; it.choice = miss ? (it.answer + 1) % 3 : it.answer; it.correct = !miss; });
  const bp = E.summarize(ex2).blueprint;
  assert.equal(bp.coveragePct, 100);
  assert.equal(bp.weakest.domain, 'Supply Chain Security');
  assert.deepEqual(bp.drill, { sim: 'cks-supply-chain', href: '/immersive/#cks-supply-chain' });
  assert.match(bp.honesty, /static analysis \(kubesec, KubeLinter\) since 2026-11-05/);
});

test('review: static-analysis coach cards get an honest CKS label; CKA mastery stays CKA-only', () => {
  assert.equal(R.VERSION, '1.3.5');
  const cards = R.cliCheckpoints(C, S).filter(c => c.simId === SIM);
  assert.equal(cards.length, 20);
  assert.ok(cards.every(c => c.domain === 'CKS · Supply chain (static analysis)'));
  assert.ok(!R.checkpoints(S).some(c => c.simId === SIM));
});

test('wiring: /immersive/ host, exam lobby copy, curriculum rows, manifest (new scene, cks_coverage, pack, honest notes)', () => {
  const html = readFileSync(path.join(root, 'docs/immersive/index.html'), 'utf8');
  assert.match(html, /id="cks-static-analysis"/);
  assert.match(html, /data-il-sim="cks-static-analysis"\s*\n\s*data-gltf="\/assets\/immersive\/cks-static-analysis\.glb"/);
  assert.match(html, /no real kubesec, KubeLinter, CI runner or kubelet, and no clock/);
  const exam = readFileSync(path.join(root, 'docs/immersive/exam/index.html'), 'utf8');
  assert.match(exam, /static-analysis \(added 2026-11-05/);
  for (const f of ['labs.json', 'mirror.json']) {
    const j = JSON.parse(readFileSync(path.join(root, 'docs/curriculum-os', f), 'utf8'));
    const row = (j.items || j.labs).find(l => l.id === 'lab-sim-cks-static-analysis');
    assert.ok(row, f);
    assert.equal(row.gltf, S.get(SIM).glb);
    assert.equal(row.immersive.sim, SIM);
    assert.equal(row.immersive.mode, '3d-first');
    assert.match(row.summary, /no live cluster, real kubesec, KubeLinter or CI runner/);
  }
  const m = JSON.parse(readFileSync(path.join(root, 'docs/assets/scenes/manifest.json'), 'utf8'));
  const sc = m.scenes.find(x => x.sim === SIM);
  assert.deepEqual([sc.gltf, sc.cert, sc.polish, sc.polishedOn], [S.get(SIM).glb, 'CKS', 'blender-cli', '2026-11-05']);
  assert.ok(m.sims.list.includes(SIM));
  assert.ok(!m.cka_coverage.interactive.includes(SIM), 'not counted as CKA coverage');
  assert.deepEqual(m.cks_coverage.interactive, ['cks-pod-security', 'cks-supply-chain', 'cks-runtime-security', 'cks-cluster-hardening', SIM]);
  assert.match(m.cks_coverage.covered['Supply Chain Security'], /kubesec and KubeLinter/);
  assert.ok(!m.cks_coverage.notCovered.some(x => /^static analysis of manifests \(kubesec \/ KubeLinter\)/.test(x)));
  assert.ok(m.cks_coverage.notCovered.some(x => /keyless \(Sigstore OIDC\) signing/.test(x)), 'keyless signing still honestly missing');
  assert.equal(m.cks_coverage.hostedFleet, false);
  assert.equal(m.cks_coverage.liveUnrealHost, false);
  assert.equal(m.sims.runtime_version, S.VERSION);
  assert.equal(m.sims.exam.version, E.VERSION);
  assert.equal(m.sims.cli.version, C.VERSION);
  assert.deepEqual(m.sims.cli.packs.find(p => p.sim === SIM).tasks, ['kubesec-gate', 'kube-linter', 'image-user']);
  assert.match(m.sims.cli.staticAnalysisNote, /No live cluster, no real kubesec, KubeLinter, CI runner or kubelet, no clock/);
});

test('voice: "kube linter" and "kube sec" normalise to the binaries', () => {
  assert.match(C.fromSpeech('kube linter lint payments-api dot yaml', SIM).line, /^kube-linter lint payments-api\.yaml$/);
  assert.match(C.fromSpeech('kube sec scan payments-api dot yaml', SIM).line, /^kubesec scan payments-api\.yaml$/);
});

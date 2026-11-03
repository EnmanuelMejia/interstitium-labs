/**
 * 2026-11-03 Musk-bar pass: CKS track part 3 — Monitoring, Logging & Runtime Security (20% of the CKS), which rested on
 * one audit-log checkpoint, plus AppArmor (System Hardening). A NEW authored asset, cks-runtime-security.glb (kit-v2 +
 * Blender CLI polish), its rules-engine drill (7 predict checkpoints), a 3-task CLI pack (Falco rule override, AppArmor
 * profile load, incident containment with readOnlyRootFilesystem), and the CKS paper drawing from it. Generic
 * tip/focus/replay/example coverage for the new pack comes from the loops in immersive-cli.test.js /
 * immersive-cli-packs.test.js (18 packs).
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
const SIM = 'cks-runtime-security';
const RULES = '/etc/falco/falco_rules.local.yaml';
const PROFILE = '/etc/apparmor.d/k8s-deny-write';
const TOUCH = 'kubectl exec -n payments deploy/payments-api -- touch /usr/local/bin/miner';

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

test('NEW asset: cks-runtime-security.glb is authored + Blender-polished, the third CKS scene; sim-* nodes hidden when secure', () => {
  const sim = S.get(SIM);
  assert.equal(S.VERSION, '1.9.0');
  assert.equal(sim.cert, 'CKS');
  assert.equal(sim.glb, '/assets/immersive/cks-runtime-security.glb');
  assert.ok(!S.list().filter(id => id !== SIM).map(id => S.get(id).glb).includes(sim.glb), 'a new asset, not a re-read of an existing scene');
  assert.deepEqual(S.list().filter(id => S.get(id).cert === 'CKS'), ['cks-pod-security', 'cks-supply-chain', SIM]);
  const j = glbJson('assets/immersive/cks-runtime-security.glb');
  const names = j.nodes.map(n => n.name);
  for (const n of ['node01', 'node-kernel', 'syscall-stream', 'falco-ds', 'falco-rules', 'falco-alerts', 'sim-falco-alert', 'sim-falco-blind', 'edge-kernel-falco', 'edge-falco-out',
    'apparmor-profile', 'sim-apparmor-missing', 'kube-apiserver', 'audit-log', 'sim-exec-recorded', 'edge-api-audit', 'ns-payments', 'rootfs-layer', 'payments-pod', 'apparmor-shield',
    'sim-attacker-shell', 'sim-rootfs-write', 'sim-write-denied', 'edge-shell-pod', 'edge-pod-kernel', 'edge-exec-api']) assert.ok(names.includes(n), n);
  assert.ok(names.some(n => /_LOD1$/.test(n)), 'Blender CLI polish ran (LOD1 decimate duplicates present)');
  const pod = j.nodes.find(n => n.name === 'payments-pod');
  assert.equal(pod.extras.il.topic, SIM, 'pedagogy extras survive polish');
  assert.equal(pod.extras.il.domain, 'runtime-security');
  assert.equal(j.nodes.find(n => n.name === 'sim-falco-alert').extras.simOnly, true);
  const base = sim.derive(sim.initial);
  assert.equal(base.verdict, 'healthy');
  for (const n of ['sim-falco-alert', 'sim-falco-blind', 'sim-apparmor-missing', 'sim-exec-recorded', 'sim-attacker-shell', 'sim-rootfs-write', 'sim-write-denied']) assert.equal(S.styleFor(n, base.rules).hide, true, n + ' hidden when secure');
  const at = set => sim.derive(S.merge(sim.initial, set)).rules;
  assert.equal(S.styleFor('sim-falco-alert', at({ intrusion: true })).hide, false);
  assert.equal(S.styleFor('sim-falco-blind', at({ shellRule: false })).hide, false);
  assert.equal(S.styleFor('sim-apparmor-missing', at({ profileLoaded: false })).hide, false);
  assert.equal(S.styleFor('sim-rootfs-write', at({ intrusion: true, readOnlyRoot: false, apparmor: false })).hide, false);
  assert.equal(S.styleFor('sim-write-denied', at({ intrusion: true })).hide, false);
  assert.equal(S.styleFor('sim-exec-recorded', at({ intrusion: true, viaExec: true })).hide, false);
  assert.equal(S.styleFor('sim-exec-recorded', at({ intrusion: true, viaExec: false })).hide, true, 'an app-exploit shell makes no API request');
});

test('rules engine: detection ≠ prevention, rule overrides, AppArmor load + deny, read-only rootfs, audit vs runtime', () => {
  const sim = S.get(SIM);
  const at = set => S.cksRuntimeDecide(S.merge(sim.initial, set));
  const v = set => sim.derive(S.merge(sim.initial, set)).verdict;
  const blind = at({ intrusion: true, falco: false, apparmor: false, readOnlyRoot: false });
  assert.deepEqual([blind.detected, blind.dropped, blind.auditSeen, blind.exposures], [false, true, false, ['binary-dropped', 'no-runtime-visibility']]);
  const det = at({ intrusion: true, viaExec: true, apparmor: false, readOnlyRoot: false });
  assert.deepEqual([det.detected, det.dropped, det.auditSeen], [true, true, true], 'Falco alerts; the write still succeeds');
  assert.equal(at({ intrusion: true, shellRule: false }).detected, false, 'a disabled rule detects nothing');
  const stuck = at({ profileLoaded: false });
  assert.deepEqual([stuck.newPods, stuck.rolloutStuck, stuck.aaActive], ['CreateContainerError', true, false]);
  assert.equal(at({ intrusion: true, readOnlyRoot: false, profileLoaded: false }).dropped, true, 'old pods without the profile are not protected');
  assert.equal(at({ intrusion: true, readOnlyRoot: false }).writeError, 'Permission denied');
  assert.equal(at({ intrusion: true, apparmor: false }).writeError, 'Read-only file system');
  assert.equal(v({ intrusion: true, apparmor: false, readOnlyRoot: false }), 'exposed');
  assert.equal(v({ intrusion: true }), 'degraded', 'detected and write-blocked, but an attacker is still inside');
  assert.equal(v({ profileLoaded: false }), 'degraded');
  assert.equal(v({ falco: false }), 'degraded', 'a missing control is a gap even when nothing happened');
  assert.equal(S.verdictTone(v({ intrusion: true, falco: false })), 'bad');
  const pre = sim.scenarios.filter(sc => sc.predict);
  assert.equal(pre.length, 7);
  assert.equal(new Set(pre.map(sc => sc.predict.answer)).size, 3, 'keyed answers spread across positions 0-2');
  for (const sc of pre) {
    assert.notEqual(sim.derive(S.merge(sim.initial, sc.set)).verdict, 'healthy', sc.id + ' breaks something');
    assert.ok(sc.predict.why.length > 200, sc.id + ' explains the mechanism');
  }
  assert.match(sim.scenarios.find(s => s.id === 'apparmor-not-loaded').predict.why, /appArmorProfile/);
  assert.match(sim.scenarios.find(s => s.id === 'audit-exec').predict.why, /not audited/);
});

test('falco-detect: Running pod, quiet logs → enabled: false override → sed -i → Warning alert; 5/5', () => {
  const s = session('falco-detect');
  assert.equal(s.verdict(), 'exposed');
  assert.match(s.run('kubectl get pods -n falco').out[1], /^falco-7xk2m\s+2\/2\s+Running/);
  const q = s.run('kubectl logs -n falco ds/falco');
  assert.ok(!q.out.some(l => /Warning Shell spawned/.test(l)));
  assert.match(q.out.join('\n'), /Loading rules from: \/etc\/falco\/falco_rules\.yaml, \/etc\/falco\/falco_rules\.local\.yaml/);
  const rules = s.run('cat ' + RULES).out;
  assert.ok(rules.includes('  enabled: false'));
  assert.ok(rules.includes('- rule: Shell in container'));
  assert.equal(s.run("sed -i 's/enabled: false/enabled: maybe/' " + RULES).exit, 1, 'an invalid value is refused');
  assert.equal(s.state.shellRule, false);
  s.run("sed -i 's/enabled: false/enabled: true/' " + RULES);
  assert.equal(s.state.shellRule, true);
  const a = s.run('kubectl logs -n falco ds/falco');
  assert.ok(a.out.some(l => /: Warning Shell spawned in a container \(user=root k8s\.ns=payments k8s\.pod=payments-api-\S+ proc\.cmdline=sh\)$/.test(l)));
  assert.match(a.out.join(' '), /representative Falco output/);
  assert.equal(s.verdict(), 'degraded');
  assert.equal(s.status().total, 5);
  assert.equal(s.status().done, true);
});

test('apparmor: profile → rollout stalls in CreateContainerError → aa-status → apparmor_parser → Permission denied; 6/6', () => {
  const s = session('apparmor');
  assert.match(s.run('cat ' + PROFILE).out.join('\n'), /deny \/\*\* w,/);
  assert.match(s.run('cat payments-api-apparmor.yaml').out.join('\n'), /appArmorProfile:\n\s+type: Localhost\n\s+localhostProfile: k8s-deny-write/);
  const ap = s.run('kubectl apply -f payments-api-apparmor.yaml');
  assert.match(ap.out.join(' '), /old pods keep serving/);
  const pods = s.run('kubectl get pods -n payments').out;
  assert.equal(pods.filter(l => /Running/.test(l)).length, 2, 'the old ReplicaSet keeps serving');
  assert.ok(pods.some(l => /0\/1\s+CreateContainerError/.test(l)));
  assert.match(s.run('kubectl describe pod -n payments').out.join('\n'), /apparmor profile not found k8s-deny-write/);
  assert.ok(!s.run('aa-status').out.some(l => /k8s-deny-write/.test(l)));
  assert.equal(s.run(TOUCH).exit, 0, 'before the profile loads, the old pods are unconfined');
  s.run('apparmor_parser -q ' + PROFILE);
  assert.ok(s.run('aa-status').out.some(l => /^\s+k8s-deny-write$/.test(l)));
  assert.equal(s.run('kubectl get pods -n payments').out.length, 3, 'rollout finished');
  const w = s.run(TOUCH);
  assert.deepEqual([w.out[0], w.exit], ['touch: /usr/local/bin/miner: Permission denied', 1]);
  assert.match(w.out.join(' '), /apparmor="DENIED"/);
  assert.equal(s.verdict(), 'degraded', 'still a writable root filesystem (a gap, not an exposure)');
  assert.equal(s.status().total, 6);
  assert.equal(s.status().done, true);
});

test('contain: alert → evidence → pods/exec audit event → readOnlyRootFilesystem replaces pods → Read-only file system; 5/5', () => {
  const s = session('contain');
  assert.equal(s.verdict(), 'exposed');
  assert.ok(s.run('kubectl logs -n falco ds/falco').out.some(l => /Warning Shell spawned/.test(l)));
  assert.deepEqual(s.run('kubectl exec -n payments deploy/payments-api -- ls /usr/local/bin').out, ['miner']);
  const au = s.run('grep pods/exec /var/log/kubernetes/audit/audit.log');
  const ev = JSON.parse(au.out[0]);
  assert.deepEqual([ev.apiVersion, ev.verb, ev.objectRef.subresource, ev.user.username], ['audit.k8s.io/v1', 'create', 'exec', 'ci-deployer']);
  assert.match(au.out[1], /commands typed inside the stream are not in any audit level/);
  const y = s.run('cat payments-api-readonly.yaml').out.join('\n');
  assert.match(y, /readOnlyRootFilesystem: true/);
  assert.match(y, /mountPath: \/tmp\n[\s\S]*emptyDir: \{\}/);
  const ap = s.run('kubectl apply -f payments-api-readonly.yaml');
  assert.match(ap.out.join(' '), /collect evidence first/);
  assert.deepEqual([s.state.readOnlyRoot, s.state.intrusion], [true, false]);
  const w = s.run(TOUCH);
  assert.deepEqual([w.out[0], w.exit], ['touch: /usr/local/bin/miner: Read-only file system', 1]);
  assert.equal(s.run('kubectl exec -n payments deploy/payments-api -- touch /tmp/scratch').exit, 0, '/tmp is the emptyDir');
  assert.equal(s.status().total, 5);
  assert.equal(s.status().done, true);
});

test('app-exploit shell: the audit log has nothing; no Falco means no alert', () => {
  const s = session(null, { intrusion: true, viaExec: false, falco: false });
  assert.equal(s.run('grep pods/exec /var/log/kubernetes/audit/audit.log').exit, 1);
  assert.match(s.run('grep pods/exec /var/log/kubernetes/audit/audit.log').out[0], /application exploit, which makes no API request/);
  assert.equal(s.run('kubectl logs -n falco ds/falco').exit, 1);
  assert.match(s.run('kubectl get pods -n falco').out[0], /No resources found/);
});

test('honesty: unmodelled forms never invent output; help and note say simulated', () => {
  const s = session();
  assert.equal(s.run('kubectl logs -n payments deploy/payments-api').exit, 2);
  assert.equal(s.run('kubectl exec -n payments deploy/payments-api -- cat /etc/shadow').exit, 2);
  assert.equal(s.run('falcoctl artifact list').exit, 127);
  assert.equal(s.run('apparmor_parser -q /etc/apparmor.d/other').exit, 2);
  const help = s.run('help').out.join('\n');
  assert.match(help, /Simulated shell/);
  assert.match(help, /no real Falco, kernel, eBPF probe or AppArmor/);
  assert.match(C.pack(SIM).note, /computed by the rules engine/);
});

test('CKS paper: Monitoring links to the runtime drill, AppArmor counts for System Hardening, pool +7', () => {
  assert.equal(E.VERSION, '1.5.0');
  assert.equal(E.CKS_BLUEPRINT.find(b => b.domain === 'Monitoring, Logging & Runtime Security').sims[0], SIM);
  assert.ok(E.CKS_BLUEPRINT.find(b => b.domain === 'System Hardening').sims.includes(SIM));
  assert.equal(E.cksDomain(SIM, 'apparmor-not-loaded'), 'System Hardening');
  assert.equal(E.cksDomain(SIM, 'apparmor-deny-write'), 'System Hardening');
  for (const id of ['rce-blind', 'falco-alert', 'rule-disabled', 'readonly-root', 'audit-exec']) assert.equal(E.cksDomain(SIM, id), 'Monitoring, Logging & Runtime Security', id);
  assert.equal(E.cksDomain('cks-pod-security', 'audit-off'), 'Monitoring, Logging & Runtime Security');
  assert.ok(E.CKS_SIMS.includes(SIM));
  assert.equal(E.pool(S, 'CKS').filter(it => it.simId === SIM).length, 7);
  assert.equal(E.pool(S, 'CKS').length, 29);
  assert.ok(!E.pool(S).some(it => it.simId === SIM), 'the CKA paper never draws a CKS checkpoint');
  for (const seed of [1, 7, 42, 2026]) {
    const ex = E.buildExam(S, { track: 'CKS', seed });
    assert.equal(ex.count, 8);
    assert.equal(new Set(ex.items.map(i => i.domain)).size, 6, 'one item per official domain first (seed ' + seed + ')');
    assert.match(ex.honesty, /kube-bench is not modelled yet/);
  }
  const ex2 = E.buildExam(S, { track: 'CKS', seed: 7 });
  ex2.items.forEach(it => { const miss = it.domain === 'Monitoring, Logging & Runtime Security'; it.choice = miss ? (it.answer + 1) % 3 : it.answer; it.correct = !miss; });
  const bp = E.summarize(ex2).blueprint;
  assert.equal(bp.coveragePct, 100);
  assert.equal(bp.weakest.domain, 'Monitoring, Logging & Runtime Security');
  assert.deepEqual(bp.drill, { sim: SIM, href: '/immersive/#cks-runtime-security' });
  assert.match(bp.honesty, /Falco runtime detection and AppArmor are simulated since 2026-11-03/);
});

test('review: runtime coach cards get an honest CKS label; CKA mastery stays CKA-only', () => {
  assert.equal(R.VERSION, '1.3.3');
  const cards = R.cliCheckpoints(C, S).filter(c => c.simId === SIM);
  assert.equal(cards.length, 16);
  assert.ok(cards.every(c => c.domain === 'CKS · Runtime security'));
  assert.ok(!R.checkpoints(S).some(c => c.simId === SIM));
});

test('wiring: /immersive/ host, exam lobby copy, curriculum rows, manifest (new scene, cks_coverage, pack, honest notes)', () => {
  const html = readFileSync(path.join(root, 'docs/immersive/index.html'), 'utf8');
  assert.match(html, /id="cks-runtime-security"/);
  assert.match(html, /data-il-sim="cks-runtime-security"\s*\n\s*data-gltf="\/assets\/immersive\/cks-runtime-security\.glb"/);
  assert.match(html, /no real Falco, kernel, eBPF probe or AppArmor, and no clock/);
  assert.doesNotMatch(html, /Falco, AppArmor and kube-bench are not modelled yet/);
  const exam = readFileSync(path.join(root, 'docs/immersive/exam/index.html'), 'utf8');
  assert.match(exam, /runtime-security \(added 2026-11-03/);
  for (const f of ['labs.json', 'mirror.json']) {
    const j = JSON.parse(readFileSync(path.join(root, 'docs/curriculum-os', f), 'utf8'));
    const row = (j.items || j.labs).find(l => l.id === 'lab-sim-cks-runtime-security');
    assert.ok(row, f);
    assert.equal(row.gltf, S.get(SIM).glb);
    assert.equal(row.immersive.sim, SIM);
    assert.equal(row.immersive.mode, '3d-first');
    assert.match(row.summary, /no live cluster, real Falco, kernel or AppArmor/);
  }
  const m = JSON.parse(readFileSync(path.join(root, 'docs/assets/scenes/manifest.json'), 'utf8'));
  const sc = m.scenes.find(x => x.sim === SIM);
  assert.deepEqual([sc.gltf, sc.cert, sc.polish, sc.polishedOn], [S.get(SIM).glb, 'CKS', 'blender-cli', '2026-11-03']);
  assert.ok(m.sims.list.includes(SIM));
  assert.ok(!m.cka_coverage.interactive.includes(SIM), 'not counted as CKA coverage');
  assert.deepEqual(m.cks_coverage.interactive, ['cks-pod-security', 'cks-supply-chain', SIM]);
  assert.match(m.cks_coverage.covered['Monitoring, Logging & Runtime Security'], /cks-runtime-security/);
  assert.match(m.cks_coverage.covered['System Hardening'], /AppArmor/);
  assert.ok(!m.cks_coverage.notCovered.some(x => /^Runtime threat detection|^AppArmor$/.test(x)));
  assert.ok(m.cks_coverage.notCovered.some(x => /kube-bench/.test(x)));
  assert.equal(m.cks_coverage.hostedFleet, false);
  assert.equal(m.cks_coverage.liveUnrealHost, false);
  assert.equal(m.sims.runtime_version, S.VERSION);
  assert.equal(m.sims.exam.version, E.VERSION);
  assert.equal(m.sims.cli.version, C.VERSION);
  assert.deepEqual(m.sims.cli.packs.find(p => p.sim === SIM).tasks, ['falco-detect', 'apparmor', 'contain']);
  assert.match(m.sims.cli.runtimeNote, /No live cluster, no real Falco, kernel, eBPF probe or AppArmor, no clock/);
});

test('voice: "app armor" and "a a status" normalise to real syntax', () => {
  assert.equal(C.fromSpeech('a a status', SIM).line, 'aa-status');
  assert.match(C.fromSpeech('cat slash etc slash app armor dot d slash k8s dash deny dash write', SIM).line || '', /^cat \/etc\/apparmor\.d\/k8s-deny-write$/);
});

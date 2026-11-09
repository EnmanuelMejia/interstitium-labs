/**
 * 2026-11-06 Musk-bar pass: CKS track part 6 — Minimize Microservice Vulnerabilities (20% of the CKS): sandboxed container
 * runtimes (RuntimeClass + gVisor), the "sandboxed runtimes (gVisor / Kata)" item the manifest listed as not modelled. A NEW
 * authored asset, cks-sandbox-runtime.glb (kit-v2 + Blender CLI polish), its rules-engine drill (7 predict checkpoints), a
 * 3-task CLI pack (create the RuntimeClass, fix the containerd handler, blast radius + overhead), and the CKS paper drawing
 * from it. Generic tip/focus/replay/example coverage for the new pack comes from the loops in immersive-cli.test.js /
 * immersive-cli-packs.test.js (21 packs).
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
const SIM = 'cks-sandbox-runtime';
const CFG = '/etc/containerd/config.toml';
const POC = 'kubectl exec -n payments deploy/payments-api -- /lab/kernel-bug-poc';
const PODS = 'kubectl get pods -n payments -o wide';

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

test('NEW asset: cks-sandbox-runtime.glb is authored + Blender-polished, the sixth CKS scene; sim-* nodes hidden when healthy', () => {
  const sim = S.get(SIM);
  assert.equal(S.VERSION, '1.12.0');
  assert.equal(sim.cert, 'CKS');
  assert.equal(sim.glb, '/assets/immersive/cks-sandbox-runtime.glb');
  assert.ok(!S.list().filter(id => id !== SIM).map(id => S.get(id).glb).includes(sim.glb), 'a new asset, not a re-read of an existing scene');
  assert.deepEqual(S.list().filter(id => S.get(id).cert === 'CKS'), ['cks-pod-security', 'cks-supply-chain', 'cks-runtime-security', 'cks-cluster-hardening', 'cks-static-analysis', SIM]);
  const j = glbJson('assets/immersive/cks-sandbox-runtime.glb');
  const names = j.nodes.map(n => n.name);
  for (const n of ['kube-apiserver', 'runtimeclass', 'rc-selector', 'rc-overhead', 'sim-rc-missing', 'deploy-card', 'field-runtimeclass', 'field-requests', 'node-01', 'host-kernel', 'containerd',
    'handler-runc', 'handler-runsc', 'sim-no-runtime-n1', 'sentry', 'gofer', 'payments-pod', 'cpu-capacity', 'sim-overhead-slab', 'sim-pending-cpu', 'attacker-poc', 'sim-escape', 'sim-contained',
    'node-02', 'node02-kernel', 'containerd-n2', 'sim-pod-node02', 'sim-no-runtime-n2', 'edge-syscall-host', 'edge-syscall-sentry', 'edge-containerd-runc', 'edge-containerd-runsc']) assert.ok(names.includes(n), n);
  assert.ok(names.some(n => /_LOD1$/.test(n)), 'Blender CLI polish ran (LOD1 decimate duplicates present)');
  const k = j.nodes.find(n => n.name === 'sentry');
  assert.equal(k.extras.il.topic, SIM, 'pedagogy extras survive polish');
  assert.equal(k.extras.il.domain, 'minimize-microservice-vulnerabilities');
  assert.equal(j.nodes.find(n => n.name === 'sim-escape').extras.simOnly, true);
  const base = sim.derive(sim.initial);
  assert.equal(base.verdict, 'healthy');
  const sims = ['sim-rc-missing', 'sim-no-runtime-n1', 'sim-no-runtime-n2', 'sim-pod-node02', 'sim-overhead-slab', 'sim-pending-cpu', 'sim-escape'];
  for (const n of sims) assert.equal(S.styleFor(n, base.rules).hide, n === 'sim-overhead-slab' ? false : true, n);
  assert.equal(S.styleFor('sim-contained', base.rules).hide, true, 'no PoC in the healthy baseline');
  const at = set => sim.derive(S.merge(sim.initial, set)).rules;
  assert.equal(S.styleFor('sim-rc-missing', at({ rcExists: false })).hide, false);
  assert.equal(S.styleFor('sim-no-runtime-n1', at({ handlerNode01: false })).hide, false);
  assert.equal(S.styleFor('sim-no-runtime-n2', at({ rcSelector: false })).hide, false);
  assert.equal(S.styleFor('sim-pod-node02', at({ rcSelector: false })).hide, false);
  assert.equal(S.styleFor('sim-no-runtime-n1', at({ rcSelector: false })).hide, true, 'node02, not node01, fails');
  assert.equal(S.styleFor('sim-pending-cpu', at({ bigReq: true })).hide, false);
  assert.equal(S.styleFor('sim-escape', at({ useRC: false, kernelBug: true })).hide, false);
  assert.equal(S.styleFor('sim-contained', at({ kernelBug: true })).hide, false);
  assert.equal(S.styleFor('sim-escape', at({ kernelBug: true })).hide, true, 'gVisor: no escape');
});

test('rules engine: RuntimeClass admission, handler on the node, scheduling, overhead, runc vs gVisor against a kernel bug', () => {
  const sim = S.get(SIM);
  const at = set => S.cksSandboxDecide(S.merge(sim.initial, set));
  const v = set => sim.derive(S.merge(sim.initial, set)).verdict;
  const ok = at({});
  assert.deepEqual([ok.phase, ok.node, ok.sandboxed, ok.kernel, ok.gaps.length], ['running-gvisor', 'node01', true, '4.4.0', 0]);
  assert.equal(at({ rcExists: false }).phase, 'rejected', 'no silent runc fallback');
  assert.match(at({ rcExists: false }).podStatus, /RuntimeClass "gvisor" not found/);
  assert.deepEqual([at({ handlerNode01: false }).phase, at({ handlerNode01: false }).node], ['sandbox-fail', 'node01']);
  assert.match(at({ handlerNode01: false }).podStatus, /no runtime for "runsc" is configured/);
  assert.deepEqual([at({ rcSelector: false }).phase, at({ rcSelector: false }).node], ['sandbox-fail', 'node02'], 'the scheduler never checks handlers');
  assert.deepEqual([at({ bigReq: true }).phase, at({ bigReq: true }).total], ['pending-cpu', 1050], 'requests + overhead are what the scheduler counts');
  assert.equal(at({ bigReq: true, overhead: false }).phase, 'running-gvisor', 'without overhead it fits (and silently over-commits the node)');
  assert.deepEqual(at({ bigReq: true, overhead: false }).gaps, ['RuntimeClass has no overhead: the sandbox\'s own CPU and memory are not accounted']);
  assert.match(at({ bigReq: true }).podStatus, /0\/2 nodes are available: 1 Insufficient cpu, 1 node\(s\) didn't match Pod's node affinity\/selector/);
  assert.deepEqual([at({ useRC: false }).phase, at({ useRC: false }).kernel], ['running-runc', '6.8.0-45-generic']);
  assert.deepEqual([at({ useRC: false, kernelBug: true }).escape, at({ kernelBug: true }).escape, at({ kernelBug: true }).contained], [true, false, true]);
  assert.equal(at({ backoff: true }).phase, 'backoff');
  assert.equal(v({}), 'healthy');
  assert.equal(v({ rcExists: false }), 'degraded');
  assert.equal(v({ useRC: false }), 'degraded', 'a shared kernel is a gap, not a breach');
  assert.equal(v({ useRC: false, kernelBug: true }), 'exposed');
  assert.equal(v({ kernelBug: true }), 'healthy', 'contained: the Sentry served the syscall');
  assert.equal(S.verdictTone(v({ useRC: false, kernelBug: true })), 'bad');
  const pre = sim.scenarios.filter(sc => sc.predict);
  assert.equal(pre.length, 7);
  assert.equal(new Set(pre.map(sc => sc.predict.answer)).size, 3, 'keyed answers spread across positions 0-2');
  for (const sc of pre) {
    assert.ok(sc.predict.why.length > 200, sc.id + ' explains the mechanism');
    assert.equal(sc.predict.options.length, 3);
  }
  assert.match(sim.scenarios.find(s => s.id === 'no-handler').predict.options[0], /no runtime for "runsc" is configured/);
  assert.match(sim.scenarios.find(s => s.id === 'gvisor-kernel-bug').predict.why, /not a replacement for patching/);
  assert.match(sim.scenarios.find(s => s.id === 'fingerprint').predict.options[1], /4\.4\.0/);
  for (const sc of pre.filter(x => !['gvisor-kernel-bug', 'fingerprint'].includes(x.id))) assert.notEqual(sim.derive(S.merge(sim.initial, sc.set)).verdict, 'healthy', sc.id + ' breaks something');
});

test('create-runtimeclass: missing class → FailedCreate (old pod serves) → create → back-off → rollout restart → Running → uname 4.4.0; 7/7', () => {
  const s = session('create-runtimeclass');
  assert.equal(s.verdict(), 'degraded');
  assert.deepEqual(s.run('kubectl get runtimeclass').out, ['No resources found']);
  assert.equal(s.run('kubectl apply -f payments-api-gvisor.yaml').out[0], 'deployment.apps/payments-api configured');
  assert.equal(s.run('kubectl apply -f payments-api-gvisor.yaml').out[0], 'deployment.apps/payments-api unchanged');
  const pods = s.run('kubectl get pods -n payments').out.join('\n');
  assert.match(pods, /payments-api-6c8f9d7b5-k9w2x\s+1\/1\s+Running/);
  assert.doesNotMatch(pods, /7d5b8c6f4/, 'no new pod: nothing was created');
  assert.match(s.run('kubectl get events -n payments').out.join('\n'), /FailedCreate\s+replicaset\/payments-api-7d5b8c6f4\s+Error creating: pods "payments-api-7d5b8c6f4-" is forbidden: pod rejected: RuntimeClass "gvisor" not found/);
  assert.equal(s.run('kubectl rollout restart deployment payments-api -n payments').exit, 0);
  assert.equal(s.run('kubectl apply -f runtimeclass-gvisor.yaml').out[0], 'runtimeclass.node.k8s.io/gvisor created');
  assert.match(s.run('kubectl get pods -n payments').out.join('\n'), /backing off after FailedCreate/, 'created after the failure: the ReplicaSet is in back-off');
  assert.equal(s.run('kubectl apply -f runtimeclass-gvisor.yaml').out[0], 'runtimeclass.node.k8s.io/gvisor unchanged');
  assert.equal(s.run('kubectl rollout restart deployment/payments-api -n payments').out[0], 'deployment.apps/payments-api restarted');
  const w = s.run(PODS).out;
  assert.match(w.join('\n'), /payments-api-7d5b8c6f4-q4m7z\s+1\/1\s+Running\s+0\s+41s\s+10\.244\.1\.21\s+node01/);
  assert.equal(w.length, 2, 'one pod: the old revision is gone');
  assert.deepEqual(s.run('kubectl exec -n payments deploy/payments-api -- uname -r').out, ['4.4.0']);
  assert.deepEqual(s.run('uname -r').out, ['6.8.0-45-generic'], 'node01 is not sandboxed');
  assert.equal(s.status().total, 7);
  assert.equal(s.status().done, true);
  assert.equal(s.verdict(), 'healthy');
  assert.equal(s.run('kubectl get runtimeclass').out.join('\n').replace(/\s+/g, ' '), 'NAME HANDLER AGE gvisor runsc 5m');
});

test('node-handler: stuck sandbox → kubelet reason → commented runsc table → sed → not loaded until containerd restarts → Running → gVisor dmesg; 7/7', () => {
  const s = session('node-handler');
  assert.equal(s.verdict(), 'degraded');
  const w = s.run(PODS).out.join('\n');
  assert.match(w, /payments-api-6c8f9d7b5-k9w2x\s+1\/1\s+Running/);
  assert.match(w, /payments-api-7d5b8c6f4-q4m7z\s+0\/1\s+ContainerCreating\s+0\s+36s\s+<none>\s+node01/);
  const d = s.run('kubectl describe pod -n payments -l app=payments-api').out.join('\n');
  assert.match(d, /FailedCreatePodSandBox\s+8s\s+kubelet\s+Failed to create pod sandbox: rpc error: code = Unknown desc = failed to get sandbox runtime: no runtime for "runsc" is configured/);
  assert.match(d, /Runtime Class Name:\s+gvisor/);
  assert.equal(s.run('cat ' + CFG).out.filter(l => /^#/.test(l)).length, 2, 'both runsc lines are commented out');
  assert.equal(s.run('systemctl restart containerd').exit, 0);
  assert.equal(s.state.handlerNode01, false, 'restart before editing changes nothing');
  assert.equal(s.run("sed -i 's/runc/runsc/' " + CFG).exit, 1, 'unmodelled edits are refused, nothing written');
  assert.equal(s.state.cfgRunsc, false);
  assert.equal(s.run("sed 's/^#//' " + CFG).out.filter(l => /runsc/.test(l) && !/^#/.test(l)).length, 2, 'without -i sed only prints');
  assert.equal(s.state.cfgRunsc, false);
  assert.equal(s.run("sed -i '/runsc/s/^#//' " + CFG).exit, 0);
  assert.equal(s.state.cfgRunsc, true);
  assert.equal(s.state.handlerNode01, false, 'containerd reads its config at start');
  assert.deepEqual(s.run('cat ' + CFG).out.slice(-2), ['[plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runsc]', '  runtime_type = "io.containerd.runsc.v1"']);
  assert.match(s.run(PODS).out.join('\n'), /ContainerCreating/, 'still stuck until the restart');
  s.run('systemctl restart containerd');
  assert.equal(s.state.handlerNode01, true);
  assert.equal(s.run(PODS).out.filter(l => /Running/.test(l)).length, 1);
  const dm = s.run('kubectl exec -n payments deploy/payments-api -- dmesg');
  assert.equal(dm.out[0], '[    0.000000] Starting gVisor...');
  assert.equal(s.status().total, 7);
  assert.equal(s.status().done, true);
  assert.equal(s.verdict(), 'healthy');
});

test('blast-radius: escape under runc → bare RuntimeClass → full → 800m Pending (overhead) → 600m → Running → PoC contained; 8/8', () => {
  const s = session('blast-radius');
  assert.equal(s.verdict(), 'exposed');
  const esc = s.run(POC);
  assert.equal(esc.exit, 0);
  assert.match(esc.out.join('\n'), /host kernel reached on node01: container escape/);
  assert.match(esc.out[0], /simulated, no real exploit code/);
  assert.match(s.run('kubectl exec -n payments deploy/payments-api -- dmesg').out[0], /Operation not permitted/, 'runc: dmesg is the host\'s and is denied');
  assert.match(s.run('kubectl describe runtimeclass gvisor').out.join('\n'), /no Overhead and no Scheduling stanza/);
  assert.equal(s.run('kubectl apply -f runtimeclass-gvisor.yaml').out[0], 'runtimeclass.node.k8s.io/gvisor configured');
  assert.match(s.run('kubectl describe runtimeclass gvisor').out.join('\n'), /Cpu:\s+250m[\s\S]*Node Selector:\s+sandbox\.gvisor\.dev\/runtime:\s+gvisor/);
  s.run('kubectl apply -f payments-api-gvisor-big.yaml');
  const p = s.run('kubectl get pods -n payments').out.join('\n');
  assert.match(p, /payments-api-5b9f7c8d6-r8n2t\s+0\/1\s+Pending/);
  assert.match(s.run('kubectl describe pod -n payments -l app=payments-api').out.join('\n'), /0\/2 nodes are available: 1 Insufficient cpu, 1 node\(s\) didn't match Pod's node affinity\/selector\. \(requests 800m \+ RuntimeClass overhead 250m = 1050m; node01 has 1000m free\)/);
  assert.match(s.run('kubectl get events -n payments').out.join('\n'), /FailedScheduling/);
  assert.equal(s.verdict(), 'degraded');
  s.run('kubectl apply -f payments-api-gvisor.yaml');
  assert.match(s.run(PODS).out.join('\n'), /payments-api-7d5b8c6f4-q4m7z\s+1\/1\s+Running/);
  const c = s.run(POC);
  assert.equal(c.exit, 1);
  assert.match(c.out.join('\n'), /Sentry implemented the syscall in user space/);
  assert.equal(s.status().total, 8);
  assert.equal(s.status().done, true);
  assert.equal(s.verdict(), 'healthy');
  assert.match(session(null, { kernelBug: false }).run(POC).out.join('\n'), /patched: not vulnerable/);
});

test('honesty: unmodelled forms never invent output; help and note say simulated', () => {
  const s = session();
  assert.equal(s.run('kubectl exec -n payments deploy/payments-api -- id').exit, 2);
  assert.equal(s.run('kubectl exec -n payments deploy/nope -- uname -r').exit, 1);
  assert.equal(s.run('kubectl rollout restart deployment web -n payments').exit, 1);
  assert.equal(s.run('kubectl apply -f nothing.yaml').exit, 1);
  assert.equal(s.run('kubectl get runtimeclass kata').exit, 1);
  assert.equal(s.run('sed -i s/a/b/ other.toml').exit, 2);
  assert.equal(s.run('systemctl restart kubelet').exit, 2);
  assert.equal(s.run('crictl ps').exit, 2);
  assert.equal(s.run('docker ps').exit, 127);
  assert.match(s.run('kubectl get pods -n other').out[0], /No resources found in other namespace/);
  const help = s.run('help').out.join('\n');
  assert.match(help, /Simulated shell/);
  assert.match(help, /no real containerd, runsc or kernel/);
  assert.match(help, /simulation with no exploit code/);
});

test('CKS paper: the 7 checkpoints count for Minimize Microservice Vulnerabilities, gap link stays on cks-pod-security, pool +7 (50)', () => {
  assert.equal(E.VERSION, '1.8.0');
  const mm = E.CKS_BLUEPRINT.find(b => b.domain === 'Minimize Microservice Vulnerabilities');
  assert.deepEqual(mm.sims, ['cks-pod-security', SIM]);
  for (const x of S.get(SIM).scenarios.filter(y => y.predict)) assert.equal(E.cksDomain(SIM, x.id), 'Minimize Microservice Vulnerabilities', x.id);
  assert.ok(E.CKS_SIMS.includes(SIM));
  assert.equal(E.pool(S, 'CKS').filter(it => it.simId === SIM).length, 7);
  assert.equal(E.pool(S, 'CKS').length, 50);
  assert.ok(!E.pool(S).some(it => it.simId === SIM), 'the CKA paper never draws a CKS checkpoint');
  for (const seed of [1, 7, 42, 2026]) {
    const ex = E.buildExam(S, { track: 'CKS', seed });
    assert.equal(ex.count, 8);
    assert.equal(new Set(ex.items.map(i => i.domain)).size, 6, 'one item per official domain first (seed ' + seed + ')');
    assert.match(ex.honesty, /kubesec, KubeLinter and gVisor run on a rules engine/);
  }
  const ex2 = E.buildExam(S, { track: 'CKS', seed: 7 });
  ex2.items.forEach(it => { const miss = it.domain === 'Minimize Microservice Vulnerabilities'; it.choice = miss ? (it.answer + 1) % 3 : it.answer; it.correct = !miss; });
  const bp = E.summarize(ex2).blueprint;
  assert.equal(bp.coveragePct, 100);
  assert.equal(bp.weakest.domain, 'Minimize Microservice Vulnerabilities');
  assert.deepEqual(bp.drill, { sim: 'cks-pod-security', href: '/immersive/#cks-pod-security' });
  assert.match(bp.honesty, /sandboxed runtimes \(RuntimeClass, gVisor\) since 2026-11-06/);
});

test('review: sandboxed-runtime coach cards get an honest CKS label; CKA mastery stays CKA-only', () => {
  assert.match(R.VERSION, /^1\.(3\.6|4\.0)$/);
  const cards = R.cliCheckpoints(C, S).filter(c => c.simId === SIM);
  assert.equal(cards.length, 22);
  assert.ok(cards.every(c => c.domain === 'CKS · Microservice vulnerabilities (sandboxed runtimes)'));
  assert.ok(!R.checkpoints(S).some(c => c.simId === SIM));
});

test('wiring: /immersive/ host, exam lobby copy, curriculum rows, manifest (new scene, cks_coverage, pack, honest notes)', () => {
  const html = readFileSync(path.join(root, 'docs/immersive/index.html'), 'utf8');
  assert.match(html, /id="cks-sandbox-runtime"/);
  assert.match(html, /data-il-sim="cks-sandbox-runtime"\s*\n\s*data-gltf="\/assets\/immersive\/cks-sandbox-runtime\.glb"/);
  assert.match(html, /no real containerd, runsc or kernel, and no clock/);
  const exam = readFileSync(path.join(root, 'docs/immersive/exam/index.html'), 'utf8');
  assert.match(exam, /sandboxed-runtime \(added 2026-11-06/);
  for (const f of ['labs.json', 'mirror.json']) {
    const j = JSON.parse(readFileSync(path.join(root, 'docs/curriculum-os', f), 'utf8'));
    const row = (j.items || j.labs).find(l => l.id === 'lab-sim-cks-sandbox-runtime');
    assert.ok(row, f);
    assert.equal(row.gltf, S.get(SIM).glb);
    assert.equal(row.immersive.sim, SIM);
    assert.equal(row.immersive.mode, '3d-first');
    assert.match(row.summary, /no live cluster, real containerd, runsc or kernel/);
  }
  const m = JSON.parse(readFileSync(path.join(root, 'docs/assets/scenes/manifest.json'), 'utf8'));
  const sc = m.scenes.find(x => x.sim === SIM);
  assert.deepEqual([sc.gltf, sc.cert, sc.polish, sc.polishedOn], [S.get(SIM).glb, 'CKS', 'blender-cli', '2026-11-06']);
  assert.ok(m.sims.list.includes(SIM));
  assert.ok(!m.cka_coverage.interactive.includes(SIM), 'not counted as CKA coverage');
  assert.deepEqual(m.cks_coverage.interactive, ['cks-pod-security', 'cks-supply-chain', 'cks-runtime-security', 'cks-cluster-hardening', 'cks-static-analysis', SIM]);
  assert.match(m.cks_coverage.covered['Minimize Microservice Vulnerabilities'], /RuntimeClass/);
  assert.ok(!m.cks_coverage.notCovered.some(x => /^sandboxed runtimes \(gVisor \/ Kata\)$/.test(x)));
  assert.ok(m.cks_coverage.notCovered.some(x => /Kata Containers/.test(x)), 'Kata honestly still missing');
  assert.equal(m.cks_coverage.hostedFleet, false);
  assert.equal(m.cks_coverage.liveUnrealHost, false);
  assert.equal(m.sims.runtime_version, S.VERSION);
  assert.equal(m.sims.exam.version, E.VERSION);
  assert.equal(m.sims.cli.version, C.VERSION);
  assert.deepEqual(m.sims.cli.packs.find(p => p.sim === SIM).tasks, ['create-runtimeclass', 'node-handler', 'blast-radius']);
  assert.match(m.sims.cli.sandboxRuntimeNote, /No live cluster, no real containerd, runsc or kernel, no clock/);
});

test('voice: "runtime class", "g visor" and "container d" normalise to the real words', () => {
  assert.match(C.fromSpeech('kube control get runtime class', SIM).line, /^kubectl get runtimeclass$/);
  assert.match(C.fromSpeech('system control restart container d', SIM).line, /^systemctl restart containerd$/);
});

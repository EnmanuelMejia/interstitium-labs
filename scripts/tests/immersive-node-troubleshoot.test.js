/**
 * 2026-10-22 Musk-bar pass: worker-node troubleshooting (CKA Troubleshooting = 30%) on a NEW authored asset,
 * node-troubleshoot.glb (kit-v2 + Blender CLI polish), its rules-engine drill (node-troubleshoot) and a 4-task CLI pack
 * with ssh sessions. Pure UMD — the browser runs exactly this code. Generic tip/focus/replay coverage for the new pack
 * comes from the loops in immersive-cli.test.js / immersive-cli-packs.test.js, which iterate C.list() (12 packs).
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
const SIM = 'node-troubleshoot';
const DROPIN = '/usr/lib/systemd/system/kubelet.service.d/10-kubeadm.conf';

function session(taskId, extra) {
  const tk = taskId ? C.task(SIM, taskId) : null;
  let state = S.merge(S.merge(S.get(SIM).initial, tk ? tk.setup : {}), extra || {});
  const ctx = C.newCtx(taskId);
  return {
    ctx,
    get state() { return state; },
    run(line) { const r = C.run(SIM, state, line, ctx); if (r.set) state = S.merge(state, r.set); return r; },
    status() { return C.taskStatus(SIM, taskId, state, ctx); },
    derived() { return S.get(SIM).derive(state); }
  };
}
function glbJson(rel) {
  const buf = readFileSync(path.join(root, 'docs', rel));
  const jl = buf.readUInt32LE(12);
  return JSON.parse(buf.toString('utf8', 20, 20 + jl).trim());
}
const node01 = r => r.out.find(l => /^node-01\s/.test(l)) || '';

test('NEW asset: node-troubleshoot.glb is authored + Blender-polished, keeps names and pedagogy extras, sim-* nodes hidden by default', () => {
  const sim = S.get(SIM);
  assert.equal(sim.glb, '/assets/immersive/node-troubleshoot.glb');
  const others = S.list().filter(id => id !== SIM).map(id => S.get(id).glb);
  assert.ok(!others.includes(sim.glb), 'a new asset, not a re-read of an existing scene');
  const j = glbJson('assets/immersive/node-troubleshoot.glb');
  const names = j.nodes.map(n => n.name);
  for (const n of ['kubelet', 'kubelet-unit', 'systemd-ring', 'cri-socket', 'containerd', 'cni-conf', 'edge-node-lease', 'node-lifecycle-controller',
    'pod-guaranteed', 'pod-burstable', 'pod-besteffort-0', 'pod-besteffort-1', 'disk-gauge', 'sim-disk-fill-3', 'sim-disk-fill-4', 'sim-taint-flag', 'journal-page-0']) {
    assert.ok(names.includes(n), n);
  }
  assert.ok(names.some(n => /_LOD1$/.test(n)), 'Blender CLI polish ran (LOD1 decimate duplicates present)');
  const kub = j.nodes.find(n => n.name === 'kubelet');
  assert.equal(kub.extras && kub.extras.il && kub.extras.il.topic, 'node-troubleshoot', 'pedagogy extras survive polish');
  assert.equal(S.styleFor('sim-taint-flag', sim.derive(sim.initial).rules).hide, true);
  assert.equal(S.styleFor('sim-disk-fill-4', sim.derive(sim.initial).rules).hide, true);
  const dp = sim.derive(S.merge(sim.initial, { diskPressure: true })).rules;
  assert.equal(S.styleFor('sim-disk-fill-4', dp).hide, false);
  assert.equal(S.styleFor('sim-taint-flag', dp).hide, false);
});

test('rules engine: kubelet / runtime / CNI / disk pressure follow documented node behaviour', () => {
  const sim = S.get(SIM);
  const at = set => S.nodeDecide(S.merge(sim.initial, set));
  assert.ok(['1.5.0', '1.6.0'].includes(S.VERSION), 'node-troubleshoot arrived in v1.5.0; v1.6.0 (2026-10-23) keeps it');
  assert.equal(at({}).ready, 'True');
  assert.equal(sim.derive(sim.initial).verdict, 'healthy');
  const k203 = at({ execLoaded: false, execOnDisk: false });
  assert.equal(k203.kubeletUnit, 'auto-restart-203');
  assert.equal(k203.readyStatus, 'Unknown', 'a silent kubelet → Unknown (shown NotReady), not False');
  assert.equal(k203.taint, 'node.kubernetes.io/unreachable');
  assert.deepEqual(k203.taintEffects, ['NoSchedule', 'NoExecute']);
  assert.equal(k203.diskPressure, 'Unknown', 'every condition goes Unknown when the kubelet stops posting');
  assert.equal(at({ execLoaded: false, execOnDisk: true }).daemonReloadNeeded, true);
  assert.equal(at({ execLoaded: false, execOnDisk: false }).daemonReloadNeeded, false);
  const rt = at({ runtimeUp: false });
  assert.equal(rt.readyStatus, 'False');
  assert.match(rt.reason, /container runtime is down/);
  assert.equal(rt.runningContainersKeepRunning, true, 'containerd-shim keeps containers alive');
  assert.equal(rt.taint, 'node.kubernetes.io/not-ready');
  const cni = at({ cniOk: false });
  assert.match(cni.reason, /NetworkReady=false reason:NetworkPluginNotReady message:Network plugin returns error: cni plugin not initialized/);
  const dp = at({ diskPressure: true });
  assert.equal(dp.ready, 'True', 'DiskPressure does not make the node NotReady');
  assert.equal(dp.taint, 'node.kubernetes.io/disk-pressure');
  assert.deepEqual(dp.taintEffects, ['NoSchedule']);
  assert.equal(dp.evictBestEffort, true);
  assert.equal(dp.newPodsLand, false);
  assert.equal(at({ diskPressure: true, kubeletOn: false }).evictBestEffort, false, 'no kubelet, no node-pressure eviction');
  assert.equal(sim.derive(S.merge(sim.initial, { diskPressure: true })).verdict, 'degraded');
  assert.equal(sim.derive(S.merge(sim.initial, { cniOk: false })).verdict, 'down');
  const keys = sim.scenarios.filter(sc => sc.predict).map(sc => sc.predict.answer);
  assert.equal(keys.length, 5);
  assert.equal(new Set(keys).size, 3, 'keyed answers spread across positions 0-2');
});

test('kubelet-203: the sed fix alone is not enough — systemd warns until daemon-reload; the full task verifies 8/8', () => {
  const s = session('kubelet-203');
  assert.match(node01(s.run('kubectl get nodes')), /NotReady/);
  const d = s.run('kubectl describe node node-01');
  assert.ok(d.out.some(l => /Ready\s+Unknown\s+NodeStatusUnknown\s+Kubelet stopped posting node status\./.test(l)));
  assert.ok(d.out.includes('Taints:             node.kubernetes.io/unreachable:NoSchedule'));
  const st = s.run('ssh node-01 systemctl status kubelet');
  assert.equal(st.exit, 3);
  assert.ok(st.out.some(l => /status=203\/EXEC/.test(l)));
  assert.ok(s.run('ssh node-01 cat ' + DROPIN).out.includes('ExecStart=/usr/local/bin/kubelet $KUBELET_KUBECONFIG_ARGS $KUBELET_CONFIG_ARGS $KUBELET_KUBEADM_ARGS $KUBELET_EXTRA_ARGS'));
  assert.deepEqual(s.run('ssh node-01 which kubelet').out, ['/usr/bin/kubelet']);
  /* sed without -i writes nothing */
  s.run("ssh node-01 sed 's|/usr/local/bin/kubelet|/usr/bin/kubelet|' " + DROPIN);
  assert.equal(s.state.execOnDisk, false);
  /* escaped-slash form works the same as the | delimiter */
  s.run("ssh node-01 sudo sed -i 's/\\/usr\\/local\\/bin\\/kubelet/\\/usr\\/bin\\/kubelet/' " + DROPIN);
  assert.equal(s.state.execOnDisk, true);
  const early = s.run('ssh node-01 sudo systemctl restart kubelet');
  assert.match(early.out[0], /changed on disk\. Run 'systemctl daemon-reload' to reload units\./);
  assert.ok(early.events.includes('kubelet-restarted-203'));
  assert.ok(s.run('ssh node-01 systemctl status kubelet').out.some(l => /203\/EXEC/.test(l)), 'still 203 — systemd runs the definition it loaded');
  s.run('ssh node-01 sudo systemctl daemon-reload');
  assert.equal(s.state.execLoaded, true);
  s.run('ssh node-01 sudo systemctl restart kubelet');
  const ok = s.run('ssh node-01 systemctl status kubelet');
  assert.equal(ok.exit, 0);
  assert.ok(ok.out.some(l => /Active: active \(running\)/.test(l)));
  assert.match(node01(s.run('kubectl get nodes')), /\bReady\b/);
  const fin = s.status();
  assert.equal(fin.total, 8);
  assert.equal(fin.done, true, fin.steps.map(x => x.done).join(','));
});

test('ssh sessions: prompt follows the host, kubectl has no kubeconfig on the worker, node commands need the node', () => {
  const s = session(null);
  assert.equal(C.promptFor(SIM, s.ctx), 'student@controlplane:~$');
  const wrong = s.run('systemctl status kubelet');
  assert.equal(wrong.exit, 2);
  assert.match(wrong.out[0], /ssh node-01 first/);
  const in1 = s.run('ssh node-01');
  assert.equal(in1.prompt, 'student@node-01:~$');
  assert.equal(C.promptFor(SIM, s.ctx), 'student@node-01:~$');
  assert.equal(s.run('systemctl status kubelet').exit, 0);
  const kc = s.run('kubectl get nodes');
  assert.equal(kc.exit, 1);
  assert.match(kc.out[0], /localhost:8080 was refused/);
  assert.match(s.run('sudo journalctl -u kubelet').out[0], /representative/, 'journal lines are labelled representative');
  s.run('exit');
  assert.equal(C.promptFor(SIM, s.ctx), 'student@controlplane:~$');
  assert.equal(s.run('ssh node-09 hostname').exit, 255);
  assert.equal(s.run('vim ' + DROPIN).exit, 2, 'no fake editor');
  assert.equal(C.promptFor('etcd-quorum', C.newCtx()), 'student@cp-0:~$', 'other packs keep their static prompt');
});

test('runtime-down: crictl fails at the containerd socket; enable --now recovers; task verifies 5/5', () => {
  const s = session('runtime-down');
  assert.ok(s.run('kubectl describe node node-01').out.some(l => /Ready\s+False\s+KubeletNotReady\s+container runtime is down/.test(l)));
  const cr = s.run('ssh node-01 sudo crictl ps');
  assert.equal(cr.exit, 1);
  assert.match(cr.out[0], /dial unix \/run\/containerd\/containerd\.sock: connect: no such file or directory/);
  assert.match(s.run('ssh node-01 systemctl status containerd').out.join('\n'), /inactive \(dead\)[\s\S]*containerd-shim/);
  assert.match(s.derived().caption, /running containers kept by shims/);
  s.run('ssh node-01 sudo systemctl enable --now containerd');
  assert.equal(s.state.runtimeUp, true);
  s.run('kubectl get nodes');
  assert.equal(s.status().done, true);
});

test('cni-missing: NetworkPluginNotReady in the journal, empty net.d, DaemonSet restart rewrites the conflist (not while the runtime is down)', () => {
  const blocked = session('cni-missing', { runtimeUp: false });
  const r0 = blocked.run('kubectl rollout restart daemonset calico-node -n kube-system');
  assert.match(r0.out.join(' '), /cannot start on node-01/);
  assert.equal(blocked.state.cniOk, false);
  const s = session('cni-missing');
  s.run('kubectl get nodes');
  s.run('kubectl describe node node-01');
  assert.ok(s.run('ssh node-01 sudo journalctl -u kubelet -n 20 --no-pager').out.some(l => /"Container runtime network not ready" networkReady="NetworkReady=false reason:NetworkPluginNotReady/.test(l)));
  assert.deepEqual(s.run('ssh node-01 ls /etc/cni/net.d').out, []);
  assert.equal(s.run('kubectl rollout restart daemonset calico-node -n default').exit, 1, 'wrong namespace → NotFound');
  s.run('kubectl rollout restart ds/calico-node -n kube-system');
  assert.equal(s.state.cniOk, true);
  assert.deepEqual(s.run('ssh node-01 ls /etc/cni/net.d').out, ['10-calico.conflist  calico-kubeconfig']);
  s.run('kubectl get nodes');
  assert.equal(s.status().done, true);
});

test('disk-pressure: Ready stays True, NoSchedule taint only, BestEffort evicted (Guaranteed/Burstable keep running), prune clears it', () => {
  const s = session('disk-pressure');
  const d = s.run('kubectl describe node node-01').out;
  assert.ok(d.some(l => /DiskPressure\s+True\s+KubeletHasDiskPressure/.test(l)));
  assert.ok(d.some(l => /Ready\s+True\s+KubeletReady/.test(l)));
  assert.ok(d.includes('Taints:             node.kubernetes.io/disk-pressure:NoSchedule'));
  assert.ok(!d.some(l => /disk-pressure:NoExecute/.test(l)));
  const pods = s.run('kubectl get pods -o wide').out;
  assert.ok(pods.some(l => /^web-6f7d9-gq2xk\s.*Running/.test(l)), 'Guaranteed survives');
  assert.ok(pods.some(l => /^api-58b4c-brs4n\s.*Running/.test(l)), 'Burstable survives');
  assert.equal(pods.filter(l => /^batch-7c5d8-\w+\s.*Evicted.*node-01$/.test(l)).length, 2, 'both BestEffort pods evicted');
  assert.equal(pods.filter(l => /Running.*node-02$/.test(l)).length, 2, 'ReplicaSet replacements land on node-02');
  assert.ok(s.run('ssh node-01 sudo journalctl -u kubelet').out.some(l => /pods ranked for eviction" pods=\["default\/batch/.test(l)), 'BestEffort ranked first');
  assert.match(s.run('ssh node-01 df -h /').out[1], /95%/);
  s.run('ssh node-01 sudo crictl rmi --prune');
  assert.equal(s.state.diskPressure, false);
  assert.ok(s.run('kubectl describe node node-01').out.includes('Taints:             <none>'));
  assert.equal(s.status().done, true);
  assert.ok(s.run('kubectl get pods').out.some(l => /Evicted/.test(l)), 'evicted pod records stay until deleted');
});

test('voice + coach: spoken systemctl/journalctl normalise into the prompt; coach never leaks the command', () => {
  assert.deepEqual(C.fromSpeech('system control daemon reload', SIM), { line: 'systemctl daemon-reload', verb: false });
  assert.deepEqual(C.fromSpeech('journal control dash u kubelet', SIM), { line: 'journalctl -u kubelet', verb: false });
  const s = session('kubelet-203');
  for (const l of ['kubectl get nodes', 'kubectl describe node node-01', 'ssh node-01 systemctl status kubelet', 'ssh node-01 cat ' + DROPIN,
    "ssh node-01 sudo sed -i 's|/usr/local/bin/kubelet|/usr/bin/kubelet|' " + DROPIN]) s.run(l);
  C.coach(SIM, 'kubelet-203', s.state, s.ctx);
  const c = C.coach(SIM, 'kubelet-203', s.state, s.ctx);
  assert.equal(c.step, 5);
  assert.equal(c.level, 'hint');
  assert.ok(!c.lines.join('\n').includes('daemon-reload'), 'hint level does not print the command');
  assert.match(c.focus, /systemd-ring/);
  const sol = C.coach(SIM, 'kubelet-203', s.state, s.ctx, { count: false, level: 'solution' });
  assert.equal(sol.solution, 'ssh node-01 sudo systemctl daemon-reload');
});

test('blueprint: Troubleshooting (30%) now has two drills; node-troubleshoot is graded CKA scope with its own 3D anchor', () => {
  const tr = E.BLUEPRINT.find(b => b.domain === 'Troubleshooting');
  assert.deepEqual(tr.sims.slice(0, 2), ['control-plane-failure', 'node-troubleshoot'], 'service-dns joins as the third drill on 2026-10-23');
  assert.equal(E.OFFICIAL[SIM], 'Troubleshooting');
  const all = E.BLUEPRINT.reduce((a, b) => a.concat(b.sims), []);
  assert.equal(new Set(all).size, all.length, 'every drill maps to exactly one domain');
});

test('wiring: /immersive/ host, curriculum mirror, manifest (new scene, pack, honest notes)', () => {
  const html = readFileSync(path.join(root, 'docs/immersive/index.html'), 'utf8');
  assert.match(html, /id="cka-node-troubleshoot"[\s\S]*?data-il-sim="node-troubleshoot"\s*\n\s*data-gltf="\/assets\/immersive\/node-troubleshoot\.glb"/);
  assert.match(html, /The shell is simulated and runs on a rules engine: there is no VM and no live node/);
  for (const f of ['labs.json', 'mirror.json']) {
    const j = JSON.parse(readFileSync(path.join(root, 'docs/curriculum-os', f), 'utf8'));
    const lab = (j.items || j.labs).find(l => l.immersive && l.immersive.sim === SIM);
    assert.ok(lab && lab.id === 'lab-sim-node-troubleshoot' && lab.publishStatus === 'published' && lab.gltf === '/assets/immersive/node-troubleshoot.glb', f);
  }
  const m = JSON.parse(readFileSync(path.join(root, 'docs/assets/scenes/manifest.json'), 'utf8'));
  const sc = m.scenes.find(x => x.sim === SIM);
  assert.equal(sc.gltf, '/assets/immersive/node-troubleshoot.glb');
  assert.equal(sc.polishedOn, '2026-10-22');
  assert.ok(m.sims.list.includes(SIM) && m.cka_coverage.interactive.includes(SIM));
  assert.equal(m.sims.cli.version, C.VERSION);
  assert.match(m.sims.cli.nodeNote, /No VM, no real kubelet, no clock/);
  assert.match(m.sims.exam.blueprint.honesty, /three drills/, 'two drills on 2026-10-22, three since 2026-10-23');
  assert.equal(m.cka_coverage.liveUnrealHost, false);
  assert.equal(m.cka_coverage.hostedFleet, false);
});

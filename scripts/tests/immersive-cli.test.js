/**
 * In-scene CLI lab tests (2026-10-16): docs/assets/il-immersive-cli.js parses real kubectl / etcdctl / crictl /
 * aws syntax, maps it onto the SAME rules-engine state as the 3D drills, and verifies Killercoda-style tasks.
 * Pure UMD — the browser runs exactly this code.
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

/** Drive a task end-to-end the way the player does: run → merge patch → next line. */
function session(sim, taskId) {
  const tk = taskId ? C.task(sim, taskId) : null;
  let state = S.merge(S.get(sim).initial, tk ? tk.setup : {});
  const ctx = C.newCtx(taskId);
  return {
    ctx,
    get state() { return state; },
    run(line) { const r = C.run(sim, state, line, ctx); if (r.set) state = S.merge(state, r.set); return r; },
    status() { return C.taskStatus(sim, taskId, state, ctx); },
    verdict() { return S.get(sim).derive(state).verdict; }
  };
}

test('exports v1.0.0 with an honest simulated-shell label and packs only for sims that exist', () => {
  assert.equal(C.VERSION, '1.0.0');
  assert.match(C.honesty, /Simulated shell/);
  assert.match(C.honesty, /Not a real shell, not a cluster, no AWS account, no hosted lab fleet/);
  assert.deepEqual(C.list().sort(), ['aws-az-failure', 'control-plane-failure', 'etcd-quorum', 'hpa-scale', 'sched-taints']);
  for (const id of C.list()) {
    assert.ok(S.get(id), id + ' has a rules-engine sim');
    const p = C.pack(id);
    assert.ok(p.tasks.length >= 2, id + ' has ≥2 tasks');
    for (const tk of p.tasks) {
      for (const k of Object.keys(tk.setup || {})) assert.ok(k in S.get(id).initial, `${id}/${tk.id} setup key ${k} is real sim state`);
      for (const st of tk.steps) assert.ok(st.hint && st.label && (st.event || st.state), `${id}/${tk.id} step complete`);
    }
  }
});

test('tokenizer: quotes, escapes, env prefixes, sudo, ssh HOST "cmd", k alias', () => {
  assert.deepEqual(C.tokenize(`kubectl patch hpa web -p '{"spec":{"maxReplicas":5}}'`), ['kubectl', 'patch', 'hpa', 'web', '-p', '{"spec":{"maxReplicas":5}}']);
  assert.deepEqual(C.tokenize('$ echo "a b" c\\ d'), ['echo', 'a b', 'c d']);
  assert.deepEqual(C.tokenize("x ''"), ['x', '']);
  assert.equal(C.flag(['--replicas=5'], '--replicas'), '5');
  assert.equal(C.flag(['--replicas', '5'], '--replicas'), '5');
  assert.equal(C.flag(['--multi-az'], '--multi-az'), true);
  assert.deepEqual(C.manifestMove(['mv', '/etc/kubernetes/manifests/kube-scheduler.yaml', '/tmp/']), { component: 'kube-scheduler', up: false });
  assert.deepEqual(C.manifestMove(['mv', '/tmp/kube-scheduler.yaml', '/etc/kubernetes/manifests/']), { component: 'kube-scheduler', up: true });
  assert.equal(C.manifestMove(['mv', '/tmp/a.yaml', '/tmp/b.yaml']), null);
  const s = session('control-plane-failure');
  assert.deepEqual(s.run("ssh worker-2 'sudo systemctl stop kubelet'").set, { kubelet2Up: false });
  assert.match(s.run('k get nodes').out.join('\n'), /worker-2\s+NotReady/);
});

test('etcd: the single survivor of 3 cannot commit — health, member list and writes all fail; quorum restores writes', () => {
  const s = session('etcd-quorum', 'lose-quorum');
  assert.equal(s.run('etcdctl endpoint health --cluster').exit, 0);
  s.run('fault stop etcd-1');
  const deg = s.run('ETCDCTL_API=3 etcdctl endpoint health --cluster --endpoints=https://10.0.0.11:2379');
  assert.equal(deg.exit, 1);
  assert.match(deg.out[0], /10\.0\.0\.11:2379 is healthy/);
  assert.match(deg.out[1], /10\.0\.0\.12:2379 is unhealthy: failed to connect/);
  assert.equal(s.run('kubectl create deployment web --image=nginx').out[0], 'deployment.apps/web created', '2/3 is still a quorum');
  s.run("ssh cp-2 'sudo mv /etc/kubernetes/manifests/etcd.yaml /tmp/'");
  assert.equal(s.verdict(), 'down');
  const h = s.run('etcdctl endpoint health --cluster');
  assert.match(h.out[0], /10\.0\.0\.11:2379 is unhealthy: failed to commit proposal: context deadline exceeded/);
  assert.equal(h.out[h.out.length - 1], 'Error: unhealthy cluster');
  assert.equal(s.run('etcdctl member list').exit, 1);
  assert.match(s.run('kubectl create deployment api --image=nginx').out[0], /etcdserver: request timed out/);
  assert.equal(s.status().completed, 2);
  s.run('fault start etcd-2');
  assert.equal(s.verdict(), 'degraded');
  assert.equal(s.status().completed, 3);
  s.run('kubectl create deployment api --image=nginx');
  assert.equal(s.status().done, true);
});

test('task steps are ordered: a write that happened BEFORE the fault does not satisfy "write while degraded"', () => {
  const s = session('etcd-quorum', 'tolerate-one');
  s.run('kubectl create deployment early --image=nginx');
  s.run('etcdctl endpoint health --cluster');
  assert.equal(s.status().completed, 0, 'nothing counts before the first step');
  s.run('fault stop etcd-0');
  assert.equal(s.status().completed, 1);
  s.run('kubectl create deployment web --image=nginx');
  assert.equal(s.status().completed, 1, 'health check must come before the degraded write');
  s.run('etcdctl endpoint health --cluster');
  s.run('kubectl create deployment web2 --image=nginx');
  assert.equal(s.status().completed, 3);
  assert.equal(s.status().next.hint, 'fault start etcd-1');
  s.run('fault start etcd-0');
  assert.equal(s.status().done, true);
});

test('control plane: scheduler manifest out → scale-up Pending with <none>; back in → bound; API down → kubectl refused, crictl still works', () => {
  const s = session('control-plane-failure', 'pending-scale');
  s.run('sudo mv /etc/kubernetes/manifests/kube-scheduler.yaml /tmp/');
  assert.equal(s.state.schedUp, false);
  assert.ok(!/kube-scheduler/.test(s.run('ls /etc/kubernetes/manifests').out[0]));
  s.run('kubectl scale deploy/web --replicas=5');
  const pods = s.run('kubectl get pods').out.join('\n');
  assert.equal((pods.match(/Pending\s+0\s+8s\s+<none>/g) || []).length, 2);
  assert.match(s.run('kubectl get deploy').out[1], /web\s+3\/5\s+5\s+3/);
  s.run('sudo mv /tmp/kube-scheduler.yaml /etc/kubernetes/manifests/');
  assert.ok(!/Pending/.test(s.run('kubectl get pods').out.join('\n')));
  assert.equal(s.status().done, true);

  const k = session('control-plane-failure', 'pending-scale');
  k.run('sudo mv /etc/kubernetes/manifests/kube-controller-manager.yaml /tmp/');
  k.run('kubectl scale deployment web --replicas=5');
  assert.equal((k.run('kubectl get pods').out.length - 1), 3, 'no ReplicaSet controller → no new pod objects at all');
  assert.equal(k.status().completed, 0, 'wrong component broken: Pending step never satisfied');

  const a = session('control-plane-failure', 'api-blind');
  a.run('sudo mv /etc/kubernetes/manifests/kube-apiserver.yaml /tmp/');
  const r = a.run('kubectl get nodes');
  assert.equal(r.exit, 1);
  assert.match(r.out[0], /connection to the server 10\.0\.0\.10:6443 was refused/);
  const c = a.run('sudo crictl ps').out.join('\n');
  assert.ok(!/kube-apiserver/.test(c) && /kube-scheduler/.test(c));
  a.run('sudo mv /tmp/kube-apiserver.yaml /etc/kubernetes/manifests/');
  a.run('kubectl get nodes');
  assert.equal(a.status().done, true);
  assert.equal(a.run('mv /etc/kubernetes/manifests/etcd.yaml /tmp/').exit, 2, 'unmodelled component is honest, not silently applied');
});

test('scheduling: real FailedScheduling reasons in filter order; label needs --overwrite; untaint binds db to node-c', () => {
  const s = session('sched-taints', 'schedule-db');
  const ev = s.run('kubectl describe pod db').out.join('\n');
  assert.match(ev, /0\/3 nodes are available: 1 node\(s\) didn't match Pod's node affinity\/selector, 1 node\(s\) had untolerated taint \{gpu: true\}, 1 node\(s\) had untolerated taint \{maintenance: true\}/);
  const no = s.run('kubectl label nodes node-c disktype=nvme');
  assert.equal(no.exit, 1);
  assert.match(no.out[0], /'disktype' already has a value \(hdd\), and --overwrite is false/);
  s.run('kubectl label nodes node-c disktype=nvme --overwrite');
  assert.match(s.run('kubectl describe pod db').out.join('\n'), /untolerated taint \{maintenance: true\}/, 'label alone is not enough');
  s.run('kubectl taint nodes node-c maintenance=true:NoExecute-');
  assert.equal(s.run('kubectl taint nodes node-c maintenance:NoExecute-').exit, 1, 'second removal: not found');
  assert.match(s.run('kubectl get pods -o wide').out.join('\n'), /db\s+1\/1\s+Running\s+node-c/);
  assert.equal(s.status().done, true);
  const c = session('sched-taints', 'cordon');
  c.run('kubectl cordon node-a');
  assert.match(c.run('kubectl get nodes').out[1], /node-a\s+Ready,SchedulingDisabled/);
  assert.match(c.run('kubectl describe pod db').out.join('\n'), /1 node\(s\) were unschedulable/);
  assert.match(c.run('kubectl get pods').out.join('\n'), /web-5d9c7-a1\s+1\/1\s+Running\s+node-a/, 'cordon does not evict');
  c.run('kubectl uncordon node-a');
  assert.equal(c.status().done, true);
});

test('HPA: <unknown> without requests; set resources → ceil(2×120/50)=5; maxReplicas 3 → ScalingLimited; metrics-server 0 → top fails', () => {
  const s = session('hpa-scale', 'unknown-target');
  assert.match(s.run('kubectl get hpa').out[1], /cpu: <unknown>\/50%\s+2\s+5\s+2/);
  assert.match(s.run('kubectl describe hpa web').out.join('\n'), /ScalingActive\s+False\s+FailedGetResourceMetric.*missing request for cpu/);
  s.run('kubectl set resources deployment web --requests=cpu=200m');
  assert.match(s.run('kubectl get hpa').out[1], /cpu: 120%\/50%\s+2\s+5\s+5/);
  assert.equal(s.status().done, true);
  const c = session('hpa-scale', 'ceiling');
  c.run('kubectl run load-generator --image=busybox -- /bin/sh -c "while true; do wget -q -O- http://web; done"');
  assert.match(c.run('kubectl describe hpa web').out.join('\n'), /ScalingLimited\s+True\s+TooManyReplicas/);
  assert.equal(c.run(`kubectl patch hpa web -p '{"spec":{"maxReplicas":7}}'`).exit, 2, 'unmodelled value is honest');
  assert.equal(c.run(`kubectl patch hpa web -p '{bad'`).exit, 1);
  c.run(`kubectl patch hpa web -p '{"spec":{"maxReplicas":5}}'`);
  c.run('kubectl get hpa');
  assert.equal(c.status().done, true);
  c.run('kubectl scale deployment metrics-server -n kube-system --replicas=0');
  assert.deepEqual(c.run('kubectl top pods').out, ['error: Metrics API not available']);
  c.run('kubectl delete pod load-generator');
  assert.equal(c.state.spike, false);
});

test('AWS: Single-AZ is a SPOF (503); --multi-az then AZ fault keeps 200; curl exit 22 only with -f', () => {
  const s = session('aws-az-failure', 'spof');
  s.run('fault az us-east-1a down');
  const c = s.run('curl -sI https://shop.example.com');
  assert.equal(c.out[0], 'HTTP/2 503');
  assert.equal(c.exit, 0, 'plain curl exits 0 on an HTTP error');
  assert.equal(s.run('curl -fsS https://shop.example.com').exit, 22);
  const th = JSON.parse(s.run('aws elbv2 describe-target-health --target-group-arn shop-web-tg').out.join('\n'));
  assert.ok(th.TargetHealthDescriptions.some(t => t.TargetHealth.State === 'healthy' && t.Target.AvailabilityZone === 'us-east-1b'));
  assert.equal(s.status().done, true);
  const m = session('aws-az-failure', 'survive-az');
  assert.equal(JSON.parse(m.run('aws rds describe-db-instances --db-instance-identifier shop-db').out.join('\n')).DBInstances[0].MultiAZ, false);
  const mod = m.run('aws rds modify-db-instance --db-instance-identifier shop-db --multi-az --apply-immediately');
  assert.match(mod.out[mod.out.length - 1], /^# sim: applied instantly; a real conversion takes minutes/);
  m.run('fault az us-east-1a down');
  const db = JSON.parse(m.run('aws rds describe-db-instances --db-instance-identifier shop-db').out.join('\n')).DBInstances[0];
  assert.equal(db.AvailabilityZone, 'us-east-1b', 'standby promoted');
  assert.equal(m.run('curl -sI https://shop.example.com').out[0], 'HTTP/2 200');
  assert.equal(m.status().done, true);
});

test('honesty: unknown binaries → 127, unmodelled subcommands never invent output, help states the scope', () => {
  const s = session('hpa-scale');
  const a = s.run('rm -rf /');
  assert.equal(a.exit, 127);
  assert.match(a.out[0], /bash: rm: command not found {2}\(simulated shell — type help\)/);
  const b = s.run('kubectl get secrets -A');
  assert.equal(b.exit, 2);
  assert.match(b.out[0], /not modelled in this drill \(simulated shell — no output is invented\)/);
  assert.equal(b.set, null);
  const h = s.run('help');
  assert.match(h.out[0], /Not a real shell, not a cluster/);
  assert.equal(s.run('clear').action, 'clear');
  assert.equal(s.run('reset').action, 'reset');
  assert.equal(s.run('   ').out.length, 0);
  assert.deepEqual(C.complete('hpa-scale', 'kubectl get h'), ['kubectl get hpa']);
  assert.equal(C.run('nope', {}, 'help').exit, 2);
});

test('every example command in every pack is modelled (no "not modelled" on the advertised list)', () => {
  for (const id of C.list()) {
    const p = C.pack(id);
    for (const ex of p.examples) {
      const s = session(id);
      const r = s.run(ex);
      assert.ok(r.exit !== 127 && !/not modelled/.test(r.out.join(' ')), `${id}: ${ex} → ${r.out[0]}`);
    }
    for (const tk of p.tasks) for (const st of tk.steps) {
      for (const cmd of st.hint.split(/\s{2}then\s{2}/)) {
        const s = session(id, tk.id);
        const r = s.run(cmd);
        assert.ok(r.exit !== 127 && !/not modelled/.test(r.out.join(' ')), `${id}/${tk.id} hint: ${cmd} → ${r.out[0]}`);
      }
    }
  }
});

test('manifest declares the CLI lab honestly and matches the runtime packs', () => {
  const m = JSON.parse(readFileSync(path.join(root, 'docs/assets/scenes/manifest.json'), 'utf8'));
  const c = m.sims.cli;
  assert.equal(c.version, C.VERSION);
  assert.deepEqual(c.packs.map(p => p.sim).sort(), C.list().sort());
  for (const p of c.packs) assert.deepEqual(p.tasks, C.pack(p.sim).tasks.map(t => t.id));
  assert.match(c.honesty, /Not a real shell, container, cluster, AWS account or hosted lab fleet/);
  assert.match(c.analytics[0], /never the raw command text/);
  assert.match(m.sims.player, /v1\.9\.0/);
  const html = readFileSync(path.join(root, 'docs/immersive/index.html'), 'utf8');
  assert.ok(html.indexOf('il-immersive-cli.js') > html.indexOf('il-immersive-sims.js'), 'CLI loads after the rules engine');
  assert.ok(html.indexOf('il-immersive-cli.js') < html.indexOf('il-immersive-3d.js'), 'CLI loads before the player');
});

test('no task is pre-solved by its setup, and every task is solvable by replaying its own hints', () => {
  for (const id of C.list()) for (const tk of C.pack(id).tasks) {
    const s = session(id, tk.id);
    assert.equal(s.status().completed, 0, `${id}/${tk.id} starts at 0`);
    for (const st of tk.steps) for (const cmd of st.hint.split(/\s{2}then\s{2}/)) s.run(cmd);
    assert.equal(s.status().done, true, `${id}/${tk.id} solvable from hints (${s.status().completed}/${s.status().total})`);
  }
});

test('state steps latch in order: toggles (non-CLI changes) count via reconcile, and recovering does not un-complete', () => {
  const s = session('etcd-quorum', 'lose-quorum');
  let state = S.merge(s.state, { m1: false, m2: false }); /* user flips two 3D toggles */
  C.reconcile('etcd-quorum', state, s.ctx);
  assert.equal(C.taskStatus('etcd-quorum', 'lose-quorum', state, s.ctx).completed, 1);
  C.run('etcd-quorum', state, 'kubectl create deployment x --image=nginx', s.ctx);
  state = S.merge(state, { m1: true });
  C.reconcile('etcd-quorum', state, s.ctx);
  const st = C.taskStatus('etcd-quorum', 'lose-quorum', state, s.ctx);
  assert.equal(st.completed, 3, 'below-quorum step stays latched after quorum returns');
});

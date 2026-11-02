/**
 * 2026-10-27 Musk-bar pass: CLI packs for the last two drills without a typed task — CNI (cni-network on the authored
 * cni-pod-network.glb) and service-mesh mTLS (mesh-mtls on the authored service-mesh-sidecar.glb). No new asset and no
 * rules-engine change: the packs drive the existing sim state. Generic tip/focus/replay/solvability coverage comes from
 * the loops in immersive-cli.test.js / immersive-cli-packs.test.js, which iterate C.list() (15 packs).
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
const CNI = 'cni-network', MESH = 'mesh-mtls';
const X = 'kubectl exec deploy/client -- ';
const PAY = 'kubectl exec -n shop deploy/frontend -- curl -s -m 3 http://payments.payments:8080/headers';

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

test('v1.6.0: two new packs (3 tasks each) on the EXISTING authored assets — no new .glb, no rules-engine change', () => {
  assert.equal(C.VERSION, '1.6.0');
  assert.equal(S.VERSION, '1.6.0', 'rules engine untouched since 2026-10-23');
  assert.deepEqual(C.pack(CNI).tasks.map(t => t.id), ['no-cni', 'cidr-overlap', 'no-kube-proxy']);
  assert.deepEqual(C.pack(MESH).tasks.map(t => t.id), ['strict-reset', 'permissive-to-strict', 'istiod-down']);
  assert.equal(S.get(CNI).glb, '/assets/immersive/cni-pod-network.glb');
  assert.equal(S.get(MESH).glb, '/assets/immersive/service-mesh-sidecar.glb');
  const steps = id => C.pack(id).tasks.reduce((n, t) => n + t.steps.length, 0);
  assert.deepEqual([steps(CNI), steps(MESH)], [22, 20]);
  for (const id of [CNI, MESH]) for (const tk of C.pack(id).tasks) for (const k of Object.keys(tk.setup)) assert.ok(k in S.get(id).initial, `${id}/${tk.id} setup key ${k} is real sim state`);
});

test('no-cni: NotReady + Pending CoreDNS + NetworkPluginNotReady + empty net.d; exec into an unscheduled pod fails; Calico fixes it; 7/7', () => {
  const s = session(CNI, 'no-cni');
  assert.equal(s.derived().verdict, 'down');
  assert.ok(s.run('kubectl get nodes').out.slice(1).every(l => /NotReady/.test(l)));
  const ks = s.run('kubectl get pods -n kube-system -o wide').out.join('\n');
  assert.match(ks, /coredns-\S+\s+0\/1\s+Pending/);
  assert.match(ks, /kube-proxy-\S+\s+1\/1\s+Running/, 'hostNetwork pods run without a CNI');
  assert.doesNotMatch(ks, /calico-node/);
  assert.match(s.run('kubectl describe node node-0').out.join('\n'), /NetworkReady=false reason:NetworkPluginNotReady message:Network plugin returns error: cni plugin not initialized/);
  assert.match(s.run('kubectl describe node node-1').out.join('\n'), /Taints:\s+node\.kubernetes\.io\/not-ready:NoSchedule/);
  assert.deepEqual(s.run('ls /etc/cni/net.d').out, []);
  assert.match(s.run(X + 'ping -c 2 192.168.77.3').out[0], /does not have a host assigned/);
  assert.match(s.run('kubectl get ippools').out[0], /doesn't have a resource type/);
  assert.match(s.run('cat calico.yaml').out[0], /lab excerpt \(sim\)/);
  const a = s.run('kubectl apply -f calico.yaml');
  assert.match(a.out.join('\n'), /daemonset\.apps\/calico-node created[\s\S]*\(sim\) output trimmed/);
  assert.equal(s.state.cniInstalled, true);
  assert.equal(s.run('kubectl apply -f calico.yaml').set, null, 'second apply is unchanged');
  assert.match(s.run('ls /etc/cni/net.d').out[0], /10-calico\.conflist/);
  assert.match(s.run('cat /etc/cni/net.d/10-calico.conflist').out.join('\n'), /"type": "calico-ipam"/);
  s.run('kubectl get nodes');
  s.run('kubectl get pods -n kube-system');
  assert.equal(s.status().done, true);
  assert.equal(s.derived().verdict, 'healthy');
});

test('cidr-overlap: same node answers, cross-node does not; restarts before the migration change nothing; Calico order fixes it; 8/8', () => {
  const s = session(CNI, 'cidr-overlap');
  assert.equal(s.run(X + 'ping -c 2 10.0.77.3').exit, 1);
  assert.match(s.run(X + 'ping -c 2 10.0.10.5').out.join('\n'), /2 packets received, 0% packet loss/);
  const wide = s.run('kubectl get pods -o wide').out.join('\n');
  assert.match(wide, /web-\S+\s+1\/1\s+Running\s+0\s+9d\s+10\.0\.77\.3\s+node-1/);
  assert.match(s.run('kubectl get nodes -o wide').out.join('\n'), /node-1\s+Ready\s+<none>\s+9d\s+v1\.37\.1\s+10\.0\.2\.11/);
  assert.match(s.run('kubectl get ippool default-ipv4-ippool -o yaml').out.join('\n'), /cidr: 10\.0\.0\.0\/16\n\s+disabled: false/);
  /* wrong orders are explained, never silently accepted */
  assert.match(s.run('kubectl rollout restart deployment').out.join('\n'), /still get addresses from default-ipv4-ippool/);
  assert.match(s.run('kubectl patch ippool default-ipv4-ippool --type merge -p \'{"spec":{"disabled":true}}\'').out[1], /create the replacement pool first/);
  assert.equal(s.state.cidrOverlap, true);
  s.run('kubectl apply -f new-pool.yaml');
  assert.match(s.run('kubectl get ippools').out.join('\n'), /new-pool/);
  s.run('kubectl patch ippool default-ipv4-ippool --type merge -p \'{"spec":{"disabled":true}}\'');
  assert.match(s.run('kubectl rollout restart deployment web').out.join('\n'), /still on the old range: client, coredns/);
  assert.equal(s.state.cidrOverlap, true, 'every pod has to move');
  s.run('kubectl rollout restart deployment');
  s.run('kubectl rollout restart deployment coredns -n kube-system');
  assert.equal(s.state.cidrOverlap, false);
  assert.match(s.run('kubectl get ippool default-ipv4-ippool -o yaml').out.join('\n'), /disabled: true/);
  assert.equal(s.run(X + 'ping -c 2 192.168.77.3').exit, 0);
  assert.equal(s.status().done, true);
  assert.equal(s.derived().verdict, 'healthy');
});

test('no-kube-proxy: names fail (DNS rides the kube-dns VIP), pod IPs answer, ClusterIP times out, ping a ClusterIP never answers; kubeadm addon restores; 7/7', () => {
  const s = session(CNI, 'no-kube-proxy');
  assert.equal(s.run(X + 'curl -s -m 3 http://web').exit, 6);
  assert.match(s.run(X + 'nslookup web').out[0], /connection timed out; no servers could be reached/);
  assert.equal(s.run(X + 'curl -s -m 3 http://192.168.77.3').exit, 0);
  assert.equal(s.run(X + 'curl -s -m 3 http://10.96.45.12').exit, 28);
  const ds = s.run('kubectl get daemonsets -n kube-system').out.join('\n');
  assert.match(ds, /calico-node/);
  assert.doesNotMatch(ds, /kube-proxy/);
  assert.match(s.run('sudo kubeadm init phase addon kube-proxy').out[0], /\[addons\] Applied essential addon: kube-proxy/);
  assert.equal(s.state.kubeProxy, true);
  assert.match(s.run(X + 'ping -c 2 10.96.45.12').out.join('\n'), /ClusterIP is a virtual IP[\s\S]*100% packet loss/, 'ICMP to a ClusterIP is not forwarded (iptables/nftables mode)');
  assert.equal(s.run(X + 'curl -s -m 3 http://10.96.45.12').exit, 0);
  assert.equal(s.run(X + 'curl -s -m 3 http://web').exit, 0);
  assert.match(s.run(X + 'nslookup web').out.join('\n'), /Name:\tweb\.default\.svc\.cluster\.local\nAddress: 10\.96\.45\.12/);
  assert.equal(s.status().done, true);
});

test('CNI free play: CoreDNS scaled to 0 breaks names but not the ClusterIP; scale back fixes it; honest refusals', () => {
  const s = session(CNI, null, { corednsUp: false });
  assert.match(s.run('kubectl get deployments -n kube-system').out.join('\n'), /coredns\s+0\/0/);
  assert.equal(s.run(X + 'curl -s -m 3 http://web').exit, 6);
  assert.equal(s.run(X + 'curl -s -m 3 http://10.96.45.12').exit, 0);
  s.run('kubectl scale deployment coredns -n kube-system --replicas=2');
  assert.equal(s.run(X + 'curl -s -m 3 http://web').exit, 0);
  assert.match(s.run('ping 192.168.77.3').out[0], /not inside the pod network/);
  assert.equal(s.run('kubeadm reset').exit, 2);
  assert.match(s.run('fault cidr sideways').out[0], /^usage: fault cni/);
  assert.match(s.run('fault kube-proxy off').out[0], /lab fault injection.*simulated/);
  assert.equal(s.state.kubeProxy, false);
  const h = s.run('help').out.join('\n');
  assert.match(h, /Not a real shell, not a cluster/);
  assert.match(h, /stands in for calicoctl or the Calico API server/);
  assert.match(h, /trimmed stand-ins for the real manifests/);
});

test('strict-reset: reset by peer under STRICT, 1/1 pods, no label; label alone does not mesh running pods; restart does; XFCC proves mTLS; 7/7', () => {
  const s = session(MESH, 'strict-reset');
  const r = s.run(PAY);
  assert.equal(r.exit, 56);
  assert.match(r.out[0], /curl: \(56\) Recv failure: Connection reset by peer/);
  assert.match(s.run('kubectl get peerauthentication -n payments').out[1], /^default\s+STRICT\s+21d$/);
  assert.ok(s.run('kubectl get pods -n shop').out.slice(1).every(l => /\s1\/1\s/.test(l)));
  assert.doesNotMatch(s.run('kubectl get namespace shop --show-labels').out[1], /istio-injection/);
  s.run('kubectl label namespace shop istio-injection=enabled');
  assert.equal(s.run('kubectl label namespace shop istio-injection=enabled').out[0], 'namespace/shop not labeled', 'idempotent like kubectl');
  assert.ok(s.run('kubectl get pods -n shop').out.slice(1).every(l => /\s1\/1\s/.test(l)), 'injection runs only at pod creation');
  assert.equal(s.run(PAY).exit, 56);
  assert.match(s.run('kubectl get namespaces -L istio-injection').out.join('\n'), /shop\s+Active\s+21d\s+enabled/);
  s.run('kubectl rollout restart deployment/frontend -n shop');
  assert.ok(s.run('kubectl get pods -n shop').out.slice(1).every(l => /\s2\/2\s/.test(l)));
  const ok = s.run(PAY).out.join('\n');
  assert.match(ok, /"X-Forwarded-Client-Cert": "By=spiffe:\/\/cluster\.local\/ns\/payments\/sa\/payments;.*URI=spiffe:\/\/cluster\.local\/ns\/shop\/sa\/frontend"/);
  assert.equal(s.status().done, true);
  assert.equal(s.derived().verdict, 'healthy');
  assert.equal(s.run('kubectl label namespace shop istio-injection-').exit, 2, 'removing the label is not modelled (running pods would keep sidecars)');
});

test('restart BEFORE the label leaves pods unmeshed (label resets "recreated after label")', () => {
  const s = session(MESH, 'strict-reset');
  s.run('kubectl rollout restart deployment/frontend -n shop');
  s.run('kubectl label namespace shop istio-injection=enabled');
  assert.equal(s.state.restarted, false);
  assert.equal(s.run(PAY).exit, 56);
});

test('permissive-to-strict: plaintext accepted without XFCC, mesh the client first, then STRICT keeps working; 7/7', () => {
  const s = session(MESH, 'permissive-to-strict');
  const plain = s.run(PAY);
  assert.equal(plain.exit, 0);
  assert.doesNotMatch(plain.out.join('\n'), /X-Forwarded-Client-Cert/);
  assert.match(s.run('kubectl get peerauthentication default -n payments -o yaml').out.join('\n'), /apiVersion: security\.istio\.io\/v1[\s\S]*mode: PERMISSIVE/);
  assert.match(s.run('cat pa-strict.yaml').out.join('\n'), /mode: STRICT/);
  s.run('kubectl label namespace shop istio-injection=enabled');
  s.run('kubectl rollout restart deployment/frontend -n shop');
  s.run('kubectl get pods -n shop');
  assert.match(s.run(PAY).out.join('\n'), /X-Forwarded-Client-Cert/);
  assert.equal(s.run('kubectl apply -f pa-strict.yaml').out[0], 'peerauthentication.security.istio.io/default configured');
  assert.equal(s.run('kubectl apply -f pa-strict.yaml').out[0], 'peerauthentication.security.istio.io/default unchanged');
  assert.equal(s.run(PAY).exit, 0);
  assert.equal(s.status().done, true);
  assert.equal(s.run('kubectl create -f pa-strict.yaml').exit, 1, 'create on an existing object is AlreadyExists');
});

test('istiod-down: data plane keeps mTLS, injection webhook (failurePolicy Fail) blocks new pods, proxy-status cannot reach istiod; scale-up completes the rollout; 6/6', () => {
  const s = session(MESH, 'istiod-down');
  assert.match(s.run(PAY).out.join('\n'), /X-Forwarded-Client-Cert/);
  assert.match(s.run('istioctl proxy-status').out[0], /^Error: unable to find any Istiod instances$/);
  assert.equal(s.run('kubectl get events -n shop').out[0], 'No events found in shop namespace.');
  s.run('kubectl rollout restart deployment/frontend -n shop');
  assert.match(s.run('kubectl get events -n shop').out[1], /FailedCreate\s+replicaset\/frontend-\S+\s+Error creating: Internal error occurred: failed calling webhook "namespace\.sidecar-injector\.istio\.io".*no endpoints available for service "istiod"/);
  assert.match(s.run('kubectl rollout status deployment/frontend -n shop').out[0], /0 out of 2 new replicas have been updated/);
  assert.match(s.run('kubectl get deployments -n istio-system').out[1], /^istiod\s+0\/0/);
  assert.match(s.run('kubectl scale deployment istiod -n istio-system --replicas=1').out[1], /ReplicaSet controller retries/);
  assert.match(s.run('kubectl rollout status deployment/frontend -n shop').out[0], /successfully rolled out/);
  assert.ok(s.run('istioctl proxy-status').out.some(l => /^frontend-\S+\.shop\s+Kubernetes\s+SYNCED/.test(l)));
  assert.equal(s.status().done, true);
  assert.equal(s.derived().verdict, 'healthy');
});

test('webhook scope: with istiod down, a rollout in an UNLABELLED namespace is not intercepted', () => {
  const s = session(MESH, null, { nsLabeled: false, restarted: false, strict: false, cpUp: false });
  const r = s.run('kubectl rollout restart deployment/frontend -n shop');
  assert.ok(r.events.includes('rollout-plain'));
  assert.equal(s.run('kubectl get events -n shop').out[0], 'No events found in shop namespace.');
});

test('voice + coach: istioctl / peer authentication / ip pool / kubeadm normalise; coach tips never leak the command; analytics verb is the binary', () => {
  assert.deepEqual(C.fromSpeech('istio control proxy status', MESH), { line: 'istioctl proxy-status', verb: false });
  assert.deepEqual(C.fromSpeech('kubectl get peer authentication dash n payments', MESH), { line: 'kubectl get peerauthentication -n payments', verb: false });
  assert.deepEqual(C.fromSpeech('kubectl get ip pools', CNI), { line: 'kubectl get ippools', verb: false });
  assert.deepEqual(C.fromSpeech('sudo kube adm init phase addon kube dash proxy', CNI), { line: 'sudo kubeadm init phase addon kube-proxy', verb: false });
  const s = session(MESH, 'strict-reset');
  for (const l of [PAY, 'kubectl get peerauthentication -n payments', 'kubectl get pods -n shop', 'kubectl get namespace shop --show-labels']) s.run(l);
  C.coach(MESH, 'strict-reset', s.state, s.ctx);
  const c = C.coach(MESH, 'strict-reset', s.state, s.ctx);
  assert.equal(c.step, 4);
  assert.equal(c.level, 'hint');
  assert.ok(!c.lines.join('\n').includes('istio-injection=enabled'), 'hint level does not print the command');
  assert.match(c.focus, /mesh-control-plane/);
  assert.equal(C.coach(MESH, 'strict-reset', s.state, s.ctx, { count: false, level: 'solution' }).solution, 'kubectl label namespace shop istio-injection=enabled');
  assert.equal(s.run('istioctl proxy-status').verb, 'istioctl');
  assert.equal(session(CNI).run('sudo kubeadm init phase addon coredns').verb, 'kubeadm');
});

test('scope + wiring: mesh stays off the graded CKA paper, CNI stays Services & Networking; manifest, page copy and curriculum rows are honest', () => {
  const all = E.BLUEPRINT.reduce((a, b) => a.concat(b.sims), []);
  assert.ok(!all.includes(MESH), 'Istio is not CKA core');
  assert.ok(E.BLUEPRINT.find(b => b.domain === 'Services & Networking').sims.includes(CNI));
  const m = JSON.parse(readFileSync(path.join(root, 'docs/assets/scenes/manifest.json'), 'utf8'));
  assert.equal(m.sims.cli.version, C.VERSION);
  assert.deepEqual(m.sims.cli.packs.find(p => p.sim === CNI).tasks, ['no-cni', 'cidr-overlap', 'no-kube-proxy']);
  assert.match(m.sims.cli.cniNote, /No live cluster, no real Calico, no VPC routing, no clock/);
  assert.match(m.sims.cli.meshNote, /no live mesh, no real Envoy or istiod/);
  assert.match(m.sims.player, /15 packs/);
  assert.equal(m.cka_coverage.liveUnrealHost, false);
  assert.equal(m.cka_coverage.hostedFleet, false);
  const html = readFileSync(path.join(root, 'docs/immersive/index.html'), 'utf8');
  assert.match(html, /id="cka-cni"[\s\S]*?CLI lab \(2026-10-27\)[\s\S]*?no live cluster and no real Calico/);
  assert.match(html, /id="cka-service-mesh"[\s\S]*?CLI lab \(2026-10-27\)[\s\S]*?no live mesh and no real Envoy or istiod/);
  for (const f of ['labs.json', 'mirror.json']) {
    const j = JSON.parse(readFileSync(path.join(root, 'docs/curriculum-os', f), 'utf8'));
    const items = j.items || j.labs;
    assert.match(items.find(l => l.id === 'lab-sim-cni-network').summary, /3-task simulated CLI lab/, f);
    assert.match(items.find(l => l.id === 'lab-sim-mesh-mtls').summary, /3-task simulated CLI lab/, f);
  }
});

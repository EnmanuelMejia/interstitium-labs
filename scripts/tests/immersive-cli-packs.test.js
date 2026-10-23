/**
 * 2026-10-20 Musk-bar pass: four new CLI packs (NetworkPolicy, RBAC, storage reclaim, Ingress API),
 * coach-driven CLI review cards in the existing on-device Leitner queue, and the spoken-command normaliser.
 * Pure UMD — the browser runs exactly this code. Tip/focus coverage for every task is asserted by the
 * generic loops in immersive-cli.test.js, which iterate C.list() (9 packs on 2026-10-20; 11 since 2026-10-21).
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

function session(sim, taskId) {
  const tk = taskId ? C.task(sim, taskId) : null;
  let state = S.merge(S.get(sim).initial, tk ? tk.setup : {});
  const ctx = C.newCtx(taskId);
  return {
    ctx,
    get state() { return state; },
    run(line) { const r = C.run(sim, state, line, ctx); if (r.set) state = S.merge(state, r.set); return r; },
    status() { return C.taskStatus(sim, taskId, state, ctx); },
    derived() { return S.get(sim).derive(state); }
  };
}
const SCAN = 'kubectl exec -n untrusted deploy/scanner -- curl -s -m 3 http://api.backend:8080';
const WEB = 'kubectl exec -n frontend deploy/web -- curl -s -m 3 http://api.backend:8080';
const NEW_PACKS = ['netpol-isolation', 'rbac-authz', 'storage-csi', 'ingress-routing'];

test('the four new packs exist, each with 3 ordered tasks, and the scene state they drive is real rules-engine state', () => {
  for (const id of NEW_PACKS) {
    const p = C.pack(id);
    assert.ok(p, id);
    assert.equal(p.tasks.length, 3, id);
    for (const tk of p.tasks) assert.ok(tk.steps.length >= 4, `${id}/${tk.id} has ≥4 ordered steps`);
  }
});

test('NetworkPolicy: probes are open before policy, deny-all drops even frontend, allow-frontend re-opens only frontend', () => {
  const s = session('netpol-isolation', 'lock-api');
  let r = s.run(SCAN);
  assert.equal(r.exit, 0);
  assert.ok(r.events.includes('probe-untrusted-open'));
  s.run('kubectl apply -f api-deny-all.yaml');
  r = s.run(WEB);
  assert.equal(r.exit, 28, 'deny-all drops frontend too');
  assert.match(r.out.join('\n'), /curl: \(28\) Connection timed out/);
  r = s.run('kubectl apply -f api-allow-frontend.yaml');
  assert.match(r.out[0], /networkpolicy\.networking\.k8s\.io\/api-netpol configured/);
  assert.equal(s.run(WEB).exit, 0);
  assert.equal(s.run(SCAN).exit, 28);
  assert.equal(s.status().done, true);
  assert.equal(s.derived().verdict, 'healthy', 'typed commands re-tint the authored scene');
});

test('NetworkPolicy: on a non-enforcing CNI (flannel) the policy exists but is ignored until the CNI enforces it', () => {
  const s = session('netpol-isolation', 'flannel');
  assert.match(s.run('kubectl get networkpolicy -n backend').out.join('\n'), /api-netpol/);
  assert.equal(s.run(SCAN).exit, 0, 'policy present, but flannel does not enforce it');
  assert.match(s.run('kubectl get daemonsets -A').out.join('\n'), /kube-flannel-ds/);
  assert.match(s.run('fault cni calico').out[0], /lab fault injection.*simulated/);
  assert.equal(s.run(SCAN).exit, 28);
  assert.equal(s.status().done, true);
});

test('NetworkPolicy egress: lockdown without a DNS rule breaks nslookup; describe shows Egress; DNS rule restores it', () => {
  const s = session('netpol-isolation', 'egress-dns');
  s.run('kubectl apply -f api-egress-lockdown.yaml');
  const dns = 'kubectl exec -n backend deploy/api -- nslookup db.backend.svc.cluster.local';
  assert.notEqual(s.run(dns).exit, 0);
  assert.match(s.run('kubectl describe networkpolicy api-netpol -n backend').out.join('\n'), /Egress/);
  s.run('kubectl apply -f api-egress-dns.yaml');
  assert.equal(s.run(dns).exit, 0);
  assert.equal(s.status().done, true);
});

test('RBAC: auth can-i answers yes/no with exit 0/1, --as forbids with the real message, nodes warn they are not namespaced', () => {
  const s = session('rbac-authz', 'least-privilege');
  let r = s.run('kubectl auth can-i list pods -n dev --as alice');
  assert.deepEqual([r.out[0], r.exit], ['no', 1]);
  r = s.run('kubectl get pods -n dev --as alice');
  assert.equal(r.exit, 1);
  assert.match(r.out[0], /^Error from server \(Forbidden\): pods is forbidden: User "alice" cannot list resource "pods" in API group "" in the namespace "dev"$/);
  assert.match(s.run('kubectl auth can-i get nodes -n dev --as alice').out[0], /not namespace scoped/);
  s.run('kubectl create rolebinding alice-pod-reader --role=pod-reader --user=alice -n dev');
  r = s.run('kubectl auth can-i list pods -n dev --as alice');
  assert.deepEqual([r.out[0], r.exit], ['yes', 0]);
  r = s.run('kubectl auth can-i list pods -n prod --as alice');
  assert.deepEqual([r.out[0], r.exit], ['no', 1], 'a RoleBinding is namespaced');
  assert.equal(s.status().done, true);
});

test('RBAC: a service account needs a ClusterRoleBinding for nodes; revoking a RoleBinding forbids again', () => {
  const s = session('rbac-authz', 'cluster-scope');
  const sa = '--as system:serviceaccount:dev:ci-bot';
  assert.equal(s.run('kubectl auth can-i get nodes ' + sa).out[0], 'no');
  s.run('kubectl create clusterrolebinding ci-bot-deployer --clusterrole=deployer --serviceaccount=dev:ci-bot');
  assert.equal(s.run('kubectl auth can-i get nodes ' + sa).out[0], 'yes');
  const v = session('rbac-authz', 'revoke');
  assert.equal(v.run('kubectl auth can-i get secrets -n dev --as bob').out[0], 'yes');
  assert.match(v.run('kubectl get rolebindings -n dev -o wide').out.join('\n'), /bob-secret-reader/);
  assert.match(v.run('kubectl delete rolebinding bob-secret-reader -n dev').out[0], /rolebinding.*"bob-secret-reader" deleted/);
  assert.match(v.run('kubectl get secrets -n dev --as bob').out[0], /Forbidden/);
  assert.equal(v.status().done, true);
});

test('storage: Retain keeps the disk (PV Released), pvc-protection holds a mounted claim, no default class leaves PVCs Pending', () => {
  const s = session('storage-csi', 'retain-data');
  s.run('kubectl patch pv pv-1 -p \'{"spec":{"persistentVolumeReclaimPolicy":"Retain"}}\'');
  const del = s.run('kubectl delete pvc pvc-1');
  assert.match(del.out.join('\n'), /pvc-protection/);
  s.run('kubectl delete pod consumer');
  assert.match(s.run('kubectl get pv').out.join('\n'), /pv-1\s+10Gi\s+RWO\s+Retain\s+Released/);
  assert.equal(s.derived().verdict, 'released');

  const n = session('storage-csi', 'no-default-sc');
  assert.match(n.run('kubectl get pvc').out.join('\n'), /Pending/);
  assert.match(n.run('kubectl describe pvc pvc-1').out.join('\n'), /no storage class is set|FailedBinding/);
  n.run('kubectl patch storageclass csi-gp3 -p \'{"metadata":{"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}\'');
  assert.match(n.run('kubectl get storageclass').out.join('\n'), /csi-gp3 \(default\)/);
});

test('ingress: honest retirement note; no controller → curl 7; Exact path 404 → Prefix 200; missing TLS secret → curl 60 (200 only with -k)', () => {
  assert.match(C.pack('ingress-routing').note, /retired ingress-nginx on 2026-03-24/);
  assert.match(C.pack('ingress-routing').note, /Gateway API/);
  const s = session('ingress-routing', 'exact-404');
  assert.match(s.run('curl -sI https://shop.example.com/api/v1/orders').out[0], /HTTP\/2 404/);
  assert.match(s.run('kubectl get ingress shop -o yaml').out.join('\n'), /pathType: Exact/);
  s.run('kubectl patch ingress shop --type=json -p \'[{"op":"replace","path":"/spec/rules/0/http/paths/0/pathType","value":"Prefix"}]\'');
  assert.match(s.run('curl -sI https://shop.example.com/api/v1/orders').out[0], /HTTP\/2 200/);
  assert.equal(s.status().done, true);
  const t = session('ingress-routing', 'tls');
  assert.equal(t.run('curl -sI https://shop.example.com/api').exit, 60);
  assert.equal(t.run('curl -skI https://shop.example.com/api').exit, 0);
  const z = session('ingress-routing');
  z.run('kubectl delete -f ingress-controller.yaml');
  assert.equal(z.run('curl -sI https://shop.example.com/api').exit, 7);
  assert.equal(z.derived().verdict, 'down');
});

test('lab files: ls / cat show real YAML, apply -f of an unknown file fails like kubectl', () => {
  const s = session('netpol-isolation');
  assert.match(s.run('ls').out.join(' '), /api-deny-all\.yaml/);
  const y = s.run('cat api-allow-frontend.yaml').out.join('\n');
  assert.match(y, /kind: NetworkPolicy/);
  assert.match(y, /namespaceSelector/);
  const r = s.run('kubectl apply -f nope.yaml');
  assert.notEqual(r.exit, 0);
  assert.match(r.out.join(' '), /nope\.yaml/);
});

test('fromSpeech: lab verbs run, spoken commands normalise to real syntax snapped to the drill vocabulary', () => {
  assert.deepEqual(C.fromSpeech('Check', 'rbac-authz'), { line: 'check', verb: true });
  assert.deepEqual(C.fromSpeech('give me a hint please', 'rbac-authz'), { line: 'hint', verb: true });
  assert.deepEqual(C.fromSpeech('Lab Muse, show me the solution', 'rbac-authz'), { line: 'solution', verb: true });
  const cases = [
    ['netpol-isolation', 'kubectl exec dash n untrusted deploy slash scanner dash dash curl dash s dash m three http colon slash slash api dot backend colon 8080', SCAN],
    ['netpol-isolation', 'kubectl describe network policy api dash netpol dash n backend', 'kubectl describe networkpolicy api-netpol -n backend'],
    ['netpol-isolation', 'kubectl apply dash f api dash egress dash dns dot yaml', 'kubectl apply -f api-egress-dns.yaml'],
    ['rbac-authz', 'kubectl create role binding alice dash pod dash reader dash dash role equals pod dash reader dash dash user equals alice dash n dev', 'kubectl create rolebinding alice-pod-reader --role=pod-reader --user=alice -n dev'],
    ['rbac-authz', 'kubectl create cluster role binding ci dash bot dash deployer dash dash cluster role equals deployer dash dash service account equals dev colon ci dash bot', 'kubectl create clusterrolebinding ci-bot-deployer --clusterrole=deployer --serviceaccount=dev:ci-bot'],
    ['storage-csi', 'kubectl delete p v c p v c one', 'kubectl delete pvc pvc-1'],
    ['control-plane-failure', 'sudo m v slash etc slash kubernetes slash manifests slash kube dash scheduler dot yaml slash tmp slash', 'sudo mv /etc/kubernetes/manifests/kube-scheduler.yaml /tmp/'],
    ['control-plane-failure', 'kubectl get pods dash n kube dash system', 'kubectl get pods -n kube-system']
  ];
  for (const [sim, said, want] of cases) assert.deepEqual(C.fromSpeech(said, sim), { line: want, verb: false }, said);
  assert.equal(C.fromSpeech('', 'rbac-authz'), null);
  assert.equal(C.fromSpeech('   ', 'rbac-authz'), null);
});

test('fromSpeech output for every new pack hint is runnable when spoken back (round trip on a sample)', () => {
  const s = session('ingress-routing', 'tls');
  const said = C.fromSpeech('kubectl create secret tls shop dash tls dash dash cert equals shop dot crt dash dash key equals shop dot key', 'ingress-routing');
  assert.equal(said.line, 'kubectl create secret tls shop-tls --cert=shop.crt --key=shop.key');
  assert.equal(s.run(said.line).exit, 0);
});

/* ---------- review cards ---------- */
function sandbox() {
  const sb = { console, localStorage: {
    _d: {},
    getItem(k) { return Object.prototype.hasOwnProperty.call(this._d, k) ? this._d[k] : null; },
    setItem(k, v) { this._d[k] = String(v); },
    removeItem(k) { delete this._d[k]; }
  } };
  sb.globalThis = sb; sb.window = sb;
  for (const f of ['il-immersive-sims.js', 'il-immersive-cli.js', 'il-immersive-exam.js', 'il-immersive-review.js']) {
    vm.runInNewContext(readFileSync(path.join(root, 'docs/assets', f), 'utf8'), sb, { filename: f });
  }
  return { S: sb.ILImmersiveSims, C: sb.ILImmersiveCLI, R: sb.ILImmersiveReview, ls: sb.localStorage };
}
const T0 = Date.UTC(2026, 9, 20, 13, 0, 0);
const MIN = 60e3, DAY = 864e5;

test('cliCheckpoints: one per task step across every pack, keyed sim::cli:task:step, with the solution only in `why`', () => {
  const { R, C: Cx } = sandbox();
  const cps = R.cliCheckpoints();
  const total = Cx.list().reduce((n, id) => n + Cx.pack(id).tasks.reduce((m, t) => m + t.steps.length, 0), 0);
  assert.equal(cps.length, total);
  const cp = cps.find(c => c.k === 'rbac-authz::cli:least-privilege:1');
  assert.ok(cp);
  assert.equal(cp.kind, 'cli');
  assert.equal(cp.step, 1);
  assert.doesNotMatch(cp.q, /kubectl create rolebinding/, 'the card prompt is the step label, not the command');
  assert.match(cp.why, /^Solution: \$ kubectl create rolebinding/);
  assert.deepEqual({ ...R.parseCli('cli:least-privilege:1') }, { taskId: 'least-privilege', step: 1 });
  assert.equal(R.parseCli('scale-down'), null);
});

test('recordCli: a coach rescue queues a box-0 card that the queue serves (due only), pass promotes, review-solution relapses', () => {
  const { S, R } = sandbox();
  assert.equal(R.queue(S, { now: T0, size: 10, topUp: false }).filter(i => i.kind === 'cli').length, 0);
  const r = R.recordCli({ simId: 'netpol-isolation', taskId: 'lock-api', step: 1, how: 'solution', now: T0 });
  assert.equal(r.grade, 'again');
  assert.equal(r.to, 0);
  const q = R.queue(S, { now: T0 + 1000, size: 10 });
  const card = q.find(i => i.kind === 'cli');
  assert.ok(card, 'the CLI card is served');
  assert.equal(card.taskId, 'lock-api');
  assert.equal(card.step, 1);
  assert.equal(card.reason, 'relearn');
  assert.match(card.reasonText, /Lab Muse had to help/);
  assert.equal(q.filter(i => i.kind === 'cli').length, 1, 'CLI cards are never used as top-ups');
  const p = R.recordCli({ simId: 'netpol-isolation', taskId: 'lock-api', step: 1, how: 'pass', ms: 20e3, now: T0 + 2 * MIN });
  assert.equal(p.grade, 'good');
  assert.ok(p.to > 0 && p.dueIn > 0);
  assert.equal(R.queue(S, { now: T0 + 3 * MIN, size: 10 }).filter(i => i.kind === 'cli').length, 0, 'not due again yet');
  const again = R.recordCli({ simId: 'netpol-isolation', taskId: 'lock-api', step: 1, how: 'review-solution', now: T0 + 2 * DAY });
  assert.equal(again.to, 0);
});

test('recordCli: 2 failed checks also queue; counts are kept per reason; mastery stays on predict checkpoints only', () => {
  const { S, R } = sandbox();
  const before = JSON.stringify(R.mastery(S, { now: T0 }));
  R.recordCli({ simId: 'rbac-authz', taskId: 'revoke', step: 2, how: 'check-fail', now: T0 });
  R.recordCli({ simId: 'rbac-authz', taskId: 'revoke', step: 2, how: 'solution', now: T0 + MIN });
  const card = R.load().cards['rbac-authz::cli:revoke:2'];
  assert.equal(card.kind, 'cli');
  assert.deepEqual(JSON.parse(JSON.stringify(card.why)), { 'check-fail': 1, solution: 1 });
  assert.equal(JSON.stringify(R.mastery(S, { now: T0 })), before, 'CLI cards do not inflate or deflate domain mastery');
  assert.equal(R.recordCli({ simId: 'rbac-authz', taskId: '', step: 0, how: 'solution' }), null);
  assert.equal(R.recordCli({ simId: 'rbac-authz', taskId: 'revoke', step: -1, how: 'solution' }), null);
  assert.match(R.speakLine(R.stats({ now: T0 + 2 * MIN }), R.queue(S, { now: T0 + 2 * MIN, size: 10 }), []), /typed CLI step/);
});

test('analytics stay verb-level: the player never puts command text in CLI card / voice events', () => {
  const src = readFileSync(path.join(root, 'docs/assets/il-immersive-3d.js'), 'utf8');
  const card = src.match(/simTrack\('immersive_cli_review_card', \{[^}]*\}/);
  const voice = src.match(/simTrack\('immersive_cli_voice', \{[^}]*\}/g) || [];
  assert.ok(card, 'review-card event exists');
  assert.doesNotMatch(card[0], /line|cmd|hint|transcript/);
  assert.ok(voice.length >= 1);
  for (const v of voice) assert.doesNotMatch(v, /line|cmd|hint|transcript|text/);
});

test('review replay never gives a free pass: replaying steps 1..i-1 lands exactly on step i (not done) for every step (99 on 2026-10-20, 136 on 2026-10-21, 160 since 2026-10-22)', () => {
  let n = 0;
  for (const id of C.list()) for (const tk of C.pack(id).tasks) for (let i = 0; i < tk.steps.length; i++) {
    const s = session(id, tk.id);
    for (let j = 0; j < i; j++) for (const cmd of tk.steps[j].hint.split(/\s{2}then\s{2}/)) { s.run(cmd); C.reconcile(id, s.state, s.ctx); }
    const st = s.status();
    assert.equal(st.completed, i, `${id}/${tk.id} replay to step ${i + 1}`);
    assert.equal(st.steps[i].done, false, `${id}/${tk.id} step ${i + 1} still for the learner`);
    n++;
  }
  assert.equal(n, 160);
});

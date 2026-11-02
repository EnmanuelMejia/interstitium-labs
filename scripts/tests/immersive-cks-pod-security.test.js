/**
 * 2026-10-29 Musk-bar pass: the first CKS (Certified Kubernetes Security Specialist) track. A NEW authored asset,
 * cks-pod-security.glb (kit-v2 + Blender CLI polish), its rules-engine drill (7 predict checkpoints), a 5-task CLI pack,
 * and a timed CKS paper scored on the 6 official CKS domains. Pure UMD, so the browser runs exactly this code. Generic
 * tip/focus/replay/example coverage for the new pack comes from the loops in immersive-cli.test.js /
 * immersive-cli-packs.test.js, which iterate C.list() (16 packs).
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
const SIM = 'cks-pod-security';
const SA = 'system:serviceaccount:payments:api-sa';
const ATT = 'kubectl exec -n default attacker -- curl -s -m 3 http://payments-api.payments:8080';
const WEB = 'kubectl exec -n frontend deploy/web -- curl -s -m 3 http://payments-api.payments:8080';
const MANIFEST = '/etc/kubernetes/manifests/kube-apiserver.yaml';

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

test('NEW asset: cks-pod-security.glb is authored + Blender-polished, the first CKS scene; sim-* nodes hidden when secure', () => {
  const sim = S.get(SIM);
  assert.equal(sim.cert, 'CKS');
  assert.equal(sim.glb, '/assets/immersive/cks-pod-security.glb');
  assert.ok(!S.list().filter(id => id !== SIM).map(id => S.get(id).glb).includes(sim.glb), 'a new asset, not a re-read of an existing scene');
  assert.deepEqual(S.list().filter(id => S.get(id).cert === 'CKS'), [SIM], 'first and only CKS drill');
  const j = glbJson('assets/immersive/cks-pod-security.glb');
  const names = j.nodes.map(n => n.name);
  for (const n of ['kube-apiserver', 'psa-gate', 'sim-psa-reject', 'audit-policy', 'audit-log', 'sim-audit-gap', 'ns-payments', 'psa-label', 'node-kernel', 'seccomp-filter',
    'payments-pod', 'sec-context', 'sim-privileged-flare', 'sa-token', 'secret-db-creds', 'sim-netpol-wall', 'netpol-tablet', 'frontend-pod', 'attacker-pod',
    'edge-frontend-api', 'edge-attacker-api', 'rbac-binding', 'sim-cluster-admin-crown', 'secrets-vault', 'edge-token-secrets']) assert.ok(names.includes(n), n);
  assert.ok(names.some(n => /_LOD1$/.test(n)), 'Blender CLI polish ran (LOD1 decimate duplicates present)');
  const pod = j.nodes.find(n => n.name === 'payments-pod');
  assert.equal(pod.extras.il.topic, SIM, 'pedagogy extras survive polish');
  assert.equal(pod.extras.il.cert, 'CKS');
  const base = sim.derive(sim.initial).rules;
  for (const n of ['sim-psa-reject', 'sim-audit-gap', 'sim-privileged-flare', 'sim-cluster-admin-crown']) assert.equal(S.styleFor(n, base).hide, true, n + ' hidden when secure');
  assert.equal(S.styleFor('sim-netpol-wall', base).hide, false, 'the default-deny wall is part of the secure baseline');
  const at = set => sim.derive(S.merge(sim.initial, set)).rules;
  assert.equal(S.styleFor('sim-psa-reject', at({ podHardened: false })).hide, false);
  assert.equal(S.styleFor('sim-privileged-flare', at({ psaEnforce: false, podHardened: false })).hide, false);
  assert.equal(S.styleFor('sim-cluster-admin-crown', at({ rbacLeast: false })).hide, false);
  assert.equal(S.styleFor('sim-audit-gap', at({ auditOn: false })).hide, false);
  assert.equal(S.styleFor('sim-netpol-wall', at({ denyIngress: false, allowFrontend: false })).hide, true);
});

test('rules engine: Pod Security Admission, seccomp default, NetworkPolicy isolation, RBAC scope and audit backend semantics', () => {
  const sim = S.get(SIM);
  const at = set => S.cksDecide(S.merge(sim.initial, set));
  assert.equal(S.VERSION, '1.7.0');
  assert.equal(sim.derive(sim.initial).verdict, 'healthy');
  assert.equal(S.verdictTone('exposed'), 'bad', 'the new unsafe verdict never renders healthy');
  /* restricted vs a privileged template: every restricted check is listed, in the controller's order */
  const rej = at({ podHardened: false, seccomp: false });
  assert.equal(rej.admitted, false);
  assert.equal(rej.podStatus, 'FailedCreate');
  assert.deepEqual(rej.violations.map(v => v.split(' (')[0]), ['privileged', 'allowPrivilegeEscalation != false', 'unrestricted capabilities', 'runAsNonRoot != true', 'seccompProfile']);
  assert.deepEqual(at({ seccomp: false }).violations.map(v => v.split(' (')[0]), ['seccompProfile'], 'restricted also requires a seccomp profile');
  /* unlabelled namespace = privileged level: the privileged pod runs as root */
  const open = at({ psaEnforce: false, podHardened: false, seccomp: false });
  assert.equal(open.admitted, true);
  assert.equal(open.privilegedRunning, true);
  assert.equal(open.runAsUser, 0);
  assert.equal(at({ psaEnforce: false, seccomp: false }).seccompMode, 0, 'no seccompProfile → Unconfined');
  assert.equal(at({}).seccompMode, 2);
  /* NetworkPolicy: allow-all until a policy selects the pod; deny-all blocks the real client; allow-frontend alone isolates too */
  assert.equal(at({ denyIngress: false, allowFrontend: false }).attackerReach, true);
  const deny = at({ allowFrontend: false });
  assert.deepEqual([deny.attackerReach, deny.frontendReach, deny.egressOk], [false, false, true], 'Ingress-only policy never isolates egress');
  const only = at({ denyIngress: false, allowFrontend: true });
  assert.deepEqual([only.attackerReach, only.frontendReach], [false, true], 'a policy selecting the pod isolates it even without default-deny');
  assert.equal(at({ rbacLeast: false }).saCanReadAllSecrets, true);
  assert.equal(at({ auditOn: false }).auditEvents, false);
  /* verdicts */
  const v = set => sim.derive(S.merge(sim.initial, set)).verdict;
  assert.equal(v({ podHardened: false }), 'rejected');
  assert.equal(v({ psaEnforce: false, podHardened: false }), 'exposed');
  assert.equal(v({ denyIngress: false, allowFrontend: false }), 'exposed');
  assert.equal(v({ rbacLeast: false }), 'exposed');
  assert.equal(v({ allowFrontend: false }), 'down');
  assert.equal(v({ auditOn: false }), 'degraded');
  assert.equal(v({ psaEnforce: false, seccomp: false }), 'degraded');
  /* checkpoints */
  const pre = sim.scenarios.filter(sc => sc.predict);
  assert.equal(pre.length, 7);
  assert.equal(new Set(pre.map(sc => sc.predict.answer)).size, 3, 'keyed answers spread across positions 0-2');
  for (const sc of pre) {
    assert.notEqual(sim.derive(S.merge(sim.initial, sc.set)).verdict, 'healthy', sc.id + ' breaks something');
    assert.ok(sc.predict.why.length > 200, sc.id + ' explains the mechanism');
  }
  assert.match(sim.scenarios.find(s => s.id === 'psa-reject').predict.why, /enforce mode evaluates Pods only; warn and audit modes also evaluate workload templates/);
  assert.match(sim.scenarios.find(s => s.id === 'audit-off').predict.why, /--audit-log-path/);
});

test('psa-enforce: no labels → server dry run → enforce restricted → privileged debug pod Forbidden; task verifies 4/4', () => {
  const s = session('psa-enforce');
  assert.equal(s.run('kubectl apply -f privileged-debug.yaml').exit, 0, 'unlabelled namespace admits a privileged pod');
  assert.ok(s.run('kubectl get ns payments --show-labels').out.some(l => /^payments\s+Active\s+30d\s+kubernetes\.io\/metadata\.name=payments$/.test(l)));
  assert.match(s.run('kubectl label --dry-run=client ns payments pod-security.kubernetes.io/enforce=restricted').out[0], /--dry-run=server/, 'client dry-run never runs admission');
  const dry = s.run('kubectl label --dry-run=server --overwrite ns payments pod-security.kubernetes.io/enforce=restricted');
  assert.deepEqual(dry.out, ['namespace/payments labeled (server dry run)'], 'hardened pods → no warnings');
  assert.equal(s.state.psaEnforce, false, 'dry run changes nothing');
  s.run('kubectl label --overwrite ns payments pod-security.kubernetes.io/enforce=restricted');
  assert.equal(s.state.psaEnforce, true);
  assert.match(s.run('kubectl label ns payments pod-security.kubernetes.io/enforce=restricted').out[0], /already has a value \(restricted\), and --overwrite is false/);
  const f = s.run('kubectl apply -f privileged-debug.yaml');
  assert.equal(f.exit, 1);
  assert.match(f.out[0], /^Error from server \(Forbidden\): error when creating "privileged-debug\.yaml": pods "debug" is forbidden: violates PodSecurity "restricted:latest": privileged \(container "debug" must not set securityContext\.privileged=true\), allowPrivilegeEscalation != false/);
  assert.equal(s.status().total, 4);
  assert.equal(s.status().done, true);
});

test('dry run over running privileged pods warns with the real existing-pods message; enforcing leaves them running', () => {
  const s = session(null, { psaEnforce: false, podHardened: false, seccomp: false });
  const dry = s.run('kubectl label --dry-run=server --overwrite ns payments pod-security.kubernetes.io/enforce=restricted');
  assert.equal(dry.out[0], 'Warning: existing pods in namespace "payments" violate the new PodSecurity enforce level "restricted:latest"');
  assert.match(dry.out[1], /^Warning: payments-api-\S+ \(and 1 other pod\): privileged, allowPrivilegeEscalation != false, unrestricted capabilities, runAsNonRoot != true, seccompProfile$/);
  const real = s.run('kubectl label --overwrite ns payments pod-security.kubernetes.io/enforce=restricted');
  assert.ok(real.out.some(l => /running pods keep running until they are recreated/.test(l)));
  assert.match(s.run('kubectl label ns payments pod-security.kubernetes.io/enforce=baseline --overwrite').out[0], /models enforce=restricted/);
  assert.match(s.run('kubectl label ns payments pod-security.kubernetes.io/warn=restricted').out[0], /warn \/ audit modes are explained, not modelled/);
});

test('harden-pod: 0/2 ready, FailedCreate lists the restricted checks; non-root without seccomp still fails; hardened → uid 10001 + Seccomp: 2; 6/6', () => {
  const s = session('harden-pod');
  assert.ok(s.run('kubectl get deployment payments-api -n payments').out.some(l => /^payments-api\s+0\/2/.test(l)));
  assert.equal(s.run('kubectl get pods -n payments').out[0], 'No resources found in payments namespace.');
  const ev = s.run('kubectl get events -n payments').out.join('\n');
  assert.match(ev, /Warning\s+FailedCreate\s+replicaset\/payments-api-7d9c6b8f5\s+Error creating: pods "payments-api-7d9c6b8f5-x2x4k" is forbidden: violates PodSecurity "restricted:latest": privileged/);
  assert.match(s.run('kubectl exec -n payments deploy/payments-api -- id').out[0], /no running pods/);
  s.run('kubectl apply -f payments-api-nonroot.yaml');
  const ev2 = s.run('kubectl describe rs -n payments').out.join('\n');
  assert.match(ev2, /violates PodSecurity "restricted:latest": seccompProfile \(pod or container "api" must set securityContext\.seccompProfile\.type to "RuntimeDefault" or "Localhost"\)$/m, 'only the seccomp check is left');
  assert.ok(s.run('cat payments-api-hardened.yaml').out.includes('          type: RuntimeDefault'));
  s.run('kubectl apply -f payments-api-hardened.yaml');
  assert.ok(s.run('kubectl get pods -n payments').out.slice(1).every(l => /1\/1\s+Running/.test(l)));
  assert.equal(s.run('kubectl exec -n payments deploy/payments-api -- id').out[0], 'uid=10001 gid=0(root) groups=0(root)');
  assert.deepEqual(s.run('kubectl exec -n payments deploy/payments-api -- grep Seccomp /proc/1/status').out, ['Seccomp:\t2', 'Seccomp_filters:\t1']);
  assert.equal(s.status().total, 6);
  assert.equal(s.status().done, true);
});

test('free play: no labels + privileged pod runs as root with every capability and no seccomp filter', () => {
  const s = session(null, { psaEnforce: false, podHardened: false, seccomp: false });
  assert.match(s.run('kubectl exec -n payments deploy/payments-api -- id').out[0], /^uid=0\(root\)/);
  assert.deepEqual(s.run('kubectl exec -n payments deploy/payments-api -- grep Seccomp /proc/1/status').out, ['Seccomp:\t0', 'Seccomp_filters:\t0']);
  assert.deepEqual(s.run('kubectl exec -n payments deploy/payments-api -- grep CapEff /proc/1/status').out, ['CapEff:\t000001ffffffffff']);
  assert.equal(s.derived().verdict, 'exposed');
});

test('default-deny: attacker 200 → deny-all times out both clients → allow-frontend re-opens frontend only; 6/6', () => {
  const s = session('default-deny');
  assert.equal(s.run('kubectl get networkpolicy -n payments').out[0], 'No resources found in payments namespace.');
  assert.equal(s.run(ATT).exit, 0);
  s.run('kubectl apply -f default-deny-ingress.yaml');
  const a = s.run(ATT);
  assert.equal(a.exit, 28, 'a NetworkPolicy drop is a timeout, not a reset');
  assert.equal(s.run(WEB).exit, 28, 'deny-all blocks the legitimate client too');
  s.run('kubectl apply -f allow-frontend.yaml');
  assert.equal(s.run(WEB).exit, 0);
  assert.equal(s.run(ATT).exit, 28, 'the attacker stays blocked');
  assert.ok(s.run('kubectl get networkpolicy -n payments').out.some(l => /^allow-frontend\s+app=payments-api/.test(l)));
  assert.equal(s.status().total, 6);
  assert.equal(s.status().done, true);
  s.run('kubectl delete networkpolicy default-deny-ingress -n payments');
  assert.equal(s.run(ATT).exit, 28, 'allow-frontend alone still selects (and isolates) the payments-api pods');
});

test('sa-least-privilege: can-i yes everywhere → find + delete the ClusterRoleBinding → Role + RoleBinding → secrets no, configmaps yes; 7/7', () => {
  const s = session('sa-least-privilege');
  const y = s.run('kubectl auth can-i get secrets -A --as ' + SA);
  assert.deepEqual([y.out[0], y.exit], ['yes', 0]);
  assert.ok(s.run('kubectl get secrets -A --as ' + SA).out.some(l => /^kube-system\s+bootstrap-token/.test(l)), 'the stolen token lists kube-system Secrets');
  assert.ok(s.run('kubectl get clusterrolebindings -o wide').out.some(l => /^api-sa-admin\s+ClusterRole\/cluster-admin\s+6d\s+payments\/api-sa$/.test(l)));
  s.run('kubectl delete clusterrolebinding api-sa-admin');
  assert.equal(s.state.rbacLeast, true);
  assert.equal(s.run('kubectl auth can-i list configmaps -n payments --as ' + SA).out[0], 'no', 'nothing granted yet');
  assert.match(s.run('kubectl create role config-reader -n payments --verb=get,list,watch --resource=secrets').out[0], /least privilege/);
  assert.match(s.run('kubectl create rolebinding x -n payments --role=config-reader --serviceaccount=api-sa').out[0], /must be <namespace>:<name>/);
  s.run('kubectl create role config-reader -n payments --verb=get,list,watch --resource=configmaps');
  s.run('kubectl create rolebinding api-sa-config-reader -n payments --role=config-reader --serviceaccount=payments:api-sa');
  const n = s.run('kubectl auth can-i get secrets -A --as ' + SA);
  assert.deepEqual([n.out[0], n.exit], ['no', 1]);
  assert.match(s.run('kubectl get secret db-creds -n payments --as ' + SA).out[0], /^Error from server \(Forbidden\): secrets is forbidden: User "system:serviceaccount:payments:api-sa" cannot get resource "secrets" in API group "" in the namespace "payments"$/);
  assert.equal(s.run('kubectl auth can-i list configmaps -n payments --as ' + SA).out[0], 'yes');
  assert.equal(s.run('kubectl auth can-i list configmaps -n frontend --as ' + SA).out[0], 'no', 'namespaced Role stays in payments');
  assert.equal(s.status().total, 7);
  assert.equal(s.status().done, true);
});

test('audit-log: commented --audit-log-path → no log file; sed -i un-comments it; Metadata event names who/what but never the data; 6/6', () => {
  const s = session('audit-log');
  const man = s.run('cat ' + MANIFEST).out;
  assert.ok(man.includes('    - --audit-policy-file=/etc/kubernetes/audit/policy.yaml'));
  assert.ok(man.includes('    # - --audit-log-path=/var/log/kubernetes/audit/audit.log'));
  assert.ok(man.includes('    - mountPath: /var/log/kubernetes/audit/'), 'the log directory is hostPath-mounted');
  assert.ok(s.run('cat /etc/kubernetes/audit/policy.yaml').out.includes('    resources: ["secrets", "configmaps"]'));
  s.run('kubectl get secret db-creds -n payments');
  const miss = s.run('tail -n 1 /var/log/kubernetes/audit/audit.log');
  assert.equal(miss.exit, 1);
  assert.match(miss.out[0], /No such file or directory/);
  assert.match(s.run("sed -i 's|--audit-log-path|# --audit-log-path|' " + MANIFEST).out[0], /invalid manifest/, 'a wrong edit is refused, not silently accepted');
  assert.equal(s.state.auditOn, false);
  assert.match(s.run("sed 's|# - --audit-log-path|- --audit-log-path|' " + MANIFEST).out[0], /without -i/);
  s.run("sed -i 's|# - --audit-log-path|- --audit-log-path|' " + MANIFEST);
  assert.equal(s.state.auditOn, true);
  assert.ok(s.run('cat ' + MANIFEST).out.includes('    - --audit-log-path=/var/log/kubernetes/audit/audit.log'));
  assert.ok(s.run('kubectl get pods -n kube-system -l component=kube-apiserver').out.some(l => /^kube-apiserver-controlplane\s+1\/1\s+Running\s+1\s+25s$/.test(l)), 'the static pod restarted once');
  assert.match(s.run('tail -n 1 /var/log/kubernetes/audit/audit.log').out[1], /no read of Secret db-creds has been recorded/, 'the read before the backend existed is gone for good');
  s.run('kubectl get secret db-creds -n payments');
  const hit = s.run('tail -n 1 /var/log/kubernetes/audit/audit.log');
  const evt = JSON.parse(hit.out[1]);
  assert.equal(evt.apiVersion, 'audit.k8s.io/v1');
  assert.equal(evt.level, 'Metadata');
  assert.equal(evt.verb, 'get');
  assert.equal(evt.user.username, 'kubernetes-admin');
  assert.deepEqual(evt.objectRef, { resource: 'secrets', namespace: 'payments', name: 'db-creds', apiVersion: 'v1' });
  assert.ok(!('requestObject' in evt) && !('responseObject' in evt) && !/czNjcjN0/.test(hit.out.join(' ')), 'Metadata level never carries the secret value');
  assert.equal(s.status().total, 6);
  assert.equal(s.status().done, true);
});

test('CKS paper: 6 official CKS domains, per-checkpoint mapping, one item per covered domain, Supply Chain honestly untested', () => {
  assert.equal(E.VERSION, '1.3.0');
  assert.deepEqual(E.CKS_BLUEPRINT.map(b => [b.domain, b.weight]), [['Cluster Setup', 15], ['Cluster Hardening', 15], ['System Hardening', 10],
    ['Minimize Microservice Vulnerabilities', 20], ['Supply Chain Security', 20], ['Monitoring, Logging & Runtime Security', 20]]);
  assert.equal(E.CKS_BLUEPRINT.reduce((n, b) => n + b.weight, 0), 100);
  for (const sc of S.get(SIM).scenarios.filter(x => x.predict)) assert.ok(E.cksDomain(SIM, sc.id), sc.id + ' maps to a CKS domain');
  assert.equal(E.cksDomain('rbac-authz', 'anything'), 'Cluster Hardening');
  assert.equal(E.cksDomain('etcd-quorum', 'lose-one'), null, 'CKA-only drills stay off the CKS paper');
  const cks = E.pool(S, 'CKS');
  assert.ok(cks.every(it => E.CKS_SIMS.includes(it.simId)));
  assert.equal(cks.filter(it => it.simId === SIM).length, 7);
  assert.ok(!E.pool(S).some(it => it.simId === SIM), 'the CKA paper never draws a CKS checkpoint');
  const ex = E.buildExam(S, { track: 'CKS', seed: 7 });
  assert.deepEqual([ex.track, ex.count, ex.minutes, ex.passPct], ['CKS', 8, 12, 67]);
  assert.equal(new Set(ex.items.map(i => i.domain)).size, 5, 'one item per covered domain first (5 of 6 have drills)');
  assert.match(ex.honesty, /not the CNCF CKS/);
  ex.items.forEach(it => { it.choice = it.answer; it.correct = true; });
  const sum = E.summarize(ex);
  assert.equal(sum.blueprint.track, 'CKS');
  assert.deepEqual(sum.blueprint.untested, ['Supply Chain Security']);
  assert.equal(sum.blueprint.coveragePct, 80);
  assert.equal(sum.blueprint.weightedPct, 100);
  assert.match(sum.blueprint.honesty, /Supply Chain Security has no drill yet/);
  /* a missed seccomp item makes System Hardening the gap and links to the CKS drill */
  const ex2 = E.buildExam(S, { track: 'CKS', seed: 7 });
  ex2.items.forEach(it => { const miss = it.domain === 'Minimize Microservice Vulnerabilities'; it.choice = miss ? (it.answer + 1) % 3 : it.answer; it.correct = !miss; });
  const bp = E.summarize(ex2).blueprint;
  assert.equal(bp.weakest.domain, 'Minimize Microservice Vulnerabilities');
  assert.deepEqual(bp.drill, { sim: SIM, href: '/immersive/#cks-pod-security' });
  /* default track unchanged */
  const cka = E.buildExam(S, { seed: 7 });
  assert.deepEqual([cka.track, cka.count, cka.minutes, cka.passPct], ['CKA', 10, 15, 66]);
  assert.equal(E.summarize(cka).blueprint.rows.length, 5);
});

test('review: CKS coach cards get an honest domain label; CKA mastery stays CKA-only', () => {
  assert.equal(R.VERSION, '1.3.1');
  const cards = R.cliCheckpoints(C, S).filter(c => c.simId === SIM);
  assert.equal(cards.length, 29);
  assert.ok(cards.every(c => c.domain === 'CKS · Workload security'));
  assert.ok(!R.checkpoints(S).some(c => c.simId === SIM), 'CKS predict checkpoints are graded on the CKS paper, not mixed into CKA readiness');
});

test('wiring: /immersive/ host, exam lobby CKS button, curriculum rows, manifest (new scene, cks_coverage, pack, honest notes)', () => {
  const html = readFileSync(path.join(root, 'docs/immersive/index.html'), 'utf8');
  assert.match(html, /id="cks-pod-security"/);
  assert.match(html, /data-il-sim="cks-pod-security"\s*\n\s*data-gltf="\/assets\/immersive\/cks-pod-security\.glb"/);
  assert.match(html, /The shell is simulated and runs on a rules engine: there is no live cluster, no real kubelet or kernel, and no clock/);
  assert.match(html, /Supply Chain Security \(20%\) has no drill yet/);
  const exam = readFileSync(path.join(root, 'docs/immersive/exam/index.html'), 'utf8');
  assert.match(exam, /data-il-exam-start data-track="CKS">CKS 8 · 12:00</);
  assert.match(exam, /data-il-exam-pool-cks/);
  const boot = readFileSync(path.join(root, 'docs/assets/il-immersive-exam-boot.js'), 'utf8');
  assert.match(boot, /getAttribute\('data-track'\)/);
  for (const f of ['labs.json', 'mirror.json']) {
    const j = JSON.parse(readFileSync(path.join(root, 'docs/curriculum-os', f), 'utf8'));
    const row = (j.items || j.labs).find(l => l.id === 'lab-sim-cks-pod-security');
    assert.ok(row, f);
    assert.equal(row.gltf, S.get(SIM).glb);
    assert.equal(row.immersive.sim, SIM);
    assert.match(row.summary, /no live cluster/);
  }
  const m = JSON.parse(readFileSync(path.join(root, 'docs/assets/scenes/manifest.json'), 'utf8'));
  const sc = m.scenes.find(x => x.sim === SIM);
  assert.equal(sc.gltf, S.get(SIM).glb);
  assert.equal(sc.cert, 'CKS');
  assert.equal(sc.polish, 'blender-cli');
  assert.ok(m.sims.list.includes(SIM));
  assert.ok(!m.cka_coverage.interactive.includes(SIM), 'not counted as CKA coverage');
  assert.deepEqual(m.cks_coverage.interactive, [SIM]);
  assert.equal(m.cks_coverage.hostedFleet, false);
  assert.equal(m.cks_coverage.liveUnrealHost, false);
  assert.ok(m.cks_coverage.notCovered.some(x => /^Supply Chain Security/.test(x)));
  assert.equal(m.sims.runtime_version, S.VERSION);
  assert.equal(m.sims.exam.version, E.VERSION);
  assert.equal(m.sims.exam.cks.defaults.passPct, 67);
  assert.deepEqual(m.sims.cli.packs.find(p => p.sim === SIM).tasks, ['psa-enforce', 'harden-pod', 'default-deny', 'sa-least-privilege', 'audit-log']);
  assert.match(m.sims.cli.cksNote, /No live cluster, no real kubelet, kernel or seccomp, no clock/);
});

test('voice: "sec comp" and "dry run" normalise to real syntax', () => {
  assert.match(C.fromSpeech('kubectl exec dash n payments deploy slash payments-api dash dash grep sec comp slash proc slash 1 slash status', SIM).line || '', /seccomp/i);
  assert.match(C.fromSpeech('kubectl label dash dash dry run equals server ns payments', SIM).line || '', /dry-run/);
});
